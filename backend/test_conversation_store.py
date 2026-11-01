"""네트워크 없이 대화 TTL·중복·CAS·문서 lease의 실제 저장 경계를 검사한다."""
from copy import deepcopy
from threading import Barrier, Thread
import unittest

from conversation_store import ConversationStore, StoreError


class Clock:
    """시간을 기다리지 않고 초 단위로 전진시키는 단조 시험 시계."""

    def __init__(self):
        """시험 시작을 임의의 양수 시각으로 고정한다."""
        self.now = 1000.0

    def __call__(self):
        """주입된 저장소에 현재 시험 시각을 반환한다."""
        return self.now

    def advance(self, seconds):
        """타이머 스레드 없이 TTL/lease 경계를 넘긴다."""
        self.now += seconds


class ConversationStoreTests(unittest.TestCase):
    """실제 저장소와 격리된 시간을 사용해 사용자 상태 보호를 검증한다."""

    def setUp(self):
        """각 시험에 독립 서버 상태·문서·대화를 만든다."""
        self.clock = Clock()
        self.store = ConversationStore(clock=self.clock)
        self.opened = self.store.open("document-a", initial_state={"goal": "공연", "hard": ["무료"]})

    def request(self, *, seq=None, revision=None, turn_id=None, opened=None, **changes):
        """서버가 발급한 메타데이터로 현재 다음 턴의 요청을 만든다."""
        metadata = (opened or self.opened)["conversation"]
        seq = metadata["next_turn_seq"] if seq is None else seq
        result = {"conversation_id": metadata["conversation_id"], "epoch": metadata["epoch"],
                  "document_id": metadata["document_id"], "turn_id": turn_id or f"turn-{seq}",
                  "turn_seq": seq, "expected_revision": metadata["revision"] if revision is None else revision,
                  "event": {"type": "message", "message": "잔잔한 음악"}}
        result.update(changes)
        return result

    def assert_error(self, code, function, *args, **kwargs):
        """오류 메시지가 아니라 안정된 코드로 저장 경계 실패를 단언한다."""
        with self.assertRaises(StoreError) as caught:
            function(*args, **kwargs)
        self.assertEqual(caught.exception.code, code)
        return caught.exception

    def finish(self, request=None, state=None, response=None):
        """예약 밖에서 계산한 상태와 업무 결과를 한 번 commit한다."""
        reservation = self.store.reserve(request or self.request())
        result = self.store.commit(reservation["token"], state or {"goal": "공연", "taste": "잔잔함"},
                                   response or {"status": "ready", "assistant_text": "공연을 찾아볼게요."})
        self.opened = {"conversation": result["conversation"], "state": result["state"]}
        return result

    def test_open_reserve_commit_snapshots_are_independent(self):
        """호출자가 입력/반환 상태를 바꿔도 정규 상태는 바뀌지 않는다."""
        self.opened["state"]["hard"].clear()
        reservation = self.store.reserve(self.request())
        self.assertEqual(reservation["state"]["hard"], ["무료"])
        state = {"goal": "공연", "hard": ["무료"]}
        response = self.store.commit(reservation["token"], state, {"status": "ready"})
        state["hard"].clear()
        response["state"]["hard"].clear()
        current = self.store.open("document-a", response["conversation"]["conversation_id"], response["conversation"]["epoch"])
        self.assertEqual(current["state"]["hard"], ["무료"])
        self.assertEqual(current["conversation"]["revision"], 1)

    def test_duplicate_completed_turn_replays_without_reservation(self):
        """응답 손실 뒤 동일 요청은 원 업무 결과와 현재 snapshot을 재전달한다."""
        request = self.request()
        response = self.finish(request)
        cached = self.store.reserve(request)
        self.assertEqual(cached["kind"], "cached")
        self.assertEqual(cached["response"]["assistant_text"], response["assistant_text"])
        self.assertTrue(cached["response"]["replayed"])
        self.assertNotIn("token", cached)

    def test_cached_old_response_has_current_canonical_state(self):
        """옛 응답 재전달이 최신 취향·revision을 덮지 않게 한다."""
        first = self.request()
        self.finish(first)
        latest = self.finish(state={"goal": "공연", "taste": "신남"})
        replay = self.store.reserve(first)["response"]
        self.assertEqual(replay["state"], latest["state"])
        self.assertEqual(replay["conversation"]["revision"], 2)
        self.assertEqual(replay["turn_seq"], 1)

    def test_pending_duplicate_and_changed_payload_do_not_create_second_job(self):
        """진행 중 중복은 busy이며 같은 turn의 다른 본문은 충돌이다."""
        request = self.request()
        reservation = self.store.reserve(request)
        self.assert_error("turn_in_progress", self.store.reserve, request)
        changed = deepcopy(request)
        changed["event"]["message"] = "신나는 공연"
        self.assert_error("turn_conflict", self.store.reserve, changed)
        self.store.commit(reservation["token"], {"goal": "공연"}, {"status": "ready"})
        self.assert_error("turn_conflict", self.store.reserve, changed)

    def test_same_revision_concurrent_requests_have_one_winner(self):
        """실제 두 스레드가 같은 revision을 예약해도 외부 작업 자격은 하나뿐이다."""
        barrier = Barrier(3)
        outcomes = []

        def run(turn_id):
            """동일 시점에 예약을 시도하고 결과 코드만 수집한다."""
            barrier.wait()
            try:
                outcomes.append(self.store.reserve(self.request(turn_id=turn_id))["kind"])
            except StoreError as error:
                outcomes.append(error.code)

        threads = [Thread(target=run, args=(name,)) for name in ("left", "right")]
        for thread in threads:
            thread.start()
        barrier.wait()
        for thread in threads:
            thread.join(timeout=2)
            self.assertFalse(thread.is_alive())
        self.assertCountEqual(outcomes, ["reserved", "conversation_busy"])

    def test_stale_revision_and_out_of_order_sequence_resynchronize(self):
        """순서나 revision이 다른 새 요청은 현재 정규 상태를 받아 재동기화한다."""
        self.finish()
        error = self.assert_error("stale_revision", self.store.reserve, self.request(revision=0))
        self.assertEqual(error.response["conversation"]["revision"], 1)
        self.assert_error("out_of_order", self.store.reserve, self.request(seq=4))

    def test_twenty_first_turn_keeps_watermark_without_old_response(self):
        """20응답 캐시에서 빠진 과거 seq를 다시 LLM/도구 작업으로 예약하지 않는다."""
        first = self.request()
        for unused in range(21):
            self.finish()
        error = self.assert_error("already_processed", self.store.reserve, first)
        self.assertEqual(error.conversation["last_committed_seq"], 21)
        self.assertEqual(error.conversation["next_turn_seq"], 22)
        self.assertEqual(len(self.store._conversations[first["conversation_id"]].recent), 20)

    def test_active_duplicate_tab_forks_clean_factory_state(self):
        """복제 문서가 활성 대화 handle을 가져도 이전 니즈·제약을 복사하지 않는다."""
        metadata = self.opened["conversation"]
        forked = self.store.open("document-b", metadata["conversation_id"], metadata["epoch"],
                                 initial_state={"goal": "", "hard": []})
        self.assertTrue(forked["forked"])
        self.assertNotEqual(forked["conversation"]["conversation_id"], metadata["conversation_id"])
        self.assertEqual(forked["state"], {"goal": "", "hard": []})

    def test_reload_waits_for_lease_then_takes_over_same_conversation(self):
        """새로고침은 활성 writer를 빼앗지 않고 만료 뒤 같은 상태에 연결한다."""
        metadata = self.opened["conversation"]
        error = self.assert_error("lease_busy", self.store.open, "document-b", metadata["conversation_id"],
                                  metadata["epoch"], mode="resume")
        self.assertEqual(error.retry_after_seconds, 10)
        self.clock.advance(10)
        resumed = self.store.open("document-b", metadata["conversation_id"], metadata["epoch"], mode="resume")
        self.assertFalse(resumed["forked"])
        self.assertEqual(resumed["state"]["hard"], ["무료"])
        self.assertGreater(resumed["conversation"]["lease_generation"], metadata["lease_generation"])

    def test_lease_handover_fences_delayed_commit(self):
        """지연 모델 작업 중 lease가 인계되면 옛 결과가 새 대화 상태에 들어가지 않는다."""
        reservation = self.store.reserve(self.request())
        metadata = self.opened["conversation"]
        self.clock.advance(11)
        resumed = self.store.open("document-b", metadata["conversation_id"], metadata["epoch"], mode="resume")
        self.assert_error("reservation_lost", self.store.commit, reservation["token"], {"goal": "옛 결과"}, {})
        current = self.store.heartbeat(metadata["conversation_id"], metadata["epoch"], "document-b")
        self.assertEqual(current["state"], resumed["state"])
        self.assertEqual(current["conversation"]["revision"], 0)
        self.assert_error("lease_lost", self.store.reserve, self.request())

    def test_lease_expiry_alone_prevents_commit(self):
        """다른 문서가 없더라도 만료 lease의 작업을 성공 commit하지 않는다."""
        reservation = self.store.reserve(self.request())
        self.clock.advance(10)
        self.assert_error("lease_expired", self.store.commit, reservation["token"], {}, {})

    def test_heartbeat_allows_long_job_without_holding_lock(self):
        """네트워크 계산을 흉내 낸 지연 동안 heartbeat는 독립적으로 성공한다."""
        reservation = self.store.reserve(self.request())
        metadata = self.opened["conversation"]
        for unused in range(5):
            self.clock.advance(5)
            self.store.heartbeat(metadata["conversation_id"], metadata["epoch"], "document-a")
        result = self.store.commit(reservation["token"], {"goal": "공연"}, {})
        self.assertEqual(result["conversation"]["revision"], 1)

    def test_release_invalidates_job_and_old_generation(self):
        """페이지 이탈 해제는 대기 작업과 이전 lease 세대를 함께 무효화한다."""
        reservation = self.store.reserve(self.request())
        metadata = self.opened["conversation"]
        self.store.release(metadata["conversation_id"], metadata["epoch"], "document-a")
        resumed = self.store.open("document-b", metadata["conversation_id"], metadata["epoch"], mode="resume")
        self.assert_error("reservation_lost", self.store.commit, reservation["token"], {}, {})
        self.assert_error("lease_lost", self.store.heartbeat, metadata["conversation_id"], metadata["epoch"],
                          "document-b", metadata["lease_generation"])
        self.assertNotEqual(resumed["conversation"]["lease_generation"], metadata["lease_generation"])

    def test_ttl_expiry_does_not_resurrect_pending_job(self):
        """TTL 뒤 도착한 작업·옛 handle 재연결은 새 상태를 만들지 않는다."""
        reservation = self.store.reserve(self.request())
        metadata = self.opened["conversation"]
        self.clock.advance(1800)
        self.assert_error("reservation_lost", self.store.commit, reservation["token"], {"goal": "옛 상태"}, {})
        self.assert_error("conversation_expired", self.store.open, "document-a", metadata["conversation_id"], metadata["epoch"])
        self.assertEqual(len(self.store._conversations), 0)

    def test_heartbeats_do_not_keep_inactive_chat_forever(self):
        """브라우저 heartbeat만 지속돼도 사용자 비활동 TTL에는 대화가 만료된다."""
        store = ConversationStore(clock=self.clock, ttl_seconds=12)
        metadata = store.open("doc")["conversation"]
        self.clock.advance(5)
        store.heartbeat(metadata["conversation_id"], metadata["epoch"], "doc")
        self.clock.advance(5)
        store.heartbeat(metadata["conversation_id"], metadata["epoch"], "doc")
        self.clock.advance(2)
        self.assert_error("conversation_expired", store.heartbeat, metadata["conversation_id"], metadata["epoch"], "doc")

    def test_capacity_rejects_new_chat_without_evicting_active_state(self):
        """포화가 기존 대화·진행 작업을 버리지 않고 TTL 이후 용량을 회수한다."""
        store = ConversationStore(clock=self.clock, max_conversations=1, ttl_seconds=15)
        initial = store.open("doc", initial_state={"goal": "보존"})
        self.assert_error("conversations_full", store.open, "other")
        self.assertEqual(store.open("doc", initial["conversation"]["conversation_id"], initial["conversation"]["epoch"])["state"]["goal"], "보존")
        self.clock.advance(15)
        self.assertEqual(store.open("other")["state"], {})

    def test_error_result_commits_meaning_once_and_retry_is_new_turn(self):
        """도구 장애를 의미와 함께 확정하고 도구 재시도는 새 seq에서 한 번만 확정한다."""
        request = self.request()
        response = self.finish(request, {"goal": "공연", "taste": "잔잔함"}, {"status": "source_error"})
        replay = self.store.reserve(request)
        self.assertEqual(replay["response"]["status"], "source_error")
        retry = self.request(event={"type": "retry_tool", "action_id": "failed-tool"})
        result = self.finish(retry, response["state"], {"status": "ready", "results": ["actual-id"]})
        self.assertEqual(result["state"], response["state"])
        self.assertEqual(result["conversation"]["revision"], 2)

    def test_cancel_uncommitted_job_prevents_late_apply(self):
        """예기치 않은 호출자 예외 뒤 취소한 token으로 상태를 반영할 수 없다."""
        reservation = self.store.reserve(self.request())
        self.assertTrue(self.store.cancel(reservation["token"]))
        self.assertFalse(self.store.cancel(reservation["token"]))
        self.assert_error("reservation_lost", self.store.commit, reservation["token"], {}, {})
        self.assertEqual(self.store.reserve(self.request())["kind"], "reserved")

    def test_invalid_input_does_not_mutate_or_leak_request(self):
        """잘못된 seq/JSON/epoch는 원 사용자 발화를 오류문에 노출하지 않는다."""
        error = self.assert_error("invalid_request", self.store.reserve, self.request(turn_seq=True))
        self.assertNotIn("잔잔한", str(error))
        self.assert_error("epoch_mismatch", self.store.reserve, self.request(epoch="other-server"))
        self.assert_error("invalid_state", self.store.open, "invalid", initial_state={"value": float("nan")})
        self.assertEqual(self.store.reserve(self.request())["kind"], "reserved")


if __name__ == "__main__":
    unittest.main()
