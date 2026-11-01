"""Naito 단일 조건 추출 호출. 키/대화 원문은 기록하지 않고 실패 시 기존 초안을 유지한다."""
import json
import os
from datetime import datetime
from pathlib import Path
from threading import BoundedSemaphore
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from chat_conditions import FIELDS, apply_interpretation
from chat_grounding import clarification_text, ground_payload
from chat_prompt import SYSTEM
from outing import InputError, KST
from preferences import FIELDS as PREFERENCE_FIELDS

ENDPOINT = "https://copa.codyssey.kr/v1/messages"  # 해커톤 제공 주소 (기본, Anthropic 형식)
ANTHROPIC_ENDPOINT = "https://api.anthropic.com/v1/messages"  # 개인 Anthropic 키
OPENAI_ENDPOINT = "https://api.openai.com/v1/chat/completions"  # 개인 OpenAI 키
PROVIDERS = {"codyssey": ENDPOINT, "anthropic": ANTHROPIC_ENDPOINT, "openai": OPENAI_ENDPOINT}


def provider():
    """LAB678_NAITO_PROVIDER: codyssey(기본) / anthropic / openai. 키 모양으로 추측하지 않는다(해커톤 키도 sk- 로 시작)."""
    chosen = os.environ.get("LAB678_NAITO_PROVIDER", "").strip().lower()
    return chosen if chosen in PROVIDERS else "codyssey"


def endpoint(key=""):
    """호출 주소 (허용된 세 곳 중 하나)."""
    return PROVIDERS[provider()]


SLOTS = BoundedSemaphore(2)


def settings():
    """앱 전용 환경변수/무시된 로컬 파일에서 키와 모델을 읽는다. 실제 값은 출력하지 않는다."""
    local = {}
    path = Path(__file__).resolve().parents[1] / ".local/naito.env"
    if path.is_file():
        for line in path.read_text(encoding="utf-8-sig").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                key, value = line.split("=", 1)
                local[key.strip()] = value.strip()
    return (os.environ.get("LAB678_NAITO_API_KEY", local.get("LAB678_NAITO_API_KEY", "")).strip(),
            os.environ.get("LAB678_NAITO_MODEL", local.get("LAB678_NAITO_MODEL", "claude-sonnet-4")).strip())


def validate_request(data):
    """짧은 발화/대화와 초안 revision을 검증한다. 오류에 사용자 원문을 포함하지 않는다."""
    message = data.get("message")
    draft = data.get("condition_draft", {})
    confirmed = data.get("confirmed_fields", [])
    revision = data.get("revision")
    history = data.get("conversation_context", [])
    if not isinstance(message, str) or not 1 <= len(message.strip()) <= 1000:
        raise InputError("invalid_message", "message", "대화는 1~1000자로 입력해 주세요.")
    if not isinstance(history, list) or len(history) > 6:
        raise InputError("invalid_context", "conversation_context", "최근 대화는 최대 6개까지 전달해 주세요.")
    for item in history:
        if (not isinstance(item, dict) or item.get("role") not in ("user", "assistant")
                or not isinstance(item.get("content"), str) or not 1 <= len(item["content"]) <= 1000):
            raise InputError("invalid_context", "conversation_context", "대화 기록 형식을 확인해 주세요.")
    try:
        apply_interpretation(draft, {}, confirmed, revision, revision)
    except (ValueError, TypeError, KeyError, AttributeError):
        raise InputError("invalid_draft", "condition_draft", "현재 입력 조건과 revision을 확인해 주세요.") from None
    return message.strip(), draft, confirmed, revision, history


def extract_conditions(message, draft, history, key, model):
    """공식 사용자 제공 주소로 1회 호출한다. 좌표는 보내지 않고 응답 최대64KiB/20초로 제한한다."""
    context = {k: draft[k] for k in {"date", "start_at", "end_at", "category", "request_kind", "stay_minutes", "start_query"} | PREFERENCE_FIELDS if k in draft}
    if isinstance(draft.get("start_location"), dict):
        context["start_query"] = draft["start_location"].get("label")
    now = datetime.now(KST)
    user_text = json.dumps(dict(now_kst=now.isoformat(timespec="seconds"), condition_draft=context,
                                conversation_context=history, message=message), ensure_ascii=False)
    if provider() == "openai":
        # OpenAI Chat Completions: JSON 객체만 받도록 지정
        request_data = dict(model=model, max_completion_tokens=1024, response_format=dict(type="json_object"),
                            messages=[dict(role="system", content=SYSTEM), dict(role="user", content=user_text)])
        headers = {"Authorization": "Bearer " + key, "Content-Type": "application/json"}
    else:
        request_data = dict(model=model, max_tokens=1024, system=SYSTEM, messages=[dict(role="user", content=user_text)])
        headers = {"x-api-key": key, "anthropic-version": "2023-06-01", "Content-Type": "application/json"}
    request = Request(endpoint(), data=json.dumps(request_data, ensure_ascii=False).encode(), headers=headers, method="POST")
    with urlopen(request, timeout=20) as response:
        raw = response.read(65537)
    if len(raw) > 65536:
        raise ValueError("AI 응답 크기 초과")
    payload = json.loads(raw)
    if provider() == "openai":
        choice = payload["choices"][0]
        if (choice.get("finish_reason") in {"length", "content_filter"}
                or choice["message"].get("refusal")
                or not isinstance(choice["message"].get("content"), str)):
            raise ValueError("AI 응답 형식 오류")
        content = choice["message"]["content"]
    else:
        blocks = payload["content"]
        if not isinstance(blocks, list) or payload.get("stop_reason") in {"max_tokens", "refusal"}:
            raise ValueError("AI 응답 형식 오류")
        content = "".join(block["text"] for block in blocks if block.get("type") == "text")
    return ground_payload(json.loads(content), message, draft, history, now=now)


def chat(data):
    """대화 API 결과를 (HTTP상태, 본문)으로 반환한다. 장애 시 가짜 해석/추천으로 대체하지 않는다."""
    message, draft, confirmed, revision, history = validate_request(data)
    key, model = settings()
    if not key or not model:
        return 503, dict(status="unconfigured", code="ai_not_configured", message="AI 연결 설정이 필요합니다. 입력 칸은 계속 사용할 수 있어요.")
    if not SLOTS.acquire(blocking=False):
        return 429, dict(status="busy", code="ai_busy", message="대화 처리 중입니다. 잠시 뒤 다시 시도해 주세요.")
    try:
        proposal = extract_conditions(message, draft, history, key, model)
        result = apply_interpretation(draft, proposal, confirmed, revision, revision)
        blocked = getattr(proposal, "blocked_fields", ())
        if blocked:
            if any(not isinstance(field, str) or field not in FIELDS for field in blocked):
                raise ValueError("AI 보류 필드를 확인해 주세요.")
            blocked = tuple(dict.fromkeys(blocked))
            result["assistant_text"] = clarification_text(blocked)
            result["ready_to_search"] = False
            result["interpretation_status"] = "needs_clarification"
            result["clarification_fields"] = list(blocked)
        elif not proposal or not any(value is not None for value in proposal.values()):
            result["assistant_text"] = "이번 말씀은 조건에 반영하지 못했어요. 입력 칸에서 확인하거나 출발지·날짜·시각·대표 분류를 다시 말씀해 주세요."
            result["ready_to_search"] = False
            result["interpretation_status"] = "no_supported_change"
        result["source"] = "naito"
        result["model"] = model
        return 200, result
    except HTTPError as exc:
        status = 429 if exc.code == 429 else 502
        exc.close()
        return status, dict(status="error", code="ai_provider_error", message="AI 서비스가 요청을 처리하지 못했습니다. 현재 입력을 유지하고 다시 시도해 주세요.")
    except TimeoutError:
        return 504, dict(status="error", code="ai_timeout", message="AI 응답이 늦습니다. 현재 입력을 유지하고 다시 시도해 주세요.")
    except (URLError, OSError):
        return 502, dict(status="error", code="ai_network", message="AI 서비스와 연결하지 못했습니다. 현재 입력을 유지해 주세요.")
    except (ValueError, TypeError, KeyError, IndexError, AttributeError):
        return 502, dict(status="error", code="ai_invalid_response", message="AI가 조건을 정확히 정리하지 못했습니다. 입력 칸에서 확인해 주세요.")
    finally:
        SLOTS.release()
