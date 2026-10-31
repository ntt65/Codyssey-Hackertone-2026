/**
 * 화면 이동과 S00 시작 · S01 홈 · S07 내 나들이.
 * #/ = S00, #/home = S01, #/chat = S02(대화 안 S02a·S03), #/place/<id> = S04, #/map/<id> = S08, #/me = S07
 */
import { pickSeason, startLeaves } from './landing.js';
import { wakeServer } from './api.js';
import { seoulWeather, greetingFor, cachedGreeting } from './weather.js';
import { initChat, renderChat } from './chat.js';
import { initPlace, renderPlace, renderMap } from './place.js';
import { isSignedIn, savedPlaces, endDemo, startDemo } from './saved.js';
import { $, el, button, readStore, writeStore, talkFor, unlockSpeech, speakKo, photo } from './util.js';

/** 까치가 일어나는 모습을 최소한 이만큼은 보여줘요 (너무 빨리 넘어가면 깜빡이는 느낌) */
const MIN_WAKE_MS = 1600;

function route() {
  const full = location.hash.replace(/^#/, '') || '/';
  const [path, query = ''] = full.split('?');
  const [, base = '', rawId] = path.split('/');
  const id = decodeURIComponent(rawId || '');
  const screen = { '': 's00', home: 's01', chat: 's02', search: 's02', place: 's04', map: 's08', me: 's07' }[base] || 's01';
  document.querySelectorAll('.screen').forEach((n) => n.classList.toggle('is-active', n.id === screen));
  document.querySelectorAll('.tab').forEach((tab) => {
    if (tab.dataset.go === `/${base}`) tab.setAttribute('aria-current', 'page');
    else tab.removeAttribute('aria-current');
  });
  $('.tabbar').hidden = !['s01', 's07'].includes(screen);
  if (screen === 's01') renderHome();
  if (screen === 's02') {
    const q = new URLSearchParams(query);
    renderChat({ voice: q.has('voice') ? true : q.has('text') ? false : undefined });
  }
  if (screen === 's04') renderPlace(id);
  if (screen === 's08') renderMap(id);
  if (screen === 's07') renderMe();
  if (screen !== 's02') window.scrollTo(0, 0);
}

/**
 * S00 까치 깨우기. 열자마자 서버를 미리 깨우기 시작하고(조용히),
 * 사용자가 까치나 버튼을 누르면 일어나는 모습 → 서버가 답하면 인사로 바꿔요.
 * 서버가 끝내 답하지 않으면 다시 깨우기를 보여줘요 (Mock 으로 넘어가지 않음).
 */
function initLanding() {
  const season = pickSeason();
  startLeaves(document.querySelector('#s00 .leaves'), season === 'none' ? 'autumn' : season, 8);

  const box = document.querySelector('#s00 .wake');
  const img = document.querySelector('#wake-img');
  const title = document.querySelector('#wake-title');
  const sub = document.querySelector('#wake-sub');
  const dots = document.querySelector('#wake-dots');
  const btn = document.querySelector('#wake-btn');
  const bubble = document.querySelector('#wake-bubble');
  const talk = document.querySelectorAll('#s00 [data-talk]');
  let pending = wakeServer();
  const weather = seoulWeather(); // 까치가 먼저 건넬 날씨 인사 (서버 깨우는 동안 같이 받아요)

  const show = (state) => {
    box.dataset.state = state;
    dots.hidden = state !== 'waking';
    bubble.hidden = state !== 'ready';
    talk.forEach((b) => { b.hidden = state !== 'ready'; });
    btn.hidden = state === 'ready';
    btn.disabled = state === 'waking';
    if (state === 'sleep' || state === 'tired') {
      img.src = 'assets/kkachi-sleep.png';
      img.alt = '빨간 목도리를 두른 까치가 단풍 가지에서 자고 있어요';
    }
    if (state === 'sleep') {
      title.textContent = '까치가 아직 자고 있어요';
      sub.innerHTML = '톡 눌러서 깨워 주세요.<br>깨우면 오늘 나들이를 같이 찾아요.';
      btn.textContent = '까치 깨우기';
      btn.className = 'btn btn--primary';
    }
    if (state === 'waking') {
      img.src = 'assets/kkachi-wake.png';
      img.alt = '까치가 날개를 펴고 기지개를 켜고 있어요';
      title.textContent = '까치가 기지개를 켜고 있어요';
      sub.innerHTML = '잠깐만 기다려 주세요.<br>처음엔 30초~1분쯤 걸릴 수 있어요.';
      btn.textContent = '일어나는 중…';
      btn.className = 'btn btn--secondary';
    }
    if (state === 'tired') {
      title.textContent = '까치가 아직 못 일어났어요';
      sub.innerHTML = '연결이 늦어지고 있어요.<br>다시 깨워 보거나, 조금 뒤에 다시 와 주세요.';
      btn.textContent = '다시 깨우기';
      btn.className = 'btn btn--primary';
    }
    if (state === 'ready') {
      img.src = 'assets/kkachi-hello.png';
      img.alt = '까치가 날개를 흔들며 인사해요';
      title.textContent = '';
      sub.textContent = '';
    }
    title.hidden = state === 'ready';
    sub.hidden = state === 'ready';
  };

  const wake = async () => {
    if (box.dataset.state === 'waking' || box.dataset.state === 'ready') return;
    if (box.dataset.state === 'tired') pending = wakeServer();
    unlockSpeech(); // 누른 순간에 소리를 열어 둬야 폰에서도 인사를 읽어 줘요
    show('waking');
    const [ok] = await Promise.all([pending, new Promise((r) => setTimeout(r, MIN_WAKE_MS))]);
    show(ok ? 'ready' : 'tired');
    if (ok) {
      const g = greetingFor(await weather);
      bubble.textContent = g.text;
      talkFor(document.querySelector('#s00 .wake__bird'), 4200);
      speakKo(g.text);
    }
  };

  document.querySelectorAll('#s00 [data-wake]').forEach((el) => el.addEventListener('click', wake));
  show('sleep');
}


/** 저장한 장소 카드 (홈 미리보기·내 나들이) */
function savedCard(p) {
  const art = el('article', 'saved-card');
  art.append(photo(p, 'saved-card__img'));
  const body = el('div', 'saved-card__body');
  body.append(el('h3', null, p.title), el('p', 'muted', p.venue || ''));
  if ((p.checks_required || []).length) body.append(el('p', 'chat-card__warn', `! ${p.checks_required[0]}`));
  const b = button('장소 정보 보기', 'btn btn--outline btn--small');
  b.dataset.go = `/place/${encodeURIComponent(p.id)}`;
  body.append(b);
  art.append(body);
  return art;
}

/** S01: 저장이 있을 때만 미리보기 (D06) */
function renderHome() {
  const list = savedPlaces();
  $('#s01 [data-signed-in]').hidden = !isSignedIn();
  $('#home-saved').hidden = !list.length;
  $('#home-saved-list').replaceChildren(...list.slice(0, 1).map(savedCard));
  talkFor($('#home-bird'), 2200);
  // 까치가 먼저 말을 걸어요: 날씨 한 줄 (못 받으면 기본 문구 그대로)
  const say = $('#home-say');
  const apply = (g) => { say.textContent = g.short ? `${g.short} 하고 싶은 나들이를 편하게 말해 주세요.` : '하고 싶은 나들이를 편하게 말해 주세요.'; $('#home-weather-credit').hidden = !g.short; };
  apply(cachedGreeting());
  seoulWeather().then((w) => apply(greetingFor(w)));
}

/** S07 내 나들이 */
function renderMe() {
  const list = savedPlaces();
  const signed = isSignedIn();
  $('#me-count').textContent = signed ? `이 브라우저에 저장한 장소 ${list.length}곳` : '아직 체험을 시작하지 않았어요';
  $('#me-empty').hidden = list.length > 0;
  $('#me-empty-text').textContent = signed ? '아직 저장한 장소가 없어요. 까치와 이야기하고 마음에 드는 곳을 저장해 보세요.'
    : '로그인 없이 쓸 수 있어요. 장소를 저장하고 싶을 때 체험을 시작하면 돼요.';
  $('#me-start').hidden = signed;
  $('#me-list').replaceChildren(...list.map(savedCard));
  $('#me-end').hidden = !signed;
  $('#me-note').hidden = true;
}

function initMe() {
  $('#me-start').addEventListener('click', () => {
    if (!startDemo()) { meNote('체험을 시작하지 못했어요. 브라우저 저장이 막혀 있는지 확인해 주세요.'); return; }
    renderMe();
  });
  $('#me-end').addEventListener('click', () => { $('#sheet-end').hidden = false; });
  $('#end-cancel').addEventListener('click', () => { $('#sheet-end').hidden = true; });
  $('#end-confirm').addEventListener('click', () => {
    $('#sheet-end').hidden = true;
    const ok = endDemo();
    renderMe();
    meNote(ok ? '체험을 끝내고 저장한 장소를 모두 지웠어요.' : '지우지 못했어요. 저장한 장소는 그대로 있어요. 다시 시도해 주세요.');
  });
  document.addEventListener('demo-changed', () => { if ($('#s07').classList.contains('is-active')) renderMe(); });
}

function meNote(t) { const n = $('#me-note'); n.textContent = t; n.hidden = false; }

/** data-go 가 붙은 버튼을 누르면 해당 화면으로 이동해요. */
function initNavigation() {
  document.addEventListener('click', (e) => {
    const target = e.target.closest('[data-go]');
    if (target && !target.disabled) {
      if (target.dataset.go.startsWith('/chat')) unlockSpeech();
      location.hash = target.dataset.go;
    }
  });
  window.addEventListener('hashchange', route);
}

initNavigation();
initChat();
initPlace();
initMe();
initLanding();
route();
