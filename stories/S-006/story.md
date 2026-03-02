# Story S-006: DAgger Correction Collection and Merge

## Project Context
- project: VLA Executor Framework
- goal: Train and evaluate an executor-only VLA that consumes external planner commands and executes atomic UI actions with record/build/train/rollout/dagger loop.

## Goal
DAgger Correction Collection and Merge

## Acceptance Criteria
- dagger collect opens minimal UI and records corrected click/action_type to corrections.jsonl.
- dagger merge applies corrected labels to episode steps and writes versioned dataset output.
- Loop supports retraining with merged dataset version.

## Non-goals
- Rich annotation tool
- Online DAgger orchestration service

## Constraints
- Correction format includes cmd_id, step_idx, corrected_action
- Merged dataset must preserve original structure

## Dependencies
- S-005

## Risks
- Wrong step indexing during merge
- Low quality manual correction

## Success Metrics
- At least one correction can be collected and merged into new dataset version

