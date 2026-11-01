# develop 기반 엔진 이식 실행 체크리스트

2026-11-01 · target `dj/develop` · base `e5697e2` · source code `b6355a0` / source docs `d541ea5`.

승인/경계는 [실시계획](agent-engine-migration-plan.md), 원본 설계는 [개발 명세](agent-implementation-spec.md)를 따른다. 이 파일은 실행한 사실만 체크한다. 실제 마이크/GPS/시각·실모델을 모의 통과로 표시하지 않는다.

## M0 원본 보존·문서 제시 — 완료

- [x] source runtime/QA 원자 커밋 b6355a0 push·원격 SHA 확인
- [x] 상세 명세·계획/체크표 d541ea5 push·사용자에게 링크 제시
- [x] 기존 이슈67 전면 개편·PR68 본문 갱신, 이전 본문 별도 보존
- [x] ‘저장하고 보여주고 시작해’, ‘체크리스트…실행 점검 보완’ 실시 승인 기록

## M1 깨끗한 대상과 기준선 — 완료

- [x] 최신 원격 develop e5697e2 재확인
- [x] 이전 local80d481b를 dj/develop-before-engine-20261101 이름에만 보존
- [x] 소유 backend33148/frontend28644 명령 확인·종료 재확인
- [x] 새 local dj/develop=e5697e2 생성, 제품 tree diff0·upstream 미지정 확인
- [x] 두 명세/계획 문서를 packet SHA 확인 후 같은 상대 경로로 복사
- [x] 대상 baseline backend134/134·utils26/26·offline chat API PASS
- [x] baseline 하네스 docstring7건·문서 복사로 인한 stale index3건 별도 기록
- [x] 보호21파일 SHA256 보존: assets/weather/util/saved, index/CSS는 최소 UI 예외 검토

## M2 서버 엔진 — 완료

- [x] core4 신규 모듈 source byte 일치 확인
- [x] agent_v3.py 실행부 분리, 기존 naito_chat은 version-dispatch3줄만 추가
- [x] legacy SYSTEM/응답/실제 도메인 모듈 보존, V3_SYSTEM만 추가
- [x] places 거리/분류 delta와 restore32KiB 조건부 경계 선택 적용
- [x] 전체 target backend241/241·표적141/141 PASS
- [x] chat_grounding/chat_conditions/outing/preferences/culture_config/contact 기준 blob 동일
- [x] 실제 HTTP→기존 preview→새 엔진 경계 통합 확인

## M3 최소 화면 연결 — 완료

- [x] 신규 session adapter와 기존 API/상태의 작은 접점
- [x] 기존 말풍선/카드·STT·hashrouter 유지, v3에서 기존 필수 설정 루프 우회
- [x] 현재 server batch 순서 렌더, 선택 버튼/상세/번호 동일 ID
- [x] 실제 모호한 출발지만 후보 팝업, 명확한 장소 자동 채택·명시 GPS 요청
- [x] 후보별 상세/지도 context, 화면 이탈 음성 정지·복귀 상태 보존
- [x] 허용 HTML/CSS 국소 diff 설명·보호 자산/날씨/저장 정책 동일성 확인

## M4 독립 전체 흐름 — 완료

- [x] target 기준 fixture·HTTP/DOM 계약 점검, 원본 성적을 재사용하지 않음
- [x] 전시/공연/산책·부분 정정·정상 빈 의미·오류·0건 구분
- [x] 두 번째 묶음3번/버튼/상세 동일 ID, 선택 모델/원천 추가0
- [x] stale/foreign/date조건 변경·중복/복원/늦은 응답 차단
- [x] 기존 legacy/API/지도/전화/저장·날씨·체험 흐름 회귀
- [x] 실제 발견 결함의 원인·최소 수정·표적 재검증 기록
- [x] target 전체 단위·문법·diff·문서/색인 정합 최종 확인

## M5 인계 — 완료

- [x] target 실제 성적/한계·파일 범위·보호 diff 기록
- [x] 기존 이슈67/PR68에 target 결과와 소스 성적을 구분해 갱신
- [x] 현재 target 서버·프론트 제공 파일/버전 일치·lease 연결 확인
- [x] 사용자 테스트 주소·진행 방법 안내, 실기기 QA 구분

## 실행 결과 장부

| 시점/범위 | 실제 결과 | 남은 점 |
|---|---|---|
| M1 clean base | backend134 PASS, utils26 PASS, offline chat API PASS | docstring7기존·계획복사색인stale3 관측 |
| M2 서버 최종 | backend241 PASS, 표적141 PASS, backend diff check PASS | 프론트/독립 HTTP 아직 진행 |
| M3 첫 연결·독립 검사 | 선택→상세 상태는 유지, 대화 복귀 후 모의 TTS 1회 추가 재생 관측 | 음성 재시작 금지 기준은 미통과. 프론트 담당이 원인을 수정하고 같은 assertion으로 재검증 중 |
| M3 일반 복귀 보완 | 기존 클릭 handler의 unlockSpeech 무음 utterance가 원인. 첫 대화/명시 음성 시작 때만 unlock하여 일반 상세 뒤로 TTS 추가0 통과 | util.js를 바꾸지 않고 연결부만 수정 |
| M3 native back 표적 | 음성 URL→선택 상세→브라우저 뒤로에서 모의 STT1→2/TTS3→4 추가 실행을 별도 재현 | 명시 홈 버튼 시작과 URL/뒤로/새로고침 복귀를 구분하는 작은 라우팅 분기로 수정·재검증 중. assertion 완화0 |
| M3 native/늦은 선택 보완 | 명시 홈 시작만 새 음성 모드로 처리하고 나머지 기존 대화 복귀는 resume. nativeback 음성0·선택 응답 지연 뒤 홈 유지 포함 DOM23 첫 실행 PASS | 다음 복제탭 강화 조건을 추가 확인 |
| M3 복제탭 강화 | 기존 fork 검사를 sound=true/mode=voice로 강화해 대화 격리는 통과하지만 자동 TTS1회 재현 | onFork 인사만 silent 말풍선으로 바꾸고 사용자 sound/mode는 보존. 같은 DOM23의 강화 assertion으로 최종 재실행 중 |
| M3~M4 최종 | 강화 fork·일반뒤로·nativeback·지연 선택 후 홈 유지 포함 실제 HTTP/DOM **23/23 PASS** | 모든 발견된 음성 경계 수정 후 동일 assertion 통과. 보호 assets/weather/util/saved/tokens 변경0 |
| M4 기존 검사 | legacy 상태 **15/15**, 기존 HTTP·대화·추천 검사 PASS, JS/Python 문법·diff PASS | 기존 검사 진입 쿼리만 agent=legacy 명시, 핵심 assertion 완화0 |
| M4 오프라인 하네스 | 도구 **26/26 PASS**, 새 정적 오류0·문서/색인/상태 정합 PASS | 전체 하네스는 기준부터 있던 docstring7건으로 FAIL. 계획 복사로 생긴 stale3건은 생성 색인 갱신으로 해소 |
| M5 로컬 준비 | backend **7256**/frontend **32388**, http://127.0.0.1:5173/ · 제공8파일 일치·v3 open·미검증 선택 거절·모델0·lease release PASS | 실제 모델/원천·마이크/GPS·시각 시험 아님. Ctrl+F5 후 새 대화로 사용자 확인 |

허용한 UI 차이는 출발지 dialog HTML10줄·해당 .origin-* CSS12줄이며 상단/홈/아이콘/전역 토큰·레이아웃은 유지했다. 기존 JS는 전송/state/render/선택/복귀의 최소 접점만 바꾸고 세션 실행부는 신규 agent-session.js로 분리했다. 서버 legacy 파일은 lazy version 분기3줄만 추가했고 기존 SYSTEM과 실제 판정/문화 모듈은 보존했다.

검사 준비 중 초기 handshake 직후 canonical 상태가 null인 현상을 한 번 관측했으나 이후 재현되지 않았고 직접 원인은 미확정이다. 이를 제품 결함 수정 완료나 원인이 확정된 하네스 문제라고 주장하지 않는다. 최종 동일23개 시나리오는 통과했으며 실제 사용자 평가에서 같은 현상이 보이면 해당 대화/응답 경계를 추가 수집한다.

기존 이슈67을 소스 전체 명세·승인 계획·대상 실제 체크리스트/결과로 전면 갱신했고, PR68 본문도 같은 소스/대상 구분으로 갱신 후 재조회 일치했다(각35463자/27101자). PR68은 외부 과거 병합 기록이며 새 PR·병합을 하지 않았다. 대상 엔진은 현재 로컬 미커밋이며 원격 dj/develop80d481b를 새 이식본이라고 표시하지 않았다.

기존 source253/19/9와 위 target 결과는 다른 성적이다. 이식은 새 단일 프로세스/대화 store 계약을 검증하며, 새 데이터 연동·예매·회차·DB/인증·전체 내비게이션 재설계를 포함하지 않는다. 실패가 남으면 해당 단계는 체크하지 않는다.

## 후속 게시 승인과 비교 근거

사용자는 실제 시험 후 **“이대로 푸시 … 이슈 … 자세히 … PR발행해”**라고 명시했다. 앞선 로컬 미게시 상태는 이 최신 지시로 갱신하며, 같은 이름의 이전 원격 tip 보존과 기대 SHA lease를 포함한 게시 절차를 별도 체크표로 기록했다. 새 PR은 develop을 대상으로 하며 병합하지 않는다.

| 같은 e5697e2 기준의 프론트 변경 | 원본 dj/agent b6355a0 | 선택 이식본 |
|---|---:|---:|
| index.html·app.css | +30 / -3 | +22 / -0 |
| api.js·state.js | +89 / -6 | +51 / -3 |
| chat.js·신규 agent-session.js | +719 / -36 | +484 / -18 |
| app.js·place.js | +172 / -13 | +76 / -8 |
| saved.js | +4 / -1 | 변경0 |
| 합계 | 기존8파일 +1014/-59 =1073변경행 | 기존7+신규1파일 +633/-29 =662변경행 |

새 adapter132줄도 대상 합계에 포함했다. 변경행은 검토 범위 지표이며 기능 품질/UX의 정량 점수가 아니다. HTML은 dialog10줄, CSS는 origin 전용12줄을 제외하면 기준과 동일하다. assets16개·weather/util/saved/tokens/landing/parse는 변경0이다. 전체 history 엔진/이전·홈 아이콘 신설을 옮기지 않고 기존 hashrouter와 화면을 유지했다.
