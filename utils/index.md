# 코드 색인

자동 생성: `python utils/scripts/catalog.py --write`. 직접 편집하지 않는다.

요약으로 위치를 찾은 뒤 필요한 코드만 읽는다. 해시는 내용 변경 확인용이며 토큰 절약량 측정값이 아니다.

템플릿은 [templates/README.md](templates/README.md), 사용법은 [README.md](README.md)를 확인한다.

| 파일 | 개요 | SHA-256 앞 12자 |
|---|---|---|
| [backend/chat_conditions.py](../backend/chat_conditions.py) | AI 해석 결과를 추천 조건 초안으로 병합한다. 네트워크·저장·추천 실행은 하지 않는다. | `c8fca428da00` |
| [backend/chat_grounding.py](../backend/chat_grounding.py) | 검증 가능한 발화 근거만 조건에 반영한다. 외부 호출·저장·행사 사실 판정은 하지 않는다. | `b957b102350c` |
| [backend/chat_prompt.py](../backend/chat_prompt.py) | 대화 조건 후보와 이번 발화 근거를 요청하는 내부 지침. | `674aabe6d4af` |
| [backend/contact.py](../backend/contact.py) | 행사 문의 전화번호. 서울시 문화포털 행사 상세 페이지의 '문의' 칸에서 번호만 읽어 와요. | `91140f742559` |
| [backend/course.py](../backend/course.py) | 서울시 후보 최대 다섯 곳의 방문 순서를 비교해 두 곳 도보 일정 하나를 제시한다. | `fc42683c7b44` |
| [backend/culture_config.py](../backend/culture_config.py) | 문화정보 키를 서버 환경/무시된 로컬 파일에서 읽는다. 비밀값을 응답·로그에 내보내지 않는다. | `f9d1551f7b88` |
| [backend/local_voice.py](../backend/local_voice.py) | Windows 개인 시연용. 카드 텍스트를 설치된 한국어 음성으로 WAV 합성한다. | `a36d41d07b14` |
| [backend/location_view.js](../backend/location_view.js) | 지도 위 내 위치 표시·갱신·중지를 제공한다. 사용자 클릭 후에만 위치 권한을 요청한다. | `89b2538a420e` |
| [backend/map_config.py](../backend/map_config.py) | 지도 표시용 공개 JavaScript 키만 읽는다. 서버 REST 키와 설정 파일은 공개하지 않는다. | `d6393a77066b` |
| [backend/map_view.js](../backend/map_view.js) | 카카오 지도 우선 표시와 기존 지도 대체를 제공하는 개인 점검용 어댑터. | `4144865fa817` |
| [backend/microphone_meter.js](../backend/microphone_meter.js) | 실제 마이크 PCM 입력의 RMS/dBFS를 측정한다. 원본 음성 저장/전송·스피커 재생은 하지 않는다. | `3598dfeffac3` |
| [backend/naito_chat.py](../backend/naito_chat.py) | Naito 단일 조건 추출 호출. 키/대화 원문은 기록하지 않고 실패 시 기존 초안을 유지한다. | `ee8efaf07b55` |
| [backend/outing.py](../backend/outing.py) | 서울시 분류별 공개 후보에서 날짜·시간·대화 선호를 확인해 추천한다. | `b904be688105` |
| [backend/places.py](../backend/places.py) | 출발지 선택용 카카오 장소명/주소 검색. 사용자 검색어·키·원문 응답은 저장하지 않는다. | `15ca7cc32b99` |
| [backend/preferences.py](../backend/preferences.py) | 대화 선호의 형식과 공식 행사 사실 기반 선별. AI가 가격·경로 사실을 만들지 않는다. | `9255a02ce149` |
| [backend/preview.py](../backend/preview.py) | 동조 개인용 로컬 추천 점검 화면. python backend/preview.py로 시작한다. | `26d2068a9ca0` |
| [backend/preview_meter.js](../backend/preview_meter.js) | 기존 점검 화면에서도 실제 마이크 입력만 독립적으로 점검한다. STT 성공으로 표시하지 않는다. | `bf80fbd716f2` |
| [backend/team_app.py](../backend/team_app.py) | 검증한 로컬 팀 프론트를 /app/에서 제공한다. 선택 파일·비밀값·저장소 전체를 공개하지 않는다. | `caeddc220712` |
| [backend/team_chat.js](../backend/team_chat.js) | 팀 프론트 164cd40의 공통 자동 대화 모듈. 최종 반영 전 담당 확인용이다. | `2c96f8eb8ec0` |
| [backend/team_culture.js](../backend/team_culture.js) | 문화정보 출처 선택·표시. 팀 복사본과 인계 패키지에서 사용하는 독립 모듈. | `f512b56f4fed` |
| [backend/team_preferences.js](../backend/team_preferences.js) | 로컬 팀 화면의 대화 선호를 최종 확인·실제 추천 요청에 연결한다. 담당 원본에는 미반영. | `290c391004ce` |
| [backend/team_voice_actions.js](../backend/team_voice_actions.js) | 공통 음성 조작. 앱에 이미 있는 화면과 현재 후보 ID만 사용하며 URL/행사 사실을 만들지 않는다. | `5884c686c079` |
| [backend/test_agent_integration.py](../backend/test_agent_integration.py) | 실제 로컬 HTTP 처리기와 모의 공급자로 대화 계약 및 CORS를 검증한다. | `af9edb28f503` |
| [backend/test_chat_conditions.py](../backend/test_chat_conditions.py) | 실제 AI를 호출하지 않는 조건 병합 테스트. 동의·최신 입력·사실 경계를 검증한다. | `d8f45e130ede` |
| [backend/test_chat_grounding.py](../backend/test_chat_grounding.py) | 실제 모델 호출 없이 발화 근거와 시간 판단의 안전 경계를 검증한다. | `0d9dafec1fbd` |
| [backend/test_contact.py](../backend/test_contact.py) | 개요 없음 | `9dfdbadbfe7f` |
| [backend/test_course.py](../backend/test_course.py) | 두 곳 도보 일정의 마감 경계·휴관 원문·결측·방문 순서를 검사한다. | `94dbe388fa2a` |
| [backend/test_culture_sources.py](../backend/test_culture_sources.py) | 문화정보 키/조회 범위와 국문 장소의 사실·오류 경계를 모의 응답으로 검사한다. | `9b0e158d3e3a` |
| [backend/test_deployment_keys.py](../backend/test_deployment_keys.py) | 배포 환경변수가 개인 로컬 키 파일보다 우선하는지 가짜 키로 검사한다. 외부 호출/실제 키 조회 없음. | `4e820f2d34cc` |
| [backend/test_map_config.py](../backend/test_map_config.py) | 지도 공개 설정이 JS 키만 노출하고 서버 키·잘못된 입력을 배제하는지 검증한다. | `00c375b43f69` |
| [backend/test_naito_chat.py](../backend/test_naito_chat.py) | Naito 모의 응답/장애와 HTTP 연결 경계를 검사한다. 실제 서비스 성공을 뜻하지 않는다. | `d2ae168ae7b3` |
| [backend/test_outing.py](../backend/test_outing.py) | 서울시 공개 응답 재생으로 입력·선별·결측·실패를 검사한다. | `4f76676a4a52` |
| [backend/test_places.py](../backend/test_places.py) | 장소/주소 검색의 입력·좌표·실제0건·공급자 장애·비밀값 노출 방지 회귀. | `8791dc24d48a` |
| [backend/test_preferences.py](../backend/test_preferences.py) | 대화→조건→추천 경계. 복수 관심사·제외·가격 미확인·확정값 보호를 재현한다. | `fcdb9301848c` |
| [backend/test_preview.py](../backend/test_preview.py) | HTTP 처리기의 입력 오류 계약과 route/course 호환을 외부 조회 없이 검증한다. | `0cffec5946b6` |
| [backend/test_team_app.py](../backend/test_team_app.py) | 같은 서버 앱 서빙의 경로 제한·미설정·정적 자산만 검사한다. 외부 API를 호출하지 않는다. | `a770a41a112e` |
| [backend/test_transit.py](../backend/test_transit.py) | 실제 노선 성공과 구분한 대중교통 어댑터 단위 검증. 가상 수치로 응답/오류 경계를 검사한다. | `a4610c4c9b6e` |
| [backend/test_walking.py](../backend/test_walking.py) | 한국어 경로 단계와 지도 좌표가 같은 응답을 사용하는지 검증한다. | `c93d16baf2e1` |
| [backend/tour_places.py](../backend/tour_places.py) | 국문 TourAPI 문화시설 조회. 상설 장소를 특정 날짜의 공연/전시로 간주하지 않는다. | `32d240c5d533` |
| [backend/transit.py](../backend/transit.py) | 개인 점검용 카카오 대중교통 텍스트 안내. 키는 서버에서만 읽고 원문 응답은 저장하지 않는다. | `e64929bf1612` |
| [backend/voice_session.js](../backend/voice_session.js) | 횟수와 무응답 시간으로 제한된 브라우저 음성 대화. 시작 클릭 없이 재생/녹음하지 않는다. | `35ba6882994d` |
| [backend/walking.py](../backend/walking.py) | 개인 점검 화면에서 선택한 행사장 두 곳의 Valhalla 보행 경로를 조회한다. | `fedc1567e347` |
| [frontend/dev_server.py](../frontend/dev_server.py) | 프론트 개발 서버. frontend 폴더를 보여주고 /preview/ 요청은 백엔드로 그대로 넘겨요. | `75a8bc5f1957` |
| [frontend/js/api.js](../frontend/js/api.js) | 백엔드 API 호출. 실패해도 Mock 후보로 바꾸지 않고, 결과 종류를 그대로 구분해서 돌려줘요. | `549a68f422ac` |
| [frontend/js/app.js](../frontend/js/app.js) | 화면 이동과 S00 시작 · S01 홈 · S07 내 나들이. | `4b6eb096f9fd` |
| [frontend/js/chat.js](../frontend/js/chat.js) | S02 까치와 대화 · S02a 부족·충돌 확인 · S03 대화 안 추천 카드 (PRD v0.7 H02~H10). | `1f4596ebca4a` |
| [frontend/js/landing.js](../frontend/js/landing.js) | S00 시작 화면: 계절에 맞는 그림을 고르고, 그림 영역에 잎(단풍잎·꽃잎)을 천천히 떨어뜨려요. | `b592d66b567b` |
| [frontend/js/parse.js](../frontend/js/parse.js) | AI 대화 연결이 없을 때 쓰는 규칙 기반 해석기. | `c384db51157c` |
| [frontend/js/place.js](../frontend/js/place.js) | S04 장소 상세 (지도 보기 = 주 행동, 내 나들이에 저장 = 보조) · S08 지도와 도보 경로 · S06 저장 시트. | `f6b061837c85` |
| [frontend/js/saved.js](../frontend/js/saved.js) | 체험 모드와 내 나들이 저장 (S06·S07). 로그인 없이 이 브라우저(localStorage)에만 저장해요. | `4b5ee1e1c71f` |
| [frontend/js/state.js](../frontend/js/state.js) | 대화·추천 상태. 새로고침해도 대화와 결과가 남도록 sessionStorage 에 보관해요. | `e16f95c0a1b3` |
| [frontend/js/util.js](../frontend/js/util.js) | 여러 화면이 같이 쓰는 작은 도구: 요소 만들기, 날짜·시각 표시, 저장소 읽기/쓰기. | `4adb4e134617` |
| [frontend/js/weather.js](../frontend/js/weather.js) | 날씨 인사. 서울의 지금 날씨를 Open-Meteo(무료, 키 없음)에서 받아 까치가 먼저 건넬 말을 코드가 정해요. | `9b257963a8cb` |
| [utils/scripts/agent_http_fixture.py](../utils/scripts/agent_http_fixture.py) | 브라우저 회귀 검사에 실제 Preview HTTP와 고정 외부 공급자 데이터를 제공한다. | `2ff9de44f1f6` |
| [utils/scripts/catalog.py](../utils/scripts/catalog.py) | Build deterministic code indexes without importing source modules. | `ecb99cd9ca5b` |
| [utils/scripts/check_chat_api.py](../utils/scripts/check_chat_api.py) | 임시 로컬 서버에서 대화 API 정상·입력·미설정·CORS를 검사한다. 외부 AI 호출은 모의다. | `6edb12fa1d4e` |
| [utils/scripts/check_chat_live.py](../utils/scripts/check_chat_live.py) | 명시 실행 시 Naito 실제 호출 3회로 공개 예문을 검증한다. 키/공급자 원문은 출력하지 않는다. | `9779f9dc2d52` |
| [utils/scripts/check_conversation_edges.py](../utils/scripts/check_conversation_edges.py) | 실제 Naito로 대화 수정·취소·시간 경계를 검사한다. 고정 시험 발화만 사용하고 키는 출력하지 않는다. | `824dcf0251ea` |
| [utils/scripts/check_culture_sources.py](../utils/scripts/check_culture_sources.py) | 실행 중인 백엔드의 서울시·국문 문화시설 연결을 검사한다. 키는 출력하지 않는다. | `00e2c4a6c6ea` |
| [utils/scripts/check_service_keys.py](../utils/scripts/check_service_keys.py) | 현재 설정 키별 실제 서비스 응답 검사. 키·헤더·공급자 URL은 기록하지 않는다. | `ea67882d8c9d` |
| [utils/scripts/check_transit_details.py](../utils/scripts/check_transit_details.py) | 공개 QA 좌표의 실제 대중교통 노선·승하차를 확인한다. 키/원문 요청/사용자 위치는 저장하지 않는다. | `43a2c98d0bdc` |
| [utils/scripts/commit_report.py](../utils/scripts/commit_report.py) | Commit an approved task with its complete UTF-8 report as the exact message. | `71ec658dfada` |
| [utils/scripts/context.py](../utils/scripts/context.py) | Render a compact restart brief from explicit state, without guessing decisions. | `fd76e9b14c3b` |
| [utils/scripts/harness.py](../utils/scripts/harness.py) | Run offline repository checks with explicit evidence and no auto-repair. | `16a9248426c4` |
| [utils/scripts/loop.py](../utils/scripts/loop.py) | Record a bounded hypothesis-change-evidence loop without executing repair code. | `2b91226d1d91` |
| [utils/scripts/prepare_chat_handoff.py](../utils/scripts/prepare_chat_handoff.py) | 팀 프론트에 적용할 최소 패치와 실행 복사본을 .local에 만든다. 작업 브랜치/팀 원본을 변경하지 않는다. | `ca6bf83683fb` |
| [utils/scripts/read_pdf.py](../utils/scripts/read_pdf.py) | Extract PDF pages locally and print a conservative redacted review copy. | `27fb9fcaa1e9` |
| [utils/scripts/reuse.py](../utils/scripts/reuse.py) | Verify copied files and snapshot selected Git files without checkout or merge. | `b0da97aea104` |
| [utils/scripts/team_chat_preview.py](../utils/scripts/team_chat_preview.py) | 팀 브랜치의 격리 복사본에 채팅 모듈을 연결하는 로컬 검증 서버. 원본 파일은 수정하지 않는다. | `f711ae91e7c2` |
| [utils/scripts/verify_watch.py](../utils/scripts/verify_watch.py) | Smoke-test a running index watcher with a temporary documented source file. | `3a98cf1bc20b` |
| [utils/scripts/watch.py](../utils/scripts/watch.py) | Refresh indexes and the short context on file changes until explicitly stopped. | `259f3fc032e0` |
| [utils/tests/test_tools.py](../utils/tests/test_tools.py) | Exercise failure paths for indexes, copying, loops, context and commit guards. | `40a7618753a1` |
