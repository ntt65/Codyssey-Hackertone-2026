/** 현재 대화 화면의 보류·재입력·늦은 응답을 실제 네트워크 없이 확인한다. */
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

/** 모의 응답과 화면 클릭으로 변경 보류 및 취소된 요청을 검사한다. */
async function main() {
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  const base = `http://127.0.0.1:${server.address().port}`;
  let browser;
  try {
    browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH, headless: true });
    const page = await browser.newPage();
    let recommendCalls = 0;
    const chatMessages = [];
    let completeDelayed;
    let delayedRequest;
    const delayedStarted = new Promise((resolve) => { delayedRequest = resolve; });
    await page.route('**/*', async (route) => {
      const url = route.request().url();
      if (url.includes('/preview/recommend')) { recommendCalls++; await route.fulfill({ status: 200, json: { status: 'no_results', candidates: [] } }); return; }
      if (url.includes('/preview/chat')) {
        const body = route.request().postDataJSON();
        chatMessages.push(body.message);
        if (body.message === '늦은 답변') {
          await new Promise((resolve) => { completeDelayed = resolve; delayedRequest(); });
          await route.fulfill({ status: 200, json: { updated_condition_draft: { category: '국악' }, conflicts: [], field_errors: [], ready_to_search: false } }).catch(() => {});
          return;
        }
        await route.fulfill({ status: 200, json: { updated_condition_draft: body.condition_draft,
          interpretation_status: 'needs_clarification', assistant_text: '오전인지 오후인지 알려 주세요.',
          ready_to_search: false, conflicts: [], field_errors: [] } });
        return;
      }
      if (!url.startsWith(base)) { await route.abort(); return; }
      await route.continue();
    });
    await page.addInitScript(() => sessionStorage.setItem('lab678_chat', JSON.stringify({
      draft: { category: '전시', date: '2026-11-02', startTime: '14:00', endTime: '17:00', startLocation: { label: '서울역', lat: 37.55, lng: 126.97 } },
      messages: [], revision: 0, sound: false, mode: 'text',
    })));
    await page.addInitScript(() => {
      window.SpeechRecognition = class {
        start() { window.__recognizer = this; }
        stop() {
          const result = [{ transcript: '끝까지 인식한 말' }];
          result.isFinal = true;
          this.onresult?.({ results: [result] });
          this.onend?.();
        }
        emit(text) {
          const result = [{ transcript: text }];
          result.isFinal = false;
          this.onresult?.({ results: [result] });
        }
      };
    });
    await page.goto(`${base}/?agent=legacy#/chat?text`);
    await page.locator('#chat-input').fill('내일 3시');
    await page.locator('#chat-form').evaluate((form) => form.requestSubmit());
    await page.getByText('오전인지 오후인지 알려 주세요.').waitFor();
    assert.equal(recommendCalls, 0, '보류된 응답으로 추천을 시작하면 안 됨');
    await page.getByRole('button', { name: '다시 말하기' }).click();
    assert.equal(await page.locator('#chat-input').inputValue(), '내일 3시');
    await page.locator('#chat-input').fill('늦은 답변');
    await page.locator('#chat-form').evaluate((form) => form.requestSubmit());
    await delayedStarted;
    await page.locator('#chat-input').fill('기다리는 동안 쓴 글');
    await page.locator('#chat-form').evaluate((form) => form.requestSubmit());
    assert.equal(await page.locator('#chat-input').inputValue(), '기다리는 동안 쓴 글', '처리 중 입력 보존');
    await page.getByRole('button', { name: '다시 말하기' }).click();
    completeDelayed();
    await page.waitForTimeout(100);
    const state = await page.evaluate(() => JSON.parse(sessionStorage.getItem('lab678_chat')));
    assert.equal(state.draft.category, '전시', '취소한 이전 응답은 반영하지 않음');
    assert.equal(recommendCalls, 0);
    await page.locator('#chat-input').fill('');
    await page.locator('#chat-mic').click();
    await page.evaluate(() => window.__recognizer.emit('중간 말'));
    await page.locator('#chat-mic').click();
    await page.waitForFunction(() => document.querySelector('#chat-log').textContent.includes('끝까지 인식한 말'));
    await page.waitForTimeout(900);
    assert.equal(chatMessages.filter((x) => x === '끝까지 인식한 말').length, 1, '최종 음성은 한 번만 전송');

    // 각 페이지는 합성 세션/모의 API를 사용하며 외부 통신을 차단한다.
    async function setup(seed, responder) {
      const tab = await browser.newPage();
      const calls = { recommend: 0, places: [] };
      await tab.addInitScript((initial) => {
        sessionStorage.setItem('lab678_chat', JSON.stringify(initial));
        window.__geoCalls = 0;
        Object.defineProperty(navigator, 'geolocation', { value: { getCurrentPosition(ok) {
          window.__geoCalls++; ok({ coords: { latitude: 37.55, longitude: 126.97 } });
        } }, configurable: true });
      }, { draft: seed.draft || {}, lastRequest: seed.lastRequest || null, messages: [], revision: 0, sound: false, mode: 'text' });
      await tab.route('**/*', async (route) => {
        const url = route.request().url();
        if (url.includes('/preview/chat')) {
          const body = route.request().postDataJSON();
          const result = responder(body);
          await route.fulfill({ status: result.status || 200, json: result.body }); return;
        }
        if (url.includes('/preview/places')) {
          const body = route.request().postDataJSON(); calls.places.push(body.query);
          await route.fulfill({ status: 200, json: { status: 'ready', places: [
            { label: body.query, lat: 37.5, lng: 127, address: '서울 강남구 개포동' },
          ] } }); return;
        }
        if (url.includes('/preview/recommend')) {
          calls.recommend++;
          await route.fulfill({ status: 200, json: { status: 'no_results', candidates: [], coverage_note: '공개 샘플 5건 범위' } }); return;
        }
        if (!url.startsWith(base)) { await route.abort(); return; }
        await route.continue();
      });
      await tab.goto(`${base}/?agent=legacy#/chat?text`);
      return { tab, calls };
    }
    async function send(tab, text) {
      await tab.locator('#chat-input').fill(text);
      await tab.locator('#chat-form').evaluate((form) => form.requestSubmit());
      await tab.getByText(text, { exact: true }).last().waitFor();
    }
    async function read(tab) { return tab.evaluate(() => JSON.parse(sessionStorage.getItem('lab678_chat'))); }
    const unavailable = () => ({ status: 503, body: { status: 'unconfigured' } });
    const fallback = await setup({}, unavailable);
    await send(fallback.tab, '내일 3시');
    await fallback.tab.getByText(/대화 해석을 사용할 수 없어요/).waitFor();
    assert.deepEqual((await read(fallback.tab)).draft, {});
    await send(fallback.tab, '오후');
    await fallback.tab.waitForTimeout(40);
    assert.deepEqual((await read(fallback.tab)).draft, {}, '오후만으로 시간을 만들지 않음');
    await send(fallback.tab, '전시 말고 국악');
    await fallback.tab.waitForTimeout(40);
    assert.deepEqual((await read(fallback.tab)).draft, {}, '부정·복합 발화는 보류');
    await send(fallback.tab, '전시');
    await fallback.tab.getByText('언제 가실 건가요?').waitFor();
    assert.equal((await read(fallback.tab)).draft.category, '전시');
    await send(fallback.tab, '내일');
    await fallback.tab.getByText('몇 시부터 몇 시까지 시간이 되세요?').waitFor();
    assert.ok((await read(fallback.tab)).draft.date);
    await fallback.tab.getByRole('button', { name: '오후 2시–5시' }).click();
    await fallback.tab.getByText(/어디에서 출발하세요/).waitFor();
    await send(fallback.tab, '개포동이요');
    await fallback.tab.getByRole('button', { name: /개포동 · 서울 강남구 개포동/ }).waitFor();
    assert.deepEqual(fallback.calls.places, ['개포동']);
    await fallback.tab.close();

    const geo = await setup({}, unavailable);
    await send(geo.tab, '현재 위치');
    await geo.tab.getByText('현재 위치를 사용하려면 아래 버튼을 눌러 주세요.').waitFor();
    assert.equal(await geo.tab.evaluate(() => window.__geoCalls), 0, '음성/문장만으로 위치 권한을 요청하지 않음');
    await geo.tab.getByRole('button', { name: '현재 위치 사용' }).click();
    assert.equal(await geo.tab.evaluate(() => window.__geoCalls), 1);
    await geo.tab.close();

    const full = { category: '전시', date: '2026-11-02', startTime: '14:00', endTime: '17:00', startLocation: { label: '서울역', lat: 37.55, lng: 126.97 }, free_only: true };
    const held = await setup({ draft: full, lastRequest: { category: '전시' } }, (body) => {
      if (body.message === '유료도 괜찮고 내일 3시') return { body: { updated_condition_draft: { ...body.condition_draft, free_only: false },
        interpretation_status: 'needs_clarification', clarification_fields: ['start_at'], assistant_text: '출발 시간을 다시 확인해 주세요.', ready_to_search: false, conflicts: [], field_errors: [] } };
      if (body.message === '오후 세 시 출발') return { body: { updated_condition_draft: { ...body.condition_draft, start_at: '2026-11-02T15:00:00+09:00' }, interpreted_fields: ['start_at'], ready_to_search: true, conflicts: [], field_errors: [] } };
      return { body: { updated_condition_draft: body.condition_draft, ready_to_search: true, conflicts: [], field_errors: [] } };
    });
    await send(held.tab, '유료도 괜찮고 내일 3시');
    await held.tab.getByRole('button', { name: /유료도 포함.*바꾸기/ }).click();
    await held.tab.waitForTimeout(40);
    assert.equal(held.calls.recommend, 0, '부분 동의 뒤 보류된 시각으로 검색 금지');
    await send(held.tab, '전시');
    await held.tab.waitForTimeout(40);
    assert.equal(held.calls.recommend, 0, '무관한 발화는 보류 해제 금지');
    await send(held.tab, '오후 세 시 출발');
    await held.tab.getByRole('button', { name: /오후 3시.*바꾸기/ }).click();
    await held.tab.getByText(/공개 샘플 5건 범위/).waitFor();
    assert.equal(held.calls.recommend, 1, '관련 시각이 확인되면 검색');
    await held.tab.close();

    const grouped = await setup({ draft: { ...full, category: '공연' }, lastRequest: { category: '전체' } },
      (body) => ({ body: { updated_condition_draft: body.condition_draft, ready_to_search: true, conflicts: [], field_errors: [] } }));
    await send(grouped.tab, '아무거나');
    await grouped.tab.getByText(/공연.*아무거나.*바꿀까요/).waitFor();
    await grouped.tab.getByRole('button', { name: /아무거나.*바꾸기/ }).click();
    await grouped.tab.getByText(/공개 샘플 5건 범위/).waitFor();
    assert.equal((await read(grouped.tab)).draft.category, '전체');
    await grouped.tab.close();

    const noDate = await setup({ draft: { category: '공연' } }, (body) => ({ body: {
      updated_condition_draft: { ...body.condition_draft, category: '전체', categories: ['전체'] },
      interpreted_fields: ['category'], ready_to_search: false, conflicts: [], field_errors: [],
    } }));
    await send(noDate.tab, '아무거나');
    await noDate.tab.getByText('언제 가실 건가요?').waitFor();
    assert.equal((await read(noDate.tab)).draft.category, '전체', '날짜가 없어도 검증된 전체 분류로 변경');
    await noDate.tab.close();

    const sequential = await setup({ draft: full, lastRequest: { category: '전시' } }, (body) => {
      if (body.message === '시각이 모호해요') return { body: { updated_condition_draft: body.condition_draft,
        interpretation_status: 'needs_clarification', clarification_fields: ['start_at', 'end_at'],
        assistant_text: '시작과 종료 시각을 확인해 주세요.', interpreted_fields: [], ready_to_search: false, conflicts: [], field_errors: [] } };
      const interpreted = body.message === '시작은 그대로' ? ['start_at'] : body.message === '끝은 그대로' ? ['end_at'] : ['category'];
      return { body: { updated_condition_draft: body.condition_draft, interpreted_fields: interpreted,
        ready_to_search: true, conflicts: [], field_errors: [] } };
    });
    await send(sequential.tab, '시각이 모호해요');
    await sequential.tab.waitForFunction(() => JSON.parse(sessionStorage.getItem('lab678_chat')).clarification?.fields?.length === 2);
    await send(sequential.tab, '전시');
    await sequential.tab.waitForTimeout(50);
    assert.deepEqual((await read(sequential.tab)).clarification.fields, ['start_at', 'end_at'], '무관 답변은 보류 유지');
    await send(sequential.tab, '시작은 그대로');
    await sequential.tab.waitForFunction(() => JSON.parse(sessionStorage.getItem('lab678_chat')).clarification?.fields?.join(',') === 'end_at');
    assert.equal(sequential.calls.recommend, 0, '같은 값 재확인 후에도 남은 보류를 유지');
    await send(sequential.tab, '끝은 그대로');
    await sequential.tab.getByText(/공개 샘플 5건 범위/).waitFor();
    assert.equal((await read(sequential.tab)).clarification, null, '두 필드를 순차 재확인하면 보류 해제');
    assert.equal(sequential.calls.recommend, 1);
    await sequential.tab.close();

    const categoryHold = await setup({ draft: { ...full, categories: ['전시'] }, lastRequest: { category: '전시' } }, (body) => {
      if (body.message === '분류가 모호해요') return { body: { updated_condition_draft: body.condition_draft,
        interpretation_status: 'needs_clarification', clarification_fields: ['categories'],
        assistant_text: '관심 분류를 확인해 주세요.', ready_to_search: false, conflicts: [], field_errors: [] } };
      return { body: { updated_condition_draft: body.condition_draft, interpreted_fields: ['category'],
        ready_to_search: true, conflicts: [], field_errors: [] } };
    });
    await send(categoryHold.tab, '분류가 모호해요');
    await categoryHold.tab.waitForFunction(() => JSON.parse(sessionStorage.getItem('lab678_chat')).clarification?.fields?.includes('categories'));
    await send(categoryHold.tab, '전시');
    await categoryHold.tab.getByText(/공개 샘플 5건 범위/).waitFor();
    assert.equal((await read(categoryHold.tab)).clarification, null, '단일 category로 categories 보류 해제');
    await categoryHold.tab.close();

    const oldServer = await setup({ draft: full, lastRequest: { category: '전시' } }, (body) => {
      if (body.message === '정보가 모호해요') return { body: { updated_condition_draft: body.condition_draft,
        interpretation_status: 'needs_clarification', assistant_text: '다시 확인해 주세요.', ready_to_search: false, conflicts: [], field_errors: [] } };
      return { body: { updated_condition_draft: body.condition_draft, ready_to_search: true, conflicts: [], field_errors: [] } };
    });
    await send(oldServer.tab, '정보가 모호해요');
    await oldServer.tab.waitForFunction(() => Boolean(JSON.parse(sessionStorage.getItem('lab678_chat')).clarification));
    await send(oldServer.tab, '전시');
    await oldServer.tab.waitForTimeout(50);
    assert.equal(oldServer.calls.recommend, 0, '이전 서버가 보류/검증 필드를 생략하면 임의 해제하지 않음');
    await oldServer.tab.close();

    const legacyGroup = await setup({ draft: { ...full, category: '체험' }, lastRequest: { category: '전체' } },
      (body) => ({ body: { updated_condition_draft: { ...body.condition_draft, category: '전체', categories: ['전체'] },
        interpreted_fields: ['category'], ready_to_search: true, conflicts: [], field_errors: [] } }));
    await send(legacyGroup.tab, '공연');
    await legacyGroup.tab.getByText(/체험·배우기.*공연.*바꿀까요/).waitFor();
    await legacyGroup.tab.getByRole('button', { name: '체험·배우기 유지' }).click();
    assert.equal((await read(legacyGroup.tab)).draft.category, '체험', '기존 그룹 분류 거절 시 보존');
    await send(legacyGroup.tab, '공연');
    await legacyGroup.tab.getByRole('button', { name: '공연으로 바꾸기' }).click();
    await legacyGroup.tab.getByText(/공개 샘플 5건 범위/).waitFor();
    assert.equal((await read(legacyGroup.tab)).draft.category, '공연', '기존 그룹 분류 수락 시 변경');
    await legacyGroup.tab.close();
    console.log('PASS: 보류·재입력·경합·음성·키 없는 단답·위치 권한·조건 확인·검색 범위·분류 전환');
  } finally {
    if (browser) await browser.close();
    await new Promise((resolve) => server.close(resolve));
  }
}

main().catch((error) => { console.error(error); process.exitCode = 1; });
