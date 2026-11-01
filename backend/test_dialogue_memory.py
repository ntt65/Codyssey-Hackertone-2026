"""v3 순수 대화 정책의 실제 실패 맥락·부분 성공·필수조건·이벤트 회귀."""
from copy import deepcopy
from datetime import datetime, timedelta
import unittest

from dialogue_memory import new_state, interpret, decide, apply_event, content_choice_event
from outing import KST


class DialogueMemoryTests(unittest.TestCase):
    """외부 모델/공급자 없이 의미 계약과 실제 grounding 경계를 검사한다."""

    def envelope(self, message, updates=None, act="inform", turn="t1", question=None):
        """현재 턴 원문 근거가 있는 실제 v3 모델 envelope를 만든다."""
        return {"schema_version": 1, "acts": [{"type": act, "question_id": question,
            "evidence": {"turn_id": turn, "quote": message}}], "updates": updates or []}

    def update(self, message, domain, field, value=None, turn="t1", identity="u1", **extra):
        """한 필드 후보를 만든다. 테스트에서 오류 항목만 명시적으로 바꾼다."""
        return {"id": identity, "domain": domain, "field": field, "op": "add", "target_id": None,
                "value": value, "strength": "soft", "evidence": {"turn_id": turn, "quote": message}, **extra}

    def located(self, service="performance"):
        """검증된 공개 예시 위치를 가진 상태를 만든다."""
        state = new_state()
        state["understanding"].update(goal="공연 관람", service=service)
        return apply_event(state, {"type": "select_origin", "place": {"label": "서울시청", "lat": 37.5665, "lng": 126.978}})

    def remember_question(self, state):
        """서버 통합 계약대로 정책이 고른 질문을 기록한다."""
        action = decide(state)
        if action.get("question"):
            state["active_question"] = deepcopy(action["question"])
            state["question_history"].append(deepcopy(action["question"]))
        return action

    def test_reported_performance_explanation_and_mood(self):
        """공연→무슨조건→잔잔한음악에서 변경질문/장르생성 없이 기존 질문과 취향을 보존한다."""
        message = "공연을 보고 싶어"
        updates = [self.update(message, "goal", "text", "공연 관람", identity="goal"),
                   self.update(message, "service", "activity", "performance", identity="service")]
        state = interpret(self.envelope(message, updates), message, new_state(), "t1")
        first = self.remember_question(state)
        self.assertEqual(first["question"]["target"], "start_location")
        self.assertNotIn("바꾸고", first["text"])
        message = "뭘 알려 줘 무슨 조건"
        state = interpret(self.envelope(message, act="explain_question", turn="t2", question=state["active_question"]["id"]), message, state, "t2")
        self.assertIn("지역을 여쭤본", decide(state)["text"])
        message = "잔잔한 음악"
        state = interpret(self.envelope(message, [self.update(message, "preference", "atmosphere", "calm", turn="t3")], turn="t3"), message, state, "t3")
        self.assertEqual(state["understanding"]["preferences"][0]["value"], "calm")
        self.assertNotIn("category", state["conditions"])
        self.assertNotIn("music_followup", state["conditions"])
        self.assertEqual(state["active_question"]["target"], "start_location")
        state = apply_event(state, {"type": "select_origin", "data": {"label": "서울시청", "lat": 37.5665, "lng": 126.978}})
        self.assertEqual(decide(state)["type"], "explore")

    def test_semantic_paraphrase_is_not_literal_word_gated(self):
        """활동 이름 없는 의역도 모델의 근거 있는 의미를 수용한다."""
        message = "큰 스크린으로 몰입하고 싶어"
        state = interpret(self.envelope(message, [self.update(message, "service", "activity", "movie")]), message, self.located(), "t1")
        self.assertEqual(state["understanding"]["service"], "movie")
        self.assertEqual(decide(state)["query"], "영화관")
        self.assertNotIn("상영작을 찾았", decide(state)["text"])

    def test_invalid_category_cannot_cancel_good_mood(self):
        """유효 취향과 잘못된 메뉴 후보를 섞어도 대화/실제 탐색을 유지한다."""
        message = "잔잔한 음악"
        state = interpret(self.envelope(message, [self.update(message, "preference", "atmosphere", "calm"),
             self.update(message, "condition", "category", "음악", identity="bad")]), message, self.located(), "t1")
        self.assertEqual(state["diagnostics"]["turn_status"], "partial")
        self.assertEqual(state["understanding"]["preferences"][0]["value"], "calm")
        self.assertNotIn("category", state["conditions"])
        self.assertEqual(decide(state)["type"], "explore")

    def test_music_does_not_expand_genres_but_explicit_genre_works(self):
        """음악 분위기에서 장르3개를 생성하지 않으며 명시 국악은 실제 메뉴로 검증한다."""
        message = "잔잔한 음악"
        state = interpret(self.envelope(message, [self.update(message, "condition", "categories", ["국악", "클래식", "콘서트"])]), message, self.located(), "t1")
        self.assertNotIn("categories", state["conditions"])
        message = "국악이 좋아"
        state = interpret(self.envelope(message, [self.update(message, "condition", "category", "국악", turn="t2")], turn="t2"), message, state, "t2")
        self.assertEqual(state["conditions"]["categories"], ["국악"])

    def test_current_turn_evidence_and_optional_metadata(self):
        """다른 턴 근거는 거절하되 선택 metadata/질문ID 오류가 유효 act를 지우지 않는다."""
        message = "공연"
        payload = self.envelope(message, [self.update(message, "service", "activity", "movie", turn="old")], question="unknown")
        payload["assistant_text"] = "임의 산문"
        state = interpret(payload, message, new_state(), "t1")
        self.assertEqual(state["understanding"]["service"], "any")
        self.assertEqual(state["latest_moves"][0]["type"], "inform")
        self.assertEqual(state["diagnostics"]["turn_status"], "partial")
        with self.assertRaises(ValueError):
            interpret({"schema_version": 1, "updates": []}, message, state, "t2")

    def test_invalid_replace_is_transactional(self):
        """잘못된 교체 후보는 이전 선호를 먼저 지우지 않는다."""
        message = "조용한 게 좋아"
        state = interpret(self.envelope(message, [self.update(message, "preference", "atmosphere", "calm", identity="p1")]), message, self.located(), "t1")
        before = deepcopy(state)
        message = "신나는 게 좋아"
        bad = self.update(message, "preference", "atmosphere", "exciting", turn="t2", op="replace", target_id="p1", polarity="invalid")
        after = interpret(self.envelope(message, [bad], turn="t2"), message, state, "t2")
        self.assertEqual(after["understanding"]["preferences"], before["understanding"]["preferences"])
        self.assertEqual(state, before)

    def test_hard_free_survives_malformed_and_omitted_candidate(self):
        """무료만 후보 손상/모델 누락 모두 유료 추천을 통과시키지 않는다."""
        message = "무료만 가능한 공연"
        for updates in ([], [self.update(message, "condition", "free_only", "yes", strength="hard")]):
            state = interpret(self.envelope(message, updates), message, self.located(), "t1")
            self.assertTrue(any(h["strength"] == "hard" for h in state["hypotheses"]))
            self.assertEqual(decide(state)["question"]["target"], "requirement")
        state = interpret(self.envelope(message, [self.update(message, "condition", "free_only", True, strength="hard")]), message, self.located(), "t1")
        self.assertTrue(state["conditions"]["free_only"])
        self.assertFalse(state["hypotheses"])
        self.assertEqual(decide(state)["type"], "explore")

    def test_hard_requirement_not_removed_by_unrelated_request(self):
        """대상 밖 해제 표현이 기존 접근성 필수조건을 지우지 않는다."""
        message = "계단 없음"
        state = interpret(self.envelope(message, [self.update(message, "requirement", "accessibility", message, strength="hard", identity="stairs")]), message, self.located(), "t1")
        message = "국악은 빼 줘"
        state = interpret(self.envelope(message, [self.update(message, "requirement", "accessibility", turn="t2", op="remove", target_id="stairs")], turn="t2"), message, state, "t2")
        self.assertTrue(state["hypotheses"])
        self.assertEqual(decide(state)["type"], "reply")

    def test_service_change_keeps_common_constraints_and_is_order_independent(self):
        """서비스 변경은 이전 분류만 무효화하며 새 취향과 공통 무료조건을 보존한다."""
        state = self.located("exhibition")
        state["conditions"].update(category="전시", categories=["전시"], free_only=True)
        message = "공연을 잔잔하게 보고 싶어"
        updates = [self.update(message, "preference", "atmosphere", "calm", identity="p1"),
                   self.update(message, "service", "activity", "performance", identity="s1")]
        result = interpret(self.envelope(message, updates), message, state, "t1")
        self.assertNotIn("category", result["conditions"])
        self.assertTrue(result["conditions"]["free_only"])
        self.assertEqual(result["understanding"]["preferences"][0]["value"], "calm")
        self.assertEqual(decide(result)["type"], "explore")

    def test_origin_and_free_pending_order(self):
        """검증된 새 위치 선택이 먼저 대기 중인 무료 변경을 덮어쓰지 않는다."""
        state = self.located()
        state["conditions"]["free_only"] = True
        state["field_meta"]["free_only"] = {"confirmed": True, "id": "old"}
        message = "유료도 괜찮아"
        state = interpret(self.envelope(message, [self.update(message, "condition", "free_only", False)]), message, state, "t1")
        self.assertEqual(state["pending_changes"][0]["field"], "free_only")
        state = apply_event(state, {"type": "select_origin", "place": {"label": "강남역", "lat": 37.4979, "lng": 127.0276}})
        self.assertEqual([p["field"] for p in state["pending_changes"]], ["free_only", "start_location"])
        state = apply_event(state, {"type": "confirm_change", "field": "free_only"})
        self.assertFalse(state["conditions"]["free_only"])
        self.assertEqual(state["conditions"]["start_location"]["label"], "서울시청")
        state = apply_event(state, {"type": "confirm_change", "field": "start_location"})
        self.assertEqual(state["conditions"]["start_location"]["label"], "강남역")

    def test_dates_optional_for_explore_required_only_for_visit(self):
        """내용 탐색에 시간을 강요하지 않고 방문 모드에서만 일정 질문을 선택한다."""
        state = self.located()
        before = deepcopy(state)
        self.assertEqual(decide(state)["type"], "explore")
        self.assertEqual(state, before)
        state = apply_event(state, {"type": "proceed", "mode": "visit"})
        self.assertEqual(decide(state)["question"]["target"], "start_at")
        message = "내일"
        tomorrow = (datetime.now(KST).date() + timedelta(days=1)).isoformat()
        state = interpret(self.envelope(message, [self.update(message, "condition", "date", tomorrow)]), message, state, "t1")
        self.assertEqual(state["conditions"]["date"], tomorrow)
        self.assertNotIn("start_at", state["conditions"])

    def test_restore_preserves_hard_without_importing_verified_coordinates(self):
        """복원은 사용자 주장이고 도구사실/확정 플래그/좌표는 재검증 대상으로 돌린다."""
        snapshot = self.located()
        snapshot["hypotheses"] = [{"id": "h1", "field": "accessibility", "strength": "hard", "value": "계단 없음"}]
        snapshot["tool_facts"] = [{"fake": "verified"}]
        restored = apply_event(new_state(), {"type": "restore", "snapshot": snapshot})
        self.assertNotIn("start_location", restored["conditions"])
        self.assertEqual(restored["conditions"]["start_query"], "서울시청")
        self.assertFalse(restored["tool_facts"])
        self.assertEqual(restored["hypotheses"][0]["status"], "unresolved")
        self.assertEqual(decide(restored)["type"], "resolve_origin")

    def test_greeting_does_not_force_location_or_condition_form(self):
        """인사를 조건변경 실패나 출발지 필수질문으로 만들지 않는다."""
        message = "안녕"
        state = interpret(self.envelope(message, act="chitchat"), message, new_state(), "t1")
        self.assertEqual(decide(state)["question"]["target"], "service")

    def test_explicit_requirement_release_not_recreated(self):
        """‘계단 없어도 괜찮아’라는 명시 완화는 같은 주제의 이전 필수조건만 해제한다."""
        message = "계단 없음"
        state = interpret(self.envelope(message, [self.update(message, "requirement", "accessibility", message, strength="hard", identity="stairs")]), message, self.located(), "t1")
        message = "계단 없어도 괜찮아"
        state = interpret(self.envelope(message, [self.update(message, "requirement", "accessibility", turn="t2", op="remove", target_id="stairs")], turn="t2"), message, state, "t2")
        self.assertFalse(state["hypotheses"])
        self.assertEqual(decide(state)["type"], "explore")

    def test_restore_question_and_legacy_hard_requirements(self):
        """복원 시 현재 질문과 구버전 필수조건도 남기며 GPS 좌표는 재사용하지 않는다."""
        snapshot = self.located()
        snapshot["active_question"] = {"id": "q:1", "target": "taste", "text": "어떤 공연이 좋으세요?"}
        snapshot["conditions"]["unsupported_requirements"] = ["계단 없음"]
        restored = apply_event(new_state(), {"type": "restore", "snapshot": snapshot})
        self.assertEqual(restored["active_question"]["target"], "taste")
        self.assertEqual(restored["hypotheses"][0]["value"], "계단 없음")
        snapshot["conditions"]["start_location"]["label"] = "현재 위치"
        restored = apply_event(new_state(), {"type": "restore", "snapshot": snapshot})
        self.assertNotIn("start_query", restored["conditions"])

    def test_schema_version_strict_and_explicit_goal_not_hard(self):
        """불리언/실수 schema와 일반적인 ‘영화 꼭’ 목적을 필수 제약으로 바꾸는 것을 막는다."""
        for version in (True, 1.0, "1"):
            with self.assertRaises(ValueError):
                interpret({"schema_version": version, "acts": []}, "안녕", new_state(), "t1")
        message = "영화 꼭 보고 싶어"
        state = interpret(self.envelope(message, [self.update(message, "service", "activity", "movie")]), message, self.located(), "t1")
        self.assertFalse(state["hypotheses"])

    def test_soft_unverified_preference_is_not_a_hard_hold(self):
        """모델이 requirement영역에 넣어도 명시 soft 분위기는 검색 전체를 막지 않는다."""
        message = "가까우면 좋겠어"
        state = interpret(self.envelope(message, [self.update(message, "requirement", "distance", message, strength="soft")]), message, self.located(), "t1")
        self.assertFalse(any(h["strength"] == "hard" for h in state["hypotheses"]))
        self.assertEqual(decide(state)["type"], "explore")

    def test_origin_answer_depends_on_question_target_not_phrasing(self):
        """설명·반복 뒤 ‘출발’ 없는 질문에도 서울시청 단답의 의미가 유지된다."""
        state = new_state()
        state["understanding"]["service"] = "performance"
        state["active_question"] = {"id": "q:location", "target": "start_location", "text": "서울시청이나 개포동 중 어디 근처에서 찾아볼까요?"}
        message = "시청 서울시청"
        state = interpret(self.envelope(message, [self.update(message, "condition", "start_query", "서울시청")]), message, state, "t1")
        self.assertEqual(state["conditions"]["start_query"], "서울시청")
        self.assertEqual(decide(state)["type"], "resolve_origin")

    def test_no_invented_duration_or_all_categories_default(self):
        """일반 취향 원문을 인용해 임의 체류시간이나 전체 메뉴 기본값을 만들지 않는다."""
        message = "잔잔한 음악이 좋아"
        for field, value in (("stay_minutes", 30), ("category", "전체")):
            state = interpret(self.envelope(message, [self.update(message, "condition", field, value)]), message, self.located(), "t1")
            self.assertNotIn(field, state["conditions"])
            self.assertEqual(state["diagnostics"]["turn_status"], "partial")

    def test_origin_query_keeps_confirmed_coordinates_until_actual_choice_consent(self):
        """새 지명 조회가 기존 확정 좌표를 지워 변경 동의를 우회하지 못한다."""
        state = self.located()
        original = deepcopy(state["conditions"]["start_location"])
        message = "수원시청"
        state = interpret(self.envelope(message, [self.update(message, "condition", "start_query", message)]), message, state, "t1")
        self.assertEqual(state["conditions"]["start_location"], original)
        self.assertEqual(decide(state)["type"], "resolve_origin")
        state = apply_event(state, {"type": "select_origin", "place": {"label": "수원시청", "lat": 37.2636, "lng": 127.0286}})
        self.assertEqual(state["conditions"]["start_location"], original)
        self.assertEqual(state["pending_changes"][0]["field"], "start_location")
        state = apply_event(state, {"type": "confirm_change", "field": "start_location"})
        self.assertEqual(state["conditions"]["start_location"]["label"], "수원시청")

    def test_same_verified_origin_alias_needs_no_lookup(self):
        """이미 확인한 장소의 정확한 별칭은 좌표나 동의를 다시 요구하지 않는다."""
        state = self.located()
        message = "서울특별시청"
        state = interpret(self.envelope(message, [self.update(message, "condition", "start_query", message)]), message, state, "t1")
        self.assertNotIn("start_query", state["conditions"])
        self.assertEqual(decide(state)["type"], "explore")
        message = "서울역에서 출발해서 서울시청에 가고 싶어"
        state = interpret(self.envelope(message, [self.update(message, "condition", "start_query", "서울시청", turn="t2")], turn="t2"), message, state, "t2")
        self.assertNotIn("start_query", state["conditions"])
        self.assertEqual(state["diagnostics"]["turn_status"], "partial")

    def test_first_bare_place_is_a_lookup_candidate_not_a_verified_coordinate(self):
        """질문 전 먼저 말한 지명도 조회하되 모델이 좌표를 확정하지 못한다."""
        message = "서울시청"
        state = interpret(self.envelope(message, [self.update(message, "condition", "start_query", message)]), message, new_state(), "t1")
        self.assertEqual(decide(state)["type"], "resolve_origin")
        self.assertNotIn("start_location", state["conditions"])

    def test_explicit_visit_plan_proceed_mode(self):
        """자연어 방문계획 요청만 visit로 전환하고 부족한 일정은 그 단계에서 질문한다."""
        message = "이걸로 내일 2시부터 방문계획을 세워줘"
        payload = self.envelope(message, act="proceed")
        payload["acts"][0]["mode"] = "visit"
        state = interpret(payload, message, self.located(), "t1")
        self.assertEqual(state["request_mode"], "visit")
        self.assertEqual(decide(state)["question"]["target"], "start_at")

    def test_generic_proceed_does_not_enter_or_keep_visit_mode(self):
        """일반 검색은 explore이며 모델의 부당한 visit 제안과 날짜만의 모드변경을 막는다."""
        for message, act, explicit_mode in (("찾아줘", "proceed", "visit"), ("방문계획 말고 그냥 찾아줘", "proceed", "visit"), ("내일", "inform", None)):
            state = self.located()
            state["request_mode"] = "visit" if act == "proceed" else "explore"
            payload = self.envelope(message, act=act)
            if explicit_mode:
                payload["acts"][0]["mode"] = explicit_mode
            result = interpret(payload, message, state, "t1")
            self.assertEqual(result["request_mode"], "explore")
        state = self.located()
        state["request_mode"] = "visit"
        message = "이 조건으로 찾아줘"
        self.assertEqual(interpret(self.envelope(message, act="proceed"), message, state, "t1")["request_mode"], "explore")

    def test_invalid_visit_routing_candidate_is_not_a_hard_requirement(self):
        """실모델 E20의 잘못된 course후보가 유효 방문전이를 필수조건 보류로 바꾸지 않는다."""
        message = "이 공연으로 내일 오후 2시부터 오후 5시까지 방문 계획을 세워줘"
        payload = self.envelope(message, [self.update(message, "condition", "request_kind", "course", strength="hard")], act="proceed")
        payload["acts"][0]["mode"] = "visit"
        state = self.located()
        tomorrow = (datetime.now(KST).date() + timedelta(days=1)).isoformat()
        state["conditions"].update(start_at=tomorrow + "T14:00:00+09:00", end_at=tomorrow + "T17:00:00+09:00")
        result = interpret(payload, message, state, "t1")
        self.assertFalse(result["hypotheses"])
        self.assertNotIn("request_kind", result["conditions"])
        self.assertEqual(decide(result)["type"], "visit")

    def test_invalid_routing_hard_labels_do_not_create_constraint_holds(self):
        """잘못된 활동/분류 후보의 hard표시가 유효한 영화 목적과 실제 조회를 막지 않는다."""
        message = "영화 보고 싶어"
        for domain, field, value in (("condition", "category", "영화"), ("condition", "categories", ["영화"]),
                                     ("goal", "text", []), ("service", "activity", "cinema")):
            updates = [self.update(message, "service", "activity", "movie", identity="service"),
                       self.update(message, domain, field, value, identity="bad", strength="hard")]
            result = interpret(self.envelope(message, updates), message, self.located(), "t1")
            self.assertEqual(result["understanding"]["service"], "movie")
            self.assertFalse(any(h["strength"] == "hard" for h in result["hypotheses"]))
            self.assertEqual(decide(result)["type"], "search_places")

    def choice_state(self):
        """현재 표시3개와 실제 서버결과를 가진 상태만 만든다. 클라이언트 후보는 받지 않는다."""
        state = self.located("exhibition")
        context = dict(execution_key="current-result", service="exhibition", conditions=deepcopy(state["conditions"]))
        candidates = [dict(id=f"event:{number}", title=f"전시 {number}", result_context=deepcopy(context)) for number in range(1, 5)]
        state.update(result_context=context, display_batch=dict(id="batch-1", execution_key="current-result", candidate_ids=["event:1", "event:2", "event:3"]),
                     tool_facts=[dict(status="ok", candidates=candidates, result_context=deepcopy(context))])
        return state

    def test_number_and_unique_name_resolve_only_the_current_visible_batch(self):
        """발화 조사를 포함한 번호는 화면3개에만 매핑하고 날짜·불명확 이름을 선택으로 추측하지 않는다."""
        state = self.choice_state()
        for text in ("3번", "세번째", "세 번째요", "세번째로할게요", "삼번", "3번이요", "3번요", "3번으로할래", "3번으로 할게요", "전시 3"):
            with self.subTest(text=text):
                self.assertEqual(content_choice_event(state, text)["candidate_id"], "event:3")
        self.assertEqual(content_choice_event(state, "4번")["selection_error"], "content_number_out_of_range")
        self.assertIsNone(content_choice_event(state, "3시"))
        self.assertIsNone(content_choice_event(state, "3번 말고 무료만"))
        self.assertIsNone(content_choice_event(state, "전시"))
        state["tool_facts"][0]["candidates"][1]["title"] = "전시 3"
        self.assertEqual(content_choice_event(state, "전시 3")["selection_error"], "ambiguous_content_name")

    def test_selection_requires_current_batch_real_fact_and_unchanged_conditions(self):
        """과거묶음·다른결과·화면밖ID·필수변경대기·조작된조건으로 선택을 확정하지 못한다."""
        state = self.choice_state()
        event = content_choice_event(state, "3번")
        selected = apply_event(state, {**event, "candidate": {"title": "조작한 사실"}})
        self.assertEqual(selected["selected_content"]["title"], "전시 3")
        self.assertEqual(decide(selected)["type"], "content_selected")
        for patch in ({"display_batch_id": "past-batch"}, {"result_execution_key": "other-result"}, {"candidate_id": "event:4"}):
            with self.assertRaises(ValueError):
                apply_event(state, {**event, **patch})
        for variant in ("pending", "conditions", "facts"):
            changed = deepcopy(state)
            if variant == "pending":
                changed["pending_changes"] = [dict(id="p", field="free_only")]
            elif variant == "conditions":
                changed["conditions"]["free_only"] = True
            else:
                changed["tool_facts"] = []
            with self.assertRaises(ValueError):
                apply_event(changed, event)

    def test_selection_ignores_origin_display_metadata_but_not_coordinates_or_filters(self):
        """원점주소 유무는 실제동일위치로 보되 좌표·날짜·필수조건 차이는 엄격하게 차단한다."""
        state = self.choice_state()
        event = content_choice_event(state, "3번")
        state["conditions"]["start_location"]["address"] = "서울 중구 세종대로 110"
        self.assertEqual(apply_event(state, event)["selected_content"]["id"], "event:3")
        for field, value in (("date", "2099-01-01"), ("free_only", True), ("budget_krw", 10000), ("exclude_terms", ["공원"])):
            changed = deepcopy(state)
            changed["conditions"][field] = value
            with self.assertRaisesRegex(ValueError, "stale_content_batch"):
                apply_event(changed, event)
        changed = deepcopy(state)
        changed["conditions"]["start_location"]["lat"] += 0.01
        with self.assertRaisesRegex(ValueError, "stale_content_batch"):
            apply_event(changed, event)

    def test_unclear_turn_retains_goal_batch_selection_and_does_not_search(self):
        """모호한 발화는 기존목적/후보/선택을 보존하고 목적질문이나 자동재검색으로 돌아가지 않는다."""
        state = self.choice_state()
        for act in ("inform", "chitchat", "proceed"):
            message = "말씀하신 주"
            updated = interpret(self.envelope(message, act=act), message, state, "t1")
            self.assertEqual(decide(updated)["type"], "reply")
            self.assertNotIn("어떤 나들이가", decide(updated)["text"])
            self.assertEqual(updated["understanding"], state["understanding"])
            self.assertEqual(updated["display_batch"], state["display_batch"])
        selected = apply_event(state, content_choice_event(state, "2번"))
        updated = interpret(self.envelope("고마워", act="chitchat"), "고마워", selected, "t1")
        self.assertEqual(decide(updated)["type"], "reply")
        self.assertIn("전시 2", decide(updated)["text"])
        self.assertEqual(updated["selected_content"], selected["selected_content"])
        no_result = self.located("exhibition")
        no_result["latest_moves"] = [{"type": "chitchat"}]
        self.assertNotIn("어떤 나들이가", decide(no_result)["text"])

    def test_changed_hard_condition_or_service_invalidates_choice_but_restore_does_not_trust_it(self):
        """실제예산/활동변경은 현재선택·묶음을 비우며 복원된 snapshot을 새 실제선택으로 신뢰하지 않는다."""
        state = self.choice_state()
        state = apply_event(state, content_choice_event(state, "2번"))
        for message, domain, field, value in (("무료만", "condition", "free_only", True), ("영화 보고 싶어", "service", "activity", "movie")):
            updated = interpret(self.envelope(message, [self.update(message, domain, field, value)]), message, state, "t1")
            self.assertIsNone(updated["display_batch"])
            self.assertIsNone(updated["selected_content"])
            self.assertIsNone(updated["result_context"])
            self.assertIn("선택은 해제", decide(updated)["text"])
            self.assertTrue(updated["tool_facts"], "과거 tool 사실이 남아도 현재 선택 검증을 통과하지 못함")
        restored = apply_event(state, dict(type="restore", snapshot=state))
        self.assertIsNone(restored["display_batch"])
        self.assertIsNone(restored["selected_content"])
        self.assertFalse(restored["tool_facts"])

    def test_fact_constraint_requires_current_semantic_evidence(self):
        """무료/예산/접근성 실제 제약은 보존하되 의미 없는 modelhard 표지만으로 보류하지 않는다."""
        for message, domain, field, value in (("무료만", "condition", "free_only", "bad"),
                                            ("예산은 10000원", "condition", "budget_krw", "bad"),
                                            ("계단 없어야 해", "requirement", "accessibility", "계단 없음")):
            result = interpret(self.envelope(message, [self.update(message, domain, field, value, strength="hard")]), message, self.located(), "t1")
            self.assertTrue(any(h["strength"] == "hard" for h in result["hypotheses"]))
        message = "공연 보고 싶어"
        result = interpret(self.envelope(message, [self.update(message, "condition", "budget_krw", "bad", strength="hard")]), message, self.located(), "t1")
        self.assertFalse(result["hypotheses"])


if __name__ == "__main__":
    unittest.main()
