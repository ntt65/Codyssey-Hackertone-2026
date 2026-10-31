# 오늘 나들이 · Lab678

> 말로 물어보면, AI 친구 **까치**가 지금 갈 수 있는 서울의 문화 나들이를 찾아 주는 서비스  
> Codyssey AI 해커톤 2026 · 팀 Lab678 (손희영 · 정민규 · 김동조)

- **배포 앱:** https://oneul-nadeuli.vercel.app
- **백엔드 API:** https://oneul-nadeuli-api.onrender.com (무료 서버라 처음 접속 시 30초~1분 깨어나는 시간이 있어요)
- **Figma:** https://www.figma.com/design/UYxmWJohkX8djuFBoNoDEG
- **기획 문서:** [PRD v0.7.0](docs/planning/PRD.md) · [MVP 화면명세서 v0.3.0](docs/planning/Lab_678_MVP_화면명세서.md)

## 무엇을 하나요

1. **까치 깨우기 → 홈**: 까치가 먼저 인사하고, 말로 또는 글자로 대화를 시작해요.
2. **대화로 조건 모으기**: "내일 오후 2시부터 5시까지 전시 보고 싶어요"처럼 말하면 AI가 날짜·시간·분류를 읽고, 빠진 것(출발지 등)만 다시 물어봐요. 60분 미만 나들이는 받지 않아요.
3. **대화 안 추천 카드 최대 3곳**: 서울시 문화행사 실시간 데이터에서 그날 열리는 곳을 출발지에서 가까운 순으로 골라요. 공식 포스터를 보여 주고, 확인되지 않은 정보는 "확인 필요"로 표시해요.
4. **상세 → 지도와 길찾기**: 카카오 지도 위에 도보 경로와 대중교통 경로(최대 3개)를 그려요. 경로를 계산하지 못하면 시간을 지어내지 않아요.
5. **내 나들이 저장**: 로그인 없이 "체험 시작" 한 번으로 이 브라우저에 저장하고, 체험을 끝내면 모두 지워요.

사실 데이터(장소·시간·가격·경로)는 코드와 공공 API가 정하고, AI는 사용자의 말을 조건으로 바꾸는 일만 해요. API가 실패해도 가짜 데이터로 바꾸지 않아요.

## 폴더

```
frontend/   화면 (HTML·CSS·Vanilla JS, 빌드 없이 정적 배포)
backend/    API 서버 (Python 표준 라이브러리만 사용) · 테스트
docs/       기획 · 화면명세 · 개발 기록
design/     Figma 링크 · 화면 · 아이콘
utils/      개발 도구 · 색인 · 검증 스크립트
```

## 실행 방법

### 1. 설치

- **Python 3.12 이상** (배포 서버 3.12, 로컬 3.14에서 확인)
- 추가로 설치할 패키지는 **없어요.** 백엔드는 Python 표준 라이브러리만 쓰고, 프론트는 빌드가 필요 없어요.

```bash
git clone https://github.com/Lab678-Hackathon/lab678.git
cd lab678
```

### 2. 환경 설정

API 키는 저장소에 넣지 않아요. [`.env.example`](.env.example)을 복사해 `.env`를 만들고 값을 채운 뒤, 터미널에 불러와요. (`.env`는 `.gitignore`에 들어 있어요.)

```bash
cp .env.example .env
# .env 를 열어 키 값을 채운 뒤
set -a; source .env; set +a
```

| 변수 | 필수 | 용도 |
|---|---|---|
| `LAB678_SEOUL_API_KEY` | 권장 | 서울시 문화행사 실시간 조회. 없으면 공개 샘플 5건만 조회돼요 |
| `LAB678_KAKAO_REST_API_KEY` | 권장 | 출발지 장소 검색, 대중교통 경로 |
| `LAB678_KAKAO_JAVASCRIPT_KEY` | 선택 | 카카오 지도 표시 (카카오 개발자 콘솔에 실행 주소 도메인 등록 필요). 없으면 OpenStreetMap 지도로 표시돼요 |
| `LAB678_NAITO_API_KEY` | 선택 | AI 대화 해석. 없으면 프론트의 규칙 기반 해석으로 동작해요 |
| `LAB678_NAITO_PROVIDER` | 선택 | `codyssey`(기본, 해커톤 제공 주소) · `anthropic` · `openai` |
| `LAB678_NAITO_MODEL` | 선택 | AI 모델 이름 (기본 `claude-sonnet-4`) |
| `LAB678_TOUR_API_KEY` | 선택 | 한국관광공사 TourAPI 문화시설 조회 (보조 기능) |
| `LAB678_ALLOWED_ORIGINS` | 배포 시 | 프론트 주소 CORS 허용 목록 (쉼표 구분) |
| `LAB678_FILE_VOICE` | 배포 시 | `off`: 서버 음성 파일 기능 끄기 |

키가 하나도 없어도 **기록 데이터 모드**(`?mode=recorded`, 10/31 저장 데이터)로 전체 흐름을 시험할 수 있어요.

### 3. 실행

터미널 두 개에서 저장소 루트 기준으로 실행해요.

```bash
# 터미널 1: 백엔드 API (http://127.0.0.1:8765)
python3 backend/preview.py

# 터미널 2: 프론트 (http://127.0.0.1:5173, /preview 요청을 백엔드로 넘겨줘요)
python3 frontend/dev_server.py
```

브라우저에서 엽니다.

- 실시간: http://127.0.0.1:5173
- 키 없이 시험: http://127.0.0.1:5173/?mode=recorded#/chat?text
  → "10월 31일 오후 2시부터 5시까지 전시 보고 싶어요" → 출발지 "QA 고정: 청량리역"

마이크는 `localhost`(또는 https)에서만 켜져요. Chrome을 권장해요.

### 4. 테스트

```bash
python3 -m unittest discover -s backend -p 'test_*.py'
```

## 배포

- **프론트:** Vercel, `frontend/` 폴더를 정적 사이트로 배포. `frontend/index.html`의 `<meta name="lab678-api">`에 백엔드 주소를 넣어요.
- **백엔드:** Render Web Service, 시작 명령 `python -u backend/preview.py --host 0.0.0.0`, Health Check `/healthz`. 키는 Render 환경변수에만 넣어요. 자세한 내용은 [Render 안내](docs/development/render-demo-guide.md)를 참고해요.

## 알려진 한계

- 문화행사 데이터는 **서울시** 공공 데이터라 서울 밖에서는 가까운 곳이 적어요.
- 직선 거리와 도보·대중교통 경로 시간은 다르며, 경로 시간은 조회 시점 기준이에요. 운영시간·예약은 공식 안내에서 다시 확인해야 해요.
- TourAPI 문화시설 조회는 해외 서버(Render)에서 공공데이터포털 응답이 막혀 배포 앱에는 연결하지 않았어요.
- 저장은 이 브라우저에만 되며 기기 간 동기화는 없어요.

## 팀과 협업

| 이름 | 역할 |
|---|---|
| 손희영 (팀장) | UX/UI · 프론트엔드 · 배포 |
| 정민규 | Product · 화면명세 · QA |
| 김동조 | 백엔드 · API · 데이터 |

협업 규칙은 [TEAM_WORKFLOW.md](TEAM_WORKFLOW.md), 개발 기록은 [docs/development](docs/development/README.md)에 있어요. 브랜치는 `develop`에서 작업하고 `main`이 제출 기준이에요.
