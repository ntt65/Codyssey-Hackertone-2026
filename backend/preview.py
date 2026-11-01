"""동조 개인용 로컬 추천 점검 화면. python backend/preview.py로 시작한다."""
import argparse
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import URLError
from urllib.parse import urlsplit

from outing import EXAMPLES, InputError, recommend
from local_voice import file_voice_available, render_wave
from course import build_course
from walking import walk_between
from transit import transit_between
from map_config import map_config
from places import search_places
from naito_chat import chat
from tour_places import culture_places
from contact import event_contact
from team_app import app_directory, app_asset

POST_PATHS = {"/preview/recommend", "/preview/voice", "/preview/walk", "/preview/transit", "/preview/places", "/preview/chat", "/preview/culture-places", "/preview/contact"}


def allowed_origins():
    """환경변수의 명시적 HTTP(S) origin만 허용한다. 와일드카드·경로·자격정보는 제외한다."""
    origins = set()
    configured = os.environ.get("LAB678_ALLOWED_ORIGINS", "").split(",")
    configured.append(os.environ.get("RENDER_EXTERNAL_URL", ""))
    for value in configured:
        value = value.strip().rstrip("/")
        try:
            parsed = urlsplit(value)
            if (parsed.scheme in {"http", "https"} and parsed.hostname and parsed.port != 0
                    and parsed.username is None and parsed.password is None and not parsed.path
                    and not parsed.query and not parsed.fragment and not any(c.isspace() for c in value)
                    and "*" not in value):
                origins.add(value)
        except ValueError:
            continue
    return origins


class Preview(BaseHTTPRequestHandler):
    """허용된 화면과 개인 검증용 JSON 요청만 제공한다."""

    def end_headers(self):
        """정상/오류 응답 모두 허용 origin에만 CORS 헤더를 적용하며 쿠키 인증은 허용하지 않는다."""
        origin = self.headers.get("Origin")
        self.send_header("Vary", "Origin")
        if origin in allowed_origins():
            self.send_header("Access-Control-Allow-Origin", origin)
        super().end_headers()

    def do_OPTIONS(self):
        """설정된 프론트의 JSON POST 사전 요청만 허용하고 그 외 origin/메서드/헤더는 거절한다."""
        if self.path not in POST_PATHS:
            self.reply(404, dict(status="error", message="지원하지 않는 경로입니다."))
            return
        requested_headers = {h.strip().lower() for h in self.headers.get("Access-Control-Request-Headers", "").split(",") if h.strip()}
        if (self.headers.get("Origin") not in allowed_origins()
                or self.headers.get("Access-Control-Request-Method") != "POST"
                or not requested_headers <= {"content-type"}):
            self.reply(403, dict(status="forbidden", message="허용된 프론트 주소와 JSON POST 요청을 확인해 주세요."))
            return
        self.send_response(204)
        self.send_header("Access-Control-Allow-Methods", "POST")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", "0")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()

    def reply(self, status, body, content_type="application/json"):
        """UTF-8 본문을 길이와 함께 응답한다."""
        if content_type == "application/json":
            body = json.dumps(body, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", content_type + "; charset=utf-8" if content_type.startswith("text/") or content_type == "application/json" else content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        """점검 폼과 저장소의 대표 요청만 제공한다."""
        path = urlsplit(self.path).path
        if path == "/" and app_directory() is not None:
            self.send_response(302)
            self.send_header("Location", "/app/?#/home")
            self.send_header("Content-Length", "0")
            self.end_headers()
        elif path == "/app-config":
            self.reply(200, dict(available=app_directory() is not None))
        elif path == "/app":
            self.send_response(302)
            self.send_header("Location", "/app/")
            self.send_header("Content-Length", "0")
            self.end_headers()
        elif path.startswith("/app/"):
            asset = app_asset(self.path)
            if asset:
                self.reply(200, asset[0], asset[1])
            elif app_directory() is None:
                self.reply(503, dict(status="unconfigured", message="자동 대화 화면 실행 파일을 준비해야 해요."))
            else:
                self.send_error(404)
        elif self.path == "/" or path == "/checks":
            page = Path(__file__).with_name("preview.html").read_text(encoding="utf-8")
            if file_voice_available():
                page = page.replace("data-file-voice hidden", "data-file-voice")
            self.reply(200, page.encode("utf-8"), "text/html")
        elif self.path == "/healthz":
            self.reply(200, dict(status="ok"))
        elif self.path == "/map-config":
            self.reply(200, map_config())
        elif self.path == "/map-view.js":
            self.reply(200, Path(__file__).with_name("map_view.js").read_bytes(), "text/javascript")
        elif self.path == "/location-view.js":
            self.reply(200, Path(__file__).with_name("location_view.js").read_bytes(), "text/javascript")
        elif self.path in {"/microphone-meter.js", "/preview-meter.js"}:
            filename = "microphone_meter.js" if self.path == "/microphone-meter.js" else "preview_meter.js"
            self.reply(200, Path(__file__).with_name(filename).read_bytes(), "text/javascript")
        elif self.path == "/example":
            self.reply(200, json.loads((EXAMPLES / "outing-request.json").read_bytes()))
        else:
            self.send_error(404)

    def do_POST(self):
        """장소 요청을 처리하고 입력·외부 공급자 오류를 다른 상태로 전달한다."""
        if self.path not in POST_PATHS:
            self.send_error(404)
            return
        origin = self.headers.get("Origin")
        same_origin = "http://" + self.headers.get("Host", "")
        if origin and origin != same_origin and origin not in allowed_origins():
            self.reply(403, dict(status="forbidden", message="허용된 프론트 주소를 확인해 주세요."))
            return
        if self.headers.get_content_type() != "application/json":
            self.send_error(415)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 8192:
                raise ValueError("요청 크기를 확인해 주세요.")
            data = json.loads(self.rfile.read(length))
            if not isinstance(data, dict):
                raise ValueError("요청 형식을 확인해 주세요.")
            if self.path == "/preview/culture-places":
                status, body = culture_places(data)
                self.reply(status, body)
                return
            if self.path == "/preview/contact":
                status, body = event_contact(data)
                self.reply(status, body)
                return
            if self.path == "/preview/chat":
                status, body = chat(data)
                self.reply(status, body)
                return
            if self.path == "/preview/places":
                status, body = search_places(data)
                self.reply(status, body)
                return
            if self.path == "/preview/transit":
                try:
                    status, body = transit_between(data.get("points"))
                except (ValueError, TypeError, KeyError):
                    status, body = 400, dict(status="need_input", message="출발지와 목적지 좌표를 확인해 주세요.")
                self.reply(status, body)
                return
            if self.path == "/preview/walk":
                try:
                    if "details" in data and type(data["details"]) is not bool:
                        raise ValueError("경로 안내 요청 형식을 확인해 주세요.")
                    status, body = walk_between(data.get("points"), data.get("details", False))
                except ValueError as exc:
                    status, body = 400, dict(message=str(exc))
                self.reply(status, body)
                return
            if self.path == "/preview/voice":
                try:
                    audio = render_wave(data.get("text"))
                except ValueError as exc:
                    self.reply(400, dict(message=str(exc)))
                except RuntimeError:
                    self.reply(503, dict(message="이 PC에서 한국어 음성 파일을 만들지 못했습니다."))
                else:
                    self.reply(200, audio, "audio/wav")
                return
            source = data.get("culture_source", "seoul")
            if source not in ("seoul", "tour"):
                raise InputError("invalid_culture_source", "culture_source", "전시·공연 또는 문화시설을 선택해 주세요.")
            if source == "tour":
                status, body = culture_places(data)
                self.reply(status, body)
                return
            result = recommend(data, data.get("mode", "live"))
            if data.get("request_kind") in ("course", "route"):
                result["course"] = build_course(data, result["candidates"])
        except InputError as exc:
            self.reply(400, dict(status="need_input", message=str(exc), code=exc.code, field=exc.field))
        except (ValueError, TypeError, KeyError):
            self.reply(400, dict(status="need_input", message="출발 좌표·분류·당일 시간 범위 또는 재생 가능한 기록을 확인해 주세요."))
        except (URLError, OSError, RuntimeError, AttributeError):
            self.reply(502, dict(status="error", message="문화정보 조회에 실패했습니다. 같은 조건으로 다시 시도해 주세요."))
        else:
            self.reply(200, result)


def server_options(argv=None):
    """로컬 기본값을 유지하고 명시한 접속 주소·배포 환경의 PORT 범위를 검증한다."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default=os.environ.get("LAB678_HOST", "127.0.0.1"), help="배포 시 0.0.0.0을 명시")
    parser.add_argument("--port", type=int, default=os.environ.get("PORT", "8765"), help="실행 포트, 0은 빈 포트 자동 선택")
    args = parser.parse_args(argv)
    if not 0 <= args.port <= 65535:
        parser.error("포트는 0~65535 범위여야 합니다.")
    return args


if __name__ == "__main__":
    args = server_options()
    server = ThreadingHTTPServer((args.host, args.port), Preview)
    print(f"http://{args.host}:{server.server_port}", flush=True)
    server.serve_forever()
