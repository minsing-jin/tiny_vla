from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from vla.dagger.merge import merge_corrections


def main() -> int:
    ep = Path("datasets/loop_dagger_ds/episodes/ep_000001")
    ep.mkdir(parents=True, exist_ok=True)

    cmd = {"cmd_id": "g1", "skill": "CLICK_UI", "hint": {}, "constraints": {}, "guard": {"type": "NOOP"}, "budget": {}}
    (ep / "cmd.json").write_text(json.dumps(cmd), encoding="utf-8")
    (ep / "steps.jsonl").write_text(
        json.dumps({"obs": {"t": 1.0, "frame_path": "frames/1.png", "cursor": [0, 0], "window": {}}, "teacher_action": {"type": "CLICK", "x": 1, "y": 1}})
        + "\n",
        encoding="utf-8",
    )

    corr = Path("corrections_loop.jsonl")
    corr.write_text(json.dumps({"cmd_id": "g1", "step_idx": 0, "corrected_action": {"type": "CLICK", "x": 9, "y": 9}}) + "\n", encoding="utf-8")

    out = Path("datasets/loop_dagger_ds_v2")
    merge_corrections("datasets/loop_dagger_ds", corr, out)

    line = (out / "episodes/ep_000001/steps.jsonl").read_text(encoding="utf-8").strip()
    row = json.loads(line)
    assert row["teacher_action"]["x"] == 9
    assert row["teacher_action"]["y"] == 9
    print("check_dagger_merge: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
