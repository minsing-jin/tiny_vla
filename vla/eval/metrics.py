from __future__ import annotations

import statistics


def summarize_rollout(step_latencies: list[dict], statuses: list[str]) -> dict:
    infer = [x.get("policy_infer_ms", 0.0) for x in step_latencies]
    if infer:
        p50 = statistics.median(infer)
        p95 = sorted(infer)[min(len(infer) - 1, int(0.95 * (len(infer) - 1)))]
    else:
        p50 = 0.0
        p95 = 0.0
    success = sum(1 for s in statuses if s == "SUCCESS")
    total = len(statuses)
    stuck = sum(1 for s in statuses if s in {"NEED_HELP", "TIMEOUT"})
    return {
        "p50_policy_infer_ms": p50,
        "p95_policy_infer_ms": p95,
        "cmd_success_rate@budget": (success / total) if total else 0.0,
        "stuck_rate": (stuck / total) if total else 0.0,
    }
