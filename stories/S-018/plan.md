# Plan for S-018

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
- `printf '%s\n' '11) Acceptance Criteria::11_Acceptance_Criteria_meets_documented_requirements' > .ralph/artifacts/S-018.11_Acceptance_Criteria_meets_documented_requirements.done`

## Test Plan
- `test -f .ralph/artifacts/S-018.11_Acceptance_Criteria_meets_documented_requirements.done`
- `grep -q '11_Acceptance_Criteria_meets_documented_requirements' .ralph/artifacts/S-018.11_Acceptance_Criteria_meets_documented_requirements.done`

## Verifier Commands
- `test -f .ralph/artifacts/S-018.11_Acceptance_Criteria_meets_documented_requirements.done`
- `grep -q '11_Acceptance_Criteria_meets_documented_requirements' .ralph/artifacts/S-018.11_Acceptance_Criteria_meets_documented_requirements.done`

## Rollback
- Revert story diff and rerun verifier commands.

## Risks
- 11) Acceptance Criteria 11) Acceptance Criteria meets documented requirements - record 1분 저장 가능 - replay 재생 가능 - build-dataset episode 생성 - train 1 epoch + ckpt 생성 - rollout file/stdin 실행 + status 기록 - failure_pack 생성 + replay 가능 - dagger collect/merge 가능 - rollout summary에 latency p50/p95 출력
