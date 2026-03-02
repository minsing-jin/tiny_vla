from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class GuardSpec:
    type: str = "NOOP"
    roi_bbox: list[int] | None = None
    threshold: float = 0.08
    template_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "GuardSpec":
        if not data:
            return cls()
        return cls(
            type=data.get("type", "NOOP"),
            roi_bbox=data.get("roi_bbox"),
            threshold=float(data.get("threshold", 0.08)),
            template_path=data.get("template_path"),
        )


@dataclass
class Command:
    cmd_id: str
    skill: str
    hint: dict[str, Any] = field(default_factory=dict)
    constraints: dict[str, Any] = field(default_factory=dict)
    guard: GuardSpec = field(default_factory=GuardSpec)
    budget: dict[str, Any] = field(default_factory=lambda: {"max_steps": 30, "max_seconds": 2.0, "max_retries": 3})

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["guard"] = asdict(self.guard)
        return d

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Command":
        return cls(
            cmd_id=data["cmd_id"],
            skill=data["skill"],
            hint=data.get("hint", {}),
            constraints=data.get("constraints", {}),
            guard=GuardSpec.from_dict(data.get("guard")),
            budget=data.get("budget", {"max_steps": 30, "max_seconds": 2.0, "max_retries": 3}),
        )


@dataclass
class Status:
    cmd_id: str
    status: str
    info: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Status":
        return cls(cmd_id=data["cmd_id"], status=data["status"], info=data.get("info", {}))


@dataclass
class AtomicAction:
    t: float
    type: str
    x: int | None = None
    y: int | None = None
    button: str | None = None
    key: str | None = None
    down: bool | None = None
    text: str | None = None
    dx: int | None = None
    dy: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AtomicAction":
        return cls(**data)


@dataclass
class Observation:
    t: float
    frame_path: str
    cursor: list[int]
    window: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Observation":
        return cls(t=float(data["t"]), frame_path=data["frame_path"], cursor=data.get("cursor", [0, 0]), window=data.get("window", {}))
