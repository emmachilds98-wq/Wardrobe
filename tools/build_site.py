"""Builds the files the published page reads: site/index.html plus site/data/*.json.

The page loads its picks, outfits and settings from these files, and the listing
photos from one file per type (data/photos/<cat>.json), fetched only when a card
with that type scrolls into view. The shared shortlist, thumbs and "his wardrobe"
marks still live in the artifact's database.

    python3 tools/build_site.py [--out site]
"""
import argparse, glob, json, os, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROFILE = {
    "sizes": [
        {"k": "Tops and knits", "v": "L"},
        {"k": "Shirts", "v": "L, or a 15.5 to 16in collar"},
        {"k": "Jackets", "v": "L"},
        {"k": "Trousers", "v": "34W 32L (never short)"},
        {"k": "Shoes", "v": "UK 11, wide fit"},
        {"k": "Safety boots", "v": "UK 11, 4E or 6E"},
    ],
    "bycat": {
        "knit": "L", "polo": "L", "coat": "L", "shirt": "L, or 15.5 to 16in collar",
        "trouser": "34W 32L", "swim": "34W or L", "shoe": "UK 11 (wide)", "lounge": "L",
        "sport": "L", "basics": "L", "tailor": "40R jacket, 34W trousers",
    },
    "notes": [
        "UK sizes only. US trouser and shoe sizes run differently, so check the size chart.",
        "No short-leg trousers: regular (32L) or long only.",
        "Workwear: high cotton, black or charcoal, relaxed or regular fit (no slim, skinny or tapered).",
        "Safety boots in extra wide fittings (4E or 6E).",
    ],
}


def load(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return json.load(f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT, "site"))
    a = ap.parse_args()
    out = a.out
    os.makedirs(os.path.join(out, "data", "photos"), exist_ok=True)

    items = load("data/items.json")
    extra = os.path.join(ROOT, "data", "items-new.json")
    if os.path.exists(extra):
        for k, v in load("data/items-new.json").items():
            items.setdefault(k, v)
    outfits = load("data/outfits.json")
    tags = load("data/styletags.json")
    checked = max((v.get("checked", "") for v in items.values()), default="")
    meta = {
        "status": {"checked": checked, "prev": "", "cadence": "Prices are checked weekly"},
        "profile": PROFILE,
        "shops": {},
        "styletags": tags,
    }

    photos = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "photos", "pack-*.json"))):
        with open(p, encoding="utf-8") as f:
            photos.update(json.load(f))
    bycat = {}
    for k, src in photos.items():
        it = items.get(k)
        if not it or not isinstance(src, str) or not src.startswith("data:image/"):
            continue
        cat = it.get("cat") if str(it.get("cat", "")).isalpha() else "other"
        bycat.setdefault(cat, {})[k] = src
        it["ph"] = True
    for cat, m in bycat.items():
        with open(os.path.join(out, "data", "photos", cat + ".json"), "w", encoding="utf-8") as f:
            json.dump(m, f, separators=(",", ":"))
    meta["photos"] = {"cats": sorted(bycat), "count": sum(len(m) for m in bycat.values())}

    for name, obj in (("items", items), ("outfits", outfits), ("meta", meta)):
        with open(os.path.join(out, "data", name + ".json"), "w", encoding="utf-8") as f:
            json.dump(obj, f, separators=(",", ":"), ensure_ascii=False)
    shutil.copyfile(os.path.join(ROOT, "page.html"), os.path.join(out, "index.html"))
    print(f"{len(items)} picks, {len(outfits)} outfits, {meta['photos']['count']} photos in {len(bycat)} files -> {out}")


if __name__ == "__main__":
    main()
