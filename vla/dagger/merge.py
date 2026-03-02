from __future__ import annotations

import json
import shutil
from pathlib import Path


def merge_corrections(dataset_dir: str | Path, corrections_path: str | Path, out_dir: str | Path) -> Path:
    src = Path(dataset_dir)
    out = Path(out_dir)
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(src, out)

    corrections = [json.loads(x) for x in Path(corrections_path).read_text(encoding="utf-8").splitlines() if x.strip()]
    by_cmd = {c["cmd_id"]: c for c in corrections}

    for ep in sorted((out / "episodes").glob("ep_*")):
        cmd = json.loads((ep / "cmd.json").read_text(encoding="utf-8"))
        c = by_cmd.get(cmd.get("cmd_id"))
        if not c:
            continue
        steps = [json.loads(x) for x in (ep / "steps.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
        idx = int(c["step_idx"])
        if 0 <= idx < len(steps):
            steps[idx]["teacher_action"] = c["corrected_action"]
            with (ep / "steps.jsonl").open("w", encoding="utf-8") as f:
                for s in steps:
                    f.write(json.dumps(s) + "\n")
    return out
