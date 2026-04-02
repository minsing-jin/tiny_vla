# Story S-021: VLA 학습 loss 최소화 반복 루프

## Goal
VLA 학습 loss 최소화 반복 루프

## Acceptance Criteria
- VLA 학습을 반복 실행하면서 epoch별 loss를 기록한다
- best_loss가 first_loss 이하가 될 때까지(또는 안전 상한 epoch) 반복한다
- 학습 이력(history.json)에 first_loss/best_loss/epochs_ran을 저장한다

## Non-goals
- 무제한 무한루프 실행

## Risks
- 학습 수렴 실패 가능성
- 환경 의존성(torch)
