# LAB678 · 에이전트 개발 문서 안내

갱신: 2026-11-01 · 이 문서의 브랜치 **`dj/develop`** · 역할: **깨끗한 develop에 엔진과 필수 화면 접점을 선택 이식한 검토본**.

## 현재 기준과 두 브랜치

| 구분 | 기준과 읽는 목적 |
|---|---|
| 원본 `dj/agent` | 검증 코드 `b6355a0`, 원본 명세 게시 `d541ea5`. 개선 설계와 원본 구현·실패/검증 근거를 보존 |
| 이식본 `dj/develop` | 검증 코드 `e7163aa`, 게시 기록 `ed923aa`. 코드 커밋의 직접 부모는 develop `e5697e2`. 원본 전체를 merge하지 않고 엔진과 필수 접점을 선택 이식 |
| [이슈 #67](https://github.com/Lab678-Hackathon/lab678/issues/67) | 현재 dj/develop 중심의 설계·기획 의도·계약·프론트 비교·검증·한계 17절. 원본의 전체 이력과 동일한 문서가 아님 |
| [PR #69](https://github.com/Lab678-Hackathon/lab678/pull/69) | dj/develop → develop 검토 요청. 확인 시 open/미병합. 게시 당시 기준을 기록하며 이후 상태는 GitHub에서 재확인 |

이번 문서 갱신의 기준 HEAD는 `ed923aa`이고 제품 검증 기준은 `e7163aa`다. 문서 수정 자체를 모델·기기·배포 재검증으로 간주하지 않는다. `dj/agent`의 후속 코드가 이미 병합된 PR68에 소급 포함됐다고 설명하지 않는다.

## 먼저 읽을 문서

1. [현재 상태와 다음 할 일](current-state.md): 이 브랜치의 역할·승인 범위·완료·다음 행동. 실제 Git 상태와 함께 읽는다.
2. [이식 계획](agent-engine-migration-plan.md) → [실행 체크리스트](agent-engine-port-progress.md) → [게시 결과](agent-engine-publication.md) 순서로 읽는다. [원본 개발 명세](agent-implementation-spec.md)는 원본 파일맵·성적을 보존한 참고이며 아래 대상 차이를 함께 읽는다.
3. [실행·API·검증 안내](team-backend-guide.md): 5173 프론트/8765 백엔드, 키·CORS·기록 모드의 범위, 재현 방법.
4. [이번 문서 갱신 체크리스트](documentation-refresh-progress.md): 현행 안내와 이력의 구분·문서 검증·게시 범위.
5. [현재 후속 작업](tasks.md), [팀 검토 체크리스트](team-integration-checklist.md): 구현 완료와 실제 기기/제품 검토 대기를 구분한다.

파일은 [저장소 색인](repo_index.md)·[기능/함수 역색인](repo_reverse_index.md)·[구조](repo_tree.md)로 좁혀 찾는다. 의미 통합·정책·실제 조회·선택 권한과 프론트 연결을 순서대로 검토한다.

## 이 브랜치의 구현과 검증

- 실행 진입점: `backend/agent_v3.py`. 세션 전송/화면 접점은 `frontend/js/agent-session.js` 및 기존 chat/place 연결부다.
- 기록된 코드 검증: **backend 241/241 · HTTP/store/DOM 23/23 · legacy 상태 15/15**. 자동 HTTP/DOM 검사는 실제 연결을 통과하되 모델·외부 공급자·음성 장치는 fixture다.
- 도구 테스트 26개 PASS. 전체 하네스는 기준부터 있던 docstring 7건으로 FAIL이며 문서·색인 정합과 별개다.
- 원본의 실모델 B 34/60·C 25/30, C 원천 12/12는 당시 호출 예산 사용량이다. 이식본의 새 성공률/시험 성적으로 옮기거나 합산하지 않는다.
- 대상 실모델·외부 원천·마이크/GPS·시각 QA 추가 실행은 없었다. 사용자 개선 체감 피드백과 모든 기기 QA 완료를 구분한다.

원본 전체 프론트 변경은 같은 e569 기준 1,073행, 이식본은 신규 세션 모듈 132줄을 포함해 662행이다. 이식본 HTML은 출발지 dialog 10줄, CSS는 전용 12줄을 추가했다. 프론트 무변경을 뜻하지 않으며 diff 행수는 품질 점수가 아니다.

## 제품·운영·이력의 경계

현행 기획은 [기획 안내](../planning/README.md)의 [PRD v0.7.0](../planning/PRD.md)·[화면명세 v0.3.0](../planning/Lab_678_MVP_화면명세서.md)다. 날짜 없는 콘텐츠 탐색/임시 선택과 방문 근거 정책의 관계는 팀 검토 대상으로 남겼으며 기획 정본을 임의 개정하지 않았다.

장소·가격·시간·ID·좌표는 실제 도구/코드가 판정하고 LLM은 의미·원문 관련성·설명만 맡는다. 영화관 위치는 제공하지만 작품·상영표·예약은 미연동이다. 행사 기간이 방문 날짜의 운영/좌석을 보장하지 않는다. 메모리 store는 단일 프로세스이며 로그인·DB·재시작을 넘는 exactly-once는 추가하지 않았다.

공통 운영은 [TEAM_WORKFLOW](../../TEAM_WORKFLOW.md), 승인 절차는 [engineering-loop](engineering-loop.md), 도구는 [utils 안내](../../utils/README.md)를 따른다. 이번 문서 갱신·두 브랜치 push는 사용자 요청 범위이며 main/develop 변경·병합·배포는 포함하지 않는다.

과거 기록은 [10/31 개발 맥락](development-context-20261031.md), [10/31 실행 안내](team-backend-guide-20261031.md), [discussion-log](discussion-log.md), [reports](reports/)에 보존했다. 역사 문서의 ‘미구현/대기/미push’ 문장을 현재 상태로 사용하지 않는다. `.local`과 `plan_dj`의 개인 자료는 팀이 실행에 의존할 공개 문서가 아니다.
