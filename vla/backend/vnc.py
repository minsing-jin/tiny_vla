from __future__ import annotations

from vla.backend.base import Backend


class VNCBackend(Backend):
    def __init__(self, *args, **kwargs) -> None:
        raise NotImplementedError("VNC backend is a placeholder in MVP.")
