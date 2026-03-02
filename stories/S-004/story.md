# Story S-004: Offline BC Training and Model Export

## Project Context
- project: VLA Executor Framework
- goal: Train and evaluate an executor-only VLA that consumes external planner commands and executes atomic UI actions with record/build/train/rollout/dagger loop.

## Goal
Offline BC Training and Model Export

## Acceptance Criteria
- PyTorch baseline model supports command-conditioned action prediction.
- train CLI runs 1 epoch from built dataset and produces model.pt, metrics.jsonl, config snapshot.
- Reported metrics include action_type_acc, click_dist_px, heatmap_topk_hit@k.
- export CLI provides ONNX export path for trained model.

## Non-goals
- SOTA model quality
- Large-scale distributed training

## Constraints
- Start with simple CNN+MLP
- Favor pipeline completeness and runtime simplicity

## Dependencies
- S-003

## Risks
- Dataset sparsity may destabilize training
- Optional dependency friction (torch)

## Success Metrics
- vla train completes 1 epoch without runtime error

