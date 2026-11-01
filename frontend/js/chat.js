/**
 * S02 까치와 대화 · S02a 부족·충돌 확인 · S03 대화 안 추천 카드 (PRD v0.7 H02~H10).
 *
 * 흐름: 사용자 말/글 → 조건 해석(/preview/chat, 없으면 규칙 해석) → 빠진 것만 하나씩 질문
 *       → 다 모이면 확인 단계 없이 바로 추천 → 대화 안에 카드 최대 3개 → 상세 보기.
 * 이미 정한 값과 다른 말이 오면 변경 전후를 물어봐요. 좌표는 장소 검색·현재 위치로만 정해요.
 */
import { state, save, resetChat } from './state.js';
import { requestRecommend, requestChat, searchPlaces } from './api.js';
import { parseUtterance, longEnough } from './parse.js';
import { $, el, button, formatDate, formatTime, todayIso, minutes, hhmm, isTest, isDebug, talkFor, unlockSpeech, photo, SPEECH_RATE } from './util.js';

const QA_START = { label: '청량리역', lat: 37.5805961, lng: 127.0482573 };
/**
 * 고르는 버튼 (Figma UI Kit 유형 아이콘과 같은 묶음, 11/1 희영 결정).
 * 서버는 전시·국악·클래식·콘서트·연극·전체만 받아서, 공연·체험·축제는 "전체"로 받고 코드가 장르 이름으로 골라요.
 * "국악 듣고 싶어요"처럼 세부 장르로 말하면 그 장르만 찾아요.
 */
const CATEGORIES = [['전시', '전시'], ['공연', '공연'], ['체험', '체험·배우기'], ['축제', '축제·행사'], ['전체', '아무거나 좋아요']];
const CATEGORY_LABEL = { 전시: '전시', 공연: '공연', 체험: '체험·배우기', 축제: '축제·행사', 전체: '아무거나' };
const GROUP = {
  공연: /국악|클래식|콘서트|연극|뮤지컬|오페라|무용|독주|독창|공연|영화/,
  체험: /교육|체험/,
  축제: /축제/,
};
/** 서버에 보낼 분류 (묶음은 전체로) */
const serverCategory = (cat) => (GROUP[cat] ? '전체' : cat);
/** 묶음 분류면 장르 이름으로 골라요 */
const inGroup = (cat, c) => !GROUP[cat] || GROUP[cat].test(c.genre || '');
const FIELD_NAME = { startLocation: '출발지', date: '날짜', time: '시간', category: '보고 싶은 것' };
const MAX_CARDS = 3;
let ticket = 0;
let busy = false;
let placeOptions = [];
let recognizer = null;
let voiceMode = false; // 말로 대화 화면이면 까치가 질문한 뒤 다시 들어요
let discardVoice = false;

/* ---------------- 조건 ---------------- */

const d = () => state.draft;

/** 받침에 맞는 조사: josa('날짜', '을', '를') → '날짜를' */
function josa(word, withBatchim, without) {
  const ch = [...String(word)].reverse().find((c) => c >= '가' && c <= '힣');
  if (!ch) return word + without;
  const jong = (ch.charCodeAt(0) - 0xac00) % 28;
  if (withBatchim === '으로') return word + (jong && jong !== 8 ? '으로' : '로');
  return word + (jong ? withBatchim : without);
}

/** 아직 안 정해진 조건 중 먼저 물어볼 것 */
function missing() {
  if (!d().category) return 'category';
  if (!d().date) return 'date';
  if (!d().startTime || !d().endTime) return 'time';
  if (!d().startLocation) return 'startLocation';
  return null;
}

/** 조건 요약 한 줄: "청량리역 · 11월 1일 (일) · 오후 2시–오후 5시 · 전시" */
function summary() {
  const parts = [];
  if (d().startLocation) parts.push(d().startLocation.label);
  if (d().date) parts.push(formatDate(d().date));
  if (d().startTime && d().endTime) parts.push(`${formatTime(d().startTime)}–${formatTime(d().endTime)}`);
  if (d().category) parts.push(CATEGORY_LABEL[d().category] || d().category);
  return parts.join(' · ');
}

/** 값 하나 바꾸기. 추천을 한 번 받은 뒤 이미 있던 값이 바뀌면 바로 덮지 않고 확인해요 (S02a 충돌). */
function patch(changes) {
  const searched = !!state.lastRequest;
  const conflicts = [];
  for (const [k, v] of Object.entries(changes)) {
    if (v == null || v === '') continue;
    const before = d()[k];
    const same = JSON.stringify(before) === JSON.stringify(v);
    if (same) continue;
    if (searched && before != null && k !== 'startQuery') conflicts.push({ field: k, before, after: v });
    else d()[k] = v;
  }
  if (conflicts.length) state.pending = conflicts[0];
  save();
}

const show = (field, v) => {
  if (v == null) return '';
  if (field === 'startLocation') return v.label;
  if (field === 'date') return formatDate(v);
  if (field === 'startTime' || field === 'endTime') return formatTime(v);
  if (field === 'category') return CATEGORY_LABEL[v] || String(v);
  return String(v);
};

/* ---------------- 대화 그리기 ---------------- */

/** 까치 말 추가 (소리 켜짐이면 읽어 줘요) */
function say(text, extra = {}) {
  const { ask, ...keep } = extra;
  state.messages.push({ role: 'ai', text, ...keep });
  save();
  render();
  speak(text, ask && voiceMode ? () => listen(true) : null);
}

function userSays(text) {
  state.messages.push({ role: 'user', text });
  save();
  render();
}

/** 대화 안 추천 카드 */
function card(c, index) {
  const art = el('article', 'chat-card');
  art.dataset.id = c.id;
  const top = photo(c, 'chat-card__img');
  const meta = [c.genre?.split('/')[0], c.district, c.fee_type].filter(Boolean).join(' · ');
  const body = el('div', 'chat-card__body');
  body.append(el('p', 'chat-card__meta', `${index + 1} · ${meta || '문화행사'}`), el('h3', null, c.title), el('p', 'muted', c.venue || '장소 이름 확인 필요'));
  body.append(el('p', 'chat-card__dist', c.distance_km != null ? `출발지에서 직선 약 ${c.distance_km}km` : '거리 확인 필요'));
  const warns = [];
  if (!c.opening_info) warns.push('운영시간 확인 필요');
  if (!c.price_info && c.fee_type !== '무료') warns.push('가격 확인 필요');
  (c.checks_required || []).slice(0, 1).forEach((t) => warns.push(t));
  if (warns.length) body.append(el('p', 'chat-card__warn', `! ${warns.join(' · ')}`));
  if (isDebug()) body.append(el('code', 'debug-id', `후보 ID: ${c.id}`));
  const more = button('상세 보기', 'btn btn--outline btn--small');
  more.dataset.go = `/place/${encodeURIComponent(c.id)}`;
  body.append(more);
  art.append(top, body);
  return art;
}

function bubble(m) {
  const row = el('div', `msg msg--${m.role}`);
  if (m.role === 'ai') {
    const av = el('div', 'msg__avatar');
    const img = el('img');
    img.src = 'assets/kkachi-face.png';
    img.alt = '';
    av.append(img);
    row.append(av);
  }
  const col = el('div', 'msg__col');
  col.append(el('span', 'msg__who', m.role === 'ai' ? '나들이 친구 까치' : '내가 한 말'));
  if (m.text) col.append(el('p', 'msg__bubble', m.text));
  if (m.summary) col.append(el('p', 'msg__summary', m.summary));
  if (m.cards?.length) {
    const list = el('div', 'chat-cards');
    m.cards.forEach((id, i) => { const c = state.candidates[id]; if (c) list.append(card(c, i)); });
    col.append(list);
  }
  if (m.loading) {
    const dots = el('span', 'loading__dots msg__dots');
    dots.append(el('i'), el('i'), el('i'));
    col.append(dots);
  }
  row.append(col);
  return row;
}

/** 아래 빠른 답 버튼: 지금 물어보는 것에 맞춰 바뀌어요 */
function actions() {
  const box = $('#chat-actions');
  box.replaceChildren();
  const chip = (label, fn, cls = 'chip') => box.append(button(label, cls, fn));
  if (busy) return;
  const last = state.messages[state.messages.length - 1];
  if (last?.retry) { chip('같은 조건으로 다시 찾기', () => search()); return; }
  if (last?.music && !state.pending) {
    ['국악', '클래식', '콘서트'].forEach((c) => chip(c, () => answer(c, { category: c })));
    chip('골고루 좋아요', () => answer('골고루 좋아요', { category: '공연' }));
    return;
  }
  if (state.pending) {
    const p = state.pending;
    chip(`${josa(show(p.field, p.after), '으로')} 바꾸기`, () => resolvePending(true), 'chip chip--primary');
    chip(`${show(p.field, p.before)} 유지`, () => resolvePending(false));
    return;
  }
  const need = missing();
  if (need === 'category') CATEGORIES.forEach(([c, label]) => chip(label, () => answer(label, { category: c })));
  else if (need === 'date') {
    chip('오늘', () => answer('오늘이요', { date: todayIso(0) }));
    chip('내일', () => answer('내일이요', { date: todayIso(1) }));
    chip('모레', () => answer('모레요', { date: todayIso(2) }));
  } else if (need === 'time') {
    const now = new Date(Date.now() + 9 * 3600e3);
    const n = Math.min(now.getUTCHours() * 60 + Math.ceil(now.getUTCMinutes() / 30) * 30, 20 * 60);
    if (d().date === todayIso()) chip('지금부터 3시간', () => answer('지금부터 3시간이요', { startTime: hhmm(n), endTime: hhmm(Math.min(n + 180, 23 * 60)) }));
    chip('오후 2시–5시', () => answer('오후 2시부터 5시까지요', { startTime: '14:00', endTime: '17:00' }));
    chip('오전 10시–12시', () => answer('오전 10시부터 12시까지요', { startTime: '10:00', endTime: '12:00' }));
  } else if (need === 'startLocation') {
    placeOptions.forEach((p) => chip(p.label, () => answer(`${p.label}에서 출발해요`, { startLocation: { label: p.label, lat: p.lat, lng: p.lng } })));
    chip('현재 위치 사용', useHere, 'chip chip--primary');
    if (isTest()) chip('QA 고정: 청량리역', () => answer('청량리역에서 출발해요', { startLocation: QA_START }));
  } else if (state.shown.length) {
    chip('다른 곳 보여줘', () => { userSays('다른 곳도 보여줘'); other(); });
    chip('더 가까운 곳', () => { userSays('더 가까운 곳으로 알려줘'); closer(); });
    chip('새로 이야기하기', () => { resetChat(); start(); }, 'chip chip--ghost');
  }
}

function render() {
  const log = $('#chat-log');
  log.replaceChildren(...state.messages.map(bubble));
  $('#chat-cond').textContent = summary() ? `지금 조건 · ${summary()}` : '';
  $('#chat-cond').hidden = !summary();
  actions();
  updateVoiceUi();
  if (recognizer && voiceMode) log.append(liveBubble());
  scrollEnd();
}

/** 맨 아래 말풍선이 아래 고정 버튼 위에 보이도록 끝까지 내려요 */
function scrollEnd() {
  requestAnimationFrame(() => requestAnimationFrame(() => {
    window.scrollTo({ top: document.documentElement.scrollHeight, behavior: 'smooth' });
  }));
}

/** 아래 고정 영역(빠른 답·말하기·입력)의 실제 높이만큼 대화 아래 여백을 둬요 (폰마다 높이가 달라요) */
function watchBottom() {
  const bottom = $('#s02 .chat__bottom');
  const apply = () => $('#s02').style.setProperty('--chat-bottom', `${Math.ceil(bottom.getBoundingClientRect().height)}px`);
  apply();
  if ('ResizeObserver' in window) new ResizeObserver(() => { apply(); }).observe(bottom);
  window.addEventListener('resize', apply);
}

/** 말로 대화 중 들리는 말을 대화 맨 아래에 바로바로 보여주는 말풍선 */
function liveBubble() {
  let row = $('#live-bubble');
  if (row) return row;
  row = el('div', 'msg msg--user msg--live');
  row.id = 'live-bubble';
  const col = el('div', 'msg__col');
  col.append(el('span', 'msg__who', '내가 한 말 · 듣는 중'), el('p', 'msg__bubble', '…'));
  row.append(col);
  return row;
}

/* ---------------- 소리 (까치가 읽어 줘요) ---------------- */

/**
 * 까치 말 읽기. 다 읽고 나면 then 실행 (말로 대화 중 다음 듣기). 소리를 끄면 잠깐 뒤 실행.
 * 까치가 말하는 동안에는 마이크를 켜지 않아요 (자기 목소리를 다시 듣지 않게).
 */
function speak(text, then) {
  const avatar = [...document.querySelectorAll('#chat-log .msg--ai .msg__avatar')].pop(); // 방금 말한 까치
  const ms = Math.min(600 + text.length * 70, 5000);
  talkFor(avatar, ms);
  const talkMs = state.sound ? Math.max(ms, 1500 + text.length * 120) : ms;
  talkFor($('#listen-bird'), talkMs);
  talkFor($('#float-bird'), talkMs);
  if (!state.sound || !('speechSynthesis' in window)) { if (then) setTimeout(then, 1200); return; }
  try {
    const busy = speechSynthesis.speaking || speechSynthesis.pending; // 홈 인사를 읽던 중이면
    speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.lang = 'ko-KR';
    u.rate = SPEECH_RATE;
    const ko = speechSynthesis.getVoices().find((v) => v.lang?.startsWith('ko'));
    if (ko) u.voice = ko;
    let done = false;
    const finish = () => {
      if (done) return;
      done = true;
      if (!then) return;
      // 폰은 읽기가 끝나기 전에 끝났다고 알려 주기도 해요. 정말 조용해질 때까지 기다렸다가 마이크를 켜요.
      const wait = (tries) => {
        if (speechSynthesis.speaking && tries < 60) { setTimeout(() => wait(tries + 1), 250); return; }
        setTimeout(then, 700);
      };
      wait(0);
    };
    u.onend = finish;
    u.onerror = finish;
    setTimeout(finish, 1500 + text.length * 180); // onend 가 안 오는 브라우저 대비
    // 끊은 직후 바로 말하면 Chrome이 첫 인사를 버리기도 해서 (홈 인사 → 대화 첫 인사) 잠깐 쉬었다 말해요
    if (busy) setTimeout(() => speechSynthesis.speak(u), 150);
    else speechSynthesis.speak(u);
  } catch { if (then) setTimeout(then, 1200); }
}

function setSound(on) {
  state.sound = on;
  save();
  const b = $('#chat-sound');
  b.setAttribute('aria-pressed', String(on));
  b.textContent = on ? '소리 켬' : '소리 끔';
  if (!on && 'speechSynthesis' in window) speechSynthesis.cancel();
}

/* ---------------- 말하기 ----------------
 * 말로 대화(voice): 까치와 "음성을 듣고 있어요" 화면이 위에 있고, 대화가 아래로 이어져요.
 *   까치가 질문하면 다 읽은 뒤 자동으로 다시 들어요. 아래 큰 버튼: 말하기 / 말하기 마치기.
 * 글자로 대화(text): 채팅 화면. 마이크를 누르면 그 자리에서 듣고, 끝나면 바로 보내요.
 */

/** 화면 모드 바꾸기 */
function setMode(mode) {
  state.mode = mode;
  voiceMode = mode === 'voice';
  save();
  $('#s02').dataset.mode = mode;
  if (mode === 'text' && recognizer) { discardVoice = true; session?.finish('discard'); }
  if (state.messages.length) render(); // 까치 모양(전신·얼굴)을 모드에 맞게
  else updateVoiceUi();
}

/** 듣는 중/아님에 따라 상태 문구와 버튼 바꾸기 */
function updateVoiceUi() {
  const on = !!recognizer;
  $('#chat-mic').classList.toggle('is-listening', on);
  $('#chat-mic').setAttribute('aria-label', on ? '듣는 중 · 누르면 보내요' : '말하기');
  $('#voice-main').classList.toggle('is-listening', on);
  $('#voice-main-label').textContent = on ? '말하기 마치기' : '말하기';
  $('#voice-wave').hidden = !on;
  $('#listen-bird').classList.toggle('is-listening', on); // 듣는 중엔 귀 기울이듯 움직여요
  $('#float-bird').classList.toggle('is-listening', on);
  $('#listen-status').textContent = on ? '음성을 듣고 있어요 · 말씀이 끝나고 잠시 조용하면 보내요' : (busy ? '까치가 찾고 있어요' : '아래 "말하기"를 누르고 말씀해 주세요');
  $('#listen-status').classList.toggle('is-idle', !on);
  $('#chat-input').placeholder = on && !voiceMode ? '듣고 있어요… 말씀이 끝나면 마이크를 다시 눌러 주세요' : '글자로 적어도 돼요';
}

/**
 * 인식 결과 합치기. 안드로이드 Chrome 은 같은 말을 누적해서 여러 번 보내요
 * ("안녕하세요" → "안녕하세요 오늘은" …). 앞 조각을 포함하는 조각이 오면 바꿔 끼우고, 이미 있는 조각은 버려요.
 */
function joinResults(results) {
  const merge = (parts, t) => {
    const prev = parts[parts.length - 1];
    const flat = (x) => x.replace(/\s+/g, '');
    if (prev && flat(t).startsWith(flat(prev))) parts[parts.length - 1] = t;
    else if (prev && flat(prev).includes(flat(t))) { /* 이미 있음 */ } else parts.push(t);
  };
  const fins = [];
  const mids = [];
  for (const r of results) {
    const t = (r[0]?.transcript || '').trim();
    if (!t) continue;
    merge(r.isFinal ? fins : mids, t);
  }
  let fin = fins.join(' ');
  let mid = mids.join(' ');
  if (mid && fin && mid.replace(/\s+/g, '').startsWith(fin.replace(/\s+/g, ''))) { fin = ''; } // 중간 결과가 확정 결과를 이미 포함
  return { fin, mid };
}

/**
 * 마이크가 까치 말(스피커 소리)을 받아 적은 것인지. 소리를 켰을 때만,
 * 들은 말이 까치의 마지막 말 안에 그대로 이어져 있으면 메아리로 봐요 (사용자 말이 예시와 비슷한 건 통과).
 */
function isEcho(text) {
  if (!state.sound) return false;
  const lastAi = [...state.messages].reverse().find((m) => m.role === 'ai' && m.text)?.text || '';
  const flat = (x) => x.replace(/[^가-힣0-9a-zA-Z]/g, '');
  const t = flat(text);
  return t.length >= 6 && flat(lastAi).includes(t);
}

/**
 * 음성 시간 설정 (민규·동조 요청, 10/31). 주소에 ?endms=5000&nospeechms=12000 처럼 붙이면 시험해 볼 수 있어요.
 * endOfSpeechMs: 마지막 말 뒤 이만큼 조용하면 말이 끝난 것으로 보고 보내요 (말 사이 쉬는 시간은 기다려요)
 * noSpeechMs: 듣기 시작 뒤 아무 말도 없으면 이만큼 기다렸다가 끝내요
 * maxAutoTurns: 까치 질문 뒤 자동으로 다시 듣는 횟수 (넘으면 "말하기"를 눌러야 해요)
 */
const q = new URLSearchParams(location.search);
const num = (name, fallback, lo, hi) => { const v = Number(q.get(name)); return v >= lo && v <= hi ? v : fallback; };
export const VOICE = {
  endOfSpeechMs: num('endms', 4000, 1000, 15000),
  noSpeechMs: num('nospeechms', 10000, 5000, 60000),
  maxTalkMs: 60000,
  maxAutoTurns: 5,
};
let autoTurns = 0;
let session = null;

/**
 * 듣기 시작. 브라우저가 짧게 끊어도 다시 이어 듣고, 우리 타이머로만 끝내요.
 * @param {boolean} auto 까치 질문 뒤 자동으로 듣는 경우
 */
function listen(auto = false) {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) { say('이 브라우저에서는 말하기를 쓸 수 없어요. 아래 칸에 글자로 적어 주세요.'); if (voiceMode) setMode('text'); return; }
  if (recognizer || busy || !$('#s02').classList.contains('is-active')) return;
  if (auto) {
    if (autoTurns >= VOICE.maxAutoTurns) { updateVoiceUi(); return; }
    autoTurns += 1;
  } else autoTurns = 0;
  if (auto && 'speechSynthesis' in window && speechSynthesis.speaking) { setTimeout(() => listen(true), 400); autoTurns -= 1; return; } // 까치가 말하는 중엔 켜지 않아요
  if ('speechSynthesis' in window) speechSynthesis.cancel();
  discardVoice = false;
  const s = session = { kept: '', finalText: '', interim: '', done: false, timers: {}, startedAt: Date.now() };
  const text = () => `${s.kept} ${s.finalText} ${s.interim}`.replace(/\s+/g, ' ').trim();
  const clear = () => Object.values(s.timers).forEach(clearTimeout);
  const show = () => {
    const t = text();
    if (voiceMode) { const live = $('#live-bubble .msg__bubble'); if (live) live.textContent = t || '…'; }
    else $('#chat-input').value = t;
  };
  s.finish = (reason) => {
    if (s.done) return;
    s.done = true;
    clear();
    const eng = recognizer;
    recognizer = null;
    try { eng?.stop(); } catch { /* 이미 멈춤 */ }
    $('#live-bubble')?.remove();
    updateVoiceUi();
    const said = text();
    if (discardVoice || reason === 'discard') { if (said && !voiceMode) $('#chat-input').value = said; return; }
    if (reason === 'denied') { say('마이크를 쓸 수 없어요. 글자로 적어 주셔도 돼요.'); setMode('text'); return; }
    if (!said) { say('잘 듣지 못했어요. "말하기"를 누르고 다시 말씀해 주세요.'); return; }
    if (!voiceMode) $('#chat-input').value = '';
    handle(said);
  };
  const begin = () => {
    const eng = new SR();
    recognizer = eng;
    eng.lang = 'ko-KR';
    eng.interimResults = true;
    eng.continuous = true;
    eng.onresult = (e) => {
      const { fin, mid } = joinResults(e.results);
      if (isEcho(`${fin} ${mid}`)) return; // 까치 목소리를 마이크가 다시 들은 것이면 무시
      s.finalText = fin;
      s.interim = mid;
      show();
      clearTimeout(s.timers.noSpeech);
      clearTimeout(s.timers.quiet);
      s.timers.quiet = setTimeout(() => s.finish('quiet'), VOICE.endOfSpeechMs); // 마지막 말 뒤 4초 조용하면 보내요
    };
    eng.onerror = (e) => {
      if (e.error === 'not-allowed' || e.error === 'service-not-allowed') s.finish('denied');
      // no-speech·network 등은 onend 에서 다시 이어 들어요 (끝내는 건 우리 타이머)
    };
    eng.onend = () => {
      if (s.done || recognizer !== eng) return;
      if (s.stopping) { s.finish('user'); return; } // 말하기 마치기: 마지막 글자까지 받고 보내요
      // 브라우저가 스스로 끊으면, 들은 말을 보관하고 다시 이어 들어요
      s.kept = `${s.kept} ${s.finalText} ${s.interim}`.trim();
      s.finalText = '';
      s.interim = '';
      setTimeout(() => { if (!s.done) { try { begin(); } catch { s.finish('end'); } } }, 150);
    };
    eng.start();
  };
  updateVoiceUi();
  if (voiceMode) { $('#chat-log').append(liveBubble()); scrollEnd(); }
  s.timers.noSpeech = setTimeout(() => { if (!text()) s.finish('nospeech'); }, VOICE.noSpeechMs);
  s.timers.max = setTimeout(() => s.finish('max'), VOICE.maxTalkMs);
  try { begin(); } catch { recognizer = null; s.done = true; clear(); updateVoiceUi(); }
}

/** 말하기 마치기: 지금까지 들은 말만 바로 보내요 */
function stopListening() {
  if (!session || session.done) return;
  session.stopping = true;
  try { recognizer?.stop(); } catch { /* 무시 */ }
  setTimeout(() => session?.finish('user'), 800); // 브라우저가 늦으면 그때까지 들은 말로 보내요
}

/** 글자로 입력하기: 채팅 화면으로. 듣던 말은 입력 칸에 넣어 고칠 수 있게 */
function toText() {
  const live = $('#live-bubble .msg__bubble')?.textContent;
  discardVoice = true;
  session?.finish('discard');
  setMode('text');
  if (live && live !== '…') $('#chat-input').value = live;
  setTimeout(() => $('#chat-input').focus(), 200);
}

/* ---------------- 해석 ---------------- */

/** 서버 대화 API 형식 ↔ 화면 조건 */
function toServerDraft() {
  const out = { request_kind: 'place' };
  if (d().startLocation) out.start_location = d().startLocation;
  if (d().category) out.category = serverCategory(d().category);
  if (d().date && d().startTime) out.start_at = `${d().date}T${d().startTime}:00+09:00`;
  if (d().date && d().endTime) out.end_at = `${d().date}T${d().endTime}:00+09:00`;
  return out;
}

function fromServerDraft(sd) {
  const out = {};
  if (sd.category) out.category = sd.category;
  if (sd.start_at) { out.date = sd.start_at.slice(0, 10); out.startTime = sd.start_at.slice(11, 16); }
  if (sd.end_at) out.endTime = sd.end_at.slice(11, 16);
  if (sd.start_location?.lat != null) out.startLocation = sd.start_location;
  if (sd.start_query && !sd.start_location) out.startQuery = sd.start_query;
  return out;
}

/** 문장 해석: AI 대화 API 가 있으면 쓰고, 없으면 규칙 해석 */
async function interpret(text) {
  const history = state.messages.slice(-7, -1).filter((m) => m.text)
    .map((m) => ({ role: m.role === 'ai' ? 'assistant' : 'user', content: m.text.slice(0, 1000) }));
  try {
    const r = await requestChat({ message: text, condition_draft: toServerDraft(), confirmed_fields: [], revision: state.revision, conversation_context: history });
    if (r.kind === 'ok') {
      state.revision += 1;
      const p = fromServerDraft(r.data.updated_condition_draft);
      // 서버 AI 는 공연·체험·축제 묶음을 몰라서 "전체"로 줄 수 있어요. 문장에 묶음 말이 있으면 그걸 써요.
      const local = parseUtterance(text).category;
      if (GROUP[local] && (!p.category || p.category === '전체')) p.category = local;
      if (r.data.music_followup || r.data.updated_condition_draft?.music_followup) p.ask = r.data.assistant_text;
      return p;
    }
  } catch { /* 규칙 해석으로 */ }
  const p = parseUtterance(text);
  if (p.useHere) p.useHere = true;
  return p;
}

/** 사용자 한마디 처리 */
async function handle(text) {
  if (busy) return;
  userSays(text);
  // 결과 뒤 짧은 요청
  if (state.shown.length && /다른\s*(곳|데)|딴\s*데/.test(text) && !/에서 출발/.test(text)) { other(); return; }
  if (state.shown.length && /가까운/.test(text)) { closer(); return; }
  busy = true;
  render();
  const p = await interpret(text);
  busy = false;
  const { useHere: here, startQuery, ask, ...changes } = p;
  patch(changes);
  if (ask) { say(ask, { ask: true, music: true }); return; } // AI 가 음악 종류를 되물을 때
  if (here) { await useHere(); return; }
  if (startQuery && !d().startLocation) { await findStart(startQuery); return; }
  if (startQuery && state.lastRequest) { await findStart(startQuery, true); return; }
  if (!Object.keys(changes).length && !startQuery) {
    if (/^(네|응|좋아|그래)/.test(text) && !missing()) { next(); return; }
    // 출발지를 물어본 상태라면 짧은 답("개포동")도 출발지 이름으로 봐요 (QA-03 P1)
    const asked = lastQuestion();
    if (asked === 'startLocation' && !d().startLocation) {
      const name = placeName(text);
      if (name) { await findStart(name); return; }
    }
    say(nothingUnderstood(asked), { ask: !!asked });
    return;
  }
  next();
}

/** 까치가 바로 앞에 물어본 것 (출발지·날짜·시간·관심사) — 결과를 보여준 뒤면 null */
function lastQuestion() {
  const lastAi = [...state.messages].reverse().find((m) => m.role === 'ai');
  if (!lastAi || lastAi.cards) return null;
  return missing();
}

/** 단답에서 장소 이름만 남기기: "개포동이요" → "개포동" */
function placeName(text) {
  const t = text.replace(/[.!?~,]/g, ' ').trim()
    .replace(/(에서\s*)?(출발(할게요|해요|합니다)?|이요|이에요|예요|요|입니다)$/u, '').trim();
  if (!t || t.length > 30 || /^(몰라|글쎄|아무|음+|어+)/.test(t)) return null;
  return t;
}

/** 알아듣지 못했을 때: 묻던 게 있으면 그 질문을 다시, 결과 뒤라면 할 수 있는 것을 안내 */
function nothingUnderstood(asked) {
  const hints = {
    startLocation: '어디에서 출발하시는지 동네나 역 이름으로 말씀해 주세요. 예: "개포동", "청량리역". 아래 "현재 위치 사용"을 눌러도 돼요.',
    date: '언제 가실지 알려 주세요. 예: "오늘", "내일", "11월 2일".',
    time: '몇 시부터 몇 시까지인지 알려 주세요. 예: "오후 2시부터 5시까지".',
    category: '어떤 걸 보고 싶으세요? 전시, 공연, 체험, 축제 중에서 골라 주세요.',
  };
  if (asked && hints[asked]) return `제가 잘 알아듣지 못했어요. ${hints[asked]}`;
  if (state.shown.length) return '다른 곳을 더 보여 드릴까요, 아니면 시간이나 보고 싶은 것, 출발지를 바꿔 볼까요? 바꾸실 내용을 말씀해 주세요.';
  if (!state.messages.some((m) => m.role === 'user' && m !== state.messages[state.messages.length - 1])) {
    return '어떤 나들이를 하고 싶으세요? 예를 들어 "내일 오후 2시부터 5시까지 전시 보고 싶어요"처럼 말씀해 주세요.';
  }
  return '저는 문화 나들이를 찾아 드리는 까치예요. 보고 싶은 것이나 시간, 출발할 곳을 알려 주시면 찾아볼게요.';
}

/** 빠른 답 버튼 */
function answer(text, changes) {
  userSays(text);
  patch(changes);
  next();
}

/** 출발지 이름 → 장소 검색 → 사용자가 고르면 확정 */
async function findStart(query, changing = false) {
  busy = true;
  say(`${josa(`"${query}"`, '을', '를')} 찾아볼게요.`);
  const r = await searchPlaces(query).catch(() => ({ kind: 'error' }));
  busy = false;
  if (r.kind === 'ready' && r.places.length) {
    placeOptions = r.places.slice(0, 3);
    if (changing) state.pending = null;
    if (changing) d().startLocation = null;
    save();
    say('어디에서 출발하실지 아래에서 골라 주세요.');
    return;
  }
  placeOptions = [];
  say(r.kind === 'no_results' ? '그 이름으로는 찾지 못했어요. 다른 이름으로 말씀하시거나, 현재 위치를 써 주세요.'
    : '지금은 장소 이름으로 출발지를 찾을 수 없어요. 아래 "현재 위치 사용"을 눌러 주세요.');
}

/** 현재 위치 (사용자가 직접 골랐을 때만 권한 요청) */
async function useHere() {
  if (!navigator.geolocation) { say('이 기기에서는 현재 위치를 쓸 수 없어요. 출발할 곳 이름을 말씀해 주세요.'); return; }
  busy = true;
  render();
  navigator.geolocation.getCurrentPosition((pos) => {
    busy = false;
    patch({ startLocation: { label: '현재 위치', lat: pos.coords.latitude, lng: pos.coords.longitude } });
    userSays('현재 위치에서 출발할게요');
    next();
  }, () => {
    busy = false;
    say('위치를 확인하지 못했어요. 출발할 곳 이름(예: 청량리역)을 말씀해 주세요.');
  }, { timeout: 10000, maximumAge: 60000 });
}

/** 바꿀지 확인 응답 */
function resolvePending(accept) {
  const p = state.pending;
  state.pending = null;
  if (accept) d()[p.field] = p.after;
  save();
  userSays(accept ? `${josa(show(p.field, p.after), '으로')} 바꿔 주세요` : `${show(p.field, p.before)} 그대로 둘게요`);
  if (accept) search();
  else say('알겠어요. 원래 조건은 그대로 두었어요.');
}

/** 다음에 할 말: 확인 → 빠진 것 질문 → 60분 확인 → 추천 */
function next() {
  if (state.pending) {
    const p = state.pending;
    const name = FIELD_NAME[p.field] || (p.field.includes('Time') ? '시간' : p.field);
    say(`${josa(name, '을', '를')} ${show(p.field, p.before)}에서 ${josa(show(p.field, p.after), '으로')} 바꿀까요? 다른 조건은 그대로 둘게요.`);
    return;
  }
  const need = missing();
  if (need === 'category') { say('어떤 걸 보고 싶으세요? 전시, 공연, 체험·배우기, 축제·행사 중에서 골라 주셔도 돼요.', { ask: true }); return; }
  if (need === 'date') { say('언제 가실 건가요?', { ask: true }); return; }
  if (need === 'time') { say('몇 시부터 몇 시까지 시간이 되세요?', { ask: true }); return; }
  if (!longEnough(d().startTime, d().endTime) || minutes(d().endTime) <= minutes(d().startTime)) {
    d().endTime = null;
    save();
    say('나들이 시간은 최소 1시간 이상으로 설정해 주세요. 몇 시까지 시간이 되세요?', { ask: true });
    return;
  }
  if (need === 'startLocation') { say('어디에서 출발하세요? 출발할 곳 이름을 말씀하시거나 현재 위치를 써 주세요.', { ask: true }); return; }
  search();
}

/* ---------------- 추천 ---------------- */

function requestBody() {
  return {
    request_kind: 'place',
    start_location: d().startLocation,
    start_at: `${d().date}T${d().startTime}:00+09:00`,
    end_at: `${d().date}T${d().endTime}:00+09:00`,
    category: serverCategory(d().category),
  };
}

/** 조건이 다 모이면 확인 단계 없이 바로 찾아요 */
async function search() {
  const mine = ++ticket;
  busy = true;
  const body = requestBody();
  state.messages.push({ role: 'ai', text: `${summary()} 조건으로 찾아볼게요.`, loading: true });
  save();
  render();
  const res = await requestRecommend(body);
  if (mine !== ticket) return; // 늦게 온 이전 응답은 버려요
  busy = false;
  const last = state.messages[state.messages.length - 1];
  if (last?.loading) delete last.loading;
  if (res.kind === 'need_input') {
    if (res.field === 'end_at' || res.code === 'minimum_duration') d().endTime = null;
    save();
    say(res.message);
    return;
  }
  if (res.kind === 'error') { say(`${res.message}`, { retry: true }); return; }
  state.lastRequest = body;
  state.sourceCheckedAt = res.data.source_checked_at || null;
  const list = (res.data.candidates || []).filter((c) => inGroup(d().category, c)); // 공연·체험·축제는 장르로 골라요
  if (!list.length) {
    state.pool = [];
    say('조건에 맞는 곳을 찾지 못했어요. 날짜나 시간, 보고 싶은 것을 바꿔 말씀해 주시면 다시 찾아볼게요.');
    return;
  }
  // 출발지에서 가까운 순서로 (서버는 받은 순서대로 줘요)
  list.sort((a, b) => (a.distance_km ?? 1e9) - (b.distance_km ?? 1e9));
  list.forEach((c) => { state.candidates[c.id] = c; });
  state.pool = list.map((c) => c.id);
  showCards(state.pool.slice(0, MAX_CARDS), distanceText(state.pool.slice(0, MAX_CARDS), list.length));
}

/**
 * 추천 안내 문구. 직선 거리 범위를 그대로 말하고, 멀면 멀다고 알려요 (QA-03 P2).
 * 직선 거리는 걷는 거리·이동시간이 아니에요.
 */
function distanceText(ids, total) {
  const ds = ids.map((id) => state.candidates[id]?.distance_km).filter((v) => v != null);
  const n = ids.length;
  const head = `${total > n ? `찾은 ${total}곳 중 ` : ''}출발지에서 직선 거리가 짧은 순서로 ${n}곳을 골랐어요.`;
  if (!ds.length) return `${head} 운영시간과 예약은 꼭 다시 확인해 주세요.`;
  const lo = Math.min(...ds), hi = Math.max(...ds);
  const range = lo === hi ? `직선 약 ${lo}km` : `직선 약 ${lo}~${hi}km`;
  if (lo > 5) return `${head} 다만 가장 가까운 곳도 직선 약 ${lo}km 떨어져 있어요 (보여 드린 곳 ${range}). 더 가까운 곳을 원하시면 보고 싶은 것을 "아무거나"로 넓히거나 날짜·출발지를 바꿔 말씀해 주세요.`;
  return `${head} (${range}) 운영시간과 예약은 꼭 다시 확인해 주세요.`;
}

function showCards(ids, text) {
  state.shown.push(...ids.filter((id) => !state.shown.includes(id)));
  state.messages.push({ role: 'ai', text, cards: ids, summary: summary() });
  save();
  render();
  speak(text);
}

/** 다른 곳: 같은 조건으로 아직 안 본 곳. 없으면 다시 찾아보고, 그래도 없으면 지금 카드 유지 (D07·D08) */
async function other() {
  const fresh = state.pool.filter((id) => !state.shown.includes(id));
  if (fresh.length) { showCards(fresh.slice(0, MAX_CARDS), '같은 조건으로 다른 곳을 골랐어요.'); return; }
  if (!state.lastRequest) { next(); return; }
  busy = true;
  render();
  const res = await requestRecommend(state.lastRequest);
  busy = false;
  if (res.kind === 'ready') {
    res.data.candidates.forEach((c) => { state.candidates[c.id] = c; });
    const more = res.data.candidates.filter((c) => inGroup(d().category, c)).sort((a, b) => (a.distance_km ?? 1e9) - (b.distance_km ?? 1e9))
      .map((c) => c.id).filter((id) => !state.shown.includes(id));
    state.pool.push(...more.filter((id) => !state.pool.includes(id)));
    if (more.length) { showCards(more.slice(0, MAX_CARDS), '같은 조건으로 새로 찾은 곳이에요.'); return; }
  }
  say(res.kind === 'error' ? '새로 찾지 못했어요. 위에 보여 드린 곳은 그대로 둘게요.' : '같은 조건으로 더 찾은 곳이 없어요. 위에 보여 드린 곳은 그대로 둘게요.', res.kind === 'error' ? { retry: false } : {});
}

/** 더 가까운 곳: 받은 후보 중 출발지에서 가까운 순 */
function closer() {
  const lastCards = [...state.messages].reverse().find((m) => m.cards)?.cards || [];
  const byDist = state.pool.map((id) => state.candidates[id]).filter((c) => c?.distance_km != null)
    .sort((a, b) => a.distance_km - b.distance_km).map((c) => c.id);
  const top = byDist.slice(0, MAX_CARDS);
  if (!top.length || top.every((id) => lastCards.includes(id))) {
    say('지금 보여 드린 곳이 이 조건에서 가장 가까운 곳이에요. 출발지를 바꾸시면 다시 찾아볼게요.');
    return;
  }
  showCards(top, '출발지에서 가까운 순서로 다시 골랐어요.');
}

/* ---------------- 시작 ---------------- */

/** 새 대화 첫 인사 */
function start() {
  if (!state.messages.length) {
    say('안녕하세요. 나들이 가고 싶은 곳 편히 말씀해 주세요.', { ask: true });
  } else render();
}

/** #/chat 들어올 때 */
export function renderChat(opts = {}) {
  if (opts.voice != null) setSound(opts.voice);
  else setSound(state.sound);
  const mode = opts.voice === true ? 'voice' : opts.voice === false ? 'text' : (state.mode || 'text');
  setMode(mode);
  const fresh = !state.messages.length;
  start();
  if (mode === 'voice' && !fresh) setTimeout(() => listen(), 300); // 처음이면 인사를 다 읽은 뒤 자동으로 들어요
  if (mode === 'text' && opts.voice === false) $('#chat-input').focus();
}

/** 이벤트 연결 (한 번) */
export function initChat() {
  watchBottom();
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(([e]) => $('#float-bird').classList.toggle('is-shown', !e.isIntersecting), { threshold: 0.15 })
      .observe($('#listen-bird'));
  }
  $('#chat-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const v = $('#chat-input').value.trim();
    if (!v) return;
    $('#chat-input').value = '';
    handle(v);
  });
  $('#chat-mic').addEventListener('click', () => { unlockSpeech(); if (recognizer) stopListening(); else listen(); });
  $('#voice-main').addEventListener('click', () => { unlockSpeech(); if (recognizer) stopListening(); else listen(); });
  $('#voice-to-text').addEventListener('click', toText);
  window.addEventListener('hashchange', () => { if (recognizer) { discardVoice = true; session?.finish('discard'); } });
  $('#chat-sound').addEventListener('click', () => { unlockSpeech(); setSound(!state.sound); });
  $('#chat-new').addEventListener('click', () => { resetChat(); placeOptions = []; start(); });
}
