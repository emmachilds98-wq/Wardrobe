# The Wardrobe

A personal outfit planner: clothes picked for one person's sizes across eight style tabs
(including Workwear), outfits drawn on a figure, live prices with links, an outfit builder, a
shortlist, and a "his wardrobe" section for things he already owns.

The main version runs as a claude.ai artifact. This repository is its offline home and also
serves a read-only copy through GitHub Pages.

| Path | What it is |
|---|---|
| `page.html` | The page source as published to the artifact. |
| `index.html` | A copy of `page.html` for GitHub Pages. With no artifact database it loads the files in `data/`, and keeps the shortlist, likes and "I have this" marks in the viewer's own browser. |
| `data/items.json` | Every pick (name, shop, price, link, styles, occasion, weather, sizes), without photos. |
| `data/outfits.json` | Every outfit and the picks it uses. |
| `data/meta.json` | Status, sizes, style tags and shop delivery notes. No names. |
| `data/photos/<type>.json` | Listing photos as small WebP data, one file per type, loaded only when a card scrolls into view. |
| `tools/export_static.py` | Rebuilds `data/` and `index.html` from a dump of the artifact's database, leaving personal details out. |
| `tools/fetch_photos.py` | Downloads and shrinks listing photos. `--browser` retries refused shops in headless Chromium. |
| `tools/shopify_pull.py` | Downloads a whole catalogue (prices, stock by size, photos) from shops that publish a product feed. |
| `tools/ld_reader.py` | Reads price, photo and stock per size from product pages with schema.org data. |
| `tools/asos_photos.py` | Fetches ASOS photos through wsrv.nl, since ASOS blocks cloud servers. |
| `tools/browser_fetch.js` | The headless-browser fallback used by `--browser`. |
| `UPGRADE_PLAN.md` | The review, what has been done, and what is next. |

## Updating the GitHub Pages copy

1. Dump the artifact's database (items, outfits, meta and photos) to a folder with the
   ArtifactData tool's `out_dir` option.
2. Run `python3 tools/export_static.py --dump <folder> --out .`
3. Commit `data/` and `index.html`, and merge.

GitHub Pages serves the `main` branch from the repository root (Settings, Pages).
