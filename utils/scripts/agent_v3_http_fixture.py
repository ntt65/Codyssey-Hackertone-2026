"""v3 실제 Preview HTTP/store/정책/탐색에 고정 모델·공급자 원본만 연결하는 A층 fixture.

실제 환경 파일/외부 API는 사용하지 않는다. check_agent_v3.cjs가 임시 서버를 시작하고
종료한다. 테스트용 관측 endpoint는 고정 대화의 모델 입력만 메모리에서 제공한다.
"""
from contextlib import ExitStack
from datetime import datetime, timedelta
import io
import json
import os
from pathlib import Path
import sys
import threading
import time
from http.server import ThreadingHTTPServer
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))
from preview import Preview
from outing import KST

CONTEXTS = []
COUNTS = {"meaning": 0, "ranking": 0, "culture": 0, "map": 0}


def model_reply(request, timeout):
    """실제 provider JSON 요청에서 고정 의미/정렬 응답만 생성한다. 정책 결과는 만들지 않는다."""
    sent = json.loads(request.data)
    context = json.loads(sent["messages"][-1]["content"])
    if "candidates" in context:
        COUNTS["ranking"] += 1
        target = "신나는" if any(p.get("value") == "lively" for p in context["preferences"]) else "잔잔한"
        parsed = {}
        for candidate in context["candidates"]:
            description = candidate.get("description") or ""
            if "잔잔한" in description or "신나는" in description:
                parsed[candidate["id"]] = dict(score=1 if target in description else -1,
                                                evidence=[dict(field="description", quote=description)])
    else:
        COUNTS["meaning"] += 1
        CONTEXTS.append(context)
        message, turn = context["message"], context["turn_id"]
        evidence = dict(turn_id=turn, quote=message)
        question = context.get("active_question") or {}
        acts = [dict(type="answer" if question else "inform", evidence=evidence)]
        updates = []

        def update(domain, field, value, **extra):
            """현재 턴의 실제 인용을 갖는 모델 후보를 추가한다."""
            item = dict(id=turn + ":" + str(len(updates)), domain=domain, field=field,
                        op="add", value=value, strength="soft", evidence=evidence)
            item.update(extra)
            updates.append(item)

        if message in {"공연을 보고 싶어", "무료만 가능한 공연", "전시 보고 싶어", "늦은 공연", "영화 보고 싶어", "카페 가고 싶어", "산책하고 싶어"}:
            if message == "늦은 공연":
                time.sleep(0.8)
            service = "movie" if "영화" in message else "cafe" if "카페" in message else "walk" if "산책" in message else "exhibition" if "전시" in message else "performance"
            update("service", "service", service)
            update("goal", "text", message)
            if message == "무료만 가능한 공연":
                update("condition", "free_only", True, strength="hard")
        elif message == "잔잔한 음악":
            update("preference", "atmosphere", "calm", polarity="prefer")
            # 실제 회귀: 잘못된 분류와 모르는 key가 유효한 취향/목적을 버리지 못해야 한다.
            update("condition", "category", "음악")
            update("condition", "mood", "calm")
        elif message == "신나는 공연":
            previous = next((p for p in context["understanding"]["preferences"] if p["dimension"] == "atmosphere"), None)
            update("preference", "atmosphere", "lively", polarity="prefer")
            if previous:
                updates[-1].update(op="replace", target_id=previous["id"])
        elif message in {"서울시청", "시청 서울시청", "수원시청", "시청"}:
            update("condition", "start_query", message)
        elif message == "무슨 조건?":
            acts = [dict(type="explain_question", question_id=question.get("id"), evidence=evidence)]
        elif message == "내일":
            update("condition", "date", (datetime.now(KST).date() + timedelta(days=1)).isoformat())
        elif message == "다른 곳도 보여줘":
            acts = [dict(type="request_alternatives", evidence=evidence)]
        elif message in {"ㅎㅎ", "고마워"}:
            acts = [dict(type="chitchat", evidence=evidence)]
        elif message == "음...":
            acts = [dict(type="inform", evidence=evidence)]
        elif message == "말씀하신 주":
            acts = []  # 정상 provider JSON이지만 유효 의미가 없는 실제 실패 분기.
        elif message in {"더 가까운 곳으로 알려줘", "테스트 중복"}:
            acts = [dict(type="proceed", evidence=evidence)]
        else:
            raise AssertionError("fixture에 정의하지 않은 테스트 발화")
        parsed = dict(schema_version=1, acts=acts, updates=updates)
    body = dict(content=[dict(type="text", text=json.dumps(parsed, ensure_ascii=False))], stop_reason="end_turn",
                model="fixed-v3-provider", usage=dict(input_tokens=50, output_tokens=25))
    return io.BytesIO(json.dumps(body, ensure_ascii=False).encode())


def map_reply(request, timeout):
    """카카오 원본 문서 형태를 반환해 실제 장소 정규화/거리 계산을 거치게 한다."""
    COUNTS["map"] += 1
    params = parse_qs(urlsplit(request.full_url).query)
    query = params["query"][0]
    if query in {"서울시청", "시청 서울시청"}:
        rows = [dict(id="100", place_name="서울특별시청", address_name="서울 중구 세종대로 110", x="126.9779", y="37.5663")]
    elif query == "수원시청":
        rows = [dict(id="200", place_name="수원시청", address_name="경기 수원시 효원로 241", x="127.0286", y="37.2635")]
    elif query == "시청":
        rows = [dict(id="100", place_name="서울특별시청", address_name="서울 중구 세종대로 110", x="126.9779", y="37.5663"),
                dict(id="200", place_name="수원시청", address_name="경기 수원시 효원로 241", x="127.0286", y="37.2635")]
    elif query in {"영화관", "카페", "공원"}:
        if params.get("sort") != ["distance"] or not params.get("x") or not params.get("y"):
            raise AssertionError("장소 탐색에 실제 origin과 거리순 누락")
        if query == "공원":
            rows = [dict(id=identity, place_name=name, category_name=category, category_group_code=group,
                         address_name="서울 중구 시험로 " + identity, x=str(lng), y="37.5663",
                         place_url="https://place.map.kakao.com/" + identity)
                    for identity, name, category, group, lng in (
                        ("501", "테스트공원 화장실", "가정,생활 > 화장실", "", 126.9780),
                        ("502", "화장실 앞 쉼터공원", "여행 > 공원", "AT4", 126.9790),
                        ("503", "테스트공원 주차장", "여행 > 공원 > 주차장", "PK6", 126.9795),
                        ("504", "넓은 공원", "", "AT4", 126.9800),
                        ("505", "테스트생태공원", "여행 > 공원 > 생태공원", "AT4", 126.9810),
                    )]
        else:
            rows = [dict(id="300", place_name="고정 테스트 " + query, address_name="서울 중구 테스트로 1",
                         category_name=query, x="126.98", y="37.56", place_url="https://place.map.kakao.com/300")]
    else:
        rows = []
    return io.BytesIO(json.dumps(dict(meta=dict(total_count=len(rows)), documents=rows), ensure_ascii=False).encode())


def culture_page(day, category, mode):
    """공식 행사 필드의 공연6건/전시4건으로 표시3건과 전체pool 순서를 분리한다."""
    COUNTS["culture"] += 1
    today = datetime.now(KST).date()
    rows = []
    for identity, title, description, genre in (
        ("101", "피아노 음악회", "잔잔한 선율의 피아노 연주", "콘서트"),
        ("102", "리듬 음악회", "신나는 리듬과 활기찬 합주", "콘서트"),
        ("103", "주말 연극", "도시 생활을 그린 연극", "연극"),
        ("104", "미술 전시", "회화 작품 전시", "전시"),
        ("105", "주말 연주", "실내악을 들려주는 연주회", "콘서트"),
        ("106", "전통 무대", "전통 음악을 들려주는 무대", "국악"),
        ("107", "합창 음악회", "여러 목소리가 함께하는 합창", "콘서트"),
        ("201", "빛 사진전", "빛을 주제로 한 사진 전시", "전시"),
        ("202", "역사 전시", "도시의 역사를 보여주는 전시", "전시"),
        ("203", "조각 전시", "조각 작품을 보여주는 전시", "전시"),
    ):
        rows.append(dict(TITLE=title, PROGRAM=description, PLACE="테스트 문화회관", CODENAME=genre,
                         HMPG_ADDR="https://culture.seoul.go.kr/event?cultcode=" + identity,
                         STRTDATE=today.isoformat(), END_DATE=(today + timedelta(days=30)).isoformat(),
                         PRO_TIME="14:00", IS_FREE="무료", USE_FEE="0원", LAT="37.567", LOT="126.98"))
    return rows, today.isoformat() + "T10:00:00+09:00", len(rows)


class FixturePreview(Preview):
    """제품 handler를 사용하고 테스트 관측 정보만 별도 GET으로 노출한다."""

    def log_message(self, format, *args):
        """테스트 원문/접근 로그를 저장하지 않는다."""

    def do_GET(self):
        """관측 이외 GET은 실제 Preview로 전달한다."""
        if self.path == "/__fixture":
            self.reply(200, dict(counts=COUNTS, contexts=CONTEXTS))
            return
        super().do_GET()


def main():
    """격리 loopback fixture를 시작하고 부모 stdin이 닫히면 모든 테스트 자원을 정리한다."""
    with ExitStack() as stack:
        stack.enter_context(patch.dict(os.environ, {"LAB678_ALLOWED_ORIGINS": sys.argv[1], "LAB678_NAITO_PROVIDER": "codyssey"}))
        stack.enter_context(patch("naito_chat.settings", return_value=("fixture-key", "fixture-model")))
        stack.enter_context(patch("naito_chat.urlopen", side_effect=model_reply))
        stack.enter_context(patch("agent_v3.urlopen", side_effect=model_reply))
        stack.enter_context(patch("places.api_key", return_value="fixture-key"))
        stack.enter_context(patch("places.urlopen", side_effect=map_reply))
        stack.enter_context(patch("outing.seoul_page", side_effect=culture_page))
        stack.enter_context(patch("exploration.culture_key", return_value="fixture-key"))
        stack.enter_context(patch("socket.socket.connect", side_effect=AssertionError("외부 연결 금지")))
        server = ThreadingHTTPServer(("127.0.0.1", 0), FixturePreview)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        try:
            print(json.dumps(dict(base=f"http://127.0.0.1:{server.server_port}")), flush=True)
            sys.stdin.readline()
        finally:
            server.shutdown()
            server.server_close()
            worker.join(timeout=5)


if __name__ == "__main__":
    main()
