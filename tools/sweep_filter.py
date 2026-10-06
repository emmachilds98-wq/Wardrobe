"""Turns the Shopify catalogues pulled by shopify_pull.py into picks for the page.

    python3 tools/sweep_filter.py <cat dir> [--out data/items-new.json] [--date 2026-10-06]

Rules (from the brief):
  - men's only, in stock in his size: L tops, 15.5-16in collars, 34W with a 32in or regular
    leg (never short, never a 34in leg), UK 11 shoes (a US 11 is not a UK 11);
  - categories from the noun, not the brand: a short-sleeve shirt is a shirt, a "Tommy Jeans"
    jumper is a jumper;
  - clean names: no "Special Offer" or "Sale" prefixes, no doubled brands or colours;
  - discounted pieces first; full-price pieces only to fill a shop's quota;
  - workwear: at least 60% cotton, no slim, skinny or tapered fits, safety boots 4E or 6E only;
  - each pick keeps the shop's own photo URL (`img_src`) for fetch_photos.py --shopify.
"""
import argparse, collections, glob, html, json, os, re, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

WOMEN = re.compile(r"\b(women'?s?|womens|ladies|lady|lady's|girls?|boys?|kids?|kid's|child(ren)?|"
                   r"junior|juniors|youth|infant|toddler|baby|babies|maternity|unisex-kids|dress|skirt|bra|tunic|kaftan|bralette|"
                   r"leggings|bikini|swimsuit|blouse|camisole)\b", re.I)
MEN = re.compile(r"\b(men|mens|men's|man|male|gents?|gent's|menswear|unisex)\b", re.I)
NOT_CLOTHES = re.compile(r"\b(gift ?card|gift ?voucher|voucher|e-?gift|sticker|poster|mug|candle|"
                         r"keyring|key ring|tent|sleeping bag|rucksack liner|stove|fuel|gas canister|"
                         r"carabiner|dog|lead|collar for|cleaner|spray|wax tin|proofer|laces?|insoles?|"
                         r"shoe care|polish|brush|sample|deposit|shipping|insurance|warranty|repair|"
                         r"magazine|book|print|art|puzzle|patch|badge|pin badge|lanyard|towel|blanket|"
                         r"cushion|bottle|flask|helmet|novelty|fancy dress|costume|kigurumi|goggles?|ear ?plugs?|hearing|mask|test|do not use|"
                         r"deodorant|compression bag|sleep bag|polishing|gaiter straps?|swim cap|silicone cap|sold individually|"
                         r"swim briefs?|endurance\+? (logo )?briefs?|expdn)\b", re.I)
BRAND_JUNK = re.compile(r"\b(tommy jeans|calvin klein jeans|armani jeans|guess jeans|ck jeans|"
                        r"jean ?store|voi jeans|true religion|replay jeans|pepe jeans|lee jeans|"
                        r"g-star raw|jack ?& ?jones|polo ralph lauren|ralph lauren polo|u\.s\. polo assn\.?|"
                        r"us polo assn|polo sport|beverly hills polo club)\b", re.I)
SKINNY = re.compile(r"\b(skinny|super ?slim|spray[- ]on|extreme slim|muscle fit)\b", re.I)
# Shops and brands that make real work clothing. At a country or fashion shop in the workwear
# list, only these count as Workwear (a Boss blazer from a workwear shop is not work clothing).
WORK_SHOPS = {"workweargurus.com", "tradeworkwear.co.uk", "tuffstuffworkwear.co.uk", "workwearhub.co.uk",
              "workwearexpress.com", "bestworkwear.co.uk", "dewaltworkwear.co.uk", "snickersworkwear.com",
              "engelbert-strauss.co.uk", "screwfix.com", "toolstation.com", "arco.co.uk", "apachesafety.co.uk",
              "safetyfootwearstore.co.uk", "amblerssafety.com", "scruffs.com", "liftingequipmentstore.com"}
WORK_BRAND = re.compile(r"\b(snickers|portwest|bl[aå]kl[aä]der|dickies|carhartt|scruffs|tuffstuff|caterpillar|"
                        r"dewalt|regatta professional|jcb|apache|fristads|mascot|helly hansen workwear|toughbuilt|"
                        r"grafters|ukd|amblers|cofra|rock ?fall|wide load|steitz|mongrel|buckler|engelbert|"
                        r"hard yakka|workwear|work|hi[- ]?vis|kneepads?|rigger)\b", re.I)
DARK = re.compile(r"\b(black|charcoal|graphite|dark grey|anthracite|carbon|jet)\b", re.I)
SLIM = re.compile(r"\b(slim|tapered|taper|muscle fit|carrot)\b", re.I)
SAFETY = re.compile(r"\b(safety|s1p?|s3|sb ?p|steel toe|composite toe|toe ?cap|midsole)\b", re.I)
WIDE = re.compile(r"\b(4e|6e|5e|eeee|eeeeee|extra wide|xw|wide fit|wide)\b", re.I)
WIDE_X = re.compile(r"\b(4e|6e|5e|eeee+|extra wide)\b", re.I)

# Order matters: the first rule that matches the cleaned title wins.
CATS = [
    ("shoe", r"\b(boots?|trainers?|sneakers?|shoes?|loafers?|derby|derbies|brogues?|oxfords?|chelsea|"
             r"sandals?|slippers?|mules?|plimsolls?|espadrilles?|chukkas?|riggers?|deck shoes?|"
             r"moccasins?|hikers?|monk strap|clogs?|slides|flip ?flops?|dealer boot)\b"),
    ("swim", r"\b(swim ?shorts?|swim ?trunks?|swimshorts?|board ?shorts?|boardshorts?|swim|trunks|"
             r"rash ?vest|wetsuit|swimwear)\b"),
    ("tailor", r"(?<!rain )(?<!track)(?<!boiler )(?<!wet)(?<!jump)\b(blazer|suit jacket|suit trousers?|waistcoat|tuxedo|dinner jacket|sport coat|"
               r"two[- ]piece|three[- ]piece|suit)\b"),
    ("lounge", r"\b(pyjamas?|pajamas?|pjs?|dressing gown|robe|loungewear|lounge pants?|"
               r"lounge shorts?|nightwear|onesie|sleep ?shorts?|sleepwear)\b"),
    ("basics", r"\b(socks?|boxers?|briefs?|trunk briefs?|underwear|undershirt|vest top|thermal|"
               r"base ?layer|long johns|multipack|\d ?pack|three pack|five pack)\b"),
    ("knit", r"\b(jumpers?|sweaters?|cardigans?|knit|knitted|knitwear|sweatshirts?|sweat|hoodie|hoody|"
             r"hooded top|fleece|quarter[- ]zip|half[- ]zip|1/4 zip|1/2 zip|roll ?neck|polo ?neck|"
             r"turtle ?neck|crew ?neck jumper|pullover|gansey|guernsey|funnel neck)\b"),
    ("coat", r"\b(track ?tops?|tracksuit tops?|track ?jackets?|hi[- ]?vis waistcoat|jackets?|coats?|parkas?|gilets?|anoraks?|cagoules?|overcoats?|peacoat|pea coat|"
             r"trench|mac|harrington|bomber|windbreaker|smock|shacket|body ?warmer|waterproof|"
             r"puffer|down jacket|softshell|shell)\b"),
    ("polo", r"\b(polo|polos|polo shirts?|t-?shirts?|tees?|tshirts?|henley|long ?sleeve top|"
             r"vest|tank|singlet|rugby shirt|football shirt|jersey|top)\b"),
    ("shirt", r"\b(shirts?|overshirts?|oxford|flannel|chambray)\b"),
    ("trouser", r"\b(trousers?|jeans?|denim|chinos?|cords?|corduroys?|cargos?|cargo pants?|pants|"
                r"joggers?|jogging bottoms|track ?pants?|sweatpants|shorts|bottoms|dungarees|bib and brace|"
                r"overalls?|slacks|work pants?|carpenter|fatigues)\b"),
    ("acc", r"\b(hats?|caps?|beanies?|bobble|scarf|scarves|snood|gloves?|mitts?|belts?|wallets?|"
             r"bags?|backpacks?|rucksacks?|holdall|tote|watch|watches|tie|ties|bow ?tie|braces|"
             r"pocket square|cufflinks?|sunglasses|bucket hat|balaclava|neck ?warmer|buff|headband|"
             r"pouch|tool ?belt|card holder|umbrella|lanyard|gaiters?|suspenders)\b"),
]
CATS = [(c, re.compile(p, re.I)) for c, p in CATS]

COLOURS = ("black navy white grey gray charcoal blue green olive khaki stone sand beige brown tan "
           "burgundy red pink orange yellow cream ecru oatmeal camel rust mustard teal purple lilac "
           "indigo denim natural ivory chocolate tobacco forest bottle sage mint sky royal ink "
           "midnight slate silver gold multi").split()
COLOUR_RE = re.compile(r"\b(" + "|".join(COLOURS) + r")\b", re.I)

GROUP_STYLE = {
    "High street": ["casual"], "Supermarkets and value": ["casual"],
    "Cheap online, delivered (sizes run small: size up)": ["casual"],
    "Big multi-brand shops": ["casual", "quiet"], "Shirtmakers and tailoring": ["quiet", "work"],
    "Knitwear and country": ["quiet"], "Shoes and watches": ["quiet"], "Outlets and discount": ["casual"],
    "Mod and terrace": ["mod"], "Street, minimal and trainers": ["casual", "street", "minimal"],
    "Heritage and workwear": ["quiet", "work", "casual"], "Workwear and safety boots": ["job"],
    "Outdoors": ["outdoor"], "More brands and sales": ["quiet", "casual"], "Pre-owned": ["casual"],
    "Rave, gym and lounge": ["rave", "lounge"], "Premium brands (buy in the sales)": ["quiet", "casual"],
}
# Shops in the workwear list that are fashion brands, not work clothing.
NOT_JOB = {"threadbare.com", "uk.representclo.com", "dubarry.com", "goodhoodstore.com", "gramicci.co.uk",
           "gymking.com", "hufworldwide.co.uk", "henrilloyd.com", "jack-wolfskin.co.uk", "kavu.co.uk",
           "lazyjacks.co.uk", "mountain-equipment.co.uk", "neweracap.co.uk", "uk.oneill.com",
           "padders.co.uk", "timex.co.uk", "voijeans.com", "volcom.co.uk"}
OUTDOORISH = {"jack-wolfskin.co.uk", "mountain-equipment.co.uk", "kavu.co.uk", "henrilloyd.com",
              "dubarry.com", "lazyjacks.co.uk", "uk.oneill.com"}


def bare(h):
    return h[4:] if h.startswith("www.") else h


def shop_directory():
    """Shop name and group for each host, read from the page's "Where to look" list."""
    page = open(os.path.join(ROOT, "page.html"), encoding="utf-8").read()
    out, group = {}, None
    for m in re.finditer(r'<span class="label">([^<]+)</span>|<a href="https://([^/"]+)[^"]*"[^>]*>([^<]+)</a>', page):
        if m.group(1):
            group = html.unescape(m.group(1)).strip()
        elif group and m.group(2):
            name = re.sub(r"\s*\(.*?\)|\s+(sale|clearance|archive|outlet|factory outlet)$", "", html.unescape(m.group(3)).strip(), flags=re.I)
            out.setdefault(bare(m.group(2)), (name, group))
    return out


def strip_tags(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()


def cotton_pct(text):
    m = re.findall(r"(\d{2,3})\s*%\s*(?:organic |bci |recycled |combed |ring[- ]spun )?cotton", text, re.I)
    if m:
        return max(int(x) for x in m)
    if re.search(r"\b(pure|all|100 ?%) cotton\b", text, re.I):
        return 100
    return None


def fabric_of(text):
    m = re.search(r"((?:\d{1,3}\s*%\s*[A-Za-z][A-Za-z -]{2,20}?(?:,\s*|\s+and\s+|\s*/\s*|\s+)?){1,4})", text)
    if m and "%" in m.group(1):
        f = re.sub(r"\s+", " ", m.group(1)).strip(" ,/")
        if 6 < len(f) < 60:
            return f
    return ""


def opts(p, v):
    """(option name, value) pairs for a variant."""
    names = [o.get("name", "") for o in p.get("options", [])]
    vals = [v.get("option1"), v.get("option2"), v.get("option3")]
    return [(names[i] if i < len(names) else "", str(x)) for i, x in enumerate(vals) if x]


TOP_L = re.compile(r"^(l|lg|large|l/xl|l-xl|m/l|42|42\"|42in|chest 42|42-44)$|\bL\b|\blarge\b", re.I)
NOT_L = re.compile(r"\b(xl|xxl|2xl|3xl|4xl|5xl|xs|xxs|s|m|small|medium|extra large|l\s*long|long|tall)\b", re.I)
COLLAR = re.compile(r"^(15\.5|15½|16|15 1/2)(\"|in|''| inch)?($|\s*/|\s*-|\s+(regular|standard|classic))", re.I)


def is_top_l(val):
    v = val.strip()
    if re.fullmatch(r"(L|Lg|Large|L/XL|L-XL|L \(42\"?\)|L \(42-44\"?\)|42|42\"|42-44|42R|Chest 42\"?)", v, re.I):
        return True
    return False


def waist_leg(val, title_and_opts):
    """(waist, leg) from a trouser size such as "34/32", "W34 L32", "34R", "34 Regular", "34"."""
    v = val.strip()
    m = re.match(r"^W?\s*(\d{2})\"?\s*(?:W)?\s*[/x,-]?\s*L?\s*(\d{2})\"?\s*(?:L)?$", v, re.I)
    if m:
        return int(m.group(1)), int(m.group(2))
    m = re.match(r"^(?:W\s*)?(\d{2})\"?\s*(R|Reg|Regular|S|Short|L|Long|XL|Extra Long|T|Tall)\b", v, re.I)
    if m:
        leg = {"r": 32, "reg": 32, "regular": 32, "s": 30, "short": 30, "l": 34, "long": 34,
               "xl": 36, "extra long": 36, "t": 34, "tall": 34}[m.group(2).lower()]
        return int(m.group(1)), leg
    m = re.match(r"^(?:W\s*|Waist\s*)?(\d{2})\"?(?:\s*W| in| inch| waist)?$", v, re.I)
    if m:
        return int(m.group(1)), None
    return None, None


def leg_from(name, val):
    if re.search(r"leg|length|inside", name, re.I):
        m = re.match(r"^(?:L\s*)?(\d{2})", val.strip())
        if m:
            return int(m.group(1))
        lv = val.lower()
        for k, n in (("short", 30), ("regular", 32), ("reg", 32), ("extra long", 36), ("long", 34)):
            if k in lv:
                return n
    return None


def shoe_uk11(p, v, us_shop):
    """True when this variant is a UK 11 (or EU 45/46 marked as UK 11). A bare "11" counts only
    when nothing on the product mentions US sizes."""
    for name, val in opts(p, v):
        val_l = val.lower().replace(" ", "")
        name_l = name.lower()
        if "us" in name_l and "uk" not in name_l:
            continue
        if re.search(r"uk11(\b|$|\.0\b|[^.\d])", val_l) and "uk11.5" not in val_l:
            return True
        if re.fullmatch(r"11(\.0)?(uk)?", val_l) and not us_shop:
            return True
        if re.fullmatch(r"(eu)?46(eu)?", val_l) and "uk11" in (p.get("body_html") or "").lower().replace(" ", ""):
            return True
    return False


def size_ok(cat, p, v, title, us_shop):
    """Returns a size label when the variant is his size, else None."""
    o = opts(p, v)
    if cat == "shoe":
        return "UK 11" if shoe_uk11(p, v, us_shop) else None
    if cat == "acc":
        vals = [x for _, x in o]
        if not vals or all(re.fullmatch(r"(one size|os|default title|o/s|one-size|n/a|\w+ ?colou?r.*|[a-z ]+)", x, re.I) for x in vals):
            if any(re.fullmatch(r"(xs|s|m|xl|xxl|small|medium|s/m)", x, re.I) for x in vals):
                return None
            return "One size"
        if any(is_top_l(x) or re.fullmatch(r"(l|large|l/xl|m/l|34|36|11|uk 11|7-11|8-11|9-12|10-13|6-11|size 11)", x.strip(), re.I) for x in vals):
            return "L"
        return None
    if cat in ("trouser", "swim", "lounge", "basics", "sport") and re.search(r"\b(trousers?|jeans|chinos?|cords?|cargos?|work pants|carpenter|slacks)\b", title, re.I) and cat == "trouser":
        w = leg = None
        for name, val in o:
            ww, ll = waist_leg(val, title)
            if ww:
                w, leg = ww, (ll if ll else leg)
            lg = leg_from(name, val)
            if lg:
                leg = lg
        if w != 34:
            return None
        if leg is None:
            m = re.search(r"\b(?:inside leg|leg length|inseam)[^0-9]{0,20}(\d{2})", strip_tags(p.get("body_html")), re.I)
            leg = int(m.group(1)) if m else None
            if leg is None:
                return "34W (leg not listed)"
        if leg in (31, 32, 33):
            return "34W 32L"
        return None
    if cat in ("trouser", "swim", "lounge", "sport", "basics"):
        for _, val in o:
            ww, ll = waist_leg(val, title)
            if ww == 34 and ll in (None, 31, 32, 33):
                return "34W"
            if is_top_l(val) or re.fullmatch(r"(l|large|l/xl|m/l|34\"?|34-36|36)", val.strip(), re.I):
                return "L"
            if cat == "basics" and re.fullmatch(r"(uk ?)?(7-11|8-11|9-12|10-13|6-11|11-14|10-12|11|uk 11)", val.strip(), re.I):
                return "UK 11"
        return None
    if cat == "shirt":
        for _, val in o:
            if is_top_l(val) or COLLAR.match(val.strip()):
                return "L" if is_top_l(val) else val.strip().split("/")[0].strip() + " collar"
        return None
    if cat == "tailor":
        if re.search(r"trouser", title, re.I):
            for name_, val in o:
                ww, ll = waist_leg(val.strip(), title)
                lg = leg_from(name_, val)
                if ww == 34 and (ll or lg) in (None, 31, 32, 33):
                    return "34W"
            return None
        for _, val in o:
            v2 = val.strip()
            if re.fullmatch(r"40\s*(R|Reg|Regular)?\"?", v2, re.I) or re.fullmatch(r"40\"?\s*/\s*(R|Regular)", v2, re.I):
                return "40R"
            ww, ll = waist_leg(v2, title)
            if ww == 34 and ll in (None, 31, 32, 33) and re.search(r"trouser", title, re.I):
                return "34W"
            if is_top_l(v2):
                return "L"
        return None
    for _, val in o:
        if is_top_l(val):
            return "L"
    return None


def category(title, ptype, tags):
    t = BRAND_JUNK.sub(" ", title)
    t = re.sub(r"\bshort[- ]sleeved?\b|\blong[- ]sleeved?\b|\bsleeveless\b", " ", t, flags=re.I)
    t = re.sub(r"\bt[ -]shirts?\b", "tshirt", t, flags=re.I)
    t = re.sub(r"\b(hi[- ]?vis|iso 20471|high[- ]vis\w*)\b.*\bwaistcoat\b|\bwaistcoat\b.*\b(hi[- ]?vis|iso 20471)\b", "hi-vis waistcoat", t, flags=re.I)
    t = re.sub(r"\b(rain ?suit|tracksuit|boiler ?suit|jumpsuit|wetsuit)\b", lambda m: "wetsuit" if "wet" in m.group(1).lower() else "overalls" if "boiler" in m.group(1).lower() or "jump" in m.group(1).lower() else "rain jacket" if "rain" in m.group(1).lower() else "tracksuit top", t, flags=re.I)
    t = re.sub(r"\bpolo ?neck\b", " rollneck jumper ", t, flags=re.I)
    t = re.sub(r"\bpolo shirt\b", " polo ", t, flags=re.I)
    t = re.sub(r"\b(t-?shirt|tshirt|sweatshirt|overshirt|rugby shirt|football shirt|shirt jacket|shirt-jacket)\b",
               lambda m: {"overshirt": "overshirt", "shirt jacket": "overshirt", "shirt-jacket": "overshirt"}.get(m.group(1).lower(), m.group(1)), t, flags=re.I)
    if re.search(r"\b(beanie|bobble hat|bucket hat|baseball cap|cap|scarf|gloves?|snood)\b", t, re.I) and not re.search(r"\b(jumper|cardigan|jacket|hoodie|toe cap)\b", t, re.I):
        return "acc"
    # Shorts (also "jersey short", "cargo short") are trousers, whatever else the title says.
    if re.search(r"\bshorts?\b", t, re.I) and not re.search(r"\b(swim|board|trunks?|pyjama|lounge|sleep)\b", t, re.I):
        return "trouser"
    for c, rx in CATS:
        if c == "shirt" and re.search(r"\b(t-?shirt|tshirt|sweatshirt)\b", t, re.I):
            continue
        if rx.search(t):
            if c == "basics" and re.search(r"\b(jumper|hoodie|sweatshirt|jacket|shirt|polo)\b", t, re.I) and not re.search(r"\bsocks?|boxers?|briefs?|underwear\b", t, re.I):
                continue
            if c == "polo" and re.search(r"\btop\b", t, re.I) and not re.search(r"\b(polo|tee|t-?shirt|henley|vest)\b", t, re.I):
                if re.search(r"\b(jumper|knit|sweat|fleece|hood)\b", ptype, re.I):
                    return "knit"
            return c
    pt = BRAND_JUNK.sub(" ", ptype + " " + " ".join(tags[:12]))
    for c, rx in CATS:
        if rx.search(pt):
            return c
    return None


JUNK_VENDOR = re.compile(r"^(special offers?|clearance|sale|outlet|archive|default|vendor|men'?s|mens|unbranded|"
                         r"generic|new|.*wholesale.*|.*\.(com|co\.uk)|.*\b(ltd|limited)\b.*)$", re.I)


def clean_title(title, vendor, shop):
    t = html.unescape(title).replace("’", "'").replace("‘", "'")
    t = re.sub(r"\b(wholesale|adults?|unisex|gents?)\b\s*", "", t, flags=re.I)
    t = re.sub(r"\[[^\]]*\]|\(\s*\)", "", t)
    t = re.sub(r"\b[A-Z]{1,3}\d{2,}[A-Z0-9]{2,}\b\s*", "", t)
    t = re.sub(r"^(?:[A-Z]{2,}(?:-[A-Z0-9]{2,})+|lsc-\w+|open)\s+", "", t)  # feed codes such as CLO-TOP-TEE
    t = re.sub(r"^\s*(special offer|sale|clearance|offer|new|last chance|bargain|outlet|archive|"
               r"reduced|limited edition|exclusive|pre-?order|web exclusive)\s*[:!\-–|]*\s*", "", t, flags=re.I)
    t = re.sub(r"\s*[-–|:]\s*(special offer|sale|clearance|last chance|reduced|online exclusive)\s*$", "", t, flags=re.I)
    t = re.sub(r"\s*\((sale|special offer|clearance)\)", "", t, flags=re.I)
    t = re.sub(r"\s*\|\s*", " - ", t)
    t = re.sub(r"\b(mens|men's|men|man's)\b\s*", "", t, flags=re.I).strip(" -–,")
    t = re.sub(r"^(special offer|clearance|sale)\s+", "", t, flags=re.I)
    for b in sorted({vendor, shop, "Tokyo Laundry", "Kensington Eastside", "Gabicci Vintage", "Gabicci Heritage", "Gabicci Classic"}, key=len, reverse=True):
        if b and len(b) > 2:
            t = re.sub(r"^\s*" + re.escape(b) + r"\s*[-–:]?\s*", "", t, flags=re.I)
            t = re.sub(r"(\s*[-–]\s*|\s+)" + re.escape(b) + r"\s*$", "", t, flags=re.I)
            t = re.sub(r"\s+" + re.escape(b) + r"\s+(?=[-–])", " ", t, flags=re.I)
    # One colour only: drop repeats such as "Navy - Navy" or "Black/Black".
    parts = [x.strip() for x in re.split(r"\s+[-–]\s+|\s*/\s*(?=[A-Z])", t) if x.strip()]
    keep, seen = [], set()
    for x in parts:
        k = x.lower()
        if k in seen:
            continue
        seen.add(k)
        keep.append(x)
    words, out, seenc = " - ".join(keep).split(), [], set()
    for w in words:
        lw = re.sub(r"\W", "", w.lower())
        if lw in COLOURS:
            if lw in seenc:
                continue
            seenc.add(lw)
        if out and re.sub(r"\W", "", out[-1].lower()) == lw:
            continue
        out.append(w)
    t = " ".join(out).strip(" -–,")
    t = re.sub(r"\s+M$", "", t)
    t = " ".join(w.title() if w.isupper() and len(w) > 3 and w not in ("PCVL", "MA-1", "N-3B") else w for w in t.split())
    return t


def make_name(title, vendor, shop, colour):
    t = clean_title(title, vendor, shop)
    vendor = re.sub(r"\s+(clothing|apparel|europe|uk|us|ltd|accessories|footwear|cap|store)$", "", (vendor or "").strip(), flags=re.I)
    vendor = re.sub(r"^(lsc-\w+|open|[A-Z]{2,}(?:-[A-Z0-9]{2,})+)$", "", vendor)
    vendor = re.sub(r"^Corgi Socks$", "Corgi", vendor)
    brand = vendor if vendor and not JUNK_VENDOR.match(vendor) and vendor.lower() != shop.lower() and len(vendor) < 30 and not re.search(r"\d", vendor) else shop
    if re.sub(r"\s*(&|and)\s*", " ", brand.lower()) in re.sub(r"\s*(&|and)\s*", " ", t.lower()):
        name = t
    else:
        name = brand + " " + t
    if colour and not COLOUR_RE.search(name) and colour.lower() not in name.lower() and len(colour) < 24 \
            and not re.search(r"\d|size|default|one|regular|r$", colour, re.I):
        name += ", " + colour.lower()
    name = re.sub(r"\s{2,}", " ", name).strip(" -–,")
    if len(name) > 90:
        name = name[:90].rsplit(" ", 1)[0].strip(" -–,")
    return name


def colour_of(p, v):
    for name, val in opts(p, v):
        if re.search(r"colou?r|shade", name, re.I):
            return val
    return ""


def occ_wx(cat, title):
    tl = title.lower()
    occ, wx = ["everyday"], ["mild"]
    if cat in ("tailor",):
        occ, wx = ["smart", "event"], ["mild", "cold"]
    elif cat == "shirt":
        occ = ["everyday", "smart"] if re.search(r"oxford|formal|poplin|twill|dress|non-iron", tl) else ["everyday", "party"]
        wx = ["mild", "warm"] if re.search(r"linen|short sleeve|cuban|camp|resort|hawaiian", tl) else ["mild", "cold"] if "flannel" in tl else ["mild"]
    elif cat == "coat":
        wx = ["mild", "wet"] if re.search(r"rain|waterproof|mac|cagoule|shell|anorak|smock", tl) else ["cold", "mild"]
        if re.search(r"parka|puffer|down|insulated|padded|wool", tl):
            wx = ["cold"]
        if re.search(r"waterproof|rain", tl):
            wx = sorted(set(wx + ["wet"]))
    elif cat == "knit":
        wx = ["cold", "mild"]
        if re.search(r"hood|sweat|fleece", tl):
            occ = ["everyday", "lounge"]
    elif cat == "polo":
        wx, occ = ["mild", "warm"], ["everyday", "party"]
    elif cat == "trouser":
        if re.search(r"\bshorts\b", tl):
            wx = ["warm"]
        else:
            wx = ["mild", "cold"]
        if re.search(r"jogger|track|sweat", tl):
            occ = ["everyday", "lounge"]
    elif cat == "swim":
        wx, occ = ["warm"], ["everyday"]
    elif cat in ("lounge", "basics"):
        occ, wx = ["lounge"], ["mild", "cold"]
    elif cat == "shoe":
        wx = ["mild", "cold", "wet"] if re.search(r"boot", tl) else ["mild", "warm"] if re.search(r"sandal|espadrille|slide|flip", tl) else ["mild"]
        if re.search(r"loafer|derby|oxford|brogue|monk", tl):
            occ = ["everyday", "smart"]
    elif cat == "acc":
        wx = ["cold"] if re.search(r"beanie|glove|scarf|snood|bobble", tl) else ["mild"]
    return occ, wx


def styles_for(host, group, cat, title):
    tl = title.lower()
    st = list(GROUP_STYLE.get(group, ["casual"]))
    if group == "Workwear and safety boots" and bare(host) in NOT_JOB:
        st = ["outdoor"] if bare(host) in OUTDOORISH else ["casual"]
    if cat == "swim" or re.search(r"linen|resort|cuban|hawaiian|board ?short|sandal|espadrille", tl):
        st.append("summer")
    if cat in ("lounge",) or re.search(r"pyjama|lounge|jogger", tl):
        st.append("lounge")
    if re.search(r"waterproof|hiking|walking|fleece|softshell|insulated|down jacket|trail", tl) and "job" not in st:
        st.append("outdoor")
    if re.search(r"harrington|fred perry|monkey boot|desert boot|fishtail|tonic|loafer|polo shirt|knitted polo|stay ?press", tl) and "job" not in st:
        st.append("mod")
    if cat == "tailor" and "quiet" not in st:
        st.append("quiet")
    seen, out = set(), []
    for s in st:
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out


def sets_for(cat, wx, title):
    s = []
    if "cold" in wx and cat in ("coat", "knit", "acc", "shoe"):
        s.append("winter")
    if "warm" in wx or cat == "swim":
        s.append("holiday")
    return s


def slug(host, handle):
    h = re.sub(r"^www\.|\.(co\.uk|com|org\.uk|co|uk)$", "", host)
    h = re.sub(r"[^a-z0-9]+", "", h.split(".")[0])[:10]
    return (h + "-" + re.sub(r"[^a-z0-9]+", "-", handle.lower()))[:70].strip("-")


def note_for(cat, price, was, fabric, size, wide, job):
    bits = []
    if was > price:
        bits.append("Down from £%s to £%s (%d%% off)." % (fmt(was), fmt(price), round(100 * (was - price) / was)))
    else:
        bits.append("£%s, full price." % fmt(price))
    if fabric:
        bits.append(fabric[0].upper() + fabric[1:] + ".")
    if wide:
        bits.append("Extra wide fitting.")
    if size and size not in ("One size",):
        bits.append("%s in stock at the last check." % size)
    return " ".join(bits)


def fmt(x):
    return ("%d" % x) if abs(x - round(x)) < 0.005 else ("%.2f" % x)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("catdir")
    ap.add_argument("--out", default=os.path.join(ROOT, "data", "items-new.json"))
    ap.add_argument("--date", default="2026-10-06")
    ap.add_argument("--per-shop", type=int, default=60)
    ap.add_argument("--per-cat", type=int, default=14)
    a = ap.parse_args()

    shops = shop_directory()
    old = json.load(open(os.path.join(ROOT, "data", "items.json"), encoding="utf-8"))
    for extra in glob.glob(os.path.join(ROOT, "data", "items-*.json")):
        if os.path.abspath(extra) != os.path.abspath(a.out):
            old.update(json.load(open(extra, encoding="utf-8")))
    old_urls = {re.sub(r"[?#].*", "", v["url"]).rstrip("/").lower() for v in old.values()}
    old_names = {re.sub(r"\W", "", v["name"].lower()) for v in old.values()}

    cands = collections.defaultdict(list)
    stats = collections.Counter()
    for path in sorted(glob.glob(os.path.join(a.catdir, "*.json"))):
        host = os.path.basename(path)[:-5]
        name, group = shops.get(bare(host), (None, None))
        if not name:
            stats["no shop name"] += 1
            continue
        try:
            prods = json.load(open(path))
        except Exception:
            continue
        # A shop that sells to women too needs a men's signal on each product.
        wfrac = sum(1 for p in prods if WOMEN.search(p.get("title", "") + " " + p.get("product_type", "") + " " + " ".join(p.get("tags", [])[:30]))) / max(1, len(prods))
        need_men = wfrac > 0.08
        us_shop = sum(1 for p in prods[:300] for v in p.get("variants", [])[:30]
                      if re.search(r"\bUS\b", " ".join(x for x in (v.get("option1"), v.get("option2")) if x) or "")) > 3
        for p in prods:
            title = p.get("title") or ""
            tags = p.get("tags") or []
            if isinstance(tags, str):
                tags = [t.strip() for t in tags.split(",")]
            ptype = p.get("product_type") or ""
            hay = " ".join([title, ptype, " ".join(tags), p.get("handle", "")])
            if re.search(r"\b\d{1,2}(-\d{1,2})? ?(years?|yrs)\b|\bage \d|school ?(uniform|shirt|trouser|jumper)|\bkids?\b", title, re.I):
                stats["children's"] += 1
                continue
            if WOMEN.search(title + " " + ptype + " " + p.get("handle", "").replace("-", " ")) or re.search(r"\sW(\s|$)|\bwnba\b", title.strip(), re.I):
                stats["women"] += 1
                continue
            if need_men and not MEN.search(hay.replace("-", " ")):
                stats["no men signal"] += 1
                continue
            if NOT_CLOTHES.search(title + " " + ptype):
                stats["not clothes"] += 1
                continue
            cat = category(title, ptype, tags)
            if not cat:
                stats["no category"] += 1
                continue
            body = strip_tags(p.get("body_html"))
            if cat == "trouser" and re.search(r"short[- ]leg|\bshort\b(?!s)|petite|\b34\"? ?leg|\bL ?34\b|long leg|tall\b", title, re.I):
                stats["short or long leg"] += 1
                continue
            if "[]" in title or re.search(r"^\W|\bclearance\s+\d", title, re.I):
                continue
            if SKINNY.search(title) or (cat == "trouser" or (cat == "tailor" and re.search(r"trouser", title, re.I))) and SLIM.search(title + " " + ptype):
                stats["slim"] += 1
                continue
            is_safety = cat == "shoe" and SAFETY.search(title + " " + ptype + " " + " ".join(tags))
            job = "job" in GROUP_STYLE.get(group, []) and bare(host) not in NOT_JOB and (
                cat != "shoe" or bool(is_safety) or re.search(r"\b(work|rigger|dealer|wellington)\b", title, re.I))
            if not job and re.search(r"\b(work ?wear|work trousers?|safety|hi[- ]?vis|kneepad|knee pad|rigger)\b", title, re.I):
                job = True
            # Workwear rules: safety footwear only; real work clothing; no T-shirts (work gives
            # him those); trousers and shorts black or charcoal, no stretch; no tailoring.
            if job and cat == "shoe" and not is_safety:
                job = False
            if job and cat != "shoe" and bare(host) not in WORK_SHOPS and not WORK_BRAND.search(
                    " ".join([title, p.get("vendor") or "", ptype, " ".join(tags[:20])])):
                job = False
            if job and cat == "tailor":
                job = False
            if job and cat == "polo" and re.search(r"\b(t-?shirts?|tees?|t|vests?|tank|singlet)\b", title, re.I):
                stats["job T-shirt"] += 1
                continue
            if job and cat == "trouser" and (not DARK.search(title + " " + " ".join(str(v.get("option1") or "") for v in p.get("variants", [])[:1]))
                                             or re.search(r"stretch", title, re.I)):
                stats["job trousers not black or stretch"] += 1
                continue
            if job and cat == "trouser" and (re.search(r"cordura", body, re.I) or re.search(r"\bpack\b", title, re.I)):
                stats["job Cordura or bundle"] += 1
                continue
            if job and cat in ("coat", "knit", "shirt") and re.search(
                    r"\b(ecru|white|cream|stone|beige|sand|natural|greige|oatmeal|undyed|light)\b", title, re.I):
                job = False
            if job and SLIM.search(title + " " + " ".join(tags)):
                stats["slim job"] += 1
                continue
            is_safety = cat == "shoe" and SAFETY.search(title + " " + ptype + " " + " ".join(tags))
            wide = bool(WIDE_X.search(title + " " + " ".join(tags) + " " + ptype)) or bool(WIDE_X.search(body[:600]))
            if is_safety and not wide:
                stats["safety not wide"] += 1
                continue
            cot = cotton_pct(body)
            if job and cat in ("trouser", "shirt", "polo", "knit", "coat") and not is_safety:
                if cot is None or cot < 60:
                    stats["job low cotton"] += 1
                    continue
            hit = None
            for v in p.get("variants", []):
                if not v.get("available"):
                    continue
                sz = size_ok(cat, p, v, title, us_shop)
                if sz:
                    hit = (v, sz)
                    break
            if not hit and p.get("nosizes") and p.get("variants"):
                hit = (p["variants"][0], "")  # the shop does not publish stock by size
            if not hit:
                stats["not in his size"] += 1
                continue
            v, sz = hit
            try:
                price = float(v.get("price") or 0)
                was = float(v.get("compare_at_price") or 0)
            except ValueError:
                continue
            if price < 3 or price > 600:
                continue
            if was <= price * 1.04:
                was = 0
            url = p.get("url") or "https://%s/products/%s" % (host, p["handle"])
            seg = (urllib.parse.urlparse(url).path.lower().strip("/").split("/") or [""])[0]
            if (re.fullmatch(r"[a-z]{2}(-[a-z]{2})?", seg) and seg not in ("gb", "uk", "en-gb", "en-uk", "en")) or \
                    re.search(r"/(en-us|en-au|en-ca|us)/", urllib.parse.urlparse(url).path.lower()):
                stats["not a UK page"] += 1
                continue
            if re.sub(r"[?#].*", "", url).rstrip("/").lower() in old_urls:
                stats["already a pick"] += 1
                continue
            colour = colour_of(p, v)
            nm = make_name(title, p.get("vendor") or "", name, colour)
            if re.sub(r"\W", "", nm.lower()) in old_names:
                stats["already a pick"] += 1
                continue
            imgs = p.get("images") or []
            img = ""
            if imgs:
                vid = v.get("id")
                img = next((i["src"] for i in imgs if vid in (i.get("variant_ids") or [])), imgs[0]["src"])
            occ, wx = occ_wx(cat, title)
            st = ["job"] if job else styles_for(host, group if not ("job" in GROUP_STYLE.get(group, []) and bare(host) not in NOT_JOB) else "High street", cat, title)
            disc = (was - price) / was if was else 0
            fab = fabric_of(body) if cot is not None or "%" in body[:400] else ""
            it = {
                "name": nm, "shop": name, "cat": cat, "price": round(price, 2),
                "url": url + ("?variant=%s" % v["id"] if v.get("id") and not p.get("url") else ""),
                "style": st, "occ": occ, "wx": wx,
                "note": note_for(cat, price, was, fab, sz, wide, job),
                "rank": int(300 - 160 * disc + min(price, 200) / 4),
                "sets": sets_for(cat, wx, title), "insize": True if sz else None,
                "sizes": ("%s in stock" % sz) if sz and sz not in ("One size",) else ("One size" if sz else ""),
                "kind": "new", "checked": a.date, "added": a.date, "img_src": img,
            }
            if was:
                it["was"] = round(was, 2)
            if fab:
                it["fabric"] = fab
            if sz == "34W (leg not listed)":
                it["sizeNote"] = "Leg length not listed: check it is a 32in (regular) leg."
                it["sizes"] = "34W in stock"
            if wide:
                it["sizeNote"] = "Extra wide fitting (4E or wider)." if cat == "shoe" else it.get("sizeNote", "")
                if not it["sizeNote"]:
                    del it["sizeNote"]
            cands[host].append((disc, it, p["handle"]))
            stats["candidate"] += 1

    out, used = {}, set()
    for host, lst in cands.items():
        lst.sort(key=lambda x: (-x[0], x[1]["price"]))
        bycat, n = collections.Counter(), 0
        seen_names = set()
        # Discounted pieces fill each shop's quota first, then full price up to a third of it.
        full = 0
        for disc, it, handle in lst:
            if n >= a.per_shop:
                break
            if bycat[it["cat"]] >= a.per_cat:
                continue
            if disc == 0:
                if full >= a.per_shop // 3:
                    continue
                full += 1
            if it["name"].lower() in seen_names:
                continue
            seen_names.add(it["name"].lower())
            key = re.sub(r",.*$", "", it["name"].lower())
            if (key, it["cat"]) in seen_names and bycat[it["cat"]] >= 3:
                continue
            seen_names.add((key, it["cat"]))
            k = slug(host, handle)
            if k in old or k in out:
                continue
            out[k] = it
            bycat[it["cat"]] += 1
            n += 1
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=0)
    print(dict(stats))
    print(len(out), "picks from", len(cands), "shops")
    print(collections.Counter(v["cat"] for v in out.values()))
    print(collections.Counter(s for v in out.values() for s in v["style"]))


if __name__ == "__main__":
    main()
