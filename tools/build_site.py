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
        {"k": "Trousers", "v": "34W 32L, regular, relaxed or wide fit"},
        {"k": "Shoes", "v": "UK 11, wide fit"},
        {"k": "Safety boots", "v": "UK 11, 4E or 6E"},
    ],
    "bycat": {
        "knit": "L", "polo": "L", "coat": "L", "shirt": "L, or 15.5 to 16in collar",
        "trouser": "34W 32L, regular or wide fit", "swim": "34W or L", "shoe": "UK 11 (wide)", "lounge": "L",
        "sport": "L", "basics": "L", "tailor": "40R jacket, 34W trousers",
    },
    "notes": [
        "UK sizes only. US trouser and shoe sizes run differently, so check the size chart.",
        "No short-leg trousers: regular (32L) or long only.",
        "Trousers that do not grip: regular, straight, relaxed or wide fits. Nothing slim, skinny or tapered.",
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


FIX_FIELDS = ("col", "col2", "pat", "per", "duty", "front", "decal", "swatch")


def check_fix_fields(k, fx, bad):
    """The look fields of one correction (or of one shape's part of it)."""
    for f in ("col", "col2"):
        if f in fx and fx[f] != "" and not re.fullmatch(r"#[0-9a-fA-F]{6}", str(fx[f])):
            bad.append(f"{k}: {f} must be #rrggbb")
    if "pat" in fx and fx["pat"] not in ("plain", "hstripe", "vstripe", "check", "print", "argyle"):
        bad.append(f"{k}: pat must be plain, hstripe, vstripe, check, print or argyle")
    for f in ("per", "duty"):
        if f in fx and not (isinstance(fx[f], (int, float)) and 0 < fx[f] < 1):
            bad.append(f"{k}: {f} must be a share between 0 and 1")
    for f in ("front", "decal"):
        if f in fx and fx[f] is not False:
            bad.append(f"{k}: {f} can only be false")
    if "swatch" in fx and not (isinstance(fx["swatch"], str) and re.match(r"data:image/(jpeg|png);base64,", fx["swatch"])
                               and len(fx["swatch"]) <= 16000):
        bad.append(f"{k}: swatch must be a small data:image/jpeg or png (a square of the cloth, under 16,000 characters)")


def check_fixes(fixes, items):
    """What is wrong in data/fixes.json: an unknown item, a colour that is not #rrggbb, an unknown pattern, a share
    out of range, or a fix with no reason ("why") or date ("checked"). "shapes" holds corrections for one garment
    shape only, for a listing that is a set worn as two pieces (a tee and shorts sold together, one photo)."""
    bad = []
    for k, fx in fixes.items():
        if k.startswith("_"):
            continue
        if k not in items:
            bad.append(f"{k}: no such item")
        check_fix_fields(k, fx, bad)
        for sh, sub in (fx.get("shapes") or {}).items():
            if sh not in SHAPE_CATS:
                bad.append(f"{k}: shapes: {sh} is not a garment shape")
            if not isinstance(sub, dict):
                bad.append(f"{k}: shapes: {sh} must hold fields"); continue
            check_fix_fields(f"{k} ({sh})", sub, bad)
            extra = [f for f in sub if f not in FIX_FIELDS]
            if extra:
                bad.append(f"{k} ({sh}): unknown field {', '.join(extra)}")
        if not fx.get("why") or not fx.get("checked"):
            bad.append(f"{k}: say why (what the shop photo shows) and when it was checked")
        extra = [f for f in fx if f not in FIX_FIELDS + ("why", "checked", "shapes")]
        if extra:
            bad.append(f"{k}: unknown field {', '.join(extra)}")
    return bad


VOCAB = {
    "occ": ("everyday", "party", "smart", "lounge", "event"),
    "style": ("quiet", "casual", "work", "minimal", "street", "lounge", "outdoor", "summer", "rave", "mod", "job", "sport"),
    "wx": ("mild", "warm", "cold", "wet"),
}
# Which kinds of pick (an item's "cat") each shape is drawn from. A pairing outside this is not an error, but it is
# usually a slip (a shoe drawn as trousers), so the build names it.
SHAPE_CATS = {
    "coat": "coat", "jacket": "coat knit", "blazer": "tailor coat", "gilet": "coat", "gown": "lounge",
    "waistcoat": "tailor coat knit", "cardigan": "knit", "hoodie": "knit lounge basics sport", "jumper": "knit lounge basics",
    "rollneck": "knit basics", "halfzip": "knit sport", "shirt": "shirt coat lounge", "sshirt": "shirt",
    "polo": "polo knit", "tee": "polo lounge basics sport", "vest": "polo sport basics",
    "trousers": "trouser lounge sport tailor", "shorts": "trouser swim shirt lounge sport",
    "boots": "shoe", "shoes": "shoe", "trainers": "shoe", "slippers": "shoe lounge",
}


# What a listing is, from its garment noun: the last one in the name before the colourway ("Chino Jacket" is a
# jacket, "Jogger Shorts" are shorts, "Tommy Jeans T-shirt" a T-shirt). Sets, pyjamas, suits and multipacks are left
# out, since they name more than one thing.
GARMENT_NOUNS = [
    ("shorts", r"shorts|short(?![- ]?sleeve)|jorts?|boardshorts|swim trunks|trunks"),
    ("trousers", r"trousers?|joggers?|jeans|chinos?|pants|cargos|sweatpants|leggings|bottoms|slacks"),
    ("top", r"t-shirts?|tees?|shirts?|polos?|jumpers?|sweatshirts?|sweaters?|hoodies?|hoody|jackets?|coats?|gilets?|"
            r"blazers?|cardigans?|overshirts?|shackets?|parkas?|anoraks?|cagoules?|windbreakers?|bombers?|harringtons?|"
            r"waistcoats?|vests?|blousons?|knit|crew|half[- ]zip|quarter[- ]zip|1/4 zip|roll ?neck|turtle ?neck|henley|tank top|"
            r"dressing gown|robe|fleece|smock"),
    ("feet", r"trainers?|sneakers?|shoes?|boots?|slippers?|sandals?|loafers?|brogues?|derbys?|mules?|sliders?|slides|"
             r"espadrilles|plimsolls|moccasins?|chukkas?"),
    ("acc", r"belts?|caps?|hats?|beanies?|scarf|scarves|snood|gloves|bags?|backpacks?|rucksacks?|sunglasses|watch|"
            r"ties?|chains?|necklace|bracelet|pocket square|socks|kneepads?|knee pads|braces|tie bar"),
]
GARMENT_RX = re.compile(r"\b(%s)\b" % "|".join("(?P<%s>%s)" % kv for kv in GARMENT_NOUNS), re.I)


def garment_kind(name):
    """shorts, trousers, top, feet or acc, from the listing's name; None when it does not say (or names a set)."""
    n = (name or "").lower()
    if re.search(r"\bset\b|pyjamas?\b|\bsuit\b|two[- ]piece|\bco-?ord\b|\b\d-pack\b|multipack", n):
        return None
    for part in (re.split(r",\s| - | with ", n)[0], n):
        last = None
        for m in GARMENT_RX.finditer(part):
            last = m
        if last:
            return next(k for k, _ in GARMENT_NOUNS if last.group(k))
    return None


def page_tables():
    """The shapes and palette the page knows, read from page.html so the checks never fall out of step with it."""
    with open(os.path.join(ROOT, "page.html"), encoding="utf-8") as f:
        src = f.read()

    def keys(name):
        m = re.search(r"var %s=\{(.*?)\}" % name, src, re.S)
        return set(re.findall(r"(\w+):", m.group(1))) if m else set()
    col = re.search(r"var COL=\{(.*?)\};", src, re.S)
    return {
        "upper": keys("UPPER"), "lower": keys("LOWER"), "feet": keys("FEET"), "accs": keys("ACCS"),
        "col": set(re.findall(r"(\w+):\[\"#", col.group(1))) if col else set(),
    }


def check_outfits(outfits, items):
    """What is wrong in the outfits (errors stop the build) and what looks odd (warnings are printed).
    Errors: a piece whose item is not a pick (unless it is marked "own"), an unknown shape, a piece drawn as a
    different kind of garment from the one its name says (shorts drawn as a jumper, a cap as trousers), a colour not in
    the page's palette (COL), a piece with no "what", an outfit with no top or no legwear (he is never drawn
    shirtless), two pairs of legwear or shoes, and occasion, style or weather words the page does not use."""
    tb = page_tables()
    shapes = tb["upper"] | tb["lower"] | tb["feet"] | tb["accs"]
    bad, odd = [], []
    for oid, o in outfits.items():
        for f in ("name", "note", "pieces", "occ", "style", "wx"):
            if not o.get(f):
                bad.append(f"{oid}: no {f}")
        for f, ok in VOCAB.items():
            vals = o.get(f) or []
            for v in vals if isinstance(vals, list) else [vals]:
                if v not in ok:
                    bad.append(f"{oid}: {f} '{v}' is not one of {', '.join(ok)}")
        ps = o.get("pieces") or []
        for p in ps:
            it, sh = p.get("item"), p.get("shape")
            if it not in items and not p.get("own"):
                bad.append(f"{oid}: {it} is not a pick")
            if sh not in shapes:
                bad.append(f"{oid}: {it} has unknown shape '{sh}'")
            if p.get("col") not in tb["col"]:
                bad.append(f"{oid}: {it} colour '{p.get('col')}' is not in the palette ({', '.join(sorted(tb['col']))})")
            if not p.get("what"):
                bad.append(f"{oid}: {it} has no 'what'")
            cat = (items.get(it) or {}).get("cat")
            if cat and sh in SHAPE_CATS and cat not in SHAPE_CATS[sh].split():
                odd.append(f"{oid}: {it} is a '{cat}' pick drawn as '{sh}'")
            gk = garment_kind((items.get(it) or {}).get("name"))
            fits = {"shorts": {"shorts"}, "trousers": {"trousers"}, "top": tb["upper"], "feet": tb["feet"], "acc": tb["accs"]}
            if gk and sh in shapes and sh not in fits[gk]:
                bad.append(f"{oid}: {it} ({(items.get(it) or {}).get('name')}) is {gk} by its name but drawn as '{sh}'")
        sh = [p.get("shape") for p in ps]
        if not any(s in tb["upper"] for s in sh):
            bad.append(f"{oid}: no top")
        if sum(s in tb["lower"] for s in sh) != 1:
            bad.append(f"{oid}: needs exactly one pair of trousers or shorts")
        if sum(s in tb["feet"] for s in sh) > 1:
            bad.append(f"{oid}: two pairs of shoes")
        if not any(s in tb["feet"] for s in sh) and o.get("occ") != "lounge":
            odd.append(f"{oid}: no shoes")
    return bad, odd


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
    for extra in sorted(glob.glob(os.path.join(ROOT, "data", "outfits-*.json"))):
        for k, v in load(os.path.relpath(extra, ROOT)).items():
            outfits.setdefault(k, v)
    tags = load("data/styletags.json")
    checked = max((v.get("checked", "") for v in items.values()), default="")
    sp = os.path.join(ROOT, "data", "status.json")
    prev = load("data/status.json").get("prev", "") if os.path.exists(sp) else ""
    meta = {
        "status": {"checked": checked, "prev": prev, "cadence": "Prices are checked weekly"},
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
    # Corrections to how an item looks on Dave (data/fixes.json), for photos the page reads wrongly. Each is checked
    # here and rides on the item as "fix", which the page applies over the photo reading (pieceLook in page.html).
    fixes = load("data/fixes.json") if os.path.exists(os.path.join(ROOT, "data", "fixes.json")) else {}
    bad = check_fixes(fixes, items)
    if bad:
        raise SystemExit("data/fixes.json: " + "; ".join(bad))
    for k, fx in fixes.items():
        if not k.startswith("_"):
            items[k]["fix"] = {f: v for f, v in fx.items() if f in FIX_FIELDS}
            if fx.get("shapes"):
                items[k]["fix"]["shapes"] = {sh: {f: v for f, v in sub.items() if f in FIX_FIELDS} for sh, sub in fx["shapes"].items()}
    bad, odd = check_outfits(outfits, items)
    for w in odd:
        print("note:", w)
    if bad:
        raise SystemExit("outfits: " + "; ".join(bad))
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
    # Dave's 3D body (tools/build_body.py); without it the page falls back to the hand-built body
    body = os.path.join(ROOT, "data", "body.json")
    if os.path.exists(body):
        shutil.copyfile(body, os.path.join(out, "data", "body.json"))
    print(f"{len(items)} picks in {len(groups)} load groups (largest {max(len(v) for v in groups.values())}), "
          f"{len(outfits)} outfits, {meta['photos']['count']} photos -> {out}")


if __name__ == "__main__":
    main()
