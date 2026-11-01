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
_PARTICLES = r"(?:(?:으로|에서|부터|까지|은|는|이|가|을|를|도|만|로))*"
_REJECTION = (r"(?:아니|아닌|아닙|아냐|말고|싫|별로|불가|(?:이)?면안|안(?:돼|되|됨|보|듣|가|하|원|좋|싫|나쁘)|못|"
              r"원하지|(?:보|듣|가|하|추천하|찾아주|보여주)지(?:않|마|말)|"
              r"(?:좋|괜찮|선호하)지(?:않|못)|(?:보고|듣고|가고|하고)싶지(?:않|마|말)|"
              r"(?:보|듣|가|하)면안)")
_REMOVAL_PROHIBITED = (r"(?:빼지|제외하지|해제하지|없애지|지우지|삭제하지|지워주지|빼주지|필요없지|"
                      r"빼면안|빼서는안|제외하면안|제외해서는안|제외해선안|해제하면안|삭제하면안)")


def _compact(text):
    """근거 비교에만 쓸 공백 없는 문자열을 만든다. 원문과 저장 상태는 바꾸지 않는다."""
    return re.sub(r"\s+", "", text).casefold()


def _term_rejected(term, message):
    """해당 항목 바로 뒤의 부정만 검사한다. 다른 절의 거절을 이 항목에 붙이지 않는다."""
    suffix = (_PARTICLES + r"(?:인)?(?:전시|공연|행사|체험|축제|관람|활동|것|곳)?"
              + _PARTICLES + _REJECTION)
    return bool(re.search(re.escape(_compact(term)) + suffix, _compact(message)))


def _explicit_removal(term, message):
    """관심어 등 긍정 조건의 항목별 해제만 인정하고 해제하지 말라는 요청은 거절한다."""
    prefix = re.escape(_compact(term)) + r"(?:조건|제약|관심어|키워드)?" + _PARTICLES
    text = _compact(message)
    if re.search(prefix + _REMOVAL_PROHIBITED, text):
        return False
    return bool(re.search(prefix + r"(?:빼|제외|해제|없애|지워|삭제|말고|필수아니|필요없|관심없)", text))


def _no_preference(message, history, topic):
    """해당 선호를 직접 해제하거나 직전 해당 질문에 무관하다고 답한 경우만 인정한다."""
    text = _compact(message)
    clear = r"상관없|아무거나|제한없|제한해제|선호없|선호해제|구분없|다좋|모두좋|둘다좋"
    if re.search(topic, text) and re.search(clear, text) and not re.search(r"없지|해제하지|좋지", text):
        return True
    question = history[-1].get("content", "") if history and history[-1].get("role") == "assistant" else ""
    return bool(re.search(topic, _compact(question)) and re.fullmatch(
        r"(?:상관없(?:어요|어|습니다)?|아무거나(?:요)?|다좋아요|둘다좋아요)[.!?]?", text))


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
        music_rejected = _term_rejected("음악", message) or _explicit_removal("음악", message)
        if category in {"국악", "클래식", "콘서트"} and music_rejected:
            return False
        if category == "전체" and (music_rejected or any(
                _term_rejected(word, message) or _explicit_removal(word, message)
                for words in _CATEGORY_WORDS.values() for word in words)):
            return False
        for word in _CATEGORY_WORDS.get(category, ()):
            if _term_rejected(word, message) or _explicit_removal(word, message):
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
    if _term_rejected(value, message):
        return False
    if re.search(escaped + _PARTICLES + r"출발" + _PARTICLES
                 + r"(?:하지|안|못|아니|아닌|아닙|싫|불가|말고|하면안|해선안|해서는안)", text):
        return False
    if "출발" in text:
        return bool(re.search(escaped + r"(?:에서|부터)?출발|출발(?:지는|지|은|장소는|점은)?" + escaped, text))
    # 질문이 없는 단답 지명은 목적지일 수도 있으므로 출발지로 확정하지 않는다.
    question = history[-1].get("content", "") if history and history[-1].get("role") == "assistant" else ""
    return bool(re.search(r"출발(?:지|할|하|은|이|은|지를|할\s*곳)?", question))


def _free_matches(value, message, draft, history):
    """명시된 무료 조건과 해제만 인정하며 질문 맥락 없는 반대 값은 막는다."""
    text = re.sub(r"\s+", "", message)
    if re.search(r"(?:아니|아닌|아닙).*(?:아니|아닌|아닙)", text):
        return False
    if value:
        if _term_rejected("무료", message):
            return False
        if re.search(r"무료(?:만|로만|로)?(?:는|은|을|를)?(?:해제|제한해제|제한없)", text):
            return False
        if re.search(r"무료(?:인)?(?:전시|공연|행사|체험|축제|관람)?(?:만|로)?(?:는|은|을|를)?(?:보여주|추천하|찾아주|보고싶)지(?:마|말|않)", text):
            return False
        if re.search(r"유료(?:도|라도)(?:괜찮|좋|돼|가능)(?!지않|지못|은아니)", text):
            return False
        return bool(re.search(r"무료(?:만|로만|로|인것만|만요|요|(?:인)?(?:전시|공연|행사|체험|축제|관람))|돈(?:은|이)?안(?:드는|들|내는)", text))
    if re.search(r"유료(?:도|라도)(?:괜찮|좋|돼|가능)(?:지않|지못|은아니)", text):
        return False
    if re.search(r"무료(?:만|로만)(?:보여|찾아|추천|원해)", text):
        return False
    if re.search(r"유료(?:도|라도)(?:괜찮|좋|돼|가능)|무료(?:만)?(?:는|은)?(?:아니|아닌|아닙|말고|해제)|무료제한(?:없|해제)", text):
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
    compact = _compact(message)
    def released(term):
        """제외의 해제와 해제하지 말라는 발화를 구분한다."""
        prefix = re.escape(_compact(term)) + _PARTICLES
        if re.search(prefix + r"제외(?:를|을|조건)?(?:해제하지|해제하면안)", compact):
            return False
        return bool(re.search(prefix + r"(?:제외(?:를|을|조건)?해제|제외하지(?:마|말|않)|빼지(?:마|말|않)|"
                              r"빼면안|빼서는안|제외하면안|제외해서는안|다시포함)", compact))
    for term in previous:
        if term in value:
            continue
        if not released(term):
            return False
    for term in value:
        if released(term):
            return False
        if term not in previous:
            prefix = re.escape(_compact(term)) + _PARTICLES
            if not re.search(prefix + r"(?:빼|제외|피해|피하|싫|말고|안가|가지마)", compact):
                return False
    return True


def _keywords_match(value, message, draft):
    """관심어 추가에는 긍정 근거, 삭제에는 해당 항목 또는 관심어 전체의 명시 해제를 요구한다."""
    previous = draft.get("keywords") if isinstance(draft.get("keywords"), list) else []
    compact = _compact(message)
    # 단순한 '전시 좋아'나 다른 조건의 해제는 기존 관심어를 삭제할 근거가 아니다.
    clear = bool(re.search(r"(?:^|[.!?,])(?:이제)?(?:관심어|키워드)(?:조건|제한)?" + _PARTICLES
                           + r"(?:모두|전부|전체)?(?:빼|지워|삭제|해제|없애)", compact))
    if re.search(_REMOVAL_PROHIBITED, compact):
        clear = False
    if not value and not previous:
        return clear
    for term in previous:
        if term not in value and not (clear or _explicit_removal(term, message)):
            return False
    for term in value:
        if _term_rejected(term, message) or _explicit_removal(term, message) or clear:
            return False
        if term not in previous and _compact(term) not in compact:
            return False
    return True


def _environment_matches(value, message, history):
    """실내외 후보를 직접 언급·거절·선호 해제와 대조한다. 모호하면 확정하지 않는다."""
    if value == "any":
        return (_no_preference(message, history, r"실내|실외|야외")
                and not any(_term_rejected(word, message) for word in ("실내", "실외", "야외")))
    terms = {"indoor": ("실내",), "outdoor": ("실외", "야외")}
    compact = _compact(message)
    mentioned = {kind for kind, words in terms.items()
                 if any(word in compact and not _term_rejected(word, message) for word in words)}
    rejected = any(_term_rejected(word, message) for word in terms[value])
    return mentioned == {value} and not rejected and not _no_preference(message, history, r"실내|실외|야외")


def _request_kind_matches(value, message, history):
    """한 곳과 코스 요청의 명시 수량·표현을 대조하고 반대·복합 요청은 보류한다."""
    kind = "course" if value == "route" else value
    terms = {"place": ("한곳", "1곳", "한군데", "1군데", "한장소", "행사하나", "한개"),
             "course": ("코스", "두곳", "2곳", "두군데", "2군데", "여러곳", "여러장소", "동선", "루트")}
    compact = _compact(message)
    mentioned = {item for item, words in terms.items()
                 if any(word in compact and not _term_rejected(word, message)
                        and not _explicit_removal(word, message) for word in words)}
    rejected = any(_term_rejected(word, message) or _explicit_removal(word, message) for word in terms[kind])
    # 한 곳/두 곳을 직접 묻는 질문에는 짧은 수량 답도 허용한다.
    question = history[-1].get("content", "") if history and history[-1].get("role") == "assistant" else ""
    if not mentioned and re.search(r"한\s*곳|두\s*곳|코스", question):
        if re.fullmatch(r"(?:하나|한개)(?:만|요|로)?[.!?]?", compact):
            mentioned = {"place"}
        elif re.fullmatch(r"(?:두개|둘)(?:만|요|로)?[.!?]?", compact):
            mentioned = {"course"}
    return mentioned == {kind} and not rejected


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
            valid = _keywords_match(value, message, draft)
            # 모델이 빈 기본값을 덧붙여도 무관한 조건까지 재질문하지 않는다.
            # 해제로 검증되지 않은 무변경 값은 interpreted_fields에도 넣지 않는다.
            if not valid and not value and not draft.get("keywords"):
                continue
        if valid and field in {"category", "categories"}:
            valid = _category_matches(value, message, draft)
        if valid and field == "music_followup" and value:
            valid = "음악" in compact and not (_term_rejected("음악", message) or _explicit_removal("음악", message))
        if valid and field == "indoor_outdoor":
            valid = _environment_matches(value, message, history)
        if valid and field == "request_kind":
            valid = _request_kind_matches(value, message, history)
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
