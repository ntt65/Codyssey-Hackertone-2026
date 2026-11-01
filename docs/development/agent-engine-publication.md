# develop 기반 엔진 선택 이식 게시 결과

2026-11-01 · 게시 브랜치 `dj/develop` · [PR69 → develop](https://github.com/Lab678-Hackathon/lab678/pull/69) · [상세 이슈67](https://github.com/Lab678-Hackathon/lab678/issues/67). PR은 검토용으로 발행했으며 병합·배포하지 않았다.

## 조상과 이식 방식

검증 코드 커밋은 `e7163aafa871d8cda2122ec3658b9bbd7f174b9d`다. 유일한 직접 부모는 기준 develop `e5697e21d02b76336c6db7fe2208675f9aff6ca4`이며, `dj/agent`의 검증 코드 `b6355a0`는 이 커밋의 조상이 아니다. 즉 원본 브랜치 전체를 merge하지 않고 깨끗한 develop에 필요한 엔진/연결부만 선택 적용했다. `dj/agent` 원본 코드·명세는 `b6355a0`/`d541ea5`로 보존했다.

동명 이전 원격 `dj/develop`의 `80d481b`는 `dj/develop-before-engine-20261101`에 먼저 보존했다. 기존 원격이 여전히 그 SHA일 때만 lease를 적용해 검증본으로 갱신했다. 원격이 바뀌었다면 덮지 않는 절차이며, `develop`과 `main`의 tip은 변경하지 않았다. 최초 생성한 PR69는 base develop/e5697e2, head dj/develop/e7163aa, 구현+검사+명세44파일의 단일 커밋이었다. 이후 게시 결과 문서 커밋은 같은 PR에 포함한다.

## 팀 화면을 유지한 최소 연결

같은 e5697e2 기준에서 원본 프론트 변경은1073행, 이번 이식은662행이다. 대상의 신규 session adapter132줄까지 포함한 수치이며, 변경행을 UX 품질 점수로 해석하지 않는다.

| 범위 | 원본 dj/agent | 이번 dj/develop |
|---|---:|---:|
| 기존/신규 파일 | 기존8 | 기존7+신규1 |
| 추가/삭제 | +1014/-59 | +633/-29 |
| HTML/CSS | +30/-3 | +22/-0 |

대상 HTML은 dialog10줄, CSS는 origin 전용12줄을 제외하면 기준과 동일하다. navbar·헤더·아이콘·기존 버튼 배치를 바꾸지 않았고 assets16개·weather/util/saved/tokens/landing/parse는 그대로다. 말풍선·카드·상세·지도·STT·hashrouter·기존 저장 정책을 유지하며 선택 버튼·실제 모호한 출발지 팝업과 세션/상태 투영/음성 복귀 접점만 추가했다. 프론트 무변경을 주장하지 않는다.

서버는 신규 핵심4모듈과 agent_v3.py 실행부로 분리했다. 기존 naito_chat에는 lazy-dispatch3줄만 추가했고 기존 SYSTEM·provider·endpoint·실제 문화/요금/시간 판정 모듈을 보존했다. 중간 chat_dialogue와 전체 history 엔진은 이식하지 않았다.

## 검증과 검토 경계

대상 baseline134개 → backend241/241·표적141/141, 실제 HTTP/store/DOM23/23, legacy상태15/15·HTTP/대화/추천 PASS, 도구26/26이다. 전체 하네스는 기준부터 있던 docstring7건으로 FAIL이며 신규 정적 오류0·문서/색인 정합 PASS다. source의253/19/9와 합산하거나 같은 성적으로 쓰지 않는다.

독립 검증이 발견한 일반뒤로 TTS, 음성URL nativeback STT/TTS, sound=true 복제탭 인사 TTS를 최소 연결부에서 수정해 같은 assertion으로 통과했다. 초기 handshake 직후 canonical null1회는 후속 비재현·직접 원인 미확정으로 남겼다. 실제 모델/원천·마이크/GPS·시각 자동평가를 수행한 것으로 표시하지 않는다. 사용자의 개선 체감 피드백은 받았지만 전체기기 QA 완료와 구분한다.

상세 동작/파일·사실 데이터 한계는 [개발 명세](agent-implementation-spec.md), 승인 범위는 [이식 계획](agent-engine-migration-plan.md), 실행·수정·검증은 [체크리스트](agent-engine-port-progress.md)를 따른다. 영화 작품/회차/예매·방문 가능성의 포괄 검증·새 DB/인증·찜/일정 UI는 이번 게시 범위가 아니다. PR69에서 코드와 검증·문서를 검토한 뒤 팀이 선택할 수 있다.

이슈67은 과거 prefix를 누적하는 대신 현재 대상 중심의17절 본문으로 재작성했다. 제품/기획 의도·세 축·대표 흐름·데이터와 시간 근거·모듈/이벤트/store·선택 권한·최소 UI 비교·실행/실패/검증·원본 평가와 구분·한계·재현/복구를 포함한다. 새 PR69 본문과 함께 재조회 일치를 확인했다. GitHub의 별도 commit status는 조회 시 보고된 항목이 없었으며 로컬 검사 통과를 GitHub CI 통과로 표시하지 않는다.
