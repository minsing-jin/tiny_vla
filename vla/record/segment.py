from __future__ import annotations

import json
from pathlib import Path

from vla.core.clock import match_observation_to_action
from vla.core.io_jsonl import read_jsonl, write_jsonl


MOVE_TYPES = {"MOVE", "MOVE_TO"}


def _collect_cmd_windows(tags: list[dict]) -> dict[str, dict]:
    data = {}
    for ev in tags:
        cmd_id = ev.get("cmd_id")
        if not cmd_id:
            continue
        data.setdefault(cmd_id, {"start": None, "end": None, "skill": None, "hint": {}})
        if ev.get("event") == "CMD_START":
            data[cmd_id]["start"] = ev.get("t")
            data[cmd_id]["skill"] = ev.get("skill", "CLICK_UI")
        elif ev.get("event") == "CMD_END":
            data[cmd_id]["end"] = ev.get("t")
        elif ev.get("event") == "SET_ROI":
            data[cmd_id]["hint"]["roi_bbox"] = ev.get("roi_bbox")
        elif ev.get("event") == "CAPTURE_REF_PATCH":
            data[cmd_id]["hint"]["ref_patch_path"] = ev.get("path")
        elif ev.get("event") == "SET_TEXT":
            data[cmd_id]["hint"]["text"] = ev.get("text", "")
    return data


def build_dataset_from_runs(runs: list[Path], out_dir: Path, align_tolerance_sec: float = 0.1, drop_unaligned: bool = True, include_move_events: bool = True) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    ep_root = out_dir / "episodes"
    ep_root.mkdir(exist_ok=True)

    ep_count = 0
    total_steps = 0
    for run in runs:
        obs = list(read_jsonl(run / "obs.jsonl"))
        actions = list(read_jsonl(run / "actions.jsonl"))
        tags = list(read_jsonl(run / "tags.jsonl"))
        windows = _collect_cmd_windows(tags)
        obs_ts = [o["t"] for o in obs]

        for cmd_id, meta in windows.items():
            st, et = meta.get("start"), meta.get("end")
            if st is None or et is None:
                continue
            cmd_actions = [a for a in actions if st <= a.get("t", 0) <= et]
            if not include_move_events:
                cmd_actions = [a for a in cmd_actions if a.get("type") not in MOVE_TYPES]

            steps = []
            for a in cmd_actions:
                idx = match_observation_to_action(obs_ts, action_t=float(a["t"]), tolerance=align_tolerance_sec)
                if idx is None:
                    if drop_unaligned:
                        continue
                    step = {"obs": None, "teacher_action": a}
                else:
                    o = obs[idx]
                    frame_rel = o["frame_path"]
                    step = {
                        "obs": o,
                        "teacher_action": a,
                        "frame_abs": str((run / frame_rel).resolve()),
                    }
                steps.append(step)

            if not steps:
                continue

            ep_count += 1
            ep_dir = ep_root / f"ep_{ep_count:06d}"
            ep_dir.mkdir(parents=True, exist_ok=True)
            cmd = {
                "cmd_id": cmd_id,
                "skill": meta.get("skill", "CLICK_UI"),
                "hint": meta.get("hint", {}),
                "constraints": {},
                "guard": {"type": "NOOP"},
                "budget": {"max_steps": 30, "max_seconds": 2.0, "max_retries": 3},
            }
            (ep_dir / "cmd.json").write_text(json.dumps(cmd, indent=2), encoding="utf-8")
            write_jsonl(ep_dir / "steps.jsonl", steps)
            total_steps += len(steps)

    manifest = {"episodes": ep_count, "steps": total_steps}
    (out_dir / "dataset_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return out_dir
