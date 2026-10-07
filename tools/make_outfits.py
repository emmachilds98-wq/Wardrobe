"""Builds new outfits from the picks, for every style.

Only picks with a listing photo, in stock in his size (or one size), are used, so every new outfit
shows real photos in its flat lay and its drawing takes each piece's real colour. Rules:
  - a top (tee, polo or shirt), trousers or shorts and shoes; a knit and a jacket or coat when the
    weather calls for it; sometimes one accessory;
  - every piece suits the outfit's weather; no shorts in the cold, no coat in the heat;
  - at most one colour that is not a neutral, and the top and trousers in different colours;
  - Workwear uses only Workwear picks and safety footwear; Lounge uses lounge pieces and slippers;
  - reduced pieces are preferred, and no pick is used in more than two new outfits.

    python3 tools/make_outfits.py [--per-style 30] [--seed 1]

Writes data/outfits-new.json (merged by build_site.py).
"""
import argparse, glob, json, os, random, re

from build_site import garment_kind

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COLW = [["off white", "cream"], ["navy", "navy"], ["midnight", "navy"], ["black", "black"], ["white", "white"],
        ["ecru", "cream"], ["cream", "cream"], ["bone", "cream"], ["oatmeal", "cream"], ["charcoal", "charcoal"],
        ["gunmetal", "charcoal"], ["grey", "grey"], ["gray", "grey"], ["marl", "grey"], ["silver", "silver"],
        ["olive", "olive"], ["khaki", "olive"], ["army", "olive"], ["sage", "olive"], ["green", "green"],
        ["chocolate", "brown"], ["mocha", "brown"], ["brown", "brown"], ["tobacco", "brown"], ["tan", "tan"],
        ["cognac", "tan"], ["camel", "camel"], ["stone", "stone"], ["beige", "stone"], ["taupe", "stone"],
        ["sand", "sand"], ["natural", "sand"], ["burgundy", "burgundy"], ["wine", "burgundy"], ["oxblood", "burgundy"],
        ["pink", "pink"], ["indigo", "indigo"], ["denim", "indigo"], ["jeans", "indigo"], ["sky", "blue"], ["blue", "blue"],
        ["red", "red"], ["rust", "rust"], ["orange", "orange"], ["mustard", "mustard"], ["yellow", "yellow"], ["purple", "purple"],
        ["lilac", "purple"], ["teal", "teal"], ["coral", "pink"], ["salmon", "pink"], ["maroon", "burgundy"], ["claret", "burgundy"],
        ["ivory", "cream"], ["slate", "grey"], ["ink", "navy"], ["forest", "green"], ["bottle", "green"], ["mint", "green"]]
PALETTE = {"red": "burgundy", "rust": "tan", "orange": "tan", "mustard": "camel", "yellow": "camel", "purple": "burgundy", "teal": "green"}
NEUTRAL = {"navy", "black", "white", "grey", "charcoal", "stone", "cream", "sand", "indigo", "brown", "tan", "camel", "olive", ""}
WHAT = {"jumper": "jumper", "rollneck": "roll neck", "halfzip": "half-zip", "cardigan": "cardigan", "hoodie": "hoodie",
        "shirt": "shirt", "sshirt": "short-sleeve shirt", "polo": "polo", "tee": "T-shirt", "vest": "vest",
        "trousers": "trousers", "shorts": "shorts", "coat": "coat", "jacket": "jacket", "gilet": "gilet", "blazer": "blazer",
        "boots": "boots", "shoes": "shoes", "trainers": "trainers", "slippers": "slippers", "cap": "flat cap", "bcap": "cap",
        "beanie": "beanie", "bucket": "bucket hat", "belt": "belt", "watch": "watch", "bag": "bag", "backpack": "backpack",
        "scarf": "scarf", "sunglasses": "sunglasses", "chain": "chain", "tie": "tie", "snood": "neck warmer"}
TOP = {"tee", "polo", "shirt", "sshirt", "vest"}
MID = {"jumper", "rollneck", "halfzip", "cardigan", "hoodie"}
OUT = {"coat", "jacket", "gilet", "blazer"}
LOW = {"trousers", "shorts"}
FEET = {"boots", "shoes", "trainers", "slippers"}
ACC = {"cap", "bcap", "beanie", "bucket", "belt", "watch", "bag", "backpack", "scarf", "sunglasses", "chain"}


def colour(name):
    n = " " + name.lower() + " "
    tail = n.rsplit(",", 1)[-1]
    for src in (tail, n):
        for w, c in COLW:
            if re.search("[^a-z]" + w + "[^a-z]", src):
                return c
    return ""


def shape(v):
    n, c = v["name"].lower(), v["cat"]
    t = lambda r: re.search(r, n)
    # (the garment the name says comes first: a shop's category can be wrong, sweat shorts filed with the knitwear,
    # a cap with the trousers; build_site.py stops on any piece drawn as another kind of garment)
    gk = garment_kind(v["name"])
    if gk in ("shorts", "trousers") and c not in ("swim",):
        return gk
    if (gk == "acc" and c != "acc") or (gk == "feet" and c not in ("shoe", "lounge")) or (gk == "top" and c in ("trouser", "shoe", "acc")):
        return None
    if c == "knit":
        return "hoodie" if t(r"hood") else "polo" if t(r"knitted polo|polo shirt") else "rollneck" if t(r"roll|turtle|funnel|mock|polo neck") \
            else "cardigan" if t(r"cardigan") else "halfzip" if t(r"zip|snap") else "jumper"
    if c == "shirt":
        return "sshirt" if t(r"short[- ]sleeve|s/s|resort|cuban|bowling|camp collar|hawaiian") else "shirt"
    if c == "polo":
        return "vest" if t(r"\bvest\b|tank") else "polo" if t(r"polo|rugby") else "tee"
    if c == "trouser":
        return "shorts" if t(r"short|jort") else "trousers"
    if c == "coat":
        return "gilet" if t(r"gilet|body ?warmer|\bvest\b") else "shirt" if t(r"overshirt|shacket") else \
            "coat" if t(r"parka|overcoat|trench|\bcoat\b") and not t(r"jacket") else "jacket"
    if c == "tailor":
        return "trousers" if t(r"trouser") else None if t(r"waistcoat|suit\b") else "blazer"
    if c == "shoe":
        return "slippers" if t(r"slipper") else "boots" if t(r"boot") else \
            "trainers" if t(r"trainer|sneaker|samba|vans|court|converse|old skool|skate|runner|running|plimsoll|gazelle|campus") else \
            None if t(r"sandal|slide|flip") else "shoes"
    if c == "lounge":
        return "slippers" if t(r"slipper|moccasin") else "hoodie" if t(r"hood") else "trousers" if t(r"jogger|lounge pant|bottoms|trouser") \
            else "jumper" if t(r"sweat|jumper|crew") else "tee" if t(r"t-shirt|\btee\b|\btop\b") and not t(r"pyjama|pj") else None
    if c == "acc":
        return "snood" if t(r"snood|neck warmer") else "scarf" if t(r"scarf") else "cap" if t(r"flat cap") else \
            "beanie" if t(r"beanie") else "bucket" if t(r"bucket") else "bcap" if t(r"\bcap\b") else \
            "belt" if t(r"belt") and not t(r"tool|pouch") else "watch" if t(r"watch") else "backpack" if t(r"backpack|rucksack") else \
            "bag" if t(r"\bbag\b") else "sunglasses" if t(r"sunglass") else "chain" if t(r"chain|necklace") else None
    return None


STYLE_OCC = {"quiet": ["everyday", "smart"], "casual": ["everyday", "party"], "mod": ["everyday", "party"],
             "rave": ["party"], "outdoor": ["everyday"], "summer": ["everyday", "party"], "job": ["everyday"],
             "lounge": ["lounge"]}
STYLE_WX = {"quiet": ["mild", "cold", "wet", "mild"], "casual": ["mild", "cold", "warm", "mild"], "mod": ["mild", "warm", "cold"],
            "rave": ["mild", "warm"], "outdoor": ["wet", "cold", "mild"], "summer": ["warm"], "job": ["mild", "cold", "warm", "wet"],
            "lounge": ["mild", "cold"]}
STYLE_NAME = {"quiet": "Classic", "casual": "Casual", "mod": "Mod", "rave": "Rave", "outdoor": "Outdoors",
              "summer": "Holiday", "job": "Workwear", "lounge": "Lounge"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--per-style", type=int, default=30)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--new-since", default="", help="weekly mode: each outfit needs a pick added on or after this date")
    ap.add_argument("--out", default=os.path.join(ROOT, "data", "outfits-new.json"))
    ap.add_argument("--id-prefix", default="g")
    a = ap.parse_args()
    rnd = random.Random(a.seed)
    items = json.load(open(os.path.join(ROOT, "data", "items.json")))
    for extra in sorted(glob.glob(os.path.join(ROOT, "data", "items-*.json"))):
        for k, v in json.load(open(extra)).items():
            items.setdefault(k, v)
    photos = set()
    for p in glob.glob(os.path.join(ROOT, "photos", "*-[0-9][0-9].json")):
        photos.update(json.load(open(p)).keys())
    old = {}
    for of in glob.glob(os.path.join(ROOT, "data", "outfits*.json")):
        if os.path.abspath(of) != os.path.abspath(a.out) or a.new_since:
            old.update(json.load(open(of)))
    used = {}
    for f in old.values():
        for p in f["pieces"]:
            used[p["item"]] = used.get(p["item"], 0) + 1
    fresh = {k for k, v in items.items() if a.new_since and v.get("added", "") >= a.new_since}

    pool = []
    for k, v in items.items():
        if k not in photos or v.get("kind") == "preowned" or v.get("insize") is False:
            continue
        if v.get("insize") is not True and v["cat"] not in ("acc",):
            continue
        sh = shape(v)
        if not sh:
            continue
        col = colour(v["name"])
        if not col and sh not in ACC | FEET:
            continue  # without a colour we cannot match it to the rest of the outfit
        pool.append((k, v, sh, col))

    def pick(style, shapes, wx, avoid_cols, taken, extra=lambda v, sh: True):
        def in_style(v):
            st = set(v["style"])
            if style in st or (style == "quiet" and st & {"work", "minimal"}) or (style == "casual" and "street" in st):
                return True
            if style == "summer":  # holiday clothes come from any style except workwear
                return "job" not in st and "warm" in v.get("wx", [])
            if style == "lounge":
                return "job" not in st
            return False
        sporty = re.compile(r"jogger|track ?(pant|bottom|top)|sweatpant|tracksuit|tricot", re.I)
        cands = [x for x in pool if x[2] in shapes and x[0] not in taken and used.get(x[0], 0) < 2 and in_style(x[1])
                 and (style in ("lounge", "rave") or not sporty.search(x[1]["name"]))
                 and (wx in x[1].get("wx", []) or not x[1].get("wx")) and extra(x[1], x[2])]
        cands = [x for x in cands if x[3] not in avoid_cols or x[3] in ("black",) and style in ("rave", "job")]
        if not cands:
            return None
        # Reduced and cheaper pieces first, with some variety.
        cands.sort(key=lambda x: (-(1 - x[1]["price"] / x[1]["was"]) if x[1].get("was") else 0) + x[1]["price"] / 150 + rnd.random() * 0.8
                   - (0.9 if x[0] in fresh else 0) - (0.6 if x[1].get("fit") else 0))
        return cands[0]

    out = {}
    for style, wxs in STYLE_WX.items():
        made = tries = 0
        while made < a.per_style and tries < a.per_style * 12:
            tries += 1
            wx = wxs[tries % len(wxs)]
            taken, pieces, cols = set(), [], []
            job = style == "job"
            lounge = style == "lounge"

            def add(x, what=None):
                taken.add(x[0])
                pieces.append(x)
                cols.append(x[3])

            def bright():
                return [c for c in cols if c not in NEUTRAL]

            top = pick(style, {"polo"} if job else (TOP if not lounge else {"tee", "polo"}), wx, set(), taken)
            if not top:
                continue
            add(top)
            low_shapes = {"shorts"} if wx == "warm" and style in ("summer", "rave") else ({"trousers"} if wx in ("cold", "wet") else LOW)
            low = pick(style, low_shapes, wx, {top[3]} | (set() if not bright() else {c for c in cols}), taken,
                       (lambda v, sh: re.search(r"jogger|lounge|bottom|sweat", v["name"], re.I) is not None) if lounge else (lambda v, sh: True))
            if not low:
                continue
            add(low)
            if wx in ("cold", "wet", "mild") and not (wx == "mild" and rnd.random() < 0.5):
                mid = pick(style, MID, wx, {low[3]} if bright() else set(), taken)
                if mid and (not bright() or mid[3] in NEUTRAL):
                    add(mid)
            if wx in ("cold", "wet") or (wx == "mild" and rnd.random() < 0.4):
                outer = pick(style, OUT if not lounge else set(), wx, set(), taken,
                             (lambda v, sh: not re.search(r"hi[- ]?vis", v["name"], re.I)))
                if outer and (not bright() or outer[3] in NEUTRAL):
                    add(outer)
            feet_shapes = {"slippers"} if lounge else ({"boots", "shoes"} if job else FEET - {"slippers"})
            feet = pick(style, feet_shapes, wx, set(), taken,
                        (lambda v, sh: re.search(r"safety|s1p|s3|toe|4e|6e|wide", v["name"], re.I) is not None) if job else (lambda v, sh: True))
            if not feet:
                continue
            add(feet)
            if rnd.random() < 0.55 and not lounge:
                acc = pick(style, ACC - ({"sunglasses"} if wx in ("cold", "wet") else {"beanie", "scarf"}), wx, set(), taken)
                if acc:
                    add(acc)
            if len(bright()) > 1:
                continue
            if a.new_since and not any(x[0] in fresh for x in pieces):
                continue
            for x in pieces:
                used[x[0]] = used.get(x[0], 0) + 1
            tot = sum(x[1]["price"] for x in pieces)
            full = sum(x[1].get("was") or x[1]["price"] for x in pieces)
            main = [x for x in pieces if x[2] in OUT] or [x for x in pieces if x[2] in MID] or [pieces[0]]
            hero, lowp = main[0], pieces[1]
            def label(x):
                return ((x[3] + " ") if x[3] else "") + WHAT[x[2]]
            name = (label(hero) + " and " + label(lowp))
            name = name[0].upper() + name[1:]
            occ = next((o for o in STYLE_OCC[style] if all(o in x[1].get("occ", [o]) for x in pieces[:2])), STYLE_OCC[style][0])
            fid = "%s-%s-%02d" % (a.id_prefix, style, made + 1)
            out[fid] = {
                "name": name,
                "note": "%d pieces for £%s%s." % (len(pieces), ("%.2f" % tot).rstrip("0").rstrip("."),
                                                   (", £%d below full price" % round(full - tot)) if full - tot >= 1 else ""),
                "occ": occ,
                "pieces": [{"col": PALETTE.get(x[3], x[3]) or "grey", "item": x[0], "shape": x[2],
                            "what": (x[3].capitalize() + " " if x[3] else "") + WHAT[x[2]] + (", worn open" if x[2] in ("jacket", "coat", "shirt") and x is not pieces[0] and x[2] != "shirt" else "")}
                           for x in pieces],
                "rank": 400 + made * 3,
                "style": [style],
                "wx": [wx],
                "look": "men " + " ".join(label(x) for x in pieces if x[2] not in ACC) + " outfit",
            }
            if job:
                out[fid]["ev"] = "site"
            made += 1
        print(style, made)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print(len(out), "new outfits")


if __name__ == "__main__":
    main()
