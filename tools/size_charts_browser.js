// Helper for size_charts.py: opens size-guide pages in headless Chromium (for shops that refuse plain
// requests or draw their chart with JavaScript) and saves the rendered HTML for the Python side to read.
// Usage: NODE_PATH=/opt/node-tools/node_modules node tools/size_charts_browser.js jobs.json
//   jobs.json: [{"url": "...", "out": "/path/page.html", "click": "optional text of a size-guide button",
//                "select": [["css selector", "option value"], ...], "wait": "optional CSS selector to wait for"}]
// Direct visits to the shop's own pages only: no relays, readers or caches.
const {chromium} = require('playwright');
const fs = require('fs');
const jobs = JSON.parse(fs.readFileSync(process.argv[2]));
(async () => {
  const b = await chromium.launch({channel: 'chromium', args: ['--disable-blink-features=AutomationControlled']});
  const ctx = await b.newContext({
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36',
    locale: 'en-GB', timezoneId: 'Europe/London', viewport: {width: 1366, height: 900}});
  async function one(j) {
    const p = await ctx.newPage();
    try {
      const r = await p.goto(j.url, {waitUntil: 'domcontentloaded', timeout: 45000});
      await p.waitForTimeout(j.pause || 3500);
      // close cookie banners so they do not cover buttons
      await p.click('#onetrust-accept-btn-handler', {timeout: 1500}).catch(() => {});
      await p.evaluate(() => { const o = document.getElementById('onetrust-consent-sdk'); if (o) o.remove(); }).catch(() => {});
      for (const t of ['Accept All', 'Accept all', 'Accept All Cookies', 'Accept Cookies', 'Allow all', 'I Accept', 'Accept']) {
        const btn = p.getByRole('button', {name: t, exact: true});
        if (await btn.count().catch(() => 0)) { await btn.first().click({timeout: 2000}).catch(() => {}); break; }
      }
      // drop-down pickers, e.g. [["#category", "men"], ["#subCategory", "tops"]]
      for (const [sel, val] of (j.select || [])) {
        await p.selectOption(sel, val, {timeout: 8000}).catch(() => {});
        await p.waitForTimeout(2000);
      }
      if (j.click) {
        const el = p.getByText(new RegExp(j.click, 'i')).first();
        await el.click({timeout: 8000}).catch(() => {});
        await p.waitForTimeout(2500);
      }
      if (j.wait) await p.waitForSelector(j.wait, {timeout: 15000}).catch(() => {});
      // include same-origin iframes (some shops put the chart in one)
      let html = await p.content();
      for (const f of p.frames().slice(1)) {
        try { html += '\n<!-- frame ' + f.url() + ' -->\n' + await f.content(); } catch (e) {}
      }
      fs.writeFileSync(j.out, html);
      console.log(JSON.stringify({url: j.url, status: r ? r.status() : 0, bytes: html.length}));
    } catch (e) {
      console.log(JSON.stringify({url: j.url, error: String(e.message).split('\n')[0].slice(0, 120)}));
    } finally { await p.close(); }
  }
  const q = jobs.slice();
  await Promise.all(Array.from({length: 4}, async () => { while (q.length) await one(q.shift()); }));
  await b.close();
})();
