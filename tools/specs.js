#!/usr/bin/env node
/* The stored product specs (phase 1 of the 3D plan): what the page reads for every piece worn in an outfit, written
   to data/specs.json, one line per piece, so a change to how a piece is read shows up as a diff in the pull request
   rather than only on the model.

   For each item and the shape it is worn as, it runs the page's own readers, exactly as the page does when the card
   is shown: the listing words (descOf: cut, collar, neck, zip, pockets, cloth, details), the shop photo (sampleLook:
   colours, pattern and its spacing, whether the photo's own front is laid on, a model shot, a close-up, a chest
   print, soles), and the corrections in data/fixes.json (pieceLook). Each colour and pattern says where it came from
   and how far to trust it:
     colour  fix 1.0 (data/fixes.json) · photo+name 0.9 (the photo agrees with the colour the listing names) ·
             photo+navy 0.85 (a navy photo lifted toward the named navy) · photo 0.7 (the listing names no colour) ·
             name 0.6 (the photo disagreed and the named colour won) · outfit 0.4 (no photo: the outfit's colour word)
     pattern fix 1.0 · swatch 1.0 (a cloth square from fixes.json) · plain 0.9 (no pattern named or seen) ·
             photo+name 0.85 (named in the listing and drawn from the photo) · photo 0.6 (seen in the photo only) ·
             unseen 0.5 (named, but the photo read plain)

     node tools/specs.js [--site docs] [--out data/specs.json]

   The pull-request check runs it on the built site and compares with data/specs.json (tools/qa/specs_diff.py);
   after a change to the readers, fixes.json or the outfits, run it and commit data/specs.json with the change. That
   check also refuses any piece read "unseen" (a pattern its listing names drawn plain): look at its photo and record in
   data/fixes.json either the pattern or that plain is right. A Fair Isle jumper once drew plain navy that way. */
const fs = require("fs"), path = require("path"), http = require("http");
let chromium;
try { ({ chromium } = require("playwright")); } catch (e) {
  try { ({ chromium } = require("/opt/node-tools/node_modules/playwright")); } catch (e2) { console.error("Playwright is needed: npm i playwright"); process.exit(1); }
}
const ROOT = path.join(__dirname, "..");
const arg = (k, d) => { const i = process.argv.indexOf("--" + k); return i < 0 ? d : process.argv[i + 1]; };
const SITE = path.resolve(ROOT, arg("site", "docs")), OUT = path.resolve(ROOT, arg("out", "data/specs.json"));

function serve(dir) {
  const types = { ".html": "text/html", ".json": "application/json", ".js": "text/javascript" };
  return new Promise(res => {
    const s = http.createServer((q, r) => {
      const u = decodeURIComponent(q.url.split("?")[0]); const f = path.join(dir, u === "/" ? "index.html" : u);
      if (!f.startsWith(dir) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { r.writeHead(404); r.end(); return; }
      r.writeHead(200, { "Content-Type": types[path.extname(f)] || "application/octet-stream" }); fs.createReadStream(f).pipe(r);
    }).listen(0, () => res(s));
  });
}

/* runs in the page: one piece's spec */
async function specOf(q) {
  const X = window.__qa(), it = X.byId[q.item];
  if (!it) return null;
  if (X.LOOK[q.item] === undefined && it.ph) {
    const src = await new Promise(r => X.getPh(q.item, r));
    if (src) { const L = await X.sampleLook(src, q.shape, X.descOf(it, q)); X.LOOK[q.item] = L || null; X.TRUE[q.item] = L ? L.str : ""; }
    else X.LOOK[q.item] = null;
  }
  const D = X.descOf(it, q), P = X.pieceLook(q), L = P.look || null, F = it.fix || {};
  const Fs = Object.assign({}, F, (F.shapes && F.shapes[q.shape]) || {});
  const out = { shape: q.shape };
  // colour
  let cs, cc;
  if (Fs.col) { cs = "fix"; cc = 1; }
  else if (!L) { cs = "outfit"; cc = 0.4; }
  else if (L.named && L.c1p) { cs = "name"; cc = 0.6; }
  else if (L.c1p) { cs = "photo+navy"; cc = 0.85; }
  else if (D.colRef && !D.colRef.out) { cs = "photo+name"; cc = 0.9; }
  else { cs = "photo"; cc = 0.7; }
  out.colour = { main: (L && L.c1) || P.col || "", second: (L && L.c2) || P.col2 || "", named: (D.colRef && D.colRef.w) || "", src: cs, conf: cc };
  if (L && L.c1p) out.colour.photo = L.c1p;
  // pattern
  const pat = (L && L.pat) || "plain", named = !!(D.stripe || D.check || D.print);
  let ps, pc;
  if (Fs.swatch) { ps = "swatch"; pc = 1; }
  else if (Fs.pat) { ps = "fix"; pc = 1; }
  else if (pat === "plain") { ps = named ? "unseen" : "plain"; pc = named ? 0.5 : 0.9; }
  else if (named) { ps = "photo+name"; pc = 0.85; }
  else { ps = "photo"; pc = 0.6; }
  out.pattern = { kind: pat, src: ps, conf: pc };
  if (L && L.per) out.pattern.per = +(+L.per).toFixed(3);
  if (L && L.duty) out.pattern.duty = +(+L.duty).toFixed(3);
  // cut, cloth and details from the listing
  const cut = {};
  ["fit", "collar", "neck", "zip", "pockets", "mat"].forEach(k => { if (D[k]) cut[k] = D[k]; });
  if (it.fit) cut.listed_fit = it.fit;
  if (it.fabric) cut.fabric = it.fabric;
  out.cut = cut;
  const det = ["tipped", "rugby", "raglan", "ringer", "pleat", "turnup", "drawcord", "chunky", "slvStripe", "graphic", "aop"].filter(k => D[k]);
  if (det.length) out.details = det;
  // what the photo reader found
  if (L) {
    const ph = {};
    ["front", "model", "close", "decal"].forEach(k => { if (L[k]) ph[k] = true; });
    ["sole", "acc", "slv"].forEach(k => { if (L[k]) ph[k] = L[k]; });
    if (Object.keys(ph).length) out.photo = ph;
  } else out.photo = { none: true };
  /* (the frame shape a pair of sunglasses is drawn with, from its listing: a change shows in the pull request) */
  if (q.shape === "sunglasses" && X.sgKind) out.form = X.sgKind(((it.name || "") + " " + (q.what || "")).toLowerCase());
  if (it.fix) out.fixed = Object.keys(Fs).filter(k => k !== "shapes").sort();
  return out;
}

(async () => {
  if (!fs.existsSync(path.join(SITE, "index.html"))) { console.error("No site at " + SITE + " (build it with tools/build_site.py)"); process.exit(1); }
  const srv = await serve(SITE), port = srv.address().port;
  const b = await chromium.launch({ executablePath: process.env.CHROME_PATH || (fs.existsSync("/opt/pw-browsers/chromium-1194/chrome-linux/chrome") ? "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" : undefined) });
  const p = await b.newPage(), errs = []; p.on("pageerror", e => errs.push(e.message));
  await p.addInitScript(() => { try { localStorage.setItem("dw-fig", "2d"); } catch (e) {} });
  await p.goto("http://localhost:" + port + "/index.html?qa=1#fits");
  await p.waitForFunction(() => window.__qa && Object.keys(window.__qa().fitById).length > 0, null, { timeout: 120000 });
  // every item and the shape it is worn as, in the outfits' own order
  const pairs = await p.evaluate(() => {
    const X = window.__qa(), seen = {}, out = [];
    Object.keys(X.fitById).sort().forEach(id => X.fitById[id].pieces.forEach(q => {
      const k = q.item + "|" + q.shape; if (!q.item || seen[k] || !X.byId[q.item]) return; seen[k] = 1;
      out.push({ item: q.item, shape: q.shape, col: q.col || "", what: q.what || "" });
    }));
    return out;
  });
  const specs = {};
  for (let i = 0; i < pairs.length; i += 25) {
    const part = await p.evaluate(async ({ qs, fn }) => {
      const f = eval("(" + fn + ")"), r = {};
      for (const q of qs) { try { r[q.item + "|" + q.shape] = await f(q); } catch (e) { r[q.item + "|" + q.shape] = { error: String(e.message || e) }; } }
      return r;
    }, { qs: pairs.slice(i, i + 25), fn: specOf.toString() });
    Object.assign(specs, part);
    process.stdout.write("\r" + Math.min(i + 25, pairs.length) + "/" + pairs.length + " pieces");
  }
  await b.close(); srv.close();
  const keys = Object.keys(specs).filter(k => specs[k]).sort();
  const body = keys.map(k => JSON.stringify(k) + ":" + JSON.stringify(specs[k])).join(",\n");
  fs.writeFileSync(OUT, "{\n" + body + "\n}\n");
  console.log("\n" + keys.length + " pieces -> " + path.relative(ROOT, OUT) + (errs.length ? " (page errors: " + errs.slice(0, 3).join("; ") + ")" : ""));
  if (errs.length) process.exitCode = 1;
})();
