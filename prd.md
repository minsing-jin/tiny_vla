# VLA Executor Framework PRD

## 0) 프로젝트 목표 (반드시 이대로)

외부 VLM(Planner)이 상위 명령(Command)을 생성한다.
본 프레임워크는 그 Command를 입력으로 받아 현재 화면에서 조작 가능한 후보를 찾아 키보드/마우스 원자 액션(atomic action)을 수행하는 Executor-VLA를 대상으로 한다.

- 데모 수집(record)
- 데이터셋 빌드(build)
- 오프라인 BC 학습(train)
- VM/로컬에서 커맨드 기반 롤아웃 평가(rollout/eval)
- 실패 구간 교정 수집(DAgger collect)
- 재학습(loop)

핵심 KPI: p95 inference latency + command success rate@budget

비목표:
- 외부 VLM(planner) 구현
- 장기 계획/추론
- 멀티게임 자동 리셋 완성(플러그인으로만)

## 1) 산출물(Deliverables)

### 1.1 레포 구조(필수)
- README.md
- pyproject.toml
- vla/
  - core/types.py, clock.py, config.py, io_jsonl.py
  - backend/base.py, local_macos.py, local_crossplat.py, vnc.py
  - record/recorder.py, tagging.py, segment.py
  - replay/replayer.py, viewer.py
  - command/source.py, server.py
  - policy/base.py, baseline.py, model.py
  - train/dataset.py, train_bc.py, export.py
  - eval/rollout.py, metrics.py, failure_pack.py
  - dagger/collector.py, ui.py
- scripts/vla_cli.py
- tests/test_types.py, test_io_jsonl.py, test_alignment.py, test_replay_roundtrip.py

### 1.2 CLI 커맨드(필수)
- vla record
- vla replay
- vla build-dataset
- vla train
- vla rollout
- vla dagger collect
- vla dagger merge
- vla export

모든 커맨드는 --help 제공 + README 예시 포함.

## 2) 핵심 계약(Contract)

### 2.1 Command
필드: cmd_id, skill, hint, constraints, guard, budget

### 2.2 Status
필드: cmd_id, status(SUCCESS|FAIL|NEED_HELP|TIMEOUT), info

### 2.3 Atomic Action
예: MOVE_TO, CLICK, KEY

### 2.4 Observation
필드: t, frame_path, cursor, window

## 3) Backend 인터페이스
- capture_frame() -> np.ndarray
- get_cursor() -> (x,y)
- get_window_meta() -> dict
- send_action(action) -> None
- sleep(dt), time()

로컬 macOS 구현 우선, 타 OS/VM은 인터페이스+placeholder.

## 4) Recorder
- FPS 프레임 저장
- 키/마우스 이벤트 JSONL 저장
- tags.jsonl에 CMD_START/SET_ROI/CAPTURE_REF_PATCH/CMD_END 기록

## 5) Segmenter
- runs/record_* -> datasets/<name>/episodes/ep_*/cmd.json, steps.jsonl
- action t_a 당 t<=t_a 최근 obs 매칭, 기본 허용오차 100ms
- MOVE 라벨 포함/제외 config 옵션

## 6) BC 학습
- PyTorch 최소 CNN+MLP
- 입력: global frame, local crop, skill embedding, hint 일부
- 출력: action_type + xy
- train 결과: model.pt, metrics.jsonl, config snapshot

## 7) Rollout/Eval
- command source: file:, stdin, ws(optional)
- max_steps/max_seconds budget 루프
- guard: NOOP, VISUAL_CHANGE, TEMPLATE_MATCH
- status/latency 저장

## 8) Failure Pack
- FAIL/NEED_HELP/TIMEOUT 시 failure_packs에 재현 번들 저장
- replay --pack 으로 재생 가능

## 9) DAgger
- collect: 클릭 교정 + action 타입 지정
- merge: corrections.jsonl을 dataset 라벨에 반영한 신규 버전 생성

## 10) 성능 측정
- capture_ms, policy_infer_ms, inject_ms, guard_ms
- p50/p95 policy_infer_ms, success rate@budget, stuck rate

## 11) Acceptance Criteria
- record 1분 저장 가능
- replay 재생 가능
- build-dataset episode 생성
- train 1 epoch + ckpt 생성
- rollout file/stdin 실행 + status 기록
- failure_pack 생성 + replay 가능
- dagger collect/merge 가능
- rollout summary에 latency p50/p95 출력

## 12) README 필수 내용
- 외부 VLM 명령을 실행하는 Executor-VLA만 훈련한다는 명시
- macOS 권한 안내
- quickstart(record/build-dataset/train/rollout/dagger collect/merge)

## 13) 실행 우선순위
1. core types + JSONL IO + CLI
2. local backend + recorder/replayer
3. tagging + build-dataset
4. BC trainer + minimal model
5. rollout + guard + metrics/latency
6. failure pack + dagger collect/merge
