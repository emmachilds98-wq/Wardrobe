"""Downloads whole catalogues from shops that publish a Shopify product feed.

    python3 tools/shopify_pull.py host1,host2,... [--out cat] [--pages 20]
    python3 tools/shopify_pull.py @hosts.txt

Writes <out>/<host>.json (a list of Shopify products: titles, types, tags, variants
with price, compare-at price and stock, and photo URLs).
"""
import argparse, concurrent.futures as cf, json, os, time, urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"


def pull(h, out, pages):
    got = []
    for page in range(1, pages + 1):
        try:
            r = urllib.request.Request(f"https://{h}/products.json?limit=250&page={page}",
                                       headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(r, timeout=40) as f:
                ps = json.load(f).get("products", [])
        except Exception:
            break
        if not ps:
            break
        got += ps
        time.sleep(0.4)
    with open(os.path.join(out, h + ".json"), "w") as f:
        json.dump(got, f)
    return h, len(got)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("hosts")
    ap.add_argument("--out", default="cat")
    ap.add_argument("--pages", type=int, default=20)
    a = ap.parse_args()
    hosts = open(a.hosts[1:]).read().split() if a.hosts.startswith("@") else a.hosts.split(",")
    seen, uniq = set(), []
    for h in hosts:
        k = h[4:] if h.startswith("www.") else h
        if k not in seen:
            seen.add(k)
            uniq.append(h)
    os.makedirs(a.out, exist_ok=True)
    with cf.ThreadPoolExecutor(12) as ex:
        for h, n in ex.map(lambda h: pull(h, a.out, a.pages), uniq):
            print(h, n, flush=True)


if __name__ == "__main__":
    main()
