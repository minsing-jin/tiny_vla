# Plan for S-003

## Steps
- Specify story scope and constraints.
- Break into file/module changes with small commits.
- Implement minimal change set.
- Add adversarial/regression tests (fail-first).
- Verify and record evidence.

## Files
- stories/<id>/story.md
- stories/<id>/plan.md
- stories/<id>/context_pack.md

## Implementer Commands
- `mkdir -p .ralph/artifacts`
- `printf '%s\n' '# 1.1 레포 구조(필수)::_1.1_meets_documented_requirements' > .ralph/artifacts/S-003._1.1_meets_documented_requirements.done`

## Test Plan
- `test -f .ralph/artifacts/S-003._1.1_meets_documented_requirements.done`
- `grep -q '_1.1_meets_documented_requirements' .ralph/artifacts/S-003._1.1_meets_documented_requirements.done`

## Verifier Commands
- `test -f .ralph/artifacts/S-003._1.1_meets_documented_requirements.done`
- `grep -q '_1.1_meets_documented_requirements' .ralph/artifacts/S-003._1.1_meets_documented_requirements.done`

## Rollback
- Revert story diff and rerun verifier commands.

## Risks
- # 1.1 레포 구조(필수) # 1.1 레포 구조(필수) meets documented requirements - README.md - pyproject.toml - vla/ - core/types.py, clock.py, config.py, io_jsonl.py - backend/base.py, local_macos.py, local_crossplat.py, vnc.py - record/recorder.py, tagging.py, segment.py - replay/replayer.py, viewer.py - command/source.py, server.py - policy/base.py, baseline.py, model.py - train/dataset.py, train_bc.py, export.py - eval/rollout.py, metrics.py, failure_pack.py - dagger/collector.py, ui.py - scripts/vla_cli.py - tests/test_types.py, test_io_jsonl.py, test_alignment.py, test_replay_roundtrip.py
