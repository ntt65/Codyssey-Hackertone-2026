"""행사 문의 전화번호. 서울시 문화포털 행사 상세 페이지의 '문의' 칸에서 번호만 읽어 와요.

서울시 문화행사 API에는 전화번호 칸이 없어서, 공식 상세 페이지(HMPG_ADDR)를 그대로 읽어요.
번호를 찾지 못하면 지어내지 않고 no_results로 답해요.
"""
import html
import re
from urllib.parse import parse_qs, urlsplit
from urllib.request import Request, urlopen

DETAIL_HOST = "culture.seoul.go.kr"
DETAIL_PATH = "/culture/culture/cultureEvent/view.do"
PHONE = re.compile(r"(?<!\d)(0\d{1,2}-\d{3,4}-\d{4}|1\d{3}-\d{4})(?!\d)")
# '문의' 바로 뒤에 이어지는 번호 묶음만 (예: "문의 070-8680-8477 / 02-337-3103")
INQUIRY = re.compile(r"문의\s*:?\s*((?:(?:0\d{1,2}-\d{3,4}-\d{4}|1\d{3}-\d{4})\s*[/,]?\s*)+)")
_cache = {}


def detail_code(url):
    """공식 상세 페이지 주소에서 행사 번호(cultcode)만 꺼내요. 다른 주소면 None."""
    parts = urlsplit(url or "")
    if parts.scheme not in ("http", "https") or parts.hostname != DETAIL_HOST or parts.path != DETAIL_PATH:
        return None
    code = parse_qs(parts.query).get("cultcode", [""])[0]
    return code if code.isdigit() else None


def phones_from_page(page):
    """상세 페이지 HTML에서 첫 '문의' 칸의 전화번호들을 순서대로 (중복 없이) 돌려줘요."""
    text = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", page)))
    block = INQUIRY.search(text)
    if not block:
        return []
    found = []
    for number in PHONE.findall(block.group(1)):
        if number not in found:
            found.append(number)
    return found


def event_contact(data):
    """POST /preview/contact {url} → (status, body). body.phones: 문의 전화번호 목록."""
    code = detail_code(data.get("url"))
    if not code:
        return 400, dict(status="need_input", message="서울시 문화포털 행사 주소를 확인해 주세요.")
    if code not in _cache:
        url = f"https://{DETAIL_HOST}{DETAIL_PATH}?cultcode={code}&menuNo=200008"
        request = Request(url, headers={"User-Agent": "Mozilla/5.0 (lab678 oneul-nadeuli)"})
        with urlopen(request, timeout=8) as response:
            _cache[code] = phones_from_page(response.read(400_000).decode("utf-8", "replace"))
    phones = _cache[code]
    if not phones:
        return 200, dict(status="no_results", message="공식 안내에 문의 전화번호가 없어요.")
    return 200, dict(status="ready", phones=phones)
