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
from vla.train.export import export_onnx
from vla.train.train_bc import train_bc


def main() -> int:
    ds = Path("datasets/loop_train_ds/episodes/ep_000001")
    frames = Path("datasets/loop_train_frames")
    ds.mkdir(parents=True, exist_ok=True)
    frames.mkdir(parents=True, exist_ok=True)

    frame = frames / "000001.png"
    cv2.imwrite(str(frame), np.zeros((256, 256, 3), dtype=np.uint8))

    cmd = {
        "cmd_id": "t1",
        "skill": "CLICK_UI",
        "hint": {"roi_bbox": [0, 0, 10, 10]},
        "constraints": {},
        "guard": {"type": "NOOP"},
        "budget": {"max_steps": 1, "max_seconds": 1, "max_retries": 1},
    }
    (ds / "cmd.json").write_text(json.dumps(cmd), encoding="utf-8")
    write_jsonl(
        ds / "steps.jsonl",
        [
            {
                "obs": {"t": 1.0, "frame_path": "frames/000001.png", "cursor": [0, 0], "window": {}},
                "teacher_action": {"t": 1.1, "type": "CLICK", "x": 1, "y": 2, "button": "LEFT"},
                "frame_abs": str(frame.resolve()),
            }
        ],
    )

    out = Path("runs/loop_train_out")
    train_bc("datasets/loop_train_ds", out, epochs=1, batch_size=1, lr=1e-3)
    assert (out / "model.pt").exists()
    assert (out / "metrics.jsonl").exists()

    onnx_path = out / "model.onnx"
    try:
        export_onnx(out / "model.pt", onnx_path)
        assert onnx_path.exists()
    except Exception as e:
        # MVP allows export placeholder behavior in environments without onnx.
        if "onnx" not in str(e).lower():
            raise
    print("check_train_export: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
