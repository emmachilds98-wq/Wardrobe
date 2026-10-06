"""Builds Dave's 3D body for the page (data/body.json) from the MakeHuman base mesh.

The MakeHuman assets used here (base mesh, targets, skeleton and skin weights) are released under
CC0 by the MakeHuman project (https://github.com/makehumancommunity/makehuman, LICENSE.ASSETS.md).
No MakeHuman program code is used: this script reads the asset files itself.

What it does:
  1. Shapes a young adult man: slim, tall, average muscle (MakeHuman "macro" targets).
  2. Poses him relaxed with the skeleton and skin weights: arms down by his sides, elbows soft, feet
     under the hips, fingers loosely curled.
  3. Lines him up with the frame the clothes are drawn in (1 unit = 1 m, feet on y=0, facing +z),
     fitting his heights (ankle, knee, crotch, waist, shoulder, chin, crown) to that frame.
  4. Bakes the Edit Dave options as morph targets in the posed space: build, shoulders, middle,
     face width and nose size.
  5. Measures cross-sections of the torso, arms, legs and neck for the clothes (base and per morph),
     labels every face by body region (so clothes can hide what they cover), and records head
     landmarks (eyes, nose, mouth, ears, skull) and a face depth map for placing the moustache,
     brows, glasses and hair.

    python3 tools/build_body.py [--mh <makehuman data dir>] [--out data/body.json]
Without --mh the asset files are downloaded from GitHub into ~/.cache/wardrobe-mh.
"""
import argparse, base64, json, math, os, sys, urllib.request
import numpy as np

RAW = "https://raw.githubusercontent.com/makehumancommunity/makehuman/master/makehuman/data/"
TARGETS = {
    "male": "macrodetails/universal-male-young-averagemuscle-averageweight.target",
    "male_minw": "macrodetails/universal-male-young-averagemuscle-minweight.target",
    "male_maxw": "macrodetails/universal-male-young-averagemuscle-maxweight.target",
    "male_maxm": "macrodetails/universal-male-young-maxmuscle-averageweight.target",
    "male_minm": "macrodetails/universal-male-young-minmuscle-averageweight.target",
    "cauc": "macrodetails/caucasian-male-young.target",
    "tall": "macrodetails/height/male-young-averagemuscle-averageweight-maxheight.target",
    "ideal": "macrodetails/proportions/male-young-averagemuscle-averageweight-idealproportions.target",
    "sh_incr": "measure/measure-shoulder-dist-incr.target",
    "sh_decr": "measure/measure-shoulder-dist-decr.target",
    "belly_incr": "stomach/stomach-pregnant-incr.target",
    "belly_decr": "stomach/stomach-pregnant-decr.target",
    "waist_incr": "measure/measure-underbust-circ-incr.target",
    "hips_incr": "measure/measure-hips-circ-incr.target",
    "head_w_incr": "head/head-scale-horiz-incr.target",
    "head_w_decr": "head/head-scale-horiz-decr.target",
    "nose_v_incr": "nose/nose-scale-vert-incr.target", "nose_v_decr": "nose/nose-scale-vert-decr.target",
    "nose_h_incr": "nose/nose-scale-horiz-incr.target", "nose_h_decr": "nose/nose-scale-horiz-decr.target",
    "nose_d_incr": "nose/nose-scale-depth-incr.target", "nose_d_decr": "nose/nose-scale-depth-decr.target",
    # a man's torso: a little more chest and a straighter waist, narrower hips
    "vshape": "torso/torso-vshape-incr.target", "bust_incr": "measure/measure-bust-circ-incr.target",
    "waist_c_incr": "measure/measure-waist-circ-incr.target", "hips_decr": "measure/measure-hips-circ-decr.target",
    "bust_decr": "measure/measure-bust-circ-decr.target", "waist_c_decr": "measure/measure-waist-circ-decr.target",
    "uarm_incr": "measure/measure-upperarm-circ-incr.target", "uarm_decr": "measure/measure-upperarm-circ-decr.target",
    "thigh_incr": "measure/measure-thigh-circ-incr.target", "thigh_decr": "measure/measure-thigh-circ-decr.target",
    "calf_incr": "measure/measure-calf-circ-incr.target", "calf_decr": "measure/measure-calf-circ-decr.target",
    "neck_incr": "measure/measure-neck-circ-incr.target", "neck_decr": "measure/measure-neck-circ-decr.target",
    "chinw_incr": "chin/chin-width-incr.target", "chinw_decr": "chin/chin-width-decr.target",
    "chinb_incr": "chin/chin-bones-incr.target", "chinb_decr": "chin/chin-bones-decr.target",
    "chinp_incr": "chin/chin-prominent-incr.target", "chinp_decr": "chin/chin-prominent-decr.target",
    "ulip_incr": "mouth/mouth-upperlip-volume-incr.target", "ulip_decr": "mouth/mouth-upperlip-volume-decr.target",
    "llip_incr": "mouth/mouth-lowerlip-volume-incr.target", "llip_decr": "mouth/mouth-lowerlip-volume-decr.target",
    "earl_incr": "ears/l-ear-scale-incr.target", "earl_decr": "ears/l-ear-scale-decr.target",
    "earr_incr": "ears/r-ear-scale-incr.target", "earr_decr": "ears/r-ear-scale-decr.target",
    "eyel_incr": "eyes/l-eye-scale-incr.target", "eyel_decr": "eyes/l-eye-scale-decr.target",
    "eyer_incr": "eyes/r-eye-scale-incr.target", "eyer_decr": "eyes/r-eye-scale-decr.target",
    "smile_down": "mouth/mouth-angles-down.target",
    # a relaxed, friendly expression
    "smile": "mouth/mouth-angles-up.target", "laugh": "mouth/mouth-laugh-lines-in.target",
    "cheek_l": "cheek/l-cheek-volume-incr.target", "cheek_r": "cheek/r-cheek-volume-incr.target",
    "fold_l": "eyes/l-eye-eyefold-down.target", "fold_r": "eyes/r-eye-eyefold-down.target",
    "lid_l": "eyes/l-eye-height2-decr.target", "lid_r": "eyes/r-eye-height2-decr.target",
}
FILES = ["3dobjs/base.obj", "rigs/default.mhskel", "rigs/default_weights.mhw"] + ["targets/" + t for t in TARGETS.values()]


def fetch_assets(root):
    for f in FILES:
        p = os.path.join(root, f)
        if os.path.exists(p):
            continue
        os.makedirs(os.path.dirname(p), exist_ok=True)
        print("downloading", f, flush=True)
        with urllib.request.urlopen(RAW + f, timeout=120) as r, open(p, "wb") as o:
            o.write(r.read())


def load_obj(p):
    V, F, G, g = [], [], [], None
    for line in open(p):
        if line.startswith("v "):
            V.append([float(x) for x in line.split()[1:4]])
        elif line.startswith("g "):
            g = line.split(None, 1)[1].strip()
        elif line.startswith("f "):
            F.append([int(t.split("/")[0]) - 1 for t in line.split()[1:]])
            G.append(g)
    return np.array(V), F, G


class Mesh:
    def __init__(self, root):
        self.root = root
        self.V0, self.F, self.G = load_obj(os.path.join(root, "3dobjs/base.obj"))
        self.cache = {}

    def target(self, key):
        if key not in self.cache:
            d = np.zeros_like(self.V0)
            lines = [l.split() for l in open(os.path.join(self.root, "targets", TARGETS[key])) if l.strip() and not l.startswith("#")]
            if lines:
                a = np.array(lines, float)
                d[a[:, 0].astype(int)] = a[:, 1:4]
            self.cache[key] = d
        return self.cache[key]

    def mix(self, ws):
        V = self.V0.copy()
        for k, w in ws.items():
            if w:
                V += w * self.target(k)
        return V


# ---- skeleton and posing (linear blend skinning) ----
def rot(axis, ang):
    axis = np.asarray(axis, float); axis = axis / np.linalg.norm(axis)
    x, y, z = axis; c, s = math.cos(ang), math.sin(ang); C = 1 - c
    return np.array([[c + x * x * C, x * y * C - z * s, x * z * C + y * s],
                     [y * x * C + z * s, c + y * y * C, y * z * C - x * s],
                     [z * x * C - y * s, z * y * C + x * s, c + z * z * C]])


class Rig:
    def __init__(self, root):
        S = json.load(open(os.path.join(root, "rigs/default.mhskel")))
        self.bones, self.joints = S["bones"], S["joints"]
        W = json.load(open(os.path.join(root, "rigs/default_weights.mhw")))["weights"]
        self.weights = W
        order, seen = [], set()
        def visit(b):
            if b in seen: return
            p = self.bones[b]["parent"]
            if p: visit(p)
            seen.add(b); order.append(b)
        for b in self.bones: visit(b)
        self.order = order

    def joint(self, V, name):
        return V[self.joints[name]].mean(0)

    def head(self, V, b): return self.joint(V, self.bones[b]["head"])
    def tail(self, V, b): return self.joint(V, self.bones[b]["tail"])

    def pose(self, V, rots):
        """rots: bone -> 3x3 world-axis rotation about the bone's head (applied in rest space, then the
        parent's motion). Returns the 4x4 world matrix of every bone."""
        M = {}
        for b in self.order:
            h = self.head(V, b)
            R = rots.get(b, np.eye(3))
            L = np.eye(4); L[:3, :3] = R; L[:3, 3] = h - R @ h
            p = self.bones[b]["parent"]
            M[b] = (M[p] @ L) if p else L
        return M

    def skin_matrix(self, n):
        """Per-vertex list of (bone, weight), normalised."""
        idx = [[] for _ in range(n)]
        for b, lst in self.weights.items():
            for v, w in lst:
                if v < n: idx[v].append((b, w))
        out = []
        for l in idx:
            s = sum(w for _, w in l)
            out.append([(b, w / s) for b, w in l] if s > 0 else [("root", 1.0)])
        return out


def apply_skin(V, M, skin, D=None):
    """Positions (or, with D, morph deltas which only take the rotation part) after skinning."""
    out = np.zeros_like(V)
    for i, l in enumerate(skin):
        acc = np.zeros(3)
        for b, w in l:
            m = M[b]
            acc += w * (m[:3, :3] @ (D[i] if D is not None else V[i]) + (0 if D is not None else m[:3, 3]))
        out[i] = acc
    return out


def skin_fast(V, M, skin, D=None):
    """Vectorised apply_skin: build one blended 3x4 matrix per vertex."""
    n = len(V); names = list(M.keys()); bi = {b: i for i, b in enumerate(names)}
    mats = np.stack([M[b][:3, :] for b in names])  # (B,3,4)
    W = np.zeros((n, len(names)))
    for i, l in enumerate(skin):
        for b, w in l:
            W[i, bi[b]] += w
    blend = np.einsum("nb,bij->nij", W, mats)
    if D is not None:
        return np.einsum("nij,nj->ni", blend[:, :, :3], D)
    return np.einsum("nij,nj->ni", blend[:, :, :3], V) + blend[:, :, 3]


def unit(v):
    return v / np.linalg.norm(v)


def between(a, b):
    a, b = unit(a), unit(b); ax = np.cross(a, b); s = np.linalg.norm(ax); c = float(np.dot(a, b))
    return np.eye(3) if s < 1e-9 else rot(ax, math.atan2(s, c))


def relaxed_pose(rig, V, arm_out=7.0, fore_fwd=14.0, twist=55.0, curl=(18, 28, 17)):
    """Arms hanging a little away from the body, elbows soft, backs of the hands facing out with the
    thumbs forward, fingers loosely curled, feet under the hips."""
    R = {}
    for side, sg in (("L", 1), ("R", -1)):
        sh = rig.head(V, "upperarm01." + side); el = rig.head(V, "lowerarm01." + side); wr = rig.head(V, "wrist." + side)
        a = math.radians(arm_out); tu = np.array([sg * math.sin(a), -math.cos(a), 0.0])
        Ru = between(el - sh, tu); R["upperarm01." + side] = Ru
        f = math.radians(fore_fwd); tf = unit(np.array([sg * math.sin(a) * 0.6, -math.cos(f), math.sin(f)]))
        ax = unit(wr - el); tw = math.radians(twist) * sg
        R["lowerarm01." + side] = between(wr - el, Ru.T @ tf) @ rot(ax, tw * 0.3)
        R["lowerarm02." + side] = rot(ax, tw * 0.45); R["wrist." + side] = rot(ax, tw * 0.25)
        w = rig.head(V, "wrist." + side); i1 = rig.head(V, "finger2-1." + side); p1 = rig.head(V, "finger5-1." + side); tt = rig.tail(V, "finger1-3." + side)
        n = unit(np.cross(i1 - w, p1 - w))
        if np.dot(tt - w, n) < 0: n = -n
        for fi in range(2, 6):
            for seg, ang in zip((1, 2, 3), curl):
                b = "finger%d-%d.%s" % (fi, seg, side); d = unit(rig.tail(V, b) - rig.head(V, b))
                R[b] = rot(unit(np.cross(d, n)), math.radians(ang * (0.85 + 0.1 * fi)))
        for seg, ang in ((2, 12), (3, 10)):
            b = "finger1-%d.%s" % (seg, side); d = unit(rig.tail(V, b) - rig.head(V, b)); R[b] = rot(unit(np.cross(d, n)), math.radians(ang))
        hp = rig.head(V, "upperleg01." + side); an = rig.head(V, "foot." + side)
        R["upperleg01." + side] = between(an - hp, np.array([hp[0] - sg * 0.12, an[1], an[2]]) - hp)
    return R


# Body regions, from the bone that moves each face most (clothes hide the regions they cover).
REGIONS = ["head", "neck", "chest", "belly", "hips", "uarm", "farm", "hand", "thigh", "shin", "foot"]
def region_of(bone):
    b = bone.split(".")[0]
    if b.startswith("neck"): return "neck"
    if b in ("spine01", "spine02", "spine03", "breast", "clavicle"): return "chest"
    if b in ("spine04", "spine05"): return "belly"
    if b in ("root", "pelvis"): return "hips"
    if b.startswith(("upperarm", "shoulder01")): return "uarm"
    if b.startswith("lowerarm"): return "farm"
    if b.startswith(("wrist", "metacarpal", "finger")): return "hand"
    if b.startswith("upperleg"): return "thigh"
    if b.startswith("lowerleg"): return "shin"
    if b.startswith(("foot", "toe")): return "foot"
    return "head"


# Heights the clothes are drawn through (the same as the old hand-built body, so the garment code fits).
TORSO_Y = [0.83, 0.9, 0.97, 1.05, 1.13, 1.22, 1.3, 1.37, 1.43, 1.47, 1.495, 1.515]
NECK_Y = [1.47, 1.515, 1.56, 1.61]
ARM_Y = [0.89, 0.905, 0.97, 1.05, 1.12, 1.18, 1.28, 1.38, 1.45]
LEG_Y = [0.07, 0.12, 0.22, 0.33, 0.41, 0.49, 0.56, 0.66, 0.77, 0.86, 0.92]
HAND_Y = [0.798, 0.81, 0.83, 0.87, 0.897]


def sections(P, vreg, ys, regs, side=0, band=0.012, centre_x=False, xmax=None):
    """[y, half-width, half-depth, x centre, z centre] of the vertices in regs near each height."""
    out = []
    mask = np.isin(vreg, [REGIONS.index(r) for r in regs])
    if side: mask &= (P[:, 0] * side > 0.004)
    if xmax: mask &= (np.abs(P[:, 0]) < xmax)
    Q = P[mask]
    for y in ys:
        b = band
        while True:
            S = Q[np.abs(Q[:, 1] - y) < b]
            if len(S) >= 12 or b > 0.06: break
            b *= 1.6
        if len(S) < 3:
            out.append(None); continue
        x0, x1 = np.percentile(S[:, 0], [1, 99]); z0, z1 = np.percentile(S[:, 2], [1, 99])
        if centre_x:
            out.append([y, (x1 - x0) / 2, (z1 - z0) / 2, (x1 + x0) / 2, (z1 + z0) / 2])
        else:
            out.append([y, max(abs(x0), abs(x1)), (z1 - z0) / 2, 0.0, (z1 + z0) / 2])
    # fill gaps from neighbours
    for i, s in enumerate(out):
        if s is None:
            nb = [out[j] for j in (i - 1, i + 1) if 0 <= j < len(out) and out[j] is not None]
            out[i] = [ys[i]] + list(np.mean([n[1:] for n in nb], 0)) if nb else [ys[i], 0.02, 0.02, 0, 0]
    return [[round(float(v), 4) for v in s] for s in out]


def face_depth(P, tris, sel, x0, x1, y0, y1, step):
    """Front surface of the head: the largest z over a grid of (x, y), by rasterising its triangles."""
    nx = int(round((x1 - x0) / step)) + 1; ny = int(round((y1 - y0) / step)) + 1
    Z = np.full((ny, nx), np.nan)
    for t in tris[sel]:
        A, B, C = P[t[0]], P[t[1]], P[t[2]]
        xs = [A[0], B[0], C[0]]; ys = [A[1], B[1], C[1]]
        i0 = max(0, int(math.floor((min(xs) - x0) / step))); i1 = min(nx - 1, int(math.ceil((max(xs) - x0) / step)))
        j0 = max(0, int(math.floor((min(ys) - y0) / step))); j1 = min(ny - 1, int(math.ceil((max(ys) - y0) / step)))
        if i1 < i0 or j1 < j0: continue
        det = (B[1] - C[1]) * (A[0] - C[0]) + (C[0] - B[0]) * (A[1] - C[1])
        if abs(det) < 1e-12: continue
        gx, gy = np.meshgrid(x0 + np.arange(i0, i1 + 1) * step, y0 + np.arange(j0, j1 + 1) * step)
        l1 = ((B[1] - C[1]) * (gx - C[0]) + (C[0] - B[0]) * (gy - C[1])) / det
        l2 = ((C[1] - A[1]) * (gx - C[0]) + (A[0] - C[0]) * (gy - C[1])) / det
        l3 = 1 - l1 - l2
        inside = (l1 >= -1e-6) & (l2 >= -1e-6) & (l3 >= -1e-6)
        z = l1 * A[2] + l2 * B[2] + l3 * C[2]
        sub = Z[j0:j1 + 1, i0:i1 + 1]
        upd = inside & (np.isnan(sub) | (z > sub))
        sub[upd] = z[upd]
    return Z


def bake_ao(P, tris, vreg, nv):
    """Soft shading baked into the skin: darker in creases and hollows (eye sockets, nostrils, ears,
    lips, between the fingers) from the surface's curvature, and where the body faces itself (inner
    arms and torso sides, inner thighs). 1 is fully lit."""
    n = len(P)
    N = np.zeros_like(P)
    a, b, c = P[tris[:, 0]], P[tris[:, 1]], P[tris[:, 2]]
    fn = np.cross(b - a, c - a)
    for k in range(3): np.add.at(N, tris[:, k], fn)
    N /= np.linalg.norm(N, axis=1, keepdims=True) + 1e-12
    S = np.zeros_like(P); cnt = np.zeros(n)
    for i, j in ((0, 1), (1, 2), (2, 0), (1, 0), (2, 1), (0, 2)):
        np.add.at(S, tris[:, i], P[tris[:, j]]); np.add.at(cnt, tris[:, i], 1)
    L = S / np.maximum(cnt, 1)[:, None] - P
    curv = np.einsum("ij,ij->i", L, N)                          # > 0 where the surface is hollow
    edge = np.linalg.norm(L, axis=1) + 1e-6
    cav = np.clip(curv / edge, -1, 1)
    for _ in range(3):                                          # spread a little so creases read softly
        S2 = np.zeros(n); np.add.at(S2, tris.ravel(), np.repeat(cav[tris].mean(1), 3)); c2 = np.zeros(n); np.add.at(c2, tris.ravel(), 1)
        cav = 0.5 * cav + 0.5 * S2 / np.maximum(c2, 1)
    headv = vreg == REGIONS.index("head")
    ao = 1 - np.where(headv, 0.95, 0.55) * np.clip(cav, 0, 0.6)          # the face's creases read more strongly
    R_ = {r: REGIONS.index(r) for r in REGIONS}
    side = np.sign(P[:, 0])
    inward = np.clip(-N[:, 0] * side, 0, 1)
    arm = np.isin(vreg, [R_["uarm"], R_["farm"]]) & (P[:, 1] > 0.95)
    ao[arm] *= 1 - 0.22 * inward[arm] ** 1.5
    tors = np.isin(vreg, [R_["chest"], R_["belly"]]) & (P[:, 1] > 1.05) & (P[:, 1] < 1.42)
    ao[tors] *= 1 - 0.18 * np.clip(np.abs(N[tors, 0]) - 0.4, 0, 1) / 0.6
    thigh = (vreg == R_["thigh"]) & (P[:, 1] > 0.55)
    ao[thigh] *= 1 - 0.2 * inward[thigh] ** 1.5
    return np.clip(ao, 0.45, 1)


def b64(a):
    return base64.b64encode(np.ascontiguousarray(a).tobytes()).decode()


BASE_MIX = {"male": 1, "male_minw": 0.25, "cauc": 1, "tall": 0.45, "ideal": 0.5,
            "vshape": 0.2, "bust_incr": 0.12, "waist_c_incr": 0.05, "hips_decr": 0.35,
            "smile": 0.55, "laugh": 0.3, "cheek_l": 0.1, "cheek_r": 0.1, "fold_l": 0.3, "fold_r": 0.3, "lid_l": 0.2, "lid_r": 0.2}
# Edit Dave's sliders: each runs from -1 to 1, using the "_n" morph below zero and the "_p" morph above it.
SLIDERS = {
    "weight": ({"male_minw": 0.75}, {"male_maxw": 0.8}),
    "muscle": ({"male_minm": 0.8}, {"male_maxm": 0.8}),
    "shoulderW": ({"sh_decr": 1}, {"sh_incr": 1}),
    "chest": ({"bust_decr": 0.8}, {"bust_incr": 0.8}),
    "waistW": ({"waist_c_decr": 0.8}, {"waist_c_incr": 0.8}),
    "belly": ({"belly_decr": 0.8}, {"belly_incr": 0.8}),
    "hips": ({"hips_decr": 0.6}, {"hips_incr": 0.8}),
    "arms": ({"uarm_decr": 0.8}, {"uarm_incr": 0.8}),
    "legs": ({"thigh_decr": 0.8, "calf_decr": 0.6}, {"thigh_incr": 0.8, "calf_incr": 0.6}),
    "neckW": ({"neck_decr": 0.8}, {"neck_incr": 0.8}),
    "faceW": ({"head_w_decr": 0.6}, {"head_w_incr": 0.6}),
    "jaw": ({"chinw_decr": 0.7, "chinb_decr": 0.4}, {"chinw_incr": 0.7, "chinb_incr": 0.4}),
    "chin": ({"chinp_decr": 0.7}, {"chinp_incr": 0.7}),
    "noseSize": ({"nose_v_decr": 0.5, "nose_h_decr": 0.4, "nose_d_decr": 0.5}, {"nose_v_incr": 0.5, "nose_h_incr": 0.45, "nose_d_incr": 0.55}),
    "lips": ({"ulip_decr": 0.7, "llip_decr": 0.7}, {"ulip_incr": 0.7, "llip_incr": 0.7}),
    "ears": ({"earl_decr": 0.6, "earr_decr": 0.6}, {"earl_incr": 0.6, "earr_incr": 0.6}),
    "eyeSize": ({"eyel_decr": 0.5, "eyer_decr": 0.5}, {"eyel_incr": 0.5, "eyer_incr": 0.5}),
    "smile": ({"smile_down": 0.5}, {"smile": 0.45}),
}
MORPHS = {}
for _k, (_n, _p) in SLIDERS.items():
    MORPHS[_k + "_n"] = _n; MORPHS[_k + "_p"] = _p
CROWN = 1.79   # top of the skull in the clothes' frame (the hair adds the rest of his height)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mh", default=os.path.expanduser("~/.cache/wardrobe-mh"))
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "body.json"))
    a = ap.parse_args()
    fetch_assets(a.mh)
    mesh, rig = Mesh(a.mh), Rig(a.mh)
    V = mesh.mix(BASE_MIX)
    M = rig.pose(V, relaxed_pose(rig, V))
    skin = rig.skin_matrix(len(V))
    P = skin_fast(V, M, skin)

    body = [f for f, g in zip(mesh.F, mesh.G) if g == "body"]
    tris = []
    for f in body:
        tris += [[f[0], f[1], f[2]], [f[0], f[2], f[3]]] if len(f) == 4 else [f]
    tris = np.array(tris)
    used = np.unique(tris); remap = -np.ones(len(V), int); remap[used] = np.arange(len(used))
    # frame: feet on y=0, skull top at CROWN, metres
    y0 = P[used, 1].min(); s = CROWN / (P[used, 1].max() - y0)
    def frame(X): return (X - np.array([0, y0, 0])) * s
    Pf = frame(P)

    # regions: per vertex (dominant bone) and per triangle (most common among its corners)
    vreg = np.array([REGIONS.index(region_of(max(l, key=lambda t: t[1])[0])) for l in skin])
    treg = np.array([np.bincount(vreg[t], minlength=len(REGIONS)).argmax() for t in tris])

    # Edit Dave options as morphs, carried into the pose by the bones' rotations
    morphs, msec, morph_d = {}, {}, {}
    ur = vreg[used]
    def measure(X):
        X = X[used]
        # the torso below the waist includes the tops of the thighs (the hips are as wide as both)
        lowT = [y for y in TORSO_Y if y < 1.0]; upT = [y for y in TORSO_Y if y >= 1.0]
        return {"torso": sections(X, ur, lowT, ["belly", "hips", "thigh"]) + sections(X, ur, upT, ["chest", "belly", "hips", "neck"]),
                "neck": sections(X, ur, NECK_Y, ["neck", "chest", "head"], xmax=0.066),
                "arm": sections(X, ur, ARM_Y, ["uarm", "farm", "hand"], side=1, centre_x=True),
                "hand": sections(X, ur, HAND_Y, ["hand"], side=1, centre_x=True),
                "leg": sections(X, ur, LEG_Y, ["thigh", "shin", "foot"], side=1, centre_x=True)}
    base_sec = measure(Pf)
    for name, mix in MORPHS.items():
        D = sum(w * mesh.target(k) for k, w in mix.items())
        Dp = skin_fast(V, M, skin, D) * s
        morph_d[name] = Dp
        idx = np.where(np.abs(Dp[used]).max(1) > 1.2e-4)[0]
        morphs[name] = {"i": b64(idx.astype(np.uint16)), "d": b64(np.round(Dp[used][idx] * 1e4).astype(np.int16))}
        ms = measure(Pf + Dp)
        msec[name] = {k: [[round(m[j] - b[j], 4) for j in range(1, 5)] for m, b in zip(ms[k], base_sec[k])] for k in ms}

    # landmarks
    def grp(name):
        fs = [f for f, g in zip(mesh.F, mesh.G) if g == name]
        return np.unique(np.concatenate([np.array(f) for f in fs]))
    eyev = grp("helper-l-eye")
    ec0 = Pf[eyev].mean(0)
    fx0, fx1, fy0, fy1, st = -0.08, 0.08, ec0[1] - 0.115, ec0[1] + 0.075, 0.0025
    hsel = (treg == REGIONS.index("head")) | (treg == REGIONS.index("neck"))
    def face_lm(PX):
        """eyes, nose, mouth, chin, crown, skull and ear from positions PX (all vertices), and the face depth map"""
        E = PX[eyev]; ec = E.mean(0); er = float(np.linalg.norm(E - ec, axis=1).mean())
        head = used[vreg[used] == REGIONS.index("head")]; H = PX[head]
        crown = float(H[:, 1].max())
        Z = face_depth(PX, tris, hsel, fx0, fx1, fy0, fy1, st)
        prof = [(fy0 + j * st, float(Z[j, int(round(-fx0 / st))])) for j in range(Z.shape[0])]
        prof = [p for p in prof if not np.isnan(p[1])]
        tip = max((p for p in prof if ec[1] - 0.09 < p[0] < ec[1] - 0.015), key=lambda p: p[1])   # nose tip
        down = [p for p in sorted(prof, key=lambda p: -p[0]) if p[0] < tip[0]]
        def turn(seq, want_min):
            """the first local minimum (or maximum) walking down the profile, ignoring flat steps"""
            best = seq[0]
            for p in seq[1:]:
                if (p[1] < best[1] - 1e-5) if want_min else (p[1] > best[1] + 1e-5): best = p
                elif (p[1] > best[1] + 0.0008) if want_min else (p[1] < best[1] - 0.0008): break
            return best
        sn = turn(down, True)                                       # under the nose
        ul = turn([p for p in down if p[0] < sn[0]], False)         # upper lip
        mo = turn([p for p in down if p[0] < ul[0]], True)          # the line between the lips
        cranium = H[H[:, 1] > ec[1] + 0.03]
        # the skull as an ellipsoid in the hair's unit frame: the eyes sit at y=0.1 and the crown at 0.95
        ax = float(np.abs(cranium[:, 0]).max()) * 1.08; zf, zb = float(cranium[:, 2].max()), float(cranium[:, 2].min())
        ay = (crown - ec[1]) / 0.85; cy = ec[1] - 0.1 * ay
        earband = H[(H[:, 1] > ec[1] - 0.035) & (H[:, 1] < ec[1] + 0.005)]
        ear = earband[np.argmax(earband[:, 0])]
        r4 = lambda v: round(float(v), 4)
        return {"eye": [r4(v) for v in ec] + [r4(er)], "noseTip": [r4(tip[0]), r4(tip[1])], "noseBase": [r4(sn[0]), r4(sn[1])],
                "mouth": [r4(mo[0]), r4(mo[1]), 0.024], "chin": r4(H[H[:, 2] > ec[2] - 0.02][:, 1].min()), "crown": r4(crown),
                "skull": [r4(cy), r4((zf + zb) / 2), r4(ax / 0.94), r4(ay), r4((zf - zb) / 2 / 0.94)], "ear": [r4(v) for v in ear]}, Z
    flm, Z = face_lm(Pf)
    # how each Edit Dave slider moves those landmarks (the page adds these, weighted)
    lmd = {}
    for name, Dp in morph_d.items():
        m_lm, _ = face_lm(Pf + Dp)
        d = {}
        for k in ("eye", "noseTip", "noseBase", "mouth", "skull", "ear"):
            dv = [round(x - y, 4) for x, y in zip(m_lm[k], flm[k])]
            if any(abs(v) > 2e-4 for v in dv): d[k] = dv
        for k in ("chin", "crown"):
            if abs(m_lm[k] - flm[k]) > 2e-4: d[k] = round(m_lm[k] - flm[k], 4)
        if d: lmd[name] = d
    feet = Pf[used[(vreg[used] == REGIONS.index("foot")) & (Pf[used, 0] > 0)]]
    hands = Pf[used[(vreg[used] == REGIONS.index("hand")) & (Pf[used, 0] > 0)]]
    hipsv = Pf[used[np.isin(vreg[used], [REGIONS.index("hips"), REGIONS.index("thigh")]) & (np.abs(Pf[used, 0]) < 0.012)]]
    tor = base_sec["torso"]; waist = min((t for t in tor if 0.95 < t[0] < 1.25), key=lambda t: t[1])
    wrist = (M["wrist.L"] @ np.r_[rig.head(V, "wrist.L"), 1])[:3]
    lm = dict(flm)
    lm.update({
        "wrist": [round(float(v), 4) for v in frame(wrist[None])[0]],
        "foot": {"x": round(float(feet[:, 0].mean()), 4), "heel": round(float(feet[:, 2].min()), 4), "toe": round(float(feet[:, 2].max()), 4),
                 "w": round(float(feet[:, 0].max() - feet[:, 0].min()) / 2, 4), "top": round(float(feet[:, 1].max()), 4)},
        "hand": {"bottom": round(float(hands[:, 1].min()), 4), "top": round(float(hands[:, 1].max()), 4)},
        "crotch": round(float(hipsv[:, 1].min()), 4) if len(hipsv) else 0.84,
        "waist": round(waist[0], 4), "shoulder": base_sec["arm"][-1][:4],
    })
    zq = np.where(np.isnan(Z), -32768, np.round(Z * 1e4)).astype(np.int16)
    ao = bake_ao(Pf[used], remap[tris], vreg[used], len(used))
    out = {
        "v": 1, "license": "Body from the MakeHuman base mesh, targets, skeleton and weights (CC0, makehumancommunity.org); shaped, posed and measured by tools/build_body.py.",
        "n": int(len(used)), "pos": b64(Pf[used].astype(np.float32)), "idx": b64(remap[tris].astype(np.uint16)),
        "treg": b64(treg.astype(np.uint8)), "ao": b64(np.round(ao * 255).astype(np.uint8)), "regions": REGIONS, "morphs": morphs,
        "sec": base_sec, "secd": msec, "lm": lm, "lmd": lmd, "sliders": list(SLIDERS),
        "face": {"x0": fx0, "y0": round(float(fy0), 4), "st": st, "nx": int(Z.shape[1]), "ny": int(Z.shape[0]), "z": b64(zq)},
    }
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w") as f:
        json.dump(out, f, separators=(",", ":"))
    print("wrote", a.out, os.path.getsize(a.out) // 1024, "KB;", len(used), "vertices,", len(tris), "triangles")
    print(json.dumps(lm, indent=1))
    for k in ("torso", "arm", "leg", "neck"):
        print(k, base_sec[k])


if __name__ == "__main__":
    main()
