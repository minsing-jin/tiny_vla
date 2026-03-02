# Story S-005: Rollout/Eval, Guard, Latency, Failure Pack

## Project Context
- project: VLA Executor Framework
- goal: Train and evaluate an executor-only VLA that consumes external planner commands and executes atomic UI actions with record/build/train/rollout/dagger loop.

## Goal
Rollout/Eval, Guard, Latency, Failure Pack

## Acceptance Criteria
- rollout supports file: and stdin command sources and optional ws placeholder.
- Each command executes loop with budget limits and returns Status SUCCESS/FAIL/NEED_HELP/TIMEOUT.
- Guard types NOOP/VISUAL_CHANGE/TEMPLATE_MATCH are supported in MVP form.
- Latency per step records capture_ms/policy_infer_ms/inject_ms/guard_ms and summary includes p50/p95 and success/stuck rates.
- Failures automatically emit replayable failure_packs with cmd/status/obs/actions/frames.

## Non-goals
- External planner orchestration
- Autonomous environment reset

## Constraints
- Persist rollout artifacts under runs/rollout_*
- Status schema must be contract compliant

## Dependencies
- S-001
- S-004

## Risks
- Guard false positives/negatives
- Latency overhead from image operations

## Success Metrics
- Rollout summary reports p50/p95 inference latency
- Failure pack can be replayed with vla replay --pack

