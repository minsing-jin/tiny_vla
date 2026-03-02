from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np


SKILL_TO_ID = {
    "CLICK_UI": 0,
    "DOUBLE_CLICK_UI": 1,
    "RIGHT_CLICK_UI": 2,
    "DRAG_UI": 3,
    "SCROLL_ROI": 4,
    "PRESS_KEY": 5,
    "PRESS_HOTKEY": 6,
    "TYPE_TEXT": 7,
    "SELECT_FROM_LIST": 8,
    "RECOVER_BACK": 9,
}

ACTION_TO_ID = {
    "MOVE_TO": 0,
    "CLICK": 1,
    "DOUBLE_CLICK": 2,
    "RIGHT_CLICK": 3,
    "KEY": 4,
    "HOTKEY": 5,
    "TYPE_TEXT": 6,
    "SCROLL": 7,
}


class EpisodeDataset:
    def __init__(self, dataset_dir: str | Path):
        self.dataset_dir = Path(dataset_dir)
        self.samples = []
        for ep in sorted((self.dataset_dir / "episodes").glob("ep_*")):
            cmd = json.loads((ep / "cmd.json").read_text(encoding="utf-8"))
            with (ep / "steps.jsonl").open("r", encoding="utf-8") as f:
                for line in f:
                    row = json.loads(line)
                    if row.get("obs") is None:
                        continue
                    frame_abs = row.get("frame_abs")
                    self.samples.append((cmd, row, frame_abs))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, i):
        cmd, row, frame_abs = self.samples[i]
        if frame_abs and Path(frame_abs).exists():
            img = cv2.imread(frame_abs)
        else:
            frame_rel = row["obs"]["frame_path"]
            src_run_frame = self.dataset_dir / frame_rel
            img = cv2.imread(str(src_run_frame)) if src_run_frame.exists() else None
        if img is None:
            img = np.zeros((256, 256, 3), dtype=np.uint8)
        img = cv2.resize(img, (256, 256))
        img = img.astype(np.float32) / 255.0
        skill_id = SKILL_TO_ID.get(cmd.get("skill", "CLICK_UI"), 0)
        roi = cmd.get("hint", {}).get("roi_bbox", [0, 0, 256, 256])
        act = row["teacher_action"]
        action_id = ACTION_TO_ID.get(act.get("type", "MOVE_TO"), 0)
        xy = np.array([float(act.get("x", 0) or 0), float(act.get("y", 0) or 0)], dtype=np.float32)
        return img.transpose(2, 0, 1), skill_id, np.array(roi, dtype=np.float32), action_id, xy
