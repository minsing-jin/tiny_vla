from __future__ import annotations

import json
from pathlib import Path

import cv2

from vla.backend.base import Backend
from vla.core.io_jsonl import append_jsonl


def _start_listeners(actions_path: Path):
    listeners = []
    try:
        from pynput import keyboard, mouse
    except Exception:
        return listeners

    def on_click(x, y, button, pressed):
        if not pressed:
            append_jsonl(actions_path, {"t": __import__("time").time(), "type": "CLICK", "x": int(x), "y": int(y), "button": str(button).split(".")[-1].upper()})

    def on_scroll(x, y, dx, dy):
        append_jsonl(actions_path, {"t": __import__("time").time(), "type": "SCROLL", "x": int(x), "y": int(y), "dx": int(dx), "dy": int(dy)})

    def on_press(key):
        k = getattr(key, "char", None) or str(key).replace("Key.", "")
        append_jsonl(actions_path, {"t": __import__("time").time(), "type": "KEY", "key": k, "down": True})

    m_listener = mouse.Listener(on_click=on_click, on_scroll=on_scroll)
    k_listener = keyboard.Listener(on_press=on_press)
    m_listener.start()
    k_listener.start()
    listeners.extend([m_listener, k_listener])
    return listeners


def record_run(backend: Backend, out_dir: str | Path, duration: float = 60.0, fps: int = 10, capture_inputs: bool = True) -> Path:
    out = Path(out_dir)
    frames_dir = out / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "duration": duration,
        "fps": fps,
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    obs_path = out / "obs.jsonl"
    actions_path = out / "actions.jsonl"
    tags_path = out / "tags.jsonl"
    tags_path.touch()

    listeners = _start_listeners(actions_path) if capture_inputs else []

    dt = 1.0 / max(1, fps)
    t0 = backend.time()
    idx = 0

    while backend.time() - t0 <= duration:
        frame = backend.capture_frame()
        idx += 1
        frame_name = f"{idx:06d}.png"
        frame_path = frames_dir / frame_name
        cv2.imwrite(str(frame_path), frame[:, :, ::-1])

        cursor = list(backend.get_cursor())
        window = backend.get_window_meta()
        append_jsonl(obs_path, {"t": backend.time(), "frame_path": str(Path("frames") / frame_name), "cursor": cursor, "window": window})
        backend.sleep(dt)

    for l in listeners:
        l.stop()

    return out
