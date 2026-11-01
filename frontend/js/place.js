/**
 * S04 장소 상세 (지도 보기 = 주 행동, 내 나들이에 저장 = 보조) · S08 지도와 도보 경로 · S06 저장 시트.
 * 대화 카드·상세·지도·저장이 같은 후보 id 를 써요. 확인 안 된 정보는 '확인 필요'로 보여요.
 * 도보 시간은 경로 계산이 성공했을 때만 보여요 (직선 거리를 걷는 시간처럼 쓰지 않아요).
 */
import { state, candidateById } from './state.js';
import { walkRoute, transitRoute, mapConfig } from './api.js';
import { isSignedIn, isSaved, savePlace, startDemo, savedPlaces } from './saved.js';
import { $, el, photo, formatDate, formatTime, checkedAt, isDebug, speakKo, talkFor } from './util.js';

let walkTicket = 0;
let route = null; // 지금 S08 의 출발·도착·도보·대중교통 결과
let pendingSave = null; // 체험 시작 전 저장 요청 1회 보관

/** 대화 후보 또는 저장한 장소에서 찾기 */
export function placeById(id) {
  return candidateById(id) || savedPlaces().find((p) => p.id === id) || null;
}

/** 방문 날짜 한 줄 ("11월 1일 (일) 관람 검토 · 무료") */
function visitLine(c) {
  const r = state.lastRequest;
  const parts = [];
  if (r) parts.push(`${formatDate(r.start_at.slice(0, 10))} ${formatTime(r.start_at.slice(11, 16))}–${formatTime(r.end_at.slice(11, 16))} 관람 검토`);
  if (c.fee_type) parts.push(c.fee_type);
  return parts.join(' · ');
}

/** S04 */
export function renderPlace(id) {
  const c = placeById(id);
  const box = $('#s04-body');
  box.replaceChildren();
  $('#s04-actions').hidden = !c;
  if (!c) {
    box.append(el('h2', null, '장소 정보를 찾을 수 없어요'), el('p', 'muted', '대화로 돌아가서 다시 골라 주세요.'));
    return;
  }
  box.append(photo(c, 'place-hero'));
  if (isSaved(c.id)) box.append(el('p', 'badge badge--ok', '내 나들이에 저장했어요'));
  box.append(el('h2', 'place-title', c.title), el('p', 'muted', c.venue || '장소 이름 확인 필요'));
  const vl = visitLine(c);
  if (vl) box.append(el('p', 'place-visit', vl));
  if (isDebug()) box.append(el('code', 'debug-id', `장소 ID: ${c.id}`));

  const info = el('div', 'info');
  const row = (label, value) => {
    const r = el('div', 'info__row');
    const t = el('div');
    t.append(el('span', 'info__label', label), value ? el('strong', null, value) : el('strong', 'muted', '정보 없음'));
    r.append(t);
    if (!value) r.append(el('span', 'badge badge--warn', '확인 필요'));
    info.append(r);
  };
  row('운영시간', c.opening_info);
  if (c.event_start_date || c.event_end_date) row('행사 기간', `${c.event_start_date || '?'} ~ ${c.event_end_date || '?'}`);
  row('관람료', c.price_info || (c.fee_type === '무료' ? '무료' : null));
  if (c.district) row('지역', c.district);
  row('대상', c.audience);
  row('거리', c.distance_km != null ? `출발지에서 직선 약 ${c.distance_km}km (걷는 시간 아님)` : null);
  box.append(info);

  const checks = c.checks_required || [];
  if (checks.length) {
    const tip = el('div', 'checklist');
    tip.append(el('strong', null, '가기 전에 확인해 주세요'));
    const ul = el('ul');
    checks.forEach((t) => ul.append(el('li', null, t)));
    tip.append(ul);
    box.append(tip);
  }
  if (c.official_url) {
    const a = el('a', 'link-btn', '공식 안내 페이지 보기');
    a.href = c.official_url;
    a.target = '_blank';
    a.rel = 'noopener';
    box.append(a);
  }
  if (c.source_checked_at) box.append(el('p', 'caption muted', `서울시 문화행사 정보 · ${checkedAt(c.source_checked_at)}`));

  $('#s04-map').dataset.go = `/map/${encodeURIComponent(c.id)}`;
  const saveBtn = $('#s04-save');
  saveBtn.dataset.id = c.id;
  const saved = isSaved(c.id);
  saveBtn.textContent = saved ? '내 나들이 보기' : '내 나들이에 저장';
  saveBtn.disabled = false;
  $('#s04-note').hidden = true;
  $('#s04-bye').hidden = true;
}

/* ---------------- 저장 (S06) ---------------- */

function note(text, warn = false) {
  const n = $('#s04-note');
  n.textContent = text;
  n.classList.toggle('is-warn', warn);
  n.hidden = false;
}

/** 저장 실행 1회 */
function doSave(id) {
  const c = placeById(id);
  if (!c) return;
  const r = savePlace(c);
  if (r === 'failed') { note('저장하지 못했어요. 브라우저 저장 공간을 확인하고 다시 눌러 주세요.', true); return; }
  renderPlace(id);
  note(r === 'already' ? '이미 내 나들이에 있어요.' : '내 나들이에 저장했어요. 이 브라우저에서만 볼 수 있어요.');
  if (r === 'saved') sayBye();
}

/** 저장한 뒤 까치가 나와서 배웅해요 */
function sayBye() {
  const bye = $('#s04-bye');
  bye.hidden = false;
  bye.scrollIntoView({ behavior: 'smooth', block: 'center' });
  speakKo(BYE_TEXT);
  talkFor($('#s04-bye-bird'), 2600);
}
const BYE_TEXT = '잘 다녀오세요. 좋은 나들이 되세요!';

function openSheet() { $('#sheet-save').hidden = false; $('#sheet-save .sheet__panel').focus(); }
function closeSheet() { $('#sheet-save').hidden = true; }

/* ---------------- 지도 (S08) ----------------
 * 카카오 지도를 먼저 쓰고(도메인 등록 필요), 불러오지 못하면 OpenStreetMap 지도로 바꿔요.
 * 지도가 바뀌어도 경로 계산 결과(도보 Valhalla, 대중교통 카카오)는 같아요.
 */
const COLORS = { WALKING: '#56616B', BUS: '#2E7D32', SUBWAY: '#1565C0', walk: '#29485B' };
let engine = null; // { kind: 'kakao'|'osm', map, layers: [] }
let kakaoReady = null;

/** 카카오 지도 SDK 불러오기 (한 번). 6초 안에 안 되면 실패로 봐요 */
function loadKakao() {
  if (kakaoReady) return kakaoReady;
  kakaoReady = (async () => {
    const cfg = await mapConfig();
    if (cfg?.provider !== 'kakao' || !cfg.javascript_key) throw new Error('no key');
    await new Promise((resolve, reject) => {
      const s = document.createElement('script');
      s.src = `https://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${encodeURIComponent(cfg.javascript_key)}`;
      const timer = setTimeout(() => reject(new Error('timeout')), 6000);
      s.onload = () => { try { window.kakao.maps.load(() => { clearTimeout(timer); resolve(); }); } catch (e) { clearTimeout(timer); reject(e); } };
      s.onerror = () => { clearTimeout(timer); reject(new Error('blocked')); };
      document.head.append(s);
    });
  })();
  return kakaoReady;
}

/** 지도 준비: 카카오 → 실패하면 OpenStreetMap */
async function getEngine() {
  if (engine) return engine;
  const box = $('#s08-mapbox');
  try {
    await loadKakao();
    const k = window.kakao.maps;
    engine = { kind: 'kakao', map: new k.Map(box, { center: new k.LatLng(37.5665, 126.978), level: 6 }), layers: [] };
    k.event.addListener(engine.map, 'click', () => { if (!$('#s08-mapwrap').classList.contains('is-full')) setBig(true); });
  } catch {
    if (!window.L) throw new Error('no map');
    const map = L.map(box, { zoomControl: false });
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 18, attribution: '© OpenStreetMap' }).addTo(map);
    engine = { kind: 'osm', map, layers: [] };
    map.on('click', () => { if (!$('#s08-mapwrap').classList.contains('is-full')) setBig(true); });
  }
  return engine;
}

/** 지도에 출발·도착과 선들을 그려요. lines: [{ path:[[lat,lng]], color, dashed }] */
function draw(from, to, lines = []) {
  if (!engine) return;
  engine.layers.forEach((l) => (engine.kind === 'kakao' ? l.setMap(null) : l.remove()));
  engine.layers = [];
  const pts = [[to.lat, to.lng], ...(from ? [[from.lat, from.lng]] : []), ...lines.flatMap((l) => l.path)];
  engine.pts = pts;
  if (engine.kind === 'kakao') {
    const k = window.kakao.maps;
    const pin = (p, label, cls) => new k.CustomOverlay({ position: new k.LatLng(p.lat, p.lng), content: `<div class="kpin ${cls}">${label}</div>`, yAnchor: 1.2, map: engine.map });
    engine.layers.push(pin(to, '도착', 'kpin--to'));
    if (from) engine.layers.push(pin(from, '출발', 'kpin--from'));
    lines.forEach((l) => engine.layers.push(new k.Polyline({ map: engine.map, path: l.path.map(([a, b]) => new k.LatLng(a, b)),
      strokeWeight: 6, strokeColor: l.color, strokeOpacity: 0.9, strokeStyle: l.dashed ? 'shortdash' : 'solid' })));
    const bounds = new k.LatLngBounds();
    pts.forEach(([a, b]) => bounds.extend(new k.LatLng(a, b)));
    setTimeout(refit, 60);
    $('#s08-credit').dataset.map = '지도 © Kakao';
  } else {
    const icon = (label, cls) => L.divIcon({ className: `pin ${cls}`, html: `<span>${label}</span>`, iconSize: [56, 32], iconAnchor: [28, 16] });
    engine.layers.push(L.marker([to.lat, to.lng], { icon: icon('도착', 'pin--to') }).addTo(engine.map));
    if (from) engine.layers.push(L.marker([from.lat, from.lng], { icon: icon('출발', 'pin--from') }).addTo(engine.map));
    lines.forEach((l) => engine.layers.push(L.polyline(l.path, { color: l.color, weight: 6, opacity: 0.85, dashArray: l.dashed ? '6 8' : null }).addTo(engine.map)));
    setTimeout(refit, 60);
    $('#s08-credit').dataset.map = '지도 © OpenStreetMap';
  }
}

/** 지도 크기가 바뀐 뒤 다시 맞추기 (출발·도착·경로가 다 보이게) */
function refit() {
  if (!engine?.pts?.length) return;
  if (engine.kind === 'kakao') {
    const k = window.kakao.maps;
    const b = new k.LatLngBounds();
    engine.pts.forEach(([a, c]) => b.extend(new k.LatLng(a, c)));
    engine.map.relayout();
    engine.map.setBounds(b, 40, 40, 40, 40);
  } else {
    engine.map.invalidateSize();
    engine.map.fitBounds(engine.pts, { padding: [40, 40], maxZoom: 16 });
  }
}

/** 지도 크게 보기: 위 상단바는 그대로 두고, 그 아래를 지도로 가득 채워요 (앱 밖으로 나가지 않아요) */
function setBig(on) {
  $('#s08-mapwrap').classList.toggle('is-full', on);
  document.body.classList.toggle('map-full-open', on);
  const info = currentMode === 'transit' && route?.transit?.kind === 'ready'
    ? (() => { const r = route.transit.routes[route.pick] || route.transit.routes[0]; return `대중교통 약 ${Math.round(r.duration_s / 60)}분 · 환승 ${r.transfers}회`; })()
    : $('#s08-result').textContent;
  $('#s08-fullinfo').textContent = [$('#s08-title').textContent, info].filter(Boolean).join('  ·  ');
  setTimeout(refit, 80);
}

/** 출처 표시: 경로 출처만 작고 희미하게. 카카오 지도는 지도 위 로고로 출처가 표시돼서 여기서는 빼요 */
function credit(text) {
  const map = $('#s08-credit').dataset.map;
  $('#s08-credit').textContent = [text, map && !map.includes('Kakao') ? map : ''].filter(Boolean).join(' · ');
}

/** S08 */
export async function renderMap(id) {
  setBig(false);
  const c = placeById(id);
  const from = state.lastRequest?.start_location || null;
  $('#s08-title').textContent = c ? `${from?.label || '출발지'} → ${c.venue || c.title}` : '장소를 찾을 수 없어요';
  $('#s08-back').dataset.go = c ? `/place/${encodeURIComponent(c.id)}` : '/chat';
  $('#s08-error').hidden = true;
  $('#s08-result').textContent = '';
  $('#s08-sub').textContent = '';
  $('#s08-routes').replaceChildren();
  $('#s08-tnote').textContent = '';
  if (!c) return;
  $('#s08-kakao').href = `https://map.kakao.com/link/to/${encodeURIComponent(c.venue || c.title)},${c.lat},${c.lng}`;
  route = { id: c.id, from, to: { lat: c.lat, lng: c.lng }, walk: null, transit: null, pick: 0 };
  setMode('walk');
  try { await getEngine(); $('#s08-maperr').hidden = true; draw(from, route.to); } catch { $('#s08-maperr').hidden = false; }
  if (!from) { $('#s08-sub').textContent = '출발지가 없어서 경로를 찾을 수 없어요. 대화에서 출발지를 정해 주세요.'; return; }
  loadWalk(c);
}

async function loadWalk(c) {
  const r0 = route;
  const mine = ++walkTicket;
  const result = $('#s08-result');
  const sub = $('#s08-sub');
  result.textContent = '도보 경로를 찾고 있어요…';
  const r = await walkRoute({ lat: r0.from.lat, lng: r0.from.lng }, r0.to);
  if (mine !== walkTicket || route !== r0) return;
  if (r.kind !== 'ready') {
    result.textContent = '도보 경로를 확인하지 못했어요';
    $('#s08-error').hidden = false;
    $('#s08-errmsg').textContent = `${r.message} 걷는 시간은 경로를 확인했을 때만 알려 드려요.`;
    sub.textContent = c.distance_km != null ? `직선 거리 약 ${c.distance_km}km (걷는 시간 아님)` : '';
    return;
  }
  r0.walk = r;
  const min = Math.round(r.duration_s / 60);
  result.textContent = `도보 약 ${min}분`;
  sub.textContent = `약 ${(r.distance_m / 1000).toFixed(1)}km${min > 30 ? ' · 걷는 시간이 긴 경로예요. 위 "대중교통"도 확인해 보세요.' : ''}`;
  if (currentMode === 'walk') showWalk();
}

function showWalk() {
  const r = route?.walk;
  draw(route.from, route.to, r?.path?.length > 1 ? [{ path: r.path, color: COLORS.walk }] : []);
  credit(r ? `도보 경로 © OpenStreetMap · ${r.provider || 'Valhalla / FOSSGIS'}` : '');
}

const fmtMin = (s) => `${Math.round(s / 60)}분`;
const modeName = { WALKING: '걷기', BUS: '버스', SUBWAY: '지하철' };

/** 대중교통 경로 카드 */
function routeCard(rt, i) {
  const card = el('button', 'route-card');
  card.type = 'button';
  card.setAttribute('aria-pressed', String(i === route.pick));
  const head = el('div', 'route-card__head');
  head.append(el('strong', null, `약 ${fmtMin(rt.duration_s)}`),
    el('span', 'muted', [`환승 ${rt.transfers}회`, rt.fare_won != null ? `${rt.fare_won.toLocaleString()}원` : '요금 확인 필요'].join(' · ')));
  const steps = el('ol', 'route-steps');
  rt.steps.forEach((st) => {
    const li = el('li', `route-step route-step--${st.mode.toLowerCase()}`);
    const name = st.mode === 'WALKING' ? `걷기 ${fmtMin(st.duration_s)}` : `${modeName[st.mode]} ${(st.vehicles || []).map((v) => v.name).slice(0, 2).join(', ') || ''} · ${fmtMin(st.duration_s)}`;
    li.append(el('span', 'route-step__name', name.trim()));
    if (st.instruction && st.mode !== 'WALKING') li.append(el('span', 'route-step__how muted', st.instruction));
    steps.append(li);
  });
  card.append(head, steps);
  card.addEventListener('click', () => { route.pick = i; showTransit(); });
  return card;
}

async function loadTransit() {
  const r0 = route;
  if (!r0?.from) return;
  if (!r0.transit) {
    $('#s08-tstate').textContent = '대중교통 경로를 찾고 있어요…';
    $('#s08-tstate').hidden = false;
    r0.transit = await transitRoute({ lat: r0.from.lat, lng: r0.from.lng }, r0.to);
    if (route !== r0) return;
  }
  showTransit();
}

function showTransit() {
  const t = route?.transit;
  if (!t) return;
  const box = $('#s08-routes');
  const st = $('#s08-tstate');
  if (t.kind !== 'ready') {
    st.hidden = false;
    st.textContent = `${t.message} 아래 카카오맵 앱에서 확인할 수 있어요.`;
    box.replaceChildren();
    draw(route.from, route.to);
    credit('');
    return;
  }
  st.hidden = true;
  box.replaceChildren(...t.routes.map(routeCard));
  $('#s08-tnote').textContent = t.time_basis || '조회 시점 경로예요. 배차·막차는 따로 확인해 주세요.';
  const rt = t.routes[route.pick] || t.routes[0];
  draw(route.from, route.to, rt.steps.filter((s) => s.path?.length > 1).map((s) => ({ path: s.path, color: COLORS[s.mode], dashed: s.mode === 'WALKING' })));
  credit(`대중교통 경로 ${t.provider || '카카오맵'}`);
}

let currentMode = 'walk';
function setMode(mode) {
  currentMode = mode;
  document.querySelectorAll('#s08 [data-mode]').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.mode === mode)));
  $('#s08-kakao').title = mode === 'transit' ? '카카오맵 앱에서 대중교통 실시간 경로 보기' : '카카오맵 앱에서 도보 실시간 경로 보기';
  $('#s08-walk').hidden = mode !== 'walk';
  $('#s08-transit').hidden = mode !== 'transit';
  if (!route) return;
  if (mode === 'walk') showWalk();
  else loadTransit();
}

/** 이벤트 연결 (한 번) */
export function initPlace() {
  $('#s04-save').addEventListener('click', (e) => {
    const id = e.currentTarget.dataset.id;
    if (isSaved(id)) { location.hash = '/me'; return; }
    if (isSignedIn()) { doSave(id); return; }
    pendingSave = id; // 체험 시작 후 자동 1회 실행
    openSheet();
  });
  $('#sheet-start').addEventListener('click', () => {
    const id = pendingSave;
    pendingSave = null;
    closeSheet();
    if (!startDemo()) { note('체험을 시작하지 못했어요. 브라우저 저장이 막혀 있는지 확인해 주세요.', true); return; }
    document.dispatchEvent(new CustomEvent('demo-changed'));
    if (id) doSave(id);
  });
  $('#sheet-cancel').addEventListener('click', () => { pendingSave = null; closeSheet(); note('저장하지 않았어요. 언제든 다시 누르면 돼요.'); });
  $('#sheet-save').addEventListener('click', (e) => { if (e.target.id === 'sheet-save') { pendingSave = null; closeSheet(); } });
  document.querySelectorAll('#s08 [data-mode]').forEach((b) => b.addEventListener('click', () => setMode(b.dataset.mode)));
  $('#s08-big').addEventListener('click', () => setBig(true));
  // 지도를 크게 본 상태에서 상단바 뒤로가기는 먼저 지도를 작게 해요
  $('#s08-back').addEventListener('click', (e) => {
    if (!$('#s08-mapwrap').classList.contains('is-full')) return;
    e.stopPropagation();
    setBig(false);
  }, true);
  $('#s08-small').addEventListener('click', () => setBig(false));
  window.addEventListener('hashchange', () => { if (!location.hash.startsWith('#/map/')) setBig(false); });
  $('#s08-retry').addEventListener('click', () => { const id = decodeURIComponent(location.hash.split('/')[2] || ''); renderMap(id); });
}

