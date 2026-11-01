/**
 * 여러 화면이 같이 쓰는 작은 도구: 요소 만들기, 날짜·시각 표시, 저장소 읽기/쓰기.
 */

export const $ = (sel, root = document) => root.querySelector(sel);
export const $$ = (sel, root = document) => root.querySelectorAll(sel);

/**
 * 텍스트만 안전하게 넣는 요소 생성기
 * @param {string} tag
 * @param {string} [className]
 * @param {string} [text]
 */
export function el(tag, className, text) {
  const n = document.createElement(tag);
  if (className) n.className = className;
  if (text != null) n.textContent = text;
  return n;
}

/** 버튼 하나 만들기 */
export function button(label, className = 'btn btn--outline', onClick) {
  const b = el('button', className, label);
  b.type = 'button';
  if (onClick) b.addEventListener('click', onClick);
  return b;
}

/** "HH:MM" → 분 */
export const minutes = (t) => { const [h, m] = t.split(':').map(Number); return h * 60 + m; };

/** 분 → "HH:MM" */
export const hhmm = (min) => `${String(Math.floor(min / 60)).padStart(2, '0')}:${String(min % 60).padStart(2, '0')}`;

/** 오늘 날짜 "YYYY-MM-DD" (한국 시간) */
export function todayIso(offsetDays = 0) {
  const d = new Date(Date.now() + 9 * 3600e3 + offsetDays * 864e5);
  return d.toISOString().slice(0, 10);
}

/** "2026-10-31" → "10월 31일 (토)" */
export function formatDate(iso) {
  const d = new Date(`${iso}T00:00:00+09:00`);
  const w = '일월화수목금토'[d.getDay()];
  return `${d.getMonth() + 1}월 ${d.getDate()}일 (${w})`;
}

/** "14:00" → "오후 2시" / "14:30" → "오후 2시 30분" */
export function formatTime(t) {
  const [h, m] = t.split(':').map(Number);
  const ap = h < 12 ? '오전' : '오후';
  const hh = ((h + 11) % 12) + 1;
  return m ? `${ap} ${hh}시 ${m}분` : `${ap} ${hh}시`;
}

/** "2026-10-31T06:27:57+09:00" → "10월 31일 06:27 기준" */
export function checkedAt(iso) {
  if (!iso) return '';
  const d = new Date(iso);
  const p = (n) => String(n).padStart(2, '0');
  return `${d.getMonth() + 1}월 ${d.getDate()}일 ${p(d.getHours())}:${p(d.getMinutes())} 기준`;
}

/** localStorage 읽기. 막혀 있거나 깨졌으면 fallback */
export function readStore(key, fallback = null) {
  try {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : fallback;
  } catch {
    return fallback;
  }
}

/** localStorage 쓰기. 실패하면 false (성공처럼 보이지 않게) */
export function writeStore(key, value) {
  try {
    if (value == null) localStorage.removeItem(key);
    else localStorage.setItem(key, JSON.stringify(value));
    return true;
  } catch {
    return false;
  }
}

/** 시험 모드: ?mode=recorded 또는 ?debug */
export const isTest = () => {
  const q = new URLSearchParams(location.search);
  return q.get('mode') === 'recorded' || q.has('debug');
};
export const isDebug = () => new URLSearchParams(location.search).has('debug');

/** 까치가 말하는 동안 움직이게 (말풍선이 나올 때) */
export function talkFor(node, ms) {
  if (!node) return;
  node.classList.add('is-talking');
  clearTimeout(node._talkTimer);
  node._talkTimer = setTimeout(() => node.classList.remove('is-talking'), ms);
}

/**
 * 읽어 주기 준비. 폰 브라우저는 사용자가 누른 순간에 한 번 열어 둬야 나중에 소리를 내요.
 * 버튼 클릭 처리 안에서 불러 주세요.
 */
export function unlockSpeech() {
  try {
    if (!('speechSynthesis' in window)) return;
    const u = new SpeechSynthesisUtterance(' ');
    u.volume = 0;
    speechSynthesis.speak(u);
  } catch { /* 소리 없이도 글자는 보여요 */ }
}

/**
 * 한국어로 읽어 주기. 실패해도 화면 글자는 그대로예요.
 * @param {string} text
 */
export function speakKo(text) {
  try {
    if (!('speechSynthesis' in window)) return;
    speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.lang = 'ko-KR';
    u.rate = 1.3; // 1.1에서 1.2배 더 빠르게 (11/1)
    const ko = speechSynthesis.getVoices().find((v) => v.lang?.startsWith('ko'));
    if (ko) u.voice = ko;
    speechSynthesis.speak(u);
  } catch { /* 무시 */ }
}

/** 장르 → 유형 아이콘 (Figma 03 · UI Kit "아이콘 · 까치 스타일 2D") */
export function typeIcon(genre = '') {
  const g = String(genre);
  if (/전시|미술/.test(g)) return 'exhibition';
  if (/전통|역사/.test(g)) return 'historic-visit';
  if (/축제/.test(g)) return 'festival-event';
  if (/교육|체험/.test(g)) return 'hands-on';
  if (/연극|국악|클래식|콘서트|뮤지컬|오페라|무용|독주|독창|공연|영화/.test(g)) return 'performance';
  return 'default';
}

/**
 * 행사 사진. 서울시 문화포털 공식 이미지가 있으면 그걸, 없거나 안 열리면 행사 유형 아이콘을 보여줘요.
 * @param {object} c 후보
 * @param {string} className 감싸는 요소 클래스
 */
export function photo(c, className) {
  const box = el('div', `${className} photo`);
  const img = el('img');
  img.loading = 'lazy';
  img.alt = c.title ? `${c.title} 공식 이미지` : '';
  const note = el('span', 'photo__note');
  const fallback = () => {
    img.onerror = null;
    img.src = `assets/icons/type-${typeIcon(c.genre)}.png`;
    img.alt = '';
    box.classList.add('is-icon');
    note.textContent = '공식 사진 없음';
  };
  if (c.image_url) {
    img.src = c.image_url;
    img.referrerPolicy = 'no-referrer';
    img.onerror = fallback;
    note.textContent = '사진 · 서울시 문화포털';
  } else fallback();
  box.append(img, note);
  return box;
}
