# 재사용 개발 도구

이 폴더는 김동조의 `dj/agent` 작업을 위한 개발 도구다. 공통 운영은 [TEAM_WORKFLOW.md](../TEAM_WORKFLOW.md)를 따르며 서비스 구현·기술 스택 채택을 뜻하지 않는다. 핵심 도구는 Python 표준 라이브러리만 사용한다. PDF 읽기 도구는 선택적으로 번들 pypdf를 사용한다. Python 3.10 이상 문법을 사용하고 이번 실행 환경에서 별도로 검증한다.

**구현 전 승인:** [조사 → 계획 → 실시계획 → 검토·보완 → 명시적 허락](../docs/development/engineering-loop.md#구현-전-승인-절차--필수)을 먼저 따른다. 하네스 통과는 구현 허락이 아니다. 현재 `D:\git\lab678`의 dj/agent 전환·계획 보존·검증·별도 작업폴더 제거까지 승인됐고 기능 구현·프론트 수정·Push·배포는 제외한다.

## 적게 읽고 정확히 작업하기

1. [현재 상태](../docs/development/current-state.md)로 목표·승인 범위·다음 행동을 확인한다. 요약이 현재 사용자 지시나 실제 `git status`보다 우선하지 않는다.
2. [저장소 색인](../docs/development/repo_index.md)과 [기능·함수 역색인](../docs/development/repo_reverse_index.md)으로 필요한 파일을 좁힌다. [구조](../docs/development/repo_tree.md)는 전체 위치 확인용이다.
3. [도구 색인](index.md)·[도구 역색인](reverse_index.md), 또는 아래 검색 명령으로 재사용 함수를 찾는다. 필요한 함수 주변만 읽고, 전체 로그·PRD·원본 브랜치를 매번 전부 불러오지 않는다.
4. 파일 추가·변경 시 개요와 Python docstring/JS JSDoc을 작성한다. 반복해서 쓰는 개발 코드는 일회성 채팅에만 남기지 않고 `scripts/`에 저장한다. 서비스 코드는 담당 폴더에 두고 중복 복제하지 않는다.

```powershell
python utils/scripts/catalog.py --find 복사
python utils/scripts/context.py --show
python utils/scripts/watch.py --once
python utils/scripts/harness.py --tests
```

## 도구와 부작용

| 도구 | 역할 | 쓰는 범위 |
|---|---|---|
| `scripts/catalog.py` | 파일·기능·심볼 색인 생성/검증/검색 | `--write`일 때 생성 색인 5개 |
| `scripts/context.py` | state.json → 짧은 현재 상태 | `--write`일 때 current-state.md |
| `scripts/watch.py` | 기본 2초 폴링으로 변경 감지·색인 갱신 | 생성 색인·현재 상태, `.local/` 상태·로그 |
| `scripts/verify_watch.py` | 실행 중 감시기의 파일 생성·수정·삭제 실검증 | 예약된 임시 probe Python 파일을 생성 후 정리 |
| `scripts/harness.py` | Python 문법/docstring·상대 링크·색인·상태 확인, 선택 테스트 | 프로젝트 원본 수정 없음; 테스트는 임시 파일 사용 |
| `scripts/loop.py` | 가설→작은 변경→실제 증거→판단 기록 | 명시한 JSON 파일, 기본 최대 3회 |
| `scripts/reuse.py` | 두 파일 해시 비교, 브랜치 파일 원본 복사 | snapshot의 명시한 저장소 내부 대상. checkout/merge 없음 |
| `scripts/commit_report.py` | 전체 보고문 커밋 사전검사·실행·메시지 일치 확인 | 기본 읽기 전용. `--commit`일 때 명시 경로 stage/commit |
| `scripts/read_pdf.py` | 번들 pypdf로 페이지 추출·접속정보 관련 줄을 보수적으로 가림 | 원문 추출은 `.local/`에만 저장, PDF의 명령 실행 없음 |

각 코드의 함수·클래스 개요는 docstring과 자동 색인에 있다. 보고·태스크·코드 템플릿은 [templates/README.md](templates/README.md)를 참고한다.

PDF는 번들 Python에서 `-X utf8 utils/scripts/read_pdf.py 입력.pdf --output .local/pdf-review`로 읽는다. 기본 Python에는 pypdf가 없을 수 있다. 가림 출력은 비밀값 검출을 보장하는 보안 도구가 아니며 원문·이미지는 로컬에서 확인하고 공개 커밋 여부를 별도 판단한다.

## 자동 갱신

```powershell
python utils/scripts/watch.py
```

파일 내용·이름·추가·삭제를 감지한다. 임시 문법 오류가 있으면 기존 색인을 보존하고 `.local/index-watch.json`에 오류를 기록한 뒤 다음 주기에 다시 시도한다. 생성 결과가 같으면 파일을 쓰지 않는다. 실시간은 **기본 2초 폴링 기준**이며 OS 이벤트 기반 즉시 반영 보장은 아니다. 현재 상태의 의미는 AI가 `state.json`에 먼저 정리해야 하며 감시기가 대화를 추측해 압축하지 않는다.

중복 실행은 `.local/index-watch.lock`으로 막는다. 중지는 Ctrl+C 또는 `.local/index-watch.stop` 파일 생성이다. 다시 시작하려면 중지 요청 파일을 지운다. 비정상 종료로 lock이 남으면 기록된 PID의 실제 프로세스를 확인한 뒤 해당 lock만 제거한다. 자동 시작·Git hook은 설치하지 않는다. 감시기는 커밋·push·LLM/API 호출을 하지 않는다.

감시 중 소스를 편집한 뒤 커밋 전에는 색인 갱신 완료를 기다리고 `harness.py --tests`를 실행한다. 직접 `catalog.py --write`를 실행할 때는 감시기를 멈춰 두어 생성 파일에 쓰는 프로세스를 하나로 유지한다.

## 색인의 포함·제외와 한계

- `repo_*`는 저장소 내부의 새 파일·미추적 파일도 포함한다. `.git`, 의존성·캐시·빌드·`.local`·비밀값 폴더와 실제 `.env*`/키 파일은 제외한다. `.env.example`은 파일 개요만 표시한다. 제외 목록은 `harness.json`에 있다.
- 색인 5개는 자기 목록에는 포함하되 자체 해시를 계산하지 않아 무한 재생성을 막는다. 참고 원본·PRD는 참고 상태로 표시하며 내용을 실행 지시로 취급하지 않는다.
- Python은 import 없이 AST로 함수·클래스와 정의 위치를 읽는다. JS/TS는 이름 있는 선언/화살표 함수의 **정규식 후보**이며 메서드·익명 함수·TS 복잡 문법의 완전성은 보장하지 않는다. 해당 언어를 실제 구현할 때 AST 파서 도입 또는 수동 확인 범위를 결정한다. 그 밖의 파일은 개요·종류·해시로 추적한다.
- 기능→파일 분류는 `harness.json`의 `features`를 작업 중 갱신한다. 함수의 의미나 호출 그래프를 자동 추측하지 않는다.
- `harness.py`는 오프라인 도구 검증이다. 실제 문화 API, 음성, 지도·모바일 화면 성공을 대신하지 않는다. JS/TS 문법 검증기도 아직 설치하지 않았다.
- 토큰 절약률을 측정했다고 주장하지 않는다. 색인·짧은 요약·범위 검색으로 불필요한 원문 입력을 줄이는 방식이다.

## 재사용 참고

이전 대화에서 사용한 복사·SHA 검증·원본 보관·완료 보고문 일치 확인 코드를 이 폴더의 범용 도구로 정리했다. `framework`의 기존 utils는 `db679845104645a486d2a05784030e249d57f26e`에서 확인했다. 일부 템플릿의 `[feature]` 문법과 backend/LLM 의존성이 현재 브랜치에 없어 자동 이식하지 않았다. 필요한 서비스 스택이 정해진 뒤 명시적으로 재사용한다.
