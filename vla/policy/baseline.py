from __future__ import annotations

import time

from vla.core.types import AtomicAction, Command, Observation
from vla.policy.base import Policy


class BaselinePolicy(Policy):
    def act(self, obs: Observation, cmd: Command) -> AtomicAction:
        t = time.time()
        skill = cmd.skill
        roi = cmd.hint.get("roi_bbox")
        if roi:
            x = int((roi[0] + roi[2]) / 2)
            y = int((roi[1] + roi[3]) / 2)
        else:
            x, y = obs.cursor

        if skill in {"CLICK_UI", "SELECT_FROM_LIST"}:
            return AtomicAction(t=t, type="CLICK", x=x, y=y, button=cmd.constraints.get("button", "LEFT"))
        if skill == "DOUBLE_CLICK_UI":
            return AtomicAction(t=t, type="DOUBLE_CLICK", x=x, y=y, button=cmd.constraints.get("button", "LEFT"))
        if skill == "RIGHT_CLICK_UI":
            return AtomicAction(t=t, type="RIGHT_CLICK", x=x, y=y, button="RIGHT")
        if skill == "TYPE_TEXT":
            return AtomicAction(t=t, type="TYPE_TEXT", text=cmd.hint.get("text", ""))
        if skill == "PRESS_KEY":
            return AtomicAction(t=t, type="KEY", key=cmd.constraints.get("key", "esc"), down=None)
        if skill == "PRESS_HOTKEY":
            modifiers = cmd.constraints.get("modifiers", [])
            key = cmd.constraints.get("key", "")
            combo = "+".join([m.lower() for m in modifiers] + ([key.lower()] if key else []))
            return AtomicAction(t=t, type="HOTKEY", text=combo)
        if skill == "SCROLL_ROI":
            dy = int(cmd.constraints.get("max_scroll", 0) or 0)
            return AtomicAction(t=t, type="SCROLL", x=x, y=y, dy=dy)
        if skill == "RECOVER_BACK":
            return AtomicAction(t=t, type="KEY", key="esc", down=None)
        return AtomicAction(t=t, type="MOVE_TO", x=x, y=y)
