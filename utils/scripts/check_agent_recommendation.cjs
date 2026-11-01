/** 현재 대화 화면에서 출발지 선택과 선호·추천 전달을 모의 API로 검사한다. */
const assert = require('node:assert/strict');
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');

const root = path.resolve(__dirname, '../../frontend');
const types = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.png': 'image/png', '.svg': 'image/svg+xml' };
const server = http.createServer((req, res) => {
  const relative = decodeURIComponent(new URL(req.url, 'http://localhost').pathname).replace(/^\/+/, '') || 'index.html';
  const file = path.resolve(root, relative);
  if (!file.startsWith(root + path.sep)) { res.writeHead(403).end(); return; }
  fs.readFile(file, (error, data) => {
    if (error) { res.writeHead(404).end(); return; }
    res.writeHead(200, { 'Content-Type': types[path.extname(file)] || 'application/octet-stream' });
    res.end(data);
  });
});

/** 서버·브라우저 네트워크를 차단하고 실제 프론트 상태 및 요청 본문을 확인한다. */
async function main() {
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  const base = `http://127.0.0.1:${server.address().port}`;
  let browser;
  try {
    browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH, headless: true });
    const page = await browser.newPage();
    let recommendBody;
    let chatBody;
    let mode = 'ready';
    await page.route('**/*', async (route) => {
      const url = route.request().url();
      if (url.includes('/preview/chat')) {
        chatBody = route.request().postDataJSON();
        const updated = { ...chatBody.condition_draft, categories: ['전체'], music_followup: false,
          keywords: ['국악'] };
        const changes = chatBody.message === '무료와 예산' ? { free_only: true, budget_krw: 10000 } : {};
        const conflicts = chatBody.message === '시청으로 출발지 변경'
          ? [{ field: 'start_query', before: chatBody.condition_draft.start_location, after: '시청' }] : [];
        await route.fulfill({ status: 200, json: { status: 'draft', updated_condition_draft: { ...updated, ...changes },
          ready_to_search: !conflicts.length, conflicts, field_errors: [] } });
        return;
      }
      if (url.includes('/preview/places')) {
        await route.fulfill({ status: 200, json: { status: 'ready', places: [
          { label: '시청', address: '서울 중구 세종대로', lat: 37.56, lng: 126.98 },
          { label: '시청', address: '경기 수원시 효원로', lat: 37.26, lng: 127.03 },
        ] } });
        return;
      }
      if (url.includes('/preview/recommend')) {
        recommendBody = route.request().postDataJSON();
        if (mode === 'error') { await route.fulfill({ status: 502, json: { status: 'error', message: '조회 실패' } }); return; }
        if (mode === 'empty') { await route.fulfill({ status: 200, json: { status: 'no_results', candidates: [] } }); return; }
        const candidates = [
          { id: 'far', title: '관심 국악', venue: '공연장', genre: '국악', distance_km: 7, preference_reasons: ['공식 행사 정보에 관심어 포함: 국악'],
            checks_required: ['예약 가능 여부·실제 이동시간 확인', '요일·휴관·회차별 시간 확인'] },
          { id: 'near', title: '가까운 국악', venue: '공연장', genre: '국악', distance_km: 1 },
        ];
        await route.fulfill({ status: 200, json: { status: 'ready', candidates, coverage_note: '조회 범위 안내' } });
        return;
      }
      if (!url.startsWith(base)) { await route.abort(); return; }
      await route.continue();
    });
    await page.addInitScript(() => sessionStorage.setItem('lab678_chat', JSON.stringify({
      draft: { category: '공연', date: '2026-11-02', startTime: '14:00', endTime: '17:00',
        startLocation: { label: '서울역', lat: 37.55, lng: 126.97 }, free_only: false,
        budget_krw: 'any', exclude_terms: [], categories: ['전체'] },
      messages: [], revision: 0, sound: false, mode: 'text',
    })));
    await page.goto(`${base}/?agent=legacy#/chat?text`);
    await page.locator('#chat-input').fill('국악 좋아요');
    await page.locator('#chat-form').evaluate((form) => form.requestSubmit());
    await page.locator('.chat-card').first().waitFor();
    assert.equal(chatBody.condition_draft.free_only, false);
    assert.equal(chatBody.condition_draft.budget_krw, 'any');
    assert.deepEqual(chatBody.condition_draft.exclude_terms, []);
    assert.equal(chatBody.condition_draft.date, '2026-11-02');
    assert.equal(recommendBody.category, '전체');
    assert.deepEqual(recommendBody.categories, ['전체']);
    assert.deepEqual(recommendBody.keywords, ['국악']);
    assert.equal(recommendBody.free_only, false);
    assert.equal(recommendBody.budget_krw, 'any');
    assert.deepEqual(recommendBody.exclude_terms, []);
    assert.equal(await page.locator('.chat-card').first().getAttribute('data-id'), 'far', '서버 순위 유지');
    assert.match(await page.locator('#chat-log').innerText(), /조회 범위 안내/);
    assert.match(await page.locator('#chat-log').innerText(), /공식 행사 정보에 관심어 포함/);
    assert.match(await page.locator('#chat-log').innerText(), /예약 가능 여부·실제 이동시간 확인/);
    assert.match(await page.locator('#chat-log').innerText(), /요일·휴관·회차별 시간 확인/);
    let state = await page.evaluate(() => JSON.parse(sessionStorage.getItem('lab678_chat')));
    assert.equal(state.draft.category, '공연', '서버 전체는 화면 묶음 공연을 지우지 않음');
    await page.getByRole('button', { name: '더 가까운 곳' }).click();
    assert.equal(await page.locator('.chat-card').last().getAttribute('data-id'), 'far');
    const visibleCards = await page.locator('.chat-cards').last().locator('.chat-card').evaluateAll((items) => items.map((item) => item.dataset.id));
    assert.deepEqual(visibleCards, ['near', 'far'], '가까운 곳 선택 시만 거리순');
    // 마지막 유효 결과를 보존한 상태에서 0건과 장애를 각각 분리한다.
    const oldPool = [...state.pool];
    mode = 'empty';
    await page.locator('#chat-input').fill('한 번 더');
    await page.locator('#chat-form').evaluate((form) => form.requestSubmit());
    await page.getByText(/조건에 맞는 곳을 찾지 못했어요/).waitFor();
    state = await page.evaluate(() => JSON.parse(sessionStorage.getItem('lab678_chat')));
    assert.deepEqual(state.pool, oldPool, '0건이어도 기존 추천 보존');
    mode = 'error';
    await page.locator('#chat-input').fill('다시 찾아줘');
    await page.locator('#chat-form').evaluate((form) => form.requestSubmit());
    await page.getByText('조회 실패').waitFor();
    state = await page.evaluate(() => JSON.parse(sessionStorage.getItem('lab678_chat')));
    assert.deepEqual(state.pool, oldPool, '장애에도 기존 추천 보존');
    await page.locator('#chat-input').fill('시청으로 출발지 변경');
    await page.locator('#chat-form').evaluate((form) => form.requestSubmit());
    await page.getByRole('button', { name: '시청 · 서울 중구 세종대로' }).waitFor();
    await page.getByRole('button', { name: '시청 · 경기 수원시 효원로' }).waitFor();
    state = await page.evaluate(() => JSON.parse(sessionStorage.getItem('lab678_chat')));
    assert.equal(state.draft.startLocation.label, '서울역', '선택 전 기존 출발지 유지');
    await page.getByRole('button', { name: '기존 출발지 유지' }).click();
    state = await page.evaluate(() => JSON.parse(sessionStorage.getItem('lab678_chat')));
    assert.equal(state.draft.startLocation.label, '서울역', '선택 취소 후 기존 출발지 유지');
    await page.locator('#chat-input').fill('시청으로 출발지 변경');
    await page.locator('#chat-form').evaluate((form) => form.requestSubmit());
    await page.getByRole('button', { name: '시청 · 서울 중구 세종대로' }).click();
    await page.getByRole('button', { name: '시청 · 서울 중구 세종대로로 바꾸기' }).waitFor();
    state = await page.evaluate(() => JSON.parse(sessionStorage.getItem('lab678_chat')));
    assert.equal(state.draft.startLocation.label, '서울역', '확인 전 기존 출발지 유지');
    await page.getByRole('button', { name: '시청 · 서울 중구 세종대로로 바꾸기' }).click();
    await page.getByText('조회 실패').last().waitFor();
    state = await page.evaluate(() => JSON.parse(sessionStorage.getItem('lab678_chat')));
    assert.equal(state.draft.startLocation.label, '시청');
    assert.equal(state.draft.startLocation.lat, 37.56);
    await page.locator('#chat-input').fill('무료와 예산');
    await page.locator('#chat-form').evaluate((form) => form.requestSubmit());
    await page.getByRole('button', { name: '무료만으로 바꾸기' }).waitFor();
    await page.getByRole('button', { name: '무료만으로 바꾸기' }).click();
    await page.getByRole('button', { name: '10,000원으로 바꾸기' }).waitFor();
    state = await page.evaluate(() => JSON.parse(sessionStorage.getItem('lab678_chat')));
    assert.equal(state.draft.free_only, true);
    assert.equal(state.draft.budget_krw, 'any', '다음 변경은 확인 전 유지');
    const mixedRequest = page.waitForRequest((req) => req.url().includes('/preview/recommend'));
    await page.getByRole('button', { name: '예산 제한 없음 유지' }).click();
    const mixedBody = (await mixedRequest).postDataJSON();
    state = await page.evaluate(() => JSON.parse(sessionStorage.getItem('lab678_chat')));
    assert.equal(state.draft.budget_krw, 'any');
    assert.equal(mixedBody.free_only, true, '먼저 수락한 변경은 마지막 거절 후에도 재검색');
    assert.equal(mixedBody.budget_krw, 'any');
    assert.match(await page.locator('#chat-cond').innerText(), /무료만/);
    await page.evaluate(async () => {
      const { state, save } = await import('/js/state.js');
      state.draft.startLocation = { label: '시청', address: '서울 중구 세종대로', lat: 37.56, lng: 126.98 };
      save();
    });
    await page.locator('#chat-input').fill('시청으로 출발지 변경');
    await page.locator('#chat-form').evaluate((form) => form.requestSubmit());
    await page.getByRole('button', { name: '시청 · 경기 수원시 효원로' }).click();
    await page.getByRole('button', { name: '시청 · 경기 수원시 효원로로 바꾸기' }).waitFor();
    await page.getByRole('button', { name: '시청 · 서울 중구 세종대로 유지' }).click();
    state = await page.evaluate(() => JSON.parse(sessionStorage.getItem('lab678_chat')));
    assert.equal(state.draft.startLocation.address, '서울 중구 세종대로', '동명 출발지 변경을 거절하면 기존 주소 유지');
    console.log('PASS: 조건 왕복·그룹·순위·거리순·조회 범위·0건·오류·주소 선택·혼합 변경 확인');
  } finally {
    if (browser) await browser.close();
    await new Promise((resolve) => server.close(resolve));
  }
}

main().catch((error) => { console.error(error); process.exitCode = 1; });
