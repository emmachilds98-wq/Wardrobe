"""Pulls products from shops that do not publish a Shopify feed, through their sitemaps.

For each host it reads robots.txt and the sitemaps it names, keeps product URLs that look like
men's clothing (sale URLs first), reads each page's schema.org Product data with ld_reader.parse,
and writes <out>/<host>.json in the same shape as shopify_pull.py, so sweep_filter.py can treat
both alike. Each product carries its real "url".

    python3 tools/sitemap_sweep.py host1,host2,... [--out cat] [--max 300]
"""
import argparse, concurrent.futures as cf, gzip, json, os, re, sys, urllib.parse, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ld_reader  # noqa: E402

UA = ld_reader.UA
MEN = re.compile(r"(^|[/_\-.])(men|mens|man|male|menswear|gents)([/_\-.]|$)", re.I)
WOMEN = re.compile(r"(women|womens|ladies|girls|boys|kids|baby|junior|child)", re.I)
CLOTHES = re.compile(r"(shirt|tee|t-shirt|polo|jumper|sweat|hood|knit|cardigan|jacket|coat|parka|gilet|"
                     r"trouser|jean|chino|cord|short|jogger|boot|shoe|trainer|sneaker|loafer|sandal|"
                     r"slipper|sock|boxer|belt|cap|hat|beanie|scarf|glove|blazer|suit|waistcoat|fleece|"
                     r"overshirt|pyjama|robe|swim)", re.I)
NOT_PRODUCT = re.compile(r"/(blog|stores?|help|pages?|about|journal|stories|c|category|categories|collections?|search)/", re.I)


def fetch(url, limit=30_000_000):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-GB", "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=40, context=ld_reader.ctx) as r:
        data = r.read(limit)
    if url.endswith(".gz") or data[:2] == b"\x1f\x8b":
        try:
            data = gzip.decompress(data)
        except OSError:
            pass
    return data.decode("utf8", "replace")


def sitemap_urls(host, cap=60):
    """All page URLs in the host's sitemaps (following sitemap indexes, at most `cap` files)."""
    roots = []
    try:
        roots = re.findall(r"(?im)^sitemap:\s*(\S+)", fetch("https://%s/robots.txt" % host))
    except Exception:
        pass
    roots = roots or ["https://%s/sitemap.xml" % host, "https://%s/sitemap_index.xml" % host]
    seen, queue, pages = set(), list(roots), []
    while queue and len(seen) < cap:
        sm = queue.pop(0)
        if sm in seen:
            continue
        seen.add(sm)
        try:
            body = fetch(sm)
        except Exception:
            continue
        locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", body)
        if "<sitemapindex" in body:
            # Product sitemaps first; skip images, blogs and stores.
            locs = [l for l in locs if not re.search(r"image|blog|store|content|page|categor|brand|video", l, re.I)]
            locs.sort(key=lambda l: 0 if re.search(r"product|pdp|item", l, re.I) else 1)
            queue.extend(locs)
        else:
            pages.extend(l.replace("&amp;", "&") for l in locs)
    return pages


def pick(urls, n):
    """Scores each URL: looks like a product page, men's, a kind of clothing, on sale. Keeps the best n."""
    scored = []
    for u in urls:
        path = urllib.parse.urlparse(u).path
        if NOT_PRODUCT.search(path) or WOMEN.search(path) or path.count("/") < 1:
            continue
        prod = bool(re.search(r"/(p|pd|product|products|prd|item|style)/|\d{5,}|\.html?$|_[A-Z0-9]{6,}", path))
        if not prod and "/l/" in path:
            continue
        sc = (3 if prod else 0) + (2 if MEN.search(path) else 0) + (2 if CLOTHES.search(path) else 0) + \
             (1 if re.search(r"sale|outlet|clearance|offer", u, re.I) else 0)
        if sc >= 3:
            scored.append((-sc, len(u), u))
    scored.sort()
    return [u for _, _, u in scored[:n]]


PRICE_RX = [r'property="product:price:amount"\s+content="([\d.]+)"', r'itemprop="price"\s+content="([\d.]+)"',
            r'"price"\s*:\s*"?(\d+(?:\.\d+)?)"?', r'"currentPrice"\s*:\s*\{?[^}]*?"value"\s*:\s*(\d+(?:\.\d+)?)']
WAS_RX = [r'"(?:wasPrice|originalPrice|listPrice|compareAtPrice|rrp)"\s*:\s*\{?[^}]*?(\d+(?:\.\d+)?)', r'class="[^"]*(?:was|original|strike)[^"]*"[^>]*>\s*£\s*(\d+(?:\.\d+)?)']


def parse(u):
    """ld_reader.parse, with the price (and was-price) read from page meta and scripts when the
    schema.org data leaves it out."""
    try:
        r = ld_reader.parse(u)
    except Exception as e:  # one odd page must not stop the whole shop
        return {"url": u, "err": str(e)[:80]}
    if r.get("err") or (r.get("price") and r.get("was") is not None):
        return r
    try:
        page, _ = ld_reader.get(u)
    except Exception:
        return r
    if not r.get("price"):
        for rx in PRICE_RX:
            m = re.search(rx, page)
            if m and 2 < float(m.group(1)) < 2000:
                r["price"] = float(m.group(1))
                break
    for rx in WAS_RX:
        m = re.search(rx, page, re.I)
        if m and r.get("price") and float(m.group(1)) > r["price"] * 1.04 and float(m.group(1)) < r["price"] * 6:
            r["was"] = float(m.group(1))
            break
    return r


def as_shopify(r):
    """ld_reader output -> a Shopify-shaped product for sweep_filter.py."""
    if r.get("err") or not r.get("name") or not r.get("price"):
        return None
    sizes = r.get("sizes") or {}
    variants = [{"id": None, "option1": str(k), "available": bool(v), "price": str(r["price"]),
                 "compare_at_price": str(r["was"]) if r.get("was") else None} for k, v in sizes.items()]
    if not variants:
        variants = [{"id": None, "option1": "One size", "available": True, "price": str(r["price"]),
                     "compare_at_price": str(r["was"]) if r.get("was") else None}]
        nosizes = True
    else:
        nosizes = False
    handle = re.sub(r"[^a-z0-9]+", "-", urllib.parse.urlparse(r["url"]).path.lower()).strip("-")[-80:]
    img = r.get("img") or r.get("og")
    return {"title": r["name"], "handle": handle, "url": r["url"], "product_type": "", "tags": [],
            "vendor": "", "body_html": "", "options": [{"name": "Size"}], "variants": variants,
            "images": [{"src": img, "variant_ids": []}] if img else [], "colour": r.get("color"), "nosizes": nosizes}


def sweep(host, out, n):
    try:
        urls = pick(sitemap_urls(host), n)
    except Exception:
        urls = []
    if not urls:
        with open(os.path.join(out, host + ".json"), "w") as f:
            json.dump([], f)
        return host, 0, 0
    prods = []
    with cf.ThreadPoolExecutor(8) as ex:
        for r in ex.map(parse, urls):
            p = as_shopify(r)
            if p:
                prods.append(p)
    with open(os.path.join(out, host + ".json"), "w") as f:
        json.dump(prods, f)
    return host, len(urls), len(prods)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("hosts")
    ap.add_argument("--out", default="cat")
    ap.add_argument("--max", type=int, default=300)
    a = ap.parse_args()
    hosts = open(a.hosts[1:]).read().split() if a.hosts.startswith("@") else a.hosts.split(",")
    os.makedirs(a.out, exist_ok=True)
    with cf.ThreadPoolExecutor(6) as ex:
        for h, nu, npr in ex.map(lambda h: sweep(h, a.out, a.max), hosts):
            print(h, nu, "pages", npr, "products", flush=True)


if __name__ == "__main__":
    main()
