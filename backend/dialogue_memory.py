"""v3 의미 상태·조건 후보·대화 정책의 순수 전이.

모델은 acts/updates만 제안한다. 현재 사용자 턴의 근거, 타입, 날짜/가격 grounding을
검사해 항목별로 반영하며 한 후보 오류가 유효한 목적을 지우지 않는다. 네트워크·저장·
LLM 호출은 하지 않는다. decide는 순수 함수이며 호출자가 반환 question을 기록한다.
"""
from copy import deepcopy
from datetime import date, datetime, timedelta
import re

from chat_grounding import ground_payload
from chat_conditions import normalize_proposal
from chat_knowledge import (ACTS, OPERATIONS, STRENGTHS, DIMENSIONS, SERVICES, GENRES,
                            CONDITION_FIELDS, SERVICE_FIELDS, ROUTING_FIELDS, FIELD_LABELS,
                            MAX_ACTS, MAX_UPDATES, MAX_PREFERENCES, MAX_HYPOTHESES, capability)
from outing import KST, coordinate


def new_state():
    """대화 한 개의 빈 도메인 상태를 만든다. ID/revision/lease는 외부 store 소유다."""
    return {"understanding": {"goal": "", "service": "any", "preferences": []},
            "conditions": {}, "hypotheses": [], "active_question": None,
            "pending_changes": [], "latest_moves": [], "tool_facts": [],
            "result_context": None, "field_meta": {}, "question_history": [],
            "display_batch": None, "display_history": None, "selected_content": None, "selection_notice": None,
            "request_mode": "explore", "diagnostics": {"issues": [], "turn_status": "understood"}}


def _text(value, maximum=160):
    """유한한 짧은 평문을 검증한다. 모델 텍스트를 실행하거나 HTML로 만들지 않는다."""
    if not isinstance(value, str) or not 1 <= len(value.strip()) <= maximum or any(ord(c) < 32 for c in value):
        raise ValueError("invalid_text")
    return value.strip()


def _evidence(value, message, turn_id):
    """새 후보의 출처가 현재 사용자 발화인지 검증한다. 의미 동일성을 증명하지는 않는다."""
    if not isinstance(value, dict) or value.get("turn_id") != turn_id:
        raise ValueError("invalid_evidence_turn")
    quote = _text(value.get("quote"), 200)
    if quote not in message:
        raise ValueError("missing_evidence_quote")
    return {"turn_id": turn_id, "quote": quote}


def _issue(state, reason, item=None):
    """진단에는 필드/코드만 넣고 사용자 인용이나 좌표를 복제하지 않는다."""
    value = {"code": reason}
    if isinstance(item, dict):
        for key in ("id", "domain", "field"):
            if isinstance(item.get(key), str):
                value[key] = item[key][:60]
    state["diagnostics"]["issues"].append(value)


def _invalidate(state):
    """현재 결과와 새 의미/조건의 혼입을 막는다. 과거 말풍선 스냅샷은 외부 UI 소유다."""
    selected = state.get("selected_content")
    if selected:
        state["selection_notice"] = f"조건이 바뀌어 이전 ‘{selected.get('title', '콘텐츠')}’ 선택은 해제했어요. "
    state["result_context"] = None
    state["display_batch"] = None
    state["display_history"] = None
    state["selected_content"] = None


def _scope(state, field, explicit=None):
    """활동 종속 선호와 공통 예산·위치·필수 제약의 소유 범위를 구별한다."""
    if explicit == "conversation":
        return explicit
    return state["understanding"]["service"] if field in SERVICE_FIELDS | DIMENSIONS else "conversation"


def _unresolved(state, item, evidence, reason, hard=False):
    """근거 있는 미해결 필수조건만 실행 보류로 남긴다. 잘못된 soft 후보는 대화를 막지 않는다."""
    entry = {"id": item.get("id", "unresolved")[:60], "kind": "requirement" if hard else "condition",
             "field": item.get("field", "requirement"), "value": evidence["quote"],
             "strength": "hard" if hard else "unspecified", "source": "user_explicit",
             "status": "unresolved", "evidence": evidence, "reason": reason,
             "scope": "conversation", "blocking_scope": ["explore", "search_places", "visit"] if hard else []}
    state["hypotheses"] = [h for h in state["hypotheses"] if h.get("id") != entry["id"]]
    state["hypotheses"].append(entry)
    state["hypotheses"] = state["hypotheses"][-MAX_HYPOTHESES:]
    if hard:
        _invalidate(state)


def _hard_evidence(item, evidence, state):
    """모델 hard 표지가 아니라 사실 제약 차원과 현재 발화의 근거를 대조한다.

    실행 라우팅 후보의 타입 오류는 필수조건이 아니다. 이것은 자연어 의도 전반을
    키워드로 재분류하는 함수가 아니라 잘못된 후보를 blocking으로 승격하는 경계다.
    """
    domain, field, text = item.get("domain"), item.get("field"), evidence["quote"]
    if not isinstance(domain, str) or not isinstance(field, str):
        return False
    if domain in {"goal", "service"} or field in ROUTING_FIELDS:
        return False
    strict = bool(re.search(r"만\s*(?:가능|원|보|가)|없어야|가능해야|이내|필수\s*조건", text))
    if re.search(r"가능하면|되도록|좋겠|선호|면\s*좋", text) and not strict:
        return False
    patterns = {
        "free_only": r"무료|유료",
        "budget_krw": r"예산|\d\s*(?:만\s*)?원",
        "date": r"오늘|내일|모레|글피|요일|주말|\d[-/.]\d|\d\s*월",
        "date_from": r"오늘|내일|모레|글피|요일|주말|\d[-/.]\d|\d\s*월",
        "date_to": r"오늘|내일|모레|글피|요일|주말|\d[-/.]\d|\d\s*월",
        "start_at": r"\d\s*(?:시|분)|\d:\d|오전|오후|출발|부터",
        "end_at": r"\d\s*(?:시|분)|\d:\d|오전|오후|종료|까지",
        "stay_minutes": r"\d\s*(?:시간|분)",
        "start_query": r"출발|근처|주변|[가-힣]+(?:동|구|역|시청|대로|길)",
        "walking_preference": r"(?:걸어서|도보).{0,12}(?:\d|이내|만)|계단|휠체어",
        "indoor_outdoor": r"실내\s*만|실외\s*만|야외\s*만|(?:실내|실외|야외).{0,6}(?:필수|반드시)",
        "exclude_terms": r"말고|제외|빼|원하지|싫|가지\s*않",
    }
    if domain == "condition":
        return field in patterns and bool(re.search(patterns[field], text))
    if domain == "requirement":
        return bool(re.search(r"계단|휠체어|예약|좌석|무료|예산|\d\s*(?:분|원)|주차|출입|반려동물|없어야|가능해야|이내", text))
    return False


def _history(state):
    """현재 주 질문만 grounding 맥락으로 전달한다. STT 공지는 여기에 들어오지 않는다."""
    question = state.get("active_question") or next((q for q in reversed(state.get("question_history", [])) if isinstance(q, dict)), None)
    if question and question.get("target") == "start_location":
        # 질문의 표면 문구가 아니라 명시한 대상이 단답의 역할을 정한다.
        return [{"role": "assistant", "content": "출발할 곳과 주변 콘텐츠를 찾을 지역은 어디인가요?"}]
    return [{"role": "assistant", "content": question["text"]}] if question and question.get("text") else []


def _date_value(value, message):
    """명시 날짜와 단순 상대 날짜를 코드로 대조한다. 시각이나 오늘을 기본값으로 만들지 않는다."""
    chosen = date.fromisoformat(_text(value, 10))
    today = datetime.now(KST).date()
    relative = {"오늘": 0, "내일": 1, "모레": 2, "글피": 3}
    found = [today + timedelta(days=offset) for token, offset in relative.items() if token in message]
    explicit = re.findall(r"(?<!\d)\d{4}[-/.]\d{1,2}[-/.]\d{1,2}(?!\d)", message)
    found.extend(date(*(int(p) for p in re.split(r"[-/.]", token))) for token in explicit)
    if chosen not in found:
        raise ValueError("ambiguous_date")
    return chosen.isoformat()


def _condition_value(field, value, evidence, message, state):
    """실제 설정의 기존 grounding을 재사용한다. 음악 분위기는 이 함수의 분류 입력이 아니다."""
    if field not in CONDITION_FIELDS:
        raise ValueError("unknown_condition")
    if field in {"date", "date_from", "date_to"}:
        return _date_value(value, message)
    if field in {"category", "categories"}:
        items = value if isinstance(value, list) else [value]
        if not items or any(not isinstance(v, str) or v not in GENRES for v in items):
            raise ValueError("invalid_category")
        # 명시 장르만 메뉴에 반영한다. '음악'만으로 국악/클래식/콘서트를 생성하지 않는다.
        if any(v != "전체" and v not in message for v in items):
            raise ValueError("genre_not_explicit")
        if "전체" in items and not re.search(r"전체|모든|아무거나|골고루|다\s*좋|상관\s*없", message):
            raise ValueError("all_categories_not_explicit")
    if field == "stay_minutes":
        spans = re.findall(r"(\d+)\s*(시간|분)", evidence["quote"])
        if not any(int(amount) * (60 if unit == "시간" else 1) == value for amount, unit in spans):
            raise ValueError("duration_not_explicit")
    if field == "start_query":
        value = _text(value, 80)
        if re.sub(r"\s+", "", value) not in re.sub(r"\s+", "", evidence["quote"]):
            raise ValueError("origin_not_in_quote")
        if re.search(re.escape(re.sub(r"\s+", "", value)) + r"(?:에|으로|로|까지)(?:가고|가려|가자|갈|방문)", re.sub(r"\s+", "", message)):
            raise ValueError("destination_not_origin")
        # 검색어는 사실 좌표가 아니다. 의미 후보의 지명은 조회할 수 있지만 실제 좌표와
        # 기존 확정 위치의 변경은 지도 결과와 별도 사용자 동의 경계에서 처리한다.
        return value
    proposal = ground_payload({"changes": {field: value}, "evidence": {field: evidence["quote"]}},
                              message, state["conditions"], _history(state))
    if field not in proposal or proposal.blocked_fields:
        raise ValueError("ungrounded_condition")
    return normalize_proposal({field: proposal[field]})[field]


def _metadata(item, evidence, state):
    """사용자 발화 후보의 출처와 명시 강도를 보관한다. 사용자 확정으로 자동 승격하지 않는다."""
    return {"id": item["id"], "source": "user_explicit", "confirmed": False,
            "evidence": evidence, "strength": item.get("strength", "unspecified"),
            "scope": _scope(state, item.get("field"), item.get("scope"))}


def _set_condition(state, field, value, meta):
    """단일 검증 조건을 적용하고 연결된 값과 미해결 항목을 정리한다."""
    before = deepcopy(state["conditions"])
    old_hypotheses = deepcopy(state["hypotheses"])
    state["conditions"][field] = deepcopy(value)
    state["field_meta"][field] = meta
    if field == "start_query":
        existing = state["conditions"].get("start_location")
        key = lambda text: re.sub(r"\s+", "", str(text)).replace("서울특별시청", "서울시청")
        same = existing and state["field_meta"].get("start_location", {}).get("confirmed") and key(existing.get("label")) == key(value)
        if same:
            state["conditions"].pop("start_query", None)
            state.pop("origin_lookup_required", None)
        else:
            # 기존 확정 좌표는 새 실제 후보를 동의하기 전까지 유지한다.
            state["origin_lookup_required"] = True
    if field == "category":
        state["conditions"]["categories"] = [value]
    elif field == "categories":
        state["conditions"]["category"] = value[0]
    state["hypotheses"] = [h for h in state["hypotheses"] if h.get("field") != field]
    if before != state["conditions"] or old_hypotheses != state["hypotheses"]:
        _invalidate(state)


def _condition_group(state, updates):
    """날짜/시각은 같은 변경 묶음으로 검증·동의한다. 다른 필드의 성공은 보존한다."""
    groups = [list(updates)]
    timed = [entry for entry in updates if entry[0] in {"date", "start_at", "end_at", "date_from", "date_to"}]
    if timed:
        groups = [timed] + [[entry] for entry in updates if entry not in timed]
    else:
        groups = [[entry] for entry in updates]
    for entries in groups:
        changes = {field: value for field, value, _ in entries}
        proposed = {**state["conditions"], **changes}
        try:
            if proposed.get("start_at") and proposed.get("end_at"):
                start, end = (datetime.fromisoformat(proposed[k]) for k in ("start_at", "end_at"))
                if start >= end or start.date() != end.date():
                    raise ValueError("invalid_time_range")
            if proposed.get("date_from") and proposed.get("date_to") and proposed["date_from"] > proposed["date_to"]:
                raise ValueError("invalid_date_range")
        except ValueError:
            for field, _, meta in entries:
                item = {"id": meta["id"], "field": field}
                _issue(state, "invalid_time_range", item)
                _unresolved(state, item, meta["evidence"], "invalid_time_range", hard=True)
            continue
        protected = [field for field in changes if state["field_meta"].get(field, {}).get("confirmed")
                     and field in state["conditions"] and state["conditions"][field] != changes[field]]
        if protected:
            identity = entries[0][2]["id"]
            state["pending_changes"] = [p for p in state["pending_changes"] if p.get("field") not in changes]
            state["pending_changes"].append({"id": identity, "field": protected[0],
                "before": deepcopy(state["conditions"].get(protected[0])), "after": changes[protected[0]],
                "changes": deepcopy(changes), "metadata": {f: m for f, _, m in entries}})
        else:
            for field, value, meta in entries:
                _set_condition(state, field, value, meta)


def _apply_update(state, item, evidence, message, conditions):
    """단일 의미 후보를 원자적으로 적용한다. 모르는 필드는 예외로 해당 후보만 격리한다."""
    domain, field, op = item.get("domain"), item.get("field"), item.get("op")
    if op not in OPERATIONS or item.get("strength", "unspecified") not in STRENGTHS:
        raise ValueError("invalid_operation")
    value = item.get("value")
    meta = _metadata(item, evidence, state)
    if domain in {"goal", "service"}:
        expected = {"goal", "text", "description"} if domain == "goal" else {"service", "activity"}
        if field not in expected:
            raise ValueError("unknown_semantic_field")
        if op in {"replace", "remove"} and item.get("target_id") != state["field_meta"].get(domain, {}).get("id"):
            raise ValueError("unknown_target")
        if op == "remove":
            if item.get("target_id") != state["field_meta"].get(domain, {}).get("id"):
                raise ValueError("unknown_target")
            value = "" if domain == "goal" else "any"
        else:
            value = _text(value)
            if domain == "service" and value not in SERVICES:
                raise ValueError("unknown_service")
        old = state["understanding"][domain]
        state["understanding"][domain] = value
        state["field_meta"][domain] = meta
        if domain == "service" and old != value:
            for key in SERVICE_FIELDS:
                state["conditions"].pop(key, None)
                state["field_meta"].pop(key, None)
            state["understanding"]["preferences"] = [p for p in state["understanding"]["preferences"] if p.get("scope") == "conversation"]
            state["hypotheses"] = [h for h in state["hypotheses"] if h.get("scope", "conversation") == "conversation"]
            state["active_question"] = None
            _invalidate(state)
        return
    if domain == "preference":
        if field not in DIMENSIONS:
            raise ValueError("unknown_preference")
        preferences = state["understanding"]["preferences"]
        target = item.get("target_id")
        matches = [p for p in preferences if p.get("id") == target]
        if op in {"replace", "remove"} and not matches:
            raise ValueError("unknown_target")
        if op in {"replace", "remove"}:
            preferences[:] = [p for p in preferences if p.get("id") != target]
        if op != "remove":
            value = _text(value, 80)
            polarity = item.get("polarity", "prefer")
            if polarity not in {"prefer", "avoid"}:
                raise ValueError("invalid_polarity")
            preferences[:] = [p for p in preferences if not (p["dimension"] == field and p["value"] == value and p["polarity"] == polarity)]
            preferences.append({**meta, "dimension": field, "value": value, "polarity": polarity})
            if len(preferences) > MAX_PREFERENCES:
                raise ValueError("preference_limit")
        _invalidate(state)
        return
    if domain == "requirement":
        if op == "remove":
            target = next((h for h in state["hypotheses"] if h.get("id") == item.get("target_id")), None)
            compact = re.sub(r"\s+", "", evidence["quote"])
            target_text = re.sub(r"\s+", "", target.get("value", "")) if target else ""
            question = state.get("active_question") or {}
            referring = target_text and target_text in compact
            referring = referring or any(topic in target_text and topic in compact for topic in ("계단", "휠체어", "도보", "예약", "무료", "예산", "실내", "주차"))
            referring = referring or (question.get("requirement_id") == item.get("target_id") and bool(re.search(r"그\s*조건|이\s*조건|직접\s*확인", message)))
            if not target or not referring or not re.search(r"해제|빼|없애|필수\s*아니|안\s*지켜|괜찮|직접\s*확인", evidence["quote"]):
                raise ValueError("unconfirmed_requirement_removal")
            state["hypotheses"] = [h for h in state["hypotheses"] if h is not target]
        else:
            _text(value, 160)
            hard = item.get("strength", "unspecified") != "soft" and _hard_evidence(item, evidence, state)
            _unresolved(state, item, evidence, "verification_unavailable", hard=hard)
        _invalidate(state)
        return
    if domain == "condition":
        if op == "replace" and item.get("target_id") != state["field_meta"].get(field, {}).get("id"):
            raise ValueError("unknown_target")
        if op == "remove":
            previous = state["field_meta"].get(field, {})
            if not previous or previous.get("id") != item.get("target_id"):
                raise ValueError("unknown_target")
            clear = {"free_only": False, "budget_krw": "any", "exclude_terms": [], "keywords": [],
                     "walking_preference": "any", "indoor_outdoor": "any"}
            if field not in clear:
                raise ValueError("unsupported_condition_removal")
            value = clear[field]
        normalized = _condition_value(field, value, evidence, message, state)
        conditions.append((field, normalized, meta))
        return
    raise ValueError("unknown_domain")


def interpret(payload, message, state, turn_id):
    """v3 envelope를 항목별 검증해 새 상태로 반환한다. 전체 무효만 ValueError다."""
    if not isinstance(payload, dict) or type(payload.get("schema_version")) is not int or payload["schema_version"] != 1:
        raise ValueError("invalid_dialogue_envelope")
    message, turn_id = _text(message, 1000), _text(turn_id, 80)
    result = deepcopy(state)
    result["latest_moves"] = []
    result["diagnostics"] = {"issues": [], "turn_status": "understood"}
    if set(payload) - {"schema_version", "acts", "updates"}:
        _issue(result, "unknown_metadata")
    valid = 0
    acts = payload.get("acts", [])
    if not isinstance(acts, list):
        _issue(result, "invalid_acts")
        acts = []
    if len(acts) > MAX_ACTS:
        _issue(result, "act_limit")
    for act in acts[:MAX_ACTS]:
        if len(result["latest_moves"]) >= MAX_ACTS:
            _issue(result, "act_limit")
            break
        try:
            if not isinstance(act, dict) or act.get("type") not in ACTS:
                raise ValueError("invalid_act")
            evidence = _evidence(act.get("evidence"), message, turn_id)
            question = result.get("active_question")
            question_id = act.get("question_id")
            if question_id and (not question or question.get("id") != question_id):
                _issue(result, "unknown_question", act)
                question_id = None
            move = {"type": act["type"], "question_id": question_id, "evidence": evidence}
            if act["type"] == "proceed":
                mode = act.get("mode", "explore")
                visit_request = bool(re.search(r"(?:방문|나들이|여행|공연|전시).{0,12}(?:계획|일정)|코스|동선|일정.{0,8}(?:짜|계획)", evidence["quote"]))
                rejected = bool(re.search(r"(?:방문\s*계획|일정|코스|동선).{0,5}(?:말고|아니|필요\s*없|하지\s*마)", evidence["quote"]))
                if not isinstance(mode, str) or mode not in {"visit", "explore"}:
                    _issue(result, "invalid_proceed_mode", act)
                    mode = "explore"
                if mode == "visit" and (not visit_request or rejected):
                    _issue(result, "visit_request_not_explicit", act)
                    mode = "explore"
                move["mode"] = mode
            result["latest_moves"].append(move)
            valid += 1
        except (ValueError, TypeError, KeyError) as exc:
            _issue(result, str(exc), act)
    updates = payload.get("updates", [])
    if not isinstance(updates, list):
        _issue(result, "invalid_updates")
        updates = []
    conditions = []
    ordered = sorted(updates[:MAX_UPDATES], key=lambda item: 0 if isinstance(item, dict) and item.get("domain") == "service" else 1)
    for item in ordered:
        evidence = None
        try:
            if not isinstance(item, dict):
                raise ValueError("invalid_update")
            _text(item.get("id"), 60)
            evidence = _evidence(item.get("evidence"), message, turn_id)
            # 후보별 복사로 잘못된 replace가 이전 값을 지우지 못하게 한다.
            candidate = deepcopy(result)
            pending = []
            _apply_update(candidate, item, evidence, message, pending)
            result = candidate
            conditions.extend(pending)
            valid += 1
        except (ValueError, TypeError, KeyError, AttributeError) as exc:
            _issue(result, str(exc), item)
            if evidence and isinstance(item, dict) and item.get("strength") == "hard" and _hard_evidence(item, evidence, result):
                _unresolved(result, item, evidence, str(exc), hard=True)
    if len(updates) > MAX_UPDATES:
        _issue(result, "update_limit")
    if not valid:
        raise ValueError("no_valid_dialogue_meaning")
    _condition_group(result, conditions)
    # 알려진 명시 필수 표현은 모델 누락 시에도 유실하지 않는다. 일반 목적의 '꼭'은 해당하지 않는다.
    for match in re.finditer(r"무료\s*만|계단\s*(?:없음|없는|없어야)|휠체어.{0,8}(?:필수|출입\s*가능|가능한\s*곳)|(?:걸어서|도보)\s*\d+\s*분\s*(?:안|이내)", message):
        term = match.group()
        suffix = message[match.end():match.end() + 16]
        if re.match(r"\s*(?:조건)?\s*(?:은|는|을|를)?\s*(?:해제|빼|필수\s*아니|괜찮|필요\s*없)", suffix):
            continue
        if term.replace(" ", "") == "무료만" and result["conditions"].get("free_only") is True:
            continue
        if not any(h.get("value") == term for h in result["hypotheses"]):
            _unresolved(result, {"id": turn_id + ":hard:" + str(match.start()), "field": "free_only" if "무료" in term else "requirement"},
                        {"turn_id": turn_id, "quote": term}, "explicit_requirement_unresolved", hard=True)
    proceeding = [move for move in result["latest_moves"] if move["type"] == "proceed"]
    if proceeding:
        result["request_mode"] = proceeding[-1].get("mode", "explore")
    question = result.get("active_question")
    if question and not any(move["type"] == "explain_question" for move in result["latest_moves"]):
        target = question.get("target")
        answered = (target == "start_location" and bool(result["conditions"].get("start_query"))) or (
            target == "service" and result["understanding"]["service"] != "any") or (
            target == "taste" and bool(result["understanding"]["preferences"]))
        if answered:
            result["active_question"] = None
    if result["diagnostics"]["issues"]:
        result["diagnostics"]["turn_status"] = "partial"
    return result


def _question(state, target, text, reason):
    """현재 질문 대상을 보존한다. 호출자가 반환한 질문을 상태와 이력에 기록한다."""
    previous = state.get("active_question")
    count = sum(q.get("target") == target for q in state.get("question_history", []) if isinstance(q, dict))
    if previous and previous.get("target") == target:
        return {**previous, "text": text, "reason": reason}
    return {"id": "q:" + target + ":" + str(count + 1), "target": target,
            "text": text, "reason": reason, "attempt": count + 1}


def content_choice_event(state, message):
    """현재 표시 묶음의 명시 번호/유일한 이름만 선택 이벤트로 해석한다. 사실/모델 호출은 없다."""
    text = message.strip().rstrip(".!?。")
    match = re.fullmatch(r"(?:(?:저는|그럼)\s*)?(?:(\d{1,2})\s*번(?:째)?|(첫|두|세|네|다섯)\s*번째|(일|이|삼|사|오)\s*번(?:째)?)\s*"
                        r"(?:이|가|을|를)?\s*(?:으로|로)?\s*(?:할래요?|할게요?|하자|갈래요?|선택(?:할게요?|해줘)?|좋아요?|요)?", text)
    batch = state.get("display_batch") or {}
    ids = batch.get("candidate_ids", [])
    identity = None
    if match:
        ordinal = int(match[1]) if match[1] else {"첫": 1, "두": 2, "세": 3, "네": 4, "다섯": 5,
                                               "일": 1, "이": 2, "삼": 3, "사": 4, "오": 5}[match[2] or match[3]]
        if not batch:
            return {"selection_error": "no_current_content_batch"}
        if ordinal < 1 or ordinal > len(ids):
            return {"selection_error": "content_number_out_of_range"}
        identity = ids[ordinal - 1]
    elif batch:
        names = {}
        for fact in state.get("tool_facts", []):
            for candidate in fact.get("candidates", []):
                if candidate.get("id") not in ids:
                    continue
                name = candidate.get("title")
                if isinstance(name, str) and name:
                    names.setdefault(name, set()).add(candidate["id"])
        matched = set()
        for name, candidates in names.items():
            if text == name or text in {name + suffix for suffix in (" 갈래", " 갈래요", "로 할래", "으로 할래", " 선택", " 선택할게요")}:
                matched.update(candidates)
        if len(matched) == 1:
            identity = matched.pop()
        elif len(matched) > 1:
            return {"selection_error": "ambiguous_content_name"}
    if identity is None:
        return None
    return {"type": "select_content", "candidate_id": identity,
            "result_execution_key": batch.get("execution_key"), "display_batch_id": batch.get("id")}


def _selection_conditions(conditions):
    """탐색과 같은 출발지 의미값(label/좌표)만 비교하고 주소 등 표시 메타는 제외한다."""
    result = deepcopy(conditions)
    origin = result.get("start_location")
    if origin is not None:
        if not isinstance(origin, dict):
            raise ValueError("invalid_origin")
        result["start_location"] = dict(label=origin.get("label"), lat=coordinate(origin.get("lat"), 90),
                                        lng=coordinate(origin.get("lng"), 180))
    return result


def _selected_candidate(state, event):
    """클라이언트 값 대신 현재 결과/표시 묶음/실제 tool 후보를 대조한 snapshot을 반환한다."""
    context, batch = state.get("result_context") or {}, state.get("display_batch") or {}
    key = context.get("execution_key")
    if not key or batch.get("execution_key") != key or event.get("result_execution_key") != key or event.get("display_batch_id") != batch.get("id"):
        raise ValueError("stale_content_batch")
    if ("conditions" in context and _selection_conditions(context["conditions"]) != _selection_conditions(state.get("conditions", {}))) or (
            context.get("service") and context["service"] != state["understanding"]["service"]):
        raise ValueError("stale_content_batch")
    if state.get("pending_changes") or state.get("origin_lookup_required") or any(
            h.get("strength") == "hard" and h.get("status") in {"unresolved", "ambiguous", "invalid"} for h in state.get("hypotheses", [])):
        raise ValueError("content_conditions_pending")
    identity = event.get("candidate_id")
    if not isinstance(identity, str) or identity not in batch.get("candidate_ids", []):
        raise ValueError("unknown_content_choice")
    for fact in state.get("tool_facts", []):
        if (fact.get("result_context") or {}).get("execution_key") != key or fact.get("status") != "ok" or fact.get("blocked"):
            continue
        candidate = next((item for item in fact.get("candidates", []) if item.get("id") == identity), None)
        if candidate:
            return deepcopy(candidate)
    raise ValueError("unknown_content_choice")


def decide(state):
    """알고 있는 의미와 실행 가능성으로 행동을 고른다. 선택 조건을 입력 폼으로 만들지 않는다."""
    understanding, conditions = state["understanding"], state["conditions"]
    service = understanding.get("service", "any")
    info = capability(service)
    moves = {move["type"] for move in state.get("latest_moves", [])}
    question = state.get("active_question")
    explaining = "explain_question" in moves
    notice = state.get("selection_notice") or ""
    prefix = ""
    if explaining and question:
        prefix = {"start_location": "콘텐츠를 찾을 지역을 여쭤본 거예요.", "taste": "어떤 분위기나 내용이 좋은지 여쭤본 거예요."}.get(question.get("target"), question.get("reason", "질문의 뜻을 설명할게요.")) + " "
    elif "complain" in moves or "correct" in moves:
        prefix = info["label"] + " 쪽으로 원하시는 목적은 기억하고 있어요. "
    prefix = notice + prefix
    if moves == {"chitchat"} and not state.get("pending_changes") and service == "any" and not state.get("result_context"):
        text = "편하게 말씀해 주세요. 공연이나 전시처럼 어떤 나들이가 끌리세요?"
        return {"type": "reply", "text": text, "question": _question(state, "service", text, "원하시는 활동부터 함께 고르려는 질문이에요.")}
    pending = state.get("pending_changes", [])
    if pending:
        item = pending[0]
        text = f"이미 확인한 {FIELD_LABELS.get(item['field'], '조건')}을 바꾸려는 요청이에요. 새 값으로 바꿀까요?"
        return {"type": "reply", "text": prefix + text, "question": _question(state, "confirm_change", text, "확정한 값의 실제 변경 확인"), "pending_id": item["id"]}
    if conditions.get("start_query") and (state.get("origin_lookup_required") or not conditions.get("start_location")):
        return {"type": "resolve_origin", "query": conditions["start_query"], "text": prefix + "말씀하신 지역의 실제 위치를 확인할게요."}
    if not conditions.get("start_location"):
        count = sum(q.get("target") == "start_location" for q in state.get("question_history", []) if isinstance(q, dict))
        text = "어느 동네나 역에서 출발하세요?" if not count else "지역 이름만 있으면 돼요. 예를 들어 서울시청이나 개포동 중 어디 근처에서 찾아볼까요?"
        return {"type": "reply", "text": prefix + text, "question": _question(state, "start_location", text, "실제 주변 콘텐츠의 검색 중심이 필요해요.")}
    blocked = [h for h in state.get("hypotheses", []) if h.get("strength") == "hard" and h.get("status") == "unresolved"]
    if blocked:
        item = blocked[0]
        text = f"꼭 지키려는 ‘{item['value']}’ 조건은 기억하고 있어요. 현재 정보로 충족 여부를 확인하지 못해요. 필수로 유지할까요, 직접 확인할 조건으로 바꿀까요?"
        requirement_question = _question(state, "requirement", text, "확인하지 못한 필수 조건을 몰래 해제하지 않기 위해서예요.")
        requirement_question["requirement_id"] = item["id"]
        return {"type": "reply", "text": prefix + text, "question": requirement_question}
    selected = state.get("selected_content")
    if "content_selected" in moves and selected:
        return {"type": "content_selected", "candidate": deepcopy(selected),
                "text": f"‘{selected['title']}’을 골랐어요. 같은 장소의 상세에서 운영 안내를 확인하거나 지도를 볼 수 있어요."}
    if state.get("result_context") and state.get("request_mode") != "visit" and "retry_tool" not in moves:
        if "request_alternatives" in moves:
            return {"type": "show_alternatives", "text": "같은 조건으로 다른 후보를 보여드릴게요."}
        if selected:
            return {"type": "reply", "text": prefix + f"‘{selected['title']}’ 선택은 유지했어요. 이 장소의 상세를 보거나 바꾸고 싶은 조건을 말씀해 주세요."}
        text = prefix + info["label"] + " 후보를 보고 있어요. 마음에 드는 카드의 ‘이곳 선택’을 누르거나 번호를 말씀해 주세요."
        return {"type": "reply", "text": text}
    if moves == {"chitchat"} and service != "any":
        return {"type": "reply", "text": prefix + info["label"] + " 나들이를 찾는 중이에요. 원하는 분위기를 더 말씀하시거나 지금 조건으로 찾아볼 수 있어요."}
    if state.get("request_mode") == "visit":
        if not conditions.get("start_at") or not conditions.get("end_at"):
            target = "start_at" if not conditions.get("start_at") else "end_at"
            text = "방문할 날짜와 시작 시각을 알려 주시겠어요?" if target == "start_at" else "언제까지 시간이 되시는지 알려 주시겠어요?"
            return {"type": "reply", "text": prefix + text, "question": _question(state, target, text, "방문 일정과 최소 가용시간을 확인하는 단계예요.")}
        return {"type": "visit", "text": prefix + "선택한 일정의 실제 운영 조건과 이동 가능성을 확인할게요."}
    text = "말씀하신 취향과 확인된 조건으로 실제 " + info["label"] + " 콘텐츠를 찾아볼게요."
    if service == "movie":
        text = "영화관 위치를 찾아볼게요. 말씀하신 영화 취향은 기억하지만 작품·상영시간·예매 정보는 아직 조회하지 못해요."
    return {"type": info["action"], "query": info["query"], "text": prefix + text}


def apply_event(state, event):
    """검증된 UI 선택/동의 이벤트를 새 상태로 반영한다. 실제 후보의 출처 검증은 호출자 소유다."""
    if not isinstance(event, dict):
        raise ValueError("invalid_event")
    result = deepcopy(state)
    kind = event.get("type")
    if kind == "select_content":
        result["selected_content"] = _selected_candidate(result, event)
        result["active_question"] = None
        result["latest_moves"] = [{"type": "content_selected"}]
    elif kind == "select_origin":
        place = event.get("place", event.get("data", event.get("location")))
        if not isinstance(place, dict):
            raise ValueError("invalid_origin")
        label = _text(place.get("label", place.get("title")), 160)
        value = {"label": label, "lat": coordinate(place.get("lat"), 90), "lng": coordinate(place.get("lng"), 180)}
        if isinstance(place.get("address"), str):
            value["address"] = _text(place["address"], 300)
        before = result["conditions"].get("start_location")
        if before and before != value and result["field_meta"].get("start_location", {}).get("confirmed"):
            result["pending_changes"].append({"id": event.get("id", "origin_change"), "field": "start_location", "before": before, "after": value, "changes": {"start_location": value}, "metadata": {"start_location": {"source": "tool_verified", "confirmed": True}}})
        else:
            _set_condition(result, "start_location", value, {"source": "tool_verified", "confirmed": True})
        result["conditions"].pop("start_query", None)
        result.pop("origin_lookup_required", None)
        result["active_question"] = None
    elif kind in {"confirm_change", "dismiss_change"}:
        target = event.get("pending_id", event.get("id", event.get("field")))
        pending = next((p for p in result["pending_changes"] if p["id"] == target or p["field"] == target), None)
        if pending is None:
            raise ValueError("unknown_pending_change")
        result["pending_changes"] = [p for p in result["pending_changes"] if p is not pending]
        if kind == "confirm_change":
            for field, value in pending["changes"].items():
                meta = {**pending.get("metadata", {}).get(field, {}), "confirmed": True}
                _set_condition(result, field, value, meta)
        result["active_question"] = None
    elif kind == "proceed":
        result["request_mode"] = "visit" if event.get("mode") == "visit" else "explore"
        if event.get("sort") not in (None, "distance"):
            raise ValueError("invalid_sort")
        if event.get("sort") == "distance":
            _set_condition(result, "walking_preference", "short",
                           {"id": "choice:distance", "source": "user_explicit", "confirmed": False, "strength": "soft"})
        result["latest_moves"] = [{"type": "proceed"}]
    elif kind in {"restore", "restoration"}:
        snapshot = event.get("snapshot", event.get("data"))
        if not isinstance(snapshot, dict):
            raise ValueError("invalid_snapshot")
        result = new_state()
        understanding = snapshot.get("understanding", {})
        if isinstance(understanding, dict):
            if understanding.get("goal"):
                result["understanding"]["goal"] = _text(understanding["goal"])
                result["field_meta"]["goal"] = {"id": "restored:goal", "source": "user_explicit", "confirmed": False, "status": "restored_claim"}
            if understanding.get("service") in SERVICES:
                result["understanding"]["service"] = understanding["service"]
                result["field_meta"]["service"] = {"id": "restored:service", "source": "user_explicit", "confirmed": False, "status": "restored_claim"}
            for pref in understanding.get("preferences", [])[:MAX_PREFERENCES]:
                if isinstance(pref, dict) and pref.get("dimension") in DIMENSIONS and pref.get("polarity", "prefer") in {"prefer", "avoid"}:
                    value = _text(pref.get("value"), 80)
                    strength = pref.get("strength", "soft")
                    if strength not in STRENGTHS:
                        raise ValueError("invalid_restored_strength")
                    result["understanding"]["preferences"].append({"id": _text(pref.get("id", "restored"), 60), "dimension": pref["dimension"], "value": value, "polarity": pref.get("polarity", "prefer"), "strength": strength, "source": "user_explicit", "confirmed": False, "scope": pref.get("scope", "conversation")})
        for field, value in snapshot.get("conditions", {}).items():
            if field == "start_location" and isinstance(value, dict) and value.get("label"):
                if value["label"] != "현재 위치":
                    result["conditions"]["start_query"] = _text(value["label"], 80)
            elif field == "unsupported_requirements" and isinstance(value, list):
                for number, requirement in enumerate(value[:MAX_HYPOTHESES]):
                    requirement = _text(requirement, 200)
                    _unresolved(result, {"id": "restored:legacy:" + str(number), "field": "requirement"}, {"turn_id": "restored", "quote": requirement}, "restored_requirement", hard=True)
            elif field in CONDITION_FIELDS:
                if field in {"date", "date_from", "date_to"}:
                    value = date.fromisoformat(_text(value, 10)).isoformat()
                else:
                    value = normalize_proposal({field: value})[field]
                result["conditions"][field] = value
                result["field_meta"][field] = {"source": "user_explicit", "confirmed": False, "status": "restored_claim"}
        for item in snapshot.get("hypotheses", [])[:MAX_HYPOTHESES]:
            if isinstance(item, dict) and item.get("strength") == "hard":
                value = _text(item.get("value"), 200)
                _unresolved(result, {"id": _text(item.get("id", "restored_requirement"), 60), "field": item.get("field", "requirement")}, {"turn_id": "restored", "quote": value}, "restored_requirement", hard=True)
        question = snapshot.get("active_question")
        if isinstance(question, dict) and question.get("target") in {"service", "taste", "start_location", "date", "start_at", "end_at", "requirement", "confirm_change"}:
            result["active_question"] = {"id": _text(question.get("id"), 80), "target": question["target"], "text": _text(question.get("text"), 400), "reason": _text(question.get("reason", "이전 대화의 질문을 복원했어요."), 400), "source": "restored_claim"}
            if question.get("requirement_id") in {h["id"] for h in result["hypotheses"]}:
                result["active_question"]["requirement_id"] = question["requirement_id"]
        result["diagnostics"] = {"issues": [], "turn_status": "restored"}
    else:
        raise ValueError("unsupported_event")
    return result
