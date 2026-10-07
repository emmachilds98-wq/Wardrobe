# Contributing: making outfits that look like the shop's clothes and fit Dave

This is the guide for anyone (person or agent) adding picks or outfits, or changing how they are drawn. It covers
what the data files hold, how the page turns a listing into clothes on Dave's 3D model, how to make an item match
its shop photo, how fitting works, and the checks that must pass before a change goes in. Read `HANDOFF.md` for
where the upgrade stands, and `REFRESH.md` for the weekly refresh.

The aim, for every piece on the 3D model and the 2D drawing: **the same colour, pattern, fabric, shape, length and
fit as the shop's photo, layered as it would really be worn, with no skin or holes where cloth should be.**

## Rules that never change

- **Dave's sizes:** L tops, 15.5–16 in collar, 34W 32L (never short or long leg), UK 11 shoes (wide fit).
- **Trousers must not grip:** no slim, skinny or tapered fits.
- **Workwear:** black or charcoal; 97%+ cotton with no stretch, or Cordura or polycotton; no work T-shirts; safety
  footwear EE, 4E or 6E with a toe cap (6E boots stay as watch items).
- **Prices in GBP only.**
- **Shop requests:** direct requests, shop feeds and sitemaps, and headless Chromium only. Never a third-party
  relay or proxy service (for example r.jina.ai).
- **Photos of Dave:** never in this public repo, cropped or not.
- **No AI model names** in commits, pull requests or code.
- **Fix the cause, not the case.** A change that fixes one outfit by special-casing it in `page.html` (an item id,
  an outfit id) is not accepted. If one item reads wrongly, correct it in `data/fixes.json` (below). If a kind of
  garment is drawn wrongly, fix the rule for that kind.

## The files

| File | What it holds |
| --- | --- |
| `data/items.json`, `data/items-*.json` | Every pick. The build merges them; the first file to define an id wins. |
| `data/outfits.json`, `data/outfits-*.json` | Every outfit. Merged the same way. |
| `data/fixes.json` | Corrections for items whose shop photo the page reads wrongly. |
| `photos/*-NN.json` | Listing photos (small WebP data URLs, keyed by item id), made by `tools/fetch_photos.py`. |
| `data/body.json` | Dave's 3D body (MakeHuman CC0), made by `tools/build_body.py`. |
| `page.html` | The whole page: styles, the 2D drawing, the Three.js 3D builder, the shop. |
| `docs/` | The built site. Never edit it by hand: run `python3 tools/build_site.py --out docs` and commit the result. |

### An item

```json
"asos-jj-harrington": {
  "name": "Jack & Jones Harrington jacket, stone",
  "shop": "ASOS", "url": "https://www.asos.com/...", "price": 45, "was": 60,
  "cat": "coat", "kind": "new",
  "style": ["quiet", "casual"], "occ": ["everyday"], "wx": ["mild"],
  "fabric": "100% cotton", "fit": "Regular",
  "note": "Why it suits him, in a sentence.", "checked": "2026-10-06", "rank": 120
}
```

The name and fabric are not just labels. The page reads them to decide how the piece is drawn (see "How the page
reads an item" below), so write them as the shop does and keep these habits:

- **Put the colourway after a comma or a dash at the end:** `"Farah Mullen Cotton Crew Neck Sweater, blue tide marl"`.
  The page looks for the colour there first. If the shop's colour name is unusual ("tide marl"), keep it, and make
  sure the outfit's `col` is the nearest palette colour.
- **Keep the garment words:** crew, V-neck, henley, half zip, button-down, Cuban collar, cargo, pleated, wide leg,
  relaxed, cropped, longline, oversized, padded, borg, cord, linen, denim. Each one changes the drawing.
- **Fill in `fabric`** from the listing ("100% cotton", "80% wool, 20% nylon") whenever the shop gives it.
- **`fit`** (trousers): one of `Regular`, `Relaxed`, `Straight`, `Wide leg`. It sets how far the legs stand off him.
- `cat` is one of: shoe, acc, coat, shirt, polo, knit, trouser, lounge, basics, tailor, swim, sport.
- `style`: quiet, casual, work, minimal, street, lounge, outdoor, summer, rave, mod, job (job is Workwear), sport.
  `occ`: everyday, party, smart, lounge, event. `wx`: mild, warm, cold, wet.

After adding items, fetch their photos (`python3 tools/fetch_photos.py`, see `REFRESH.md`). An item with no photo
is drawn from its name and the outfit's palette colour only, so it will rarely match.

### An outfit

```json
"autumn-budget": {
  "name": "Autumn weekend on a budget",
  "note": "Four pieces in brown, olive and beige for about £135 all in.",
  "occ": "everyday", "style": ["quiet", "casual"], "wx": ["mild"], "rank": 5,
  "look": "men beige harrington jacket brown jumper olive chinos brown leather trainers autumn outfit",
  "pieces": [
    {"item": "asos-jj-harrington", "shape": "jacket",   "col": "stone", "what": "Harrington jacket"},
    {"item": "uq-merino-crew",     "shape": "jumper",   "col": "brown", "what": "Merino jumper"},
    {"item": "sw-cord",            "shape": "trousers", "col": "olive", "what": "Cords"},
    {"item": "sw-trainer",         "shape": "trainers", "col": "brown", "what": "Leather trainers"}
  ]
}
```

- `occ` is one word; `style` and `wx` are lists (same words as for items). `ev` (optional) ties an outfit to an event,
  `tags` (optional) are free words for search. `rank` orders the outfit list (lower first). `look` is the search
  phrase for the card's Google Images and Pinterest links (ideas for how it is worn).
- **Each piece:** `item` (a pick's id; or `"own": "his work T-shirt"` with no item for something he already has),
  `shape` (below), `col` (a palette colour, below), `what` (the short name shown on the card, and read for a few
  words, below).
- **Every outfit needs at least one top, exactly one pair of trousers or shorts, and (outside lounge outfits) one
  pair of shoes.** The build stops if a top or legwear is missing. He is never drawn shirtless: an open jacket,
  blazer, coat, gilet, cardigan or waistcoat with nothing under it gets a plain white tee added, but put a real
  pick under it instead.
- Order does not matter. The page sorts tops by layer.

### Shapes

| Shape | Layer | Use it for |
| --- | --- | --- |
| `vest` | 0 | Vests and tank tops |
| `tee` | 0 | T-shirts (add "long" to `what` or the name for long sleeves) |
| `polo` | 0 | Polo shirts, knitted polos |
| `sshirt` | 0 | Short-sleeved shirts (Cuban, bowling, resort) |
| `shirt` | 0 | Long-sleeved shirts; overshirts and shackets too (named so, they hang over a shirt under them) |
| `rollneck` | 0 | Roll necks and turtlenecks |
| `jumper` | 1 | Crew and V-neck jumpers, sweatshirts; knitted vests and slipovers (named so, drawn sleeveless) |
| `hoodie` | 1 | Hoodies, zip or overhead |
| `halfzip` | 1 | Half and quarter zips, fleeces with a zip neck |
| `cardigan` | 1 | Cardigans (drawn open) |
| `waistcoat` | 1 | Tailored waistcoats |
| `jacket` | 2 | Jackets: Harrington, bomber, denim, trucker, fleece, shell, parka (drawn long), puffer (padded) |
| `blazer` | 2 | Blazers and sports jackets |
| `coat` | 2 | Overcoats, macs, long coats |
| `gilet` | 2 | Gilets and bodywarmers |
| `gown` | 2 | Dressing gowns |
| `trousers`, `shorts` | | Legwear (exactly one) |
| `boots`, `shoes`, `trainers`, `slippers` | | Footwear (at most one) |
| `scarf`, `snood`, `cap`, `bcap`, `beanie`, `bucket`, `belt`, `watch`, `tie`, `square`, `bag`, `backpack`, `sunglasses`, `chain`, `kneepads` | | Accessories |

Layer 2 pieces and cardigans are worn open over what is under them. A layer 0 or 1 piece is worn open when its
`what` says **"worn open"** (an open shirt over a tee). Shirts and polos are tucked in when the outfit has a blazer,
waistcoat or tie, or tailored or suit trousers (never with shorts); an overshirt over another shirt is not tucked.

Pick the shape for what the garment is, not where it is listed (shops file sweat shorts with knitwear and caps
with denim, and `tools/make_outfits.py` now reads the garment word in the name before the category): a knitted polo is `polo`, a shacket is `shirt`, a
fleece zip-through is `jacket` or `halfzip` by its neck. The build prints a note when a pick's `cat` is unusual for
the shape it is drawn as; check it.

### Palette colours (`col`)

`navy, cream, white, camel, olive, grey, charcoal, blue, brown, tan, burgundy, stone, sand, black, pink, green, indigo, silver`

`col` is the nearest of these to the item's real colour. It is what the 2D thumbnails use, and what the 3D model
falls back to when the photo cannot be read. A colour outside the palette stops the build. Pick it by looking at
the photo, not the name: an "ecru" jacket is `cream`, a "khaki" parka is `olive` or `sand` depending on the shade.

## How the page reads an item

When an outfit is shown, each piece goes through four steps. Knowing them is how you make a piece match.

1. **The listing's words** (`descOf` in `page.html`), from the item's `name`, `fabric` and `note` and the piece's
   `what`:
   - collar: button-down, band/grandad/mandarin, Cuban/camp/resort/bowling, spread/cutaway;
   - neck: V-neck, henley, mock/funnel, roll/turtle, crew;
   - zip: full zip/zip-through, half/quarter zip;
   - pockets: cargo/combat/utility; two/patch pockets/chore/overshirt/CPO; pocket;
   - fit: oversized/boxy/baggy/loose/wide (loose), relaxed, slim/skinny/muscle/fitted;
   - details: tipped, rugby, raglan/baseball/ringer, pleat, turn-up, drawstring, sleeve stripes or tape;
   - pattern words: check, plaid, tartan, gingham, houndstooth, herringbone, madras; stripe, Breton; print, camo,
     floral, paisley, Fair Isle, argyle, jacquard, geometric, tie-dye, all-over; graphic, logo, slogan, embroidered,
     badge, varsity;
   - material: leather, suede/nubuck, nylon/shell/waterproof/ripstop/puffer/padded/down, linen, cord/corduroy,
     denim/jean, fleece/sherpa/borg, wool/merino/cashmere/lambswool/tweed, satin/silk, waffle; chunky/cable/aran;
   - the named colour (the colourway after the last comma or dash first), a second colour ("white and black",
     "navy with white trim") and trim colours. Brand names that contain a colour word (Pretty Green, Red Wing,
     White Stuff) are ignored.
2. **The shop photo** (`sampleLook` / `readLook`): the background is flooded away from the corners, skin is found and
   left out, and the cloth that is left gives the main colour (`c1`), a second colour (`c2`), the pattern (`pat`:
   plain, hstripe, vstripe, check or print), the stripe or check spacing (`per`, a share of the garment's length) and
   how much of it is the stripe colour (`duty`), a swatch of a print, a cut-out of a chest graphic (`decal`), a photo
   front for flat-lays (`front`) and the sleeve colour where it differs (`slv`). If the listing names a colour and
   the photo disagrees (a black mesh vest on a model against white reads as skin and white), the named colour wins.
   Navy and indigo read darker than the named colour are taken halfway back toward it (they photograph nearly
   black). Denim follows its own rule (washes are read from the photo, never replaced by the name). **Stripes and
   checks are only read when the listing names a pattern** (stripe, Breton, check, plaid, gingham, print...): an
   unnamed repeat in a photo is nearly always something else, such as a zip and drawcords, a ribbed knit, or another
   piece the model wears. So if a striped or checked item is drawn plain, its name is missing the pattern word.
3. **The correction** (`data/fixes.json`, applied by `pieceLook`): anything you have set for the item replaces what
   the photo gave.
4. **Drawing:** the 3D builder (`make3Dcore`) and the 2D drawing (`figure`) both use the result, so they agree.

## Making an item look like its shop photo

1. Build and serve a test copy (see "Checking your change" below), then put the item beside its photo:
   `node tools/qa/multi.js out.png shirt id1,id2,...` (one 3D render per item next to its shop photo). Judge colour,
   pattern scale, collar, length and fit against the photo, not against your memory of the outfit.
2. If it is wrong, find out at which step:
   - the words: is the colourway at the end of the name? Is the neck, collar, zip or fit word there?
   - the photo: `node tools/qa/dump.js out.json` writes every piece's reading. Look at the item's `c1`, `c2`, `pat`.
   - the shape: is it the right shape for the garment?
3. **Fix the data first.** A better name or `fabric` (as the shop gives it), or the right `shape` or `col`, fixes
   most problems and stays fixed when the code changes.
4. **If the photo is read wrongly** (a lifestyle photo, a model's skin taken for the cloth, a stripe read as a
   check), add a correction to `data/fixes.json`:

   ```json
   "asos-jj-harrington": {
     "col": "#1b1c1e",
     "pat": "plain",
     "why": "The photo is on a dark background and reads as grey; the listing and photo show black.",
     "checked": "2026-10-07"
   }
   ```

   | Field | What it sets |
   | --- | --- |
   | `col` | The main colour, `#rrggbb`, sampled from the cloth in the shop photo (not the shadows or highlights). |
   | `col2` | The second colour (stripes, checks, trim), `#rrggbb`, or `""` for none. |
   | `pat` | `plain`, `hstripe` (across), `vstripe` (down), `check` or `print`. `plain` also drops a read swatch or front. |
   | `per` | Stripe or check spacing as a share of the garment's length, between 0 and 1 (a Breton is about 0.04). |
   | `duty` | How much of each stripe repeat is the second colour, between 0 and 1. |
   | `front` | `false` drops the photo front (when a model photo was taken for a flat-lay). |
   | `decal` | `false` drops the chest graphic cut from the photo (when it picked up something that is not a print). |
   | `why` | Required: what the shop photo shows, in a sentence. |
   | `checked` | Required: the date you checked it against the shop's page. |

   The build checks every entry (a known item, `#rrggbb` colours, a known pattern, shares between 0 and 1, `why` and
   `checked` present) and stops if one is wrong. Re-check the item with `multi.js` after adding it.
5. **If a whole kind of photo is read wrongly**, change the reader in `page.html`, but only with `dump.js` run before
   and after on every outfit, and the differences looked at one by one. A change that makes any item worse is
   reverted, even if it fixes others.

## How clothes are fitted to Dave

All fitting happens in `make3Dcore` in `page.html`, on the real body in `data/body.json`.

- **Maps of the body.** `fitMaps` measures the body as radial maps: the torso round a line through his chest (T), the
  shoulders seen from a point in his chest (Y), the neck round its own centre (N) and each arm round its own (A).
  Each map holds, per height (or elevation) and direction, how far out the body reaches. Hollows (between the pecs,
  the spine's groove, under the arms) are bridged with a convex hull, because cloth does not follow them.
- **Tops** are one fitted piece each (`fitTop`): torso, armholes and sleeves together, built out from the maps by the
  piece's ease. Ease is set by layer (about 0.8 cm next to the skin, 1.7 cm for knits, 3 cm for jackets), plus more
  for loose or relaxed words, less for slim, plus padding for puffers, and each layer is always a little further out
  than the one under it. The Edit Dave "cloth fit" slider scales it.
- **Lengths.** Tops end a set distance above or below his crotch (a tee covers the waistband, a blazer the seat), so
  lengths follow his body. "cropped" or "boxy" raise the hem, "longline" lowers it; parkas, macs and trenches are
  long. Short sleeves for `tee`, `polo` and `sshirt` (unless named long).
- **Layering.** As each piece is made it is added to maps of what he is wearing (`occAddMesh`), and the next piece is
  pushed outside them (`occPushPt`), so nothing underneath can come through. Collars (`fitCollar`) are built round the
  neck base and stand on what is under them. Sleeves under a long-sleeved outer layer are not built.
- **Trousers and shorts.** The seat, hips and tops of the thighs are one draped piece (`lowerWrap`); each leg carries
  on below it (`legSecs`), with the crotch sealed where the legs meet. The leg's cut comes from `fit` and the name:
  wide/baggy/barrel/parachute, relaxed/loose/carpenter/cargo, slim/tapered/cuffed/jogger, bootcut/flare, cropped/ankle.
  Over boots the hem rests on the boot. Cuffed joggers gather above the shoe.
- **His skin under the clothes.** The body's triangles that clothes cover are left out, so skin can never poke
  through cloth (`bodyIdx`, from rules per region and height). After the clothes are built, any of those triangles
  that no cloth actually goes round (checked on the maps of what he wears) are put back, so the edge of a neckline, a
  vest's armhole or a cropped hem never opens onto the background. If you add a garment with a new opening, this is
  what keeps his skin there; check it from the side and the back.
- **Hidden parts.** A closed outer layer hides the front details of what is under it (pockets, plackets, cords). A
  top worn over the waistband hides the belt.

### Rules for fitting changes

- Fit from the body maps, never from fixed numbers for one body: Edit Dave changes his shape, and every piece must
  still fit.
- Keep every layer outside the layer under it through the occupancy maps; never hide a poke by moving one piece.
- A new garment detail is built on the fitted cloth (its rows and columns), not floating at a fixed position.
- Check every outfit that uses the shapes you touched, from all five views (below), not just the one you were
  looking at.

### Adding a new garment shape

1. Add it to `UPPER`, `LOWER`, `FEET` or `ACCS` in `page.html`, and to `LAYER` and `HEM` if it is a top.
2. Give it a hem distance (`dH` in `make3Dcore`), its ease, whether it is open, and whether it has sleeves.
3. Draw it in 2D (`figure`).
4. Add it to the shape table in this guide and to `SHAPE_CATS` in `tools/build_site.py`.
5. Add an outfit using it to `tools/qa/gate.txt`, so the pull-request check covers it from then on.

## Checking your change

Everything below must pass before a change is merged. The pull-request check (`.github/workflows/check-3d.yml`)
runs the build checks and the 3D check automatically, but run them yourself first.

1. **Build:** `python3 tools/build_site.py --out docs`. It stops on:
   - an outfit piece whose item is not a pick, an unknown shape, a colour not in the palette, a piece with no `what`;
   - a piece drawn as a different kind of garment from the one its name says (sweat shorts drawn as a jumper, a cap
     as trousers). The kind comes from the last garment word in the name before the colourway (`garment_kind`), so a
     "Chino Jacket" is a jacket and "Jogger Shorts" are shorts;
   - an outfit with no top, or not exactly one pair of legwear, or two pairs of shoes;
   - an `occ`, `style` or `wx` word the page does not use;
   - a wrong `data/fixes.json` entry.

   It prints a note for outfits with no shoes and for unusual pick/shape pairs. Commit `docs/` with your change: the
   live site is served from it, and the pull-request check fails if it is out of date.
2. **Serve a test copy:** `sh tools/qa/serve.sh /tmp/wardrobe-qa 8770` (in the background). All QA scripts read
   `QA_PORT` (default 8770).
3. **Look at it:**
   - `node tools/qa/zoom.js out.png <outfit id> "rotY,camY,camZ,lookY;..."`: close-ups from any angle (front
     `0,1.3,1.4,1.25`; back `3.14159,1.3,1.4,1.25`).
   - `node tools/qa/multi.js out.png shirt id1,id2`: items beside their shop photos.
   - `node tools/qa/ray.js <outfit> "[[x,y],...]"`: which layers sit at a point, front to back.
   - `node tools/qa/smoke.js`: the Outfits view in 2D and 3D, with any page errors.
4. **Run the 3D check** on the outfits you touched:
   `node tools/check_3d.js --site docs --ids a,b,c --out qa --debug` (or `--ids @file` with one id per line).
   For a change to the 3D builder or the photo reader, run it on every outfit (see below).

### What the 3D check measures

Each outfit is rendered from five views (front, front three-quarter, side, back three-quarter, back), as the page
shows it and in flat ID colours (one per piece, the body by region). It counts, in pixels at 300×440:

| Count | What it is | Limit |
| --- | --- | --- |
| `poke` | An inner layer or his skin showing through a piece worn over it (islands inside the outer piece). | 30 |
| `holes` | Background showing through the clothes. | 25 |
| `stray` | Small bits of a piece standing off on their own. | 40 |
| `skin` | His skin where the outfit covers him: torso under a top (below the armholes when a vest is worn on its own), upper arms under sleeves, forearms under long sleeves, thighs under shorts, legs under trousers. A gap at a hem, cuff or waistband, or a hole in the cloth. | 12 |
| `seethrough` | Where the background shows inside the clothes but his body would be there: a hole in the cloth, cloth sunk inside him, or skin cut away where no cloth covers it. | 12 |
| `sunk` | The same at the outline of the figure (cloth sunk inside him at an edge, or a sleeve too short). His feet are left out: a shoe is a shell over the foot. | 60 |
| `colour` | A plain piece whose rendered colour is far from its target (another hue, much too light or dark, or lost its colour). The target is the photo reading or the `data/fixes.json` colour. | — |

`poke`, `holes` and `stray` are counted on the front, side and back views; `skin`, `seethrough` and `sunk` on all five.
A count over its limit flags the outfit, and the flag names the part of him it is over ("front skin 40 (belly 30,
hips 10)"). `report.json` in the output folder has every count; with `--debug` the ID image of each view is saved
with the faults marked in red, and sunk cloth at the outline in yellow (`<id>-<view>-id.png`), next to the render.

**The limits are not to be raised to make a change pass.** If a limit is wrong (it flags something you can show is
not visible on the page), change how the check measures it, and show with `--debug` images that real faults are
still caught (cut a hole in a piece, shorten a sleeve, and see it flagged).

### When the 3D check fails

1. Open the `-id.png` and render for the flagged view (`qa/`, or the run's `qa-*` artifact on the pull request). Red
   marks where the fault is.
2. Look closer with `zoom.js` from that side, and `ray.js` on a red point to see which layers are there.
3. Fix the cause in the rule that made it (the fit, the layer push, the hem distance), not in that outfit. Then re-run
   the check on every outfit using the shapes involved.

Common causes:

- skin at a waist: a top's hem above the waistband of the trousers (check `dH` and the tuck rule);
- skin at a cuff: a sleeve ending short of the wrist, or a short sleeve under a long one that was not built;
- see-through on the torso: a gap between the yoke and the body of a top, or the front opening of a top with nothing
  under it;
- poke: an inner collar, placket or hem not pushed outside the outer layer (look at the occupancy maps);
- holes at the crotch or between the legs: the trouser seal;
- colour: a wrong photo reading (correct it in `data/fixes.json`) or a wrong palette `col`.

### The full check

Changes to `page.html`'s 3D builder or photo reader need the full run over all outfits (45–90 minutes):

```sh
python3 tools/build_site.py --out /tmp/snap
for k in 0 1 2; do node tools/check_3d.js --site /tmp/snap --shard $k/3 --out /tmp/qa$k & done; wait
```

Merge the three `report.json` files and fix every flagged outfit before merging. The weekly refresh also runs it
(`--report` writes the summary into `data/refresh-report.json`).

## Recipes

**A new outfit**
1. Add the picks it needs to `data/items-YYYY-MM-DD.json` (sizes and taste rules above), fetch their photos.
2. Add the outfit to `data/outfits-YYYY-MM-DD.json`: a top, legwear, shoes; the right shape and palette colour for
   each piece; a `note` that says why it suits him.
3. Build, then `multi.js` on its items and `check_3d.js --ids <outfit>`. Fix anything flagged.
4. Commit `data/` and `docs/`. The pull-request check renders it again.

**A colour that is wrong on the model**
1. Check the item's name has its colourway and its outfit `col` is right.
2. `dump.js`: what did the photo give?
3. Correct it in `data/fixes.json` with `why` and `checked`, build, and check with `multi.js`.

**Skin or a hole on an outfit**
1. `check_3d.js --ids <outfit> --debug`, then `zoom.js` and `ray.js` where it is red.
2. Fix the rule for that kind of piece in `make3Dcore` (or `fitTop`, `lowerWrap`, `legSecs`, `fitCollar`).
3. Re-check every outfit using that shape; run the full check if it touches all tops or all trousers.

## Lessons learned (do not repeat these)

- **Classes in the ID pass must be worked out once**, before any materials are swapped; reading them after a swap put
  the floor in the body's class.
- **Do not overwrite the body's `color` attribute** for the region pass; it carries the skin colours. Use a separate
  attribute and shader.
- **Every mesh needs UVs** if it uses a cloth texture; without them it renders as one pale colour (the open-front
  facing strip did).
- **`norm()` in `page.html` keeps only the fields it knows.** A new item field the page should read must be added
  there (as `fix` was, through `normFix`).
- **Radial offsets square the shoulders**: dilate the map (`fmDilate`) rather than pushing points out along rays.
- **Collars tip forward** if they are built round a centre that moves with the neck; use the fixed neck-base centre.
- **Skin colour alone does not find skin in photos** for darker-skinned models; widening the colour range broke cream,
  stone, tan and khaki items. It was reverted.
- **Dropping a photo's cloth square when the colour disagrees** made more items worse than better. It was reverted.
- **A bulky top can stand its armhole out past the line of his arm.** The sleeve's directions used to be read from
  the armhole's points round the arm; on a puffer the armhole no longer went round it and the sleeve came out flat,
  with a slit down the inside of the forearm. Directions now follow the armhole's length when that happens.
- **Cutting away skin by region and height alone leaves gaps** where a neckline or armhole sits lower than the cut
  (the sides of a crew neck, a muscle vest). The cut is now checked against the cloth actually built.
- **One item looking right is not proof.** Check every item of that kind with `multi.js`, and every outfit with
  `check_3d.js`.
