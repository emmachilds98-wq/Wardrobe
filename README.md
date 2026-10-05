# Dave's Wardrobe

A personal outfit planner for Dave: clothes picked for his sizes across seven styles, outfits
drawn on a figure of him, live prices with links, an outfit builder, and a shared shortlist.

The live version runs as a claude.ai artifact:
<https://claude.ai/artifact/8uqcGr2eNmzbQv8UVBshY2>. This repository is its offline home: the
page source, a copy of its data, the listing photos, and the tools that refresh them.

| Path | What it is |
|---|---|
| `page.html` | The page source as published. Opened directly in a browser it shows the layout; picks and outfits load only inside the artifact, where its database lives. |
| `data/items.json` | Every pick (name, shop, price, link, styles, occasion, weather, sizes). |
| `data/outfits.json` | Every outfit and the picks it uses. |
| `photos/` | Listing photos, shrunk to small WebP files and packed into JSON files the page loads. |
| `tools/fetch_photos.py` | Downloads and packs the listing photos. `--browser` retries refused shops in headless Chromium. |
| `tools/shopify_pull.py` | Downloads a whole catalogue (prices, stock by size, photos) from shops that publish a product feed. |
| `tools/asos_photos.py` | Fetches ASOS photos through wsrv.nl, since ASOS blocks cloud servers. |
| `tools/browser_fetch.js` | The headless-browser fallback used by `--browser`. |
| `UPGRADE_PLAN.md` | The review, what has been done, and what is next. |

Nothing here is part of the Greebtown app.
