"""단일 프로세스의 임시 대화 상태·턴 중복·writer lease를 관리한다.

외부 호출은 reserve와 commit 사이에서 호출자가 수행한다. 상태의 의미/사실
검증과 snapshot 복원은 호출자의 책임이며 이 저장소는 인증·영속성을 제공하지 않는다.
"""
from collections import OrderedDict
from copy import deepcopy
from dataclasses import dataclass, field
import hashlib
import json
import secrets
from threading import RLock
import time


class StoreError(Exception):
    """원문·handle을 메시지에 노출하지 않는 동기화 오류와 현재 snapshot."""

    def __init__(self, code, status=409, *, state=None, conversation=None, retry_after_seconds=None):
        """HTTP 상태·안전한 코드와 독립 복사한 재동기화 자료를 보관한다."""
        super().__init__(code)
        self.code = code
        self.status = self.status_code = status
        self.state = deepcopy(state)
        self.conversation = deepcopy(conversation)
        self.retry_after_seconds = retry_after_seconds

    def as_response(self):
        """허용된 호출자가 현재 상태를 재동기화할 API 오류 본문을 반환한다."""
        result = {"status": "error", "code": self.code}
        if self.state is not None:
            result["state"] = deepcopy(self.state)
        if self.conversation is not None:
            result["conversation"] = deepcopy(self.conversation)
        if self.retry_after_seconds is not None:
            result["retry_after_seconds"] = self.retry_after_seconds
        return result

    @property
    def response(self):
        """호출자가 오류 본문을 속성으로 읽을 수 있게 한다."""
        return self.as_response()


@dataclass
class _Reservation:
    """한 턴의 입력 hash와 commit을 제한하는 소유권 fence."""
    token: str
    conversation_id: str
    epoch: str
    document_id: str
    lease_generation: int
    revision: int
    turn_id: str
    turn_seq: int
    request_hash: str


@dataclass
class _Conversation:
    """TTL 동안만 살아 있는 정규 상태와 bounded 응답 cache."""
    conversation_id: str
    epoch: str
    document_id: str
    state: dict
    last_activity: float
    lease_until: float
    revision: int = 0
    last_committed_seq: int = 0
    lease_generation: int = 1
    recent: OrderedDict = field(default_factory=OrderedDict)
    reservation: object = None


def _identifier(value):
    """본문/로그를 포함하지 않고 짧은 opaque ID 형식만 확인한다."""
    return isinstance(value, str) and 1 <= len(value) <= 160 and not any(ord(c) < 33 for c in value)


def _json_copy(value):
    """유한 JSON 자료만 독립 복사하며 함수·NaN 같은 객체를 거부한다."""
    return json.loads(json.dumps(value, ensure_ascii=False, allow_nan=False))


class ConversationStore:
    """TTL30분/100대화/20응답/10초 lease의 메모리 저장소; 모든 시간은 초다."""

    def __init__(self, *, ttl_seconds=1800, max_conversations=100, recent_turns=20,
                 lease_seconds=10, clock=None):
        """단조 시계 주입으로 실제 기다림 없이 만료·동시성을 검증할 수 있게 한다."""
        if (ttl_seconds <= 0 or lease_seconds <= 0 or max_conversations < 1 or recent_turns < 1):
            raise ValueError("저장소 한도는 양수여야 합니다.")
        self.ttl_seconds = ttl_seconds
        self.max_conversations = max_conversations
        self.recent_turns = recent_turns
        self.lease_seconds = lease_seconds
        self._clock = clock or time.monotonic
        self._lock = RLock()
        self._conversations = {}
        self._tokens = {}

    def _metadata(self, item, now):
        """서버의 절대 단조시각 대신 남은 lease와 버전을 공개한다."""
        return {"conversation_id": item.conversation_id, "epoch": item.epoch,
                "document_id": item.document_id, "revision": item.revision,
                "last_committed_seq": item.last_committed_seq,
                "next_turn_seq": item.last_committed_seq + 1,
                "lease_generation": item.lease_generation,
                "lease_expires_in": max(0, item.lease_until - now),
                "lease_seconds": self.lease_seconds, "ttl_seconds": self.ttl_seconds}

    def _error(self, code, item=None, *, status=409, retry_after_seconds=None):
        """현재 snapshot을 포함한 오류를 만들되 원 요청은 포함하지 않는다."""
        return StoreError(code, status, state=item.state if item else None,
                          conversation=self._metadata(item, self._clock()) if item else None,
                          retry_after_seconds=retry_after_seconds)

    def _invalidate(self, item):
        """예약 token을 제거해 취소·인계·만료된 작업의 commit을 차단한다."""
        if item.reservation is not None:
            self._tokens.pop(item.reservation.token, None)
            item.reservation = None

    def _prune(self, now):
        """사용자 활동 TTL이 지난 자료만 제거하며 heartbeat는 TTL을 늘리지 않는다."""
        expired = [key for key, item in self._conversations.items()
                   if now - item.last_activity >= self.ttl_seconds]
        for key in expired:
            self._invalidate(self._conversations.pop(key))

    def _get(self, conversation_id, epoch, now):
        """만료·서버 재시작·다른 epoch를 기존 상태로 조용히 복구하지 않는다."""
        self._prune(now)
        item = self._conversations.get(conversation_id)
        if item is None:
            raise self._error("conversation_expired", status=410)
        if item.epoch != epoch:
            raise self._error("epoch_mismatch", status=410)
        return item

    def _owner(self, item, document_id, now, lease_generation=None):
        """현재 문서의 유효 lease만 허용하며 만료 owner의 자동 갱신은 금지한다."""
        if item.document_id != document_id:
            raise self._error("lease_lost", item)
        if item.lease_until <= now:
            raise self._error("lease_expired", item)
        if lease_generation is not None and lease_generation != item.lease_generation:
            raise self._error("lease_lost", item)

    def _new(self, document_id, initial_state, now, forked):
        """기존 대화 내용을 복사하지 않고 호출자가 검증한 초기 상태로 생성한다."""
        self._prune(now)
        if len(self._conversations) >= self.max_conversations:
            raise self._error("conversations_full", status=503)
        try:
            state = _json_copy(initial_state if initial_state is not None else {})
        except (TypeError, ValueError):
            raise self._error("invalid_state", status=400) from None
        if not isinstance(state, dict):
            raise self._error("invalid_state", status=400)
        item = _Conversation(secrets.token_urlsafe(24), secrets.token_urlsafe(18), document_id,
                             state, now, now + self.lease_seconds)
        self._conversations[item.conversation_id] = item
        return {"state": deepcopy(item.state), "conversation": self._metadata(item, now), "forked": forked}

    def open(self, document_id, conversation_id=None, epoch=None, initial_state=None, *, mode="open"):
        """새 대화 생성/재연결; 활성 다른 문서는 fork, resume 모드는 만료까지 대기한다.

        initial_state는 새 대화의 초기값이며 기존 snapshot을 덮어쓰지 않는다.
        mode=fork도 기존 내용을 복제하지 않는다. 복원 검증은 호출자가 먼저 수행한다.
        """
        if not _identifier(document_id) or mode not in {"open", "resume", "fork"}:
            raise self._error("invalid_request", status=400)
        with self._lock:
            now = self._clock()
            if conversation_id is None or mode == "fork":
                try:
                    return self._new(document_id, initial_state, now, mode == "fork")
                except (ValueError, TypeError):
                    raise self._error("invalid_state", status=400) from None
            if not _identifier(conversation_id) or not _identifier(epoch):
                raise self._error("invalid_request", status=400)
            item = self._get(conversation_id, epoch, now)
            if item.document_id != document_id and item.lease_until > now:
                if mode == "resume":
                    raise self._error("lease_busy", item, retry_after_seconds=item.lease_until - now)
                return self._new(document_id, initial_state, now, True)
            if item.document_id != document_id or item.lease_until <= now:
                self._invalidate(item)
                item.document_id = document_id
                item.lease_generation += 1
            item.lease_until = now + self.lease_seconds
            item.last_activity = now
            return {"state": deepcopy(item.state), "conversation": self._metadata(item, now), "forked": False}

    def heartbeat(self, conversation_id, epoch, document_id, lease_generation=None):
        """살아 있는 현재 문서의 lease만 연장하고 사용자 활동 TTL은 늘리지 않는다."""
        with self._lock:
            now = self._clock()
            item = self._get(conversation_id, epoch, now)
            self._owner(item, document_id, now, lease_generation)
            item.lease_until = now + self.lease_seconds
            return {"state": deepcopy(item.state), "conversation": self._metadata(item, now)}

    def release(self, conversation_id, epoch, document_id, lease_generation=None):
        """이전 문서의 best-effort 해제도 예약을 fence하여 늦은 완료를 무효화한다."""
        with self._lock:
            now = self._clock()
            item = self._get(conversation_id, epoch, now)
            self._owner(item, document_id, now, lease_generation)
            self._invalidate(item)
            item.lease_until = now
            item.lease_generation += 1
            return {"conversation": self._metadata(item, now)}

    def reserve(self, request):
        """검증된 메타데이터의 다음 턴을 예약하거나 중복 결과/동기화 오류를 반환한다.

        반환 kind=reserved의 token/state로 네트워크 작업을 수행한 뒤 commit한다.
        kind=cached는 네트워크 재실행 없이 현재 canonical snapshot을 함께 반환한다.
        """
        if (not isinstance(request, dict)
                or any(not _identifier(request.get(key)) for key in ("conversation_id", "epoch", "document_id", "turn_id"))
                or type(request.get("turn_seq")) is not int or request["turn_seq"] < 1
                or type(request.get("expected_revision")) is not int or request["expected_revision"] < 0
                or not isinstance(request.get("event"), (dict, str))):
            raise self._error("invalid_request", status=400)
        try:
            encoded = json.dumps(request, ensure_ascii=False, sort_keys=True, allow_nan=False).encode("utf-8")
        except (TypeError, ValueError):
            raise self._error("invalid_request", status=400) from None
        request_hash = hashlib.sha256(encoded).hexdigest()
        with self._lock:
            now = self._clock()
            item = self._get(request["conversation_id"], request["epoch"], now)
            self._owner(item, request["document_id"], now, request.get("lease_generation"))
            seq, turn_id = request["turn_seq"], request["turn_id"]
            prior = item.recent.get(seq)
            if prior is not None:
                if prior["turn_id"] != turn_id or prior["request_hash"] != request_hash:
                    raise self._error("turn_conflict", item)
                response = deepcopy(prior["response"])
                response.update(state=deepcopy(item.state), conversation=self._metadata(item, now), replayed=True)
                return {"kind": "cached", "response": response,
                        "state": deepcopy(item.state), "conversation": self._metadata(item, now)}
            if seq <= item.last_committed_seq:
                raise self._error("already_processed", item)
            if any(record["turn_id"] == turn_id for record in item.recent.values()):
                raise self._error("turn_conflict", item)
            pending = item.reservation
            if pending is not None:
                if pending.turn_id == turn_id:
                    code = "turn_in_progress" if pending.request_hash == request_hash else "turn_conflict"
                    raise self._error(code, item)
                raise self._error("conversation_busy", item)
            if request["expected_revision"] != item.revision:
                raise self._error("stale_revision", item)
            if seq != item.last_committed_seq + 1:
                raise self._error("out_of_order", item)
            reservation = _Reservation(secrets.token_urlsafe(24), item.conversation_id, item.epoch,
                                       item.document_id, item.lease_generation, item.revision,
                                       turn_id, seq, request_hash)
            item.reservation = reservation
            self._tokens[reservation.token] = reservation
            item.last_activity = now
            return {"kind": "reserved", "token": reservation.token,
                    "state": deepcopy(item.state), "conversation": self._metadata(item, now)}

    def commit(self, token, state, response):
        """예약·epoch·revision·writer lease가 유효할 때만 상태와 결과를 한 번 확정한다."""
        try:
            next_state, result = _json_copy(state), _json_copy(response)
        except (TypeError, ValueError):
            raise self._error("invalid_state", status=400) from None
        if not isinstance(next_state, dict) or not isinstance(result, dict):
            raise self._error("invalid_state", status=400)
        with self._lock:
            now = self._clock()
            self._prune(now)
            reservation = self._tokens.get(token)
            if reservation is None:
                raise self._error("reservation_lost")
            item = self._get(reservation.conversation_id, reservation.epoch, now)
            try:
                self._owner(item, reservation.document_id, now, reservation.lease_generation)
                if item.reservation is not reservation or item.revision != reservation.revision:
                    raise self._error("stale_revision", item)
            except StoreError:
                self._invalidate(item)
                raise
            item.state = next_state
            item.revision += 1
            item.last_committed_seq = reservation.turn_seq
            item.last_activity = now
            result.update(state=deepcopy(item.state), conversation=self._metadata(item, now),
                          turn_id=reservation.turn_id, turn_seq=reservation.turn_seq)
            item.recent[reservation.turn_seq] = {"turn_id": reservation.turn_id,
                                                "request_hash": reservation.request_hash,
                                                "response": deepcopy(result)}
            while len(item.recent) > self.recent_turns:
                item.recent.popitem(last=False)
            self._invalidate(item)
            return result

    def cancel(self, token):
        """호출자의 예기치 않은 예외에서 미확정 예약과 늦은 commit을 무효화한다."""
        with self._lock:
            reservation = self._tokens.get(token)
            if reservation is None:
                return False
            item = self._conversations.get(reservation.conversation_id)
            if item is None or item.reservation is not reservation:
                self._tokens.pop(token, None)
                return False
            self._invalidate(item)
            return True
