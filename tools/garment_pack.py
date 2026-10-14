"""The garment templates' compact storage (data/garments/<kind>.json, "v": 2), written by tools/build_garments.py.

Every array in a template is uint16, stored column by column (all x, then all y, then all z), each column as the
step from the one before it (mod 65536), then base64. The steps are what make it small on the wire: the pattern
points and the triangles over them run in order, so their steps are small numbers that gzip packs tightly. A float
array (pos, pat, bind.w) is quantised first, each column over its own range: value = o[c] + q * s[c], s[c] = range /
65535, which is about 0.03 mm for a point 2 m tall and well under a micron for the binding's heights off his body.
A packed array is {"k": columns, "d": base64, and for floats "o", "s"}; a plain base64 string is the older "v": 1
form (float32 or the array's own integer type) and the page reads either.

Run on its own it converts data/garments from "v": 1 in place (no Blender needed) and prints the sizes, plain and
gzipped, and the largest difference in any array and in any point rebuilt on his body as the page rebuilds it:

    python3 tools/garment_pack.py [--dir data/garments] [--check]

--check only reports (on files already packed, the difference against the float32 they came from is not known).
"""
import argparse, base64, glob, gzip, json, os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
# (the template's arrays: name, columns, float or integer, the page's type for it)
FIELDS = [("pos", 3, np.float32), ("pat", 2, np.float32), ("vmap", 1, np.uint16), ("piece", 1, np.uint8),
          ("idx", 3, np.uint16), ("bind.tri", 1, np.uint16), ("bind.w", 3, np.float32), ("pins", 2, np.uint16)]


def b64(a):
    return base64.b64encode(np.ascontiguousarray(a).tobytes()).decode()


def pack(a, k):
    """one array as the compact form: a (n x k, or flat) float or integer array"""
    a = np.asarray(a).reshape(-1, k)
    out = {"k": k}
    if np.issubdtype(a.dtype, np.floating):
        a = a.astype(np.float64); lo = a.min(0) if len(a) else np.zeros(k); st = ((a.max(0) if len(a) else lo) - lo) / 65535
        st[st == 0] = 1
        q = np.round((a - lo) / st).astype(np.int64)
        out["o"] = [float(v) for v in lo]; out["s"] = [float(v) for v in st]
    else:
        q = a.astype(np.int64)
        if len(q) and (q.min() < 0 or q.max() > 65535): raise ValueError("an integer array outside uint16")
    d = np.diff(q.T, axis=1, prepend=0) % 65536
    out["d"] = b64(d.astype(np.uint16))
    return out


def unpack(v, dt):
    """either form back to an n x k array of the page's type (floats as the page has them: float32)"""
    if isinstance(v, str):
        return np.frombuffer(base64.b64decode(v), dtype=dt)
    k = v["k"]; d = np.frombuffer(base64.b64decode(v["d"]), dtype=np.uint16).astype(np.int64).reshape(k, -1)
    q = (np.cumsum(d, axis=1) % 65536).T
    if "o" in v:
        return (np.array(v["o"]) + q * np.array(v["s"])).astype(np.float32).reshape(-1)
    return q.astype(dt).reshape(-1)


def _get(d, name):
    o = d
    for p in name.split("."): o = o.get(p) if isinstance(o, dict) else None
    return o


def _set(d, name, v):
    ps = name.split("."); o = d
    for p in ps[:-1]: o = o[p]
    o[ps[-1]] = v


def pack_part(d):
    """a template (or its hood) packed in place"""
    for name, k, dt in FIELDS:
        v = _get(d, name)
        if v is not None: _set(d, name, pack(unpack(v, dt), k))
    return d


def rebuild(t, BP, I):
    """each welded point placed on his body as the page's drapeBind does (sx 1): X = (1-b-c) A + b B + c C + h n"""
    tri = unpack(t["bind"]["tri"], np.uint16).astype(np.int64); w = unpack(t["bind"]["w"], np.float32).reshape(-1, 3).astype(np.float64)
    A, B, C = (BP[I[tri * 3 + j]] for j in range(3))
    n = np.cross(B - A, C - A); n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-30)
    wb, wc, h = w[:, :1], w[:, 1:2], w[:, 2:3]
    return (1 - wb - wc) * A + wb * B + wc * C + h * n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=os.path.join(ROOT, "data", "garments"))
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    body = json.load(open(os.path.join(ROOT, "data", "body.json")))
    BP = np.frombuffer(base64.b64decode(body["pos"]), np.float32).reshape(-1, 3).astype(np.float64)
    I = np.frombuffer(base64.b64decode(body["idx"]), np.uint16).astype(np.int64)
    tot = [0, 0, 0, 0]; worst = {"array": 0.0, "point": 0.0}
    for f in sorted(glob.glob(os.path.join(a.dir, "*.json"))):
        s0 = open(f).read(); d0 = json.loads(s0); d = json.loads(s0)
        parts = [(d0, d)] + ([(d0["hood"], d["hood"])] if "hood" in d else [])
        for p0, p in parts: pack_part(p)
        d["v"] = 2
        if "about" in d:   # (the note in the file says how it is stored, as tools/build_garments.py writes it now)
            d["about"] = d["about"].replace("(float32 x, y, z,", "(x, y, z,").replace("idx (triangles over them, uint16)", "idx (triangles over them)") + \
                " Every array is packed as tools/garment_pack.py says (uint16, column by column, each the step from the one " \
                "before; floats quantised over each column's range, value = o + q s)."
        s = json.dumps(d, separators=(",", ":"))
        # (how far any value and any rebuilt point moved: float32 before, the packed form as the page decodes it)
        da = dp = 0.0
        for p0, p in parts:
            for name, k, dt in FIELDS:
                v0, v = _get(p0, name), _get(p, name)
                if v0 is None: continue
                x0, x = unpack(v0, dt).astype(np.float64), unpack(v, dt).astype(np.float64)
                if x0.shape != x.shape: raise SystemExit("%s %s: the packed array has another length" % (f, name))
                if not np.issubdtype(dt, np.floating) and not np.array_equal(x0, x): raise SystemExit("%s %s: integers changed" % (f, name))
                if name in ("pos", "pat"): da = max(da, float(np.abs(x0 - x).max()))
            dp = max(dp, float(np.abs(rebuild(p0, BP, I) - rebuild(p, BP, I)).max()))
        worst["array"] = max(worst["array"], da); worst["point"] = max(worst["point"], dp)
        z0, z = len(gzip.compress(s0.encode(), 9)), len(gzip.compress(s.encode(), 9))
        if d0.get("v", 1) >= 2: s, z = s0, z0
        row = [len(s0), z0, len(s), z]; tot = [x + y for x, y in zip(tot, row)]
        print("%-16s %8d -> %8d bytes, gzipped %8d -> %8d; pos/pat %.4f mm, rebuilt points %.4f mm"
              % (os.path.basename(f), row[0], row[2], row[1], row[3], 1000 * da, 1000 * dp))
        if not a.check and d0.get("v", 1) < 2:
            open(f, "w").write(s)
    print("%-16s %8d -> %8d bytes (%.2f), gzipped %8d -> %8d (%.2f); largest difference: pos/pat %.4f mm, rebuilt points %.4f mm"
          % ("all", tot[0], tot[2], tot[2] / tot[0], tot[1], tot[3], tot[3] / tot[1], 1000 * worst["array"], 1000 * worst["point"]))


if __name__ == "__main__":
    main()
