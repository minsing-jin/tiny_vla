# Plan for S-021

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
- `test -d datasets/real_executor/episodes`
- `python3.11 scripts/loop_checks/train_until_min_loss_from_dataset.py --dataset datasets/real_executor --out runs/train_real_loop --max-epochs 50 --patience 5 --min-samples 10`

## Test Plan
- `pytest -q`

## Verifier Commands
- `python3.11 scripts/loop_checks/train_until_min_loss_from_dataset.py --dataset datasets/real_executor --out runs/train_real_loop --max-epochs 50 --patience 5 --min-samples 10`
- `test -f runs/train_real_loop/history.json`
- `python3.11 - << 'PY2'
import json
from pathlib import Path
h=json.loads(Path('runs/train_real_loop/history.json').read_text())
assert h['best_loss'] <= h['first_loss']
assert h['samples'] >= 10
print('loss_ok',h['first_loss'],h['best_loss'],'samples',h['samples'])
PY2`

## Rollback
- Revert story diff and rerun verifier commands.

## Risks
- 실데이터 부족 시 학습 불안정
- torch/onnx 환경 의존
