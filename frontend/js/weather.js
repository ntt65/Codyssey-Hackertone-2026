/**
 * 날씨 인사. 서울의 지금 날씨를 Open-Meteo(무료, 키 없음)에서 받아 까치가 먼저 건넬 말을 코드가 정해요.
 * 날씨를 못 받으면 기본 인사로 말해요 (날씨를 지어내지 않아요).
 * 출처 표시: 날씨 데이터 © Open-Meteo (CC BY 4.0)
 */
const URL_SEOUL = 'https://api.open-meteo.com/v1/forecast?latitude=37.5665&longitude=126.978&current=temperature_2m,weather_code&timezone=Asia%2FSeoul';
const CACHE_KEY = 'lab678_weather';
const CACHE_MS = 30 * 60 * 1000;
export const DEFAULT_GREETING = '안녕하세요. 오늘은 나들이가 어떠세요?';

/** WMO 날씨 코드 → 말 */
function sky(code) {
  if (code === 0) return { kind: 'clear', word: '맑고' };
  if (code <= 2) return { kind: 'clear', word: '구름이 조금 있고' };
  if (code === 3) return { kind: 'cloudy', word: '흐리고' };
  if (code === 45 || code === 48) return { kind: 'cloudy', word: '안개가 끼었고' };
  if (code >= 51 && code <= 57) return { kind: 'rain', word: '이슬비가 내리고' };
  if ((code >= 61 && code <= 67) || (code >= 80 && code <= 82)) return { kind: 'rain', word: '비가 오고' };
  if ((code >= 71 && code <= 77) || code === 85 || code === 86) return { kind: 'snow', word: '눈이 오고' };
  if (code >= 95) return { kind: 'storm', word: '천둥번개가 치고' };
  return null;
}

/**
 * 날씨에 맞는 인사말 (코드가 정해요)
 * @param {{temp:number, code:number}|null} w
 * @returns {{text:string, short:string}} text: 까치 첫 인사, short: 홈에 붙일 한 줄
 */
export function greetingFor(w) {
  const s = w && sky(w.code);
  if (!s || typeof w.temp !== 'number') return { text: DEFAULT_GREETING, short: '' };
  const t = Math.round(w.temp);
  const now = `오늘 서울은 ${s.word} ${t}도예요.`;
  let tip;
  if (s.kind === 'rain' || s.kind === 'storm') tip = '우산 챙기시고, 실내 전시나 공연 나들이는 어떠세요?';
  else if (s.kind === 'snow') tip = '길이 미끄러우니 가까운 실내 나들이는 어떠세요?';
  else if (t >= 30) tip = '더우니 시원한 실내 전시 나들이는 어떠세요?';
  else if (t <= 0) tip = '많이 추워요. 따뜻하게 입으시고 가까운 곳으로 나들이 어떠세요?';
  else if (s.kind === 'clear') tip = '나들이 가기 좋은 날이에요. 오늘은 나들이가 어떠세요?';
  else tip = '오늘은 가까운 곳으로 나들이가 어떠세요?';
  return { text: `안녕하세요. ${now} ${tip}`, short: now };
}

/** 서울 지금 날씨. 5초 안에 못 받으면 null. 30분 동안은 저장해 둔 값을 써요. */
export async function seoulWeather() {
  try {
    const c = JSON.parse(sessionStorage.getItem(CACHE_KEY) || 'null');
    if (c && Date.now() - c.at < CACHE_MS) return c.w;
  } catch { /* 무시 */ }
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), 5000);
  try {
    const r = await fetch(URL_SEOUL, { signal: ctrl.signal });
    if (!r.ok) return null;
    const cur = (await r.json()).current || {};
    const w = { temp: cur.temperature_2m, code: cur.weather_code };
    if (typeof w.temp !== 'number' || typeof w.code !== 'number') return null;
    try { sessionStorage.setItem(CACHE_KEY, JSON.stringify({ at: Date.now(), w })); } catch { /* 무시 */ }
    return w;
  } catch {
    return null;
  } finally {
    clearTimeout(timer);
  }
}

/** 이미 받아 둔 날씨로 바로 인사말 만들기 (없으면 기본 인사) */
export function cachedGreeting() {
  try {
    const c = JSON.parse(sessionStorage.getItem(CACHE_KEY) || 'null');
    return greetingFor(c && Date.now() - c.at < CACHE_MS ? c.w : null);
  } catch {
    return greetingFor(null);
  }
}
