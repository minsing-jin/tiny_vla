from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from vla.core.types import AtomicAction, Command, Observation, Status


def run_help(cmd: list[str]) -> None:
    p = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if p.returncode != 0:
        raise RuntimeError(f"command failed: {' '.join(cmd)}\n{p.stderr}\n{p.stdout}")


def main() -> int:
    c = Command(cmd_id="c1", skill="CLICK_UI")
    assert Command.from_dict(c.to_dict()).cmd_id == "c1"

    s = Status(cmd_id="c1", status="SUCCESS", info={"attempts": 1})
    assert Status.from_dict(s.to_dict()).status == "SUCCESS"

    a = AtomicAction(t=1.0, type="CLICK", x=1, y=2, button="LEFT")
    assert AtomicAction.from_dict(a.to_dict()).button == "LEFT"

    o = Observation(t=1.0, frame_path="f.png", cursor=[0, 0], window={})
    assert Observation.from_dict(o.to_dict()).frame_path == "f.png"

    commands = [
        [sys.executable, "-m", "scripts.vla_cli", "--help"],
        [sys.executable, "-m", "scripts.vla_cli", "record", "--help"],
        [sys.executable, "-m", "scripts.vla_cli", "replay", "--help"],
        [sys.executable, "-m", "scripts.vla_cli", "build-dataset", "--help"],
        [sys.executable, "-m", "scripts.vla_cli", "train", "--help"],
        [sys.executable, "-m", "scripts.vla_cli", "rollout", "--help"],
        [sys.executable, "-m", "scripts.vla_cli", "dagger", "collect", "--help"],
        [sys.executable, "-m", "scripts.vla_cli", "dagger", "merge", "--help"],
        [sys.executable, "-m", "scripts.vla_cli", "export", "--help"],
    ]
    for cmd in commands:
        run_help(cmd)

    print("check_core_cli: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
