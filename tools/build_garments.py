"""Builds the garment templates (data/garments/<archetype>.json): flat pattern pieces sewn on Dave's body and draped
as cloth in headless Blender, then baked for the page.

What it does:
  1. Makes Dave's body as the page draws him with his saved shape (CHAR_DEF in page.html: the Edit Dave morphs of
     data/body.json and the proportions of propWarp), in his relaxed pose and in an A-pose (arms out at 40 degrees),
     with the same vertices, from the MakeHuman rig tools/build_body.py uses.
  2. Cuts each archetype's pattern pieces flat (front, back, sleeves, rib bands, hood halves, collar), in metres, from
     its measurements for size L (MEAS), and meshes them (constrained Delaunay, about 1.4 cm apart).
  3. Places the pieces round the A-posed body, sews them with Blender's sewing springs and drapes them under gravity,
     then lowers the arms to his relaxed pose while the cloth follows. A hood is draped on its own after the garment,
     its neckline held on the garment's, falling back from his head onto his shoulders.
  4. Bakes for the page: every point's position on him, its place on the flat pattern (the page's cloth keeps these
     lengths, so a size or a body can change and the cloth still has its cut, and stripes and checks run with the
     pattern), the piece it belongs to, and where it sits on his body (the nearest triangle, and the offset from it),
     so it moves with every Edit Dave change before the page settles the layers.

    python3 tools/build_garments.py [--only hoodie,halfzip,jacket] [--debug <dir>] [--frames 1.0]

It runs itself inside Blender 4.5 LTS: BLENDER=<path to blender>, else ~/.cache/wardrobe-blender, where Blender is
downloaded from download.blender.org (and checked against its published sha256) on first use. The MakeHuman assets
come as in tools/build_body.py (--mh). --frames scales the simulation's length (0.3 for a quick look). --debug writes
each stage (placed, relaxed, mid-drape, draped) as JSON for tools/garment_view.js. GB_SELF=0 turns Blender's
self-collision off; GB_DBG=1 prints the pieces behind the worst corner in the corner check.

STATUS (12 Oct 2026, PR #35, stopped part-way; see STATUS.md and UPGRADE_PLAN.md 2zzzzzzzzzzzzzzzzz): steps 1 to 3 run for
the hoodie (body only), the quarter-zip and the jacket; the hoodie is checked by eye and the other two only run. Not
written yet: the hood's own drape, step 4 (nothing is written to data/garments yet) and anything in the page.
"""
import argparse, base64, hashlib, json, math, os, re, subprocess, sys, tarfile, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BLENDER_VER, BLENDER_DIR = "4.5.14", "Blender4.5"
BLENDER_TAR = "blender-%s-linux-x64.tar.xz" % BLENDER_VER


def find_blender():
    if os.environ.get("BLENDER"):
        return os.environ["BLENDER"]
    cache = os.path.expanduser("~/.cache/wardrobe-blender")
    exe = os.path.join(cache, BLENDER_TAR[:-7], "blender")
    if os.path.exists(exe):
        return exe
    os.makedirs(cache, exist_ok=True)
    base = "https://download.blender.org/release/%s/" % BLENDER_DIR
    tar = os.path.join(cache, BLENDER_TAR)
    print("downloading", base + BLENDER_TAR, flush=True)
    urllib.request.urlretrieve(base + BLENDER_TAR, tar)
    sums = urllib.request.urlopen(base + "blender-%s.sha256" % BLENDER_VER, timeout=60).read().decode()
    want = next(l.split()[0] for l in sums.splitlines() if l.strip().endswith(BLENDER_TAR))
    h = hashlib.sha256()
    with open(tar, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    if h.hexdigest() != want:
        os.remove(tar)
        sys.exit("Blender download does not match its sha256")
    with tarfile.open(tar) as t:
        t.extractall(cache)
    os.remove(tar)
    return exe


try:
    import bpy  # noqa: F401
    IN_BLENDER = True
except ImportError:
    IN_BLENDER = False

if not IN_BLENDER:
    if __name__ == "__main__":
        cmd = [find_blender(), "-b", "--factory-startup", "--python-exit-code", "1", "--python", os.path.abspath(__file__), "--"] + sys.argv[1:]
        sys.exit(subprocess.call(cmd))
    raise SystemExit

# ---------------------------------------------------------------- inside Blender
import bmesh
import mathutils
import numpy as np
from mathutils.geometry import delaunay_2d_cdt

sys.path.insert(0, HERE)
import build_body as BB  # noqa: E402


def b64(a):
    return base64.b64encode(np.ascontiguousarray(a).tobytes()).decode()


def unb64(s, dt):
    return np.frombuffer(base64.b64decode(s), dtype=dt)


def sstep(a, b, v):
    t = np.clip((np.asarray(v, float) - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


# ---- Dave's saved shape, from page.html ----
def char_def():
    src = open(os.path.join(ROOT, "page.html"), encoding="utf8").read()
    m = re.search(r"var CHAR_DEF=(\{[\s\S]*?\});", src)
    C = {k: float(v) for k, v in re.findall(r"(\w+):(-?\d+(?:\.\d+)?)(?=[,}])", m.group(1))}
    keys = json.loads(re.search(r"var BODY_KEYS=(\[[^\]]*\])", src).group(1))
    return C, keys


def prop_warp(C, chin):
    """page.html propWarp: heights band by band (legs, torso, neck, head), the arms re-hung at their length, the
    shoulders sloped and the torso deepened; None when his proportions are the standard ones."""
    v = lambda k: C.get(k, 0.0)
    K = dict(fl=1 + 0.1 * v("legLen"), ft=1 + 0.1 * v("torsoLen"), fn=1 + 0.3 * v("neckLen"), af=1 + 0.1 * v("armLen"),
             hs=1 + 0.1 * v("headSize"), td=1 + 0.13 * v("torsoDepth"), ss=v("shoulderSlope"))
    A, Cc, S, Ch = 0.09, 0.85, 1.45, chin
    c1 = A + (Cc - A) * K["fl"]; s1 = c1 + (S - Cc) * K["ft"]; h1 = s1 + (Ch - S) * K["fn"]

    def W(y):
        return np.where(y <= A, y, np.where(y <= Cc, A + (y - A) * K["fl"], np.where(y <= S, c1 + (y - Cc) * K["ft"],
                        np.where(y <= Ch, s1 + (y - S) * K["fn"], h1 + (y - Ch) * K["hs"]))))

    def hk(y):
        return np.where(y >= Ch, K["hs"], np.where(y > Ch - 0.05, 1 + (K["hs"] - 1) * (y - (Ch - 0.05)) / 0.05, 1.0))

    def pt(P, arm, hz):
        P = P.copy(); x, y, z = P[:, 0].copy(), P[:, 1].copy(), P[:, 2].copy(); SL = -0.028 * K["ss"]
        a = arm & (y < S)
        wd = sstep(Cc - 0.1, Cc + 0.04, y) * (1 - sstep(1.5, 1.57, y))
        z2 = np.where((wd > 0) & (K["td"] != 1), -0.01 + (z + 0.01) * (1 + (K["td"] - 1) * wd), z)
        ws = sstep(0.07, 0.19, np.abs(x)) * sstep(1.3, 1.44, y) * (1 - sstep(1.56, 1.62, y)) if SL else 0 * y
        k = hk(y)
        yo = W(y) + SL * ws
        xo = np.where(k != 1, x * k, x); zo = np.where(k != 1, hz + (z2 - hz) * k, z2)
        P[:, 0] = np.where(a, x, xo); P[:, 1] = np.where(a, W(np.full_like(y, S)) - (S - y) * K["af"] + SL, yo)
        P[:, 2] = np.where(a, z, zo)
        return P
    return pt


class Body:
    """Dave's body: relaxed (as the page draws him with his saved shape) and in A-poses, same vertices."""

    def __init__(self, mh, apose_deg=(40, 30, 20, 12)):
        d = json.load(open(os.path.join(ROOT, "data", "body.json")))
        self.d = d
        n = d["n"]
        self.idx = unb64(d["idx"], np.uint16).astype(np.int64).reshape(-1, 3)
        self.treg = unb64(d["treg"], np.uint8)
        self.regions = d["regions"]
        P0 = unb64(d["pos"], np.float32).reshape(-1, 3).astype(np.float64)
        C, keys = char_def()
        self.char = C
        w = {}
        for k in keys:
            vv = C.get(k, 0.0)
            if vv < 0: w[k + "_n"] = -vv
            elif vv > 0: w[k + "_p"] = vv
        self.w = w
        Prel = P0.copy()
        for m, f in w.items():
            M = d["morphs"].get(m)
            if not M: continue
            I = unb64(M["i"], np.uint16).astype(np.int64); D = unb64(M["d"], np.int16).reshape(-1, 3).astype(np.float64)
            Prel[I] += D * 1e-4 * f
        # the arms (page bodyArmMask: arm, forearm and hand triangles, but the top of the shoulder stays with the torso)
        R = self.regions; am = np.zeros(n, bool)
        for t, rg in enumerate(self.treg):
            if R[rg] in ("uarm", "farm", "hand"): am[self.idx[t]] = True
        am &= P0[:, 1] <= 1.43
        self.armMask = am
        self.vreg = np.zeros(n, np.int64)
        for t, rg in enumerate(self.treg): self.vreg[self.idx[t]] = rg
        lm = d["lm"]
        self.lm = lm
        # (the landmarks moved by his shape, as bodyLM does; only the skull's centre and the chin are needed)
        chin, sk1 = lm["chin"], lm["skull"][1]
        for m, f in w.items():
            dd = d.get("lmd", {}).get(m, {})
            if "chin" in dd: chin += dd["chin"] * f
            if "skull" in dd: sk1 += dd["skull"][1] * f
        self.PW = prop_warp(C, lm["chin"])
        self.hz = sk1
        self.rel0 = Prel
        self.rel = self.warp(Prel)

        # the A-poses from the rig: his shape mixed in the rest space, posed with the base body's joints (as
        # build_body.py poses the base and its morphs), framed as body.json is
        mesh, rig = BB.Mesh(mh), BB.Rig(mh)
        V = mesh.mix(BB.BASE_MIX)
        Mr = rig.pose(V, BB.relaxed_pose(rig, V))
        skin = rig.skin_matrix(len(V))
        Pb = BB.skin_fast(V, Mr, skin)
        body = [f for f, g in zip(mesh.F, mesh.G) if g == "body"]
        tris = []
        for f in body: tris += [[f[0], f[1], f[2]], [f[0], f[2], f[3]]] if len(f) == 4 else [f]
        used = np.unique(np.array(tris))
        y0 = Pb[used, 1].min(); s = BB.CROWN / (Pb[used, 1].max() - y0)
        frame = lambda X: (X - np.array([0, y0, 0])) * s
        Vd = V.copy()
        for m, f in w.items():
            for k, ww in BB.MORPHS[m].items(): Vd += f * ww * mesh.target(k)
        chk = frame(BB.skin_fast(Vd, Mr, skin))[used]
        err = float(np.abs(chk - Prel).max())
        print("relaxed pose from the rig vs body.json: %.2f mm" % (err * 1000), flush=True)
        if err > 0.003: raise SystemExit("the rig does not reproduce data/body.json; rebuild the body first")
        self.apose, self.joints = [], []
        for deg in apose_deg:
            Ma = rig.pose(V, BB.relaxed_pose(rig, V, arm_out=deg, fore_fwd=14.0 * min(1, 12.0 / deg)))
            self.apose.append(self.warp(frame(BB.skin_fast(Vd, Ma, skin))[used]))
            J = {}
            for side, sg in (("L", 1), ("R", -1)):
                for nm, bone in (("sh", "upperarm01"), ("el", "lowerarm01"), ("wr", "wrist")):
                    h = rig.head(V, bone + "." + side); p = (Ma[bone + "." + side] @ np.r_[h, 1])[:3]
                    q = self.PW(frame(p[None]), np.array([nm != "sh"]), self.hz)[0] if self.PW else frame(p[None])[0]
                    J[nm + side] = q
            self.joints.append(J)
        self.n = n

    def warp(self, P):
        return self.PW(P, self.armMask, self.hz) if self.PW else P.copy()

    def region_tris(self, names):
        R = self.regions; ok = np.array([R[r] in names for r in self.treg])
        return np.where(ok)[0]


# ---------------------------------------------------------------- patterns
# Measurements in cm for size L. The shops' charts give L as a body chest (Duck and Cover 41-43 in, Ellesse 40-42,
# SikSilk 40-41.5, ASOS 42-44: data/sizecharts.json); a garment's own chest is that plus the ease of its kind (about
# 13 cm for a sweatshirt or hoodie, 18 for a jacket worn over one). Lengths are from the high point of the shoulder.
#   chest, length, shoulder (point to point), armhole (depth from the shoulder's high point), neck_w (across, high
#   point to high point), neck_f / neck_b (neckline drop at the front and back), sh_drop (shoulder slope), band (hem
#   band height), band_k (its width against the body's, a rib pulling in), sleeve (shoulder point to cuff end), bicep
#   (all round), wrist (all round, above the cuff), cuff (cuff height), cuff_c (cuff all round), collar (height)
MEAS = {
    "hoodie": dict(chest=120, length=70, shoulder=48, armhole=24, neck_w=19, neck_f=8.5, neck_b=2.2, sh_drop=4.5, band=6,
                   band_k=0.86, sleeve=63, bicep=40, wrist=27, cuff=7, cuff_c=20, hood_h=35, hood_d=25),
    "halfzip": dict(chest=120, length=70, shoulder=48, armhole=24, neck_w=18, neck_f=6.5, neck_b=2.2, sh_drop=4.5, band=6,
                    band_k=0.86, sleeve=63, bicep=40, wrist=27, cuff=7, cuff_c=20, collar=7),
    "jacket": dict(chest=124, length=68, shoulder=49, armhole=25.5, neck_w=19, neck_f=7.5, neck_b=2.2, sh_drop=4.5, band=4,
                   band_k=0.93, sleeve=65, bicep=44, wrist=28, cuff=5, cuff_c=24, collar=6.5, open=1),
}
H = 0.014   # mesh spacing (m)


def plen(P):
    return float(np.linalg.norm(np.diff(P, axis=0), axis=1).sum())


def resample(P, n):
    """n points along polyline P (both ends kept), evenly spaced by arc length"""
    P = np.asarray(P, float); s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]
    t = np.linspace(0, s[-1], n)
    return np.stack([np.interp(t, s, P[:, k]) for k in range(P.shape[1])], 1)


def bez(p0, p1, p2, p3, k=40):
    t = np.linspace(0, 1, k)[:, None]; p0, p1, p2, p3 = map(np.asarray, (p0, p1, p2, p3))
    return (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3


def seg(a, b, k=8):
    return np.linspace(np.asarray(a, float), np.asarray(b, float), k)


class Piece:
    """A flat pattern piece: its outline as named edges (each a polyline, CCW, each starting where the last ended)."""

    def __init__(self, name, grp, edges, stiff=0.0):
        self.name, self.grp, self.edges, self.stiff = name, grp, edges, stiff
        self.order = [e[0] for e in edges]

    def edge(self, nm):
        return dict(self.edges)[nm]


def bodice(M, kind, s, split=False):
    """Front or back (kind), its edges named by the pattern's sides: p for x > 0, n for x < 0. split: a front cut
    down the middle (an open jacket), returned as two pieces."""
    C, L = M["chest"] / 100 * s, M["length"] / 100 * s
    hw, yua, sw, ysp, nw = C / 4, L - M["armhole"] / 100 * s, M["shoulder"] / 200 * s, L - M["sh_drop"] / 100 * s, M["neck_w"] / 200 * s
    hb, bk = M["band"] / 100 * s, M["band_k"]
    nd = (M["neck_f"] if kind == "front" else M["neck_b"]) / 100 * s
    # (the band's rib pulls the hem in: the side seam steps in over 3 cm above it, as the body is gathered into the band)
    side = np.vstack([seg((hw * bk, 0), (hw * bk, hb), 4), bez((hw * bk, hb), (hw * bk, hb + 0.018 * s), (hw, hb + 0.012 * s), (hw, hb + 0.03 * s), 8)[1:], seg((hw, hb + 0.03 * s), (hw, yua), 12)[1:]])
    # (trued as a pattern is: the armhole leaves the side seam level and meets the shoulder at a right angle, and the
    # neckline leaves the shoulder at a right angle, so the pieces' corners add up to a full turn where they are sewn
    # together and the cloth lies flat there instead of standing up in a funnel or an ear)
    sd = np.array([nw - sw, L - ysp]); sd /= np.linalg.norm(sd)          # along the shoulder, toward the neck
    perp = np.array([-sd[1], sd[0]])                                     # at right angles to it
    if perp[1] > 0: perp = -perp                                         # (pointing down)
    ah = ysp - yua
    arm = bez((hw, yua), (hw - 0.62 * (hw - sw), yua), (sw, ysp) + perp * 0.45 * ah, (sw, ysp))
    sh = seg((sw, ysp), (nw, L), 6)
    nperp = -np.array([sd[1], -sd[0]]) if sd[1] > 0 else np.array([sd[1], -sd[0]])
    nperp = perp.copy()
    k1 = max(nd * 0.6, 0.012)
    if kind == "front":
        nk = bez((nw, L), np.array((nw, L)) + nperp * k1, (nw * 0.5, L - nd), (0, L - nd))
    else:
        nk = bez((nw, L), np.array((nw, L)) + nperp * k1, (nw * 0.45, L - nd), (0, L - nd))
    mir = lambda P: P[::-1] * np.array([-1, 1])
    hemp = seg((0, 0), (hw * bk, 0), 10)
    if split:
        cf = seg((0, L - nd), (0, 0), 20)
        p = Piece(kind + "_p", 0, [("hem", hemp), ("side_p", side), ("arm_p", arm), ("sh_p", sh), ("neck_p", nk), ("cf_p", cf)])
        n = Piece(kind + "_n", 0, [("hem", mir(hemp)), ("cf_n", mir(cf)), ("neck_n", mir(nk)), ("sh_n", mir(sh)), ("arm_n", mir(arm)), ("side_n", mir(side))])
        return [p, n]
    hem = seg((-hw * bk, 0), (hw * bk, 0), 20)
    return [Piece(kind, 0, [("hem", hem), ("side_p", side), ("arm_p", arm), ("sh_p", sh), ("neck_p", nk), ("neck_n", mir(nk)),
                           ("sh_n", mir(sh)), ("arm_n", mir(arm)), ("side_n", mir(side))])]


def sleeve(M, s, arm_len, grp):
    """A set-in sleeve, cap on top: its cap's height is solved so the cap is 3% longer than the armhole it is set in."""
    SLV, bc, wr, ch, cc = M["sleeve"] / 100 * s, M["bicep"] / 200 * s, M["wrist"] / 200 * s, M["cuff"] / 100 * s, M["cuff_c"] / 200 * s

    def build(cap):
        # (an S: the cap leaves the underarm level, at right angles to the sleeve's seam, hollows, then rounds over
        # the top, level at its crown)
        yb = SLV - cap
        mid = np.array([bc * 0.52, yb + cap * 0.48])
        lo = bez((bc, yb), (bc * 0.8, yb), mid + np.array([0.08, -0.12]) * cap, mid)
        hi = bez(mid, mid + np.array([-0.08, 0.12]) * cap * 2.2, (bc * 0.3, SLV), (0, SLV))
        return yb, np.vstack([lo, hi[1:]])
    lo, hi = 0.04 * s, 0.2 * s
    for _ in range(40):
        cap = (lo + hi) / 2; yb, capp = build(cap)
        if 2 * plen(capp) < arm_len * 1.03: lo = cap
        else: hi = cap
    under = np.vstack([seg((cc, 0), (cc, ch), 4), bez((cc, ch), (cc, ch + 0.015 * s), (wr, ch + 0.01 * s), (wr, ch + 0.025 * s), 8)[1:], seg((wr, ch + 0.025 * s), (bc, yb), 20)[1:]])
    mir = lambda P: P[::-1] * np.array([-1, 1])
    return Piece("sleeve" + ("_L" if grp == 1 else "_R"), grp, [("cuff", seg((-cc, 0), (cc, 0), 8)), ("under_p", under), ("cap_p", capp),
                 ("cap_n", mir(capp)), ("under_n", mir(under))]), yb, cap


def hood_half(M, s, nf, nb, side):
    """One side of a two-piece hood: its neckline (front part nf long, back part nb), the seam up its back and over
    the crown, and the face edge. x runs from the face edge back, so the two halves mirror."""
    Hh, Dd = M["hood_h"] / 100 * s, M["hood_d"] / 100 * s
    U = nf + nb
    F, B = np.array([0.0, 0.0]), np.array([U, 0.03 * s])
    neck = bez(F, (U * 0.35, -0.012 * s), (U * 0.7, 0.0), B)
    neck = resample(neck, 60)
    k = int(np.searchsorted(np.r_[0, np.cumsum(np.linalg.norm(np.diff(neck, axis=0), axis=1))], nf))
    back = bez(B, (U + 0.06 * s, Hh * 0.45), (Dd + 0.03 * s, Hh), (0.035 * s, Hh))
    face = bez((0.035 * s, Hh), (0.0, Hh * 0.7), (0.012 * s, Hh * 0.3), F)
    return Piece("hood_" + side, 3, [("neck_f", neck[:k + 1]), ("neck_b", neck[k:]), ("back", back), ("face", face)])


def collar(M, s, length, closed):
    """A stand collar along the neckline, taller at the back by nothing, the top edge 4% shorter so it hugs the neck."""
    h = M["collar"] / 100 * s
    top = 0.96
    if closed:
        return Piece("collar", 4, [("neck", seg((-length / 2, 0), (length / 2, 0), 30)), ("cf_p", seg((length / 2, 0), (length / 2 * top, h), 6)),
                                   ("top", seg((length / 2 * top, h), (-length / 2 * top, h), 30)), ("cf_n", seg((-length / 2 * top, h), (-length / 2, 0), 6))], stiff=1.0)
    return Piece("collar", 4, [("neck", seg((-length / 2, 0), (length / 2, 0), 30)), ("end_p", seg((length / 2, 0), (length / 2 - 0.004 * s, h), 6)),
                               ("top", seg((length / 2 - 0.004 * s, h), (-length / 2 + 0.004 * s, h), 30)), ("end_n", seg((-length / 2 + 0.004 * s, h), (-length / 2, 0), 6))], stiff=1.0)


# ---- meshing ----
def inside(poly, pts):
    """even-odd test of each point against a closed polygon"""
    x, y = pts[:, 0][:, None], pts[:, 1][:, None]
    a, b = poly, np.roll(poly, -1, axis=0)
    c = ((a[:, 1] > y) != (b[:, 1] > y)) & (x < (b[:, 0] - a[:, 0]) * (y - a[:, 1]) / (b[:, 1] - a[:, 1] + 1e-12) + a[:, 0])
    return (c.sum(1) % 2) == 1


def mesh_piece(pc, counts):
    """Triangulates a piece: its edges sampled (seamed edges with the count shared with their partner), a grid inside,
    constrained Delaunay. Gives pc.V (2D), pc.T (triangles) and pc.B[edge] (the outline's vertex ids along it)."""
    bpts, bids, eids = [], {}, {}
    for nm, P in pc.edges:
        n = counts.get((pc.name, nm)) or max(2, int(round(plen(P) / H)) + 1)
        Q = resample(P, n)
        ids = []
        for j, q in enumerate(Q):
            if j == len(Q) - 1: break   # (the next edge starts here)
            ids.append(len(bpts)); bpts.append(q)
        eids[nm] = ids
    nb = len(bpts)
    for i, nm in enumerate(pc.order):   # each edge's last point is the next edge's first
        nxt = pc.order[(i + 1) % len(pc.order)]
        eids[nm] = eids[nm] + [eids[nxt][0]]
    B = np.array(bpts)
    lo, hi = B.min(0), B.max(0)
    xs = np.arange(lo[0] + H / 2, hi[0], H); ys = np.arange(lo[1] + H / 2, hi[1], H * 0.866)
    inner = []
    for j, y in enumerate(ys):
        for x in xs + (H / 2 if j % 2 else 0):
            inner.append((x, y))
    inner = np.array(inner)
    keep = inside(B, inner)
    inner = inner[keep]
    if len(inner):
        d = np.min(np.linalg.norm(inner[:, None, :] - B[None, :, :], axis=2), axis=1)
        inner = inner[d > 0.55 * H]
    allp = np.vstack([B, inner]) if len(inner) else B
    vc = [mathutils.Vector((float(p[0]), float(p[1]))) for p in allp]
    out = delaunay_2d_cdt(vc, [], [list(range(nb))], 1, 1e-7, True)
    V2, E2, F2, ov = out[0], out[1], out[2], out[3]
    mp = {}
    for newi, olds in enumerate(ov):
        for o in olds: mp[o] = newi
    V = np.array([[v.x, v.y] for v in V2])
    Tr = np.array([f for f in F2 if len(f) == 3])
    # (the triangulation also fills the outline's hollows, a sleeve cap's or a neckline's: only what is inside it stays)
    Tr = Tr[inside(B, V[Tr].mean(1))]
    # (and lays slivers of no area along straight edges)
    e1, e2 = V[Tr[:, 1]] - V[Tr[:, 0]], V[Tr[:, 2]] - V[Tr[:, 0]]
    Tr = Tr[np.abs(e1[:, 0] * e2[:, 1] - e1[:, 1] * e2[:, 0]) / 2 > 0.02 * H * H]
    used = np.unique(Tr); rm = -np.ones(len(V), int); rm[used] = np.arange(len(used))
    pc.V, pc.T = V[used], rm[Tr]
    mp = {o: rm[n] for o, n in mp.items()}
    pc.B = {nm: [mp[i] for i in ids] for nm, ids in eids.items()}
    return pc


def mirror(pc, name):
    """the same piece for the other side (x negated, the outline turned to stay counter-clockwise)"""
    return Piece(name, pc.grp, [(nm, P[::-1] * np.array([-1, 1])) for nm, P in pc.edges[::-1]], pc.stiff)


# ---- the archetypes: pieces and seams ----
class Garment:
    def __init__(self, arch, scale):
        self.arch, self.M, self.s = arch, MEAS[arch], scale
        M, s = self.M, scale
        op = bool(M.get("open"))
        P = {}
        for pc in bodice(M, "front", s, split=op) + bodice(M, "back", s): P[pc.name] = pc
        fp, fn = ("front_p", "front_n") if op else ("front", "front")
        self.fp, self.fn = fp, fn
        arm_len = plen(P[fp].edge("arm_p")) + plen(P["back"].edge("arm_n"))
        for g in (1, 2):
            sl, self.yb, self.cap = sleeve(M, s, arm_len, g)
            P[sl.name] = sl
        # seams: [(piece, edge), ...] on one side against the other, sampled alike; the direction is found from the
        # placement. bias: how much of the closing move the first side takes (1: it moves onto the second).
        S = [([(fp, "sh_p")], [("back", "sh_n")], 0.5), ([(fn, "sh_n")], [("back", "sh_p")], 0.5),
             ([(fp, "side_p")], [("back", "side_n")], 0.5), ([(fn, "side_n")], [("back", "side_p")], 0.5),
             ([("sleeve_L", "cap_p")], [(fp, "arm_p")], 0.85), ([("sleeve_L", "cap_n")], [("back", "arm_n")], 0.85),
             ([("sleeve_R", "cap_p")], [(fn, "arm_n")], 0.85), ([("sleeve_R", "cap_n")], [("back", "arm_p")], 0.85),
             ([("sleeve_L", "under_p")], [("sleeve_L", "under_n")], 0.5), ([("sleeve_R", "under_p")], [("sleeve_R", "under_n")], 0.5)]
        # the neckline round from the middle of the front, by his right, the back and his left
        ring = [(fn, "neck_n"), ("back", "neck_p"), ("back", "neck_n"), (fp, "neck_p")]
        self.ring = ring
        rl = [plen(P[a].edge(b)) for a, b in ring]
        if "collar" in M:
            c = collar(M, s, sum(rl), closed=not op)
            # (its neckline cut into the same four parts)
            x0 = c.edge("neck")[0][0]; cum = np.r_[0, np.cumsum(rl)]
            parts = [seg((x0 + cum[i], 0), (x0 + cum[i + 1], 0), 8) for i in range(4)]
            c.edges = [("n%d" % i, parts[i]) for i in range(4)] + [e for e in c.edges if e[0] != "neck"]
            c.order = [e[0] for e in c.edges]
            P["collar"] = c
            S.append(([("collar", "n%d" % i) for i in range(4)], ring, 1.0))
            if not op: S.append(([("collar", "cf_p")], [("collar", "cf_n")], 0.5))
        self.P, self.S = P, S
        self.hood = None
        if "hood_h" in M:
            hl = hood_half(M, s, rl[3], rl[2], "L")
            self.hood = {"hood_L": hl, "hood_R": mirror(hl, "hood_R")}
            self.hood_S = [([("hood_L", "back")], [("hood_R", "back")], 0.5)]
            # (each half's neckline on the garment's: his left from the front by the shoulder to the back, and his right)
            self.hood_ring = {"hood_L": [("neck_f", (fp, "neck_p")), ("neck_b", ("back", "neck_n"))],
                              "hood_R": [("neck_f", (fn, "neck_n")), ("neck_b", ("back", "neck_p"))]}


def seam_counts(seams, pieces):
    """one count per seam part, the larger of its two sides' (so both are sampled alike)"""
    cnt = {}
    for A, Bs, _ in seams:
        for (pa, ea), (pb, eb) in zip(A, Bs):
            n = max(2, int(round(max(plen(pieces[pa].edge(ea)), plen(pieces[pb].edge(eb))) / H)) + 1)
            n = max(n, cnt.get((pa, ea), 0), cnt.get((pb, eb), 0))
            cnt[(pa, ea)] = cnt[(pb, eb)] = n
    return cnt


# ---- body measurements in a pose ----
def torso_at(P, body, y, band=0.012):
    reg = np.array([body.regions[r] for r in body.vreg])
    sel = (~body.armMask) & np.isin(reg, ["chest", "belly", "hips", "neck"]) & (np.abs(P[:, 1] - y) < band)
    X = P[sel]
    return float(np.abs(X[:, 0]).max()), float((X[:, 2].max() - X[:, 2].min()) / 2), float((X[:, 2].max() + X[:, 2].min()) / 2)


def hps(P, body):
    reg = np.array([body.regions[r] for r in body.vreg])
    sel = (~body.armMask) & np.isin(reg, ["chest", "neck"]) & (np.abs(P[:, 0]) > 0.078) & (np.abs(P[:, 0]) < 0.092)
    return float(P[sel, 1].max())


class Arc:
    """an ellipse round the torso, by arc length from the front (x = a sin t, z = zc + b cos t)"""

    def __init__(self, a, b, zc):
        self.a, self.b, self.zc = a, b, zc
        t = np.linspace(0, np.pi, 4001); q = np.stack([a * np.sin(t), b * np.cos(t)], 1)
        self.t, self.s = t, np.r_[0, np.cumsum(np.linalg.norm(np.diff(q, axis=0), axis=1))]

    def theta(self, s):
        return np.sign(s) * np.interp(np.abs(s), self.s, self.t)


def ellipse_for(per, r):
    return per / (math.pi * (3 * (1 + r) - math.sqrt((3 + r) * (1 + 3 * r))))


def place(G, pieces, body, pose):
    """3D positions for every piece round the A-posed body (pose index), before sewing"""
    P = body.apose[pose]; J = body.joints[pose]; M, s = G.M, G.s
    L = M["length"] / 100 * s
    yh = hps(P, body)
    yua3 = yh - M["armhole"] / 100 * s
    hw, hd, zc = torso_at(P, body, yua3 + 0.02)
    for yy in (yua3 - 0.12, yua3 - 0.25):
        a2, b2, _ = torso_at(P, body, yy); hw, hd = max(hw, a2), max(hd, b2)
    C = M["chest"] / 100 * s
    r = (hd + 0.022) / (hw + 0.026)
    ea = ellipse_for(C, r); eb = ea * r
    print("  torso %.3f x %.3f at %.3f; cloth round it %.3f x %.3f" % (hw, hd, zc, ea, eb), flush=True)
    arc = Arc(ea, eb, zc)
    Lb, Rb = 0.13 * s, 0.11
    y0 = yh + 0.02 - (L - Lb) - Rb * math.sin(Lb / Rb)
    out = {}
    for nm, pc in pieces.items():
        V = pc.V; X = np.zeros((len(V), 3))
        if nm.startswith(("front", "back")):
            th = arc.theta(V[:, 0]) + (np.pi if nm.startswith("back") else 0.0)
            q = np.stack([ea * np.sin(th), eb * np.cos(th)], 1); rc = np.linalg.norm(q, axis=1)
            yp = V[:, 1]; up = yp > L - Lb
            ph = np.where(up, (yp - (L - Lb)) / Rb, 0)
            rr = np.maximum(0.055, rc - Rb * (1 - np.cos(ph)))
            X[:, 0] = q[:, 0] / rc * rr; X[:, 2] = zc + q[:, 1] / rc * rr
            X[:, 1] = np.where(up, y0 + (L - Lb) + Rb * np.sin(ph), y0 + yp)
        elif nm.startswith("sleeve"):
            side = nm[-1]; sg = 1 if side == "L" else -1
            sh, el, wr = J["sh" + side], J["el" + side], J["wr" + side]
            l1, l2 = np.linalg.norm(el - sh), np.linalg.norm(wr - el)
            d1, d2 = (el - sh) / l1, (wr - el) / l2
            und = pc.edge("under_p"); yb = G.yb
            hwid = lambda y: np.interp(y, und[:, 1], und[:, 0])
            au = 0.03
            kax = min(1.0, (l1 + l2 - 0.012 - au) / yb)
            for i, (x, y) in enumerate(V):
                a = au + (yb - y) * kax if y < yb else au - (y - yb)
                if a < l1: c, d = sh + d1 * a, d1
                else: c, d = el + d2 * (a - l1), d2
                w = 2 * float(hwid(min(y, yb)))
                R = w / (2 * np.pi) + 0.004
                upp = sg * np.cross([0, 0, 1.0], d); upp /= np.linalg.norm(upp)
                fw = np.array([0, 0, 1.0]) - d[2] * d; fw /= np.linalg.norm(fw)
                ph = 2 * np.pi * x / w
                X[i] = c + R * (np.cos(ph) * upp + np.sin(ph) * fw)
        else:
            X[:] = np.nan   # (a collar: placed on the neckline it is sewn to)
        out[nm] = X
    return out


def close_seams(pieces, X, seams, reach=0.10):
    """Turns each seam the way its two sides lie, then moves both sides toward each other (bias), carrying the
    pieces' nearby points along, so the sewing starts nearly closed. Gives the sewing pairs (global ids)."""
    pairs = []
    for A, Bs, bias in seams:
        ia, ib = [], []
        for (pa, ea), (pb, eb) in zip(A, Bs):
            a = list(pieces[pa].B[ea]); b = list(pieces[pb].B[eb])
            if len(a) != len(b): raise SystemExit("seam %s.%s / %s.%s: %d against %d points" % (pa, ea, pb, eb, len(a), len(b)))
            XA, XB = X[pa][a], X[pb][b]
            if not np.isnan(XA).any() and np.linalg.norm(XA - XB[::-1], axis=1).mean() < np.linalg.norm(XA - XB, axis=1).mean():
                b = b[::-1]
            ia += [(pa, i) for i in a]; ib += [(pb, i) for i in b]
        pairs.append([ia, ib, bias])
    # a piece not yet placed (a collar) stands up from what it is sewn to; its seam's direction from the order of
    # the neckline parts (its own parts run the same way)
    for pr in pairs:
        ia, ib, bias = pr
        pa = ia[0][0]
        if not np.isnan(X[pa]).any(): continue
        pc = pieces[pa]; tgt = np.array([X[p][i] for p, i in ib]); src = [i for _, i in ia]
        V = pc.V; X[pa] = np.zeros((len(V), 3)); nx = V[src, 0]
        cen = tgt.mean(0)
        for j in range(len(V)):
            k = int(np.argmin(np.abs(nx - V[j, 0]))); base = tgt[k]
            rad = base - cen; rad[1] = 0; rad /= (np.linalg.norm(rad) + 1e-9)
            h = V[j, 1] - V[src[k], 1]
            X[pa][j] = base + np.array([0, h, 0]) + rad * 0.004
    for ia, ib, bias in pairs:
        XA = np.array([X[p][i] for p, i in ia]); XB = np.array([X[p][i] for p, i in ib]); mid = XA * (1 - bias) + XB * bias
        for side, pts in ((ia, XA), (ib, XB)):
            D = mid - pts; byp = {}
            for (p, i), dd in zip(side, D): byp.setdefault(p, []).append((i, dd))
            for p, lst in byp.items():
                pc = pieces[p]; ids = np.array([i for i, _ in lst]); DD = np.array([dd for _, dd in lst])
                dist = np.linalg.norm(pc.V[:, None, :] - pc.V[None, ids, :], axis=2)
                wgt = 1 / (dist ** 2 + 1e-6); fall = sstep(reach, 0.0, dist.min(1))
                X[p] += (wgt @ DD) / wgt.sum(1)[:, None] * fall[:, None]
    off, k = {}, 0
    for nm in pieces: off[nm] = k; k += len(pieces[nm].V)
    gp = []
    for ia, ib, _ in pairs:
        gp += [(off[pa] + i, off[pb] + j) for (pa, i), (pb, j) in zip(ia, ib)]
    return gp, off


def vnormals(P, idx):
    N = np.zeros_like(P); a, b, c = P[idx[:, 0]], P[idx[:, 1]], P[idx[:, 2]]
    fn = np.cross(b - a, c - a)
    for k in range(3): np.add.at(N, idx[:, k], fn)
    # (one normal per position: the body repeats vertices along its seams)
    key = np.round(P * 4000).astype(np.int64); _, inv = np.unique(key, axis=0, return_inverse=True)
    inv = inv.reshape(-1)
    S = np.zeros((inv.max() + 1, 3)); np.add.at(S, inv, N); N = S[inv]
    return N / (np.linalg.norm(N, axis=1, keepdims=True) + 1e-12)


def push_out(X, P, N, minimum=0.008):
    """points closer than minimum to his skin (or inside it) moved out along its normal"""
    kd = mathutils.kdtree.KDTree(len(P))
    for i, p in enumerate(P): kd.insert(p, i)
    kd.balance()
    moved = 0
    for i in range(len(X)):
        _, j, _ = kd.find(X[i])
        dd = float(np.dot(X[i] - P[j], N[j]))
        if dd < minimum:
            X[i] += N[j] * (minimum - dd); moved += 1
    return moved


def weld(n, pairs):
    """one vertex for each sewn pair (and chains of them, where seams meet at a corner)"""
    par = list(range(n))
    def f(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    for i, j in pairs:
        a, b = f(i), f(j)
        if a != b: par[max(a, b)] = min(a, b)
    root = np.array([f(i) for i in range(n)]); u, can = np.unique(root, return_inverse=True)
    return can.reshape(-1), len(u)


def cloth_edges(Tw, T, Vpat):
    """the welded mesh's edges, each with its length on the flat pattern (an edge along a seam is in both pieces:
    the two lengths, which differ where a seam is eased, averaged)"""
    acc = {}
    for t in range(len(Tw)):
        for k in range(3):
            a, b = Tw[t, k], Tw[t, (k + 1) % 3]; key = (min(a, b), max(a, b))
            L = float(np.linalg.norm(Vpat[T[t, k]] - Vpat[T[t, (k + 1) % 3]]))
            acc.setdefault(key, []).append(L)
    E = np.array(list(acc.keys())); R = np.array([np.mean(v) for v in acc.values()])
    return E, R


def relax(X, E, R, P, N, iters=500, smooth=(0.25, 0.03)):
    """the cloth eased to its pattern's lengths (no gravity), kept outside his body: a Jacobi position solve"""
    kd = mathutils.kdtree.KDTree(len(P))
    for i, p in enumerate(P): kd.insert(p, i)
    kd.balance()
    nb = np.zeros(len(X)); np.add.at(nb, E[:, 0], 1); np.add.at(nb, E[:, 1], 1)
    for it in range(iters):
        d = X[E[:, 1]] - X[E[:, 0]]; L = np.linalg.norm(d, axis=1) + 1e-12
        c = ((L - R) / L)[:, None] * d * 0.5
        acc = np.zeros_like(X); np.add.at(acc, E[:, 0], c); np.add.at(acc, E[:, 1], -c)
        X += 1.6 * acc / nb[:, None]
        # (smoothed hard at first, then lightly: Blender keeps whatever creases the cloth starts with as its own)
        sm = smooth[0] if it < iters * 0.6 else smooth[1]
        S = np.zeros_like(X); np.add.at(S, E[:, 0], X[E[:, 1]]); np.add.at(S, E[:, 1], X[E[:, 0]])
        X += sm * (S / nb[:, None] - X)
        if it % 8 == 0 or it == iters - 1:
            for i in range(len(X)):
                _, j, _ = kd.find(X[i]); dd = float(np.dot(X[i] - P[j], N[j]))
                if dd < 0.006: X[i] += N[j] * (0.006 - dd)
    d = X[E[:, 1]] - X[E[:, 0]]; st = np.linalg.norm(d, axis=1) / R
    return np.percentile(st, [5, 50, 95])


# ---- Blender ----
def new_obj(name, X, T, edges=()):
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(map(float, x)) for x in X], [tuple(map(int, e)) for e in edges], [tuple(map(int, t)) for t in T])
    me.update()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    return ob


def set_key(ob, name, X):
    kb = ob.shape_key_add(name=name, from_mix=False)
    kb.data.foreach_set("co", np.asarray(X, np.float32).ravel())
    return kb


def body_obj(body, poses, frames, name="dave"):
    """his body as a collider, its shape keys walking it from the first pose to the last at the given frames"""
    ob = new_obj(name, poses[0], body.idx)
    set_key(ob, "Basis", poses[0])
    keys = [set_key(ob, "p%d" % i, X) for i, X in enumerate(poses[1:], 1)]
    for i, kb in enumerate(keys):
        f0 = frames[i]; f1 = frames[i + 1]
        kb.value = 0.0; kb.keyframe_insert("value", frame=f0)
        kb.value = 1.0; kb.keyframe_insert("value", frame=f1)
        if i + 1 < len(keys):
            kb.keyframe_insert("value", frame=f1)
            kb.value = 0.0; kb.keyframe_insert("value", frame=frames[i + 2])
    for fc in (ob.data.shape_keys.animation_data.action.fcurves if keys else []):
        for kp in fc.keyframe_points: kp.interpolation = "LINEAR"
    ob.modifiers.new("collide", "COLLISION")
    ob.collision.thickness_outer = 0.003; ob.collision.thickness_inner = 0.02; ob.collision.cloth_friction = 8.0; ob.collision.damping = 0.1
    return ob


def static_collider(name, X, T, th=0.002):
    ob = new_obj(name, X, T)
    ob.modifiers.new("collide", "COLLISION")
    ob.collision.thickness_outer = th; ob.collision.thickness_inner = 0.006; ob.collision.cloth_friction = 6.0
    return ob


def cloth_obj(name, X, T, flat, sew, stiff=None, pins=None, mass=0.3, tension=15.0, bending=0.5, frames=100, grav=None):
    ob = new_obj(name, X, T, sew)
    fk = None
    if flat is not None:
        set_key(ob, "Basis", X); fk = set_key(ob, "flat", flat); fk.value = 0.0
    if stiff is not None and stiff.any():
        vg = ob.vertex_groups.new(name="stiff"); vg.add([int(i) for i in np.where(stiff > 0)[0]], 1.0, "REPLACE")
    if pins is not None and len(pins):
        vg = ob.vertex_groups.new(name="pin"); vg.add([int(i) for i in pins], 1.0, "REPLACE")
    cm = ob.modifiers.new("cloth", "CLOTH"); cs = cm.settings
    cs.quality = 10; cs.mass = mass; cs.air_damping = 1.0
    cs.tension_stiffness = tension; cs.compression_stiffness = tension; cs.shear_stiffness = tension * 0.3
    cs.bending_stiffness = bending; cs.tension_damping = 5; cs.compression_damping = 5; cs.shear_damping = 5; cs.bending_damping = 0.5
    if fk is not None: cs.rest_shape_key = fk
    if len(sew):
        cs.use_sewing_springs = True; cs.sewing_force_max = 20.0
    if stiff is not None and stiff.any():
        cs.vertex_group_bending = "stiff"; cs.bending_stiffness_max = bending * 40
    if pins is not None and len(pins):
        cs.vertex_group_mass = "pin"; cs.pin_stiffness = 5.0
    cc = cm.collision_settings
    cc.use_collision = True; cc.distance_min = 0.004; cc.collision_quality = 4
    cc.use_self_collision = bool(int(os.environ.get("GB_SELF", "1"))); cc.self_distance_min = 0.0035; cc.self_friction = 5.0
    cm.point_cache.frame_start = 1; cm.point_cache.frame_end = frames
    ew = cs.effector_weights
    for f, g in (grav or [(1, 1.0)]):
        ew.gravity = g; ew.keyframe_insert("gravity", frame=f)
    return ob


def positions(obs):
    dg = bpy.context.evaluated_depsgraph_get()
    out = []
    for ob in obs:
        ev = ob.evaluated_get(dg); m = ev.to_mesh()
        co = np.zeros(len(m.vertices) * 3, np.float32); m.vertices.foreach_get("co", co); ev.to_mesh_clear()
        out.append(co.reshape(-1, 3).astype(np.float64))
    return out


def run(frames, obs, label, snap=None, gravity=(0.0, -9.81, 0.0)):
    """steps the simulation; snap(frame, positions) is called at each frame in snap.at. (The page's frame has y up;
    Blender's gravity points down its z unless told otherwise.)"""
    sc = bpy.context.scene; sc.frame_start = 1; sc.frame_end = frames
    sc.gravity = gravity; sc.use_gravity = True
    import time
    t0 = time.time()
    for f in range(1, frames + 1):
        sc.frame_set(f)
        if snap and f in snap.at: snap(f, positions(obs))
        if f % 20 == 0 or f == frames: print("  %s frame %d/%d, %.0f s" % (label, f, frames, time.time() - t0), flush=True)
    return positions(obs)


def flat_layout(pieces):
    """each piece flat in one plane, side by side (only the lengths and angles inside a piece matter)"""
    out, x = [], 0.0
    for pc in pieces.values():
        V = pc.V - pc.V.min(0); out.append(np.c_[V[:, 0] + x, V[:, 1], np.zeros(len(V))]); x += V[:, 0].max() + 0.3
    return np.vstack(out)


def clear_scene():
    for ob in list(bpy.data.objects): bpy.data.objects.remove(ob, do_unlink=True)
    for me in list(bpy.data.meshes): bpy.data.meshes.remove(me)


def debug_json(path, body, P, meshes, lines=()):
    out = {"body": {"pos": b64(P.astype(np.float32)), "idx": b64(body.idx.astype(np.uint32))}, "meshes": [], "lines": b64(np.array(lines, np.float32).reshape(-1))}
    for nm, X, T, col in meshes:
        out["meshes"].append({"name": nm, "pos": b64(X.astype(np.float32)), "idx": b64(np.asarray(T, np.uint32)), "col": col})
    json.dump(out, open(path, "w"))


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--mh", default=os.path.expanduser("~/.cache/wardrobe-mh"))
    ap.add_argument("--out", default=os.path.join(ROOT, "data", "garments"))
    ap.add_argument("--only", default="")
    ap.add_argument("--frames", type=float, default=1.0)
    ap.add_argument("--debug", default="")
    a = ap.parse_args(argv)
    BB.fetch_assets(a.mh)
    body = Body(a.mh)
    # (the page scales the warped figure back up to his height: a template metre is this much of a real one)
    top = body.PW(np.array([[0, 1.79, 0.0]]), np.array([False]), body.hz)[0][1] if body.PW else 1.79
    scale = 1 / ((body.char.get("height", 183) / 183) * 1.79 / top)
    print("body ready: %d vertices, cloth scale %.4f" % (body.n, scale), flush=True)
    archs = [x for x in (a.only.split(",") if a.only else ["hoodie", "halfzip", "jacket"]) if x]
    for arch in archs:
        G = Garment(arch, scale)
        cnt = seam_counts(G.S, G.P)
        for pc in G.P.values(): mesh_piece(pc, cnt)
        print(arch, {k: len(v.V) for k, v in G.P.items()}, flush=True)
        X = place(G, G.P, body, 0)
        pairs, off = close_seams(G.P, X, G.S)
        P0 = body.apose[0]; N0 = vnormals(P0, body.idx)
        allX = np.vstack([X[k] for k in G.P]); T = np.vstack([G.P[k].T + off[k] for k in G.P])
        print("  pushed out", push_out(allX, P0, N0), "points", flush=True)
        if a.debug:
            gap = np.array([np.linalg.norm(allX[i] - allX[j]) for i, j in pairs])
            print("  sewing gaps: mean %.4f max %.4f" % (gap.mean(), gap.max()), flush=True)
            lines = [list(allX[i]) + list(allX[j]) for i, j in pairs]
            debug_json(os.path.join(a.debug, arch + "-placed.json"), body, P0, [(arch, allX, T, "#7a2a30")], lines)
        # one connected garment: seams welded, eased to the pattern's lengths round him
        can, nw = weld(len(allX), pairs)
        Xw = np.zeros((nw, 3)); np.add.at(Xw, can, allX); Xw /= np.bincount(can, minlength=nw)[:, None]
        Tw = can[T]
        Vpat = np.vstack([G.P[k].V for k in G.P])
        E, R = cloth_edges(Tw, T, Vpat)
        # where pieces are sewn together their corners should add up to a full turn (half a turn on an open edge)
        ang = np.zeros(nw); nfree = {}
        for t in range(len(T)):
            for k in range(3):
                p0, p1, p2 = Vpat[T[t, k]], Vpat[T[t, (k + 1) % 3]], Vpat[T[t, (k + 2) % 3]]
                u, v = p1 - p0, p2 - p0
                ang[Tw[t, k]] += math.degrees(math.acos(np.clip(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v) + 1e-15), -1, 1)))
        ecount = {}
        for t in range(len(Tw)):
            for k in range(3):
                key = tuple(sorted((Tw[t, k], Tw[t, (k + 1) % 3]))); ecount[key] = ecount.get(key, 0) + 1
        onb = np.zeros(nw, bool)
        for (i, j), c in ecount.items():
            if c == 1: onb[i] = onb[j] = True
        mult = np.bincount(can, minlength=nw)
        dev = np.where(onb, ang - 180, ang - 360)
        sew = mult > 1
        worst = np.argsort(-np.abs(dev * sew))[:4]
        if os.environ.get("GB_DBG"):
            names = [(k, i) for k in G.P for i in range(len(G.P[k].V))]
            for w in worst[:2]:
                orig = np.where(can == w)[0]
                print("   ", [(names[o][0], names[o][1], [e for e, ids in G.P[names[o][0]].B.items() if names[o][1] in ids]) for o in orig])
        print("  corners where pieces meet: " + ", ".join("%+.0f deg (%s at %.2f %.2f)" % (dev[w], "edge" if onb[w] else "inside", *Xw[w, :2]) for w in worst), flush=True)
        print("  welded: %d points, %d triangles, %d edges" % (nw, len(Tw), len(E)), flush=True)
        print("  eased to the pattern: edge/pattern 5%% %.3f, median %.3f, 95%% %.3f" % tuple(relax(Xw, E, R, P0, N0)), flush=True)
        if a.debug: debug_json(os.path.join(a.debug, arch + "-relaxed.json"), body, P0, [(arch, Xw, Tw, "#7a2a30")])
        # the drape under gravity, then his arms come down to his relaxed pose
        F = lambda f: max(2, int(round(f * a.frames)))
        step = F(14)
        poses = body.apose + [body.rel]
        pf = [F(24) + i * step for i in range(len(poses))]
        frames = pf[-1] + F(30)
        clear_scene()
        bo = body_obj(body, poses, pf)
        stw = np.zeros(nw); np.maximum.at(stw, can, np.concatenate([np.full(len(G.P[k].V), G.P[k].stiff) for k in G.P]))
        co = cloth_obj(arch, Xw, Tw, None, [], stiff=stw, frames=frames)

        def snap(f, X):
            if a.debug: debug_json(os.path.join(a.debug, "%s-f%03d.json" % (arch, f)), body, poses[max(0, min(len(poses) - 1, sum(1 for q in pf if q <= f) - 1))], [(arch, X[0], Tw, "#7a2a30")])
        snap.at = {pf[0], pf[2]}
        Xs, = run(frames, [co], arch, snap)
        st = np.linalg.norm(Xs[E[:, 0]] - Xs[E[:, 1]], axis=1) / R
        print("  draped: edge/pattern 5%% %.3f, median %.3f, 95%% %.3f" % tuple(np.percentile(st, [5, 50, 95])), flush=True)
        if a.debug:
            debug_json(os.path.join(a.debug, arch + "-draped.json"), body, body.rel, [(arch, Xs, Tw, "#7a2a30")])

main()
