from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RecordConfig:
    fps: int = 10
    duration: float = 60.0


@dataclass
class BuildDatasetConfig:
    align_tolerance_sec: float = 0.1
    drop_unaligned: bool = True
    include_move_events: bool = True


@dataclass
class TrainConfig:
    epochs: int = 1
    batch_size: int = 32
    lr: float = 1e-3
