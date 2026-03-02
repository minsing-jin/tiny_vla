# Story S-003: Tagging and Dataset Builder

## Project Context
- project: VLA Executor Framework
- goal: Train and evaluate an executor-only VLA that consumes external planner commands and executes atomic UI actions with record/build/train/rollout/dagger loop.

## Goal
Tagging and Dataset Builder

## Acceptance Criteria
- tagging workflow can emit CMD_START/SET_ROI/CAPTURE_REF_PATCH/CMD_END events to tags.jsonl.
- build-dataset converts runs/record_* into datasets/<name>/episodes/ep_*/cmd.json and steps.jsonl.
- Step alignment matches nearest observation where obs.t <= action.t with default 100ms tolerance.
- MOVE event inclusion is configurable for teacher labels.

## Non-goals
- Auto semantic command segmentation without tags

## Constraints
- Warn or drop unaligned steps based on config
- Keep output compatible with BC training input

## Dependencies
- S-001
- S-002

## Risks
- Sparse or noisy tags causing short episodes
- Alignment mistakes reducing data quality

## Success Metrics
- Dataset build produces episodes with at least 10 steps in sample run

