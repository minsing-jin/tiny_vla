# VLA Executor Framework Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement an end-to-end executor-only VLA MVP with CLI for record/replay/build-dataset/train/rollout/dagger/export.

**Architecture:** Create modular package `vla` with clear contracts in `core.types`, plugin-like backends, minimal recorder/replayer/segmenter, tiny BC model, rollout evaluator with guards and latency metrics, and DAgger correction tools.

**Tech Stack:** Python 3.10+, dataclasses, argparse, numpy, opencv-python, mss, pyautogui/pynput, torch.

---

### Task 1: Scaffold package and core contracts
- Create package tree and contract dataclasses.
- Add JSONL IO and alignment utilities.
- Add initial tests for types/IO/alignment.

### Task 2: Backend + record/replay
- Implement backend interface and macOS best-effort backend.
- Implement recorder and tagging tools.
- Implement replay and viewer.

### Task 3: Dataset build + policy + training
- Segment raw run into command episodes.
- Implement tiny policy baseline and train script.
- Add export placeholder.

### Task 4: Rollout/eval/failure packs/DAgger
- Implement command sources and rollout loop.
- Implement metrics and failure pack creation.
- Implement DAgger collect and merge.

### Task 5: CLI, docs, verification
- Wire `vla` CLI commands.
- Write README quickstart and permissions guidance.
- Run tests and smoke commands, then report evidence.

