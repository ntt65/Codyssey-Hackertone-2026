"""v3 탐색의 실제 공급자 형태·조건 적용·근거 정렬·미확인/장애 경계를 오프라인 재현한다."""
from copy import deepcopy
from datetime import datetime
import json
import unittest
from unittest.mock import patch

from exploration import explore
from outing import EXAMPLES, KST, InputError


class FixedDatetime(datetime):
    """기간 평가의 시스템 기준일을 고정한다. 사용자의 방문일을 대신하지 않는다."""

    @classmethod
    def now(cls, tz=None):
        """2026-11-01 한국 시각을 반환한다."""
        return cls(2026, 11, 1, 12, 0, tzinfo=KST).astimezone(tz or KST)


class ExplorationTests(unittest.TestCase):
    """추천의 필수 일정 없이 콘텐츠를 찾되 hard 조건과 source 사실 경계를 유지한다."""

    def setUp(self):
        """저장된 실제 공급자 필드 형태를 복사하고 평가용 내용·ID를 명시적으로 구성한다."""
        self.base = json.loads((EXAMPLES / "seoul-events.capture.json").read_bytes())["captures"][0]["rows"][0]
        self.base.update(STRTDATE="2026-11-01 00:00:00", END_DATE="2026-12-31 00:00:00",
                         LAT="37.566", LOT="126.978", CODENAME="콘서트", PRO_TIME="14:00",
                         IS_FREE="무료", USE_FEE="0원")
        self.calm = dict(self.base, TITLE="피아노 음악회", PROGRAM="잔잔한 선율의 피아노 연주",
                         HMPG_ADDR="https://culture.seoul.go.kr/event?cultcode=101")
        self.lively = dict(self.base, TITLE="리듬 음악회", PROGRAM="신나는 리듬과 활기찬 합주",
                           HMPG_ADDR="https://culture.seoul.go.kr/event?cultcode=102")
        self.state = dict(revision=4, understanding=dict(goal="공연을 보고 싶어", service="performance", preferences=[]),
                          conditions=dict(start_location=dict(label="서울시청", lat=37.5663, lng=126.9779)), hypotheses=[])
        self.clock = patch("exploration.datetime", FixedDatetime)
        self.clock.start()
        self.addCleanup(self.clock.stop)

    def source(self, rows):
        """네트워크 없이 원본 공급자의 (rows, checked_at, total) 계약을 재현한다."""
        return patch("exploration.outing.seoul_page", return_value=(rows, "2026-11-01T12:00:00+09:00", len(rows)))

    def preference(self, value, **extra):
        """실제 의미 모듈의 명시 선호 계약을 만든다."""
        return dict(id="pref-1", dimension="atmosphere", value=value, polarity="prefer", strength="soft",
                    source="user_explicit", evidence=dict(turn_id="turn-1", quote="잔잔한 음악"), scope="performance", **extra)

    def walk_state(self):
        """문화행사 fixture와 격리된 산책 목적·검증 원점을 준비한다."""
        state = deepcopy(self.state)
        state["understanding"].update(goal="산책", service="walk", preferences=[])
        return state

    def walk_place(self, identity, label, category, *, lat=37.57, group="AT4"):
        """실제 공개 장소가 아닌 합성 카카오 정규화 후보를 만든다."""
        return dict(id="kakao:keyword:" + identity, label=label, category_name=category,
                    category_group_code=group, category_group_name=None, lat=lat, lng=126.978,
                    address="평가용 주소", official_url="https://place.map.kakao.com/" + identity)

    def venue_source(self, items):
        """실카카오 호출 없이 기존 거리순 첫5건 경계의 반환만 고정한다."""
        return patch("exploration.places.search_places", return_value=(200, dict(
            status="ready" if items else "no_results", places=items, source_total=len(items),
            source_checked_at="2026-11-01T12:00:00+09:00")))

    def test_walk_nearby_amenities_cannot_outrank_two_real_destinations(self):
        """거리·관심어 점수가 높은 화장실/주차장/관리소를 빼고 정상 공원2건만 반환한다."""
        state = self.walk_state()
        state["conditions"]["keywords"] = ["화장실"]
        items = [self.walk_place("1", "평가용 공원 화장실", "가정,생활 > 공공시설 > 화장실", lat=37.5663),
                 self.walk_place("2", "평가용 공원 주차장", "교통,수송 > 주차장", lat=37.5664, group="PK6"),
                 self.walk_place("3", "평가용 관리사무소", "여행 > 공원 > 관리사무소", lat=37.5665),
                 self.walk_place("4", "평가용 동쪽 공원", "여행 > 관광,명소 > 공원", lat=37.58),
                 self.walk_place("5", "평가용 서쪽 공원", "여행 > 관광,명소 > 공원 > 도시근린공원", lat=37.57)]
        with self.venue_source(items) as source:
            result = explore(state)
        self.assertEqual([item["id"] for item in result["candidates"]], [items[4]["id"], items[3]["id"]])
        self.assertEqual(result["excluded_counts"]["walk_amenity"], 3)
        self.assertEqual(result["eligibility"]["eligible_count"], 2)
        self.assertEqual(result["eligibility"]["checked_count"], 5)
        self.assertEqual(source.call_count, 1)
        self.assertEqual(source.call_args.args[0]["query"], "공원")
        self.assertEqual(source.call_args.args[0]["origin"], dict(lat=37.5663, lng=126.9779))
        self.assertIn("조회한 5건", result["coverage_note"])
        self.assertIn("추가 페이지 미조회", result["coverage_note"])
        self.assertIn("상세분류", result["applied"][0]["basis"])

    def test_walk_name_does_not_override_primary_or_amenity_category(self):
        """정상 공원 명칭의 화장실 단어는 허용하고 이름만 공원인 부대시설은 제외한다."""
        main = self.walk_place("1", "화장실 이용 가능한 평가용 공원", "여행 > 관광,명소 > 공원")
        amenity = self.walk_place("2", "평가용 행복공원", "여행 > 관광,명소 > 공원 > 화장실", lat=37.5663)
        original = deepcopy(main)
        with self.venue_source([amenity, main]):
            result = explore(self.walk_state())
        self.assertEqual([item["id"] for item in result["candidates"]], [main["id"]])
        candidate = result["candidates"][0]
        self.assertEqual((candidate["title"], candidate["lat"], candidate["lng"]), (main["label"], main["lat"], main["lng"]))
        self.assertEqual(candidate["eligibility"]["category_path"], ["여행", "관광,명소", "공원"])
        self.assertEqual(main, original)

    def test_walk_broad_group_and_missing_categories_never_claim_matching(self):
        """관광명소AT4·공원 이름만으로 승인하지 않고 결측/다른용도를 역할별 집계한다."""
        items = [self.walk_place("1", "평가용 공원", None),
                 self.walk_place("2", "평가용 공원", ""),
                 self.walk_place("3", "평가용 공원", "여행 > 관광,명소"),
                 self.walk_place("4", "평가용 공원 카페", "음식점 > 카페", group="CE7")]
        with self.venue_source(items):
            result = explore(self.walk_state())
        self.assertEqual(result["candidates"], [])
        self.assertEqual(result["excluded_counts"]["walk_unverified"], 3)
        self.assertEqual(result["excluded_counts"]["walk_incompatible"], 1)
        self.assertEqual(result["eligibility"]["eligible_count"], 0)
        self.assertIn("walk_destination", result["unknown"])
        self.assertTrue(any(item["field"] == "walk_destination" for item in result["not_applied"]))
        self.assertIn("분류 미확인 3건 제외", result["coverage_note"])

    def test_walk_all_amenities_returns_zero_without_inventing_parent_park(self):
        """부대시설뿐이면 부모 공원 ID/좌표를 만들거나 결과 개수를 채우지 않는다."""
        items = [self.walk_place("1", "평가용 공원 화장실", "공공시설 > 공중화장실"),
                 self.walk_place("2", "평가용 공원 주차장", "교통시설 > 주차장", group="PK6"),
                 self.walk_place("3", "평가용 공원 관리소", "공원 > 관리소")]
        with self.venue_source(items) as source:
            result = explore(self.walk_state())
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["candidates"], [])
        self.assertEqual(result["excluded_counts"]["walk_amenity"], 3)
        self.assertEqual(source.call_count, 1)
        self.assertIn("조회한 3건", result["coverage_note"])
        self.assertNotIn("근처에 공원이 없", result["coverage_note"])

    def test_walk_pk6_conflict_is_not_rescued_by_park_category(self):
        """상세분류가공원이어도 실제주차장그룹과충돌하면 주 목적지로 승인하지 않는다."""
        parking = self.walk_place("1", "평가용 공원", "여행 > 공원", group="PK6")
        main = self.walk_place("2", "평가용 공원", "여행 > 공원")
        with self.venue_source([parking, main]):
            result = explore(self.walk_state())
        self.assertEqual([item["id"] for item in result["candidates"]], [main["id"]])
        self.assertEqual(result["excluded_counts"]["walk_amenity"], 1)
        self.assertEqual(result["candidates"][0]["category_group_code"], "AT4")

    def test_walk_eligibility_does_not_relax_price_or_unverified_hard_requirement(self):
        """공원 적합성 통과 뒤에도 확인되지 않은 무료필수조건과 실제 hard 보류를 유지한다."""
        state = self.walk_state()
        state["conditions"]["free_only"] = True
        main = self.walk_place("1", "평가용 공원", "여행 > 공원")
        with self.venue_source([main]):
            result = explore(state)
        self.assertEqual(result["eligibility"]["eligible_count"], 1)
        self.assertEqual(result["candidates"], [])
        self.assertIn("price", result["unknown"])
        self.assertTrue(state["conditions"]["free_only"])
        state["hypotheses"] = [dict(strength="hard", status="unresolved", value="계단 없음", blocking_scope=["explore"])]
        with self.venue_source([main]) as source:
            blocked = explore(state)
        self.assertTrue(blocked["blocked"])
        source.assert_not_called()

    def test_walk_filter_does_not_change_movie_cafe_or_food_behavior(self):
        """이번 산책 판정은 기존 영화관/카페/식사 조회와 원 ID·좌표를 바꾸지 않는다."""
        for service, category, group in [("movie", "문화,예술 > 영화관", "CT1"),
                                          ("cafe", "음식점 > 카페", "CE7"), ("food", "음식점", "FD6")]:
            state = self.walk_state()
            state["understanding"]["service"] = service
            place = self.walk_place("1", "평가용 장소", category, group=group)
            with self.subTest(service=service), self.venue_source([place]):
                result = explore(state)
            self.assertEqual([item["id"] for item in result["candidates"]], [place["id"]])
            self.assertNotIn("eligibility", result)
            self.assertEqual(result["candidates"][0]["lat"], place["lat"])
            self.assertIn("keyword 조회", result["applied"][0]["basis"])
            self.assertIn("추가 검증 없음", result["applied"][0]["basis"])

    def test_explicit_closer_sort_uses_actual_distance_before_semantic_preference(self):
        """더 가까운 곳은 직선거리를 우선하며 기존 무료조건·취향과 사실 근거를 보존한다."""
        from dialogue_memory import apply_event, new_state
        state = new_state()
        state.update(self.state)
        state["conditions"] = dict(state["conditions"], free_only=True)
        state["understanding"]["preferences"] = [self.preference("calm")]
        state = apply_event(state, {"type": "proceed", "sort": "distance"})
        far = dict(self.calm, LAT="37.70", LOT="127.10")
        near = dict(self.lively, LAT="37.5663", LOT="126.978")
        with self.source([far, near]):
            result = explore(state, ranker=lambda rows, prefs: {
                "seoul:101": {"score": 1, "evidence": [{"field": "description", "quote": far["PROGRAM"]}]}})
        self.assertTrue(state["conditions"]["free_only"])
        self.assertEqual(result["candidates"][0]["id"], "seoul:102")
        self.assertLess(result["candidates"][0]["distance_km"], result["candidates"][1]["distance_km"])

    def test_restored_hard_preference_is_not_downgraded_to_soft(self):
        """복원 뒤에도 검증할 수 없는 필수 취향은 유지하며 조회로 조용히 우회하지 않는다."""
        from dialogue_memory import apply_event, new_state
        snapshot = new_state()
        snapshot["understanding"]["service"] = "performance"
        snapshot["understanding"]["preferences"] = [dict(self.preference("calm"), strength="hard")]
        restored = apply_event(new_state(), {"type": "restore", "snapshot": snapshot})
        self.assertEqual(restored["understanding"]["preferences"][0]["strength"], "hard")
        restored["conditions"] = self.state["conditions"]
        with self.source([self.calm]) as source:
            result = explore(restored)
        self.assertTrue(result["blocked"])
        source.assert_not_called()

    def test_no_required_date_or_fabricated_window(self):
        """종료시각·장르 없이 진행/예정 콘텐츠를 찾고 오늘 방문 시간창을 만들지 않는다."""
        original = deepcopy(self.state)
        expired = dict(self.calm, END_DATE="2026-10-31", STRTDATE="2026-10-01",
                       HMPG_ADDR="https://culture.seoul.go.kr/event?cultcode=103")
        future = dict(self.lively, STRTDATE="2026-12-01")
        with self.source([self.calm, expired, future]), patch("outing.validate") as validation:
            result = explore(self.state)
        validation.assert_not_called()
        self.assertEqual([c["id"] for c in result["candidates"]], ["seoul:101", "seoul:102"])
        self.assertEqual(result["excluded_counts"]["expired"], 1)
        self.assertIsNone(result["range"]["date_from"])
        self.assertFalse(result["range"]["visit_window_created"])
        self.assertEqual(self.state, original)
        self.assertTrue(all(c["visit_status"] == "not_checked" and c["visit_validation_context"] is None for c in result["candidates"]))
        self.assertEqual(result["candidates"][0]["result_context"]["conditions"], original["conditions"])

    def test_performance_does_not_substitute_exhibition_or_venue(self):
        """공연 요청은 실제 공연 행사만 반환하고 전시/시설로 성공을 가장하지 않는다."""
        exhibit = dict(self.calm, CODENAME="전시/미술")
        with self.source([exhibit, self.lively]) as source, patch("exploration.places.search_places") as venue:
            result = explore(self.state)
        self.assertEqual(source.call_args.args[1], "전체")
        venue.assert_not_called()
        self.assertEqual([c["id"] for c in result["candidates"]], ["seoul:102"])

    def test_calm_lively_change_order_with_actual_description_evidence(self):
        """서로 구분되는 실제 소개 근거가 있으면 분위기 변경이 같은 후보의 순서를 바꾼다."""
        def ranker(candidates, prefs):
            """명시 fixture 원문의 분위기를 비교하는 독립 모의 의미 판정기다."""
            target = "잔잔한" if prefs[0]["value"] == "calm" else "신나는"
            return {c["id"]: dict(score=1 if target in c["description"] else -1,
                                  evidence=[dict(field="description", quote=c["description"])]) for c in candidates}
        self.state["understanding"]["preferences"] = [self.preference("calm")]
        with self.source([self.calm, self.lively]):
            calm = explore(self.state, ranker=ranker)
        self.state["understanding"]["preferences"][0]["value"] = "lively"
        with self.source([self.calm, self.lively]):
            lively = explore(self.state, ranker=ranker)
        self.assertEqual(calm["candidates"][0]["id"], "seoul:101")
        self.assertEqual(lively["candidates"][0]["id"], "seoul:102")
        self.assertEqual(calm["ranking"]["status"], "applied")
        self.assertNotEqual(calm["result_context"]["execution_key"], lively["result_context"]["execution_key"])
        self.assertEqual(calm["candidates"][0]["genre"], "콘서트")

    def test_unverified_quote_id_and_mutation_cannot_change_facts(self):
        """존재하지 않는 인용·후보 ID를 무시하고 ranker의 객체 수정도 원본 사실에 반영하지 않는다."""
        def ranker(candidates, prefs):
            """의도적으로 사실 변조와 없는 인용을 시도하는 판정기다."""
            candidates[0]["price_info"] = "무료"
            return {"seoul:101": dict(score=1, evidence=[dict(field="description", quote="존재하지 않는 문장")]),
                    "made-up": dict(score=1, evidence=[dict(field="title", quote="허구")])}
        self.state["understanding"]["preferences"] = [self.preference("calm")]
        with self.source([self.calm]):
            result = explore(self.state, ranker=ranker)
        self.assertEqual(result["ranking"]["status"], "unknown")
        self.assertEqual(result["candidates"][0]["price_info"], "0원")
        self.assertIsNone(result["candidates"][0]["semantic_score"])

    def test_missing_ranking_or_error_keeps_facts_without_match_claim(self):
        """분위기 근거 판정이 없거나 실패해도 실제 콘텐츠는 보존하고 맞춤 성공을 주장하지 않는다."""
        self.state["understanding"]["preferences"] = [self.preference("calm")]
        with self.source([self.calm]):
            result = explore(self.state)
        self.assertEqual(result["ranking"]["status"], "unavailable")
        self.assertEqual(result["not_applied"][0]["field"], "semantic_preferences")
        with self.source([self.calm]):
            failed = explore(self.state, ranker=lambda *_: (_ for _ in ()).throw(TimeoutError()))
        self.assertEqual(failed["status"], "ok")
        self.assertEqual(failed["ranking"]["status"], "source_error")
        self.assertEqual(len(failed["candidates"]), 1)

    def test_hard_price_and_negation_do_not_relax_for_zero(self):
        """무료만·국악 제외는 실제 요금과 분류로 적용하며 미확인/유료를 복원하지 않는다."""
        rows = [self.calm, dict(self.lively, IS_FREE="유료", USE_FEE="20,000원"),
                dict(self.calm, HMPG_ADDR="https://culture.seoul.go.kr/event?cultcode=103", IS_FREE="", USE_FEE=""),
                dict(self.calm, HMPG_ADDR="https://culture.seoul.go.kr/event?cultcode=104", CODENAME="국악")]
        self.state["conditions"].update(free_only=True, exclude_terms=["국악"])
        with self.source(rows):
            result = explore(self.state)
        self.assertEqual([c["id"] for c in result["candidates"]], ["seoul:101"])
        self.assertEqual(result["excluded_counts"]["price"], 1)
        self.assertEqual(result["excluded_counts"]["exclusion"], 1)
        self.assertIn("price", result["unknown"])
        self.state["conditions"]["exclude_terms"].append("피아노")
        with self.source(rows):
            self.assertEqual(explore(self.state)["candidates"], [])

    def test_contradictory_free_and_partial_fee_is_unknown(self):
        """공식 무료 태그가 있어도 일부유료·복수요금 설명과 충돌하면 hard 무료로 통과하지 않는다."""
        self.state["conditions"]["free_only"] = True
        for price in ("무료(일부 유료)", "10,000원", "재료비 별도"):
            with self.subTest(price=price), self.source([dict(self.calm, USE_FEE=price)]):
                result = explore(self.state)
            self.assertEqual(result["candidates"], [])
            self.assertIn("price", result["unknown"])

    def test_unresolved_hard_requirement_prevents_source(self):
        """검증 불가 필수 제약은 source 조회 전 차단하고 입력을 지우지 않는다."""
        self.state["hypotheses"] = [dict(kind="requirement", strength="hard", status="unresolved", value="계단 없는 곳만", blocking_scope=["explore"])]
        with patch("exploration.outing.seoul_page") as source:
            result = explore(self.state)
        source.assert_not_called()
        self.assertTrue(result["blocked"])
        self.assertEqual(result["unknown"], ["hard_requirement"])

    def test_structured_hard_genre_exclusion_is_not_blocked_twice(self):
        """실제 exclude_terms에 연결된 장르 제외는 unsupported로 중복 보류하지 않는다."""
        self.state["understanding"]["preferences"] = [dict(id="p", dimension="genre", value="국악", polarity="avoid", strength="hard")]
        self.state["conditions"]["exclude_terms"] = ["국악"]
        with self.source([dict(self.calm, CODENAME="국악"), self.lively]):
            result = explore(self.state)
        self.assertNotIn("blocked", result)
        self.assertEqual([c["id"] for c in result["candidates"]], ["seoul:102"])

    def test_selected_date_and_short_window_are_filters_not_visit_approval(self):
        """명시한 30분 구간도 탐색 필터로만 쓰며 60분 방문계획이나 방문검증으로 승격하지 않는다."""
        self.state["conditions"].update(date="2026-11-02", start_at="2026-11-02T14:00:00+09:00", end_at="2026-11-02T14:30:00+09:00")
        missing_time = dict(self.lively, PRO_TIME="회차별 다름")
        with self.source([self.calm, missing_time]):
            result = explore(self.state)
        self.assertEqual([c["id"] for c in result["candidates"]], ["seoul:101"])
        self.assertIn("time", result["unknown"])
        self.assertEqual(result["candidates"][0]["visit_status"], "not_checked")

    def test_source_zero_and_source_error_are_distinct(self):
        """정상 공급자 0건과 장애를 구분하고 다른 종류의 시설을 몰래 반환하지 않는다."""
        with self.source([]):
            empty = explore(self.state)
        with patch("exploration.outing.seoul_page", side_effect=OSError("offline")):
            failed = explore(self.state)
        self.assertEqual((empty["status"], empty["candidates"]), ("ok", []))
        self.assertEqual(failed["status"], "source_error")
        self.assertEqual(failed["candidates"], [])

    def test_movie_venue_cannot_claim_showtimes_or_taste_match(self):
        """실제 영화관 위치·직선거리만 표시하고 작품 취향 정렬 callback을 호출하지 않는다."""
        self.state["understanding"].update(service="movie", preferences=[self.preference("calm")])
        self.state["understanding"]["preferences"][0]["scope"] = "movie"
        place = dict(id="kakao:keyword:123", label="실제 형태의 영화관", lat=37.56, lng=126.98,
                     address="서울 중구", road_address="서울 중구 테스트로 1", official_url="https://place.map.kakao.com/123", category_name="영화관")
        with patch("exploration.places.search_places", return_value=(200, dict(status="ready", places=[place], source_total=1))) as source:
            ranker = unittest.mock.Mock()
            result = explore(self.state, ranker=ranker)
        ranker.assert_not_called()
        self.assertEqual(source.call_args.args[0]["origin"], dict(lat=37.5663, lng=126.9779))
        candidate = result["candidates"][0]
        self.assertEqual(candidate["result_kind"], "venue_exploration")
        self.assertIsNone(candidate["opening_info"])
        self.assertIsNone(candidate["price_info"])
        self.assertEqual(result["ranking"]["status"], "unsupported_source")
        self.assertIn("상영표", result["coverage_note"])

    def test_movie_unknown_hard_price_or_date_cannot_pass(self):
        """영화관 자료로 알 수 없는 요금·영업일을 필수 조건 충족으로 간주하지 않는다."""
        self.state["understanding"]["service"] = "movie"
        self.state["conditions"]["free_only"] = True
        place = dict(id="kakao:keyword:123", label="영화관", lat=37.56, lng=126.98)
        with patch("exploration.places.search_places", return_value=(200, dict(status="ready", places=[place]))):
            result = explore(self.state)
        self.assertEqual(result["candidates"], [])
        self.assertIn("price", result["unknown"])

    def test_invalid_user_coordinate_and_date_are_not_provider_zero(self):
        """잘못된 사용자 좌표/날짜는 InputError로 식별하고 source 조회 전에 중단한다."""
        self.state["conditions"]["start_location"]["lat"] = True
        with self.assertRaises(InputError), patch("exploration.outing.seoul_page") as source:
            explore(self.state)
        source.assert_not_called()
        self.state["conditions"]["start_location"]["lat"] = 37.56
        self.state["conditions"]["date"] = "2026-02-30"
        with self.assertRaises(InputError):
            explore(self.state)

    def test_other_service_hard_preference_does_not_block_current_goal(self):
        """다른 서비스에 종속된 hard 취향은 현재 공연 탐색을 전역 차단하지 않는다."""
        self.state["understanding"]["preferences"] = [dict(id="p", dimension="atmosphere", value="quiet", strength="hard", scope="cafe")]
        with self.source([self.calm]):
            result = explore(self.state)
        self.assertNotIn("blocked", result)
        self.assertEqual(len(result["candidates"]), 1)

    def test_zero_budget_is_applied_and_ranker_receives_source_hash(self):
        """0원 예산도 명시 필터로 기록하고 의미 판정에 실제 출처 hash를 함께 제공한다."""
        self.state["conditions"]["budget_krw"] = 0
        self.state["understanding"]["preferences"] = [self.preference("calm")]
        def ranker(candidates, prefs):
            """선택 정렬 캐시가 쓸 source hash와 실제 필드의 일치를 검사한다."""
            self.assertEqual(len(candidates[0]["source_field_hash"]), 64)
            self.assertEqual(candidates[0]["source_fields"]["description"], candidates[0]["description"])
            return {}
        with self.source([self.calm]):
            result = explore(self.state, ranker=ranker)
        self.assertIn(dict(field="budget_krw", value=0, basis="공개 자료에서 확인되는 후보만 통과"), result["applied"])
        self.assertEqual(result["ranking"]["status"], "unknown")

    def test_conflicting_date_is_not_silently_reinterpreted(self):
        """서로 다른 명시 날짜와 시각을 한 방문 일정처럼 섞어 조회하지 않는다."""
        self.state["conditions"].update(date="2026-11-02", start_at="2026-11-03T14:00:00+09:00")
        with patch("exploration.outing.seoul_page") as source, self.assertRaises(InputError):
            explore(self.state)
        source.assert_not_called()


if __name__ == "__main__":
    unittest.main()
