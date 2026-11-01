"""출발지 선택용 카카오 장소명/주소 검색. 사용자 검색어·키·원문 응답은 저장하지 않는다."""
import hashlib
import json
from datetime import datetime
from threading import BoundedSemaphore
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen

from outing import InputError, KST, coordinate, distance_km
from transit import api_key

_SLOTS = BoundedSemaphore(2)


def search_input(data):
    """검색어 1~80자와 keyword/address를 검증한다. 요청값을 오류에 되돌려 쓰지 않는다."""
    query = data.get("query")
    kind = data.get("type", "keyword")
    if not isinstance(query, str) or not 1 <= len(query.strip()) <= 80 or any(ord(c) < 32 for c in query):
        raise InputError("invalid_query", "query", "장소명이나 주소를 1~80자로 입력해 주세요.")
    if kind not in ("keyword", "address"):
        raise InputError("invalid_search_type", "type", "장소명 또는 주소 검색을 선택해 주세요.")
    return query.strip(), kind


def search_origin(data):
    """선택한 출발 좌표만 검색 중심으로 사용한다. 누락 시 전국 정확도순 동작을 유지한다."""
    origin = data.get("origin")
    if origin is None:
        return None
    if not isinstance(origin, dict) or set(origin) != {"lat", "lng"}:
        raise InputError("invalid_origin", "origin", "검색할 출발 위치를 다시 선택해 주세요.")
    try:
        return coordinate(origin["lat"], 90), coordinate(origin["lng"], 180)
    except ValueError:
        raise InputError("invalid_origin", "origin", "검색할 출발 위치를 다시 선택해 주세요.") from None


def text_or_none(value):
    """공급자 텍스트를 제한된 길이로 읽고 공백·누락은 null로 유지한다."""
    return value.strip() if isinstance(value, str) and 0 < len(value.strip()) <= 500 else None


def normalize_places(body, kind, origin=None):
    """공급자 x/y를 숫자 lng/lat로 바꾸고 선택 가능한 최대5건만 반환한다. 손상과0건을 구분한다."""
    documents = body.get("documents")
    total = body.get("meta", {}).get("total_count")
    if not isinstance(documents, list) or type(total) is not int or total < len(documents) or total < 0:
        raise ValueError("검색 응답 형식 오류")
    if not documents and total:
        raise ValueError("검색 목록 누락")
    places, skipped = [], 0
    for item in documents[:5]:
        try:
            lat, lng = coordinate(item.get("y"), 90), coordinate(item.get("x"), 180)
            address = text_or_none(item.get("address_name"))
            if kind == "keyword":
                label = text_or_none(item.get("place_name"))
                identity = text_or_none(item.get("id"))
                road = text_or_none(item.get("road_address_name"))
                url = text_or_none(item.get("place_url"))
                parsed = urlsplit(url or "")
                if not (parsed.scheme in {"http", "https"} and parsed.hostname == "place.map.kakao.com"
                        and parsed.username is None and parsed.password is None):
                    url = None
            else:
                label = address
                road_data = item.get("road_address")
                road = text_or_none(road_data.get("address_name")) if isinstance(road_data, dict) else None
                identity = hashlib.sha256(f"{address}|{lat}|{lng}".encode()).hexdigest()[:20]
                url = None
            if not label or not identity:
                raise ValueError("선택 장소 식별 정보 누락")
            place = dict(id=f"kakao:{kind}:{identity}", label=label, lat=lat, lng=lng,
                         address=address, road_address=road, official_url=url, type=kind)
            if origin is not None:
                place["distance_km"] = distance_km(origin[0], origin[1], lat, lng)
            if kind == "keyword":
                place["category_name"] = text_or_none(item.get("category_name"))
                place["category_group_code"] = text_or_none(item.get("category_group_code"))
                place["category_group_name"] = text_or_none(item.get("category_group_name"))
            places.append(place)
        except (ValueError, TypeError, AttributeError):
            skipped += 1
    if documents and not places:
        raise ValueError("선택할 수 있는 검색 좌표 없음")
    return dict(status="ready" if places else "no_results", places=places, source="kakao_local",
                source_total=total, skipped_count=skipped, source_checked_at=datetime.now(KST).isoformat(timespec="seconds"),
                message="출발지를 선택해 주세요." if places else "검색 결과가 없어요. 다른 장소명이나 주소를 입력해 주세요.")


def search_places(data):
    """카카오에 검색어를 보내 후보를 반환한다. HTTP 상태·권한/쿼터/시간초과를 구분하고 비밀값은 숨긴다."""
    query, kind = search_input(data)
    origin = search_origin(data)
    try:
        key = api_key()
    except (OSError, ValueError):
        key = ""
    if not key:
        return 503, dict(status="unconfigured", code="search_unconfigured", message="장소 검색 연결 설정을 확인해야 해요.")
    if not _SLOTS.acquire(blocking=False):
        return 429, dict(status="limited", code="search_busy", message="검색 중이에요. 잠시 후 다시 시도해 주세요.")
    try:
        parameters = dict(query=query, size=5, page=1)
        if origin is not None and kind == "keyword":
            parameters.update(x=origin[1], y=origin[0], sort="distance")
        url = f"https://dapi.kakao.com/v2/local/search/{kind}.json?" + urlencode(parameters)
        request = Request(url, headers={"Authorization":"KakaoAK " + key, "Accept":"application/json"})
        with urlopen(request, timeout=6) as response:
            raw = response.read(500001)
        if len(raw) > 500000:
            raise ValueError("검색 응답 크기 오류")
        result = normalize_places(json.loads(raw), kind, origin)
        result["origin_applied"] = origin is not None and kind == "keyword"
        return 200, result
    except HTTPError as exc:
        code = exc.code
        exc.close()
        if code in (401, 403):
            return 503, dict(status="unavailable", code="search_permission", message="장소 검색 API 권한을 확인해야 해요.")
        if code == 429:
            return 429, dict(status="limited", code="search_quota", message="검색 한도에 도달했어요. 잠시 후 다시 시도해 주세요.")
    except TimeoutError:
        return 504, dict(status="timeout", code="search_timeout", message="검색이 지연됐어요. 다시 시도해 주세요.")
    except URLError as exc:
        if isinstance(exc.reason, TimeoutError):
            return 504, dict(status="timeout", code="search_timeout", message="검색이 지연됐어요. 다시 시도해 주세요.")
    except (OSError, ValueError, TypeError, AttributeError):
        pass
    finally:
        _SLOTS.release()
    return 502, dict(status="unavailable", code="search_failed", message="장소를 검색하지 못했어요. 다시 시도해 주세요.")
