# VLA Executor Framework Design

Goal: Build an executor-only VLA framework that consumes external planner Commands and performs atomic UI actions with recording, dataset build, BC training, rollout eval, failure packs, and DAgger loops.

## Architecture
- `vla.core`: stable schemas (`Command`, `Status`, `AtomicAction`, `Observation`) and IO/time alignment utilities.
- `vla.backend`: pluggable environment backends; macOS local backend is best-effort MVP.
- `vla.record/replay`: demo collection + playback.
- `vla.train/policy`: minimal BC pipeline with tiny baseline model.
- `vla.eval/dagger`: command rollout, guard checks, metrics, failure pack generation, correction merge.
- `scripts/vla_cli.py`: unified CLI entrypoint.

## Data Flow
1. `record` writes raw run artifacts (`frames`, `obs.jsonl`, `actions.jsonl`, `tags.jsonl`).
2. `build-dataset` segments by tagged command windows and aligns action->observation by nearest previous timestamp.
3. `train` reads episodes and trains a minimal action predictor.
4. `rollout` reads commands from file/stdin/ws placeholder, executes policy through backend, evaluates guard, writes status/latency.
5. Failures are packed for replay and DAgger correction collection.
6. `dagger merge` patches labels into a new dataset version.

## Error Handling
- Backends fail gracefully with actionable permission guidance.
- Optional dependencies (`torch`, `mss`, `pyautogui`, `pynput`, `opencv`) are guarded with explicit runtime errors.
- Unimplemented optional features are placeholders with clear exceptions.

## Testing
- Schema serialization/deserialization.
- JSONL roundtrip.
- Timestamp alignment behavior.
- Replay log roundtrip sanity.

