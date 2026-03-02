from pathlib import Path

from vla.core.io_jsonl import write_jsonl
from vla.replay.replayer import load_run_streams


def test_replay_load(tmp_path: Path):
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    write_jsonl(run_dir / "obs.jsonl", [{"t": 1.0, "frame_path": "a.png", "cursor": [0, 0], "window": {}}])
    write_jsonl(run_dir / "actions.jsonl", [{"t": 1.01, "type": "CLICK", "x": 1, "y": 2}])
    obs, actions = load_run_streams(run_dir)
    assert len(obs) == 1
    assert len(actions) == 1
