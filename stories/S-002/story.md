# Story S-002: Backend Plugin and Demo Record/Replay

## Project Context
- project: VLA Executor Framework
- goal: Train and evaluate an executor-only VLA that consumes external planner commands and executes atomic UI actions with record/build/train/rollout/dagger loop.

## Goal
Backend Plugin and Demo Record/Replay

## Acceptance Criteria
- Backend base interface exposes capture_frame/get_cursor/get_window_meta/send_action/sleep/time.
- local_macos backend supports best-effort capture and input injection with graceful permission errors.
- record command saves manifest/frames/obs.jsonl/actions.jsonl/tags.jsonl in runs/record_*.
- replay command replays recorded actions and can view frame stream.

## Non-goals
- Full VM backend implementation
- Perfect cross-platform automation

## Constraints
- Prefer mss capture
- Use pyautogui or pynput for injection/listening
- Document macOS accessibility and screen recording permission requirements

## Dependencies
- S-001

## Risks
- OS permission failures
- Input injection variability

## Success Metrics
- 1-minute record run can be saved
- Replay can consume recorded run

