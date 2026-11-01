/**
 * 대화 상태 회귀 검사: 실제 앱 DOM에 합성 세션과 모의 API를 연결한다.
 * 실행: node utils/scripts/check_agent_regressions.cjs
 * 선택 환경변수: PLAYWRIGHT_MODULE, CHROMIUM_PATH. 외부 통신·실제 AI 호출은 차단한다.
 */
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

const initialDraft = {
  category: '전시', categories: ['전시'], date: '2026-11-02', startTime: '14:00', endTime: '17:00',
  startLocation: { label: '서울역', lat: 37.55, lng: 126.97 }, free_only: false,
};
const paid = [1, 2, 3, 4].map((n) => ({
  id: `paid${n}`, title: `유료 전시 ${n}`, genre: '전시', fee_type: '유료', distance_km: 5 - n, venue: '미술관',
}));
const free = [{ id: 'free1', title: '무료 전시', genre: '전시', fee_type: '무료', distance_km: 0.5, venue: '전시장' }];
const cityHall = { label: '시청', address: '서울 중구 세종대로', lat: 37.56, lng: 126.98 };

/** 모의 서버도 현재 API처럼 충돌한 장소는 기존 draft에 반영하지 않는다. */
function chatReply(body) {
  const draft = structuredClone(body.condition_draft);
  const reply = { status: 'draft', updated_condition_draft: draft, conflicts: [], field_errors: [],
    interpreted_fields: [], ready_to_search: true };
  if (body.message.includes('시청')) {
    reply.interpreted_fields = ['start_query'];
    if (draft.start_location) {
      reply.conflicts = [{ field: 'start_query', before: draft.start_location, after: '시청' }];
    } else {
      draft.start_query = '시청';
    }
    reply.ready_to_search = false;
  } else if (body.message.includes('무료')) {
    // 프론트는 confirmed_fields=[]를 보내므로 서버는 값을 갱신하고 화면이 변경 확인을 한다.
    draft.free_only = true;
    reply.interpreted_fields = ['free_only'];
  }
  return reply;
}

/** DOM에서 입력 폼을 제출한다. 처리 중 입력 보존도 실제 이벤트 경로를 사용한다. */
async function send(page, text) {
  await page.locator('#chat-input').fill(text);
  await page.locator('#chat-form').evaluate((form) => form.requestSubmit());
}

/** 비동기 응답이 화면에 반영될 때까지 마지막 저장 메시지를 기다린다. */
async function settled(page) {
  await page.waitForFunction(() => {
    const state = JSON.parse(sessionStorage.getItem('lab678_chat'));
    const last = state?.messages?.at(-1);
    return last?.role === 'ai' && !last.loading;
  });
}

/** 화면과 같은 sessionStorage 상태의 복사본을 읽는다. */
async function read(page) {
  return page.evaluate(() => JSON.parse(sessionStorage.getItem('lab678_chat')));
}

/** 지연 응답 준비가 회귀로 사라져도 검사가 무기한 기다리지 않게 한다. */
async function bounded(promise, message) {
  let timer;
  try {
    return await Promise.race([promise, new Promise((_, reject) => {
      timer = setTimeout(() => reject(new Error(message)), 6000);
    })]);
  } finally {
    clearTimeout(timer);
  }
}

/** 보존된 유료 카드의 개수·요약과 새 조건에 대한 요청을 확인한다. */
async function assertPaidPreserved(page, calls, oldSummary) {
  const state = await read(page);
  const messages = state.messages.filter((m) => m.cards?.length);
  assert.equal(messages.length, 1, '다른 조건의 이전 후보를 새로운 카드로 표시하지 않음');
  assert.equal(messages[0].summary, oldSummary, '기존 카드의 조건 요약 보존');
  assert.deepEqual(messages[0].cards, ['paid1', 'paid2', 'paid3']);
  assert.equal(await page.locator('.chat-card').count(), 3, '0건/오류에도 이전 카드는 보존');
  assert.ok(calls.recommend.slice(1).every((body) => body.free_only === true), '후속 검색은 최신 무료 조건 사용');
}

/** 각 시나리오를 별도 브라우저 세션에서 실행하고 실패를 모아 보고한다. */
async function main() {
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  const base = `http://127.0.0.1:${server.address().port}`;
  let browser;
  const failures = [];
  let passed = 0;
  try {
    browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH, headless: true });

    /** 외부 네트워크를 차단하고 선택한 mock을 주입한 독립 탭을 만든다. */
    async function setup(seed = {}, handlers = {}) {
      const page = await browser.newPage();
      page.setDefaultTimeout(6000);
      const calls = { chat: [], recommend: [], places: [] };
      const errors = [];
      page.on('pageerror', (error) => errors.push(error.message));
      await page.addInitScript((data) => sessionStorage.setItem('lab678_chat', JSON.stringify(data)), {
        draft: structuredClone(initialDraft), messages: [], revision: 0, sound: false, mode: 'text', ...seed,
      });
      await page.route('**/*', async (route) => {
        const url = route.request().url();
        if (url.includes('/preview/chat')) {
          const body = route.request().postDataJSON();
          calls.chat.push(body);
          await route.fulfill({ status: 200, json: handlers.chat ? await handlers.chat(body) : chatReply(body) });
          return;
        }
        if (url.includes('/preview/places')) {
          calls.places.push(route.request().postDataJSON());
          await route.fulfill({ status: 200, json: { status: 'ready', places: [cityHall] } });
          return;
        }
        if (url.includes('/preview/recommend')) {
          const body = route.request().postDataJSON();
          calls.recommend.push(body);
          const response = handlers.recommend ? await handlers.recommend(body, calls.recommend.length)
            : { status: 200, json: { status: 'ready', candidates: body.free_only ? free : paid } };
          await route.fulfill(response).catch(() => {});
          return;
        }
        if (!url.startsWith(base)) { await route.abort(); return; }
        await route.continue();
      });
      await page.goto(`${base}/?agent=legacy#/chat?text`);
      return { page, calls, errors };
    }

    /** 실패 시에도 다음 독립 시나리오를 수행하고 생성 탭을 닫는다. */
    async function test(name, run) {
      const pagesBefore = new Set(browser.contexts().flatMap((context) => context.pages()));
      try {
        await run();
        passed++;
        console.log(`PASS: ${name}`);
      } catch (error) {
        failures.push(`${name}: ${error.message}`);
        console.error(`FAIL: ${name}: ${error.message}`);
      } finally {
        for (const context of browser.contexts()) {
          for (const page of context.pages()) if (!pagesBefore.has(page)) await page.close();
        }
      }
    }

    for (const failure of ['empty', 'error']) {
      await test(`${failure}: 조건 변경 뒤 이전 후보를 다른 곳/가까운 곳으로 재사용하지 않음`, async () => {
        const { page, calls, errors } = await setup({}, {
          recommend: (body) => !body.free_only ? { status: 200, json: { status: 'ready', candidates: paid } }
            : failure === 'empty' ? { status: 200, json: { status: 'no_results', candidates: [] } }
              : { status: 502, json: { status: 'error', message: '검증용 조회 실패' } },
        });
        await send(page, '추천해줘');
        await page.locator('.chat-card').first().waitFor();
        const oldSummary = (await read(page)).messages.find((m) => m.cards)?.summary;
        await send(page, '무료만');
        await page.getByRole('button', { name: '무료만으로 바꾸기' }).click();
        await settled(page);
        assert.equal((await read(page)).draft.free_only, true);
        await send(page, '다른 곳 보여줘');
        await settled(page);
        await assertPaidPreserved(page, calls, oldSummary);
        await send(page, '더 가까운 곳');
        await settled(page);
        await assertPaidPreserved(page, calls, oldSummary);
        assert.deepEqual(errors, []);
      });
    }

    await test('시간 버튼으로 해당 보류를 해제하고 추천 진행', async () => {
      const { page, calls } = await setup({ draft: { ...initialDraft, startTime: null, endTime: null },
        clarification: { text: '시간을 다시 알려 주세요.', fields: ['start_at', 'end_at'] } });
      await page.getByRole('button', { name: '오후 2시–5시' }).click();
      await settled(page);
      const state = await read(page);
      assert.equal(state.draft.startTime, '14:00');
      assert.equal(state.draft.endTime, '17:00');
      assert.equal(state.clarification, null);
      assert.equal(calls.recommend.length, 1);
    });

    for (const field of ['category', 'time']) {
      await test(`기존 값과 같은 ${field} 버튼 재확인도 보류 해제`, async () => {
        const { page, calls } = await setup({ clarification: {
          text: '원하는 조건을 다시 알려 주세요.', fields: field === 'category' ? ['category', 'categories'] : ['start_at', 'end_at'],
        } });
        await page.getByRole('button', { name: field === 'category' ? '전시' : '오후 2시–5시', exact: true }).click();
        await settled(page);
        const state = await read(page);
        assert.equal(state.clarification, null);
        assert.equal(calls.recommend.length, 1);
        assert.equal(state.draft.category, initialDraft.category);
        assert.equal(state.draft.startTime, initialDraft.startTime);
        assert.equal(state.draft.endTime, initialDraft.endTime);
      });
    }

    for (const accept of [true, false]) {
      await test(`출발지 보류: 선택 뒤 ${accept ? '수락하면 해제' : '거절하면 유지'}`, async () => {
        const { page, calls } = await setup();
        await send(page, '추천해줘');
        await page.locator('.chat-card').first().waitFor();
        await page.evaluate(async () => {
          const { state, save } = await import('/js/state.js');
          state.clarification = { text: '출발지를 다시 말씀해 주세요.', fields: ['start_query'] };
          save();
        });
        await send(page, '시청에서 출발');
        await page.getByRole('button', { name: '시청 · 서울 중구 세종대로', exact: true }).click();
        assert.equal((await read(page)).draft.startLocation.label, '서울역', '변경 확인 전 기존 위치 유지');
        await page.getByRole('button', { name: accept ? '시청 · 서울 중구 세종대로로 바꾸기' : '서울역 유지' }).click();
        await settled(page);
        const state = await read(page);
        assert.equal(calls.places.length, 1);
        if (accept) {
          assert.equal(state.clarification, null);
          assert.equal(state.draft.startLocation.lat, cityHall.lat);
          assert.equal(calls.recommend.length, 2);
          assert.equal(calls.recommend[1].start_location.address, cityHall.address);
        } else {
          assert.deepEqual(state.clarification.fields, ['start_query']);
          assert.equal(state.draft.startLocation.label, '서울역');
          assert.equal(calls.recommend.length, 1);
        }
      });
    }

    await test('무료 변경 확인과 출발지 후보 선택을 모두 마친 뒤 검색', async () => {
      const { page, calls } = await setup({}, { chat: (body) => {
        const reply = chatReply(body);
        if (body.message.includes('시청')) {
          reply.updated_condition_draft.free_only = true;
          reply.interpreted_fields.push('free_only');
        }
        return reply;
      } });
      await send(page, '추천해줘');
      await page.locator('.chat-card').first().waitFor();
      await send(page, '무료로 시청에서 출발');
      await page.getByRole('button', { name: '무료만으로 바꾸기' }).click();
      await page.getByRole('button', { name: '시청 · 서울 중구 세종대로', exact: true }).waitFor();
      assert.equal(calls.recommend.length, 1, '장소 후보 선택 전에 기존 출발지로 검색하지 않음');
      assert.equal((await read(page)).draft.startLocation.label, '서울역');
      await page.getByRole('button', { name: '시청 · 서울 중구 세종대로', exact: true }).click();
      assert.equal(calls.recommend.length, 1, '출발지 변경 수락 전 검색하지 않음');
      await page.getByRole('button', { name: '시청 · 서울 중구 세종대로로 바꾸기' }).click();
      await settled(page);
      assert.equal(calls.recommend.length, 2);
      assert.equal(calls.recommend[1].start_location.label, '시청');
      assert.equal(calls.recommend[1].free_only, true);
    });

    await test('다중 보류는 시간 선택 후 출발지 선택으로 순서대로 해제', async () => {
      const { page, calls } = await setup({
        draft: { ...initialDraft, startTime: null, endTime: null, startLocation: null },
        clarification: { text: '시간과 출발지를 다시 알려 주세요.', fields: ['start_at', 'end_at', 'start_query'] },
      });
      await page.getByRole('button', { name: '오후 2시–5시' }).click();
      await settled(page);
      assert.deepEqual((await read(page)).clarification.fields, ['start_query']);
      assert.equal(calls.recommend.length, 0);
      await send(page, '시청에서 출발');
      await page.getByRole('button', { name: '시청 · 서울 중구 세종대로', exact: true }).click();
      await settled(page);
      assert.equal((await read(page)).clarification, null);
      assert.equal(calls.recommend.length, 1);
    });

    await test('현재 위치 확정은 출발지 보류만 해제하고 시간 보류는 유지', async () => {
      const { page, calls } = await setup({
        clarification: { text: '시간과 출발지를 다시 알려 주세요.', fields: ['start_at', 'start_query'] },
      });
      await page.evaluate(() => {
        Object.defineProperty(navigator, 'geolocation', { configurable: true, value: {
          getCurrentPosition(success) { success({ coords: { latitude: 37.6, longitude: 127.1 } }); },
        } });
      });
      await send(page, '현재 위치');
      await page.getByRole('button', { name: '현재 위치 사용', exact: true }).click();
      await settled(page);
      const state = await read(page);
      assert.deepEqual(state.clarification.fields, ['start_at']);
      assert.equal(state.draft.startLocation.label, '현재 위치');
      assert.equal(state.draft.startLocation.lat, 37.6);
      assert.equal(calls.recommend.length, 0);
      assert.equal(calls.chat.length, 0);
    });

    await test('복합 무료+가까운 요청은 해석·확인 후 새 조건으로 검색', async () => {
      const { page, calls } = await setup();
      await send(page, '추천해줘');
      await page.locator('.chat-card').first().waitFor();
      await send(page, '무료만 가능한 가까운 곳');
      await page.getByRole('button', { name: '무료만으로 바꾸기' }).click();
      await settled(page);
      assert.equal(calls.chat.length, 2, '복합 요청은 서버 해석을 생략하지 않음');
      assert.equal(calls.chat[1].message, '무료만 가능한 가까운 곳');
      assert.equal(calls.recommend[1].free_only, true);
      assert.deepEqual((await read(page)).messages.filter((m) => m.cards).at(-1).cards, ['free1']);
    });

    await test('보류 중 가까운 곳 요청은 기존 후보를 다시 표시하지 않음', async () => {
      const { page, calls } = await setup();
      await send(page, '추천해줘');
      await page.locator('.chat-card').first().waitFor();
      await page.evaluate(async () => {
        const { state, save } = await import('/js/state.js');
        state.clarification = { text: '시간을 다시 말씀해 주세요.', fields: ['start_at'] };
        save();
      });
      await send(page, '더 가까운 곳');
      await settled(page);
      assert.equal((await read(page)).messages.filter((m) => m.cards).length, 1);
      assert.equal(calls.recommend.length, 1);
      assert.deepEqual((await read(page)).clarification.fields, ['start_at']);
    });

    await test('미확인 필수 조건은 다른 곳과 가까운 곳으로 우회하지 않음', async () => {
      const { page, calls } = await setup();
      await send(page, '추천해줘');
      await page.locator('.chat-card').first().waitFor();
      await page.evaluate(async () => {
        const { state, save } = await import('/js/state.js');
        state.draft.unsupported_requirements = ['엘리베이터 필수'];
        save();
      });
      for (const text of ['다른 곳 보여줘', '더 가까운 곳']) {
        await send(page, text);
        await settled(page);
        assert.equal((await read(page)).messages.filter((m) => m.cards).length, 1);
        assert.equal(calls.recommend.length, 1);
      }
    });

    await test('출발지 변경 후 같은 후보가 와도 과거 카드의 거리·조건 보존', async () => {
      const { page, calls } = await setup({}, { recommend: (_body, n) => ({ status: 200,
        json: { status: 'ready', candidates: n === 1 ? paid : paid.map((c) => ({ ...c, distance_km: 0.1 })) },
      }) });
      await send(page, '추천해줘');
      await page.locator('.chat-card').first().waitFor();
      const previousDistance = await page.locator('.chat-cards').first().locator('.chat-card__dist').first().innerText();
      const previousSummary = await page.locator('.msg__summary').first().innerText();
      await send(page, '시청에서 출발');
      await page.getByRole('button', { name: '시청 · 서울 중구 세종대로', exact: true }).click();
      await page.getByRole('button', { name: '시청 · 서울 중구 세종대로로 바꾸기' }).click();
      await settled(page);
      assert.equal(await page.locator('.chat-cards').count(), 2);
      assert.equal(calls.recommend[1].start_location.label, '시청');
      assert.equal(await page.locator('.chat-cards').first().locator('.chat-card__dist').first().innerText(), previousDistance);
      assert.equal(await page.locator('.msg__summary').first().innerText(), previousSummary);
      assert.match(await page.locator('.msg__summary').last().innerText(), /시청/);
      assert.match(await page.locator('.chat-cards').last().locator('.chat-card__dist').first().innerText(), /0\.1km/);
    });

    await test('새 대화 뒤 도착한 다른 곳 추천 응답 무시', async () => {
      let release;
      let began;
      const started = new Promise((resolve) => { began = resolve; });
      const { page } = await setup({}, { recommend: async (_body, n) => {
        if (n === 1) return { status: 200, json: { status: 'ready', candidates: paid } };
        began();
        await new Promise((resolve) => { release = resolve; });
        return { status: 200, json: { status: 'ready', candidates: [{ ...paid[0], id: 'late', title: '늦은 결과' }] } };
      } });
      await send(page, '추천해줘');
      await page.locator('.chat-card').first().waitFor();
      await send(page, '다른 곳 보여줘');
      await settled(page);
      await send(page, '다른 곳 보여줘');
      await bounded(started, '다른 곳의 지연 추천 요청이 시작되지 않음');
      await page.locator('#chat-new').click();
      const response = page.waitForResponse((res) => res.url().includes('/preview/recommend'));
      release();
      await response;
      // fetch promise의 상태 반영 microtask와 다음 렌더 프레임까지 기다린다.
      await page.evaluate(() => new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve))));
      const state = await read(page);
      assert.deepEqual(state.draft, {});
      assert.equal(state.messages.some((m) => m.cards?.length), false);
      assert.equal(state.candidates.late, undefined);
      assert.equal(await page.locator('.chat-card').count(), 0);
    });

    console.log(`Agent regression scenarios: ${passed} PASS, ${failures.length} FAIL`);
    if (failures.length) throw new Error(failures.join('\n'));
  } finally {
    if (browser) await browser.close();
    await new Promise((resolve) => server.close(resolve));
  }
}

main().catch((error) => { console.error(error); process.exitCode = 1; });
