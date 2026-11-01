"""브라우저 회귀 검사에 실제 Preview HTTP와 고정 외부 공급자 데이터를 제공한다.

check_agent_http.cjs가 시작·종료한다. 환경 파일은 읽지 않으며 외부 소켓 연결은 차단한다.
대화 grounding/병합, 장소 정규화, 추천 필터, CORS는 실제 앱 코드를 사용한다.
"""

from contextlib import ExitStack
import io
import json
import os
from pathlib import Path
import sys
import threading
from http.server import ThreadingHTTPServer
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))
from preview import Preview


def provider_reply(request, timeout):
    """실제 공급자 요청 형식을 읽고 테스트 발화에만 고정 모델 후보를 돌려준다."""
    sent = json.loads(request.data)
    context = json.loads(sent["messages"][0]["content"])
    message = context["message"]
    if message == "무료만 가능한 가까운 곳":
        changes, evidence = {"free_only": True}, {"free_only": message}
    elif message == "무료만 아닌 유료도 괜찮아요":
        # 의미가 반대인 모델 오답이 실제 HTTP 응답에서 보류되는지 검사한다.
        changes, evidence = {"free_only": True}, {"free_only": message}
    elif message == "유료도 괜찮아요":
        changes, evidence = {"free_only": False}, {"free_only": message}
    elif message == "출발지는 시청으로 바꿔줘":
        changes, evidence = {"start_query": "시청"}, {"start_query": message}
    else:
        raise AssertionError("지원하지 않는 테스트 발화")
    payload = {"content": [{"type": "text", "text": json.dumps(
        {"changes": changes, "evidence": evidence}, ensure_ascii=False)}], "stop_reason": "end_turn"}
    return io.BytesIO(json.dumps(payload, ensure_ascii=False).encode("utf-8"))


def places_reply(request, timeout):
    """동명 서울/수원 시청을 카카오 원본 형식의 모의 응답으로 제공한다."""
    rows = [
        {"id": "1", "place_name": "시청", "address_name": "서울 중구 세종대로",
         "x": "126.98", "y": "37.56"},
        {"id": "2", "place_name": "시청", "address_name": "경기 수원시 효원로",
         "x": "127.03", "y": "37.26"},
    ]
    return io.BytesIO(json.dumps({"meta": {"total_count": 2}, "documents": rows},
                                ensure_ascii=False).encode("utf-8"))


def culture_page(day, category, mode):
    """고정 행사 두 개를 제공하고 실제 추천 코드가 가격·분류·거리를 계산하게 한다."""
    rows = []
    for identity, fee in (("101", "무료"), ("102", "유료")):
        rows.append({"TITLE": fee + " 테스트 전시", "PLACE": "테스트 전시장", "CODENAME": "전시",
                     "HMPG_ADDR": "https://culture.seoul.go.kr/culture/culture/cultureEvent/view.do?cultcode=" + identity,
                     "STRTDATE": day, "END_DATE": day, "PRO_TIME": "09:00~18:00",
                     "IS_FREE": fee, "USE_FEE": "무료" if fee == "무료" else "10000원",
                     "LAT": "37.57", "LOT": "126.98"})
    return rows, day + "T10:00:00+09:00", len(rows)


class QuietPreview(Preview):
    """실제 처리기는 유지하고 테스트 프로세스의 HTTP 로그만 생략한다."""

    def log_message(self, format, *args):
        """고정 테스트 요청의 접근 로그를 저장하지 않는다."""


def main():
    """허용 origin의 loopback 서버를 시작하고 부모의 stdin 종료 요청 후 정리한다."""
    with ExitStack() as stack:
        stack.enter_context(patch.dict(os.environ, {"LAB678_ALLOWED_ORIGINS": sys.argv[1],
                                                    "LAB678_NAITO_PROVIDER": "codyssey"}))
        stack.enter_context(patch("naito_chat.settings", return_value=("fixture-key", "fixture-model")))
        stack.enter_context(patch("naito_chat.urlopen", side_effect=provider_reply))
        stack.enter_context(patch("places.api_key", return_value="fixture-key"))
        stack.enter_context(patch("places.urlopen", side_effect=places_reply))
        stack.enter_context(patch("outing.seoul_page", side_effect=culture_page))
        stack.enter_context(patch("outing.culture_key", return_value=""))
        stack.enter_context(patch("socket.socket.connect", side_effect=AssertionError("외부 연결 금지")))
        server = ThreadingHTTPServer(("127.0.0.1", 0), QuietPreview)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        try:
            print(json.dumps({"base": f"http://127.0.0.1:{server.server_port}"}), flush=True)
            sys.stdin.readline()
        finally:
            server.shutdown()
            server.server_close()
            worker.join(timeout=5)


if __name__ == "__main__":
    main()
