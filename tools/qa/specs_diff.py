"""Compares two stored-spec files (tools/specs.js): what changed in how each outfit piece is read.

    python3 tools/qa/specs_diff.py data/specs.json new.json [--ci]

Colours count as changed when they move more than COLOUR_TOL apart (RGB distance), a stripe's spacing or width
when it moves more than SPACE_TOL; anything else (pattern kind, source, cut, details, photo findings, corrections)
when it differs at all. With --ci it exits with an error when anything changed, for the pull-request check: a change
to the readers, data/fixes.json or the outfits must come with the regenerated data/specs.json, so the reviewer sees
what it moved. It also fails while any piece is read "unseen": a pattern the listing names (stripe, check, print,
Fair Isle...) that the photo reader drew plain. Each one is looked at against its shop photo and given an entry in
data/fixes.json: the pattern (pat, col2, per, duty, or a swatch), or pat "plain" with why plain is right.
"""
import json, sys

COLOUR_TOL = 12
SPACE_TOL = 0.01


def rgb(h):
    try:
        return [int(h[i:i + 2], 16) for i in (1, 3, 5)] if isinstance(h, str) and len(h) == 7 and h[0] == "#" else None
    except ValueError:
        return None


def same_colour(a, b):
    x, y = rgb(a), rgb(b)
    if x is None or y is None:
        return a == b
    return sum((p - q) ** 2 for p, q in zip(x, y)) ** 0.5 <= COLOUR_TOL


def changes(a, b):
    """What differs between one piece's two specs, as short phrases."""
    out = []
    ca, cb = a.get("colour", {}), b.get("colour", {})
    for k in ("main", "second", "photo"):
        if not same_colour(ca.get(k, ""), cb.get(k, "")):
            out.append("colour %s %s -> %s" % (k, ca.get(k, "") or "none", cb.get(k, "") or "none"))
    for k in ("named", "src"):
        if ca.get(k) != cb.get(k):
            out.append("colour %s %s -> %s" % (k, ca.get(k) or "none", cb.get(k) or "none"))
    pa, pb = a.get("pattern", {}), b.get("pattern", {})
    for k in ("kind", "src"):
        if pa.get(k) != pb.get(k):
            out.append("pattern %s %s -> %s" % (k, pa.get(k), pb.get(k)))
    for k in ("per", "duty"):
        if abs((pa.get(k) or 0) - (pb.get(k) or 0)) > SPACE_TOL:
            out.append("pattern %s %s -> %s" % (k, pa.get(k), pb.get(k)))
    for k in ("cut", "details", "photo", "fixed", "shape", "form"):
        if a.get(k) != b.get(k):
            out.append("%s %s -> %s" % (k, json.dumps(a.get(k)), json.dumps(b.get(k))))
    return out


def main():
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    ci = "--ci" in sys.argv
    old, new = (json.load(open(p, encoding="utf-8")) for p in args[:2])
    gone = sorted(set(old) - set(new))
    added = sorted(set(new) - set(old))
    moved = {k: changes(old[k], new[k]) for k in sorted(set(old) & set(new))}
    moved = {k: v for k, v in moved.items() if v}
    for k in added:
        print("new      %s" % k)
    for k in gone:
        print("gone     %s" % k)
    for k, v in moved.items():
        print("changed  %s: %s" % (k, "; ".join(v)))
    n = len(added) + len(gone) + len(moved)
    print("%d pieces: %d new, %d gone, %d read differently" % (len(new), len(added), len(gone), len(moved)))
    unseen = sorted(k for k, v in new.items() if (v.get("pattern") or {}).get("src") == "unseen")
    for k in unseen:
        print("unseen   %s: its listing names a pattern the photo reader drew plain" % k)
    if ci and unseen:
        print("::error::%d piece(s) read 'unseen' (a pattern named in the listing, drawn plain): look at each shop photo"
              " and add an entry to data/fixes.json, with the pattern or with pat 'plain' and why plain is right"
              " (CONTRIBUTING.md, 'Correcting how an item looks')." % len(unseen))
    if ci and n:
        print("::error::data/specs.json is out of date. Run: python3 tools/build_site.py --out docs && node tools/specs.js,"
              " look at what moved (python3 tools/qa/specs_diff.py <old> data/specs.json) and commit data/specs.json.")
    if ci and (n or unseen):
        sys.exit(1)


if __name__ == "__main__":
    main()
