# Dave's Wardrobe

A personal outfit planner for Dave: clothes picked for his sizes across eight style tabs (including Workwear for his job), outfits
drawn on a figure of him, live prices with links, an outfit builder, and a shared shortlist.

The live version runs as a claude.ai artifact, <https://claude.ai/artifact/8uqcGr2eNmzbQv8UVBshY2>,
and as a public copy on GitHub Pages, <https://emmachilds98-wq.github.io/Wardrobe/> (built into
`docs/`). This repository is its home: the page source, its data, the listing photos, and the tools
that refresh them every week (see `REFRESH.md`).

| Path | What it is |
|---|---|
| `page.html` | The page source as published. Opened directly in a browser it shows the layout; picks and outfits load only inside the artifact, where its database lives. |
| `data/items.json` | Every pick (name, shop, price, link, styles, occasion, weather, sizes). |
| `data/outfits.json` | Every outfit and the picks it uses. A piece marked `"own"` is something he already has (his work T-shirt), with nothing to buy. |
| `photos/` | Listing photos, shrunk to small WebP files and packed into JSON files the page loads. |
| `tools/fetch_photos.py` | Downloads and packs the listing photos. `--browser` retries refused shops in headless Chromium. |
| `tools/shopify_pull.py` | Downloads a whole catalogue (prices, stock by size, photos) from shops that publish a product feed. |
| `tools/sweep_filter.py` | Turns the downloaded catalogues into picks: his sizes, clean names, right categories, sale first, workwear rules. Writes `data/items-new.json`. |
| `data/items-new.json` | Picks from the October 2026 sweep of Shopify shops (merged with `items.json` by `build_site.py`). |
| `tools/ld_reader.py` | Reads price, photo and stock per size from product pages with schema.org data. |
| `data/styletags.json` | Older picks that also belong to the Mod and skate, Holiday or Workwear styles. |
| `tools/asos_photos.py` | Fetches ASOS photos through wsrv.nl, since ASOS blocks cloud servers. |
| `tools/build_site.py` | Builds `site/` (the page plus its data and photo files, in load groups of under 900) for publishing. |
| `tools/browser_fetch.js` | The headless-browser fallback used by `--browser`. |
| `tools/weekly_refresh.py` | The weekly refresh: downloads catalogues, re-checks every pick (price, his size, still sold), applies the Workwear rules and mends outfits. |
| `tools/browser_check.js` | Headless-Chromium fallback for product pages that refuse a plain request. |
| `data/items-YYYY-MM-DD*.json`, `data/outfits-YYYY-MM-DD.json` | Each week's new picks and outfits. |
| `data/refresh-report.json` | What the last refresh changed: price moves, removals, renames, Workwear changes, shops not checked. |
| `docs/` | The built site (page plus data and photo files), served by GitHub Pages and published to the artifact. |
| `REFRESH.md` | The weekly refresh, step by step. |
| `UPGRADE_PLAN.md` | The review, what has been done, and what is next. |

Nothing here is part of the Greebtown app.
