"""Builds the files the published page reads: site/index.html plus site/data/*.json.

The page loads its picks, outfits and settings from these files. Picks come in load
groups of under 900 (data/items/<group>.json, listed in data/items.json); shirts and
coats always have groups of their own. Each group's listing photos sit in
data/photos/<group>.json, fetched only when a card from that group scrolls into view. The shared shortlist, thumbs and "his wardrobe"
marks still live in the artifact's database.

    python3 tools/build_site.py [--out site]
"""
import argparse, glob, json, os, re, shutil

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


GROUP_MAX = 899
PHOTO_CHUNK = 150
OWN_GROUP = ("shirt", "coat")


def load_groups(items):
    """Splits the picks into groups of at most GROUP_MAX, one kind of thing per group where
    it is big enough. Shirts and coats always get their own; small kinds share a group."""
    bycat = {}
    for k in sorted(items, key=lambda k: (items[k].get("rank", 9999), k)):
        bycat.setdefault(items[k].get("cat") or "other", []).append(k)
    groups, small = {}, []
    for cat in sorted(bycat):
        ids = bycat[cat]
        if cat in OWN_GROUP or len(ids) >= 300:
            n = -(-len(ids) // GROUP_MAX)
            for i in range(n):
                groups[cat if n == 1 else "%s-%d" % (cat, i + 1)] = ids[i::n]
        else:
            small.append(cat)
    cur, name = [], []
    for cat in small:
        if cur and len(cur) + len(bycat[cat]) > GROUP_MAX:
            groups["-".join(name)] = cur
            cur, name = [], []
        cur = cur + bycat[cat]
        name.append(cat)
    if cur:
        groups["-".join(name)] = cur
    return groups


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT, "site"))
    a = ap.parse_args()
    out = a.out
    os.makedirs(os.path.join(out, "data", "photos"), exist_ok=True)

    items = load("data/items.json")
    for extra in sorted(glob.glob(os.path.join(ROOT, "data", "items-*.json"))):
        for k, v in load(os.path.relpath(extra, ROOT)).items():
            items.setdefault(k, v)
    outfits = load("data/outfits.json")
    if os.path.exists(os.path.join(ROOT, "data", "outfits-new.json")):
        for k, v in load("data/outfits-new.json").items():
            outfits.setdefault(k, v)
    tags = load("data/styletags.json")
    checked = max((v.get("checked", "") for v in items.values()), default="")
    meta = {
        "status": {"checked": checked, "prev": "", "cadence": "Prices are checked weekly"},
        "profile": PROFILE,
        "shops": {},
        "styletags": tags,
    }

    photos = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "photos", "*-[0-9][0-9].json"))):
        with open(p, encoding="utf-8") as f:
            photos.update(json.load(f))
    bycat = {}
    # Tidy before publishing: an old price more than six times the current one is a data error,
    # not a sale, and a few feeds leave a trademark sign at the start of a name.
    for v in items.values():
        if v.get("was") and v.get("price") and v["was"] > v["price"] * 6:
            v.pop("was")
        v["name"] = re.sub(r"\s{2,}", " ", re.sub(r"^[^\w(]+", "", v.get("name", ""))).strip()
    groups = load_groups(items)
    for g, ids in groups.items():
        for k in ids:
            items[k]["pg"] = g
            items[k].pop("img_src", None)
    # Photos go in files of at most PHOTO_CHUNK per load group, so opening one category on a phone
    # fetches about a megabyte rather than the whole group's photos. "pg" names an item's photo file.
    for g, ids in groups.items():
        have = [k for k in ids if isinstance(photos.get(k), str) and photos[k].startswith("data:image/")]
        for n in range(0, len(have), PHOTO_CHUNK):
            name = "%s-p%d" % (g, n // PHOTO_CHUNK + 1)
            for k in have[n:n + PHOTO_CHUNK]:
                bycat.setdefault(name, {})[k] = photos[k]
                items[k]["pg"] = name
                items[k]["ph"] = True
    for g, m in bycat.items():
        with open(os.path.join(out, "data", "photos", g + ".json"), "w", encoding="utf-8") as f:
            json.dump(m, f, separators=(",", ":"))
    meta["photos"] = {"cats": sorted(bycat), "count": sum(len(m) for m in bycat.values())}

    os.makedirs(os.path.join(out, "data", "items"), exist_ok=True)
    for g, ids in groups.items():
        with open(os.path.join(out, "data", "items", g + ".json"), "w", encoding="utf-8") as f:
            json.dump({k: items[k] for k in ids}, f, separators=(",", ":"), ensure_ascii=False)
    index = {"_groups": ["data/items/%s.json" % g for g in groups]}
    for name, obj in (("items", index), ("outfits", outfits), ("meta", meta)):
        with open(os.path.join(out, "data", name + ".json"), "w", encoding="utf-8") as f:
            json.dump(obj, f, separators=(",", ":"), ensure_ascii=False)
    shutil.copyfile(os.path.join(ROOT, "page.html"), os.path.join(out, "index.html"))
    print(f"{len(items)} picks in {len(groups)} load groups (largest {max(len(v) for v in groups.values())}), "
          f"{len(outfits)} outfits, {meta['photos']['count']} photos -> {out}")


if __name__ == "__main__":
    main()
