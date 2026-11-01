"""실제 로컬 HTTP 처리기와 모의 공급자로 대화 계약 및 CORS를 검증한다."""

import io
import json
import os
import threading
import unittest
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from unittest.mock import patch

from preview import Preview


class AgentHttpIntegrationTests(unittest.TestCase):
    """외부 네트워크 없이 Preview의 실제 HTTP 경계와 대화 처리를 통과한다."""

    @classmethod
    def setUpClass(cls):
        """임시 loopback 서버와 공급자·설정 대체를 시작한다."""
        cls.origin = "http://localhost:5173"
        cls.env_patch = patch.dict(os.environ, {"LAB678_ALLOWED_ORIGINS": cls.origin,
                                                "LAB678_NAITO_PROVIDER": "codyssey"})
        cls.settings_patch = patch("naito_chat.settings", return_value=("local-test-key", "local-test-model"))
        cls.provider_patch = patch("naito_chat.urlopen", side_effect=cls.mock_provider)
        cls.env_patch.start()
        cls.settings_patch.start()
        cls.provider_patch.start()
        try:
            cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Preview)
        except BaseException:
            cls.provider_patch.stop()
            cls.settings_patch.stop()
            cls.env_patch.stop()
            raise
        cls.worker = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.worker.start()

    @classmethod
    def tearDownClass(cls):
        """서버, 스레드, 프로세스 환경과 모의 공급자를 복원한다."""
        cls.server.shutdown()
        cls.server.server_close()
        cls.worker.join(timeout=5)
        cls.provider_patch.stop()
        cls.settings_patch.stop()
        cls.env_patch.stop()

    @staticmethod
    def mock_provider(request, timeout):
        """서버가 보낸 메시지에 맞춘 Anthropic 형식의 고정 JSON을 반환한다."""
        sent = json.loads(request.data)
        context = json.loads(sent["messages"][0]["content"])
        if context["message"] == "유료도 괜찮고 3시에 출발":
            content = {"changes": {"free_only": False, "start_at": "2026-11-02T15:00:00+09:00"},
                       "evidence": {"free_only": "유료도 괜찮고", "start_at": "3시"}}
        elif context["message"] == "오후 두 시에 출발":
            content = {"changes": {"start_at": "2026-11-02T14:00:00+09:00"},
                       "evidence": {"start_at": "오후 두 시"}}
        else:
            raise AssertionError("예상하지 못한 외부 공급자 요청")
        body = {"content": [{"type": "text", "text": json.dumps(content, ensure_ascii=False)}],
                "stop_reason": "end_turn"}
        return io.BytesIO(json.dumps(body, ensure_ascii=False).encode("utf-8"))

    def request(self, method, path, payload=None, headers=None):
        """새 HTTP 연결로 실제 상태·헤더·JSON 본문을 읽는다."""
        connection = HTTPConnection("127.0.0.1", self.server.server_port, timeout=5)
        try:
            raw = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
            connection.request(method, path, body=raw, headers=headers or {})
            response = connection.getresponse()
            body = response.read()
            return response.status, dict(response.getheaders()), json.loads(body) if body else None
        finally:
            connection.close()

    def test_partial_clarification_and_same_value_confirmation(self):
        """부분 보류·기존 초안 보존과 같은 값 재확인을 실제 POST에서 검사한다."""
        draft = {"date": "2026-11-02", "start_at": "2026-11-02T14:00:00+09:00", "free_only": True}
        headers = {"Content-Type": "application/json", "Origin": self.origin}
        status, response_headers, body = self.request("POST", "/preview/chat", {
            "message": "유료도 괜찮고 3시에 출발", "condition_draft": draft,
            "confirmed_fields": [], "revision": 0}, headers)
        self.assertEqual(status, 200)
        self.assertEqual(response_headers.get("Access-Control-Allow-Origin"), self.origin)
        self.assertEqual(body["interpretation_status"], "needs_clarification")
        self.assertEqual(body["clarification_fields"], ["start_at"])
        self.assertEqual(body["interpreted_fields"], ["free_only"])
        self.assertFalse(body["updated_condition_draft"]["free_only"])
        self.assertEqual(body["updated_condition_draft"]["start_at"], draft["start_at"])
        self.assertFalse(body["ready_to_search"])
        self.assertEqual(draft["free_only"], True)

        status, _, followup = self.request("POST", "/preview/chat", {
            "message": "오후 두 시에 출발", "condition_draft": body["updated_condition_draft"],
            "confirmed_fields": [], "revision": 1}, headers)
        self.assertEqual(status, 200)
        self.assertEqual(followup["updated_condition_draft"]["start_at"], draft["start_at"])
        self.assertEqual(followup["interpreted_fields"], ["start_at"])
        self.assertNotIn("clarification_fields", followup)
        self.assertNotIn("local-test-key", json.dumps(body, ensure_ascii=False))
        self.assertNotIn("local-test-key", json.dumps(followup, ensure_ascii=False))

    def test_cors_preflight_and_disallowed_origin(self):
        """허용된 사전 요청과 거부된 origin의 실제 HTTP 응답을 확인한다."""
        preflight = {"Origin": self.origin, "Access-Control-Request-Method": "POST",
                     "Access-Control-Request-Headers": "content-type"}
        status, headers, _ = self.request("OPTIONS", "/preview/chat", headers=preflight)
        self.assertEqual(status, 204)
        self.assertEqual(headers.get("Access-Control-Allow-Origin"), self.origin)
        self.assertIn("POST", headers.get("Access-Control-Allow-Methods", ""))
        preflight["Origin"] = "http://untrusted.example"
        status, headers, _ = self.request("OPTIONS", "/preview/chat", headers=preflight)
        self.assertEqual(status, 403)
        self.assertNotIn("Access-Control-Allow-Origin", headers)
        status, headers, body = self.request("POST", "/preview/chat", {"message": "x", "revision": 0},
                                             {"Content-Type": "application/json", "Origin": "http://untrusted.example"})
        self.assertEqual((status, body["status"]), (403, "forbidden"))
        self.assertNotIn("Access-Control-Allow-Origin", headers)


if __name__ == "__main__":
    unittest.main()
