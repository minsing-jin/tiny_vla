from __future__ import annotations

import time as _time

import numpy as np

from vla.backend.base import Backend
from vla.core.types import AtomicAction


class LocalMacOSBackend(Backend):
    def __init__(self) -> None:
        try:
            import mss
            import pyautogui
        except Exception as e:
            raise RuntimeError(
                "local backend requires mss and pyautogui. On macOS, also grant Accessibility and Screen Recording permissions."
            ) from e
        self._mss = mss.mss()
        self._pyautogui = pyautogui

    def capture_frame(self) -> np.ndarray:
        monitor = self._mss.monitors[1]
        shot = self._mss.grab(monitor)
        arr = np.array(shot)[:, :, :3]
        return arr[:, :, ::-1]

    def get_cursor(self) -> tuple[int, int]:
        x, y = self._pyautogui.position()
        return int(x), int(y)

    def get_window_meta(self) -> dict:
        w, h = self._pyautogui.size()
        return {"x": 0, "y": 0, "w": int(w), "h": int(h), "dpi_scale": 1.0}

    def send_action(self, action: AtomicAction) -> None:
        p = self._pyautogui
        if action.type == "MOVE_TO" and action.x is not None and action.y is not None:
            p.moveTo(action.x, action.y)
        elif action.type == "CLICK":
            btn = (action.button or "LEFT").lower()
            if action.x is not None and action.y is not None:
                p.click(x=action.x, y=action.y, button=btn)
            else:
                p.click(button=btn)
        elif action.type == "DOUBLE_CLICK":
            btn = (action.button or "LEFT").lower()
            p.doubleClick(x=action.x, y=action.y, button=btn)
        elif action.type == "RIGHT_CLICK":
            p.rightClick(x=action.x, y=action.y)
        elif action.type == "KEY" and action.key:
            if action.down is False:
                p.keyUp(action.key)
            elif action.down is True:
                p.keyDown(action.key)
            else:
                p.press(action.key)
        elif action.type == "HOTKEY" and action.text:
            keys = [k.strip() for k in action.text.split("+") if k.strip()]
            if keys:
                p.hotkey(*keys)
        elif action.type == "TYPE_TEXT" and action.text is not None:
            p.write(action.text)
        elif action.type == "SCROLL":
            p.scroll(int(action.dy or 0))

    def sleep(self, dt: float) -> None:
        _time.sleep(max(0.0, dt))

    def time(self) -> float:
        return _time.time()
