from __future__ import annotations


def match_observation_to_action(obs_ts: list[float], action_t: float, tolerance: float = 0.1) -> int | None:
    """Return index of nearest obs with t <= action_t and within tolerance."""
    best_idx = None
    best_dt = None
    for i, t in enumerate(obs_ts):
        if t > action_t:
            break
        dt = action_t - t
        if best_dt is None or dt < best_dt:
            best_dt = dt
            best_idx = i
    if best_dt is None or best_dt > tolerance:
        return None
    return best_idx
