/** 대상 브랜치 A층: 실제 브라우저→CORS HTTP→v3 store/정책/탐색. 모델·공급자만 fixture다. */
const assert = require('node:assert/strict');
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const { spawn } = require('node:child_process');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const root = path.resolve(__dirname, '../../frontend');
const types = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.png': 'image/png', '.svg': 'image/svg+xml' };

/** Start the isolated actual backend and read only its loopback address. */
async function fixture(origin) {
  const child = spawn(process.env.PYTHON || 'python', ['-X', 'utf8', path.join(__dirname, 'agent_v3_http_fixture.py'), origin],
    { windowsHide: true, stdio: ['pipe', 'pipe', 'pipe'] });
  let errors = '';
  child.stderr.on('data', (chunk) => { errors += chunk.toString(); });
  try {
    const base = await new Promise((resolve, reject) => {
      const timer = setTimeout(() => reject(new Error(`fixture timeout: ${errors}`)), 10000);
      let buffer = '';
      child.once('error', (error) => { clearTimeout(timer); reject(error); });
      child.once('exit', (code) => { clearTimeout(timer); reject(new Error(`fixture exited ${code}: ${errors}`)); });
      child.stdout.on('data', (chunk) => {
        buffer += chunk.toString();
        if (!buffer.includes('\n')) return;
        clearTimeout(timer);
        try { resolve(JSON.parse(buffer.split('\n')[0]).base); } catch (error) { reject(error); }
      });
    });
    return { child, base };
  } catch (error) { child.kill(); throw error; }
}

/** Stop only the fixture process created by this test. */
async function stop(child) {
  if (!child || child.exitCode !== null) return;
  await new Promise((resolve) => {
    const timer = setTimeout(() => { child.kill(); resolve(); }, 3000);
    child.once('exit', () => { clearTimeout(timer); resolve(); });
    child.stdin.end('\n');
  });
}

/** Read the real imported frontend state without depending on private storage-key details. */
async function read(page) {
  return page.evaluate(async () => JSON.parse(JSON.stringify((await import('/js/state.js')).state)));
}

/** Wait until the UI has applied an actual canonical HTTP response and is ready for another event. */
async function ready(page) {
  await page.waitForFunction(async () => {
    const { state } = await import('/js/state.js');
    return state.agent.conversation && document.querySelector('#chat-actions')?.children.length > 0;
  });
}

/** Submit the existing form and await its actual v3 message response and completed render. */
async function send(page, text) {
  const response = page.waitForResponse((res) => res.url().endsWith('/preview/chat') && res.request().method() === 'POST'
    && res.request().postDataJSON()?.event?.type === 'message');
  await page.locator('#chat-input').fill(text);
  await page.locator('#chat-form').evaluate((form) => form.requestSubmit());
  const res = await response;
  assert.equal(res.status(), 200, `v3 message status: ${text}`);
  assert.equal(res.headers()['access-control-allow-origin'], new URL(page.url()).origin, 'actual CORS response matches this frontend origin');
  const body = await res.json();
  await applied(page, body);
  return body;
}

/** Await the committed response revision rather than accidentally accepting the previous ready UI. */
async function applied(page, body) {
  if (body.conversation) await page.waitForFunction(async (meta) => {
    const current = (await import('/js/state.js')).state.agent.conversation;
    return current?.conversation_id === meta.conversation_id && current.revision >= meta.revision;
  }, body.conversation);
  await ready(page);
}

/** Trigger an actual selection button and wait for its canonical HTTP and UI application. */
async function selectButton(page, button) {
  const [response] = await Promise.all([
    page.waitForResponse((res) => res.url().endsWith('/preview/chat') && res.request().method() === 'POST'
      && res.request().postDataJSON()?.event?.type === 'select_content'),
    button.click(),
  ]);
  assert.equal(response.status(), 200);
  const body = await response.json();
  await applied(page, body);
  return body;
}

/** Read the isolated fixture's model/source counters; these are never real provider usage. */
async function observations(context, apiBase) {
  return (await context.request.get(`${apiBase}/__fixture`)).json();
}

/** Count synthetic speech activity while prohibiting actual microphone and GPS access. */
function selectionSpeechCounters() {
  window.__choiceSpeech = { starts: 0, speaks: 0 };
  if (navigator.mediaDevices) Object.defineProperty(navigator.mediaDevices, 'getUserMedia', {
    configurable: true, value: async () => { throw new DOMException('No fixture microphone', 'NotAllowedError'); },
  });
  if (navigator.geolocation) Object.defineProperty(navigator.geolocation, 'getCurrentPosition', {
    configurable: true, value: (_success, failure) => failure?.({ code: 1, message: 'No fixture GPS' }),
  });
  window.SpeechRecognition = class {
    start() { window.__choiceSpeech.starts += 1; this.onstart?.(); }
    stop() { this.onend?.(); }
    abort() { this.onend?.(); }
  };
  window.webkitSpeechRecognition = window.SpeechRecognition;
  window.SpeechSynthesisUtterance = class { constructor(text) { this.text = text; } };
  Object.defineProperty(window, 'speechSynthesis', { configurable: true, value: {
    speaking: false, pending: false, getVoices: () => [], cancel() {}, resume() {},
    speak(utterance) { window.__choiceSpeech.speaks += 1; setTimeout(() => utterance.onend?.(), 0); },
    addEventListener() {}, removeEventListener() {},
  } });
}

/** Assert server-issued batch order is the exact visible card order and contains no hidden pool IDs. */
async function batchMatchesCards(page, body) {
  const batch = body.state.display_batch;
  assert.ok(batch?.id && batch.execution_key && batch.candidate_ids.length > 0 && batch.candidate_ids.length <= 3);
  const row = page.locator('.chat-cards').last();
  await row.waitFor();
  const displayed = await row.locator('[data-select-content]').evaluateAll((buttons) => buttons.map((button) => button.dataset.selectContent));
  assert.deepEqual(displayed, batch.candidate_ids, 'visible card order follows this server batch');
  assert.deepEqual(body.tool_result?.display_batch?.candidate_ids, batch.candidate_ids);
  return batch;
}

/** Create a fresh conversation with genuine policy/source processing and no direct state seeding. */
async function choicePage(context, origin, service = 'performance') {
  const page = await context.newPage();
  page.setDefaultTimeout(12000);
  await page.goto(`${origin}/#/chat?text`);
  await ready(page);
  await send(page, service === 'exhibition' ? '전시 보고 싶어' : '무료만 가능한 공연');
  const result = await send(page, '서울시청');
  await batchMatchesCards(page, result);
  return { page, result };
}

/** Make a backend boundary event with current metadata, avoiding the client stale-button guard. */
async function directEvent(context, apiBase, origin, metadata, event, label) {
  const response = await context.request.post(`${apiBase}/preview/chat`, { headers: { Origin: origin }, data: {
    agent_version: 3, conversation_id: metadata.conversation_id, epoch: metadata.epoch,
    document_id: metadata.document_id, lease_generation: metadata.lease_generation,
    expected_revision: metadata.revision, turn_seq: metadata.next_turn_seq, turn_id: label, event,
  } });
  assert.equal(response.status(), 200, `direct boundary event: ${label}`);
  return response.json();
}

/** Verify transferred target origin picking and walk eligibility through raw provider fixtures. */
async function targetScenarios(context, origin, apiBase) {
  const page = await context.newPage();
  page.setDefaultTimeout(12000);
  try {
    await page.goto(`${origin}/#/chat?text`);
    await ready(page);
    await send(page, '산책하고 싶어');
    const walk = await send(page, '서울시청');
    const batch = await batchMatchesCards(page, walk);
    assert.equal(walk.state.understanding.service, 'walk');
    assert.equal(walk.tool_result.eligibility.checked_count, 5);
    assert.equal(walk.tool_result.eligibility.eligible_count, 2);
    assert.deepEqual(walk.tool_result.candidates.map((c) => c.title), ['화장실 앞 쉼터공원', '테스트생태공원']);
    assert.equal(batch.candidate_ids.length, 2, 'two eligible source results produce two cards without padding');
    assert.equal(walk.tool_result.excluded_counts.walk_amenity, 2);
    assert.equal(walk.tool_result.excluded_counts.walk_unverified, 1);
    assert.match(walk.tool_result.coverage_note, /조회한 5건/);
    const before = await observations(context, apiBase);
    const selected = await send(page, '2번');
    assert.equal(selected.state.selected_content.id, batch.candidate_ids[1]);
    assert.deepEqual(selected.state.conditions, walk.state.conditions);
    assert.deepEqual((await observations(context, apiBase)).counts, before.counts);

    await page.locator('#s04.is-active').waitFor();
    await page.goto(`${origin}/#/chat?text`);
    await ready(page);
    await page.locator('#chat-new').click();
    await send(page, '공연을 보고 싶어');
    const ambiguous = await send(page, '시청');
    assert.equal(ambiguous.state.conditions.start_location, undefined);
    await page.locator('#origin-picker[open]').waitFor();
    const rows = page.locator('#origin-options .origin-option');
    assert.equal(await rows.count(), 2);
    assert.match(await rows.nth(0).innerText(), /서울특별시청[\s\S]*서울 중구/);
    assert.match(await rows.nth(1).innerText(), /수원시청[\s\S]*경기 수원시/);
    const choosing = page.waitForResponse((res) => res.url().endsWith('/preview/chat')
      && res.request().method() === 'POST' && res.request().postDataJSON()?.event?.type === 'select_origin');
    await rows.nth(0).click();
    const chosenResponse = await choosing;
    assert.equal(chosenResponse.status(), 200);
    const chosen = await chosenResponse.json();
    await applied(page, chosen);
    assert.equal(await page.locator('#origin-picker').evaluate((dialog) => dialog.open), false);
    assert.equal(chosen.state.conditions.start_location.label, '서울특별시청');
    assert.equal(chosen.state.conditions.start_location.lat, 37.5663);
    assert.equal(chosen.state.conditions.start_location.lng, 126.9779);
    await batchMatchesCards(page, chosen);
    return 2;
  } finally { await page.close(); }
}

/** Preserve the exact candidate identity while selecting through cards, details, ordinal text and stale boundaries. */
async function choiceScenarios(context, origin, apiBase) {
  let checks = 0;
  const pages = [];
  const errors = [];
  const open = async (service) => {
    const value = await choicePage(context, origin, service);
    pages.push(value.page);
    value.page.on('pageerror', (error) => errors.push(error.message));
    return value;
  };
  const returnChat = async (page) => {
    await page.goto(`${origin}/#/chat?text`);
    await ready(page);
  };
  const selection = (result, id) => ({ type: 'select_content', candidate_id: id,
    result_execution_key: result.state.display_batch.execution_key, display_batch_id: result.state.display_batch.id });
  try {
    const cardCase = await open();
    const cardPage = cardCase.page;
    const first = cardCase.result;
    const expected = first.state.display_batch.candidate_ids[2];
    assert.ok(first.tool_result.candidates.length >= 6, 'fixture has more eligible source results than visible cards');
    const beforeView = await observations(context, apiBase);
    await cardPage.locator('.chat-cards').last().locator('.chat-card').nth(2).getByRole('button', { name: '상세 보기', exact: true }).click();
    await cardPage.locator('#s04.is-active').waitFor();
    assert.equal((await read(cardPage)).agent.domain.selected_content, null, 'opening details alone never selects content');
    assert.equal((await read(cardPage)).selectedCandidate.id, expected);
    assert.deepEqual((await observations(context, apiBase)).counts, beforeView.counts, 'detail viewing makes no model/source query');
    checks += 1;

    await returnChat(cardPage);
    const beforeSelect = await observations(context, apiBase);
    const cardSelection = await selectButton(cardPage, cardPage.locator('.chat-cards').last().locator('[data-select-content]').nth(2));
    assert.equal(cardSelection.next_action.type, 'content_selected', JSON.stringify(cardSelection.next_action));
    assert.equal(cardSelection.next_action.candidate.id, expected);
    assert.equal(cardSelection.state.selected_content.id, expected);
    try { await cardPage.locator('#s04.is-active').waitFor(); }
    catch (error) {
      const failed = await read(cardPage);
      console.error(JSON.stringify({ selection: cardSelection.next_action, canonicalId: cardSelection.state.selected_content?.id,
        batch: cardSelection.state.display_batch, mirrorId: failed.selectedContent?.id,
        lastMessages: failed.messages.slice(-2), url: cardPage.url(), pageErrors: errors }));
      throw error;
    }
    assert.deepEqual(cardSelection.state.conditions, first.state.conditions);
    assert.equal(cardSelection.state.conditions.free_only, true, 'explicit free-only requirement survives selection');
    assert.deepEqual(cardSelection.state.understanding, first.state.understanding);
    assert.deepEqual(cardSelection.state.history.slice(0, first.state.history.length), first.state.history, 'selection preserves the preceding conversation history');
    assert.equal(cardSelection.state.active_question, null, 'selection does not create a mandatory date/time question');
    assert.equal(cardSelection.tool_result, null, 'selection reuses the verified snapshot instead of running a new source');
    assert.deepEqual((await observations(context, apiBase)).counts, beforeSelect.counts);
    checks += 1;

    assert.equal(await cardPage.locator('#s04-map').getAttribute('data-go'), `/map/${encodeURIComponent(expected)}`);
    assert.equal(await cardPage.locator('#s04-save').getAttribute('data-id'), expected);
    await cardPage.locator('#s04-map').click();
    await cardPage.locator('#s08.is-active').waitFor();
    assert.equal((await read(cardPage)).selectedCandidate.id, expected);
    assert.equal(await cardPage.locator('#s08-back').getAttribute('data-go'), `/place/${encodeURIComponent(expected)}`, 'target keeps its existing map-to-place back route for an active candidate');
    await cardPage.locator('#s08-back').click();
    await cardPage.locator('#s04.is-active').waitFor();
    assert.equal((await read(cardPage)).agent.domain.selected_content.id, expected, 'returning through the existing hash route keeps selection');
    await cardPage.locator('#s04-save').click();
    if (await cardPage.locator('#sheet-start').isVisible()) await cardPage.locator('#sheet-start').click();
    await cardPage.waitForFunction(async (id) => (await import('/js/saved.js')).savedPlaces().some((item) => item.id === id), expected);
    assert.equal((await read(cardPage)).agent.domain.selected_content.id, expected, 'map/save actions retain the same canonical selection');
    checks += 1;

    const detailCase = await open();
    assert.equal(detailCase.result.state.display_batch.candidate_ids[2], expected);
    await detailCase.page.locator('.chat-cards').last().locator('.chat-card').nth(2).getByRole('button', { name: '상세 보기', exact: true }).click();
    await detailCase.page.locator('#s04.is-active').waitFor();
    const detailSelection = await selectButton(detailCase.page, detailCase.page.locator('#s04-select-content'));
    assert.equal(detailSelection.state.selected_content.id, expected);
    const numberCase = await open();
    const beforeNumber = await observations(context, apiBase);
    const numberSelection = await send(numberCase.page, '3번');
    assert.equal(numberSelection.state.selected_content.id, expected, 'card/detail/ordinal text all choose the same displayed ID');
    assert.deepEqual((await observations(context, apiBase)).counts, beforeNumber.counts, 'ordinal selection is resolved before the model');
    checks += 1;

    await returnChat(numberCase.page);
    const beforeOther = await observations(context, apiBase);
    const other = await send(numberCase.page, '다른 곳도 보여줘');
    const secondBatch = await batchMatchesCards(numberCase.page, other);
    assert.notEqual(secondBatch.id, numberCase.result.state.display_batch.id);
    const actualThird = secondBatch.candidate_ids[2];
    assert.equal(actualThird, numberCase.result.tool_result.candidates[5].id);
    assert.notEqual(actualThird, numberCase.result.tool_result.candidates[2].id, 'second visible batch third must not mean full server pool third');
    assert.deepEqual((await observations(context, apiBase)).counts, beforeOther.counts, 'explicit other-results request uses the existing verified pool');
    for (const text of ['세 번째', '3번으로 할래']) {
      const selected = await send(numberCase.page, text);
      assert.equal(selected.state.selected_content.id, actualThird);
      await numberCase.page.locator('#s04.is-active').waitFor();
      await returnChat(numberCase.page);
    }
    assert.deepEqual((await observations(context, apiBase)).counts, beforeOther.counts);
    checks += 1;

    const oldButton = numberCase.page.locator('.chat-cards').first().locator('[data-select-content]').first();
    assert.ok(await oldButton.isDisabled(), 'past batches remain visible but are not selectable');
    const current = await read(numberCase.page);
    const beforeStale = await observations(context, apiBase);
    const stale = await directEvent(context, apiBase, origin, current.agent.conversation,
      selection(numberCase.result, expected), 'qa-old-batch');
    assert.ok(stale.next_action.selection_error);
    assert.equal(stale.next_action.type, 'reply');
    assert.deepEqual(stale.state.selected_content, current.agent.domain.selected_content);
    assert.deepEqual((await observations(context, apiBase)).counts, beforeStale.counts);
    checks += 1;

    const foreignCase = await open();
    const beforeForeign = await observations(context, apiBase);
    const foreign = await directEvent(context, apiBase, origin, foreignCase.result.conversation,
      selection(first, expected), 'qa-foreign-batch');
    assert.ok(foreign.next_action.selection_error);
    assert.equal(foreign.state.selected_content, null);
    assert.deepEqual((await observations(context, apiBase)).counts, beforeForeign.counts);
    checks += 1;

    const changedCase = await open();
    const changed = await directEvent(context, apiBase, origin, changedCase.result.conversation,
      { type: 'message', text: '내일' }, 'qa-date-change');
    assert.notEqual(changed.state.display_batch.id, changedCase.result.state.display_batch.id);
    const beforeChangedSelection = await observations(context, apiBase);
    const rejected = await directEvent(context, apiBase, origin, changed.conversation,
      selection(changedCase.result, changedCase.result.state.display_batch.candidate_ids[2]), 'qa-date-stale-selection');
    assert.ok(rejected.next_action.selection_error);
    assert.deepEqual(rejected.state.conditions, changed.state.conditions);
    assert.deepEqual(rejected.state.selected_content, changed.state.selected_content);
    assert.deepEqual((await observations(context, apiBase)).counts, beforeChangedSelection.counts);
    checks += 1;

    const exhibitCase = await open('exhibition');
    const exhibitionThird = exhibitCase.result.state.display_batch.candidate_ids[2];
    const beforeExhibitionSelect = await observations(context, apiBase);
    const chosenExhibit = await send(exhibitCase.page, '3번');
    assert.equal(chosenExhibit.state.selected_content.id, exhibitionThird);
    assert.equal(chosenExhibit.state.understanding.service, 'exhibition');
    assert.deepEqual((await observations(context, apiBase)).counts, beforeExhibitionSelect.counts);
    await exhibitCase.page.locator('#s04.is-active').waitFor();
    await returnChat(exhibitCase.page);
    const previous = await read(exhibitCase.page);
    const beforeConversation = await observations(context, apiBase);
    for (const text of ['ㅎㅎ', '음...', '말씀하신 주', '고마워']) {
      const reply = await send(exhibitCase.page, text);
      assert.equal(reply.state.understanding.service, 'exhibition');
      assert.deepEqual(reply.state.conditions, previous.agent.domain.conditions);
      assert.equal(reply.state.selected_content.id, exhibitionThird);
      assert.doesNotMatch(reply.assistant_text, /어떤 활동|어떤 나들이가 끌리|출발하세요|처음부터/);
    }
    const afterConversation = await observations(context, apiBase);
    assert.equal(afterConversation.counts.culture + afterConversation.counts.map,
      beforeConversation.counts.culture + beforeConversation.counts.map, 'unclear/social words preserve the current goal and results');
    checks += 1;

    const voiceCase = await open();
    const voicePage = voiceCase.page;
    await voicePage.locator('#s02 .topbar [data-go="/home"]').click();
    await voicePage.locator('#s01.is-active').waitFor();
    await voicePage.locator('#s01 [data-go="/chat?voice"]').click();
    await voicePage.locator('#s02.is-active').waitFor();
    await ready(voicePage);
    await voicePage.waitForTimeout(1500);
    assert.equal((await read(voicePage)).mode, 'voice');
    const voiceBefore = await read(voicePage);
    const voiceButton = voicePage.locator('.chat-cards').last().locator('[data-select-content]').nth(1);
    await voiceButton.scrollIntoViewIfNeeded();
    const focusId = await voiceButton.getAttribute('id');
    const scroll = await voicePage.evaluate(() => window.scrollY);
    const voiceSelection = await selectButton(voicePage, voiceButton);
    await voicePage.locator('#s04.is-active').waitFor();
    assert.equal(voiceSelection.state.selected_content.id, voiceCase.result.state.display_batch.candidate_ids[1]);
    const pausedCounters = await voicePage.evaluate(() => ({ ...window.__choiceSpeech }));
    await voicePage.waitForTimeout(400);
    assert.ok(await voicePage.locator('#s04').evaluate((screen) => screen.classList.contains('is-active')), 'hidden chat finally-render does not navigate away from selection details');
    assert.deepEqual(await voicePage.evaluate(() => window.__choiceSpeech), pausedCounters, 'selection details stay paused after hidden chat finally-render');
    const detailState = await read(voicePage);
    await voicePage.locator('#s04 .topbar [data-go="/chat"]').click();
    await voicePage.locator('#s02.is-active').waitFor();
    await voicePage.waitForFunction((id) => document.activeElement?.id === id, focusId);
    assert.ok(Math.abs((await voicePage.evaluate(() => window.scrollY)) - scroll) <= 5, 'selection return restores the clicked card scroll');
    await voicePage.waitForTimeout(1300);
    assert.deepEqual(await voicePage.evaluate(() => window.__choiceSpeech), pausedCounters, 'returning to voice chat never restarts synthetic STT/TTS');
    const voiceAfter = await read(voicePage);
    assert.equal(voiceAfter.agent.conversation.conversation_id, voiceBefore.agent.conversation.conversation_id);
    assert.deepEqual(voiceAfter.agent.domain.conditions, voiceBefore.agent.domain.conditions);
    assert.deepEqual(voiceAfter.agent.domain.understanding, voiceBefore.agent.domain.understanding);
    assert.deepEqual(voiceAfter.messages, detailState.messages, 'return does not append a greeting or another selection acknowledgement');
    checks += 1;

    const nativeCase = await open('exhibition');
    const nativePage = nativeCase.page;
    await nativePage.locator('#s02 .topbar [data-go="/home"]').click();
    await nativePage.locator('#s01.is-active').waitFor();
    await nativePage.locator('#s01 [data-go="/chat?voice"]').click();
    await nativePage.locator('#s02.is-active').waitFor();
    await ready(nativePage);
    await nativePage.waitForTimeout(1500);
    const nativeBefore = await read(nativePage);
    const nativeSelection = await selectButton(nativePage, nativePage.locator('.chat-cards').last().locator('[data-select-content]').first());
    await nativePage.locator('#s04.is-active').waitFor();
    const nativePaused = await nativePage.evaluate(() => ({ ...window.__choiceSpeech }));
    await nativePage.goBack();
    await nativePage.locator('#s02.is-active').waitFor();
    assert.match(new URL(nativePage.url()).hash, /\/chat\?voice/);
    await nativePage.waitForTimeout(1500);
    assert.deepEqual(await nativePage.evaluate(() => window.__choiceSpeech), nativePaused,
      'native back to a voice URL never starts STT/TTS again');
    const nativeAfter = await read(nativePage);
    assert.equal(nativeAfter.agent.domain.selected_content.id, nativeSelection.state.selected_content.id);
    assert.deepEqual(nativeAfter.agent.domain.conditions, nativeBefore.agent.domain.conditions);
    assert.deepEqual(nativeAfter.agent.domain.understanding, nativeBefore.agent.domain.understanding);
    checks += 1;

    const lateCase = await open();
    const latePage = lateCase.page;
    const lateExpected = lateCase.result.state.display_batch.candidate_ids[0];
    let releaseDelivery;
    const deliveryGate = new Promise((resolve) => { releaseDelivery = resolve; });
    let requestCaptured;
    const captured = new Promise((resolve) => { requestCaptured = resolve; });
    await latePage.route('**/preview/chat', async (route) => {
      if (route.request().method() !== 'POST' || route.request().postDataJSON()?.event?.type !== 'select_content') return route.continue();
      const response = await route.fetch();
      requestCaptured();
      await deliveryGate;
      await route.fulfill({ response });
    });
    const beforeLate = await observations(context, apiBase);
    const delivery = latePage.waitForResponse((res) => res.url().endsWith('/preview/chat')
      && res.request().method() === 'POST' && res.request().postDataJSON()?.event?.type === 'select_content');
    delivery.catch(() => {}); // A failed click must still allow the normal cleanup path to run.
    try {
      await Promise.all([captured, latePage.locator('.chat-cards').last().locator('[data-select-content]').first().click()]);
      await latePage.locator('#s02 .topbar [data-go="/home"]').click();
      await latePage.locator('#s01.is-active').waitFor();
      releaseDelivery();
      const lateResponse = await delivery;
      assert.equal(lateResponse.status(), 200);
      const lateBody = await lateResponse.json();
      await applied(latePage, lateBody);
      await latePage.waitForTimeout(150);
      assert.ok(await latePage.locator('#s01').evaluate((screen) => screen.classList.contains('is-active')),
        'a delivered selection response never pulls the user back from home into details');
      const lateState = await read(latePage);
      assert.equal(lateState.agent.domain.selected_content.id, lateExpected, 'canonical selection is retained after route departure');
      assert.deepEqual(lateState.agent.domain.conditions, lateCase.result.state.conditions);
      assert.deepEqual(lateState.agent.domain.understanding, lateCase.result.state.understanding);
      assert.deepEqual((await observations(context, apiBase)).counts, beforeLate.counts);
    } finally { releaseDelivery(); }
    checks += 1;
    assert.deepEqual(errors, []);
    return checks;
  } finally {
    await Promise.all(pages.map((page) => page.close()));
  }
}

/** Execute independent state/context assertions against the existing UI, without screenshots or devices. */
async function main() {
  let apiBase, browser, child;
  const frontendRequests = [];
  const server = http.createServer((req, res) => {
    const relative = decodeURIComponent(new URL(req.url, 'http://localhost').pathname).replace(/^\/+/, '') || 'index.html';
    if (req.method === 'POST') frontendRequests.push(relative);
    const file = path.resolve(root, relative);
    if (!file.startsWith(root + path.sep)) { res.writeHead(403).end(); return; }
    fs.readFile(file, (error, data) => {
      if (error) { res.writeHead(404).end(); return; }
      if (relative === 'index.html') data = Buffer.from(data.toString().replace(
        /(<meta name="lab678-api" content=")[^"]*(">)/, `$1${apiBase}$2`));
      res.writeHead(200, { 'Content-Type': types[path.extname(file)] || 'application/octet-stream' });
      res.end(data);
    });
  });
  let checks = 0;
  try {
    await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
    const base = `agent.localhost:${server.address().port}`;
    const origin = `http://${base}`;
    ({ child, base: apiBase } = await fixture(origin));
    browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH, headless: true,
      args: ['--host-resolver-rules=MAP *.localhost 127.0.0.1', '--no-proxy-server'] });
    const context = await browser.newContext();
    await context.addInitScript(selectionSpeechCounters);
    await context.route('**/*', async (route) => {
      const url = new URL(route.request().url());
      if (url.origin === new URL(apiBase).origin && ['/preview/contact', '/preview/walk', '/preview/transit', '/map-config'].includes(url.pathname)) {
        const body = url.pathname === '/preview/contact' ? { phones: [] } : url.pathname === '/map-config' ? {} : { kind: 'unavailable', message: 'Fixed selection-only route source' };
        return route.fulfill({ status: 200, contentType: 'application/json', headers: {
          'Access-Control-Allow-Origin': origin, 'Access-Control-Allow-Headers': 'Content-Type',
          'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        }, body: JSON.stringify(body) });
      }
      if ([origin, new URL(apiBase).origin].includes(new URL(route.request().url()).origin)) await route.continue();
      else await route.abort();
    });
    const page = await context.newPage();
    page.setDefaultTimeout(12000);
    await page.goto(`${origin}/#/chat?text`);
    await ready(page);
    const initial = await read(page);
    assert.ok(initial.agent.conversation, 'canonical handshake remains present after the UI becomes ready');
    const initialHandle = initial.agent.conversation.conversation_id;
    assert.ok(initialHandle);

    // A real request with no origin can ask one relevant question; a partial bad menu candidate is isolated.
    const first = await send(page, '공연을 보고 싶어');
    assert.equal(first.state.understanding.service, 'performance');
    assert.equal(first.state.active_question.target, 'start_location');
    const questionId = first.state.active_question.id;
    await page.evaluate(async () => {
      const { state, save } = await import('/js/state.js');
      state.messages.push({ role: 'ai', text: '잘 듣지 못했어요. 다시 말씀해 주세요.', statusNotice: true });
      save();
      (await import('/js/chat.js')).renderChat({ voice: false });
    });
    const explained = await send(page, '무슨 조건?');
    assert.match(explained.assistant_text, /지역을 여쭤본/);
    assert.equal(explained.state.active_question.id, questionId);
    const taste = await send(page, '잔잔한 음악');
    assert.equal(taste.state.understanding.preferences[0].value, 'calm');
    assert.equal(taste.state.conditions.category, undefined);
    assert.equal(taste.state.diagnostics.turn_status, 'partial');
    const observation = await (await context.request.get(`${apiBase}/__fixture`, { headers: { Origin: origin } })).json();
    assert.ok(observation.contexts.every((c) => !(c.conversation_context || []).some((m) => m.content.includes('잘 듣지'))));
    assert.equal(observation.contexts.at(-1).active_question.id, questionId);
    checks += 1;

    // The actual place normalizer, policy, source adapter, hard filters and rank evidence all run over HTTP.
    const explored = await send(page, '시청 서울시청');
    await page.locator('.chat-card').first().waitFor();
    assert.equal(explored.tool_result.result_kind, 'content_exploration');
    assert.equal(explored.state.conditions.start_location.label, '서울특별시청');
    assert.equal(explored.state.conditions.date, undefined);
    assert.equal(explored.state.conditions.start_at, undefined);
    assert.equal(explored.state.conditions.end_at, undefined);
    assert.equal(explored.tool_result.range.visit_window_created, false);
    assert.equal(explored.diagnostics.stage, 'tool');
    assert.ok(explored.diagnostics.model_calls <= 2);
    assert.equal(explored.tool_result.candidates[0].title, '피아노 음악회');
    assert.ok(explored.tool_result.candidates.every((c) => c.candidate_kind === 'cultural_event' && c.visit_status === 'not_checked'));
    checks += 1;

    const lively = await send(page, '신나는 공연');
    assert.equal(lively.tool_result.candidates[0].title, '리듬 음악회');
    assert.deepEqual(lively.state.understanding.preferences.map((p) => p.value), ['lively']);
    assert.ok(lively.tool_result.candidates[0].semantic_evidence[0].quote.includes('신나는'));
    checks += 1;

    // Resolving a replacement query must keep the confirmed old coordinates until actual change consent.
    const changedOrigin = await send(page, '수원시청');
    assert.equal(changedOrigin.state.conditions.start_location.label, '서울특별시청', 'old verified origin survives lookup until consent');
    assert.equal(changedOrigin.state.pending_changes[0]?.field, 'start_location');
    const [confirmed] = await Promise.all([
      page.waitForResponse((res) => res.url().endsWith('/preview/chat') && res.request().method() === 'POST'
        && res.request().postDataJSON()?.event?.type === 'confirm_change'),
      page.getByRole('button', { name: '변경할게요', exact: true }).click(),
    ]);
    assert.equal(confirmed.status(), 200);
    await applied(page, await confirmed.json());
    assert.equal((await read(page)).agent.domain.conditions.start_location.label, '수원시청');
    checks += 1;

    // Old global request data must not create a visit date in an exploration detail.
    await page.evaluate(async () => {
      const { state, save } = await import('/js/state.js');
      state.lastRequest = { start_at: '2025-12-24T14:00:00+09:00', end_at: '2025-12-24T17:00:00+09:00', start_location: { label: '옛 출발지', lat: 35, lng: 129 } };
      save();
    });
    await page.locator('.chat-card').first().getByRole('button', { name: '상세 보기' }).click();
    await page.locator('#s04.is-active').waitFor();
    assert.match(await page.locator('.place-visit').innerText(), /방문 날짜.*아직 확인하지/);
    assert.doesNotMatch(await page.locator('.place-visit').innerText(), /12월 24|14:00/);
    assert.equal((await read(page)).selectedCandidate.result_context.conditions.start_location.label, '서울특별시청');
    await page.goto(`${origin}/#/chat?text`);
    await ready(page);
    checks += 1;

    // Reload reconnects to the same server conversation; copied live tabs fork rather than sharing a writer.
    const beforeReload = await read(page);
    await page.reload();
    await ready(page);
    const reloaded = await read(page);
    assert.equal(reloaded.agent.conversation.conversation_id, initialHandle);
    assert.equal(reloaded.agent.domain.understanding.preferences[0].value, 'lively');
    assert.notEqual(reloaded.agent.conversation.document_id, beforeReload.agent.conversation.document_id);
    assert.ok(!frontendRequests.includes('preview/chat'), 'release targets the configured backend origin');
    const newPage = context.waitForEvent('page');
    await page.evaluate(async () => {
      const { state, save } = await import('/js/state.js');
      const previous = { sound: state.sound, mode: state.mode };
      state.sound = true;
      state.mode = 'voice';
      save();
      window.open(location.href, '_blank');
      Object.assign(state, previous);
      save();
    });
    const copied = await newPage;
    copied.setDefaultTimeout(12000);
    await copied.waitForLoadState();
    await ready(copied);
    const fork = await read(copied);
    assert.notEqual(fork.agent.conversation.conversation_id, initialHandle);
    assert.equal(fork.agent.domain.understanding.preferences.length, 0);
    assert.equal(fork.selectedCandidate, null);
    await copied.waitForTimeout(1200);
    assert.deepEqual(await copied.evaluate(() => window.__choiceSpeech), { starts: 0, speaks: 0 },
      'a copied tab forks silently even when the copied chat had sound and voice mode enabled');
    await copied.close();
    checks += 1;

    // A reset fences an in-flight old turn, clears selected details/tastes, and writes a new namespace.
    const request = page.waitForRequest((req) => req.url().endsWith('/preview/chat') && req.method() === 'POST'
      && req.postDataJSON()?.event?.text === '늦은 공연');
    await page.locator('#chat-input').fill('늦은 공연');
    await page.locator('#chat-form').evaluate((form) => form.requestSubmit());
    await request;
    await page.locator('#chat-new').click();
    const reset = await read(page);
    assert.equal(reset.selectedCandidate, null);
    assert.equal(reset.agent.domain, null);
    const movie = await send(page, '영화 보고 싶어');
    assert.equal(movie.state.understanding.service, 'movie');
    assert.equal(movie.state.understanding.preferences.length, 0);
    assert.equal(movie.state.conditions.start_location, undefined);
    await page.waitForFunction(async () => (await import('/js/state.js')).state.messages.at(-1)?.role === 'ai');
    await new Promise((resolve) => setTimeout(resolve, 950));
    const afterLate = await read(page);
    assert.equal(afterLate.agent.domain.understanding.service, 'movie');
    assert.equal(afterLate.agent.domain.understanding.preferences.length, 0);
    assert.notEqual(afterLate.agent.conversation.conversation_id, initialHandle);
    assert.equal(afterLate.messages.some((m) => m.text?.includes('피아노')), false);
    checks += 1;

    // Exact duplicate turn transport replays once; the actual model is not called a second time.
    const current = await read(page);
    const meta = current.agent.conversation;
    const body = { agent_version: 3, conversation_id: meta.conversation_id, epoch: meta.epoch,
      document_id: meta.document_id, lease_generation: meta.lease_generation,
      expected_revision: meta.revision, turn_seq: meta.next_turn_seq, turn_id: 'test-duplicate-v3',
      event: { type: 'message', text: '테스트 중복' } };
    const beforeDuplicate = await (await context.request.get(`${apiBase}/__fixture`)).json();
    const post = () => context.request.post(`${apiBase}/preview/chat`, { headers: { Origin: origin }, data: body });
    const once = await (await post()).json();
    const twice = await (await post()).json();
    assert.equal(twice.replayed, true);
    assert.equal(twice.conversation.revision, once.conversation.revision);
    const afterDuplicate = await (await context.request.get(`${apiBase}/__fixture`)).json();
    assert.equal(afterDuplicate.counts.meaning - beforeDuplicate.counts.meaning, 1);
    checks += 1;

    // Long canonical restoration has a narrowly larger transport budget; claims never import verified facts.
    const restoredMeta = twice.conversation;
    const snapshot = {
      understanding: { goal: '공연 관람을 이어가고 싶어요', service: 'performance',
        preferences: Array.from({ length: 16 }, (_, index) => ({ id: `restore-pref-${index}`, dimension: 'atmosphere',
          value: `${index}번 취향 ` + '차'.repeat(70), polarity: 'prefer', strength: index === 0 ? 'hard' : 'soft', scope: 'performance' })) },
      conditions: { start_location: { label: '현재 위치', lat: 0, lng: 0, verified: true }, free_only: true },
      hypotheses: Array.from({ length: 16 }, (_, index) => ({ id: `restore-hard-${index}`, field: 'requirement',
        value: `${index}번 필수 ` + '계'.repeat(190), strength: 'hard', status: 'unresolved' })),
      active_question: { id: 'q:restored-hard', target: 'requirement', text: '이 조건을 직접 확인할까요?',
        reason: '이전 대화의 필수 조건입니다.', requirement_id: 'restore-hard-0' },
      tool_facts: [{ source: 'forged', candidates: [{ id: 'forged:1', visit_status: 'verified' }] }],
    };
    const restoreBody = { agent_version: 3, conversation_id: restoredMeta.conversation_id, epoch: restoredMeta.epoch,
      document_id: restoredMeta.document_id, lease_generation: restoredMeta.lease_generation,
      expected_revision: restoredMeta.revision, turn_seq: restoredMeta.next_turn_seq, turn_id: 'test-large-restore',
      event: { type: 'restore', snapshot } };
    const restoreBytes = Buffer.byteLength(JSON.stringify(restoreBody), 'utf8');
    assert.ok(restoreBytes > 8192 && restoreBytes < 32768, 'fixture exercises the actual byte-size restoration boundary');
    const beforeRestore = await (await context.request.get(`${apiBase}/__fixture`)).json();
    const restoredResponse = await context.request.post(`${apiBase}/preview/chat`, { headers: { Origin: origin }, data: restoreBody });
    assert.equal(restoredResponse.status(), 200, 'valid v3 restore larger than legacy body limit is accepted');
    const restored = await restoredResponse.json();
    assert.equal(restored.state.understanding.service, 'performance');
    assert.equal(restored.state.understanding.preferences.length, 16);
    assert.equal(restored.state.understanding.preferences[0].strength, 'hard', 'restoration must not silently weaken a hard preference');
    assert.equal(restored.state.hypotheses.length, 16);
    assert.ok(restored.state.hypotheses.every((item) => item.strength === 'hard' && item.status === 'unresolved'));
    assert.equal(restored.state.conditions.start_location, undefined, 'restored current-location claims never import client coordinates');
    assert.equal(restored.state.field_meta.service.confirmed, false);
    assert.deepEqual(restored.state.tool_facts, [], 'stale or forged tool validation is not restored');
    const afterRestore = await (await context.request.get(`${apiBase}/__fixture`)).json();
    assert.equal(afterRestore.counts.meaning, beforeRestore.counts.meaning, 'restore does not reinterpret the user through the model');
    assert.equal(afterRestore.counts.culture + afterRestore.counts.map, beforeRestore.counts.culture + beforeRestore.counts.map,
      'unverified current-location snapshot never starts a source query');
    const legacyOversize = await context.request.post(`${apiBase}/preview/chat`, {
      headers: { Origin: origin }, data: { ...restoreBody, agent_version: 1 },
    });
    assert.equal(legacyOversize.status(), 400, 'legacy 8KiB body limit remains in force');
    const normalOversize = await context.request.post(`${apiBase}/preview/chat`, {
      headers: { Origin: origin }, data: { ...restoreBody, event: { type: 'message', text: '테스트 중복', snapshot } },
    });
    assert.equal(normalOversize.status(), 400, 'only restoration can use the extended v3 body limit');
    checks += 1;
    checks += await choiceScenarios(context, origin, apiBase);
    checks += await targetScenarios(context, origin, apiBase);
    console.log(`PASS: v3 actual HTTP/store/DOM ${checks} scenarios (fixed model/provider; no real API, mic, GPS or screenshots)`);
  } finally {
    if (browser) await browser.close();
    await stop(child);
    await new Promise((resolve) => server.close(resolve));
  }
}

main().catch((error) => { console.error(error); process.exitCode = 1; });
