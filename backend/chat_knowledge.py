"""v3 대화의 허용 개념과 실제 조회 능력. 운영·요금·장소 사실을 포함하지 않는다.

이 목록은 자연어의 동의어 사전이 아니다. 의미 해석은 모델이 하고 코드는 타입과
실행 경계만 검사한다. 새 공급자·모델·인증 의존성을 만들지 않는다.
"""

VERSION = 1
ACTS = {"inform", "answer", "explain_question", "correct", "complain", "proceed",
        "request_alternatives", "chitchat"}
OPERATIONS = {"add", "replace", "remove"}
STRENGTHS = {"hard", "soft", "unspecified"}
DIMENSIONS = {"atmosphere", "genre", "subject", "activity", "companion", "pace", "other"}
SERVICES = {
    "any": {"label": "나들이", "action": "explore", "query": "문화행사"},
    "performance": {"label": "공연", "action": "explore", "query": "공연"},
    "exhibition": {"label": "전시", "action": "explore", "query": "전시"},
    "movie": {"label": "영화", "action": "search_places", "query": "영화관"},
    "walk": {"label": "산책", "action": "search_places", "query": "공원"},
    "cafe": {"label": "카페", "action": "search_places", "query": "카페"},
    "food": {"label": "식사", "action": "search_places", "query": "음식점"},
    "experience": {"label": "체험", "action": "explore", "query": "체험"},
    "travel": {"label": "나들이", "action": "search_places", "query": "관광명소"},
}
GENRES = {"전시", "전체", "국악", "클래식", "콘서트", "연극"}
CONDITION_FIELDS = {"start_query", "date", "date_from", "date_to", "start_at", "end_at",
                    "category", "categories", "request_kind", "stay_minutes", "free_only",
                    "budget_krw", "keywords", "exclude_terms", "walking_preference", "indoor_outdoor"}
SERVICE_FIELDS = {"category", "categories", "keywords", "music_followup"}
ROUTING_FIELDS = {"goal", "text", "description", "service", "activity", "category", "categories", "request_kind"}
FIELD_LABELS = {"start_query": "출발 지역", "start_location": "출발 위치", "date": "날짜",
                "date_from": "시작 날짜", "date_to": "마지막 날짜", "start_at": "시작 시각",
                "end_at": "종료 시각", "free_only": "무료 조건", "budget_krw": "관람 예산",
                "category": "공연·전시 분류", "categories": "관심 분류"}
MAX_ACTS = 8
MAX_UPDATES = 16
MAX_PREFERENCES = 16
MAX_HYPOTHESES = 16


def capability(service):
    """허용된 활동의 실행 능력 복사본을 반환한다. 미지원 개념은 열린 탐색으로 남긴다."""
    return dict(SERVICES.get(service, SERVICES["any"]))
