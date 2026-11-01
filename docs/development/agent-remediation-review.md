# 대화·추천 에이전트 개선 및 재검토 자료

검증일: 2026-11-01, Asia/Seoul. 대상 브랜치: `dj/agent`. 비교 기준: `origin/develop`의 `1876fe6`(이번 게시 준비 중 fetch로 재확인). 이번 결함 보완 전 HEAD는 `3c88433`이다. 후속 커밋과 최종 PR의 head SHA는 Git 이력을 기준으로 확인한다.

공유 자료: [검토 이슈 #67](https://github.com/Lab678-Hackathon/lab678/issues/67), [develop 대상 PR #68](https://github.com/Lab678-Hackathon/lab678/pull/68). PR 생성 후 열린 상태·미병합을 확인했다. 구현 검증 기준 커밋은 `c453e30`이며 이후 게시 기록 커밋은 문서·상태·색인만 갱신한다.

## 목적과 승인 범위

대화로 모은 조건이 추천까지 유지되고, 모호한 내용을 사용자가 바로잡으면 정상적으로 진행되도록 수정했다. 사용자가 검토 결과를 받은 뒤 “개선계획 세우고 개선해”라고 승인했다. 이후 “끝나면 push하고 issue에 작업내용 개선내용 테스트 내용 다른 LLM이 분석할수 있는 자료 다 올려주고 develop으로 pr해줘 머지는 하지마”라고 요청했다. 변경은 `dj/agent`에 기록하고 `develop` 대상 PR로 제출하며 병합·자동 병합·배포는 실행하지 않는다.

앞선 계획의 A~D에 해당하는 대화·추천·카드와 관련 테스트가 대상이다. 운영/예약 확인 정책, 최대 검색 반경, 추가 음성 공급자, 신규 계정/저장 정책은 이번에 임의 확정하지 않았다. 기능 수정 전 존재하던 미커밋 변경은 보존해 통합·검증했다.

## develop 대비 기능 묶음

| 묶음 | 변경 내용 | 주요 파일 |
|---|---|---|
| 발화 근거 검증 | 모델 제안과 이번 발화의 원문 근거·시각을 대조. 없는 장소/시각·모호한 조건은 보류. 세 공급자가 같은 검증을 사용 | `backend/chat_grounding.py`, `chat_prompt.py`, `naito_chat.py` |
| 음성·대화 조작 | 듣는 중 ‘말씀 끝 · 보내기 ▶’, 다시 말하기, 처리 중 입력 보존, 취소된 응답 무시 | `frontend/js/chat.js` |
| 조건 전달·주소 확인 | 무료/예산/관심사/제외 조건 왕복, 주소가 있는 출발지 후보, 선택·변경 동의 전 기존 좌표 유지 | `frontend/js/chat.js`, `backend/chat_conditions.py` |
| 카드 표시 | 카드 폭·글자·상세 버튼 확대, 서버 순위와 추천 사유·조회 범위·확인 필요 항목 표시 | `frontend/css/app.css`, `frontend/js/chat.js` |
| 상태 전이 결함 보완 | 후보 검색 조건 보존, 이전 카드 스냅샷, 정확한 단독 명령 처리, 관련 보류만 해제, 늦은 요청 무시 | `frontend/js/chat.js`, `state.js` |
| 의미 검증 보완 | 무료/출발지/분류/실내외/장소 수의 부정·정정, 제외 금지, 관심어 임의 삭제 차단 | `backend/chat_grounding.py`, `chat_conditions.py` |
| 검증·인계 | 대화/추천 UI 모의, 독립 상태 회귀 15개, 실제 브라우저·로컬 HTTP 연결, 실행 안내·색인 | `utils/scripts/check_agent_*.cjs`, `agent_http_fixture.py`, 관련 백엔드 테스트 |

브랜치에는 이전 작업의 운영 규칙·승인 기록·보고문·생성 색인도 포함된다. 이 문서는 기능 검토 시작점이며, 다른 LLM은 실제 `git diff origin/develop...HEAD`와 현재 PR 파일 목록을 기준으로 검토 범위를 확정해야 한다.

## 확인한 결함과 수정 후 동작

이전 대화 이해 개선을 포함한 develop 대비 전체 목록과 커밋별 근거는 [이슈67](https://github.com/Lab678-Hackathon/lab678/issues/67)의 ‘develop 대비 전체 개선 목록’에 기록했다. 원문 근거·출발/목적지·KST 날짜/시각·부분 보류·같은 값 재확인·관람료 예산·선호 보존을 각각 구분한다. develop부터 존재한 문맥 전달·음악 프롬프트·공급자 어댑터·추천 엔진과 이번의 검증/화면 연결 개선을 중복 주장하지 않는다.

시간 검증은 보수적이다. ‘오후2시부터5시까지’의 뒤 시각에 오후를 자동 상속하지 않으며 ‘오후2시부터 오후5시까지’처럼 명확한 양끝을 요구한다. `11월2일`, `11/2`, 다음주/요일·상대 지연 등 현재 미지원 표현은 보류한다. 실제 모델의 대화 품질 향상률을 측정한 결과는 아니다.

| 재현 조건 | 수정 전 | 수정 후 / 회귀 |
|---|---|---|
| 유료 후보 → 무료만 수락 → 검색 0건 또는 오류 → 다른 곳/가까운 곳 | 옛 유료 후보에 ‘무료만’ 요약을 붙여 다시 표시 | 후보 검색 당시 요청·화면 분류를 `poolContext`에 저장. 현재 조건과 다르면 새 조건으로 검색, 옛 카드는 원래 요약 유지 |
| 같은 ID 행사에 새 출발지 기준 거리가 반환 | 과거 카드까지 새 거리로 변경 가능 | 메시지별 `cardSnapshots`로 과거 카드의 거리·사유 보존 |
| 시간 보류 → ‘오후 2시–5시’ 선택 | 값이 바뀌어도 보류가 남아 추천 0회 | 명시 선택한 시각에 해당하는 보류 해제, 다른 보류 유지 |
| 출발지 보류 → 검색 → 선택 → 변경 수락/거절 | 수락해도 출발지 보류 반복 | 수락/GPS 성공 때 관련 보류만 해제, 거절·무관 답변은 유지 |
| 무료 변경과 새 출발지를 한 번에 요청 | 무료 확인 직후 장소 미선택 상태로 기존 위치 검색 가능 | 출발지 후보가 남으면 선택·동의까지 기다림 |
| ‘무료만 가능한 가까운 곳’ | 해석 API를 생략하고 옛 후보 정렬 | 정확한 단독 명령만 빠르게 처리, 복합 문장은 해석·확인 후 검색 |
| 기존 서울 ‘시청’ → ‘출발지는 시청으로 바꿔줘’ | label이 같으면 검색 생략 | 같은 label도 후보 재검색. 주소·좌표 선택 및 동의 후 반영 |
| ‘서울역에서 출발하면 안 돼요’에 서울역 후보 | 잘못된 출발지 수용 | 보류. 명확히 정정한 새 출발지는 수용 |
| ‘무료만 아닌 유료도 괜찮아요’에 무료만 후보 | 반대 조건 수용 | 반대 후보 보류, 유료 허용 후보는 수용 |
| 기존 관심어 미술 + ‘전시 좋아’에 빈 관심어 후보 | 미술 삭제 | 명시 해제 없는 삭제 보류. 관심어 개별/전체 해제는 허용 |
| 실외를 원했는데 indoor, 음악 거절인데 음악 분류, 한 곳인데 course | 인용만 맞으면 수용 가능 | 조건별 긍정·부정·정정·수량 검사, 불명확하면 보류 |
| 다른 곳 검색/GPS/장소 검색 응답 전에 새 대화 시작 | 오래된 응답이 새 상태에 적용될 위험 | 요청 세대·조건 일치 여부를 검사해 오래된 응답 무시 |

서버 의미 검증 사례는 **잘못된 모델 후보를 주입한 방어 회귀**이다. 실제 모델이 그러한 오답을 냈거나 그 빈도를 측정했다는 뜻이 아니다. 일반적인 부정 표현과 명시적 정정을 검사하지만 모든 한국어 의미를 규칙으로 완전히 판정한다는 보장은 없다. 불명확한 이중 부정은 추가 질문으로 보류한다.

## 상태·API 계약을 읽는 순서

1. `frontend/js/state.js`: draft, pending/pendingQueue, clarification, lastRequest, poolContext, messages/cardSnapshots.
2. `frontend/js/chat.js`: `handle` → `interpret` → `patch` → `applyClarificationEvidence`/`confirmExplicitChoices` → `next` → `search`. `other`/`closer`는 동일한 추천 허용 조건을 검사한다.
3. `backend/naito_chat.py`: 요청 검증 → 외부 모델 응답 파싱 → `ground_payload` → `apply_interpretation` → 보류·검증된 필드 메타데이터 반환.
4. `backend/chat_grounding.py`: 문자 인용 일치와 별도로 조건별 의미·시각 검사. `backend/chat_conditions.py`: 초안 병합/충돌과 출발지 재검색 경계.
5. `backend/outing.py`, `preferences.py`, `places.py`: 사실 데이터와 추천·필터·좌표 정규화. LLM은 장소 좌표·요금·운영 사실을 생성하지 않는다.

기존 대화 API에 추가된 선택 필드는 `interpretation_status`, `clarification_fields`, `interpreted_fields`다. `clarification_fields`는 보류할 필드명, `interpreted_fields`는 이번 발화에서 검증된 후보의 필드명이다. 값이나 원문을 메타데이터에 추가하지 않는다. 해석된 검색어가 있다고 출발 좌표가 확정된 것은 아니므로 실제 장소 선택/동의가 필요하다. 이번 후속 수정은 외부 API 스키마를 추가로 바꾸지 않았다.

`poolContext`와 `cardSnapshots`는 브라우저 세션 상태다. 구버전 세션에 검색 맥락이 없으면 기존 pool을 새 결과로 재사용하지 않고 다시 검색한다. 과거 카드의 스냅샷 보존은 대화 표시 범위이며, 상세 페이지는 기존처럼 전역 최신 후보 데이터를 사용한다.

## 실제 실행 결과

| 명령 | 결과 | 검증 범위 |
|---|---|---|
| `python -X utf8 -m unittest discover -s backend -p test_*.py` | 134 PASS | 기존126 + 후속 회귀8, 각 테스트에 여러 표현 subtest 포함. 실제 로컬 HTTP 요청과 CORS 허용/거부 포함 |
| `node utils/scripts/check_agent_dialogue.cjs` | PASS | 실제 앱 DOM, 모의 API/STT. 보류·재입력·경합·키 없는 단답·위치 권한·분류 전환 |
| `node utils/scripts/check_agent_recommendation.cjs` | PASS | 조건 왕복·서버 순위·거리순·0건·오류·주소 선택·혼합 조건 확인 |
| `node utils/scripts/check_agent_regressions.cjs` | 15 PASS / 0 FAIL | 위 상태 전이, 취소, GPS, 카드 맥락 보존 등 독립 회귀 |
| `node utils/scripts/check_agent_http.cjs` | PASS | 실제 브라우저 CORS → 별도 로컬 Preview HTTP → 실제 grounding/병합/장소 정규화/추천 필터. 외부 공급자만 모의 |
| `node --check` | PASS | chat/state와 위 CJS 파일 4개 |
| `git diff --check` | PASS | 패치 공백 검사 |
| `python -X utf8 utils/scripts/harness.py --tests` | 도구26 PASS, 정적7건 잔존 | 기존 테스트 docstring 누락. 아래 상세와 구분 |

추천 UI 테스트가 이전에 실패한 직접 원인은 fixture가 모든 턴에서 `free_only=false`를 강제로 덮어써 직전 무료 조건과 충돌시킨 것이다. fixture는 현재 조건을 유지하도록 고쳤으며, 별도로 실제 복합 조건/출발지 충돌을 회귀에 추가했다. 타임아웃을 늘리거나 assertion을 제거해 통과시키지 않았다.

하네스의 기존 정적 실패는 `backend/test_contact.py` 모듈/클래스/메서드 docstring 6건과 `backend/test_culture_sources.py`의 `OfficialImageTest` docstring 1건이다. 이번 서비스 결함 보완과 무관한 기존 파일은 수정하지 않았다. 생성 색인 stale은 갱신해 해소했다. 하네스 전체 PASS로 보고하지 않는다.

## 재실행

저장소 루트에서 위 명령을 실행한다. 프론트는 정적 파일이며 별도 빌드가 없다. 브라우저 검증에는 Node, Python, Playwright와 Chromium/Chrome이 필요하다. 필요한 경우 `PLAYWRIGHT_MODULE`(설치된 모듈 경로), `CHROMIUM_PATH`(브라우저 실행 파일), `PYTHON`을 지정한다. 의존성을 자동 설치하거나 서비스 환경을 바꾸지는 않는다.

`check_agent_http.cjs`는 임시 loopback 서버 두 개를 띄우고, `agent.localhost`의 프론트에서 `127.0.0.1`의 백엔드로 실제 CORS 요청을 한다. HTML의 API 메타데이터는 테스트 응답에서만 치환하며 저장소 프론트 파일은 바꾸지 않는다. `agent_http_fixture.py`는 실제 환경 설정을 읽는 함수와 외부 공급자 호출을 고정하고 외부 소켓 연결을 차단한다. 서버·브라우저는 테스트 종료 시 정리한다.

테스트 데이터는 합성이므로 실제 행사가 있다는 증거가 아니다. 정식 실행 데이터는 기존 문화 API 경로가 결정한다. 키·실제 환경 파일·개인 보존본은 이 자료에 포함하지 않는다.

## 다른 LLM 검토 요청

- `origin/develop...HEAD`의 코드와 테스트를 함께 읽고 결과가 사용자 조건을 보존하는지 독립 검토한다. 테스트 통과를 실서비스 QA 완료로 해석하지 않는다.
- 가격/장소/시각/관심사 변경 후 0건·오류·취소·새 대화 경계를 우선 확인한다. 특히 여러 필드의 수락/거절 순서와 같은 값 재확인을 검사한다.
- grounding의 정상 표현 과잉 차단 및 누락된 부정/정정 표현을 검토한다. 새로운 반례는 사용자 발화·주입 후보·기존 draft·기대값·실제값을 함께 기록한다. 실제 모델 응답 관측과 후보 주입 검사를 분리한다.
- 실제 기기의 STT/TTS·레이아웃, 실 AI/공공 API, 배포 환경의 origin/키/프론트·백엔드 버전 일치는 별도 QA가 필요하다. 이번 수정으로 모두 완료됐다고 주장하지 않는다.
- 운영·예약 정보가 불명확한 후보의 기본 노출 정책 등 E 범위는 기존 계획의 미정/별도 검토 상태를 확인하고 임의 변경하지 않는다.

완료 보고문은 `docs/development/reports/20261101-agent-remediation-*.md`에 보존한다. PR에서 팀이 기능·문서 변경을 선택해 검토하고 병합 여부를 결정한다.
