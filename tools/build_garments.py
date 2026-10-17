"""Builds the garment templates (data/garments/<archetype>.json): flat pattern pieces sewn on Dave's body and draped
as cloth in headless Blender, then baked for the page.

What it does:
  1. Makes Dave's body as the page draws him with his saved shape (CHAR_DEF in page.html: the Edit Dave morphs of
     data/body.json and the proportions of propWarp), in his relaxed pose and in an A-pose (arms out at 40 degrees),
     with the same vertices, from the MakeHuman rig tools/build_body.py uses.
  2. Cuts each archetype's pattern pieces flat (front, back, sleeves, rib bands, hood halves, collar), in metres, from
     its measurements for size L (MEAS), and meshes them (constrained Delaunay, about 1.4 cm apart).
  3. Places the pieces round the A-posed body, welds the seams, eases the cloth to the pattern's lengths and drapes it
     under gravity, then lowers the arms to his relaxed pose while the cloth follows. A hood is draped on its own after the garment,
     its neckline held on the garment's, falling back from his head onto his shoulders.
  4. Bakes for the page: every point's position on him, its place on the flat pattern (the page's cloth keeps these
     lengths, so a size or a body can change and the cloth still has its cut, and stripes and checks run with the
     pattern), the piece it belongs to, and where it sits on his body (the nearest triangle, and the offset from it),
     so it moves with every Edit Dave change before the page settles the layers.

    python3 tools/build_garments.py [--only hoodie,halfzip,jacket] [--debug <dir>] [--frames 1.0]

The scarf (--only scarf, data/garments/scarf.json) is not sewn: a band 180 x 11 cm (a scarf folded along its length)
wound a turn and a half round his neck with both ends down his front (SCARF, SCARF_WRAP, scarf_path: the loop as far out
as he and the jumper are at each way round his neck, higher at the sides and dipping at the front onto his chest, the
ends leaving it at the sides of his neck and turning down over his collarbones, the upper edge of its first turn held
at the back of his neck as its grip on a collar holds it) over his body and the draped jumper (data/garments/jumper.json,
so build that first), then let fall. About 30 seconds. GB_SCARF_FWD=0.5 (and the rest of SCARF_WRAP) tries another
wrap.

Trousers (--only chinos,chinos_boot; MEAS entries with legs=1) are cut as a pair (Trousers: a front and a back panel for each leg,
sewn down both sides of each leg and up the front and the back, and a waistband), their inseam from his crotch to
3.5 cm off the floor, placed round his legs and hips (place_legs) and draped in his relaxed pose without his arms, the
waistband held where it is put; each point is bound to his body on its own side (bind). The page drapes them with
window.__legDrape on by default (UPGRADE_PLAN.md, section 5 item 6: straight trousers and jeans; chinos_boot, the same
ending 11 cm off the floor, over boots).

It runs itself inside Blender 4.5 LTS: BLENDER=<path to blender>, else ~/.cache/wardrobe-blender, where Blender is
downloaded from download.blender.org (and checked against its published sha256) on first use. The MakeHuman assets
come as in tools/build_body.py (--mh). --frames scales the simulation's length (0.3 for a quick look). --debug writes
each stage (placed, relaxed, mid-drape, draped) as JSON for tools/garment_view.js. GB_SELF=0 turns Blender's
self-collision off; GB_SNAPS=2,4,8 writes those frames too (with --debug); GB_DBG=1 prints the pieces behind the
worst corner in the corner check, and how far each row of the scarf round his neck is moved out and bent.

STATUS (12 Oct 2026, PR #36; see STATUS.md and UPGRADE_PLAN.md 2zzzzzzzzzzzzzzzzzz): the hoodie (with its hood), the
quarter-zip and the jacket drape cleanly and are written to data/garments; the page draws them with window.__drape set.
Options for trying drapes: --start (the A-pose placed in), --hold (frames settled at each pose), --bending, --mass,
--tension, --friction, --hood-bending, --apose-only (a quick look), --reuse (with --debug: the last draped garment, to
try the hood alone). It also runs as a plain script under Python with the bpy module (pip install bpy).
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
    # (download.blender.org refuses Python's own user agent)
    get = lambda u, **k: urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "wardrobe-build/1"}), **k)
    with get(base + BLENDER_TAR) as r, open(tar, "wb") as o:
        for b in iter(lambda: r.read(1 << 20), b""):
            o.write(b)
    sums = get(base + "blender-%s.sha256" % BLENDER_VER, timeout=60).read().decode()
    want = next(l.split()[0] for l in sums.splitlines() if l.strip().endswith(BLENDER_TAR))
    h = hashlib.sha256()
    with open(tar, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    if h.hexdigest() != want:
        os.remove(tar)
        sys.exit("Blender download does not match its sha256")
    with tarfile.open(tar) as t:
        t.extractall(cache, **({"filter": "tar"} if hasattr(tarfile, "tar_filter") else {}))
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
import mathutils.bvhtree
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
        # (the page warps the arm and the torso apart (propWarp), and his shoulder slope drops the arm's skin by up to
        # 1.7 cm more than the chest beside it: a torn ridge at the front of each armpit, which in the A-pose lies on
        # his chest and caught the cloth. Here the two are blended over a few centimetres of skin instead.)
        key = np.round(P0 * 4000).astype(np.int64); _, inv = np.unique(key, axis=0, return_inverse=True); inv = inv.reshape(-1)
        E = np.vstack([self.idx[:, [0, 1]], self.idx[:, [1, 2]], self.idx[:, [2, 0]]]); E = inv[E]
        nu = inv.max() + 1; wu = np.zeros(nu); np.maximum.at(wu, inv, am.astype(float))
        deg = np.bincount(E.ravel(), minlength=nu).astype(float)
        for _ in range(8):
            acc = np.zeros(nu); np.add.at(acc, E[:, 0], wu[E[:, 1]]); np.add.at(acc, E[:, 1], wu[E[:, 0]])
            wu = 0.5 * wu + 0.5 * acc / np.maximum(deg, 1)
        self.armW = sstep(0.0, 1.0, wu[inv])
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
        if not self.PW: return P.copy()
        n = len(P); w = self.armW[:, None]
        return w * self.PW(P, np.ones(n, bool), self.hz) + (1 - w) * self.PW(P, np.zeros(n, bool), self.hz)

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
    # the same jacket zipped up (its front one piece, the collar closed round his neck)
    "jacket_up": dict(chest=124, length=68, shoulder=49, armhole=25.5, neck_w=19, neck_f=7.5, neck_b=2.2, sh_drop=4.5, band=4,
                      band_k=0.93, sleeve=65, bicep=44, wrist=28, cuff=5, cuff_c=24, collar=6.5),
    # knits: a crew neck (a rib neckband standing 2.5 cm) and a roll neck (6 cm showing), a little closer than a
    # sweatshirt. (A roll neck cut to a 15 cm neckline with a 9 cm collar crumpled against his jaw and pulled a fold
    # down the front.)
    "jumper": dict(chest=116, length=68, shoulder=47, armhole=23.5, neck_w=17, neck_f=7, neck_b=2, sh_drop=4.5, band=5,
                   band_k=0.88, sleeve=64, bicep=38, wrist=25, cuff=6, cuff_c=19, collar=2.5),
    "rollneck": dict(chest=116, length=68, shoulder=47, armhole=23.5, neck_w=17, neck_f=5, neck_b=2, sh_drop=4.5, band=5,
                     band_k=0.88, sleeve=64, bicep=38, wrist=25, cuff=6, cuff_c=19, collar=6),   # (the roll as it shows, folded)
    # a tee: short sleeves open at the end (wrist: all round there), a plain hem, a 2 cm neckband
    "tee": dict(chest=108, length=72, shoulder=46, armhole=22, neck_w=17, neck_f=8, neck_b=2, sh_drop=4.5, band=0, band_k=1,
                sleeve=21, bicep=38, wrist=36, cuff=0, cuff_c=0, collar=2),
    # a long-sleeved tee: the tee's body and neckband, its sleeves to the wrist (a little narrower round the arm than
    # the short sleeve, tapering to the wrist) and finished in a narrow 3 cm rib cuff, as a long-sleeved tee is
    "tee_ls": dict(chest=108, length=72, shoulder=46, armhole=22, neck_w=17, neck_f=8, neck_b=2, sh_drop=4.5, band=0, band_k=1,
                   sleeve=64, bicep=36, wrist=23, cuff=3, cuff_c=19, collar=2),
    # a shirt: a point collar (a 3 cm stand and a 4.5 cm leaf folded down over it, 7 cm to its points), buttoned cuffs
    # a little narrower than the sleeve, a plain hem; worn open (its front in two, the collar open at the front) or done
    # up (the front one piece, the page draws its placket and buttons)
    "shirt": dict(chest=110, length=79, shoulder=47, armhole=24, neck_w=16, neck_f=7.5, neck_b=2, sh_drop=4.5, band=0, band_k=1,
                  sleeve=64, bicep=40, wrist=25, cuff=6.5, cuff_c=24, collar=3, leaf=4.5, point=7, open=1),
    "shirt_up": dict(chest=110, length=79, shoulder=47, armhole=24, neck_w=16, neck_f=7.5, neck_b=2, sh_drop=4.5, band=0, band_k=1,
                     sleeve=64, bicep=40, wrist=25, cuff=6.5, cuff_c=24, collar=3, leaf=4.5, point=7),
    # a short-sleeved shirt: the shirt's cut and point collar, a little shorter (it is worn out as often as in), its
    # sleeves to above the elbow, finished in a 2.5 cm turned-up band a little closer than the sleeve; worn open or done
    # up as the shirt is. (With a plain hem and no band, worn open, its leaf stood straight out from the stand at the back.
    # Done up, its shoulders slope half a centimetre more: with the open one's, it sat higher on him than the long
    # shirt does, and its collar showed above a half-zip's stand at the sides of his neck, w20261008-quiet-04)
    "sshirt": dict(chest=110, length=76, shoulder=47, armhole=24, neck_w=16, neck_f=7.5, neck_b=2, sh_drop=4.5, band=0, band_k=1,
                   sleeve=24, bicep=41, wrist=37, cuff=2.5, cuff_c=36, collar=3, leaf=4.5, point=7, open=1),
    "sshirt_up": dict(chest=110, length=76, shoulder=47, armhole=24, neck_w=16, neck_f=7.5, neck_b=2, sh_drop=5, band=0, band_k=1,
                      sleeve=24, bicep=41, wrist=37, cuff=2.5, cuff_c=36, collar=3, leaf=4.5, point=7),
    # a resort shirt (a camp, Cuban or revere collar): the short-sleeved shirt's cut a little boxier (116 cm round the
    # chest) with a straight hem, its collar a 2.5 cm stand under a 5 cm leaf, 8 cm to its points, that lies open. Worn
    # open, its front in two; done up, the neck cut in a 14 cm V (vneck) to the top button, the collar open in it. (On a
    # 1 cm stand, as a camp collar's, the leaf did not fold down: it crumpled at the back of his neck)
    "camp": dict(chest=116, length=74, shoulder=48, armhole=24, neck_w=16, neck_f=7.5, neck_b=2, sh_drop=4.5, band=0, band_k=1,
                 sleeve=24, bicep=43, wrist=39, cuff=2.5, cuff_c=38, collar=2.5, leaf=5, point=8, open=1),
    "camp_up": dict(chest=116, length=74, shoulder=48, armhole=24, neck_w=16, neck_f=14, neck_b=2, sh_drop=5, band=0, band_k=1,
                    sleeve=24, bicep=43, wrist=39, cuff=2.5, cuff_c=38, collar=2.5, leaf=5, point=8, vneck=1),
    # a polo: the tee's body, a little higher at the front of the neck, short sleeves finished in a 2.5 cm rib armband a
    # little closer than the sleeve, and a knitted collar (a 2 cm stand and a 4.5 cm leaf folded down over it, 6.5 cm to its
    # points) closed round his neck; the page draws its placket and buttons
    "polo": dict(chest=108, length=72, shoulder=46, armhole=22, neck_w=17, neck_f=7.5, neck_b=2, sh_drop=4.5, band=0, band_k=1,
                 sleeve=23, bicep=38, wrist=35, cuff=2.5, cuff_c=33, collar=2, leaf=4.5, point=6.5),
    # a long-sleeved polo: the polo's body and knitted collar, its sleeves to the wrist (a little narrower round the arm,
    # tapering) finished in a 5 cm rib cuff, as the long-sleeved tee's
    "polo_ls": dict(chest=108, length=72, shoulder=46, armhole=22, neck_w=17, neck_f=7.5, neck_b=2, sh_drop=4.5, band=0, band_k=1,
                    sleeve=64, bicep=36, wrist=23, cuff=5, cuff_c=19, collar=2, leaf=4.5, point=6.5),
    # a vest (a tank top): the tee's body a little closer, no sleeves (no sleeve key), 5 cm straps either side of a wide
    # scooped neckline, 14 cm deep at the front and 6 at the back, and deep armholes. (Its 1.5 cm binding cut as the
    # tee's neckband, a stand, stood up off the scoop and pulled it into a shallow V at his throat: left out, the edge as
    # turned and stitched)
    "vest": dict(chest=100, length=72, shoulder=29, armhole=27, neck_w=19, neck_f=14, neck_b=6, sh_drop=2.5, band=0, band_k=1),
    # a sleeveless tee (a vest top, a training or muscle tank with a crew neck): the tee's body and 2 cm neckband, no
    # sleeves (no sleeve key), its armholes cut in to a 42 cm shoulder and deep (25 cm), as the shop photos'. Its neckline
    # is 1.5 cm higher at the front than the tee's: cut like the tee's, with no sleeves to carry it, its front hung from
    # the neckband and dipped into a V at his throat, deeper than the tee's
    "vest_tee": dict(chest=106, length=72, shoulder=42, armhole=25, neck_w=17, neck_f=6.5, neck_b=2, sh_drop=4, band=0, band_k=1,
                     collar=2),
    # a mock-neck tee: the long-sleeved tee's body, sleeves and cuffs, its neckline a little higher at the front (5 cm, as
    # the roll neck's) and a 3.5 cm band standing round his neck instead of a neckband
    "tee_mock": dict(chest=108, length=72, shoulder=46, armhole=22, neck_w=16.5, neck_f=5, neck_b=2, sh_drop=4.5, band=0, band_k=1,
                     sleeve=64, bicep=36, wrist=23, cuff=3, cuff_c=19, collar=3.5),
    # a knitted vest (a sweater vest, a slipover): the jumper's knit a little closer, no sleeves (no sleeve key), its
    # armholes cut in and deep, a V neck 14 cm deep at the front (vneck), and the jumper's 5 cm rib hem band; the page lays
    # the rib round the V. (Cut 20 cm deep, the V showed his chest where the vest is worn with nothing under it)
    "kvest": dict(chest=110, length=66, shoulder=36, armhole=26, neck_w=18, neck_f=14, neck_b=2.5, sh_drop=4.5, band=5,
                  band_k=0.9, vneck=1),
    # a V-neck jumper: the jumper's knit, sleeves, rib cuffs and hem band, its neck cut in a V 14 cm deep (vneck) with no
    # collar sewn on: the page lays a rib round the V, as on the knitted vest (a stand on a V stands up off it)
    "jumper_v": dict(chest=116, length=68, shoulder=47, armhole=23.5, neck_w=17, neck_f=14, neck_b=2, sh_drop=4.5, band=5,
                     band_k=0.88, sleeve=64, bicep=38, wrist=25, cuff=6, cuff_c=19, vneck=1),
    # a cardigan: the V-neck jumper's knit a little roomier (118 round the chest, for a shirt or a polo under it) and
    # longer (70 cm), its V deeper (22 cm, to the top button at the middle of his chest) and its hem band less gathered;
    # worn open (its front in two) or buttoned (the front one piece). The page lays the rib up its fronts and round the V,
    # and draws its buttons
    "cardigan": dict(chest=118, length=70, shoulder=47, armhole=24, neck_w=17.5, neck_f=22, neck_b=2, sh_drop=4.5, band=5,
                     band_k=0.92, sleeve=64, bicep=39, wrist=25, cuff=6, cuff_c=19, vneck=1, open=1),
    "cardigan_up": dict(chest=118, length=70, shoulder=47, armhole=24, neck_w=17.5, neck_f=22, neck_b=2, sh_drop=4.5, band=5,
                        band_k=0.92, sleeve=64, bicep=39, wrist=25, cuff=6, cuff_c=19, vneck=1),
    # a padded or puffer jacket: the track jacket's cut with a padded jacket's room (132 cm round the chest, 8 more than
    # the track jacket, so it goes over a sweatshirt or a quarter-zip with its padding; sleeves 48 cm round the bicep),
    # a taller stand collar, a narrow elastic hem and elastic cuffs; worn open (its front in two) or zipped up
    "puffer": dict(chest=132, length=69, shoulder=50, armhole=27, neck_w=20, neck_f=7.5, neck_b=2.2, sh_drop=4.5, band=3,
                   band_k=0.92, sleeve=66, bicep=48, wrist=30, cuff=4, cuff_c=23, collar=7.5, pad=0.15, open=1),
    "puffer_up": dict(chest=132, length=69, shoulder=50, armhole=27, neck_w=20, neck_f=7.5, neck_b=2.2, sh_drop=4.5, band=3,
                      band_k=0.92, sleeve=66, bicep=48, wrist=30, cuff=4, cuff_c=23, collar=7.5, pad=0.15),
    # a hooded zip jacket (a shell, windbreaker, softshell or hooded fleece): the track jacket's cut with no collar, its
    # hood sewn into the neckline, a little bigger than a hoodie's (it goes over a cap, and over a hoodie's hood when
    # it is up); worn open (its front in two) or zipped up
    "jacket_hood": dict(chest=124, length=69, shoulder=49, armhole=25.5, neck_w=19.5, neck_f=7, neck_b=2.2, sh_drop=4.5, band=3,
                        band_k=0.95, sleeve=65, bicep=44, wrist=28, cuff=4, cuff_c=24, hood_h=37, hood_d=27, open=1),
    "jacket_hood_up": dict(chest=124, length=69, shoulder=49, armhole=25.5, neck_w=19.5, neck_f=7, neck_b=2.2, sh_drop=4.5,
                           band=3, band_k=0.95, sleeve=65, bicep=44, wrist=28, cuff=4, cuff_c=24, hood_h=37, hood_d=27),
    # a collared zip jacket (a Harrington, a coach or a Capitol jacket): the track jacket's cut a little shorter, a rib hem,
    # and a shirt's collar a size up (a 3 cm stand and a 5 cm leaf folded down over it, 7.5 cm to its points); worn open
    # (its front in two, the collar open at the front) or zipped up
    "jacket_coll": dict(chest=124, length=66, shoulder=49, armhole=25.5, neck_w=18.5, neck_f=7.5, neck_b=2.2, sh_drop=4.5, band=4.5,
                        band_k=0.9, sleeve=65, bicep=43, wrist=27, cuff=5, cuff_c=22, collar=3, leaf=5, point=7.5, open=1),
    "jacket_coll_up": dict(chest=124, length=66, shoulder=49, armhole=25.5, neck_w=18.5, neck_f=7.5, neck_b=2.2, sh_drop=4.5,
                           band=4.5, band_k=0.9, sleeve=65, bicep=43, wrist=27, cuff=5, cuff_c=22, collar=3, leaf=5, point=7.5),
    # a hooded padded jacket: the padded jacket's cut and room with no stand collar, its hood sewn into the neckline
    # (bigger again, for its padding: 38 cm high, 28 deep), padded as the rest; worn open or zipped up. Its neckline is a
    # centimetre narrower than the padded jacket's: with no stand collar to hold it, worn open the padded fronts slid off
    # his shoulders and the whole jacket fell down his arms
    "puffer_hood": dict(chest=132, length=70, shoulder=50, armhole=27, neck_w=19, neck_f=7.5, neck_b=2.2, sh_drop=4.5, band=3,
                        band_k=0.92, sleeve=66, bicep=48, wrist=30, cuff=4, cuff_c=23, hood_h=38, hood_d=28, pad=0.15, open=1),
    "puffer_hood_up": dict(chest=132, length=70, shoulder=50, armhole=27, neck_w=19, neck_f=7.5, neck_b=2.2, sh_drop=4.5, band=3,
                           band_k=0.92, sleeve=66, bicep=48, wrist=30, cuff=4, cuff_c=23, hood_h=38, hood_d=28, pad=0.15),
    # a parka: a hooded zip jacket cut long, to his upper thighs (78 cm), roomier (128 cm round the chest) for what
    # goes under it, a plain hem (a drawcord, not a rib) and its hood a size up again; worn open or zipped up
    "parka": dict(chest=128, length=78, shoulder=50, armhole=26.5, neck_w=19, neck_f=7.5, neck_b=2.2, sh_drop=4.5, band=3,
                  band_k=0.98, sleeve=66, bicep=46, wrist=29, cuff=4, cuff_c=24, hood_h=38, hood_d=28, open=1),
    "parka_up": dict(chest=128, length=78, shoulder=50, armhole=26.5, neck_w=19, neck_f=7.5, neck_b=2.2, sh_drop=4.5, band=3,
                     band_k=0.98, sleeve=66, bicep=46, wrist=29, cuff=4, cuff_c=24, hood_h=38, hood_d=28),
    # a chore jacket (a chore, utility, field or work jacket in canvas or twill): boxy, cut to below his hips (72 cm), 122
    # round the chest, a plain hem, buttoned cuffs and the collared jacket's shirt collar; worn open or buttoned (the
    # page draws its buttons and pockets)
    "chore": dict(chest=122, length=72, shoulder=49, armhole=25.5, neck_w=18.5, neck_f=7.5, neck_b=2.2, sh_drop=4.5, band=0,
                  band_k=1, sleeve=65, bicep=43, wrist=28, cuff=5, cuff_c=25, collar=3, leaf=5, point=7.5, open=1),
    "chore_up": dict(chest=122, length=72, shoulder=49, armhole=25.5, neck_w=18.5, neck_f=7.5, neck_b=2.2, sh_drop=4.5,
                     band=0, band_k=1, sleeve=65, bicep=43, wrist=28, cuff=5, cuff_c=25, collar=3, leaf=5, point=7.5),
    # a denim or trucker jacket: cut short, to his belt (64 cm), closer (118 round the chest), a 5 cm waistband buttoned
    # round him (stiff denim, barely drawn in), buttoned cuffs and the shirt collar a size up; worn open or buttoned
    "trucker": dict(chest=118, length=64, shoulder=48, armhole=25, neck_w=18.5, neck_f=7.5, neck_b=2.2, sh_drop=4.5, band=5,
                    band_k=0.96, sleeve=65, bicep=42, wrist=27, cuff=5, cuff_c=24, collar=3, leaf=5, point=7.5, open=1),
    "trucker_up": dict(chest=118, length=64, shoulder=48, armhole=25, neck_w=18.5, neck_f=7.5, neck_b=2.2, sh_drop=4.5, band=5,
                       band_k=0.96, sleeve=65, bicep=42, wrist=27, cuff=5, cuff_c=24, collar=3, leaf=5, point=7.5),
    # a bomber jacket: the track jacket's cut a little roomier and shorter (122 round the chest, 64 cm), gathered into
    # a 6 cm rib hem band and 6 cm rib cuffs, a 4.5 cm rib collar standing round his neck; worn open or zipped up
    "bomber": dict(chest=122, length=64, shoulder=49, armhole=25.5, neck_w=19, neck_f=7.5, neck_b=2.2, sh_drop=4.5, band=6,
                   band_k=0.86, sleeve=65, bicep=44, wrist=27, cuff=6, cuff_c=20, collar=4.5, open=1),
    "bomber_up": dict(chest=122, length=64, shoulder=49, armhole=25.5, neck_w=19, neck_f=7.5, neck_b=2.2, sh_drop=4.5, band=6,
                      band_k=0.86, sleeve=65, bicep=44, wrist=27, cuff=6, cuff_c=20, collar=4.5),
    # a blazer (a suit jacket, a sport coat): a tailored jacket cut to cover his seat (76 cm), closer than a zip jacket (114
    # round the chest, for a shirt or a fine knit under it), squarer shoulders (it is padded there), sleeves with a plain
    # hem that shows the shirt's cuff, and a shawl collar: a stand round the neckline (lapel_stand), which is cut in
    # a V down to the top button at his waist (vneck, 44 cm from his shoulder), and the collar and lapels in one piece
    # folded back over it (lapel_leaf: 4.5 cm deep round the back of his neck, 8.5 across his chest, narrowing to the
    # button). Worn open (its front in two) or buttoned (the front one piece, open above the button in the V). (With
    # sleeves 38 cm round the arm, slimmer than a half-zip's, the half-zip under it showed at the back of the armholes)
    "blazer": dict(chest=114, length=76, shoulder=47, armhole=25, neck_w=18, neck_f=44, neck_b=2.2, sh_drop=3.5, band=0, band_k=1,
                   sleeve=64, bicep=41, wrist=29, cuff=0, cuff_c=0, collar=3, leaf=4.5, lapel=8.5, vneck=1, open=1),
    "blazer_up": dict(chest=114, length=76, shoulder=47, armhole=25, neck_w=18, neck_f=44, neck_b=2.2, sh_drop=3.5, band=0, band_k=1,
                      sleeve=64, bicep=41, wrist=29, cuff=0, cuff_c=0, collar=3, leaf=4.5, lapel=8.5, vneck=1),
    # an overcoat (a wool or wool-look coat, a longline coat): the blazer's shawl collar on a coat cut to his knees (104
    # cm), roomier (128 round the chest, 45 round the arm) for a jumper, a hoodie or a suit jacket under it, the V to a top
    # button higher on his chest (36 cm) and the lapels wider (10 cm); worn open or buttoned
    "overcoat": dict(chest=128, length=104, shoulder=50, armhole=27, neck_w=19.5, neck_f=36, neck_b=2.4, sh_drop=3.5, band=0, band_k=1,
                     sleeve=66, bicep=45, wrist=31, cuff=0, cuff_c=0, collar=3.5, leaf=5, lapel=10, vneck=1, open=1),
    "overcoat_up": dict(chest=128, length=104, shoulder=50, armhole=27, neck_w=19.5, neck_f=36, neck_b=2.4, sh_drop=3.5, band=0, band_k=1,
                        sleeve=66, bicep=45, wrist=31, cuff=0, cuff_c=0, collar=3.5, leaf=5, lapel=10, vneck=1),
    # a car coat (a mac): the overcoat's room cut a little shorter (96 cm), with a shirt collar a size up again (a 3.5 cm
    # stand and a 5.5 cm leaf, 8 cm to its points), buttoned to the neck under a fly front; worn open or done up
    "carcoat": dict(chest=126, length=96, shoulder=50, armhole=26.5, neck_w=19.5, neck_f=8, neck_b=2.4, sh_drop=4, band=0, band_k=1,
                    sleeve=66, bicep=45, wrist=31, cuff=0, cuff_c=0, collar=3.5, leaf=5.5, point=8, open=1),
    "carcoat_up": dict(chest=126, length=96, shoulder=50, armhole=26.5, neck_w=19.5, neck_f=8, neck_b=2.4, sh_drop=4, band=0, band_k=1,
                       sleeve=66, bicep=45, wrist=31, cuff=0, cuff_c=0, collar=3.5, leaf=5.5, point=8),
    # a gilet (a bodywarmer) done up: no sleeves (no sleeve key), its armholes cut deeper and in to the point of his
    # shoulder so a jumper's or a hoodie's sleeve comes through, a plain hem and the jacket's stand collar, zipped
    "gilet": dict(chest=124, length=69, shoulder=43, armhole=27, neck_w=19, neck_f=7.5, neck_b=2.2, sh_drop=4.5, band=3, band_k=0.92,
                  collar=6.5),
    # a hooded gilet: the gilet's cut with no stand collar, the hooded padded jacket's hood sewn into a neckline a little
    # wider and lower at the front, as a hoodie's (it is always done up, so nothing slides off his shoulders), zipped.
    # (Cut to the gilet's neckline, a shirt's collar under it came through the hood's front either side of his neck)
    "gilet_hood": dict(chest=124, length=69, shoulder=43, armhole=27, neck_w=20, neck_f=9, neck_b=2.2, sh_drop=4.5, band=3,
                       band_k=0.92, hood_h=38, hood_d=28),
    # an aviator (a flying jacket, faux leather or suede with a shearling collar): the collared jacket's cut, a 5 cm
    # waistband barely drawn in, and a big collar, a 4 cm stand under a 8 cm leaf, 11 cm to its points, that lies out
    # over his shoulders (the page draws it in the shearling's colour); worn open or zipped up
    "aviator": dict(chest=124, length=66, shoulder=49, armhole=25.5, neck_w=19, neck_f=7.5, neck_b=2.2, sh_drop=4.5, band=5,
                    band_k=0.96, sleeve=65, bicep=44, wrist=28, cuff=5, cuff_c=24, collar=4, leaf=8, point=11, open=1),
    "aviator_up": dict(chest=124, length=66, shoulder=49, armhole=25.5, neck_w=19, neck_f=7.5, neck_b=2.2, sh_drop=4.5, band=5,
                       band_k=0.96, sleeve=65, bicep=44, wrist=28, cuff=5, cuff_c=24, collar=4, leaf=8, point=11),
    # trousers (legs=1), for a 34 in waist: waist (the waistband all round), seat (the panels all round at the seat
    # line), knee and hem (each leg all round), wb (waistband height), rise (from the crotch up to the waistband's top
    # at the front, straight up his body). Their lengths come from his own body (Trousers): the crotch from his skin,
    # the hem 3.5 cm off the floor. A straight chino: the waistband on his hips where make3Dcore's trousers sit (a rise
    # of 26 put it at his navel, 10 cm above them), a little room at the seat, straight from the knee to the hem.
    "chinos": dict(legs=1, waist=87, seat=100, knee=46, hem=41, wb=4, rise=16, length=100),
    # the same chino cut to end 11 cm off the floor (hem_y), for over boots: its hem rests on the boot's front, so the
    # toe, the laces and the start of the shaft show, as make3Dcore's trousers stop on a boot (9 to 12 cm up)
    "chinos_boot": dict(legs=1, waist=87, seat=100, knee=46, hem=41, wb=4, rise=16, length=100, hem_y=11),
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

    def __init__(self, name, grp, edges, stiff=0.0, band=0.0):
        self.name, self.grp, self.edges, self.stiff, self.band = name, grp, edges, stiff, band
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
    side = seg((hw, hb), (hw, yua), 12)
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
    if kind == "front" and M.get("vneck"):
        # (a V neck: from the shoulder straight down and in to its point, a little full at the top)
        nk = bez((nw, L), np.array((nw, L)) + nperp * 0.02 * s, (nw * 0.3, L - nd * 0.7), (0, L - nd))
    elif kind == "front":
        nk = bez((nw, L), np.array((nw, L)) + nperp * k1, (nw * 0.5, L - nd), (0, L - nd))
    else:
        nk = bez((nw, L), np.array((nw, L)) + nperp * k1, (nw * 0.45, L - nd), (0, L - nd))
    mir = lambda P: P[::-1] * np.array([-1, 1])
    # the hem band: a rib of its own, narrower than the body (band_k), the body gathered into it all round. (Stepped in
    # at the side seams instead, the cloth stood up in a cone at each hip.)
    bw = hw * bk
    if split:
        cf = seg((0, L - nd), (0, hb), 20)
        p = Piece(kind + "_p", 0, [("hem", seg((0, hb), (hw, hb), 10)), ("side_p", side), ("arm_p", arm), ("sh_p", sh), ("neck_p", nk), ("cf_p", cf)])
        n = mirror(p, kind + "_n")
        if not hb: return [p, n]
        bp = Piece(kind + "_p_band", 0, [("bot", seg((0, 0), (bw, 0), 10)), ("side_p", seg((bw, 0), (bw, hb), 4)), ("top", seg((bw, hb), (0, hb), 10)),
                                          ("cf_p", seg((0, hb), (0, 0), 4))], band=bk)
        return [p, n, bp, mirror(bp, kind + "_n_band")]
    body = Piece(kind, 0, [("hem", seg((-hw, hb), (hw, hb), 20)), ("side_p", side), ("arm_p", arm), ("sh_p", sh), ("neck_p", nk), ("neck_n", mir(nk)),
                           ("sh_n", mir(sh)), ("arm_n", mir(arm)), ("side_n", mir(side))])
    if not hb: return [body]
    return [body,
            Piece(kind + "_band", 0, [("bot", seg((-bw, 0), (bw, 0), 20)), ("side_p", seg((bw, 0), (bw, hb), 4)), ("top", seg((bw, hb), (-bw, hb), 20)),
                                      ("side_n", seg((-bw, hb), (-bw, 0), 4))], band=bk)]


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
    under = seg((wr, ch), (bc, yb), 20)
    mir = lambda P: P[::-1] * np.array([-1, 1])
    sd = "_L" if grp == 1 else "_R"
    # (the cuff a rib of its own, the sleeve gathered into it, as the hem band is)
    cuff = Piece("cuff" + sd, grp, [("bot", seg((-cc, 0), (cc, 0), 8)), ("under_p", seg((cc, 0), (cc, ch), 4)), ("top", seg((cc, ch), (-cc, ch), 8)),
                                    ("under_n", seg((-cc, ch), (-cc, 0), 4))], band=cc / wr) if ch else None
    return Piece("sleeve" + sd, grp, [("wrist", seg((-wr, ch), (wr, ch), 8)), ("under_p", under), ("cap_p", capp),
                 ("cap_n", mir(capp)), ("under_n", mir(under))]), cuff, yb, cap


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


def leaf(M, s, length):
    """A shirt collar's leaf, sewn along the top of the stand and folded down over it. Cut as a ring's part (the band a
    cone's surface lies flat as): its outer edge longer than its neck edge in proportion to how far it falls, so folded
    down it lies on his shoulders rather than standing off them; deeper toward the front, to its points. pc.fold keeps
    the ring's radius and angle, for placing it folded (close_seams)."""
    h, hp = M["leaf"] / 100 * s, M["point"] / 100 * s
    L0 = length
    # (the outer edge 8% longer, as a shirt collar's is: folded down it then reaches round the base of his neck. At 14%
    # it rippled along the back)
    phi = 0.08 * L0 / h; r0 = L0 / phi
    at = lambda th, d: np.array([(r0 + d) * math.sin(th), (r0 + d) * math.cos(th) - r0])
    e = phi / 2
    neck = np.array([at(t, 0) for t in np.linspace(-e, e, 30)])
    dep = lambda t: h + (hp - h) * sstep(0.45, 1.0, abs(t) / e)
    out = np.array([at(t, dep(t)) for t in np.linspace(e, -e, 30)])
    pc = Piece("leaf", 4, [("neck", neck), ("end_p", seg(at(e, 0), out[0], 6)), ("out", out), ("end_n", seg(out[-1], at(-e, 0), 6))], stiff=1.0)
    pc.fold = {"r0": r0, "phi": phi}
    return pc


def lapel_stand(M, s, rl, closed):
    """A tailored jacket's collar stand (a blazer's): sewn round the whole neckline, a V down to the top button, its full
    height round the back of his neck and narrowing down each side of the V to almost nothing at the button, so the roll
    line along its top runs from inside his neck to the button, as a lapel's does. rl: the neckline's four parts (the V
    on his left, the back to the middle, the back on, the V on his right). Placed carried on from the panel it is sewn to
    (close_seams): up at the back of his neck, in across his chest down the V, where it lies as the lapel's underside."""
    h, h0 = M["collar"] / 100 * s, 0.005 * s
    L = sum(rl); x0 = -L / 2; cum = np.r_[0, np.cumsum(rl)]
    hgt = lambda x: float(np.interp(x - x0, [0, cum[1], cum[3], cum[4]], [h0, h, h, h0]))
    xs = np.linspace(L / 2, -L / 2, 121)
    top = np.array([(x, hgt(x)) for x in xs])
    ends = ("cf_p", "cf_n") if closed else ("end_p", "end_n")
    pc = Piece("collar", 4, [("neck", seg((-L / 2, 0), (L / 2, 0), 30)), (ends[0], seg((L / 2, 0), (L / 2, h0), 2)), ("top", top),
                             (ends[1], seg((-L / 2, h0), (-L / 2, 0), 2))], stiff=1.0)
    pc.roll = True
    return pc


def lapel_leaf(M, s, top, xh):
    """A tailored jacket's collar and lapels in one (a shawl collar): sewn along the top of lapel_stand and folded back
    over it. Round the back of his neck it is a shirt collar's leaf (cut as a ring's part, its outer edge 8% longer, so
    it lies on his shoulders); down the V it is cut straight, as a lapel lies flat on his chest, widening from the
    collar's depth (leaf) to the lapel's (lapel) a third of the way down and narrowing to 1.5 cm at the button. top: the
    stand's top edge it is sewn to (his left first), xh: the x of the high points of his shoulders on it. pc.lapel keeps
    its neck edge, for placing it folded (close_seams)."""
    h, hl, he = M["leaf"] / 100 * s, M["lapel"] / 100 * s, 0.015 * s
    tp = top[::-1]; cl = np.r_[0, np.cumsum(np.linalg.norm(np.diff(tp, axis=0), axis=1))]
    s1, s2 = (float(np.interp(x, tp[:, 0], cl)) for x in xh); L0 = cl[-1]
    r0 = h / 0.08; eb = (s2 - s1) / 2 / r0; Lv = (s1 + L0 - s2) / 2
    # the neck edge: the arc round the back, then straight on along its ends for the V (dense, with its normals)
    t = np.linspace(-eb, eb, 200)
    arc = np.stack([r0 * np.sin(t), r0 * np.cos(t) - r0], 1); an = np.stack([np.sin(t), np.cos(t)], 1)
    tr = np.array([math.cos(eb), -math.sin(eb)]); nr = np.array([math.sin(eb), math.cos(eb)])
    u = np.linspace(0, Lv, 400)[1:]
    right = arc[-1] + u[:, None] * tr; left = (arc[0] + u[:, None] * (tr * [-1, 1]))[::-1]
    nk = np.vstack([left, arc, right]); nn = np.vstack([np.tile(nr * [-1, 1], (len(left), 1)), an, np.tile(nr, (len(right), 1))])
    sl = np.r_[0, np.cumsum(np.linalg.norm(np.diff(nk, axis=0), axis=1))]
    # its depth from the neck edge: down the V (v from the shoulder to the button) widening, then narrowing
    v = np.clip(np.maximum(s1 - sl, sl - s2) / Lv, 0, 1)
    dep = np.where(v < 0.3, h + (hl - h) * sstep(0.0, 0.3, v), hl + (he - hl) * sstep(0.3, 1.0, v))
    out = nk + nn * dep[:, None]
    k = np.linspace(0, len(nk) - 1, 61).astype(int)
    pc = Piece("leaf", 4, [("neck", resample(nk, 61)), ("end_p", seg(nk[-1], out[-1], 3)), ("out", out[k][::-1]),
                           ("end_n", seg(out[0], nk[0], 3))], stiff=1.0)
    pc.lapel = (nk, sl)
    return pc


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
    def nm2(nm):   # (an edge on the piece's x > 0 side is now on its x < 0 side)
        return nm[:-2] + {"_p": "_n", "_n": "_p"}[nm[-2:]] if nm[-2:] in ("_p", "_n") and nm.startswith(("side", "cf", "neck", "sh", "arm")) else nm
    return Piece(name, pc.grp, [(nm2(nm) if pc.grp == 0 else nm, P[::-1] * np.array([-1, 1])) for nm, P in pc.edges[::-1]], pc.stiff, pc.band)


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
        # (a gilet has none: its armholes are left open)
        slv, cu, self.yb, self.cap = "sleeve" in M, None, None, None
        if slv:
            arm_len = plen(P[fp].edge("arm_p")) + plen(P["back"].edge("arm_n"))
            # (his left sleeve is the right one turned over, as a pattern piece is cut twice from folded cloth: every piece
            # then faces outward on him. Wrapped round his left arm unturned it faced inward, and Blender's bending, which
            # measures the angle between neighbouring triangles by the way they face, fought a half turn all round that
            # armhole, leaving a rippled ridge along its seam.)
            sl, cu, self.yb, self.cap = sleeve(M, s, arm_len, 2)
            sl1, cu1, _, _ = sleeve(M, s, arm_len, 1)
            P["sleeve_L"] = mirror(sl1, "sleeve_L"); P["sleeve_R"] = sl
            if cu: P["cuff_L"] = mirror(cu1, "cuff_L"); P["cuff_R"] = cu
        bands = [k for k in P if k.endswith("_band")]
        # seams: [(piece, edge), ...] on one side against the other, sampled alike, and whether the two sides run the
        # same way along the seam (each piece's outline runs counter-clockwise seen from outside, so two pieces sewn
        # edge to edge run opposite ways). bias: how much of the closing
        # move the first side takes (1: it moves onto the second).
        S = [([(fp, "sh_p")], [("back", "sh_n")], 0.5, False), ([(fn, "sh_n")], [("back", "sh_p")], 0.5, False),
             ([(fp, "side_p")], [("back", "side_n")], 0.5, False), ([(fn, "side_n")], [("back", "side_p")], 0.5, False)]
        if slv:
            S += [([("sleeve_L", "cap_p")], [(fp, "arm_p")], 0.85, False), ([("sleeve_L", "cap_n")], [("back", "arm_n")], 0.85, False),
                  ([("sleeve_R", "cap_p")], [(fn, "arm_n")], 0.85, False), ([("sleeve_R", "cap_n")], [("back", "arm_p")], 0.85, False),
                  ([("sleeve_L", "under_p")], [("sleeve_L", "under_n")], 0.5, False), ([("sleeve_R", "under_p")], [("sleeve_R", "under_n")], 0.5, False)]
        if cu:
            S += [([("cuff_L", "top")], [("sleeve_L", "wrist")], 1.0, False), ([("cuff_R", "top")], [("sleeve_R", "wrist")], 1.0, False),
                  ([("cuff_L", "under_p")], [("cuff_L", "under_n")], 0.5, False), ([("cuff_R", "under_p")], [("cuff_R", "under_n")], 0.5, False)]
        # the hem bands: each on its body piece's hem, and to each other at the sides (and the open front's not at all)
        for b in bands:
            S.append(([(b, "top")], [(b[:-5], "hem")], 1.0, False))
        if bands:
            S += [([(fp + "_band", "side_p")], [("back_band", "side_n")], 0.5, False), ([(fn + "_band", "side_n")], [("back_band", "side_p")], 0.5, False)]
        # the neckline round from the middle of the front, by his left, the back and his right, against the way the
        # front and back run (so a collar along it faces outward)
        ring = [(fp, "neck_p"), ("back", "neck_n"), ("back", "neck_p"), (fn, "neck_n")]
        self.ring = ring
        rl = [plen(P[a].edge(b)) for a, b in ring]
        if "collar" in M:
            c = lapel_stand(M, s, rl, closed=not op) if "lapel" in M else collar(M, s, sum(rl), closed=not op)
            # (its neckline cut into the same four parts)
            x0 = c.edge("neck")[0][0]; cum = np.r_[0, np.cumsum(rl)]
            parts = [seg((x0 + cum[i], 0), (x0 + cum[i + 1], 0), 8) for i in range(4)]
            c.edges = [("n%d" % i, parts[i]) for i in range(4)] + [e for e in c.edges if e[0] != "neck"]
            c.order = [e[0] for e in c.edges]
            P["collar"] = c
            S.append(([("collar", "n%d" % i) for i in range(4)], ring, 1.0, False))
            if not op: S.append(([("collar", "cf_p")], [("collar", "cf_n")], 0.5, False))
            if "leaf" in M:
                # (the leaf along the stand's top but for 1.5 cm at each front end, where the stand buttons, folded down
                # over it: placed so in close_seams. Along all of it, the leaf's two ends met in one point at his throat)
                # (a lapel's ends come down to the button: only half a centimetre of its stand left bare there)
                tp = c.edge("top"); cl = np.r_[0, np.cumsum(np.linalg.norm(np.diff(tp, axis=0), axis=1))]; g = (0.005 if "lapel" in M else 0.015) * s
                # (a lapel stand's top bends where it narrows down the V: cut finer, so the bend is kept)
                nt = 240 if "lapel" in M else 12
                cut = lambda a0, a1, n=12: resample(np.array([[np.interp(t, cl, tp[:, 0]), np.interp(t, cl, tp[:, 1])] for t in np.linspace(a0, a1, n)]), n)
                parts = [("top_p", cut(0, g)), ("top", cut(g, cl[-1] - g, nt)), ("top_n", cut(cl[-1] - g, cl[-1]))]
                i = [e[0] for e in c.edges].index("top"); c.edges = c.edges[:i] + parts + c.edges[i + 1:]; c.order = [e[0] for e in c.edges]
                P["leaf"] = lapel_leaf(M, s, c.edge("top"), (x0 + cum[1], x0 + cum[3])) if "lapel" in M else leaf(M, s, plen(c.edge("top")))
                S.append(([("leaf", "neck")], [("collar", "top")], 1.0, False))
        # (a padded jacket's padding stiffens all of it: pad is the share of the collar's stiffness its other pieces get)
        for pc in P.values(): pc.stiff = max(pc.stiff, M.get("pad", 0.0))
        self.P, self.S = P, S
        self.hood = None
        if "hood_h" in M:
            hl = hood_half(M, s, rl[0], rl[1], "L")
            self.hood = {"hood_L": hl, "hood_R": mirror(hl, "hood_R")}
            self.hood_S = [([("hood_L", "back")], [("hood_R", "back")], 0.5, False)]
            # (each half's neckline on the garment's: his left from the front by the shoulder to the back, and his right)
            self.hood_ring = {"hood_L": [("neck_f", (fp, "neck_p")), ("neck_b", ("back", "neck_n"))],
                              "hood_R": [("neck_f", (fn, "neck_n")), ("neck_b", ("back", "neck_p"))]}


# ---- trousers: each leg a front and a back panel, the two legs sewn up the front and the back, a waistband ----
def crotch_height(P, body):
    """the height of his crotch: the lowest of his skin within 6 mm of his middle, above his knees"""
    sel = (~body.armMask) & (np.abs(P[:, 0]) < 0.006) & (P[:, 1] > 0.6)
    return float(P[sel, 1].min())


def trouser_panels(M, s, yin, yrise):
    """A front and a back panel for his left leg (the right ones are these mirrored), cut as a trouser block is: x
    across (the front's middle at 0, his left side seam at x > 0; the back's middle at 0, his left side at x < 0), y up
    from the hem. yin: the inseam (hem to the crotch), yrise: the crotch to the panels' top at the front (the waistband
    goes on above). The back reaches 1.5 cm higher at its middle, its seam slanting in toward the side seam at the
    top, and its crotch goes deeper (an eighth of the seat against the front's sixteenth), as it has to go round his
    seat. (3 cm higher, the waistband stood 1.5 cm above make3Dcore's at his back once draped, and pushed the tops
    over it out there.)"""
    c = lambda v: v / 100 * s
    W, S, K, HM = c(M["waist"]), c(M["seat"]), c(M["knee"]), c(M["hem"])
    Hf, ys, yk = yin + yrise, yin + yrise * 0.42, yin * 0.5 + c(4)
    fx, bx = S / 16, S / 8.5
    fs, bs = S / 4 - c(1), S / 4 + c(1)                  # (front and back across the seat line, middle to side)
    cf = (fs - fx) / 2; cb = (bx - bs) / 2               # (the crease lines)
    kf, kb, hf, hb = K / 2 - c(1), K / 2 + c(1), HM / 2 - c(1), HM / 2 + c(1)
    # the front: hem, side seam, waist, rise (its middle, down to the crotch point), inseam
    f_hem = seg((cf - hf / 2, 0), (cf + hf / 2, 0), 12)
    f_side = np.vstack([seg((cf + hf / 2, 0), (cf + kf / 2, yk), 10)[:-1], bez((cf + kf / 2, yk), (cf + kf / 2 + (fs - kf / 2 - cf) * 0.45, yin * 0.82),
                        (fs, yin - c(3)), (fs, ys))[:-1], bez((fs, ys), (fs, ys + (Hf - ys) * 0.4), (W / 4, Hf - c(4)), (W / 4, Hf))])
    f_waist = seg((W / 4, Hf), (0, Hf), 12)
    f_rise = np.vstack([seg((0, Hf), (0, ys), 6)[:-1], bez((0, ys), (0, yin + (ys - yin) * 0.35), (-fx * 0.55, yin), (-fx, yin))])
    f_ins = np.vstack([bez((-fx, yin), (-fx, yin - c(7)), (cf - kf / 2, yk + c(14)), (cf - kf / 2, yk))[:-1], seg((cf - kf / 2, yk), (cf - hf / 2, 0), 10)])
    front = Piece("front_L", 0, [("hem", f_hem), ("side", f_side), ("waist", f_waist), ("rise", f_rise), ("inseam", f_ins)])
    # the back: hem, inseam, rise (up from its crotch point, a centimetre lower), waist, side seam
    yb = yin - c(1); top = np.array((-c(3), Hf + c(1.5)))
    b_hem = seg((cb - hb / 2, 0), (cb + hb / 2, 0), 12)
    b_ins = np.vstack([seg((cb + hb / 2, 0), (cb + kb / 2, yk), 10)[:-1], bez((cb + kb / 2, yk), (cb + kb / 2, yk + c(12)), (bx, yb - c(7)), (bx, yb))])
    sl = (top - np.array((0, ys))) / np.linalg.norm(top - np.array((0, ys)))   # (the back seam's slant)
    b_rise = np.vstack([bez((bx, yb), (bx * 0.35, yb + c(0.5)), (0, yin + (ys - yin) * 0.2), (0, ys))[:-1], seg((0, ys), top, 8)])
    sx = top[0] - W / 4
    b_waist = seg(top, (sx, Hf - c(0.5)), 12)
    # (the side seam leaves the waist at right angles to it, downward, so the corners there make a full turn)
    wd = np.array((sx, Hf - c(0.5))) - top; wd /= np.linalg.norm(wd); dn = np.array((-wd[1], wd[0])); dn = -dn if dn[1] > 0 else dn
    b_side = np.vstack([bez((sx, Hf - c(0.5)), np.array((sx, Hf - c(0.5))) + dn * c(4), (-bs, ys + (Hf - ys) * 0.4), (-bs, ys))[:-1],
                        bez((-bs, ys), (-bs, yin - c(3)), (cb - kb / 2 - (bs - kb / 2 + cb) * 0.45, yin * 0.82), (cb - kb / 2, yk))[:-1],
                        seg((cb - kb / 2, yk), (cb - hb / 2, 0), 10)])
    back = Piece("back_L", 0, [("hem", b_hem), ("inseam", b_ins), ("rise", b_rise), ("waist", b_waist), ("side", b_side)])
    return front, back


class Trousers:
    """A pair of trousers (MEAS with legs=1): his left leg's front and back panels and the mirrored right ones, sewn
    down the outside and the inside of each leg and up the front and the back, a waistband round the top. Its lengths
    are his own: the inseam from his crotch to 3.5 cm off the floor (or MEAS hem_y, in cm)."""

    def __init__(self, arch, scale, body):
        self.arch, self.M, self.s = arch, MEAS[arch], scale
        M, s = self.M, scale
        self.yc = crotch_height(body.rel, body)
        self.yhem = M.get("hem_y", 3.5) / 100
        yin, yrise = self.yc - self.yhem, (M["rise"] - M["wb"]) / 100 * s
        fl, bl = trouser_panels(M, s, yin, yrise)
        P = {"front_L": fl, "back_L": bl, "front_R": mirror(fl, "front_R"), "back_R": mirror(bl, "back_R")}
        # the waistband: a band round his waist, sewn along the panels' tops (round from the front's middle by his
        # left, the back and his right) and closed at the front
        ring = [("front_L", "waist"), ("back_L", "waist"), ("back_R", "waist"), ("front_R", "waist")]
        rl = [plen(P[a].edge(b)) for a, b in ring]; cum = np.r_[0, np.cumsum(rl)]; wb = M["wb"] / 100 * s
        parts = [("n%d" % i, seg((cum[i], 0), (cum[i + 1], 0), 8)) for i in range(4)]
        P["band"] = Piece("band", 0, parts + [("cf_p", seg((cum[4], 0), (cum[4], wb), 4)), ("top", seg((cum[4], wb), (0, wb), 24)), ("cf_n", seg((0, wb), (0, 0), 4))])
        S = []
        for sd in "LR":
            S += [([("front_" + sd, "side")], [("back_" + sd, "side")], 0.5, False), ([("front_" + sd, "inseam")], [("back_" + sd, "inseam")], 0.5, False)]
        S += [([("front_L", "rise")], [("front_R", "rise")], 0.5, False), ([("back_L", "rise")], [("back_R", "rise")], 0.5, False),
              ([("band", "n%d" % i) for i in range(4)], ring, 1.0, False), ([("band", "cf_p")], [("band", "cf_n")], 0.5, False)]
        self.P, self.S, self.hood, self.ring = P, S, None, ring
        print("  crotch at %.3f m; inseam %.3f, rise %.3f (in his warped frame)" % (self.yc, yin, yrise), flush=True)


def leg_axis(P, body, side):
    """the middle of his leg (side 1: his left, x > 0) by height, every centimetre: x, z and its half-width"""
    reg = np.array([body.regions[r] for r in body.vreg])
    sel = (~body.armMask) & np.isin(reg, ["thigh", "shin", "foot", "hips"]) & (P[:, 0] * side > 0.004)
    Q = P[sel]; out = []
    for y in np.arange(0.0, 1.2, 0.01):
        q = Q[np.abs(Q[:, 1] - y) < 0.012]
        if len(q) < 6: out.append(out[-1] if out else (0.1 * side, 0.05, 0.05)); continue
        out.append(((q[:, 0].min() + q[:, 0].max()) / 2, (q[:, 2].min() + q[:, 2].max()) / 2, max(np.ptp(q[:, 0]), np.ptp(q[:, 2])) / 2))
    return np.array(out)


def edge_x(pc, nm, y):
    """x of a piece's edge at height y on the pattern (the edge's nearest sample in y)"""
    E = pc.edge(nm); return float(np.interp(y, *zip(*sorted(zip(E[:, 1], E[:, 0])))))


def place_legs(G, pieces, body):
    """3D positions for the trousers' pieces round his relaxed body, before sewing: below his crotch each leg's front and
    back wrapped round that leg (from its inside round to its outside), above it the four round his hips as an ellipse
    from the front's and the back's middles to the side seams, the crotch's extensions running under him to his crotch,
    the one blending into the other over a few centimetres; the waistband placed by close_seams on their tops"""
    P = body.rel; yc, y0 = G.yc, G.yhem
    axes = {1: leg_axis(P, body, 1), -1: leg_axis(P, body, -1)}
    reg = np.array([body.regions[r] for r in body.vreg]); torso = (~body.armMask) & np.isin(reg, ["belly", "hips", "thigh"])
    zcr = float(np.mean(P[(~body.armMask) & (np.abs(P[:, 0]) < 0.01) & (np.abs(P[:, 1] - yc) < 0.01), 2]))
    def ell(y):
        q = P[torso & (np.abs(P[:, 1] - y) < 0.01)]
        return np.abs(q[:, 0]).max() + 0.015, np.ptp(q[:, 2]) / 2 + 0.015, (q[:, 2].max() + q[:, 2].min()) / 2
    out = {}
    for nm, pc in pieces.items():
        if nm == "band":
            out[nm] = np.full((len(pc.V), 3), np.nan); continue
        sd = 1 if nm.endswith("_L") else -1; fr = nm.startswith("front"); ax = axes[sd]
        X = np.zeros((len(pc.V), 3))
        for i, (x, y) in enumerate(pc.V):
            yb = y0 + y
            # (the leg: from the inseam's x at this height to the side seam's, round from his leg's inside)
            xin = edge_x(pc, "inseam", min(y, yc - y0 - 1e-4)) if y < yc - y0 else edge_x(pc, "inseam", yc - y0 - 1e-4)
            xout = edge_x(pc, "side", y)
            u = np.clip((x - xin) / (xout - xin + 1e-9), 0, 1)
            ph = sd * (np.radians(-90 + 180 * u) if fr else np.radians(-90 - 180 * u))
            k = int(np.clip(round(yb / 0.01), 0, len(ax) - 1)); cx, cz, rl = ax[k]
            wf = abs(xout - xin)
            other = pieces[("back_" if fr else "front_") + ("L" if sd > 0 else "R")]
            wo = abs(edge_x(other, "side", y) - edge_x(other, "inseam", min(y, yc - y0 - 1e-4)))
            r = max((wf + wo) / (2 * np.pi), rl + 0.01)
            leg = np.array([cx + r * np.sin(ph), yb, cz + r * np.cos(ph)])
            # (the hips: the front's middle at the front, the back's at the back, the side seams at his sides)
            ea, eb, zc = ell(max(yb, yc + 0.02))
            sw = abs(edge_x(pc, "side", y)) + 1e-9
            ext = np.sign(x) != np.sign(edge_x(pc, "side", y)) and abs(x) > 1e-6
            if not ext:
                th = np.radians(90 * x / sw) if fr else np.radians(180 + 90 * x / sw)
                hip = np.array([ea * np.sin(th), max(yb, yc + 0.005), zc + eb * np.cos(th)])
            else:
                # (beyond the middle: under him, from the front's (or back's) middle to his crotch)
                mid = np.array([0.0, max(yb, yc + 0.005), zc + (eb if fr else -eb)])
                t = abs(x) / (pieces["front_L" if fr else "back_L"].edge("rise")[:, 0].__abs__().max() + 1e-9)
                hip = (1 - t) * mid + t * np.array([0.0, yc - 0.012, zcr])
            w = float(sstep(yc + 0.05, yc - 0.01, yb))
            X[i] = w * leg + (1 - w) * hip
        out[nm] = X
    return out


def seam_counts(seams, pieces):
    """one count per seam part, the larger of its two sides' (so both are sampled alike)"""
    cnt = {}
    for A, Bs, *_ in seams:
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
            th = arc.theta(V[:, 0] / (pc.band or 1.0)) + (np.pi if nm.startswith("back") else 0.0)   # (a band starts stretched to the body's width)
            q = np.stack([ea * np.sin(th), eb * np.cos(th)], 1); rc = np.linalg.norm(q, axis=1)
            yp = V[:, 1]; up = yp > L - Lb
            ph = np.where(up, (yp - (L - Lb)) / Rb, 0)
            rr = np.maximum(0.055, rc - Rb * (1 - np.cos(ph)))
            X[:, 0] = q[:, 0] / rc * rr; X[:, 2] = zc + q[:, 1] / rc * rr
            X[:, 1] = np.where(up, y0 + (L - Lb) + Rb * np.sin(ph), y0 + yp)
        elif nm.startswith(("sleeve", "cuff")):
            side = nm[-1]; sg = 1 if side == "L" else -1
            sh, el, wr = J["sh" + side], J["el" + side], J["wr" + side]
            l1, l2 = np.linalg.norm(el - sh), np.linalg.norm(wr - el)
            d1, d2 = (el - sh) / l1, (wr - el) / l2
            sv = pieces["sleeve_" + side]
            und = sv.edge("under_p"); yb = G.yb; ou = np.argsort(und[:, 1])
            hwid = lambda y: np.interp(y, und[ou, 1], np.abs(und[ou, 0]))
            ch = M["cuff"] / 100 * s
            au = 0.03
            kax = min(1.0, (l1 + l2 - 0.012 - au) / yb)

            def tube(x, y, cw=None):
                a = au + (yb - y) * kax
                if a < l1: c, d = sh + d1 * a, d1
                else: c, d = el + d2 * (a - l1), d2
                w = 2 * float(hwid(max(y, ch)))
                R = w / (2 * np.pi) + 0.004
                upp = sg * np.cross([0, 0, 1.0], d); upp /= np.linalg.norm(upp)
                fw = np.array([0, 0, 1.0]) - d[2] * d; fw /= np.linalg.norm(fw)
                ph = -sg * 2 * np.pi * x / (cw or w)      # (his right sleeve's x > 0 to the front, his left's x < 0: outside, seen from outside)
                return c + R * (np.cos(ph) * upp + np.sin(ph) * fw)
            if nm.startswith("cuff"):
                # (a cuff starts stretched to the sleeve's wrist)
                cw = 2 * float(np.abs(pc.edge("top")[:, 0]).max())
                for i, (x, y) in enumerate(V): X[i] = tube(x, y, cw)
                out[nm] = X; continue
            # the cap: from the tube's ring at the underarm straight up to the armhole it is sewn to (already placed
            # on the front and back), so it starts smooth. (Wrapped on along the arm and pulled onto the armhole, it
            # started crushed into his shoulder, and Blender kept those creases.)
            ce, ct = [], []
            for A, Bs, bias, same in G.S:
                for (pa, ea), (pb, eb) in zip(A, Bs):
                    if pa == nm and ea.startswith("cap"):
                        ia, ib = pc.B[ea], pieces[pb].B[eb]
                        ce += list(ia); ct += list(out[pb][ib if same else ib[::-1]])
            ce, ct = np.array(ce), np.array(ct)
            o = np.argsort(V[ce, 0]); cx, cy, ct = V[ce, 0][o], V[ce, 1][o], ct[o]
            for i, (x, y) in enumerate(V):
                if y <= yb:
                    X[i] = tube(x, y); continue
                yc = np.interp(x, cx, cy)
                t = np.clip((y - yb) / max(yc - yb, 1e-4), 0, 1)
                tgt = np.array([np.interp(x, cx, ct[:, k]) for k in range(3)])
                X[i] = (1 - t) * tube(x, yb) + t * tgt
        else:
            X[:] = np.nan   # (a collar: placed on the neckline it is sewn to)
        out[nm] = X
    return out


def close_seams(pieces, X, seams, reach=0.10):
    """Turns each seam the way its two sides lie, then moves both sides toward each other (bias), carrying the
    pieces' nearby points along, so the sewing starts nearly closed. Gives the sewing pairs (global ids)."""
    pairs = []
    for A, Bs, bias, same in seams:
        ia, ib = [], []
        for (pa, ea), (pb, eb) in zip(A, Bs):
            a = list(pieces[pa].B[ea]); b = list(pieces[pb].B[eb])
            if len(a) != len(b): raise SystemExit("seam %s.%s / %s.%s: %d against %d points" % (pa, ea, pb, eb, len(a), len(b)))
            if not same: b = b[::-1]
            XA, XB = X[pa][a], X[pb][b]
            if not np.isnan(XA).any() and np.linalg.norm(XA - XB[::-1], axis=1).mean() < np.linalg.norm(XA - XB, axis=1).mean():
                # (the pattern decides; where the placing says otherwise the pieces start out twisted at that seam)
                print("  seam %s.%s / %s.%s starts nearer the other way round" % (pa, ea, pb, eb), flush=True)
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
        if getattr(pc, "roll", False):
            # (a tailored jacket's stand: straight up round the back of his neck, as a collar stands, and down the V
            # carried on from the front it is sewn to, the way the front runs across the seam (from its points within 4
            # cm on the pattern to the seam's), in across his chest; the one turning into the other over the first 8 cm
            # of the V from his shoulder. Carried on from the back too, it went in over his neck: the back is placed
            # rolled over his shoulders there)
            dirs = []
            for p, i in ib:
                Vb = pieces[p].V; dd = np.linalg.norm(Vb - Vb[i], axis=1); near = (dd > 1e-6) & (dd < 0.04)
                d = (X[p][i] - X[p][near]).mean(0); d /= np.linalg.norm(d) + 1e-12
                top = Vb[Vb[:, 1] > Vb[:, 1].max() - 1e-6]
                w = 0.0 if p == "back" else float(sstep(0.0, 0.08, np.linalg.norm(top - Vb[i], axis=1).min()))
                d = (1 - w) * np.array([0, 1.0, 0]) + w * d; dirs.append(d / (np.linalg.norm(d) + 1e-12))
            dirs = np.array(dirs); dirs = np.array([dirs[max(0, k - 2):k + 3].mean(0) for k in range(len(dirs))])
            dirs /= np.linalg.norm(dirs, axis=1, keepdims=True)
            pc.dirs = np.zeros((len(V), 3))
            for j in range(len(V)):
                k = int(np.argmin(np.abs(nx - V[j, 0]))); base = tgt[k]
                rad = base - cen; rad[1] = 0; rad /= (np.linalg.norm(rad) + 1e-9)
                X[pa][j] = base + dirs[k] * (V[j, 1] - V[src[k], 1]) + rad * 0.004; pc.dirs[j] = dirs[k]
            continue
        if getattr(pc, "lapel", None) is not None:
            # (a lapel: each point by its place along the neck edge and its distance from it, folded back from the
            # stand's top the way the stand came up, and laid 7 mm out from the cloth there (the stand, the front or
            # the back, turned to face out from him), so it lies over the stand and on down the front across his chest,
            # and down the back of his neck over the stand onto his shoulders. Its fold starts on the stand's top: laid
            # out 7 mm there too, sewing it on drew all of it back in onto the front)
            nk, sl = pc.lapel
            d2 = ((V[:, None, :] - nk[None, :, :]) ** 2).sum(2); kk = d2.argmin(1)
            sv, dv = sl[kk], np.sqrt(d2[np.arange(len(V)), kk])
            fold = np.array([-pieces[p].dirs[i] for p, i in ib])
            o = np.argsort(sv[src]); ss, tg, fd = sv[src][o], tgt[o], fold[o]
            cloth = [k for k in pieces if not np.isnan(X[k]).any() and pieces[k].grp in (0, 4)]
            CP = np.vstack([X[k] for k in cloth]); zc = CP[:, 2].mean()
            CN = np.vstack([vnormals(X[k], pieces[k].T) for k in cloth])
            CN *= np.where(np.einsum("ij,ij->i", CN, CP - np.c_[np.zeros(len(CP)), CP[:, 1], np.full(len(CP), zc)]) < 0, -1.0, 1.0)[:, None]
            kd = mathutils.kdtree.KDTree(len(CP))
            for k, q in enumerate(CP): kd.insert(q, k)
            kd.balance()
            for j in range(len(V)):
                base = np.array([np.interp(sv[j], ss, tg[:, k]) for k in range(3)])
                f = np.array([np.interp(sv[j], ss, fd[:, k]) for k in range(3)]); f /= np.linalg.norm(f) + 1e-12
                raw = base + f * dv[j]
                _, q, _ = kd.find(raw); n = CN[q]
                X[pa][j] = raw - n * float(np.dot(raw - CP[q], n)) + n * 0.007 * float(sstep(0.0, 0.012, dv[j]))
            continue
        if getattr(pc, "fold", None):
            # (a leaf: each point by its angle round the ring it is cut as, along the seam, and its distance from the
            # neck edge down from there, falling outward as a collar's leaf does over the stand)
            r0, phi = pc.fold["r0"], pc.fold["phi"]
            th = np.arctan2(V[:, 0], V[:, 1] + r0); dd = np.hypot(V[:, 0], V[:, 1] + r0) - r0
            ts = th[src]; o = np.argsort(ts); ts, tg = ts[o], tgt[o]
            for j in range(len(V)):
                base = np.array([np.interp(th[j], ts, tg[:, k]) for k in range(3)])
                rad = base - cen; rad[1] = 0; rad /= (np.linalg.norm(rad) + 1e-9)
                X[pa][j] = base + np.array([0, -dd[j] * 0.8, 0]) + rad * (0.005 + dd[j] * 0.6)
            continue
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


def relax(X, E, R, P, N, iters=500, smooth=(0.25, 0.03), fixed=None, over=None):
    """the cloth eased to its pattern's lengths (no gravity), kept outside his body: a Jacobi position solve. fixed:
    points held where they are (a hood's neckline, on the garment's). over: (points, points they lie over, triangles):
    the first kept 5 mm out from the second (a lapel over the front, the cloth facing out from him)"""
    X0 = X.copy()
    kd = mathutils.kdtree.KDTree(len(P))
    for i, p in enumerate(P): kd.insert(p, i)
    kd.balance()
    nb = np.zeros(len(X)); np.add.at(nb, E[:, 0], 1); np.add.at(nb, E[:, 1], 1)
    for it in range(iters):
        d = X[E[:, 1]] - X[E[:, 0]]; L = np.linalg.norm(d, axis=1) + 1e-12
        c = ((L - R) / L)[:, None] * d * 0.5
        acc = np.zeros_like(X); np.add.at(acc, E[:, 0], c); np.add.at(acc, E[:, 1], -c)
        X += 1.6 * acc / nb[:, None]
        # (smoothed hard at first, then lightly: Blender keeps whatever creases the cloth starts with as its own. Each
        # smoothing step is followed by one a little larger the other way (Taubin's), so the cloth is not shrunk onto
        # him: shrunk, its ease gathered into sharp fins along the side seams, which Blender then kept)
        sm = smooth[0] if it < iters * 0.6 else smooth[1]
        for k in (sm, -1.04 * sm):
            S = np.zeros_like(X); np.add.at(S, E[:, 0], X[E[:, 1]]); np.add.at(S, E[:, 1], X[E[:, 0]])
            X += k * (S / nb[:, None] - X)
        if fixed is not None: X[fixed] = X0[fixed]
        if over is not None and (it % 8 == 0 or it == iters - 1):
            top, und, Tw = over
            Nu = vnormals(X, Tw)[und]; Xu = X[und]; zc = Xu[:, 2].mean()
            Nu *= np.where(np.einsum("ij,ij->i", Nu, Xu - np.c_[np.zeros(len(Xu)), Xu[:, 1], np.full(len(Xu), zc)]) < 0, -1.0, 1.0)[:, None]
            ku = mathutils.kdtree.KDTree(len(Xu))
            for k, q in enumerate(Xu): ku.insert(q, k)
            ku.balance()
            for i in top:
                _, j, _ = ku.find(X[i]); dd = float(np.dot(X[i] - Xu[j], Nu[j]))
                if dd < 0.005: X[i] += Nu[j] * (0.005 - dd)
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


def body_obj(body, poses, frames, hold=0, friction=8.0, name="dave"):
    """his body as a collider, its shape keys walking it from the first pose to the last: pose i is reached at
    frames[i] and held for hold frames before moving on to the next"""
    ob = new_obj(name, poses[0], body.idx)
    # (keys made from here on are linear; Blender 5 has no Action.fcurves to set them afterwards)
    bpy.context.preferences.edit.keyframe_new_interpolation_type = "LINEAR"
    set_key(ob, "Basis", poses[0])
    keys = [set_key(ob, "p%d" % i, X) for i, X in enumerate(poses[1:], 1)]
    for i, kb in enumerate(keys):
        kb.value = 0.0; kb.keyframe_insert("value", frame=frames[i] + hold)
        kb.value = 1.0; kb.keyframe_insert("value", frame=frames[i + 1])
        if i + 1 < len(keys):
            kb.keyframe_insert("value", frame=frames[i + 1] + hold)
            kb.value = 0.0; kb.keyframe_insert("value", frame=frames[i + 2])
    ob.modifiers.new("collide", "COLLISION")
    ob.collision.thickness_outer = 0.003; ob.collision.thickness_inner = 0.02; ob.collision.cloth_friction = friction; ob.collision.damping = 0.1
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
        # (each point at its piece's weight: the bending stiffness runs from bending at 0 to bending_stiffness_max at 1)
        vg = ob.vertex_groups.new(name="stiff")
        for w in np.unique(stiff[stiff > 0]): vg.add([int(i) for i in np.where(stiff == w)[0]], float(w), "REPLACE")
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
    """steps the simulation; snap(frame, positions) is called at each frame in snap.at. gravity: a vector, or a function
    of the frame giving one. (The page's frame has y up; Blender's gravity points down its z unless told otherwise.)"""
    sc = bpy.context.scene; sc.frame_start = 1; sc.frame_end = frames
    sc.use_gravity = True
    import time
    t0 = time.time()
    for f in range(1, frames + 1):
        sc.gravity = gravity(f) if callable(gravity) else gravity
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

def head_shape(P, body):
    """his head as an ellipsoid: centre and half-widths (x, y, z) from its skin in pose P"""
    reg = np.array([body.regions[r] for r in body.vreg]); H = P[reg == "head"]
    lo, hi = H.min(0), H.max(0)
    return (lo + hi) / 2, (hi - lo) / 2


def hood_seams(G):
    """the hood's seams for sampling: its back seam, and each half's neckline on the garment's (opposite ways)"""
    return G.hood_S + [([(h, e)], [g], 1.0, False) for h, lst in G.hood_ring.items() for e, g in lst]


def drape_hood(G, body, can, off, Xs, Tw, a, F):
    """The hood, draped after the garment: its two halves sewn up the back and placed up round his head, the neckline
    held on the draped garment's, then let fall back off his head onto his shoulders (gravity tilted backward at
    first), against his body and the draped garment. Gives the hood's welded points, triangles, its pattern and the
    garment points its neckline is sewn to."""
    HP = G.hood
    P = body.rel; N = vnormals(P, body.idx)
    hc, hr = head_shape(P, body); hr = hr + np.array([0.03, 0.02, 0.03])
    # each half's neckline: the garment's points it is sewn to (the garment's edge runs the other way)
    tgt = {}
    for h, lst in G.hood_ring.items():
        ids, gids = [], []
        for e, (gp, ge) in lst:
            ia = HP[h].B[e]; ib = G.P[gp].B[ge][::-1]
            ids += list(ia); gids += [can[off[gp] + i] for i in ib]
        tgt[h] = (np.array(ids), np.array(gids))
    X = {}
    for h, pc in HP.items():
        sg = 1 if h.endswith("L") else -1
        V = pc.V; ax = np.abs(V[:, 0]); Hh = V[:, 1].max(); ids, gids = tgt[h]
        U = ax[ids].max()
        o = np.argsort(ax[ids]); nx = ax[ids][o]; nt = Xs[gids][o]
        Nk = lambda x: np.array([np.interp(x, nx, nt[:, k]) for k in range(3)])
        ph0, th0, v1 = 0.6, -0.35, 0.3
        Q = np.zeros((len(V), 3))
        for i, (x, y) in enumerate(V):
            u = min(1.0, abs(x) / U); ph = ph0 + (np.pi - ph0) * u; v = y / Hh
            S = lambda th: hc + hr * np.array([sg * math.cos(th) * math.sin(ph), math.sin(th), math.cos(th) * math.cos(ph)])
            Q[i] = Nk(abs(x)) * (1 - v / v1) + S(th0) * (v / v1) if v < v1 else S(th0 + (np.pi / 2 - 0.12 - th0) * (v - v1) / (1 - v1))
        Q[ids] = Xs[gids]
        X[h] = Q
    pairs, offh = close_seams(HP, X, G.hood_S)
    allX = np.vstack([X[k] for k in HP]); T = np.vstack([HP[k].T + offh[k] for k in HP])
    canh, nh = weld(len(allX), pairs)
    Xh = np.zeros((nh, 3)); np.add.at(Xh, canh, allX); Xh /= np.bincount(canh, minlength=nh)[:, None]
    Th = canh[T]; Vpat = np.vstack([HP[k].V for k in HP])
    pin = np.concatenate([canh[offh[h] + tgt[h][0]] for h in HP]); pg = np.concatenate([tgt[h][1] for h in HP])
    Xh[pin] = Xs[pg]
    E, R = cloth_edges(Th, T, Vpat)
    print("  hood: %d points; eased to the pattern: edge/pattern 5%% %.3f, median %.3f, 95%% %.3f" % ((nh,) + tuple(relax(Xh, E, R, P, N, fixed=pin))), flush=True)
    if a.debug: debug_json(os.path.join(a.debug, G.arch + "-hood-placed.json"), body, P, [(G.arch, Xs, Tw, "#7a2a30"), ("hood", Xh, Th, "#a0414a")])
    clear_scene()
    static_collider("dave", P, body.idx, th=0.003)
    static_collider("garment", Xs, Tw, th=0.003)
    fall, settle = F(40), F(50)
    co = cloth_obj("hood", Xh, Th, None, [], pins=pin, frames=fall + settle, bending=a.hood_bending, mass=a.mass, tension=a.tension)
    co.modifiers["cloth"].settings.pin_stiffness = 50.0
    grav = lambda f: (0.0, -6.0, -8.0) if f <= fall else (0.0, -9.81, 0.0)

    def snap(f, Xf):
        if a.debug: debug_json(os.path.join(a.debug, "%s-hood-f%03d.json" % (G.arch, f)), body, P, [(G.arch, Xs, Tw, "#7a2a30"), ("hood", Xf[0], Th, "#a0414a")])
    snap.at = {F(10), fall} | {int(f) for f in os.environ.get("GB_SNAPS", "").split(",") if f}
    Xd, = run(fall + settle, [co], "hood", snap, gravity=grav)
    if a.debug: debug_json(os.path.join(a.debug, G.arch + "-hood-draped.json"), body, P, [(G.arch, Xs, Tw, "#7a2a30"), ("hood", Xd, Th, "#a0414a")])
    st = np.linalg.norm(Xd[E[:, 0]] - Xd[E[:, 1]], axis=1) / R
    print("  hood draped: edge/pattern 5%% %.3f, median %.3f, 95%% %.3f; neckline off the garment's by %.1f mm at most" % (tuple(np.percentile(st, [5, 50, 95])) + (1000 * np.linalg.norm(Xd[pin] - Xs[pg], axis=1).max(),)), flush=True)
    return Xd, Th, canh, offh, pin, pg


ARM_REG, TORSO_REG = ("uarm", "farm", "hand"), ("chest", "belly", "hips", "neck", "head")

# ---------------------------------------------------------------- the scarf
# A scarf wound a turn and a half round his neck, both ends hanging down his front, one longer than the other (lengths
# in cm): a 180 x 22 cm scarf folded in half along its length, as it is usually worn, so a band 11 cm wide (folded to
# 14 cm, the turn and a half took so much of it that the ends reached only his upper chest). It is not sewn: it is laid
# on him (draped over his body and, as a stand-in for what he wears under it, the draped jumper) and let fall.
SCARF = dict(length=180, width=11, longer=10)
# (how it is wound: each end leaves the loop `fwd` radians forward of the side of his neck and hangs `apart` m from the
# middle; the loop starts `room` m out from him (or the jumper), each turn `step` m further out, its middle `y` m above
# the base of his neck behind and `side` m higher at the sides; round his neck the band leans out, `lean` the tangent
# of its angle from upright)
SCARF_WRAP = dict(fwd=0.35, apart=0.055, room=0.018, step=0.01, y=0.012, side=0.04, lean=0.45)
for _k in list(SCARF_WRAP):
    if os.environ.get("GB_SCARF_" + _k.upper()): SCARF_WRAP[_k] = float(os.environ["GB_SCARF_" + _k.upper()])


class Flat:
    """a piece with no seams, already meshed: its points on the flat pattern (V), triangles (T) and group"""

    def __init__(self, name, V, T, grp=0):
        self.name, self.V, self.T, self.grp, self.stiff, self.band = name, V, T, grp, 0.0, 0.0


def scarf_piece(s, h=0.014):
    W, L = SCARF["width"] / 100 * s, SCARF["length"] / 100 * s
    nu, nv = int(round(W / h)) + 1, int(round(L / h)) + 1
    u, v = np.linspace(0, W, nu), np.linspace(0, L, nv)
    V = np.array([[x, y] for y in v for x in u])
    T = []
    for j in range(nv - 1):
        for i in range(nu - 1):
            a = j * nu + i; b = a + 1; c = a + nu; d = c + 1
            T += [[a, b, d], [a, d, c]]
    return Flat("scarf", V, np.array(T)), nu, nv


def scarf_path(P, body, under, bvs, L, longer):
    """its centre line laid on him before the drape, as a scarf is wound once round: up his front from the foot of the
    longer end, over his right collarbone to the side of his neck, round the back of it, across the front of his throat,
    round the back again and forward to the left side of his neck, then down over his left collarbone (a turn and a half,
    each pass further out and a little higher than the last, so it lies over the one before). Each end turns down over
    the curve of his shoulder, where cloth can turn without folding: brought round to the front of his throat and turned
    straight down there, flat on his chest, the band had to fold on itself where it turned, and bunched into a knot.
    Gives points, the way out from him at each, and the length of each part."""
    reg = np.array([body.regions[r] for r in body.vreg]); Nk = P[reg == "neck"]
    y0 = Nk[:, 1].min(); base = Nk[Nk[:, 1] < y0 + 0.025]
    cz = (base[:, 2].min() + base[:, 2].max()) / 2
    U = np.vstack([P, under])
    def height(th):
        # (higher at the sides of his neck, where his shoulders rise into it, than behind; across his throat it dips onto
        # the top of his chest, as a scarf wound round lies: level all round, its front was squeezed between his chin
        # and chest and heaped up over his chin)
        fr = (1 + math.cos(th)) / 2
        return y0 + SCARF_WRAP["y"] - 0.045 * fr + SCARF_WRAP["side"] * math.sin(th) ** 2
    # (how far out he is, or the jumper on him, at each way round his neck at the loop's height: found from outside. An
    # ellipse round his bare neck sat inside his shoulders and the jumper's collar at the sides, 3 cm deep)
    ths = np.linspace(0, 2 * np.pi, 73)[:-1]; rs = []
    for th in ths:
        dv = np.array([math.sin(th), 0.0, math.cos(th)]); o = np.array([0.0, height(th), cz]) + 0.3 * dv
        hit = 0.0
        for bv, _ in bvs:
            loc, _, _, dist = bv.ray_cast(mathutils.Vector(o), mathutils.Vector(-dv), 0.3)
            if loc is not None: hit = max(hit, 0.3 - dist)
        rs.append(hit)
    rs = np.array(rs); rs = np.array([np.mean(np.take(rs, range(k - 2, k + 3), mode="wrap")) for k in range(len(rs))])
    def rad(th):
        k = (th % (2 * np.pi)) / (2 * np.pi) * len(rs); k0 = int(k) % len(rs); f = k - int(k)
        return rs[k0] * (1 - f) + rs[(k0 + 1) % len(rs)] * f
    def front(x, y):
        sel = U[(np.abs(U[:, 0] - x) < 0.02) & (np.abs(U[:, 1] - y) < 0.015)]
        return sel[:, 2].max() if len(sel) else cz + rad(0.0)
    yN = y0 + 0.0
    d = SCARF_WRAP["fwd"]                      # (how far forward of the side of his neck each end leaves the loop)
    th0, span = -(np.pi / 2 - d), 3 * np.pi + 2 * d
    def ring(th):
        g = (th0 - th) / (2 * np.pi)            # (turns so far)
        r = rad(th) + SCARF_WRAP["room"] + SCARF_WRAP["step"] * g
        return np.array([r * math.sin(th), height(th) + 0.006 * g, cz + r * math.cos(th)])
    R = [ring(t) for t in np.linspace(th0, th0 - span, 300)]
    def hang(x, ytop, off):
        return [np.array([x, y, front(x, y) + off]) for y in np.arange(ytop, 0.55, -0.01)]
    # (each end from its foot up over his collarbone to where it meets the loop, by way of a curve)
    xs = SCARF_WRAP["apart"]
    Ha = hang(-xs, yN - 0.06, 0.012); Hb = hang(xs, yN - 0.06, 0.02)
    def join(p0, p1, d1, k=16):
        c1 = p0 + np.array([0, 0.035, 0.0]); c2 = p1 - d1 * 0.04
        return [bezp(p0, c1, c2, p1, t) for t in np.linspace(0, 1, k)[1:-1]]
    dA = R[1] - R[0]; dA /= np.linalg.norm(dA); dB = R[-1] - R[-2]; dB /= np.linalg.norm(dB)
    A = Ha[::-1] + join(Ha[0], R[0], dA)
    B = join(Hb[0], R[-1], -dB)[::-1] + Hb
    C = np.array(A + R + B)
    seg = np.r_[0, np.cumsum(np.linalg.norm(np.diff(C, axis=0), axis=1))]
    la, lr = seg[len(A)], seg[len(A) + len(R) - 1] - seg[len(A)]
    print("  round his neck at the loop: %.3f m out at the sides, %.3f in front, %.3f behind; loop %.2f m, ends %.2f m" % (
        (rad(np.pi / 2) + rad(-np.pi / 2)) / 2, rad(0), rad(np.pi), lr, L - lr), flush=True)
    # (cut to the scarf's length: the longer end hanging longer by `longer`)
    ha = (L - lr + longer) / 2; hb = L - lr - ha
    s0 = la - ha; s1 = la + lr + hb
    nA, nR = len(A), len(R)
    def out(i):
        # (the way out from him: from his neck's middle round the loop, straight out of his chest down each end, and
        # turning from one to the other up each join, so the band twists over his collarbone rather than all at once)
        ro = C[i] - np.array([0, C[i][1], cz]); ro /= np.linalg.norm(ro) + 1e-12
        if nA <= i < nA + nR: return ro
        k = (i - (nA - 15)) / 15.0 if i < nA else ((nA + nR + 14) - i) / 15.0
        w = sstep(0.0, 1.0, k)
        v = (1 - w) * np.array([0, 0, 1.0]) + w * ro
        return v / (np.linalg.norm(v) + 1e-12)
    return C, seg, s0, s1, out, (cz, yN, la, lr)


def bezp(p0, p1, p2, p3, t):
    return (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t * t * p2 + t ** 3 * p3


def drape_scarf(body, a, F, scale):
    """The scarf (SCARF): laid along scarf_path on him, the band's width across it (round his neck leaning out, its lower
    half bent out over his shoulders; flat across his front where it hangs), over his body and the draped jumper, then
    let fall."""
    P = body.rel; N = vnormals(P, body.idx)
    jp = os.path.join(a.out, "jumper.json")
    J = json.load(open(jp)); Xj = unb64(J["pos"], np.float32).reshape(-1, 3).astype(np.float64)
    Tj = unb64(J["vmap"], np.uint16).astype(np.int64)[unb64(J["idx"], np.uint16).astype(np.int64)].reshape(-1, 3)
    pc, nu, nv = scarf_piece(scale)
    L = pc.V[:, 1].max(); W = pc.V[:, 0].max()
    bvs = [(mathutils.bvhtree.BVHTree.FromPolygons(P.tolist(), body.idx.tolist()), False),
           (mathutils.bvhtree.BVHTree.FromPolygons(Xj.tolist(), Tj.tolist()), True)]
    C, seg, s0, s1, out, (cz, yN, la, lr) = scarf_path(P, body, Xj, bvs, L, SCARF["longer"] / 100 * scale)
    print("scarf: %d points (%d across, %d along); path %.2f m, scarf %.2f m" % (len(pc.V), nu, nv, seg[-1], L), flush=True)
    # each row of the band at its place along the path: its centre, the way along, out, and across
    rows = []; prev = None
    for j in range(nv):
        sv = s0 + pc.V[j * nu, 1]
        i = int(np.clip(np.searchsorted(seg, sv) - 1, 0, len(C) - 2)); f = (sv - seg[i]) / max(1e-9, seg[i + 1] - seg[i])
        c = C[i] * (1 - f) + C[i + 1] * f; t = C[i + 1] - C[i]; t /= np.linalg.norm(t)
        n = out(i); n = n - t * np.dot(n, t); n /= np.linalg.norm(n) + 1e-12
        b = np.cross(t, n); b /= np.linalg.norm(b) + 1e-12
        if prev is not None and np.dot(b, prev) < 0: b = -b
        prev = b
        rows.append((sv, c, n, b, sstep(yN - 0.09, yN - 0.03, c[1])))
    # (its cross-section: round his neck it leans out over his shoulders, as a scarf lies on them, the half above its
    # middle straight and the half below bending further out as it goes down, by as much as it takes to clear his
    # shoulders and the jumper on them. Leant out straight, its lower edge ran into the slope of his shoulders at the
    # sides of his neck, and moving each point that did out of him on its own stretched the band there to five times
    # its length, which it kept: the cloth takes the shape it is laid in as its own)
    def gap(Q):
        g = 1.0
        for bv, shell in bvs:
            for q in Q:
                loc, nor, _, dist = bv.find_nearest(mathutils.Vector(q))
                if loc is None: continue
                s = float(np.dot(q - np.array(loc), np.array(nor)))
                # (the jumper is open at his neck: above its collar the nearest of it is the collar's edge, not a side)
                if shell and abs(s) < 0.7 * dist: continue
                g = min(g, s)
        return g
    xs_ = pc.V[:nu, 0] - W / 2
    def section(c, n, b, rw, push, bend):
        up = 1.0 if b[1] >= 0 else -1.0; u = up * b
        a0 = math.atan(SCARF_WRAP["lean"] * rw)
        c = c + push * n; Q = np.zeros((nu, 3))
        for k, s in enumerate(xs_):
            r = abs(s); hi = s * up >= 0
            if hi: Q[k] = c + r * (u * math.cos(a0) - n * math.sin(a0))
            else:
                # (the lower half's direction turns out from a0 to a0 + bend across it: summed in small steps)
                m = 12; p = c.copy()
                for q in range(m):
                    al = a0 + bend * (q + 0.5) / m * r / (W / 2)
                    p = p + r / m * (-u * math.cos(al) + n * math.sin(al))
                Q[k] = p
        return Q
    hi_ = lambda b: (xs_ * (1.0 if b[1] >= 0 else -1.0)) >= 0
    clr = 0.006
    push = np.zeros(nv); bend = np.zeros(nv)
    for j, (sv, c, n, b, rw) in enumerate(rows):
        if rw <= 0: continue
        Q = section(c, n, b, rw, 0.0, 0.0); h = hi_(b)
        g = gap(Q[h]); push[j] = max(0.0, clr - g) if g < clr else 0.0
        best = (-1.0, 0.0)
        for bd in np.arange(0.0, 1.31, 0.05):
            g = gap(section(c, n, b, rw, push[j], bd)[~h])
            if g >= clr: best = (g, bd); break
            if g > best[0]: best = (g, bd)
        bend[j] = best[1]
        if os.environ.get("GB_DBG"): print("    row %3d sv %.3f rw %.2f c %s push %.1f mm bend %.0f gap %.1f mm" % (j, sv, rw, np.round(c, 3), push[j] * 1000, math.degrees(bend[j]), best[0] * 1000), flush=True)
    def smooth(v, k=2, m=3):
        w = np.array([v[max(0, j - k):j + k + 1].max() for j in range(len(v))])
        return np.array([w[max(0, j - m):j + m + 1].mean() for j in range(len(w))])
    push, bend = smooth(push), smooth(bend)
    print("  round his neck: moved out up to %.1f mm, lower half bent out up to %.0f degrees" % (push.max() * 1000, math.degrees(bend.max())), flush=True)
    X = np.zeros((len(pc.V), 3)); pins = []
    for j, (sv, c, n, b, rw) in enumerate(rows):
        X[j * nu:(j + 1) * nu] = section(c, n, b, rw, push[j], bend[j])
        # (the upper edge of the loop's first turn round the back of his neck is held where it is laid, as the scarf's
        # grip on his collar holds it: left free, the back of the loop slid down his neck and, the loop being closed,
        # drew the front up over his chin in a crumpled heap)
        if la <= sv <= la + lr * (np.pi + SCARF_WRAP["fwd"]) / (3 * np.pi + 2 * SCARF_WRAP["fwd"]) and (c[2] - cz) < -0.02:
            pins.append(j * nu + (nu - 1 if b[1] >= 0 else 0))
    print("  pushed out of his body", push_out(X, P, N, 0.006), "points", flush=True)
    Nj = vnormals(Xj, Tj)
    print("  pushed out of the jumper", push_out(X, Xj, Nj, 0.006), "points", flush=True)
    T = pc.T
    if a.debug:
        os.makedirs(a.debug, exist_ok=True)
        debug_json(os.path.join(a.debug, "scarf-placed.json"), body, P, [("jumper", Xj, Tj, "#9aa0a6"), ("scarf", X, T, "#26304a")])
    clear_scene()
    static_collider("dave", P, body.idx, th=0.003)
    static_collider("jumper", Xj, Tj, th=0.003)
    # (it has settled by about frame 35, each point moving a millimetre or two in five frames; after that the layers'
    # pushing on each other slowly works the front of the loop up off his throat and crumples it, so it stops at 40)
    frames = F(40)
    co = cloth_obj("scarf", X, T, None, [], pins=pins, frames=frames, bending=a.bending, mass=a.mass, tension=a.tension)
    if pins: co.modifiers["cloth"].settings.pin_stiffness = 20.0
    print("  held at the back of his neck:", len(pins), "points", flush=True)
    cc = co.modifiers["cloth"].collision_settings; cc.self_distance_min = 0.004; cc.distance_min = 0.004

    def snap(f, Xf):
        if a.debug: debug_json(os.path.join(a.debug, "scarf-f%03d.json" % f), body, P, [("jumper", Xj, Tj, "#9aa0a6"), ("scarf", Xf[0], T, "#26304a")])
    snap.at = {F(10), F(20), F(30)} | {int(f) for f in os.environ.get("GB_SNAPS", "").split(",") if f}
    Xs, = run(frames, [co], "scarf", snap)
    if a.debug: debug_json(os.path.join(a.debug, "scarf-draped.json"), body, P, [("jumper", Xj, Tj, "#9aa0a6"), ("scarf", Xs, T, "#26304a")])
    E = np.array(sorted({tuple(sorted((int(t[k]), int(t[(k + 1) % 3])))) for t in T for k in range(3)}))
    R = np.linalg.norm(pc.V[E[:, 0]] - pc.V[E[:, 1]], axis=1)
    st = np.linalg.norm(Xs[E[:, 0]] - Xs[E[:, 1]], axis=1) / R
    print("  draped: edge/pattern 5%% %.3f, median %.3f, 95%% %.3f" % tuple(np.percentile(st, [5, 50, 95])), flush=True)
    path = os.path.join(a.out, "scarf.json")
    out_ = {"v": 1, "arch": "scarf", "size": "one", "meas_cm": dict(SCARF), "scale": round(scale, 5), "char": dict(body.char),
            "about": "Made by tools/build_garments.py: a scarf folded along its length, wound a turn and a half round Dave's "
                     "neck with both ends down his front and draped over his body and the draped jumper in headless Blender. As the other "
                     "templates: pos, vmap, piece, pat (x across the band, y along it from the longer end's foot), idx, bind."}
    out_.update(template({"scarf": pc}, np.arange(len(pc.V)), Xs, T, body, lambda q: TORSO_REG))
    json.dump(out_, open(path, "w"), separators=(",", ":"))
    print("  wrote %s (%.0f KB)" % (os.path.relpath(path, ROOT), os.path.getsize(path) / 1024), flush=True)



def bind(X, regs, body, P):
    """Each point's place on his body P: the nearest triangle among those of its regions (regs[i]: a tuple of region
    names), as barycentric weights of the point's foot on that triangle's plane (b, c; a = 1 - b - c) and its height
    h along the triangle's unit normal (cross(b - a, c - a), his triangles' own order): X = a A + b B + c C + h n."""
    tri = np.zeros(len(X), np.int64); W = np.zeros((len(X), 3))
    for rs in set(regs):
        sel = np.array([r == rs for r in regs]); cand = body.region_tris(rs)
        # (a trouser leg's points only on that side of him: "+x" his left, "-x" his right)
        sd = 1 if "+x" in rs else (-1 if "-x" in rs else 0)
        if sd: cand = cand[P[body.idx[cand]].mean(1)[:, 0] * sd > -0.01]
        A, B, C = P[body.idx[cand, 0]], P[body.idx[cand, 1]], P[body.idx[cand, 2]]
        kd = mathutils.kdtree.KDTree(len(cand))
        for k, c in enumerate((A + B + C) / 3): kd.insert(c, k)
        kd.balance()
        for i in np.where(sel)[0]:
            best, bd = None, 1e9
            for _, k, _ in kd.find_n(X[i], 16):
                q = mathutils.geometry.closest_point_on_tri(mathutils.Vector(X[i]), *(mathutils.Vector(v) for v in (A[k], B[k], C[k])))
                d = (q - mathutils.Vector(X[i])).length
                if d < bd: best, bd = k, d
            a, b, c = A[best], B[best], C[best]; n = np.cross(b - a, c - a); n /= np.linalg.norm(n)
            e1, e2, r = b - a, c - a, X[i] - a; h = float(np.dot(r, n)); r = r - h * n
            M = np.array([[e1 @ e1, e1 @ e2], [e1 @ e2, e2 @ e2]]); w = np.linalg.solve(M, [r @ e1, r @ e2])
            tri[i] = cand[best]; W[i] = (w[0], w[1], h)
    return tri, W


def template(pieces, can, Xs, T, body, regs_of):
    """one mesh for the page: its welded points (positions and binding), and its pattern points (each with its
    welded point, its piece and its place on the flat pattern) with the triangles over them"""
    names = list(pieces); pid = np.concatenate([np.full(len(pieces[k].V), i) for i, k in enumerate(names)])
    first = np.full(len(Xs), -1)
    for o in range(len(can) - 1, -1, -1): first[can[o]] = o
    regs = [regs_of(pieces[names[pid[o]]]) for o in first]
    tri, W = bind(Xs, regs, body, body.rel)
    h = np.abs(W[:, 2])
    print("  bound to his body: height off it median %.1f mm, 95%% %.1f, max %.1f" % tuple(1000 * np.percentile(h, [50, 95, 100])), flush=True)
    return {"pieces": [{"name": k, "grp": pieces[k].grp, "band": round(pieces[k].band, 4), "stiff": pieces[k].stiff} for k in names],
            "n": len(Xs), "pos": b64(Xs.astype(np.float32)), "m": len(can), "vmap": b64(can.astype(np.uint16)),
            "piece": b64(pid.astype(np.uint8)), "pat": b64(np.vstack([pieces[k].V for k in names]).astype(np.float32)),
            "idx": b64(np.asarray(T, np.uint16)), "bind": {"tri": b64(tri.astype(np.uint16)), "w": b64(W.astype(np.float32))}}


def write_template(path, G, body, can, Xs, T, hood=None):
    # (a coat cut below his seat, over 90 cm, is bound to his thighs too: bound to his hips only, its skirt's points were
    # placed by triangles up to 37 cm away, far to one side of them, and the page's body, a little unlike the builder's
    # there, swung them in, so the coat narrowed below his seat into a skirt)
    body_reg = TORSO_REG + ("thigh",) if G.M["length"] > 90 else TORSO_REG
    regs_of = lambda pc: ARM_REG if pc.grp in (1, 2) else body_reg
    if G.M.get("legs"):
        # (trousers: a leg bound to that leg, from his hips down to his feet; the waistband to his waist and hips)
        regs_of = lambda pc: ("belly", "hips") if pc.name == "band" else ("belly", "hips", "thigh", "shin", "foot", "+x" if pc.name.endswith("_L") else "-x")
    out = {"v": 1, "arch": G.arch, "size": "L", "meas_cm": G.M, "scale": round(G.s, 5),
           "char": {k: v for k, v in body.char.items()},
           "about": "Made by tools/build_garments.py: sewn from flat pattern pieces and draped on Dave (CHAR_DEF, after "
                    "propWarp) in headless Blender. pos: welded points (float32 x, y, z, his warped frame; the page scales "
                    "the figure by 1/scale afterwards). Pattern points: vmap (their welded point), piece, pat (their place "
                    "on the flat pattern in metres: x round, y up from the hem), idx (triangles over them, uint16). bind: "
                    "each welded point's body triangle (data/body.json idx) and b, c, h: X = (1-b-c) A + b B + c C + h n, "
                    "n the unit normal cross(B-A, C-A). hood.pins: hood point, garment point it is sewn to."}
    out.update(template(G.P, can, Xs, T, body, regs_of))
    if hood is not None:
        Xd, Th, canh, offh, pin, pg = hood
        Th_un = np.vstack([G.hood[k].T + offh[k] for k in G.hood])
        out["hood"] = template(G.hood, canh, Xd, Th_un, body, lambda pc: TORSO_REG)
        out["hood"]["pins"] = b64(np.stack([pin, pg], 1).astype(np.uint16))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(out, open(path, "w"), separators=(",", ":"))
    print("  wrote %s (%.0f KB)" % (os.path.relpath(path, ROOT), os.path.getsize(path) / 1024), flush=True)


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    ap = argparse.ArgumentParser()
    ap.add_argument("--mh", default=os.path.expanduser("~/.cache/wardrobe-mh"))
    ap.add_argument("--out", default=os.path.join(ROOT, "data", "garments"))
    ap.add_argument("--only", default="")
    ap.add_argument("--frames", type=float, default=1.0)
    ap.add_argument("--debug", default="")
    ap.add_argument("--hold", type=float, default=0, help="frames the cloth settles at each pose before the next")
    ap.add_argument("--bending", type=float, default=0.5)
    ap.add_argument("--start", type=int, default=0, help="the A-pose the cloth is placed and first draped in (0: 40 degrees, 1: 30, 2: 20, 3: 12)")
    ap.add_argument("--apose-only", action="store_true", help="drape in the A-pose only (a quick look)")
    ap.add_argument("--reuse", action="store_true", help="with --debug: take the draped garment from the last run (to try the hood)")
    ap.add_argument("--hood-bending", type=float, default=0.5)
    ap.add_argument("--mass", type=float, default=0.3, help="kg per point")
    ap.add_argument("--tension", type=float, default=15.0)
    ap.add_argument("--friction", type=float, default=8.0, help="the cloth's friction on his body")
    a = ap.parse_args(argv)
    BB.fetch_assets(a.mh)
    body = Body(a.mh)
    # (the page scales the warped figure back up to his height: a template metre is this much of a real one)
    top = body.PW(np.array([[0, 1.79, 0.0]]), np.array([False]), body.hz)[0][1] if body.PW else 1.79
    scale = 1 / ((body.char.get("height", 183) / 183) * 1.79 / top)
    print("body ready: %d vertices, cloth scale %.4f" % (body.n, scale), flush=True)
    archs = [x for x in (a.only.split(",") if a.only else list(MEAS) + ["scarf"]) if x]
    F0 = lambda f: max(2, int(round(f * a.frames)))
    if "scarf" in archs:
        archs.remove("scarf"); drape_scarf(body, a, F0, scale)
    for arch in archs:
        legs = bool(MEAS[arch].get("legs"))
        G = Trousers(arch, scale, body) if legs else Garment(arch, scale)
        cnt = seam_counts(G.S + (hood_seams(G) if G.hood else []), {**G.P, **(G.hood or {})})
        for pc in list(G.P.values()) + list((G.hood or {}).values()): mesh_piece(pc, cnt)
        print(arch, {k: len(v.V) for k, v in G.P.items()}, flush=True)
        X = place_legs(G, G.P, body) if legs else place(G, G.P, body, a.start)
        pairs, off = close_seams(G.P, X, G.S)
        P0 = body.rel if legs else body.apose[a.start]; N0 = vnormals(P0, body.idx)
        if legs:
            # (trousers are draped on his relaxed body, his arms left out: his hands hang beside his thighs, and
            # kept out of them the trousers stood off his legs there)
            P0, N0 = P0[~body.armMask], N0[~body.armMask]
        allX = np.vstack([X[k] for k in G.P]); T = np.vstack([G.P[k].T + off[k] for k in G.P])
        print("  pushed out", push_out(allX, P0, N0), "points", flush=True)
        if a.debug:
            gap = np.array([np.linalg.norm(allX[i] - allX[j]) for i, j in pairs])
            print("  sewing gaps: mean %.4f max %.4f" % (gap.mean(), gap.max()), flush=True)
            lines = [list(allX[i]) + list(allX[j]) for i, j in pairs]
            debug_json(os.path.join(a.debug, arch + "-placed.json"), body, body.rel if legs else P0, [(arch, allX, T, "#7a2a30")], lines)
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
        # every piece must face outward once sewn: two triangles either side of an edge run it opposite ways
        way = {}
        for t in range(len(Tw)):
            for k in range(3):
                i, j = Tw[t, k], Tw[t, (k + 1) % 3]; way.setdefault((min(i, j), max(i, j)), []).append(i < j)
        flip = sum(1 for v in way.values() if len(v) == 2 and v[0] == v[1])
        if flip: raise SystemExit("%d sewn edges join pieces facing opposite ways: mirror one of them" % flip)
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
        over = None
        if "lapel" in G.M or G.M.get("leaf", 0) >= 8:
            # (a lapel kept out over the front, the back and the stand while it is eased: eased freely, its lower end
            # went in under the front, where the two lie close. So is a big collar's leaf lying out over his shoulders,
            # an aviator's: eased freely, the jacket's back and shoulders came through it in patches)
            on = {k: np.zeros(nw, bool) for k in G.P}
            for k in G.P: on[k][can[off[k]:off[k] + len(G.P[k].V)]] = True
            body_on = on["back"] | on["collar"] | np.any([on[k] for k in G.P if k.startswith("front")], axis=0)
            over = (np.where(on["leaf"] & ~body_on)[0], np.where(body_on & ~on["leaf"])[0], Tw)
        print("  eased to the pattern: edge/pattern 5%% %.3f, median %.3f, 95%% %.3f" % tuple(relax(Xw, E, R, P0, N0, over=over)), flush=True)
        if a.debug:
            debug_json(os.path.join(a.debug, arch + "-relaxed.json"), body, body.rel if legs else P0, [(arch, Xw, Tw, "#7a2a30")])
            pid = np.concatenate([np.full(len(G.P[k].V), i) for i, k in enumerate(G.P)])
            np.savez(os.path.join(a.debug, arch + "-weld.npz"), can=can, Vpat=Vpat, pid=pid, names=np.array(list(G.P)), T=T, Tw=Tw, E=E, R=R, Xw=Xw)
        # the drape under gravity, then his arms come down to his relaxed pose
        F = lambda f: max(2, int(round(f * a.frames)))
        step, hold = F(14), (F(a.hold) if a.hold else 0)
        poses = body.apose[a.start:a.start + 1] if a.apose_only else body.apose[a.start:] + [body.rel]
        pf = [F(24) + i * (step + hold) for i in range(len(poses))]
        frames = pf[-1] + F(30)
        cache = os.path.join(a.debug, arch + "-draped.npy") if a.debug else ""
        if a.reuse and os.path.exists(cache):
            Xs = np.load(cache); print("  draped garment from", cache, flush=True)
            hood = drape_hood(G, body, can, off, Xs, Tw, a, F) if G.hood else None
            write_template(os.path.join(a.out, arch + ".json"), G, body, can, Xs, T, hood)
            continue
        clear_scene()
        if legs:
            # (trousers: his relaxed body without his arms as the collider, the waistband held where it was eased to,
            # the legs let fall)
            keep = ~np.any(body.armMask[body.idx], axis=1)
            bo = new_obj("dave", body.rel, body.idx[keep]); bo.modifiers.new("collide", "COLLISION")
            bo.collision.thickness_outer = 0.003; bo.collision.thickness_inner = 0.02; bo.collision.cloth_friction = a.friction; bo.collision.damping = 0.1
            pins = np.unique(can[off["band"]:off["band"] + len(G.P["band"].V)])
            frames = F(70)
            co = cloth_obj(arch, Xw, Tw, None, [], pins=pins, frames=frames, bending=a.bending, mass=a.mass, tension=a.tension)

            def snap(f, X):
                if a.debug: debug_json(os.path.join(a.debug, "%s-f%03d.json" % (arch, f)), body, body.rel, [(arch, X[0], Tw, "#7a2a30")])
            snap.at = {int(f) for f in os.environ.get("GB_SNAPS", "").split(",") if f}
            Xs, = run(frames, [co], arch, snap)
            st = np.linalg.norm(Xs[E[:, 0]] - Xs[E[:, 1]], axis=1) / R
            print("  draped: edge/pattern 5%% %.3f, median %.3f, 95%% %.3f" % tuple(np.percentile(st, [5, 50, 95])), flush=True)
            if a.debug: debug_json(os.path.join(a.debug, arch + "-draped.json"), body, body.rel, [(arch, Xs, Tw, "#7a2a30")])
            write_template(os.path.join(a.out, arch + ".json"), G, body, can, Xs, T)
            continue
        bo = body_obj(body, poses, pf, hold, a.friction)
        stw = np.zeros(nw); np.maximum.at(stw, can, np.concatenate([np.full(len(G.P[k].V), G.P[k].stiff) for k in G.P]))
        co = cloth_obj(arch, Xw, Tw, None, [], stiff=stw, frames=frames, bending=a.bending, mass=a.mass, tension=a.tension)

        def snap(f, X):
            if a.debug: debug_json(os.path.join(a.debug, "%s-f%03d.json" % (arch, f)), body, poses[max(0, min(len(poses) - 1, sum(1 for q in pf if q <= f) - 1))], [(arch, X[0], Tw, "#7a2a30")])
        snap.at = set(pf) | {int(f) for f in os.environ.get("GB_SNAPS", "").split(",") if f}
        Xs, = run(frames, [co], arch, snap)
        st = np.linalg.norm(Xs[E[:, 0]] - Xs[E[:, 1]], axis=1) / R
        print("  draped: edge/pattern 5%% %.3f, median %.3f, 95%% %.3f" % tuple(np.percentile(st, [5, 50, 95])), flush=True)
        if a.debug:
            debug_json(os.path.join(a.debug, arch + "-draped.json"), body, poses[-1], [(arch, Xs, Tw, "#7a2a30")])
            if not a.apose_only: np.save(cache, Xs)
        if a.apose_only: continue
        hood = drape_hood(G, body, can, off, Xs, Tw, a, F) if G.hood else None
        write_template(os.path.join(a.out, arch + ".json"), G, body, can, Xs, T, hood)

main()
