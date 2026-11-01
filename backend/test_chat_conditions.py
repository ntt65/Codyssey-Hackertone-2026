"""실제 AI를 호출하지 않는 조건 병합 테스트. 동의·최신 입력·사실 경계를 검증한다."""
import unittest
from copy import deepcopy

from chat_conditions import apply_interpretation, resolve_changes


class ChatConditionTests(unittest.TestCase):
    """공급자와 프론트가 연결되기 전에 검증할 독립적인 대화 상태 사례다."""

    def setUp(self):
        """검증된 출발 좌표와 정확히 60분인 조건을 준비한다."""
        self.draft = dict(start_location=dict(label="청량리역", lat=37.5805961, lng=127.0482573),
                          start_at="2026-10-31T14:00:00+09:00", end_at="2026-10-31T15:00:00+09:00",
                          category="전시", request_kind="place")

    def apply(self, proposal, confirmed=None, draft=None, current_revision=2):
        """현재 입력의 revision 2에 대한 해석을 적용한다."""
        return apply_interpretation(self.draft if draft is None else draft, proposal,
                                    confirmed or [], 2, current_revision)

    def resolve(self, result, decisions):
        """초안이 변하지 않은 상태에서 사용자 동의/거절을 적용한다."""
        return resolve_changes(result, decisions, result["updated_condition_draft"], 2)

    def test_category_and_no_mutation(self):
        """국악 해석은 초안에만 반영하고 원본·최종 확인 경계를 유지한다."""
        original = deepcopy(self.draft)
        result = self.apply({"category": "국악"})
        self.assertEqual(result["updated_condition_draft"]["category"], "국악")
        self.assertTrue(result["ready_to_search"])
        self.assertTrue(result["requires_final_confirmation"])
        self.assertEqual(self.draft, original)

    def test_missing_question_and_no_default_origin(self):
        """비어 있는 입력에는 출발지 질문 하나와 전체 누락 항목을 반환한다."""
        result = self.apply({"category": "국악", "start_query": "서울역"}, draft={})
        self.assertNotIn("start_location", result["updated_condition_draft"])
        self.assertEqual(result["missing_fields"][0], "start_location")
        self.assertIn("어디에서", result["assistant_text"])
        self.assertFalse(result["ready_to_search"])

    def test_confirmed_accept_reject_and_pending(self):
        """확정 분류 변경은 수락/거절/미응답을 구분한다."""
        result = self.apply({"category": "국악"}, ["category"])
        self.assertEqual(result["updated_condition_draft"]["category"], "전시")
        self.assertFalse(result["ready_to_search"])
        accepted = self.resolve(result, {"category": True})
        rejected = self.resolve(result, {"category": False})
        self.assertEqual(accepted["updated_condition_draft"]["category"], "국악")
        self.assertEqual(rejected["updated_condition_draft"]["category"], "전시")
        self.assertTrue(rejected["ready_to_search"])
        self.assertFalse(self.resolve(result, {})["ready_to_search"])

    def test_changed_origin_invalidates_coordinates_only_on_accept(self):
        """새 출발지 동의 뒤 기존 좌표를 재사용하지 않으며 거절하면 보존한다."""
        result = self.apply({"start_query": "서울역"})
        self.assertIn("start_location", result["updated_condition_draft"])
        accepted = self.resolve(result, {"start_query": True})
        self.assertNotIn("start_location", accepted["updated_condition_draft"])
        self.assertIn("start_location", accepted["missing_fields"])
        self.assertIn("start_location", self.resolve(result, {"start_query": False})["updated_condition_draft"])

    def test_same_name_origin_still_requires_place_reselection(self):
        """시청처럼 같은 이름인 다른 장소도 재검색하며 동의 전에는 기존 좌표를 보존한다."""
        self.draft["start_location"] = dict(label="시청", lat=37.5665, lng=126.9780)
        original = deepcopy(self.draft)
        result = self.apply({"start_query": "시청"}, ["start_location"])
        self.assertEqual(result["conflicts"], [dict(field="start_query", before=original["start_location"], after="시청")])
        self.assertFalse(result["ready_to_search"])
        self.assertEqual(result["updated_condition_draft"], original)
        accepted = self.resolve(result, {"start_query": True})
        self.assertEqual(accepted["updated_condition_draft"]["start_query"], "시청")
        self.assertNotIn("start_location", accepted["updated_condition_draft"])
        self.assertEqual(self.resolve(result, {"start_query": False})["updated_condition_draft"], original)
        self.assertEqual(self.draft, original)

    def test_stale_response_and_manual_edit(self):
        """AI 응답/동의 대기 중 직접 수정된 현재값은 보존한다."""
        self.assertEqual(self.apply({"category": "국악"}, current_revision=3)["status"], "stale")
        result = self.apply({"category": "국악"}, ["category"])
        changed = deepcopy(self.draft)
        changed["category"] = "연극"
        self.assertEqual(resolve_changes(result, {"category": True}, changed, 2)["status"], "stale")
        self.assertEqual(resolve_changes(result, {}, self.draft, 3)["status"], "stale")

    def test_59_rejected_60_allowed(self):
        """최소60분 규칙은 기존 추천 서버 검증을 그대로 사용한다."""
        result = self.apply({"end_at": "2026-10-31T14:59:00+09:00"})
        self.assertEqual(result["field_errors"][0]["code"], "minimum_duration")
        self.assertFalse(result["ready_to_search"])
        self.assertTrue(self.apply({})["ready_to_search"])

    def test_course_requires_stay_and_alias(self):
        """route는 course로 정규화하고 체류시간을 임의 기본값으로 채우지 않는다."""
        result = self.apply({"request_kind": "route"})
        self.assertEqual(result["updated_condition_draft"]["request_kind"], "course")
        self.assertIn("stay_minutes", result["missing_fields"])
        self.assertTrue(self.apply({"request_kind": "course", "stay_minutes": 30})["ready_to_search"])

    def test_bad_or_factual_model_output_rejected(self):
        """좌표/행사 사실/비정상 형식은 해석 결과로 받지 않는다."""
        proposals = [{"start_location": self.draft["start_location"]}, {"price": 0},
                     {"category": []}, {"start_at": "내일"}, {"end_at": "2026-10-31T17:00:00"},
                     {"stay_minutes": True}, {"stay_minutes": 0}, {"start_query": " "},
                     {"request_kind": "unknown"}, {"start_query": "역\n"}]
        for proposal in proposals:
            with self.subTest(proposal=proposal), self.assertRaises(ValueError):
                self.apply(proposal)

    def test_null_no_change_and_timezone(self):
        """null은 삭제가 아니며 시각은 한국 시간으로 바꾼다."""
        result = self.apply({"category": None, "start_at": "2026-10-31T05:00:00+00:00"})
        self.assertEqual(result["updated_condition_draft"]["category"], "전시")
        self.assertEqual(result["updated_condition_draft"]["start_at"], self.draft["start_at"])

    def test_invalid_decisions_and_state(self):
        """문자열 동의·모르는 항목·비정상 revision을 거절한다."""
        result = self.apply({"category": "국악"}, ["category"])
        for decisions in [{"category": "yes"}, {"unknown": True}]:
            with self.assertRaises(ValueError):
                self.resolve(result, decisions)
        with self.assertRaises(ValueError):
            apply_interpretation({}, {}, [], True, 1)


if __name__ == "__main__":
    unittest.main()
