from __future__ import annotations

import json
from pathlib import Path

from vla.dagger.ui import ClickCollector


def collect_corrections(pack_dir: str | Path, out_path: str | Path) -> Path:
    pack = Path(pack_dir)
    obs = [json.loads(x) for x in (pack / "obs.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    cmd = json.loads((pack / "cmd.json").read_text(encoding="utf-8"))

    if not obs:
        raise RuntimeError("empty failure pack obs")

    target = obs[-1]
    img_path = target.get("frame_abs")
    if not img_path or not Path(img_path).exists():
        frames = sorted((pack / "frames").glob("*.png"))
        if not frames:
            raise RuntimeError("no image for correction")
        img_path = str(frames[-1])

    cc = ClickCollector()
    point = cc.collect_point(img_path)
    if point is None:
        raise RuntimeError("no correction selected")

    action_type = input("action_type (default CLICK): ").strip() or "CLICK"
    row = {
        "cmd_id": cmd["cmd_id"],
        "step_idx": len(obs) - 1,
        "corrected_action": {"type": action_type, "x": int(point[0]), "y": int(point[1])},
    }
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")
    return out
