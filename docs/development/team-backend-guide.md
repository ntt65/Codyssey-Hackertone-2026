# LAB678 · 에이전트 실행·API·검증 안내

갱신: 2026-11-01 · **`dj/develop`** · 제품 검증 코드 `e7163aa`. [개발 문서 안내](README.md)에서 원본/대상과 문서 읽는 순서를 먼저 확인한다. 이 안내는 팀 기획 확정·배포 승인이나 실제 기기 QA 완료를 뜻하지 않는다.

## 브랜치와 실행 준비

`dj/agent`는 원본, `dj/develop`은 develop `e5697e2`를 직접 기반으로 엔진을 선택 이식한 검토본이다. 게시된 코드/문서 기준은 각각 b6355a0/d541ea5와 e7163aa/ed923aa이며 후속 문서 커밋은 제품 검증 성적을 바꾸지 않는다. 예전 ‘22커밋 미push’, ‘프론트 실파일 미공유’는 [10/31 안내](team-backend-guide-20261031.md)의 이력이다.

다른 작업이 있는 폴더는 보존하고 별도 확인 폴더를 사용한다. 아래 폴더가 이미 있으면 새 이름을 고른다. 이 명령은 원격을 받는 읽기/확인 예시이며 병합 명령이 아니다.

```shell
git status
git fetch origin
git log -1 --oneline origin/dj/develop
git worktree add --detach ../lab678-agent-review origin/dj/develop
cd ../lab678-agent-review
```

Python 3.12 이상에서 백엔드·정적 프론트 실행에 별도 Python 패키지나 프론트 빌드는 필요하지 않다. Node/Playwright/Chrome은 선택적 브라우저 회귀 검사에 별도로 필요하다.

## 로컬 실행과 환경

저장소 루트에서 터미널 두 개로 실행한다. Windows에서는 `python`, 다른 환경에서는 설치된 `python3` 등을 사용한다.

```shell
python backend/preview.py
python frontend/dev_server.py
```

사용자 화면은 **http://127.0.0.1:5173/**, API 기본 주소는 **http://127.0.0.1:8765**다. 8765의 기존 `/checks`는 개발 점검 화면이다. 5173은 `/preview/` POST를 백엔드로 프록시하며 `LAB678_API`로 대상 API를 지정할 수 있다. 기본 포트가 이미 사용 중이면 기존 소유 서버를 확인하고 임의 종료하지 않는다. 코드 변경 후에는 해당 백엔드를 재시작한다.

각 PC의 127.0.0.1은 자기 PC다. 문서의 주소를 공용 배포 주소로 공유하지 않는다. 이번 PR 코드를 기존 배포 앱에 적용한 것으로 표시하지 않는다.

- 환경변수 이름은 [루트 실행 안내](../../README.md)와 [환경변수 예시](../../.env.example)를 따른다. 실제 키/환경 파일을 채팅·Git·응답·로그에 넣지 않는다.
- 기본 v3 자연어 대화에는 유효한 `LAB678_NAITO_API_KEY`와 현재 설정 provider/model이 필요하다. 미설정/연결/응답 형식 오류를 구분하고 입력·대화를 보존한다. v3 실패를 프론트 규칙 파서의 성공으로 바꾸지 않는다.
- 기존 코드가 지원하는 `.local/naito.env`는 키와 모델의 로컬 설정일 뿐 공개·복제 대상이 아니다. 다른 제공자/모델을 문서 갱신 과정에서 바꾸지 않는다. 일반 `.env` 전체를 자동 로딩한다고 가정하지 말고 환경변수나 명시된 로컬 설정을 사용한다.
- 서울시 문화 키가 없을 때의 sample 범위, 실제 장소/경로에 필요한 카카오 설정은 [문화 자료](culture-sources.md)·[장소 계약](place-search-api.md)·[추천 계약](recommend-api.md)을 확인한다.
- `?mode=recorded`는 기존 추천/문화 조회의 기록 자료 모드다. 자연어 AI·장소/경로·지도·음성까지 키 없이 전부 작동하는 모드가 아니다. 10/31 자료는 현재 방문 가능성을 보장하지 않는다.
- 기본 프론트 프록시 외의 origin은 `LAB678_ALLOWED_ORIGINS`의 명시 CORS 허용을 사용한다. OPTIONS/CORS는 구현되어 있다. CORS 설정이 외부 API 접속이나 실제 배포 정상 동작을 보장하지는 않는다.

## 구현·선택·음성의 경계

이 브랜치의 실행은 `backend/agent_v3.py`, 핵심 의미/정책·사실 탐색·임시 store는 `chat_knowledge.py`, `dialogue_memory.py`, `exploration.py`, `conversation_store.py`다. 세션 접점은 `frontend/js/agent-session.js`다. 소스의 전체 history/내비게이션 구현과 대상의 최소 접점을 혼동하지 않는다.

기본 대화는 v3다. 목적/취향·추천 조건·메뉴 진행을 분리해 보존하고, 확인된 정보로 실제 후보를 제안한다. ‘이곳 선택’과 현재 표시 묶음의 ‘3번’은 같은 실제 후보 ID를 선택한다. 상세 열람·임시 선택·내 나들이 저장·예약 확정은 각각 다른 의미다. 날짜 없는 탐색을 허용하지만 기존 명시 방문계획의 최소 60분 검증을 제거하지 않았다.

음성은 기존 브라우저 STT/TTS를 사용한다. 실제 마이크·한국어 음성·권한·GPS·모바일 배치는 사용자 기기에서 확인해야 한다. 자동 회귀의 모의 장치 카운터를 실기기 인식률로 설명하지 않는다. 실패 시 텍스트로 이어갈 수 있다. 지원되지 않는 영화 상영표·예약이나 남은 토큰 수치를 추측하지 않는다.

## API 연결

| 메서드·경로 | 현재 용도/문서 |
|---|---|
| `POST /preview/chat` | `agent_version=3`의 open/message/select/heartbeat/release 등 이벤트. [개발 명세](agent-implementation-spec.md)의 계약과 대상 차이를 확인 |
| `POST /preview/places` | 실제 출발지 장소/주소 검색. [장소 계약](place-search-api.md) |
| `POST /preview/recommend` | 명시 방문계획 place/course·route 호환과 최소시간 검증. [추천 계약](recommend-api.md) |
| `POST /preview/walk`, `/preview/transit` | 실제 이동 경로. [이동 인계](outing-handoff.md) |
| `POST /preview/contact` | 실제 공식 출처의 문의 연락처. 없는 번호를 생성하지 않음 |
| `POST /preview/voice` | 기존 Windows 파일 음성 경로. 브라우저 STT/TTS와 별도 |

v3는 canonical handle/epoch/revision/document/lease/turn을 사용한다. 오래된 표시 묶음·다른 대화 후보·조건 변경 뒤의 선택은 거절한다. 일반 요청/legacy는 8KiB, v3 restore만 32KiB다. 400 입력, 409 동기화/lease, 429 제한, 502 외부/형식, 503 미설정, 504 timeout을 구분한다. HTTP200의 구조화된 `source_error`도 읽어야 하며 카드 수나 HTTP200만으로 의미/조회 성공을 판정하지 않는다.

## 검증과 공유

기록된 이 브랜치 성적은 **backend 241/241 · HTTP/store/DOM 23/23 · legacy 상태 15/15**, 도구 26개 PASS다. source 실모델 B/C 평가와 target fixture 평가를 합산하지 않는다. 전체 하네스에는 기준부터 있던 docstring 7건이 남아 있다.

```shell
python -m unittest discover -s backend -v
node utils/scripts/check_agent_v3.cjs
node utils/scripts/check_agent_regressions.cjs
node utils/scripts/check_agent_http.cjs
python utils/scripts/harness.py --tests
```

브라우저 회귀는 필요시 `PLAYWRIGHT_MODULE`, `CHROMIUM_PATH`, `PYTHON`을 지정한다. 이식 대상의 기존 HTTP·대화·추천 회귀는 스크립트가 legacy query로 확인한다. 이번 문서 정리에서는 제품 검사를 다시 실행하지 않고 링크·색인·state·도구 검사와 제품 파일 불변을 검증한다.

사용자 시험은 Ctrl+F5 → 새 대화 → 목적·지역 → 현재 카드 선택/‘3번’ → 다른 묶음 선택 → 상세·지도·저장·복귀 순서로 한다. 실패는 브랜치/커밋·단계·HTTP/turn/revision과 실제/기대 결과를 기록하되 키·민감 원문·정밀 위치는 공개하지 않는다.

현재 공유는 [이슈67](https://github.com/Lab678-Hackathon/lab678/issues/67)과 [PR69](https://github.com/Lab678-Hackathon/lab678/pull/69)를 따른다. PR68은 과거 외부 병합 이력이다. 이번 요청은 두 브랜치 문서 갱신·push까지이며 merge·main/develop 변경·배포·Discord 전송은 실시하지 않는다.
