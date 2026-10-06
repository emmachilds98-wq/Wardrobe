// Weekly refresh fallback: product pages that refuse a plain request are opened in headless Chromium,
// and their schema.org (JSON-LD) blocks are handed back to weekly_refresh.py to read price and stock.
// Usage: node browser_check.js in.json out.json   (in.json: {"id": "https://..."}; needs playwright)
const {chromium} = require('playwright'); const fs = require('fs');
const urls = JSON.parse(fs.readFileSync(process.argv[2])); const out = process.argv[3];
(async () => {
  const b = await chromium.launch({args: ['--disable-blink-features=AutomationControlled']});
  const ctx = await b.newContext({userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36',
    locale: 'en-GB', viewport: {width: 1280, height: 900}});
  // Photos, fonts and media are not needed to read the price.
  await ctx.route('**/*', r => ['image', 'media', 'font'].includes(r.request().resourceType()) ? r.abort() : r.continue());
  const res = {}; const q = Object.keys(urls);
  async function one(id) {
    const p = await ctx.newPage();
    try {
      const r = await p.goto(urls[id], {waitUntil: 'domcontentloaded', timeout: 35000});
      await p.waitForTimeout(2000);
      const ld = await p.$$eval('script[type="application/ld+json"]', s => s.map(x => x.textContent));
      // Some pages leave the price out of their JSON-LD but carry it in meta tags.
      const price = await p.evaluate(() => {
        const e = document.querySelector('meta[property="product:price:amount"],meta[itemprop="price"],[itemprop="price"][content]');
        return e ? e.getAttribute('content') : null;
      });
      res[id] = {status: r ? r.status() : 0, url: p.url(), ld, price, title: (await p.title()).slice(0, 80)};
    } catch (e) { res[id] = {status: 0, err: String(e.message).split('\n')[0].slice(0, 100)}; }
    finally { await p.close(); }
  }
  await Promise.all(Array.from({length: 4}, async () => { while (q.length) await one(q.shift()); }));
  fs.writeFileSync(out, JSON.stringify(res));
  await b.close();
  const ok = Object.values(res).filter(r => r.ld && r.ld.length).length;
  console.log('browser: ' + ok + ' of ' + Object.keys(urls).length + ' pages gave product data');
})();
