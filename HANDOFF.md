# Handover: finishing the wardrobe upgrade

For the next agent picking up Dave's wardrobe planner. Read this first, then `CONTRIBUTING.md` (how
outfits are made, matched to their shop photos and fitted, and the checks every change must pass), then
`UPGRADE_PLAN.md` section 4 (the review and order of work) and its latest entries, then `REFRESH.md`.

- **Live page (GitHub Pages):** <https://emmachilds98-wq.github.io/Wardrobe/>. It is served from
  `main`; the root `index.html` opens `docs/`.
- **claude.ai artifact:** <https://claude.ai/artifact/8uqcGr2eNmzbQv8UVBshY2>. It holds the
  shared database: shortlist, thumbs, his wardrobe and his saved fits.
- **Review and plan doc (Claude Doc):** <https://claude.ai/code/artifact/a11be046-83a3-47dc-855c-67657c180e7e>.
  The "Order of work" table there has a Status column. Keep it current.
- **Weekly refresh routine:** trigger `trig_01911aWmpSBcYLDdVLAzoa3y`, Fridays 06:51 London. It
  follows `REFRESH.md`, including the fabric backfill and the full 3D check.

## The goal

Every item on the 3D model should look like the real product: right colour, pattern, fabric,
shape, length and fit, and layered as it would be worn. The 2D drawing and the rest of the site
should match. Emma asked for the upgrade to continue until that is done.

## Rules that never change

**Dave's sizes and taste:**
- L tops, 15.5–16 in collar, 34W 32L (never short or long leg), UK 11 shoes.
- Trousers must not grip: no slim, skinny or tapered.
- **Workwear:**
  - Black or charcoal, 100% cotton (97%+), no stretch; Cordura or polycotton.
  - No work T-shirts.
  - Safety footwear EE, 4E or 6E with a toe cap. 6E boots stay as watch items.
- Prices in GBP only.

**Data and access:**
- **Shop requests:** never route them through third-party relay or proxy services (for example
  r.jina.ai). Use only direct requests, shop feeds and sitemaps, and headless Chromium.
- **Photos of Dave:** never put them in this public repo, cropped or not. The classifier refused
  it as personal data. They may go in only if Emma adds a permission rule herself.
- **Model names:** none in commits, PRs or code.

**Publishing the artifact:**
- Page: `docs/index.html`.
- Data: every file under `docs/data/` (about 71 files, including `data/body.json`), passed in
  `files` by its path relative to `docs/`.
- Never pass `capabilities`: that keeps the db.

## How to work

1. Branch from `main`.
2. Edit `page.html`. This is the whole page: CSS, the 2D figure, the Three.js r128 3D builder and
   the shop.
3. Build: `python3 tools/build_site.py --out docs` (copies the page to `docs/index.html` and writes
   `docs/data`).
4. Serve a test copy: `sh tools/qa/serve.sh /tmp/wardrobe-qa 8770` in the background. It injects
   `window.__dw` into a copy, never into `docs/`.
5. Look at what you changed. All QA scripts read `QA_PORT` (default 8770):
   - `node tools/qa/zoom.js out.png <outfit id or JSON pieces> "rotY,camY,camZ,lookY;..." [bg]`:
     close-ups from any angle (front is `0,1.3,1.4,1.25`; back is `3.14159,...`).
   - `node tools/qa/multi.js out.png shirt id1,id2,...`: items one by one beside their shop photos.
     The best way to judge fidelity.
   - `node tools/qa/ray.js <outfit> "[[x,y],...]"`: which layers sit where, front to back. Use it
     to find what pokes through what.
   - `node tools/qa/smoke.js`: Outfits view in 2D and 3D, with page errors.
   - `node tools/qa/dump.js out.json`: every outfit piece's photo reading. Run it on the old and
     the new build and diff them whenever you touch the photo reader (`sampleLook`).
6. Run the 3D check:
   - Single outfits: `node tools/check_3d.js --site <dir> --ids a,b --out <dir> [--debug]`. It
     renders five views and flags skin where clothes should be, see-through cloth, sunk cloth at the
     outline, pokes (an inner layer showing through), holes, stray parts and colour drift. With
     `--debug` it also saves an ID image with the faults in red. Limits and what each count means
     are in `CONTRIBUTING.md`; never raise a limit to make a change pass.
   - Every pull request runs the build's data checks and the 3D check on the outfits it touches plus
     `tools/qa/gate.txt` (`.github/workflows/check-3d.yml`).
   - The full run over all 574 outfits takes 45–80 min. Run it in the background on a snapshot
     copy of `docs/`.
7. Ship it:
   - Commit, push, and open a draft PR.
   - When the checks are clean, mark it ready and merge with the full 40-character head SHA as
     `expectedHeadSha`.
   - Republish the artifact.
   - Confirm the Pages site serves the new build (fetch it and look for a string you added).
   - Add an entry to `UPGRADE_PLAN.md` and update the doc's status column.

**Where things are in `page.html`** (search by name):

| Part | Functions |
| --- | --- |
| Listing words | `descOf` (fit, collar, fabric…), `texOf` (cloth pattern from the name) |
| Photo reader | `sampleLook`, with `swatch()` inside it, run through `trueFor`. Colours, stripes, checks, prints, photo fronts, the named-colour check, the denim rule |
| 3D scene | `make3D` / `make3Dcore`. Tops: `fitTop`, `wrapGeo` / `wrap`. Trousers: `lowerWrap`, `legSecs`. Collars: `fitCollar`. Layers: occupancy maps `occPushPt` / `occAddMesh` |
| Cloth textures | `lookTex` (3D), `lookFill` (2D) |
| Accessories, shoes, boots, ties, bags | The long `else if(p.shape===...)` chain near the end of `make3Dcore` |
| 2D drawing | `figure()`, `face2D`, `applyChar2D` |
| Edit Dave and fitting room | `CHAR`, `openCE`, `UNDERWEAR` |

## Where it stands (7 Oct 2026, PR #11)

**3D check:**
- The first full run flagged 93 of 574 outfits. All are fixed.
- The second run flagged 3. All are fixed, and the 76 related outfits re-checked clean.
- A third full run on the final build was still going when this was written. If
  `node tools/check_3d.js --site docs --report` shows any flags, start there.

**Done in part, by phase of the plan:**

| Phase | Done | Not yet |
| --- | --- | --- |
| 1 | Listing and photo reading at page load | Stored specs (`data/specs.json`), archetypes |
| 2 | Real CC0 body driven by Edit Dave, fitting room with underwear | Newer Three.js, poses |
| 4 | Colours, denim washes, prints repeating as they are, checks woven from the photo, photo fronts for flat-lays, sunglasses | Fabric library, stripe/check shader, shoe photos |
| 5 | Fitted tops, layering and tucks, hoods, boots and hems, trouser cuts | Ease-driven fit from measurements |
| 7 | Weekly 3D checks | Scoring against photos, approve page |

**Elsewhere:**
- 2D: Dave from Edit Dave, trousers by cut.
- Shop: fabric filter, better search, real price drops, a "why it suits him" line.
- Data: fabric backfill.

## What to do next, in order

1. **Close the small known faults.** Check each with `zoom.js` and `check_3d.js`.
   - **Polo collars:** a small notch at the back of some (`fitCollar`).
   - Done: belts (a shirt or polo is tucked when a belt is worn, in 2D and 3D, and the belt goes
     round the waistband), workwear kit drawn over the clothes (tool belts, holster pockets,
     pouches, aprons), pocket squares in the breast pocket (PR #12), and pale slivers from flat-lay
     backgrounds on photo fronts.
   - **Tee under shirt:** check that a tee under an open shirt never covers the shirt
     (barrel-chore, ox-open, ramsey-weekend, x11-passenger).
   - **`ramsey-street` on the loose cloth fit:** a few pixels of the overshirt's collar show inside the hoodie's neck
     opening (poke 31, limit 30; the same on `main`). It looks right (a collar peeking out), but the check counts collar
     bits enclosed by the hood as pokes. Done: `wk-chore` (a chore jacket now goes over the knit) and three other
     collar-under-knit outfits (collar rows are evened out round the neck).
   - Done: sets listed as one item and worn as two pieces can be corrected per garment shape
     (`"shapes"` in `data/fixes.json`); the Tokyo Laundry Keir set is (black tee, grey marl shorts).
   - Done: named stripes the photo cannot measure (close-ups, folds, a model in shot) are drawn as
     clean stripes in the cloth's colours, and close-up photos scale their pattern down (`L.close`).
   - Done: model photos are found by the shape of a head and neck (`headM`), whatever the skin
     colour, and their fronts are not used (hoodies excepted: a hood up looks the same). Hands at
     the sides are not looked for yet.
2. **Store what is read (Phase 1 / step 3):**
   - Write each piece's reading (colour, pattern, cloth square, fit, length, collar) into
     `data/specs.json` at build time, with its source and a confidence.
   - Done: the manual override (`data/fixes.json`, applied by `pieceLook`) and the data checks in
     `build_site.py` (outfits and fixes).
   - This also makes the page faster, since photos are no longer read on every visit.
3. **Faster page (step 4):**
   - Load photo packs per screen.
   - Done for the outfit cards: lighter hair (`LITE3D`) cut each card render from about 2.0 million
     triangles to 0.45 million. The 3D view still draws the full hair (about 1.9 million triangles
     of curls); a level of detail by distance would help phones there too.
   - Build the body and hair once and swap only the clothes.
4. **Engine and poses (Phase 2):**
   - Three.js r128 → r160+. `encoding` becomes `colorSpace`, the `if(T.sRGBEncoding)` guards
     must change, and lights need about ×π.
   - Then three poses.
   - Ask Emma first: it is a listed decision.
5. **Garment templates (Phase 3):**
   - About 45 archetypes draped in headless Blender (download.blender.org is reachable), with
     morphs for length, ease and leg width.
   - Ask Emma first.
6. **Phases 4–7 as in the plan:**
   - Fabric sets (ambientCG, Poly Haven, CC0).
   - Shoe lasts and photo-projected shoe sides.
   - Ease-driven fit.
   - Render-against-photo scoring (outline overlap ≥ 0.8 and colour ΔE ≤ 5 for 90% of pieces),
     with an approve page.

**Rules for every change:**
- Judge it against the shop photos with `multi.js`, not by eye in one outfit.
- Run `dump.js` before and after any photo-reader change.
- Re-run `check_3d.js` on every outfit that uses the shapes you touched.
- A change that makes some items worse is reverted, even if it fixes others. Two such attempts
  are recorded in 2zx: a wider skin rule, and dropping cloth squares when the colour disagrees.

## Needed from Emma

- Dave's measurements: chest, waist, hips, inside leg, shoulder and sleeve. Also confirm 1.83 m
  and the 15.5–16 in neck.
- **Reference photos:** what to do with them. Either she adds a permission rule so they can go
  in the repo, or they stay private.
- **Phases 2 and 3:** a yes to the newer Three.js and to Blender-made templates.
