from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np

from vla.core.types import AtomicAction


class Backend(ABC):
    @abstractmethod
    def capture_frame(self) -> np.ndarray:
        raise NotImplementedError

    @abstractmethod
    def get_cursor(self) -> tuple[int, int]:
        raise NotImplementedError

    @abstractmethod
    def get_window_meta(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def send_action(self, action: AtomicAction) -> None:
        raise NotImplementedError

    @abstractmethod
    def sleep(self, dt: float) -> None:
        raise NotImplementedError

    @abstractmethod
    def time(self) -> float:
        raise NotImplementedError
