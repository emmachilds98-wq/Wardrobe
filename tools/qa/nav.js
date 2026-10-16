// node tools/qa/nav.js [--site docs] : checks every way in to a view or a dialog has a way back out, on a desktop and
// a phone screen. Moves between the views with the menu and walks Back and Forward through them; the title takes him
// to the start (Shop) without reloading; an outfit's large view (the fitting room) closes with Escape, Back and its
// own button (Close on a desktop, ‹ on a phone), and opens from a shared #fit/<id> link; Edit Dave closes with Back
// (leaving the large view under it open), and with changes not saved asks first (Save and close, Discard changes,
// Keep editing) whether it is closed with its button, Escape or Back; Compare closes with Back, Escape and its own
// button, and Back from Compare opened over the large view returns to the outfits. Any page error fails the run.
// Prints one line per check; exits 1 when any fails. QA_PORT=<port> uses a server already running instead of --site.
const http = require("http"), fs = require("fs"), path = require("path");
let chromium;
try { ({ chromium } = require("playwright")); } catch (e) {
  try { ({ chromium } = require("/opt/node22/lib/node_modules/playwright")); } catch (e2) { console.error("Playwright is needed: npm i playwright"); process.exit(1); }
}
const ROOT = path.join(__dirname, "..", "..");
const arg = (k, d) => { const i = process.argv.indexOf("--" + k); return i < 0 ? d : process.argv[i + 1]; };
const SITE = path.resolve(ROOT, arg("site", "docs"));

function serve(dir) {
  const types = { ".html": "text/html", ".json": "application/json", ".js": "text/javascript", ".png": "image/png", ".webp": "image/webp", ".jpg": "image/jpeg", ".svg": "image/svg+xml" };
  return new Promise(res => {
    const s = http.createServer((q, r) => {
      const u = decodeURIComponent(q.url.split("?")[0]); const f = path.join(dir, u === "/" ? "index.html" : u);
      if (!f.startsWith(dir) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { r.writeHead(404); r.end(); return; }
      r.writeHead(200, { "Content-Type": types[path.extname(f)] || "application/octet-stream" }); fs.createReadStream(f).pipe(r);
    }).listen(0, () => res(s));
  });
}

let fails = 0;
function ok(scr, name, pass, more) { if (!pass) fails++; console.log((pass ? "ok   " : "FAIL ") + scr.padEnd(8) + name + (more ? "  (" + more + ")" : "")); }

async function run(b, base, scr) {
  const phone = scr === "phone";
  const ctx = await b.newContext(phone ? { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 } : { viewport: { width: 1280, height: 850 } });
  const p = await ctx.newPage(), errs = [];
  p.on("pageerror", e => errs.push(e.message));
  const S = () => p.evaluate(() => { const o = id => !!(document.getElementById(id) || {}).open; return { hash: location.hash, view: document.body.getAttribute("data-v"), zoom: o("zoom"),
    ce: o("chared"), cmp: o("cmp"), ask: !(document.getElementById("ce-ask") || { hidden: true }).hidden,
    dlg: (history.state || {}).dlg || "", mark: !!window.__navMark }; });
  const wait = (ms) => p.waitForTimeout(ms);
  // the control is on screen and can be pressed (not display:none, not zero-sized)
  const shown = (sel) => p.evaluate(s => [...document.querySelectorAll(s)].some(e => { const r = e.getBoundingClientRect(), c = getComputedStyle(e); return r.width > 0 && r.height > 0 && c.visibility !== "hidden" && c.display !== "none"; }), sel);
  // presses the first one on screen (as a click from the page: a mouse click waits on the 3D model, slow in software)
  const tap = async (sel) => { const h = await p.$$(sel); for (const e of h) { if (await e.isVisible()) { await e.evaluate(x => x.click()); return true; } } return false; };

  await p.goto(base + "/#shop", { waitUntil: "networkidle" }); await wait(1500);
  await p.evaluate(() => { window.__navMark = 1; });

  // the views, with the menu, then Back and Forward through them
  const order = ["fits", "build", "list", "guide", "mine", "sale"], seen = [];
  for (const v of order) { const did = await tap('[data-go="' + v + '"]:not(a)'); await wait(250); const s = await S(); seen.push(s.view); if (!did) ok(scr, "menu has " + v, false, "no visible button"); }
  ok(scr, "menu moves between the views", seen.join() === order.join(), seen.join());
  ok(scr, "menu on screen after scrolling", await (async () => { await p.evaluate(() => window.scrollTo(0, 3000)); await wait(200); const r = await shown('.mast [data-go="fits"]:not(a), nav [data-go="fits"]:not(a)'); await p.evaluate(() => window.scrollTo(0, 0)); return r; })());
  const back = [];
  for (let i = 0; i < order.length; i++) { await p.goBack(); await wait(250); back.push((await S()).view); }
  ok(scr, "Back walks back through the views", back.join() === order.slice(0, -1).reverse().concat("shop").join(), back.join());
  await p.goForward(); await wait(250);
  ok(scr, "Forward", (await S()).view === "fits");

  // the title is a way to the start
  await tap('[data-go="guide"]:not(a)'); await wait(250);
  await tap("#mast-h a"); await wait(400);
  let s = await S();
  ok(scr, "title goes to the start (Shop)", s.view === "shop" && s.hash === "#shop" && s.mark, JSON.stringify(s));
  await p.goBack(); await wait(250);
  ok(scr, "Back after the title returns", (await S()).view === "guide");

  // an outfit's large view
  await tap('[data-go="fits"]:not(a)'); await wait(800);
  const card = '#fit-grid [data-zoom]';
  const openFit = async () => { await p.evaluate(c => document.querySelector(c).click(), card); await wait(1500); return S(); };
  s = await openFit();
  const fid = decodeURIComponent((s.hash.match(/^#fit\/(.+)$/) || [])[1] || "");
  ok(scr, "outfit opens large, with its own address", s.zoom && !!fid, s.hash);
  ok(scr, "large view has a visible way out", await shown(phone ? "#zoom .fr-back" : "#zoom .fr-x"));
  await p.keyboard.press("Escape"); await wait(600); s = await S();
  ok(scr, "Escape closes the large view", !s.zoom && s.hash === "#fits", JSON.stringify(s));
  await openFit(); await p.goBack(); await wait(800); s = await S();
  ok(scr, "Back closes the large view", !s.zoom && s.hash === "#fits" && s.view === "fits", JSON.stringify(s));
  await openFit(); await tap(phone ? "#zoom .fr-back" : "#zoom .fr-x"); await wait(800); s = await S();
  ok(scr, "its button closes the large view", !s.zoom && s.hash === "#fits", JSON.stringify(s));
  await p.goBack(); await wait(400); s = await S();
  ok(scr, "Back after closing it leaves the outfits", !s.zoom && s.view !== "fits", JSON.stringify(s));

  // Edit Dave over the large view
  await p.goto(base + "/#fit/" + encodeURIComponent(fid), { waitUntil: "networkidle" }); await wait(2500); s = await S();
  ok(scr, "a shared outfit link opens it large", s.zoom && s.view === "fits", JSON.stringify(s));
  const openCE = async () => { await p.evaluate(() => document.querySelector("#zoom [data-chared]").click()); await wait(1500); return S(); };
  s = await openCE();
  ok(scr, "Edit Dave opens from the outfit", s.ce && s.zoom && s.dlg === "ce", JSON.stringify(s));
  ok(scr, "Edit Dave has a visible way out", await shown(phone ? "#chared .ce-cancel" : "#chared .fr-x"));
  await p.goBack(); await wait(800); s = await S();
  ok(scr, "Back closes Edit Dave, keeps the outfit", !s.ce && s.zoom && s.hash === "#fit/" + encodeURIComponent(fid), JSON.stringify(s));
  // with a change not saved
  const change = () => p.evaluate(() => { const r = document.querySelector('#chared input[type="range"][data-cer]'); if (!r) return false; r.value = String(Math.min(+r.max, +r.value + (+r.max - +r.min) / 4)); r.dispatchEvent(new Event("input", { bubbles: true })); return true; });
  await openCE(); ok(scr, "a slider in Edit Dave", await change());
  const saved0 = await p.evaluate(() => localStorage.getItem("dw-char"));
  await tap(phone ? "#chared .ce-cancel" : "#chared .fr-x"); await wait(300); s = await S();
  ok(scr, "closing with a change asks first", s.ce && s.ask, JSON.stringify(s));
  await tap('#ce-ask [data-ceask="keep"]'); await wait(200); s = await S();
  ok(scr, "Keep editing stays", s.ce && !s.ask);
  await p.keyboard.press("Escape"); await wait(300); s = await S();
  ok(scr, "Escape with a change asks", s.ce && s.ask);
  await p.keyboard.press("Escape"); await wait(300); s = await S();
  ok(scr, "Escape again dismisses the question", s.ce && !s.ask);
  await p.goBack(); await wait(600); s = await S();
  ok(scr, "Back with a change asks, Edit Dave stays a step", s.ce && s.ask && s.dlg === "ce", JSON.stringify(s));
  await tap('#ce-ask [data-ceask="discard"]'); await wait(800); s = await S();
  ok(scr, "Discard closes, outfit stays", !s.ce && s.zoom && !s.dlg, JSON.stringify(s));
  ok(scr, "Discard keeps the saved Dave", (await p.evaluate(() => localStorage.getItem("dw-char"))) === saved0);
  await openCE(); await change(); await p.keyboard.press("Escape"); await wait(300);
  await tap('#ce-ask [data-ceask="save"]'); await wait(800); s = await S();
  ok(scr, "Save and close saves", !s.ce && s.zoom && !s.dlg && (await p.evaluate(() => localStorage.getItem("dw-char"))) !== saved0, JSON.stringify(s));
  await p.keyboard.press("Escape"); await wait(600); s = await S();
  ok(scr, "then the outfit closes as usual", !s.zoom && s.hash === "#fits", JSON.stringify(s));

  // Edit Dave from a page, closed with no change: no extra step left in history
  await tap('[data-go="guide"]:not(a)'); await wait(300); await tap('[data-go="mine"]:not(a)'); await wait(300);
  const n0 = await p.evaluate(() => history.length);
  await p.evaluate(() => document.querySelector('[data-v="mine"] [data-chared], #v-mine [data-chared], section [data-chared]') ? document.querySelector('[data-v="mine"] [data-chared], #v-mine [data-chared], section [data-chared]').click() : document.querySelector("[data-chared]").click());
  await wait(1200); s = await S(); const ceOn = s.ce;
  await p.keyboard.press("Escape"); await wait(600); s = await S();
  ok(scr, "Edit Dave from a page closes with Escape", ceOn && !s.ce && !s.dlg, JSON.stringify(s));
  await p.goBack(); await wait(400); s = await S();
  ok(scr, "then Back goes to the view before", s.view === "guide", JSON.stringify(s) + " history " + n0);

  // Compare
  await tap('[data-go="fits"]:not(a)'); await wait(800);
  const openCmp = async () => { await p.evaluate(() => document.querySelector("#fit-grid [data-cmpadd]").click()); await wait(1200); return S(); };
  s = await openCmp();
  ok(scr, "Compare opens", s.cmp && s.dlg === "cmp", JSON.stringify(s));
  ok(scr, "Compare has a visible way out", await shown(phone ? "#cmp .fr-back" : "#cmp .fr-acts [data-cmpclose]"));
  const hb = await p.evaluate(() => { const r = document.querySelector("#cmp .cmp-head").getBoundingClientRect(); return [Math.round(r.top), Math.round(r.height)]; });
  ok(scr, "Compare's header has room", hb[0] >= 0 && hb[1] >= 40, "top " + hb[0] + ", height " + hb[1]);
  await p.goBack(); await wait(600); s = await S();
  ok(scr, "Back closes Compare", !s.cmp && s.view === "fits" && !s.dlg, JSON.stringify(s));
  await openCmp(); await p.keyboard.press("Escape"); await wait(600); s = await S();
  ok(scr, "Escape closes Compare", !s.cmp && !s.dlg, JSON.stringify(s));
  await openCmp(); await tap(phone ? "#cmp .fr-back" : "#cmp .fr-acts [data-cmpclose]"); await wait(600); s = await S();
  ok(scr, "its button closes Compare", !s.cmp && !s.dlg, JSON.stringify(s));
  if (!phone) {   // (a phone's large view keeps Compare to the outfit cards)
    await openFit(); await tap("#zoom .fr-cmp"); await wait(1200); s = await S();
    ok(scr, "Compare from the large view takes its place", s.cmp && !s.zoom && s.dlg === "cmp", JSON.stringify(s));
    await p.goBack(); await wait(800); s = await S();
    ok(scr, "Back from it returns to the outfits", !s.cmp && !s.zoom && s.hash === "#fits", JSON.stringify(s));
  }

  // a reload keeps no dialog step
  await openCmp(); await p.reload({ waitUntil: "networkidle" }); await wait(1500); s = await S();
  ok(scr, "after a reload no dialog is a step", !s.cmp && !s.dlg, JSON.stringify(s));

  ok(scr, "no page errors", !errs.length, errs.slice(0, 3).join(" | "));
  await ctx.close();
}

(async () => {
  let srv = null, base;
  if (process.env.QA_PORT) base = "http://localhost:" + process.env.QA_PORT;
  else { if (!fs.existsSync(path.join(SITE, "index.html"))) { console.error("No site at " + SITE + " (build it with tools/build_site.py)"); process.exit(1); } srv = await serve(SITE); base = "http://localhost:" + srv.address().port; }
  const b = await chromium.launch({ executablePath: process.env.CHROME_PATH || (fs.existsSync("/opt/pw-browsers/chromium-1194/chrome-linux/chrome") ? "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" : undefined),
    args: ["--use-gl=swiftshader", "--enable-unsafe-swiftshader"] });
  for (const scr of ["desktop", "phone"]) await run(b, base, scr);
  await b.close(); if (srv) srv.close();
  console.log(fails ? fails + " failed" : "all passed"); process.exit(fails ? 1 : 0);
})();
