from __future__ import annotations

import json
from pathlib import Path
import sys

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from vla.core.io_jsonl import write_jsonl
from vla.record.segment import build_dataset_from_runs


def main() -> int:
    run = Path("runs/loop_dataset_src")
    (run / "frames").mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(run / "frames/000001.png"), np.zeros((32, 32, 3), dtype=np.uint8))

    write_jsonl(run / "obs.jsonl", [{"t": 1.0, "frame_path": "frames/000001.png", "cursor": [1, 2], "window": {}}])
    write_jsonl(run / "actions.jsonl", [{"t": 1.05, "type": "CLICK", "x": 3, "y": 4, "button": "LEFT"}])
    write_jsonl(
        run / "tags.jsonl",
        [
            {"t": 1.01, "event": "CMD_START", "cmd_id": "d1", "skill": "CLICK_UI"},
            {"t": 1.06, "event": "CMD_END", "cmd_id": "d1"},
        ],
    )

    out = Path("datasets/loop_dataset_out")
    build_dataset_from_runs([run], out)
    m = json.loads((out / "dataset_manifest.json").read_text(encoding="utf-8"))
    assert m["episodes"] >= 1
    assert m["steps"] >= 1
    print("check_build_dataset: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
