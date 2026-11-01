"""실제 모델/실 API 품질과 구분한 v3 orchestration 경계 회귀.

모델 출력은 의미 계약 fixture이며 실모델 성공으로 집계하지 않는다. 실제 순수 의미
정책·ConversationStore·지도 채택·exploration 필터는 실행하고 외부 I/O만 고정한다.
"""
from copy import deepcopy
import io
import json
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

import naito_chat
import agent_v3
from conversation_store import ConversationStore
from dialogue_memory import new_state, apply_event
from exploration import explore as real_explore
from outing import EXAMPLES

REAL_MODEL_JSON = agent_v3.model_json


ORIGIN = {"id": "kakao:cityhall", "label": "서울특별시청", "address": "서울 중구 세종대로 110",
          "lat": 37.5663, "lng": 126.9779}


class Clock:
    """네트워크 대기 없이 lease 인계 시점만 독립 제어한다."""

    def __init__(self):
        """시작 시각을 고정한다."""
        self.value = 1000.0

    def __call__(self):
        """저장소가 사용하는 단조 시각을 반환한다."""
        return self.value


class NaitoV3Tests(unittest.TestCase):
    """메시지→실제 정책→도구→원자 commit과 오류 분류를 독립 검증한다."""

    def setUp(self):
        """개별 저장소와 안전한 외부 경계를 설치하며 실제 환경 키를 읽지 않는다."""
        self.clock = Clock()
        self.store = ConversationStore(clock=self.clock)
        self.state = new_state()
        self.document = "document-test"
        opened = self.store.open(self.document, initial_state=self.state)
        self.meta = opened["conversation"]
        self.model = self.start(patch("agent_v3.model_json", side_effect=self.model_reply))
        self.start(patch("naito_chat.settings", return_value=("synthetic-key", "synthetic-model")))
        self.start(patch("agent_v3._V3_STORE", self.store))
        self.start(patch.dict(agent_v3._V3_RANK_CACHE, {}, clear=True))
        self.explore = self.start(patch("exploration.explore", side_effect=self.exploration_reply))
        self.maps = self.start(patch("places.search_places", return_value=(200, {"status": "ready", "places": [ORIGIN]})))

    def start(self, patcher):
        """시험이 실패해도 monkeypatch를 복구한다."""
        value = patcher.start()
        self.addCleanup(patcher.stop)
        return value

    def payload(self, message, turn_id, updates=(), act="inform", question_id=None):
        """원문 근거를 가진 의미 후보만 반환하고 기대 정책/행동은 주입하지 않는다."""
        return {"schema_version": 1, "acts": [{"type": act, "question_id": question_id,
                "evidence": {"turn_id": turn_id, "quote": message}}],
                "updates": [{"id": f"{turn_id}:{index}", "domain": domain, "field": field,
                             "value": value, "op": "add", "strength": "soft", "target_id": None,
                             "evidence": {"turn_id": turn_id, "quote": message}}
                            for index, (domain, field, value) in enumerate(updates)]}

    def model_reply(self, system, context, **limits):
        """고정 의미 fixture와 고정 원문에 대한 모의 관련성 판정을 구분한다."""
        if "candidates" in context:
            desired = context["preferences"][0]["value"]
            target = "잔잔한" if desired == "calm" else "신나는"
            value = {candidate["id"]: {"score": 1 if target in candidate["description"] else -1,
                      "evidence": [{"field": "description", "quote": candidate["description"]}]}
                     for candidate in context["candidates"]}
            return value, {"model": "synthetic-model", "usage": {"input_tokens": 1}}
        message, turn = context["message"], context["turn_id"]
        updates = []
        act = "inform"
        if "공연" in message:
            updates = [("goal", "text", "공연 관람"), ("service", "activity", "performance")]
        if "잔잔한" in message:
            updates.append(("preference", "atmosphere", "calm"))
        if "서울시청" in message:
            updates.append(("condition", "start_query", "서울시청"))
        if "무슨 조건" in message:
            act = "explain_question"
        if message == "찾아줘":
            act = "proceed"
        question = (context.get("active_question") or {}).get("id")
        return self.payload(message, turn, updates, act, question), {"model": "synthetic-model", "usage": {}}

    def exploration_reply(self, state, mode, ranker):
        """호출된 실제 상태를 검사할 수 있는 경계 결과만 반환한다."""
        return {"status": "ok", "result_kind": "content_exploration", "source": "synthetic-source",
                "candidates": [{"id": "seoul:101", "title": "고정 공연", "genre": "콘서트"}],
                "result_context": {"execution_key": "fixture-key", "service": state["understanding"]["service"]},
                "not_applied": [], "coverage_note": "모의 공급자 경계"}

    def request(self, event, **changes):
        """마지막 canonical 메타데이터의 다음 턴을 구성한다."""
        result = {"agent_version": 3, "conversation_id": self.meta["conversation_id"], "epoch": self.meta["epoch"],
                  "document_id": self.document, "turn_seq": self.meta["next_turn_seq"],
                  "turn_id": f"turn-{self.meta['next_turn_seq']}", "expected_revision": self.meta["revision"], "event": event}
        result.update(changes)
        return result

    def call(self, event, **changes):
        """실제 chat 분기와 저장소 commit을 통과한 응답 메타데이터를 이어간다."""
        request = self.request(event, **changes)
        status, response = naito_chat.chat(request)
        if response.get("conversation"):
            self.meta = response["conversation"]
        return status, response

    def message(self, text):
        """STT 최종 텍스트와 같은 message 이벤트를 실행한다."""
        return self.call({"type": "message", "text": text})

    def locate(self, service="performance"):
        """검증 위치를 가진 새 서버 상태로 시작하고 클라이언트 초안 주입을 하지 않는다."""
        state = new_state()
        state["understanding"].update(goal="공연 관람", service=service)
        state = apply_event(state, {"type": "select_origin", "place": ORIGIN})
        opened = self.store.open(self.document, initial_state=state, mode="fork")
        self.meta = opened["conversation"]
        return state

    def fixed_rows(self):
        """실제 공급자 필드형식에 독립 평가용 두 소개와 고정 ID를 넣는다."""
        base = json.loads((EXAMPLES / "seoul-events.capture.json").read_bytes())["captures"][0]["rows"][0]
        base.update(STRTDATE="2026-11-01", END_DATE="2099-12-31", LAT="37.566", LOT="126.978",
                    CODENAME="콘서트", PRO_TIME="14:00", IS_FREE="무료", USE_FEE="0원")
        calm = dict(base, TITLE="피아노 음악회", PROGRAM="잔잔한 선율의 피아노 연주", HMPG_ADDR="https://culture.seoul.go.kr/event?cultcode=101")
        lively = dict(base, TITLE="리듬 음악회", PROGRAM="신나는 리듬과 활기찬 합주", HMPG_ADDR="https://culture.seoul.go.kr/event?cultcode=102")
        return calm, lively

    def visit_state(self, end_at):
        """방문 단계의 검증 입력·기존 공연 취향을 서버 초기 상태로 준비한다."""
        state = new_state()
        state["understanding"].update(goal="공연 관람", service="performance", preferences=[{
            "id": "calm-pref", "dimension": "atmosphere", "value": "calm", "polarity": "prefer",
            "strength": "soft", "scope": "performance", "source": "user_explicit"}])
        state = apply_event(state, {"type": "select_origin", "place": ORIGIN})
        state["request_mode"] = "visit"
        state["conditions"].update(request_kind="place", start_at="2099-11-01T14:00:00+09:00",
                                   end_at=end_at, free_only=True)
        self.meta = self.store.open(self.document, initial_state=state, mode="fork")["conversation"]
        return state

    def test_open_heartbeat_release_make_no_model_or_source_calls(self):
        """저장 연결·heartbeat·해제가 대화 추론이나 외부 조회를 실행하지 않는다."""
        status, opened = self.call({"type": "open"})
        self.assertEqual(status, 200)
        status, beat = self.call({"type": "heartbeat"})
        self.assertEqual(status, 200)
        self.assertEqual(beat["conversation"]["revision"], opened["conversation"]["revision"])
        self.assertEqual(self.call({"type": "release"})[0], 200)
        self.model.assert_not_called()
        self.explore.assert_not_called()

    def test_reported_performance_explanation_mood_and_exact_map_pipeline(self):
        """공연→설명요청→잔잔함→서울시청이 실제 정책과 지도 채택 뒤 공연 조회로 연결된다."""
        status, first = self.message("공연 보고 싶어")
        self.assertEqual(status, 200)
        self.assertEqual(first["state"]["active_question"]["target"], "start_location")
        status, explanation = self.message("뭘 알려 줘 무슨 조건")
        self.assertEqual(status, 200)
        self.assertIn("지역을 여쭤본", explanation["assistant_text"])
        status, mood = self.message("잔잔한 음악")
        self.assertEqual(status, 200)
        self.assertEqual(mood["state"]["understanding"]["preferences"][0]["value"], "calm")
        self.assertNotIn("category", mood["state"]["conditions"])
        status, result = self.message("시청 서울시청")
        self.assertEqual(status, 200)
        self.assertEqual(result["state"]["conditions"]["start_location"]["lat"], ORIGIN["lat"])
        self.assertEqual(result["tool_result"]["result_kind"], "content_exploration")
        self.assertEqual(self.maps.call_args.args[0]["query"], "서울시청")
        queried = self.explore.call_args.args[0]
        self.assertEqual(queried["understanding"]["service"], "performance")
        self.assertEqual(queried["understanding"]["preferences"][0]["value"], "calm")
        self.assertNotIn("end_at", queried["conditions"])

    def test_partial_invalid_category_keeps_good_mood_and_explores(self):
        """정상 취향+잘못된 음악category 하나가 전체502나 필수조건 루프를 만들지 않는다."""
        self.locate()

        def mixed(system, context, **limits):
            """정상 의미와 고의 손상한 메뉴 후보를 같은 모델 응답에 넣는다."""
            return self.payload(context["message"], context["turn_id"],
                                [("preference", "atmosphere", "calm"), ("condition", "category", "음악")]), {}

        self.model.side_effect = mixed
        status, response = self.message("잔잔한 음악")
        self.assertEqual(status, 200)
        self.assertEqual(response["state"]["diagnostics"]["turn_status"], "partial")
        self.assertNotIn("category", response["state"]["conditions"])
        self.assertEqual(response["state"]["understanding"]["preferences"][0]["value"], "calm")
        self.assertEqual(self.explore.call_count, 1)

    def test_duplicate_and_stale_requests_never_reexecute_model(self):
        """성공 응답 손실의 재전달·과거revision은 모델 호출 횟수를 늘리지 않는다."""
        request = self.request({"type": "message", "text": "공연 보고 싶어"})
        status, first = naito_chat.chat(request)
        self.assertEqual(status, 200)
        replay_status, replay = naito_chat.chat(request)
        self.assertEqual(replay_status, 200)
        self.assertTrue(replay["replayed"])
        self.assertEqual(self.model.call_count, 1)
        self.meta = first["conversation"]
        stale = self.request({"type": "message", "text": "잔잔한 음악"}, expected_revision=0)
        self.assertEqual(naito_chat.chat(stale)[0], 409)
        self.assertEqual(self.model.call_count, 1)

    def test_source_error_keeps_meaning_and_retry_calls_only_failed_tool(self):
        """도구0건과 장애를 구분하고 재시도에서 잔잔함 의미를 다시 적용하지 않는다."""
        self.locate()
        self.explore.side_effect = [{"status": "source_error", "code": "exploration_source_error", "candidates": []},
                                    self.exploration_reply(new_state(), "live", None)]
        status, failed = self.message("잔잔한 음악")
        self.assertEqual(status, 200)
        self.assertEqual(failed["tool_result"]["status"], "source_error")
        self.assertIn("조회 연결", failed["assistant_text"])
        self.assertEqual(failed["state"]["understanding"]["preferences"][0]["value"], "calm")
        action = failed["state"]["last_tool_action"]["id"]
        status, retried = self.call({"type": "retry_tool", "action_id": action})
        self.assertEqual(status, 200)
        self.assertEqual(self.model.call_count, 1)
        self.assertEqual(retried["state"]["understanding"], failed["state"]["understanding"])
        self.assertEqual(self.explore.call_count, 2)

    def test_map_source_error_remains_typed_and_retries_without_reinterpretation(self):
        """지도503은 실제0건과 구분하며 같은 지명 도구 재시도에 모델을 다시 쓰지 않는다."""
        self.message("공연 보고 싶어")
        self.maps.return_value = (503, {"status": "error", "code": "map_unconfigured", "places": []})
        status, failed = self.message("서울시청")
        self.assertEqual(status, 200)
        lookup = failed["next_action"]["origin_lookup"]
        self.assertEqual(lookup["status"], "source_error")
        self.assertEqual(lookup["http_status"], 503)
        self.assertEqual(lookup["code"], "map_unconfigured")
        self.assertNotIn("start_location", failed["state"]["conditions"])
        action = failed["state"]["last_tool_action"]
        self.assertEqual(action["kind"], "resolve_origin")
        self.assertTrue(action["failed"])
        self.maps.return_value = (200, {"status": "ready", "places": [ORIGIN]})
        status, retried = self.call({"type": "retry_tool", "action_id": action["id"]})
        self.assertEqual(status, 200)
        self.assertEqual(retried["state"]["conditions"]["start_location"]["lat"], ORIGIN["lat"])
        self.assertEqual(retried["state"]["understanding"]["service"], "performance")
        self.assertEqual(self.model.call_count, 2)
        self.assertEqual(self.maps.call_count, 2)

    def test_map_no_results_is_distinct_from_source_failure(self):
        """정상 지도0건은 연결장애라고 표시하거나 임의 좌표를 채택하지 않는다."""
        self.message("공연 보고 싶어")
        self.maps.return_value = (200, {"status": "no_results", "places": []})
        status, response = self.message("서울시청")
        self.assertEqual(status, 200)
        self.assertEqual(response["next_action"]["origin_lookup"]["status"], "no_results")
        self.assertEqual(response["next_action"]["origin_lookup"]["http_status"], 200)
        self.assertNotIn("start_location", response["state"]["conditions"])
        self.assertFalse(response["state"].get("last_tool_action", {}).get("failed", False))
        self.explore.assert_not_called()

    def test_tool_timeout_preserves_meaning_and_has_retry_action(self):
        """조회 timeout은 의미502로 숨기지 않고 보존된 의미에서 도구만 재시도할 수 있다."""
        self.locate()
        with patch("agent_v3._v3_tool", side_effect=TimeoutError):
            status, failed = self.message("잔잔한 음악")
        self.assertEqual(status, 504)
        self.assertEqual(failed["diagnostics"]["stage"], "tool")
        self.assertEqual(failed["state"]["understanding"]["preferences"][0]["value"], "calm")
        action = failed["state"]["last_tool_action"]["id"]
        self.assertTrue(failed["state"]["last_tool_action"]["failed"])
        self.assertEqual(self.call({"type": "retry_tool", "action_id": action})[0], 200)
        self.assertEqual(self.model.call_count, 1)

    def test_model_timeout_is_meaning_failure_and_next_turn_recovers(self):
        """모델 timeout의 단계·마지막 상태를 보존하고 다음 명시 발화가 정상 처리된다."""
        self.model.side_effect = TimeoutError
        status, failed = self.message("공연 보고 싶어")
        self.assertEqual(status, 504)
        self.assertEqual(failed["diagnostics"]["stage"], "meaning")
        self.assertEqual(failed["diagnostics"]["model_calls"], 1)
        self.assertEqual(failed["state"]["understanding"]["service"], "any")
        self.model.side_effect = self.model_reply
        self.assertEqual(self.message("공연 보고 싶어")[0], 200)

    def test_cached_failure_preserves_http_status_without_model_retry(self):
        """동일 오류 응답의 재전달이502를200으로 바꾸거나 모델을 다시 부르지 않는다."""
        self.model.side_effect = ValueError("synthetic invalid envelope")
        request = self.request({"type": "message", "text": "공연 보고 싶어"})
        first_status, first = naito_chat.chat(request)
        replay_status, replay = naito_chat.chat(request)
        self.assertEqual(first_status, 502)
        self.assertEqual(replay_status, first_status)
        self.assertEqual(replay["code"], first["code"])
        self.assertEqual(self.model.call_count, 1)

    def test_provider_error_keeps_safe_code_and_status(self):
        """제공자429는 구조502로 바꾸지 않고 안전한 원인·단계를 남긴다."""
        self.model.side_effect = HTTPError("https://provider.invalid", 429, "synthetic", {}, None)
        status, response = self.message("공연 보고 싶어")
        self.assertEqual(status, 429)
        self.assertEqual(response["code"], "ai_rate_limit")
        self.assertEqual(response["diagnostics"]["stage"], "meaning")
        self.assertNotIn("provider.invalid", json.dumps(response, ensure_ascii=False))

    def test_unconfigured_provider_returns_503_without_unhandled_exception(self):
        """설정이 없다는 원인을 숨기거나 서버 예외로 넘기지 않는다."""
        with patch("agent_v3.model_json", wraps=REAL_MODEL_JSON), \
                patch("naito_chat.settings", return_value=("", "synthetic-model")), \
                patch("agent_v3.urlopen") as provider:
            status, response = self.message("공연 보고 싶어")
        provider.assert_not_called()
        self.assertEqual(status, 503)
        self.assertEqual(response["code"], "ai_not_configured")

    def test_actual_provider_json_decode_failure_is_not_disguised_as_policy_bug(self):
        """실제 provider decoder를 거친 손상 JSON이 의미 단계 오류로 기록된다."""
        with patch("agent_v3.model_json", wraps=REAL_MODEL_JSON), \
                patch("naito_chat.provider", return_value="codyssey"), \
                patch("agent_v3.urlopen", return_value=io.BytesIO(b"not-json")):
            status, failed = self.message("공연 보고 싶어")
        self.assertEqual(status, 502)
        self.assertEqual(failed["diagnostics"]["stage"], "meaning")
        self.assertEqual(failed["diagnostics"]["failure_type"], "JSONDecodeError")
        self.assertEqual(failed["state"]["understanding"]["service"], "any")

    def test_true_hard_requirement_blocks_even_after_proceed_event(self):
        """실제 명시 필수 제약을 새 취향이나 진행 버튼으로 조용히 우회하지 않는다."""
        self.locate()
        status, requirement = self.message("계단 없는 공연")
        self.assertEqual(status, 200)
        self.assertEqual(requirement["state"]["active_question"]["target"], "requirement")
        self.assertTrue(any(item["strength"] == "hard" for item in requirement["state"]["hypotheses"]))
        self.assertEqual(self.call({"type": "proceed"})[0], 200)
        self.explore.assert_not_called()

    def test_zero_candidates_is_distinct_from_source_failure(self):
        """조회 성공0건은 source_error 재시도 대상으로 바꾸거나 후보를 만들지 않는다."""
        self.locate()
        self.explore.side_effect = lambda *args: {"status": "ok", "candidates": [], "coverage_note": "고정된 조회범위"}
        status, response = self.message("찾아줘")
        self.assertEqual(status, 200)
        self.assertEqual(response["tool_result"]["status"], "ok")
        self.assertEqual(response["tool_result"]["candidates"], [])
        self.assertIn("조건에 맞는 새 콘텐츠", response["assistant_text"])
        self.assertFalse(response["state"]["last_tool_action"]["failed"])

    def test_invalid_envelope_is_502_while_policy_bug_is_500(self):
        """사용자에게 같은 일반오류로 보여도 내부 모델형식/정책버그 원인을 구분한다."""
        self.model.return_value = ({"schema_version": 1, "acts": [], "updates": []}, {})
        self.model.side_effect = None
        status, malformed = self.message("공연 보고 싶어")
        self.assertEqual(status, 502)
        self.assertEqual(malformed["diagnostics"]["stage"], "meaning")
        self.model.side_effect = self.model_reply
        with patch("dialogue_memory.decide", side_effect=AttributeError("synthetic policy bug")):
            status, broken = self.message("공연 보고 싶어")
        self.assertEqual(status, 500)
        self.assertEqual(broken["diagnostics"]["stage"], "policy")
        self.assertEqual(broken["state"]["understanding"]["service"], "any", "실패 정책의 잠정 의미는 마지막 상태로 rollback")

    def test_unknown_origin_choice_is_client_error_and_keeps_coordinates(self):
        """없는 후보ID 선택이 모델502나 임의 좌표 채택이 되지 않는다."""
        state = self.locate()
        status, response = self.call({"type": "select_origin", "place_id": "made-up"})
        self.assertIn(status, {400, 422})
        self.assertEqual(response["diagnostics"]["stage"], "event")
        self.assertEqual(response["state"]["conditions"], state["conditions"])
        self.model.assert_not_called()
        self.explore.assert_not_called()

    def test_lease_handover_during_model_drops_old_result(self):
        """늦은 모델 응답은 새 owner의 revision과 목적을 바꾸지 않는다."""
        metadata = deepcopy(self.meta)

        def late(system, context, **limits):
            """모델 처리 중 reload의 lease 인계를 재현한다."""
            self.clock.value += 11
            self.store.open("new-document", metadata["conversation_id"], metadata["epoch"], mode="resume")
            return self.model_reply(system, context, **limits)

        self.model.side_effect = late
        status, response = self.message("공연 보고 싶어")
        self.assertEqual(status, 409)
        self.assertNotEqual(response.get("status"), "ok")
        canonical = self.store.heartbeat(metadata["conversation_id"], metadata["epoch"], "new-document")
        self.assertEqual(canonical["conversation"]["revision"], 0)
        self.assertEqual(canonical["state"]["understanding"]["service"], "any")

    def test_actual_exploration_filter_ranking_and_source_ids_cross_orchestrator(self):
        """실제explore를 연결해 의미 취향이 원본 소개·ID 기반 정렬까지 전달되는지 검사한다."""
        self.locate()
        calm, lively = self.fixed_rows()
        with patch("exploration.explore", wraps=real_explore), \
                patch("exploration.outing.seoul_page", return_value=([lively, calm], "2026-11-01T12:00:00+09:00", 2)), \
                patch("exploration.culture_key", return_value=None):
            status, response = self.message("잔잔한 음악")
        self.assertEqual(status, 200)
        result = response["tool_result"]
        self.assertEqual(result["candidates"][0]["id"], "seoul:101")
        self.assertEqual(result["candidates"][0]["description"], calm["PROGRAM"])
        self.assertEqual(result["ranking"]["status"], "applied")
        self.assertEqual(response["diagnostics"]["model_calls"], 2)
        self.assertEqual(self.model.call_count, 2)
        self.assertNotIn("end_at", response["state"]["conditions"])

    def test_optional_rank_timeout_preserves_content_and_counts_attempt(self):
        """선택2콜 실패도 시도 수에 포함하고 실제 후보를 버리거나 맞춤 성공으로 가장하지 않는다."""
        self.locate()
        calm, lively = self.fixed_rows()

        def failed_rank(system, context, **limits):
            """첫 의미 호출은 성공하고 후보 후처리만 의도적으로 실패시킨다."""
            if "candidates" in context:
                raise TimeoutError()
            return self.model_reply(system, context, **limits)

        self.model.side_effect = failed_rank
        with patch("exploration.explore", wraps=real_explore), \
                patch("exploration.outing.seoul_page", return_value=([lively, calm], "2026-11-01T12:00:00+09:00", 2)), \
                patch("exploration.culture_key", return_value=None):
            status, response = self.message("잔잔한 음악")
        self.assertEqual(status, 200)
        self.assertEqual({item["id"] for item in response["tool_result"]["candidates"]}, {"seoul:101", "seoul:102"})
        self.assertNotEqual(response["tool_result"]["ranking"]["status"], "applied")
        self.assertEqual(response["diagnostics"]["model_calls"], 2)
        self.assertEqual(self.model.call_count, 2)

    def prepare_content_choices(self):
        """실제 orchestration에7개 고정 source 후보를 제공해 서버3개 표시계약을 만든다."""
        self.locate("exhibition")

        def result(state, mode, ranker):
            """현재 서버조건과 연결된 사실형 후보만 반환한다."""
            context = dict(execution_key="choice-result-" + str(state["conditions"].get("free_only", False)),
                           service=state["understanding"]["service"], conditions=deepcopy(state["conditions"]))
            return dict(status="ok", result_kind="content_exploration", not_applied=[], coverage_note="고정 source7건",
                        result_context=context, candidates=[dict(id=f"seoul:{number}", title=f"전시 {number}",
                        lat=37.567, lng=126.98, result_context=deepcopy(context)) for number in range(1, 8)])

        self.explore.side_effect = result
        status, response = self.message("찾아줘")
        self.assertEqual(status, 200)
        return response

    def select_event(self, response, identity=None):
        """클라이언트는 사실 snapshot 대신 서버가 발급한 ID와 결과/묶음 참조만 보낸다."""
        batch = response["state"]["display_batch"]
        return dict(type="select_content", candidate_id=identity or batch["candidate_ids"][0],
                    result_execution_key=batch["execution_key"], display_batch_id=batch["id"])

    def test_current_batch_number_name_and_button_share_selection_without_model_or_source(self):
        """화면3번·음성단답·동일카드버튼은 같은 검증후보로 연결하고 날짜나 재조회가 생기지 않는다."""
        response = self.prepare_content_choices()
        batch = response["tool_result"]["display_batch"]
        self.assertEqual(batch, response["state"]["display_batch"])
        self.assertEqual(batch["candidate_ids"], ["seoul:1", "seoul:2", "seoul:3"])
        before = deepcopy(response["state"]["conditions"])
        self.model.reset_mock()
        source_calls = self.explore.call_count
        for text in ("3번", "세번째", "세번째로할게요", "삼번", "3번이요", "3번요", "3번으로 할게요", "전시 3"):
            with self.subTest(text=text):
                status, selected = self.message(text)
                self.assertEqual(status, 200)
                self.assertEqual(selected["next_action"]["type"], "content_selected")
                self.assertEqual(selected["next_action"]["candidate"]["id"], "seoul:3")
                self.assertIsNone(selected["tool_result"])
                self.assertEqual(selected["state"]["conditions"], before)
                self.assertNotIn("start_at", selected["state"]["conditions"])
        status, button = self.call(self.select_event(response, "seoul:3"))
        self.assertEqual(status, 200)
        self.assertEqual(button["state"]["selected_content"]["id"], "seoul:3")
        self.model.assert_not_called()
        self.assertEqual(self.explore.call_count, source_calls)

    def test_actual_exploration_address_normalization_does_not_reject_the_current_selection(self):
        """실제exploration이 원점주소를 표시메타로생략해도 동일canonical좌표 후보선택은 성공한다."""
        self.locate("performance")
        with patch("exploration.explore", wraps=real_explore), \
                patch("exploration.outing.seoul_page", return_value=(list(self.fixed_rows()), "2026-11-01T12:00:00+09:00", 2)) as source, \
                patch("exploration.culture_key", return_value=None):
            status, result = self.message("찾아줘")
            self.assertEqual(status, 200)
            self.assertIn("address", result["state"]["conditions"]["start_location"])
            self.assertNotIn("address", result["tool_result"]["result_context"]["conditions"]["start_location"])
            model_calls, source_calls = self.model.call_count, source.call_count
            status, selected = self.call(self.select_event(result))
            self.assertEqual(status, 200)
            self.assertEqual(selected["next_action"]["type"], "content_selected")
            self.assertEqual(selected["state"]["conditions"], result["state"]["conditions"])
            self.assertEqual(source.call_count, source_calls)
            self.assertEqual(self.model.call_count, model_calls)

    def test_alternatives_advance_only_server_batch_and_reject_old_or_foreign_choices(self):
        """다음묶음은 동일서버풀의4~6번이며 과거묶음·풀밖ID·다른대화는 선택/조회하지 못한다."""
        initial = self.prepare_content_choices()
        old = self.select_event(initial)
        self.model.reset_mock()
        source_calls = self.explore.call_count
        status, other = self.message("다른 곳도 보여줘")
        self.assertEqual(status, 200)
        self.assertEqual(other["state"]["display_batch"]["candidate_ids"], ["seoul:4", "seoul:5", "seoul:6"])
        self.assertNotEqual(other["state"]["display_batch"]["id"], initial["state"]["display_batch"]["id"])
        for event in (old, self.select_event(other, "seoul:99")):
            status, rejected = self.call(event)
            self.assertEqual(status, 200)
            self.assertIn("selection_error", rejected["next_action"])
            self.assertIsNone(rejected["tool_result"])
            self.assertIsNone(rejected["state"]["selected_content"])
        self.message("다른 곳도 보여줘")
        status, exhausted = self.message("다른 곳도 보여줘")
        self.assertEqual(status, 200)
        self.assertIsNone(exhausted["tool_result"])
        self.assertIn("모두 보여드렸", exhausted["assistant_text"])
        self.locate("exhibition")
        status, foreign = self.call(old)
        self.assertEqual(status, 200)
        self.assertEqual(foreign["next_action"]["selection_error"], "stale_content_batch")
        self.model.assert_not_called()
        self.assertEqual(self.explore.call_count, source_calls)

    def test_unclear_chitchat_and_empty_meaning_keep_selection_without_false_model_success(self):
        """모호한 정상해석은 현재선택 안내로회복하되 깨진envelope는 별도오류로 남긴다."""
        initial = self.prepare_content_choices()
        self.call(self.select_event(initial, "seoul:2"))
        source_calls = self.explore.call_count
        understanding = initial["state"]["understanding"]
        for payload_kind in ("inform", "chitchat", "empty"):
            message = "말씀하신 주"
            payload = self.payload(message, "temporary", act=payload_kind if payload_kind != "empty" else "inform")
            if payload_kind == "empty":
                payload.update(acts=[], updates=[])

            def meaning(system, context, **limits):
                """실제 현재turn 근거만 바꿔 정책/저장소 검증은 그대로 통과한다."""
                value = deepcopy(payload)
                for act in value["acts"]:
                    act["evidence"]["turn_id"] = context["turn_id"]
                return value, {"model": "fixed-meaning"}

            with patch("agent_v3.model_json", side_effect=meaning):
                status, response = self.message(message)
            self.assertEqual(status, 200)
            self.assertEqual(response["next_action"]["type"], "reply")
            self.assertEqual(response["state"]["selected_content"]["id"], "seoul:2")
            self.assertEqual(response["state"]["understanding"], understanding)
            self.assertIsNone(response["tool_result"])
            self.assertNotIn("어떤 나들이가", response["assistant_text"])
        with patch("agent_v3.model_json", return_value=({"broken": True}, {})):
            status, broken = self.message("불명확 발화")
        self.assertEqual(status, 502)
        self.assertEqual(broken["code"], "ai_response_invalid")
        self.assertEqual(self.explore.call_count, source_calls)

    def test_real_filter_change_clears_old_selection_and_old_batch_cannot_bypass_it(self):
        """무료필터 변경은 기존선택을해제한뒤 새결과만발급하고 이전버튼으로 새조건을우회하지 못한다."""
        initial = self.prepare_content_choices()
        old = self.select_event(initial, "seoul:2")
        self.call(old)

        def free_meaning(system, context, **limits):
            """무료명시 현재발화의 실제조건후보만 제공한다."""
            return self.payload(context["message"], context["turn_id"], [("condition", "free_only", True)]), {}

        with patch("agent_v3.model_json", side_effect=free_meaning):
            status, changed = self.message("무료만")
        self.assertEqual(status, 200)
        self.assertTrue(changed["state"]["conditions"]["free_only"])
        self.assertIn("선택은 해제", changed["assistant_text"])
        self.assertIsNone(changed["state"]["selected_content"])
        self.assertNotEqual(changed["state"]["display_batch"]["execution_key"], initial["state"]["display_batch"]["execution_key"])
        source_calls = self.explore.call_count
        status, rejected = self.call(old)
        self.assertEqual(status, 200)
        self.assertEqual(rejected["next_action"]["selection_error"], "stale_content_batch")
        self.assertTrue(rejected["state"]["conditions"]["free_only"])
        self.assertEqual(self.explore.call_count, source_calls)

    def test_visit_under_sixty_minutes_rejects_before_any_source(self):
        """방문 단계의60분 미만 입력은 minimum_duration이며 소스 조회 전에 중단한다."""
        self.visit_state("2099-11-01T14:59:00+09:00")
        with patch("outing.seoul_page") as source, \
                patch("outing.recommend", side_effect=AssertionError("legacy recommend must not route v3 visit")) as legacy:
            status, response = self.call({"type": "proceed", "mode": "visit"})
        self.assertEqual(status, 400)
        self.assertEqual(response["code"], "minimum_duration")
        source.assert_not_called()
        legacy.assert_not_called()
        self.explore.assert_not_called()
        self.model.assert_not_called()

    def test_visit_uses_same_performance_filters_preferences_and_explicit_context(self):
        """방문 전환이 공연을 전시로 바꾸지 않고 원 취향·실제 시간/출발지 맥락을 유지한다."""
        state = self.visit_state("2099-11-01T15:00:00+09:00")
        calm, unused = self.fixed_rows()
        exhibition = dict(calm, TITLE="고정 전시", CODENAME="전시/미술", PROGRAM="잔잔한 사진 전시",
                          PRO_TIME="10:00~18:00", HMPG_ADDR="https://culture.seoul.go.kr/event?cultcode=103")
        with patch("exploration.explore", wraps=real_explore) as actual_explore, \
                patch("exploration.outing.seoul_page", return_value=([exhibition, calm], "2026-11-01T12:00:00+09:00", 2)), \
                patch("exploration.culture_key", return_value=None), \
                patch("outing.recommend", side_effect=AssertionError("legacy recommend must not route v3 visit")) as legacy:
            status, response = self.call({"type": "proceed", "mode": "visit"})
        self.assertEqual(status, 200)
        legacy.assert_not_called()
        queried = actual_explore.call_args.args[0]
        self.assertEqual(queried["understanding"]["service"], "performance")
        self.assertEqual(queried["understanding"]["preferences"], state["understanding"]["preferences"])
        self.assertNotIn("category", queried["conditions"], "validate용 전체 분류가 실제 탐색조건에 유입되지 않음")
        result = response["tool_result"]
        self.assertEqual(result["result_kind"], "visit_plan")
        self.assertEqual([candidate["id"] for candidate in result["candidates"]], ["seoul:101"])
        self.assertEqual(result["ranking"]["status"], "applied")
        candidate = result["candidates"][0]
        self.assertEqual(candidate["visit_status"], "unknown")
        self.assertEqual(candidate["semantic_evidence"][0]["quote"], calm["PROGRAM"])
        self.assertEqual(candidate["visit_validation_context"]["start_at"], state["conditions"]["start_at"])
        self.assertEqual(candidate["visit_validation_context"]["end_at"], state["conditions"]["end_at"])
        self.assertEqual(candidate["origin_context"], state["conditions"]["start_location"])


if __name__ == "__main__":
    unittest.main()
