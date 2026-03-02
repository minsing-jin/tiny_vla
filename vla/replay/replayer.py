from __future__ import annotations

from pathlib import Path

from vla.backend.base import Backend
from vla.core.io_jsonl import read_jsonl


def load_run_streams(run_dir: str | Path):
    run = Path(run_dir)
    obs = list(read_jsonl(run / "obs.jsonl"))
    actions = list(read_jsonl(run / "actions.jsonl"))
    return obs, actions


def replay_actions(run_dir: str | Path, backend: Backend | None = None, speed: float = 1.0) -> None:
    _, actions = load_run_streams(run_dir)
    if not actions:
        return
    t0 = actions[0]["t"]
    for i, a in enumerate(actions):
        if backend is not None:
            from vla.core.types import AtomicAction

            backend.send_action(AtomicAction.from_dict(a))
        if i + 1 < len(actions):
            dt = (actions[i + 1]["t"] - a["t"]) / max(speed, 1e-6)
            if backend is not None:
                backend.sleep(max(0.0, dt))
