from pathlib import Path

from vla.core.io_jsonl import read_jsonl, write_jsonl


def test_jsonl_roundtrip(tmp_path: Path):
    path = tmp_path / "a.jsonl"
    rows = [{"a": 1}, {"b": 2}]
    write_jsonl(path, rows)
    out = list(read_jsonl(path))
    assert out == rows
