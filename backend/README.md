# backend · 에이전트 실행과 검토

2026-11-01 · 브랜치 **`dj/develop`** · 제품 검증 코드 `e7163aa`. 이 브랜치는 깨끗한 develop에 엔진과 필수 화면 접점을 선택 이식한 검토본이다.

[개발 문서 안내](../docs/development/README.md) → [현재 상태](../docs/development/current-state.md) → [실행·API·검증 안내](../docs/development/team-backend-guide.md) 순서로 확인한다. 원본 설계와 이식 완료를 같은 성적으로 읽지 않는다.

## 실행

저장소 루트에서 두 터미널로 실행한다.

```shell
python backend/preview.py
python frontend/dev_server.py
```

사용자 화면은 **http://127.0.0.1:5173/**, API는 기본 **http://127.0.0.1:8765**다. 8765의 `/checks`는 개발 점검용이다. Python 3.12 이상·표준 라이브러리를 사용한다. 키/환경은 [루트 안내](../README.md)·[환경변수 예시](../.env.example)를 따른다. 실제 환경 파일을 공개하거나 복사하지 않는다.

기본 자연어 대화에는 AI 설정이 필요하며 기록 자료 모드가 AI/장소/경로/음성을 모두 대체하지 않는다. 5173은 API 프록시를 사용하고 다른 origin은 `LAB678_ALLOWED_ORIGINS`의 허용 목록을 따른다. 현재 CORS/OPTIONS와 명시 방문계획 최소 60분 검증은 구현되어 있다.

## 코드·계약·검증

실행 진입점은 `backend/agent_v3.py`이고 핵심 모듈은 `chat_knowledge.py`, `dialogue_memory.py`, `conversation_store.py`, `exploration.py`다. 위치·가격·시간·ID는 실제 도구/코드가 판정한다. [에이전트 명세](../docs/development/agent-implementation-spec.md)와 이식본의 파일맵 차이를 함께 확인한다.

- [추천 계약](../docs/development/recommend-api.md), [출발지 계약](../docs/development/place-search-api.md), [이동·UI 인계](../docs/development/outing-handoff.md), [문화 공급자](../docs/development/culture-sources.md).
- 기록된 제품 성적: **backend 241/241 · HTTP/store/DOM 23/23 · legacy 상태 15/15**. 실제 HTTP/DOM 연결·fixture 모델/공급자/장치의 범위다.
- 회귀 명령: `python -m unittest discover -s backend -v`. 브라우저 검사는 개발 실행 안내의 Node/Playwright 준비가 필요하다.
- 문서/도구 하네스는 `python utils/scripts/harness.py --tests`. 기존 docstring 7건 FAIL과 문서 정합을 구분한다.
- 실모델·마이크/GPS·실제 사용자 화면 만족도·공개 배포 QA 완료를 주장하지 않는다.

[배포 설정 안내](../docs/development/render-demo-guide.md)는 별도 참조다. 이번 이식 PR/문서 정리가 배포 앱에 반영됐다는 뜻은 아니며 main/develop 병합·배포하지 않는다.
