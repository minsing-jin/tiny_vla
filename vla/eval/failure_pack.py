from __future__ import annotations

import json
import shutil
from pathlib import Path


def make_failure_pack(base_out: Path, cmd: dict, status: dict, obs_rows: list[dict], action_rows: list[dict]) -> Path:
    pack_root = Path("failure_packs")
    pack_root.mkdir(exist_ok=True)
    pack = pack_root / f"pack_{cmd['cmd_id']}"
    if pack.exists():
        shutil.rmtree(pack)
    pack.mkdir(parents=True)
    frames_dir = pack / "frames"
    frames_dir.mkdir(exist_ok=True)

    for o in obs_rows:
        fp = Path(o["frame_abs"]) if o.get("frame_abs") else None
        if fp and fp.exists():
            shutil.copy2(fp, frames_dir / fp.name)

    with (pack / "cmd.json").open("w", encoding="utf-8") as f:
        json.dump(cmd, f, indent=2)
    with (pack / "status.json").open("w", encoding="utf-8") as f:
        json.dump(status, f, indent=2)
    with (pack / "obs.jsonl").open("w", encoding="utf-8") as f:
        for o in obs_rows:
            f.write(json.dumps(o) + "\n")
    with (pack / "actions.jsonl").open("w", encoding="utf-8") as f:
        for a in action_rows:
            f.write(json.dumps(a) + "\n")
    return pack
