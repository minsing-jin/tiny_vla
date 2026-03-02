# vla-executor-framework

이 프레임워크는 **외부 VLM(Planner)이 생성한 Command를 실행하는 Executor-VLA만 훈련**합니다.

## What it does
- `record`: 데모 수집 (frames/obs/actions/tags)
- `replay`: 저장된 데모 또는 failure pack 재생
- `build-dataset`: raw 로그를 command episode 데이터셋으로 변환
- `train`: 오프라인 BC 학습
- `rollout`: command stream 기반 실행 및 status 반환
- `dagger collect/merge`: 실패 구간 교정 및 병합
- `export`: ONNX export placeholder

## macOS 권한 안내
로컬 입력 주입/캡처 사용 시 다음 권한이 필요할 수 있습니다.
- 시스템 설정 > 개인정보 보호 및 보안 > 손쉬운 사용(Accessibility)
- 화면 기록(Screen Recording)

권한이 없으면 backend가 graceful error를 출력하고 종료합니다.

## Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install -e .[local,train]
```

## Quickstart
```bash
# 1) Record demo (60s)
vla record --out runs/record_demo --duration 60 --fps 10

# 2) Tag commands (interactive)
vla tag --run runs/record_demo

# 3) Build dataset
vla build-dataset --runs_glob 'runs/record_*' --out datasets/demo

# 4) Train BC
vla train --dataset datasets/demo --out runs/train_demo --epochs 1

# 5) Rollout from file command source
vla rollout --command_source file:commands.jsonl --out runs/rollout_demo

# 6) Replay failure pack
vla replay --pack failure_packs/some_failure_pack

# 7) DAgger collect/merge
vla dagger collect --pack failure_packs/some_failure_pack --out corrections.jsonl
vla dagger merge --dataset datasets/demo --corrections corrections.jsonl --out datasets/demo_dagger1
```

## CLI
각 명령은 `--help`를 제공합니다.
```bash
vla record --help
vla replay --help
vla build-dataset --help
vla train --help
vla rollout --help
vla dagger collect --help
vla dagger merge --help
vla export --help
```
