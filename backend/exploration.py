"""v3 콘텐츠 탐색: 방문 일정을 만들어 내지 않고 실제 행사/장소와 적용 근거를 반환한다.

입력은 dialogue state의 understanding/conditions다. 외부 조회 실패와 정상 0건을
구분하며, 가격/기간/거리 hard 조건은 실제 자료로 판정한다. 선택 ranker는 기존
후보의 관련성만 제안할 수 있고 ID/인용문은 코드가 검증한다. legacy 추천은 변경하지 않는다.
"""
from copy import deepcopy
from datetime import date, datetime
import hashlib
import json
import math
import re
from urllib.parse import parse_qs, urlsplit

import outing
import places
import preferences
from culture_config import culture_key

VENUE_QUERIES = {"movie": "영화관", "cafe": "카페", "food": "음식점", "restaurant": "음식점",
                 "walk": "공원", "experience": "체험", "travel": "관광명소"}
PERFORMANCE_GENRES = {"국악", "클래식", "콘서트", "연극", "무용", "뮤지컬", "오페라", "독주", "독창회"}
RANK_FIELDS = {"title", "venue", "genre", "description"}
# 정책상 주 산책 목적지로 확인할 상세분류. 장소명 문자열은 이 판정에 쓰지 않는다.
WALK_MAIN_TYPES = {"공원", "도시공원", "도시근린공원", "근린공원", "어린이공원", "소공원",
                   "수변공원", "생태공원", "자연공원", "국립공원", "도립공원", "군립공원",
                   "산책로", "산책길", "둘레길", "숲길"}
WALK_AMENITY_TYPES = {"화장실", "공중화장실", "공공화장실", "개방화장실", "이동식화장실", "장애인화장실",
                      "주차장", "공영주차장", "민영주차장", "부설주차장", "노외주차장", "노상주차장",
                      "관리사무소", "공원관리사무소", "관리소", "공원관리소", "관리센터", "관리시설",
                      "매표소", "안내소", "출입구", "입구", "출구", "편의시설", "부대시설", "수유실"}
# 카카오 공식 Local CategoryGroupCode. AT4(관광명소)는 범위가 넓어 승인 근거로 쓰지 않는다.
WALK_OTHER_GROUPS = {"MT1", "CS2", "PS3", "SC4", "AC5", "OL7", "SW8", "BK9",
                     "CT1", "AG2", "PO3", "AD5", "FD6", "CE7", "HP8", "PM9"}


def _digest(value):
    """JSON으로 표현 가능한 조건/사실의 순서 독립 fingerprint를 반환한다."""
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, default=str).encode()).hexdigest()


def _text(value, limit=2000):
    """공급자 문자열만 길이 제한해 읽는다. 결측을 임의 설명으로 채우지 않는다."""
    return value.strip()[:limit] if isinstance(value, str) and value.strip() else None


def _day(value, field):
    """명시 날짜를 ISO 날짜로 검증한다. 잘못된 날짜는 InputError로 전달한다."""
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise outing.InputError("invalid_date", field, "날짜를 다시 확인해 주세요.")
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise outing.InputError("invalid_date", field, "날짜를 다시 확인해 주세요.") from None


def _inputs(state):
    """canonical 상태와 이전 draft/dialogue 별칭을 읽고 좌표/선택 필터만 검증한다."""
    understanding = state.get("understanding", state.get("dialogue", {}))
    conditions = deepcopy(state.get("conditions", state.get("draft", {})))
    if not isinstance(understanding, dict) or not isinstance(conditions, dict):
        raise outing.InputError("invalid_state", "state", "대화 상태를 다시 확인해 주세요.")
    service = understanding.get("service", "any")
    if service not in {"any", "performance", "exhibition", *VENUE_QUERIES}:
        raise outing.InputError("unsupported_service", "service", "찾을 활동을 다시 말씀해 주세요.")
    origin = conditions.get("start_location", conditions.get("startLocation"))
    if not isinstance(origin, dict) or not _text(origin.get("label")):
        raise outing.InputError("invalid_location", "start_location", "찾을 지역을 말씀해 주세요.")
    try:
        lat, lng = outing.coordinate(origin.get("lat"), 90), outing.coordinate(origin.get("lng"), 180)
    except ValueError:
        raise outing.InputError("invalid_coordinate", "start_location", "확인된 지역 좌표가 필요해요.") from None
    conditions["start_location"] = dict(label=origin["label"], lat=lat, lng=lng)
    try:
        options = preferences.normalize(conditions)
    except ValueError as exc:
        raise outing.InputError("invalid_preferences", "preferences", str(exc)) from None
    return understanding, conditions, service, (lat, lng), options


def _window(conditions):
    """선택한 날짜/기간·시각만 읽는다. 미입력 날짜와 종료시각을 생성하지 않는다."""
    first = last = None
    if conditions.get("date"):
        first = last = _day(conditions["date"], "date")
    if conditions.get("date_from"):
        first = _day(conditions["date_from"], "date_from")
    if conditions.get("date_to"):
        last = _day(conditions["date_to"], "date_to")
    times = []
    for field in ("start_at", "end_at"):
        value = conditions.get(field)
        if value is None:
            times.append(None)
            continue
        try:
            parsed = datetime.fromisoformat(value)
            if parsed.tzinfo is None:
                raise ValueError("timezone missing")
            parsed = parsed.astimezone(outing.KST)
        except (ValueError, TypeError):
            raise outing.InputError("invalid_time", field, "시간대를 포함한 시각을 다시 확인해 주세요.") from None
        times.append(parsed)
    start, end = times
    if conditions.get("date") and any(value and value.date() != first for value in (start, end)):
        raise outing.InputError("conflicting_date", "date", "날짜와 시각의 날짜가 서로 달라요. 방문일을 다시 확인해 주세요.")
    if start and not first:
        first = start.date()
    if end and not last:
        last = end.date()
    if (first and last and first > last) or (start and end and (start >= end or start.date() != end.date())):
        raise outing.InputError("invalid_time_range", "end_at", "날짜와 시간 순서를 다시 확인해 주세요.")
    return first, last, start, end


def _event(row, checked, origin):
    """서울시 실제 행 하나를 기존 행사 카드 필드로 정규화한다. 잘못된 식별/기간은 제외한다."""
    url = urlsplit(row.get("HMPG_ADDR") or "")
    identity = parse_qs(url.query).get("cultcode", [""])[0]
    if (url.scheme not in {"http", "https"} or url.hostname != "culture.seoul.go.kr"
            or url.username or url.password or not identity.isdigit()):
        raise ValueError("invalid event identity")
    title, venue, genre = (_text(row.get(key)) for key in ("TITLE", "PLACE", "CODENAME"))
    if not title or not venue or not genre:
        raise ValueError("missing event fields")
    first, last = (date.fromisoformat(row[key][:10]) for key in ("STRTDATE", "END_DATE"))
    if first > last:
        raise ValueError("invalid event dates")
    try:
        lat, lng = outing.coordinate(row.get("LAT"), 90), outing.coordinate(row.get("LOT"), 180)
        if not lat or not lng:
            raise ValueError("missing coordinates")
        distance = outing.distance_km(*origin, lat, lng)
    except ValueError:
        lat = lng = distance = None
    description = "\n".join(filter(None, (_text(row.get(key)) for key in ("PROGRAM", "CONTENTS", "ETC_DESC")))) or None
    candidate = dict(id="seoul:" + identity, title=title, venue=venue, genre=genre,
                     description=description, lat=lat, lng=lng, distance_km=distance,
                     district=_text(row.get("GUNAME")), address=None,
                     event_start_date=first.isoformat(), event_end_date=last.isoformat(),
                     opening_info=_text(row.get("PRO_TIME")), price_info=_text(row.get("USE_FEE")),
                     fee_type=_text(row.get("IS_FREE")), audience=_text(row.get("USE_TRGT")),
                     official_url=url.geturl(), image_url=outing.official_image(row.get("MAIN_IMG")),
                     fixed_start_at=None, source="seoul_culture", candidate_kind="cultural_event",
                     status="check", visit_status="not_checked", visit_validation_context=None,
                     checks_required=["콘텐츠 탐색 결과 · 방문 날짜의 운영·예약·이동 가능성 별도 확인"],
                     source_checked_at=checked)
    return candidate


def _venue(place, checked, service, origin):
    """실지도 장소를 카드 형태로 바꾼다. 영화관을 상영작/회차나 검증된 방문계획으로 바꾸지 않는다."""
    title = _text(place.get("label"))
    if not title or not _text(place.get("id")):
        raise ValueError("missing venue identity")
    lat, lng = outing.coordinate(place.get("lat"), 90), outing.coordinate(place.get("lng"), 180)
    return dict(id=place["id"], title=title, label=title, venue=title, lat=lat, lng=lng,
                distance_km=outing.distance_km(*origin, lat, lng),
                address=_text(place.get("road_address")) or _text(place.get("address")), district=None,
                genre=_text(place.get("category_name")), description=None, image_url=None,
                category_name=_text(place.get("category_name")),
                category_group_code=_text(place.get("category_group_code")),
                category_group_name=_text(place.get("category_group_name")),
                event_start_date=None, event_end_date=None, fixed_start_at=None,
                opening_info=None, price_info=None, fee_type=None, audience=None,
                official_url=_text(place.get("official_url")), source="kakao_local", candidate_kind="venue",
                service=service, status="check", visit_status="not_checked", visit_validation_context=None,
                checks_required=["장소 위치 정보 · 운영시간·요금·예약 별도 확인"]
                + (["영화 작품·상영 회차·좌석 정보 미연동"] if service == "movie" else []),
                source_checked_at=checked)


def _source(service, conditions, options, origin, mode, first):
    """기존 공급자 조회를 재사용한다. validate/recommend의 필수 일정 생성 경로는 호출하지 않는다."""
    if service in VENUE_QUERIES:
        if mode != "live":
            raise RuntimeError("venue recordings unavailable")
        status, data = places.search_places(dict(query=VENUE_QUERIES[service], type="keyword",
                                                origin=dict(lat=origin[0], lng=origin[1])))
        if status != 200 or data.get("status") not in {"ready", "no_results"}:
            raise RuntimeError("venue source unavailable")
        checked = data.get("source_checked_at") or datetime.now(outing.KST).isoformat(timespec="seconds")
        candidates, invalid = [], 0
        for place in data.get("places", []):
            try:
                candidates.append(_venue(place, checked, service, origin))
            except (ValueError, TypeError, KeyError):
                invalid += 1
        return candidates, dict(source="kakao_local", source_checked_at=checked,
                                source_total=data.get("source_total"), source_limit=5,
                                queried_query=VENUE_QUERIES[service],
                                scope="검증된 좌표에서 직선거리순 장소 최대5건 · 반경 제한 및 영업 여부 미검증"), invalid
    categories = options.get("categories") or ([conditions["category"]] if conditions.get("category") else [])
    category = categories[0] if len(categories) == 1 else "전시" if service == "exhibition" else "전체"
    anchor = (first or datetime.now(outing.KST).date()).isoformat()
    rows, checked, total = outing.seoul_page(anchor, category, mode)
    access = "recorded" if mode == "recorded" else "authenticated" if culture_key("seoul") else "sample"
    limit = outing.SEOUL_FETCH_LIMIT if access == "authenticated" else 5
    candidates, invalid = [], 0
    for row in rows:
        try:
            candidate = _event(row, checked, origin)
            parts = set(re.split(r"[/·,]", candidate["genre"]))
            if service == "exhibition" and not any("전시" in part for part in parts):
                continue
            if service == "performance" and not parts & PERFORMANCE_GENRES:
                continue
            if categories and "전체" not in categories and not parts & set(categories):
                continue
            candidates.append(candidate)
        except (ValueError, TypeError, KeyError, AttributeError):
            invalid += 1
    return list({item["id"]: item for item in candidates}.values()), dict(
        source="seoul_culture", source_checked_at=checked, source_total=total, source_limit=limit,
        queried_category=category, access=access,
        scope=f"서울시 {access} 공개 행사 최대{limit}건의 조회 범위 · 서울 전체 콘텐츠 보유/방문 보장 아님"), invalid


def _walk_eligibility(candidates):
    """공급자 분류로 주 산책 목적지만 남긴다. 이름·거리·모델 점수는 승인 근거가 아니다.

    상세 경로의 마지막 분류가 주 목적지여야 하며 경로 중 부대시설 또는 PK6는
    먼저 제외한다. 분류 결측·미지원 leaf·AT4만 있는 경우는 미확인으로 남긴다.
    원 ID/좌표를 보존하며 부모 공원 생성·추가 조회·다른 활동 분류는 수행하지 않는다.
    """
    accepted = []
    counts = dict(walk_amenity=0, walk_incompatible=0, walk_unverified=0)
    for candidate in candidates:
        category = candidate.get("category_name")
        path = [re.sub(r"\s+", "", part) for part in category.split(">") if part.strip()] if isinstance(category, str) else []
        group = candidate.get("category_group_code")
        if group == "PK6" or any(part in WALK_AMENITY_TYPES for part in path):
            counts["walk_amenity"] += 1
            continue
        if group in WALK_OTHER_GROUPS:
            counts["walk_incompatible"] += 1
            continue
        if not path or path[-1] not in WALK_MAIN_TYPES:
            counts["walk_unverified"] += 1
            continue
        candidate["eligibility"] = dict(status="eligible", service="walk", basis="provider_category",
                                         category_name=category, category_path=path, category_group_code=group,
                                         reason="main_walk_destination")
        accepted.append(candidate)
    return accepted, dict(service="walk", checked_count=len(candidates), eligible_count=len(accepted),
                          excluded_counts=counts, scope="retrieved_candidates_only")


def _hard_filter(candidates, conditions, options, window, venue_only):
    """실제 기간/요금/명시 제외와 거리 한도를 판정한다. 필요한 사실 결측은 통과시키지 않는다."""
    first, last, start, end = window
    today = datetime.now(outing.KST).date()
    counts = dict(expired=0, date=0, time=0, exclusion=0, price=0, distance=0, unknown=0)
    accepted = []
    unknown = set()
    radius = conditions.get("max_distance_km")
    if radius is not None and (isinstance(radius, bool) or not isinstance(radius, (int, float))
                               or not math.isfinite(radius) or radius < 0):
        raise outing.InputError("invalid_distance", "max_distance_km", "거리 제한을 다시 확인해 주세요.")
    for item in candidates:
        if not venue_only:
            item_first, item_last = date.fromisoformat(item["event_start_date"]), date.fromisoformat(item["event_end_date"])
            if item_last < today:
                counts["expired"] += 1
                continue
            if (first and item_last < first) or (last and item_first > last):
                counts["date"] += 1
                continue
        elif first or last:
            unknown.add("date")
            counts["unknown"] += 1
            continue
        if start or end:
            if venue_only or not (start and end):
                unknown.add("time")
                counts["unknown"] += 1
                continue
            match = outing.time_match(dict(PRO_TIME=item["opening_info"], CODENAME=item["genre"]), start, end)
            if match is not True:
                counts["unknown" if match is None else "time"] += 1
                if match is None:
                    unknown.add("time")
                continue
        source_text = " ".join(str(item.get(field) or "") for field in ("title", "venue", "genre", "district", "description")).casefold()
        if any(term.casefold() in source_text for term in options.get("exclude_terms", [])):
            counts["exclusion"] += 1
            continue
        budget = options.get("budget_krw", "any")
        if options.get("free_only") or budget != "any":
            amount = _price(item)
            if amount is None:
                unknown.add("price")
                counts["unknown"] += 1
                continue
            if (options.get("free_only") and amount != 0) or (budget != "any" and amount > budget):
                counts["price"] += 1
                continue
        if radius is not None:
            if item["distance_km"] is None:
                unknown.add("distance")
                counts["unknown"] += 1
                continue
            if item["distance_km"] > radius:
                counts["distance"] += 1
                continue
        accepted.append(item)
    return accepted, counts, sorted(unknown)


def _price(candidate):
    """무료 표기와 구체 요금이 충돌하면 unknown이다. 복수/부분 유료를 무료로 통과시키지 않는다."""
    amount = preferences.known_price(candidate)
    text = (candidate.get("price_info") or "").strip()
    if candidate.get("fee_type") == "무료" and text and text not in {"무료", "0원", "전석 0원"}:
        return None
    if candidate.get("fee_type") == "유료" and amount == 0:
        return None
    return amount


def _unknown_hard_preferences(items, options, conditions):
    """이미 장르 필터/명시 제외로 표현한 hard 선호만 허용하고 나머지 의미 hard는 보류한다."""
    unknown = []
    categories = options.get("categories", [conditions.get("category")])
    for item in items:
        if not isinstance(item, dict) or item.get("strength") != "hard":
            continue
        value = item.get("value")
        if item.get("dimension") == "genre" and isinstance(value, str):
            if item.get("polarity") == "avoid" and value in options.get("exclude_terms", []):
                continue
            if item.get("polarity") != "avoid" and value in categories:
                continue
        unknown.append(item)
    return unknown


def _rank(candidates, semantic_preferences, options, ranker, venue_only):
    """실제 원문 인용이 유효한 점수만 사용한다. 선택 정렬 실패는 코드 정렬로 복구한다."""
    ranking = dict(status="not_requested", matched_ids=[])
    scores = {}
    soft = [item for item in semantic_preferences if isinstance(item, dict) and item.get("strength") != "hard"]
    # 모델 입력을 제한하는 호출자도 출발지와 무관한 공급자 첫 행만 보지 않도록 기본순서를 먼저 계산한다.
    for item in candidates:
        source_text = " ".join(str(item.get(field) or "") for field in sorted(RANK_FIELDS)).casefold()
        item["matched_keywords"] = [word for word in options.get("keywords", []) if word.casefold() in source_text]
    def baseline(item):
        """모델 호출 전 관심어·실제 직선거리를 이용해 후보 입력 순서를 정한다."""
        interest = -len(item["matched_keywords"])
        distance = (item["distance_km"] is None, item["distance_km"] or 0)
        return (*distance, interest, item["id"]) if options.get("walking_preference") == "short" else (interest, *distance, item["id"])
    candidates.sort(key=baseline)
    if soft and venue_only:
        ranking["status"] = "unsupported_source"
    elif soft and ranker:
        try:
            proposed = ranker(deepcopy(candidates), deepcopy(soft))
            if not isinstance(proposed, dict):
                raise ValueError("invalid ranking envelope")
            for candidate in candidates:
                proposed_item = proposed.get(candidate["id"])
                if not isinstance(proposed_item, dict):
                    continue
                score, evidence = proposed_item.get("score"), proposed_item.get("evidence")
                if (isinstance(score, bool) or not isinstance(score, (int, float)) or not math.isfinite(score)
                        or not -1 <= score <= 1 or not isinstance(evidence, list) or not evidence):
                    continue
                valid = all(isinstance(proof, dict) and proof.get("field") in RANK_FIELDS
                            and isinstance(proof.get("quote"), str) and proof["quote"].strip()
                            and proof["quote"] in (candidate.get(proof["field"]) or "") for proof in evidence)
                if valid:
                    scores[candidate["id"]] = score
                    candidate["semantic_evidence"] = deepcopy(evidence)
            ranking.update(status="applied" if scores else "unknown", matched_ids=list(scores))
        except Exception:
            ranking["status"] = "source_error"
    elif soft:
        ranking["status"] = "unavailable"
    for item in candidates:
        hits = item["matched_keywords"]
        item["preference_reasons"] = (["공개 자료에 관심어 포함: " + ", ".join(hits)] if hits else [])
        for proof in item.get("semantic_evidence", []):
            item["preference_reasons"].append("공개 자료의 관련 표현: " + proof["quote"])
        item["semantic_score"] = scores.get(item["id"])
    def order(item):
        """관련성/관심어와 실제 직선거리를 정렬한다. 보행 시간을 추정하지 않는다."""
        relevance = (-scores.get(item["id"], 0), -len(item["matched_keywords"]))
        distance = (item["distance_km"] is None, item["distance_km"] or 0)
        return (*distance, *relevance, item["id"]) if options.get("walking_preference") == "short" else (*relevance, *distance, item["id"])
    candidates.sort(key=order)
    return ranking


def explore(state, mode="live", ranker=None):
    """실제 탐색 결과와 적용/미적용 근거를 반환한다. InputError 외 조회장애는 source_error다.

    ranker(candidates, preferences)는 {candidate_id:{score:-1..1,evidence:[{field,quote}]}}
    형식의 선택 동기 콜백이다. 좌표/가격/시간 등 사실을 변경할 수 없다. 이 함수는 상태를
    수정하거나 방문일/60분 시간창을 생성하지 않는다. 새 네트워크는 기존 source 함수만 사용한다.
    """
    understanding, conditions, service, origin, options = _inputs(state)
    window = _window(conditions)
    semantic_preferences = understanding.get("preferences", [])
    if not isinstance(semantic_preferences, list):
        semantic_preferences = []
    semantic_preferences = [item for item in semantic_preferences if isinstance(item, dict)
                            and item.get("scope", "conversation") in {"conversation", service}]
    venue_only = service in VENUE_QUERIES
    kind = "venue_exploration" if venue_only else "content_exploration"
    first, last, start, end = window
    context = dict(service=service, conditions=deepcopy(conditions), revision=state.get("revision", 0),
                   preference_fingerprint=_digest(semantic_preferences), result_kind=kind)
    context["execution_key"] = _digest(context)
    result = dict(status="ok", result_kind=kind, candidates=[], applied=[], not_applied=[], unknown=[],
                  excluded_counts={}, source=None, source_checked_at=None, result_context=context,
                  range=dict(date_from=first.isoformat() if first else None, date_to=last.isoformat() if last else None,
                             date_filter_explicit=bool(first or last), excludes_ended_before=datetime.now(outing.KST).date().isoformat(),
                             visit_window_created=False))
    unresolved = [item for item in state.get("hypotheses", []) if isinstance(item, dict)
                  and item.get("strength") == "hard" and item.get("status") in {"unresolved", "ambiguous", "invalid"}
                  and (not item.get("blocking_scope") or "explore" in item["blocking_scope"]
                       or (venue_only and "search_places" in item["blocking_scope"]))]
    hard_preferences = _unknown_hard_preferences(semantic_preferences, options, conditions)
    if options.get("unsupported_requirements") or unresolved or hard_preferences:
        result.update(blocked=True, unknown=["hard_requirement"], excluded_counts={"unverified_hard_requirement": 1},
                      not_applied=[dict(field="hard_requirement", reason="현재 공급자 근거로 필수 조건 충족을 확인하지 못해 탐색을 보류했습니다.")])
        return result
    try:
        candidates, source, invalid = _source(service, conditions, options, origin, mode, first)
    except (OSError, RuntimeError, ValueError, TypeError, KeyError, AttributeError):
        result.update(status="source_error", source="kakao_local" if venue_only else "seoul_culture",
                      code="exploration_source_error", message="콘텐츠 제공기관의 응답을 확인하지 못했습니다. 기존 조건과 결과는 유지해 주세요.")
        return result
    result.update(source)
    eligibility = None
    if service == "walk":
        candidates, eligibility = _walk_eligibility(candidates)
        result["eligibility"] = eligibility
    candidates, counts, unknown = _hard_filter(candidates, conditions, options, window, venue_only)
    if eligibility:
        counts.update(eligibility["excluded_counts"])
        if counts["walk_unverified"]:
            unknown.append("walk_destination")
    counts["invalid_source_item"] = invalid
    for candidate in candidates:
        candidate["source_fields"] = {field: candidate.get(field) for field in sorted(RANK_FIELDS)}
        candidate["source_field_hash"] = _digest(candidate["source_fields"])
    context["source_version"] = source["source_checked_at"]
    context["execution_key"] = _digest({key: value for key, value in context.items() if key != "execution_key"})
    ranking = _rank(candidates, semantic_preferences, options, ranker, venue_only)
    result.update(excluded_counts=counts, unknown=unknown, ranking=ranking)
    basis = ("공급자 상세분류로 주 산책 목적지 적합성을 확인한 후보만 통과" if service == "walk"
             else "공급자 keyword 조회 · 활동 목적 적합성 추가 검증 없음" if venue_only
             else "공급자 행사 분류")
    result["applied"] = [dict(field="service", value=service, basis=basis)]
    for field in ("date", "date_from", "date_to", "start_at", "end_at", "free_only", "budget_krw", "exclude_terms", "max_distance_km"):
        value = conditions.get(field)
        if (field in conditions and value is not None and value != [] and value != "any"
                and not (field == "free_only" and value is False)):
            result["applied"].append(dict(field=field, value=deepcopy(conditions[field]), basis="공개 자료에서 확인되는 후보만 통과"))
    for field in unknown:
        reason = ("산책 목적지인지 공급자 상세분류로 확인하지 못한 후보는 제외했습니다."
                  if field == "walk_destination" else "필수 사실 미확인 후보는 충족으로 간주하지 않고 제외했습니다.")
        result["not_applied"].append(dict(field=field, reason=reason))
    if options.get("indoor_outdoor", "any") != "any":
        result["not_applied"].append(dict(field="indoor_outdoor", reason="공개 자료로 실내·실외 여부를 확인하지 못했습니다."))
    if any(item.get("strength") != "hard" for item in semantic_preferences) and ranking["status"] != "applied":
        result["not_applied"].append(dict(field="semantic_preferences", reason=ranking["status"]))
    elif ranking["status"] == "applied":
        result["applied"].append(dict(field="semantic_preferences", basis="실제 원문 인용을 검증한 관련성 정렬"))
    for candidate in candidates:
        candidate["result_kind"] = kind
        candidate["result_context"] = deepcopy(context)
    result["candidates"] = candidates
    result["coverage_note"] = source["scope"] + (" · 영화 작품/상영표/예매 정보 미연동" if service == "movie" else "")
    if eligibility:
        excluded = eligibility["excluded_counts"]
        result["coverage_note"] += (f" · 조회한 {eligibility['checked_count']}건 중 주 산책 목적지 분류 확인 "
                                    f"{eligibility['eligible_count']}건 · 부대시설/다른 용도 "
                                    f"{excluded['walk_amenity'] + excluded['walk_incompatible']}건, "
                                    f"분류 미확인 {excluded['walk_unverified']}건 제외 · 추가 페이지 미조회")
    return result
