/**
 * 백엔드 API 호출. 실패해도 Mock 후보로 바꾸지 않고, 결과 종류를 그대로 구분해서 돌려줘요.
 * 계약: docs/development/recommend-api.md, docs/development/place-search-api.md
 */

/**
 * API 주소. index.html 의 <meta name="lab678-api"> 값(Render https 주소)을 써요.
 * 내 PC(localhost)에서는 같은 주소(개발 서버 프록시)로 불러요.
 */
const LOCAL = ['localhost', '127.0.0.1'].includes(location.hostname);
const API_BASE = LOCAL ? '' : (document.querySelector('meta[name="lab678-api"]')?.content || '').replace(/\/$/, '');

/**
 * 서버 깨우기. 무료 Render 는 쉬면 잠들어서 첫 응답이 30초~1분 걸려요.
 * 내 PC 에서는 개발 서버 프록시라 바로 준비됨으로 봐요.
 * @param {number} timeoutMs
 * @returns {Promise<boolean>} 준비되면 true, 시간이 지나도 응답이 없으면 false
 */
export async function wakeServer(timeoutMs = 75000) {
  if (LOCAL) return true;
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), timeoutMs);
  try {
    const r = await fetch(`${API_BASE}/healthz`, { signal: ctrl.signal, cache: 'no-store' });
    return r.ok;
  } catch {
    return false;
  } finally {
    clearTimeout(timer);
  }
}

/**
 * 시험 모드: 주소에 ?mode=recorded 를 붙이면 기록 데이터, 없으면 실시간(live).
 * @returns {'recorded'|'live'}
 */
export function testMode() {
  return new URLSearchParams(location.search).get('mode') === 'recorded' ? 'recorded' : 'live';
}

/**
 * JSON POST. 응답이 HTML 오류여도 죽지 않게 본문 파싱 실패를 따로 처리해요.
 * @returns {Promise<{status:number, data:object|null}|null>} 통신 자체가 실패하면 null
 */
async function post(path, body, signal) {
  let res;
  try {
    res = await fetch(`${API_BASE}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
      signal,
    });
  } catch (e) {
    if (e.name === 'AbortError') throw e;
    return null;
  }
  let data = null;
  try { data = await res.json(); } catch { /* HTML 오류 등 */ }
  return { status: res.status, data };
}

/**
 * 추천을 요청해요.
 * @param {object} body request_kind, start_location{label,lat,lng}, start_at, end_at, category
 * @returns {Promise<{kind:'ready'|'no_results'|'need_input'|'error', data?:object, message?:string, field?:string, code?:string}>}
 *   ready: 후보 있음 · no_results: 0건 · need_input: 입력 오류(400, field 가 있으면 해당 칸) · error: 서버·네트워크 오류
 */
export async function requestRecommend(body) {
  const r = await post('/preview/recommend', { ...body, mode: testMode() });
  if (!r) return { kind: 'error', message: '인터넷 연결을 확인하고 다시 시도해 주세요.' };
  const { status, data } = r;
  if (status === 200 && data?.status === 'ready') return { kind: 'ready', data };
  if (status === 200 && data?.status === 'no_results') return { kind: 'no_results', data };
  if (status === 400) return { kind: 'need_input', message: data?.message || '입력한 조건을 확인해 주세요.', field: data?.field, code: data?.code };
  return { kind: 'error', message: data?.message || '추천을 불러오지 못했어요. 다시 시도해 주세요.' };
}

/**
 * 출발지를 장소명·주소로 찾아요. 사용자가 결과 중 하나를 골라야 출발지가 정해져요.
 * @param {string} query
 * @param {AbortSignal} signal 새 검색이 시작되면 이전 요청을 취소해요
 * @returns {Promise<{kind:'ready'|'no_results'|'need_input'|'error', places?:object[], message?:string}>}
 */
export async function searchPlaces(query, signal) {
  const r = await post('/preview/places', { query, type: 'keyword' }, signal);
  if (!r) return { kind: 'error', message: '인터넷 연결을 확인하고 다시 찾아 주세요.' };
  const { status, data } = r;
  if (status === 200 && data?.status === 'ready') return { kind: 'ready', places: data.places || [] };
  if (status === 200 && data?.status === 'no_results') return { kind: 'no_results', message: '검색 결과가 없어요. 다른 이름이나 주소로 찾아 주세요.' };
  if (status === 400) return { kind: 'need_input', message: data?.message || '검색어를 확인해 주세요.' };
  if (status === 429) return { kind: 'error', message: '검색이 잠시 몰렸어요. 조금 뒤에 다시 찾아 주세요.' };
  return { kind: 'error', message: '출발지 검색을 지금 쓸 수 없어요. 현재 위치를 쓰거나 잠시 뒤 다시 찾아 주세요.' };
}

/**
 * 대화 해석 (/preview/chat). 서버에 AI 설정이 없거나 오래된 서버면 kind:'unavailable' 로 돌려줘요.
 * 그때는 화면에서 규칙 기반 해석으로 이어가요.
 * @param {object} body message, condition_draft, confirmed_fields, revision, conversation_context
 * @returns {Promise<{kind:'ok'|'unavailable'|'error', data?:object, message?:string}>}
 */
export async function requestChat(body) {
  const r = await post('/preview/chat', body);
  if (!r) return { kind: 'unavailable' };
  const { status, data } = r;
  if (status === 200 && data?.updated_condition_draft) return { kind: 'ok', data };
  if (status === 404 || status === 503 || status === 405) return { kind: 'unavailable' };
  return { kind: 'error', message: data?.message || 'AI 응답을 받지 못했어요.' };
}

/**
 * 도보 경로. 경로 계산이 성공했을 때만 시간·거리를 돌려줘요 (추정값을 만들지 않아요).
 * @param {{lat:number,lng:number}} from
 * @param {{lat:number,lng:number}} to
 * @returns {Promise<{kind:'ready', duration_s:number, distance_m:number, path?:number[][], provider?:string}|{kind:'error', message:string}>}
 */
export async function walkRoute(from, to) {
  const r = await post('/preview/walk', { points: [from, to], details: true });
  if (!r) return { kind: 'error', message: '인터넷 연결을 확인하고 다시 시도해 주세요.' };
  const { status, data } = r;
  if (status === 200 && typeof data?.duration_s === 'number') return { kind: 'ready', ...data };
  return { kind: 'error', message: data?.message || '도보 경로를 확인하지 못했어요. 잠시 후 다시 시도해 주세요.' };
}

/** 지도 설정: 카카오 JavaScript 키(브라우저용, 도메인 제한 키)만 받아요. 실패하면 null */
let mapConfigCache;
export async function mapConfig() {
  if (mapConfigCache !== undefined) return mapConfigCache;
  try {
    const r = await fetch(`${API_BASE}/map-config`);
    mapConfigCache = r.ok ? await r.json() : null;
  } catch { mapConfigCache = null; }
  return mapConfigCache;
}

/**
 * 대중교통 경로 (카카오 대중교통, 조회 시점 기준). 경로를 못 찾으면 시간을 만들지 않아요.
 * @returns {Promise<{kind:'ready', routes:object[], time_basis?:string}|{kind:'no_results'|'error', message:string}>}
 */
export async function transitRoute(from, to) {
  const r = await post('/preview/transit', { points: [from, to] });
  if (!r) return { kind: 'error', message: '인터넷 연결을 확인하고 다시 시도해 주세요.' };
  const { status, data } = r;
  if (status === 200 && data?.status === 'ready' && data.routes?.length) return { kind: 'ready', ...data };
  if (status === 200 && data?.status === 'no_results') return { kind: 'no_results', message: data.message || '이 구간의 대중교통 경로를 찾지 못했어요.' };
  return { kind: 'error', message: data?.message || '대중교통 경로를 확인하지 못했어요. 잠시 후 다시 시도해 주세요.' };
}

/**
 * 행사 문의 전화번호 (서울시 문화포털 상세 페이지의 '문의' 칸)
 * @param {string} url 공식 안내 주소
 * @returns {Promise<string[]>} 번호 목록, 없거나 실패하면 []
 */
export async function eventContact(url) {
  const r = await post('/preview/contact', { url });
  return r?.status === 200 && r.data?.status === 'ready' ? r.data.phones : [];
}
