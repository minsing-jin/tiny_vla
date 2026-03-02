# Story S-001: Core Contract and CLI Skeleton

## Project Context
- project: VLA Executor Framework
- goal: Train and evaluate an executor-only VLA that consumes external planner commands and executes atomic UI actions with record/build/train/rollout/dagger loop.

## Goal
Core Contract and CLI Skeleton

## Acceptance Criteria
- Repository tree includes required core/backend/record/replay/command/policy/train/eval/dagger modules.
- Command, Status, AtomicAction, Observation, GuardSpec contracts are defined and serializable.
- JSONL read/write utilities and timestamp alignment helper exist.
- CLI provides record/replay/build-dataset/train/rollout/dagger collect/dagger merge/export with --help.

## Non-goals
- Implement external VLM planner
- Complex long-horizon planning

## Constraints
- Use Python package layout under vla/
- All logs and training/eval artifacts must use contract schema

## Dependencies
- (none)

## Risks
- Schema drift between modules
- CLI argument inconsistency

## Success Metrics
- All core tests pass
- All required CLI --help commands are callable

