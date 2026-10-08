"""Reads each shop's men's tops size chart and writes what sizes M, L and XL mean there.

    python3 tools/size_charts.py [--shops "A,B"] [--out data/sizecharts.json]

For every shop in SHOPS below it fetches the shop's own size-guide page (or its Shopify product
JSON, or its sizing API), finds the chart, and stores the chest for M, L and XL in inches, with
whether the chart gives the body ("to fit chest") or the garment's own chest, plus the shirt
collar for L and what waist 34 means where the same page says so. Shops whose chart cannot be
read go under "_missing" with the reason. With --shops only those shops are re-read and the rest
of the existing file is kept.

Rule from HANDOFF.md: shop pages are only ever requested directly from the shop (its own pages,
feeds and JSON endpoints) or opened in headless Chromium (tools/size_charts_browser.js). Never
route them through relays, readers, caches or scraping services.

Each entry in SHOPS says where the chart is and how to read it:
  url     the page holding the chart
  via     "get" (plain request, the default), "browser" (headless Chromium, for pages that refuse
          plain requests or draw the chart with JavaScript), "shopify" (body_html of a product's
          .js), "asos" (ASOS's own size-guide API, opened in the browser)
  table   which chart to use: a regex matched against the text just before each table (its
          heading), or an int (the n-th table that has a chest row or column)
  text    for charts drawn without <table>: (anchor regex, value position) - reads "L 42 106.7"
          style runs in the page text after the anchor
  row     for charts drawn without <table> with sizes across the top: (anchor regex, row label regex) -
          reads "S M L XL Chest 88-96 96-104 104-112 112-124" after the anchor
  json    for charts kept as JSON records in the page: (size key, chest key), e.g. ("size", "chest")
  col     the chest column's index, for tables whose header row does not line up with the data
  unit    "cm" or "in" when the chart does not say
  kind    "body" or "garment"; half=True when the chart gives half the chest (pit to pit)
  collar  regex for the collar/neck column in the same chart (L's collar is stored)
  w34     a fixed note on waist 34 read from the same page, if any
  sizes   relabels when a shop names sizes differently, e.g. {"L": "4"}
"""
import argparse, datetime, html, json, os, re, subprocess, sys, tempfile, urllib.request
from html.parser import HTMLParser

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
HERE = os.path.dirname(os.path.abspath(__file__))
TODAY = datetime.date.today().isoformat()
ABOUT = ("Men's tops size charts by shop, read from each shop's own size guide. Inches. kind: body = to fit "
         "chest, garment = the garment's own chest. Checked date is when it was read.")

SHOPS = {}  # filled in below the helpers

# ---------------------------------------------------------------- fetching


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-GB,en;q=0.9",
                                               "Accept": "text/html,application/json;q=0.9,*/*;q=0.8"})
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read().decode("utf8", "replace")


def browser(jobs):
    """Open pages in headless Chromium (direct connection) and return {url: rendered html}.
    jobs: [(url, shop config)]; the config's click / pause / select steer the page."""
    if not jobs:
        return {}
    tmp = tempfile.mkdtemp(prefix="sizecharts-")
    spec = []
    for i, (url, cfg) in enumerate(jobs):
        spec.append({"url": url, "out": os.path.join(tmp, f"{i}.html"), "click": cfg.get("click"),
                     "pause": cfg.get("pause"), "select": cfg.get("select")})
    with open(os.path.join(tmp, "jobs.json"), "w") as f:
        json.dump(spec, f)
    env = dict(os.environ, NODE_PATH=os.environ.get("NODE_PATH", "/opt/node-tools/node_modules"))
    subprocess.run(["node", os.path.join(HERE, "size_charts_browser.js"), os.path.join(tmp, "jobs.json")],
                   env=env, timeout=60 * 30, check=False)
    out = {}
    for j in spec:
        if os.path.exists(j["out"]):
            out[j["url"]] = open(j["out"], errors="replace").read()
    return out

# ---------------------------------------------------------------- reading html


class Tables(HTMLParser):
    """Collects every <table> as rows of cell texts (colspans repeated so columns line up), the
    page's visible text, and for each table the visible text just before it (its heading)."""
    SKIP = {"script", "style", "noscript", "svg", "template", "head"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tables, self.text, self.stack, self.skip = [], [], [], 0
        self.cell = None

    def handle_starttag(self, tag, a):
        a = dict(a)
        if tag in self.SKIP:
            self.skip += 1
        elif tag == "table":
            self.stack.append({"rows": [], "ctx": re.sub(r"\s+", " ", "".join(self.text[-80:]))[-200:]})
        elif tag == "tr" and self.stack:
            self.stack[-1]["rows"].append([])
        elif tag in ("td", "th") and self.stack:
            if not self.stack[-1]["rows"]:
                self.stack[-1]["rows"].append([])
            span = re.sub(r"\D", "", a.get("colspan") or "1") or "1"
            self.cell = {"txt": [], "span": min(int(span), 12)}
        elif tag in ("br", "p", "div", "li", "h1", "h2", "h3", "h4", "h5", "h6"):
            self.text.append(" ")

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            self.skip = max(0, self.skip - 1)
        elif tag in ("td", "th") and self.stack and self.cell is not None:
            t = re.sub(r"\s+", " ", "".join(self.cell["txt"])).strip()
            self.stack[-1]["rows"][-1].extend([t] * self.cell["span"])
            self.cell = None
        elif tag == "table" and self.stack:
            t = self.stack.pop()
            t["rows"] = [r for r in t["rows"] if any(x for x in r)]
            self.tables.append(t)

    def handle_data(self, d):
        if self.skip:
            return
        if self.cell is not None:
            self.cell["txt"].append(d)
        self.text.append(d)


def parse_html(s):
    # charts kept in JSON strings (Shopify settings, page builders) hold escaped html
    if "\\u003c" in s or "\\u003C" in s:
        s += "\n" + s.replace("\\u003c", "<").replace("\\u003C", "<").replace("\\u003e", ">") \
            .replace("\\u003E", ">").replace('\\"', '"').replace("\\/", "/")
    p = Tables()
    p.feed(s)
    text = re.sub(r"\s+", " ", "".join(p.text))
    return p.tables, text

# ---------------------------------------------------------------- reading a chart

SIZE_WORDS = {"S": ("s", "small"), "M": ("m", "medium", "med"), "L": ("l", "large", "lrg"),
              "XL": ("xl", "x-large", "x large", "extra large", "xlarge", "1xl")}
NUM = r"\d+(?:\.\d+)?(?:\s*½)?"
RANGE = NUM + r"(?:\s*(?:-|–|—|to|/)\s*" + NUM + r")?"


def size_of(cell, relabel=None):
    """'L', 'Large', 'L (42")', 'UK L' -> 'L' (or None)."""
    t = re.sub(r"\s+", " ", cell.strip().lower())
    t = re.sub(r"^(uk|size|uk size)\s+", "", t)
    if relabel:
        for k, v in relabel.items():
            if t == v.lower() or re.match(re.escape(v.lower()) + r"\b", t):
                return k
    for k, words in SIZE_WORDS.items():
        for w in words:
            if t == w or re.match(re.escape(w) + r"(\s*[(/|:,]|\s+\d|\s*$)", t):
                return k
    return None


def numbers(cell):
    c = cell.replace(",", ".").replace("½", ".5").replace("¼", ".25").replace("¾", ".75")
    c = re.sub(r"(\d)\s+1/2", r"\1.5", re.sub(r"(\d)\s+1/4", r"\1.25", re.sub(r"(\d)\s+3/4", r"\1.75", c)))
    c = re.sub(r"(\d)\.(\d+)\.(\d+)", r"\1.\2", c)
    return [float(x.replace(" ", "")) for x in re.findall(r"\d+(?:\.\d+)?", c)]


def split_units(cell):
    """'107cm 42"' or '43" / 109cm' -> {"cm": [107], "in": [42]}; {} when the cell holds one unit."""
    c = cell.replace(",", ".").replace("½", ".5")
    out = {}
    for m in re.finditer(r"(\d+(?:\.\d+)?(?:\s*(?:-|–|to)\s*\d+(?:\.\d+)?)?)\s*(cms?|\"|”|''|inch(?:es)?|ins?(?![a-z]))", c, re.I):
        u = "cm" if m.group(2).lower().startswith("cm") else "in"
        out.setdefault(u, []).extend(numbers(m.group(1)))
    return out if len(out) == 2 else {}


def cell_value(cell, hdr=""):
    """Numbers in a chart cell and their unit; prefers inches when a cell gives both."""
    both = split_units(cell)
    if both:
        return both["in"], "in"
    return numbers(cell), unit_in(cell) or unit_in(hdr)


def unit_in(txt):
    t = txt.lower()
    if re.search(r"\bcms?\b|centimet", t):
        return "cm"
    if re.search(r"inch|\bins?\b|\"|”|''", t):
        return "in"
    return None


CHEST = r"chest|pit|p2p|ptp"


def read_grid(rows, relabel=None, collar=None, chest=CHEST, col=None):
    """Chest (and collar) per size from one table, sizes down the side or across the top.
    Returns {size: {"v": [numbers], "unit": unit or None, "head": header text, "collar": text}}.
    `col` names the chest column outright, for tables whose headers do not line up with the data."""
    out = {}
    if col is not None:
        for r in rows:
            k = size_of(r[0], relabel) if r else None
            if k and k not in out and col < len(r) and numbers(r[col]):
                v, u = cell_value(r[col])
                out[k] = {"v": v, "unit": u, "head": f"column {col}", "all": [], "collar": None}
        return out
    # sizes down the side: a header row naming a chest column
    for hi, hdr in enumerate(rows[:4]):
        cols = [i for i, h in enumerate(hdr) if re.search(chest, h, re.I)]
        if not cols:
            continue
        ccol = [i for i, h in enumerate(hdr) if collar and re.search(collar, h, re.I)]
        for r in rows[hi + 1:]:
            k = next((size_of(r[j], relabel) for j in range(min(2, len(r))) if size_of(r[j], relabel)), None)
            if not k or k in out:
                continue
            got = []
            for c in cols:
                if c < len(r) and numbers(r[c]):
                    v, u = cell_value(r[c], hdr[c])
                    sub = rows[hi + 1] if hi + 1 < len(rows) else []
                    if not u and c < len(sub) and not size_of(sub[0] if sub else ""):
                        u = unit_in(sub[c])
                    got.append((v, u))
            if got:
                v, u = got[0]
                out[k] = {"v": v, "unit": u, "head": hdr[cols[0]], "all": got,
                          "collar": r[ccol[0]] if ccol and ccol[0] < len(r) else None}
        if out:
            return out
    # sizes across the top: a row of size labels, and a row starting with "chest" (above or below
    # it, or the size row itself). When that row is only a label, the rows under it named "cm" /
    # "inches" hold the values (inches preferred).
    def labelled(label_re, keys, hi):
        for ri, r in enumerate(rows):
            if not r or not re.search(label_re, r[0], re.I):
                continue
            cand = [(r, unit_in(r[0]))] if ri != hi or True else []
            if not any(numbers(r[i]) for i in keys if i < len(r)) or ri == hi:
                cand = [(u, unit_in(u[0])) for u in rows[ri + 1: ri + 4]
                        if u and re.fullmatch(r"\s*(cms?|centimet\w*|inch(es)?|ins?)\s*", u[0], re.I)]
                cand.sort(key=lambda x: x[1] != "in")
            for row, u in cand:
                if any(i < len(row) and numbers(row[i]) for i in keys):
                    return row, u
        return None, None
    for hi, hdr in enumerate(rows[:6]):
        keys = {i: size_of(h, relabel) for i, h in enumerate(hdr) if i > 0}
        keys = {i: k for i, k in keys.items() if k}
        if len(set(keys.values())) < 2:
            continue
        r, ru = labelled(chest, keys, hi)
        if not r:
            continue
        crow, cu = labelled(collar, keys, hi) if collar else (None, None)
        for i, k in keys.items():
            if i < len(r) and numbers(r[i]) and k not in out:
                v, u = cell_value(r[i], r[0])
                out[k] = {"v": v, "unit": u or ru, "head": r[0], "all": [(numbers(r[i]), None)],
                          "collar": crow[i] if crow and i < len(crow) else None}
        if out:
            return out
    return out


def read_text(text, anchor, pos=0, relabel=None):
    """Charts drawn with divs: after `anchor`, read runs like 'M 40 101.6 L 42 106.7'."""
    m = re.search(anchor, text, re.I)
    if not m:
        return {}
    seg = text[m.end(): m.end() + 1500]
    out = {}
    for k, words in SIZE_WORDS.items():
        labels = [relabel[k]] if relabel and k in relabel else [w for w in words if w not in ("med", "lrg")]
        for w in labels:
            mm = re.search(r"(?<![\w-])" + re.escape(w) + r"\s+((?:" + RANGE + r")(?:\s*(?:cm|\"|in)?\s*(?:/|\|)?\s*(?:"
                           + RANGE + r"))*)", seg, re.I)
            if mm:
                vals = re.findall(RANGE, mm.group(1))
                if pos < len(vals):
                    out[k] = {"v": numbers(vals[pos]), "unit": None, "head": anchor, "all": [], "collar": None}
                    break
    return out


SIZE_TOKEN = r"(?:\d?X{0,4}[SL]|M)"


def read_row(text, anchor, label, relabel=None):
    """Charts drawn with divs, sizes across the top: after `anchor` a run of size labels, then `label` and one
    value per label ("XS S M L XL Chest 84-88 88-96 96-104 104-112 112-124"). A size named twice (its cm and
    its inch column) keeps its first value."""
    m = re.search(anchor, text, re.I)
    if not m:
        return {}
    seg = text[m.end(): m.end() + 3000]
    labels, pos = [], 0
    for t in re.finditer(r"\S+", seg):
        if not re.fullmatch(SIZE_TOKEN, t.group(0), re.I):
            break
        labels.append(t.group(0))
        pos = t.end()
    lm = re.search(label, seg[pos:], re.I)
    if len(labels) < 3 or not lm:
        return {}
    cells = re.findall(RANGE + r"|(?<!\S)[-–](?!\S)", seg[pos + lm.end():])[:len(labels)]
    out = {}
    for lbl, cell in zip(labels, cells):
        k = size_of(lbl, relabel)
        if k and k not in out and numbers(cell):
            out[k] = {"v": numbers(cell), "unit": None, "head": label, "all": [], "collar": None}
    return out


def read_json(raw, keys, relabel=None):
    """Charts kept as JSON records in the page, e.g. {"size":"L","chest":"102 - 108"} with keys ("size",
    "chest"): the first record for each size, so a chart given in cm and then in inches is read in cm."""
    sk, ck = keys
    out = {}
    for m in re.finditer(r"\{[^{}]*\}", raw):
        if '"%s"' % ck not in m.group(0):
            continue
        try:
            rec = json.loads(m.group(0))
        except ValueError:
            continue
        if not isinstance(rec, dict) or sk not in rec or ck not in rec:
            continue
        k = size_of(str(rec[sk]), relabel)
        if k and k not in out and numbers(str(rec[ck])):
            out[k] = {"v": numbers(str(rec[ck])), "unit": None, "head": ck, "all": [], "collar": None}
    return out


def to_inches(v, unit, half=False):
    """[lo, hi] in inches (cm / 2.54, doubled for half-chest charts), rounded to 0.5."""
    v = v[:2]
    if unit is None:
        unit = "cm" if max(v) > (31 if half else 62) else "in"
    f = (1 / 2.54 if unit == "cm" else 1.0) * (2 if half else 1)
    r = sorted(round(x * f * 2) / 2 for x in v)
    if len(r) == 1:
        r = r * 2
    return [int(x) if x == int(x) else x for x in r]


def pick_chart(cfg, tables, text, raw=""):
    if cfg.get("json"):
        return read_json(raw, cfg["json"], cfg.get("sizes")), "json"
    if cfg.get("row"):
        anchor, label = cfg["row"]
        return read_row(text, anchor, label, cfg.get("sizes")), anchor
    if cfg.get("text"):
        anchor, pos = cfg["text"]
        return read_text(text, anchor, pos, cfg.get("sizes")), anchor
    want = cfg.get("table", 0)
    n = 0
    for t in tables:
        got = read_grid(t["rows"], cfg.get("sizes"), cfg.get("collar"), cfg.get("chest", CHEST), cfg.get("col"))
        if not got or not all(k in got for k in ("M", "L", "XL")):
            continue
        if isinstance(want, int):
            if n == want:
                return got, t["ctx"]
            n += 1
        elif re.search(want, t["ctx"], re.I):
            return got, t["ctx"]
    return {}, None


def entry(cfg, got):
    """The JSON entry for one shop, or a reason it could not be read."""
    if not all(k in got for k in ("M", "L", "XL")):
        return None, "chart found but M, L or XL missing" if got else "no chart found on the page"
    e = {}
    for k in ("S", "M", "L", "XL"):
        if k in got:
            v = got[k]["v"]
            if "nth" in cfg:  # the cell holds several numbers (e.g. "59 23.2" = cm then inches)
                v = v[cfg["nth"]:cfg["nth"] + 1]
            e[k] = to_inches(v, cfg.get("unit") or got[k]["unit"], cfg.get("half"))
    if cfg.get("upto"):
        # the chart gives "chest up to": a size runs from the size below's limit to its own
        for k, below in (("XL", "L"), ("L", "M"), ("M", "S")):
            if below in e:
                e[k] = [e[below][1], e[k][1]]
    e.pop("S", None)
    e["kind"] = cfg.get("kind", "body")
    # sanity: a men's L is 36-50in round the body, or 38-56in for a garment
    lo, hi = (36, 50) if e["kind"] == "body" else (38, 56)
    if not (lo <= e["L"][0] <= hi and lo <= e["L"][1] <= hi) or not (e["M"][0] <= e["L"][0] <= e["XL"][0]):
        return None, f"chart read but values look wrong (L={e['L']})"
    if cfg.get("collar") and got["L"].get("collar"):
        c = got["L"]["collar"]
        cn = numbers(c)
        if cn and max(cn) > 25:  # collar given in cm
            cn = [round(x / 2.54 * 2) / 2 for x in cn]
        if cn:
            e["collar"] = "-".join(f"{x:g}" for x in sorted(set(cn)))
    if cfg.get("w34"):
        e["w34"] = cfg["w34"]
    e["src"] = cfg["url"]
    e["checked"] = TODAY
    if cfg.get("note"):
        e["note"] = cfg["note"]
    return e, None


def read_shop(name, cfg, pages):
    url = cfg["url"]
    try:
        if cfg.get("via") == "asos":
            raw = pages.get(url)
            if not raw:
                return None, "ASOS size API not reachable in the browser"
            m = re.search(r"<pre[^>]*>(.*?)</pre>", raw, re.S)
            data = json.loads(html.unescape(m.group(1) if m else raw))
            got = {}
            for z in data.get("sizes", []):
                k = size_of(z.get("brandSizeText", ""))
                for d in z.get("dimensions", []):
                    if k and re.search("chest", d.get("dimensionText", ""), re.I):
                        ms = {x["unit"].lower(): x["value"] for x in d.get("measurements", [])}
                        if "in" in ms:
                            got[k] = {"v": numbers(ms["in"]), "unit": "in", "head": "Chest", "all": [], "collar": None}
                        elif "cm" in ms:
                            got[k] = {"v": numbers(ms["cm"]), "unit": "cm", "head": "Chest", "all": [], "collar": None}
            return entry(cfg, got)
        if cfg.get("via") == "browser":
            raw = pages.get(url)
            if not raw:
                return None, "page did not open in headless Chromium"
        elif cfg.get("via") == "shopify":
            raw = json.loads(get(url)).get("description") or ""
        else:
            raw = get(url)
    except Exception as ex:  # noqa: BLE001 - any fetch error just marks the shop missing
        return None, f"could not fetch the size guide ({str(ex)[:60]})"
    tables, text = parse_html(raw)
    got, _ = pick_chart(cfg, tables, text, raw)
    return entry(cfg, got)

# ---------------------------------------------------------------- the shops


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shops", help="comma-separated shop names to re-read (default: all)")
    ap.add_argument("--out", default=os.path.join(HERE, "..", "data", "sizecharts.json"))
    a = ap.parse_args()
    names = [s.strip() for s in a.shops.split(",")] if a.shops else list(SHOPS)
    old = {}
    if a.shops and os.path.exists(a.out):
        old = json.load(open(a.out))
    res = {"_about": ABOUT}
    res.update({k: v for k, v in old.items() if not k.startswith("_")})
    missing = dict(old.get("_missing", {}))
    jobs = [(SHOPS[n]["url"], SHOPS[n]) for n in names
            if n in SHOPS and SHOPS[n].get("via") in ("browser", "asos")]
    pages = browser(jobs)
    for n in names:
        if n in MISSING:
            res.pop(n, None)
            missing[n] = MISSING[n]
            continue
        if n not in SHOPS:
            print(f"unknown shop: {n}", file=sys.stderr)
            continue
        e, why = read_shop(n, SHOPS[n], pages)
        if e:
            res[n] = e
            missing.pop(n, None)
            print(f"{n:28} L {e['L']} ({e['kind']})", flush=True)
        else:
            res.pop(n, None)
            missing[n] = why
            print(f"{n:28} MISSING: {why}", flush=True)
    for n in pick_shops() - set(SHOPS) - set(MISSING) - set(res):
            missing[n] = "not looked at yet: no chart source recorded in SHOPS"
    res["_missing"] = dict(sorted(missing.items()))
    keys = ["_about"] + sorted(k for k in res if not k.startswith("_")) + ["_missing"]
    with open(a.out, "w") as f:
        json.dump({k: res[k] for k in keys}, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"{len(keys) - 2} shops with charts, {len(res['_missing'])} missing -> {a.out}")

# Where each shop's chart is. Notes say which chart was used when a shop has several.
G = "garment"
SG = "size guide|size chart|sizing|size & fit|fit guide"  # text of the button that opens a product page's chart
SHOPS.update({
    "ASOS": dict(url="https://www.asos.com/api/sizing/sizeapi/v1/SizeGuide/9676?language=en-GB", via="asos",
                 note="ASOS DESIGN men's guide (ASOS's own label); other brands on ASOS use their own charts"),
    "M&S": dict(url="https://www.marksandspencer.com/c/size-guides?category=men&subcategory=tops", via="browser",
                pause=8000, unit="in", note="Men's Tops guide; casual shirts use the same chest sizes"),
    "Tokyo Laundry": dict(url="https://www.tokyolaundry.com/pages/size-guides", unit="in",
                          text=("Mens - Tops Size Chest Approx in Inches Chest Approx in CM", 0),
                          note="one approximate chest per size"),
    "Brakeburn": dict(url="https://www.brakeburn.com/pages/size-guide-2026", table=1, collar="collar"),
    "Lyle & Scott": dict(url="https://www.lyleandscott.com/pages/size-guides", via="browser", table=1,
                         note="Men's Tops chart, one chest value per size"),
    "Montirex": dict(url="https://montirex.com/pages/size-guide", table=0, unit="in"),
    "Original Penguin": dict(url="https://www.originalpenguin.co.uk/pages/size-guide", table=1),
    "Duck and Cover": dict(url="https://www.duckandcover.co.uk/pages/size-guide", table=0),
    "Farah": dict(url="https://www.farah.co.uk/pages/size-guide", table=1),
    "Luke 1977": dict(url="https://www.luke1977.com/products/hawich-overshirt-black", table=1, unit="in", kind=G,
                      note="no general chart; garment chest from the Hawich overshirt's own chart"),
    "Pretty Green": dict(url="https://www.prettygreen.com/products/multi-strobe-shirt", unit="cm", half=True, kind=G,
                         note="no general chart; pit-to-pit from a shirt's garment chart, doubled"),
    "T.M. Lewin": dict(url="https://tmlewin.co.uk/pages/size-guides", table="Casual fit", unit="in",
                       note="casual shirts chart; their polo, T-shirt and knitwear chart puts L at 42-44in"),
    "Tog24": dict(url="https://www.tog24.com/pages/size-guide-men", table=0, unit="in", note="one chest value per size"),
    "Universal Works": dict(url="https://www.universalworks.co.uk/products/soft-blue-mc-stripe-road-trip-shirt.js",
                            via="shopify", unit="cm", half=True, kind=G,
                            note="no general chart; chest width laid flat from a shirt's garment chart, doubled"),
    "Animal": dict(url="https://www.animal.co.uk/pages/size-guide", table=0, unit="cm"),
    "Berghaus": dict(url="https://www.berghaus.com/products/mens-harthwaite-shirt-grey-4a000144001", table=0,
                     note="men's chart for jackets, fleeces, base layers, shirts and tees (shown on product pages)"),
    "Cernucci": dict(url="https://cernucci.com/products/short-sleeve-boxy-check-shirt-navy", table=0,
                     note="tops chart shown on product pages (body measurements)"),
    "Skechers": dict(url="https://www.skechers.co.uk/on/demandware.store/Sites-UKSkechers-Site/en_GB/Product-SizeChart"
                         "?cid=mens-apparel", table=0, unit="in"),
    "Saltrock": dict(url="https://www.saltrock.com/products/blvd-s-s-shirt-dress-blue", via="browser",
                     click=SG, table=0, note="chart shown on a shirt's product page"),
    "Savile Row Company": dict(url="https://www.savilerowco.com/products/pink-linen-cotton-classic-fit-short-sleeve-"
                                   "button-down-casual-shirt-1357bpkmss", via="browser", click=SG, pause=6000,
                               table=0, unit="in", collar="collar",
                               note="classic-fit casual shirt chart; it also gives the shirt's own chest (L 50in)"),
    "Gym King": dict(url="https://www.gymking.com/pages/size-guide", table=0, col=3, unit="cm",
                     note="men's chart (UK sizes); the site may open its US page, the chart is the same"),
    "Percival": dict(url="https://www.percivalclo.com/products/drape-cuban-shirt-percival-x-warren-mint-green",
                     unit="cm", half=True, kind=G,
                     note="no general chart; pit-to-pit from the Drape Cuban shirt's chart, doubled"),
    "Samuel Windsor": dict(url="https://www.samuel-windsor.co.uk/pages/size-guide", table=0, unit="in",
                           note="classic-fit shirts chart"),
    "Schöffel": dict(url="https://www.schoffelcountry.com/pages/size-guide", table="polos", unit="in",
                     note="polos and T-shirts chart; jackets and knitwear use numbered sizes"),
    "KAVU": dict(url="https://www.kavu.co.uk/pages/size-guide", table=r"\bMenswear Sizes", unit="in",
                 note="the chart says it gives body sizes"),
    "Folk": dict(url="https://www.folkclothing.com/products/folk-relaxed-fit-shirt-black-melange", unit="cm", half=True,
                 kind=G, note="no general chart; chest laid flat from the relaxed-fit shirt's chart, doubled"),
    "Bamboo Clothing": dict(url="https://www.bambooclothing.co.uk/pages/size-guides", table=2, unit="in"),
    "Dubarry": dict(url="https://www.dubarry.com/products/gilligan-mens-tencel-modal-polo-black", table=0,
                    note="men's clothing chart for outerwear, knits and polos (shown on product pages)"),
    "Volcom": dict(url="https://www.volcom.co.uk/pages/size-chart-all", table=0, note="apparel tops chart (US sizing)"),
    "Uniqlo": dict(url="https://www.uniqlo.com/uk/en/products/E486614-000/00", via="browser", chest="body width",
                   unit="in", half=True, kind=G,
                   note="no general chart; body width from the product's own measurements, doubled"),
    "Ellesse": dict(url="https://www.ellesse.com/pages/size-guides", table=0, unit="in"),
    "Gabicci": dict(url="https://www.gabicci.com/pages/size-guides", table=0,
                    note="Heritage knitwear chart; Heritage and Vintage shirts give the same to-fit chest"),
    "Stan Ray": dict(url="https://www.stanray.com/products/quilted-plaid-overshirt-brown-aw25", via="browser",
                     click=SG, pause=6000, table=0, half=True, kind=G,
                     note="no general chart; pit-to-pit from the quilted overshirt's chart, doubled"),
    "Universal Textiles": dict(url="https://www.universal-textiles.com/pages/size-guides", table=0, unit="in",
                               note="the shop's general men's clothing guide (it sells several brands)"),
    "Threadbare": dict(url="https://threadbare.com/pages/mens-size-guide", table=0),
    "Ted Baker": dict(url="https://www.tedbaker.com/products/stripe-shirt-light-blue", via="browser",
                      click=SG, pause=6000, table=0, unit="in", collar="collar",
                      note="Ted size 4 is L; one chest value per size"),
    "Puma": dict(url="https://uk.puma.com/uk/en/pd/tad-essentials-solid-cat-tee-men/525908", via="browser",
                 click=SG, chest="bust", unit="cm", kind=G,
                 note="no general chest chart; garment chest from a T-shirt's product measurements"),
    "Sealskinz": dict(url="https://www.sealskinz.com/products/shingham-mens-short-sleeve-print-trail-shirt",
                      via="browser", click=SG, table=0, unit="in", note="chart shown on a shirt's product page"),
    "Lazy Jacks": dict(url="https://www.lazyjacks.co.uk/pages/size-guide-new", table=0, collar="neck",
                       note="men's body size chart"),
    "Hikerdelic": dict(url="https://www.hikerdelic.com/pages/size-guide", table=1),
    "Finisterre": dict(url="https://finisterre.com/pages/size-guide", table=1, note="men's tops and jackets"),
    "Rydale": dict(url="https://www.rydale.com/products/ebberston-country-check-shirts", via="browser",
                   click=SG, table=0, unit="in", note="'your chest size', one value per size"),
    "Alpkit": dict(url="https://www.alpkit.com/products/blank-canvas-tee-m", table=0, unit="cm", half=True, kind=G,
                   note="men's T-shirt chart: half chest 2.5cm below the armhole, doubled"),
    "Montane": dict(url="https://www.montane.com/pages/size-guide-men", table=0, note="one chest value per size"),
    "Speedo": dict(url="https://www.speedo.com/products/unisex-v-class-pro-hoodie-blue-800506117966", table=0,
                   unit="in", note="chart shown on product pages"),
    "howies": dict(url="https://www.howies.co.uk/pages/size-chart", table=0, unit="in"),
    "Peregrine": dict(url="https://peregrineclothing.co.uk/products/kenilworth-shirt", via="browser", table=0,
                      click=SG, pause=6000, chest=r"^cm\b",
                      nth=0, unit="cm", half=True, kind=G,
                      note="no general chart; chest laid flat from the Kenilworth shirt's measurements, doubled"),
    "Peacocks": dict(url="https://www.peacocks.co.uk/on/demandware.store/Sites-peacocks-Site/default/Product-SizeChart"
                         "?cid=size-guide-mens-general", table=0),
    "Closure London": dict(url="https://www.closurelondon.com/pages/size-guide", table=0, unit="in",
                           note="one chest value per size"),
    "Trespass": dict(url="https://www.trespass.com/size-chart", table=1, unit="in"),
    "M and M Direct": dict(url="https://www.mandmdirect.com/gb/en/sizecharts", table=0,
                           note="the shop's general men's tops chart (it sells many brands)"),
    "Criminal Damage": dict(url="https://www.criminaldamage.co.uk/pages/size-guide", table=0, kind=G,
                            note="T-shirt garment chest (full round)"),
    "Brook Taverner": dict(url="https://www.brooktaverner.co.uk/size-guide/", table=0, collar="collar",
                           note="shirts chart; the collar is the shirt's own measurement"),
    "Charles Tyrwhitt": dict(url="https://www.charlestyrwhitt.com/uk/size-guides/SS26-casual-shirts.html", table=0,
                             unit="in", collar="neck", upto=True,
                             note="casual shirts; the chart gives chest 'up to', so L is over 41.5in up to 45in"),
    "Merc": dict(url="https://www.merc.co.uk/pages/size-guide", table=0),
    "Weird Fish": dict(url="https://www.weirdfish.co.uk/info/sizing-info", table=0, note="one chest value per size"),
    "Jump the Gun": dict(url="https://www.jumpthegun.co.uk/products/the-six-button-oxford-sky", table=0,
                         chest="pit", unit="in", half=True, kind=G,
                         note="no general chart; pit-to-pit from the Oxford shirt's chart, doubled"),
    "Mountain Equipment": dict(url="https://www.mountain-equipment.co.uk/pages/size-chart", table=0),
    "Haglöfs": dict(url="https://www.haglofs.com/en/explore-haglofs/guides/size-guide", table=1, unit="in",
                    note="Size Guide A (most garments), one chest value per size"),
    "Thought": dict(url="https://www.wearethought.com/pages/size-guide-mens", table=0, collar="neck",
                    note="men's guide in UK sizes (the site may open its US page)"),
    "Seasalt": dict(url="https://www.seasaltcornwall.com/need-help/size-guide", table=0, unit="cm"),
    "SikSilk": dict(url="https://siksilk.gorgias.help/en-US/siksilk-menswear-size-guide-28255", table=0, unit="cm",
                    note="menswear tops chart in the shop's help centre (linked from its size-guide page); the cm "
                         "ranges are used, its inch column gives one value per size (L 42in)"),
    "Passenger": dict(url="https://www.passenger-clothing.com/products/acreage-organic-cotton-shirt-khaki",
                      via="browser", click="Size & Fit Guide", pause=6000, table=0, unit="cm",
                      note="body chart in the product page's Size & Fit Guide"),
    "Blue Inc": dict(url="https://www.blueinc.co.uk/pages/size-guide", table=0,
                     note="one chart for all tops, knitwear, jackets, coats and shirts"),
    "O'Neill": dict(url="https://uk.oneill.com/pages/mens-tees-shortsleeve", table=0, unit="cm",
                    note="men's tees chart; its hoodies, shirts and jackets charts give the same chest"),
    "Superdry": dict(url="https://cdn.superdry.com/size_guides/mens_en_310.html", table=r"Chest\s*$",
                     chest=r"^inches$", unit="in", note="men's size guide shown on product pages (chest table)"),
    "River Island": dict(url="https://www.riverisland.com/how-can-we-help/size-guides/mens",
                         table=r"Tops & Shirts\s*$", note="men's tops and shirts chart"),
    "Regatta": dict(url="https://www.regatta.com/size-guide/", table=r"Men's - Jackets, Fleeces", unit="in",
                    note="men's jackets, fleeces, gilets, shirts and T-shirts chart"),
    "TuffStuff": dict(url="https://www.tuffstuffworkwear.co.uk/products/tuffstuff-logo-t-shirt", table=0, unit="in",
                      note="chest (approx) chart shown on its product pages; workwear sizing runs large"),
    "AllSaints": dict(url="https://www.allsaints.com/sizeguide.html", table=1, unit="in", collar="neck",
                      note="menswear clothing chart in inches, one chest value per size"),
    "Weekend Offender": dict(url="https://www.weekendoffender.com/pages/t-shirts-polos-size-guide", table=0, col=1,
                             unit="cm", half=True, kind=G,
                             note="T-shirts and polos chart: chest laid flat (pit to pit), doubled"),
    "Mountain Warehouse": dict(url="https://www.mountainwarehouse.com/help/size-guide/",
                               table=r"Mens Jackets & Tops\s*$", note="men's jackets and tops chart (cm row used)"),
    "Nike": dict(url="https://www.nike.com/gb/size-fit/mens-tops-alpha", table=0, unit="in",
                 note="men's tops chart (body measurements)"),
    "DeWalt Workwear": dict(url="https://www.dewaltworkwear.co.uk/pages/size-guide", table=r"Tops and Jackets\s*$",
                            unit="in", collar="neck", note="tops and jackets chart; workwear sizing runs large"),
    "Burton": dict(url="https://www.burton.co.uk/pages/informational/size-guide", table=r"Sweatshirts and Hoodies\s*$",
                   unit="in", note="tops, shirts, T-shirts, polos, sweatshirts and hoodies chart (to fit chest)"),
    "Uskees": dict(url="https://uskees.com/products/6010-technique-trek-shirt-onyx", via="browser", click="Size chart",
                   pause=8000, table=0, half=True, kind=G,
                   note="no general chart; chest laid flat from the Technique trek shirt's chart, doubled"),
    "Jack Wolfskin": dict(url="https://www.jack-wolfskin.co.uk/products/1404031_t0386", json=("size", "chest"),
                          note="men's body chart kept on its product pages (Norbo shirt); the same on its other "
                               "men's shirts"),
    "New Era": dict(url="https://www.neweracap.co.uk/products/new-era-resort-natural-short-sleeve-shirt-14891298",
                    row=(r"MEN \(EU\) MEN \(EU\) MEN \(ASIA\).{0,80}?Region: Show all Size", r"\bChest\b"),
                    note="Men (EU) apparel chart in a product page's size guide"),
    "Rains": dict(url="https://www.rains.com/products/classic-t-shirt-rains-male", table=0, chest="chest width",
                  unit="cm", half=True, kind=G,
                  note="no general chart; chest width from the Classic T-shirt's chart, doubled"),
    "Community Clothing": dict(url="https://communityclothing.co.uk/products/tom-short-sleeve-military-two-pocket-shirt-"
                                   "stone", via="browser", click="Size Guide", pause=10000, table=0, kind=G,
                               note="men's T-shirt chart shown in a product page's size guide: the garment's own "
                                    "chest, length and sleeve (XS is 39.4in round)"),
    "Spoke": dict(url="https://spoke-london.com/pages/tops-size-chart?type=box-tee", via="browser", pause=8000,
                  table=r"laid flat\.\s*$", half=True, kind=G,
                  note="Box Tee product measurements: chest laid flat, doubled"),
})

MULTI = "sells many brands, each with its own chart; no shop-wide chart"
MISSING = {
    "Jean Store": MULTI, "80s Casual Classics": MULTI, "Slam City Skates": MULTI, "Flatspot": MULTI,
    "Route One": MULTI, "Urban Industry": MULTI, "Urban Excess": MULTI, "Philip Morris Direct": MULTI,
    "Hollands Country Clothing": MULTI, "Marrkt": MULTI, "Goodhood": MULTI, "Oi Polloi": MULTI,
    "Foot Locker": MULTI, "Spartoo": MULTI, "Best Workwear": MULTI, "Workwear Gurus": MULTI,
    "Trade Workwear": MULTI, "Rock Solid Safety": MULTI,
    "Millets": MULTI + " (and plain requests are refused)", "Blacks": MULTI + " (and plain requests are refused)",
    "Go Outdoors": MULTI + " (and plain requests are refused)",
    "Vinted": "second-hand marketplace; sizes are the sellers' own",
    "Military Kit": "army-surplus shop selling several makers; no shop-wide chart found",
    "Military Mart": "army-surplus shop selling several makers; no shop-wide chart found",
    "Trueface": "its product chart gives L as 15.7-16.5in 'chest', which is not a chest measurement",
    "Moss": "only a suit-jacket chart in numbered sizes; no S/M/L tops chart found",
    "Cyberjammies": "nightwear shop; its men's size guide has no chest table that could be read",
    "Corgi": "knitwear size guide has no chest table that could be read",
    "London Sock Company": "no tops size chart found",
}
NONE_FOUND = "no size chart found on its product pages or size-guide pages"
for _s in ("HUF", "Sunspel", "Peter Christian"):
    MISSING[_s] = NONE_FOUND
for _s in ("END.", "size?", "USC", "JD Sports", "Sports Direct", "BrandAlley", "Summits", "Wynsors", "Hirst Footwear",
           "Stuarts London", "Herring Shoes", "Lifting Equipment Store", "Workwear Express"):
    MISSING[_s] = MULTI
IMAGE = "its size chart is only a picture, so it cannot be read"
MISSING.update({
    "Debenhams": "marketplace selling many brands, each with its own chart; no shop-wide chart",
    "eBay": "marketplace; sizes are the sellers' own",
    "Rokit": "vintage shop; each piece is one-off and measured on its own",
    "Fila": IMAGE + " (men's size guide image on its product pages)",
    "Lambretta": IMAGE + " (an SVG drawn as shapes, in its product pages' size guide)",
    "Henri Lloyd": IMAGE + " (men's size chart image)",
    "Albam": IMAGE + " (one image per product in its Size Chart tab)",
    "Kestin": IMAGE + " (size-chart app images on its product pages)",
    "Scruffs": IMAGE + " (men's tops and jackets size guide image)",
    "Solovair": IMAGE + " (polo shirt size chart image)",
    "Brave Soul": "its product pages' size-guide pop-up is empty; no size-guide page found",
    "Matalan": "its products carry no size guide (empty in the page data) and no size-guide page was found",
    "Twisted Tailor": "its shirt and polo pages have no size chart, only a size picker; no size-guide page found",
    "BOSS": "its menswear chart gives only size conversions (L is UK 40R), no chest measurement",
    "Carhartt WIP": "garment measurements are kept per product in script data that the tool cannot read",
    "Cotton Traders": "its size-chart page shows no chart table, in plain requests or headless Chromium",
    "WoolOvers": "its pages refuse plain requests and headless Chromium (403)",
    "Admiral": "its size guide is a pop-up app that showed no chart in headless Chromium",
})


def pick_shops():
    """Shops that sell tops in the picks (data/items*.json), so new shops show up as not yet charted."""
    import glob
    items = {}
    for f in sorted(glob.glob(os.path.join(HERE, "..", "data", "items*.json"))):
        try:
            items.update(json.load(open(f)))
        except (OSError, ValueError):
            pass
    tops = ("knit", "polo", "shirt", "coat", "basics", "lounge", "sport")
    return {v.get("shop") for v in items.values() if isinstance(v, dict) and v.get("cat") in tops} - {None}


if __name__ == "__main__":
    main()
