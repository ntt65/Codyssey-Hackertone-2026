"""AI 해석 결과를 추천 조건 초안으로 병합한다. 네트워크·저장·추천 실행은 하지 않는다.

LLM이 전달한 좌표/행사 사실은 거절한다. 확인된 조건은 동의 전 유지하고,
revision이 바뀐 응답은 폐기한다. 실제 AI 공급자와 프론트 연결은 별도다.
"""
from copy import deepcopy
from datetime import datetime

from outing import CATEGORIES, InputError, KST, validate
from preferences import FIELDS as PREFERENCE_FIELDS, normalize

FIELDS = {"start_query", "start_at", "end_at", "category", "request_kind", "stay_minutes"} | PREFERENCE_FIELDS
REQUIRED = ("start_location", "start_at", "end_at", "category", "request_kind")
QUESTIONS = {
    "start_location": "어디에서 출발하세요? 장소 검색 결과에서 출발지를 선택해 주세요.",
    "start_at": "출발 날짜와 시각을 알려 주세요.",
    "end_at": "나들이를 마칠 날짜와 시각을 알려 주세요.",
    "category": "어떤 문화활동을 원하세요?",
    "request_kind": "행사 한 곳을 찾을까요, 두 곳 코스를 찾을까요?",
    "stay_minutes": "전시 한 곳에서 몇 분 머무를까요?",
}


def normalize_proposal(proposal):
    """허용된 조건만 정규화한다. null은 변경 없음, 좌표·잘못된 값은 ValueError다."""
    if not isinstance(proposal, dict) or set(proposal) - FIELDS:
        raise ValueError("AI 조건 형식을 확인해 주세요.")
    result = normalize(proposal)
    for field, value in proposal.items():
        if value is None or field in PREFERENCE_FIELDS:
            continue
        if field == "start_query":
            if not isinstance(value, str) or not 1 <= len(value.strip()) <= 80 or any(ord(c) < 32 for c in value):
                raise ValueError("출발지 검색어 형식이 잘못됐습니다.")
            value = value.strip()
        elif field in {"start_at", "end_at"}:
            if not isinstance(value, str):
                raise ValueError("날짜와 시각 형식이 잘못됐습니다.")
            parsed = datetime.fromisoformat(value)
            if parsed.tzinfo is None:
                raise ValueError("시간대가 필요합니다.")
            value = parsed.astimezone(KST).isoformat(timespec="seconds")
        elif field == "category":
            if not isinstance(value, str) or value not in CATEGORIES:
                raise ValueError("지원하는 대표 분류를 선택해 주세요.")
        elif field == "request_kind":
            if value not in ("place", "course", "route"):
                raise ValueError("추천 종류를 확인해 주세요.")
            value = "course" if value == "route" else value
        elif type(value) is not int or not 1 <= value <= 240:
            raise ValueError("체류시간은 1~240분 정수여야 합니다.")
        result[field] = value
    # 분류와 복수 관심사는 하나의 변경 단위로 병합한다.
    if "categories" in result:
        result["category"] = result["categories"][0]
    elif "category" in result:
        result["categories"] = [result["category"]]
    if "categories" in result and "music_followup" not in result:
        result["music_followup"] = False
    return result


def summarize(draft, revision, conflicts=None):
    """코드로 누락·추천 입력·60분을 검사한다. ready는 S02a 진입 가능이며 추천 승인이 아니다."""
    conflicts = deepcopy(conflicts or [])
    missing = [field for field in REQUIRED if draft.get(field) is None or draft.get(field) == ""]
    if draft.get("request_kind") in ("course", "route") and draft.get("stay_minutes") is None:
        missing.append("stay_minutes")
    errors = []
    if not any(field in missing for field in REQUIRED):
        try:
            validate(draft)
        except InputError as exc:
            errors.append(dict(field=exc.field, code=exc.code, message=str(exc)))
    if draft.get("request_kind") in ("course", "route") and "stay_minutes" not in missing:
        value = draft.get("stay_minutes")
        if type(value) is not int or not 1 <= value <= 240:
            errors.append(dict(field="stay_minutes", code="invalid_stay", message="체류시간은 1~240분 정수여야 합니다."))
    if conflicts:
        message = "이미 확인한 조건과 달라요. 변경 전후를 확인하고 반영할 항목을 선택해 주세요."
    elif errors:
        message = errors[0]["message"]
    elif draft.get("unsupported_requirements"):
        message = "아직 확인할 수 없는 필수 조건이에요: " + ", ".join(draft["unsupported_requirements"]) + ". 필수로 유지할까요, 직접 확인할 조건으로 바꿀까요?"
    elif draft.get("music_followup"):
        message = "음악이라면 국악·클래식·콘서트를 찾아볼 수 있어요. 어떤 음악이 좋으세요? 골고루 듣고 싶다고 하셔도 돼요."
    elif missing:
        message = QUESTIONS[missing[0]]
    else:
        message = "조건이 준비됐어요. 조건 확인 화면에서 확인한 뒤 추천받기를 눌러 주세요."
    return dict(status="needs_confirmation" if conflicts else "draft", base_revision=revision,
                assistant_text=message, updated_condition_draft=deepcopy(draft),
                missing_fields=missing, field_errors=errors, conflicts=conflicts,
                ready_to_search=not (missing or errors or conflicts or draft.get("music_followup") or draft.get("unsupported_requirements")), requires_final_confirmation=True)


def put_value(draft, field, value):
    """출발지 검색어가 바뀌면 이전 좌표를 제거한다. 다른 조건은 초안에만 반영한다."""
    draft[field] = deepcopy(value)
    if field == "categories":
        draft["category"] = value[0]
    if field == "start_query":
        draft.pop("start_location", None)


def apply_interpretation(draft, proposal, confirmed_fields, base_revision, current_revision):
    """해석 결과를 복사한 초안에 반영한다. 확정값 충돌·늦은 응답은 자동 반영하지 않는다."""
    if (not isinstance(draft, dict) or not isinstance(confirmed_fields, list)
            or any(not isinstance(f, str) or f not in FIELDS | {"start_location"} for f in confirmed_fields)
            or type(base_revision) is not int or type(current_revision) is not int
            or min(base_revision, current_revision) < 0):
        raise ValueError("대화 상태 형식을 확인해 주세요.")
    if base_revision != current_revision:
        return dict(status="stale", base_revision=base_revision, ready_to_search=False)
    changes = normalize_proposal(proposal)
    # 확정 분류를 거절해도 연결된 categories/music_followup이 몰래 바뀌지 않게 묶는다.
    category_change = {k: changes.pop(k) for k in ("category", "categories", "music_followup") if k in changes}
    if category_change:
        categories = category_change.get("categories", draft.get("categories", [draft["category"]] if draft.get("category") else None))
        if categories:
            changes["categories"] = categories
        if "music_followup" in category_change:
            changes["music_followup"] = category_change["music_followup"]
    updated = deepcopy(draft)
    conflicts = []
    for field, value in changes.items():
        before = draft.get(field)
        protected = field in confirmed_fields
        if field == "categories":
            before = draft.get("categories", [draft["category"]] if draft.get("category") else None)
            protected = protected or "category" in confirmed_fields
            if before != value and before is not None and protected:
                conflicts.append(dict(field="category", before=draft.get("category"), after=value[0],
                                      related={"categories": value, "music_followup": category_change.get("music_followup", False)}))
                continue
        if field == "music_followup" and any(c["field"] == "category" for c in conflicts):
            continue
        if field == "start_query" and draft.get("start_location"):
            before = draft["start_location"]
            # 이름만으로 장소의 동일성을 판단하지 않는다. 같은 이름도 재검색·선택한다.
            protected = True
        if before == value:
            continue
        if before is not None and protected:
            conflicts.append(dict(field=field, before=deepcopy(before), after=value))
        else:
            put_value(updated, field, value)
    return summarize(updated, base_revision, conflicts)


def resolve_changes(result, decisions, current_draft, current_revision):
    """동일 초안/revision에서 명시적 bool 동의만 반영한다. 미응답 충돌은 유지한다."""
    if (current_revision != result["base_revision"]
            or current_draft != result["updated_condition_draft"]):
        return dict(status="stale", base_revision=result["base_revision"], ready_to_search=False)
    fields = {item["field"] for item in result["conflicts"]}
    if not isinstance(decisions, dict) or set(decisions) - fields or any(type(v) is not bool for v in decisions.values()):
        raise ValueError("변경 동의는 항목별 참/거짓으로 전달해 주세요.")
    updated = deepcopy(current_draft)
    unresolved = []
    for item in result["conflicts"]:
        field = item["field"]
        if field not in decisions:
            unresolved.append(item)
        elif decisions[field]:
            put_value(updated, field, item["after"])
            for key, value in item.get("related", {}).items():
                put_value(updated, key, value)
    return summarize(updated, current_revision, unresolved)
