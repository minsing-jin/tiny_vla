from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from vla.backend.base import Backend
from vla.core.types import AtomicAction
from vla.eval.rollout import run_rollout
from vla.policy.baseline import BaselinePolicy


class DummyBackend(Backend):
    def __init__(self) -> None:
        self._t = 2000.0

    def capture_frame(self) -> np.ndarray:
        return np.zeros((64, 64, 3), dtype=np.uint8)

    def get_cursor(self) -> tuple[int, int]:
        return (8, 8)

    def get_window_meta(self) -> dict:
        return {"x": 0, "y": 0, "w": 64, "h": 64, "dpi_scale": 1.0}

    def send_action(self, action: AtomicAction) -> None:
        return None

    def sleep(self, dt: float) -> None:
        self._t += max(0.0, dt)

    def time(self) -> float:
        self._t += 0.02
        return self._t


def main() -> int:
    cmd_path = Path("commands_loop_rollout.jsonl")
    row = {
        "cmd_id": "r1",
        "skill": "CLICK_UI",
        "hint": {"roi_bbox": [0, 0, 10, 10]},
        "constraints": {},
        "guard": {"type": "NOOP"},
        "budget": {"max_steps": 2, "max_seconds": 0.2, "max_retries": 1},
    }
    cmd_path.write_text(json.dumps(row) + "\n", encoding="utf-8")

    out = Path("runs/loop_rollout_out")
    summary = run_rollout(DummyBackend(), BaselinePolicy(), f"file:{cmd_path}", out)
    assert "p50_policy_infer_ms" in summary
    assert "p95_policy_infer_ms" in summary
    assert (out / "status.jsonl").exists()
    assert Path("failure_packs/pack_r1").exists()
    print("check_rollout_failure: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
