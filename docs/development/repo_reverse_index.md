# 저장소 기능·함수 역색인

자동 생성. 호출·참조 그래프가 아니라 기능 라우팅과 정의 위치의 역색인이다.

## 기능 → 파일

- **정식 문화정보 조회 확대·국문 문화시설**: [backend/culture_config.py](../../backend/culture_config.py), [backend/culture.env.example](../../backend/culture.env.example), [backend/tour_places.py](../../backend/tour_places.py), [backend/test_culture_sources.py](../../backend/test_culture_sources.py), [utils/scripts/check_culture_sources.py](../../utils/scripts/check_culture_sources.py), [docs/development/culture-sources.md](../../docs/development/culture-sources.md)
- **팀 프론트 실파일 적용 패키지·통합 검사**: [utils/scripts/prepare_chat_handoff.py](../../utils/scripts/prepare_chat_handoff.py), [docs/development/frontend-chat-package.md](../../docs/development/frontend-chat-package.md), [docs/development/qa-handoff/manifest.json](../../docs/development/qa-handoff/manifest.json)
- **자연어 수정·조건 해제·추천 회복 검증**: [utils/scripts/check_conversation_edges.py](../../utils/scripts/check_conversation_edges.py), [utils/scripts/check_preference_recovery.cjs](../../utils/scripts/check_preference_recovery.cjs), [docs/development/conversation-validation.md](../../docs/development/conversation-validation.md), [docs/development/qa-conversation/edges.json](../../docs/development/qa-conversation/edges.json), [docs/development/qa-conversation/recovery.json](../../docs/development/qa-conversation/recovery.json)
- **자연어 선호 탐색·자동 설정·실제 후보 선별**: [backend/preferences.py](../../backend/preferences.py), [backend/test_preferences.py](../../backend/test_preferences.py), [backend/team_preferences.js](../../backend/team_preferences.js), [utils/scripts/check_natural_flow.cjs](../../utils/scripts/check_natural_flow.cjs), [docs/development/natural-language-handoff.md](../../docs/development/natural-language-handoff.md), [docs/development/qa-natural/result.json](../../docs/development/qa-natural/result.json)
- **자연어 중심 추천·이전 구현 비교**: [docs/development/natural-language-recommendation-review.md](../../docs/development/natural-language-recommendation-review.md)
- **팀 화면 AI 채팅·조건 동기화·동의 UI**: [backend/team_chat.js](../../backend/team_chat.js), [utils/scripts/team_chat_preview.py](../../utils/scripts/team_chat_preview.py), [utils/scripts/check_chat_ui.cjs](../../utils/scripts/check_chat_ui.cjs), [docs/development/chat-ui-handoff.md](../../docs/development/chat-ui-handoff.md), [docs/development/qa-chat/result.json](../../docs/development/qa-chat/result.json)
- **대화 조건 초안·변경 동의·최신 입력 보호**: [backend/chat_conditions.py](../../backend/chat_conditions.py), [backend/test_chat_conditions.py](../../backend/test_chat_conditions.py), [docs/development/chat-conditions.md](../../docs/development/chat-conditions.md)
- **Naito 채팅·모델 설정·HTTP 검증**: [backend/naito_chat.py](../../backend/naito_chat.py), [backend/test_naito_chat.py](../../backend/test_naito_chat.py), [utils/scripts/check_chat_api.py](../../utils/scripts/check_chat_api.py), [utils/scripts/check_chat_live.py](../../utils/scripts/check_chat_live.py), [docs/development/naito-usage.md](../../docs/development/naito-usage.md), [docs/development/examples/naito-chat.live.json](../../docs/development/examples/naito-chat.live.json)
- **QA-01 실제 팀 화면·추천·상세 ID 검증**: [utils/scripts/check_team_flow.cjs](../../utils/scripts/check_team_flow.cjs), [docs/development/qa01-team-connection.md](../../docs/development/qa01-team-connection.md), [docs/development/examples/qa01-request.recorded.json](../../docs/development/examples/qa01-request.recorded.json)
- **출발지 장소·주소 검색과 프론트 연결**: [backend/places.py](../../backend/places.py), [backend/test_places.py](../../backend/test_places.py), [backend/preview.py](../../backend/preview.py), [utils/scripts/check_place_search.cjs](../../utils/scripts/check_place_search.cjs), [docs/development/place-search-api.md](../../docs/development/place-search-api.md)
- **내 위치 표시·정확도·갱신·수집 중지**: [backend/location_view.js](../../backend/location_view.js), [backend/map_view.js](../../backend/map_view.js), [backend/preview.html](../../backend/preview.html), [utils/scripts/check_location_ui.cjs](../../utils/scripts/check_location_ui.cjs), [docs/development/kakao-map-location.md](../../docs/development/kakao-map-location.md)
- **카카오 지도 전환·번호핀·경로 표시**: [backend/map_config.py](../../backend/map_config.py), [backend/map_view.js](../../backend/map_view.js), [backend/test_map_config.py](../../backend/test_map_config.py), [backend/preview.html](../../backend/preview.html), [utils/scripts/check_kakao_map.cjs](../../utils/scripts/check_kakao_map.cjs), [docs/development/kakao-map-location.md](../../docs/development/kakao-map-location.md)
- **단일 서비스 배포 준비·상태 확인·음성 지원 구분**: [backend/preview.py](../../backend/preview.py), [backend/local_voice.py](../../backend/local_voice.py), [backend/test_preview.py](../../backend/test_preview.py), [utils/scripts/check_deployment.cjs](../../utils/scripts/check_deployment.cjs), [docs/development/render-demo-guide.md](../../docs/development/render-demo-guide.md)
- **코스 제외 예정·취소·명시적 재생성**: [backend/preview.html](../../backend/preview.html), [utils/scripts/check_course_edit.cjs](../../utils/scripts/check_course_edit.cjs), [docs/development/outing-handoff.md](../../docs/development/outing-handoff.md)
- **추천 재요청·실패 복원·늦은 응답 방지**: [backend/preview.html](../../backend/preview.html), [utils/scripts/check_result_preservation.cjs](../../utils/scripts/check_result_preservation.cjs), [docs/development/outing-handoff.md](../../docs/development/outing-handoff.md)
- **별도 프론트 연결·CORS·상세 사실 필드**: [backend/preview.py](../../backend/preview.py), [backend/outing.py](../../backend/outing.py), [backend/test_preview.py](../../backend/test_preview.py), [backend/test_outing.py](../../backend/test_outing.py), [utils/scripts/check_frontend_connection.cjs](../../utils/scripts/check_frontend_connection.cjs), [docs/development/recommend-api.md](../../docs/development/recommend-api.md)
- **추천 입력 60분·route 호환·오류 계약**: [backend/outing.py](../../backend/outing.py), [backend/preview.py](../../backend/preview.py), [backend/preview.html](../../backend/preview.html), [backend/test_outing.py](../../backend/test_outing.py), [backend/test_preview.py](../../backend/test_preview.py), [utils/scripts/check_input_contract.cjs](../../utils/scripts/check_input_contract.cjs), [docs/development/recommend-api.md](../../docs/development/recommend-api.md)
- **동료·LLM 백엔드 참조·실행 안내**: [docs/development/team-backend-guide.md](../../docs/development/team-backend-guide.md), [docs/development/team-integration-checklist.md](../../docs/development/team-integration-checklist.md), [backend/README.md](../../backend/README.md)
- **화면명세 수신·화면별 구현 차이 점검**: [docs/development/screen-spec-review.md](../../docs/development/screen-spec-review.md)
- **대중교통 내부 텍스트·지도 안내·서버 키 연결**: [backend/transit.py](../../backend/transit.py), [backend/test_transit.py](../../backend/test_transit.py), [backend/preview.py](../../backend/preview.py), [backend/preview.html](../../backend/preview.html), [utils/scripts/check_transit_ui.cjs](../../utils/scripts/check_transit_ui.cjs), [docs/development/transit-progress.md](../../docs/development/transit-progress.md)
- **시간 충돌 동의·한 곳/이른 출발 대안**: [backend/course.py](../../backend/course.py), [backend/test_course.py](../../backend/test_course.py), [backend/preview.html](../../backend/preview.html), [utils/scripts/check_course_alternatives.cjs](../../utils/scripts/check_course_alternatives.cjs), [docs/development/course-alternatives-progress.md](../../docs/development/course-alternatives-progress.md)
- **앱 내부 한국어 도보 안내·경로 지도 전환**: [backend/walking.py](../../backend/walking.py), [backend/test_walking.py](../../backend/test_walking.py), [backend/preview.py](../../backend/preview.py), [backend/preview.html](../../backend/preview.html), [utils/scripts/check_outing_ui.cjs](../../utils/scripts/check_outing_ui.cjs), [docs/development/outing-handoff.md](../../docs/development/outing-handoff.md)
- **선택·코스 구간별 외부 경로안내**: [backend/preview.html](../../backend/preview.html), [utils/scripts/check_outing_ui.cjs](../../utils/scripts/check_outing_ui.cjs), [docs/development/outing-handoff.md](../../docs/development/outing-handoff.md), [docs/development/mobility-routing-review.md](../../docs/development/mobility-routing-review.md)
- **두 곳 도보 문화코스**: [backend/course.py](../../backend/course.py), [backend/test_course.py](../../backend/test_course.py), [backend/walking.py](../../backend/walking.py), [backend/preview.html](../../backend/preview.html), [utils/scripts/check_outing_ui.cjs](../../utils/scripts/check_outing_ui.cjs), [docs/development/outing-handoff.md](../../docs/development/outing-handoff.md)
- **행사장 사이 도보 거리·시간**: [backend/walking.py](../../backend/walking.py), [backend/preview.py](../../backend/preview.py), [backend/preview.html](../../backend/preview.html), [utils/scripts/check_outing_ui.cjs](../../utils/scripts/check_outing_ui.cjs), [docs/development/mobility-routing-review.md](../../docs/development/mobility-routing-review.md)
- **문화행사 추천·점검 화면**: [backend/outing.py](../../backend/outing.py), [backend/local_voice.py](../../backend/local_voice.py), [backend/preview.py](../../backend/preview.py), [backend/preview.html](../../backend/preview.html), [backend/test_outing.py](../../backend/test_outing.py), [utils/scripts/check_outing_ui.cjs](../../utils/scripts/check_outing_ui.cjs), [docs/development/outing-handoff.md](../../docs/development/outing-handoff.md)
- **문화외출 MVP 실행계획·시연 검증**: [docs/development/mvp-plan.md](../../docs/development/mvp-plan.md), [docs/development/tasks.md](../../docs/development/tasks.md)
- **작업 재개·대화 압축**: [docs/development/current-state.md](../../docs/development/current-state.md), [utils/scripts/context.py](../../utils/scripts/context.py)
- **자동 색인·코드 재사용**: [utils/scripts/catalog.py](../../utils/scripts/catalog.py), [utils/scripts/watch.py](../../utils/scripts/watch.py), [utils/index.md](../../utils/index.md)
- **검증·수정 루프**: [utils/scripts/harness.py](../../utils/scripts/harness.py), [utils/scripts/loop.py](../../utils/scripts/loop.py), [docs/development/engineering-loop.md](../../docs/development/engineering-loop.md)
- **원본 복사·검증**: [utils/scripts/reuse.py](../../utils/scripts/reuse.py), [docs/reference/README.md](../../docs/reference/README.md)
- **작업별 전체 보고문 커밋**: [utils/scripts/commit_report.py](../../utils/scripts/commit_report.py), [docs/development/reports](../../docs/development/reports)
- **문화외출·이동 안내 검토**: [docs/development/tasks.md](../../docs/development/tasks.md), [docs/development/mobility-routing-review.md](../../docs/development/mobility-routing-review.md)
- **무인증·체험 프로필·브라우저 저장**: [docs/development/demo-profile-design.md](../../docs/development/demo-profile-design.md), [docs/development/examples/demo-users.sample.json](../../docs/development/examples/demo-users.sample.json)
- **해커톤 GPU 서버·매뉴얼**: [docs/development/hackathon-server-usage-review.md](../../docs/development/hackathon-server-usage-review.md), [docs/reference/hackathon-server/README.md](../../docs/reference/hackathon-server/README.md), [utils/scripts/read_pdf.py](../../utils/scripts/read_pdf.py)
- **framework·KONNECT 분석 우선 재사용**: [docs/development/konnect-reuse-reading-guide.md](../../docs/development/konnect-reuse-reading-guide.md)
- **키별 실동작·문화시설 추천화면 연결**: [backend/team_culture.js](../../backend/team_culture.js), [utils/scripts/check_service_keys.py](../../utils/scripts/check_service_keys.py), [utils/scripts/check_culture_ui.cjs](../../utils/scripts/check_culture_ui.cjs), [docs/development/service-key-status.md](../../docs/development/service-key-status.md)
- **자동 음성 시작 지연·첫 안내 선택·시간 진단**: [backend/team_chat.js](../../backend/team_chat.js), [backend/voice_session.js](../../backend/voice_session.js), [utils/scripts/check_voice_session.cjs](../../utils/scripts/check_voice_session.cjs), [utils/scripts/check_voice_navigation.cjs](../../utils/scripts/check_voice_navigation.cjs), [docs/development/voice-start-latency.md](../../docs/development/voice-start-latency.md), [backend/team_voice_actions.js](../../backend/team_voice_actions.js), [backend/preview.html](../../backend/preview.html), [utils/scripts/check_voice_diagnostics.cjs](../../utils/scripts/check_voice_diagnostics.cjs), [utils/scripts/check_microphone_meter.cjs](../../utils/scripts/check_microphone_meter.cjs)
- **자동 음성 대화·횟수/무응답 종료**: [backend/voice_session.js](../../backend/voice_session.js), [backend/team_chat.js](../../backend/team_chat.js), [utils/scripts/check_voice_session.cjs](../../utils/scripts/check_voice_session.cjs), [docs/development/automatic-voice.md](../../docs/development/automatic-voice.md)
- **공통 자동 대화·음성 화면 이동**: [backend/team_voice_actions.js](../../backend/team_voice_actions.js), [backend/team_chat.js](../../backend/team_chat.js), [backend/voice_session.js](../../backend/voice_session.js), [utils/scripts/check_voice_navigation.cjs](../../utils/scripts/check_voice_navigation.cjs), [utils/scripts/check_voice_session.cjs](../../utils/scripts/check_voice_session.cjs), [docs/development/automatic-voice.md](../../docs/development/automatic-voice.md)
- **마이크 자동 대화 켜기·끄기 표시**: [backend/team_chat.js](../../backend/team_chat.js), [utils/scripts/check_voice_session.cjs](../../utils/scripts/check_voice_session.cjs), [docs/development/automatic-voice.md](../../docs/development/automatic-voice.md)
- **듣는 중 파동·브라우저 음성 호환**: [backend/team_chat.js](../../backend/team_chat.js), [backend/voice_session.js](../../backend/voice_session.js), [utils/scripts/check_voice_session.cjs](../../utils/scripts/check_voice_session.cjs), [docs/development/voice-browser-compatibility.md](../../docs/development/voice-browser-compatibility.md)
- **기존 점검 화면→자동 대화 홈 진입**: [backend/preview.html](../../backend/preview.html), [utils/scripts/check_voice_entry.cjs](../../utils/scripts/check_voice_entry.cjs), [docs/development/automatic-voice.md](../../docs/development/automatic-voice.md)
- **단일 나들이 진입·실제 마이크 입력 미터**: [backend/team_app.py](../../backend/team_app.py), [backend/microphone_meter.js](../../backend/microphone_meter.js), [backend/preview_meter.js](../../backend/preview_meter.js), [backend/test_team_app.py](../../backend/test_team_app.py), [utils/scripts/check_unified_chat.cjs](../../utils/scripts/check_unified_chat.cjs), [utils/scripts/check_microphone_meter.cjs](../../utils/scripts/check_microphone_meter.cjs), [docs/development/unified-chat-and-meter.md](../../docs/development/unified-chat-and-meter.md)
- **대중교통 노선·모바일 경로 카드**: [backend/transit.py](../../backend/transit.py), [backend/preview.html](../../backend/preview.html), [backend/test_transit.py](../../backend/test_transit.py), [utils/scripts/check_transit_details.py](../../utils/scripts/check_transit_details.py), [utils/scripts/check_transit_mobile.cjs](../../utils/scripts/check_transit_mobile.cjs), [docs/development/transit-mobile.md](../../docs/development/transit-mobile.md)
- **음성 진단·실시간 중간 글자·새 채팅 인계**: [backend/team_chat.js](../../backend/team_chat.js), [backend/voice_session.js](../../backend/voice_session.js), [utils/scripts/check_voice_diagnostics.cjs](../../utils/scripts/check_voice_diagnostics.cjs), [docs/development/next-chat-handoff.md](../../docs/development/next-chat-handoff.md)
- **사진 지정 초기 설정 폼 복원·휴대폰 화면**: [backend/team_chat.js](../../backend/team_chat.js), [backend/team_culture.js](../../backend/team_culture.js), [utils/scripts/check_voice_navigation.cjs](../../utils/scripts/check_voice_navigation.cjs), [docs/development/qa-simple-settings](../../docs/development/qa-simple-settings)
- **진행 점검·공유·충돌 통합**: [docs/development/release-checklist.md](../../docs/development/release-checklist.md)
- **배포 키 환경변수·공공데이터·Naito**: [backend/deploy.env.example](../../backend/deploy.env.example), [backend/test_deployment_keys.py](../../backend/test_deployment_keys.py), [docs/development/deployment-keys.md](../../docs/development/deployment-keys.md)

## 심볼 → 정의 파일

| 심볼 | 위치 | 개요 |
|---|---|---|
| `$` | [backend/team_chat.js:69](../../backend/team_chat.js#L69) | JS/TS 정규식 후보; AST 검증 아님 |
| `$` | [frontend/js/util.js:4](../../frontend/js/util.js#L4) | JS/TS 정규식 후보; AST 검증 아님 |
| `$$` | [frontend/js/util.js:6](../../frontend/js/util.js#L6) | JS/TS 정규식 후보; AST 검증 아님 |
| `actions` | [frontend/js/chat.js:165](../../frontend/js/chat.js#L165) | JS/TS 정규식 후보; AST 검증 아님 |
| `allowed_origins` | [backend/preview.py:24](../../backend/preview.py#L24) | 환경변수의 명시적 HTTP(S) origin만 허용한다. 와일드카드·경로·자격정보는 제외한다. |
| `answer` | [frontend/js/chat.js:580](../../frontend/js/chat.js#L580) | JS/TS 정규식 후보; AST 검증 아님 |
| `api_key` | [backend/transit.py:20](../../backend/transit.py#L20) | 전용 환경변수 또는 로컬 제외 파일의 키 한 개만 읽는다. 값은 응답·로그에 출력하지 않는다. |
| `app_asset` | [backend/team_app.py:32](../../backend/team_app.py#L32) | 현재 /app/ 요청의 제한된 정적 자산을 반환한다. 경로이탈/비밀파일/과대 파일은 거절한다. |
| `app_directory` | [backend/team_app.py:12](../../backend/team_app.py#L12) | .local의 인계 패키지 frontend만 선택한다. 미설정/손상은 경로 노출 없이 미연결로 처리한다. |
| `apply` | [backend/preferences.py:50](../../backend/preferences.py#L50) | 무료/예산/명시 제외를 적용하고 관심 키워드·직선 근접성으로 정렬한다. 미확인은 숨기지 않는다. |
| `apply` | [frontend/js/app.js:177](../../frontend/js/app.js#L177) | JS/TS 정규식 후보; AST 검증 아님 |
| `apply` | [frontend/js/chat.js:227](../../frontend/js/chat.js#L227) | JS/TS 정규식 후보; AST 검증 아님 |
| `apply.order` | [backend/preferences.py:78](../../backend/preferences.py#L78) | 걷기 최소 선호 시 근접성 먼저, 그 외 관심어 먼저. 실제 도보 시간으로 간주하지 않는다. |
| `apply_interpretation` | [backend/chat_conditions.py:106](../../backend/chat_conditions.py#L106) | 해석 결과를 복사한 초안에 반영한다. 확정값 충돌·늦은 응답은 자동 반영하지 않는다. |
| `applyDraft` | [backend/team_chat.js:293](../../backend/team_chat.js#L293) | JS/TS 정규식 후보; AST 검증 아님 |
| `begin` | [backend/voice_session.js:33](../../backend/voice_session.js#L33) | JS/TS 정규식 후보; AST 검증 아님 |
| `begin` | [frontend/js/chat.js:418](../../frontend/js/chat.js#L418) | JS/TS 정규식 후보; AST 검증 아님 |
| `beginVoiceDiagnostics` | [backend/team_chat.js:110](../../backend/team_chat.js#L110) | JS/TS 정규식 후보; AST 검증 아님 |
| `broken_links` | [utils/scripts/harness.py:49](../../utils/scripts/harness.py#L49) | Check relative inline links outside fenced code; skip URLs and anchors. |
| `bubble` | [frontend/js/chat.js:135](../../frontend/js/chat.js#L135) | JS/TS 정규식 후보; AST 검증 아님 |
| `build_course` | [backend/course.py:102](../../backend/course.py#L102) | 사용자 출발 좌표와 공개 후보의 도보 초를 한 번 조회해 가장 짧은 가능한 조합을 선택한다. |
| `button` | [frontend/js/util.js:22](../../frontend/js/util.js#L22) | JS/TS 정규식 후보; AST 검증 아님 |
| `cachedGreeting` | [frontend/js/weather.js:68](../../frontend/js/weather.js#L68) | JS/TS 정규식 후보; AST 검증 아님 |
| `call` | [backend/tour_places.py:20](../../backend/tour_places.py#L20) | 공식 고정 주소로 호출하며 응답 크기/형식을 제한한다. 원본 URL/키 포함 오류를 반환하지 않는다. |
| `cancel` | [backend/voice_session.js:110](../../backend/voice_session.js#L110) | JS/TS 정규식 후보; AST 검증 아님 |
| `cancel` | [backend/voice_session.js:26](../../backend/voice_session.js#L26) | JS/TS 정규식 후보; AST 검증 아님 |
| `cancelVoiceRequest` | [backend/team_chat.js:411](../../backend/team_chat.js#L411) | JS/TS 정규식 후보; AST 검증 아님 |
| `candidateById` | [frontend/js/state.js:54](../../frontend/js/state.js#L54) | JS/TS 정규식 후보; AST 검증 아님 |
| `candidateIndex` | [backend/team_voice_actions.js:18](../../backend/team_voice_actions.js#L18) | JS/TS 정규식 후보; AST 검증 아님 |
| `candidateSpeech` | [backend/team_voice_actions.js:55](../../backend/team_voice_actions.js#L55) | JS/TS 정규식 후보; AST 검증 아님 |
| `card` | [frontend/js/chat.js:115](../../frontend/js/chat.js#L115) | JS/TS 정규식 후보; AST 검증 아님 |
| `chat` | [backend/naito_chat.py:128](../../backend/naito_chat.py#L128) | 대화 API 결과를 (HTTP상태, 본문)으로 반환한다. 장애 시 가짜 해석/추천으로 대체하지 않는다. |
| `ChatConditionTests` | [backend/test_chat_conditions.py:8](../../backend/test_chat_conditions.py#L8) | 공급자와 프론트가 연결되기 전에 검증할 독립적인 대화 상태 사례다. |
| `ChatConditionTests.apply` | [backend/test_chat_conditions.py:17](../../backend/test_chat_conditions.py#L17) | 현재 입력의 revision 2에 대한 해석을 적용한다. |
| `ChatConditionTests.resolve` | [backend/test_chat_conditions.py:22](../../backend/test_chat_conditions.py#L22) | 초안이 변하지 않은 상태에서 사용자 동의/거절을 적용한다. |
| `ChatConditionTests.setUp` | [backend/test_chat_conditions.py:11](../../backend/test_chat_conditions.py#L11) | 검증된 출발 좌표와 정확히 60분인 조건을 준비한다. |
| `ChatConditionTests.test_59_rejected_60_allowed` | [backend/test_chat_conditions.py:73](../../backend/test_chat_conditions.py#L73) | 최소60분 규칙은 기존 추천 서버 검증을 그대로 사용한다. |
| `ChatConditionTests.test_bad_or_factual_model_output_rejected` | [backend/test_chat_conditions.py:87](../../backend/test_chat_conditions.py#L87) | 좌표/행사 사실/비정상 형식은 해석 결과로 받지 않는다. |
| `ChatConditionTests.test_category_and_no_mutation` | [backend/test_chat_conditions.py:26](../../backend/test_chat_conditions.py#L26) | 국악 해석은 초안에만 반영하고 원본·최종 확인 경계를 유지한다. |
| `ChatConditionTests.test_changed_origin_invalidates_coordinates_only_on_accept` | [backend/test_chat_conditions.py:55](../../backend/test_chat_conditions.py#L55) | 새 출발지 동의 뒤 기존 좌표를 재사용하지 않으며 거절하면 보존한다. |
| `ChatConditionTests.test_confirmed_accept_reject_and_pending` | [backend/test_chat_conditions.py:43](../../backend/test_chat_conditions.py#L43) | 확정 분류 변경은 수락/거절/미응답을 구분한다. |
| `ChatConditionTests.test_course_requires_stay_and_alias` | [backend/test_chat_conditions.py:80](../../backend/test_chat_conditions.py#L80) | route는 course로 정규화하고 체류시간을 임의 기본값으로 채우지 않는다. |
| `ChatConditionTests.test_invalid_decisions_and_state` | [backend/test_chat_conditions.py:103](../../backend/test_chat_conditions.py#L103) | 문자열 동의·모르는 항목·비정상 revision을 거절한다. |
| `ChatConditionTests.test_missing_question_and_no_default_origin` | [backend/test_chat_conditions.py:35](../../backend/test_chat_conditions.py#L35) | 비어 있는 입력에는 출발지 질문 하나와 전체 누락 항목을 반환한다. |
| `ChatConditionTests.test_null_no_change_and_timezone` | [backend/test_chat_conditions.py:97](../../backend/test_chat_conditions.py#L97) | null은 삭제가 아니며 시각은 한국 시간으로 바꾼다. |
| `ChatConditionTests.test_stale_response_and_manual_edit` | [backend/test_chat_conditions.py:64](../../backend/test_chat_conditions.py#L64) | AI 응답/동의 대기 중 직접 수정된 현재값은 보존한다. |
| `check` | [utils/scripts/catalog.py:225](../../utils/scripts/catalog.py#L225) | Return missing or stale generated indexes; tolerate Git line endings. |
| `checkedAt` | [frontend/js/util.js:57](../../frontend/js/util.js#L57) | JS/TS 정규식 후보; AST 검증 아님 |
| `chip` | [frontend/js/chat.js:168](../../frontend/js/chat.js#L168) | JS/TS 정규식 후보; AST 검증 아님 |
| `clear` | [frontend/js/chat.js:396](../../frontend/js/chat.js#L396) | JS/TS 정규식 후보; AST 검증 아님 |
| `clearShapes` | [backend/location_view.js:9](../../backend/location_view.js#L9) | JS/TS 정규식 후보; AST 검증 아님 |
| `closer` | [frontend/js/chat.js:744](../../frontend/js/chat.js#L744) | JS/TS 정규식 후보; AST 검증 아님 |
| `closeSheet` | [frontend/js/place.js:122](../../frontend/js/place.js#L122) | JS/TS 정규식 후보; AST 검증 아님 |
| `code_checks` | [utils/scripts/harness.py:20](../../utils/scripts/harness.py#L20) | Parse Python statically and require module/function/class docstrings. |
| `compact` | [utils/scripts/catalog.py:63](../../utils/scripts/catalog.py#L63) | Return one short Markdown-safe line from a docstring. |
| `conditionLabel` | [backend/team_chat.js:338](../../backend/team_chat.js#L338) | JS/TS 정규식 후보; AST 검증 아님 |
| `config` | [utils/scripts/catalog.py:21](../../utils/scripts/catalog.py#L21) | Read only the public harness configuration, never environment values. |
| `contents` | [utils/scripts/verify_watch.py:24](../../utils/scripts/verify_watch.py#L24) | Read generated text, tolerating a brief replacement window. |
| `coordinate` | [backend/outing.py:30](../../backend/outing.py#L30) | 유한한 위경도 숫자를 검증하고 잘못된 입력은 ValueError로 알린다. |
| `course_alternatives` | [backend/course.py:69](../../backend/course.py#L69) | 동의 요청에만 같은 시간 한 곳·최대 두 시간 이른 두 곳의 검증된 대안을 반환한다. |
| `CourseTests` | [backend/test_course.py:9](../../backend/test_course.py#L9) | 전시와 고정 공연이 있는 당일 요청을 독립적으로 검증한다. |
| `CourseTests.setUp` | [backend/test_course.py:12](../../backend/test_course.py#L12) | 한국 시각 한 시간과 20분씩 관람할 수 있는 두 전시를 준비한다. |
| `CourseTests.test_alternative_unknown_missing_and_day_boundary` | [backend/test_course.py:67](../../backend/test_course.py#L67) | 미확인 시간·누락 구간을 가능으로 만들지 않고 이전 날짜로 옮기지 않는다. |
| `CourseTests.test_boundary` | [backend/test_course.py:21](../../backend/test_course.py#L21) | 도보 두 구간과 관람이 마감에 딱 맞으면 허용하고 1초 초과하면 제외한다. |
| `CourseTests.test_consent_and_alternatives` | [backend/test_course.py:47](../../backend/test_course.py#L47) | 동의 없이는 대안을 만들지 않고 종료·체류를 보존한 한 곳/이른 출발을 계산한다. |
| `CourseTests.test_order_and_missing_routes` | [backend/test_course.py:36](../../backend/test_course.py#L36) | 순서를 바꿔 가능한 일정만 선택하고 누락된 구간은 이동 0초로 쓰지 않는다. |
| `CourseTests.test_unknown_and_wait` | [backend/test_course.py:26](../../backend/test_course.py#L26) | 공연 시작 전 대기는 포함하고 종료 미상 또는 휴관 조건 미상은 확정하지 않는다. |
| `create` | [backend/map_view.js:49](../../backend/map_view.js#L49) | JS/TS 정규식 후보; AST 검증 아님 |
| `credit` | [frontend/js/place.js:224](../../frontend/js/place.js#L224) | JS/TS 정규식 후보; AST 검증 아님 |
| `culture_key` | [backend/culture_config.py:6](../../backend/culture_config.py#L6) | seoul/tour 키를 읽는다. 명시 환경값이 로컬 파일보다 우선하며 미설정은 빈 문자열이다. |
| `culture_places` | [backend/tour_places.py:114](../../backend/tour_places.py#L114) | 선택적 문화시설 API. 키 없음503/조회 실패502/정상0건을 구분하며 행사 추천에 몰래 혼합하지 않는다. |
| `culture_places.details` | [backend/tour_places.py:134](../../backend/tour_places.py#L134) | 동일 ID의 소개/홈페이지를 가져온다. 상세 호출 실패를 값 없음으로 숨기지 않는다. |
| `cultureLabel` | [backend/team_culture.js:5](../../backend/team_culture.js#L5) | JS/TS 정규식 후보; AST 검증 아님 |
| `CultureSourceTests` | [backend/test_culture_sources.py:13](../../backend/test_culture_sources.py#L13) | 실제 키 없이 가능한 공급자 계약 회귀. 실서비스 성공과 구분한다. |
| `CultureSourceTests.response` | [backend/test_culture_sources.py:22](../../backend/test_culture_sources.py#L22) | 공식 response/header/body 형태를 생성한다. 실제 행사 데이터가 아니다. |
| `CultureSourceTests.setUp` | [backend/test_culture_sources.py:16](../../backend/test_culture_sources.py#L16) | 공개 위치의 시험 입력과 가상 문화시설 응답을 준비한다. |
| `CultureSourceTests.test_detail_identity_and_html` | [backend/test_culture_sources.py:71](../../backend/test_culture_sources.py#L71) | 상세 ID 불일치를 거절하고 공식 텍스트/링크만 정규화한다. |
| `CultureSourceTests.test_facility_facts_and_unknowns` | [backend/test_culture_sources.py:61](../../backend/test_culture_sources.py#L61) | 상설 장소에 행사 날짜/가격/공연 시작을 만들어 넣지 않는다. |
| `CultureSourceTests.test_full_facility_lookup_budget_and_secrets` | [backend/test_culture_sources.py:101](../../backend/test_culture_sources.py#L101) | 목록→소개→공통 상세를 연결하고 무료 조건·비밀값 비노출을 확인한다. |
| `CultureSourceTests.test_full_facility_lookup_budget_and_secrets.source` | [backend/test_culture_sources.py:103](../../backend/test_culture_sources.py#L103) | 세 고정 API의 모의 응답을 반환한다. |
| `CultureSourceTests.test_homepage_with_provider_annotation` | [backend/test_culture_sources.py:82](../../backend/test_culture_sources.py#L82) | 실제 응답의 홈페이지 뒤 SNS 안내는 제외하고 잘못된 링크는 null로 둔다. |
| `CultureSourceTests.test_scope_and_missing_key_before_network` | [backend/test_culture_sources.py:92](../../backend/test_culture_sources.py#L92) | 공연/코스/기록/잘못된반경 요청은 거절하고 키없음은503이다. |
| `CultureSourceTests.test_seoul_auth_failure_no_sample_retry` | [backend/test_culture_sources.py:37](../../backend/test_culture_sources.py#L37) | 유효하지 않은 정식 키를 sample 성공으로 숨기지 않는다. |
| `CultureSourceTests.test_seoul_authenticated_and_sample_limits` | [backend/test_culture_sources.py:27](../../backend/test_culture_sources.py#L27) | 정식 키1000건·미설정sample5건을 구분하며 입력 키를 경로 구분자로 해석하지 않는다. |
| `CultureSourceTests.test_source_failure_not_empty_or_partial_success` | [backend/test_culture_sources.py:116](../../backend/test_culture_sources.py#L116) | 실패·권한거절·제한을0건으로 바꾸지 않고 URL에 있는 키를 오류로 내보내지 않는다. |
| `CultureSourceTests.test_tour_request_encoding_and_axis` | [backend/test_culture_sources.py:45](../../backend/test_culture_sources.py#L45) | 국문 고정 주소·경도X/위도Y·인코딩키 1회 변환을 검사한다. |
| `CultureSourceTests.test_tour_zero_vs_malformed` | [backend/test_culture_sources.py:55](../../backend/test_culture_sources.py#L55) | 0건은 정상이며 누락 목록/오류코드/XML은 정상 빈 결과가 아니다. |
| `currentCandidate` | [backend/team_voice_actions.js:47](../../backend/team_voice_actions.js#L47) | JS/TS 정규식 후보; AST 검증 아님 |
| `d` | [frontend/js/chat.js:41](../../frontend/js/chat.js#L41) | JS/TS 정규식 후보; AST 검증 아님 |
| `decide` | [backend/team_chat.js:346](../../backend/team_chat.js#L346) | JS/TS 정규식 후보; AST 검증 아님 |
| `decode_shape` | [backend/walking.py:50](../../backend/walking.py#L50) | Valhalla polyline6를 위도·경도 배열로 변환한다. 손상·범위 초과는 ValueError다. |
| `DeploymentKeyTests` | [backend/test_deployment_keys.py:10](../../backend/test_deployment_keys.py#L10) | 환경변수 기반 배포와 로컬 개발의 설정 경계를 확인한다. |
| `DeploymentKeyTests.test_culture_environment_precedence` | [backend/test_deployment_keys.py:13](../../backend/test_deployment_keys.py#L13) | 서울시/공공데이터 표준명과 호환명을 환경에서 읽으면 로컬 파일을 열지 않는다. |
| `DeploymentKeyTests.test_explicit_empty_naito_and_culture_disable_local_keys` | [backend/test_deployment_keys.py:28](../../backend/test_deployment_keys.py#L28) | 서버에서 명시적으로 비운 공공데이터/Naito 키를 개인 파일로 몰래 대체하지 않는다. |
| `DeploymentKeyTests.test_naito_environment_precedence` | [backend/test_deployment_keys.py:21](../../backend/test_deployment_keys.py#L21) | 로컬 파일이 존재해도 서버 환경의 Naito 키/모델이 우선한다. |
| `DeploymentKeyTests.test_rest_environment_precedence` | [backend/test_deployment_keys.py:36](../../backend/test_deployment_keys.py#L36) | 서버 REST 키가 있으면 개인 파일을 읽지 않는다. 공개 지도 설정과 혼동하지 않는다. |
| `describe` | [utils/scripts/catalog.py:69](../../utils/scripts/catalog.py#L69) | Extract file overview, fingerprint, imports and symbol locations statically. |
| `describe.visit` | [utils/scripts/catalog.py:79](../../utils/scripts/catalog.py#L79) | Walk definitions and keep qualified names for nested functions. |
| `distance_km` | [backend/outing.py:127](../../backend/outing.py#L127) | 두 좌표의 대권거리(km)를 구한다. 보행·대중교통 이동시간을 뜻하지 않는다. |
| `distanceText` | [frontend/js/chat.js:705](../../frontend/js/chat.js#L705) | JS/TS 정규식 후보; AST 검증 아님 |
| `doSave` | [frontend/js/place.js:101](../../frontend/js/place.js#L101) | JS/TS 정규식 후보; AST 검증 아님 |
| `draft` | [backend/team_chat.js:157](../../backend/team_chat.js#L157) | JS/TS 정규식 후보; AST 검증 아님 |
| `draw` | [frontend/js/place.js:170](../../frontend/js/place.js#L170) | JS/TS 정규식 후보; AST 검증 아님 |
| `drawWave` | [backend/microphone_meter.js:94](../../backend/microphone_meter.js#L94) | JS/TS 정규식 후보; AST 검증 아님 |
| `el` | [frontend/js/util.js:14](../../frontend/js/util.js#L14) | JS/TS 정규식 후보; AST 검증 아님 |
| `empty` | [frontend/js/state.js:12](../../frontend/js/state.js#L12) | JS/TS 정규식 후보; AST 검증 아님 |
| `endDemo` | [frontend/js/saved.js:38](../../frontend/js/saved.js#L38) | JS/TS 정규식 후보; AST 검증 아님 |
| `endpoint` | [backend/naito_chat.py:26](../../backend/naito_chat.py#L26) | 호출 주소 (허용된 세 곳 중 하나). |
| `EndpointTest` | [backend/test_naito_chat.py:90](../../backend/test_naito_chat.py#L90) | 개요 없음 |
| `EndpointTest.test_openai_request_and_response` | [backend/test_naito_chat.py:103](../../backend/test_naito_chat.py#L103) | OpenAI 형식: Bearer 키, system+user 메시지, JSON 응답을 꺼내요. |
| `EndpointTest.test_provider_switch` | [backend/test_naito_chat.py:91](../../backend/test_naito_chat.py#L91) | 설정한 제공자 주소로만 호출하고, 모르는 값이면 해커톤 주소. 키 모양으로 추측하지 않는다. |
| `entries` | [utils/scripts/catalog.py:113](../../utils/scripts/catalog.py#L113) | Describe every active code file once; do not scan historical snapshots. |
| `expected` | [utils/scripts/context.py:42](../../utils/scripts/context.py#L42) | Read the configured public state file and generate the brief. |
| `extract_conditions` | [backend/naito_chat.py:94](../../backend/naito_chat.py#L94) | 공식 사용자 제공 주소로 1회 호출한다. 좌표는 보내지 않고 응답 최대64KiB/20초로 제한한다. |
| `fallback` | [frontend/js/util.js:152](../../frontend/js/util.js#L152) | JS/TS 정규식 후보; AST 검증 아님 |
| `file_hash` | [utils/scripts/reuse.py:33](../../utils/scripts/reuse.py#L33) | Hash file contents in chunks without logging their values. |
| `file_overview` | [utils/scripts/catalog.py:138](../../utils/scripts/catalog.py#L138) | Describe a file using only its static overview, heading, or file type. |
| `file_voice_available` | [backend/local_voice.py:25](../../backend/local_voice.py#L25) | Windows 파일 합성 지원 여부만 반환한다. 음성 설치·합성 성공은 별도 검증한다. |
| `fill` | [frontend/js/app.js:139](../../frontend/js/app.js#L139) | JS/TS 정규식 후보; AST 검증 아님 |
| `findStart` | [frontend/js/chat.js:587](../../frontend/js/chat.js#L587) | JS/TS 정규식 후보; AST 검증 아님 |
| `finish` | [backend/voice_session.js:102](../../backend/voice_session.js#L102) | JS/TS 정규식 후보; AST 검증 아님 |
| `finish` | [backend/voice_session.js:12](../../backend/voice_session.js#L12) | JS/TS 정규식 후보; AST 검증 아님 |
| `finish` | [frontend/js/chat.js:267](../../frontend/js/chat.js#L267) | JS/TS 정규식 후보; AST 검증 아님 |
| `flat` | [frontend/js/chat.js:333](../../frontend/js/chat.js#L333) | JS/TS 정규식 후보; AST 검증 아님 |
| `flat` | [frontend/js/chat.js:357](../../frontend/js/chat.js#L357) | JS/TS 정규식 후보; AST 검증 아님 |
| `fmtMin` | [frontend/js/place.js:277](../../frontend/js/place.js#L277) | JS/TS 정규식 후보; AST 검증 아님 |
| `formatDate` | [frontend/js/util.js:42](../../frontend/js/util.js#L42) | JS/TS 정규식 후보; AST 검증 아님 |
| `formatTime` | [frontend/js/util.js:49](../../frontend/js/util.js#L49) | JS/TS 정규식 후보; AST 검증 아님 |
| `fromServerDraft` | [frontend/js/chat.js:485](../../frontend/js/chat.js#L485) | JS/TS 정규식 후보; AST 검증 아님 |
| `generated_paths` | [utils/scripts/catalog.py:150](../../utils/scripts/catalog.py#L150) | Return the actual output paths, independent of optional configuration hints. |
| `getEngine` | [frontend/js/place.js:151](../../frontend/js/place.js#L151) | JS/TS 정규식 후보; AST 검증 아님 |
| `greetingFor` | [frontend/js/weather.js:29](../../frontend/js/weather.js#L29) | JS/TS 정규식 후보; AST 검증 아님 |
| `handle` | [frontend/js/chat.js:518](../../frontend/js/chat.js#L518) | JS/TS 정규식 후보; AST 검증 아님 |
| `handleAction` | [backend/team_chat.js:220](../../backend/team_chat.js#L220) | JS/TS 정규식 후보; AST 검증 아님 |
| `Handler` | [frontend/dev_server.py:19](../../frontend/dev_server.py#L19) | 정적 파일은 그대로, /preview/ 로 시작하는 POST 는 백엔드로 전달해요. |
| `Handler.do_POST` | [frontend/dev_server.py:22](../../frontend/dev_server.py#L22) | 백엔드 응답의 상태 코드와 본문을 바꾸지 않고 돌려줘요. |
| `hhmm` | [frontend/js/util.js:33](../../frontend/js/util.js#L33) | JS/TS 정규식 후보; AST 검증 아님 |
| `icon` | [frontend/js/place.js:188](../../frontend/js/place.js#L188) | JS/TS 정규식 후보; AST 검증 아님 |
| `inGroup` | [frontend/js/chat.js:30](../../frontend/js/chat.js#L30) | JS/TS 정규식 후보; AST 검증 아님 |
| `initChat` | [frontend/js/chat.js:778](../../frontend/js/chat.js#L778) | JS/TS 정규식 후보; AST 검증 아님 |
| `initCulture` | [backend/team_culture.js:11](../../backend/team_culture.js#L11) | JS/TS 정규식 후보; AST 검증 아님 |
| `initLanding` | [frontend/js/app.js:45](../../frontend/js/app.js#L45) | JS/TS 정규식 후보; AST 검증 아님 |
| `initMe` | [frontend/js/app.js:195](../../frontend/js/app.js#L195) | JS/TS 정규식 후보; AST 검증 아님 |
| `initNavigation` | [frontend/js/app.js:215](../../frontend/js/app.js#L215) | JS/TS 정규식 후보; AST 검증 아님 |
| `initNotify` | [frontend/js/app.js:145](../../frontend/js/app.js#L145) | JS/TS 정규식 후보; AST 검증 아님 |
| `initPlace` | [frontend/js/place.js:348](../../frontend/js/place.js#L348) | JS/TS 정규식 후보; AST 검증 아님 |
| `InputError` | [backend/outing.py:20](../../backend/outing.py#L20) | 추천 입력 오류의 공개 코드·필드·안내문을 담는다. 원본 입력값은 포함하지 않는다. |
| `InputError.__init__` | [backend/outing.py:23](../../backend/outing.py#L23) | HTTP 오류 응답과 필드별 안내에 사용할 고정 메타데이터를 보관한다. |
| `inspectVoiceEnvironment` | [backend/team_chat.js:91](../../backend/team_chat.js#L91) | JS/TS 정규식 후보; AST 검증 아님 |
| `integrate_index` | [utils/scripts/prepare_chat_handoff.py:17](../../utils/scripts/prepare_chat_handoff.py#L17) | 원본 HTML에 모듈을 한 번만 연결한다. 이미 연결되거나 구조가 다르면 거절한다. |
| `integrate_results` | [utils/scripts/prepare_chat_handoff.py:38](../../utils/scripts/prepare_chat_handoff.py#L38) | 추천·상세의 출처 표시만 확장하며 같은 후보 ID/지도/카드 흐름을 유지한다. |
| `integrate_search` | [utils/scripts/prepare_chat_handoff.py:24](../../utils/scripts/prepare_chat_handoff.py#L24) | 확정 요청과 S02a 요약의 두 지점만 확장한다. 다른 팀 변경을 추측해 덮어쓰지 않는다. |
| `interpret` | [frontend/js/chat.js:497](../../frontend/js/chat.js#L497) | JS/TS 정규식 후보; AST 검증 아님 |
| `invalidate` | [backend/team_chat.js:373](../../backend/team_chat.js#L373) | JS/TS 정규식 후보; AST 검증 아님 |
| `isDebug` | [frontend/js/util.js:90](../../frontend/js/util.js#L90) | JS/TS 정규식 후보; AST 검증 아님 |
| `isEcho` | [frontend/js/chat.js:354](../../frontend/js/chat.js#L354) | JS/TS 정규식 후보; AST 검증 아님 |
| `isSaved` | [frontend/js/saved.js:16](../../frontend/js/saved.js#L16) | JS/TS 정규식 후보; AST 검증 아님 |
| `isSignedIn` | [frontend/js/saved.js:8](../../frontend/js/saved.js#L8) | JS/TS 정규식 후보; AST 검증 아님 |
| `isTest` | [frontend/js/util.js:86](../../frontend/js/util.js#L86) | JS/TS 정규식 후보; AST 검증 아님 |
| `joinResults` | [frontend/js/chat.js:330](../../frontend/js/chat.js#L330) | JS/TS 정규식 후보; AST 검증 아님 |
| `josa` | [frontend/js/chat.js:45](../../frontend/js/chat.js#L45) | JS/TS 정규식 후보; AST 검증 아님 |
| `known_price` | [backend/preferences.py:39](../../backend/preferences.py#L39) | 공식 무료 표시 또는 단일 원화 가격만 판독한다. 할인/복수 좌석/범위는 미확인이다. |
| `lastQuestion` | [frontend/js/chat.js:549](../../frontend/js/chat.js#L549) | JS/TS 정규식 후보; AST 검증 아님 |
| `list` | [frontend/js/chat.js:688](../../frontend/js/chat.js#L688) | JS/TS 정규식 후보; AST 검증 아님 |
| `listen` | [backend/voice_session.js:162](../../backend/voice_session.js#L162) | JS/TS 정규식 후보; AST 검증 아님 |
| `listen` | [frontend/js/chat.js:383](../../frontend/js/chat.js#L383) | JS/TS 정규식 후보; AST 검증 아님 |
| `listenForReply` | [backend/voice_session.js:4](../../backend/voice_session.js#L4) | JS/TS 정규식 후보; AST 검증 아님 |
| `liveBubble` | [frontend/js/chat.js:234](../../frontend/js/chat.js#L234) | JS/TS 정규식 후보; AST 검증 아님 |
| `ll` | [backend/map_view.js:53](../../backend/map_view.js#L53) | JS/TS 정규식 후보; AST 검증 아님 |
| `load` | [backend/map_view.js:22](../../backend/map_view.js#L22) | JS/TS 정규식 후보; AST 검증 아님 |
| `load` | [frontend/js/state.js:27](../../frontend/js/state.js#L27) | JS/TS 정규식 후보; AST 검증 아님 |
| `loadKakao` | [frontend/js/place.js:133](../../frontend/js/place.js#L133) | JS/TS 정규식 후보; AST 검증 아님 |
| `loadTransit` | [frontend/js/place.js:301](../../frontend/js/place.js#L301) | JS/TS 정규식 후보; AST 검증 아님 |
| `loadWalk` | [frontend/js/place.js:249](../../frontend/js/place.js#L249) | JS/TS 정규식 후보; AST 검증 아님 |
| `logVoice` | [backend/team_chat.js:74](../../backend/team_chat.js#L74) | JS/TS 정규식 후보; AST 검증 아님 |
| `longEnough` | [frontend/js/parse.js:94](../../frontend/js/parse.js#L94) | JS/TS 정규식 후보; AST 검증 아님 |
| `main` | [utils/scripts/catalog.py:232](../../utils/scripts/catalog.py#L232) | Write, validate, or search the catalog with bounded console output. |
| `main` | [utils/scripts/check_chat_api.py:35](../../utils/scripts/check_chat_api.py#L35) | 외부 키 사용 없이 4개 HTTP 구간을 검사하고 임시 서버를 반드시 종료한다. |
| `main` | [utils/scripts/check_chat_live.py:18](../../utils/scripts/check_chat_live.py#L18) | 국악·장소/시간·확정 시간 변경을 1회씩 호출하고 사실 경계와 충돌 보존을 검사한다. |
| `main` | [utils/scripts/check_conversation_edges.py:19](../../utils/scripts/check_conversation_edges.py#L19) | 독립 예산·제외·제약·시간 시나리오를 실행하고 조건 유지/해제를 명시적으로 검사한다. |
| `main` | [utils/scripts/check_culture_sources.py:30](../../utils/scripts/check_culture_sources.py#L30) | 서울시 실제 조회와 TourAPI 설정/실조회를 명확히 나누어 결과를 저장한다. |
| `main` | [utils/scripts/check_service_keys.py:16](../../utils/scripts/check_service_keys.py#L16) | 공개 청량리역 조건으로 서비스별 결과를 요약한다. HTTP200과 실제 기능 성공을 구분한다. |
| `main` | [utils/scripts/check_transit_details.py:15](../../utils/scripts/check_transit_details.py#L15) | 고정 청량리역→서울돈화문국악당 구간을 실조회하고 확인된 공개 경로 필드만 기록한다. |
| `main` | [utils/scripts/commit_report.py:52](../../utils/scripts/commit_report.py#L52) | Check by default; stage and commit only when --commit is explicitly given. |
| `main` | [utils/scripts/context.py:48](../../utils/scripts/context.py#L48) | Write, check, or print only the short restart brief. |
| `main` | [utils/scripts/harness.py:88](../../utils/scripts/harness.py#L88) | Run the harness once; fixing failures requires a separately scoped change. |
| `main` | [utils/scripts/loop.py:40](../../utils/scripts/loop.py#L40) | Persist only task evidence; never run shell, LLM, network or Git writes. |
| `main` | [utils/scripts/prepare_chat_handoff.py:124](../../utils/scripts/prepare_chat_handoff.py#L124) | 명시한 로컬 Git ref로 인계 산출물을 생성한다. 네트워크/push/checkout/merge는 하지 않는다. |
| `main` | [utils/scripts/read_pdf.py:33](../../utils/scripts/read_pdf.py#L33) | Extract page-delimited local evidence and display masked page text. |
| `main` | [utils/scripts/reuse.py:77](../../utils/scripts/reuse.py#L77) | Compare two files or copy an explicitly selected local Git snapshot. |
| `main` | [utils/scripts/team_chat_preview.py:35](../../utils/scripts/team_chat_preview.py#L35) | 루프백에만 서버를 띄워 팀 HTML과 기존 API 프록시에 독립 모듈을 붙인다. |
| `main` | [utils/scripts/verify_watch.py:32](../../utils/scripts/verify_watch.py#L32) | Verify creation, symbol/overview changes and deletion; clean our probe. |
| `main` | [utils/scripts/watch.py:39](../../utils/scripts/watch.py#L39) | Watch in a cooperative single-process loop; retain errors in local status. |
| `main.Handler` | [utils/scripts/team_chat_preview.py:46](../../utils/scripts/team_chat_preview.py#L46) | 팀 프록시/정적 서빙을 유지하고 index와 채팅 모듈 두 경로만 추가한다. |
| `main.Handler.do_GET` | [utils/scripts/team_chat_preview.py:49](../../utils/scripts/team_chat_preview.py#L49) | 원본 HTML을 디스크에 수정하지 않고 모듈 script를 응답에만 추가한다. |
| `main.run` | [utils/scripts/check_conversation_edges.py:31](../../utils/scripts/check_conversation_edges.py#L31) | 변경된 초안과 결과를 기록한다. 실패 원문은 정규화된 시험 응답만 남긴다. |
| `map_config` | [backend/map_config.py:9](../../backend/map_config.py#L9) | 환경변수 우선으로 JS 키를 반환한다. 미설정은 기존 지도를 유지하며 값은 로그하지 않는다. |
| `mapConfig` | [frontend/js/api.js:127](../../frontend/js/api.js#L127) | JS/TS 정규식 후보; AST 검증 아님 |
| `MapConfigTests` | [backend/test_map_config.py:8](../../backend/test_map_config.py#L8) | 실제 로컬 키를 읽지 않고 환경·파일 우선순위와 공개 범위를 점검한다. |
| `MapConfigTests.test_file_or_missing_key` | [backend/test_map_config.py:18](../../backend/test_map_config.py#L18) | BOM 허용 파일의 정확한 변수만 읽고 미설정·부적절한 값은 기본 지도로 남긴다. |
| `MapConfigTests.test_key_priority_and_public_scope` | [backend/test_map_config.py:11](../../backend/test_map_config.py#L11) | 환경변수의 JS 키만 공개하고 REST 키나 로컬 파일은 조회하지 않는다. |
| `markdown_files` | [utils/scripts/harness.py:39](../../utils/scripts/harness.py#L39) | Select active documentation, excluding copied PRDs and historical snapshots. |
| `measure` | [backend/microphone_meter.js:34](../../backend/microphone_meter.js#L34) | JS/TS 정규식 후보; AST 검증 아님 |
| `meNote` | [frontend/js/app.js:211](../../frontend/js/app.js#L211) | JS/TS 정규식 후보; AST 검증 아님 |
| `merge` | [frontend/js/chat.js:331](../../frontend/js/chat.js#L331) | JS/TS 정규식 후보; AST 검증 아님 |
| `metric` | [backend/transit.py:34](../../backend/transit.py#L34) | 응답의 초·m·원 값을 유한한 음수 아닌 수로 제한한다. 미확인은 0으로 대체하지 않는다. |
| `MicrophoneMeter` | [backend/microphone_meter.js:2](../../backend/microphone_meter.js#L2) | JS/TS 정규식 후보; AST 검증 아님 |
| `minutes` | [frontend/js/util.js:30](../../frontend/js/util.js#L30) | JS/TS 정규식 후보; AST 검증 아님 |
| `missing` | [frontend/js/chat.js:54](../../frontend/js/chat.js#L54) | JS/TS 정규식 후보; AST 검증 아님 |
| `mountConversation` | [backend/team_chat.js:176](../../backend/team_chat.js#L176) | JS/TS 정규식 후보; AST 검증 아님 |
| `mountInputMeter` | [backend/microphone_meter.js:81](../../backend/microphone_meter.js#L81) | JS/TS 정규식 후보; AST 검증 아님 |
| `NaitoChatTests` | [backend/test_naito_chat.py:12](../../backend/test_naito_chat.py#L12) | 서비스 키 없이 실행되는 공급자 어댑터 회귀다. |
| `NaitoChatTests.setUp` | [backend/test_naito_chat.py:15](../../backend/test_naito_chat.py#L15) | 최소 정상 대화 입력을 준비한다. |
| `NaitoChatTests.test_empty_interpretation_not_reported_as_applied` | [backend/test_naito_chat.py:80](../../backend/test_naito_chat.py#L80) | 지원하지 않는 발화를 반영 완료로 안내하지 않는다. |
| `NaitoChatTests.test_errors_do_not_disclose_or_replace` | [backend/test_naito_chat.py:59](../../backend/test_naito_chat.py#L59) | 공급자 오류/비JSON/사실 생성은 오류로 남기고 키·원문·가짜 초안을 노출하지 않는다. |
| `NaitoChatTests.test_missing_key` | [backend/test_naito_chat.py:19](../../backend/test_naito_chat.py#L19) | 미설정은 503이며 외부 호출을 하지 않는다. |
| `NaitoChatTests.test_provider_request_excludes_coordinates` | [backend/test_naito_chat.py:32](../../backend/test_naito_chat.py#L32) | 키는 헤더에만, 좌표는 제외하며 공식 고정 주소로 한 번 요청한다. |
| `NaitoChatTests.test_response_size_and_json_boundary` | [backend/test_naito_chat.py:74](../../backend/test_naito_chat.py#L74) | 과대 응답/일반 텍스트/잘못된 응답 구조를 파싱 성공으로 취급하지 않는다. |
| `NaitoChatTests.test_success_and_no_recommendation` | [backend/test_naito_chat.py:49](../../backend/test_naito_chat.py#L49) | 모의 국악 해석 뒤 출발지 질문으로 이어지며 추천은 실행하지 않는다. |
| `NaitoChatTests.test_validate_before_provider` | [backend/test_naito_chat.py:25](../../backend/test_naito_chat.py#L25) | 잘못된 요청은 공급자/키 조회 전에 거절한다. |
| `navigateVoice` | [backend/team_chat.js:210](../../backend/team_chat.js#L210) | JS/TS 정규식 후보; AST 검증 아님 |
| `next` | [frontend/js/chat.js:633](../../frontend/js/chat.js#L633) | JS/TS 정규식 후보; AST 검증 아님 |
| `normalize` | [backend/preferences.py:9](../../backend/preferences.py#L9) | 선호 부분 갱신을 검증한다. 빈 목록/false/any는 명시적 해제이며 null은 변경 없음이다. |
| `normalize_place` | [backend/tour_places.py:79](../../backend/tour_places.py#L79) | 목록/상세 사실만 통합한다. 결측 좌표·운영·요금은 null, 관람 가능 여부는 check다. |
| `normalize_places` | [backend/places.py:32](../../backend/places.py#L32) | 공급자 x/y를 숫자 lng/lat로 바꾸고 선택 가능한 최대5건만 반환한다. 손상과0건을 구분한다. |
| `normalize_proposal` | [backend/chat_conditions.py:24](../../backend/chat_conditions.py#L24) | 허용된 조건만 정규화한다. null은 변경 없음, 좌표·잘못된 값은 ValueError다. |
| `normalize_routes` | [backend/transit.py:91](../../backend/transit.py#L91) | 공식 응답의 경로 최대 세 개를 초·m 단위로 검증한다. 누락·공급자 오류는 실패로 구분한다. |
| `note` | [backend/team_chat.js:256](../../backend/team_chat.js#L256) | JS/TS 정규식 후보; AST 검증 아님 |
| `note` | [frontend/js/place.js:92](../../frontend/js/place.js#L92) | JS/TS 정규식 후보; AST 검증 아님 |
| `nothingUnderstood` | [frontend/js/chat.js:564](../../frontend/js/chat.js#L564) | JS/TS 정규식 후보; AST 검증 아님 |
| `num` | [frontend/js/chat.js:369](../../frontend/js/chat.js#L369) | JS/TS 정규식 후보; AST 검증 아님 |
| `official_image` | [backend/outing.py:117](../../backend/outing.py#L117) | 서울시 문화포털의 공식 대표 이미지 주소만 넘긴다. 다른 주소·형식이 이상하면 None (화면은 대체 그림 사용). |
| `official_link` | [backend/tour_places.py:54](../../backend/tour_places.py#L54) | 공식 응답이 제공한 홈페이지만 허용한다. ID로 확인하지 않은 상세 URL을 만들어 내지 않는다. |
| `OfficialImageTest` | [backend/test_culture_sources.py:130](../../backend/test_culture_sources.py#L130) | 개요 없음 |
| `OfficialImageTest.test_only_seoul_culture_portal_images` | [backend/test_culture_sources.py:131](../../backend/test_culture_sources.py#L131) | 공식 문화포털 이미지만 https 로 넘기고, 다른 주소·빈 값은 None. |
| `openingQuestion` | [backend/team_voice_actions.js:13](../../backend/team_voice_actions.js#L13) | JS/TS 정규식 후보; AST 검증 아님 |
| `openOriginalMenu` | [backend/team_chat.js:200](../../backend/team_chat.js#L200) | JS/TS 정규식 후보; AST 검증 아님 |
| `openSheet` | [frontend/js/place.js:120](../../frontend/js/place.js#L120) | JS/TS 정규식 후보; AST 검증 아님 |
| `other` | [frontend/js/chat.js:725](../../frontend/js/chat.js#L725) | JS/TS 정규식 후보; AST 검증 아님 |
| `OutingTests` | [backend/test_outing.py:9](../../backend/test_outing.py#L9) | 개인 추천의 의미가 바뀌는 경계 사례를 재현한다. |
| `OutingTests.setUp` | [backend/test_outing.py:12](../../backend/test_outing.py#L12) | 각 사례에 독립적인 청량리역 요청을 준비한다. |
| `OutingTests.test_actual_fields` | [backend/test_outing.py:16](../../backend/test_outing.py#L16) | 빈 요금, 무료 분류, 명시한 0원, 거리 오름차순을 보존한다. |
| `OutingTests.test_bad_input` | [backend/test_outing.py:77](../../backend/test_outing.py#L77) | 잘못된 출발 좌표나 종료 시각으로 외부 API를 호출하지 않는다. |
| `OutingTests.test_detail_fields_from_source` | [backend/test_outing.py:29](../../backend/test_outing.py#L29) | 행사 기간·지역은 공급자 원문을 쓰고 장소명을 주소로 바꾸지 않는다. |
| `OutingTests.test_empty_and_error` | [backend/test_outing.py:84](../../backend/test_outing.py#L84) | 실제 후보 0건을 공급자 장애와 구분한다. |
| `OutingTests.test_end_boundary` | [backend/test_outing.py:43](../../backend/test_outing.py#L43) | 전시 종료 시각에 도착하는 입력은 단순 운영구간에서 제외한다. |
| `OutingTests.test_genre_mismatch` | [backend/test_outing.py:91](../../backend/test_outing.py#L91) | 국악 조회에 전시가 섞이거나 전시만 반환돼도 국악 외 행사는 제외한다. |
| `OutingTests.test_input_error_fields` | [backend/test_outing.py:63](../../backend/test_outing.py#L63) | 시간 누락·형식·시간대·역전·다음날 및 잘못된 좌표의 필드를 특정한다. |
| `OutingTests.test_minimum_duration_before_source` | [backend/test_outing.py:50](../../backend/test_outing.py#L50) | 59분과 59분59초는 외부 조회 전에 거절하며 정확히 60분은 허용한다. |
| `OutingTests.test_recording_scope` | [backend/test_outing.py:102](../../backend/test_outing.py#L102) | 저장하지 않은 분류를 같은 날의 전체 기록으로 대체하지 않는다. |
| `p` | [frontend/js/util.js:60](../../frontend/js/util.js#L60) | JS/TS 정규식 후보; AST 검증 아님 |
| `p2` | [frontend/js/app.js:134](../../frontend/js/app.js#L134) | JS/TS 정규식 후보; AST 검증 아님 |
| `parseUtterance` | [frontend/js/parse.js:37](../../frontend/js/parse.js#L37) | JS/TS 정규식 후보; AST 검증 아님 |
| `patch` | [frontend/js/chat.js:73](../../frontend/js/chat.js#L73) | JS/TS 정규식 후보; AST 검증 아님 |
| `phase` | [backend/voice_session.js:151](../../backend/voice_session.js#L151) | JS/TS 정규식 후보; AST 검증 아님 |
| `photo` | [frontend/js/util.js:146](../../frontend/js/util.js#L146) | JS/TS 정규식 후보; AST 검증 아님 |
| `pickSeason` | [frontend/js/landing.js:21](../../frontend/js/landing.js#L21) | JS/TS 정규식 후보; AST 검증 아님 |
| `pin` | [frontend/js/place.js:178](../../frontend/js/place.js#L178) | JS/TS 정규식 후보; AST 검증 아님 |
| `placeById` | [frontend/js/place.js:16](../../frontend/js/place.js#L16) | JS/TS 정규식 후보; AST 검증 아님 |
| `placeName` | [frontend/js/chat.js:556](../../frontend/js/chat.js#L556) | JS/TS 정규식 후보; AST 검증 아님 |
| `PlaceSearchTests` | [backend/test_places.py:12](../../backend/test_places.py#L12) | 외부 조회를 대체한 경계 검사다. 실제 키 호출은 별도 브라우저 검사로 수행한다. |
| `PlaceSearchTests.fixture` | [backend/test_places.py:15](../../backend/test_places.py#L15) | 공개 장소를 뜻하지 않는 모의 공급자 문서를 만든다. |
| `PlaceSearchTests.test_address_id_and_coordinates` | [backend/test_places.py:38](../../backend/test_places.py#L38) | 주소 결과는 공급자 주소·좌표를 보존하고 재조회에도 같은 파생 식별자를 만든다. |
| `PlaceSearchTests.test_empty_vs_invalid_source` | [backend/test_places.py:47](../../backend/test_places.py#L47) | 정상0건과 좌표 손상·목록 누락을 구분하며 일부 손상 행은 별도 집계한다. |
| `PlaceSearchTests.test_failures` | [backend/test_places.py:76](../../backend/test_places.py#L76) | 권한·쿼터·시간초과·손상 응답의 공개 오류만 반환하며 공급자 상세는 숨긴다. |
| `PlaceSearchTests.test_inputs_before_network` | [backend/test_places.py:20](../../backend/test_places.py#L20) | 공백·길이초과·제어문자·잘못된 종류를 키 조회/외부 호출 전에 거절한다. |
| `PlaceSearchTests.test_keyword_coordinates_and_null` | [backend/test_places.py:28](../../backend/test_places.py#L28) | x/y를 올바른 축으로 변환하고 공란 주소·출처 URL을 임의 보완하지 않는다. |
| `PlaceSearchTests.test_missing_key` | [backend/test_places.py:69](../../backend/test_places.py#L69) | 키 미설정을 정상0건으로 반환하거나 외부 조회하지 않는다. |
| `PlaceSearchTests.test_provider_request` | [backend/test_places.py:58](../../backend/test_places.py#L58) | 키는 헤더에만 두고 검색어는 URL 인코딩하며 최대5건을 요청한다. |
| `plain` | [backend/tour_places.py:46](../../backend/tour_places.py#L46) | 공식 응답의 HTML 표기를 평문으로 바꾸고 빈 값은 null로 유지한다. |
| `post` | [frontend/js/api.js:45](../../frontend/js/api.js#L45) | JS/TS 정규식 후보; AST 검증 아님 |
| `post` | [utils/scripts/check_culture_sources.py:19](../../utils/scripts/check_culture_sources.py#L19) | 로컬 HTTP 상태/정규화 응답만 읽는다. 공급자 키가 있는 URL은 직접 출력하지 않는다. |
| `PreferenceTests` | [backend/test_preferences.py:12](../../backend/test_preferences.py#L12) | 실제 기록과 명시적 모의 공식 행사를 구분해 조건 반영을 확인한다. |
| `PreferenceTests.setUp` | [backend/test_preferences.py:15](../../backend/test_preferences.py#L15) | 기존 QA 입력과 독립된 공식 응답 모양의 행을 준비한다. |
| `PreferenceTests.test_budget_excludes_unknown_and_multiple_prices` | [backend/test_preferences.py:63](../../backend/test_preferences.py#L63) | 1인 관람료 한도는 미확인·할인·복수좌석을 충족으로 간주하지 않는다. |
| `PreferenceTests.test_confirmed_categories_atomic` | [backend/test_preferences.py:30](../../backend/test_preferences.py#L30) | 대표 분류 변경을 거절하면 연결된 복수 분류도 변경되지 않는다. |
| `PreferenceTests.test_exclusion_never_restored_when_zero` | [backend/test_preferences.py:73](../../backend/test_preferences.py#L73) | 모든 기록 후보를 제외해도 제한을 완화하거나 샘플로 대체하지 않는다. |
| `PreferenceTests.test_invalid_and_explicit_clear` | [backend/test_preferences.py:96](../../backend/test_preferences.py#L96) | 잘못된 형식을 거절하며 명시적 false/any/빈 목록은 보존한다. |
| `PreferenceTests.test_keyword_and_short_walk_order` | [backend/test_preferences.py:79](../../backend/test_preferences.py#L79) | 관심어 우선과 가까운 곳 우선은 순서를 실제로 바꾸며 도보 보장은 하지 않는다. |
| `PreferenceTests.test_multiple_categories_query_and_dedup` | [backend/test_preferences.py:39](../../backend/test_preferences.py#L39) | 분류별 조회 후 ID 중복을 제거하고 장르 밖 후보를 제외한다. |
| `PreferenceTests.test_multiple_categories_query_and_dedup.source` | [backend/test_preferences.py:41](../../backend/test_preferences.py#L41) | 두 음악 장르와 공통 행을 돌려주는 모의 공급자다. |
| `PreferenceTests.test_music_discovery_then_broad_accept` | [backend/test_preferences.py:21](../../backend/test_preferences.py#L21) | 음악→골고루는 분류를 강요하지 않고 같은 초안의 세 분류를 유지한다. |
| `PreferenceTests.test_no_partial_success_when_one_source_fails` | [backend/test_preferences.py:51](../../backend/test_preferences.py#L51) | 한 관심사 조회 실패를 0건/다른 분류 성공으로 숨기지 않는다. |
| `PreferenceTests.test_same_id_with_different_official_url_once` | [backend/test_preferences.py:56](../../backend/test_preferences.py#L56) | 메뉴 쿼리가 다른 동일 행사도 후보 ID 기준으로 한 번만 반환한다. |
| `PreferenceTests.test_unverified_hard_requirement_blocks_before_source` | [backend/test_preferences.py:89](../../backend/test_preferences.py#L89) | 계단 없음 등 필수 제약을 검증 못하면 외부 호출 전 명시적으로 차단한다. |
| `preferenceText` | [backend/team_preferences.js:16](../../backend/team_preferences.js#L16) | JS/TS 정규식 후보; AST 검증 아님 |
| `preflight` | [utils/scripts/commit_report.py:23](../../utils/scripts/commit_report.py#L23) | Validate branch, cutoff, report encoding, scoped paths and an empty index. |
| `prepare` | [utils/scripts/prepare_chat_handoff.py:53](../../utils/scripts/prepare_chat_handoff.py#L53) | 공개 Git 프론트 복사본에 패치를 실제 적용하고 결과 해시를 검증한 뒤 인계 ZIP을 만든다. |
| `Preview` | [backend/preview.py:43](../../backend/preview.py#L43) | 허용된 화면과 개인 검증용 JSON 요청만 제공한다. |
| `Preview.do_GET` | [backend/preview.py:83](../../backend/preview.py#L83) | 점검 폼과 저장소의 대표 요청만 제공한다. |
| `Preview.do_OPTIONS` | [backend/preview.py:54](../../backend/preview.py#L54) | 설정된 프론트의 JSON POST 사전 요청만 허용하고 그 외 origin/메서드/헤더는 거절한다. |
| `Preview.do_POST` | [backend/preview.py:127](../../backend/preview.py#L127) | 장소 요청을 처리하고 입력·외부 공급자 오류를 다른 상태로 전달한다. |
| `Preview.end_headers` | [backend/preview.py:46](../../backend/preview.py#L46) | 정상/오류 응답 모두 허용 origin에만 CORS 헤더를 적용하며 쿠키 인증은 허용하지 않는다. |
| `Preview.reply` | [backend/preview.py:72](../../backend/preview.py#L72) | UTF-8 본문을 길이와 함께 응답한다. |
| `PreviewContractTests` | [backend/test_preview.py:12](../../backend/test_preview.py#L12) | 실제 POST 처리기를 사용하되 응답 전송과 외부 공급자만 대체한다. |
| `PreviewContractTests.request` | [backend/test_preview.py:15](../../backend/test_preview.py#L15) | JSON 요청을 HTTP 처리기에 전달하고 상태 코드·응답을 반환한다. |
| `PreviewContractTests.setUp` | [backend/test_preview.py:30](../../backend/test_preview.py#L30) | 각 테스트가 사용할 독립적인 정상 요청을 읽는다. |
| `PreviewContractTests.test_chat_route_and_validation` | [backend/test_preview.py:35](../../backend/test_preview.py#L35) | 새 대화 경로는 어댑터 응답을 전달하고 잘못된 입력은 필드 오류를 반환한다. |
| `PreviewContractTests.test_culture_source_routes_and_errors` | [backend/test_preview.py:44](../../backend/test_preview.py#L44) | 문화시설 선택은 같은 추천 경로에서 전달하며 오류를 행사로 대체하지 않는다. |
| `PreviewContractTests.test_file_voice_disabled` | [backend/test_preview.py:141](../../backend/test_preview.py#L141) | 파일 음성이 꺼진 서버에서는 버튼을 숨기고 합성 요청도 실행하지 않는다. |
| `PreviewContractTests.test_home_uses_same_origin_app_when_prepared` | [backend/test_preview.py:154](../../backend/test_preview.py#L154) | 대화 복사본을 준비했으면 기본 주소는 단일 앱 홈으로 이동한다. |
| `PreviewContractTests.test_invalid_kind` | [backend/test_preview.py:85](../../backend/test_preview.py#L85) | 지원하지 않는 요청 종류를 place로 조용히 대체하지 않는다. |
| `PreviewContractTests.test_kind_compatibility` | [backend/test_preview.py:68](../../backend/test_preview.py#L68) | 정확히 60분인 route/course가 같은 코스 경로로, place는 후보만 반환한다. |
| `PreviewContractTests.test_origin_configuration` | [backend/test_preview.py:90](../../backend/test_preview.py#L90) | 허용 주소의 정확한 일치만 사용하고 와일드카드·자격정보·잘못된 설정을 제외한다. |
| `PreviewContractTests.test_place_search_contract` | [backend/test_preview.py:164](../../backend/test_preview.py#L164) | 새 검색 경로에도 입력400·허용origin·공급자 상태 전달을 동일 적용한다. |
| `PreviewContractTests.test_preflight` | [backend/test_preview.py:99](../../backend/test_preview.py#L99) | 설정된 origin·POST·Content-Type만 사전 요청에서 허용한다. |
| `PreviewContractTests.test_render_origin` | [backend/test_preview.py:121](../../backend/test_preview.py#L121) | 서버 설정의 공개 HTTPS 주소만 허용하고 비슷한 다른 주소는 거절한다. |
| `PreviewContractTests.test_server_options` | [backend/test_preview.py:130](../../backend/test_preview.py#L130) | 배포 포트·주소를 지원하되 명시 옵션이 우선하고 잘못된 포트는 시작 전에 거절한다. |
| `PreviewContractTests.test_short_duration_response` | [backend/test_preview.py:57](../../backend/test_preview.py#L57) | 60분 미만은 필드/코드가 있는 400이며 문화/코스 조회를 하지 않는다. |
| `PreviewContractTests.test_source_error_is_not_input_error` | [backend/test_preview.py:78](../../backend/test_preview.py#L78) | 공급자 장애는 필드 오류 대신 502이며 공급자 예외 내용은 숨긴다. |
| `provider` | [backend/naito_chat.py:20](../../backend/naito_chat.py#L20) | LAB678_NAITO_PROVIDER: codyssey(기본) / anthropic / openai. 키 모양으로 추측하지 않는다(해커톤 키도 sk- 로 시작). |
| `provider_response` | [backend/test_transit.py:11](../../backend/test_transit.py#L11) | 공식 스키마를 따르는 가상 도보·지하철·도보 3구간을 만든다. 시연 데이터가 아니다. |
| `put_value` | [backend/chat_conditions.py:97](../../backend/chat_conditions.py#L97) | 출발지 검색어가 바뀌면 이전 좌표를 제거한다. 다른 조건은 초안에만 반영한다. |
| `query_walking` | [backend/walking.py:16](../../backend/walking.py#L16) | 개인 화면의 도보 조회 간격을 제한하고 공급자의 JSON 또는 실패 상태를 반환한다. |
| `readStore` | [frontend/js/util.js:65](../../frontend/js/util.js#L65) | JS/TS 정규식 후보; AST 검증 아님 |
| `readVoiceReply` | [backend/voice_session.js:93](../../backend/voice_session.js#L93) | JS/TS 정규식 후보; AST 검증 아님 |
| `recommend` | [backend/outing.py:150](../../backend/outing.py#L150) | 검증된 요청의 후보를 계산한다. 입력 오류와 공급자 오류를 별도로 전달한다. |
| `record` | [utils/scripts/loop.py:21](../../utils/scripts/loop.py#L21) | Append one evidenced attempt, rejecting terminal states and blind repeats. |
| `refit` | [frontend/js/place.js:198](../../frontend/js/place.js#L198) | JS/TS 정규식 후보; AST 검증 아님 |
| `refresh` | [backend/location_view.js:36](../../backend/location_view.js#L36) | JS/TS 정규식 후보; AST 검증 아님 |
| `refresh` | [backend/team_culture.js:24](../../backend/team_culture.js#L24) | JS/TS 정규식 후보; AST 검증 아님 |
| `refresh` | [utils/scripts/watch.py:30](../../utils/scripts/watch.py#L30) | Render state before indexing it; leave source and decisions untouched. |
| `remember` | [backend/team_chat.js:266](../../backend/team_chat.js#L266) | JS/TS 정규식 후보; AST 검증 아님 |
| `render` | [frontend/js/chat.js:205](../../frontend/js/chat.js#L205) | JS/TS 정규식 후보; AST 검증 아님 |
| `render` | [utils/scripts/catalog.py:204](../../utils/scripts/catalog.py#L204) | Produce all utility and repository indexes without volatile timestamps. |
| `render` | [utils/scripts/context.py:22](../../utils/scripts/context.py#L22) | Render bounded, human-curated lists while preserving their decision status. |
| `render_repo` | [utils/scripts/catalog.py:156](../../utils/scripts/catalog.py#L156) | Index every eligible file plus code symbols, features and directory layout. |
| `render_utils` | [utils/scripts/catalog.py:118](../../utils/scripts/catalog.py#L118) | Render stable forward and reverse indexes with repository-relative links. |
| `render_wave` | [backend/local_voice.py:30](../../backend/local_voice.py#L30) | 문자열을 표준 입력으로 전달해 메모리에서 합성하고, 실패·과부하 때 예외를 반환한다. |
| `renderChat` | [frontend/js/chat.js:766](../../frontend/js/chat.js#L766) | JS/TS 정규식 후보; AST 검증 아님 |
| `renderHome` | [frontend/js/app.js:170](../../frontend/js/app.js#L170) | JS/TS 정규식 후보; AST 검증 아님 |
| `renderMap` | [frontend/js/place.js:230](../../frontend/js/place.js#L230) | JS/TS 정규식 후보; AST 검증 아님 |
| `renderMe` | [frontend/js/app.js:183](../../frontend/js/app.js#L183) | JS/TS 정규식 후보; AST 검증 아님 |
| `renderNotify` | [frontend/js/app.js:132](../../frontend/js/app.js#L132) | JS/TS 정규식 후보; AST 검증 아님 |
| `renderPlace` | [frontend/js/place.js:30](../../frontend/js/place.js#L30) | JS/TS 정규식 후보; AST 검증 아님 |
| `renderPreferenceSummary` | [backend/team_preferences.js:30](../../backend/team_preferences.js#L30) | JS/TS 정규식 후보; AST 검증 아님 |
| `renderResultPreferences` | [backend/team_preferences.js:40](../../backend/team_preferences.js#L40) | JS/TS 정규식 후보; AST 검증 아님 |
| `renderVoiceState` | [backend/team_chat.js:474](../../backend/team_chat.js#L474) | JS/TS 정규식 후보; AST 검증 아님 |
| `repo_files` | [utils/scripts/catalog.py:46](../../utils/scripts/catalog.py#L46) | Inventory repository files, including untracked work, without reading secrets. |
| `request` | [utils/scripts/check_chat_api.py:19](../../utils/scripts/check_chat_api.py#L19) | 임시 서버로 JSON POST 또는 CORS OPTIONS를 보내 상태/본문/허용 origin을 반환한다. |
| `requestBody` | [frontend/js/chat.js:655](../../frontend/js/chat.js#L655) | JS/TS 정규식 후보; AST 검증 아님 |
| `requestChat` | [frontend/js/api.js:102](../../frontend/js/api.js#L102) | JS/TS 정규식 후보; AST 검증 아님 |
| `requestRecommend` | [frontend/js/api.js:69](../../frontend/js/api.js#L69) | JS/TS 정규식 후보; AST 검증 아님 |
| `resetChat` | [frontend/js/state.js:44](../../frontend/js/state.js#L44) | JS/TS 정규식 후보; AST 검증 아님 |
| `resolve_changes` | [backend/chat_conditions.py:153](../../backend/chat_conditions.py#L153) | 동일 초안/revision에서 명시적 bool 동의만 반영한다. 미응답 충돌은 유지한다. |
| `resolvePending` | [frontend/js/chat.js:622](../../frontend/js/chat.js#L622) | JS/TS 정규식 후보; AST 검증 아님 |
| `review_text` | [utils/scripts/read_pdf.py:18](../../utils/scripts/read_pdf.py#L18) | Mask credential-related lines and two following lines before console output. |
| `route` | [frontend/js/app.js:15](../../frontend/js/app.js#L15) | JS/TS 정규식 후보; AST 검증 아님 |
| `route_path` | [backend/transit.py:48](../../backend/transit.py#L48) | 선택적 WGS84 [경도,위도] 경로를 Leaflet [위도,경도]로 변환한다. 손상 시 선만 생략한다. |
| `routeCard` | [frontend/js/place.js:282](../../frontend/js/place.js#L282) | JS/TS 정규식 후보; AST 검증 아님 |
| `row` | [frontend/js/place.js:47](../../frontend/js/place.js#L47) | JS/TS 정규식 후보; AST 검증 아님 |
| `run` | [utils/scripts/harness.py:63](../../utils/scripts/harness.py#L63) | Execute finite static checks and optional isolated utility tests. |
| `safe_target` | [utils/scripts/reuse.py:18](../../utils/scripts/reuse.py#L18) | Resolve a relative destination without traversal, links or Git internals. |
| `save` | [frontend/js/state.js:39](../../frontend/js/state.js#L39) | JS/TS 정규식 후보; AST 검증 아님 |
| `savedCard` | [frontend/js/app.js:156](../../frontend/js/app.js#L156) | JS/TS 정규식 후보; AST 검증 아님 |
| `savedPlaces` | [frontend/js/saved.js:12](../../frontend/js/saved.js#L12) | JS/TS 정규식 후보; AST 검증 아님 |
| `savePlace` | [frontend/js/saved.js:27](../../frontend/js/saved.js#L27) | JS/TS 정규식 후보; AST 검증 아님 |
| `saveVoiceLog` | [backend/team_chat.js:124](../../backend/team_chat.js#L124) | JS/TS 정규식 후보; AST 검증 아님 |
| `say` | [frontend/js/chat.js:100](../../frontend/js/chat.js#L100) | JS/TS 정규식 후보; AST 검증 아님 |
| `sayBye` | [frontend/js/place.js:112](../../frontend/js/place.js#L112) | JS/TS 정규식 후보; AST 검증 아님 |
| `schedule_pair` | [backend/course.py:35](../../backend/course.py#L35) | 두 구간과 당일 시간표를 합산해 가능·미확인·충돌 및 방문별 예상시각을 반환한다. |
| `screenContext` | [backend/team_voice_actions.js:5](../../backend/team_voice_actions.js#L5) | JS/TS 정규식 후보; AST 검증 아님 |
| `script` | [backend/map_view.js:9](../../backend/map_view.js#L9) | JS/TS 정규식 후보; AST 검증 아님 |
| `scrollEnd` | [frontend/js/chat.js:218](../../frontend/js/chat.js#L218) | JS/TS 정규식 후보; AST 검증 아님 |
| `search` | [frontend/js/chat.js:667](../../frontend/js/chat.js#L667) | JS/TS 정규식 후보; AST 검증 아님 |
| `search_input` | [backend/places.py:16](../../backend/places.py#L16) | 검색어 1~80자와 keyword/address를 검증한다. 요청값을 오류에 되돌려 쓰지 않는다. |
| `search_places` | [backend/places.py:73](../../backend/places.py#L73) | 카카오에 검색어를 보내 후보를 반환한다. HTTP 상태·권한/쿼터/시간초과를 구분하고 비밀값은 숨긴다. |
| `searchOrigin` | [backend/team_chat.js:367](../../backend/team_chat.js#L367) | JS/TS 정규식 후보; AST 검증 아님 |
| `searchPlaces` | [frontend/js/api.js:85](../../frontend/js/api.js#L85) | JS/TS 정규식 후보; AST 검증 아님 |
| `send` | [backend/team_chat.js:387](../../backend/team_chat.js#L387) | JS/TS 정규식 후보; AST 검증 아님 |
| `seoul_page` | [backend/outing.py:81](../../backend/outing.py#L81) | 지정일 키 없으면5건, 정식 키면 최대 1000건(SEOUL_FETCH_LIMIT)을 조회한다. 인증 실패를 sample로 대체하지 않는다. |
| `seoulWeather` | [frontend/js/weather.js:45](../../frontend/js/weather.js#L45) | JS/TS 정규식 후보; AST 검증 아님 |
| `server_options` | [backend/preview.py:205](../../backend/preview.py#L205) | 로컬 기본값을 유지하고 명시한 접속 주소·배포 환경의 PORT 범위를 검증한다. |
| `serverCategory` | [frontend/js/chat.js:28](../../frontend/js/chat.js#L28) | JS/TS 정규식 후보; AST 검증 아님 |
| `setBig` | [frontend/js/place.js:213](../../frontend/js/place.js#L213) | JS/TS 정규식 후보; AST 검증 아님 |
| `setMode` | [frontend/js/chat.js:301](../../frontend/js/chat.js#L301) | JS/TS 정규식 후보; AST 검증 아님 |
| `setMode` | [frontend/js/place.js:336](../../frontend/js/place.js#L336) | JS/TS 정규식 후보; AST 검증 아님 |
| `setSeasonArt` | [frontend/js/landing.js:36](../../frontend/js/landing.js#L36) | JS/TS 정규식 후보; AST 검증 아님 |
| `setSound` | [frontend/js/chat.js:284](../../frontend/js/chat.js#L284) | JS/TS 정규식 후보; AST 검증 아님 |
| `settings` | [backend/naito_chat.py:59](../../backend/naito_chat.py#L59) | 앱 전용 환경변수/무시된 로컬 파일에서 키와 모델을 읽는다. 실제 값은 출력하지 않는다. |
| `short_text` | [backend/transit.py:41](../../backend/transit.py#L41) | 이동 안내 원문을 길이 제한된 텍스트로 받아 HTML 실행 없이 표시하도록 반환한다. |
| `show` | [frontend/js/app.js:59](../../frontend/js/app.js#L59) | JS/TS 정규식 후보; AST 검증 아님 |
| `show` | [frontend/js/chat.js:397](../../frontend/js/chat.js#L397) | JS/TS 정규식 후보; AST 검증 아님 |
| `show` | [frontend/js/chat.js:87](../../frontend/js/chat.js#L87) | JS/TS 정규식 후보; AST 검증 아님 |
| `showCards` | [frontend/js/chat.js:715](../../frontend/js/chat.js#L715) | JS/TS 정규식 후보; AST 검증 아님 |
| `showConflicts` | [backend/team_chat.js:318](../../backend/team_chat.js#L318) | JS/TS 정규식 후보; AST 검증 아님 |
| `showHistory` | [backend/team_chat.js:274](../../backend/team_chat.js#L274) | JS/TS 정규식 후보; AST 검증 아님 |
| `showLiveTranscript` | [backend/team_chat.js:82](../../backend/team_chat.js#L82) | JS/TS 정규식 후보; AST 검증 아님 |
| `showTransit` | [frontend/js/place.js:313](../../frontend/js/place.js#L313) | JS/TS 정규식 후보; AST 검증 아님 |
| `showWalk` | [frontend/js/place.js:271](../../frontend/js/place.js#L271) | JS/TS 정규식 후보; AST 검증 아님 |
| `signature` | [utils/scripts/watch.py:18](../../utils/scripts/watch.py#L18) | Track eligible file names and metadata, excluding outputs and temp files. |
| `singleInput` | [backend/team_chat.js:509](../../backend/team_chat.js#L509) | JS/TS 정규식 후보; AST 검증 아님 |
| `sky` | [frontend/js/weather.js:12](../../frontend/js/weather.js#L12) | JS/TS 정규식 후보; AST 검증 아님 |
| `snapshot` | [utils/scripts/reuse.py:42](../../utils/scripts/reuse.py#L42) | Preflight all selected blobs, then copy exactly without replacing files. |
| `snapshot` | [utils/scripts/team_chat_preview.py:20](../../utils/scripts/team_chat_preview.py#L20) | 명시한 Git ref의 프론트만 해시별 경로에 복사한다. 기존 복사본은 덮어쓰지 않는다. |
| `source_files` | [utils/scripts/catalog.py:26](../../utils/scripts/catalog.py#L26) | List supported source files in configured roots, excluding symlinks. |
| `speak` | [backend/team_chat.js:283](../../backend/team_chat.js#L283) | JS/TS 정규식 후보; AST 검증 아님 |
| `speak` | [frontend/js/chat.js:251](../../frontend/js/chat.js#L251) | JS/TS 정규식 후보; AST 검증 아님 |
| `speakKo` | [frontend/js/util.js:117](../../frontend/js/util.js#L117) | JS/TS 정규식 후보; AST 검증 아님 |
| `start` | [backend/location_view.js:46](../../backend/location_view.js#L46) | JS/TS 정규식 후보; AST 검증 아님 |
| `start` | [frontend/js/chat.js:759](../../frontend/js/chat.js#L759) | JS/TS 정규식 후보; AST 검증 아님 |
| `start` | [utils/scripts/loop.py:14](../../utils/scripts/loop.py#L14) | Create an explicit task state with at most ten verification attempts. |
| `startDemo` | [frontend/js/saved.js:20](../../frontend/js/saved.js#L20) | JS/TS 정규식 후보; AST 검증 아님 |
| `startLeaves` | [frontend/js/landing.js:46](../../frontend/js/landing.js#L46) | JS/TS 정규식 후보; AST 검증 아님 |
| `status` | [backend/location_view.js:15](../../backend/location_view.js#L15) | JS/TS 정규식 후보; AST 검증 아님 |
| `step_transport` | [backend/transit.py:66](../../backend/transit.py#L66) | 공급자의 차량 이름·정류장 순서를 보존한다. 선택 필드 손상/누락은 미확인으로 남긴다. |
| `step_transport.label` | [backend/transit.py:68](../../backend/transit.py#L68) | 선택적 공개 노선/역 이름만 길이를 제한해 받는다. 없으면 사실을 추정하지 않는다. |
| `stop` | [backend/location_view.js:25](../../backend/location_view.js#L25) | JS/TS 정규식 후보; AST 검증 아님 |
| `stopListening` | [frontend/js/chat.js:457](../../frontend/js/chat.js#L457) | JS/TS 정규식 후보; AST 검증 아님 |
| `stopSingleRecognition` | [backend/team_chat.js:502](../../backend/team_chat.js#L502) | JS/TS 정규식 후보; AST 검증 아님 |
| `summarize` | [backend/chat_conditions.py:63](../../backend/chat_conditions.py#L63) | 코드로 누락·추천 입력·60분을 검사한다. ready는 S02a 진입 가능이며 추천 승인이 아니다. |
| `summary` | [frontend/js/chat.js:63](../../frontend/js/chat.js#L63) | JS/TS 정규식 후보; AST 검증 아님 |
| `talkFor` | [frontend/js/util.js:93](../../frontend/js/util.js#L93) | JS/TS 정규식 후보; AST 검증 아님 |
| `TeamAppTests` | [backend/test_team_app.py:11](../../backend/test_team_app.py#L11) | 선택한 검증 복사본 외 파일을 요청할 수 없도록 경계를 검사한다. |
| `TeamAppTests.setUp` | [backend/test_team_app.py:14](../../backend/test_team_app.py#L14) | 별도 임시 저장소에 공개 자산과 비밀 파일을 분리해 만든다. |
| `TeamAppTests.test_bad_selection` | [backend/test_team_app.py:42](../../backend/test_team_app.py#L42) | 미설정/손상/외부 폴더 설정은 모두 미연결이다. |
| `TeamAppTests.test_traversal_and_private_files` | [backend/test_team_app.py:36](../../backend/test_team_app.py#L36) | 퍼센트 인코딩·절대/역슬래시 경로와 비밀 확장자 요청은 거절한다. |
| `TeamAppTests.test_valid_assets` | [backend/test_team_app.py:30](../../backend/test_team_app.py#L30) | 아래 경로의 index/JS와 query만 허용한다. |
| `testMode` | [frontend/js/api.js:37](../../frontend/js/api.js#L37) | JS/TS 정규식 후보; AST 검증 아님 |
| `text` | [frontend/js/chat.js:395](../../frontend/js/chat.js#L395) | JS/TS 정규식 후보; AST 검증 아님 |
| `text_or_none` | [backend/places.py:27](../../backend/places.py#L27) | 공급자 텍스트를 제한된 길이로 읽고 공백·누락은 null로 유지한다. |
| `time_match` | [backend/outing.py:134](../../backend/outing.py#L134) | 단순 전시 개방구간/공연 시작을 검사한다. 복합 운영규칙은 미확인(None)이다. |
| `to24` | [frontend/js/parse.js:23](../../frontend/js/parse.js#L23) | JS/TS 정규식 후보; AST 검증 아님 |
| `todayIso` | [frontend/js/util.js:36](../../frontend/js/util.js#L36) | JS/TS 정규식 후보; AST 검증 아님 |
| `ToolsTest` | [utils/tests/test_tools.py:25](../../utils/tests/test_tools.py#L25) | Check behavior with independent fixtures rather than mirrored implementation. |
| `ToolsTest.git_repo` | [utils/tests/test_tools.py:46](../../utils/tests/test_tools.py#L46) | Initialize only the disposable Git fixture; set fixture-local identity. |
| `ToolsTest.setUp` | [utils/tests/test_tools.py:28](../../utils/tests/test_tools.py#L28) | Create a minimal isolated repository fixture and public harness config. |
| `ToolsTest.state` | [utils/tests/test_tools.py:52](../../utils/tests/test_tools.py#L52) | Return a complete minimal context payload with no inferred policy. |
| `ToolsTest.test_commit_branch_and_report_guards` | [utils/tests/test_tools.py:180](../../utils/tests/test_tools.py#L180) | Wrong branch and CRLF reports cannot pass commit preflight. |
| `ToolsTest.test_commit_deadline` | [utils/tests/test_tools.py:175](../../utils/tests/test_tools.py#L175) | The exact Korean submission cutoff rejects a commit before touching Git. |
| `ToolsTest.test_complete_report_message_bytes` | [utils/tests/test_tools.py:235](../../utils/tests/test_tools.py#L235) | Git stores the full Markdown report, not just a shortened subject. |
| `ToolsTest.test_conditional_python_function` | [utils/tests/test_tools.py:100](../../utils/tests/test_tools.py#L100) | Functions declared under control flow remain discoverable. |
| `ToolsTest.test_context_preserves_next_actions` | [utils/tests/test_tools.py:122](../../utils/tests/test_tools.py#L122) | A restart brief includes actionable next steps with their literal status. |
| `ToolsTest.test_context_rejects_unbounded_or_missing_data` | [utils/tests/test_tools.py:128](../../utils/tests/test_tools.py#L128) | Oversized lists and absent sections fail instead of silently truncating. |
| `ToolsTest.test_copy_rejects_unsafe_targets` | [utils/tests/test_tools.py:138](../../utils/tests/test_tools.py#L138) | Traversal, Windows drive paths, Git internals and backslashes are refused. |
| `ToolsTest.test_docstring_and_syntax_failures` | [utils/tests/test_tools.py:109](../../utils/tests/test_tools.py#L109) | Missing documentation and syntax errors produce actionable diagnostics. |
| `ToolsTest.test_empty_overview` | [utils/tests/test_tools.py:105](../../utils/tests/test_tools.py#L105) | Whitespace-only overviews yield an explicit missing-summary label. |
| `ToolsTest.test_hash_compares_bytes` | [utils/tests/test_tools.py:144](../../utils/tests/test_tools.py#L144) | Different line endings are different original file bytes. |
| `ToolsTest.test_index_detects_body_change` | [utils/tests/test_tools.py:62](../../utils/tests/test_tools.py#L62) | Changing only a function body invalidates the fingerprint index. |
| `ToolsTest.test_indexes_converge_without_recursive_hashes` | [utils/tests/test_tools.py:94](../../utils/tests/test_tools.py#L94) | Generating indexes twice is a no-op even though outputs index themselves. |
| `ToolsTest.test_js_overview_and_exports` | [utils/tests/test_tools.py:77](../../utils/tests/test_tools.py#L77) | Documented JS exports are discoverable without executing JavaScript. |
| `ToolsTest.test_link_checks_ignore_code_examples` | [utils/tests/test_tools.py:117](../../utils/tests/test_tools.py#L117) | Relative missing links fail, while fenced placeholders and HTTPS do not. |
| `ToolsTest.test_loop_blocked_and_pass` | [utils/tests/test_tools.py:169](../../utils/tests/test_tools.py#L169) | Blocked and successful tasks cannot silently restart themselves. |
| `ToolsTest.test_loop_duplicate_and_evidence` | [utils/tests/test_tools.py:159](../../utils/tests/test_tools.py#L159) | Blind retries and empty evidence are rejected without mutating the original. |
| `ToolsTest.test_loop_limit_and_terminal_state` | [utils/tests/test_tools.py:151](../../utils/tests/test_tools.py#L151) | A failed final attempt ends the loop and prevents further records. |
| `ToolsTest.test_pdf_review_masks_credential_context` | [utils/tests/test_tools.py:245](../../utils/tests/test_tools.py#L245) | Credential lines and their immediate context stay out of review output. |
| `ToolsTest.test_pdf_review_preserves_korean_guidance` | [utils/tests/test_tools.py:252](../../utils/tests/test_tools.py#L252) | Normal Korean workload and schedule notes remain available for review. |
| `ToolsTest.test_python_qualified_symbols` | [utils/tests/test_tools.py:56](../../utils/tests/test_tools.py#L56) | Classes and async methods retain qualified names and source locations. |
| `ToolsTest.test_repository_inventory_and_secret_exclusion` | [utils/tests/test_tools.py:82](../../utils/tests/test_tools.py#L82) | New arbitrary files enter repo indexes while secret file contents stay out. |
| `ToolsTest.test_snapshot_conflict_preflight` | [utils/tests/test_tools.py:195](../../utils/tests/test_tools.py#L195) | A conflicting destination prevents all writes, including earlier files. |
| `ToolsTest.test_source_exclusions` | [utils/tests/test_tools.py:71](../../utils/tests/test_tools.py#L71) | Excluded directories and reference snapshots never enter the code catalog. |
| `ToolsTest.test_staged_changes_rejected` | [utils/tests/test_tools.py:226](../../utils/tests/test_tools.py#L226) | Existing staged work is not silently combined into a task commit. |
| `ToolsTest.test_watcher_detects_add_modify_delete` | [utils/tests/test_tools.py:215](../../utils/tests/test_tools.py#L215) | Source additions, content changes and deletion alter the watcher signature. |
| `ToolsTest.test_watcher_excludes_its_outputs` | [utils/tests/test_tools.py:207](../../utils/tests/test_tools.py#L207) | Generated outputs do not trigger another watcher cycle even without config hints. |
| `ToolsTest.write` | [utils/tests/test_tools.py:39](../../utils/tests/test_tools.py#L39) | Write a temporary UTF-8 test file and return its location. |
| `toServerDraft` | [frontend/js/chat.js:477](../../frontend/js/chat.js#L477) | JS/TS 정규식 후보; AST 검증 아님 |
| `toText` | [frontend/js/chat.js:465](../../frontend/js/chat.js#L465) | JS/TS 정규식 후보; AST 검증 아님 |
| `track` | [backend/map_view.js:62](../../backend/map_view.js#L62) | JS/TS 정규식 후보; AST 검증 아님 |
| `transit_between` | [backend/transit.py:139](../../backend/transit.py#L139) | 좌표 두 개로 사용자 요청당 1회 조회한다. 미설정/인증/한도/빈 결과/실패를 구별한다. |
| `transitRoute` | [frontend/js/api.js:140](../../frontend/js/api.js#L140) | JS/TS 정규식 후보; AST 검증 아님 |
| `TransitTests` | [backend/test_transit.py:19](../../backend/test_transit.py#L19) | 비밀값 비노출·단위·미연결·잘못된 좌표·HTTP200 오류·한도를 독립적으로 검사한다. |
| `TransitTests.setUp` | [backend/test_transit.py:22](../../backend/test_transit.py#L22) | 실제 사용자 위치와 무관한 공개 장소 좌표를 준비한다. |
| `TransitTests.test_bad_payloads` | [backend/test_transit.py:93](../../backend/test_transit.py#L93) | 음수·누락·잘못된 이동수단·손상된 성공 응답을 정상이 아닌 것으로 처리한다. |
| `TransitTests.test_missing_access_walk` | [backend/test_transit.py:38](../../backend/test_transit.py#L38) | 실응답처럼 지하철만 표시되어도 생략된 접근/마지막 도보를 0으로 확정하지 않는다. |
| `TransitTests.test_normalization` | [backend/test_transit.py:26](../../backend/test_transit.py#L26) | 초/m/환승/요금 및 미확인 요금을 보존한다. |
| `TransitTests.test_optional_vehicle_metadata_is_not_guessed` | [backend/test_transit.py:62](../../backend/test_transit.py#L62) | 누락/손상된 노선·역 이름을 안내문에서 추측하지 않고 HTML 문자도 평문으로 전달한다. |
| `TransitTests.test_request_and_provider_errors` | [backend/test_transit.py:112](../../backend/test_transit.py#L112) | 헤더만 키를 담고 날짜는 보내지 않으며 인증·한도·통신·본문 오류를 구분한다. |
| `TransitTests.test_route_geometry` | [backend/test_transit.py:73](../../backend/test_transit.py#L73) | 경위도 순서를 검증하고 손상/누락 경로선 때문에 텍스트 안내까지 잃지 않는다. |
| `TransitTests.test_unconfigured_and_coordinates` | [backend/test_transit.py:104](../../backend/test_transit.py#L104) | 미설정 시 외부 호출을 하지 않고 입력 누락·중복 좌표는 거절한다. |
| `TransitTests.test_vehicle_and_stops` | [backend/test_transit.py:49](../../backend/test_transit.py#L49) | 호선/버스 이름과 승하차를 실제 응답 필드에서만 보존하며 대체 노선도 유지한다. |
| `typeIcon` | [frontend/js/util.js:131](../../frontend/js/util.js#L131) | JS/TS 정규식 후보; AST 검증 아님 |
| `unlockSpeech` | [frontend/js/util.js:104](../../frontend/js/util.js#L104) | JS/TS 정규식 후보; AST 검증 아님 |
| `updateVoiceUi` | [frontend/js/chat.js:312](../../frontend/js/chat.js#L312) | JS/TS 정규식 후보; AST 검증 아님 |
| `useHere` | [frontend/js/chat.js:606](../../frontend/js/chat.js#L606) | JS/TS 정규식 후보; AST 검증 아님 |
| `userSays` | [frontend/js/chat.js:107](../../frontend/js/chat.js#L107) | JS/TS 정규식 후보; AST 검증 아님 |
| `validate` | [backend/outing.py:40](../../backend/outing.py#L40) | 개인 장소 요청을 검증하고 한국 시각의 당일 구간과 출발점을 반환한다. |
| `validate_request` | [backend/naito_chat.py:72](../../backend/naito_chat.py#L72) | 짧은 발화/대화와 초안 revision을 검증한다. 오류에 사용자 원문을 포함하지 않는다. |
| `verify_message` | [utils/scripts/commit_report.py:17](../../utils/scripts/commit_report.py#L17) | Compare raw latest-commit message bytes to the complete report file. |
| `visit_window` | [backend/course.py:11](../../backend/course.py#L11) | 행사 시간 원문에서 검증 가능한 당일 시작·종료와 고정 공연 여부를 얻는다. |
| `visitLine` | [frontend/js/place.js:21](../../frontend/js/place.js#L21) | JS/TS 정규식 후보; AST 검증 아님 |
| `voiceAction` | [backend/team_voice_actions.js:26](../../backend/team_voice_actions.js#L26) | JS/TS 정규식 후보; AST 검증 아님 |
| `VoiceSession` | [backend/voice_session.js:127](../../backend/voice_session.js#L127) | JS/TS 정규식 후보; AST 검증 아님 |
| `voiceSettings` | [backend/team_chat.js:463](../../backend/team_chat.js#L463) | JS/TS 정규식 후보; AST 검증 아님 |
| `wait` | [frontend/js/chat.js:272](../../frontend/js/chat.js#L272) | JS/TS 정규식 후보; AST 검증 아님 |
| `wait_for` | [utils/scripts/verify_watch.py:14](../../utils/scripts/verify_watch.py#L14) | Wait a bounded period for generated evidence or report the failed phase. |
| `waitForSpeech` | [backend/voice_session.js:28](../../backend/voice_session.js#L28) | JS/TS 정규식 후보; AST 검증 아님 |
| `wake` | [frontend/js/app.js:100](../../frontend/js/app.js#L100) | JS/TS 정규식 후보; AST 검증 아님 |
| `wakeServer` | [frontend/js/api.js:19](../../frontend/js/api.js#L19) | JS/TS 정규식 후보; AST 검증 아님 |
| `walk_between` | [backend/walking.py:98](../../backend/walking.py#L98) | 두 행사 좌표로 도보 예상 초·m를 얻는다. 잘못된 입력과 조회 실패를 구분한다. |
| `walking_details` | [backend/walking.py:76](../../backend/walking.py#L76) | 같은 공급자 응답에서 한국어 단계·m·경로 인덱스·좌표를 검증해 반환한다. |
| `WalkingTests` | [backend/test_walking.py:9](../../backend/test_walking.py#L9) | 경로선 정밀도와 손상된 단계 응답을 검증한다. |
| `WalkingTests.setUp` | [backend/test_walking.py:12](../../backend/test_walking.py#L12) | 두 지점과 짧은 공급자 응답을 독립적으로 준비한다. |
| `WalkingTests.test_bad_steps` | [backend/test_walking.py:38](../../backend/test_walking.py#L38) | 지도 밖 단계나 영어 대체 응답을 한국어 안내 성공으로 표시하지 않는다. |
| `WalkingTests.test_detail_and_summary` | [backend/test_walking.py:28](../../backend/test_walking.py#L28) | 기존 요약 응답을 유지하고 상세 요청에만 단계와 경로선을 추가한다. |
| `WalkingTests.test_polyline_precision` | [backend/test_walking.py:20](../../backend/test_walking.py#L20) | 공개 polyline 예제의 정수 값을 백만분의 일 도 단위로 해독한다. |
| `walkRoute` | [frontend/js/api.js:117](../../frontend/js/api.js#L117) | JS/TS 정규식 후보; AST 검증 아님 |
| `watchBottom` | [frontend/js/chat.js:225](../../frontend/js/chat.js#L225) | JS/TS 정규식 후보; AST 검증 아님 |
| `withPreferences` | [backend/team_preferences.js:9](../../backend/team_preferences.js#L9) | JS/TS 정규식 후보; AST 검증 아님 |
| `write_indexes` | [utils/scripts/catalog.py:211](../../utils/scripts/catalog.py#L211) | Write changed outputs only, allowing repeated watcher runs to be quiet. |
| `writeStore` | [frontend/js/util.js:75](../../frontend/js/util.js#L75) | JS/TS 정규식 후보; AST 검증 아님 |
