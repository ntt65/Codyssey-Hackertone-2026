/** 실제 브라우저→별도 origin HTTP→조건 검증/추천을 검사한다. 외부 공급자만 고정한다. */
const assert = require('node:assert/strict');
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const { spawn } = require('node:child_process');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');

const root = path.resolve(__dirname, '../../frontend');
const types = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.png': 'image/png', '.svg': 'image/svg+xml' };

/** Python fixture를 시작하고 포트를 읽는다. 실패하면 원인만 전달하며 원문 대화는 기록하지 않는다. */
async function fixture(origin) {
  const child = spawn(process.env.PYTHON || 'python', ['-X', 'utf8', path.join(__dirname, 'agent_http_fixture.py'), origin],
    { windowsHide: true, stdio: ['pipe', 'pipe', 'pipe'] });
  let errors = '';
  child.stderr.on('data', (chunk) => { errors += chunk.toString(); });
  try {
    const base = await new Promise((resolve, reject) => {
      const timer = setTimeout(() => reject(new Error(`HTTP fixture 시작 시간 초과: ${errors}`)), 10000);
      let buffer = '';
      child.once('error', (error) => { clearTimeout(timer); reject(error); });
      child.once('exit', (code) => { clearTimeout(timer); reject(new Error(`HTTP fixture 종료 ${code}: ${errors}`)); });
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

/** 자식 프로세스에 종료를 요청하고 시간 내 정리되지 않으면 이 테스트가 만든 프로세스만 종료한다. */
async function stopFixture(child) {
  if (!child || child.exitCode !== null) return;
  await new Promise((resolve) => {
    const timer = setTimeout(() => { child.kill(); resolve(); }, 3000);
    child.once('exit', () => { clearTimeout(timer); resolve(); });
    child.stdin.end('\n');
  });
}

/** 실제 프론트를 제공하고 API 응답은 가로채지 않은 채 브라우저의 결과를 검증한다. */
async function main() {
  let apiBase;
  const server = http.createServer((req, res) => {
    const relative = decodeURIComponent(new URL(req.url, 'http://localhost').pathname).replace(/^\/+/, '') || 'index.html';
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
  let browser, child;
  try {
    await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
    const base = `http://agent.localhost:${server.address().port}`;
    ({ child, base: apiBase } = await fixture(base));
    browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH, headless: true,
      args: ['--host-resolver-rules=MAP *.localhost 127.0.0.1', '--no-proxy-server'] });
    const page = await browser.newPage();
    page.setDefaultTimeout(10000);
    await page.route('**/*', async (route) => {
      if ([new URL(base).origin, new URL(apiBase).origin].includes(new URL(route.request().url()).origin)) await route.continue();
      else await route.abort();
    });
    const chatResponses = [], recommendationResponses = [];
    page.on('response', (response) => {
      if (response.request().method() !== 'POST') return;
      if (response.url().endsWith('/preview/chat')) chatResponses.push(response);
      if (response.url().endsWith('/preview/recommend')) recommendationResponses.push(response);
    });
    await page.addInitScript(() => sessionStorage.setItem('lab678_chat', JSON.stringify({
      draft: { category: '전시', categories: ['전시'], date: '2026-11-02', startTime: '14:00', endTime: '17:00',
        startLocation: { label: '시청', address: '서울 중구 세종대로', lat: 37.56, lng: 126.98 }, free_only: false },
      messages: [], revision: 0, mode: 'text', sound: false,
    })));
    const send = async (text) => {
      await page.locator('#chat-input').fill(text);
      await page.locator('#chat-form').evaluate((form) => form.requestSubmit());
    };
    const read = () => page.evaluate(() => JSON.parse(sessionStorage.getItem('lab678_chat')));
    await page.goto(`${base}/?agent=legacy#/chat?text`);
    await send('무료만 가능한 가까운 곳');
    await page.locator('.chat-card').first().waitFor();
    assert.equal(chatResponses.length, 1);
    assert.equal(chatResponses[0].headers()['access-control-allow-origin'], base, '브라우저가 실제 CORS 응답을 수신');
    assert.deepEqual((await recommendationResponses[0].json()).candidates.map((item) => item.fee_type), ['무료']);

    // 잘못된 모델 후보를 HTTP 경계에서 차단하고 사용자 재확인 후에만 검색한다.
    await send('무료만 아닌 유료도 괜찮아요');
    await page.waitForFunction(() => JSON.parse(sessionStorage.getItem('lab678_chat')).clarification?.fields?.includes('free_only'));
    assert.equal(recommendationResponses.length, 1);
    assert.equal((await chatResponses.at(-1).json()).interpretation_status, 'needs_clarification');
    await send('유료도 괜찮아요');
    await page.getByRole('button', { name: '유료도 포함으로 바꾸기' }).click();
    await page.waitForFunction(() => JSON.parse(sessionStorage.getItem('lab678_chat')).pool?.length === 2);
    assert.equal((await read()).clarification, null);
    assert.equal((await read()).draft.free_only, false);

    // 실제 서버가 같은 label도 재검색하도록 하고 좌표 선택·동의 경계를 보존한다.
    await send('출발지는 시청으로 바꿔줘');
    await page.getByRole('button', { name: '시청 · 경기 수원시 효원로', exact: true }).click();
    await page.getByRole('button', { name: '시청 · 서울 중구 세종대로 유지' }).click();
    assert.equal((await read()).draft.startLocation.lat, 37.56);
    await send('출발지는 시청으로 바꿔줘');
    await page.getByRole('button', { name: '시청 · 경기 수원시 효원로', exact: true }).click();
    const nextSearch = page.waitForResponse((response) => response.url().endsWith('/preview/recommend') && response.request().method() === 'POST');
    await page.getByRole('button', { name: '시청 · 경기 수원시 효원로로 바꾸기' }).click();
    await nextSearch;
    assert.equal((await read()).draft.startLocation.lat, 37.26);
    assert.equal(recommendationResponses.at(-1).request().postDataJSON().start_location.lat, 37.26);
    console.log('PASS: 실제 브라우저 CORS·HTTP 대화 검증·무료 필터·보류 재확인·동명 장소 선택/거절');
  } finally {
    if (browser) await browser.close();
    await stopFixture(child);
    await new Promise((resolve) => server.close(resolve));
  }
}

main().catch((error) => { console.error(error); process.exitCode = 1; });
