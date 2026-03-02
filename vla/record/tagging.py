from __future__ import annotations

import uuid
from pathlib import Path

import cv2

from vla.core.io_jsonl import append_jsonl


def _latest_frame(run_dir: Path):
    frames = sorted((run_dir / "frames").glob("*.png"))
    return frames[-1] if frames else None


def _select_roi(image_path: Path):
    img = cv2.imread(str(image_path))
    if img is None:
        return None
    x, y, w, h = cv2.selectROI("select_roi", img, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow("select_roi")
    if w <= 0 or h <= 0:
        return None
    return [int(x), int(y), int(x + w), int(y + h)]


def interactive_tagging(run_dir: str | Path) -> None:
    run = Path(run_dir)
    tags = run / "tags.jsonl"
    ref_dir = run / "ref_patches"
    ref_dir.mkdir(exist_ok=True)

    current_cmd = None
    print("Tagging commands. Actions: start, end, roi, ref, text, quit")
    while True:
        cmd = input("tag> ").strip().lower()
        t = __import__("time").time()
        if cmd == "start":
            skill = input("skill: ").strip() or "CLICK_UI"
            current_cmd = str(uuid.uuid4())
            append_jsonl(tags, {"t": t, "event": "CMD_START", "cmd_id": current_cmd, "skill": skill})
            print(f"started {current_cmd}")
        elif cmd == "end":
            if current_cmd:
                append_jsonl(tags, {"t": t, "event": "CMD_END", "cmd_id": current_cmd})
                print(f"ended {current_cmd}")
                current_cmd = None
        elif cmd == "roi":
            if not current_cmd:
                print("start command first")
                continue
            lf = _latest_frame(run)
            if not lf:
                print("no frame")
                continue
            roi = _select_roi(lf)
            if roi:
                append_jsonl(tags, {"t": t, "event": "SET_ROI", "cmd_id": current_cmd, "roi_bbox": roi})
        elif cmd == "ref":
            if not current_cmd:
                print("start command first")
                continue
            lf = _latest_frame(run)
            if not lf:
                print("no frame")
                continue
            roi = _select_roi(lf)
            if not roi:
                continue
            img = cv2.imread(str(lf))
            x1, y1, x2, y2 = roi
            patch = img[y1:y2, x1:x2]
            path = ref_dir / f"{current_cmd}.png"
            cv2.imwrite(str(path), patch)
            append_jsonl(tags, {"t": t, "event": "CAPTURE_REF_PATCH", "cmd_id": current_cmd, "path": str(path.relative_to(run))})
        elif cmd == "text":
            if not current_cmd:
                print("start command first")
                continue
            text = input("hint text: ").strip()
            append_jsonl(tags, {"t": t, "event": "SET_TEXT", "cmd_id": current_cmd, "text": text})
        elif cmd == "quit":
            break
