from __future__ import annotations

import json
import time
from pathlib import Path

import cv2
import numpy as np

from vla.command.source import iter_commands
from vla.core.io_jsonl import append_jsonl
from vla.core.types import Observation, Status
from vla.eval.failure_pack import make_failure_pack
from vla.eval.metrics import summarize_rollout


def _crop(frame: np.ndarray, roi):
    if not roi:
        return frame
    x1, y1, x2, y2 = roi
    h, w = frame.shape[:2]
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w, x2), min(h, y2)
    if x2 <= x1 or y2 <= y1:
        return frame
    return frame[y1:y2, x1:x2]


def _guard_ok(guard: dict, prev_frame: np.ndarray, cur_frame: np.ndarray) -> bool:
    gtype = guard.get("type", "NOOP")
    if gtype == "NOOP":
        return False
    roi = guard.get("roi_bbox")
    a = _crop(prev_frame, roi)
    b = _crop(cur_frame, roi)
    if gtype == "VISUAL_CHANGE":
        if a.size == 0 or b.size == 0:
            return False
        diff = np.mean(np.abs(a.astype(np.float32) - b.astype(np.float32))) / 255.0
        return diff > float(guard.get("threshold", 0.08))
    if gtype == "TEMPLATE_MATCH":
        tpath = guard.get("template_path")
        if not tpath:
            return False
        tpl = cv2.imread(str(tpath))
        if tpl is None or b.size == 0:
            return False
        if b.shape[0] < tpl.shape[0] or b.shape[1] < tpl.shape[1]:
            return False
        score = cv2.matchTemplate(b, tpl, cv2.TM_CCOEFF_NORMED).max()
        return float(score) >= float(guard.get("threshold", 0.8))
    return False


def run_rollout(backend, policy, command_source: str, out_dir: str | Path) -> dict:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    step_latencies = []
    statuses = []

    for cmd in iter_commands(command_source):
        start = backend.time()
        max_steps = int(cmd.budget.get("max_steps", 30))
        max_seconds = float(cmd.budget.get("max_seconds", 2.0))
        obs_rows = []
        action_rows = []

        prev_frame = backend.capture_frame()
        final_status = "TIMEOUT"
        reason = "budget_exceeded"

        for step_idx in range(max_steps):
            if backend.time() - start > max_seconds:
                final_status = "TIMEOUT"
                reason = "budget_seconds"
                break

            t0 = time.perf_counter()
            frame = backend.capture_frame()
            capture_ms = (time.perf_counter() - t0) * 1000.0

            ts = backend.time()
            frame_name = f"{cmd.cmd_id}_{step_idx:04d}.png"
            frame_path = out / frame_name
            cv2.imwrite(str(frame_path), frame[:, :, ::-1])
            cursor = list(backend.get_cursor())
            obs = Observation(t=ts, frame_path=frame_name, cursor=cursor, window=backend.get_window_meta())
            obs_row = obs.to_dict()
            obs_row["frame_abs"] = str(frame_path.resolve())
            append_jsonl(out / "obs.jsonl", obs_row)
            obs_rows.append(obs_row)

            t1 = time.perf_counter()
            action = policy.act(obs, cmd)
            infer_ms = (time.perf_counter() - t1) * 1000.0

            t2 = time.perf_counter()
            backend.send_action(action)
            inject_ms = (time.perf_counter() - t2) * 1000.0

            t3 = time.perf_counter()
            now_frame = backend.capture_frame()
            ok = _guard_ok(cmd.guard.to_dict() if hasattr(cmd.guard, "to_dict") else dict(cmd.guard), prev_frame, now_frame)
            guard_ms = (time.perf_counter() - t3) * 1000.0
            prev_frame = now_frame

            arow = action.to_dict()
            append_jsonl(out / "actions.jsonl", arow)
            action_rows.append(arow)

            lat = {
                "cmd_id": cmd.cmd_id,
                "step_idx": step_idx,
                "capture_ms": capture_ms,
                "policy_infer_ms": infer_ms,
                "inject_ms": inject_ms,
                "guard_ms": guard_ms,
            }
            append_jsonl(out / "latency.jsonl", lat)
            step_latencies.append(lat)

            if ok:
                final_status = "SUCCESS"
                reason = "guard_triggered"
                break

        if final_status != "SUCCESS":
            final_status = "NEED_HELP" if reason not in {"budget_seconds"} else "TIMEOUT"

        st = Status(
            cmd_id=cmd.cmd_id,
            status=final_status,
            info={
                "attempts": len(action_rows),
                "last_action": action_rows[-1] if action_rows else None,
                "reason": reason,
                "confidence": 0.5,
            },
        )
        srow = st.to_dict()
        append_jsonl(out / "status.jsonl", srow)
        statuses.append(final_status)

        if final_status in {"FAIL", "NEED_HELP", "TIMEOUT"}:
            make_failure_pack(out, cmd.to_dict(), srow, obs_rows, action_rows)

    summary = summarize_rollout(step_latencies, statuses)
    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary
