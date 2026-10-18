"""Compares two files of shipped photo readings (data/looks.json, written by tools/specs.js): whether the readings the
page takes as read still match what the readers make of the photos.

    python3 tools/qa/looks_diff.py data/looks.json new.json [--ci]

Colours count as changed when they move more than specs_diff's COLOUR_TOL apart, numbers (sheen, a stripe's spacing
and width) more than 0.01; words and flags when they differ at all; and a reading shipped on one side only. With --ci
it exits with an error when anything changed: run tools/specs.js and commit data/looks.json (and docs/, rebuilt).
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from specs_diff import same_colour  # noqa: E402

NUM_TOL = 0.01


def changes(a, b):
    out = []
    for k in sorted(set(a) | set(b)):
        x, y = a.get(k), b.get(k)
        if isinstance(x, str) and x.startswith("#") or isinstance(y, str) and y.startswith("#"):
            same = all(same_colour(p, q) for p, q in zip((x or "").split("|"), (y or "").split("|"))) and (x or "").count("|") == (y or "").count("|")
        elif isinstance(x, (int, float)) and isinstance(y, (int, float)) and not isinstance(x, bool) and not isinstance(y, bool):
            same = abs(x - y) <= NUM_TOL
        else:
            same = x == y
        if not same:
            out.append("%s %s -> %s" % (k, x, y))
    return out


def main():
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    a, b = (json.load(open(p, encoding="utf-8")) for p in args[:2])
    gone = sorted(set(a) - set(b))
    new = sorted(set(b) - set(a))
    moved = {k: changes(a[k], b[k]) for k in sorted(set(a) & set(b))}
    moved = {k: v for k, v in moved.items() if v}
    for k in new:
        print("new  " + k)
    for k in gone:
        print("gone " + k)
    for k, v in moved.items():
        print("read " + k + ": " + "; ".join(v))
    print("%d readings: %d new, %d gone, %d read differently" % (len(b), len(new), len(gone), len(moved)))
    if "--ci" in sys.argv and (new or gone or moved):
        print("::error::data/looks.json is out of date. Run: node tools/specs.js, then python3 tools/build_site.py --out docs, and commit data/looks.json and docs/.")
        sys.exit(1)


if __name__ == "__main__":
    main()
