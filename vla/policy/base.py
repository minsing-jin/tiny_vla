from __future__ import annotations

from abc import ABC, abstractmethod

from vla.core.types import AtomicAction, Command, Observation


class Policy(ABC):
    @abstractmethod
    def act(self, obs: Observation, cmd: Command) -> AtomicAction:
        raise NotImplementedError
