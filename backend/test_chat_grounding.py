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

    def test_departure_and_destination_are_distinct(self):
        """목적지와 출발지를 혼동하지 않고 짧은 출발지 답도 수용한다."""
        message = "서울역에서 출발해 시청에 가고 싶어요"
        self.assertEqual(self.check(message, {"start_query": "시청"}, {"start_query": "시청"}), {})
        self.assertEqual(self.check(message, {"start_query": "서울역"}, {"start_query": "서울역"}),
                         {"start_query": "서울역"})
        self.assertEqual(self.check("시청에 가고 싶어요", {"start_query": "시청"}, {"start_query": "시청"}), {})
        self.assertEqual(self.check("시청이요", {"start_query": "시청"}, {"start_query": "시청"}), {})
        self.assertEqual(self.check("시청이요", {"start_query": "시청"}, {"start_query": "시청"},
                                    history=[{"role": "assistant", "content": "어디에서 출발하세요?"}]),
                         {"start_query": "시청"})
        self.assertEqual(self.check("시청이요", {"start_query": "시청"}, {"start_query": "시청"},
                                    history=[{"role": "assistant", "content": "어디로 가고 싶으세요?"}]), {})

    def test_free_preference_requires_matching_intent(self):
        """무료 조건을 반대로 바꾸지 않고 명확한 해제를 처리한다."""
        for value, accepted in [(True, True), (False, False)]:
            result = self.check("무료만 보여줘", {"free_only": value}, {"free_only": "무료만"})
            self.assertEqual(bool(result), accepted)
        result = self.check("무료 전시 보고 싶어요", {"free_only": True}, {"free_only": "무료 전시"})
        self.assertEqual(result, {"free_only": True})
        result = self.check("무료 전시는 말고 유료 전시도 괜찮아요", {"free_only": True},
                            {"free_only": "무료 전시는 말고"})
        self.assertEqual(result, {})
        result = self.check("유료도 괜찮아요", {"free_only": False}, {"free_only": "유료도 괜찮아요"},
                            {"free_only": True})
        self.assertEqual(result, {"free_only": False})
        result = self.check("무료만 아니고 유료도 괜찮아요", {"free_only": True},
                            {"free_only": "무료만 아니고 유료도 괜찮아요"})
        self.assertEqual(result, {})
        result = self.check("상관없어요", {"free_only": False}, {"free_only": "상관없어요"},
                            {"free_only": True}, [{"role": "assistant", "content": "무료만 볼까요, 유료도 괜찮으세요?"}])
        self.assertEqual(result, {"free_only": False})

    def test_admission_budget_amount_and_scope(self):
        """관람료와 명시된 원화 금액이 일치해야 예산을 변경한다."""
        for value, accepted in [(10000, True), (100000, False)]:
            result = self.check("관람료 만원 이내", {"budget_krw": value}, {"budget_krw": "만원"})
            self.assertEqual(bool(result), accepted)
        result = self.check("입장료 10,000원 이내", {"budget_krw": 10000}, {"budget_krw": "10,000원"})
        self.assertEqual(result, {"budget_krw": 10000})
        result = self.check("총 예산 만원", {"budget_krw": 10000}, {"budget_krw": "만원"})
        self.assertEqual(result, {})
        result = self.check("관람료 제한 없어요", {"budget_krw": "any"}, {"budget_krw": "제한 없어요"})
        self.assertEqual(result, {"budget_krw": "any"})
        result = self.check("관람료 1만원에서 2만원 사이", {"budget_krw": 20000}, {"budget_krw": "2만원"})
        self.assertEqual(result, {})

    def test_required_conditions_not_silently_removed(self):
        """기존 필수조건을 보존하고 명시된 조건만 해제한다."""
        draft = {"unsupported_requirements": ["계단 없음"]}
        result = self.check("실내만 꼭 원해요", {"unsupported_requirements": []},
                            {"unsupported_requirements": "실내만"}, draft)
        self.assertEqual(result, {})
        result = self.check("실내만 꼭 원해요", {"unsupported_requirements": ["계단 없음", "실내만"]},
                            {"unsupported_requirements": "실내만"}, draft)
        self.assertEqual(result, {"unsupported_requirements": ["계단 없음", "실내만"]})
        result = self.check("계단 없음 조건 빼줘", {"unsupported_requirements": []},
                            {"unsupported_requirements": "계단 없음 조건 빼줘"}, draft)
        self.assertEqual(result, {"unsupported_requirements": []})
        result = self.check("계단 없음은 지키고 실내만 조건 빼줘", {"unsupported_requirements": []},
                            {"unsupported_requirements": "실내만 조건 빼줘"}, draft)
        self.assertEqual(result, {})
        result = self.check("실내만 싫어요", {"unsupported_requirements": ["실내만"]},
                            {"unsupported_requirements": "실내만 싫어요"})
        self.assertEqual(result, {})

    def test_night_twelve_does_not_become_noon(self):
        """밤 12시의 날짜 경계는 낮 12시로 자동 확정하지 않는다."""
        result = self.check("내일 밤 12시에 출발", {"start_at": "2026-11-02T12:00:00+09:00"},
                            {"start_at": "밤 12시"})
        self.assertEqual(result, {})
        self.assertEqual(result.blocked_fields, ("start_at",))
        result = self.check("내일 낮 12시에 출발", {"start_at": "2026-11-02T12:00:00+09:00"},
                            {"start_at": "낮 12시"})
        self.assertEqual(result, {"start_at": "2026-11-02T12:00:00+09:00"})

    def test_negation_cannot_invert_free_or_time(self):
        """부정된 무료·유료와 시각을 반대로 확정하지 않는다."""
        for message, changes, evidence in [
            ("무료만 보여주지 마", {"free_only": True}, {"free_only": "무료만"}),
            ("유료도 괜찮지 않아요", {"free_only": False}, {"free_only": "유료도 괜찮지 않아요"}),
            ("내일 오후 2시 출발은 안돼요", {"start_at": "2026-11-02T14:00:00+09:00"}, {"start_at": "오후 2시"}),
            ("내일 오후 2시에는 출발하지 말아주세요", {"start_at": "2026-11-02T14:00:00+09:00"}, {"start_at": "오후 2시"}),
        ]:
            with self.subTest(message=message):
                self.assertEqual(self.check(message, changes, evidence), {})
        self.assertEqual(self.check("내일 오후 2시 출발해요", {"start_at": "2026-11-02T14:00:00+09:00"},
                                    {"start_at": "오후 2시"}), {"start_at": "2026-11-02T14:00:00+09:00"})

    def test_rejected_departure_does_not_become_origin(self):
        """출발하지 않는 장소와 명시적으로 출발하는 장소를 구분한다."""
        message = "서울역에서 출발하지 말고 시청에서 출발해요"
        self.assertEqual(self.check(message, {"start_query": "서울역"}, {"start_query": "서울역"}), {})
        self.assertEqual(self.check(message, {"start_query": "시청"}, {"start_query": "시청"}), {"start_query": "시청"})

    def test_minimum_price_is_not_maximum_budget(self):
        """이상·초과 같은 하한을 관람료 상한으로 변환하지 않는다."""
        for message in ("관람료 만원 이상인 것만", "입장료 1만원 초과"):
            self.assertEqual(self.check(message, {"budget_krw": 10000}, {"budget_krw": "만원"}), {})
        self.assertEqual(self.check("관람료 만원 이내", {"budget_krw": 10000}, {"budget_krw": "만원"}),
                         {"budget_krw": 10000})

    def test_excluded_places_need_explicit_release(self):
        """제외 목록을 명시적 해제 없이 지우지 않고 항목별 해제는 보존한다."""
        draft = {"exclude_terms": ["시청", "강남"]}
        self.assertEqual(self.check("전시가 좋아요", {"exclude_terms": []}, {"exclude_terms": "전시"}, draft), {})
        self.assertEqual(self.check("시청은 제외하지 말아줘", {"exclude_terms": ["강남"]},
                                    {"exclude_terms": "시청은 제외하지 말아줘"}, draft), {"exclude_terms": ["강남"]})
        self.assertEqual(self.check("시청은 제외하지 말아줘", {"exclude_terms": []},
                                    {"exclude_terms": "시청은 제외하지 말아줘"}, draft), {})
        self.assertEqual(self.check("시청을 빼지 마", {"exclude_terms": ["강남"]},
                                    {"exclude_terms": "시청을 빼지 마"}, draft), {"exclude_terms": ["강남"]})
        self.assertEqual(self.check("강남도 빼줘", {"exclude_terms": ["시청", "강남"]},
                                    {"exclude_terms": "강남도 빼줘"}, {"exclude_terms": ["시청"]}),
                         {"exclude_terms": ["시청", "강남"]})

    def test_required_condition_negated_release_is_not_release(self):
        """필수조건을 빼지 말라는 발화는 조건 해제가 아니다."""
        draft = {"unsupported_requirements": ["계단 없음"]}
        for message in ("계단 없음 조건 빼지 마", "계단 없음 조건 해제하지 마", "계단 없음 조건은 필요없지 않아"):
            with self.subTest(message=message):
                self.assertEqual(self.check(message, {"unsupported_requirements": []},
                                            {"unsupported_requirements": message}, draft), {})

    def test_free_inflected_negation_and_allowed_paid_options(self):
        """무료의 활용형 부정과 유료 허용을 구분하고 정상 무료 요청은 유지한다."""
        for message in ("무료만 아닌 유료도 괜찮아요", "무료만은 아닙니다", "무료만은 아니에요",
                        "무료만 보여줘, 유료도 괜찮아요"):
            with self.subTest(message=message):
                self.assertEqual(self.check(message, {"free_only": True}, {"free_only": message}), {})
        for message in ("무료만 아닌 유료도 괜찮아요", "유료도 괜찮아요", "무료 제한 해제해줘"):
            with self.subTest(message=message):
                self.assertEqual(self.check(message, {"free_only": False}, {"free_only": message}), {"free_only": False})
        for message in ("무료만 보여줘", "무료 공연만 찾아줘", "돈 안 드는 전시"):
            with self.subTest(message=message):
                self.assertEqual(self.check(message, {"free_only": True}, {"free_only": message}), {"free_only": True})
        for value in (True, False):
            self.assertEqual(self.check("무료만은 아닌 게 아니에요", {"free_only": value},
                                        {"free_only": "무료만은 아닌 게 아니에요"}), {})

    def test_departure_prohibition_correction_and_short_answer(self):
        """출발 금지의 활용형·짧은 부정 답변을 막고 정정된 출발지는 수용한다."""
        history = [{"role": "assistant", "content": "어디에서 출발하세요?"}]
        for message in ("서울역에서 출발하면 안 돼요", "서울역에서 출발해서는 안 돼요",
                        "서울역에서는 출발 못해요", "서울역은 아니에요"):
            with self.subTest(message=message):
                self.assertEqual(self.check(message, {"start_query": "서울역"}, {"start_query": "서울역"}, history=history), {})
        message = "서울역에서 출발하면 안 돼요. 시청에서 출발해요"
        self.assertEqual(self.check(message, {"start_query": "시청"}, {"start_query": "시청"}), {"start_query": "시청"})
        self.assertEqual(self.check("출발지는 시청으로 바꿔줘", {"start_query": "시청"}, {"start_query": "시청"}),
                         {"start_query": "시청"})

    def test_keywords_keep_unmentioned_preferences_and_explicit_clear(self):
        """무관한 답변은 기존 관심어를 지우지 않고 개별 정정과 전체 해제는 허용한다."""
        draft = {"keywords": ["미술", "사진"]}
        for message in ("전시 좋아", "미술은 빼지 마", "미술을 빼면 안 돼", "관심어 전부 지우지 마", "관심어 전부 빼면 안 돼"):
            with self.subTest(message=message):
                self.assertEqual(self.check(message, {"keywords": []}, {"keywords": message}, draft), {})
        self.assertEqual(self.check("전시 좋아", {"keywords": ["미술", "사진", "전시"]}, {"keywords": "전시"}, draft),
                         {"keywords": ["미술", "사진", "전시"]})
        for message in ("미술은 빼줘", "미술 말고 사진", "미술 키워드 삭제해줘"):
            with self.subTest(message=message):
                self.assertEqual(self.check(message, {"keywords": ["사진"]}, {"keywords": message}, draft), {"keywords": ["사진"]})
        self.assertEqual(self.check("관심어 전부 지워줘", {"keywords": []}, {"keywords": "관심어 전부 지워줘"}, draft), {"keywords": []})
        self.assertEqual(self.check("사진은 싫어요", {"keywords": ["사진"]}, {"keywords": "사진"}), {})
        result = self.check("전시 좋아", {"category": "전시", "keywords": []},
                            {"category": "전시", "keywords": "전시"})
        self.assertEqual(result, {"category": "전시"})
        self.assertEqual(result.blocked_fields, ())

    def test_indoor_outdoor_opposites_corrections_and_release(self):
        """반대 실내외 값과 의미 없는 해제는 막고 명시 선호·정정·해제를 수용한다."""
        cases = [("실외가 좋아요", "outdoor"), ("야외 행사 원해요", "outdoor"),
                 ("실내가 좋아요", "indoor"), ("실내 말고 실외", "outdoor"),
                 ("야외는 싫고 실내로", "indoor"), ("실내는 안 좋아요, 실외로", "outdoor"),
                 ("야외는 별로예요. 실내가 좋아요", "indoor"), ("실내는 좋지 않아요. 실외로", "outdoor"),
                 ("실외는 안 원해요. 실내로", "indoor")]
        for message, expected in cases:
            for value in ("indoor", "outdoor", "any"):
                with self.subTest(message=message, value=value):
                    result = self.check(message, {"indoor_outdoor": value}, {"indoor_outdoor": message})
                    self.assertEqual(result, {"indoor_outdoor": value} if value == expected else {})
        self.assertEqual(self.check("실내외 상관없어요", {"indoor_outdoor": "any"}, {"indoor_outdoor": "실내외 상관없어요"}),
                         {"indoor_outdoor": "any"})
        self.assertEqual(self.check("상관없어요", {"indoor_outdoor": "any"}, {"indoor_outdoor": "상관없어요"},
                                    history=[{"role": "assistant", "content": "실내와 야외 중 어디가 좋으세요?"}]), {"indoor_outdoor": "any"})
        self.assertEqual(self.check("상관없어요", {"indoor_outdoor": "any"}, {"indoor_outdoor": "상관없어요"}), {})
        for message in ("실내가 싫지는 않아요", "실내는 안 싫어요"):
            self.assertEqual(self.check(message, {"indoor_outdoor": "indoor"}, {"indoor_outdoor": message}), {})
        self.assertEqual(self.check("실내는 상관없지만 야외는 싫어요", {"indoor_outdoor": "any"},
                                    {"indoor_outdoor": "실내는 상관없지만 야외는 싫어요"}), {})

    def test_exclusion_addition_needs_exclusion_not_just_mention(self):
        """제외 금지나 평범한 장소 언급으로 새 제외를 만들지 않는다."""
        for message in ("시청은 빼지 말아줘", "시청을 제외하지 마", "시청이 좋아요", "시청 제외 해제해줘",
                        "시청을 빼면 안 돼", "시청을 제외하면 안 돼"):
            with self.subTest(message=message):
                self.assertEqual(self.check(message, {"exclude_terms": ["시청"]}, {"exclude_terms": message}), {})
        for message in ("시청은 빼줘", "시청 제외해줘", "시청 말고", "시청은 싫어요"):
            with self.subTest(message=message):
                self.assertEqual(self.check(message, {"exclude_terms": ["시청"]}, {"exclude_terms": message}), {"exclude_terms": ["시청"]})
        draft = {"exclude_terms": ["시청"]}
        self.assertEqual(self.check("시청은 제외 해제하지 마", {"exclude_terms": []}, {"exclude_terms": "시청은 제외 해제하지 마"}, draft), {})

    def test_music_group_rejection_does_not_become_music_categories(self):
        """음악 전체의 거절을 국악·클래식·콘서트 선호로 바꾸지 않는다."""
        for message in ("음악은 싫어요", "음악 말고 전시", "음악은 듣고 싶지 않아요", "음악은 빼줘"):
            for category in ("국악", "클래식", "콘서트", "전체"):
                with self.subTest(message=message, category=category):
                    self.assertEqual(self.check(message, {"categories": [category]}, {"categories": message}), {})
        self.assertEqual(self.check("음악 말고 전시", {"category": "전시"}, {"category": "전시"}), {"category": "전시"})
        self.assertEqual(self.check("클래식 말고 국악", {"category": "국악"}, {"category": "국악"}), {"category": "국악"})
        self.assertEqual(self.check("음악 듣고 싶어요", {"categories": ["국악", "클래식", "콘서트"], "music_followup": True},
                                    {"categories": "음악", "music_followup": "음악"}),
                         {"categories": ["국악", "클래식", "콘서트"], "music_followup": True})
        self.assertEqual(self.check("음악은 싫어요", {"music_followup": True}, {"music_followup": "음악"}), {})

    def test_place_and_course_counts_cannot_be_inverted(self):
        """한 곳과 코스를 뒤집지 않고 명확한 정정과 질문 뒤의 짧은 답변은 수용한다."""
        cases = [("한 곳만", "place"), ("행사 하나 찾아줘", "place"),
                 ("두 군데 코스", "course"), ("여러 곳 둘러볼래", "course"),
                 ("코스 말고 한 곳", "place"), ("한 곳 말고 두 곳", "course")]
        for message, expected in cases:
            for value in ("place", "course", "route"):
                with self.subTest(message=message, value=value):
                    result = self.check(message, {"request_kind": value}, {"request_kind": message})
                    self.assertEqual(result, {"request_kind": value} if ("course" if value == "route" else value) == expected else {})
        self.assertEqual(self.check("하나요", {"request_kind": "place"}, {"request_kind": "하나요"},
                                    history=[{"role": "assistant", "content": "한 곳을 찾을까요, 두 곳 코스가 좋으세요?"}]), {"request_kind": "place"})
        self.assertEqual(self.check("하나요", {"request_kind": "place"}, {"request_kind": "하나요"}), {})


if __name__ == "__main__":
    unittest.main()
