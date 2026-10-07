#!/usr/bin/env node
/* The automatic 3D checks: renders every outfit on Dave's 3D model from the front, the side and the back, and
   counts what should never be seen.
     - poke: an inner layer (or his skin) showing through a piece worn over it, as islands inside the outer piece;
     - holes: background showing through the clothes;
     - stray: small bits of a piece standing off on their own;
     - colour: a plain piece whose rendered colour is far from its shop colour (hue, or much too light or dark).
   Each view is drawn twice: once as the page shows it, and once with every piece in its own flat colour (an "ID"
   pass), which is what the counts are made on.

     node tools/check_3d.js [--site docs] [--ids a,b] [--sample N] [--out qa] [--report]

   --site     the built site to serve (default docs/, built by tools/build_site.py)
   --ids      only these outfits; --sample N: every outfit's N-th share (a spread of N outfits)
   --out      where the report and the pictures of flagged outfits go (default qa/)
   --report   also write the summary into data/refresh-report.json ("checks_3d")
   Needs Playwright and Chromium (CHROME_PATH to use a particular Chromium). */
const fs = require("fs"), path = require("path"), http = require("http");
let chromium;
try { ({ chromium } = require("playwright")); } catch (e) {
  try { ({ chromium } = require("/opt/node22/lib/node_modules/playwright")); } catch (e2) { console.error("Playwright is needed: npm i playwright"); process.exit(1); }
}
const ROOT = path.join(__dirname, "..");
const arg = (k, d) => { const i = process.argv.indexOf("--" + k); return i < 0 ? d : (process.argv[i + 1] && !process.argv[i + 1].startsWith("--") ? process.argv[i + 1] : true); };
const SITE = path.resolve(ROOT, arg("site", "docs")), OUT = path.resolve(ROOT, arg("out", "qa"));
const LIMITS = { poke: 30, holes: 25, stray: 40 };

function serve(dir) {
  const types = { ".html": "text/html", ".json": "application/json", ".js": "text/javascript", ".png": "image/png", ".webp": "image/webp" };
  return new Promise(res => {
    const s = http.createServer((q, r) => {
      const u = decodeURIComponent(q.url.split("?")[0]); const f = path.join(dir, u === "/" ? "index.html" : u);
      if (!f.startsWith(dir) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { r.writeHead(404); r.end(); return; }
      r.writeHead(200, { "Content-Type": types[path.extname(f)] || "application/octet-stream" }); fs.createReadStream(f).pipe(r);
    }).listen(0, () => res(s));
  });
}

/* runs in the page: builds the outfit, renders the three views (as shown, and the ID pass) and measures them */
async function checkOutfit(arg) {
  const id = arg.id, dbg = arg.dbg;
  const X = window.__qa(), T = window.THREE, f = X.fitById[id];
  if (!f) return { id, error: "no such outfit" };
  const ps = X.effPieces(f);
  for (const p of ps) {   // the shop photo reading, as the page does when the card is shown
    const it = X.byId[p.item]; if (!it || p.fixed || X.LOOK[p.item] !== undefined) continue;
    const src = await new Promise(r => X.getPh(p.item, r)); if (!src) { X.LOOK[p.item] = null; continue; }
    const L = await X.sampleLook(src, p.shape, X.descOf(it, p)); X.LOOK[p.item] = L || null; X.TRUE[p.item] = L ? L.str : "";
  }
  const W = 300, H = 440;
  if (!window.__qaR) { window.__qaR = new T.WebGLRenderer({ antialias: false, preserveDrawingBuffer: true }); window.__qaR.setSize(W, H); }
  const r = window.__qaR, gl = r.getContext();
  const o = X.make3D(ps);
  const cam = new T.PerspectiveCamera(13, W / H, 0.1, 50); cam.position.set(0, 0.95, 8.7); cam.lookAt(0, 0.93, 0);
  /* classes in the ID pass: 0 background, 20 body, 40 legwear, 50 shoes, 60.. tops (inner to outer), 140 the rest;
     a piece's parts laid deliberately over the piece worn over it (a hood on a jacket's back) count as that outer piece */
  const kinds = []; o.scene.traverse(n => { if (n.isMesh) kinds.push(n); });
  const upN = ps.filter(p => /^(coat|jacket|blazer|gilet|gown|waistcoat|cardigan|hoodie|jumper|rollneck|halfzip|shirt|sshirt|polo|tee|vest)$/.test(p.shape)).length + 1;
  function cls(n) { if (n.material && n.material.type === "ShadowMaterial") return 0;   // the floor's shadow
    const k = n.userData.kind || "body"; if (k === "body") return 20; if (k === "lo") return 40; if (k === "ft") return 50; if (k === "acc") return 140;
    const m = /^up(\d+)(o?)$/.exec(k); if (m) return 60 + 10 * (m[2] ? upN : +m[1]); return 140; }
  const orig = new Map(); kinds.forEach(n => orig.set(n, n.material));
  const openC = {}; kinds.forEach(n => { if (n.userData.open) openC[cls(n)] = 1; });   // pieces worn open (their front shows what is under them)
  /* which meshes hang from an arm (sleeves, cuffs, hands, the arm itself): a gap between an arm and his body is the
     background seen past his side, not a hole in the clothes */
  const onArm = n => { for (let a = n; a; a = a.parent) if (a.userData && a.userData.arm) return true; return false; };
  const armOf = new Map(); kinds.forEach(n => armOf.set(n, onArm(n)));
  const armM = new T.MeshBasicMaterial({ color: new T.Color(1, 1, 1), side: T.DoubleSide }), restM = new T.MeshBasicMaterial({ color: new T.Color(0.5, 0.5, 0.5), side: T.DoubleSide });
  /* a top is one piece, sleeves and all: its own arm mask (per vertex) says which parts are sleeve */
  const maskM = new T.ShaderMaterial({ side: T.DoubleSide,
    vertexShader: "attribute float armF; varying float vA; void main(){ vA = armF; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }",
    fragmentShader: "varying float vA; void main(){ gl_FragColor = vec4(vA > 0.5 ? 1.0 : 0.5, 0.0, 0.0, 1.0); }" });
  const armMat = n => { if (armOf.get(n)) return armM; const am = n.userData.armMask, g = n.geometry;
    if (am && !n.isInstancedMesh && g && g.attributes.position && am.length === g.attributes.position.count) {
      if (!g.attributes.armF) g.setAttribute("armF", new T.Float32BufferAttribute(Float32Array.from(am), 1)); return maskM; }
    return restM; };
  const idMat = {}; function idm(c) { return idMat[c] || (idMat[c] = new T.MeshBasicMaterial({ color: new T.Color(c / 255, 0, 0), side: T.DoubleSide })); }
  const views = { front: 0.15, side: 1.2, back: Math.PI }, res = { id, name: f.name, views: {}, colour: [] }, px = new Uint8Array(W * H * 4);
  const bgN = o.scene.background;
  for (const v in views) {
    o.man.rotation.y = views[v];
    // as the page shows it
    r.toneMapping = T.ACESFilmicToneMapping; r.toneMappingExposure = 1.08; r.outputEncoding = T.sRGBEncoding; r.shadowMap.enabled = true;
    o.scene.background = new T.Color("#e6dfd0"); kinds.forEach(n => { n.material = orig.get(n); });
    r.render(o.scene, cam); const shot = r.domElement.toDataURL("image/png"); gl.readPixels(0, 0, W, H, gl.RGBA, gl.UNSIGNED_BYTE, px); const lit = px.slice();
    // the ID pass
    r.toneMapping = T.NoToneMapping; r.outputEncoding = T.LinearEncoding; r.shadowMap.enabled = false; o.scene.background = new T.Color(0, 0, 0);
    kinds.forEach(n => { n.material = idm(cls(n)); });
    r.render(o.scene, cam); gl.readPixels(0, 0, W, H, gl.RGBA, gl.UNSIGNED_BYTE, px);
    const C = new Uint8Array(W * H); for (let i = 0; i < W * H; i++) C[i] = Math.round(px[i * 4] / 10) * 10;
    // the arm pass: 255 arm, 128 the rest, 0 background
    kinds.forEach(n => { n.material = cls(n) === 0 ? idm(0) : armMat(n); });
    r.render(o.scene, cam); gl.readPixels(0, 0, W, H, gl.RGBA, gl.UNSIGNED_BYTE, px);
    const A = new Uint8Array(W * H); for (let i = 0; i < W * H; i++) A[i] = px[i * 4] > 190 ? 2 : (px[i * 4] > 60 ? 1 : 0);
    const at = (x, y) => (x < 0 || y < 0 || x >= W || y >= H) ? 0 : C[y * W + x], D = 4, dirs = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]];
    let poke = 0, holes = 0, stray = 0; const marks = [];
    /* poke: a pixel of an inner layer (or his skin) with a piece worn over it on all four sides, above and below in
       its column and left and right in its row (so a collar above a jumper, a hem below it or an open front are not
       counted, but a layer showing through the middle of the back is) */
    /* (counted from behind, where every piece is closed, and from the front where the piece over it is done up; not from
       the side, where his arm in front of his body would look the same) */
    const isOuter = (c, q) => q >= 40 && q !== 50 && q !== 140 && (c === 20 ? v === "back" : c === 40 ? q >= 60 : q > c) && (v === "back" || (v === "front" && !openC[q]));
    const R = 70;
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
      const c = C[y * W + x];
      if (v !== "side" && (c === 20 || c === 40 || (c >= 60 && c !== 140))) {
        let sides = 0;
        for (const d of [[1, 0], [-1, 0], [0, 1], [0, -1]]) { for (let t = 2; t <= R; t++) { const q = at(x + d[0] * t, y + d[1] * t); if (q === 0) break; if (isOuter(c, q)) { sides++; break; } } }
        if (sides === 4 && !(c === 20 && y < H * 0.12)) { poke++; marks.push(x, y); }
      }
      if (c >= 40 && c !== 140 && c !== 50) { let bg = 0; for (const d of dirs) if (at(x + d[0] * D, y + d[1] * D) === 0) bg++; if (bg >= 7) stray++; }   // a bit of a piece standing alone
    }
    /* holes: background the outside cannot reach, in small compact patches ringed by clothes (not by his hands or skin) */
    const seen = new Uint8Array(W * H), st = [];
    for (let x = 0; x < W; x++) { st.push(x, 0, x, H - 1); } for (let y = 0; y < H; y++) { st.push(0, y, W - 1, y); }
    while (st.length) { const y = st.pop(), x = st.pop(), k = y * W + x; if (seen[k] || C[k]) continue; seen[k] = 1;
      if (x > 0) st.push(x - 1, y); if (x < W - 1) st.push(x + 1, y); if (y > 0) st.push(x, y - 1); if (y < H - 1) st.push(x, y + 1); }
    for (let k0 = 0; k0 < W * H; k0++) { if (seen[k0] || C[k0]) continue;
      const comp = [], q = [k0]; seen[k0] = 1; let x0 = W, x1 = 0, y0 = H, y1 = 0, nearSkin = false, byArm = false, byRest = false;
      while (q.length) { const k = q.pop(), x = k % W, y = (k - x) / W; comp.push(k); x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y);
        for (const d of [[1, 0], [-1, 0], [0, 1], [0, -1]]) { const xx = x + d[0], yy = y + d[1]; if (xx < 0 || yy < 0 || xx >= W || yy >= H) continue; const kk = yy * W + xx;
          if (C[kk] === 20) nearSkin = true; if (C[kk]) { if (A[kk] === 2) byArm = true; else if (A[kk] === 1) byRest = true; }
          if (!seen[kk] && !C[kk]) { seen[kk] = 1; q.push(kk); } } }
      if (byArm && byRest) continue;   // between an arm and his body: background seen past his side
      if (!nearSkin && comp.length <= 80 && x1 - x0 <= 14 && y1 - y0 <= 14) { holes += comp.length; comp.forEach(k => marks.push(k % W, (k - k % W) / W)); }
    }
    res.views[v] = { poke, holes, stray, shot: (poke > 30 || holes > 25 || stray > 40) ? shot : "" };
    if (dbg) {   // the ID pass as greys, with what was counted marked in red
      const cv = document.createElement("canvas"); cv.width = W; cv.height = H; const cx = cv.getContext("2d"), im = cx.createImageData(W, H);
      for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) { const k = ((H - 1 - y) * W + x) * 4, c = C[y * W + x]; im.data[k] = im.data[k + 1] = im.data[k + 2] = c; im.data[k + 3] = 255; }
      for (let i = 0; i < marks.length; i += 2) { const k = ((H - 1 - marks[i + 1]) * W + marks[i]) * 4; im.data[k] = 255; im.data[k + 1] = 0; im.data[k + 2] = 0; }
      cx.putImageData(im, 0, 0); res.views[v].dbg = cv.toDataURL("image/png");
    }
    // colour of each plain piece, front view only, from the inside of its area (3x3 all the same class)
    if (v === "front") {
      const pieces = ps.map((p, i) => p).filter(p => p.item); const sums = {};
      for (let y = 1; y < H - 1; y++) for (let x = 1; x < W - 1; x++) { const c = C[y * W + x]; if (c < 40 || c === 140 || c === 50) continue;
        let same = true; for (let dy = -1; dy <= 1 && same; dy++) for (let dx = -1; dx <= 1; dx++) if (C[(y + dy) * W + x + dx] !== c) { same = false; break; }
        if (!same) continue; const s = sums[c] || (sums[c] = [0, 0, 0, 0]); const k = (y * W + x) * 4; s[0] += lit[k]; s[1] += lit[k + 1]; s[2] += lit[k + 2]; s[3]++; }
      res.sums = sums;
    }
  }
  // which class each piece drew in, with its colour and whether it is plain (only plain pieces are colour-checked)
  const ups = []; o.scene.traverse(n => { if (n.isMesh && n.userData.item && /^up\d+$/.test(n.userData.kind || "") && ups.indexOf(n.userData.kind + "|" + n.userData.item) < 0) ups.push(n.userData.kind + "|" + n.userData.item); });
  ps.forEach(p => { const L = X.LOOK[p.item], hx = X.TRUE[p.item], col = hx ? hx.split("|")[0] : X.cc(p.col)[0];
    let c = null; if (/^(trousers|shorts)$/.test(p.shape)) c = 40; else { const u = ups.find(s => s.endsWith("|" + p.item)); if (u) c = 60 + 10 * +u.split("|")[0].slice(2); }
    if (c == null || !res.sums || !res.sums[c] || res.sums[c][3] < 150) return;
    const s = res.sums[c]; res.colour.push({ item: p.item, shape: p.shape, want: col, got: [s[0] / s[3], s[1] / s[3], s[2] / s[3]].map(Math.round), plain: !L || L.pat === "plain", px: s[3] });
  });
  delete res.sums;
  o.scene.traverse(n => { if (n.isMesh) { n.geometry && n.geometry.dispose(); } });
  o.scene.background = bgN;
  return res;
}

function hsl(c) { const r = c[0] / 255, g = c[1] / 255, b = c[2] / 255, mx = Math.max(r, g, b), mn = Math.min(r, g, b), l = (mx + mn) / 2, d = mx - mn, s = d ? d / (1 - Math.abs(2 * l - 1)) : 0; let h = 0;
  if (d) { h = mx === r ? ((g - b) / d) % 6 : mx === g ? (b - r) / d + 2 : (r - g) / d + 4; h *= 60; if (h < 0) h += 360; } return [h, s, l, d]; }
function rgb(hex) { return [1, 3, 5].map(i => parseInt(hex.substr(i, 2), 16)); }
/* a plain piece's colour is off when a clearly coloured piece comes out another hue, or a piece comes out far lighter or darker
   than it is (the studio light and shade make every piece read a little darker, so the band is generous) */
function colourOff(c) {
  if (!c.plain || !/^#[0-9a-f]{6}$/i.test(c.want)) return "";
  const w = hsl(rgb(c.want)), g = hsl(c.got); let dh = Math.abs(w[0] - g[0]); dh = Math.min(dh, 360 - dh);
  /* (colourfulness is judged on chroma, the spread between the strongest and weakest channel: by HSL saturation
     alone an off-white reads as strongly coloured) */
  if (w[3] > 0.12 && w[2] > 0.15 && w[2] < 0.85 && g[3] > 0.05 && dh > 35) return "hue " + Math.round(dh) + "°";
  if (w[3] > 0.18 && g[3] < 0.04 && w[2] > 0.2) return "lost its colour";
  const lw = w[2], lg = g[2];
  /* (very dark cloth always reads a little lighter on the lit model: the sky light and sheen lift it) */
  const up = lw < 0.25 ? 1.9 : 1.45;
  if (lw > 0.12 && (lg < lw * 0.42 || lg > lw * up + 0.05)) return "lightness " + lw.toFixed(2) + " → " + lg.toFixed(2);
  if (lw <= 0.12 && lg > 0.4) return "much too light";
  return "";
}

(async () => {
  if (!fs.existsSync(path.join(SITE, "index.html"))) { console.error("No site at " + SITE + " (build it with tools/build_site.py)"); process.exit(1); }
  fs.mkdirSync(OUT, { recursive: true });
  const srv = await serve(SITE), port = srv.address().port;
  const b = await chromium.launch({ executablePath: process.env.CHROME_PATH || (fs.existsSync("/opt/pw-browsers/chromium-1194/chrome-linux/chrome") ? "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" : undefined),
    args: ["--use-gl=swiftshader", "--enable-unsafe-swiftshader"] });
  const p = await b.newPage(), errs = []; p.on("pageerror", e => errs.push(e.message));
  await p.goto("http://localhost:" + port + "/index.html?qa=1#fits");
  await p.waitForFunction(() => window.__qa && Object.keys(window.__qa().fitById).length > 0, null, { timeout: 120000 });
  await p.evaluate(() => window.__qa().loadThree());
  await p.waitForFunction(() => !!window.__qa().body(), null, { timeout: 120000 });
  let ids = await p.evaluate(() => Object.keys(window.__qa().fitById));
  if (arg("ids")) ids = String(arg("ids")).split(",");
  else if (arg("sample")) { const n = +arg("sample"), st = Math.max(1, Math.floor(ids.length / n)); ids = ids.filter((_, i) => i % st === 0).slice(0, n); }
  const out = [], t0 = Date.now();
  for (let i = 0; i < ids.length; i++) {
    let r;
    try { r = await p.evaluate(checkOutfit, { id: ids[i], dbg: !!arg("debug") }); } catch (e) { r = { id: ids[i], error: String(e.message || e).slice(0, 200) }; }
    if (r.views) {
      r.flags = [];
      for (const v in r.views) { const m = r.views[v];
        for (const k of ["poke", "holes", "stray"]) if (m[k] > LIMITS[k]) r.flags.push(v + " " + k + " " + m[k]);
        if (m.dbg) { fs.writeFileSync(path.join(OUT, r.id + "-" + v + "-id.png"), Buffer.from(m.dbg.split(",")[1], "base64")); delete m.dbg; }
        if (m.shot) { fs.writeFileSync(path.join(OUT, r.id + "-" + v + ".png"), Buffer.from(m.shot.split(",")[1], "base64")); m.shot = r.id + "-" + v + ".png"; } else delete m.shot; }
      r.colour.forEach(c => { const why = colourOff(c); if (why) { c.off = why; r.flags.push("colour " + c.item + ": " + why); } });
    }
    out.push(r);
    if ((i + 1) % 10 === 0 || i === ids.length - 1) process.stdout.write("\r" + (i + 1) + "/" + ids.length + " outfits, " + Math.round((Date.now() - t0) / 1000) + "s");
  }
  process.stdout.write("\n");
  const flagged = out.filter(r => r.error || (r.flags && r.flags.length));
  const count = k => out.filter(r => r.flags && r.flags.some(f => f.includes(k))).length;
  const summary = { date: new Date().toISOString().slice(0, 10), outfits: out.length, flagged: flagged.length,
    poke: count("poke"), holes: count("holes"), stray: count("stray"), colour: count("colour"), errors: out.filter(r => r.error).length, page_errors: errs.slice(0, 5) };
  fs.writeFileSync(path.join(OUT, "report.json"), JSON.stringify({ summary, outfits: out }, null, 1));
  console.log(JSON.stringify(summary));
  flagged.slice(0, 40).forEach(r => console.log(" ", r.id, "-", r.error || r.flags.join("; ")));
  if (arg("report")) {
    const rp = path.join(ROOT, "data", "refresh-report.json"), rep = fs.existsSync(rp) ? JSON.parse(fs.readFileSync(rp, "utf8")) : {};
    rep.checks_3d = { summary, flagged: flagged.map(r => ({ id: r.id, flags: r.error ? ["error: " + r.error] : r.flags })) };
    fs.writeFileSync(rp, JSON.stringify(rep, null, 1));
  }
  await b.close(); srv.close();
})();
