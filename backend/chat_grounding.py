"""검증 가능한 발화 근거만 조건에 반영한다. 외부 호출·저장·행사 사실 판정은 하지 않는다.

원문 인용은 의미의 정확성을 보증하지 않는다. 시간과 날짜는 지원하는 표현만 코드로
대조하며, 파싱할 수 없는 경우 보수적으로 보류한다.
"""
from datetime import date, datetime, timedelta
import re

from chat_conditions import FIELDS, normalize_proposal
from outing import KST

FIELD_LABELS = dict(start_query="출발지", start_at="출발 날짜와 시각", end_at="종료 날짜와 시각",
                    category="관심 분류", categories="관심 분류", request_kind="추천 종류",
                    stay_minutes="한 장소 체류시간", music_followup="음악 취향", free_only="무료 여부",
                    budget_krw="관람료 예산", keywords="관심어", exclude_terms="제외 조건",
                    walking_preference="걷기 선호", indoor_outdoor="실내·실외 선호",
                    unsupported_requirements="필수 조건")

_NUMBER = {"한": 1, "하나": 1, "두": 2, "둘": 2, "세": 3, "셋": 3,
           "네": 4, "넷": 4, "다섯": 5, "여섯": 6, "일곱": 7, "여덟": 8,
           "아홉": 9, "열": 10, "열한": 11, "열두": 12}
_CLOCK = re.compile(r"(?<!\d)(\d{1,2}|열두|열한|다섯|여섯|일곱|여덟|아홉|하나|둘|셋|넷|열|한|두|세|네)\s*시(?!간)(?:\s*(반|\d{1,2}\s*분))?|(?<!\d)(\d{1,2}):(\d{2})(?!\d)")
_PERIOD = re.compile(r"오전|오후|아침|저녁|밤|낮|새벽")
_DATE = re.compile(r"(?<!\d)\d{4}[-/.]\d{1,2}[-/.]\d{1,2}(?!\d)|오늘|내일|모레|글피|어제|그제")
_UNSUPPORTED_DATE = re.compile(r"이번\s*주|다음\s*주|주말|[월화수목금토일]요일|\d{1,2}\s*월|(?<![\d/.-])\d{1,2}[/.]\d{1,2}(?![\d/.-])")
_START = re.compile(r"출발(?!지)|시작|부터")
_END = re.compile(r"마치|종료|끝|돌아|귀가|까지")
_CATEGORY_WORDS = {"전시": ("전시",), "국악": ("국악", "꾹악"), "클래식": ("클래식", "클레식", "클라식"),
                   "콘서트": ("콘서트", "콘써트"), "연극": ("연극",)}


class GroundedProposal(dict):
    """조건 후보와 별도로 보류된 필드명만 보관한다. 사용자 원문은 저장하지 않는다."""

    def __init__(self, changes, blocked_fields=()):
        """호출자 데이터를 복사하고 보류 필드를 고정한다."""
        super().__init__(changes)
        self.blocked_fields = tuple(blocked_fields)


def _date_from_text(text, now):
    """현재 발화의 지원되는 단일 날짜만 계산한다. 애매하거나 여러 날짜면 None이다."""
    if _UNSUPPORTED_DATE.search(text):
        return None, True
    matches = list(_DATE.finditer(text))
    if len(matches) != 1:
        return None, bool(matches)
    token = matches[0].group()
    offsets = {"그제": -2, "어제": -1, "오늘": 0, "내일": 1, "모레": 2, "글피": 3}
    if token in offsets:
        return now.astimezone(KST).date() + timedelta(days=offsets[token]), True
    try:
        parts = re.split(r"[-/.]", token)
        return date(*(int(part) for part in parts)), True
    except ValueError:
        return None, True


def _draft_date(draft, field):
    """초안의 명시 날짜를 반환한다. 유효하지 않거나 서로 다르면 보류한다."""
    days = set()
    for key in ("date", "start_at", "end_at"):
        value = draft.get(key)
        if not isinstance(value, str):
            continue
        try:
            if key == "date":
                days.add(date.fromisoformat(value))
            else:
                parsed = datetime.fromisoformat(value)
                if parsed.tzinfo is not None:
                    days.add(parsed.astimezone(KST).date())
        except ValueError:
            continue
    return next(iter(days)) if len(days) == 1 else None


def _clock_values(text):
    """발화의 명시 시각을 분 단위로 계산한다. 모호한 시각은 None으로 둔다."""
    values = []
    previous_end = 0
    for match in _CLOCK.finditer(text):
        token = match.group(1) or match.group(3)
        hour = int(token) if token.isdigit() else _NUMBER[token]
        minute_text = match.group(2)
        minute = 30 if minute_text == "반" else int(re.sub(r"\D", "", minute_text)) if minute_text else int(match.group(4) or 0)
        # 앞 시각의 오전/오후를 뒤 시각에 상속하면 정오를 넘기는 범위를 오해한다.
        before = text[previous_end:match.start()]
        previous_end = match.end()
        periods = list(_PERIOD.finditer(before))
        period = periods[-1].group() if periods else None
        if minute > 59 or hour > 23 or (period and hour > 12):
            values.append((match, None))
            continue
        if period in ("오후", "저녁", "밤", "낮"):
            hour = hour % 12 + 12
        elif period in ("오전", "아침", "새벽"):
            hour %= 12
        elif 1 <= hour <= 12:
            values.append((match, None))
            continue
        values.append((match, hour * 60 + minute))
    return values


def _question_target(history):
    """직전 질문이 시작 또는 종료 하나를 묻는 경우에만 대상을 반환한다."""
    if not history or history[-1].get("role") != "assistant":
        return None
    question = history[-1].get("content", "")
    start, end = bool(_START.search(question)), bool(_END.search(question))
    if start == end:
        return None
    return "start_at" if start else "end_at"


def _time_matches(field, value, message, quote, draft, history, now):
    """모델 시각을 발화의 날짜·시각·대상과 비교한다. 지원하지 않는 표현은 보류한다."""
    try:
        parsed = datetime.fromisoformat(value)
        if parsed.tzinfo is None:
            return False
        parsed = parsed.astimezone(KST)
    except (ValueError, TypeError):
        return False
    # 상대 시각을 단순 시각으로 잘못 해석하지 않는다.
    if re.search(r"늦춰|늦게|당겨|앞당|후에|뒤에|시간\s*뒤|시간\s*후", message):
        return False
    day, explicit_date = _date_from_text(message, now)
    if explicit_date and day is None:
        return False
    if not explicit_date:
        day = _draft_date(draft, field)
    if day is None or parsed.date() != day:
        return False
    clocks = _clock_values(message)
    if len(clocks) > 2:
        return False
    if not clocks:
        # 날짜만 정정하는 경우에만 이미 확정된 해당 시각을 그대로 보존한다.
        previous = draft.get(field)
        if not explicit_date or not _DATE.search(quote) or not isinstance(previous, str):
            return False
        try:
            old = datetime.fromisoformat(previous)
            return old.tzinfo is not None and old.astimezone(KST).time() == parsed.time()
        except ValueError:
            return False
    if len(clocks) == 2:
        # 두 시각의 역할이 명시적으로 '부터 ... 까지'일 때만 순서를 해석한다.
        first, second = clocks
        between = message[first[0].end():second[0].start()]
        after = message[second[0].end():]
        if not re.search(r"부터", between) or not re.search(r"까지", after):
            return False
        selected = first if field == "start_at" else second
    else:
        selected = clocks[0]
        start, end = bool(_START.search(message)), bool(_END.search(message))
        target = ("start_at" if start else "end_at") if start != end else _question_target(history)
        if target != field:
            return False
    if selected[0].group() not in quote:
        return False
    minutes = selected[1]
    return (minutes is not None and parsed.hour * 60 + parsed.minute == minutes
            and parsed.second == 0 and parsed.microsecond == 0)


def _category_matches(value, message, draft):
    """명시된 분류의 부정·다른 분류로의 임의 변경만 보수적으로 차단한다."""
    proposed = value if isinstance(value, list) else [value]
    spoken = {category for category, words in _CATEGORY_WORDS.items() if any(word in message for word in words)}
    for category in proposed:
        for word in _CATEGORY_WORDS.get(category, ()):
            if re.search(re.escape(word) + r"\s*(?:은|는|이|가|을|를)?\s*(?:말고|아니|싫|빼|제외)", message):
                return False
    previous = draft.get("categories", [draft.get("category")])
    if not isinstance(previous, list):
        previous = []
    # 음악은 복수 분류를 의미할 수 있고 '전체'는 미지원 관심어를 보존하는 표현이다.
    if spoken and "음악" not in message:
        return all(category in spoken or category in previous or category == "전체" for category in proposed)
    return True


def ground_payload(payload, message, draft, history, now=None):
    """원문 근거·형식·검증 가능한 시각을 검사하고 차단된 필드를 분리한다.

    타당한 인용은 비시간 선호의 의미 정확성을 증명하지 않는다. 지원 범위 밖의
    날짜·시간은 기존 값 대신 보류한다. 잘못된 최상위 응답은 ValueError다.
    """
    if not isinstance(payload, dict) or set(payload) != {"changes", "evidence"}:
        raise ValueError("AI 근거 응답 형식을 확인해 주세요.")
    changes, evidence = payload["changes"], payload["evidence"]
    if not isinstance(changes, dict) or set(changes) - FIELDS:
        raise ValueError("AI 조건 항목을 확인해 주세요.")
    if not isinstance(evidence, dict) or set(evidence) - set(changes):
        raise ValueError("AI 근거 항목을 확인해 주세요.")
    if now is None:
        now = datetime.now(KST)
    if now.tzinfo is None:
        raise ValueError("시간대가 있는 현재 시각이 필요합니다.")
    accepted, blocked = {}, []
    compact = re.sub(r"\s+", "", message).casefold()
    for field, value in changes.items():
        if value is None:
            continue
        try:
            normalize_proposal({field: value})
        except (ValueError, TypeError):
            blocked.append(field)
            continue
        quote = evidence.get(field)
        valid = isinstance(quote, str) and 1 <= len(quote.strip()) <= 200 and quote.strip() in message
        if valid and field in {"start_at", "end_at"}:
            valid = _time_matches(field, value, message, quote, draft, history, now)
        if valid and field == "start_query":
            valid = re.sub(r"\s+", "", value).casefold() in re.sub(r"\s+", "", quote).casefold()
        if valid and field in {"keywords", "exclude_terms"}:
            previous = draft.get(field) if isinstance(draft.get(field), list) else []
            valid = all(term in previous or re.sub(r"\s+", "", term).casefold() in compact for term in value)
        if valid and field in {"category", "categories"}:
            valid = _category_matches(value, message, draft)
        if valid:
            accepted[field] = value
        else:
            blocked.append(field)
    # 서로 결합된 분류 항목의 일부만 조용히 변경하지 않는다.
    category_fields = {"category", "categories", "music_followup"}
    if category_fields.intersection(blocked):
        for field in list(accepted):
            if field in category_fields:
                blocked.append(field)
                del accepted[field]
    return GroundedProposal(accepted, blocked)


def clarification_text(fields):
    """보류 필드명을 한국어 확인 질문으로 바꾼다. 원문과 모델 응답은 노출하지 않는다."""
    labels = list(dict.fromkeys(FIELD_LABELS[field] for field in fields))
    return "말씀하신 내용만으로 " + "·".join(labels) + "을 확정하지 않았어요. 해당 조건을 다시 알려 주시겠어요?"
