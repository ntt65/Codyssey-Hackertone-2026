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
    await page.goto(`${base}/#/chat?text`);
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
    console.log('PASS: 보류 안내, 재입력, 처리 중 입력, 늦은 응답, 음성 최종 결과와 중복 전송');
  } finally {
    if (browser) await browser.close();
    await new Promise((resolve) => server.close(resolve));
  }
}

main().catch((error) => { console.error(error); process.exitCode = 1; });
