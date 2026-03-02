from __future__ import annotations

import time as _time

import numpy as np

from vla.backend.base import Backend
from vla.core.types import AtomicAction


class LocalCaptureOnlyBackend(Backend):
    def __init__(self) -> None:
        try:
            import mss
            import pyautogui
        except Exception as e:
            raise RuntimeError("capture-only backend requires mss and pyautogui") from e
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
        return None

    def sleep(self, dt: float) -> None:
        _time.sleep(max(0.0, dt))

    def time(self) -> float:
        return _time.time()
