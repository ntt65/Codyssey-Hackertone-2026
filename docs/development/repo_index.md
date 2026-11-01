# 저장소 파일·기능 색인

자동 생성. 생성 문서·비밀값·의존성 제외 규칙은 utils/harness.json과 utils/README.md를 따른다.
Python 함수·클래스는 AST, JS/TS는 이름 있는 선언·화살표 함수 후보만 정규식으로 찾는다. 익명·메서드 등은 완전성 미보장.
개요가 부족한 파일은 의미를 추측하지 않는다. 기능 분류는 harness.json의 명시적 매핑이다.

| 파일 | 개요 | 상태 / 해시 |
|---|---|---|
| [.env.example](../../.env.example) | 설정·자료 파일; 필요할 때 원문 확인 | `815ba0e63859` |
| [.github/ISSUE_TEMPLATE/bug.md](../../.github/ISSUE_TEMPLATE/bug.md) | --- | `4864828de1ee` |
| [.github/ISSUE_TEMPLATE/task.md](../../.github/ISSUE_TEMPLATE/task.md) | --- | `1ee33bbd2c25` |
| [.github/pull_request_template.md](../../.github/pull_request_template.md) | ## 무엇을 했나요 | `ec68f1c48e6b` |
| [.gitignore](../../.gitignore) | 설정·자료 파일; 필요할 때 원문 확인 | `77b6eb2fdbf9` |
| [AGENTS.md](../../AGENTS.md) | Lab678 · AI 작업 안내 | `f59ccf400bff` |
| [CLAUDE.md](../../CLAUDE.md) | @AGENTS.md | `a853633c4e5c` |
| [GEMINI.md](../../GEMINI.md) | @AGENTS.md | `a853633c4e5c` |
| [README.md](../../README.md) | 오늘 나들이 · Lab678 | `1d6a865500c1` |
| [TEAM_WORKFLOW.md](../../TEAM_WORKFLOW.md) | 678 Lab · TEAM_WORKFLOW | `bbe50fd59065` |
| [backend/AGENTS.md](../../backend/AGENTS.md) | backend 작업 | `15ed2f76becf` |
| [backend/README.md](../../backend/README.md) | backend | `424d271d4f1b` |
| [backend/chat_conditions.py](../../backend/chat_conditions.py) | AI 해석 결과를 추천 조건 초안으로 병합한다. 네트워크·저장·추천 실행은 하지 않는다. | `c8fca428da00` |
| [backend/chat_grounding.py](../../backend/chat_grounding.py) | 검증 가능한 발화 근거만 조건에 반영한다. 외부 호출·저장·행사 사실 판정은 하지 않는다. | `b957b102350c` |
| [backend/chat_prompt.py](../../backend/chat_prompt.py) | 대화 조건 후보와 이번 발화 근거를 요청하는 내부 지침. | `674aabe6d4af` |
| [backend/contact.py](../../backend/contact.py) | 행사 문의 전화번호. 서울시 문화포털 행사 상세 페이지의 '문의' 칸에서 번호만 읽어 와요. | `91140f742559` |
| [backend/course.py](../../backend/course.py) | 서울시 후보 최대 다섯 곳의 방문 순서를 비교해 두 곳 도보 일정 하나를 제시한다. | `fc42683c7b44` |
| [backend/culture.env.example](../../backend/culture.env.example) | 설정·자료 파일; 필요할 때 원문 확인 | `255838f205b9` |
| [backend/culture_config.py](../../backend/culture_config.py) | 문화정보 키를 서버 환경/무시된 로컬 파일에서 읽는다. 비밀값을 응답·로그에 내보내지 않는다. | `f9d1551f7b88` |
| [backend/deploy.env.example](../../backend/deploy.env.example) | 설정·자료 파일; 필요할 때 원문 확인 | `01e3d3cec8ed` |
| [backend/local_voice.py](../../backend/local_voice.py) | Windows 개인 시연용. 카드 텍스트를 설치된 한국어 음성으로 WAV 합성한다. | `a36d41d07b14` |
| [backend/location_view.js](../../backend/location_view.js) | 지도 위 내 위치 표시·갱신·중지를 제공한다. 사용자 클릭 후에만 위치 권한을 요청한다. | `89b2538a420e` |
| [backend/map_config.py](../../backend/map_config.py) | 지도 표시용 공개 JavaScript 키만 읽는다. 서버 REST 키와 설정 파일은 공개하지 않는다. | `d6393a77066b` |
| [backend/map_view.js](../../backend/map_view.js) | 카카오 지도 우선 표시와 기존 지도 대체를 제공하는 개인 점검용 어댑터. | `4144865fa817` |
| [backend/microphone_meter.js](../../backend/microphone_meter.js) | 실제 마이크 PCM 입력의 RMS/dBFS를 측정한다. 원본 음성 저장/전송·스피커 재생은 하지 않는다. | `3598dfeffac3` |
| [backend/naito_chat.py](../../backend/naito_chat.py) | Naito 단일 조건 추출 호출. 키/대화 원문은 기록하지 않고 실패 시 기존 초안을 유지한다. | `ee8efaf07b55` |
| [backend/outing.py](../../backend/outing.py) | 서울시 분류별 공개 후보에서 날짜·시간·대화 선호를 확인해 추천한다. | `b904be688105` |
| [backend/places.py](../../backend/places.py) | 출발지 선택용 카카오 장소명/주소 검색. 사용자 검색어·키·원문 응답은 저장하지 않는다. | `15ca7cc32b99` |
| [backend/preferences.py](../../backend/preferences.py) | 대화 선호의 형식과 공식 행사 사실 기반 선별. AI가 가격·경로 사실을 만들지 않는다. | `9255a02ce149` |
| [backend/preview.html](../../backend/preview.html) | 설정·자료 파일; 필요할 때 원문 확인 | `bc7fe2a17f11` |
| [backend/preview.py](../../backend/preview.py) | 동조 개인용 로컬 추천 점검 화면. python backend/preview.py로 시작한다. | `26d2068a9ca0` |
| [backend/preview_meter.js](../../backend/preview_meter.js) | 기존 점검 화면에서도 실제 마이크 입력만 독립적으로 점검한다. STT 성공으로 표시하지 않는다. | `bf80fbd716f2` |
| [backend/team_app.py](../../backend/team_app.py) | 검증한 로컬 팀 프론트를 /app/에서 제공한다. 선택 파일·비밀값·저장소 전체를 공개하지 않는다. | `caeddc220712` |
| [backend/team_chat.js](../../backend/team_chat.js) | 팀 프론트 164cd40의 공통 자동 대화 모듈. 최종 반영 전 담당 확인용이다. | `2c96f8eb8ec0` |
| [backend/team_culture.js](../../backend/team_culture.js) | 문화정보 출처 선택·표시. 팀 복사본과 인계 패키지에서 사용하는 독립 모듈. | `f512b56f4fed` |
| [backend/team_preferences.js](../../backend/team_preferences.js) | 로컬 팀 화면의 대화 선호를 최종 확인·실제 추천 요청에 연결한다. 담당 원본에는 미반영. | `290c391004ce` |
| [backend/team_voice_actions.js](../../backend/team_voice_actions.js) | 공통 음성 조작. 앱에 이미 있는 화면과 현재 후보 ID만 사용하며 URL/행사 사실을 만들지 않는다. | `5884c686c079` |
| [backend/test_agent_integration.py](../../backend/test_agent_integration.py) | 실제 로컬 HTTP 처리기와 모의 공급자로 대화 계약 및 CORS를 검증한다. | `af9edb28f503` |
| [backend/test_chat_conditions.py](../../backend/test_chat_conditions.py) | 실제 AI를 호출하지 않는 조건 병합 테스트. 동의·최신 입력·사실 경계를 검증한다. | `d8f45e130ede` |
| [backend/test_chat_grounding.py](../../backend/test_chat_grounding.py) | 실제 모델 호출 없이 발화 근거와 시간 판단의 안전 경계를 검증한다. | `0d9dafec1fbd` |
| [backend/test_contact.py](../../backend/test_contact.py) | 개요 없음 | `9dfdbadbfe7f` |
| [backend/test_course.py](../../backend/test_course.py) | 두 곳 도보 일정의 마감 경계·휴관 원문·결측·방문 순서를 검사한다. | `94dbe388fa2a` |
| [backend/test_culture_sources.py](../../backend/test_culture_sources.py) | 문화정보 키/조회 범위와 국문 장소의 사실·오류 경계를 모의 응답으로 검사한다. | `9b0e158d3e3a` |
| [backend/test_deployment_keys.py](../../backend/test_deployment_keys.py) | 배포 환경변수가 개인 로컬 키 파일보다 우선하는지 가짜 키로 검사한다. 외부 호출/실제 키 조회 없음. | `4e820f2d34cc` |
| [backend/test_map_config.py](../../backend/test_map_config.py) | 지도 공개 설정이 JS 키만 노출하고 서버 키·잘못된 입력을 배제하는지 검증한다. | `00c375b43f69` |
| [backend/test_naito_chat.py](../../backend/test_naito_chat.py) | Naito 모의 응답/장애와 HTTP 연결 경계를 검사한다. 실제 서비스 성공을 뜻하지 않는다. | `d2ae168ae7b3` |
| [backend/test_outing.py](../../backend/test_outing.py) | 서울시 공개 응답 재생으로 입력·선별·결측·실패를 검사한다. | `4f76676a4a52` |
| [backend/test_places.py](../../backend/test_places.py) | 장소/주소 검색의 입력·좌표·실제0건·공급자 장애·비밀값 노출 방지 회귀. | `8791dc24d48a` |
| [backend/test_preferences.py](../../backend/test_preferences.py) | 대화→조건→추천 경계. 복수 관심사·제외·가격 미확인·확정값 보호를 재현한다. | `fcdb9301848c` |
| [backend/test_preview.py](../../backend/test_preview.py) | HTTP 처리기의 입력 오류 계약과 route/course 호환을 외부 조회 없이 검증한다. | `0cffec5946b6` |
| [backend/test_team_app.py](../../backend/test_team_app.py) | 같은 서버 앱 서빙의 경로 제한·미설정·정적 자산만 검사한다. 외부 API를 호출하지 않는다. | `a770a41a112e` |
| [backend/test_transit.py](../../backend/test_transit.py) | 실제 노선 성공과 구분한 대중교통 어댑터 단위 검증. 가상 수치로 응답/오류 경계를 검사한다. | `a4610c4c9b6e` |
| [backend/test_walking.py](../../backend/test_walking.py) | 한국어 경로 단계와 지도 좌표가 같은 응답을 사용하는지 검증한다. | `c93d16baf2e1` |
| [backend/tour_places.py](../../backend/tour_places.py) | 국문 TourAPI 문화시설 조회. 상설 장소를 특정 날짜의 공연/전시로 간주하지 않는다. | `32d240c5d533` |
| [backend/transit.py](../../backend/transit.py) | 개인 점검용 카카오 대중교통 텍스트 안내. 키는 서버에서만 읽고 원문 응답은 저장하지 않는다. | `e64929bf1612` |
| [backend/voice_session.js](../../backend/voice_session.js) | 횟수와 무응답 시간으로 제한된 브라우저 음성 대화. 시작 클릭 없이 재생/녹음하지 않는다. | `35ba6882994d` |
| [backend/walking.py](../../backend/walking.py) | 개인 점검 화면에서 선택한 행사장 두 곳의 Valhalla 보행 경로를 조회한다. | `fedc1567e347` |
| [design/AGENTS.md](../../design/AGENTS.md) | design 작업 | `57262504e6ff` |
| [design/README.md](../../design/README.md) | design | `e8cd21971ef0` |
| [docs/AGENTS.md](../../docs/AGENTS.md) | 문서 작업 | `6943f61f8205` |
| [docs/README.md](../../docs/README.md) | docs | `6f5e3f0160f6` |
| [docs/development/README.md](../../docs/development/README.md) | LAB678 · 김동조 개발 작업 맥락 | `fefb130a8df0` |
| [docs/development/agent-remediation-review.md](../../docs/development/agent-remediation-review.md) | 대화·추천 에이전트 개선 및 재검토 자료 | `4fd85d5cf104` |
| [docs/development/automatic-voice.md](../../docs/development/automatic-voice.md) | 자동 음성 대화·종료 설정 | `c953304f4258` |
| [docs/development/chat-conditions.md](../../docs/development/chat-conditions.md) | 대화 조건 처리 코어와 연결 제안 | `99996fc7f1fc` |
| [docs/development/chat-ui-handoff.md](../../docs/development/chat-ui-handoff.md) | 팀 화면 채팅 연결 · 로컬 검증과 인계 | `969cfd58f695` |
| [docs/development/conversation-validation.md](../../docs/development/conversation-validation.md) | 자연어 대화·추천 추가 구간 검증 | `febb45abfa52` |
| [docs/development/course-alternatives-progress.md](../../docs/development/course-alternatives-progress.md) | 시간 부족 → 동의 → 대안 선택 진행표 | `a662e7da1bee` |
| [docs/development/culture-sources.md](../../docs/development/culture-sources.md) | 서울시 조회 확대와 국문 문화시설 연결 | `27085042b590` |
| [docs/development/current-state.md](../../docs/development/current-state.md) | 현재 상태와 다음 할 일 | `e880ac27f028` |
| [docs/development/demo-login-server-progress.md](../../docs/development/demo-login-server-progress.md) | 데모 로그인·해커톤 서버 검토 진행표 | `ca878f31c5f8` |
| [docs/development/demo-profile-design.md](../../docs/development/demo-profile-design.md) | 인증 없는 이용·체험 프로필·로컬 저장 설계안 | `87e1d5b21681` |
| [docs/development/deployment-keys.md](../../docs/development/deployment-keys.md) | 공공데이터·Naito 배포 키 처리 | `6666b0215a8f` |
| [docs/development/discussion-log.md](../../docs/development/discussion-log.md) | LAB678 · 김동조 대화·작업 기록 | `db7b3688c34a` |
| [docs/development/engineering-loop.md](../../docs/development/engineering-loop.md) | 개발 도구·반복 검증·컨텍스트 운영 | `8503cbd5c4f0` |
| [docs/development/examples/course-selected-place.live.json](../../docs/development/examples/course-selected-place.live.json) | 구조화 설정·상태 데이터 | `2c89a9a3ae68` |
| [docs/development/examples/demo-users.sample.json](../../docs/development/examples/demo-users.sample.json) | 구조화 설정·상태 데이터 | `f148990a7ff7` |
| [docs/development/examples/naito-chat.live.json](../../docs/development/examples/naito-chat.live.json) | 구조화 설정·상태 데이터 | `0dfca98bb171` |
| [docs/development/examples/outing-request.json](../../docs/development/examples/outing-request.json) | 구조화 설정·상태 데이터 | `3fc7504a23dd` |
| [docs/development/examples/outing-response.json](../../docs/development/examples/outing-response.json) | 구조화 설정·상태 데이터 | `1e10713e15a7` |
| [docs/development/examples/place-search.address.live.json](../../docs/development/examples/place-search.address.live.json) | 구조화 설정·상태 데이터 | `2aca35a6dd39` |
| [docs/development/examples/place-search.keyword.live.json](../../docs/development/examples/place-search.keyword.live.json) | 구조화 설정·상태 데이터 | `f9b69124ae00` |
| [docs/development/examples/qa01-request.recorded.json](../../docs/development/examples/qa01-request.recorded.json) | 구조화 설정·상태 데이터 | `5e7257028c5c` |
| [docs/development/examples/recommend-response.recorded.json](../../docs/development/examples/recommend-response.recorded.json) | 구조화 설정·상태 데이터 | `3e7b476fdf1a` |
| [docs/development/examples/recommend-selected-place.live.json](../../docs/development/examples/recommend-selected-place.live.json) | 구조화 설정·상태 데이터 | `efb567e18ab3` |
| [docs/development/examples/seoul-events.capture.json](../../docs/development/examples/seoul-events.capture.json) | 구조화 설정·상태 데이터 | `1bb3cf6f854e` |
| [docs/development/frontend-chat-package.md](../../docs/development/frontend-chat-package.md) | 팀 프론트 채팅·자동 추천 적용 패키지 | `63176c42b68e` |
| [docs/development/hackathon-server-usage-review.md](../../docs/development/hackathon-server-usage-review.md) | 해커톤 GPU/일반 서버 활용 검토 | `6f9d563a603a` |
| [docs/development/kakao-map-location.md](../../docs/development/kakao-map-location.md) | 카카오 지도 전환·내 위치 표시 구현 기록 | `5f09316bad27` |
| [docs/development/keyless-routing-review.md](../../docs/development/keyless-routing-review.md) | 키 없는 이동 안내 방식 대조 · 2026-10-31 | `75fdb523ad1e` |
| [docs/development/konnect-reuse-reading-guide.md](../../docs/development/konnect-reuse-reading-guide.md) | KONNECT 재사용 전 읽기·경량화 가이드 | `ec75964b0824` |
| [docs/development/loops/tooling-index.json](../../docs/development/loops/tooling-index.json) | 구조화 설정·상태 데이터 | `21338df780cb` |
| [docs/development/mobility-routing-review.md](../../docs/development/mobility-routing-review.md) | LAB678 · 도보·대중교통 이동 안내 기술검토 | `459a27237290` |
| [docs/development/mvp-plan.md](../../docs/development/mvp-plan.md) | 김동조의 문화외출 MVP 개발 계획 | `5642ac169efe` |
| [docs/development/naito-usage.md](../../docs/development/naito-usage.md) | Naito 사용 안내 · 사용자 제공 자료 보관 | `389a2cdf022a` |
| [docs/development/natural-language-handoff.md](../../docs/development/natural-language-handoff.md) | 자연어 자동 설정·추천 연결 | `50fd9e2ac944` |
| [docs/development/natural-language-recommendation-review.md](../../docs/development/natural-language-recommendation-review.md) | 자연어 중심 추천 · 이전 구현과 현재 구현 비교 | `887c56732be0` |
| [docs/development/next-chat-handoff.md](../../docs/development/next-chat-handoff.md) | 새 채팅 인계 · 2026-10-31 | `6371b77c0171` |
| [docs/development/outing-handoff.md](../../docs/development/outing-handoff.md) | 동조 개발용 추천 인계 초안 | `011173a93c92` |
| [docs/development/place-search-api.md](../../docs/development/place-search-api.md) | 출발지 검색과 첫 프론트 연결 안내 | `516b447a35e2` |
| [docs/development/planning-doc-refresh-progress.md](../../docs/development/planning-doc-refresh-progress.md) | 기획 정본 v0.7.0·화면명세 v0.3.0 갱신 체크표 | `2e1a7d682bcf` |
| [docs/development/qa-chat/chat-conflict.png](../../docs/development/qa-chat/chat-conflict.png) | 설정·자료 파일; 필요할 때 원문 확인 | `4ebd31bbf62d` |
| [docs/development/qa-chat/chat-to-detail.png](../../docs/development/qa-chat/chat-to-detail.png) | 설정·자료 파일; 필요할 때 원문 확인 | `721da4d00e8d` |
| [docs/development/qa-chat/result.json](../../docs/development/qa-chat/result.json) | 구조화 설정·상태 데이터 | `916661ad0e7d` |
| [docs/development/qa-conversation/edges.json](../../docs/development/qa-conversation/edges.json) | 구조화 설정·상태 데이터 | `d34edb3a6733` |
| [docs/development/qa-conversation/recovery.json](../../docs/development/qa-conversation/recovery.json) | 구조화 설정·상태 데이터 | `e3efbcb1a824` |
| [docs/development/qa-culture/authenticated-check.json](../../docs/development/qa-culture/authenticated-check.json) | 구조화 설정·상태 데이터 | `43d8efde0c92` |
| [docs/development/qa-culture/initial-check.json](../../docs/development/qa-culture/initial-check.json) | 구조화 설정·상태 데이터 | `3ada97ab1f31` |
| [docs/development/qa-culture/tour-key-check.json](../../docs/development/qa-culture/tour-key-check.json) | 구조화 설정·상태 데이터 | `9e8ffcb98130` |
| [docs/development/qa-culture/tour-live-check.json](../../docs/development/qa-culture/tour-live-check.json) | 구조화 설정·상태 데이터 | `7be68f3d5f1c` |
| [docs/development/qa-handoff/manifest.json](../../docs/development/qa-handoff/manifest.json) | 구조화 설정·상태 데이터 | `a4914fbfd248` |
| [docs/development/qa-handoff/natural-flow.json](../../docs/development/qa-handoff/natural-flow.json) | 구조화 설정·상태 데이터 | `92da7446d1f4` |
| [docs/development/qa-handoff/recovery.json](../../docs/development/qa-handoff/recovery.json) | 구조화 설정·상태 데이터 | `e0bfb0cd955b` |
| [docs/development/qa-microphone-toggle/navigation-checks.json](../../docs/development/qa-microphone-toggle/navigation-checks.json) | 구조화 설정·상태 데이터 | `f956569395cb` |
| [docs/development/qa-microphone-toggle/session-checks.json](../../docs/development/qa-microphone-toggle/session-checks.json) | 구조화 설정·상태 데이터 | `7c4f0540f315` |
| [docs/development/qa-natural/confirmation.png](../../docs/development/qa-natural/confirmation.png) | 설정·자료 파일; 필요할 때 원문 확인 | `960cb0c107d1` |
| [docs/development/qa-natural/result.json](../../docs/development/qa-natural/result.json) | 구조화 설정·상태 데이터 | `e0f0f86da933` |
| [docs/development/qa-natural/results.png](../../docs/development/qa-natural/results.png) | 설정·자료 파일; 필요할 때 원문 확인 | `6c3b486a2a8c` |
| [docs/development/qa-services/culture-ui-first-run.json](../../docs/development/qa-services/culture-ui-first-run.json) | 구조화 설정·상태 데이터 | `ddc2cedec22f` |
| [docs/development/qa-services/culture-ui.json](../../docs/development/qa-services/culture-ui.json) | 구조화 설정·상태 데이터 | `60cce7681013` |
| [docs/development/qa-services/keys.json](../../docs/development/qa-services/keys.json) | 구조화 설정·상태 데이터 | `b93a30476d11` |
| [docs/development/qa-services/manifest.json](../../docs/development/qa-services/manifest.json) | 구조화 설정·상태 데이터 | `933deea6d386` |
| [docs/development/qa-services/map-check.json](../../docs/development/qa-services/map-check.json) | 구조화 설정·상태 데이터 | `22cdffba7735` |
| [docs/development/qa-simple-settings/diagnostic.json](../../docs/development/qa-simple-settings/diagnostic.json) | 구조화 설정·상태 데이터 | `7c0dbc27192f` |
| [docs/development/qa-simple-settings/meter.json](../../docs/development/qa-simple-settings/meter.json) | 구조화 설정·상태 데이터 | `df6b312ce5c2` |
| [docs/development/qa-simple-settings/navigation.json](../../docs/development/qa-simple-settings/navigation.json) | 구조화 설정·상태 데이터 | `b4b15ab29e94` |
| [docs/development/qa-simple-settings/summary.json](../../docs/development/qa-simple-settings/summary.json) | 구조화 설정·상태 데이터 | `33d3e0a74afa` |
| [docs/development/qa-simple-settings/voice.json](../../docs/development/qa-simple-settings/voice.json) | 구조화 설정·상태 데이터 | `879aaac7de22` |
| [docs/development/qa-transit-mobile/ui-checks.json](../../docs/development/qa-transit-mobile/ui-checks.json) | 구조화 설정·상태 데이터 | `4db565c5576c` |
| [docs/development/qa-unified-chat/diagnostic-checks.json](../../docs/development/qa-unified-chat/diagnostic-checks.json) | 구조화 설정·상태 데이터 | `8cb7d9886f12` |
| [docs/development/qa-unified-chat/meter-checks.json](../../docs/development/qa-unified-chat/meter-checks.json) | 구조화 설정·상태 데이터 | `df6b312ce5c2` |
| [docs/development/qa-unified-chat/navigation-checks.json](../../docs/development/qa-unified-chat/navigation-checks.json) | 구조화 설정·상태 데이터 | `a59db1199217` |
| [docs/development/qa-unified-chat/unified-checks.json](../../docs/development/qa-unified-chat/unified-checks.json) | 구조화 설정·상태 데이터 | `2dcc5d04024b` |
| [docs/development/qa-unified-chat/voice-checks.json](../../docs/development/qa-unified-chat/voice-checks.json) | 구조화 설정·상태 데이터 | `e69c5eac50fe` |
| [docs/development/qa-voice-navigation/navigation-checks.json](../../docs/development/qa-voice-navigation/navigation-checks.json) | 구조화 설정·상태 데이터 | `bf75a5ba236e` |
| [docs/development/qa-voice-navigation/session-checks.json](../../docs/development/qa-voice-navigation/session-checks.json) | 구조화 설정·상태 데이터 | `f55c9857e869` |
| [docs/development/qa-voice-session/live-ai-check.json](../../docs/development/qa-voice-session/live-ai-check.json) | 구조화 설정·상태 데이터 | `25db6dc853a5` |
| [docs/development/qa-voice-session/manifest.json](../../docs/development/qa-voice-session/manifest.json) | 구조화 설정·상태 데이터 | `97d4ba1674a9` |
| [docs/development/qa-voice-session/mock-checks.json](../../docs/development/qa-voice-session/mock-checks.json) | 구조화 설정·상태 데이터 | `f55c9857e869` |
| [docs/development/qa-voice-start/diagnostic-checks.json](../../docs/development/qa-voice-start/diagnostic-checks.json) | 구조화 설정·상태 데이터 | `7c0dbc27192f` |
| [docs/development/qa-voice-start/meter-checks.json](../../docs/development/qa-voice-start/meter-checks.json) | 구조화 설정·상태 데이터 | `df6b312ce5c2` |
| [docs/development/qa-voice-start/navigation-checks.json](../../docs/development/qa-voice-start/navigation-checks.json) | 구조화 설정·상태 데이터 | `d7497482802e` |
| [docs/development/qa-voice-start/summary.json](../../docs/development/qa-voice-start/summary.json) | 구조화 설정·상태 데이터 | `05f912871488` |
| [docs/development/qa-voice-start/voice-checks.json](../../docs/development/qa-voice-start/voice-checks.json) | 구조화 설정·상태 데이터 | `879aaac7de22` |
| [docs/development/qa-voice-wave/mock-checks.json](../../docs/development/qa-voice-wave/mock-checks.json) | 구조화 설정·상태 데이터 | `2c739be597f3` |
| [docs/development/qa01-team-connection.md](../../docs/development/qa01-team-connection.md) | QA-01 팀 화면 첫 연결 결과 | `560b3050bcc1` |
| [docs/development/qa01/live-s03.png](../../docs/development/qa01/live-s03.png) | 설정·자료 파일; 필요할 때 원문 확인 | `d2e8cdabdc09` |
| [docs/development/qa01/live-s04.png](../../docs/development/qa01/live-s04.png) | 설정·자료 파일; 필요할 때 원문 확인 | `be287206af0a` |
| [docs/development/qa01/recorded-s03.png](../../docs/development/qa01/recorded-s03.png) | 설정·자료 파일; 필요할 때 원문 확인 | `944df3c97c69` |
| [docs/development/qa01/recorded-s04.png](../../docs/development/qa01/recorded-s04.png) | 설정·자료 파일; 필요할 때 원문 확인 | `55cf50dc3a7a` |
| [docs/development/qa01/result.json](../../docs/development/qa01/result.json) | 구조화 설정·상태 데이터 | `5a0a33f45d70` |
| [docs/development/recommend-api.md](../../docs/development/recommend-api.md) | 추천 API 연결 안내 | `3a2151269f76` |
| [docs/development/release-checklist.md](../../docs/development/release-checklist.md) | 진행 점검·남은 일·공유 체크표 · 2026-10-31 | `d254c622c3af` |
| [docs/development/render-demo-guide.md](../../docs/development/render-demo-guide.md) | Render 단일 서비스 시연 준비 | `c602a7361e22` |
| [docs/development/repo_index.md](../../docs/development/repo_index.md) | 자동 생성 색인 | `generated` |
| [docs/development/repo_reverse_index.md](../../docs/development/repo_reverse_index.md) | 자동 생성 색인 | `generated` |
| [docs/development/repo_tree.md](../../docs/development/repo_tree.md) | 자동 생성 색인 | `generated` |
| [docs/development/reports/2026-10-31-audible-card.md](../../docs/development/reports/2026-10-31-audible-card.md) | 읽기 기능은 구현돼 있었지만, 기존에는 브라우저의 읽기 종료 신호만 확인해서 실제로 소리가 났는지 알 수 없었습니다. **소리가 안 들릴 때 쓸 수 있는 ‘음성 파일로 듣기’를 추가했습니다.** | `78df591fa5f7` |
| [docs/development/reports/2026-10-31-chrome-gugak.md](../../docs/development/reports/2026-10-31-chrome-gugak.md) | **일반 Chrome에서 “국악을 듣고 싶어”라고 말하면 국악 행사 2건이 지도와 카드에 표시되는 흐름을 실기기 확인 완료로 기록했습니다.** 화면의 1번은 서울돈화문국악당의 ‘코공’, 2번은 국립박물관문화재단의 ‘소리: 성덕대왕신종’입니다. | `55128c14b8a4` |
| [docs/development/reports/2026-10-31-chrome-speech.md](../../docs/development/reports/2026-10-31-chrome-speech.md) | **동조님 PC의 일반 Chrome에서 한국어 음성 입력을 확인했습니다.** 버튼을 누른 뒤 1.52초에 발화를 감지했고, 3.51초에 13자를 전사한 뒤 정상 종료했습니다. 시연은 일반 Chrome으로 진행하면 됩니다. | `7eae2e2fcfee` |
| [docs/development/reports/2026-10-31-course-alternatives.md](../../docs/development/reports/2026-10-31-course-alternatives.md) | 시간 부족 안내 뒤에 **동의 → 대안 1·2 → 선택 적용**을 추가했습니다. | `e10c209fabf0` |
| [docs/development/reports/2026-10-31-course-demo-check.md](../../docs/development/reports/2026-10-31-course-demo-check.md) | 보내주신 화면에서 **시간 부족 안내**는 확인됐습니다. 당시 적용된 출발·종료 시각은 화면에 없어 정확한 원인까지 확인하기 어려웠습니다. 이제 결과 상단에 적용한 조건을 표시합니다. | `c308afeadab9` |
| [docs/development/reports/2026-10-31-course-edit.md](../../docs/development/reports/2026-10-31-course-edit.md) | 코스에서 장소 제외와 다시 만들기를 분리했습니다. | `0dddf7259e2a` |
| [docs/development/reports/2026-10-31-current-prd-sync.md](../../docs/development/reports/2026-10-31-current-prd-sync.md) | 구버전 PRD를 개인용으로 따로 보관하지 않도록 정리했습니다. | `0b7e39f43bef` |
| [docs/development/reports/2026-10-31-demo-server-reuse.md](../../docs/development/reports/2026-10-31-demo-server-reuse.md) | 인증·DB 간소화안, 두 브랜치 재사용 순서, 해커톤 서버 활용안을 기록하고 커밋했습니다. | `64c2078b9f0a` |
| [docs/development/reports/2026-10-31-develop-sync.md](../../docs/development/reports/2026-10-31-develop-sync.md) | 최신 develop을 받아 dj/develop에 동기화했습니다. | `bc7c723fe243` |
| [docs/development/reports/2026-10-31-direct-push.md](../../docs/development/reports/2026-10-31-direct-push.md) | develop 직접 반영 사전 검증과 공유 상태를 기록했습니다. | `f4a571c67deb` |
| [docs/development/reports/2026-10-31-directions.md](../../docs/development/reports/2026-10-31-directions.md) | **추천 → 선택 → 경로안내** 구간을 연결했습니다. | `53bf5d622189` |
| [docs/development/reports/2026-10-31-discord-status-checklist.md](../../docs/development/reports/2026-10-31-discord-status-checklist.md) | 디스코드에 붙여 넣을 공유 초안입니다. | `917835065e4d` |
| [docs/development/reports/2026-10-31-events.md](../../docs/development/reports/2026-10-31-events.md) | 서울시 문화행사 API에서 10월 31일 전시 5건과 전체 분류 5건을 조회해 기록했습니다. 상세 요금이 0원인 전시와 빈 전시를 모두 확인했고, 행사 ID·좌표·조회시각을 보존했습니다. 청량리역 출발 좌표도 원자료와 대조했습니다. 다음은 이 기록과  | `f41b4eefb48e` |
| [docs/development/reports/2026-10-31-frontend-ready.md](../../docs/development/reports/2026-10-31-frontend-ready.md) | 팀 화면이 완성되기 전에 연결할 준비를 마쳤습니다. | `4c3c048e75f3` |
| [docs/development/reports/2026-10-31-guide-push-ready.md](../../docs/development/reports/2026-10-31-guide-push-ready.md) | 참조 방법을 [개발 참조·실행 안내](D:/git/lab678/docs/development/team-backend-guide.md)에 저장하고, **저장소 README·백엔드 README·개발 README에서 찾을 수 있게 연결했습니다.** | `bab37a115379` |
| [docs/development/reports/2026-10-31-input-contract.md](../../docs/development/reports/2026-10-31-input-contract.md) | 진행표의 다음 단계인 입력 검증과 API 전달 준비를 마쳤습니다. | `9cc04ab6bf02` |
| [docs/development/reports/2026-10-31-kakao-live-check.md](../../docs/development/reports/2026-10-31-kakao-live-check.md) | 카카오 도메인 등록 후 실제 지도 연결을 확인했습니다. | `682c76caad0b` |
| [docs/development/reports/2026-10-31-kakao-map.md](../../docs/development/reports/2026-10-31-kakao-map.md) | 카카오 지도로 전환할 수 있도록 지도 표시 코드를 연결했습니다. | `506bcd8cb45e` |
| [docs/development/reports/2026-10-31-keyless-routing-review.md](../../docs/development/reports/2026-10-31-keyless-routing-review.md) | **도보는 우리도 이미 API 키 없이 가져옵니다. 다만 현재 도보 서버로 서울 대중교통까지 조회할 수는 없었습니다.** 제시하신 다른 앱의 방식은 참고할 부분이 있지만, 설명만으로 “정확한 대중교통·무장애 길찾기”가 구현됐다고 판단하기는 어렵습니다. | `82c35b650861` |
| [docs/development/reports/2026-10-31-konnect-preview.md](../../docs/development/reports/2026-10-31-konnect-preview.md) | 동조님 점검 화면에 **KONNECT의 홈 → 조건 입력 → 지도·가로 카드** 구성을 반영했습니다. 열어 둔 탭을 새로고침하고 **‘나들이 찾기’**를 누르면 됩니다. [점검 화면 열기](http://127.0.0.1:8765/) | `e5b8bc2e6408` |
| [docs/development/reports/2026-10-31-live-location.md](../../docs/development/reports/2026-10-31-live-location.md) | 지도에 내 위치 표시와 이동 중 갱신·중지를 추가했습니다. | `e1cdac5c5f92` |
| [docs/development/reports/2026-10-31-local-plan-folder.md](../../docs/development/reports/2026-10-31-local-plan-folder.md) | 개인용 [plan_dj](D:/git/lab678/plan_dj) 폴더를 만들고 **Git 업로드와 자동 색인에서 제외**했습니다. 제외 설정을 검증하고 커밋했습니다. | `0e98567ce29a` |
| [docs/development/reports/2026-10-31-mobility-review.md](../../docs/development/reports/2026-10-31-mobility-review.md) | 도보·대중교통 기술검토서와 동조님 개발 할 일을 추가했습니다. | `81af98fd50b8` |
| [docs/development/reports/2026-10-31-mvp-plan.md](../../docs/development/reports/2026-10-31-mvp-plan.md) | 동조님 MVP 실행계획을 보완해 `dj/develop`에 커밋했습니다. [MVP 실행계획과 단계별 체크표](D:/git/lab678/docs/development/mvp-plan.md) | `666b99ec023e` |
| [docs/development/reports/2026-10-31-personal-attachment-copy.md](../../docs/development/reports/2026-10-31-personal-attachment-copy.md) | 답변 반영했습니다. **첨부 원본의 개인 사본은 `plan_dj`에 보관**합니다. | `4d0637d24a1d` |
| [docs/development/reports/2026-10-31-personal-notes-scope.md](../../docs/development/reports/2026-10-31-personal-notes-scope.md) | `plan_dj`를 **동조님이 저에게 특별히 요청한 개인 사항만 보관하는 폴더**로 정리했습니다. | `5993598693c0` |
| [docs/development/reports/2026-10-31-planning-doc-refresh.md](../../docs/development/reports/2026-10-31-planning-doc-refresh.md) | Lab 678 기획 정본 갱신 완료 보고 | `ae7ccd21a542` |
| [docs/development/reports/2026-10-31-preview-map.md](../../docs/development/reports/2026-10-31-preview-map.md) | **청량리역에서 나들이를 찾아 지도와 카드로 선택하는 첫 흐름이 동작합니다.** 개인 점검 서버를 실행해 두었습니다. [내 PC에서 나들이 찾기 열기](http://127.0.0.1:8765/) | `4a9257d9b522` |
| [docs/development/reports/2026-10-31-preview-speech.md](../../docs/development/reports/2026-10-31-preview-speech.md) | 민규님 대화 덕분에 **v0.5 문서가 아직 보이지 않는 경위**를 파악했습니다. 10월 31일 오전 원격 저장소를 확인했을 때 브랜치는 기존 6개였고, PR은 협업 규칙 관련 #1·#2뿐이었습니다. PRD 문서 5종과 UI·API 최종 합의는 확인  | `2b2e617a1f5e` |
| [docs/development/reports/2026-10-31-preview.md](../../docs/development/reports/2026-10-31-preview.md) | 실데이터 확보에 이어 개인 점검 화면에서 **출발 조건 → 실시간 추천 → 선택 → 조건 변경·재조회**를 연결했습니다. [내 PC에서 나들이 찾기 열기](http://127.0.0.1:8765/) | `80fa1c370c23` |
| [docs/development/reports/2026-10-31-release-ready.md](../../docs/development/reports/2026-10-31-release-ready.md) | 최신 develop을 개인 브랜치에 반영하고 공유 준비를 마쳤습니다. | `a6c9d4400bb7` |
| [docs/development/reports/2026-10-31-render-preparation.md](../../docs/development/reports/2026-10-31-render-preparation.md) | Render에 화면과 서버를 함께 올릴 준비를 마쳤습니다. | `5823a35d5146` |
| [docs/development/reports/2026-10-31-result-preservation.md](../../docs/development/reports/2026-10-31-result-preservation.md) | 연결 준비에 이어 추천 결과가 사라지지 않도록 보완했습니다. | `ad3587f044db` |
| [docs/development/reports/2026-10-31-route-text.md](../../docs/development/reports/2026-10-31-route-text.md) | **경로안내를 앱 안에서 텍스트로 먼저 보도록 바꿨습니다.** | `2509c7caa514` |
| [docs/development/reports/2026-10-31-screen-spec-review.md](../../docs/development/reports/2026-10-31-screen-spec-review.md) | 정민규님 화면명세를 읽고 **원본과 구현 대조 체크표를 `dj/develop`에 저장·커밋했습니다.** | `7e7494014a91` |
| [docs/development/reports/2026-10-31-section-checks.md](../../docs/development/reports/2026-10-31-section-checks.md) | 기능마다 확인을 요청해 같은 점검을 여러 번 하게 했습니다. 앞으로는 구간을 완성하고 제가 먼저 테스트한 뒤, 동조님께 필요한 확인만 최대 3개로 모아 요청하겠습니다. | `1229071d979a` |
| [docs/development/reports/2026-10-31-simple-settings-restore.md](../../docs/development/reports/2026-10-31-simple-settings-restore.md) | 두 번째 화면을 간단한 초기 설정 폼으로 복원했습니다. 자동 대화는 첫 화면에만 표시합니다. | `d02400d1b787` |
| [docs/development/reports/2026-10-31-speaker-check.md](../../docs/development/reports/2026-10-31-speaker-check.md) | **음성 입력 → 국악 추천 → 카드 읽기**까지 동조님 PC에서 확인됐습니다. 스피커 청취를 완료로 표시하고 `dj/develop`에 커밋했습니다. 다음 개발 작업은 두 문화활동을 한 코스로 묶을 수 있도록 **장소 사이의 실제 이동시간을 확인하는  | `5eaa0d5d3ac7` |
| [docs/development/reports/2026-10-31-speech-input-errors.md](../../docs/development/reports/2026-10-31-speech-input-errors.md) | 기존 화면은 여러 오류를 모두 ‘음성 인식 실패’로 표시했습니다. 브라우저가 알려주는 원인과 오류 코드를 표시하도록 수정했습니다. 동조님 PC에서 처음 실패한 원인은 아직 확인되지 않았습니다. | `34a338bdfece` |
| [docs/development/reports/2026-10-31-speech-offline.md](../../docs/development/reports/2026-10-31-speech-offline.md) | 이번 실패에서 먼저 확인할 건 **인터넷 연결**입니다. 13자가 전사된 시도에서는 브라우저 온라인 표시가 `true`였고, 이번에는 **`false`**였습니다. 마이크 권한은 `granted`였지만 캡처가 시작된 지 **2ms 만에** `netwo | `6ca19eb21a54` |
| [docs/development/reports/2026-10-31-speech-trace.md](../../docs/development/reports/2026-10-31-speech-trace.md) | 동조님이 보신 대로 **말할 시간이 생기기 전에 꺼졌습니다.** 마이크 권한은 허용됐지만 캡처가 **197ms 만에 종료**됐고, 발화 시작(`speechstart`)은 기록되지 않았습니다. | `9fe23ca839ce` |
| [docs/development/reports/2026-10-31-spoken-category.md](../../docs/development/reports/2026-10-31-spoken-category.md) | **국악을 말했는데 전시가 나온 문제를 수정했습니다.** 기존에는 음성이 메모에만 들어가서 ‘분류 반영’을 따로 누르지 않으면 기본값인 전시로 검색됐습니다. | `d9106baa3688` |
| [docs/development/reports/2026-10-31-team-backend-guide.md](../../docs/development/reports/2026-10-31-team-backend-guide.md) | [상세 안내문을 저장했습니다](D:/git/lab678/docs/development/team-backend-guide.md). 아래 내용을 팀원과 각자의 LLM에 공유하면 됩니다. 아직 push하지 않아 최신 파일은 로컬에만 있습니다. | `1d77a4c965b1` |
| [docs/development/reports/2026-10-31-team-feedback-review.md](../../docs/development/reports/2026-10-31-team-feedback-review.md) | **지금은 기능 확장보다 팀 UI 연결과 시연 안정화가 우선입니다.** 팀원 질문을 실제 코드와 대조해 [통합 체크표](D:/git/lab678/docs/development/team-integration-checklist.md)에 기록했습니다. 아래 | `a9ca2e0b94e4` |
| [docs/development/reports/2026-10-31-team-requests-record.md](../../docs/development/reports/2026-10-31-team-requests-record.md) | 팀원 요청을 할 일과 작업 우선순위에 기록했습니다. | `1f274e093c89` |
| [docs/development/reports/2026-10-31-tooling-setup.md](../../docs/development/reports/2026-10-31-tooling-setup.md) | 개발 도구·자동 색인·대화 상태 압축을 설정하고 작업 단위로 커밋했습니다. | `920b866a8677` |
| [docs/development/reports/2026-10-31-transit-guide.md](../../docs/development/reports/2026-10-31-transit-guide.md) | **대중교통 안내 화면과 연결 코드를 추가했습니다. 실제 노선 조회는 API 키 연결 대기입니다.** | `26978482f259` |
| [docs/development/reports/2026-10-31-transit-live.md](../../docs/development/reports/2026-10-31-transit-live.md) | **키 연결과 실제 대중교통 조회가 성공했습니다.** | `cfd799873745` |
| [docs/development/reports/2026-10-31-transit-map.md](../../docs/development/reports/2026-10-31-transit-map.md) | 대중교통도 외부 지도로 나가지 않고 앱 안에서 볼 수 있게 했습니다. | `7c1d87071396` |
| [docs/development/reports/2026-10-31-transit-provider-factcheck.md](../../docs/development/reports/2026-10-31-transit-provider-factcheck.md) | **구현 흐름은 타당하지만, 핵심 전제가 오래됐습니다. 우리 상황에서는 카카오부터 실제로 시험하는 게 좋겠습니다.** | `205da681552d` |
| [docs/development/reports/2026-10-31-two-stop-course.md](../../docs/development/reports/2026-10-31-two-stop-course.md) | **두 곳 문화코스**를 구현했습니다. 출발지부터 첫 행사장까지의 도보, 두 행사 사이 이동, 관람시간을 합쳐 방문 순서와 예상 시각을 보여줍니다. | `27a95f3ce6f9` |
| [docs/development/reports/2026-10-31-voice-compact-entry.md](../../docs/development/reports/2026-10-31-voice-compact-entry.md) | 로컬 화면을 반영하고 커밋했습니다. | `302221217d37` |
| [docs/development/reports/2026-10-31-voice-diagnostics-handoff.md](../../docs/development/reports/2026-10-31-voice-diagnostics-handoff.md) | 새 채팅용 [인계 문서·전체 체크표](D:/git/lab678/docs/development/next-chat-handoff.md)와 [현재 상태](D:/git/lab678/docs/development/current-state.md)를 저장했습니다. | `12d6dbac2ee9` |
| [docs/development/reports/2026-10-31-walk-demo.md](../../docs/development/reports/2026-10-31-walk-demo.md) | 동조님 시연 PC에서 **국악 추천 → 행사 선택 → 도보 시간 확인**까지 정상 동작한 것으로 기록했습니다. | `a933333d6e14` |
| [docs/development/reports/2026-10-31-walk.md](../../docs/development/reports/2026-10-31-walk.md) | 두 행사 사이 도보 시간을 추천 화면에서 확인할 수 있습니다. | `ca0e5a18f78b` |
| [docs/development/reports/20261031-conversation-discovery-direction.md](../../docs/development/reports/20261031-conversation-discovery-direction.md) | 짧은 대화로 나들이 선호를 파악하는 방향을 기록했습니다. | `1f4b51a8520b` |
| [docs/development/reports/20261031-naito-chat-prepared.md](../../docs/development/reports/20261031-naito-chat-prepared.md) | Naito 채팅 연결과 조건 보호 로직을 준비했습니다. | `baeb0168da7c` |
| [docs/development/reports/20261031-naito-live-verified.md](../../docs/development/reports/20261031-naito-live-verified.md) | Naito 실제 연결을 확인했습니다. | `e16788c66a66` |
| [docs/development/reports/20261031-natural-language-review.md](../../docs/development/reports/20261031-natural-language-review.md) | 자연어 중심 추천의 이전 구현과 현재 구현을 비교했습니다. | `37730cabc0d2` |
| [docs/development/reports/20261031-place-search-integration.md](../../docs/development/reports/20261031-place-search-integration.md) | 출발지 검색 API와 프론트 연결 자료를 준비했습니다. | `a80f01dcc97e` |
| [docs/development/reports/20261031-push-pr-issue.md](../../docs/development/reports/20261031-push-pr-issue.md) | 최신 백엔드 11개 커밋을 dj/develop에 Push했습니다. | `3997b176db63` |
| [docs/development/reports/20261031-qa01-received.md](../../docs/development/reports/20261031-qa01-received.md) | 기획의 QA-01 기준과 후속 할 일을 기록했습니다. | `a2bbe699a7f5` |
| [docs/development/reports/20261031-team-chat-connected.md](../../docs/development/reports/20261031-team-chat-connected.md) | 팀 화면 복사본에 실제 AI 채팅을 연결했습니다. | `5ca2c00c2742` |
| [docs/development/reports/20261031-team-flow-connected.md](../../docs/development/reports/20261031-team-flow-connected.md) | 희영님 프론트와 백엔드의 첫 연결을 확인했습니다. | `fca80fdf4ac7` |
| [docs/development/reports/20261031-user-preferences-kakao-review.md](../../docs/development/reports/20261031-user-preferences-kakao-review.md) | 사용자 선호 저장과 카카오 로그인 활용 범위를 확인했습니다. | `df79496b6b1f` |
| [docs/development/reports/20261101-agent-cards-d.md](../../docs/development/reports/20261101-agent-cards-d.md) | 추천 카드가 대화 영역의 가로 공간을 더 사용하도록 넓히고, 제목·거리 글자와 상세 보기 버튼을 키웠습니다. 기존 세로 카드와 최대 3곳 표시를 유지합니다. | `598f9a3f2dac` |
| [docs/development/reports/20261101-agent-clarification.md](../../docs/development/reports/20261101-agent-clarification.md) | 여러 조건을 한 번에 말했을 때 모호한 항목을 화면이 계속 확인할 수 있도록, 대화 API의 보류 응답에 `clarification_fields`를 추가했습니다. 기존 응답 필드는 유지하며 허용된 필드명만 전달합니다. | `cdd708572df4` |
| [docs/development/reports/20261101-agent-dialogue-b.md](../../docs/development/reports/20261101-agent-dialogue-b.md) | 대화 화면에서 듣는 중 버튼을 ‘말씀 끝 · 보내기 ▶’로 표시하고, 다시 말하기와 처리 중 입력 보존을 추가했습니다. 서버가 해석을 보류하거나 충돌을 알리면 안내하고 자동 추천을 멈추며, 취소된 이전 응답은 적용하지 않습니다. | `34fcf577480c` |
| [docs/development/reports/20261101-agent-fixes-a.md](../../docs/development/reports/20261101-agent-fixes-a.md) | 에이전트가 출발지와 목적지를 혼동하거나 무료·예산·필수 조건을 잘못 반영하는 경우와 밤 12시를 낮 12시로 받아들이는 경우를 보류하도록 백엔드를 보완했습니다. | `ede782ecbfcb` |
| [docs/development/reports/20261101-agent-full-issue.md](../../docs/development/reports/20261101-agent-full-issue.md) | 이슈 #67을 develop 대비 dj/agent 전체 개선 목록으로 보완했습니다. 이전의 발화 근거·날짜와 시각·출발지·부분 보류·재확인 개선부터 음성·추천·카드·테스트까지 전후 사례와 코드·커밋 근거를 정리했습니다. | `1456213c7ca1` |
| [docs/development/reports/20261101-agent-grounding.md](../../docs/development/reports/20261101-agent-grounding.md) | 백엔드의 발화 근거·시각 검증 1단계를 구현했습니다. 모델이 말하지 않은 출발지나 발화와 다른 날짜·시각을 제안하면 보류하고, 모호한 시각이나 시작·종료 대상을 임의로 확정하지 않도록 했습니다. 세 공급자에 공통 검증을 연결했습니다. | `e23026ec9e66` |
| [docs/development/reports/20261101-agent-http-contract.md](../../docs/development/reports/20261101-agent-http-contract.md) | 보류된 조건을 사용자가 다시 확인했을 때 화면이 같은 값의 재확인과 관련 없는 답변을 구분할 수 있도록 대화 API에 `interpreted_fields`를 추가했습니다. 검증된 필드명만 전달하고 원문과 값은 포함하지 않습니다. | `3b4794db034c` |
| [docs/development/reports/20261101-agent-negation-fixes.md](../../docs/development/reports/20261101-agent-negation-fixes.md) | 추가 점검에서 확인한 부정 표현과 조건 해제 오류를 보완했습니다. 무료·유료의 부정, 예산의 ‘이상’과 ‘이내’, 출발하지 않는 장소·시각, 명시적으로 해제하지 않은 제외·필수 조건을 구분하도록 했습니다. | `9442cb177f68` |
| [docs/development/reports/20261101-agent-recommendation-c.md](../../docs/development/reports/20261101-agent-recommendation-c.md) | 출발지 검색 후보에 주소를 함께 표시하고 선택 전에는 기존 출발지를 유지하도록 했습니다. 무료·예산·관심사·제외 등 서버가 검증한 선호와 명시적 해제를 추천 요청까지 전달합니다. | `179c3ec86b19` |
| [docs/development/reports/20261101-agent-remediation-backend.md](../../docs/development/reports/20261101-agent-remediation-backend.md) | 대화 해석에서 무료·출발지·음악·실내외·장소 수의 반대 의미와 관심어 임의 삭제를 차단했습니다. 정상 요청·정정·명시적 해제는 허용하고, 같은 이름의 출발지도 검색·선택·변경 동의를 거치도록 했습니다. | `85e596e8ba19` |
| [docs/development/reports/20261101-agent-remediation-frontend.md](../../docs/development/reports/20261101-agent-remediation-frontend.md) | 추천 후보에 검색 당시 조건을 연결해 무료 조건 변경 후 이전 유료 후보가 다시 노출되는 문제를 수정했습니다. 명시적 선택 후 관련 보류를 해제하고, 복합 문장을 해석하며, 과거 카드의 거리·조건과 취소된 요청의 경계를 보존합니다. | `ed9c739b107b` |
| [docs/development/reports/20261101-agent-remediation-published.md](../../docs/development/reports/20261101-agent-remediation-published.md) | 개선·검증 후 `dj/agent`를 push했습니다. | `3ed52d7364f9` |
| [docs/development/reports/20261101-agent-remediation-validation.md](../../docs/development/reports/20261101-agent-remediation-validation.md) | 실제 브라우저에서 로컬 백엔드의 CORS·대화 검증·무료 필터·동명 장소 선택을 함께 확인하는 검증 도구와 다른 LLM용 분석 자료를 추가했습니다. 작업 범위·재현 사례·수정 근거·실행 방법·한계를 기록하고 상태와 색인을 갱신했습니다. | `f52ba4ae0b46` |
| [docs/development/reports/20261101-dj-agent-setup.md](../../docs/development/reports/20261101-dj-agent-setup.md) | 완료했습니다. 최신 원격 develop의 `252c07c`에서 **`dj/agent`**를 분기했습니다. | `2a2b9c9d11c6` |
| [docs/development/reports/20261101-final-agent-plan.md](../../docs/development/reports/20261101-final-agent-plan.md) | `develop`을 다시 가져와 확인했습니다. 원격에 새 커밋은 없고 현재 `dj/agent`가 최신 `origin/develop`을 포함합니다. | `5c149bb36e90` |
| [docs/development/reports/20261101-root-location-commit.md](../../docs/development/reports/20261101-root-location-commit.md) | dj/agent의 본 작업폴더 전환과 승인 범위 기록을 한 작업으로 커밋했습니다. | `d03510c5f2bf` |
| [docs/development/reports/automatic-voice-session.md](../../docs/development/reports/automatic-voice-session.md) | **자동 음성 대화를 연결했습니다.** [최신 화면](http://127.0.0.1:5175/?#/search)을 Chrome에서 새로고침해 주세요. | `89c4c83ccc10` |
| [docs/development/reports/common-automatic-dialogue.md](../../docs/development/reports/common-automatic-dialogue.md) | 자동 대화와 화면 이동을 로컬 통합 화면에 연결했습니다. | `0e90a23f2f4d` |
| [docs/development/reports/conversation-validation.md](../../docs/development/reports/conversation-validation.md) | 추가 테스트를 완료했습니다. **이번 검사에서 새 오류는 발견되지 않았습니다.** | `fbb6d5175cdc` |
| [docs/development/reports/culture-source-preparation.md](../../docs/development/reports/culture-source-preparation.md) | 서울시 키를 연결할 준비를 마쳤습니다. | `35dd8e313c0c` |
| [docs/development/reports/deployment-status-correction.md](../../docs/development/reports/deployment-status-correction.md) | 희영님 설명이 맞습니다. **기존 Render 서비스를 계속 사용하면 됩니다.** 공개 저장소 URL로 가져오는 서비스는 GitHub 앱 승인 없이 수동 배포할 수 있습니다. 제가 승인을 배포의 필수조건으로 안내한 부분은 정정합니다. [Render 공 | `07ca98b7d21d` |
| [docs/development/reports/frontend-chat-package.md](../../docs/development/reports/frontend-chat-package.md) | 팀 프론트에 연결할 **적용 패키지**를 준비했습니다. | `008b893d2a48` |
| [docs/development/reports/microphone-toggle.md](../../docs/development/reports/microphone-toggle.md) | 마이크 버튼을 켜기·끄기 방식으로 정리했습니다. | `e3f18d2bec91` |
| [docs/development/reports/natural-language-recommendation.md](../../docs/development/reports/natural-language-recommendation.md) | 자연어 대화 → 자동 설정 → 추천 연결을 구현했습니다. | `d51cc33f5ebe` |
| [docs/development/reports/seoul-live-and-tour-key.md](../../docs/development/reports/seoul-live-and-tour-key.md) | TourAPI 키는 **공공데이터포털**에서 받으면 됩니다. | `c0b2d6582a32` |
| [docs/development/reports/service-key-ui-integration.md](../../docs/development/reports/service-key-ui-integration.md) | 공유하신 메일은 **희영님의 로컬 QA 통과 보고**입니다. Render 승인 알림은 아니며, 본문에서도 Render/Vercel 실제 통신은 미검증입니다. | `cab4dc2c69af` |
| [docs/development/reports/tour-key-verification.md](../../docs/development/reports/tour-key-verification.md) | 인증키 저장은 확인했습니다. **국문 관광정보 서비스 활용신청이 추가로 필요합니다.** | `80c2de79ec0d` |
| [docs/development/reports/tour-live-verification.md](../../docs/development/reports/tour-live-verification.md) | **TourAPI 실제 조회에 성공했습니다.** | `857942ca72fc` |
| [docs/development/reports/transit-mobile-cards.md](../../docs/development/reports/transit-mobile-cards.md) | 대중교통 노선과 모바일 표시를 수정했습니다. | `767e51957169` |
| [docs/development/reports/voice-entry-navigation.md](../../docs/development/reports/voice-entry-navigation.md) | 사진은 기존 점검 화면(8765)입니다. **마이크는 [최신 자동 대화 홈](http://127.0.0.1:5175/?#/home)에 있습니다.** | `155e2a2adc35` |
| [docs/development/reports/voice-wave-and-compatibility.md](../../docs/development/reports/voice-wave-and-compatibility.md) | 화면은 모바일 폭에서 검사했지만, **맥북·휴대폰의 자동 음성 대화는 실제 기기 확인이 필요합니다.** 브라우저 음성 인식에는 지원 차이가 있습니다. [MDN 공식 호환성 안내](https://developer.mozilla.org/en-US/docs | `e86f5f6e2737` |
| [docs/development/screen-spec-review.md](../../docs/development/screen-spec-review.md) | 화면명세 v0.1 수신·구현 대조 체크표 | `6be14b542825` |
| [docs/development/service-key-status.md](../../docs/development/service-key-status.md) | 키별 실제 동작·앱 반영 점검 | `20d43495185e` |
| [docs/development/state.json](../../docs/development/state.json) | 구조화 설정·상태 데이터 | `cabdb69b0985` |
| [docs/development/tasks.md](../../docs/development/tasks.md) | LAB678 · 김동조 개발 할 일 | `555cf41b5052` |
| [docs/development/team-backend-guide.md](../../docs/development/team-backend-guide.md) | LAB678 · 동료와 LLM을 위한 개발 참조·실행 안내 | `a8cfdbe6a06b` |
| [docs/development/team-integration-checklist.md](../../docs/development/team-integration-checklist.md) | 팀 의견 대조 · 최종 UI 연결 우선 체크표 | `a9c94afd0cf6` |
| [docs/development/tooling-progress.md](../../docs/development/tooling-progress.md) | 재사용 도구·자동 색인·컨텍스트 구축 진행 체크표 | `b72aa1e78379` |
| [docs/development/transit-mobile.md](../../docs/development/transit-mobile.md) | 대중교통 노선·모바일 경로 카드 | `d35437eecf22` |
| [docs/development/transit-progress.md](../../docs/development/transit-progress.md) | 앱 내부 대중교통 안내 진행표 | `de4987d17983` |
| [docs/development/unified-chat-and-meter.md](../../docs/development/unified-chat-and-meter.md) | 단일 나들이 진입·실제 마이크 입력 미터 | `9fa3d9571e6a` |
| [docs/development/voice-browser-compatibility.md](../../docs/development/voice-browser-compatibility.md) | 음성·모바일 호환성 점검 | `039a457d831f` |
| [docs/development/voice-start-latency.md](../../docs/development/voice-start-latency.md) | 자동 대화 시작 지연 · 사용자 로그 분석 | `2e6d64401f62` |
| [docs/meetings/2026-10-28.md](../../docs/meetings/2026-10-28.md) | 10/28 팀 회의 | `4423b5dec6ce` |
| [docs/planning/AGENTS.md](../../docs/planning/AGENTS.md) | 첨부 기획 원본 | `참고 원본 / 966218f93a04` |
| [docs/planning/Lab_678_MVP_화면명세서.md](../../docs/planning/Lab_678_MVP_화면명세서.md) | Lab 678 \| 오늘 나들이 — MVP 화면명세서 v0.3.0 | `참고 원본 / 2b163732bf13` |
| [docs/planning/PRD.md](../../docs/planning/PRD.md) | Lab 678 \| 오늘 나들이 — 제품 요구사항 정의서(PRD) v0.7.0 | `참고 원본 / 4e50419c2295` |
| [docs/planning/README.md](../../docs/planning/README.md) | Lab 678 \| 오늘 나들이 — 기획 문서 안내 및 AI 협업 읽기 기준 | `참고 원본 / 8fe9b716a44e` |
| [docs/planning/archive/Lab_678_시니어_문화외출_독립형_PRD_v0.1_20261030.md](../../docs/planning/archive/Lab_678_시니어_문화외출_독립형_PRD_v0.1_20261030.md) | Lab 678 \| PRD v0.1 | `참고 원본 / 12da2334b1ca` |
| [docs/planning/archive/Lab_678_시니어_문화외출_독립형_PRD_v0.4_20261030.md](../../docs/planning/archive/Lab_678_시니어_문화외출_독립형_PRD_v0.4_20261030.md) | Lab 678 \| 시니어 AI 음성 문화외출 추천 서비스 PRD v0.4 | `참고 원본 / d04427254a8f` |
| [docs/planning/archive/Lab_678_시니어_문화외출_음성추천_PRD_v0.3_20261030.md](../../docs/planning/archive/Lab_678_시니어_문화외출_음성추천_PRD_v0.3_20261030.md) | Lab 678 \| 시니어 AI 음성 문화외출 추천 서비스 — 통합 PRD v0.3 | `참고 원본 / d1b478326627` |
| [docs/planning/handoff/Lab_678_UI_착수패키지_손희영_20261030.md](../../docs/planning/handoff/Lab_678_UI_착수패키지_손희영_20261030.md) | Lab 678 \| 손희영 UX/UI 병렬 착수 패키지 v0.1 | `참고 원본 / d0837643bb03` |
| [docs/planning/handoff/Lab_678_개발_착수패키지_김동조_20261030.md](../../docs/planning/handoff/Lab_678_개발_착수패키지_김동조_20261030.md) | Lab 678 \| 김동조 개발 병렬 착수 패키지 v0.1 | `참고 원본 / b466bfac11aa` |
| [docs/planning/handoff/Lab_678_공동설계_병렬착수_공통합의안_20261030.md](../../docs/planning/handoff/Lab_678_공동설계_병렬착수_공통합의안_20261030.md) | Lab 678 \| 공동설계 및 병렬작업 착수 — 공통 합의안 v0.1 | `참고 원본 / 32b75bbdee73` |
| [docs/reference/AGENTS.md](../../docs/reference/AGENTS.md) | 과거 자료 보관 | `참고 원본 / e174f58df81a` |
| [docs/reference/README.md](../../docs/reference/README.md) | 외부 브랜치 원본 보관 | `참고 원본 / 02f3a96325d3` |
| [docs/reference/TEAM_WORKFLOW/.env.example](../../docs/reference/TEAM_WORKFLOW/.env.example) | 설정·자료 파일; 필요할 때 원문 확인 | `참고 원본 / 34b5286295f8` |
| [docs/reference/TEAM_WORKFLOW/.github/ISSUE_TEMPLATE/bug.md](../../docs/reference/TEAM_WORKFLOW/.github/ISSUE_TEMPLATE/bug.md) | --- | `참고 원본 / 4864828de1ee` |
| [docs/reference/TEAM_WORKFLOW/.github/ISSUE_TEMPLATE/task.md](../../docs/reference/TEAM_WORKFLOW/.github/ISSUE_TEMPLATE/task.md) | --- | `참고 원본 / 1ee33bbd2c25` |
| [docs/reference/TEAM_WORKFLOW/.github/pull_request_template.md](../../docs/reference/TEAM_WORKFLOW/.github/pull_request_template.md) | ## 무엇을 했나요 | `참고 원본 / ec68f1c48e6b` |
| [docs/reference/TEAM_WORKFLOW/.gitignore](../../docs/reference/TEAM_WORKFLOW/.gitignore) | 설정·자료 파일; 필요할 때 원문 확인 | `참고 원본 / 2634a4efe969` |
| [docs/reference/TEAM_WORKFLOW/AGENTS.md](../../docs/reference/TEAM_WORKFLOW/AGENTS.md) | Lab678 · Codyssey AI 해커톤 2026 | `참고 원본 / d0e312ebbab1` |
| [docs/reference/TEAM_WORKFLOW/CLAUDE.md](../../docs/reference/TEAM_WORKFLOW/CLAUDE.md) | @AGENTS.md | `참고 원본 / d631d88045f7` |
| [docs/reference/TEAM_WORKFLOW/GEMINI.md](../../docs/reference/TEAM_WORKFLOW/GEMINI.md) | @AGENTS.md | `참고 원본 / d631d88045f7` |
| [docs/reference/TEAM_WORKFLOW/README.md](../../docs/reference/TEAM_WORKFLOW/README.md) | Lab678 · Codyssey AI 해커톤 2026 | `참고 원본 / 4e90d1430113` |
| [docs/reference/TEAM_WORKFLOW/TEAM_WORKFLOW.md](../../docs/reference/TEAM_WORKFLOW/TEAM_WORKFLOW.md) | 678 Lab · TEAM_WORKFLOW | `참고 원본 / bbe50fd59065` |
| [docs/reference/TEAM_WORKFLOW/backend/README.md](../../docs/reference/TEAM_WORKFLOW/backend/README.md) | backend | `참고 원본 / 2b80d1450b24` |
| [docs/reference/TEAM_WORKFLOW/design/README.md](../../docs/reference/TEAM_WORKFLOW/design/README.md) | design | `참고 원본 / 69ce5d8adb44` |
| [docs/reference/TEAM_WORKFLOW/docs/README.md](../../docs/reference/TEAM_WORKFLOW/docs/README.md) | docs | `참고 원본 / 57dbb44fc25e` |
| [docs/reference/TEAM_WORKFLOW/docs/meetings/2026-10-28.md](../../docs/reference/TEAM_WORKFLOW/docs/meetings/2026-10-28.md) | 10/28 팀 회의 | `참고 원본 / 4423b5dec6ce` |
| [docs/reference/TEAM_WORKFLOW/frontend/README.md](../../docs/reference/TEAM_WORKFLOW/frontend/README.md) | frontend | `참고 원본 / d05cc43ab85a` |
| [docs/reference/hackathon-server/README.md](../../docs/reference/hackathon-server/README.md) | 해커톤 GPU 서버 매뉴얼 보관 기록 | `참고 원본 / eac24535b9c1` |
| [frontend/AGENTS.md](../../frontend/AGENTS.md) | frontend 작업 | `27fb4a4ac041` |
| [frontend/README.md](../../frontend/README.md) | frontend | `3a0057924e8e` |
| [frontend/assets/home-hero.jpg](../../frontend/assets/home-hero.jpg) | 설정·자료 파일; 필요할 때 원문 확인 | `5e6a9e9032d8` |
| [frontend/assets/icons/type-default.png](../../frontend/assets/icons/type-default.png) | 설정·자료 파일; 필요할 때 원문 확인 | `c783349fc85a` |
| [frontend/assets/icons/type-exhibition.png](../../frontend/assets/icons/type-exhibition.png) | 설정·자료 파일; 필요할 때 원문 확인 | `34d14e374da3` |
| [frontend/assets/icons/type-festival-event.png](../../frontend/assets/icons/type-festival-event.png) | 설정·자료 파일; 필요할 때 원문 확인 | `21fb4d9426b6` |
| [frontend/assets/icons/type-hands-on.png](../../frontend/assets/icons/type-hands-on.png) | 설정·자료 파일; 필요할 때 원문 확인 | `386b0bd0f32a` |
| [frontend/assets/icons/type-historic-visit.png](../../frontend/assets/icons/type-historic-visit.png) | 설정·자료 파일; 필요할 때 원문 확인 | `a7fc68c9e325` |
| [frontend/assets/icons/type-performance.png](../../frontend/assets/icons/type-performance.png) | 설정·자료 파일; 필요할 때 원문 확인 | `008c1d162c72` |
| [frontend/assets/kkachi-face.png](../../frontend/assets/kkachi-face.png) | 설정·자료 파일; 필요할 때 원문 확인 | `4d6ed3445ece` |
| [frontend/assets/kkachi-hello.png](../../frontend/assets/kkachi-hello.png) | 설정·자료 파일; 필요할 때 원문 확인 | `ba33c042b5e0` |
| [frontend/assets/kkachi-sleep.png](../../frontend/assets/kkachi-sleep.png) | 설정·자료 파일; 필요할 때 원문 확인 | `96f0e18604ee` |
| [frontend/assets/kkachi-wake.png](../../frontend/assets/kkachi-wake.png) | 설정·자료 파일; 필요할 때 원문 확인 | `beb2eb11c0d9` |
| [frontend/assets/landing-autumn.jpg](../../frontend/assets/landing-autumn.jpg) | 설정·자료 파일; 필요할 때 원문 확인 | `069b53a306dc` |
| [frontend/assets/landing-spring.jpg](../../frontend/assets/landing-spring.jpg) | 설정·자료 파일; 필요할 때 원문 확인 | `4c86c55ba3eb` |
| [frontend/assets/place-craft.jpg](../../frontend/assets/place-craft.jpg) | 설정·자료 파일; 필요할 때 원문 확인 | `12d60383685d` |
| [frontend/assets/place-museum.jpg](../../frontend/assets/place-museum.jpg) | 설정·자료 파일; 필요할 때 원문 확인 | `c23f71eb4d5e` |
| [frontend/assets/place-palace.jpg](../../frontend/assets/place-palace.jpg) | 설정·자료 파일; 필요할 때 원문 확인 | `2203217fdd43` |
| [frontend/css/app.css](../../frontend/css/app.css) | 설정·자료 파일; 필요할 때 원문 확인 | `66b648b07aa6` |
| [frontend/css/tokens.css](../../frontend/css/tokens.css) | 설정·자료 파일; 필요할 때 원문 확인 | `6dec9efdbdee` |
| [frontend/dev_server.py](../../frontend/dev_server.py) | 프론트 개발 서버. frontend 폴더를 보여주고 /preview/ 요청은 백엔드로 그대로 넘겨요. | `75a8bc5f1957` |
| [frontend/index.html](../../frontend/index.html) | 설정·자료 파일; 필요할 때 원문 확인 | `c27c155cbbd4` |
| [frontend/js/api.js](../../frontend/js/api.js) | 백엔드 API 호출. 실패해도 Mock 후보로 바꾸지 않고, 결과 종류를 그대로 구분해서 돌려줘요. | `549a68f422ac` |
| [frontend/js/app.js](../../frontend/js/app.js) | 화면 이동과 S00 시작 · S01 홈 · S07 내 나들이. | `4b6eb096f9fd` |
| [frontend/js/chat.js](../../frontend/js/chat.js) | S02 까치와 대화 · S02a 부족·충돌 확인 · S03 대화 안 추천 카드 (PRD v0.7 H02~H10). | `1f4596ebca4a` |
| [frontend/js/landing.js](../../frontend/js/landing.js) | S00 시작 화면: 계절에 맞는 그림을 고르고, 그림 영역에 잎(단풍잎·꽃잎)을 천천히 떨어뜨려요. | `b592d66b567b` |
| [frontend/js/parse.js](../../frontend/js/parse.js) | AI 대화 연결이 없을 때 쓰는 규칙 기반 해석기. | `c384db51157c` |
| [frontend/js/place.js](../../frontend/js/place.js) | S04 장소 상세 (지도 보기 = 주 행동, 내 나들이에 저장 = 보조) · S08 지도와 도보 경로 · S06 저장 시트. | `f6b061837c85` |
| [frontend/js/saved.js](../../frontend/js/saved.js) | 체험 모드와 내 나들이 저장 (S06·S07). 로그인 없이 이 브라우저(localStorage)에만 저장해요. | `4b5ee1e1c71f` |
| [frontend/js/state.js](../../frontend/js/state.js) | 대화·추천 상태. 새로고침해도 대화와 결과가 남도록 sessionStorage 에 보관해요. | `e16f95c0a1b3` |
| [frontend/js/util.js](../../frontend/js/util.js) | 여러 화면이 같이 쓰는 작은 도구: 요소 만들기, 날짜·시각 표시, 저장소 읽기/쓰기. | `4adb4e134617` |
| [frontend/js/weather.js](../../frontend/js/weather.js) | 날씨 인사. 서울의 지금 날씨를 Open-Meteo(무료, 키 없음)에서 받아 까치가 먼저 건넬 말을 코드가 정해요. | `9b257963a8cb` |
| [utils/AGENTS.md](../../utils/AGENTS.md) | utils 작업 | `606b01a12f06` |
| [utils/README.md](../../utils/README.md) | 재사용 개발 도구 | `53fb5ee52c33` |
| [utils/harness.json](../../utils/harness.json) | 구조화 설정·상태 데이터 | `1ecf7aee9457` |
| [utils/index.md](../../utils/index.md) | 자동 생성 색인 | `generated` |
| [utils/reverse_index.md](../../utils/reverse_index.md) | 자동 생성 색인 | `generated` |
| [utils/scripts/agent_http_fixture.py](../../utils/scripts/agent_http_fixture.py) | 브라우저 회귀 검사에 실제 Preview HTTP와 고정 외부 공급자 데이터를 제공한다. | `2ff9de44f1f6` |
| [utils/scripts/catalog.py](../../utils/scripts/catalog.py) | Build deterministic code indexes without importing source modules. | `ecb99cd9ca5b` |
| [utils/scripts/check_agent_dialogue.cjs](../../utils/scripts/check_agent_dialogue.cjs) | 설정·자료 파일; 필요할 때 원문 확인 | `fd3592b61708` |
| [utils/scripts/check_agent_http.cjs](../../utils/scripts/check_agent_http.cjs) | 설정·자료 파일; 필요할 때 원문 확인 | `12b57bf3d168` |
| [utils/scripts/check_agent_recommendation.cjs](../../utils/scripts/check_agent_recommendation.cjs) | 설정·자료 파일; 필요할 때 원문 확인 | `c9581835d37e` |
| [utils/scripts/check_agent_regressions.cjs](../../utils/scripts/check_agent_regressions.cjs) | 설정·자료 파일; 필요할 때 원문 확인 | `dc8400e77e89` |
| [utils/scripts/check_chat_api.py](../../utils/scripts/check_chat_api.py) | 임시 로컬 서버에서 대화 API 정상·입력·미설정·CORS를 검사한다. 외부 AI 호출은 모의다. | `6edb12fa1d4e` |
| [utils/scripts/check_chat_live.py](../../utils/scripts/check_chat_live.py) | 명시 실행 시 Naito 실제 호출 3회로 공개 예문을 검증한다. 키/공급자 원문은 출력하지 않는다. | `9779f9dc2d52` |
| [utils/scripts/check_chat_ui.cjs](../../utils/scripts/check_chat_ui.cjs) | 설정·자료 파일; 필요할 때 원문 확인 | `a102019818ac` |
| [utils/scripts/check_conversation_edges.py](../../utils/scripts/check_conversation_edges.py) | 실제 Naito로 대화 수정·취소·시간 경계를 검사한다. 고정 시험 발화만 사용하고 키는 출력하지 않는다. | `824dcf0251ea` |
| [utils/scripts/check_course_alternatives.cjs](../../utils/scripts/check_course_alternatives.cjs) | 설정·자료 파일; 필요할 때 원문 확인 | `51a8659ad740` |
| [utils/scripts/check_course_edit.cjs](../../utils/scripts/check_course_edit.cjs) | 설정·자료 파일; 필요할 때 원문 확인 | `085af9c51d06` |
| [utils/scripts/check_culture_sources.py](../../utils/scripts/check_culture_sources.py) | 실행 중인 백엔드의 서울시·국문 문화시설 연결을 검사한다. 키는 출력하지 않는다. | `00e2c4a6c6ea` |
| [utils/scripts/check_culture_ui.cjs](../../utils/scripts/check_culture_ui.cjs) | 설정·자료 파일; 필요할 때 원문 확인 | `ea0eac085599` |
| [utils/scripts/check_deployment.cjs](../../utils/scripts/check_deployment.cjs) | 설정·자료 파일; 필요할 때 원문 확인 | `9377b6f0ed3b` |
| [utils/scripts/check_frontend_connection.cjs](../../utils/scripts/check_frontend_connection.cjs) | 설정·자료 파일; 필요할 때 원문 확인 | `94ef7ca24f28` |
| [utils/scripts/check_input_contract.cjs](../../utils/scripts/check_input_contract.cjs) | 설정·자료 파일; 필요할 때 원문 확인 | `142e3223552f` |
| [utils/scripts/check_kakao_map.cjs](../../utils/scripts/check_kakao_map.cjs) | 설정·자료 파일; 필요할 때 원문 확인 | `929f230af4af` |
| [utils/scripts/check_location_ui.cjs](../../utils/scripts/check_location_ui.cjs) | 설정·자료 파일; 필요할 때 원문 확인 | `74709133a296` |
| [utils/scripts/check_microphone_meter.cjs](../../utils/scripts/check_microphone_meter.cjs) | 설정·자료 파일; 필요할 때 원문 확인 | `f7957844a996` |
| [utils/scripts/check_natural_flow.cjs](../../utils/scripts/check_natural_flow.cjs) | 설정·자료 파일; 필요할 때 원문 확인 | `30eda5f33e16` |
| [utils/scripts/check_outing_ui.cjs](../../utils/scripts/check_outing_ui.cjs) | 설정·자료 파일; 필요할 때 원문 확인 | `9163b58a7889` |
| [utils/scripts/check_place_search.cjs](../../utils/scripts/check_place_search.cjs) | 설정·자료 파일; 필요할 때 원문 확인 | `2452371fcdb6` |
| [utils/scripts/check_preference_recovery.cjs](../../utils/scripts/check_preference_recovery.cjs) | 설정·자료 파일; 필요할 때 원문 확인 | `79a0132af3ef` |
| [utils/scripts/check_result_preservation.cjs](../../utils/scripts/check_result_preservation.cjs) | 설정·자료 파일; 필요할 때 원문 확인 | `fc27ca0e6ae5` |
| [utils/scripts/check_service_keys.py](../../utils/scripts/check_service_keys.py) | 현재 설정 키별 실제 서비스 응답 검사. 키·헤더·공급자 URL은 기록하지 않는다. | `ea67882d8c9d` |
| [utils/scripts/check_team_flow.cjs](../../utils/scripts/check_team_flow.cjs) | 설정·자료 파일; 필요할 때 원문 확인 | `1f6037ee2505` |
| [utils/scripts/check_transit_details.py](../../utils/scripts/check_transit_details.py) | 공개 QA 좌표의 실제 대중교통 노선·승하차를 확인한다. 키/원문 요청/사용자 위치는 저장하지 않는다. | `43a2c98d0bdc` |
| [utils/scripts/check_transit_mobile.cjs](../../utils/scripts/check_transit_mobile.cjs) | 설정·자료 파일; 필요할 때 원문 확인 | `ac5628b7071b` |
| [utils/scripts/check_transit_ui.cjs](../../utils/scripts/check_transit_ui.cjs) | 설정·자료 파일; 필요할 때 원문 확인 | `9bd93ee6d49a` |
| [utils/scripts/check_unified_chat.cjs](../../utils/scripts/check_unified_chat.cjs) | 설정·자료 파일; 필요할 때 원문 확인 | `99bb0c3df866` |
| [utils/scripts/check_voice_diagnostics.cjs](../../utils/scripts/check_voice_diagnostics.cjs) | 설정·자료 파일; 필요할 때 원문 확인 | `c697b604ed65` |
| [utils/scripts/check_voice_entry.cjs](../../utils/scripts/check_voice_entry.cjs) | 설정·자료 파일; 필요할 때 원문 확인 | `e31eab4e19ef` |
| [utils/scripts/check_voice_navigation.cjs](../../utils/scripts/check_voice_navigation.cjs) | 설정·자료 파일; 필요할 때 원문 확인 | `86249b3fed9a` |
| [utils/scripts/check_voice_session.cjs](../../utils/scripts/check_voice_session.cjs) | 설정·자료 파일; 필요할 때 원문 확인 | `b6bf0f549c0d` |
| [utils/scripts/commit_report.py](../../utils/scripts/commit_report.py) | Commit an approved task with its complete UTF-8 report as the exact message. | `71ec658dfada` |
| [utils/scripts/context.py](../../utils/scripts/context.py) | Render a compact restart brief from explicit state, without guessing decisions. | `fd76e9b14c3b` |
| [utils/scripts/harness.py](../../utils/scripts/harness.py) | Run offline repository checks with explicit evidence and no auto-repair. | `16a9248426c4` |
| [utils/scripts/loop.py](../../utils/scripts/loop.py) | Record a bounded hypothesis-change-evidence loop without executing repair code. | `2b91226d1d91` |
| [utils/scripts/prepare_chat_handoff.py](../../utils/scripts/prepare_chat_handoff.py) | 팀 프론트에 적용할 최소 패치와 실행 복사본을 .local에 만든다. 작업 브랜치/팀 원본을 변경하지 않는다. | `ca6bf83683fb` |
| [utils/scripts/read_pdf.py](../../utils/scripts/read_pdf.py) | Extract PDF pages locally and print a conservative redacted review copy. | `27fb9fcaa1e9` |
| [utils/scripts/reuse.py](../../utils/scripts/reuse.py) | Verify copied files and snapshot selected Git files without checkout or merge. | `b0da97aea104` |
| [utils/scripts/team_chat_preview.py](../../utils/scripts/team_chat_preview.py) | 팀 브랜치의 격리 복사본에 채팅 모듈을 연결하는 로컬 검증 서버. 원본 파일은 수정하지 않는다. | `f711ae91e7c2` |
| [utils/scripts/verify_watch.py](../../utils/scripts/verify_watch.py) | Smoke-test a running index watcher with a temporary documented source file. | `3a98cf1bc20b` |
| [utils/scripts/watch.py](../../utils/scripts/watch.py) | Refresh indexes and the short context on file changes until explicitly stopped. | `259f3fc032e0` |
| [utils/templates/README.md](../../utils/templates/README.md) | 작업·코드 템플릿 | `1ca52a619cac` |
| [utils/templates/js_module.js.tmpl](../../utils/templates/js_module.js.tmpl) | /** | `fe2e1416837b` |
| [utils/templates/python_module.py.tmpl](../../utils/templates/python_module.py.tmpl) | """모듈 개요: 구현할 목적과 재사용 키워드를 작성한다. | `38c455a0dc3f` |
| [utils/templates/task.md.tmpl](../../utils/templates/task.md.tmpl) | 작업 이름 | `796b088dbc69` |
| [utils/tests/test_tools.py](../../utils/tests/test_tools.py) | Exercise failure paths for indexes, copying, loops, context and commit guards. | `40a7618753a1` |
