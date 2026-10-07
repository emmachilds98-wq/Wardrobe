"""Lists the outfits a change touches, for the pull-request 3D check (.github/workflows/check-3d.yml).

An outfit is touched when it is new or its entry changed in data/outfits*.json, or when it uses an item whose
correction in data/fixes.json, or whose entry in data/items*.json, changed. The base is a git ref (the branch the
pull request goes into). Prints one id per line, at most --max of them (a spread, when there are more).

    python3 tools/qa/changed_outfits.py origin/main [--max 60]
"""
import argparse, glob, json, os, re, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def order(names, stem):
    """data/<stem>.json first, then data/<stem>-*.json in name order (as the build merges them)."""
    main_f = "data/%s.json" % stem
    return [n for n in names if n == main_f] + sorted(n for n in names if re.fullmatch(r"data/%s-.+\.json" % re.escape(stem), n))


def merged(texts):
    out = {}
    for t in texts:
        try:
            for k, v in json.loads(t or "{}").items():
                out.setdefault(k, v)
        except ValueError:
            pass
    return out


def at_ref(ref, stem):
    """The merged files for stem as they were at ref."""
    names = subprocess.run(["git", "ls-tree", "--name-only", ref, "data/"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    return merged(subprocess.run(["git", "show", ref + ":" + n], cwd=ROOT, capture_output=True, text=True).stdout for n in order(names, stem))


def now(stem):
    names = [os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, "data", "*.json"))]
    texts = []
    for n in order(names, stem):
        with open(os.path.join(ROOT, n), encoding="utf-8") as f:
            texts.append(f.read())
    return merged(texts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("base")
    ap.add_argument("--max", type=int, default=60)
    a = ap.parse_args()
    o0, o1 = at_ref(a.base, "outfits"), now("outfits")
    i0, i1 = at_ref(a.base, "items"), now("items")
    f0, f1 = at_ref(a.base, "fixes"), now("fixes")
    # (only what changes the drawing counts: a price or stock change does not)
    look = ("name", "cat", "fabric", "fit", "note")
    items = {k for k in set(i0) | set(i1) if {f: (i0.get(k) or {}).get(f) for f in look} != {f: (i1.get(k) or {}).get(f) for f in look}}
    items |= {k for k in set(f0) | set(f1) if not k.startswith("_") and f0.get(k) != f1.get(k)}
    ids = [k for k, o in o1.items() if o0.get(k) != o or any(p.get("item") in items for p in o.get("pieces", []))]
    if len(ids) > a.max:
        st = len(ids) / a.max
        ids = [ids[int(i * st)] for i in range(a.max)]
    print("\n".join(ids))


if __name__ == "__main__":
    main()
