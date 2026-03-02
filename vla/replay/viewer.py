from __future__ import annotations

from pathlib import Path

import cv2

from vla.core.io_jsonl import read_jsonl


def view_run(run_dir: str | Path, wait_ms: int = 30) -> None:
    run = Path(run_dir)
    for obs in read_jsonl(run / "obs.jsonl"):
        img = cv2.imread(str(run / obs["frame_path"]))
        if img is None:
            continue
        cv2.imshow("vla_replay", img)
        if cv2.waitKey(wait_ms) & 0xFF == ord("q"):
            break
    cv2.destroyAllWindows()
