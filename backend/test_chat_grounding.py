"""실제 모델 호출 없이 발화 근거와 시간 판단의 안전 경계를 검증한다."""
import unittest
from datetime import datetime

from chat_grounding import ground_payload
from outing import KST


class GroundingTests(unittest.TestCase):
    """명시되지 않은 조건이나 모호한 시간은 이전 조건을 바꾸지 않는다."""

    def check(self, message, changes, evidence, draft=None, history=None):
        """고정된 한국 기준 시각으로 해석 결과를 검증한다."""
        return ground_payload({"changes": changes, "evidence": evidence}, message, draft or {}, history or [],
                              now=datetime(2026, 11, 1, 10, 0, tzinfo=KST))

    def test_no_invented_place_and_literal_quote(self):
        """발화에 없는 장소 및 실제 발화에 없는 인용을 보류한다."""
        proposal = self.check("전시 보고 싶어요", {"start_query": "강남역", "category": "전시"},
                              {"start_query": "전시", "category": "전시"})
        self.assertEqual(proposal, {"category": "전시"})
        self.assertEqual(proposal.blocked_fields, ("start_query",))
        proposal = self.check("서울역에서 출발", {"start_query": "시청역"}, {"start_query": "서울역"})
        self.assertEqual(proposal, {})
        proposal = self.check("서울 역에서 출발", {"start_query": "서울역"}, {"start_query": "서울 역"})
        self.assertEqual(proposal, {"start_query": "서울역"})

    def test_explicit_date_and_time_verify_values(self):
        """오후 두 시와 날짜는 각각 실제 14시·내일과 일치해야 한다."""
        message = "내일 오후 두 시에 출발해요"
        for value, accepted in [("2026-11-02T14:00:00+09:00", True),
                                ("2026-11-02T16:00:00+09:00", False),
                                ("2026-11-03T14:00:00+09:00", False),
                                ("2026-11-02T14:00:00+00:00", False)]:
            with self.subTest(value=value):
                result = self.check(message, {"start_at": value}, {"start_at": "오후 두 시"})
                self.assertEqual(bool(result), accepted)

    def test_ambiguous_clock_and_choice_question(self):
        """질문에 오전과 오후가 모두 있어도 짧은 시간 답을 임의 확정하지 않는다."""
        for message, draft, history in [
            ("내일 3시요", {}, []),
            ("세 시요", {"date": "2026-11-02"}, [{"role": "assistant", "content": "오전 세 시인가요, 오후 세 시인가요?"}]),
        ]:
            with self.subTest(message=message):
                result = self.check(message, {"start_at": "2026-11-02T15:00:00+09:00"},
                                    {"start_at": message}, draft, history)
                self.assertEqual(result, {})
                self.assertEqual(result.blocked_fields, ("start_at",))

    def test_change_target_and_explicit_range(self):
        """바꿀 대상이 없으면 보류하고 명시된 시간 범위의 양끝을 각각 대조한다."""
        draft = {"start_at": "2026-11-02T14:00:00+09:00", "end_at": "2026-11-02T18:00:00+09:00"}
        result = self.check("오후 3시로 바꿔", {"start_at": "2026-11-02T15:00:00+09:00"},
                            {"start_at": "오후 3시"}, draft)
        self.assertEqual(result, {})
        message = "내일 오후 2시부터 오후 5시까지"
        changes = {"start_at": "2026-11-02T14:00:00+09:00", "end_at": "2026-11-02T17:00:00+09:00"}
        result = self.check(message, changes, {"start_at": message, "end_at": message})
        self.assertEqual(result, changes)
        swapped = {"start_at": changes["end_at"], "end_at": changes["start_at"]}
        result = self.check(message, swapped, {"start_at": message, "end_at": message})
        self.assertEqual(result, {})
        self.assertEqual(set(result.blocked_fields), set(swapped))

    def test_only_bad_time_is_blocked(self):
        """명확한 분류는 보존하면서 서로 다른 잘못된 시각만 보류한다."""
        message = "내일 오후 2시부터 오후 5시까지 전시"
        changes = {"start_at": "2026-11-02T14:00:00+09:00", "end_at": "2026-11-02T18:00:00+09:00", "category": "전시"}
        result = self.check(message, changes, {key: message for key in changes})
        self.assertEqual(result, {"start_at": changes["start_at"], "category": "전시"})
        self.assertEqual(result.blocked_fields, ("end_at",))

    def test_time_period_is_not_inherited_from_previous_clock(self):
        """오전 11시에서 1시로 가는 범위는 정오 전후가 불명확하다."""
        for message in ("내일 오전 11시부터 1시까지", "내일 오후 2시부터 5시까지"):
            result = self.check(message, {"end_at": "2026-11-02T13:00:00+09:00"}, {"end_at": message})
            self.assertEqual(result, {})
            self.assertEqual(result.blocked_fields, ("end_at",))

    def test_time_correction_is_held(self):
        """정정 문장에 시각이 여러 개면 최종 의도를 임의로 해석하지 않는다."""
        message = "내일 오후 2시 말고 오후 3시 출발"
        result = self.check(message, {"start_at": "2026-11-02T15:00:00+09:00"}, {"start_at": message})
        self.assertEqual(result, {})

    def test_negated_category_and_unrelated_time_quote(self):
        """명시적으로 거부한 분류와 시각이 빠진 인용은 수용하지 않는다."""
        result = self.check("전시 말고 국악", {"categories": ["전시"]}, {"categories": "전시 말고 국악"})
        self.assertEqual(result, {})
        result = self.check("전시 보고 싶어요", {"category": "국악"}, {"category": "전시"})
        self.assertEqual(result, {})
        result = self.check("클레식 듣고 싶어요", {"category": "클래식"}, {"category": "클레식"})
        self.assertEqual(result, {"category": "클래식"})
        result = self.check("내일 오후 2시 출발", {"start_at": "2026-11-02T14:00:00+09:00"},
                            {"start_at": "내일"})
        self.assertEqual(result, {})

    def test_draft_date_and_date_only_preserve_time(self):
        """초안 날짜와 명시된 시각, 날짜만 변경 시 기존 시각 보존을 허용한다."""
        proposal = self.check("오후 2시에 출발", {"start_at": "2026-11-02T14:00:00+09:00"},
                              {"start_at": "오후 2시"}, {"date": "2026-11-02"})
        self.assertEqual(len(proposal), 1)
        proposal = self.check("내일로 바꿔", {"start_at": "2026-11-02T14:00:00+09:00"},
                              {"start_at": "내일"}, {"start_at": "2026-11-01T14:00:00+09:00"})
        self.assertEqual(len(proposal), 1)
        proposal = self.check("내일로 바꿔", {"start_at": "2026-11-02T00:00:00+09:00"},
                              {"start_at": "내일"}, {"start_at": "2026-11-01T14:00:00+09:00"})
        self.assertEqual(proposal, {})

    def test_relative_and_unsupported_dates_are_held(self):
        """상대 지연이나 요일을 모델이 임의 시각으로 바꾸면 보류한다."""
        draft = {"start_at": "2026-11-02T14:00:00+09:00"}
        for message in ("15분 늦춰", "다음 주 월요일 오후 3시에 출발"):
            result = self.check(message, {"start_at": "2026-11-02T15:00:00+09:00"},
                                {"start_at": message}, draft)
            self.assertEqual(result, {})

    def test_malformed_envelope_and_unknown_field_fail(self):
        """상위 스키마 오류와 사실 필드는 실패로 처리한다."""
        for payload in ({"changes": {}, "evidence": {}, "other": 1},
                        {"changes": {"lat": 1}, "evidence": {"lat": "1"}}):
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                ground_payload(payload, "1", {}, [], datetime(2026, 11, 1, tzinfo=KST))


if __name__ == "__main__":
    unittest.main()
