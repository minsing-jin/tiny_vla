from __future__ import annotations

from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from vla.backend.base import Backend
from vla.core.types import AtomicAction
from vla.record.recorder import record_run
from vla.replay.replayer import load_run_streams


class DummyBackend(Backend):
    def __init__(self) -> None:
        self._t = 1000.0

    def capture_frame(self) -> np.ndarray:
        return np.zeros((48, 64, 3), dtype=np.uint8)

    def get_cursor(self) -> tuple[int, int]:
        return (10, 20)

    def get_window_meta(self) -> dict:
        return {"x": 0, "y": 0, "w": 64, "h": 48, "dpi_scale": 1.0}

    def send_action(self, action: AtomicAction) -> None:
        return None

    def sleep(self, dt: float) -> None:
        self._t += max(0.0, dt)

    def time(self) -> float:
        self._t += 0.01
        return self._t


def main() -> int:
    out = Path("runs/loop_record_smoke")
    backend = DummyBackend()
    record_run(backend, out, duration=0.25, fps=5, capture_inputs=False)
    assert (out / "manifest.json").exists()
    assert (out / "obs.jsonl").exists()
    # In no-input mode, actions stream can be absent/empty.
    if (out / "actions.jsonl").exists():
        assert (out / "actions.jsonl").is_file()
    assert (out / "tags.jsonl").exists()

    obs, actions = load_run_streams(out)
    assert len(obs) >= 1
    assert isinstance(actions, list)
    print("check_backend_record_replay: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
