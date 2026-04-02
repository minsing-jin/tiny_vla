# AGENTS

## Ralph Loop Principles
- Artifact-first: persistent memory lives in files, not chat.
- Evidence-gated: PASS requires executable evidence.
- Context-pack memory: update `stories/<id>/context_pack.md` every loop.
- Self-improvement: append reusable lessons to `LESSONS.md`.

## Role Contracts
### specify-gidometa
- Input: user idea + repo context
- Output: `prd.json`, `stories/<id>/story.md`

### planner
- Input: `prd.json`, `stories/<id>/story.md`
- Output: `stories/<id>/plan.md`

### context-scribe
- Input: diff + logs + story artifacts
- Output: `stories/<id>/context_pack.md`, `LESSONS.md` (when needed)

### implementer
- Input: `story.md`, `plan.md`, `context_pack.md`, `errors.md`
- Output: code changes

### testsmith
- Input: story context + current code
- Output: fail-first and regression tests

### verifier
- Input: code + plan + context pack + logs
- Output PASS: `stories/<id>/evidence.md`
- Output FAIL: `stories/<id>/errors.md`

### reviewer
- Input: current diff + tests
- Output: actionable review notes (commands or checks)

### show-me-the-hook
- Input: updated user directives + current PRD
- Output: patched `prd.json`/`story.md`/`plan.md`

### qa dr.strange
- Input: full PRD + runnable system
- Output: E2E evidence

### issue tiger
- Input: issue metadata
- Output: branch/PR automation artifacts

## Loop Sequence
specify-gidometa -> planner -> context-scribe -> implementer -> testsmith -> verifier
FAIL => context-scribe update -> implementer retry
ALL PASS => qa dr.strange
