# Debug Bundle: S-021 attempt 1

- phase: `builder`
- command: `test -d datasets/real_executor/episodes`
- returncode: `1`

## Root-Cause Checklist
- Reproduce the failure command exactly once from logs.
- Compare with prior successful evidence/context pack.
- Apply one minimal fix then rerun verifier.

## Git Snapshot
- head: `1391aef`

```
M prd.json
 M stories/S-001/story.md
 M stories/S-002/story.md
 M stories/S-003/story.md
 M stories/S-004/story.md
 M stories/S-005/story.md
 M stories/S-006/story.md
?? .ralph/
?? AGENTS.md
?? E2E_EVIDENCE.md
?? LESSONS.md
?? PRD_VALIDATION_ERRORS.md
?? PROGRESS.jsonl
?? commands_loop_rollout.jsonl
?? commands_pc5.jsonl
?? corrections_loop.jsonl
?? corrections_pc6.jsonl
?? prd.md
?? progress.md
?? ralph_state.json
?? scripts/loop_checks/
?? stories/S-001/context_pack.md
?? stories/S-001/evidence.md
?? stories/S-001/plan.md
?? stories/S-002/context_pack.md
?? stories/S-002/evidence.md
?? stories/S-002/plan.md
?? stories/S-003/context_pack.md
?? stories/S-003/evidence.md
?? stories/S-003/plan.md
?? stories/S-004/context_pack.md
?? stories/S-004/evidence.md
?? stories/S-004/plan.md
?? stories/S-005/context_pack.md
?? stories/S-005/evidence.md
?? stories/S-005/plan.md
?? stories/S-006/context_pack.md
?? stories/S-006/evidence.md
?? stories/S-006/plan.md
?? stories/S-007/
?? stories/S-008/
?? stories/S-009/
?? stories/S-010/
?? stories/S-011/
?? stories/S-012/
?? stories/S-013/
?? stories/S-014/
?? stories/S-015/
?? stories/S-016/
?? stories/S-017/
?? stories/S-018/
?? stories/S-019/
?? stories/S-020/
?? stories/S-021/
```

```
prd.json               | 1281 +++++++++++++++++++++++++++++++++++++++++++-----
 stories/S-001/story.md |   25 +-
 stories/S-002/story.md |   28 +-
 stories/S-003/story.md |   26 +-
 stories/S-004/story.md |   26 +-
 stories/S-005/story.md |   29 +-
 stories/S-006/story.md |   25 +-
 7 files changed, 1218 insertions(+), 222 deletions(-)
```
