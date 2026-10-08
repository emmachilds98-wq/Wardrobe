# The weekly refresh

Every week the wardrobe is checked against the shops: prices updated, picks that are no longer
sold (or no longer sold in his size) removed, new picks that fit added, outfits mended, and the
result published to the claude.ai artifact and to GitHub Pages.

- Artifact: <https://claude.ai/artifact/8uqcGr2eNmzbQv8UVBshY2>
- GitHub Pages: <https://emmachilds98-wq.github.io/Wardrobe/> (served from `main`; the root
  `index.html` opens `docs/`, which `build_site.py` writes)

## Steps

Use today's date as `D` (YYYY-MM-DD). Work on a branch, then merge to `main` so Pages updates.

1. **Download the catalogues** (about 15 minutes, 2 to 3 GB in `cat/`, which git ignores):

       python3 tools/weekly_refresh.py pull

2. **Check every pick** (about 30 to 60 minutes):

       python3 tools/weekly_refresh.py check --date D --browser

   - Shopify shops: matched by handle in the catalogue. Any pick missing from it is looked up
     on its own (`/products/<handle>.js`), so a partial download never removes a pick.
   - Other shops: read from the product page's schema.org data. Pages that refuse a plain
     request are opened in headless Chromium (`tools/browser_check.js`, a direct connection).
   - A pick is removed only when the page is gone (404 or 410), the product is sold out in
     every size, or his size is sold out. 6E safety boots are kept as watch items.
   - Price moves set `prev` (the "Price drop" tag) and add to `hist`. `added` is cleared on
     everything not new this week.
   - Prices are only trusted in pounds: requests ask for the UK market, other currencies are
     retried, and a shop whose prices all move by one shared factor is left alone.
   - The Workwear rules are applied (`weekly_refresh.py rules` does the same on its own).
   - Trouser fit: Dave likes trousers that do not grip. Slim, skinny and tapered trousers and shorts
     are removed (by name, our note, or the shop's description; a "relaxed taper" stays, and cuffed
     joggers only go if they are slim), and regular, straight, relaxed and wide fits get a `fit` label
     and rank higher. `weekly_refresh.py fit` does the same on its own.
   - The results are in `data/refresh-report.json`.
   - Then `python3 tools/weekly_refresh.py fabric` reads each pick's fibre composition from its listing
     (it also fixes card notes), and `node tools/check_3d.js --site docs --report` runs the 3D checks after the
     build in step 6.

3. **Find new picks** that fit (his sizes, style rules, Workwear rules, reduced first):

       python3 tools/sitemap_sweep.py @<non-Shopify hosts> --out cat_sm --max 150
       python3 tools/sweep_filter.py cat    --out data/items-D.json     --date D --per-shop 6 --per-cat 2
       python3 tools/sweep_filter.py cat_sm --out data/items-D-sm.json  --date D --per-shop 6 --per-cat 2

   The non-Shopify hosts are the shops behind `data/items-shops.json` that are not in
   `cat/_status.json`. Look over the new names: drop women's, children's, slim-fit work
   trousers, non-cotton work trousers, and anything that is not clothing.

4. **Photos for the new picks** (`--browser` retries the shops that refuse):

       python3 tools/fetch_photos.py --items data/items-D.json --prefix wD --size 360x450 --fit contain --quality 60 --browser --skip-existing

   Use the date without dashes in the prefix (for example `w20261006`). Then put the new photos
   on a contact sheet and look: drop women's, children's and anything that is not his clothing,
   and add a rule to `sweep_filter.py` for each kind of mistake so it does not come back.

4b. **Size charts** for shops with new picks (direct requests and headless Chromium only):

       python3 tools/size_charts.py --shops "<shop>,<shop>"

   Shops whose pages refuse plain requests are opened in headless Chromium (`via: "browser"` in its `SHOPS` table).
   It keeps the other shops' entries. A shop it cannot read goes under `_missing` with the reason; the card then
   shows no size check for it.

5. **Outfits:** first mend outfits that lost a piece, then add some built on the new picks:

       python3 tools/weekly_refresh.py outfits
       python3 tools/make_outfits.py --new-since D --per-style 4 --out data/outfits-D.json --id-prefix wD

   Read the new outfits and drop any that do not suit their style.

6. **Build and check:** `python3 tools/build_site.py --out docs`. Serve `docs/` locally and
   open it in Chromium: picks and outfits load, there are no console errors, and "New this
   week" shows only this week's picks.

7. **Publish:**
   - Commit, push the branch, open a PR and merge it to `main` (GitHub Pages rebuilds from it).
   - Republish the artifact from `docs/`: page `docs/index.html`, and every file under
     `docs/data/` passed in `files` with its path relative to `docs/`. Keep the artifact's
     `db` capability (do not pass `capabilities`), so the shortlist, thumbs and his wardrobe
     marks carry over. Set `null` for published data files that no longer exist.
   - Add a short entry to `UPGRADE_PLAN.md` with the numbers from the report.

## Shops that cannot be checked from the cloud

ASOS, Next, Zara, John Lewis, Fred Perry, TK Maxx, Dr Martens and a few others refuse requests
from cloud servers, even through a real browser. Their picks keep last week's price, and the
page warns once a price is more than 30 days old. Running step 2 from a home computer checks
them. Third-party relay or proxy services are not used.
