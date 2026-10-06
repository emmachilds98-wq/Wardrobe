"""The weekly refresh: re-checks every pick against the shop, then makes room for new ones.

    python3 tools/weekly_refresh.py pull  [--cat cat]          # download every Shopify shop's catalogue
    python3 tools/weekly_refresh.py check [--cat cat] [--date YYYY-MM-DD] [--browser]
    python3 tools/weekly_refresh.py outfits [--date YYYY-MM-DD]  # mend outfits that lost a piece

`pull` reads /products.json from every shop behind a pick (and every Shopify shop in "Where to
look", so sweep_filter.py can find new picks), with retries, and records whether each catalogue
came down whole (cat/_status.json). A pick is only ever removed on firm evidence: its product page
is gone (404 or 410), the product has no stock left in any size, or his size is sold out. A shop
that refuses or times out leaves its picks as they were, and the report lists them.

`check` updates each pick in place, in whichever data/items*.json file holds it:
  - price, was-price and stock in his size from the live listing;
  - when the price moves, `prev` keeps last week's price (the page shows "Price drop") and `hist`
    gains the old price with its date;
  - `checked` becomes today; `added` is cleared on picks that are not new this week, so the page's
    "New this week" means what it says;
  - picks that are no longer sold, or no longer sold in his size, are removed. Extra wide (6E)
    safety boots stay as watch items when only his size is out, since so few exist.
Shops that are not on Shopify are read from the product page's schema.org data (ld_reader), and
with --browser, pages that refuse a plain request are opened in headless Chromium
(tools/browser_check.js). The run writes data/refresh-report.json.
"""
import argparse, collections, concurrent.futures as cf, datetime, glob, json, os, re, subprocess, sys, time
import urllib.error, urllib.parse, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sitemap_sweep  # noqa: E402
import sweep_filter as sf  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
ITEM_FILES = ["data/items.json"] + sorted(
    os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, "data", "items-*.json")))


GB = "localization=GB; cart_currency=GBP"


def get(url, accept="application/json", tries=4):
    """(status, body, final url). Asks for the UK market, since shops geolocate this server and
    otherwise answer in dollars or euros. Retries timeouts, 429/5xx and answers in another
    currency (Shopify names its currency in the cart_currency cookie); a 404 or 410 comes
    straight back."""
    for n in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept,
                                                       "Accept-Language": "en-GB", "Cookie": GB})
            with urllib.request.urlopen(req, timeout=40) as r:
                cur = re.search(r"cart_currency=([A-Z]{3})", " ".join(r.headers.get_all("Set-Cookie") or []))
                if cur and cur.group(1) != "GBP":
                    raise ValueError("answered in " + cur.group(1))
                return r.status, r.read().decode("utf8", "replace"), r.geturl()
        except urllib.error.HTTPError as e:
            if e.code in (404, 410):
                return e.code, "", url
            if e.code not in (429, 500, 502, 503, 504) or n == tries - 1:
                return e.code, "", url
        except Exception:
            if n == tries - 1:
                return 0, "", url
        time.sleep(2 * (n + 1))
    return 0, "", url


def load_items():
    files = {}
    for f in ITEM_FILES:
        with open(os.path.join(ROOT, f), encoding="utf-8") as fh:
            files[f] = json.load(fh)
    return files


def save_items(files):
    """Writes each items file back in its own layout (key order as loaded, same indent), so a
    week's diff shows only what changed."""
    for f, d in files.items():
        with open(os.path.join(ROOT, f), "w", encoding="utf-8") as fh:
            json.dump(d, fh, ensure_ascii=False, indent=1 if f == "data/items.json" else 0)


def host_of(url):
    return urllib.parse.urlparse(url).netloc.lower()


def handle_of(url):
    m = re.search(r"/products/([^/?#]+)", url)
    return urllib.parse.unquote(m.group(1)) if m else None


def variant_of(url):
    m = re.search(r"[?&]variant=(\d+)", url)
    return int(m.group(1)) if m else None


# ---------------------------------------------------------------- pull

def pull_one(host, out, pages):
    got, complete, page = [], False, 1
    while page <= pages:
        st, body, _ = get("https://%s/products.json?limit=250&page=%d" % (host, page))
        if st != 200:
            break
        try:
            ps = json.loads(body).get("products", [])
        except ValueError:
            break
        if not ps:
            complete = True
            break
        got += ps
        page += 1
        time.sleep(0.3)
    if got or complete:
        with open(os.path.join(out, host + ".json"), "w") as f:
            json.dump(got, f)
    return host, len(got), complete


def cmd_pull(a):
    files = load_items()
    hosts = collections.Counter()
    for d in files.values():
        for v in d.values():
            if "/products/" in v["url"]:
                hosts[host_of(v["url"])] += 1
    # Every shop in the directory that answers /products.json, for new picks.
    page = open(os.path.join(ROOT, "page.html"), encoding="utf-8").read()
    have = {sf.bare(h) for h in hosts}
    for h in re.findall(r'<a href="https://([^/"]+)[^"]*" target="_blank"', page):
        if sf.bare(h.lower()) not in have:
            have.add(sf.bare(h.lower()))
            hosts[h.lower()] += 0
    os.makedirs(a.cat, exist_ok=True)
    status = {}
    with cf.ThreadPoolExecutor(a.workers) as ex:
        for h, n, done in ex.map(lambda h: pull_one(h, a.cat, a.pages), sorted(hosts)):
            if n or done:
                status[h] = {"n": n, "complete": done, "picks": hosts[h]}
                print(h, n, "complete" if done else "PARTIAL", flush=True)
    with open(os.path.join(a.cat, "_status.json"), "w") as f:
        json.dump(status, f, indent=1)


# ---------------------------------------------------------------- check

def from_js(p):
    """A /products/<handle>.js product -> the /products.json shape (prices in pounds)."""
    out = dict(p)
    out["options"] = [{"name": o if isinstance(o, str) else o.get("name", "")} for o in p.get("options", [])]
    out["variants"] = []
    for v in p.get("variants", []):
        v = dict(v)
        for k in ("price", "compare_at_price"):
            if isinstance(v.get(k), int):
                v[k] = "%.2f" % (v[k] / 100)
        out["variants"].append(v)
    out["body_html"] = p.get("description", "")
    return out


def size_sibling(p, base, w):
    """True when variant w differs from the pick's own variant only in size (same colour, fit...)."""
    names = [o.get("name", "").lower() for o in p.get("options", [])]
    for i, n in enumerate(names):
        if re.search(r"size|waist|leg|length|fit|width", n):
            continue
        k = "option%d" % (i + 1)
        if base.get(k) != w.get(k):
            return False
    return True


def judge_shopify(it, p, us_shop):
    """What the live product says about this pick: (verdict, fields to update)."""
    title = p.get("title") or ""
    vs = p.get("variants") or []
    if not vs or not any(v.get("available") for v in vs):
        return "sold out", {}
    vid = variant_of(it["url"])
    base = next((v for v in vs if v.get("id") == vid), None)
    cands = [v for v in vs if (base is None or size_sibling(p, base, v))]
    mine = [(v, sf.size_ok(it["cat"], p, v, title, us_shop)) for v in cands]
    mine = [(v, s) for v, s in mine if s]
    if base is not None and base not in [v for v, _ in mine]:
        # The pick's own variant may be his size under a label the filter does not read.
        mine.insert(0, (base, it.get("sizes", "").replace(" in stock", "") or "his size"))
    live = [(v, s) for v, s in mine if v.get("available")]
    if mine and not live:
        return "his size sold out", {}
    use = (live[0][0] if live else base) or next(v for v in vs if v.get("available"))
    try:
        price = round(float(use.get("price") or 0), 2)
        was = round(float(use.get("compare_at_price") or 0), 2)
    except ValueError:
        return "unreadable", {}
    if price <= 0:
        return "unreadable", {}
    upd = {"price": price, "was": was if was > price * 1.04 else 0}
    if live:
        upd["insize"] = True
        sz = live[0][1]
        if sz and not it.get("sizes", "").startswith(sz):
            upd["sizes"] = sz + " in stock" if sz != "One size" else "One size"
    if live and base is not None and live[0][0] is not base and live[0][0].get("id"):
        upd["url"] = re.sub(r"variant=\d+", "variant=%s" % live[0][0]["id"], it["url"])
    return "ok", upd


def judge_ld(it, r):
    """Same, for a page read through its schema.org data."""
    if r.get("err"):
        e = r["err"]
        if re.search(r"HTTP Error (404|410)", e):
            return "gone", {}
        return "unreachable", {"err": e}
    if not r.get("price"):
        return "unreadable", {}
    if r.get("currency") and r["currency"] != "GBP":
        return "unreliable price", {"err": "priced in " + r["currency"]}
    final = r.get("url") or it["url"]
    if host_of(final) == host_of(it["url"]) and urllib.parse.urlparse(final).path.rstrip("/") in ("", "/men", "/mens"):
        return "gone", {}
    upd = {"price": round(float(r["price"]), 2), "was": round(float(r["was"]), 2) if r.get("was") else 0}
    if r.get("name") and not same_thing(it, r["name"]):
        upd["rename"] = r["name"]
    sizes = r.get("sizes") or {}
    if sizes:
        if not any(sizes.values()):
            return "sold out", {}
        p = sitemap_sweep.as_shopify(dict(r, name=r.get("name") or it["name"]))
        hits = [(v, sf.size_ok(it["cat"], p, v, it["name"], False)) for v in p["variants"]]
        hits = [(v, s) for v, s in hits if s]
        if hits:
            if not any(v["available"] for v, _ in hits):
                return "his size sold out", {}
            upd["insize"] = True
    return "ok", upd


def shifted(items, verdicts, keys):
    """True when most of a shop's picks changed price by one shared factor: a currency or VAT
    switch, not a sale. Real price changes come in different sizes."""
    rs = [verdicts[k][1]["price"] / items[k]["price"] for k in keys
          if verdicts.get(k, ("",))[0] == "ok" and items[k].get("price") and "price" in verdicts[k][1]]
    moved = [r for r in rs if abs(r - 1) > 0.02]
    if len(rs) < 5 or len(moved) < 0.6 * len(rs):
        return False
    moved.sort()
    mid = moved[len(moved) // 2]
    near = [r for r in moved if abs(r / mid - 1) < 0.04]
    return len(near) >= 0.6 * len(rs)


def watch_item(it):
    """6E safety footwear is so rare that a sold-out pair stays listed (as "his size sold out")
    so the page flags it when it comes back."""
    return "job" in it.get("style", []) and it.get("cat") == "shoe" and re.search(r"\b(6E|EEEEEE)\b", it["name"] + " " + it.get("sizeNote", ""))


STOP = set(sf.COLOURS) | {"mens", "men", "the", "and", "with", "fit", "regular", "slim", "relaxed", "tailored", "new"}


def words(s):
    return {w for w in re.findall(r"[a-z]{3,}", s.lower()) if w not in STOP}


def same_thing(it, page_name):
    """False when the page's product shares almost nothing with the pick's name: the pick was
    named after a different product (an earlier sweep read a recommended item's data)."""
    a, b = words(it["name"]) - words(it["shop"]), words(page_name) - words(it["shop"])
    if not a or not b:
        return True
    return len(a & b) / min(len(a), len(b)) >= 0.34


def apply(it, upd, date, report, key):
    old = it.get("price")
    if "price" in upd and old and abs(upd["price"] - old) >= 0.01:
        h = it.get("hist") or []
        if not h or h[-1][1] != old:
            h.append([it.get("checked") or date, old])
        it["hist"] = h[-6:]
        it["prev"] = old
        report["price_down" if upd["price"] < old else "price_up"].append(
            [key, it["shop"], it["name"], old, upd["price"]])
    elif "prev" in it:
        del it["prev"]  # unchanged this week: no "Price drop" tag
    for k in ("price", "url", "sizes"):
        if k in upd and it.get(k) != upd[k]:
            it[k] = upd[k]
    if upd.get("rename"):
        nm = re.sub(r"\s+", " ", upd["rename"]).strip()
        if not nm.lower().startswith(it["shop"].lower()):
            nm = it["shop"] + " " + nm
        report["renamed"].append([key, it["shop"], it["name"], nm])
        it["name"] = nm
        it["cat"] = sf.category(nm, "", []) or it["cat"]
    if "was" in upd:
        if upd["was"]:
            if it.get("was") != upd["was"]:
                it["was"] = upd["was"]
        else:
            it.pop("was", None)
    if upd.get("insize") is True:
        if it.get("insize") is False:
            report["back_in_size"].append([key, it["shop"], it["name"]])
        it["insize"] = True
    if "price" in upd:
        it["note"] = refresh_note(it)
    it["checked"] = date


def refresh_note(it):
    """Rewrites the price sentence at the start of a note written by sweep_filter, keeps the rest."""
    note = it.get("note", "")
    price, was = it["price"], it.get("was") or 0
    lead = ("Down from £%s to £%s (%d%% off)." % (sf.fmt(was), sf.fmt(price), round(100 * (was - price) / was))
            if was > price else "£%s, full price." % sf.fmt(price))
    m = re.match(r"^(Down from £[\d.]+ to £[\d.]+ \(\d+% off\)\.|£[\d.]+, full price\.)\s*", note)
    return (lead + " " + note[m.end():]).strip() if m else note


def cmd_check(a):
    date = a.date
    files = load_items()
    where = {k: f for f, d in files.items() for k in d}
    items = {k: files[f][k] for k, f in where.items()}
    status = {}
    sp = os.path.join(a.cat, "_status.json")
    if os.path.exists(sp):
        status = json.load(open(sp))
    report = collections.defaultdict(list)
    verdicts = {}
    prev_date = max((it.get("checked", "") for it in items.values() if it.get("checked", "") < date), default="")

    # 1. Shopify shops: match each pick to its product in the downloaded catalogue.
    byhost = collections.defaultdict(list)
    for k, it in items.items():
        if it.get("kind") == "preowned":
            continue
        byhost[host_of(it["url"])].append(k)
    lookups = []
    for h, keys in sorted(byhost.items()):
        path = os.path.join(a.cat, h + ".json")
        shop_keys = [k for k in keys if handle_of(items[k]["url"])]
        if not shop_keys or not os.path.exists(path):
            continue
        prods = json.load(open(path))
        idx = {p.get("handle"): p for p in prods}
        us_shop = sum(1 for p in prods[:300] for v in p.get("variants", [])[:30]
                      if re.search(r"\bUS\b", " ".join(x for x in (v.get("option1"), v.get("option2")) if x) or "")) > 3
        for k in shop_keys:
            p = idx.get(handle_of(items[k]["url"]))
            if p:
                verdicts[k] = judge_shopify(items[k], p, us_shop)
            else:
                lookups.append((k, us_shop))

    # Not in the catalogue: ask for the product itself, so a partial download never removes a pick.
    def one(arg):
        k, us_shop = arg
        url = items[k]["url"]
        st, body, final = get("https://%s/products/%s.js" % (host_of(url), urllib.parse.quote(handle_of(url))))
        if st in (404, 410):
            return k, ("gone", {})
        if st != 200:
            return k, ("unreachable", {"err": "HTTP %s" % st})
        try:
            return k, judge_shopify(items[k], from_js(json.loads(body)), us_shop)
        except ValueError:
            return k, ("unreadable", {})
    with cf.ThreadPoolExecutor(a.workers) as ex:
        for k, v in ex.map(one, lookups):
            verdicts[k] = v

    # A shop whose prices all moved by the same factor answered in another currency (or
    # without VAT): read those picks one by one, and if the shift is still there, leave them.
    for h, keys in sorted(byhost.items()):
        if shifted(items, verdicts, keys):
            again = [(k, False) for k in keys if k in verdicts]
            with cf.ThreadPoolExecutor(a.workers) as ex:
                for k, v in ex.map(one, again):
                    verdicts[k] = v
            if shifted(items, verdicts, keys):
                for k in keys:
                    if verdicts.get(k, ("",))[0] == "ok":
                        verdicts[k] = ("unreliable price", {"err": "prices in another currency"})
                report["currency_shift"].append(h)

    # 2. Everything else: the product page's schema.org data.
    rest = [k for k in items if k not in verdicts and items[k].get("kind") != "preowned"]
    with cf.ThreadPoolExecutor(a.workers) as ex:
        for k, r in zip(rest, ex.map(lambda k: sitemap_sweep.parse(items[k]["url"]), rest)):
            verdicts[k] = judge_ld(items[k], r)

    for h, keys in sorted(byhost.items()):
        if not any(handle_of(items[k]["url"]) for k in keys) and shifted(items, verdicts, keys):
            for k in keys:
                if verdicts.get(k, ("",))[0] == "ok":
                    verdicts[k] = ("unreliable price", {"err": "every price moved by the same factor"})
            report["currency_shift"].append(h)

    # 3. Pages that refused a plain request: once more in headless Chromium.
    blocked = [k for k, (v, _) in verdicts.items() if v in ("unreachable", "unreadable")]
    if a.browser and blocked:
        tmp = os.path.join(a.cat, "_browser")
        os.makedirs(tmp, exist_ok=True)
        with open(os.path.join(tmp, "in.json"), "w") as f:
            json.dump({k: items[k]["url"] for k in blocked}, f)
        subprocess.run(["node", os.path.join(ROOT, "tools", "browser_check.js"),
                        os.path.join(tmp, "in.json"), os.path.join(tmp, "out.json")], check=False)
        try:
            got = json.load(open(os.path.join(tmp, "out.json")))
        except Exception:
            got = {}
        for k, r in got.items():
            if r.get("status") in (404, 410):
                verdicts[k] = ("gone", {})
            elif r.get("ld") or r.get("price"):
                got_ld = sitemap_sweep_ld(r.get("ld") or [], r.get("url") or items[k]["url"])
                if not got_ld.get("price") and r.get("price"):
                    try:
                        got_ld = {"url": r.get("url"), "price": float(r["price"]), "sizes": {}}
                    except ValueError:
                        pass
                v = judge_ld(items[k], got_ld)
                if v[0] not in ("unreachable", "unreadable"):
                    verdicts[k] = v
                    report["via_browser"].append(k)

    # 4. Apply.
    removed = {}
    for k, (v, upd) in sorted(verdicts.items()):
        it = items[k]
        if v == "ok":
            apply(it, upd, date, report, k)
        elif v in ("his size sold out", "sold out") and watch_item(it):
            it["insize"] = False
            it["checked"] = date
            report["kept_watch"].append([k, it["shop"], it["name"]])
        elif v in ("gone", "sold out", "his size sold out"):
            removed[k] = [v, it["shop"], it["name"], where[k]]
        else:
            report["not_checked"].append([k, it["shop"], v, upd.get("err", "")])
    for k, (why, shop, name, f) in removed.items():
        del files[f][k]
    report["removed"] = [[k] + v[:3] for k, v in sorted(removed.items(), key=lambda x: (x[1][1], x[1][2]))]
    report["removed_items"] = {k: items[k] for k in removed}  # so `outfits` can find a like-for-like swap

    enforce_workwear(files, report)

    # "New this week" is for this week's picks only.
    for f, d in files.items():
        for it in d.values():
            if it.get("added") and (it["added"] != date or f == "data/items.json" or not re.search(r"items-\d{4}-\d\d-\d\d", f)):
                it.pop("added")
    save_items(files)
    summary = {
        "date": date, "picks_before": len(items), "removed": len(removed),
        "checked": sum(1 for v, _ in verdicts.values() if v == "ok"),
        "price_down": len(report["price_down"]), "price_up": len(report["price_up"]),
        "not_checked": len(report["not_checked"]),
        "not_checked_by_shop": collections.Counter(r[1] for r in report["not_checked"]).most_common(),
        "removed_why": collections.Counter(v[0] for v in removed.values()),
    }
    with open(os.path.join(ROOT, "data", "status.json"), "w") as f:
        json.dump({"checked": date, "prev": prev_date}, f)
    out = {"summary": summary, **{k: v for k, v in report.items()}}
    with open(os.path.join(ROOT, "data", "refresh-report.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(json.dumps(summary, indent=1, ensure_ascii=False))


def sitemap_sweep_ld(ld_list, url):
    """JSON-LD blocks collected by the browser -> the dict ld_reader.parse returns."""
    import html as _h
    page = "".join('<script type="application/ld+json">%s</script>' % _h.escape(x, quote=False) for x in ld_list)
    real_get = sitemap_sweep.ld_reader.get
    try:
        sitemap_sweep.ld_reader.get = lambda u: (page, url)
        return sitemap_sweep.ld_reader.parse(url)
    finally:
        sitemap_sweep.ld_reader.get = real_get


# ---------------------------------------------------------------- Workwear rules

WORK_ACC = re.compile(r"\b(gloves?|beanie|watch cap|socks?|base ?layer|thermal|long johns|neck ?warmer|snood|"
                      r"knee ?pads?|braces|pouch|holster|tool ?belt|ear defenders?|balaclava|headover|face wrap)\b", re.I)
NOT_GEAR = re.compile(r"\b(tie[- ]down|stake|laptop|briefcase|survival bag|bivvy|mag rig|mag sleeve|grenade|first aid|"
                      r"tool roll|kit bag|sleep(ing)? bag|tent|ratchet|strap with)\b", re.I)
JOB_TEE = re.compile(r"\b(t-?shirts?|tees?|t|vests?|tank|singlet)\b", re.I)
WIDE_FIT = re.compile(r"\b(4E|5E|6E|EE|EEE|EEEE+|extra wide|6V)\b", re.I)


def job_breaks(v, swept=False):
    """Why a Workwear-tagged pick breaks Emma's rules, or "" when it keeps them: no T-shirts (work
    gives him those); trousers and shorts black or charcoal, 97% cotton or more, no stretch, slim or
    Cordura; safety footwear extra wide (EE or wider) only."""
    n = v["name"]
    if swept and v["cat"] != "shoe" and sf.bare(host_of(v["url"])) not in sf.WORK_SHOPS and not sf.WORK_BRAND.search(n) \
            and not (v["cat"] in ("acc", "basics") and WORK_ACC.search(n)):
        return "not work clothing"
    if v["cat"] == "polo" and JOB_TEE.search(n):
        return "T-shirt"
    if v["cat"] == "trouser":
        cot = sf.cotton_pct(v.get("fabric", "") + " " + v.get("note", ""))
        if sf.SLIM.search(n) or sf.SKINNY.search(n):
            return "slim fit"
        if not sf.DARK.search(n):
            return "not black or charcoal"
        if re.search(r"stretch|active|flex|tri-?dri|x1500|cordura", n, re.I):
            return "stretch or Cordura"
        if cot is None or cot < 97:
            return "not 100% cotton" if cot else "fabric not confirmed as cotton"
    if v["cat"] == "shoe" and not WIDE_FIT.search(n + " " + v.get("sizeNote", "") + " " + v.get("note", "")):
        return "not extra wide"
    return ""


def enforce_workwear(files, report):
    """Takes the Workwear tag off picks that break the rules; they stay in their other styles.
    Also removes kit that is not clothing at all (tie-down straps, bivvy bags and the like)."""
    for f, d in files.items():
        for k in [k for k, v in d.items() if v["cat"] in ("acc", "basics") and NOT_GEAR.search(v["name"])]:
            report["removed_not_clothing"].append([k, d[k]["shop"], d[k]["name"]])
            del d[k]
        for k, v in d.items():
            if "job" in v.get("style", []):
                why = job_breaks(v, swept=f != "data/items.json")
                if why:
                    v["style"] = [x for x in v["style"] if x != "job"] or (["outdoor"] if v["cat"] == "shoe" else ["casual"])
                    report["workwear_untagged"].append([k, v["shop"], v["name"], why])


def cmd_rules(a):
    files = load_items()
    report = collections.defaultdict(list)
    enforce_workwear(files, report)
    save_items(files)
    rp = os.path.join(ROOT, "data", "refresh-report.json")
    r = json.load(open(rp)) if os.path.exists(rp) else {}
    for key in ("workwear_untagged", "removed_not_clothing"):
        r[key] = r.get(key, []) + report[key]
    with open(rp, "w", encoding="utf-8") as f:
        json.dump(r, f, ensure_ascii=False, indent=1)
    print(len(report["workwear_untagged"]), "picks lost the Workwear tag")


# ---------------------------------------------------------------- outfits

def cmd_outfits(a):
    """Outfits that lost a piece get the closest live pick of the same shape and colour, or are
    dropped when nothing fits."""
    import make_outfits as mo
    files = load_items()
    items = {k: v for d in files.values() for k, v in d.items()}
    report = {"swapped": [], "dropped": []}
    rp0 = os.path.join(ROOT, "data", "refresh-report.json")
    gone = (json.load(open(rp0)).get("removed_items") or {}) if os.path.exists(rp0) else {}
    photos = set()
    for pp in glob.glob(os.path.join(ROOT, "photos", "*-[0-9][0-9].json")):
        photos.update(json.load(open(pp)))
    use = collections.Counter()
    ofiles = {f: json.load(open(os.path.join(ROOT, f), encoding="utf-8"))
              for f in ["data/outfits.json"] + sorted(os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, "data", "outfits-*.json")))}
    for d in ofiles.values():
        for o in d.values():
            for p in o["pieces"]:
                use[p["item"]] += 1
    for f, d in ofiles.items():
        for ok in list(d):
            o = d[ok]
            styles = set(o.get("style", []))
            for p in o["pieces"]:
                it0 = items.get(p["item"])
                job_bound = "job" in styles and it0 is not None and "job" not in it0.get("style", []) and \
                    p.get("shape") in ("trousers", "shorts", "boots", "shoes", "tee")
                if it0 is not None and not job_bound:
                    continue
                inside = {q["item"] for q in o["pieces"]}
                was = gone.get(p["item"]) or items.get(p["item"], {})
                one_shop = re.search(r"head to toe", o["name"], re.I) and was.get("shop")
                lounge = styles & {"lounge", "rave"}
                best = None
                for k, v in items.items():
                    if k in inside or v.get("kind") == "preowned" or v.get("insize") is False:
                        continue
                    if styles and not styles & set(v.get("style", [])):
                        continue
                    if "job" in styles and "job" not in v.get("style", []) and p.get("shape") in ("trousers", "shorts", "boots", "shoes", "tee"):
                        continue
                    if one_shop and v["shop"] != was["shop"]:
                        continue
                    if was and v["cat"] != was.get("cat") and not (p.get("shape") == "tee" and v["cat"] == "polo"):
                        continue
                    try:
                        sh = mo.shape(v)
                    except Exception:
                        continue
                    if sh != p.get("shape") and not (p.get("shape") == "tee" and "job" in styles and sh == "polo"):
                        continue
                    col = mo.colour(v["name"])
                    score = (0 if col == p.get("col") else 2 if col in mo.NEUTRAL and p.get("col") in mo.NEUTRAL
                             else 3 if col in mo.NEUTRAL else 5) + \
                        (0 if not was or v["cat"] == was.get("cat") else 3) + \
                        (0 if was and v["shop"] == was.get("shop") else 1) + \
                        (0 if lounge or not re.search(r"jogger|track ?(pant|bottom)|sweatpant", v["name"], re.I) else 3) + \
                        (0 if k in photos else 1) + \
                        (0 if v.get("insize") is True else 1) + use[k] * 0.5 + v.get("price", 99) / 100
                    if best is None or score < best[0]:
                        best = (score, k, col)
                if best and best[0] < 5:
                    report["swapped"].append([ok, o["name"], p["item"], best[1], items[best[1]]["name"]])
                    p["item"] = best[1]
                    p["shape"] = mo.shape(items[best[1]]) or p["shape"]
                    p["what"] = ((best[2].capitalize() + " ") if best[2] else "") + mo.WHAT.get(p["shape"], "piece")
                    if best[2]:
                        p["col"] = best[2]
                    use[best[1]] += 1
                else:
                    report["dropped"].append([ok, o["name"], p["item"]])
                    del d[ok]
                    break
    # Generated outfits are named after their colours ("Navy jacket and grey trousers"); rename
    # the ones whose pieces changed so the name still describes them.
    changed = {x[0] for x in report["swapped"]}
    for f, d in ofiles.items():
        for ok, o in d.items():
            if ok in changed and re.match(r"^\w+ [\w-]+( [\w-]+)? and \w+ [\w-]+( [\w-]+)?$", o["name"]):
                ps = o["pieces"]
                main = [q for q in ps if q["shape"] in mo.OUT] or [q for q in ps if q["shape"] in mo.MID] or ps[:1]
                low = next((q for q in ps if q["shape"] in mo.LOW), None)
                if low and main[0] is not low:
                    lab = lambda q: ((q["col"] + " ") if q.get("col") else "") + mo.WHAT.get(q["shape"], q["shape"])
                    nm = lab(main[0]) + " and " + lab(low)
                    o["name"] = nm[0].upper() + nm[1:]
    for f, d in ofiles.items():
        with open(os.path.join(ROOT, f), "w", encoding="utf-8") as fh:
            json.dump(d, fh, ensure_ascii=False, indent=1)
    rp = os.path.join(ROOT, "data", "refresh-report.json")
    r = json.load(open(rp)) if os.path.exists(rp) else {}
    r["outfits"] = report
    with open(rp, "w", encoding="utf-8") as fh:
        json.dump(r, fh, ensure_ascii=False, indent=1)
    print(len(report["swapped"]), "pieces swapped,", len(report["dropped"]), "outfits dropped")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["pull", "check", "rules", "outfits"])
    ap.add_argument("--cat", default=os.path.join(ROOT, "cat"))
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--pages", type=int, default=60)
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--browser", action="store_true")
    a = ap.parse_args()
    {"pull": cmd_pull, "check": cmd_check, "rules": cmd_rules, "outfits": cmd_outfits}[a.cmd](a)


if __name__ == "__main__":
    main()
