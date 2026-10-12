// Drape proof of concept: each layer is a cloth (particles + distance constraints sized from a pattern), settled under
// gravity in wearing order against the body and the layers under it. Body: data/body.json from the Wardrobe repo.
const stage = document.querySelector('three-d-stage');
const { THREE } = await stage.ready;
const URLS = ['https://raw.githubusercontent.com/emmachilds98-wq/Wardrobe/main/data/body.json',
  'https://emmachilds98-wq.github.io/Wardrobe/docs/data/body.json'];
const TAU = Math.PI * 2, RG = { head: 0, neck: 1, chest: 2, belly: 3, hips: 4, uarm: 5, farm: 6, hand: 7, thigh: 8, shin: 9, foot: 10 };
const KEYS = ['weight', 'muscle', 'shoulderW', 'chest', 'waistW', 'belly', 'hips', 'arms', 'legs', 'neckW', 'bicep', 'forearm', 'thigh', 'calf'];
// page.html: CHAR_DEF (his saved shape) and PRESETS
const PRESETS = {
  dave: { weight: -0.649, muscle: -0.25, shoulderW: -0.15, chest: -0.428, waistW: -0.1, belly: 0.25, hips: -0.167, arms: -0.3, legs: 0.675, neckW: -0.15 },
  slim: { weight: -0.6, muscle: -0.15, chest: -0.2, belly: -0.4, arms: -0.3, legs: -0.25 },
  athletic: { weight: -0.1, muscle: 0.65, shoulderW: 0.4, chest: 0.35, waistW: -0.15, belly: -0.45, arms: 0.35, legs: 0.25, neckW: 0.3, bicep: 0.4, forearm: 0.3, calf: 0.25 },
  heavier: { weight: 0.6, belly: 0.55, waistW: 0.45, chest: 0.2, hips: 0.25, arms: 0.25, legs: 0.2, neckW: 0.3, thigh: 0.3, forearm: 0.2 },
};
// garment measurements in cm (illustrative size chart: chest all round, length from the shoulder, biceps all round)
const SIZES = { M: { hc: 112, hl: 70, hb: 38, jc: 118, jl: 68, jb: 42 }, L: { hc: 120, hl: 72, hb: 40, jc: 126, jl: 70, jb: 44 }, XL: { hc: 128, hl: 74, hb: 42, jc: 134, jl: 72, jb: 46 } };
const S = { body: 'dave', size: 'L', hood: 'out' };
let B = null, token = 0;
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const frame = () => new Promise(r => requestAnimationFrame(r));
const $ = s => document.querySelector(s);
const status = t => { $('#status').textContent = t; };

function dec(b64, T) { const s = atob(b64), u = new Uint8Array(s.length); for (let i = 0; i < s.length; i++) u[i] = s.charCodeAt(i); return new T(u.buffer); }
async function loadBody() {
  for (const u of URLS) {
    try {
      const r = await fetch(u); if (!r.ok) continue; const d = await r.json();
      const b = { n: d.n, pos: dec(d.pos, Float32Array), idx: dec(d.idx, Uint16Array), treg: dec(d.treg, Uint8Array), lm: d.lm, morphs: {} };
      for (const k in d.morphs) b.morphs[k] = { i: dec(d.morphs[k].i, Uint16Array), d: dec(d.morphs[k].d, Int16Array) };
      b.vreg = new Uint8Array(b.n); for (let t = 0; t < b.idx.length; t++) b.vreg[b.idx[t]] = b.treg[(t / 3) | 0];
      return b;
    } catch (e) { /* next */ }
  }
  throw new Error('Could not load data/body.json from the repo');
}
function shapeBody(ch) {
  const P = new Float32Array(B.pos);
  for (const k of KEYS) {
    const v = +ch[k] || 0; if (!v) continue; const M = B.morphs[k + (v < 0 ? '_n' : '_p')]; if (!M) continue;
    const f = Math.abs(v) * 1e-4, I = M.i, D = M.d;
    for (let j = 0; j < I.length; j++) { const o = I[j] * 3; P[o] += D[j * 3] * f; P[o + 1] += D[j * 3 + 1] * f; P[o + 2] += D[j * 3 + 2] * f; }
  }
  return P;
}
// one normal per position: the body repeats vertices along its seams
function smoothNormals(P, I) {
  const N = new Float32Array(P.length);
  for (let t = 0; t < I.length; t += 3) {
    const a = I[t] * 3, b = I[t + 1] * 3, c = I[t + 2] * 3;
    const ux = P[b] - P[a], uy = P[b + 1] - P[a + 1], uz = P[b + 2] - P[a + 2], vx = P[c] - P[a], vy = P[c + 1] - P[a + 1], vz = P[c + 2] - P[a + 2];
    const nx = uy * vz - uz * vy, ny = uz * vx - ux * vz, nz = ux * vy - uy * vx;
    for (const o of [a, b, c]) { N[o] += nx; N[o + 1] += ny; N[o + 2] += nz; }
  }
  const M = new Map(), key = o => Math.round(P[o] * 4000) + ',' + Math.round(P[o + 1] * 4000) + ',' + Math.round(P[o + 2] * 4000);
  for (let o = 0; o < P.length; o += 3) { const k = key(o), m = M.get(k); if (m) { m[0] += N[o]; m[1] += N[o + 1]; m[2] += N[o + 2]; } else M.set(k, [N[o], N[o + 1], N[o + 2]]); }
  for (let o = 0; o < P.length; o += 3) { const m = M.get(key(o)), l = Math.hypot(m[0], m[1], m[2]) || 1; N[o] = m[0] / l; N[o + 1] = m[1] / l; N[o + 2] = m[2] / l; }
  return N;
}
function pick(P, N, test) {
  const a = [], b = [];
  for (let i = 0; i < P.length / 3; i++) if (test(i, P[i * 3], P[i * 3 + 1], P[i * 3 + 2])) { a.push(P[i * 3], P[i * 3 + 1], P[i * 3 + 2]); if (N) b.push(N[i * 3], N[i * 3 + 1], N[i * 3 + 2]); }
  return { P: new Float32Array(a), N: N ? new Float32Array(b) : null };
}
const cat = (...a) => { const o = new Float32Array(a.reduce((s, x) => s + x.length, 0)); let k = 0; for (const x of a) { o.set(x, k); k += x.length; } return o; };

// ---- collision: nearest surface point per 1 cm voxel, pushed out along its normal ----
function collider(P, N, th, reach = 0.04, h = 0.01) {
  let x0 = 1e9, y0 = 1e9, z0 = 1e9, x1 = -1e9, y1 = -1e9, z1 = -1e9; const n = P.length / 3;
  for (let i = 0; i < n; i++) { const x = P[i * 3], y = P[i * 3 + 1], z = P[i * 3 + 2]; x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y); z0 = Math.min(z0, z); z1 = Math.max(z1, z); }
  x0 -= reach; y0 -= reach; z0 -= reach;
  const nx = Math.ceil((x1 + reach - x0) / h) + 1, ny = Math.ceil((y1 + reach - y0) / h) + 1, nz = Math.ceil((z1 + reach - z0) / h) + 1;
  const I = new Int32Array(nx * ny * nz).fill(-1), D = new Float32Array(nx * ny * nz).fill(1e9), r = Math.ceil(reach / h), R2 = reach * reach;
  for (let v = 0; v < n; v++) {
    const px = P[v * 3], py = P[v * 3 + 1], pz = P[v * 3 + 2], cx = Math.round((px - x0) / h), cy = Math.round((py - y0) / h), cz = Math.round((pz - z0) / h);
    for (let a = Math.max(0, cx - r); a <= Math.min(nx - 1, cx + r); a++) for (let b = Math.max(0, cy - r); b <= Math.min(ny - 1, cy + r); b++) for (let c = Math.max(0, cz - r); c <= Math.min(nz - 1, cz + r); c++) {
      const dx = x0 + a * h - px, dy = y0 + b * h - py, dz = z0 + c * h - pz, d2 = dx * dx + dy * dy + dz * dz;
      const k = (a * ny + b) * nz + c; if (d2 < R2 && d2 < D[k]) { D[k] = d2; I[k] = v; }
    }
  }
  return { x0, y0, z0, h, nx, ny, nz, I, P, N, th };
}
function push(c, P, o) {
  const ix = Math.round((P[o] - c.x0) / c.h), iy = Math.round((P[o + 1] - c.y0) / c.h), iz = Math.round((P[o + 2] - c.z0) / c.h);
  if (ix < 0 || iy < 0 || iz < 0 || ix >= c.nx || iy >= c.ny || iz >= c.nz) return;
  const v = c.I[(ix * c.ny + iy) * c.nz + iz]; if (v < 0) return; const q = v * 3, N = c.N, Q = c.P;
  const d = (P[o] - Q[q]) * N[q] + (P[o + 1] - Q[q + 1]) * N[q + 1] + (P[o + 2] - Q[q + 2]) * N[q + 2];
  if (d < c.th) { const m = c.th - d; P[o] += N[q] * m; P[o + 1] += N[q + 1] * m; P[o + 2] += N[q + 2] * m; }
}

// ---- radial maps (the starting shell only; the cloth's shape comes from the settle) ----
function fillConvex(m) {
  const NB = m.length, f = m.slice();
  for (let i = 0; i < NB; i++) if (!f[i]) { let a = 1, b = 1; while (!m[(i - a + NB) % NB] && a < NB) a++; while (!m[(i + b) % NB] && b < NB) b++; const va = m[(i - a + NB) % NB], vb = m[(i + b) % NB]; f[i] = (va * b + vb * a) / (a + b); }
  const K = Math.round(NB / 7), o = new Float32Array(NB);
  for (let i = 0; i < NB; i++) { let best = 0; for (let j = -K; j <= K; j++) best = Math.max(best, f[(i + j + NB) % NB] * Math.cos(j * TAU / NB)); o[i] = best; }
  return o;
}
function hRing(P, y, cx, cz, band, NB) {
  const m = new Float32Array(NB);
  for (let i = 0; i < P.length; i += 3) { const dy = P[i + 1] - y; if (dy > band || dy < -band) continue; const dx = P[i] - cx, dz = P[i + 2] - cz, b = Math.floor((Math.atan2(dx, dz) / TAU + 1) * NB) % NB, r = Math.hypot(dx, dz); if (r > m[b]) m[b] = r; }
  return fillConvex(m);
}
function eRing(P, O, el, band, NB) {
  const m = new Float32Array(NB);
  for (let i = 0; i < P.length; i += 3) { const dx = P[i] - O[0], dy = P[i + 1] - O[1], dz = P[i + 2] - O[2], hz = Math.hypot(dx, dz), e = Math.atan2(dy, hz); if (Math.abs(e - el) > band) continue; const b = Math.floor((Math.atan2(dx, dz) / TAU + 1) * NB) % NB, r = Math.hypot(hz, dy); if (r > m[b]) m[b] = r; }
  return fillConvex(m);
}
function samp(m, t) { const NB = m.length; let f = (t / TAU) * NB; f = ((f % NB) + NB) % NB; const i = Math.floor(f), u = f - i; return m[i] * (1 - u) + m[(i + 1) % NB] * u; }
const perim = (m, g) => m.reduce((s, r) => s + (r + g), 0) * TAU / m.length;

// ---- cloth ----
function newCloth() { return { pos: [], pin: [], gm: [], grp: [], ax: [], ca: [], cb: [], cr: [], ck: [], tri: [], ta: [], tb: [], tr: [], n: 0 }; }
function addGrid(cl, R, C, wrap, f, opt = {}) {
  const base = cl.n;
  for (let r = 0; r < R; r++) for (let c = 0; c < C; c++) { const q = f(r, c); cl.pos.push(...q.p); cl.ax.push(...q.ax); cl.pin.push(q.pin || 0); cl.gm.push(q.gm ?? 1); cl.grp.push(q.grp); cl.n++; }
  const id = (r, c) => base + r * C + ((c % C) + C) % C, P = cl.pos;
  for (let pass = 0; pass < (opt.smooth || 0); pass++) for (let r = 1; r < R - 1; r++) for (let c = 0; c < C; c++) { const i = id(r, c); if (cl.pin[i] || cl.gm[i] < 1) continue; const a = id(r - 1, c) * 3, b = id(r + 1, c) * 3, o = i * 3; for (let k = 0; k < 3; k++) P[o + k] = 0.5 * P[o + k] + 0.25 * (P[a + k] + P[b + k]); }
  const dist = (i, j) => Math.hypot(P[i * 3] - P[j * 3], P[i * 3 + 1] - P[j * 3 + 1], P[i * 3 + 2] - P[j * 3 + 2]);
  const add = (i, j, k, s = 1) => { cl.ca.push(i); cl.cb.push(j); cl.ck.push(k); cl.cr.push(dist(i, j) * s); };
  const cc = wrap ? C : C - 1, kb = opt.kb || (() => 0.25);
  // tethers: a particle may come nearer the row it hangs from, never further (stops the cloth stretching under its weight)
  if (opt.tether) for (let r = 0; r < R; r++) for (let c = 0; c < C; c++) { const ar = opt.tether(r); if (ar < 0 || ar === r) continue; const i = id(r, c), j = id(ar, c); cl.ta.push(i); cl.tb.push(j); cl.tr.push(dist(i, j) * 1.01); }
  for (let r = 0; r < R; r++) {
    let per = 0; for (let c = 0; c < cc; c++) per += dist(id(r, c), id(r, c + 1));
    const s = opt.hs ? opt.hs(r, per) : 1;
    for (let c = 0; c < cc; c++) add(id(r, c), id(r, c + 1), 1, s);
    for (let c = 0; c < (wrap ? C : C - 2); c++) add(id(r, c), id(r, c + 2), kb(r), s);
  }
  for (let r = 0; r < R - 1; r++) for (let c = 0; c < C; c++) { add(id(r, c), id(r + 1, c), 1); if (r < R - 2) add(id(r, c), id(r + 2, c), kb(r)); }
  for (let r = 0; r < R - 1; r++) for (let c = 0; c < cc; c++) {
    add(id(r, c), id(r + 1, c + 1), 0.5); add(id(r, c + 1), id(r + 1, c), 0.5);
    cl.tri.push(id(r, c), id(r + 1, c), id(r, c + 1), id(r, c + 1), id(r + 1, c), id(r + 1, c + 1));
  }
  return { base, R, C };
}
function finish(cl) {
  return Object.assign(cl, { P: new Float32Array(cl.pos), AX: new Float32Array(cl.ax), PIN: new Uint8Array(cl.pin), GM: new Float32Array(cl.gm), GRP: new Uint8Array(cl.grp),
    TA: new Int32Array(cl.ta), TB: new Int32Array(cl.tb), TR: new Float32Array(cl.tr), CA: new Int32Array(cl.ca), CB: new Int32Array(cl.cb), CR: new Float32Array(cl.cr), CK: new Float32Array(cl.ck), TRI: new Uint32Array(cl.tri) });
}
function groupPts(cl, g, side) { const a = []; for (let i = 0; i < cl.n; i++) if (cl.GRP[i] === g && (!side || cl.P[i * 3] * side > 0)) a.push(cl.P[i * 3], cl.P[i * 3 + 1], cl.P[i * 3 + 2]); return new Float32Array(a); }

function buildTop(cfg, X) {
  const cl = newCloth(), open = !!cfg.open, C = open ? 58 : 64, a0 = open ? 0.26 : 0;
  const th = c => open ? a0 + (TAU - 2 * a0) * c / (C - 1) : TAU * c / C;
  const yN = X.yN, yY = yN - 0.2, yH = yN - cfg.len * 0.97, nT = Math.round((yY - yH) / 0.022), nY = 8, nC = cfg.collar || 0, zY = X.zc(yY);
  const rows = []; let Etop = 0;
  for (let r = 0; r <= nT; r++) {
    const y = yH + (yY - yH) * r / nT, z = X.zc(y), map = hRing(X.cloud, y, 0, z, 0.013, 96);
    const E = Math.max(0, (cfg.chest / 100 - perim(map, cfg.gap)) / TAU) * clamp((yN - 0.16 - y) / 0.12, 0.25, 1);
    if (r === nT) Etop = E; rows.push({ k: 't', y, z, map, E });
  }
  for (let k = 1; k <= nY; k++) { const el = k * 1.08 / nY; rows.push({ k: 'y', el, map: eRing(X.cloud, [0, yY, zY], el, 0.07, 96), E: Etop * (1 - k / nY) ** 2 }); }
  const nRow = rows.length; rows.push({ k: 'n', map: hRing(X.neck, yN, 0, X.zN, 0.012, 96) });
  for (let j = 1; j <= nC; j++) rows.push({ k: 'c', j });
  const W = t => (0.3 + 0.7 * Math.sin(t) ** 2) / 0.65;
  const G = addGrid(cl, rows.length, C, !open, (r, c) => {
    const t = th(c), s = Math.sin(t), co = Math.cos(t), w = rows[r];
    if (w.k === 't') { const rad = samp(w.map, t) + cfg.gap + w.E * W(t); return { p: [s * rad, w.y, w.z + co * rad], ax: [0, w.y, w.z], grp: 0 }; }
    if (w.k === 'y') { const rad = samp(w.map, t) + cfg.gap + w.E * W(t), ce = Math.cos(w.el), se = Math.sin(w.el); return { p: [s * ce * rad, yY + se * rad, zY + co * ce * rad], ax: [0, yY + se * rad, zY], grp: 0 }; }
    const nr = samp(rows[nRow].map, t) + cfg.neckGap;
    if (w.k === 'n') return { p: [s * nr, yN, X.zN + co * nr], ax: [0, yN, X.zN], grp: 0, pin: 1 };
    const rr = nr + 0.004 * w.j, yy = yN + 0.017 * w.j; return { p: [s * rr, yy, X.zN + co * rr], ax: [0, yy, X.zN], grp: 0, gm: 0.15 };
  }, { hs: (r, per) => (cfg.rib && r < 3) ? clamp(cfg.rib / 100 / per, 0.72, 1) : 1, kb: r => rows[r].k === 'c' ? 0.9 : 0.25, tether: r => r < nRow ? nRow : -1, smooth: 6 });
  cl.neckRow = { base: G.base + nRow * C, C, th }; cl.collarTop = yN + 0.017 * nC;
  for (const sd of [1, -1]) addSleeve(cl, cfg, X, sd);
  return finish(cl);
}
function addSleeve(cl, cfg, X, sd) {
  const arm = X.arm[sd > 0 ? 0 : 1], armB = X.armBody[sd > 0 ? 0 : 1], nS = 22, CS = 24, yT = 1.4, yB = X.wristY + 0.015, rows = [];
  let cx = 0.2 * sd, cz = 0.02;
  for (let r = 0; r <= nS; r++) {
    const t = r / nS, y = yT + (yB - yT) * t; let sx = 0, sz = 0, k = 0;
    for (let i = 0; i < armB.length; i += 3) if (Math.abs(armB[i + 1] - y) < 0.015) { sx += armB[i]; sz += armB[i + 2]; k++; }
    if (k) { cx = sx / k; cz = sz / k; }
    rows.push({ t, y, cx, cz, map: hRing(arm, y, cx, cz, 0.013, 48) });
  }
  const e0 = Math.max(0, (cfg.bicep / 100 - perim(rows[3].map, cfg.gap)) / TAU), out = sd > 0 ? Math.PI / 2 : -Math.PI / 2;
  addGrid(cl, nS + 1, CS, true, (r, c) => {
    const w = rows[r], t = TAU * c / CS, y = w.y + 0.035 * Math.max(0, 1 - w.t / 0.18) * Math.cos(t - out);
    const rad = samp(w.map, t) + cfg.gap + 0.004 + e0 * (1 - w.t) ** 1.2;
    return { p: [w.cx + Math.sin(t) * rad, y, w.cz + Math.cos(t) * rad], ax: [w.cx, y, w.cz], grp: 1, pin: r === 0 ? 1 : 0 };
  }, { hs: (r, per) => r >= nS - 1 ? clamp(cfg.cuff / 100 / per, 0.7, 1) : 1, tether: () => 0 });
}
function buildHood(hd, X) {
  const cl = newCloth(), nr = hd.neckRow, cols = [];
  for (let c = 0; c < nr.C; c++) { const t = nr.th(c); if (t > 0.6 && t < TAU - 0.6) cols.push({ i: nr.base + c, t }); }
  addGrid(cl, 18, cols.length, false, (r, c) => {
    const { i, t } = cols[c], o = i * 3, P = hd.P, rx = Math.sin(t), rz = Math.cos(t);
    const ph = Math.abs(t - Math.PI) / (Math.PI - 0.6), L = 1 - 0.8 * ph * ph; let u = 0, v = 0;
    const bx = Math.sin(t) * 0.3, bz = -1, bl = Math.hypot(bx, bz);
    const BETA = [45, 0, -50, -75];
    for (let k = 4; k <= r; k++) { const b = (BETA[k - 4] ?? -82) * Math.PI / 180; u += Math.cos(b) * 0.024 * L; v += Math.sin(b) * 0.024 * L; }
    const k3 = Math.min(r, 3), ru = 0.003 + 0.002 * k3;
    v += 0.022 * k3;
    return { p: [P[o] + rx * ru + bx / bl * u, P[o + 1] + v, P[o + 2] + rz * ru + bz / bl * u], ax: [0, P[o + 1] + v, X.zN], grp: r <= 3 ? 2 : 3, pin: r === 0 ? 1 : 0 };
  }, { kb: () => 0.35, tether: () => 0 });
  return finish(cl);
}
function clothCollider(cl) {
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(cl.P.slice(), 3)); g.setIndex(new THREE.BufferAttribute(cl.TRI, 1)); g.computeVertexNormals();
  const N = g.attributes.normal.array.slice(), P = cl.P.slice(), A = cl.AX;
  for (let o = 0; o < P.length; o += 3) {
    let rx = P[o] - A[o], ry = P[o + 1] - A[o + 1], rz = P[o + 2] - A[o + 2];
    if (N[o] * rx + N[o + 1] * ry + N[o + 2] * rz < 0) { N[o] *= -1; N[o + 1] *= -1; N[o + 2] *= -1; }
    if (!N[o] && !N[o + 1] && !N[o + 2]) { const l = Math.hypot(rx, ry, rz) || 1; N[o] = rx / l; N[o + 1] = ry / l; N[o + 2] = rz / l; }
  }
  g.dispose(); return collider(P, N, 0.007, 0.04);
}
async function settle(cl, steps, cols, mesh, label, my) {
  const P = cl.P, Q = P.slice(), n = cl.n, { CA, CB, CR, CK, PIN, GM, GRP, TA, TB, TR } = cl, nc = CA.length, nt = TA.length, G = -9.8 / 3600;
  for (let s = 0; s < steps; s++) {
    if (my !== token) return false;
    for (let i = 0; i < n; i++) { if (PIN[i]) continue; const o = i * 3; for (let a = 0; a < 3; a++) { const v = (P[o + a] - Q[o + a]) * 0.96; Q[o + a] = P[o + a]; P[o + a] += v; } P[o + 1] += G * GM[i]; }
    for (let it = 0; it < 10; it++) { if (it === 5) for (let i = 0; i < n; i++) { if (PIN[i]) continue; const L = cols[GRP[i]]; if (L) for (const c of L) push(c, P, i * 3); }
      for (let c = 0; c < nc; c++) {
      const a = CA[c], b = CB[c], wi = PIN[a] ? 0 : 1, wj = PIN[b] ? 0 : 1; if (!(wi + wj)) continue; const i = a * 3, j = b * 3;
      const dx = P[j] - P[i], dy = P[j + 1] - P[i + 1], dz = P[j + 2] - P[i + 2], d = Math.sqrt(dx * dx + dy * dy + dz * dz) || 1e-9, f = (d - CR[c]) / d * CK[c] / (wi + wj);
      P[i] += dx * f * wi; P[i + 1] += dy * f * wi; P[i + 2] += dz * f * wi; P[j] -= dx * f * wj; P[j + 1] -= dy * f * wj; P[j + 2] -= dz * f * wj;
    } }
    for (let c = 0; c < nt; c++) { const i = TA[c] * 3, j = TB[c] * 3, dx = P[i] - P[j], dy = P[i + 1] - P[j + 1], dz = P[i + 2] - P[j + 2], d = Math.sqrt(dx * dx + dy * dy + dz * dz); if (d > TR[c]) { const f = TR[c] / d; P[i] = P[j] + dx * f; P[i + 1] = P[j + 1] + dy * f; P[i + 2] = P[j + 2] + dz * f; } }
    for (let i = 0; i < n; i++) { if (PIN[i]) continue; const L = cols[GRP[i]]; if (L) for (const c of L) push(c, P, i * 3); }
    if (s % 7 === 6 || s === steps - 1) { refresh(mesh); status(label + ' ' + Math.round(100 * (s + 1) / steps) + '%'); await frame(); }
  }
  return true;
}

// ---- scene ----
const mat = {
  body: new THREE.MeshStandardMaterial({ name: 'skin_and_denim', vertexColors: true, roughness: 0.7 }),
  marl: new THREE.MeshStandardMaterial({ name: 'grey_marl', color: '#8f9194', roughness: 0.95, side: THREE.DoubleSide }),
  navy: new THREE.MeshStandardMaterial({ name: 'navy', color: '#222c45', roughness: 0.72, side: THREE.DoubleSide }),
};
const group = new THREE.Group(); group.name = 'dave_g-mod-27';
const mk = (name, m) => { const o = new THREE.Mesh(new THREE.BufferGeometry(), m); o.name = name; o.castShadow = o.receiveShadow = true; group.add(o); return o; };
const M = { body: mk('body', mat.body), hoodie: mk('hoodie', mat.marl), hood: mk('hood', mat.marl), jacket: mk('jacket', mat.navy) };
function refresh(m) { const g = m.geometry; g.attributes.position.needsUpdate = true; g.computeVertexNormals(); g.computeBoundingSphere(); }
function setCloth(m, cl) { const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(cl.P, 3)); g.setIndex(new THREE.BufferAttribute(cl.TRI, 1)); g.computeVertexNormals(); m.geometry.dispose(); m.geometry = g; m.visible = true; }
function setBody(P, N) {
  const g = new THREE.BufferGeometry(), col = new Float32Array(P.length), L = B.lm, ey = L.eye[1], ez = L.eye[2];
  const C = h => { const c = new THREE.Color(h); return [c.r, c.g, c.b]; }, skin = C('#e2b08f'), jean = C('#2f3b52'), boot = C('#2b2420'), hair = C('#38261b');
  for (let i = 0; i < B.n; i++) {
    const r = B.vreg[i], y = P[i * 3 + 1], z = P[i * 3 + 2]; let c = skin;
    if (r === RG.foot) c = boot; else if (r === RG.thigh || r === RG.shin || ((r === RG.hips || r === RG.belly) && y < 1.0)) c = jean;
    else if (r === RG.head && (y > ey + 0.075 || (y > ey + 0.02 && z < ez - 0.07))) c = hair;
    col.set(c, i * 3);
  }
  g.setAttribute('position', new THREE.BufferAttribute(P, 3)); g.setAttribute('normal', new THREE.BufferAttribute(N, 3)); g.setAttribute('color', new THREE.BufferAttribute(col, 3));
  g.setIndex(new THREE.BufferAttribute(B.idx, 1)); g.computeBoundingSphere(); M.body.geometry.dispose(); M.body.geometry = g;
}
const VIEWS = { front: [[0, 1.3, 3.0], [0, 1.1, 0]], q: [[2.0, 1.5, 2.2], [0, 1.15, 0]], side: [[3.0, 1.3, 0], [0, 1.1, 0]], back: [[0, 1.4, -3.0], [0, 1.15, 0]], neck: [[0.7, 1.72, -0.85], [0, 1.47, 0]] };
function view(k) { const [p, t] = VIEWS[k]; stage._camera.position.set(...p); stage._controls.target.set(...t); stage._controls.update(); document.querySelectorAll('[data-view]').forEach(b => b.setAttribute('aria-pressed', b.dataset.view === k)); }

// like check_3d's "under" rays: round the back of his neck, across the collar's height, which is met first
function rays(X, yTop) { // horizontal rays from behind, at the collar's height
  const rc = new THREE.Raycaster(); let hood = 0, collar = 0, n = 0; group.updateMatrixWorld(true);
  for (const a of [-0.5, -0.25, 0, 0.25, 0.5]) for (let y = X.yN + 0.01; y <= yTop - 0.004; y += 0.01) {
    const t = Math.PI + a, o = new THREE.Vector3(Math.sin(t) * 0.6, y, X.zN + Math.cos(t) * 0.6);
    rc.set(o, new THREE.Vector3(0, y, X.zN).sub(o).normalize());
    const hit = rc.intersectObjects([M.hood, M.jacket, M.body], false)[0]; n++;
    if (hit && hit.object === M.hood) hood++; else if (hit && hit.object === M.jacket) collar++;
  }
  return { hood, collar, n };
}


async function run() {
  const my = ++token, t0 = performance.now(), sz = SIZES[S.size];
  $('#result').textContent = '';
  status('Shaping body…'); await frame();
  const P = shapeBody(PRESETS[S.body]), N = smoothNormals(P, B.idx), V = B.vreg, yS = B.lm.shoulder[0];
  setBody(P, N); M.hoodie.visible = M.hood.visible = M.jacket.visible = false;
  const isArm = (r, y) => r === RG.farm || r === RG.hand || (r === RG.uarm && y < yS - 0.08);
  const coreC = pick(P, N, (i, x, y) => y > 0.6 && !isArm(V[i], y));
  const armC = pick(P, N, (i, x, y) => V[i] === RG.uarm || V[i] === RG.farm || V[i] === RG.hand);
  const torso = pick(P, null, (i, x, y) => y > 0.6 && y < 1.62 && V[i] !== RG.head && !isArm(V[i], y)).P;
  const armBody = [1, -1].map(s => pick(P, null, (i, x) => (V[i] === RG.uarm || V[i] === RG.farm) && x * s > 0.1).P);
  const neck = pick(P, null, (i, x, y) => (V[i] === RG.neck || V[i] === RG.chest || V[i] === RG.head) && Math.abs(x) < 0.066 && y > 1.46 && y < 1.58).P;
  const band = (Y, test) => { let a = 1e9, b = -1e9; for (let i = 0; i < P.length / 3; i++) { const y = P[i * 3 + 1]; if (Math.abs(y - Y) < 0.012 && test(i)) { const z = P[i * 3 + 2]; a = Math.min(a, z); b = Math.max(b, z); } } return a < b ? (a + b) / 2 : 0; };
  const zc = Y => band(Y, i => Math.abs(P[i * 3]) < 0.06 && V[i] !== RG.head && !isArm(V[i], Y));
  const X = { yN: 1.505, zN: band(1.505, i => (V[i] === RG.neck || V[i] === RG.chest) && Math.abs(P[i * 3]) < 0.066), zc, wristY: B.lm.wrist[1], armBody };
  const body = collider(coreC.P, coreC.N, 0.006), arms = collider(armC.P, armC.N, 0.006);
  let chest = 0; for (const y of [1.22, 1.26, 1.3]) chest = Math.max(chest, perim(hRing(torso, y, 0, zc(y), 0.012, 96), 0));
  const HC = { chest: sz.hc, len: sz.hl / 100, rib: sz.hc * 0.82, bicep: sz.hb, cuff: 19, gap: 0.008, neckGap: 0.012 };
  const JC = { chest: sz.jc, len: sz.jl / 100, bicep: sz.jb, cuff: 27, gap: 0.012, neckGap: 0.012, open: 1, collar: 3 };

  const hoodie = buildTop(HC, { ...X, cloud: torso, neck, arm: armBody });
  setCloth(M.hoodie, hoodie);
  if (!await settle(hoodie, 140, { 0: [body], 1: [arms] }, M.hoodie, 'Settling hoodie', my)) return;
  const hoodieC = clothCollider(hoodie), neckRow = [];
  for (let c = 0; c < hoodie.neckRow.C; c++) { const o = (hoodie.neckRow.base + c) * 3; neckRow.push(hoodie.P[o], hoodie.P[o + 1], hoodie.P[o + 2]); }
  const jacketX = extra => ({ ...X, cloud: cat(torso, groupPts(hoodie, 0), extra || new Float32Array()), neck: cat(neck, new Float32Array(neckRow), extra || new Float32Array()),
    arm: [1, -1].map((s, k) => cat(armBody[k], groupPts(hoodie, 1, s))) });
  let jacket, hood;
  if (S.hood === 'out') {
    jacket = buildTop(JC, jacketX()); setCloth(M.jacket, jacket);
    if (!await settle(jacket, 140, { 0: [body, hoodieC], 1: [arms, hoodieC] }, M.jacket, 'Settling jacket', my)) return;
    const jacketC = clothCollider(jacket);
    hood = buildHood(hoodie, X); setCloth(M.hood, hood);
    if (!await settle(hood, 150, { 2: [body], 3: [body, hoodieC, jacketC] }, M.hood, 'Laying the hood out over the jacket', my)) return;
  } else {
    hood = buildHood(hoodie, X); setCloth(M.hood, hood);
    if (!await settle(hood, 150, { 2: [body], 3: [body, hoodieC] }, M.hood, 'Laying the hood on the hoodie', my)) return;
    const hoodC = clothCollider(hood);
    jacket = buildTop(JC, jacketX(hood.P)); setCloth(M.jacket, jacket);
    if (!await settle(jacket, 140, { 0: [body, hoodieC, hoodC], 1: [arms, hoodieC] }, M.jacket, 'Putting the jacket on over the hood', my)) return;
  }
  const hits = rays(X, jacket.collarTop), secs = ((performance.now() - t0) / 1000).toFixed(1);
  status('Settled in ' + secs + ' s');
  $('#result').innerHTML =
    '<div><b>Back of the neck:</b> of ' + hits.n + ' rays at the collar’s height from behind, ' + hits.hood + (hits.hood === 1 ? ' meets' : ' meet') + ' the hood first and ' + hits.collar + ' the collar. ' + (hits.hood > hits.collar * 3 ? 'The hood lies out over the jacket’s collar.' : hits.collar > hits.hood * 3 ? 'The collar stands over the hood.' : '') + '</div>' +
    '<div><b>Fit:</b> his chest on this body is ' + Math.round(chest * 100) + ' cm. Hoodie ' + S.size + ' ' + sz.hc + ' cm (' + Math.round(sz.hc - chest * 100) + ' cm ease), jacket ' + sz.jc + ' cm.</div>';
}

document.addEventListener('click', e => {
  const b = e.target.closest('button[data-k]'); if (b) { S[b.dataset.k] = b.dataset.v; document.querySelectorAll('button[data-k="' + b.dataset.k + '"]').forEach(x => x.setAttribute('aria-pressed', x === b)); run(); return; }
  const v = e.target.closest('button[data-view]'); if (v) view(v.dataset.view);
});
try {
  status('Loading Dave’s body from the repo…');
  B = await loadBody();
  setBody(shapeBody(PRESETS.dave), smoothNormals(shapeBody(PRESETS.dave), B.idx));
  stage.setObject(group); view('q');
  await run();
} catch (e) { status(e.message); console.error(e); }
