# Lab678 · AI 작업 안내

작업을 시작하기 전에 [TEAM_WORKFLOW.md](TEAM_WORKFLOW.md)를 읽고 따라요. 팀 역할, 브랜치·PR·Merge, 사전 공유, 테스트·보안 및 보고의 공통 기준은 이 문서 하나로 관리해요. 합의·제안·미정 표시를 구분하고 미정 사항을 임의로 확정하지 않아요.

프로젝트 구조와 실행 방법은 [README.md](README.md), 환경변수 형식은 `.env.example`, 실제 작업 요구사항은 확정된 PRD·화면·API 명세를 확인해요.

**제품 기획 작업 시작점:** [docs/planning/README.md](docs/planning/README.md)를 먼저 읽고, [최신 PRD v0.7.0](docs/planning/PRD.md)와 [MVP 화면명세서 v0.3.0](docs/planning/Lab_678_MVP_화면명세서.md)를 함께 확인해요. `handoff/`는 착수 참고, `archive/`는 구버전 이력이고 현행 요구사항 기준이 아니에요. 팀 검토 대기와 실제 QA 완료를 구분해요.

- 커밋·push는 사용자가 명시적으로 요청할 때만 해요.
- 커밋 메시지에 Co-Authored-By 같은 AI 표시는 넣지 않고 사용자 명의로만 커밋해요. 커밋 메시지는 한국어로 짧게 써요.
- 제출 마감은 11/1(일) 13:00이고, 마감 뒤에는 커밋하지 않아요.
- 장소·가격·시간 같은 사실 데이터는 코드가 정하고, LLM은 설명·해석만 해요.

## 개인 개발 작업 맥락

현재 작업폴더는 **`D:\git\lab678`**, 실제 작업 브랜치는 최신 `origin/develop`의 `e5697e2`에서 새로 만든 **`dj/develop`**이에요. 원본 `dj/agent` 코드 `b6355a0`·명세 `d541ea5`는 push해 보존했고, 이전 로컬 `dj/develop` tip은 `dj/develop-before-engine-20261101`에 남겼어요. 사용자 최신 지시 “계획 저장하고 보여주고 시작해”, “체크리스트를 만들어 하나씩 체크하면서 실행 점검 보완 진행해”로 [엔진 이식 계획](docs/development/agent-engine-migration-plan.md)의 M0~M5를 승인받았어요. [실행 체크리스트](docs/development/agent-engine-port-progress.md)를 실제 검증 후 체크하며 진행해요. 최소 선택 버튼·실제 모호한 출발지 팝업 외 전체 UI 교체는 제외해요. 원격 dj/develop force·새 PR·병합·배포는 별도 승인 없이 하지 않아요.

후속 사용자 **“이대로 푸시 … PR발행해”**로 현재 검증본의 커밋·push와 새 `dj/develop → develop` PR 발행을 승인받았어요. 이전 원격 tip80d481b는 보존 ref를 먼저 만든 뒤, 조회한 SHA가 같을 때만 lease로 새 검증본을 게시해요. 마감 제한에 대한 이 게시 요청의 예외를 기록하고 공통 guard/날짜는 바꾸지 않아요. 이전의 미게시/새 PR 미승인 표시는 당시 기록이며, 병합·배포 금지는 유지해요.

게시 코드 `e7163aa`의 직접 부모가 develop `e5697e2`이고 source `b6355a0`가 조상이 아님을 확인했어요. [PR69](https://github.com/Lab678-Hackathon/lab678/pull/69)는 open/미병합이며 [게시 기록](docs/development/agent-engine-publication.md)과 [이슈67](https://github.com/Lab678-Hackathon/lab678/issues/67)에 설계·프론트 최소 변경·검증·한계를 정리했어요. 이후 추가 개발·병합·배포는 이 게시 요청에서 추정하지 않아요.

`dj/agent` 작업을 이어갈 때는 [현재 상태와 다음 할 일](docs/development/current-state.md)을 먼저 확인해요. [저장소 색인](docs/development/repo_index.md)·[기능/함수 역색인](docs/development/repo_reverse_index.md)·[구조](docs/development/repo_tree.md)로 파일을 좁히고, 필요한 경우에만 [개발 맥락](docs/development/README.md)과 [대화·작업 기록](docs/development/discussion-log.md)의 해당 부분을 읽어요. 공통 운영 규칙은 계속 `TEAM_WORKFLOW.md`를 기준으로 삼아요.

김동조님은 완료한 작업을 작업 단위로 커밋하도록 상시 요청했어요. 이 요청에 따라 `dj/agent`에서 작업별로 커밋하며, push는 별도 명시 요청이 있을 때만 해요.

커밋 메시지는 작업 완료 후 사용자에게 출력하는 보고문 전체를 요약하거나 바꾸지 않고 그대로 기록해요. 이 최신 사용자 지시를 짧은 커밋 메시지 권장보다 우선해요.

## 개인 작업 승인 절차 — 2026-11-01 사용자 명시

- **조사·원인 분석 → 개발계획 → 구체적인 실시계획 → 사용자 검토·보완 → 명시적 허락 → 승인된 범위의 실시·검증** 순서를 지켜요. 상세 기준은 [구현 전 승인 절차](docs/development/engineering-loop.md#구현-전-승인-절차--필수)를 따라요.
- 승인 전에는 조사·계획·기록만 해요. 개선 의견, 예시 대화, “좋겠다”, 진행 상황 질문, 자유 형식 답변을 구현 허락으로 해석하지 않아요. 이전의 “분석만” 또는 수정 금지를 임의로 해제하지 않아요.
- 실시계획에 대상 파일·담당·허용/제외 범위·검증·복구 방법을 적고, 사용자가 무엇을 허락했는지 원문 근거와 함께 기록해요. 승인된 동일 범위는 계속 진행하되 범위가 달라지면 다시 허락받아요.
- **프론트 수정 금지 해제:** 2026-11-01 사용자가 “그냥 프론트 코드도 수정하는 걸로 바꾸자 ... 나중에 이슈 PR날리면 팀장이 취사 선택”이라고 명시했어요. `dj/agent`에서 계획에 따라 프론트 수정도 검토할 수 있어요. 기존 UI/UX를 존중하고 팀장의 최종 선택을 전제로 해요. 이슈·PR 생성, push·병합·배포는 별도 요청 없이 하지 않아요.
- 현재 승인된 실제 이식 작업은 새 `dj/develop`에서 해요. `dj/agent`는 원본/명세 보존 브랜치로 두고 `main`·`develop` 변경, 원격 브랜치 강제 교체, 병합·배포 권한을 이식 승인에서 추정하지 않아요.
- 하네스 통과·루프 시작·완료 작업의 커밋 상시 요청은 구현 승인이 아니에요. 현재 하네스는 사용자 허락을 기술적으로 강제하는 장치가 아니므로 승인 확인을 생략하지 않아요.

## 작업 계획·색인·진행 보고

- 작업마다 세부 계획과 단계별 체크표를 만들고 실행 전·후 현재 상태를 출력해요. 이번 도구 작업은 [진행 체크표](docs/development/tooling-progress.md)를 따라요. 이후 작업은 이 형식으로 별도 체크표를 만들어요.
- 새 파일·기능·함수의 개요와 docstring/JSDoc, 기능→파일 분류를 작성하고 저장소 색인과 utils 색인을 갱신해요. 생성 규칙·명령·한계는 [utils/README.md](utils/README.md)를 따라요.
- 대화 정정·방향 변경·작업 종료·인계 때 `docs/development/state.json`을 갱신해 현재 목표·승인 범위·완료·진행·다음 행동·미정을 압축해요. 상세 이력과 전체 완료 보고문은 보존해요.
- [검증 루프](docs/development/engineering-loop.md)에 따라 근거가 있는 최소 수정만 반복하고 한도·실패·미실시를 기록해요. 커밋할 때마다 변경 내용과 검증 결과를 보고해요. 감시기는 생성 문서만 갱신하고 자동 커밋·push는 하지 않아요.

## 이전 코드 참조

재사용 전 [두 브랜치 읽기·경량화 가이드](docs/development/konnect-reuse-reading-guide.md)를 확인해요. `framework`는 경량 범용 기반으로 `framework_doc/` 분석·색인을 먼저, `konnect`는 이전 완성 기능으로 `study/` 분석·색인을 먼저 읽고 필요한 소스·테스트만 대조해요. Google 로그인·Supabase·다중 LLM 호출은 이번 서비스의 필수 전제로 삼지 않아요. 최신 사용자 지시·확정 요구에 맞춰 선택하고 아직 서비스 이식은 시작하지 않았어요.
