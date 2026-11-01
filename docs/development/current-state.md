# 현재 상태와 다음 할 일

갱신: 2026-11-01 (Asia/Seoul)

자동 생성: `docs/development/state.json` 수정 후 `python utils/scripts/context.py --write`.
요약은 작업 재개용이다. 공통 규칙·원문·현재 git status가 우선한다.

## 사용자·팀·브랜치

- 김동조 · Lab678 개발. 현재 dj/agent, 작업폴더 D:/git/lab678/.local/worktrees/dj-agent. 기존 D:/git/lab678의 dj/develop·원본 기록/백업 보존.

## 현재 목표

- 승인된 dj/agent 분기·계획 복사본 정리 완료. 이후 작업은 새 worktree에서 진행하며 기능 구현은 별도 계획/허락 대기.

## 승인된 범위·운영

- 2026-11-01 사용자 명시: “분기·복사본 정리만 승인”. 최신 원격 develop 기반 별도 worktree와 계획 복사본 정리·개인 브랜치 설정/승인규칙 이관만 허용.
- 조사→개발계획→실시계획→검토·보완→명시적 허락→실시·검증. 의견·샘플·질문·시간경과를 승인으로 추정하지 않는다. 같은 승인 범위만 계속 진행한다.
- frontend/ 및 UI용 JS/HTML·우회사본/패치 수정 금지. 프론트는 담당자 전달안만 정리한다.
- main/develop/dj/develop의 기존 파일·로컬 브랜치 보존. 기능 이식/수정·복원·병합·Push·배포·모델 설치/합성·실제 키 복사는 이번 미승인.
- plan_dj는 개인 개발용·Git/공유 색인 제외. 원본 D:/git/lab678/plan_dj의 src/ZIP/대화/완료 이력은 삭제하지 않는다.
- 완료 작업의 로컬 커밋 상시 요청은 dj/agent에 적용하되 Push는 별도 명시 요청. 전체 완료 보고문을 커밋 메시지로 그대로 기록, AI 공동명의 금지·사용자 명의. 11/1 13:00 KST 이후 커밋 금지.

## 완료·검증

- origin/develop을 Fetch해 252c07c03b060a77ddd874f48b0f99ed4cbb1416에서 dj/agent/worktree 생성. 기존 main/develop/dj/develop 이동 없음.
- plan_dj 763개를 새 폴더에 바이트 검증 복사 후 새 복사본의 중복/과거 자료만 정리. 원본 삭제0. 새 활성 계획6파일, 미완료5개+분리/미정2개.
- 기본 구현 완료 항목은 새 구현 TODO에서 제외. 개인 고도화는 develop에 없어 이식·검증 대기로 유지. 프론트 요구는 담당자 전달로 분리.
- AGENTS·engineering-loop 승인 규칙 이관, utils/harness.json 개인 브랜치 기준을 dj/agent로 설정. 서비스/프론트·하네스 스크립트 기능 변경 없음.
- 준비검증 때 원본375/763 해시 일치 확인. 최종 비교는 원본 코드/ZIP 불변·삭제0, 진행기록5개 후속 갱신 보존. 새 develop 조상/코드 동일/계획6·제외·링크·색인/상태 정상, 기존 설명 누락2건 유지.

## 진행 중

- 현재 기능 구현 진행 없음. 준비 검증/보고를 기록하고 다음 사용자 지시를 기다린다.

## 다음 할 일 — 순서대로

- A02 개인 고도화와 공급자 어댑터의 이식 계획부터 검토한다. 조사/실시계획 보완 후 사용자 명시 허락 전에는 구현하지 않는다.
- A03 모호한 날짜/시각·부분 조건, A04 API/화면 소비 차이 전달, A05 방문 가능 근거, A06 새 기준 QA 계획은 plan_dj/TODO.md의 잔여 범위로 관리한다.

## 미정·주의

- 기본 브라우저 음성/TourAPI/코스·길찾기/검색·60분/CORS는 소스가 존재하므로 재개발로 분류하지 않는다. 새 기준 전체 QA·실기기·배포 완료와는 구분한다.
- 개인 chat_prompt/chat_grounding/전용 테스트/평가기와 공급자 어댑터 통합은 아직 미반영. 이전 개인 평가를 새 브랜치 성적으로 쓰지 않는다.
- A07 음성 자연스러움/로컬 TTS는 별도 검토, A08 문화Q&A·지속선호·S05 팀 연결은 미정이다. 이번 준비 승인에서 구현 허락을 추정하지 않는다.
- 원본 개발 폴더는 dj/develop 그대로이며 새 작업에는 이 별도 worktree 경로를 명시한다. 실제 .env/키와 서버 실행 상태는 복사하지 않았다.

## 필요할 때 읽을 자료

- plan_dj/README.md → TODO.md → execution-plan.md. decisions.md에는 미정, preserved-assets.md에는 원본/백업, cleanup-manifest.json에는 복사·제외·잔여 추적 근거.
- 공통 운영 TEAM_WORKFLOW.md, 개인 승인 AGENTS.md/engineering-loop. 실제 최신 코드와 현재 Git 상태를 우선한다.
- reports/20261101-dj-agent-setup.md에 준비 결과·검증 한계 기록. 개인 정리 근거는 plan_dj/cleanup-manifest.json과 .local/agent-setup-verification-20261101.json.
