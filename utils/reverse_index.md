# 함수·클래스 역색인

자동 생성. Python은 AST, JS/TS는 export 정규식 요약이며 호출 그래프가 아니다.

작업 키워드 검색: `python utils/scripts/catalog.py --find 검색어`.

| 심볼 | 정의 위치 | 개요 |
|---|---|---|
| `$` | [backend/team_chat.js:69](../backend/team_chat.js#L69) | JS/TS 정규식 후보; AST 검증 아님 |
| `$` | [frontend/js/util.js:4](../frontend/js/util.js#L4) | JS/TS 정규식 후보; AST 검증 아님 |
| `$$` | [frontend/js/util.js:6](../frontend/js/util.js#L6) | JS/TS 정규식 후보; AST 검증 아님 |
| `_apply_update` | [backend/dialogue_memory.py:249](../backend/dialogue_memory.py#L249) | 단일 의미 후보를 원자적으로 적용한다. 모르는 필드는 예외로 해당 후보만 격리한다. |
| `_budget_matches` | [backend/chat_grounding.py:313](../backend/chat_grounding.py#L313) | 관람료 금액·제한 해제를 확인할 수 있을 때만 예산을 적용한다. |
| `_category_matches` | [backend/chat_grounding.py:219](../backend/chat_grounding.py#L219) | 명시된 분류의 부정·다른 분류로의 임의 변경만 보수적으로 차단한다. |
| `_clock_values` | [backend/chat_grounding.py:117](../backend/chat_grounding.py#L117) | 발화의 명시 시각을 분 단위로 계산한다. 모호한 시각은 None으로 둔다. |
| `_compact` | [backend/chat_grounding.py:39](../backend/chat_grounding.py#L39) | 근거 비교에만 쓸 공백 없는 문자열을 만든다. 원문과 저장 상태는 바꾸지 않는다. |
| `_condition_group` | [backend/dialogue_memory.py:212](../backend/dialogue_memory.py#L212) | 날짜/시각은 같은 변경 묶음으로 검증·동의한다. 다른 필드의 성공은 보존한다. |
| `_condition_value` | [backend/dialogue_memory.py:145](../backend/dialogue_memory.py#L145) | 실제 설정의 기존 grounding을 재사용한다. 음악 분위기는 이 함수의 분류 입력이 아니다. |
| `_Conversation` | [backend/conversation_store.py:60](../backend/conversation_store.py#L60) | TTL 동안만 살아 있는 정규 상태와 bounded 응답 cache. |
| `_date_from_text` | [backend/chat_grounding.py:80](../backend/chat_grounding.py#L80) | 현재 발화의 지원되는 단일 날짜만 계산한다. 애매하거나 여러 날짜면 None이다. |
| `_date_value` | [backend/dialogue_memory.py:132](../backend/dialogue_memory.py#L132) | 명시 날짜와 단순 상대 날짜를 코드로 대조한다. 시각이나 오늘을 기본값으로 만들지 않는다. |
| `_day` | [backend/exploration.py:47](../backend/exploration.py#L47) | 명시 날짜를 ISO 날짜로 검증한다. 잘못된 날짜는 InputError로 전달한다. |
| `_digest` | [backend/exploration.py:37](../backend/exploration.py#L37) | JSON으로 표현 가능한 조건/사실의 순서 독립 fingerprint를 반환한다. |
| `_draft_date` | [backend/chat_grounding.py:98](../backend/chat_grounding.py#L98) | 초안의 명시 날짜를 반환한다. 유효하지 않거나 서로 다르면 보류한다. |
| `_environment_matches` | [backend/chat_grounding.py:379](../backend/chat_grounding.py#L379) | 실내외 후보를 직접 언급·거절·선호 해제와 대조한다. 모호하면 확정하지 않는다. |
| `_event` | [backend/exploration.py:116](../backend/exploration.py#L116) | 서울시 실제 행 하나를 기존 행사 카드 필드로 정규화한다. 잘못된 식별/기간은 제외한다. |
| `_evidence` | [backend/dialogue_memory.py:36](../backend/dialogue_memory.py#L36) | 새 후보의 출처가 현재 사용자 발화인지 검증한다. 의미 동일성을 증명하지는 않는다. |
| `_exclusions_match` | [backend/chat_grounding.py:329](../backend/chat_grounding.py#L329) | 제외 항목은 새 발화에 있거나 기존에 있어야 하며 해제는 항목별 명시해야 한다. |
| `_exclusions_match.released` | [backend/chat_grounding.py:335](../backend/chat_grounding.py#L335) | 제외의 해제와 해제하지 말라는 발화를 구분한다. |
| `_explicit_removal` | [backend/chat_grounding.py:51](../backend/chat_grounding.py#L51) | 관심어 등 긍정 조건의 항목별 해제만 인정하고 해제하지 말라는 요청은 거절한다. |
| `_free_matches` | [backend/chat_grounding.py:266](../backend/chat_grounding.py#L266) | 명시된 무료 조건과 해제만 인정하며 질문 맥락 없는 반대 값은 막는다. |
| `_hard_evidence` | [backend/dialogue_memory.py:88](../backend/dialogue_memory.py#L88) | 모델 hard 표지가 아니라 사실 제약 차원과 현재 발화의 근거를 대조한다. |
| `_hard_filter` | [backend/exploration.py:249](../backend/exploration.py#L249) | 실제 기간/요금/명시 제외와 거리 한도를 판정한다. 필요한 사실 결측은 통과시키지 않는다. |
| `_history` | [backend/dialogue_memory.py:123](../backend/dialogue_memory.py#L123) | 현재 주 질문만 grounding 맥락으로 전달한다. STT 공지는 여기에 들어오지 않는다. |
| `_identifier` | [backend/conversation_store.py:75](../backend/conversation_store.py#L75) | 본문/로그를 포함하지 않고 짧은 opaque ID 형식만 확인한다. |
| `_inputs` | [backend/exploration.py:57](../backend/exploration.py#L57) | canonical 상태와 이전 draft/dialogue 별칭을 읽고 좌표/선택 필터만 검증한다. |
| `_invalidate` | [backend/dialogue_memory.py:56](../backend/dialogue_memory.py#L56) | 현재 결과와 새 의미/조건의 혼입을 막는다. 과거 말풍선 스냅샷은 외부 UI 소유다. |
| `_issue` | [backend/dialogue_memory.py:46](../backend/dialogue_memory.py#L46) | 진단에는 필드/코드만 넣고 사용자 인용이나 좌표를 복제하지 않는다. |
| `_json_copy` | [backend/conversation_store.py:80](../backend/conversation_store.py#L80) | 유한 JSON 자료만 독립 복사하며 함수·NaN 같은 객체를 거부한다. |
| `_keywords_match` | [backend/chat_grounding.py:357](../backend/chat_grounding.py#L357) | 관심어 추가에는 긍정 근거, 삭제에는 해당 항목 또는 관심어 전체의 명시 해제를 요구한다. |
| `_metadata` | [backend/dialogue_memory.py:180](../backend/dialogue_memory.py#L180) | 사용자 발화 후보의 출처와 명시 강도를 보관한다. 사용자 확정으로 자동 승격하지 않는다. |
| `_no_preference` | [backend/chat_grounding.py:60](../backend/chat_grounding.py#L60) | 해당 선호를 직접 해제하거나 직전 해당 질문에 무관하다고 답한 경우만 인정한다. |
| `_origin_matches` | [backend/chat_grounding.py:243](../backend/chat_grounding.py#L243) | 명시적 출발 표현이나 직전 출발지 질문과 지명을 대조한다. |
| `_price` | [backend/exploration.py:310](../backend/exploration.py#L310) | 무료 표기와 구체 요금이 충돌하면 unknown이다. 복수/부분 유료를 무료로 통과시키지 않는다. |
| `_price_amount` | [backend/chat_grounding.py:291](../backend/chat_grounding.py#L291) | 근거의 단일 원화 금액만 읽는다. 복합 표현은 추측하지 않는다. |
| `_question` | [backend/dialogue_memory.py:441](../backend/dialogue_memory.py#L441) | 현재 질문 대상을 보존한다. 호출자가 반환한 질문을 상태와 이력에 기록한다. |
| `_question_target` | [backend/chat_grounding.py:149](../backend/chat_grounding.py#L149) | 직전 질문이 시작 또는 종료 하나를 묻는 경우에만 대상을 반환한다. |
| `_rank` | [backend/exploration.py:338](../backend/exploration.py#L338) | 실제 원문 인용이 유효한 점수만 사용한다. 선택 정렬 실패는 코드 정렬로 복구한다. |
| `_rank.baseline` | [backend/exploration.py:347](../backend/exploration.py#L347) | 모델 호출 전 관심어·실제 직선거리를 이용해 후보 입력 순서를 정한다. |
| `_rank.order` | [backend/exploration.py:385](../backend/exploration.py#L385) | 관련성/관심어와 실제 직선거리를 정렬한다. 보행 시간을 추정하지 않는다. |
| `_request_kind_matches` | [backend/chat_grounding.py:392](../backend/chat_grounding.py#L392) | 한 곳과 코스 요청의 명시 수량·표현을 대조하고 반대·복합 요청은 보류한다. |
| `_requirements_match` | [backend/chat_grounding.py:412](../backend/chat_grounding.py#L412) | 필수 조건의 임의 삭제와 발화에 없는 신규 제약을 차단한다. |
| `_requirements_match.explicitly_removed` | [backend/chat_grounding.py:422](../backend/chat_grounding.py#L422) | 제거할 각 항목에 해제 표현이 직접 연결된 경우만 인정한다. |
| `_requirements_match.present` | [backend/chat_grounding.py:418](../backend/chat_grounding.py#L418) | 띄어쓰기를 제외한 조건 원문이 발화에 있는지 확인한다. |
| `_Reservation` | [backend/conversation_store.py:46](../backend/conversation_store.py#L46) | 한 턴의 입력 hash와 commit을 제한하는 소유권 fence. |
| `_scope` | [backend/dialogue_memory.py:67](../backend/dialogue_memory.py#L67) | 활동 종속 선호와 공통 예산·위치·필수 제약의 소유 범위를 구별한다. |
| `_selected_candidate` | [backend/dialogue_memory.py:502](../backend/dialogue_memory.py#L502) | 클라이언트 값 대신 현재 결과/표시 묶음/실제 tool 후보를 대조한 snapshot을 반환한다. |
| `_selection_conditions` | [backend/dialogue_memory.py:490](../backend/dialogue_memory.py#L490) | 탐색과 같은 출발지 의미값(label/좌표)만 비교하고 주소 등 표시 메타는 제외한다. |
| `_set_condition` | [backend/dialogue_memory.py:187](../backend/dialogue_memory.py#L187) | 단일 검증 조건을 적용하고 연결된 값과 미해결 항목을 정리한다. |
| `_source` | [backend/exploration.py:173](../backend/exploration.py#L173) | 기존 공급자 조회를 재사용한다. validate/recommend의 필수 일정 생성 경로는 호출하지 않는다. |
| `_term_rejected` | [backend/chat_grounding.py:44](../backend/chat_grounding.py#L44) | 해당 항목 바로 뒤의 부정만 검사한다. 다른 절의 거절을 이 항목에 붙이지 않는다. |
| `_text` | [backend/dialogue_memory.py:29](../backend/dialogue_memory.py#L29) | 유한한 짧은 평문을 검증한다. 모델 텍스트를 실행하거나 HTML로 만들지 않는다. |
| `_text` | [backend/exploration.py:42](../backend/exploration.py#L42) | 공급자 문자열만 길이 제한해 읽는다. 결측을 임의 설명으로 채우지 않는다. |
| `_time_matches` | [backend/chat_grounding.py:160](../backend/chat_grounding.py#L160) | 모델 시각을 발화의 날짜·시각·대상과 비교한다. 지원하지 않는 표현은 보류한다. |
| `_unknown_hard_preferences` | [backend/exploration.py:321](../backend/exploration.py#L321) | 이미 장르 필터/명시 제외로 표현한 hard 선호만 허용하고 나머지 의미 hard는 보류한다. |
| `_unresolved` | [backend/dialogue_memory.py:74](../backend/dialogue_memory.py#L74) | 근거 있는 미해결 필수조건만 실행 보류로 남긴다. 잘못된 soft 후보는 대화를 막지 않는다. |
| `_v3_display_batch` | [backend/agent_v3.py:228](../backend/agent_v3.py#L228) | 서버 결과의 현재 표시 순서만 최대3개 발급한다. 후보 사실과 전체 풀은 바꾸지 않는다. |
| `_v3_execute` | [backend/agent_v3.py:260](../backend/agent_v3.py#L260) | Execute one policy plan against actual adapters and preserve errors as typed tool facts. |
| `_v3_model_context` | [backend/agent_v3.py:100](../backend/agent_v3.py#L100) | Provide semantic memory and current question, excluding coordinates, tool pools, and status notices. |
| `_v3_model_context.without_coordinates` | [backend/agent_v3.py:106](../backend/agent_v3.py#L106) | Strip location coordinates from nested metadata before sending semantic context. |
| `_v3_place_key` | [backend/agent_v3.py:143](../backend/agent_v3.py#L143) | Normalize map name aliases without inventing a place or coordinate. |
| `_v3_ranker` | [backend/agent_v3.py:178](../backend/agent_v3.py#L178) | Build a single optional semantic ranking call keyed by actual source fields and preferences. |
| `_v3_ranker.rank` | [backend/agent_v3.py:186](../backend/agent_v3.py#L186) | Rank at most 24 actual candidates; failure leaves deterministic ordering intact. |
| `_v3_resolve_origin` | [backend/agent_v3.py:149](../backend/agent_v3.py#L149) | Adopt a unique actual match; retain ambiguous real candidates for the existing picker. |
| `_v3_result_text` | [backend/agent_v3.py:211](../backend/agent_v3.py#L211) | Describe real result status and limits without letting a model create factual claims. |
| `_v3_selection_error` | [backend/agent_v3.py:250](../backend/agent_v3.py#L250) | 선택 실패는 새 검색/대화 초기화 없이 현재 후보에서 회복할 안내로 반환한다. |
| `_v3_tool` | [backend/agent_v3.py:121](../backend/agent_v3.py#L121) | Bound tool waiting and outstanding work; a timed-out worker cannot commit conversation state. |
| `_v3_tool.run` | [backend/agent_v3.py:129](../backend/agent_v3.py#L129) | Release the worker admission slot even when a source raises an exception. |
| `_venue` | [backend/exploration.py:151](../backend/exploration.py#L151) | 실지도 장소를 카드 형태로 바꾼다. 영화관을 상영작/회차나 검증된 방문계획으로 바꾸지 않는다. |
| `_walk_eligibility` | [backend/exploration.py:219](../backend/exploration.py#L219) | 공급자 분류로 주 산책 목적지만 남긴다. 이름·거리·모델 점수는 승인 근거가 아니다. |
| `_window` | [backend/exploration.py:81](../backend/exploration.py#L81) | 선택한 날짜/기간·시각만 읽는다. 미입력 날짜와 종료시각을 생성하지 않는다. |
| `actions` | [frontend/js/chat.js:301](../frontend/js/chat.js#L301) | JS/TS 정규식 후보; AST 검증 아님 |
| `agentActions` | [frontend/js/chat.js:1345](../frontend/js/chat.js#L1345) | JS/TS 정규식 후보; AST 검증 아님 |
| `agentConnected` | [frontend/js/agent-session.js:20](../frontend/js/agent-session.js#L20) | JS/TS 정규식 후보; AST 검증 아님 |
| `AgentHttpIntegrationTests` | [backend/test_agent_integration.py:15](../backend/test_agent_integration.py#L15) | 외부 네트워크 없이 Preview의 실제 HTTP 경계와 대화 처리를 통과한다. |
| `AgentHttpIntegrationTests.mock_provider` | [backend/test_agent_integration.py:50](../backend/test_agent_integration.py#L50) | 서버가 보낸 메시지에 맞춘 Anthropic 형식의 고정 JSON을 반환한다. |
| `AgentHttpIntegrationTests.request` | [backend/test_agent_integration.py:66](../backend/test_agent_integration.py#L66) | 새 HTTP 연결로 실제 상태·헤더·JSON 본문을 읽는다. |
| `AgentHttpIntegrationTests.setUpClass` | [backend/test_agent_integration.py:19](../backend/test_agent_integration.py#L19) | 임시 loopback 서버와 공급자·설정 대체를 시작한다. |
| `AgentHttpIntegrationTests.tearDownClass` | [backend/test_agent_integration.py:40](../backend/test_agent_integration.py#L40) | 서버, 스레드, 프로세스 환경과 모의 공급자를 복원한다. |
| `AgentHttpIntegrationTests.test_cors_preflight_and_disallowed_origin` | [backend/test_agent_integration.py:105](../backend/test_agent_integration.py#L105) | 허용된 사전 요청과 거부된 origin의 실제 HTTP 응답을 확인한다. |
| `AgentHttpIntegrationTests.test_partial_clarification_and_same_value_confirmation` | [backend/test_agent_integration.py:78](../backend/test_agent_integration.py#L78) | 부분 보류·기존 초안 보존과 같은 값 재확인을 실제 POST에서 검사한다. |
| `allowed_origins` | [backend/preview.py:25](../backend/preview.py#L25) | 환경변수의 명시적 HTTP(S) origin만 허용한다. 와일드카드·경로·자격정보는 제외한다. |
| `answer` | [frontend/js/chat.js:981](../frontend/js/chat.js#L981) | JS/TS 정규식 후보; AST 검증 아님 |
| `api_key` | [backend/transit.py:20](../backend/transit.py#L20) | 전용 환경변수 또는 로컬 제외 파일의 키 한 개만 읽는다. 값은 응답·로그에 출력하지 않는다. |
| `app_asset` | [backend/team_app.py:32](../backend/team_app.py#L32) | 현재 /app/ 요청의 제한된 정적 자산을 반환한다. 경로이탈/비밀파일/과대 파일은 거절한다. |
| `app_directory` | [backend/team_app.py:12](../backend/team_app.py#L12) | .local의 인계 패키지 frontend만 선택한다. 미설정/손상은 경로 노출 없이 미연결로 처리한다. |
| `apply` | [backend/preferences.py:50](../backend/preferences.py#L50) | 무료/예산/명시 제외를 적용하고 관심 키워드·직선 근접성으로 정렬한다. 미확인은 숨기지 않는다. |
| `apply` | [frontend/js/agent-session.js:31](../frontend/js/agent-session.js#L31) | JS/TS 정규식 후보; AST 검증 아님 |
| `apply` | [frontend/js/app.js:230](../frontend/js/app.js#L230) | JS/TS 정규식 후보; AST 검증 아님 |
| `apply` | [frontend/js/chat.js:387](../frontend/js/chat.js#L387) | JS/TS 정규식 후보; AST 검증 아님 |
| `apply.order` | [backend/preferences.py:78](../backend/preferences.py#L78) | 걷기 최소 선호 시 근접성 먼저, 그 외 관심어 먼저. 실제 도보 시간으로 간주하지 않는다. |
| `apply_event` | [backend/dialogue_memory.py:587](../backend/dialogue_memory.py#L587) | 검증된 UI 선택/동의 이벤트를 새 상태로 반영한다. 실제 후보의 출처 검증은 호출자 소유다. |
| `apply_interpretation` | [backend/chat_conditions.py:106](../backend/chat_conditions.py#L106) | 해석 결과를 복사한 초안에 반영한다. 확정값 충돌·늦은 응답은 자동 반영하지 않는다. |
| `applyClarificationEvidence` | [frontend/js/chat.js:834](../frontend/js/chat.js#L834) | JS/TS 정규식 후보; AST 검증 아님 |
| `applyDraft` | [backend/team_chat.js:293](../backend/team_chat.js#L293) | JS/TS 정규식 후보; AST 검증 아님 |
| `begin` | [backend/voice_session.js:33](../backend/voice_session.js#L33) | JS/TS 정규식 후보; AST 검증 아님 |
| `begin` | [frontend/js/chat.js:598](../frontend/js/chat.js#L598) | JS/TS 정규식 후보; AST 검증 아님 |
| `beginVoiceDiagnostics` | [backend/team_chat.js:110](../backend/team_chat.js#L110) | JS/TS 정규식 후보; AST 검증 아님 |
| `broken_links` | [utils/scripts/harness.py:49](../utils/scripts/harness.py#L49) | Check relative inline links outside fenced code; skip URLs and anchors. |
| `bubble` | [frontend/js/chat.js:264](../frontend/js/chat.js#L264) | JS/TS 정규식 후보; AST 검증 아님 |
| `build_course` | [backend/course.py:102](../backend/course.py#L102) | 사용자 출발 좌표와 공개 후보의 도보 초를 한 번 조회해 가장 짧은 가능한 조합을 선택한다. |
| `button` | [frontend/js/util.js:22](../frontend/js/util.js#L22) | JS/TS 정규식 후보; AST 검증 아님 |
| `cachedGreeting` | [frontend/js/weather.js:68](../frontend/js/weather.js#L68) | JS/TS 정규식 후보; AST 검증 아님 |
| `call` | [backend/tour_places.py:20](../backend/tour_places.py#L20) | 공식 고정 주소로 호출하며 응답 크기/형식을 제한한다. 원본 URL/키 포함 오류를 반환하지 않는다. |
| `cancel` | [backend/voice_session.js:110](../backend/voice_session.js#L110) | JS/TS 정규식 후보; AST 검증 아님 |
| `cancel` | [backend/voice_session.js:26](../backend/voice_session.js#L26) | JS/TS 정규식 후보; AST 검증 아님 |
| `cancelVoiceRequest` | [backend/team_chat.js:411](../backend/team_chat.js#L411) | JS/TS 정규식 후보; AST 검증 아님 |
| `candidateById` | [frontend/js/state.js:92](../frontend/js/state.js#L92) | JS/TS 정규식 후보; AST 검증 아님 |
| `candidateIndex` | [backend/team_voice_actions.js:18](../backend/team_voice_actions.js#L18) | JS/TS 정규식 후보; AST 검증 아님 |
| `candidateSpeech` | [backend/team_voice_actions.js:55](../backend/team_voice_actions.js#L55) | JS/TS 정규식 후보; AST 검증 아님 |
| `capability` | [backend/chat_knowledge.py:40](../backend/chat_knowledge.py#L40) | 허용된 활동의 실행 능력 복사본을 반환한다. 미지원 개념은 열린 탐색으로 남긴다. |
| `captureChatPosition` | [frontend/js/app.js:22](../frontend/js/app.js#L22) | JS/TS 정규식 후보; AST 검증 아님 |
| `card` | [frontend/js/chat.js:241](../frontend/js/chat.js#L241) | JS/TS 정규식 후보; AST 검증 아님 |
| `chat` | [backend/naito_chat.py:108](../backend/naito_chat.py#L108) | 대화 API 결과를 (HTTP상태, 본문)으로 반환한다. 장애 시 가짜 해석/추천으로 대체하지 않는다. |
| `chat_v3` | [backend/agent_v3.py:325](../backend/agent_v3.py#L325) | Run canonical v3 events with partial interpretation, bounded tools, and fenced commits. |
| `ChatConditionTests` | [backend/test_chat_conditions.py:8](../backend/test_chat_conditions.py#L8) | 공급자와 프론트가 연결되기 전에 검증할 독립적인 대화 상태 사례다. |
| `ChatConditionTests.apply` | [backend/test_chat_conditions.py:17](../backend/test_chat_conditions.py#L17) | 현재 입력의 revision 2에 대한 해석을 적용한다. |
| `ChatConditionTests.resolve` | [backend/test_chat_conditions.py:22](../backend/test_chat_conditions.py#L22) | 초안이 변하지 않은 상태에서 사용자 동의/거절을 적용한다. |
| `ChatConditionTests.setUp` | [backend/test_chat_conditions.py:11](../backend/test_chat_conditions.py#L11) | 검증된 출발 좌표와 정확히 60분인 조건을 준비한다. |
| `ChatConditionTests.test_59_rejected_60_allowed` | [backend/test_chat_conditions.py:87](../backend/test_chat_conditions.py#L87) | 최소60분 규칙은 기존 추천 서버 검증을 그대로 사용한다. |
| `ChatConditionTests.test_bad_or_factual_model_output_rejected` | [backend/test_chat_conditions.py:101](../backend/test_chat_conditions.py#L101) | 좌표/행사 사실/비정상 형식은 해석 결과로 받지 않는다. |
| `ChatConditionTests.test_category_and_no_mutation` | [backend/test_chat_conditions.py:26](../backend/test_chat_conditions.py#L26) | 국악 해석은 초안에만 반영하고 원본·최종 확인 경계를 유지한다. |
| `ChatConditionTests.test_changed_origin_invalidates_coordinates_only_on_accept` | [backend/test_chat_conditions.py:55](../backend/test_chat_conditions.py#L55) | 새 출발지 동의 뒤 기존 좌표를 재사용하지 않으며 거절하면 보존한다. |
| `ChatConditionTests.test_confirmed_accept_reject_and_pending` | [backend/test_chat_conditions.py:43](../backend/test_chat_conditions.py#L43) | 확정 분류 변경은 수락/거절/미응답을 구분한다. |
| `ChatConditionTests.test_course_requires_stay_and_alias` | [backend/test_chat_conditions.py:94](../backend/test_chat_conditions.py#L94) | route는 course로 정규화하고 체류시간을 임의 기본값으로 채우지 않는다. |
| `ChatConditionTests.test_invalid_decisions_and_state` | [backend/test_chat_conditions.py:117](../backend/test_chat_conditions.py#L117) | 문자열 동의·모르는 항목·비정상 revision을 거절한다. |
| `ChatConditionTests.test_missing_question_and_no_default_origin` | [backend/test_chat_conditions.py:35](../backend/test_chat_conditions.py#L35) | 비어 있는 입력에는 출발지 질문 하나와 전체 누락 항목을 반환한다. |
| `ChatConditionTests.test_null_no_change_and_timezone` | [backend/test_chat_conditions.py:111](../backend/test_chat_conditions.py#L111) | null은 삭제가 아니며 시각은 한국 시간으로 바꾼다. |
| `ChatConditionTests.test_same_name_origin_still_requires_place_reselection` | [backend/test_chat_conditions.py:64](../backend/test_chat_conditions.py#L64) | 시청처럼 같은 이름인 다른 장소도 재검색하며 동의 전에는 기존 좌표를 보존한다. |
| `ChatConditionTests.test_stale_response_and_manual_edit` | [backend/test_chat_conditions.py:78](../backend/test_chat_conditions.py#L78) | AI 응답/동의 대기 중 직접 수정된 현재값은 보존한다. |
| `check` | [utils/scripts/catalog.py:225](../utils/scripts/catalog.py#L225) | Return missing or stale generated indexes; tolerate Git line endings. |
| `checkedAt` | [frontend/js/util.js:57](../frontend/js/util.js#L57) | JS/TS 정규식 후보; AST 검증 아님 |
| `chip` | [frontend/js/chat.js:304](../frontend/js/chat.js#L304) | JS/TS 정규식 후보; AST 검증 아님 |
| `clarification_text` | [backend/chat_grounding.py:510](../backend/chat_grounding.py#L510) | 보류 필드명을 한국어 확인 질문으로 바꾼다. 원문과 모델 응답은 노출하지 않는다. |
| `clear` | [frontend/js/chat.js:576](../frontend/js/chat.js#L576) | JS/TS 정규식 후보; AST 검증 아님 |
| `clearShapes` | [backend/location_view.js:9](../backend/location_view.js#L9) | JS/TS 정규식 후보; AST 검증 아님 |
| `Clock` | [backend/test_conversation_store.py:9](../backend/test_conversation_store.py#L9) | 시간을 기다리지 않고 초 단위로 전진시키는 단조 시험 시계. |
| `Clock` | [backend/test_naito_v3.py:27](../backend/test_naito_v3.py#L27) | 네트워크 대기 없이 lease 인계 시점만 독립 제어한다. |
| `Clock.__call__` | [backend/test_conversation_store.py:16](../backend/test_conversation_store.py#L16) | 주입된 저장소에 현재 시험 시각을 반환한다. |
| `Clock.__call__` | [backend/test_naito_v3.py:34](../backend/test_naito_v3.py#L34) | 저장소가 사용하는 단조 시각을 반환한다. |
| `Clock.__init__` | [backend/test_conversation_store.py:12](../backend/test_conversation_store.py#L12) | 시험 시작을 임의의 양수 시각으로 고정한다. |
| `Clock.__init__` | [backend/test_naito_v3.py:30](../backend/test_naito_v3.py#L30) | 시작 시각을 고정한다. |
| `Clock.advance` | [backend/test_conversation_store.py:20](../backend/test_conversation_store.py#L20) | 타이머 스레드 없이 TTL/lease 경계를 넘긴다. |
| `closeOriginPicker` | [frontend/js/chat.js:1420](../frontend/js/chat.js#L1420) | JS/TS 정규식 후보; AST 검증 아님 |
| `closer` | [frontend/js/chat.js:1235](../frontend/js/chat.js#L1235) | JS/TS 정규식 후보; AST 검증 아님 |
| `closeSheet` | [frontend/js/place.js:148](../frontend/js/place.js#L148) | JS/TS 정규식 후보; AST 검증 아님 |
| `code_checks` | [utils/scripts/harness.py:20](../utils/scripts/harness.py#L20) | Parse Python statically and require module/function/class docstrings. |
| `compact` | [utils/scripts/catalog.py:63](../utils/scripts/catalog.py#L63) | Return one short Markdown-safe line from a docstring. |
| `conditionKey` | [frontend/js/chat.js:1107](../frontend/js/chat.js#L1107) | JS/TS 정규식 후보; AST 검증 아님 |
| `conditionLabel` | [backend/team_chat.js:338](../backend/team_chat.js#L338) | JS/TS 정규식 후보; AST 검증 아님 |
| `config` | [utils/scripts/catalog.py:21](../utils/scripts/catalog.py#L21) | Read only the public harness configuration, never environment values. |
| `configureAgent` | [frontend/js/agent-session.js:14](../frontend/js/agent-session.js#L14) | JS/TS 정규식 후보; AST 검증 아님 |
| `confirmClarificationFields` | [frontend/js/chat.js:805](../frontend/js/chat.js#L805) | JS/TS 정규식 후보; AST 검증 아님 |
| `confirmExplicitChoices` | [frontend/js/chat.js:823](../frontend/js/chat.js#L823) | JS/TS 정규식 후보; AST 검증 아님 |
| `ContactTest` | [backend/test_contact.py:6](../backend/test_contact.py#L6) | 개요 없음 |
| `ContactTest.test_detail_code_only_for_culture_portal` | [backend/test_contact.py:7](../backend/test_contact.py#L7) | 개요 없음 |
| `ContactTest.test_no_inquiry_means_no_phone` | [backend/test_contact.py:17](../backend/test_contact.py#L17) | 개요 없음 |
| `ContactTest.test_phones_from_first_inquiry` | [backend/test_contact.py:13](../backend/test_contact.py#L13) | 개요 없음 |
| `ContactTest.test_rejects_other_urls` | [backend/test_contact.py:20](../backend/test_contact.py#L20) | 개요 없음 |
| `content_choice_event` | [backend/dialogue_memory.py:451](../backend/dialogue_memory.py#L451) | 현재 표시 묶음의 명시 번호/유일한 이름만 선택 이벤트로 해석한다. 사실/모델 호출은 없다. |
| `contents` | [utils/scripts/verify_watch.py:24](../utils/scripts/verify_watch.py#L24) | Read generated text, tolerating a brief replacement window. |
| `contentSelectionState` | [frontend/js/chat.js:171](../frontend/js/chat.js#L171) | JS/TS 정규식 후보; AST 검증 아님 |
| `conversation_store` | [backend/agent_v3.py:46](../backend/agent_v3.py#L46) | Return the process-local bounded canonical store; no user data is written to disk. |
| `ConversationStore` | [backend/conversation_store.py:85](../backend/conversation_store.py#L85) | TTL30분/100대화/20응답/10초 lease의 메모리 저장소; 모든 시간은 초다. |
| `ConversationStore.__init__` | [backend/conversation_store.py:88](../backend/conversation_store.py#L88) | 단조 시계 주입으로 실제 기다림 없이 만료·동시성을 검증할 수 있게 한다. |
| `ConversationStore._error` | [backend/conversation_store.py:112](../backend/conversation_store.py#L112) | 현재 snapshot을 포함한 오류를 만들되 원 요청은 포함하지 않는다. |
| `ConversationStore._get` | [backend/conversation_store.py:131](../backend/conversation_store.py#L131) | 만료·서버 재시작·다른 epoch를 기존 상태로 조용히 복구하지 않는다. |
| `ConversationStore._invalidate` | [backend/conversation_store.py:118](../backend/conversation_store.py#L118) | 예약 token을 제거해 취소·인계·만료된 작업의 commit을 차단한다. |
| `ConversationStore._metadata` | [backend/conversation_store.py:102](../backend/conversation_store.py#L102) | 서버의 절대 단조시각 대신 남은 lease와 버전을 공개한다. |
| `ConversationStore._new` | [backend/conversation_store.py:150](../backend/conversation_store.py#L150) | 기존 대화 내용을 복사하지 않고 호출자가 검증한 초기 상태로 생성한다. |
| `ConversationStore._owner` | [backend/conversation_store.py:141](../backend/conversation_store.py#L141) | 현재 문서의 유효 lease만 허용하며 만료 owner의 자동 갱신은 금지한다. |
| `ConversationStore._prune` | [backend/conversation_store.py:124](../backend/conversation_store.py#L124) | 사용자 활동 TTL이 지난 자료만 제거하며 heartbeat는 TTL을 늘리지 않는다. |
| `ConversationStore.cancel` | [backend/conversation_store.py:305](../backend/conversation_store.py#L305) | 호출자의 예기치 않은 예외에서 미확정 예약과 늦은 commit을 무효화한다. |
| `ConversationStore.commit` | [backend/conversation_store.py:269](../backend/conversation_store.py#L269) | 예약·epoch·revision·writer lease가 유효할 때만 상태와 결과를 한 번 확정한다. |
| `ConversationStore.heartbeat` | [backend/conversation_store.py:196](../backend/conversation_store.py#L196) | 살아 있는 현재 문서의 lease만 연장하고 사용자 활동 TTL은 늘리지 않는다. |
| `ConversationStore.open` | [backend/conversation_store.py:166](../backend/conversation_store.py#L166) | 새 대화 생성/재연결; 활성 다른 문서는 fork, resume 모드는 만료까지 대기한다. |
| `ConversationStore.release` | [backend/conversation_store.py:205](../backend/conversation_store.py#L205) | 이전 문서의 best-effort 해제도 예약을 fence하여 늦은 완료를 무효화한다. |
| `ConversationStore.reserve` | [backend/conversation_store.py:216](../backend/conversation_store.py#L216) | 검증된 메타데이터의 다음 턴을 예약하거나 중복 결과/동기화 오류를 반환한다. |
| `ConversationStoreTests` | [backend/test_conversation_store.py:25](../backend/test_conversation_store.py#L25) | 실제 저장소와 격리된 시간을 사용해 사용자 상태 보호를 검증한다. |
| `ConversationStoreTests.assert_error` | [backend/test_conversation_store.py:45](../backend/test_conversation_store.py#L45) | 오류 메시지가 아니라 안정된 코드로 저장 경계 실패를 단언한다. |
| `ConversationStoreTests.finish` | [backend/test_conversation_store.py:52](../backend/test_conversation_store.py#L52) | 예약 밖에서 계산한 상태와 업무 결과를 한 번 commit한다. |
| `ConversationStoreTests.request` | [backend/test_conversation_store.py:34](../backend/test_conversation_store.py#L34) | 서버가 발급한 메타데이터로 현재 다음 턴의 요청을 만든다. |
| `ConversationStoreTests.setUp` | [backend/test_conversation_store.py:28](../backend/test_conversation_store.py#L28) | 각 시험에 독립 서버 상태·문서·대화를 만든다. |
| `ConversationStoreTests.test_active_duplicate_tab_forks_clean_factory_state` | [backend/test_conversation_store.py:143](../backend/test_conversation_store.py#L143) | 복제 문서가 활성 대화 handle을 가져도 이전 니즈·제약을 복사하지 않는다. |
| `ConversationStoreTests.test_cached_old_response_has_current_canonical_state` | [backend/test_conversation_store.py:83](../backend/test_conversation_store.py#L83) | 옛 응답 재전달이 최신 취향·revision을 덮지 않게 한다. |
| `ConversationStoreTests.test_cancel_uncommitted_job_prevents_late_apply` | [backend/test_conversation_store.py:243](../backend/test_conversation_store.py#L243) | 예기치 않은 호출자 예외 뒤 취소한 token으로 상태를 반영할 수 없다. |
| `ConversationStoreTests.test_capacity_rejects_new_chat_without_evicting_active_state` | [backend/test_conversation_store.py:223](../backend/test_conversation_store.py#L223) | 포화가 기존 대화·진행 작업을 버리지 않고 TTL 이후 용량을 회수한다. |
| `ConversationStoreTests.test_duplicate_completed_turn_replays_without_reservation` | [backend/test_conversation_store.py:73](../backend/test_conversation_store.py#L73) | 응답 손실 뒤 동일 요청은 원 업무 결과와 현재 snapshot을 재전달한다. |
| `ConversationStoreTests.test_error_result_commits_meaning_once_and_retry_is_new_turn` | [backend/test_conversation_store.py:232](../backend/test_conversation_store.py#L232) | 도구 장애를 의미와 함께 확정하고 도구 재시도는 새 seq에서 한 번만 확정한다. |
| `ConversationStoreTests.test_heartbeat_allows_long_job_without_holding_lock` | [backend/test_conversation_store.py:182](../backend/test_conversation_store.py#L182) | 네트워크 계산을 흉내 낸 지연 동안 heartbeat는 독립적으로 성공한다. |
| `ConversationStoreTests.test_heartbeats_do_not_keep_inactive_chat_forever` | [backend/test_conversation_store.py:212](../backend/test_conversation_store.py#L212) | 브라우저 heartbeat만 지속돼도 사용자 비활동 TTL에는 대화가 만료된다. |
| `ConversationStoreTests.test_invalid_input_does_not_mutate_or_leak_request` | [backend/test_conversation_store.py:251](../backend/test_conversation_store.py#L251) | 잘못된 seq/JSON/epoch는 원 사용자 발화를 오류문에 노출하지 않는다. |
| `ConversationStoreTests.test_lease_expiry_alone_prevents_commit` | [backend/test_conversation_store.py:176](../backend/test_conversation_store.py#L176) | 다른 문서가 없더라도 만료 lease의 작업을 성공 commit하지 않는다. |
| `ConversationStoreTests.test_lease_handover_fences_delayed_commit` | [backend/test_conversation_store.py:164](../backend/test_conversation_store.py#L164) | 지연 모델 작업 중 lease가 인계되면 옛 결과가 새 대화 상태에 들어가지 않는다. |
| `ConversationStoreTests.test_open_reserve_commit_snapshots_are_independent` | [backend/test_conversation_store.py:60](../backend/test_conversation_store.py#L60) | 호출자가 입력/반환 상태를 바꿔도 정규 상태는 바뀌지 않는다. |
| `ConversationStoreTests.test_pending_duplicate_and_changed_payload_do_not_create_second_job` | [backend/test_conversation_store.py:93](../backend/test_conversation_store.py#L93) | 진행 중 중복은 busy이며 같은 turn의 다른 본문은 충돌이다. |
| `ConversationStoreTests.test_release_invalidates_job_and_old_generation` | [backend/test_conversation_store.py:192](../backend/test_conversation_store.py#L192) | 페이지 이탈 해제는 대기 작업과 이전 lease 세대를 함께 무효화한다. |
| `ConversationStoreTests.test_reload_waits_for_lease_then_takes_over_same_conversation` | [backend/test_conversation_store.py:152](../backend/test_conversation_store.py#L152) | 새로고침은 활성 writer를 빼앗지 않고 만료 뒤 같은 상태에 연결한다. |
| `ConversationStoreTests.test_same_revision_concurrent_requests_have_one_winner` | [backend/test_conversation_store.py:104](../backend/test_conversation_store.py#L104) | 실제 두 스레드가 같은 revision을 예약해도 외부 작업 자격은 하나뿐이다. |
| `ConversationStoreTests.test_same_revision_concurrent_requests_have_one_winner.run` | [backend/test_conversation_store.py:109](../backend/test_conversation_store.py#L109) | 동일 시점에 예약을 시도하고 결과 코드만 수집한다. |
| `ConversationStoreTests.test_stale_revision_and_out_of_order_sequence_resynchronize` | [backend/test_conversation_store.py:126](../backend/test_conversation_store.py#L126) | 순서나 revision이 다른 새 요청은 현재 정규 상태를 받아 재동기화한다. |
| `ConversationStoreTests.test_ttl_expiry_does_not_resurrect_pending_job` | [backend/test_conversation_store.py:203](../backend/test_conversation_store.py#L203) | TTL 뒤 도착한 작업·옛 handle 재연결은 새 상태를 만들지 않는다. |
| `ConversationStoreTests.test_twenty_first_turn_keeps_watermark_without_old_response` | [backend/test_conversation_store.py:133](../backend/test_conversation_store.py#L133) | 20응답 캐시에서 빠진 과거 seq를 다시 LLM/도구 작업으로 예약하지 않는다. |
| `coordinate` | [backend/outing.py:30](../backend/outing.py#L30) | 유한한 위경도 숫자를 검증하고 잘못된 입력은 ValueError로 알린다. |
| `course_alternatives` | [backend/course.py:69](../backend/course.py#L69) | 동의 요청에만 같은 시간 한 곳·최대 두 시간 이른 두 곳의 검증된 대안을 반환한다. |
| `CourseTests` | [backend/test_course.py:9](../backend/test_course.py#L9) | 전시와 고정 공연이 있는 당일 요청을 독립적으로 검증한다. |
| `CourseTests.setUp` | [backend/test_course.py:12](../backend/test_course.py#L12) | 한국 시각 한 시간과 20분씩 관람할 수 있는 두 전시를 준비한다. |
| `CourseTests.test_alternative_unknown_missing_and_day_boundary` | [backend/test_course.py:67](../backend/test_course.py#L67) | 미확인 시간·누락 구간을 가능으로 만들지 않고 이전 날짜로 옮기지 않는다. |
| `CourseTests.test_boundary` | [backend/test_course.py:21](../backend/test_course.py#L21) | 도보 두 구간과 관람이 마감에 딱 맞으면 허용하고 1초 초과하면 제외한다. |
| `CourseTests.test_consent_and_alternatives` | [backend/test_course.py:47](../backend/test_course.py#L47) | 동의 없이는 대안을 만들지 않고 종료·체류를 보존한 한 곳/이른 출발을 계산한다. |
| `CourseTests.test_order_and_missing_routes` | [backend/test_course.py:36](../backend/test_course.py#L36) | 순서를 바꿔 가능한 일정만 선택하고 누락된 구간은 이동 0초로 쓰지 않는다. |
| `CourseTests.test_unknown_and_wait` | [backend/test_course.py:26](../backend/test_course.py#L26) | 공연 시작 전 대기는 포함하고 종료 미상 또는 휴관 조건 미상은 확정하지 않는다. |
| `create` | [backend/map_view.js:49](../backend/map_view.js#L49) | JS/TS 정규식 후보; AST 검증 아님 |
| `createContentSelectionButton` | [frontend/js/chat.js:183](../frontend/js/chat.js#L183) | JS/TS 정규식 후보; AST 검증 아님 |
| `credit` | [frontend/js/place.js:250](../frontend/js/place.js#L250) | JS/TS 정규식 후보; AST 검증 아님 |
| `culture_key` | [backend/culture_config.py:6](../backend/culture_config.py#L6) | seoul/tour 키를 읽는다. 명시 환경값이 로컬 파일보다 우선하며 미설정은 빈 문자열이다. |
| `culture_page` | [utils/scripts/agent_http_fixture.py:54](../utils/scripts/agent_http_fixture.py#L54) | 고정 행사 두 개를 제공하고 실제 추천 코드가 가격·분류·거리를 계산하게 한다. |
| `culture_page` | [utils/scripts/agent_v3_http_fixture.py:132](../utils/scripts/agent_v3_http_fixture.py#L132) | 공식 행사 필드의 공연6건/전시4건으로 표시3건과 전체pool 순서를 분리한다. |
| `culture_places` | [backend/tour_places.py:114](../backend/tour_places.py#L114) | 선택적 문화시설 API. 키 없음503/조회 실패502/정상0건을 구분하며 행사 추천에 몰래 혼합하지 않는다. |
| `culture_places.details` | [backend/tour_places.py:134](../backend/tour_places.py#L134) | 동일 ID의 소개/홈페이지를 가져온다. 상세 호출 실패를 값 없음으로 숨기지 않는다. |
| `cultureLabel` | [backend/team_culture.js:5](../backend/team_culture.js#L5) | JS/TS 정규식 후보; AST 검증 아님 |
| `CultureSourceTests` | [backend/test_culture_sources.py:13](../backend/test_culture_sources.py#L13) | 실제 키 없이 가능한 공급자 계약 회귀. 실서비스 성공과 구분한다. |
| `CultureSourceTests.response` | [backend/test_culture_sources.py:22](../backend/test_culture_sources.py#L22) | 공식 response/header/body 형태를 생성한다. 실제 행사 데이터가 아니다. |
| `CultureSourceTests.setUp` | [backend/test_culture_sources.py:16](../backend/test_culture_sources.py#L16) | 공개 위치의 시험 입력과 가상 문화시설 응답을 준비한다. |
| `CultureSourceTests.test_detail_identity_and_html` | [backend/test_culture_sources.py:71](../backend/test_culture_sources.py#L71) | 상세 ID 불일치를 거절하고 공식 텍스트/링크만 정규화한다. |
| `CultureSourceTests.test_facility_facts_and_unknowns` | [backend/test_culture_sources.py:61](../backend/test_culture_sources.py#L61) | 상설 장소에 행사 날짜/가격/공연 시작을 만들어 넣지 않는다. |
| `CultureSourceTests.test_full_facility_lookup_budget_and_secrets` | [backend/test_culture_sources.py:101](../backend/test_culture_sources.py#L101) | 목록→소개→공통 상세를 연결하고 무료 조건·비밀값 비노출을 확인한다. |
| `CultureSourceTests.test_full_facility_lookup_budget_and_secrets.source` | [backend/test_culture_sources.py:103](../backend/test_culture_sources.py#L103) | 세 고정 API의 모의 응답을 반환한다. |
| `CultureSourceTests.test_homepage_with_provider_annotation` | [backend/test_culture_sources.py:82](../backend/test_culture_sources.py#L82) | 실제 응답의 홈페이지 뒤 SNS 안내는 제외하고 잘못된 링크는 null로 둔다. |
| `CultureSourceTests.test_scope_and_missing_key_before_network` | [backend/test_culture_sources.py:92](../backend/test_culture_sources.py#L92) | 공연/코스/기록/잘못된반경 요청은 거절하고 키없음은503이다. |
| `CultureSourceTests.test_seoul_auth_failure_no_sample_retry` | [backend/test_culture_sources.py:37](../backend/test_culture_sources.py#L37) | 유효하지 않은 정식 키를 sample 성공으로 숨기지 않는다. |
| `CultureSourceTests.test_seoul_authenticated_and_sample_limits` | [backend/test_culture_sources.py:27](../backend/test_culture_sources.py#L27) | 정식 키1000건·미설정sample5건을 구분하며 입력 키를 경로 구분자로 해석하지 않는다. |
| `CultureSourceTests.test_source_failure_not_empty_or_partial_success` | [backend/test_culture_sources.py:116](../backend/test_culture_sources.py#L116) | 실패·권한거절·제한을0건으로 바꾸지 않고 URL에 있는 키를 오류로 내보내지 않는다. |
| `CultureSourceTests.test_tour_request_encoding_and_axis` | [backend/test_culture_sources.py:45](../backend/test_culture_sources.py#L45) | 국문 고정 주소·경도X/위도Y·인코딩키 1회 변환을 검사한다. |
| `CultureSourceTests.test_tour_zero_vs_malformed` | [backend/test_culture_sources.py:55](../backend/test_culture_sources.py#L55) | 0건은 정상이며 누락 목록/오류코드/XML은 정상 빈 결과가 아니다. |
| `currentCandidate` | [backend/team_voice_actions.js:47](../backend/team_voice_actions.js#L47) | JS/TS 정규식 후보; AST 검증 아님 |
| `d` | [frontend/js/chat.js:59](../frontend/js/chat.js#L59) | JS/TS 정규식 후보; AST 검증 아님 |
| `decide` | [backend/dialogue_memory.py:526](../backend/dialogue_memory.py#L526) | 알고 있는 의미와 실행 가능성으로 행동을 고른다. 선택 조건을 입력 폼으로 만들지 않는다. |
| `decide` | [backend/team_chat.js:346](../backend/team_chat.js#L346) | JS/TS 정규식 후보; AST 검증 아님 |
| `decode_shape` | [backend/walking.py:50](../backend/walking.py#L50) | Valhalla polyline6를 위도·경도 배열로 변환한다. 손상·범위 초과는 ValueError다. |
| `DeploymentKeyTests` | [backend/test_deployment_keys.py:10](../backend/test_deployment_keys.py#L10) | 환경변수 기반 배포와 로컬 개발의 설정 경계를 확인한다. |
| `DeploymentKeyTests.test_culture_environment_precedence` | [backend/test_deployment_keys.py:13](../backend/test_deployment_keys.py#L13) | 서울시/공공데이터 표준명과 호환명을 환경에서 읽으면 로컬 파일을 열지 않는다. |
| `DeploymentKeyTests.test_explicit_empty_naito_and_culture_disable_local_keys` | [backend/test_deployment_keys.py:28](../backend/test_deployment_keys.py#L28) | 서버에서 명시적으로 비운 공공데이터/Naito 키를 개인 파일로 몰래 대체하지 않는다. |
| `DeploymentKeyTests.test_naito_environment_precedence` | [backend/test_deployment_keys.py:21](../backend/test_deployment_keys.py#L21) | 로컬 파일이 존재해도 서버 환경의 Naito 키/모델이 우선한다. |
| `DeploymentKeyTests.test_rest_environment_precedence` | [backend/test_deployment_keys.py:36](../backend/test_deployment_keys.py#L36) | 서버 REST 키가 있으면 개인 파일을 읽지 않는다. 공개 지도 설정과 혼동하지 않는다. |
| `describe` | [utils/scripts/catalog.py:69](../utils/scripts/catalog.py#L69) | Extract file overview, fingerprint, imports and symbol locations statically. |
| `describe.visit` | [utils/scripts/catalog.py:79](../utils/scripts/catalog.py#L79) | Walk definitions and keep qualified names for nested functions. |
| `detail_code` | [backend/contact.py:19](../backend/contact.py#L19) | 공식 상세 페이지 주소에서 행사 번호(cultcode)만 꺼내요. 다른 주소면 None. |
| `DialogueMemoryTests` | [backend/test_dialogue_memory.py:10](../backend/test_dialogue_memory.py#L10) | 외부 모델/공급자 없이 의미 계약과 실제 grounding 경계를 검사한다. |
| `DialogueMemoryTests.choice_state` | [backend/test_dialogue_memory.py:327](../backend/test_dialogue_memory.py#L327) | 현재 표시3개와 실제 서버결과를 가진 상태만 만든다. 클라이언트 후보는 받지 않는다. |
| `DialogueMemoryTests.envelope` | [backend/test_dialogue_memory.py:13](../backend/test_dialogue_memory.py#L13) | 현재 턴 원문 근거가 있는 실제 v3 모델 envelope를 만든다. |
| `DialogueMemoryTests.located` | [backend/test_dialogue_memory.py:23](../backend/test_dialogue_memory.py#L23) | 검증된 공개 예시 위치를 가진 상태를 만든다. |
| `DialogueMemoryTests.remember_question` | [backend/test_dialogue_memory.py:29](../backend/test_dialogue_memory.py#L29) | 서버 통합 계약대로 정책이 고른 질문을 기록한다. |
| `DialogueMemoryTests.test_changed_hard_condition_or_service_invalidates_choice_but_restore_does_not_trust_it` | [backend/test_dialogue_memory.py:405](../backend/test_dialogue_memory.py#L405) | 실제예산/활동변경은 현재선택·묶음을 비우며 복원된 snapshot을 새 실제선택으로 신뢰하지 않는다. |
| `DialogueMemoryTests.test_current_turn_evidence_and_optional_metadata` | [backend/test_dialogue_memory.py:85](../backend/test_dialogue_memory.py#L85) | 다른 턴 근거는 거절하되 선택 metadata/질문ID 오류가 유효 act를 지우지 않는다. |
| `DialogueMemoryTests.test_dates_optional_for_explore_required_only_for_visit` | [backend/test_dialogue_memory.py:158](../backend/test_dialogue_memory.py#L158) | 내용 탐색에 시간을 강요하지 않고 방문 모드에서만 일정 질문을 선택한다. |
| `DialogueMemoryTests.test_explicit_requirement_release_not_recreated` | [backend/test_dialogue_memory.py:190](../backend/test_dialogue_memory.py#L190) | ‘계단 없어도 괜찮아’라는 명시 완화는 같은 주제의 이전 필수조건만 해제한다. |
| `DialogueMemoryTests.test_explicit_visit_plan_proceed_mode` | [backend/test_dialogue_memory.py:278](../backend/test_dialogue_memory.py#L278) | 자연어 방문계획 요청만 visit로 전환하고 부족한 일정은 그 단계에서 질문한다. |
| `DialogueMemoryTests.test_fact_constraint_requires_current_semantic_evidence` | [backend/test_dialogue_memory.py:421](../backend/test_dialogue_memory.py#L421) | 무료/예산/접근성 실제 제약은 보존하되 의미 없는 modelhard 표지만으로 보류하지 않는다. |
| `DialogueMemoryTests.test_first_bare_place_is_a_lookup_candidate_not_a_verified_coordinate` | [backend/test_dialogue_memory.py:271](../backend/test_dialogue_memory.py#L271) | 질문 전 먼저 말한 지명도 조회하되 모델이 좌표를 확정하지 못한다. |
| `DialogueMemoryTests.test_generic_proceed_does_not_enter_or_keep_visit_mode` | [backend/test_dialogue_memory.py:287](../backend/test_dialogue_memory.py#L287) | 일반 검색은 explore이며 모델의 부당한 visit 제안과 날짜만의 모드변경을 막는다. |
| `DialogueMemoryTests.test_greeting_does_not_force_location_or_condition_form` | [backend/test_dialogue_memory.py:184](../backend/test_dialogue_memory.py#L184) | 인사를 조건변경 실패나 출발지 필수질문으로 만들지 않는다. |
| `DialogueMemoryTests.test_hard_free_survives_malformed_and_omitted_candidate` | [backend/test_dialogue_memory.py:108](../backend/test_dialogue_memory.py#L108) | 무료만 후보 손상/모델 누락 모두 유료 추천을 통과시키지 않는다. |
| `DialogueMemoryTests.test_hard_requirement_not_removed_by_unrelated_request` | [backend/test_dialogue_memory.py:120](../backend/test_dialogue_memory.py#L120) | 대상 밖 해제 표현이 기존 접근성 필수조건을 지우지 않는다. |
| `DialogueMemoryTests.test_invalid_category_cannot_cancel_good_mood` | [backend/test_dialogue_memory.py:66](../backend/test_dialogue_memory.py#L66) | 유효 취향과 잘못된 메뉴 후보를 섞어도 대화/실제 탐색을 유지한다. |
| `DialogueMemoryTests.test_invalid_replace_is_transactional` | [backend/test_dialogue_memory.py:97](../backend/test_dialogue_memory.py#L97) | 잘못된 교체 후보는 이전 선호를 먼저 지우지 않는다. |
| `DialogueMemoryTests.test_invalid_routing_hard_labels_do_not_create_constraint_holds` | [backend/test_dialogue_memory.py:315](../backend/test_dialogue_memory.py#L315) | 잘못된 활동/분류 후보의 hard표시가 유효한 영화 목적과 실제 조회를 막지 않는다. |
| `DialogueMemoryTests.test_invalid_visit_routing_candidate_is_not_a_hard_requirement` | [backend/test_dialogue_memory.py:302](../backend/test_dialogue_memory.py#L302) | 실모델 E20의 잘못된 course후보가 유효 방문전이를 필수조건 보류로 바꾸지 않는다. |
| `DialogueMemoryTests.test_music_does_not_expand_genres_but_explicit_genre_works` | [backend/test_dialogue_memory.py:76](../backend/test_dialogue_memory.py#L76) | 음악 분위기에서 장르3개를 생성하지 않으며 명시 국악은 실제 메뉴로 검증한다. |
| `DialogueMemoryTests.test_no_invented_duration_or_all_categories_default` | [backend/test_dialogue_memory.py:237](../backend/test_dialogue_memory.py#L237) | 일반 취향 원문을 인용해 임의 체류시간이나 전체 메뉴 기본값을 만들지 않는다. |
| `DialogueMemoryTests.test_number_and_unique_name_resolve_only_the_current_visible_batch` | [backend/test_dialogue_memory.py:336](../backend/test_dialogue_memory.py#L336) | 발화 조사를 포함한 번호는 화면3개에만 매핑하고 날짜·불명확 이름을 선택으로 추측하지 않는다. |
| `DialogueMemoryTests.test_origin_and_free_pending_order` | [backend/test_dialogue_memory.py:142](../backend/test_dialogue_memory.py#L142) | 검증된 새 위치 선택이 먼저 대기 중인 무료 변경을 덮어쓰지 않는다. |
| `DialogueMemoryTests.test_origin_answer_depends_on_question_target_not_phrasing` | [backend/test_dialogue_memory.py:227](../backend/test_dialogue_memory.py#L227) | 설명·반복 뒤 ‘출발’ 없는 질문에도 서울시청 단답의 의미가 유지된다. |
| `DialogueMemoryTests.test_origin_query_keeps_confirmed_coordinates_until_actual_choice_consent` | [backend/test_dialogue_memory.py:245](../backend/test_dialogue_memory.py#L245) | 새 지명 조회가 기존 확정 좌표를 지워 변경 동의를 우회하지 못한다. |
| `DialogueMemoryTests.test_reported_performance_explanation_and_mood` | [backend/test_dialogue_memory.py:37](../backend/test_dialogue_memory.py#L37) | 공연→무슨조건→잔잔한음악에서 변경질문/장르생성 없이 기존 질문과 취향을 보존한다. |
| `DialogueMemoryTests.test_restore_preserves_hard_without_importing_verified_coordinates` | [backend/test_dialogue_memory.py:172](../backend/test_dialogue_memory.py#L172) | 복원은 사용자 주장이고 도구사실/확정 플래그/좌표는 재검증 대상으로 돌린다. |
| `DialogueMemoryTests.test_restore_question_and_legacy_hard_requirements` | [backend/test_dialogue_memory.py:199](../backend/test_dialogue_memory.py#L199) | 복원 시 현재 질문과 구버전 필수조건도 남기며 GPS 좌표는 재사용하지 않는다. |
| `DialogueMemoryTests.test_same_verified_origin_alias_needs_no_lookup` | [backend/test_dialogue_memory.py:259](../backend/test_dialogue_memory.py#L259) | 이미 확인한 장소의 정확한 별칭은 좌표나 동의를 다시 요구하지 않는다. |
| `DialogueMemoryTests.test_schema_version_strict_and_explicit_goal_not_hard` | [backend/test_dialogue_memory.py:211](../backend/test_dialogue_memory.py#L211) | 불리언/실수 schema와 일반적인 ‘영화 꼭’ 목적을 필수 제약으로 바꾸는 것을 막는다. |
| `DialogueMemoryTests.test_selection_ignores_origin_display_metadata_but_not_coordinates_or_filters` | [backend/test_dialogue_memory.py:370](../backend/test_dialogue_memory.py#L370) | 원점주소 유무는 실제동일위치로 보되 좌표·날짜·필수조건 차이는 엄격하게 차단한다. |
| `DialogueMemoryTests.test_selection_requires_current_batch_real_fact_and_unchanged_conditions` | [backend/test_dialogue_memory.py:349](../backend/test_dialogue_memory.py#L349) | 과거묶음·다른결과·화면밖ID·필수변경대기·조작된조건으로 선택을 확정하지 못한다. |
| `DialogueMemoryTests.test_semantic_paraphrase_is_not_literal_word_gated` | [backend/test_dialogue_memory.py:58](../backend/test_dialogue_memory.py#L58) | 활동 이름 없는 의역도 모델의 근거 있는 의미를 수용한다. |
| `DialogueMemoryTests.test_service_change_keeps_common_constraints_and_is_order_independent` | [backend/test_dialogue_memory.py:129](../backend/test_dialogue_memory.py#L129) | 서비스 변경은 이전 분류만 무효화하며 새 취향과 공통 무료조건을 보존한다. |
| `DialogueMemoryTests.test_soft_unverified_preference_is_not_a_hard_hold` | [backend/test_dialogue_memory.py:220](../backend/test_dialogue_memory.py#L220) | 모델이 requirement영역에 넣어도 명시 soft 분위기는 검색 전체를 막지 않는다. |
| `DialogueMemoryTests.test_unclear_turn_retains_goal_batch_selection_and_does_not_search` | [backend/test_dialogue_memory.py:386](../backend/test_dialogue_memory.py#L386) | 모호한 발화는 기존목적/후보/선택을 보존하고 목적질문이나 자동재검색으로 돌아가지 않는다. |
| `DialogueMemoryTests.update` | [backend/test_dialogue_memory.py:18](../backend/test_dialogue_memory.py#L18) | 한 필드 후보를 만든다. 테스트에서 오류 항목만 명시적으로 바꾼다. |
| `distance_km` | [backend/outing.py:127](../backend/outing.py#L127) | 두 좌표의 대권거리(km)를 구한다. 보행·대중교통 이동시간을 뜻하지 않는다. |
| `distanceText` | [frontend/js/chat.js:1187](../frontend/js/chat.js#L1187) | JS/TS 정규식 후보; AST 검증 아님 |
| `doSave` | [frontend/js/place.js:127](../frontend/js/place.js#L127) | JS/TS 정규식 후보; AST 검증 아님 |
| `draft` | [backend/team_chat.js:157](../backend/team_chat.js#L157) | JS/TS 정규식 후보; AST 검증 아님 |
| `draw` | [frontend/js/place.js:196](../frontend/js/place.js#L196) | JS/TS 정규식 후보; AST 검증 아님 |
| `drawWave` | [backend/microphone_meter.js:94](../backend/microphone_meter.js#L94) | JS/TS 정규식 후보; AST 검증 아님 |
| `el` | [frontend/js/util.js:14](../frontend/js/util.js#L14) | JS/TS 정규식 후보; AST 검증 아님 |
| `empty` | [frontend/js/state.js:35](../frontend/js/state.js#L35) | JS/TS 정규식 후보; AST 검증 아님 |
| `endDemo` | [frontend/js/saved.js:38](../frontend/js/saved.js#L38) | JS/TS 정규식 후보; AST 검증 아님 |
| `endpoint` | [backend/agent_v3.py:34](../backend/agent_v3.py#L34) | Reuse the existing allowlisted provider address. |
| `endpoint` | [backend/naito_chat.py:28](../backend/naito_chat.py#L28) | 호출 주소 (허용된 세 곳 중 하나). |
| `EndpointTest` | [backend/test_naito_chat.py:145](../backend/test_naito_chat.py#L145) | 공급자별 요청 형식과 모의 응답의 공통 검증 경계를 확인한다. |
| `EndpointTest.test_invalid_envelope_and_truncated_replies_do_not_apply` | [backend/test_naito_chat.py:197](../backend/test_naito_chat.py#L197) | 공급자의 손상·절단 응답은 보류 성공으로 가장하지 않고 오류를 반환한다. |
| `EndpointTest.test_openai_request_and_response` | [backend/test_naito_chat.py:159](../backend/test_naito_chat.py#L159) | OpenAI 형식: Bearer 키, system+user 메시지, JSON 응답을 꺼내요. |
| `EndpointTest.test_provider_switch` | [backend/test_naito_chat.py:147](../backend/test_naito_chat.py#L147) | 설정한 제공자 주소로만 호출하고, 모르는 값이면 해커톤 주소. 키 모양으로 추측하지 않는다. |
| `EndpointTest.test_providers_reject_unspoken_place_and_preserve_valid_category` | [backend/test_naito_chat.py:174](../backend/test_naito_chat.py#L174) | 세 공급자에서 발화에 없는 출발지 후보만 보류하고 명확한 분류는 유지한다. |
| `ensureAgent` | [frontend/js/agent-session.js:49](../frontend/js/agent-session.js#L49) | JS/TS 정규식 후보; AST 검증 아님 |
| `entries` | [utils/scripts/catalog.py:113](../utils/scripts/catalog.py#L113) | Describe every active code file once; do not scan historical snapshots. |
| `envelope` | [frontend/js/agent-session.js:23](../frontend/js/agent-session.js#L23) | JS/TS 정규식 후보; AST 검증 아님 |
| `event_contact` | [backend/contact.py:41](../backend/contact.py#L41) | POST /preview/contact {url} → (status, body). body.phones: 문의 전화번호 목록. |
| `eventContact` | [frontend/js/api.js:168](../frontend/js/api.js#L168) | JS/TS 정규식 후보; AST 검증 아님 |
| `expected` | [utils/scripts/context.py:42](../utils/scripts/context.py#L42) | Read the configured public state file and generate the brief. |
| `ExplorationTests` | [backend/test_exploration.py:21](../backend/test_exploration.py#L21) | 추천의 필수 일정 없이 콘텐츠를 찾되 hard 조건과 source 사실 경계를 유지한다. |
| `ExplorationTests.preference` | [backend/test_exploration.py:44](../backend/test_exploration.py#L44) | 실제 의미 모듈의 명시 선호 계약을 만든다. |
| `ExplorationTests.setUp` | [backend/test_exploration.py:24](../backend/test_exploration.py#L24) | 저장된 실제 공급자 필드 형태를 복사하고 평가용 내용·ID를 명시적으로 구성한다. |
| `ExplorationTests.source` | [backend/test_exploration.py:40](../backend/test_exploration.py#L40) | 네트워크 없이 원본 공급자의 (rows, checked_at, total) 계약을 재현한다. |
| `ExplorationTests.test_calm_lively_change_order_with_actual_description_evidence` | [backend/test_exploration.py:231](../backend/test_exploration.py#L231) | 서로 구분되는 실제 소개 근거가 있으면 분위기 변경이 같은 후보의 순서를 바꾼다. |
| `ExplorationTests.test_calm_lively_change_order_with_actual_description_evidence.ranker` | [backend/test_exploration.py:233](../backend/test_exploration.py#L233) | 명시 fixture 원문의 분위기를 비교하는 독립 모의 의미 판정기다. |
| `ExplorationTests.test_conflicting_date_is_not_silently_reinterpreted` | [backend/test_exploration.py:401](../backend/test_exploration.py#L401) | 서로 다른 명시 날짜와 시각을 한 방문 일정처럼 섞어 조회하지 않는다. |
| `ExplorationTests.test_contradictory_free_and_partial_fee_is_unknown` | [backend/test_exploration.py:293](../backend/test_exploration.py#L293) | 공식 무료 태그가 있어도 일부유료·복수요금 설명과 충돌하면 hard 무료로 통과하지 않는다. |
| `ExplorationTests.test_explicit_closer_sort_uses_actual_distance_before_semantic_preference` | [backend/test_exploration.py:174](../backend/test_exploration.py#L174) | 더 가까운 곳은 직선거리를 우선하며 기존 무료조건·취향과 사실 근거를 보존한다. |
| `ExplorationTests.test_hard_price_and_negation_do_not_relax_for_zero` | [backend/test_exploration.py:277](../backend/test_exploration.py#L277) | 무료만·국악 제외는 실제 요금과 분류로 적용하며 미확인/유료를 복원하지 않는다. |
| `ExplorationTests.test_invalid_user_coordinate_and_date_are_not_provider_zero` | [backend/test_exploration.py:368](../backend/test_exploration.py#L368) | 잘못된 사용자 좌표/날짜는 InputError로 식별하고 source 조회 전에 중단한다. |
| `ExplorationTests.test_missing_ranking_or_error_keeps_facts_without_match_claim` | [backend/test_exploration.py:264](../backend/test_exploration.py#L264) | 분위기 근거 판정이 없거나 실패해도 실제 콘텐츠는 보존하고 맞춤 성공을 주장하지 않는다. |
| `ExplorationTests.test_movie_unknown_hard_price_or_date_cannot_pass` | [backend/test_exploration.py:358](../backend/test_exploration.py#L358) | 영화관 자료로 알 수 없는 요금·영업일을 필수 조건 충족으로 간주하지 않는다. |
| `ExplorationTests.test_movie_venue_cannot_claim_showtimes_or_taste_match` | [backend/test_exploration.py:340](../backend/test_exploration.py#L340) | 실제 영화관 위치·직선거리만 표시하고 작품 취향 정렬 callback을 호출하지 않는다. |
| `ExplorationTests.test_no_required_date_or_fabricated_window` | [backend/test_exploration.py:205](../backend/test_exploration.py#L205) | 종료시각·장르 없이 진행/예정 콘텐츠를 찾고 오늘 방문 시간창을 만들지 않는다. |
| `ExplorationTests.test_other_service_hard_preference_does_not_block_current_goal` | [backend/test_exploration.py:379](../backend/test_exploration.py#L379) | 다른 서비스에 종속된 hard 취향은 현재 공연 탐색을 전역 차단하지 않는다. |
| `ExplorationTests.test_performance_does_not_substitute_exhibition_or_venue` | [backend/test_exploration.py:222](../backend/test_exploration.py#L222) | 공연 요청은 실제 공연 행사만 반환하고 전시/시설로 성공을 가장하지 않는다. |
| `ExplorationTests.test_restored_hard_preference_is_not_downgraded_to_soft` | [backend/test_exploration.py:191](../backend/test_exploration.py#L191) | 복원 뒤에도 검증할 수 없는 필수 취향은 유지하며 조회로 조용히 우회하지 않는다. |
| `ExplorationTests.test_selected_date_and_short_window_are_filters_not_visit_approval` | [backend/test_exploration.py:320](../backend/test_exploration.py#L320) | 명시한 30분 구간도 탐색 필터로만 쓰며 60분 방문계획이나 방문검증으로 승격하지 않는다. |
| `ExplorationTests.test_source_zero_and_source_error_are_distinct` | [backend/test_exploration.py:330](../backend/test_exploration.py#L330) | 정상 공급자 0건과 장애를 구분하고 다른 종류의 시설을 몰래 반환하지 않는다. |
| `ExplorationTests.test_structured_hard_genre_exclusion_is_not_blocked_twice` | [backend/test_exploration.py:311](../backend/test_exploration.py#L311) | 실제 exclude_terms에 연결된 장르 제외는 unsupported로 중복 보류하지 않는다. |
| `ExplorationTests.test_unresolved_hard_requirement_prevents_source` | [backend/test_exploration.py:302](../backend/test_exploration.py#L302) | 검증 불가 필수 제약은 source 조회 전 차단하고 입력을 지우지 않는다. |
| `ExplorationTests.test_unverified_quote_id_and_mutation_cannot_change_facts` | [backend/test_exploration.py:250](../backend/test_exploration.py#L250) | 존재하지 않는 인용·후보 ID를 무시하고 ranker의 객체 수정도 원본 사실에 반영하지 않는다. |
| `ExplorationTests.test_unverified_quote_id_and_mutation_cannot_change_facts.ranker` | [backend/test_exploration.py:252](../backend/test_exploration.py#L252) | 의도적으로 사실 변조와 없는 인용을 시도하는 판정기다. |
| `ExplorationTests.test_walk_all_amenities_returns_zero_without_inventing_parent_park` | [backend/test_exploration.py:118](../backend/test_exploration.py#L118) | 부대시설뿐이면 부모 공원 ID/좌표를 만들거나 결과 개수를 채우지 않는다. |
| `ExplorationTests.test_walk_broad_group_and_missing_categories_never_claim_matching` | [backend/test_exploration.py:102](../backend/test_exploration.py#L102) | 관광명소AT4·공원 이름만으로 승인하지 않고 결측/다른용도를 역할별 집계한다. |
| `ExplorationTests.test_walk_eligibility_does_not_relax_price_or_unverified_hard_requirement` | [backend/test_exploration.py:142](../backend/test_exploration.py#L142) | 공원 적합성 통과 뒤에도 확인되지 않은 무료필수조건과 실제 hard 보류를 유지한다. |
| `ExplorationTests.test_walk_filter_does_not_change_movie_cafe_or_food_behavior` | [backend/test_exploration.py:159](../backend/test_exploration.py#L159) | 이번 산책 판정은 기존 영화관/카페/식사 조회와 원 ID·좌표를 바꾸지 않는다. |
| `ExplorationTests.test_walk_name_does_not_override_primary_or_amenity_category` | [backend/test_exploration.py:89](../backend/test_exploration.py#L89) | 정상 공원 명칭의 화장실 단어는 허용하고 이름만 공원인 부대시설은 제외한다. |
| `ExplorationTests.test_walk_nearby_amenities_cannot_outrank_two_real_destinations` | [backend/test_exploration.py:67](../backend/test_exploration.py#L67) | 거리·관심어 점수가 높은 화장실/주차장/관리소를 빼고 정상 공원2건만 반환한다. |
| `ExplorationTests.test_walk_pk6_conflict_is_not_rescued_by_park_category` | [backend/test_exploration.py:132](../backend/test_exploration.py#L132) | 상세분류가공원이어도 실제주차장그룹과충돌하면 주 목적지로 승인하지 않는다. |
| `ExplorationTests.test_zero_budget_is_applied_and_ranker_receives_source_hash` | [backend/test_exploration.py:387](../backend/test_exploration.py#L387) | 0원 예산도 명시 필터로 기록하고 의미 판정에 실제 출처 hash를 함께 제공한다. |
| `ExplorationTests.test_zero_budget_is_applied_and_ranker_receives_source_hash.ranker` | [backend/test_exploration.py:391](../backend/test_exploration.py#L391) | 선택 정렬 캐시가 쓸 source hash와 실제 필드의 일치를 검사한다. |
| `ExplorationTests.venue_source` | [backend/test_exploration.py:61](../backend/test_exploration.py#L61) | 실카카오 호출 없이 기존 거리순 첫5건 경계의 반환만 고정한다. |
| `ExplorationTests.walk_place` | [backend/test_exploration.py:55](../backend/test_exploration.py#L55) | 실제 공개 장소가 아닌 합성 카카오 정규화 후보를 만든다. |
| `ExplorationTests.walk_state` | [backend/test_exploration.py:49](../backend/test_exploration.py#L49) | 문화행사 fixture와 격리된 산책 목적·검증 원점을 준비한다. |
| `explore` | [backend/exploration.py:394](../backend/exploration.py#L394) | 실제 탐색 결과와 적용/미적용 근거를 반환한다. InputError 외 조회장애는 source_error다. |
| `extract_conditions` | [backend/naito_chat.py:71](../backend/naito_chat.py#L71) | 공식 사용자 제공 주소로 1회 호출한다. 좌표는 보내지 않고 응답 최대64KiB/20초로 제한한다. |
| `fallback` | [frontend/js/util.js:158](../frontend/js/util.js#L158) | JS/TS 정규식 후보; AST 검증 아님 |
| `file_hash` | [utils/scripts/reuse.py:33](../utils/scripts/reuse.py#L33) | Hash file contents in chunks without logging their values. |
| `file_overview` | [utils/scripts/catalog.py:138](../utils/scripts/catalog.py#L138) | Describe a file using only its static overview, heading, or file type. |
| `file_voice_available` | [backend/local_voice.py:25](../backend/local_voice.py#L25) | Windows 파일 합성 지원 여부만 반환한다. 음성 설치·합성 성공은 별도 검증한다. |
| `fill` | [frontend/js/app.js:192](../frontend/js/app.js#L192) | JS/TS 정규식 후보; AST 검증 아님 |
| `findStart` | [frontend/js/chat.js:994](../frontend/js/chat.js#L994) | JS/TS 정규식 후보; AST 검증 아님 |
| `finish` | [backend/voice_session.js:102](../backend/voice_session.js#L102) | JS/TS 정규식 후보; AST 검증 아님 |
| `finish` | [backend/voice_session.js:12](../backend/voice_session.js#L12) | JS/TS 정규식 후보; AST 검증 아님 |
| `finish` | [frontend/js/chat.js:433](../frontend/js/chat.js#L433) | JS/TS 정규식 후보; AST 검증 아님 |
| `FixedDatetime` | [backend/test_exploration.py:12](../backend/test_exploration.py#L12) | 기간 평가의 시스템 기준일을 고정한다. 사용자의 방문일을 대신하지 않는다. |
| `FixedDatetime.now` | [backend/test_exploration.py:16](../backend/test_exploration.py#L16) | 2026-11-01 한국 시각을 반환한다. |
| `FixturePreview` | [utils/scripts/agent_v3_http_fixture.py:156](../utils/scripts/agent_v3_http_fixture.py#L156) | 제품 handler를 사용하고 테스트 관측 정보만 별도 GET으로 노출한다. |
| `FixturePreview.do_GET` | [utils/scripts/agent_v3_http_fixture.py:162](../utils/scripts/agent_v3_http_fixture.py#L162) | 관측 이외 GET은 실제 Preview로 전달한다. |
| `FixturePreview.log_message` | [utils/scripts/agent_v3_http_fixture.py:159](../utils/scripts/agent_v3_http_fixture.py#L159) | 테스트 원문/접근 로그를 저장하지 않는다. |
| `flat` | [frontend/js/chat.js:507](../frontend/js/chat.js#L507) | JS/TS 정규식 후보; AST 검증 아님 |
| `flat` | [frontend/js/chat.js:531](../frontend/js/chat.js#L531) | JS/TS 정규식 후보; AST 검증 아님 |
| `fmtMin` | [frontend/js/place.js:304](../frontend/js/place.js#L304) | JS/TS 정규식 후보; AST 검증 아님 |
| `forkConversation` | [frontend/js/state.js:86](../frontend/js/state.js#L86) | JS/TS 정규식 후보; AST 검증 아님 |
| `forkListener` | [frontend/js/agent-session.js:11](../frontend/js/agent-session.js#L11) | JS/TS 정규식 후보; AST 검증 아님 |
| `formatDate` | [frontend/js/util.js:42](../frontend/js/util.js#L42) | JS/TS 정규식 후보; AST 검증 아님 |
| `formatTime` | [frontend/js/util.js:49](../frontend/js/util.js#L49) | JS/TS 정규식 후보; AST 검증 아님 |
| `fromServerDraft` | [frontend/js/chat.js:738](../frontend/js/chat.js#L738) | JS/TS 정규식 후보; AST 검증 아님 |
| `generated_paths` | [utils/scripts/catalog.py:150](../utils/scripts/catalog.py#L150) | Return the actual output paths, independent of optional configuration hints. |
| `getEngine` | [frontend/js/place.js:177](../frontend/js/place.js#L177) | JS/TS 정규식 후보; AST 검증 아님 |
| `greetingFor` | [frontend/js/weather.js:29](../frontend/js/weather.js#L29) | JS/TS 정규식 후보; AST 검증 아님 |
| `ground_payload` | [backend/chat_grounding.py:441](../backend/chat_grounding.py#L441) | 원문 근거·형식·검증 가능한 시각을 검사하고 차단된 필드를 분리한다. |
| `GroundedProposal` | [backend/chat_grounding.py:71](../backend/chat_grounding.py#L71) | 조건 후보와 별도로 보류된 필드명만 보관한다. 사용자 원문은 저장하지 않는다. |
| `GroundedProposal.__init__` | [backend/chat_grounding.py:74](../backend/chat_grounding.py#L74) | 호출자 데이터를 복사하고 보류 필드를 고정한다. |
| `GroundingTests` | [backend/test_chat_grounding.py:9](../backend/test_chat_grounding.py#L9) | 명시되지 않은 조건이나 모호한 시간은 이전 조건을 바꾸지 않는다. |
| `GroundingTests.check` | [backend/test_chat_grounding.py:12](../backend/test_chat_grounding.py#L12) | 고정된 한국 기준 시각으로 해석 결과를 검증한다. |
| `GroundingTests.test_admission_budget_amount_and_scope` | [backend/test_chat_grounding.py:160](../backend/test_chat_grounding.py#L160) | 관람료와 명시된 원화 금액이 일치해야 예산을 변경한다. |
| `GroundingTests.test_ambiguous_clock_and_choice_question` | [backend/test_chat_grounding.py:39](../backend/test_chat_grounding.py#L39) | 질문에 오전과 오후가 모두 있어도 짧은 시간 답을 임의 확정하지 않는다. |
| `GroundingTests.test_change_target_and_explicit_range` | [backend/test_chat_grounding.py:51](../backend/test_chat_grounding.py#L51) | 바꿀 대상이 없으면 보류하고 명시된 시간 범위의 양끝을 각각 대조한다. |
| `GroundingTests.test_departure_and_destination_are_distinct` | [backend/test_chat_grounding.py:126](../backend/test_chat_grounding.py#L126) | 목적지와 출발지를 혼동하지 않고 짧은 출발지 답도 수용한다. |
| `GroundingTests.test_departure_prohibition_correction_and_short_answer` | [backend/test_chat_grounding.py:267](../backend/test_chat_grounding.py#L267) | 출발 금지의 활용형·짧은 부정 답변을 막고 정정된 출발지는 수용한다. |
| `GroundingTests.test_draft_date_and_date_only_preserve_time` | [backend/test_chat_grounding.py:99](../backend/test_chat_grounding.py#L99) | 초안 날짜와 명시된 시각, 날짜만 변경 시 기존 시각 보존을 허용한다. |
| `GroundingTests.test_excluded_places_need_explicit_release` | [backend/test_chat_grounding.py:229](../backend/test_chat_grounding.py#L229) | 제외 목록을 명시적 해제 없이 지우지 않고 항목별 해제는 보존한다. |
| `GroundingTests.test_exclusion_addition_needs_exclusion_not_just_mention` | [backend/test_chat_grounding.py:319](../backend/test_chat_grounding.py#L319) | 제외 금지나 평범한 장소 언급으로 새 제외를 만들지 않는다. |
| `GroundingTests.test_explicit_date_and_time_verify_values` | [backend/test_chat_grounding.py:28](../backend/test_chat_grounding.py#L28) | 오후 두 시와 날짜는 각각 실제 14시·내일과 일치해야 한다. |
| `GroundingTests.test_free_inflected_negation_and_allowed_paid_options` | [backend/test_chat_grounding.py:251](../backend/test_chat_grounding.py#L251) | 무료의 활용형 부정과 유료 허용을 구분하고 정상 무료 요청은 유지한다. |
| `GroundingTests.test_free_preference_requires_matching_intent` | [backend/test_chat_grounding.py:140](../backend/test_chat_grounding.py#L140) | 무료 조건을 반대로 바꾸지 않고 명확한 해제를 처리한다. |
| `GroundingTests.test_indoor_outdoor_opposites_corrections_and_release` | [backend/test_chat_grounding.py:297](../backend/test_chat_grounding.py#L297) | 반대 실내외 값과 의미 없는 해제는 막고 명시 선호·정정·해제를 수용한다. |
| `GroundingTests.test_keywords_keep_unmentioned_preferences_and_explicit_clear` | [backend/test_chat_grounding.py:279](../backend/test_chat_grounding.py#L279) | 무관한 답변은 기존 관심어를 지우지 않고 개별 정정과 전체 해제는 허용한다. |
| `GroundingTests.test_malformed_envelope_and_unknown_field_fail` | [backend/test_chat_grounding.py:119](../backend/test_chat_grounding.py#L119) | 상위 스키마 오류와 사실 필드는 실패로 처리한다. |
| `GroundingTests.test_minimum_price_is_not_maximum_budget` | [backend/test_chat_grounding.py:222](../backend/test_chat_grounding.py#L222) | 이상·초과 같은 하한을 관람료 상한으로 변환하지 않는다. |
| `GroundingTests.test_music_group_rejection_does_not_become_music_categories` | [backend/test_chat_grounding.py:331](../backend/test_chat_grounding.py#L331) | 음악 전체의 거절을 국악·클래식·콘서트 선호로 바꾸지 않는다. |
| `GroundingTests.test_negated_category_and_unrelated_time_quote` | [backend/test_chat_grounding.py:87](../backend/test_chat_grounding.py#L87) | 명시적으로 거부한 분류와 시각이 빠진 인용은 수용하지 않는다. |
| `GroundingTests.test_negation_cannot_invert_free_or_time` | [backend/test_chat_grounding.py:203](../backend/test_chat_grounding.py#L203) | 부정된 무료·유료와 시각을 반대로 확정하지 않는다. |
| `GroundingTests.test_night_twelve_does_not_become_noon` | [backend/test_chat_grounding.py:193](../backend/test_chat_grounding.py#L193) | 밤 12시의 날짜 경계는 낮 12시로 자동 확정하지 않는다. |
| `GroundingTests.test_no_invented_place_and_literal_quote` | [backend/test_chat_grounding.py:17](../backend/test_chat_grounding.py#L17) | 발화에 없는 장소 및 실제 발화에 없는 인용을 보류한다. |
| `GroundingTests.test_only_bad_time_is_blocked` | [backend/test_chat_grounding.py:66](../backend/test_chat_grounding.py#L66) | 명확한 분류는 보존하면서 서로 다른 잘못된 시각만 보류한다. |
| `GroundingTests.test_place_and_course_counts_cannot_be_inverted` | [backend/test_chat_grounding.py:344](../backend/test_chat_grounding.py#L344) | 한 곳과 코스를 뒤집지 않고 명확한 정정과 질문 뒤의 짧은 답변은 수용한다. |
| `GroundingTests.test_rejected_departure_does_not_become_origin` | [backend/test_chat_grounding.py:216](../backend/test_chat_grounding.py#L216) | 출발하지 않는 장소와 명시적으로 출발하는 장소를 구분한다. |
| `GroundingTests.test_relative_and_unsupported_dates_are_held` | [backend/test_chat_grounding.py:111](../backend/test_chat_grounding.py#L111) | 상대 지연이나 요일을 모델이 임의 시각으로 바꾸면 보류한다. |
| `GroundingTests.test_required_condition_negated_release_is_not_release` | [backend/test_chat_grounding.py:243](../backend/test_chat_grounding.py#L243) | 필수조건을 빼지 말라는 발화는 조건 해제가 아니다. |
| `GroundingTests.test_required_conditions_not_silently_removed` | [backend/test_chat_grounding.py:174](../backend/test_chat_grounding.py#L174) | 기존 필수조건을 보존하고 명시된 조건만 해제한다. |
| `GroundingTests.test_time_correction_is_held` | [backend/test_chat_grounding.py:81](../backend/test_chat_grounding.py#L81) | 정정 문장에 시각이 여러 개면 최종 의도를 임의로 해석하지 않는다. |
| `GroundingTests.test_time_period_is_not_inherited_from_previous_clock` | [backend/test_chat_grounding.py:74](../backend/test_chat_grounding.py#L74) | 오전 11시에서 1시로 가는 범위는 정오 전후가 불명확하다. |
| `handle` | [frontend/js/chat.js:852](../frontend/js/chat.js#L852) | JS/TS 정규식 후보; AST 검증 아님 |
| `handleAction` | [backend/team_chat.js:220](../backend/team_chat.js#L220) | JS/TS 정규식 후보; AST 검증 아님 |
| `Handler` | [frontend/dev_server.py:19](../frontend/dev_server.py#L19) | 정적 파일은 그대로, /preview/ 로 시작하는 POST 는 백엔드로 전달해요. |
| `Handler.do_POST` | [frontend/dev_server.py:22](../frontend/dev_server.py#L22) | 백엔드 응답의 상태 코드와 본문을 바꾸지 않고 돌려줘요. |
| `hhmm` | [frontend/js/util.js:33](../frontend/js/util.js#L33) | JS/TS 정규식 후보; AST 검증 아님 |
| `icon` | [frontend/js/place.js:214](../frontend/js/place.js#L214) | JS/TS 정규식 후보; AST 검증 아님 |
| `inGroup` | [frontend/js/chat.js:30](../frontend/js/chat.js#L30) | JS/TS 정규식 후보; AST 검증 아님 |
| `initChat` | [frontend/js/chat.js:1297](../frontend/js/chat.js#L1297) | JS/TS 정규식 후보; AST 검증 아님 |
| `initCulture` | [backend/team_culture.js:11](../backend/team_culture.js#L11) | JS/TS 정규식 후보; AST 검증 아님 |
| `initLanding` | [frontend/js/app.js:98](../frontend/js/app.js#L98) | JS/TS 정규식 후보; AST 검증 아님 |
| `initMe` | [frontend/js/app.js:248](../frontend/js/app.js#L248) | JS/TS 정규식 후보; AST 검증 아님 |
| `initNavigation` | [frontend/js/app.js:268](../frontend/js/app.js#L268) | JS/TS 정규식 후보; AST 검증 아님 |
| `initNotify` | [frontend/js/app.js:198](../frontend/js/app.js#L198) | JS/TS 정규식 후보; AST 검증 아님 |
| `initPlace` | [frontend/js/place.js:375](../frontend/js/place.js#L375) | JS/TS 정규식 후보; AST 검증 아님 |
| `InputError` | [backend/outing.py:20](../backend/outing.py#L20) | 추천 입력 오류의 공개 코드·필드·안내문을 담는다. 원본 입력값은 포함하지 않는다. |
| `InputError.__init__` | [backend/outing.py:23](../backend/outing.py#L23) | HTTP 오류 응답과 필드별 안내에 사용할 고정 메타데이터를 보관한다. |
| `inspectVoiceEnvironment` | [backend/team_chat.js:91](../backend/team_chat.js#L91) | JS/TS 정규식 후보; AST 검증 아님 |
| `integrate_index` | [utils/scripts/prepare_chat_handoff.py:17](../utils/scripts/prepare_chat_handoff.py#L17) | 원본 HTML에 모듈을 한 번만 연결한다. 이미 연결되거나 구조가 다르면 거절한다. |
| `integrate_results` | [utils/scripts/prepare_chat_handoff.py:38](../utils/scripts/prepare_chat_handoff.py#L38) | 추천·상세의 출처 표시만 확장하며 같은 후보 ID/지도/카드 흐름을 유지한다. |
| `integrate_search` | [utils/scripts/prepare_chat_handoff.py:24](../utils/scripts/prepare_chat_handoff.py#L24) | 확정 요청과 S02a 요약의 두 지점만 확장한다. 다른 팀 변경을 추측해 덮어쓰지 않는다. |
| `interpret` | [backend/dialogue_memory.py:339](../backend/dialogue_memory.py#L339) | v3 envelope를 항목별 검증해 새 상태로 반환한다. 전체 무효만 ValueError다. |
| `interpret` | [frontend/js/chat.js:769](../frontend/js/chat.js#L769) | JS/TS 정규식 후보; AST 검증 아님 |
| `invalidate` | [backend/team_chat.js:373](../backend/team_chat.js#L373) | JS/TS 정규식 후보; AST 검증 아님 |
| `isDebug` | [frontend/js/util.js:90](../frontend/js/util.js#L90) | JS/TS 정규식 후보; AST 검증 아님 |
| `isEcho` | [frontend/js/chat.js:528](../frontend/js/chat.js#L528) | JS/TS 정규식 후보; AST 검증 아님 |
| `isSaved` | [frontend/js/saved.js:16](../frontend/js/saved.js#L16) | JS/TS 정규식 후보; AST 검증 아님 |
| `isSignedIn` | [frontend/js/saved.js:8](../frontend/js/saved.js#L8) | JS/TS 정규식 후보; AST 검증 아님 |
| `isTest` | [frontend/js/util.js:86](../frontend/js/util.js#L86) | JS/TS 정규식 후보; AST 검증 아님 |
| `joinResults` | [frontend/js/chat.js:504](../frontend/js/chat.js#L504) | JS/TS 정규식 후보; AST 검증 아님 |
| `josa` | [frontend/js/chat.js:63](../frontend/js/chat.js#L63) | JS/TS 정규식 후보; AST 검증 아님 |
| `known_price` | [backend/preferences.py:39](../backend/preferences.py#L39) | 공식 무료 표시 또는 단일 원화 가격만 판독한다. 할인/복수 좌석/범위는 미확인이다. |
| `lastQuestion` | [frontend/js/chat.js:950](../frontend/js/chat.js#L950) | JS/TS 정규식 후보; AST 검증 아님 |
| `list` | [frontend/js/chat.js:1168](../frontend/js/chat.js#L1168) | JS/TS 정규식 후보; AST 검증 아님 |
| `listen` | [backend/voice_session.js:162](../backend/voice_session.js#L162) | JS/TS 정규식 후보; AST 검증 아님 |
| `listen` | [frontend/js/chat.js:557](../frontend/js/chat.js#L557) | JS/TS 정규식 후보; AST 검증 아님 |
| `listenForReply` | [backend/voice_session.js:4](../backend/voice_session.js#L4) | JS/TS 정규식 후보; AST 검증 아님 |
| `liveBubble` | [frontend/js/chat.js:394](../frontend/js/chat.js#L394) | JS/TS 정규식 후보; AST 검증 아님 |
| `ll` | [backend/map_view.js:53](../backend/map_view.js#L53) | JS/TS 정규식 후보; AST 검증 아님 |
| `load` | [backend/map_view.js:22](../backend/map_view.js#L22) | JS/TS 정규식 후보; AST 검증 아님 |
| `load` | [frontend/js/state.js:57](../frontend/js/state.js#L57) | JS/TS 정규식 후보; AST 검증 아님 |
| `loadKakao` | [frontend/js/place.js:159](../frontend/js/place.js#L159) | JS/TS 정규식 후보; AST 검증 아님 |
| `loadTransit` | [frontend/js/place.js:328](../frontend/js/place.js#L328) | JS/TS 정규식 후보; AST 검증 아님 |
| `loadWalk` | [frontend/js/place.js:276](../frontend/js/place.js#L276) | JS/TS 정규식 후보; AST 검증 아님 |
| `localId` | [frontend/js/state.js:15](../frontend/js/state.js#L15) | JS/TS 정규식 후보; AST 검증 아님 |
| `logVoice` | [backend/team_chat.js:74](../backend/team_chat.js#L74) | JS/TS 정규식 후보; AST 검증 아님 |
| `longEnough` | [frontend/js/parse.js:94](../frontend/js/parse.js#L94) | JS/TS 정규식 후보; AST 검증 아님 |
| `main` | [utils/scripts/agent_http_fixture.py:73](../utils/scripts/agent_http_fixture.py#L73) | 허용 origin의 loopback 서버를 시작하고 부모의 stdin 종료 요청 후 정리한다. |
| `main` | [utils/scripts/agent_v3_http_fixture.py:170](../utils/scripts/agent_v3_http_fixture.py#L170) | 격리 loopback fixture를 시작하고 부모 stdin이 닫히면 모든 테스트 자원을 정리한다. |
| `main` | [utils/scripts/catalog.py:232](../utils/scripts/catalog.py#L232) | Write, validate, or search the catalog with bounded console output. |
| `main` | [utils/scripts/check_chat_api.py:35](../utils/scripts/check_chat_api.py#L35) | 외부 키 사용 없이 4개 HTTP 구간을 검사하고 임시 서버를 반드시 종료한다. |
| `main` | [utils/scripts/check_chat_live.py:18](../utils/scripts/check_chat_live.py#L18) | 국악·장소/시간·확정 시간 변경을 1회씩 호출하고 사실 경계와 충돌 보존을 검사한다. |
| `main` | [utils/scripts/check_conversation_edges.py:19](../utils/scripts/check_conversation_edges.py#L19) | 독립 예산·제외·제약·시간 시나리오를 실행하고 조건 유지/해제를 명시적으로 검사한다. |
| `main` | [utils/scripts/check_culture_sources.py:30](../utils/scripts/check_culture_sources.py#L30) | 서울시 실제 조회와 TourAPI 설정/실조회를 명확히 나누어 결과를 저장한다. |
| `main` | [utils/scripts/check_service_keys.py:16](../utils/scripts/check_service_keys.py#L16) | 공개 청량리역 조건으로 서비스별 결과를 요약한다. HTTP200과 실제 기능 성공을 구분한다. |
| `main` | [utils/scripts/check_transit_details.py:15](../utils/scripts/check_transit_details.py#L15) | 고정 청량리역→서울돈화문국악당 구간을 실조회하고 확인된 공개 경로 필드만 기록한다. |
| `main` | [utils/scripts/commit_report.py:52](../utils/scripts/commit_report.py#L52) | Check by default; stage and commit only when --commit is explicitly given. |
| `main` | [utils/scripts/context.py:48](../utils/scripts/context.py#L48) | Write, check, or print only the short restart brief. |
| `main` | [utils/scripts/harness.py:88](../utils/scripts/harness.py#L88) | Run the harness once; fixing failures requires a separately scoped change. |
| `main` | [utils/scripts/loop.py:40](../utils/scripts/loop.py#L40) | Persist only task evidence; never run shell, LLM, network or Git writes. |
| `main` | [utils/scripts/prepare_chat_handoff.py:124](../utils/scripts/prepare_chat_handoff.py#L124) | 명시한 로컬 Git ref로 인계 산출물을 생성한다. 네트워크/push/checkout/merge는 하지 않는다. |
| `main` | [utils/scripts/read_pdf.py:33](../utils/scripts/read_pdf.py#L33) | Extract page-delimited local evidence and display masked page text. |
| `main` | [utils/scripts/reuse.py:77](../utils/scripts/reuse.py#L77) | Compare two files or copy an explicitly selected local Git snapshot. |
| `main` | [utils/scripts/team_chat_preview.py:35](../utils/scripts/team_chat_preview.py#L35) | 루프백에만 서버를 띄워 팀 HTML과 기존 API 프록시에 독립 모듈을 붙인다. |
| `main` | [utils/scripts/verify_watch.py:32](../utils/scripts/verify_watch.py#L32) | Verify creation, symbol/overview changes and deletion; clean our probe. |
| `main` | [utils/scripts/watch.py:39](../utils/scripts/watch.py#L39) | Watch in a cooperative single-process loop; retain errors in local status. |
| `main.Handler` | [utils/scripts/team_chat_preview.py:46](../utils/scripts/team_chat_preview.py#L46) | 팀 프록시/정적 서빙을 유지하고 index와 채팅 모듈 두 경로만 추가한다. |
| `main.Handler.do_GET` | [utils/scripts/team_chat_preview.py:49](../utils/scripts/team_chat_preview.py#L49) | 원본 HTML을 디스크에 수정하지 않고 모듈 script를 응답에만 추가한다. |
| `main.run` | [utils/scripts/check_conversation_edges.py:31](../utils/scripts/check_conversation_edges.py#L31) | 변경된 초안과 결과를 기록한다. 실패 원문은 정규화된 시험 응답만 남긴다. |
| `map_config` | [backend/map_config.py:9](../backend/map_config.py#L9) | 환경변수 우선으로 JS 키를 반환한다. 미설정은 기존 지도를 유지하며 값은 로그하지 않는다. |
| `map_reply` | [utils/scripts/agent_v3_http_fixture.py:98](../utils/scripts/agent_v3_http_fixture.py#L98) | 카카오 원본 문서 형태를 반환해 실제 장소 정규화/거리 계산을 거치게 한다. |
| `mapConfig` | [frontend/js/api.js:141](../frontend/js/api.js#L141) | JS/TS 정규식 후보; AST 검증 아님 |
| `MapConfigTests` | [backend/test_map_config.py:8](../backend/test_map_config.py#L8) | 실제 로컬 키를 읽지 않고 환경·파일 우선순위와 공개 범위를 점검한다. |
| `MapConfigTests.test_file_or_missing_key` | [backend/test_map_config.py:18](../backend/test_map_config.py#L18) | BOM 허용 파일의 정확한 변수만 읽고 미설정·부적절한 값은 기본 지도로 남긴다. |
| `MapConfigTests.test_key_priority_and_public_scope` | [backend/test_map_config.py:11](../backend/test_map_config.py#L11) | 환경변수의 JS 키만 공개하고 REST 키나 로컬 파일은 조회하지 않는다. |
| `markdown_files` | [utils/scripts/harness.py:39](../utils/scripts/harness.py#L39) | Select active documentation, excluding copied PRDs and historical snapshots. |
| `measure` | [backend/microphone_meter.js:34](../backend/microphone_meter.js#L34) | JS/TS 정규식 후보; AST 검증 아님 |
| `meNote` | [frontend/js/app.js:264](../frontend/js/app.js#L264) | JS/TS 정규식 후보; AST 검증 아님 |
| `merge` | [frontend/js/chat.js:505](../frontend/js/chat.js#L505) | JS/TS 정규식 후보; AST 검증 아님 |
| `metric` | [backend/transit.py:34](../backend/transit.py#L34) | 응답의 초·m·원 값을 유한한 음수 아닌 수로 제한한다. 미확인은 0으로 대체하지 않는다. |
| `MicrophoneMeter` | [backend/microphone_meter.js:2](../backend/microphone_meter.js#L2) | JS/TS 정규식 후보; AST 검증 아님 |
| `minutes` | [frontend/js/util.js:30](../frontend/js/util.js#L30) | JS/TS 정규식 후보; AST 검증 아님 |
| `missing` | [frontend/js/chat.js:72](../frontend/js/chat.js#L72) | JS/TS 정규식 후보; AST 검증 아님 |
| `model_json` | [backend/agent_v3.py:56](../backend/agent_v3.py#L56) | Call the configured provider once with a bounded JSON response and safe usage metadata. |
| `model_reply` | [utils/scripts/agent_v3_http_fixture.py:27](../utils/scripts/agent_v3_http_fixture.py#L27) | 실제 provider JSON 요청에서 고정 의미/정렬 응답만 생성한다. 정책 결과는 만들지 않는다. |
| `model_reply.update` | [utils/scripts/agent_v3_http_fixture.py:49](../utils/scripts/agent_v3_http_fixture.py#L49) | 현재 턴의 실제 인용을 갖는 모델 후보를 추가한다. |
| `mountConversation` | [backend/team_chat.js:176](../backend/team_chat.js#L176) | JS/TS 정규식 후보; AST 검증 아님 |
| `mountInputMeter` | [backend/microphone_meter.js:81](../backend/microphone_meter.js#L81) | JS/TS 정규식 후보; AST 검증 아님 |
| `NaitoChatTests` | [backend/test_naito_chat.py:12](../backend/test_naito_chat.py#L12) | 서비스 키 없이 실행되는 공급자 어댑터 회귀다. |
| `NaitoChatTests.setUp` | [backend/test_naito_chat.py:15](../backend/test_naito_chat.py#L15) | 최소 정상 대화 입력을 준비한다. |
| `NaitoChatTests.test_clarification_fields_validate_and_do_not_leak` | [backend/test_naito_chat.py:127](../backend/test_naito_chat.py#L127) | 보류 필드에는 허용 이름만 한 번 노출하고 원문은 포함하지 않는다. |
| `NaitoChatTests.test_empty_interpretation_not_reported_as_applied` | [backend/test_naito_chat.py:82](../backend/test_naito_chat.py#L82) | 지원하지 않는 발화를 반영 완료로 안내하지 않는다. |
| `NaitoChatTests.test_errors_do_not_disclose_or_replace` | [backend/test_naito_chat.py:61](../backend/test_naito_chat.py#L61) | 공급자 오류/비JSON/사실 생성은 오류로 남기고 키·원문·가짜 초안을 노출하지 않는다. |
| `NaitoChatTests.test_interpreted_fields_preserve_reconfirmation_and_omit_blocked` | [backend/test_naito_chat.py:109](../backend/test_naito_chat.py#L109) | 기존 값 재확인과 명시 해제는 필드명으로만 내보내고 보류와 null은 제외한다. |
| `NaitoChatTests.test_missing_key` | [backend/test_naito_chat.py:19](../backend/test_naito_chat.py#L19) | 미설정은 503이며 외부 호출을 하지 않는다. |
| `NaitoChatTests.test_provider_reply_cannot_clear_required_condition` | [backend/test_naito_chat.py:93](../backend/test_naito_chat.py#L93) | 모의 공급자의 필수 조건 무단 삭제는 보류하고 기존 초안을 보존한다. |
| `NaitoChatTests.test_provider_request_excludes_coordinates` | [backend/test_naito_chat.py:32](../backend/test_naito_chat.py#L32) | 키는 헤더에만, 좌표는 제외하며 공식 고정 주소로 한 번 요청한다. |
| `NaitoChatTests.test_response_size_and_json_boundary` | [backend/test_naito_chat.py:76](../backend/test_naito_chat.py#L76) | 과대 응답/일반 텍스트/잘못된 응답 구조를 파싱 성공으로 취급하지 않는다. |
| `NaitoChatTests.test_success_and_no_recommendation` | [backend/test_naito_chat.py:49](../backend/test_naito_chat.py#L49) | 모의 국악 해석 뒤 출발지 질문으로 이어지며 추천은 실행하지 않는다. |
| `NaitoChatTests.test_validate_before_provider` | [backend/test_naito_chat.py:25](../backend/test_naito_chat.py#L25) | 잘못된 요청은 공급자/키 조회 전에 거절한다. |
| `NaitoV3Tests` | [backend/test_naito_v3.py:39](../backend/test_naito_v3.py#L39) | 메시지→실제 정책→도구→원자 commit과 오류 분류를 독립 검증한다. |
| `NaitoV3Tests.call` | [backend/test_naito_v3.py:112](../backend/test_naito_v3.py#L112) | 실제 chat 분기와 저장소 commit을 통과한 응답 메타데이터를 이어간다. |
| `NaitoV3Tests.exploration_reply` | [backend/test_naito_v3.py:97](../backend/test_naito_v3.py#L97) | 호출된 실제 상태를 검사할 수 있는 경계 결과만 반환한다. |
| `NaitoV3Tests.fixed_rows` | [backend/test_naito_v3.py:133](../backend/test_naito_v3.py#L133) | 실제 공급자 필드형식에 독립 평가용 두 소개와 고정 ID를 넣는다. |
| `NaitoV3Tests.locate` | [backend/test_naito_v3.py:124](../backend/test_naito_v3.py#L124) | 검증 위치를 가진 새 서버 상태로 시작하고 클라이언트 초안 주입을 하지 않는다. |
| `NaitoV3Tests.message` | [backend/test_naito_v3.py:120](../backend/test_naito_v3.py#L120) | STT 최종 텍스트와 같은 message 이벤트를 실행한다. |
| `NaitoV3Tests.model_reply` | [backend/test_naito_v3.py:72](../backend/test_naito_v3.py#L72) | 고정 의미 fixture와 고정 원문에 대한 모의 관련성 판정을 구분한다. |
| `NaitoV3Tests.payload` | [backend/test_naito_v3.py:63](../backend/test_naito_v3.py#L63) | 원문 근거를 가진 의미 후보만 반환하고 기대 정책/행동은 주입하지 않는다. |
| `NaitoV3Tests.prepare_content_choices` | [backend/test_naito_v3.py:437](../backend/test_naito_v3.py#L437) | 실제 orchestration에7개 고정 source 후보를 제공해 서버3개 표시계약을 만든다. |
| `NaitoV3Tests.prepare_content_choices.result` | [backend/test_naito_v3.py:441](../backend/test_naito_v3.py#L441) | 현재 서버조건과 연결된 사실형 후보만 반환한다. |
| `NaitoV3Tests.request` | [backend/test_naito_v3.py:104](../backend/test_naito_v3.py#L104) | 마지막 canonical 메타데이터의 다음 턴을 구성한다. |
| `NaitoV3Tests.select_event` | [backend/test_naito_v3.py:454](../backend/test_naito_v3.py#L454) | 클라이언트는 사실 snapshot 대신 서버가 발급한 ID와 결과/묶음 참조만 보낸다. |
| `NaitoV3Tests.setUp` | [backend/test_naito_v3.py:42](../backend/test_naito_v3.py#L42) | 개별 저장소와 안전한 외부 경계를 설치하며 실제 환경 키를 읽지 않는다. |
| `NaitoV3Tests.start` | [backend/test_naito_v3.py:57](../backend/test_naito_v3.py#L57) | 시험이 실패해도 monkeypatch를 복구한다. |
| `NaitoV3Tests.test_actual_exploration_address_normalization_does_not_reject_the_current_selection` | [backend/test_naito_v3.py:484](../backend/test_naito_v3.py#L484) | 실제exploration이 원점주소를 표시메타로생략해도 동일canonical좌표 후보선택은 성공한다. |
| `NaitoV3Tests.test_actual_exploration_filter_ranking_and_source_ids_cross_orchestrator` | [backend/test_naito_v3.py:398](../backend/test_naito_v3.py#L398) | 실제explore를 연결해 의미 취향이 원본 소개·ID 기반 정렬까지 전달되는지 검사한다. |
| `NaitoV3Tests.test_actual_provider_json_decode_failure_is_not_disguised_as_policy_bug` | [backend/test_naito_v3.py:324](../backend/test_naito_v3.py#L324) | 실제 provider decoder를 거친 손상 JSON이 의미 단계 오류로 기록된다. |
| `NaitoV3Tests.test_alternatives_advance_only_server_batch_and_reject_old_or_foreign_choices` | [backend/test_naito_v3.py:502](../backend/test_naito_v3.py#L502) | 다음묶음은 동일서버풀의4~6번이며 과거묶음·풀밖ID·다른대화는 선택/조회하지 못한다. |
| `NaitoV3Tests.test_cached_failure_preserves_http_status_without_model_retry` | [backend/test_naito_v3.py:294](../backend/test_naito_v3.py#L294) | 동일 오류 응답의 재전달이502를200으로 바꾸거나 모델을 다시 부르지 않는다. |
| `NaitoV3Tests.test_current_batch_number_name_and_button_share_selection_without_model_or_source` | [backend/test_naito_v3.py:460](../backend/test_naito_v3.py#L460) | 화면3번·음성단답·동일카드버튼은 같은 검증후보로 연결하고 날짜나 재조회가 생기지 않는다. |
| `NaitoV3Tests.test_duplicate_and_stale_requests_never_reexecute_model` | [backend/test_naito_v3.py:205](../backend/test_naito_v3.py#L205) | 성공 응답 손실의 재전달·과거revision은 모델 호출 횟수를 늘리지 않는다. |
| `NaitoV3Tests.test_invalid_envelope_is_502_while_policy_bug_is_500` | [backend/test_naito_v3.py:356](../backend/test_naito_v3.py#L356) | 사용자에게 같은 일반오류로 보여도 내부 모델형식/정책버그 원인을 구분한다. |
| `NaitoV3Tests.test_lease_handover_during_model_drops_old_result` | [backend/test_naito_v3.py:380](../backend/test_naito_v3.py#L380) | 늦은 모델 응답은 새 owner의 revision과 목적을 바꾸지 않는다. |
| `NaitoV3Tests.test_lease_handover_during_model_drops_old_result.late` | [backend/test_naito_v3.py:384](../backend/test_naito_v3.py#L384) | 모델 처리 중 reload의 lease 인계를 재현한다. |
| `NaitoV3Tests.test_map_no_results_is_distinct_from_source_failure` | [backend/test_naito_v3.py:258](../backend/test_naito_v3.py#L258) | 정상 지도0건은 연결장애라고 표시하거나 임의 좌표를 채택하지 않는다. |
| `NaitoV3Tests.test_map_source_error_remains_typed_and_retries_without_reinterpretation` | [backend/test_naito_v3.py:236](../backend/test_naito_v3.py#L236) | 지도503은 실제0건과 구분하며 같은 지명 도구 재시도에 모델을 다시 쓰지 않는다. |
| `NaitoV3Tests.test_model_timeout_is_meaning_failure_and_next_turn_recovers` | [backend/test_naito_v3.py:283](../backend/test_naito_v3.py#L283) | 모델 timeout의 단계·마지막 상태를 보존하고 다음 명시 발화가 정상 처리된다. |
| `NaitoV3Tests.test_open_heartbeat_release_make_no_model_or_source_calls` | [backend/test_naito_v3.py:155](../backend/test_naito_v3.py#L155) | 저장 연결·heartbeat·해제가 대화 추론이나 외부 조회를 실행하지 않는다. |
| `NaitoV3Tests.test_optional_rank_timeout_preserves_content_and_counts_attempt` | [backend/test_naito_v3.py:415](../backend/test_naito_v3.py#L415) | 선택2콜 실패도 시도 수에 포함하고 실제 후보를 버리거나 맞춤 성공으로 가장하지 않는다. |
| `NaitoV3Tests.test_optional_rank_timeout_preserves_content_and_counts_attempt.failed_rank` | [backend/test_naito_v3.py:420](../backend/test_naito_v3.py#L420) | 첫 의미 호출은 성공하고 후보 후처리만 의도적으로 실패시킨다. |
| `NaitoV3Tests.test_partial_invalid_category_keeps_good_mood_and_explores` | [backend/test_naito_v3.py:188](../backend/test_naito_v3.py#L188) | 정상 취향+잘못된 음악category 하나가 전체502나 필수조건 루프를 만들지 않는다. |
| `NaitoV3Tests.test_partial_invalid_category_keeps_good_mood_and_explores.mixed` | [backend/test_naito_v3.py:192](../backend/test_naito_v3.py#L192) | 정상 의미와 고의 손상한 메뉴 후보를 같은 모델 응답에 넣는다. |
| `NaitoV3Tests.test_provider_error_keeps_safe_code_and_status` | [backend/test_naito_v3.py:305](../backend/test_naito_v3.py#L305) | 제공자429는 구조502로 바꾸지 않고 안전한 원인·단계를 남긴다. |
| `NaitoV3Tests.test_real_filter_change_clears_old_selection_and_old_batch_cannot_bypass_it` | [backend/test_naito_v3.py:563](../backend/test_naito_v3.py#L563) | 무료필터 변경은 기존선택을해제한뒤 새결과만발급하고 이전버튼으로 새조건을우회하지 못한다. |
| `NaitoV3Tests.test_real_filter_change_clears_old_selection_and_old_batch_cannot_bypass_it.free_meaning` | [backend/test_naito_v3.py:569](../backend/test_naito_v3.py#L569) | 무료명시 현재발화의 실제조건후보만 제공한다. |
| `NaitoV3Tests.test_reported_performance_explanation_mood_and_exact_map_pipeline` | [backend/test_naito_v3.py:166](../backend/test_naito_v3.py#L166) | 공연→설명요청→잔잔함→서울시청이 실제 정책과 지도 채택 뒤 공연 조회로 연결된다. |
| `NaitoV3Tests.test_source_error_keeps_meaning_and_retry_calls_only_failed_tool` | [backend/test_naito_v3.py:219](../backend/test_naito_v3.py#L219) | 도구0건과 장애를 구분하고 재시도에서 잔잔함 의미를 다시 적용하지 않는다. |
| `NaitoV3Tests.test_tool_timeout_preserves_meaning_and_has_retry_action` | [backend/test_naito_v3.py:270](../backend/test_naito_v3.py#L270) | 조회 timeout은 의미502로 숨기지 않고 보존된 의미에서 도구만 재시도할 수 있다. |
| `NaitoV3Tests.test_true_hard_requirement_blocks_even_after_proceed_event` | [backend/test_naito_v3.py:335](../backend/test_naito_v3.py#L335) | 실제 명시 필수 제약을 새 취향이나 진행 버튼으로 조용히 우회하지 않는다. |
| `NaitoV3Tests.test_unclear_chitchat_and_empty_meaning_keep_selection_without_false_model_success` | [backend/test_naito_v3.py:530](../backend/test_naito_v3.py#L530) | 모호한 정상해석은 현재선택 안내로회복하되 깨진envelope는 별도오류로 남긴다. |
| `NaitoV3Tests.test_unclear_chitchat_and_empty_meaning_keep_selection_without_false_model_success.meaning` | [backend/test_naito_v3.py:542](../backend/test_naito_v3.py#L542) | 실제 현재turn 근거만 바꿔 정책/저장소 검증은 그대로 통과한다. |
| `NaitoV3Tests.test_unconfigured_provider_returns_503_without_unhandled_exception` | [backend/test_naito_v3.py:314](../backend/test_naito_v3.py#L314) | 설정이 없다는 원인을 숨기거나 서버 예외로 넘기지 않는다. |
| `NaitoV3Tests.test_unknown_origin_choice_is_client_error_and_keeps_coordinates` | [backend/test_naito_v3.py:370](../backend/test_naito_v3.py#L370) | 없는 후보ID 선택이 모델502나 임의 좌표 채택이 되지 않는다. |
| `NaitoV3Tests.test_visit_under_sixty_minutes_rejects_before_any_source` | [backend/test_naito_v3.py:587](../backend/test_naito_v3.py#L587) | 방문 단계의60분 미만 입력은 minimum_duration이며 소스 조회 전에 중단한다. |
| `NaitoV3Tests.test_visit_uses_same_performance_filters_preferences_and_explicit_context` | [backend/test_naito_v3.py:600](../backend/test_naito_v3.py#L600) | 방문 전환이 공연을 전시로 바꾸지 않고 원 취향·실제 시간/출발지 맥락을 유지한다. |
| `NaitoV3Tests.test_zero_candidates_is_distinct_from_source_failure` | [backend/test_naito_v3.py:345](../backend/test_naito_v3.py#L345) | 조회 성공0건은 source_error 재시도 대상으로 바꾸거나 후보를 만들지 않는다. |
| `NaitoV3Tests.visit_state` | [backend/test_naito_v3.py:142](../backend/test_naito_v3.py#L142) | 방문 단계의 검증 입력·기존 공연 취향을 서버 초기 상태로 준비한다. |
| `navigateVoice` | [backend/team_chat.js:210](../backend/team_chat.js#L210) | JS/TS 정규식 후보; AST 검증 아님 |
| `new_state` | [backend/dialogue_memory.py:19](../backend/dialogue_memory.py#L19) | 대화 한 개의 빈 도메인 상태를 만든다. ID/revision/lease는 외부 store 소유다. |
| `newChat` | [frontend/js/chat.js:687](../frontend/js/chat.js#L687) | JS/TS 정규식 후보; AST 검증 아님 |
| `next` | [frontend/js/chat.js:1063](../frontend/js/chat.js#L1063) | JS/TS 정규식 후보; AST 검증 아님 |
| `normalize` | [backend/preferences.py:9](../backend/preferences.py#L9) | 선호 부분 갱신을 검증한다. 빈 목록/false/any는 명시적 해제이며 null은 변경 없음이다. |
| `normalize_place` | [backend/tour_places.py:79](../backend/tour_places.py#L79) | 목록/상세 사실만 통합한다. 결측 좌표·운영·요금은 null, 관람 가능 여부는 check다. |
| `normalize_places` | [backend/places.py:45](../backend/places.py#L45) | 공급자 x/y를 숫자 lng/lat로 바꾸고 선택 가능한 최대5건만 반환한다. 손상과0건을 구분한다. |
| `normalize_proposal` | [backend/chat_conditions.py:24](../backend/chat_conditions.py#L24) | 허용된 조건만 정규화한다. null은 변경 없음, 좌표·잘못된 값은 ValueError다. |
| `normalize_routes` | [backend/transit.py:91](../backend/transit.py#L91) | 공식 응답의 경로 최대 세 개를 초·m 단위로 검증한다. 누락·공급자 오류는 실패로 구분한다. |
| `note` | [backend/team_chat.js:256](../backend/team_chat.js#L256) | JS/TS 정규식 후보; AST 검증 아님 |
| `note` | [frontend/js/place.js:118](../frontend/js/place.js#L118) | JS/TS 정규식 후보; AST 검증 아님 |
| `nothingUnderstood` | [frontend/js/chat.js:965](../frontend/js/chat.js#L965) | JS/TS 정규식 후보; AST 검증 아님 |
| `num` | [frontend/js/chat.js:543](../frontend/js/chat.js#L543) | JS/TS 정규식 후보; AST 검증 아님 |
| `official_image` | [backend/outing.py:117](../backend/outing.py#L117) | 서울시 문화포털의 공식 대표 이미지 주소만 넘긴다. 다른 주소·형식이 이상하면 None (화면은 대체 그림 사용). |
| `official_link` | [backend/tour_places.py:54](../backend/tour_places.py#L54) | 공식 응답이 제공한 홈페이지만 허용한다. ID로 확인하지 않은 상세 URL을 만들어 내지 않는다. |
| `OfficialImageTest` | [backend/test_culture_sources.py:130](../backend/test_culture_sources.py#L130) | 개요 없음 |
| `OfficialImageTest.test_only_seoul_culture_portal_images` | [backend/test_culture_sources.py:131](../backend/test_culture_sources.py#L131) | 공식 문화포털 이미지만 https 로 넘기고, 다른 주소·빈 값은 None. |
| `openingQuestion` | [backend/team_voice_actions.js:13](../backend/team_voice_actions.js#L13) | JS/TS 정규식 후보; AST 검증 아님 |
| `openOriginalMenu` | [backend/team_chat.js:200](../backend/team_chat.js#L200) | JS/TS 정규식 후보; AST 검증 아님 |
| `openOriginPicker` | [frontend/js/chat.js:1399](../frontend/js/chat.js#L1399) | JS/TS 정규식 후보; AST 검증 아님 |
| `openSelectedContent` | [frontend/js/chat.js:222](../frontend/js/chat.js#L222) | JS/TS 정규식 후보; AST 검증 아님 |
| `openSheet` | [frontend/js/place.js:146](../frontend/js/place.js#L146) | JS/TS 정규식 후보; AST 검증 아님 |
| `originNameKey` | [frontend/js/chat.js:1372](../frontend/js/chat.js#L1372) | JS/TS 정규식 후보; AST 검증 아님 |
| `other` | [frontend/js/chat.js:1209](../frontend/js/chat.js#L1209) | JS/TS 정규식 후보; AST 검증 아님 |
| `OutingTests` | [backend/test_outing.py:9](../backend/test_outing.py#L9) | 개인 추천의 의미가 바뀌는 경계 사례를 재현한다. |
| `OutingTests.setUp` | [backend/test_outing.py:12](../backend/test_outing.py#L12) | 각 사례에 독립적인 청량리역 요청을 준비한다. |
| `OutingTests.test_actual_fields` | [backend/test_outing.py:16](../backend/test_outing.py#L16) | 빈 요금, 무료 분류, 명시한 0원, 거리 오름차순을 보존한다. |
| `OutingTests.test_bad_input` | [backend/test_outing.py:77](../backend/test_outing.py#L77) | 잘못된 출발 좌표나 종료 시각으로 외부 API를 호출하지 않는다. |
| `OutingTests.test_detail_fields_from_source` | [backend/test_outing.py:29](../backend/test_outing.py#L29) | 행사 기간·지역은 공급자 원문을 쓰고 장소명을 주소로 바꾸지 않는다. |
| `OutingTests.test_empty_and_error` | [backend/test_outing.py:84](../backend/test_outing.py#L84) | 실제 후보 0건을 공급자 장애와 구분한다. |
| `OutingTests.test_end_boundary` | [backend/test_outing.py:43](../backend/test_outing.py#L43) | 전시 종료 시각에 도착하는 입력은 단순 운영구간에서 제외한다. |
| `OutingTests.test_genre_mismatch` | [backend/test_outing.py:91](../backend/test_outing.py#L91) | 국악 조회에 전시가 섞이거나 전시만 반환돼도 국악 외 행사는 제외한다. |
| `OutingTests.test_input_error_fields` | [backend/test_outing.py:63](../backend/test_outing.py#L63) | 시간 누락·형식·시간대·역전·다음날 및 잘못된 좌표의 필드를 특정한다. |
| `OutingTests.test_minimum_duration_before_source` | [backend/test_outing.py:50](../backend/test_outing.py#L50) | 59분과 59분59초는 외부 조회 전에 거절하며 정확히 60분은 허용한다. |
| `OutingTests.test_recording_scope` | [backend/test_outing.py:102](../backend/test_outing.py#L102) | 저장하지 않은 분류를 같은 날의 전체 기록으로 대체하지 않는다. |
| `p` | [frontend/js/util.js:60](../frontend/js/util.js#L60) | JS/TS 정규식 후보; AST 검증 아님 |
| `p2` | [frontend/js/app.js:187](../frontend/js/app.js#L187) | JS/TS 정규식 후보; AST 검증 아님 |
| `parseUtterance` | [frontend/js/parse.js:37](../frontend/js/parse.js#L37) | JS/TS 정규식 후보; AST 검증 아님 |
| `patch` | [frontend/js/chat.js:102](../frontend/js/chat.js#L102) | JS/TS 정규식 후보; AST 검증 아님 |
| `pauseChatNavigation` | [frontend/js/chat.js:1288](../frontend/js/chat.js#L1288) | JS/TS 정규식 후보; AST 검증 아님 |
| `phase` | [backend/voice_session.js:151](../backend/voice_session.js#L151) | JS/TS 정규식 후보; AST 검증 아님 |
| `phones_from_page` | [backend/contact.py:28](../backend/contact.py#L28) | 상세 페이지 HTML에서 첫 '문의' 칸의 전화번호들을 순서대로 (중복 없이) 돌려줘요. |
| `photo` | [frontend/js/util.js:152](../frontend/js/util.js#L152) | JS/TS 정규식 후보; AST 검증 아님 |
| `pickSeason` | [frontend/js/landing.js:21](../frontend/js/landing.js#L21) | JS/TS 정규식 후보; AST 검증 아님 |
| `pin` | [frontend/js/place.js:204](../frontend/js/place.js#L204) | JS/TS 정규식 후보; AST 검증 아님 |
| `placeById` | [frontend/js/place.js:17](../frontend/js/place.js#L17) | JS/TS 정규식 후보; AST 검증 아님 |
| `placeName` | [frontend/js/chat.js:957](../frontend/js/chat.js#L957) | JS/TS 정규식 후보; AST 검증 아님 |
| `places_reply` | [utils/scripts/agent_http_fixture.py:42](../utils/scripts/agent_http_fixture.py#L42) | 동명 서울/수원 시청을 카카오 원본 형식의 모의 응답으로 제공한다. |
| `PlaceSearchTests` | [backend/test_places.py:13](../backend/test_places.py#L13) | 외부 조회를 대체한 경계 검사다. 실제 키 호출은 별도 브라우저 검사로 수행한다. |
| `PlaceSearchTests.fixture` | [backend/test_places.py:16](../backend/test_places.py#L16) | 공개 장소를 뜻하지 않는 모의 공급자 문서를 만든다. |
| `PlaceSearchTests.test_address_id_and_coordinates` | [backend/test_places.py:39](../backend/test_places.py#L39) | 주소 결과는 공급자 주소·좌표를 보존하고 재조회에도 같은 파생 식별자를 만든다. |
| `PlaceSearchTests.test_empty_vs_invalid_source` | [backend/test_places.py:63](../backend/test_places.py#L63) | 정상0건과 좌표 손상·목록 누락을 구분하며 일부 손상 행은 별도 집계한다. |
| `PlaceSearchTests.test_failures` | [backend/test_places.py:126](../backend/test_places.py#L126) | 권한·쿼터·시간초과·손상 응답의 공개 오류만 반환하며 공급자 상세는 숨긴다. |
| `PlaceSearchTests.test_inputs_before_network` | [backend/test_places.py:21](../backend/test_places.py#L21) | 공백·길이초과·제어문자·잘못된 종류를 키 조회/외부 호출 전에 거절한다. |
| `PlaceSearchTests.test_invalid_origin_before_network_and_legacy_query` | [backend/test_places.py:111](../backend/test_places.py#L111) | 잘못된 원점을 외부 호출 전에 거절하고 원점 없는 기존 검색 계약을 보존한다. |
| `PlaceSearchTests.test_keyword_coordinates_and_null` | [backend/test_places.py:29](../backend/test_places.py#L29) | x/y를 올바른 축으로 변환하고 공란 주소·출처 URL을 임의 보완하지 않는다. |
| `PlaceSearchTests.test_keyword_preserves_provider_category_role_without_inference` | [backend/test_places.py:48](../backend/test_places.py#L48) | 원 분류경로·PK6주차장 그룹을 보존하고 결측을 관광명소로 채우지 않는다. |
| `PlaceSearchTests.test_missing_key` | [backend/test_places.py:85](../backend/test_places.py#L85) | 키 미설정을 정상0건으로 반환하거나 외부 조회하지 않는다. |
| `PlaceSearchTests.test_origin_bias_and_actual_straight_distance` | [backend/test_places.py:92](../backend/test_places.py#L92) | 사용자가 선택한 원점을 카카오 거리순 조회에 전달하고 실제 좌표의 직선거리를 계산한다. |
| `PlaceSearchTests.test_provider_request` | [backend/test_places.py:74](../backend/test_places.py#L74) | 키는 헤더에만 두고 검색어는 URL 인코딩하며 최대5건을 요청한다. |
| `plain` | [backend/tour_places.py:46](../backend/tour_places.py#L46) | 공식 응답의 HTML 표기를 평문으로 바꾸고 빈 값은 null로 유지한다. |
| `play` | [frontend/js/chat.js:448](../frontend/js/chat.js#L448) | JS/TS 정규식 후보; AST 검증 아님 |
| `post` | [frontend/js/api.js:45](../frontend/js/api.js#L45) | JS/TS 정규식 후보; AST 검증 아님 |
| `post` | [utils/scripts/check_culture_sources.py:19](../utils/scripts/check_culture_sources.py#L19) | 로컬 HTTP 상태/정규화 응답만 읽는다. 공급자 키가 있는 URL은 직접 출력하지 않는다. |
| `PreferenceTests` | [backend/test_preferences.py:12](../backend/test_preferences.py#L12) | 실제 기록과 명시적 모의 공식 행사를 구분해 조건 반영을 확인한다. |
| `PreferenceTests.setUp` | [backend/test_preferences.py:15](../backend/test_preferences.py#L15) | 기존 QA 입력과 독립된 공식 응답 모양의 행을 준비한다. |
| `PreferenceTests.test_budget_excludes_unknown_and_multiple_prices` | [backend/test_preferences.py:63](../backend/test_preferences.py#L63) | 1인 관람료 한도는 미확인·할인·복수좌석을 충족으로 간주하지 않는다. |
| `PreferenceTests.test_confirmed_categories_atomic` | [backend/test_preferences.py:30](../backend/test_preferences.py#L30) | 대표 분류 변경을 거절하면 연결된 복수 분류도 변경되지 않는다. |
| `PreferenceTests.test_exclusion_never_restored_when_zero` | [backend/test_preferences.py:73](../backend/test_preferences.py#L73) | 모든 기록 후보를 제외해도 제한을 완화하거나 샘플로 대체하지 않는다. |
| `PreferenceTests.test_invalid_and_explicit_clear` | [backend/test_preferences.py:96](../backend/test_preferences.py#L96) | 잘못된 형식을 거절하며 명시적 false/any/빈 목록은 보존한다. |
| `PreferenceTests.test_keyword_and_short_walk_order` | [backend/test_preferences.py:79](../backend/test_preferences.py#L79) | 관심어 우선과 가까운 곳 우선은 순서를 실제로 바꾸며 도보 보장은 하지 않는다. |
| `PreferenceTests.test_multiple_categories_query_and_dedup` | [backend/test_preferences.py:39](../backend/test_preferences.py#L39) | 분류별 조회 후 ID 중복을 제거하고 장르 밖 후보를 제외한다. |
| `PreferenceTests.test_multiple_categories_query_and_dedup.source` | [backend/test_preferences.py:41](../backend/test_preferences.py#L41) | 두 음악 장르와 공통 행을 돌려주는 모의 공급자다. |
| `PreferenceTests.test_music_discovery_then_broad_accept` | [backend/test_preferences.py:21](../backend/test_preferences.py#L21) | 음악→골고루는 분류를 강요하지 않고 같은 초안의 세 분류를 유지한다. |
| `PreferenceTests.test_no_partial_success_when_one_source_fails` | [backend/test_preferences.py:51](../backend/test_preferences.py#L51) | 한 관심사 조회 실패를 0건/다른 분류 성공으로 숨기지 않는다. |
| `PreferenceTests.test_same_id_with_different_official_url_once` | [backend/test_preferences.py:56](../backend/test_preferences.py#L56) | 메뉴 쿼리가 다른 동일 행사도 후보 ID 기준으로 한 번만 반환한다. |
| `PreferenceTests.test_unverified_hard_requirement_blocks_before_source` | [backend/test_preferences.py:89](../backend/test_preferences.py#L89) | 계단 없음 등 필수 제약을 검증 못하면 외부 호출 전 명시적으로 차단한다. |
| `preferenceText` | [backend/team_preferences.js:16](../backend/team_preferences.js#L16) | JS/TS 정규식 후보; AST 검증 아님 |
| `preflight` | [utils/scripts/commit_report.py:23](../utils/scripts/commit_report.py#L23) | Validate branch, cutoff, report encoding, scoped paths and an empty index. |
| `prepare` | [utils/scripts/prepare_chat_handoff.py:53](../utils/scripts/prepare_chat_handoff.py#L53) | 공개 Git 프론트 복사본에 패치를 실제 적용하고 결과 해시를 검증한 뒤 인계 ZIP을 만든다. |
| `prepareView` | [frontend/js/app.js:29](../frontend/js/app.js#L29) | JS/TS 정규식 후보; AST 검증 아님 |
| `Preview` | [backend/preview.py:44](../backend/preview.py#L44) | 허용된 화면과 개인 검증용 JSON 요청만 제공한다. |
| `Preview.do_GET` | [backend/preview.py:84](../backend/preview.py#L84) | 점검 폼과 저장소의 대표 요청만 제공한다. |
| `Preview.do_OPTIONS` | [backend/preview.py:55](../backend/preview.py#L55) | 설정된 프론트의 JSON POST 사전 요청만 허용하고 그 외 origin/메서드/헤더는 거절한다. |
| `Preview.do_POST` | [backend/preview.py:128](../backend/preview.py#L128) | 장소 요청을 처리하고 입력·외부 공급자 오류를 다른 상태로 전달한다. |
| `Preview.end_headers` | [backend/preview.py:47](../backend/preview.py#L47) | 정상/오류 응답 모두 허용 origin에만 CORS 헤더를 적용하며 쿠키 인증은 허용하지 않는다. |
| `Preview.reply` | [backend/preview.py:73](../backend/preview.py#L73) | UTF-8 본문을 길이와 함께 응답한다. |
| `PreviewContractTests` | [backend/test_preview.py:12](../backend/test_preview.py#L12) | 실제 POST 처리기를 사용하되 응답 전송과 외부 공급자만 대체한다. |
| `PreviewContractTests.request` | [backend/test_preview.py:15](../backend/test_preview.py#L15) | JSON 요청을 HTTP 처리기에 전달하고 상태 코드·응답을 반환한다. |
| `PreviewContractTests.setUp` | [backend/test_preview.py:30](../backend/test_preview.py#L30) | 각 테스트가 사용할 독립적인 정상 요청을 읽는다. |
| `PreviewContractTests.test_chat_route_and_validation` | [backend/test_preview.py:35](../backend/test_preview.py#L35) | 새 대화 경로는 어댑터 응답을 전달하고 잘못된 입력은 필드 오류를 반환한다. |
| `PreviewContractTests.test_culture_source_routes_and_errors` | [backend/test_preview.py:44](../backend/test_preview.py#L44) | 문화시설 선택은 같은 추천 경로에서 전달하며 오류를 행사로 대체하지 않는다. |
| `PreviewContractTests.test_file_voice_disabled` | [backend/test_preview.py:141](../backend/test_preview.py#L141) | 파일 음성이 꺼진 서버에서는 버튼을 숨기고 합성 요청도 실행하지 않는다. |
| `PreviewContractTests.test_home_uses_same_origin_app_when_prepared` | [backend/test_preview.py:154](../backend/test_preview.py#L154) | 대화 복사본을 준비했으면 기본 주소는 단일 앱 홈으로 이동한다. |
| `PreviewContractTests.test_invalid_kind` | [backend/test_preview.py:85](../backend/test_preview.py#L85) | 지원하지 않는 요청 종류를 place로 조용히 대체하지 않는다. |
| `PreviewContractTests.test_kind_compatibility` | [backend/test_preview.py:68](../backend/test_preview.py#L68) | 정확히 60분인 route/course가 같은 코스 경로로, place는 후보만 반환한다. |
| `PreviewContractTests.test_origin_configuration` | [backend/test_preview.py:90](../backend/test_preview.py#L90) | 허용 주소의 정확한 일치만 사용하고 와일드카드·자격정보·잘못된 설정을 제외한다. |
| `PreviewContractTests.test_place_search_contract` | [backend/test_preview.py:164](../backend/test_preview.py#L164) | 새 검색 경로에도 입력400·허용origin·공급자 상태 전달을 동일 적용한다. |
| `PreviewContractTests.test_preflight` | [backend/test_preview.py:99](../backend/test_preview.py#L99) | 설정된 origin·POST·Content-Type만 사전 요청에서 허용한다. |
| `PreviewContractTests.test_render_origin` | [backend/test_preview.py:121](../backend/test_preview.py#L121) | 서버 설정의 공개 HTTPS 주소만 허용하고 비슷한 다른 주소는 거절한다. |
| `PreviewContractTests.test_server_options` | [backend/test_preview.py:130](../backend/test_preview.py#L130) | 배포 포트·주소를 지원하되 명시 옵션이 우선하고 잘못된 포트는 시작 전에 거절한다. |
| `PreviewContractTests.test_short_duration_response` | [backend/test_preview.py:57](../backend/test_preview.py#L57) | 60분 미만은 필드/코드가 있는 400이며 문화/코스 조회를 하지 않는다. |
| `PreviewContractTests.test_source_error_is_not_input_error` | [backend/test_preview.py:78](../backend/test_preview.py#L78) | 공급자 장애는 필드 오류 대신 502이며 공급자 예외 내용은 숨긴다. |
| `projectAgentSnapshot` | [frontend/js/chat.js:1322](../frontend/js/chat.js#L1322) | JS/TS 정규식 후보; AST 검증 아님 |
| `provider` | [backend/agent_v3.py:29](../backend/agent_v3.py#L29) | Reuse the existing explicitly selected provider without guessing from a key. |
| `provider` | [backend/naito_chat.py:22](../backend/naito_chat.py#L22) | LAB678_NAITO_PROVIDER: codyssey(기본) / anthropic / openai. 키 모양으로 추측하지 않는다(해커톤 키도 sk- 로 시작). |
| `provider_reply` | [utils/scripts/agent_http_fixture.py:21](../utils/scripts/agent_http_fixture.py#L21) | 실제 공급자 요청 형식을 읽고 테스트 발화에만 고정 모델 후보를 돌려준다. |
| `provider_response` | [backend/test_transit.py:11](../backend/test_transit.py#L11) | 공식 스키마를 따르는 가상 도보·지하철·도보 3구간을 만든다. 시연 데이터가 아니다. |
| `put_value` | [backend/chat_conditions.py:97](../backend/chat_conditions.py#L97) | 출발지 검색어가 바뀌면 이전 좌표를 제거한다. 다른 조건은 초안에만 반영한다. |
| `query_walking` | [backend/walking.py:16](../backend/walking.py#L16) | 개인 화면의 도보 조회 간격을 제한하고 공급자의 JSON 또는 실패 상태를 반환한다. |
| `QuietPreview` | [utils/scripts/agent_http_fixture.py:66](../utils/scripts/agent_http_fixture.py#L66) | 실제 처리기는 유지하고 테스트 프로세스의 HTTP 로그만 생략한다. |
| `QuietPreview.log_message` | [utils/scripts/agent_http_fixture.py:69](../utils/scripts/agent_http_fixture.py#L69) | 고정 테스트 요청의 접근 로그를 저장하지 않는다. |
| `readStore` | [frontend/js/util.js:65](../frontend/js/util.js#L65) | JS/TS 정규식 후보; AST 검증 아님 |
| `readVoiceReply` | [backend/voice_session.js:93](../backend/voice_session.js#L93) | JS/TS 정규식 후보; AST 검증 아님 |
| `recommend` | [backend/outing.py:150](../backend/outing.py#L150) | 검증된 요청의 후보를 계산한다. 입력 오류와 공급자 오류를 별도로 전달한다. |
| `recommendationBlocked` | [frontend/js/chat.js:1124](../frontend/js/chat.js#L1124) | JS/TS 정규식 후보; AST 검증 아님 |
| `recommendationContext` | [frontend/js/chat.js:1114](../frontend/js/chat.js#L1114) | JS/TS 정규식 후보; AST 검증 아님 |
| `record` | [utils/scripts/loop.py:21](../utils/scripts/loop.py#L21) | Append one evidenced attempt, rejecting terminal states and blind repeats. |
| `refit` | [frontend/js/place.js:224](../frontend/js/place.js#L224) | JS/TS 정규식 후보; AST 검증 아님 |
| `refresh` | [backend/location_view.js:36](../backend/location_view.js#L36) | JS/TS 정규식 후보; AST 검증 아님 |
| `refresh` | [backend/team_culture.js:24](../backend/team_culture.js#L24) | JS/TS 정규식 후보; AST 검증 아님 |
| `refresh` | [utils/scripts/watch.py:30](../utils/scripts/watch.py#L30) | Render state before indexing it; leave source and decisions untouched. |
| `refreshContentSelectionControls` | [frontend/js/chat.js:202](../frontend/js/chat.js#L202) | JS/TS 정규식 후보; AST 검증 아님 |
| `releaseAgent` | [frontend/js/agent-session.js:127](../frontend/js/agent-session.js#L127) | JS/TS 정규식 후보; AST 검증 아님 |
| `releaseAgentConnection` | [frontend/js/api.js:120](../frontend/js/api.js#L120) | JS/TS 정규식 후보; AST 검증 아님 |
| `releaseClarifications` | [frontend/js/chat.js:798](../frontend/js/chat.js#L798) | JS/TS 정규식 후보; AST 검증 아님 |
| `remember` | [backend/team_chat.js:266](../backend/team_chat.js#L266) | JS/TS 정규식 후보; AST 검증 아님 |
| `rememberCandidates` | [frontend/js/chat.js:1134](../frontend/js/chat.js#L1134) | JS/TS 정규식 후보; AST 검증 아님 |
| `render` | [frontend/js/chat.js:363](../frontend/js/chat.js#L363) | JS/TS 정규식 후보; AST 검증 아님 |
| `render` | [utils/scripts/catalog.py:204](../utils/scripts/catalog.py#L204) | Produce all utility and repository indexes without volatile timestamps. |
| `render` | [utils/scripts/context.py:22](../utils/scripts/context.py#L22) | Render bounded, human-curated lists while preserving their decision status. |
| `render_repo` | [utils/scripts/catalog.py:156](../utils/scripts/catalog.py#L156) | Index every eligible file plus code symbols, features and directory layout. |
| `render_utils` | [utils/scripts/catalog.py:118](../utils/scripts/catalog.py#L118) | Render stable forward and reverse indexes with repository-relative links. |
| `render_wave` | [backend/local_voice.py:30](../backend/local_voice.py#L30) | 문자열을 표준 입력으로 전달해 메모리에서 합성하고, 실패·과부하 때 예외를 반환한다. |
| `renderChat` | [frontend/js/chat.js:1259](../frontend/js/chat.js#L1259) | JS/TS 정규식 후보; AST 검증 아님 |
| `renderHome` | [frontend/js/app.js:223](../frontend/js/app.js#L223) | JS/TS 정규식 후보; AST 검증 아님 |
| `renderMap` | [frontend/js/place.js:256](../frontend/js/place.js#L256) | JS/TS 정규식 후보; AST 검증 아님 |
| `renderMe` | [frontend/js/app.js:236](../frontend/js/app.js#L236) | JS/TS 정규식 후보; AST 검증 아님 |
| `renderNotify` | [frontend/js/app.js:185](../frontend/js/app.js#L185) | JS/TS 정규식 후보; AST 검증 아님 |
| `renderPlace` | [frontend/js/place.js:33](../frontend/js/place.js#L33) | JS/TS 정규식 후보; AST 검증 아님 |
| `renderPreferenceSummary` | [backend/team_preferences.js:30](../backend/team_preferences.js#L30) | JS/TS 정규식 후보; AST 검증 아님 |
| `renderResultPreferences` | [backend/team_preferences.js:40](../backend/team_preferences.js#L40) | JS/TS 정규식 후보; AST 검증 아님 |
| `renderVoiceState` | [backend/team_chat.js:474](../backend/team_chat.js#L474) | JS/TS 정규식 후보; AST 검증 아님 |
| `repo_files` | [utils/scripts/catalog.py:46](../utils/scripts/catalog.py#L46) | Inventory repository files, including untracked work, without reading secrets. |
| `request` | [utils/scripts/check_chat_api.py:19](../utils/scripts/check_chat_api.py#L19) | 임시 서버로 JSON POST 또는 CORS OPTIONS를 보내 상태/본문/허용 origin을 반환한다. |
| `requestAgent` | [frontend/js/api.js:112](../frontend/js/api.js#L112) | JS/TS 정규식 후보; AST 검증 아님 |
| `requestBody` | [frontend/js/chat.js:1091](../frontend/js/chat.js#L1091) | JS/TS 정규식 후보; AST 검증 아님 |
| `requestChat` | [frontend/js/api.js:102](../frontend/js/api.js#L102) | JS/TS 정규식 후보; AST 검증 아님 |
| `requestRecommend` | [frontend/js/api.js:69](../frontend/js/api.js#L69) | JS/TS 정규식 후보; AST 검증 아님 |
| `resetChat` | [frontend/js/state.js:78](../frontend/js/state.js#L78) | JS/TS 정규식 후보; AST 검증 아님 |
| `resolve_changes` | [backend/chat_conditions.py:151](../backend/chat_conditions.py#L151) | 동일 초안/revision에서 명시적 bool 동의만 반영한다. 미응답 충돌은 유지한다. |
| `resolvePending` | [frontend/js/chat.js:1040](../frontend/js/chat.js#L1040) | JS/TS 정규식 후보; AST 검증 아님 |
| `restoreSnapshot` | [frontend/js/agent-session.js:39](../frontend/js/agent-session.js#L39) | JS/TS 정규식 후보; AST 검증 아님 |
| `retryLastTurn` | [frontend/js/chat.js:648](../frontend/js/chat.js#L648) | JS/TS 정규식 후보; AST 검증 아님 |
| `review_text` | [utils/scripts/read_pdf.py:18](../utils/scripts/read_pdf.py#L18) | Mask credential-related lines and two following lines before console output. |
| `route` | [frontend/js/app.js:42](../frontend/js/app.js#L42) | JS/TS 정규식 후보; AST 검증 아님 |
| `route_path` | [backend/transit.py:48](../backend/transit.py#L48) | 선택적 WGS84 [경도,위도] 경로를 Leaflet [위도,경도]로 변환한다. 손상 시 선만 생략한다. |
| `routeCard` | [frontend/js/place.js:309](../frontend/js/place.js#L309) | JS/TS 정규식 후보; AST 검증 아님 |
| `row` | [frontend/js/place.js:51](../frontend/js/place.js#L51) | JS/TS 정규식 후보; AST 검증 아님 |
| `run` | [utils/scripts/harness.py:63](../utils/scripts/harness.py#L63) | Execute finite static checks and optional isolated utility tests. |
| `safe_target` | [utils/scripts/reuse.py:18](../utils/scripts/reuse.py#L18) | Resolve a relative destination without traversal, links or Git internals. |
| `safeFallback` | [frontend/js/chat.js:753](../frontend/js/chat.js#L753) | JS/TS 정규식 후보; AST 검증 아님 |
| `sameRecommendationContext` | [frontend/js/chat.js:1119](../frontend/js/chat.js#L1119) | JS/TS 정규식 후보; AST 검증 아님 |
| `save` | [frontend/js/state.js:70](../frontend/js/state.js#L70) | JS/TS 정규식 후보; AST 검증 아님 |
| `savedCard` | [frontend/js/app.js:209](../frontend/js/app.js#L209) | JS/TS 정규식 후보; AST 검증 아님 |
| `savedPlaces` | [frontend/js/saved.js:12](../frontend/js/saved.js#L12) | JS/TS 정규식 후보; AST 검증 아님 |
| `savePlace` | [frontend/js/saved.js:27](../frontend/js/saved.js#L27) | JS/TS 정규식 후보; AST 검증 아님 |
| `saveVoiceLog` | [backend/team_chat.js:124](../backend/team_chat.js#L124) | JS/TS 정규식 후보; AST 검증 아님 |
| `say` | [frontend/js/chat.js:156](../frontend/js/chat.js#L156) | JS/TS 정규식 후보; AST 검증 아님 |
| `sayBye` | [frontend/js/place.js:138](../frontend/js/place.js#L138) | JS/TS 정규식 후보; AST 검증 아님 |
| `schedule_pair` | [backend/course.py:35](../backend/course.py#L35) | 두 구간과 당일 시간표를 합산해 가능·미확인·충돌 및 방문별 예상시각을 반환한다. |
| `screenContext` | [backend/team_voice_actions.js:5](../backend/team_voice_actions.js#L5) | JS/TS 정규식 후보; AST 검증 아님 |
| `script` | [backend/map_view.js:9](../backend/map_view.js#L9) | JS/TS 정규식 후보; AST 검증 아님 |
| `scrollEnd` | [frontend/js/chat.js:376](../frontend/js/chat.js#L376) | JS/TS 정규식 후보; AST 검증 아님 |
| `search` | [frontend/js/chat.js:1145](../frontend/js/chat.js#L1145) | JS/TS 정규식 후보; AST 검증 아님 |
| `search_input` | [backend/places.py:16](../backend/places.py#L16) | 검색어 1~80자와 keyword/address를 검증한다. 요청값을 오류에 되돌려 쓰지 않는다. |
| `search_origin` | [backend/places.py:27](../backend/places.py#L27) | 선택한 출발 좌표만 검색 중심으로 사용한다. 누락 시 전국 정확도순 동작을 유지한다. |
| `search_places` | [backend/places.py:93](../backend/places.py#L93) | 카카오에 검색어를 보내 후보를 반환한다. HTTP 상태·권한/쿼터/시간초과를 구분하고 비밀값은 숨긴다. |
| `searchOrigin` | [backend/team_chat.js:367](../backend/team_chat.js#L367) | JS/TS 정규식 후보; AST 검증 아님 |
| `searchPlaces` | [frontend/js/api.js:85](../frontend/js/api.js#L85) | JS/TS 정규식 후보; AST 검증 아님 |
| `selectContent` | [frontend/js/chat.js:207](../frontend/js/chat.js#L207) | JS/TS 정규식 후보; AST 검증 아님 |
| `send` | [backend/team_chat.js:387](../backend/team_chat.js#L387) | JS/TS 정규식 후보; AST 검증 아님 |
| `sendAgent` | [frontend/js/agent-session.js:105](../frontend/js/agent-session.js#L105) | JS/TS 정규식 후보; AST 검증 아님 |
| `sendAgentEvent` | [frontend/js/chat.js:1428](../frontend/js/chat.js#L1428) | JS/TS 정규식 후보; AST 검증 아님 |
| `seoul_page` | [backend/outing.py:81](../backend/outing.py#L81) | 지정일 키 없으면5건, 정식 키면 최대 1000건(SEOUL_FETCH_LIMIT)을 조회한다. 인증 실패를 sample로 대체하지 않는다. |
| `seoulWeather` | [frontend/js/weather.js:45](../frontend/js/weather.js#L45) | JS/TS 정규식 후보; AST 검증 아님 |
| `server_options` | [backend/preview.py:215](../backend/preview.py#L215) | 로컬 기본값을 유지하고 명시한 접속 주소·배포 환경의 PORT 범위를 검증한다. |
| `serverCategory` | [frontend/js/chat.js:28](../frontend/js/chat.js#L28) | JS/TS 정규식 후보; AST 검증 아님 |
| `setBig` | [frontend/js/place.js:239](../frontend/js/place.js#L239) | JS/TS 정규식 후보; AST 검증 아님 |
| `setMode` | [frontend/js/chat.js:475](../frontend/js/chat.js#L475) | JS/TS 정규식 후보; AST 검증 아님 |
| `setMode` | [frontend/js/place.js:363](../frontend/js/place.js#L363) | JS/TS 정규식 후보; AST 검증 아님 |
| `setSeasonArt` | [frontend/js/landing.js:36](../frontend/js/landing.js#L36) | JS/TS 정규식 후보; AST 검증 아님 |
| `setSound` | [frontend/js/chat.js:455](../frontend/js/chat.js#L455) | JS/TS 정규식 후보; AST 검증 아님 |
| `settings` | [backend/agent_v3.py:24](../backend/agent_v3.py#L24) | Resolve the same configured key/model only when the existing caller requests it. |
| `settings` | [backend/naito_chat.py:36](../backend/naito_chat.py#L36) | 앱 전용 환경변수/무시된 로컬 파일에서 키와 모델을 읽는다. 실제 값은 출력하지 않는다. |
| `short_text` | [backend/transit.py:41](../backend/transit.py#L41) | 이동 안내 원문을 길이 제한된 텍스트로 받아 HTML 실행 없이 표시하도록 반환한다. |
| `show` | [frontend/js/app.js:112](../frontend/js/app.js#L112) | JS/TS 정규식 후보; AST 검증 아님 |
| `show` | [frontend/js/chat.js:140](../frontend/js/chat.js#L140) | JS/TS 정규식 후보; AST 검증 아님 |
| `show` | [frontend/js/chat.js:577](../frontend/js/chat.js#L577) | JS/TS 정규식 후보; AST 검증 아님 |
| `showCards` | [frontend/js/chat.js:1197](../frontend/js/chat.js#L1197) | JS/TS 정규식 후보; AST 검증 아님 |
| `showConflicts` | [backend/team_chat.js:318](../backend/team_chat.js#L318) | JS/TS 정규식 후보; AST 검증 아님 |
| `showHistory` | [backend/team_chat.js:274](../backend/team_chat.js#L274) | JS/TS 정규식 후보; AST 검증 아님 |
| `showLiveTranscript` | [backend/team_chat.js:82](../backend/team_chat.js#L82) | JS/TS 정규식 후보; AST 검증 아님 |
| `showTransit` | [frontend/js/place.js:340](../frontend/js/place.js#L340) | JS/TS 정규식 후보; AST 검증 아님 |
| `showWalk` | [frontend/js/place.js:298](../frontend/js/place.js#L298) | JS/TS 정규식 후보; AST 검증 아님 |
| `signature` | [utils/scripts/watch.py:18](../utils/scripts/watch.py#L18) | Track eligible file names and metadata, excluding outputs and temp files. |
| `singleInput` | [backend/team_chat.js:509](../backend/team_chat.js#L509) | JS/TS 정규식 후보; AST 검증 아님 |
| `sky` | [frontend/js/weather.js:12](../frontend/js/weather.js#L12) | JS/TS 정규식 후보; AST 검증 아님 |
| `snapshot` | [utils/scripts/reuse.py:42](../utils/scripts/reuse.py#L42) | Preflight all selected blobs, then copy exactly without replacing files. |
| `snapshot` | [utils/scripts/team_chat_preview.py:20](../utils/scripts/team_chat_preview.py#L20) | 명시한 Git ref의 프론트만 해시별 경로에 복사한다. 기존 복사본은 덮어쓰지 않는다. |
| `snapshotListener` | [frontend/js/agent-session.js:10](../frontend/js/agent-session.js#L10) | JS/TS 정규식 후보; AST 검증 아님 |
| `source_files` | [utils/scripts/catalog.py:26](../utils/scripts/catalog.py#L26) | List supported source files in configured roots, excluding symlinks. |
| `speak` | [backend/team_chat.js:283](../backend/team_chat.js#L283) | JS/TS 정규식 후보; AST 검증 아님 |
| `speak` | [frontend/js/chat.js:411](../frontend/js/chat.js#L411) | JS/TS 정규식 후보; AST 검증 아님 |
| `speakKo` | [frontend/js/util.js:119](../frontend/js/util.js#L119) | JS/TS 정규식 후보; AST 검증 아님 |
| `spokenOriginChoice` | [frontend/js/chat.js:1382](../frontend/js/chat.js#L1382) | JS/TS 정규식 후보; AST 검증 아님 |
| `start` | [backend/location_view.js:46](../backend/location_view.js#L46) | JS/TS 정규식 후보; AST 검증 아님 |
| `start` | [frontend/js/chat.js:1252](../frontend/js/chat.js#L1252) | JS/TS 정규식 후보; AST 검증 아님 |
| `start` | [utils/scripts/loop.py:14](../utils/scripts/loop.py#L14) | Create an explicit task state with at most ten verification attempts. |
| `startDemo` | [frontend/js/saved.js:20](../frontend/js/saved.js#L20) | JS/TS 정규식 후보; AST 검증 아님 |
| `startLeaves` | [frontend/js/landing.js:46](../frontend/js/landing.js#L46) | JS/TS 정규식 후보; AST 검증 아님 |
| `status` | [backend/location_view.js:15](../backend/location_view.js#L15) | JS/TS 정규식 후보; AST 검증 아님 |
| `step_transport` | [backend/transit.py:66](../backend/transit.py#L66) | 공급자의 차량 이름·정류장 순서를 보존한다. 선택 필드 손상/누락은 미확인으로 남긴다. |
| `step_transport.label` | [backend/transit.py:68](../backend/transit.py#L68) | 선택적 공개 노선/역 이름만 길이를 제한해 받는다. 없으면 사실을 추정하지 않는다. |
| `stop` | [backend/location_view.js:25](../backend/location_view.js#L25) | JS/TS 정규식 후보; AST 검증 아님 |
| `stopListening` | [frontend/js/chat.js:638](../frontend/js/chat.js#L638) | JS/TS 정규식 후보; AST 검증 아님 |
| `stopSingleRecognition` | [backend/team_chat.js:502](../backend/team_chat.js#L502) | JS/TS 정규식 후보; AST 검증 아님 |
| `storageKey` | [frontend/js/state.js:34](../frontend/js/state.js#L34) | JS/TS 정규식 후보; AST 검증 아님 |
| `StoreError` | [backend/conversation_store.py:16](../backend/conversation_store.py#L16) | 원문·handle을 메시지에 노출하지 않는 동기화 오류와 현재 snapshot. |
| `StoreError.__init__` | [backend/conversation_store.py:19](../backend/conversation_store.py#L19) | HTTP 상태·안전한 코드와 독립 복사한 재동기화 자료를 보관한다. |
| `StoreError.as_response` | [backend/conversation_store.py:28](../backend/conversation_store.py#L28) | 허용된 호출자가 현재 상태를 재동기화할 API 오류 본문을 반환한다. |
| `StoreError.response` | [backend/conversation_store.py:40](../backend/conversation_store.py#L40) | 호출자가 오류 본문을 속성으로 읽을 수 있게 한다. |
| `summarize` | [backend/chat_conditions.py:63](../backend/chat_conditions.py#L63) | 코드로 누락·추천 입력·60분을 검사한다. ready는 S02a 진입 가능이며 추천 승인이 아니다. |
| `summary` | [frontend/js/chat.js:81](../frontend/js/chat.js#L81) | JS/TS 정규식 후보; AST 검증 아님 |
| `talkFor` | [frontend/js/util.js:93](../frontend/js/util.js#L93) | JS/TS 정규식 후보; AST 검증 아님 |
| `task` | [frontend/js/agent-session.js:53](../frontend/js/agent-session.js#L53) | JS/TS 정규식 후보; AST 검증 아님 |
| `tastes` | [frontend/js/chat.js:95](../frontend/js/chat.js#L95) | JS/TS 정규식 후보; AST 검증 아님 |
| `TeamAppTests` | [backend/test_team_app.py:11](../backend/test_team_app.py#L11) | 선택한 검증 복사본 외 파일을 요청할 수 없도록 경계를 검사한다. |
| `TeamAppTests.setUp` | [backend/test_team_app.py:14](../backend/test_team_app.py#L14) | 별도 임시 저장소에 공개 자산과 비밀 파일을 분리해 만든다. |
| `TeamAppTests.test_bad_selection` | [backend/test_team_app.py:42](../backend/test_team_app.py#L42) | 미설정/손상/외부 폴더 설정은 모두 미연결이다. |
| `TeamAppTests.test_traversal_and_private_files` | [backend/test_team_app.py:36](../backend/test_team_app.py#L36) | 퍼센트 인코딩·절대/역슬래시 경로와 비밀 확장자 요청은 거절한다. |
| `TeamAppTests.test_valid_assets` | [backend/test_team_app.py:30](../backend/test_team_app.py#L30) | 아래 경로의 index/JS와 query만 허용한다. |
| `testMode` | [frontend/js/api.js:37](../frontend/js/api.js#L37) | JS/TS 정규식 후보; AST 검증 아님 |
| `text` | [frontend/js/chat.js:575](../frontend/js/chat.js#L575) | JS/TS 정규식 후보; AST 검증 아님 |
| `text_or_none` | [backend/places.py:40](../backend/places.py#L40) | 공급자 텍스트를 제한된 길이로 읽고 공백·누락은 null로 유지한다. |
| `time_match` | [backend/outing.py:134](../backend/outing.py#L134) | 단순 전시 개방구간/공연 시작을 검사한다. 복합 운영규칙은 미확인(None)이다. |
| `to24` | [frontend/js/parse.js:23](../frontend/js/parse.js#L23) | JS/TS 정규식 후보; AST 검증 아님 |
| `todayIso` | [frontend/js/util.js:36](../frontend/js/util.js#L36) | JS/TS 정규식 후보; AST 검증 아님 |
| `ToolsTest` | [utils/tests/test_tools.py:25](../utils/tests/test_tools.py#L25) | Check behavior with independent fixtures rather than mirrored implementation. |
| `ToolsTest.git_repo` | [utils/tests/test_tools.py:46](../utils/tests/test_tools.py#L46) | Initialize only the disposable Git fixture; set fixture-local identity. |
| `ToolsTest.setUp` | [utils/tests/test_tools.py:28](../utils/tests/test_tools.py#L28) | Create a minimal isolated repository fixture and public harness config. |
| `ToolsTest.state` | [utils/tests/test_tools.py:52](../utils/tests/test_tools.py#L52) | Return a complete minimal context payload with no inferred policy. |
| `ToolsTest.test_commit_branch_and_report_guards` | [utils/tests/test_tools.py:180](../utils/tests/test_tools.py#L180) | Wrong branch and CRLF reports cannot pass commit preflight. |
| `ToolsTest.test_commit_deadline` | [utils/tests/test_tools.py:175](../utils/tests/test_tools.py#L175) | The exact Korean submission cutoff rejects a commit before touching Git. |
| `ToolsTest.test_complete_report_message_bytes` | [utils/tests/test_tools.py:235](../utils/tests/test_tools.py#L235) | Git stores the full Markdown report, not just a shortened subject. |
| `ToolsTest.test_conditional_python_function` | [utils/tests/test_tools.py:100](../utils/tests/test_tools.py#L100) | Functions declared under control flow remain discoverable. |
| `ToolsTest.test_context_preserves_next_actions` | [utils/tests/test_tools.py:122](../utils/tests/test_tools.py#L122) | A restart brief includes actionable next steps with their literal status. |
| `ToolsTest.test_context_rejects_unbounded_or_missing_data` | [utils/tests/test_tools.py:128](../utils/tests/test_tools.py#L128) | Oversized lists and absent sections fail instead of silently truncating. |
| `ToolsTest.test_copy_rejects_unsafe_targets` | [utils/tests/test_tools.py:138](../utils/tests/test_tools.py#L138) | Traversal, Windows drive paths, Git internals and backslashes are refused. |
| `ToolsTest.test_docstring_and_syntax_failures` | [utils/tests/test_tools.py:109](../utils/tests/test_tools.py#L109) | Missing documentation and syntax errors produce actionable diagnostics. |
| `ToolsTest.test_empty_overview` | [utils/tests/test_tools.py:105](../utils/tests/test_tools.py#L105) | Whitespace-only overviews yield an explicit missing-summary label. |
| `ToolsTest.test_hash_compares_bytes` | [utils/tests/test_tools.py:144](../utils/tests/test_tools.py#L144) | Different line endings are different original file bytes. |
| `ToolsTest.test_index_detects_body_change` | [utils/tests/test_tools.py:62](../utils/tests/test_tools.py#L62) | Changing only a function body invalidates the fingerprint index. |
| `ToolsTest.test_indexes_converge_without_recursive_hashes` | [utils/tests/test_tools.py:94](../utils/tests/test_tools.py#L94) | Generating indexes twice is a no-op even though outputs index themselves. |
| `ToolsTest.test_js_overview_and_exports` | [utils/tests/test_tools.py:77](../utils/tests/test_tools.py#L77) | Documented JS exports are discoverable without executing JavaScript. |
| `ToolsTest.test_link_checks_ignore_code_examples` | [utils/tests/test_tools.py:117](../utils/tests/test_tools.py#L117) | Relative missing links fail, while fenced placeholders and HTTPS do not. |
| `ToolsTest.test_loop_blocked_and_pass` | [utils/tests/test_tools.py:169](../utils/tests/test_tools.py#L169) | Blocked and successful tasks cannot silently restart themselves. |
| `ToolsTest.test_loop_duplicate_and_evidence` | [utils/tests/test_tools.py:159](../utils/tests/test_tools.py#L159) | Blind retries and empty evidence are rejected without mutating the original. |
| `ToolsTest.test_loop_limit_and_terminal_state` | [utils/tests/test_tools.py:151](../utils/tests/test_tools.py#L151) | A failed final attempt ends the loop and prevents further records. |
| `ToolsTest.test_pdf_review_masks_credential_context` | [utils/tests/test_tools.py:245](../utils/tests/test_tools.py#L245) | Credential lines and their immediate context stay out of review output. |
| `ToolsTest.test_pdf_review_preserves_korean_guidance` | [utils/tests/test_tools.py:252](../utils/tests/test_tools.py#L252) | Normal Korean workload and schedule notes remain available for review. |
| `ToolsTest.test_python_qualified_symbols` | [utils/tests/test_tools.py:56](../utils/tests/test_tools.py#L56) | Classes and async methods retain qualified names and source locations. |
| `ToolsTest.test_repository_inventory_and_secret_exclusion` | [utils/tests/test_tools.py:82](../utils/tests/test_tools.py#L82) | New arbitrary files enter repo indexes while secret file contents stay out. |
| `ToolsTest.test_snapshot_conflict_preflight` | [utils/tests/test_tools.py:195](../utils/tests/test_tools.py#L195) | A conflicting destination prevents all writes, including earlier files. |
| `ToolsTest.test_source_exclusions` | [utils/tests/test_tools.py:71](../utils/tests/test_tools.py#L71) | Excluded directories and reference snapshots never enter the code catalog. |
| `ToolsTest.test_staged_changes_rejected` | [utils/tests/test_tools.py:226](../utils/tests/test_tools.py#L226) | Existing staged work is not silently combined into a task commit. |
| `ToolsTest.test_watcher_detects_add_modify_delete` | [utils/tests/test_tools.py:215](../utils/tests/test_tools.py#L215) | Source additions, content changes and deletion alter the watcher signature. |
| `ToolsTest.test_watcher_excludes_its_outputs` | [utils/tests/test_tools.py:207](../utils/tests/test_tools.py#L207) | Generated outputs do not trigger another watcher cycle even without config hints. |
| `ToolsTest.write` | [utils/tests/test_tools.py:39](../utils/tests/test_tools.py#L39) | Write a temporary UTF-8 test file and return its location. |
| `toServerDraft` | [frontend/js/chat.js:718](../frontend/js/chat.js#L718) | JS/TS 정규식 후보; AST 검증 아님 |
| `toText` | [frontend/js/chat.js:706](../frontend/js/chat.js#L706) | JS/TS 정규식 후보; AST 검증 아님 |
| `track` | [backend/map_view.js:62](../backend/map_view.js#L62) | JS/TS 정규식 후보; AST 검증 아님 |
| `transit_between` | [backend/transit.py:139](../backend/transit.py#L139) | 좌표 두 개로 사용자 요청당 1회 조회한다. 미설정/인증/한도/빈 결과/실패를 구별한다. |
| `transitRoute` | [frontend/js/api.js:154](../frontend/js/api.js#L154) | JS/TS 정규식 후보; AST 검증 아님 |
| `TransitTests` | [backend/test_transit.py:19](../backend/test_transit.py#L19) | 비밀값 비노출·단위·미연결·잘못된 좌표·HTTP200 오류·한도를 독립적으로 검사한다. |
| `TransitTests.setUp` | [backend/test_transit.py:22](../backend/test_transit.py#L22) | 실제 사용자 위치와 무관한 공개 장소 좌표를 준비한다. |
| `TransitTests.test_bad_payloads` | [backend/test_transit.py:93](../backend/test_transit.py#L93) | 음수·누락·잘못된 이동수단·손상된 성공 응답을 정상이 아닌 것으로 처리한다. |
| `TransitTests.test_missing_access_walk` | [backend/test_transit.py:38](../backend/test_transit.py#L38) | 실응답처럼 지하철만 표시되어도 생략된 접근/마지막 도보를 0으로 확정하지 않는다. |
| `TransitTests.test_normalization` | [backend/test_transit.py:26](../backend/test_transit.py#L26) | 초/m/환승/요금 및 미확인 요금을 보존한다. |
| `TransitTests.test_optional_vehicle_metadata_is_not_guessed` | [backend/test_transit.py:62](../backend/test_transit.py#L62) | 누락/손상된 노선·역 이름을 안내문에서 추측하지 않고 HTML 문자도 평문으로 전달한다. |
| `TransitTests.test_request_and_provider_errors` | [backend/test_transit.py:112](../backend/test_transit.py#L112) | 헤더만 키를 담고 날짜는 보내지 않으며 인증·한도·통신·본문 오류를 구분한다. |
| `TransitTests.test_route_geometry` | [backend/test_transit.py:73](../backend/test_transit.py#L73) | 경위도 순서를 검증하고 손상/누락 경로선 때문에 텍스트 안내까지 잃지 않는다. |
| `TransitTests.test_unconfigured_and_coordinates` | [backend/test_transit.py:104](../backend/test_transit.py#L104) | 미설정 시 외부 호출을 하지 않고 입력 누락·중복 좌표는 거절한다. |
| `TransitTests.test_vehicle_and_stops` | [backend/test_transit.py:49](../backend/test_transit.py#L49) | 호선/버스 이름과 승하차를 실제 응답 필드에서만 보존하며 대체 노선도 유지한다. |
| `typeIcon` | [frontend/js/util.js:137](../frontend/js/util.js#L137) | JS/TS 정규식 후보; AST 검증 아님 |
| `unlockSpeech` | [frontend/js/util.js:104](../frontend/js/util.js#L104) | JS/TS 정규식 후보; AST 검증 아님 |
| `updateContentSelectionButton` | [frontend/js/chat.js:193](../frontend/js/chat.js#L193) | JS/TS 정규식 후보; AST 검증 아님 |
| `updateVoiceUi` | [frontend/js/chat.js:486](../frontend/js/chat.js#L486) | JS/TS 정규식 후보; AST 검증 아님 |
| `useHere` | [frontend/js/chat.js:1016](../frontend/js/chat.js#L1016) | JS/TS 정규식 후보; AST 검증 아님 |
| `userSays` | [frontend/js/chat.js:163](../frontend/js/chat.js#L163) | JS/TS 정규식 후보; AST 검증 아님 |
| `validate` | [backend/outing.py:40](../backend/outing.py#L40) | 개인 장소 요청을 검증하고 한국 시각의 당일 구간과 출발점을 반환한다. |
| `validate_request` | [backend/naito_chat.py:49](../backend/naito_chat.py#L49) | 짧은 발화/대화와 초안 revision을 검증한다. 오류에 사용자 원문을 포함하지 않는다. |
| `verify_message` | [utils/scripts/commit_report.py:17](../utils/scripts/commit_report.py#L17) | Compare raw latest-commit message bytes to the complete report file. |
| `visit_window` | [backend/course.py:11](../backend/course.py#L11) | 행사 시간 원문에서 검증 가능한 당일 시작·종료와 고정 공연 여부를 얻는다. |
| `visitLine` | [frontend/js/place.js:23](../frontend/js/place.js#L23) | JS/TS 정규식 후보; AST 검증 아님 |
| `visitorNamespace` | [frontend/js/state.js:20](../frontend/js/state.js#L20) | JS/TS 정규식 후보; AST 검증 아님 |
| `voiceAction` | [backend/team_voice_actions.js:26](../backend/team_voice_actions.js#L26) | JS/TS 정규식 후보; AST 검증 아님 |
| `VoiceSession` | [backend/voice_session.js:127](../backend/voice_session.js#L127) | JS/TS 정규식 후보; AST 검증 아님 |
| `voiceSettings` | [backend/team_chat.js:463](../backend/team_chat.js#L463) | JS/TS 정규식 후보; AST 검증 아님 |
| `wait` | [frontend/js/chat.js:438](../frontend/js/chat.js#L438) | JS/TS 정규식 후보; AST 검증 아님 |
| `wait_for` | [utils/scripts/verify_watch.py:14](../utils/scripts/verify_watch.py#L14) | Wait a bounded period for generated evidence or report the failed phase. |
| `waitForSpeech` | [backend/voice_session.js:28](../backend/voice_session.js#L28) | JS/TS 정규식 후보; AST 검증 아님 |
| `wake` | [frontend/js/app.js:153](../frontend/js/app.js#L153) | JS/TS 정규식 후보; AST 검증 아님 |
| `wakeServer` | [frontend/js/api.js:19](../frontend/js/api.js#L19) | JS/TS 정규식 후보; AST 검증 아님 |
| `walk_between` | [backend/walking.py:98](../backend/walking.py#L98) | 두 행사 좌표로 도보 예상 초·m를 얻는다. 잘못된 입력과 조회 실패를 구분한다. |
| `walking_details` | [backend/walking.py:76](../backend/walking.py#L76) | 같은 공급자 응답에서 한국어 단계·m·경로 인덱스·좌표를 검증해 반환한다. |
| `WalkingTests` | [backend/test_walking.py:9](../backend/test_walking.py#L9) | 경로선 정밀도와 손상된 단계 응답을 검증한다. |
| `WalkingTests.setUp` | [backend/test_walking.py:12](../backend/test_walking.py#L12) | 두 지점과 짧은 공급자 응답을 독립적으로 준비한다. |
| `WalkingTests.test_bad_steps` | [backend/test_walking.py:38](../backend/test_walking.py#L38) | 지도 밖 단계나 영어 대체 응답을 한국어 안내 성공으로 표시하지 않는다. |
| `WalkingTests.test_detail_and_summary` | [backend/test_walking.py:28](../backend/test_walking.py#L28) | 기존 요약 응답을 유지하고 상세 요청에만 단계와 경로선을 추가한다. |
| `WalkingTests.test_polyline_precision` | [backend/test_walking.py:20](../backend/test_walking.py#L20) | 공개 polyline 예제의 정수 값을 백만분의 일 도 단위로 해독한다. |
| `walkRoute` | [frontend/js/api.js:131](../frontend/js/api.js#L131) | JS/TS 정규식 후보; AST 검증 아님 |
| `wantsAnyCategory` | [frontend/js/chat.js:732](../frontend/js/chat.js#L732) | JS/TS 정규식 후보; AST 검증 아님 |
| `watchBottom` | [frontend/js/chat.js:385](../frontend/js/chat.js#L385) | JS/TS 정규식 후보; AST 검증 아님 |
| `withPreferences` | [backend/team_preferences.js:9](../backend/team_preferences.js#L9) | JS/TS 정규식 후보; AST 검증 아님 |
| `write_indexes` | [utils/scripts/catalog.py:211](../utils/scripts/catalog.py#L211) | Write changed outputs only, allowing repeated watcher runs to be quiet. |
| `writeStore` | [frontend/js/util.js:75](../frontend/js/util.js#L75) | JS/TS 정규식 후보; AST 검증 아님 |
