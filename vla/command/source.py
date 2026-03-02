from __future__ import annotations

import json
from pathlib import Path
from typing import Iterator

from vla.core.io_jsonl import read_jsonl
from vla.core.types import Command


def iter_commands(command_source: str) -> Iterator[Command]:
    if command_source.startswith("file:"):
        path = Path(command_source.split(":", 1)[1])
        for row in read_jsonl(path):
            yield Command.from_dict(row)
    elif command_source == "stdin":
        while True:
            line = input().strip()
            if not line:
                continue
            yield Command.from_dict(json.loads(line))
    elif command_source.startswith("ws://") or command_source.startswith("http://") or command_source.startswith("https://"):
        raise NotImplementedError("network command source placeholder in MVP")
    else:
        raise ValueError(f"unsupported command_source: {command_source}")
