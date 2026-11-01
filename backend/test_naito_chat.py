"""Naito 모의 응답/장애와 HTTP 연결 경계를 검사한다. 실제 서비스 성공을 뜻하지 않는다."""
import io
import json
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError

from naito_chat import chat, extract_conditions
from outing import InputError


class NaitoChatTests(unittest.TestCase):
    """서비스 키 없이 실행되는 공급자 어댑터 회귀다."""

    def setUp(self):
        """최소 정상 대화 입력을 준비한다."""
        self.data = dict(message="국악을 듣고 싶어", revision=0, condition_draft={})

    def test_missing_key(self):
        """미설정은 503이며 외부 호출을 하지 않는다."""
        with patch("naito_chat.settings", return_value=("", "claude-sonnet-4")), patch("naito_chat.extract_conditions") as call:
            self.assertEqual(chat(self.data)[0], 503)
            call.assert_not_called()

    def test_validate_before_provider(self):
        """잘못된 요청은 공급자/키 조회 전에 거절한다."""
        for change in [dict(message=""), dict(revision=True), dict(conversation_context=[{"role": "system", "content": "x"}])]:
            with self.subTest(change=change), patch("naito_chat.settings") as config, self.assertRaises(InputError):
                chat(dict(self.data, **change))
            config.assert_not_called()

    def test_provider_request_excludes_coordinates(self):
        """키는 헤더에만, 좌표는 제외하며 공식 고정 주소로 한 번 요청한다."""
        body = {"content": [{"type": "text", "text": json.dumps({"changes": {"category": "국악"}, "evidence": {"category": "국악"}}, ensure_ascii=False)}], "stop_reason": "end_turn"}
        draft = dict(date="2026-10-31", start_location=dict(label="청량리역", lat=37.5805961, lng=127.0482573))
        with patch("naito_chat.urlopen", return_value=io.BytesIO(json.dumps(body).encode())) as call:
            self.assertEqual(extract_conditions("국악", draft, [], "secret-test", "claude-sonnet-4"), {"category": "국악"})
        request = call.call_args.args[0]
        self.assertEqual(request.full_url, "https://copa.codyssey.kr/v1/messages")
        self.assertEqual(request.get_header("X-api-key"), "secret-test")
        self.assertEqual(request.get_header("Anthropic-version"), "2023-06-01")
        self.assertEqual(json.loads(request.data)["max_tokens"], 1024)
        context = json.loads(json.loads(request.data)["messages"][0]["content"])
        self.assertEqual(context["condition_draft"]["date"], "2026-10-31")
        self.assertNotIn(b"secret-test", request.data)
        self.assertNotIn(b"37.5805961", request.data)
        self.assertEqual(call.call_count, 1)

    def test_success_and_no_recommendation(self):
        """모의 국악 해석 뒤 출발지 질문으로 이어지며 추천은 실행하지 않는다."""
        with patch("naito_chat.settings", return_value=("secret", "claude-sonnet-4")), \
                patch("naito_chat.extract_conditions", return_value={"category": "국악"}):
            status, result = chat(self.data)
        self.assertEqual(status, 200)
        self.assertEqual(result["source"], "naito")
        self.assertEqual(result["updated_condition_draft"]["category"], "국악")
        self.assertFalse(result["ready_to_search"])
        self.assertNotIn("clarification_fields", result)
        self.assertEqual(result["interpreted_fields"], ["category"])

    def test_errors_do_not_disclose_or_replace(self):
        """공급자 오류/비JSON/사실 생성은 오류로 남기고 키·원문·가짜 초안을 노출하지 않는다."""
        cases = [(TimeoutError("secret-test"), 504), (URLError("secret-test"), 502),
                 (HTTPError("https://example.test", 429, "secret-test", {}, None), 429),
                 (ValueError("secret-test"), 502)]
        with patch("naito_chat.settings", return_value=("secret-test", "claude-sonnet-4")):
            for error, expected in cases:
                with self.subTest(expected=expected), patch("naito_chat.extract_conditions", side_effect=error):
                    status, result = chat(self.data)
                self.assertEqual(status, expected)
                self.assertNotIn("secret-test", json.dumps(result))
                self.assertNotIn("updated_condition_draft", result)
            with patch("naito_chat.extract_conditions", return_value={"lat": 37.5}):
                self.assertEqual(chat(self.data)[1]["code"], "ai_invalid_response")

    def test_response_size_and_json_boundary(self):
        """과대 응답/일반 텍스트/잘못된 응답 구조를 파싱 성공으로 취급하지 않는다."""
        for raw in [b"x" * 65537, b"not-json", b"{}", b'{"content":[],"stop_reason":"max_tokens"}']:
            with patch("naito_chat.urlopen", return_value=io.BytesIO(raw)), self.assertRaises((ValueError, KeyError)):
                extract_conditions("국악", {}, [], "secret", "test")

    def test_empty_interpretation_not_reported_as_applied(self):
        """지원하지 않는 발화를 반영 완료로 안내하지 않는다."""
        with patch("naito_chat.settings", return_value=("secret", "claude-sonnet-4")), \
                patch("naito_chat.extract_conditions", return_value={}):
            status, result = chat(self.data)
        self.assertEqual(status, 200)
        self.assertEqual(result["interpretation_status"], "no_supported_change")
        self.assertFalse(result["ready_to_search"])
        self.assertNotIn("clarification_fields", result)
        self.assertNotIn("interpreted_fields", result)

    def test_provider_reply_cannot_clear_required_condition(self):
        """모의 공급자의 필수 조건 무단 삭제는 보류하고 기존 초안을 보존한다."""
        payload = {"changes": {"unsupported_requirements": []}, "evidence": {"unsupported_requirements": "실내만"}}
        body = {"content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False)}], "stop_reason": "end_turn"}
        data = dict(message="실내만 꼭 원해요", condition_draft={"unsupported_requirements": ["계단 없음"]}, revision=1)
        with patch("naito_chat.settings", return_value=("secret-test", "mock-model")), \
                patch.dict("os.environ", {"LAB678_NAITO_PROVIDER": "codyssey"}), \
                patch("naito_chat.urlopen", return_value=io.BytesIO(json.dumps(body).encode())):
            status, result = chat(data)
        self.assertEqual(status, 200)
        self.assertEqual(result["updated_condition_draft"]["unsupported_requirements"], ["계단 없음"])
        self.assertEqual(result["interpretation_status"], "needs_clarification")
        self.assertFalse(result["ready_to_search"])
        self.assertEqual(result["clarification_fields"], ["unsupported_requirements"])
        self.assertNotIn("interpreted_fields", result)

    def test_interpreted_fields_preserve_reconfirmation_and_omit_blocked(self):
        """기존 값 재확인과 명시 해제는 필드명으로만 내보내고 보류와 null은 제외한다."""
        from chat_grounding import GroundedProposal
        draft = {"free_only": False, "category": "전시"}
        proposal = GroundedProposal({"free_only": False, "category": "전시", "start_at": None}, ("start_query",))
        with patch("naito_chat.settings", return_value=("secret-test", "mock-model")), \
                patch("naito_chat.extract_conditions", return_value=proposal):
            status, result = chat(dict(self.data, message="비공개 발화", condition_draft=draft))
        self.assertEqual(status, 200)
        self.assertEqual(result["interpreted_fields"], ["free_only", "category"])
        self.assertEqual(result["clarification_fields"], ["start_query"])
        self.assertNotIn("비공개 발화", json.dumps(result, ensure_ascii=False))
        with patch("naito_chat.settings", return_value=("secret-test", "mock-model")), \
                patch("naito_chat.extract_conditions", return_value=GroundedProposal({"free_only": False}, ("free_only",))):
            status, result = chat(dict(self.data, condition_draft=draft))
        self.assertEqual(status, 200)
        self.assertNotIn("interpreted_fields", result)

    def test_clarification_fields_validate_and_do_not_leak(self):
        """보류 필드에는 허용 이름만 한 번 노출하고 원문은 포함하지 않는다."""
        from chat_grounding import GroundedProposal
        with patch("naito_chat.settings", return_value=("secret-test", "mock-model")):
            proposal = GroundedProposal({}, ("start_query", "start_query", "free_only"))
            with patch("naito_chat.extract_conditions", return_value=proposal):
                status, result = chat(dict(self.data, message="비공개 발화"))
            self.assertEqual(status, 200)
            self.assertEqual(result["clarification_fields"], ["start_query", "free_only"])
            self.assertNotIn("비공개 발화", json.dumps(result, ensure_ascii=False))
            proposal = GroundedProposal({}, ("비공개 발화",))
            with patch("naito_chat.extract_conditions", return_value=proposal):
                status, result = chat(dict(self.data, message="비공개 발화"))
            self.assertEqual(status, 502)
            self.assertNotIn("clarification_fields", result)
            self.assertNotIn("비공개 발화", json.dumps(result, ensure_ascii=False))


class EndpointTest(unittest.TestCase):
    """공급자별 요청 형식과 모의 응답의 공통 검증 경계를 확인한다."""
    def test_provider_switch(self):
        """설정한 제공자 주소로만 호출하고, 모르는 값이면 해커톤 주소. 키 모양으로 추측하지 않는다."""
        import naito_chat
        with patch.dict("os.environ", {"LAB678_NAITO_PROVIDER": ""}):
            self.assertEqual(naito_chat.endpoint("sk-ant-abc"), naito_chat.ENDPOINT)
        with patch.dict("os.environ", {"LAB678_NAITO_PROVIDER": "openai"}):
            self.assertEqual(naito_chat.endpoint(), naito_chat.OPENAI_ENDPOINT)
        with patch.dict("os.environ", {"LAB678_NAITO_PROVIDER": "anthropic"}):
            self.assertEqual(naito_chat.endpoint(), naito_chat.ANTHROPIC_ENDPOINT)
        with patch.dict("os.environ", {"LAB678_NAITO_PROVIDER": "https://evil.example.com"}):
            self.assertEqual(naito_chat.endpoint(), naito_chat.ENDPOINT)

    def test_openai_request_and_response(self):
        """OpenAI 형식: Bearer 키, system+user 메시지, JSON 응답을 꺼내요."""
        import io, json as _json, naito_chat
        content = _json.dumps({"changes": {"category": "전시"}, "evidence": {"category": "전시"}}, ensure_ascii=False)
        body = {"choices": [{"finish_reason": "stop", "message": {"content": content}}]}
        with patch.dict("os.environ", {"LAB678_NAITO_PROVIDER": "openai"}), \
             patch("naito_chat.urlopen", return_value=io.BytesIO(_json.dumps(body).encode())) as net:
            out = naito_chat.extract_conditions("전시 보고 싶어요", {}, [], "sk-test", "gpt-test")
        req = net.call_args.args[0]
        self.assertEqual(out, {"category": "전시"})
        self.assertEqual(req.full_url, naito_chat.OPENAI_ENDPOINT)
        self.assertEqual(req.get_header("Authorization"), "Bearer sk-test")
        sent = _json.loads(req.data)
        self.assertEqual([m["role"] for m in sent["messages"]], ["system", "user"])

    def test_providers_reject_unspoken_place_and_preserve_valid_category(self):
        """세 공급자에서 발화에 없는 출발지 후보만 보류하고 명확한 분류는 유지한다."""
        import naito_chat
        model_payload = {"changes": {"category": "전시", "start_query": "강남역"},
                         "evidence": {"category": "전시", "start_query": "전시"}}
        model_content = json.dumps(model_payload, ensure_ascii=False)
        for selected in ("codyssey", "anthropic", "openai"):
            if selected == "openai":
                response = {"choices": [{"finish_reason": "stop", "message": {"content": model_content}}]}
            else:
                response = {"content": [{"type": "text", "text": model_content}], "stop_reason": "end_turn"}
            with self.subTest(provider=selected), \
                    patch.dict("os.environ", {"LAB678_NAITO_PROVIDER": selected}), \
                    patch("naito_chat.settings", return_value=("secret", "mock-model")), \
                    patch("naito_chat.urlopen", return_value=io.BytesIO(json.dumps(response).encode())) as network:
                status, result = naito_chat.chat(dict(message="전시 보고 싶어요", condition_draft={}, revision=0))
            self.assertEqual(status, 200)
            self.assertEqual(result["updated_condition_draft"]["category"], "전시")
            self.assertNotIn("start_query", result["updated_condition_draft"])
            self.assertFalse(result["ready_to_search"])
            self.assertEqual(result["interpretation_status"], "needs_clarification")
            self.assertEqual(network.call_count, 1)

    def test_invalid_envelope_and_truncated_replies_do_not_apply(self):
        """공급자의 손상·절단 응답은 보류 성공으로 가장하지 않고 오류를 반환한다."""
        import naito_chat
        responses = [
            {"content": [{"type": "text", "text": '{"category":"국악"}'}], "stop_reason": "end_turn"},
            {"content": [{"type": "text", "text": '{"changes":{},"evidence":{}}'}], "stop_reason": "max_tokens"},
            {"choices": [{"finish_reason": "length", "message": {"content": '{"changes":{},"evidence":{}}'}}]},
            {"choices": [{"finish_reason": "content_filter", "message": {"content": '{"changes":{},"evidence":{}}'}}]},
            {"choices": [{"finish_reason": "stop", "message": {"content": '{"changes":{},"evidence":{}}', "refusal": "refused"}}]},
        ]
        for selected, response in zip(("codyssey", "anthropic", "openai", "openai", "openai"), responses):
            with self.subTest(provider=selected), \
                    patch.dict("os.environ", {"LAB678_NAITO_PROVIDER": selected}), \
                    patch("naito_chat.settings", return_value=("secret", "mock-model")), \
                    patch("naito_chat.urlopen", return_value=io.BytesIO(json.dumps(response).encode())):
                status, result = naito_chat.chat(dict(message="국악", condition_draft={}, revision=0))
            self.assertEqual(status, 502)
            self.assertEqual(result["code"], "ai_invalid_response")
            self.assertNotIn("updated_condition_draft", result)
