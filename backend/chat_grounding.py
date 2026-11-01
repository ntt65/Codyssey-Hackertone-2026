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
        # 밤 12시는 자정/날짜 경계가 불명확하다. 낮 12시로 환산하지 않는다.
        if hour == 12 and period in ("밤", "저녁"):
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
    # 단일 시각 뒤에 이어진 부정은 그 시각을 승인하는 근거가 아니다.
    suffix = re.sub(r"\s+", "", message[selected[0].end():])
    if re.match(r"(?:(?:에|에는|은|는|이|가|을|를|으로|부터|까지))*"
                r"(?:(?:출발|시작|종료|마치|끝|귀가)(?:은|는|이|가|을|를)?)?"
                r"(?:안|못|아니|싫|불가|말고|하지|하면안)", suffix):
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


def _origin_matches(value, quote, message, history):
    """명시적 출발 표현이나 직전 출발지 질문과 지명을 대조한다."""
    name = re.sub(r"\s+", "", value).casefold()
    quoted = re.sub(r"\s+", "", quote).casefold()
    text = re.sub(r"\s+", "", message).casefold()
    if name not in quoted:
        return False
    escaped = re.escape(name)
    # 장소가 가고 싶은 목적지로 명시된 경우, 다른 곳의 출발 표현으로 인정하지 않는다.
    if re.search(escaped + r"(?:에|으로|로|까지)(?:가고|가려|가자|갈|가요|방문|보고|가겠)", text):
        return False
    if re.search(escaped + r"(?:에서|부터)?출발(?:은|는|이|가|을|를)?(?:하지|안|못|아니|싫|불가|말고)", text):
        return False
    if "출발" in text:
        return bool(re.search(escaped + r"(?:에서|부터)?출발|출발(?:지는|지|은|장소는|점은)?" + escaped, text))
    # 질문이 없는 단답 지명은 목적지일 수도 있으므로 출발지로 확정하지 않는다.
    question = history[-1].get("content", "") if history and history[-1].get("role") == "assistant" else ""
    return bool(re.search(r"출발(?:지|할|하|은|이|은|지를|할\s*곳)?", question))


def _free_matches(value, message, draft, history):
    """명시된 무료 조건과 해제만 인정하며 질문 맥락 없는 반대 값은 막는다."""
    text = re.sub(r"\s+", "", message)
    if value:
        if re.search(r"무료(?:인)?(?:전시|공연|행사|체험|축제|관람)?(?:만|로)?(?:는|은|을|를)?(?:아니|말고|싫|불가|안돼|안됨|해제|원하지않)", text):
            return False
        if re.search(r"무료(?:인)?(?:전시|공연|행사|체험|축제|관람)?(?:만|로)?(?:는|은|을|를)?(?:보여주|추천하|찾아주|보고싶)지(?:마|말|않)", text):
            return False
        return bool(re.search(r"무료(?:만|로만|로|인것만|만요|요|(?:인)?(?:전시|공연|행사|체험|축제|관람))|돈(?:은|이)?안(?:드는|들|내는)", text))
    if re.search(r"유료(?:도|라도)(?:괜찮|좋|돼|가능)(?:지않|지못|은아니)", text):
        return False
    if re.search(r"유료(?:도|라도)(?:괜찮|좋|돼|가능)|무료(?:만)?(?:는|은)?(?:아니|말고|해제)|무료제한(?:없|해제)", text):
        return True
    question = history[-1].get("content", "") if history and history[-1].get("role") == "assistant" else ""
    return bool(re.search(r"무료|유료", question) and re.fullmatch(r"(?:상관없(?:어요|어|습니다)?|아무거나(?:요)?)[.!?]?", text))


def _price_amount(quote):
    """근거의 단일 원화 금액만 읽는다. 복합 표현은 추측하지 않는다."""
    text = re.sub(r"\s+", "", quote)
    matches = list(re.finditer(r"(?<![\d,.만천백십일이삼사오육칠팔구])([\d,]+|일|이|삼|사|오|육|칠|팔|구)?(만|천)?원", text))
    if len(matches) != 1:
        return None
    match = matches[0]
    amount, unit = match.group(1), match.group(2)
    if not amount and not unit:
        return None
    if amount is None:
        number = 1
    elif amount in "일이삼사오육칠팔구":
        number = "일이삼사오육칠팔구".index(amount) + 1
    else:
        try:
            number = int(amount.replace(",", ""))
        except ValueError:
            return None
    return number * {None: 1, "천": 1000, "만": 10000}[unit]


def _budget_matches(value, quote, message, history):
    """관람료 금액·제한 해제를 확인할 수 있을 때만 예산을 적용한다."""
    question = history[-1].get("content", "") if history and history[-1].get("role") == "assistant" else ""
    # 총 외출 비용은 관람료 상한과 다르다.
    if re.search(r"총\s*(?:비용|예산)|교통비|식비", message):
        return False
    if not re.search(r"관람료|입장료|입장권|티켓|표값|관람\s*예산", message + question):
        return False
    if value == "any":
        return bool(re.search(r"제한\s*(?:없|해제)|상관\s*없|얼마든|예산\s*(?:없|해제)", message))
    # budget_krw는 상한이므로 하한을 같은 금액의 상한으로 바꾸지 않는다.
    if re.search(r"(?:원\s*(?:이상|초과|넘|보다\s*(?:높|많)))", message):
        return False
    return _price_amount(quote) == value and _price_amount(message) == value


def _exclusions_match(value, message, draft):
    """제외 항목은 새 발화에 있거나 기존에 있어야 하며 해제는 항목별 명시해야 한다."""
    previous = draft.get("exclude_terms")
    if not isinstance(previous, list):
        previous = []
    compact = re.sub(r"\s+", "", message).casefold()
    for term in previous:
        if term in value:
            continue
        escaped = re.escape(re.sub(r"\s+", "", term).casefold())
        # 빼기/제외 자체는 제외 추가이므로 해제라는 표현과 구분한다.
        if not re.search(escaped + r"(?:은|는|을|를)?(?:제외(?:를|을|조건)?해제|제외하지(?:마|말|않)|빼지(?:마|말|않)|다시포함)", compact):
            return False
    return all(term in previous or re.sub(r"\s+", "", term).casefold() in compact for term in value)


def _requirements_match(value, message, draft):
    """필수 조건의 임의 삭제와 발화에 없는 신규 제약을 차단한다."""
    previous = draft.get("unsupported_requirements")
    if not isinstance(previous, list):
        previous = []
    compact = re.sub(r"\s+", "", message).casefold()
    def present(term):
        """띄어쓰기를 제외한 조건 원문이 발화에 있는지 확인한다."""
        return re.sub(r"\s+", "", term).casefold() in compact
    removed = [term for term in previous if term not in value]
    def explicitly_removed(term):
        """제거할 각 항목에 해제 표현이 직접 연결된 경우만 인정한다."""
        escaped = re.escape(re.sub(r"\s+", "", term).casefold())
        if re.search(escaped + r"(?:조건|제약)?(?:은|는|을|를)?"
                     r"(?:빼지(?:마|말|않)|제외하지(?:마|말|않)|해제하지(?:마|말|않)|"
                     r"없애지(?:마|말|않)|지우지(?:마|말|않)|필요없지않)", compact):
            return False
        return bool(re.search(escaped + r"(?:조건|제약)?(?:은|는|을|를)?(?:빼|제외|해제|없애|지워|필수아니|필요없)", compact))
    if removed and not all(explicitly_removed(term) for term in removed):
        return False
    for term in value:
        if term in previous:
            continue
        escaped = re.escape(re.sub(r"\s+", "", term).casefold())
        if not present(term) or re.search(escaped + r"(?:은|는|을|를)?(?:말고|아니|싫|빼|제외)", compact):
            return False
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
            valid = _origin_matches(value, quote, message, history)
        if valid and field == "free_only":
            valid = _free_matches(value, message, draft, history)
        if valid and field == "budget_krw":
            valid = _budget_matches(value, quote, message, history)
        if valid and field == "unsupported_requirements":
            valid = _requirements_match(value, message, draft)
        if valid and field == "exclude_terms":
            valid = _exclusions_match(value, message, draft)
        if valid and field == "keywords":
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
