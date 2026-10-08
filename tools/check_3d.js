#!/usr/bin/env node
/* The automatic 3D checks: renders every outfit on Dave's 3D model from the front, the side and the back, and
   counts what should never be seen.
     - poke: an inner layer (or his skin) showing through a piece worn over it, as islands inside the outer piece;
     - holes: background showing through the clothes;
     - stray: small bits of a piece standing off on their own;
     - skin: his skin seen where the outfit covers him (his torso under a top, his arms under long sleeves, his legs
       under trousers): a gap at a hem, a cuff or a waistband, or a hole in the cloth;
     - seethrough: places where the background shows but his (hidden) body would: a hole in the cloth, or cloth that
       has sunk inside him there;
     - colour: a plain piece whose rendered colour is far from its shop colour (hue, or much too light or dark);
     - under: a scarf or snood with a top's collar over it at the back or sides of his neck (rays round his neck meet the
       top first and the scarf just behind it);
     - legs: trousers whose legs are joined down the thighs (a ray between his legs, front or back, from a hand to a
       palm's width below the crotch meets the trousers instead of passing between them);
     - form: a flat cap drawn as a baseball cap: its peak reaching well past the front of its crown, instead of the
       crown being carried forward over the peak.
     - slit: a thin line of an inner layer between two parts of a closed piece worn over it (a seam opened);
     - offset: an inner layer drawn over the piece worn over it because of a depth offset (a photo front or print laid
       on the cloth), found by drawing the view with and without the offsets.
   Poke is also counted from the three-quarter views (cloth through cloth only); slit and offset on all five, where a
   fault of this kind shows as the model turns.
   Each view is drawn as the page shows it and in flat colours (one per piece, an "ID" pass), which is what the
   counts are made on; skin and see-through are also checked from both three-quarter views.

     node tools/check_3d.js [--site docs] [--ids a,b] [--sample N] [--out qa] [--report]

   --site     the built site to serve (default docs/, built by tools/build_site.py)
   --ids      only these outfits (a,b or @file, one per line); --sample N: every outfit's N-th share (a spread of N outfits); --shard k/n: every
              n-th outfit from the k-th, to run n checks at once (each with its own --out)
   --fail     exit with an error when anything is flagged or the page throws (for the pull-request check)
   --out      where the report and the pictures of flagged outfits go (default qa/)
   --report   also write the summary into data/refresh-report.json ("checks_3d")
   --body     check on another of Edit Dave's body types (slim, average, athletic, heavier) or cloth fits (close, loose)
   Needs Playwright and Chromium (CHROME_PATH to use a particular Chromium). */
const fs = require("fs"), path = require("path"), http = require("http");
let chromium;
try { ({ chromium } = require("playwright")); } catch (e) {
  try { ({ chromium } = require("/opt/node22/lib/node_modules/playwright")); } catch (e2) { console.error("Playwright is needed: npm i playwright"); process.exit(1); }
}
const ROOT = path.join(__dirname, "..");
const arg = (k, d) => { const i = process.argv.indexOf("--" + k); return i < 0 ? d : (process.argv[i + 1] && !process.argv[i + 1].startsWith("--") ? process.argv[i + 1] : true); };
const SITE = path.resolve(ROOT, arg("site", "docs")), OUT = path.resolve(ROOT, arg("out", "qa"));
const LIMITS = { poke: 30, slit: 20, offset: 8, holes: 25, stray: 40, skin: 12, seethrough: 12, sunk: 60, under: 2, legs: 2, form: 0 };

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
  const id = arg.id, dbg = arg.dbg, LIMITS = arg.lim;
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
  /* (each mesh's class is fixed before any pass swaps its material: the floor is known by its shadow material) */
  const CLS = new Map(); kinds.forEach(n => CLS.set(n, cls(n))); const clsOf = n => CLS.get(n);
  const openC = {}; kinds.forEach(n => { if (n.userData.open) openC[clsOf(n)] = 1; });   // pieces worn open (their front shows what is under them)
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
  /* what the outfit covers (for the skin count): a top always covers his torso below the collarbones (he is never
     shirtless); long sleeves cover his arms down to the wrist, short sleeves the top of his arm; trousers cover his legs
     down to the ankle, shorts to just above the knee */
  const B = X.body(), RG = B.regions, footR = RG.indexOf("foot"), crotch = B.lm.crotch, wrist = B.lm.wrist[1];
  const dp = X.dressed(ps), nmOf = q => (((X.byId[q.item] || {}).name || "") + " " + (q.what || "")).toLowerCase();
  const tops = dp.filter(q => /^(coat|jacket|blazer|gilet|gown|waistcoat|cardigan|hoodie|jumper|rollneck|halfzip|shirt|sshirt|polo|tee|vest)$/.test(q.shape));
  const sleeveless = q => /^(vest|waistcoat|gilet)$/.test(q.shape) || /knitted vest|knit vest|sweater vest|slipover|tank ?top|sleeveless/.test(nmOf(q));
  const shortSl = q => /^(tee|polo|sshirt)$/.test(q.shape) && !/long/.test(nmOf(q));
  const longSl = tops.some(q => !sleeveless(q) && !shortSl(q)), shortOnly = !longSl && tops.some(q => !sleeveless(q));
  // (worn on its own, a vest's armholes and scoop show his chest down to the armhole's foot, about 1.19 m on a muscle vest)
  const torsoTop = tops.length && tops.every(sleeveless) ? 1.17 : 1.42;
  const lo = dp.find(q => /^(trousers|shorts)$/.test(q.shape));
  const covered = (reg, y) => { const r = RG[reg];
    if (r === "chest" || r === "belly" || r === "hips") return tops.length > 0 && y < torsoTop;
    if (r === "uarm") return longSl || (shortOnly && y > 1.3);
    if (r === "farm") return longSl && y > wrist + 0.04;
    if (r === "thigh") return !!lo && (lo.shape === "trousers" || y > crotch - 0.25);
    if (r === "shin") return !!lo && lo.shape === "trousers" && y > 0.17;
    return false; };
  /* layering and shape, measured on the model itself with rays rather than on the pictures */
  o.man.rotation.y = 0; o.scene.updateMatrixWorld(true);
  const rc = new T.Raycaster(), geo = { under: 0, legs: 0, form: 0, notes: [] }, hitK = n => n.userData.kind || "body";
  const boxOf = it => { const bx = new T.Box3(); kinds.forEach(n => { if (n.userData.item === it) bx.expandByObject(n); }); return bx.isEmpty() ? null : bx; };
  const hits = () => rc.intersectObjects(kinds, false).filter(x => clsOf(x.object) !== 0);
  /* (a scarf round his neck: from behind and the sides, over its top 9 cm, nothing of a top may lie over it) */
  ps.filter(p => /^(scarf|snood)$/.test(p.shape)).forEach(p => { const bx = boxOf(p.item); if (!bx) return; const cz = (bx.min.z + bx.max.z) / 2;
    for (let y = bx.max.y - 0.09; y < bx.max.y - 0.004; y += 0.01) for (let a = 0; a < 32; a++) { const t = a / 32 * Math.PI * 2, dx = Math.sin(t), dz = Math.cos(t); if (dz > 0.3) continue;
      rc.set(new T.Vector3(dx * 0.6, y, cz + dz * 0.6), new T.Vector3(-dx, 0, -dz)); const h = hits();
      const iT = h.findIndex(x => /^up/.test(hitK(x.object))), iS = h.findIndex(x => x.object.userData.item === p.item);
      if (iT >= 0 && iS > iT && h[iS].distance - h[iT].distance < 0.025) geo.under++; } });
  /* (trousers: between his legs, front and back, below the crotch's own rounding) */
  const loP = ps.find(q => q.shape === "trousers");
  if (loP) for (let y = crotch - 0.3; y <= crotch - 0.12; y += 0.01) for (const dz of [1, -1]) {
    rc.set(new T.Vector3(0, y, dz * 0.8), new T.Vector3(0, 0, -dz)); const h = hits(); if (h.length && hitK(h[0].object) === "lo") geo.legs++; }
  /* (a flat cap's crown is carried forward to a lip over its peak, so from the side the two end together; a baseball
     cap's crown stops at its band, well behind the end of its peak. The crown is the cap's largest mesh, the peak the
     rest: how far the peak reaches past the crown, under 2 cm on a flat cap) */
  ps.filter(p => p.shape === "cap").forEach(p => { const ms = kinds.filter(n => n.userData.item === p.item && n.geometry && n.geometry.attributes.position); if (ms.length < 2) return;
    const crown = ms.reduce((a, n) => n.geometry.attributes.position.count > a.geometry.attributes.position.count ? n : a), cb = new T.Box3().setFromObject(crown), pb = new T.Box3();
    ms.forEach(n => { if (n !== crown) pb.expandByObject(n); }); const past = pb.max.z - cb.max.z;
    geo.capPast = +past.toFixed(3); if (past > 0.02) { geo.form++; geo.notes.push("flat cap's peak reaches " + Math.round(past * 100) + " cm past its crown, as a baseball cap's"); } });
  /* the body drawn by part and height (red: its part, green: its height, blue: 255 marks the body) */
  const bodyN = kinds.find(n => n.userData.isBody);
  let regM = null, fullIdx = null, cutIdx = null;
  if (bodyN) { const g = bodyN.geometry, nv = g.attributes.position.count, P0 = B.cache && B.cache.pos ? B.cache.pos : g.attributes.position.array, rgA = new Float32Array(nv * 3);
    for (let t = 0; t < B.idx.length / 3; t++) for (let j = 0; j < 3; j++) { const v = B.idx[t * 3 + j]; rgA[v * 3] = (B.treg[t] * 20 + 10) / 255; }
    for (let v = 0; v < nv; v++) { rgA[v * 3 + 1] = Math.max(0, Math.min(1, P0[v * 3 + 1] / 1.9)); rgA[v * 3 + 2] = 1; }
    g.setAttribute("regC", new T.Float32BufferAttribute(rgA, 3));
    regM = new T.ShaderMaterial({ side: T.DoubleSide, vertexShader: "attribute vec3 regC; varying vec3 vR; void main(){ vR = regC; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }",
      fragmentShader: "varying vec3 vR; void main(){ gl_FragColor = vec4(vR, 1.0); }" });
    cutIdx = g.index; fullIdx = new T.BufferAttribute(B.idx, 1); }
  /* the ID pass as greys, with what was counted marked in red */
  /* the ID image with the faults in red (sunk cloth at the outline in yellow) */
  function dbgImg(C, marks, soft) { const cv = document.createElement("canvas"); cv.width = W; cv.height = H; const cx = cv.getContext("2d"), im = cx.createImageData(W, H);
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) { const k = ((H - 1 - y) * W + x) * 4, c = C[y * W + x]; im.data[k] = im.data[k + 1] = im.data[k + 2] = c; im.data[k + 3] = 255; }
    const paint = (L, g) => { for (let i = 0; i < L.length; i += 2) { const k = ((H - 1 - L[i + 1]) * W + L[i]) * 4; im.data[k] = 255; im.data[k + 1] = g; im.data[k + 2] = 0; } };
    paint(soft || [], 200); paint(marks, 0);
    cx.putImageData(im, 0, 0); return cv.toDataURL("image/png"); }
  const idMat = {}; function idm(c) { return idMat[c] || (idMat[c] = new T.MeshBasicMaterial({ color: new T.Color(c / 255, 0, 0), side: T.DoubleSide })); }
  /* (in the ID pass each mesh keeps its own depth settings, so whatever wins in the page's picture wins here too: a
     shirt's photo front drawn with a depth offset once came through a jacket at a glancing angle on the page, while
     the ID pass, with no offset, showed the jacket) */
  const idOf = n => { const m0 = [].concat(orig.get(n))[0], c = clsOf(n); if (!m0 || !(m0.polygonOffset || m0.depthWrite === false)) return idm(c);
    const k = [c, m0.polygonOffset ? 1 : 0, m0.polygonOffsetFactor || 0, m0.polygonOffsetUnits || 0, m0.depthWrite === false ? 0 : 1, m0.transparent ? 1 : 0].join("|");
    return idMat[k] || (idMat[k] = new T.MeshBasicMaterial({ color: new T.Color(c / 255, 0, 0), side: T.DoubleSide, polygonOffset: !!m0.polygonOffset,
      polygonOffsetFactor: m0.polygonOffsetFactor || 0, polygonOffsetUnits: m0.polygonOffsetUnits || 0, depthWrite: m0.depthWrite !== false, transparent: !!m0.transparent })); };
  const views = { front: 0.15, fq: 0.8, side: 1.2, bq: 2.4, back: Math.PI }, quarter = { fq: 1, bq: 1 }, res = { id, name: f.name, views: {}, colour: [], geo }, px = new Uint8Array(W * H * 4);
  const bgN = o.scene.background;
  /* slit: a thin line (1 to 3 pixels) of an inner layer between two parts of one piece worn over it, across or down,
     as a seam that has opened (between a sleeve and the body, along a zip): flickers as the model turns. Read from the
     ID pass C of the view being counted. */
  let C = null;
  const slits = (v, marks) => { let n = 0; const id = (x, y) => (x < 0 || y < 0 || x >= W || y >= H) ? 0 : C[y * W + x];
    for (let y = 1; y < H - 1; y++) for (let x = 1; x < W - 1; x++) { const c = C[y * W + x]; if (!(c === 40 || (c >= 60 && c !== 140))) continue;
      let hit = false;
      for (const d of [[1, 0], [0, 1]]) { let a = 0, b = 0;
        for (let t = 1; t <= 3 && !a; t++) { const q = id(x - d[0] * t, y - d[1] * t); if (q !== c) { a = q; } }
        for (let t = 1; t <= 3 && !b; t++) { const q = id(x + d[0] * t, y + d[1] * t); if (q !== c) { b = q; } }
        if (a && a === b && a > c && a !== 140 && a !== 50 && !openC[a]) { hit = true; break; } }   // (not the strip of what is under an open front, seen edge-on)
      if (hit) { n++; marks.push(x, y); } }
    return n; };
  for (const v in views) {
    o.man.rotation.y = views[v];
    // as the page shows it
    r.toneMapping = T.ACESFilmicToneMapping; r.toneMappingExposure = 1.08; r.outputEncoding = T.sRGBEncoding; r.shadowMap.enabled = true;
    o.scene.background = new T.Color("#e6dfd0"); kinds.forEach(n => { n.material = orig.get(n); });
    r.render(o.scene, cam); const shot = r.domElement.toDataURL("image/png"); gl.readPixels(0, 0, W, H, gl.RGBA, gl.UNSIGNED_BYTE, px); const lit = px.slice(), marks = [], soft = [];
    let skin = 0, see = 0, sunk = 0; const where = {};   // (which part of him each fault is over, for the report)
    // the ID pass
    r.toneMapping = T.NoToneMapping; r.outputEncoding = T.LinearEncoding; r.shadowMap.enabled = false; o.scene.background = new T.Color(0, 0, 0);
    kinds.forEach(n => { n.material = idm(clsOf(n)); });
    r.render(o.scene, cam); gl.readPixels(0, 0, W, H, gl.RGBA, gl.UNSIGNED_BYTE, px);
    const C0 = new Uint8Array(W * H); for (let i = 0; i < W * H; i++) C0[i] = Math.round(px[i * 4] / 10) * 10;
    kinds.forEach(n => { n.material = idOf(n); });
    r.render(o.scene, cam); gl.readPixels(0, 0, W, H, gl.RGBA, gl.UNSIGNED_BYTE, px);
    C = new Uint8Array(W * H); for (let i = 0; i < W * H; i++) C[i] = Math.round(px[i * 4] / 10) * 10;
    /* offset: where a piece's depth offset (a photo front, a print laid on the cloth) lets an inner layer cover the piece
       worn over it, compared with the same view drawn without the offsets */
    let offset = 0; for (let i = 0; i < W * H; i++) if (C[i] !== C0[i] && C[i] >= 20 && C0[i] > C[i] && C0[i] !== 140) { offset++; marks.push(i % W, (i - i % W) / W); }
    if (bodyN) {
      /* skin: each visible skin pixel's body part and height, against what the outfit covers */
      kinds.forEach(n => { n.material = n === bodyN ? regM : idm(clsOf(n) === 0 ? 0 : 1); });
      r.render(o.scene, cam); gl.readPixels(0, 0, W, H, gl.RGBA, gl.UNSIGNED_BYTE, px);
      for (let i = 0; i < W * H; i++) { if (px[i * 4 + 2] < 200) continue; const reg = Math.round((px[i * 4] - 10) / 20), y = px[i * 4 + 1] / 255 * 1.9;
        if (covered(reg, y)) { skin++; marks.push(i % W, (i - i % W) / W); where["skin " + RG[reg]] = (where["skin " + RG[reg]] || 0) + 1; } }
      /* see-through: drawn again with the whole of his body; background that turns into body is a hole or sunken cloth */
      /* (his feet are left out: a shoe is a shell over the foot, and the hidden foot reaching past its outline is never seen) */
      bodyN.geometry.setIndex(fullIdx); kinds.forEach(n => { n.material = n === bodyN ? regM : idm(clsOf(n)); });
      r.render(o.scene, cam); gl.readPixels(0, 0, W, H, gl.RGBA, gl.UNSIGNED_BYTE, px); bodyN.geometry.setIndex(cutIdx);
      const S = new Uint8Array(W * H); for (let i = 0; i < W * H; i++) if (C[i] === 0 && px[i * 4 + 2] > 200 && Math.round((px[i * 4] - 10) / 20) !== footR) S[i] = 1;
      /* only background shut in by the outfit counts (a hole); his hidden body poking past the outline (a foot past a
         shoe, a shoulder past a tight top) cannot be seen, and is only noted as "sunk" */
      const outside = new Uint8Array(W * H), st0 = [];
      for (let x = 0; x < W; x++) st0.push(x, 0, x, H - 1); for (let y = 0; y < H; y++) st0.push(0, y, W - 1, y);
      while (st0.length) { const y = st0.pop(), x = st0.pop(), k = y * W + x; if (outside[k] || C[k]) continue; outside[k] = 1;
        if (x > 0) st0.push(x - 1, y); if (x < W - 1) st0.push(x + 1, y); if (y > 0) st0.push(x, y - 1); if (y < H - 1) st0.push(x, y + 1); }
      /* (single stray pixels are rounding, not holes: only patches of 3 or more count) */
      for (let i = 0; i < W * H; i++) { if (!S[i]) continue; const x = i % W, y = (i - x) / W; let nb = 0;
        for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) { if (!dx && !dy) continue; const xx = x + dx, yy = y + dy; if (xx >= 0 && yy >= 0 && xx < W && yy < H && S[yy * W + xx]) nb++; }
        if (nb < 2) continue; const wk = (outside[i] ? "sunk " : "seethrough ") + RG[Math.round((px[i * 4] - 10) / 20)]; where[wk] = (where[wk] || 0) + 1;
        if (outside[i]) { sunk++; soft.push(x, y); } else { see++; marks.push(x, y); } }
    }
    if (quarter[v]) {   // the three-quarter views count skin, see-through, and cloth showing through cloth
      const at4 = (x, y) => (x < 0 || y < 0 || x >= W || y >= H) ? 0 : C[y * W + x], fr = v === "fq";
      /* (as from the front for the front three-quarter, pieces worn open left out; as from behind for the back one; his
         skin is not counted, as a hand in front of him at this angle looks the same) */
      const outer4 = (c, q) => q >= 40 && q !== 50 && q !== 140 && (c === 40 ? q >= 60 : q > c) && !(fr && openC[q]);
      let poke = 0; const slit = slits(v, marks);
      for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) { const c = C[y * W + x]; if (!(c === 40 || (c >= 60 && c !== 140))) continue; let sides = 0;
        for (const d of [[1, 0], [-1, 0], [0, 1], [0, -1]]) { for (let t = 2; t <= 70; t++) { const q = at4(x + d[0] * t, y + d[1] * t); if (q === 0) break; if (outer4(c, q)) { sides++; break; } } }
        if (sides === 4) { poke++; marks.push(x, y); } }
      res.views[v] = { poke, slit, offset, skin, seethrough: see, sunk, where, shot: (poke > LIMITS.poke || slit > LIMITS.slit || offset > LIMITS.offset || skin > LIMITS.skin || see > LIMITS.seethrough || sunk > LIMITS.sunk) ? shot : "" };
      if (dbg) res.views[v].dbg = dbgImg(C, marks, soft);
      continue; }
    // the arm pass: 255 arm, 128 the rest, 0 background
    kinds.forEach(n => { n.material = clsOf(n) === 0 ? idm(0) : armMat(n); });
    r.render(o.scene, cam); gl.readPixels(0, 0, W, H, gl.RGBA, gl.UNSIGNED_BYTE, px);
    const A = new Uint8Array(W * H); for (let i = 0; i < W * H; i++) A[i] = px[i * 4] > 190 ? 2 : (px[i * 4] > 60 ? 1 : 0);
    const at = (x, y) => (x < 0 || y < 0 || x >= W || y >= H) ? 0 : C[y * W + x], D = 4, dirs = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]];
    let poke = 0, holes = 0, stray = 0; const slit = slits(v, marks);
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
    res.views[v] = { poke, slit, offset, holes, stray, skin, seethrough: see, sunk, where, shot: (poke > LIMITS.poke || slit > LIMITS.slit || offset > LIMITS.offset || holes > LIMITS.holes || stray > LIMITS.stray || skin > LIMITS.skin || see > LIMITS.seethrough || sunk > LIMITS.sunk) ? shot : "" };
    if (dbg) res.views[v].dbg = dbgImg(C, marks, soft);
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
  // (the colour aimed for is the one the page draws: the photo reading, or the item's correction in data/fixes.json)
  ps.forEach(p0 => { const p = X.pieceLook ? X.pieceLook(p0) : p0, L = p.look || X.LOOK[p.item], hx = X.TRUE[p.item];
    const col = p.look && p.look.fix ? p.col : (hx ? hx.split("|")[0] : X.cc(p.col)[0]);
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
  // --body: check on another of Edit Dave's body types (or cloth fit) instead of his saved one, set as the page would
  // set it; the types are read from the page itself, so they never fall out of step with it
  const BODY = arg("body");
  if (BODY && BODY !== "dave") {
    let ch; try { ch = require("./qa/body").charFor(fs.readFileSync(path.join(SITE, "index.html"), "utf8"), BODY); } catch (e) { console.error("--body: " + e.message); process.exit(1); }
    await p.addInitScript(c => { try { localStorage.setItem("dw-char", JSON.stringify(c)); } catch (e) {} }, ch);
  }
  await p.goto("http://localhost:" + port + "/index.html?qa=1#fits");
  await p.waitForFunction(() => window.__qa && Object.keys(window.__qa().fitById).length > 0, null, { timeout: 120000 });
  await p.evaluate(() => window.__qa().loadThree());
  await p.waitForFunction(() => !!window.__qa().body(), null, { timeout: 120000 });
  let ids = await p.evaluate(() => Object.keys(window.__qa().fitById));
  if (arg("ids")) { const v = String(arg("ids"));   // a list, or @file with one id per line or comma (blank lines and # notes left out)
    ids = (v.startsWith("@") ? fs.readFileSync(path.resolve(ROOT, v.slice(1)), "utf8").replace(/#.*/g, "") : v).split(/[\s,]+/).filter(Boolean);
    const all = new Set(await p.evaluate(() => Object.keys(window.__qa().fitById))), gone = ids.filter(k => !all.has(k));
    if (gone.length) console.log("not outfits (left out): " + gone.join(", "));
    ids = [...new Set(ids.filter(k => all.has(k)))]; }
  else if (arg("sample")) { const n = +arg("sample"), st = Math.max(1, Math.floor(ids.length / n)); ids = ids.filter((_, i) => i % st === 0).slice(0, n); }
  if (arg("shard")) { const sh = String(arg("shard")).split("/").map(Number); ids = ids.filter((_, i) => i % sh[1] === sh[0]); }   // --shard k/n: every n-th outfit from the k-th (run n at once)
  if (!ids.length) { console.log("No outfits to check."); await b.close(); srv.close(); return; }
  const out = [], t0 = Date.now();
  for (let i = 0; i < ids.length; i++) {
    let r;
    try { r = await p.evaluate(checkOutfit, { id: ids[i], dbg: !!arg("debug"), lim: LIMITS }); } catch (e) { r = { id: ids[i], error: String(e.message || e).slice(0, 200) }; }
    if (r.views) {
      r.flags = [];
      for (const v in r.views) { const m = r.views[v];
        for (const k of ["poke", "slit", "offset", "holes", "stray", "skin", "seethrough", "sunk"]) if (m[k] > LIMITS[k]) {
          // (for skin and see-through, the part of him it is over: "front skin 40 (belly 30, hips 10)")
          const on = Object.entries(m.where || {}).filter(e => e[0].startsWith(k + " ")).sort((a, b) => b[1] - a[1]).map(e => e[0].slice(k.length + 1) + " " + e[1]).join(", ");
          r.flags.push(v + " " + k + " " + m[k] + (on ? " (" + on + ")" : "")); }
        if (m.dbg) { fs.writeFileSync(path.join(OUT, r.id + "-" + v + "-id.png"), Buffer.from(m.dbg.split(",")[1], "base64")); delete m.dbg; }
        if (m.shot) { fs.writeFileSync(path.join(OUT, r.id + "-" + v + ".png"), Buffer.from(m.shot.split(",")[1], "base64")); m.shot = r.id + "-" + v + ".png"; } else delete m.shot; }
      r.colour.forEach(c => { const why = colourOff(c); if (why) { c.off = why; r.flags.push("colour " + c.item + ": " + why); } });
      const g = r.geo || {};
      if (g.under > LIMITS.under) r.flags.push("under " + g.under + " (a top's collar over the scarf at the back of his neck)");
      if (g.legs > LIMITS.legs) r.flags.push("legs " + g.legs + " (the trouser legs joined down the thighs)");
      if (g.form > LIMITS.form) r.flags.push("form " + g.notes.join("; "));
    }
    out.push(r);
    if ((i + 1) % 10 === 0 || i === ids.length - 1) process.stdout.write("\r" + (i + 1) + "/" + ids.length + " outfits, " + Math.round((Date.now() - t0) / 1000) + "s");
  }
  process.stdout.write("\n");
  const flagged = out.filter(r => r.error || (r.flags && r.flags.length));
  const count = k => out.filter(r => r.flags && r.flags.some(f => f.includes(k))).length;
  const summary = { date: new Date().toISOString().slice(0, 10), body: BODY || "dave", outfits: out.length, flagged: flagged.length,
    poke: count("poke"), slit: count("slit"), offset: count("offset"), holes: count("holes"), stray: count("stray"), skin: count("skin"), seethrough: count("seethrough"), sunk: count("sunk"), colour: count("colour"), under: count("under "), legs: count("legs "), form: count("form "), errors: out.filter(r => r.error).length, page_errors: errs.slice(0, 5) };
  fs.writeFileSync(path.join(OUT, "report.json"), JSON.stringify({ summary, outfits: out }, null, 1));
  console.log(JSON.stringify(summary));
  flagged.slice(0, 40).forEach(r => console.log(" ", r.id, "-", r.error || r.flags.join("; ")));
  if (arg("report")) {
    const rp = path.join(ROOT, "data", "refresh-report.json"), rep = fs.existsSync(rp) ? JSON.parse(fs.readFileSync(rp, "utf8")) : {};
    rep.checks_3d = { summary, flagged: flagged.map(r => ({ id: r.id, flags: r.error ? ["error: " + r.error] : r.flags })) };
    fs.writeFileSync(rp, JSON.stringify(rep, null, 1));
  }
  await b.close(); srv.close();
  if (errs.length) console.log("page errors: " + errs.slice(0, 5).join(" | "));
  if (arg("fail") && (flagged.length || errs.length)) process.exitCode = 1;
})();
