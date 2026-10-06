"""Build the GitHub Pages copy from a dump of the artifact's database.

Usage:
    python3 tools/export_static.py --dump DIR [--out .]

DIR holds the JSON files written by the ArtifactData tool's out_dir option:
DIR/items/<id>.json, DIR/outfits/<id>.json, DIR/meta/<id>.json and,
optionally, DIR/photos/<id>.json: either one photo ({"img": "data:image/webp;base64,..."})
or a chunk of photos ({"imgs": {"<itemId>": "data:image/webp;base64,...", ...}}).

It writes, under --out:
    data/items.json        every pick, keyed by id, without photos
    data/outfits.json      every outfit, keyed by id
    data/meta.json         status, sizes, style tags and shop delivery notes
    data/photos/<cat>.json photos, one file per type, loaded only when needed
    index.html             a copy of page.html, so the site address opens it

Personal details are left out of the public copy: the name, the list of
clothes he owns, the colour notes about his looks, his measurements, and any
note that names a person. The shared shortlist, votes, saved outfits and
"he has this" marks are never exported.
"""
import argparse
import datetime
import glob
import json
import os
import re
import shutil

PERSONAL = re.compile(r"\b(dave|emma|boyfriend|girlfriend|sensitive skin|his skin)\b", re.I)
DROP_PROFILE = {"name", "owns", "colours", "measure"}


def load_dir(path):
    out = {}
    for f in sorted(glob.glob(os.path.join(path, "*.json"))):
        out[os.path.basename(f)[:-5]] = json.load(open(f))
    return out


def scrub_text(s):
    if not isinstance(s, str):
        return s
    if PERSONAL.search(s):
        s = PERSONAL.sub("", s)
        s = re.sub(r"\s{2,}", " ", s).strip()
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dump", required=True)
    ap.add_argument("--out", default=".")
    ap.add_argument("--packs", default="photos", help="old photo packs to fall back on")
    a = ap.parse_args()

    items = load_dir(os.path.join(a.dump, "items"))
    outfits = load_dir(os.path.join(a.dump, "outfits"))
    meta = load_dir(os.path.join(a.dump, "meta"))
    photos = {}
    for k, v in load_dir(os.path.join(a.dump, "photos")).items():
        if isinstance(v.get("imgs"), dict):  # a chunk doc: {"imgs": {itemId: dataURI}}
            photos.update(v["imgs"])
        elif v.get("img"):
            photos[k] = v["img"]
    for f in glob.glob(os.path.join(a.packs, "pack-*.json")):
        for k, v in json.load(open(f)).items():
            photos.setdefault(k, v)

    by_cat = {}
    out_items = {}
    for k, d in items.items():
        d = dict(d)
        img = d.pop("img", None) or photos.get(k)
        d.pop("ph", None)
        if isinstance(img, str) and img.startswith("data:image/"):
            d["ph"] = 1
            cat = d.get("cat") if re.fullmatch(r"[a-z]+", str(d.get("cat", ""))) else "other"
            by_cat.setdefault(cat, {})[k] = img
        for f in ("name", "note", "sizeNote", "offer"):
            if f in d:
                d[f] = scrub_text(d[f])
        out_items[k] = d

    out_fits = {}
    for k, d in outfits.items():
        d = dict(d)
        for f in ("name", "note"):
            d[f] = scrub_text(d.get(f, ""))
        for p in d.get("pieces", []):
            p["what"] = scrub_text(p.get("what", ""))
        out_fits[k] = d

    profile = {k: v for k, v in meta.get("profile", {}).items() if k not in DROP_PROFILE}
    profile["notes"] = [n for n in profile.get("notes", []) if isinstance(n, str) and not PERSONAL.search(n)]
    status = dict(meta.get("status", {}))
    status["exported"] = datetime.date.today().isoformat()
    status.pop("cadence", None)
    out_meta = {
        "status": status,
        "profile": profile,
        "styletags": meta.get("styletags", {}),
        "shops": meta.get("shops", {}),
    }

    blob = json.dumps([out_items, out_fits, out_meta])
    left = PERSONAL.findall(blob)
    if left:
        raise SystemExit("personal words still present: %s" % sorted(set(left)))

    data = os.path.join(a.out, "data")
    os.makedirs(os.path.join(data, "photos"), exist_ok=True)
    for f in glob.glob(os.path.join(data, "photos", "*.json")):
        os.remove(f)
    json.dump(out_items, open(os.path.join(data, "items.json"), "w"), separators=(",", ":"), sort_keys=True)
    json.dump(out_fits, open(os.path.join(data, "outfits.json"), "w"), separators=(",", ":"), sort_keys=True)
    json.dump(out_meta, open(os.path.join(data, "meta.json"), "w"), indent=1, sort_keys=True)
    for cat, m in by_cat.items():
        json.dump(m, open(os.path.join(data, "photos", cat + ".json"), "w"), separators=(",", ":"), sort_keys=True)
    shutil.copyfile(os.path.join(a.out, "page.html"), os.path.join(a.out, "index.html"))
    print("%d picks (%d with photos), %d outfits, %d photo files" % (
        len(out_items), sum(len(m) for m in by_cat.values()), len(out_fits), len(by_cat)))


if __name__ == "__main__":
    main()
