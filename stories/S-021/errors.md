# Errors: S-021

- phase: `builder`
- returncode: `1`

## Reproduction
```bash
test -d datasets/real_executor/episodes
```

## Observed
```text
(no output)
```

## Fix Instructions
- Identify root cause from command output and changed files.
- Apply one minimal fix, then rerun verifier commands.

