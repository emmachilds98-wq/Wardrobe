# Continuing the upgrade: a guide for the next engineer

Written 15 Oct 2026, when work paused after PR #68; updated for the draped blazers, overcoats, remaining jackets, polos, V-necks, cardigans, the last jackets, collars under open jackets, the sleeveless tee, henley and mock-neck tee, open overshirts under open jackets, and Three.js 0.186.1. Read this first, then `STATUS.md` (what is happening now and the
log), `HANDOFF.md` (how the page fits together) and `CONTRIBUTING.md` (the data rules and every check). The long
history and the reason behind each rule is in `UPGRADE_PLAN.md`, newest sections last before "3. Next steps".

## Where it stands

- **Live site**: GitHub Pages serves `docs/` from `main`: <https://emmachilds98-wq.github.io/Wardrobe/>.
- **Claude artifact**: <https://claude.ai/artifact/FtdHKgXdaBGrVmpbVYTrLn> is the one copy Emma keeps and comments
  on. It must always match `main` (see "Shipping" below). Other copies belong to other accounts; ignore them.
- **What the upgrade is**: each top in the 3D fitting room used to be drawn by `make3Dcore`, the page's hand-built
  shapes (stiff shells). The upgrade replaces them with **draped templates**: real flat patterns sewn and settled
  as cloth on Dave in headless Blender (`tools/build_garments.py`, output `data/garments/<template>.json`), then fitted
  to whichever body and layers are worn, in the page (`drapeTops`, `drapeSettle`).
- **Coverage**: 946 top pieces across the outfits are draped. Only 6 still use `make3Dcore`'s shapes, plus every top
  worn tucked in, which is never draped (`TUCK0`): 5 that `drapeArch` sends nowhere (Carhartt's Super Dux and the
  four insulated and borg-lined overshirts) and the borg zip-through in
  g-casual-01, which it sends to `puffer` but which stays on `make3Dcore` over a half-zip (see the rule by `TUCK0`). (Counted piece by piece in each outfit. `tools/qa/drape_survey.js`,
  below, gives one row per item, its template taken from the first outfit it is in, so a piece filed under another
  shape in another outfit can hide there: the guide said 932 and 20 until this was counted.) Run it for the live list.
- **Templates** (`DRAPEF` in `page.html`; `_up` is the same garment done up, and the plain name is worn open where it
  can open, per `DRAPEOPEN`):
  - Knits and tees: `tee`, `tee_ls`, `jumper`, `jumper_v` (a V neck), `cardigan(_up)` (`jumper_v`'s knit with its front
    in two), `rollneck`, `halfzip`, `hoodie`, `kvest`, `vest` (a tank), `vest_tee` (a sleeveless tee: the tee's crew
    neck, no sleeves, deep armholes), `tee_mock` (`tee_ls` with a 3.5 cm band standing round his neck).
  - Shirts and polos: `shirt(_up)`, `sshirt(_up)`, `camp(_up)`, `polo`, `polo_ls`.
  - Jackets: `jacket(_up)` (the track jacket's cut), `jacket_hood(_up)`, `jacket_coll(_up)`, `bomber(_up)`,
    `chore(_up)`, `trucker(_up)`, `puffer(_up)`, `puffer_hood(_up)`, `parka(_up)`, `aviator(_up)` (a big collar drawn in the
    shearling's colour), `gilet`, `gilet_hood` (a hood, no stand collar).
  - Tailoring: `blazer(_up)` (a shawl collar: the collar and lapels in one, rolled down the V to the button).
  - Coats: `overcoat(_up)` (the blazer's lapels on a coat to his knees), `carcoat(_up)` (a shirt collar, a fly front).
  - Accessories: `scarf`.
- **Which template a piece gets**: `drapeArch(p)` in `page.html` decides, from the piece's shape and the words in its
  item name and `what`. It returns `null` for anything a template would draw wrongly; that piece keeps `make3Dcore`'s
  shapes. Every rule there has a comment saying why.

## What is left, in a sensible order

The plan for the model from here, in order, with how to tackle each item and when it is done, is `UPGRADE_PLAN.md`
section 5 (16 Oct 2026): his jawline (done 16 Oct, PR #82), Edit Dave's skin tone and new colours (done 16 Oct, PR #83) and its panel layout (done 16 Oct, PR #84), the shoes and trouser hems (the hems done 16 Oct, PR #85, the shoes PR #87), a relaxed stance and poses (a breath and a
sway in the live views was tried in PR #88 and taken out in PR #89: it read as the picture rocking),
tucked-in tops, draped trousers, then the items below and the rest. The table lists the tops still on `make3Dcore`.

| Item | Pieces (outfits) | What it needs |
| --- | --- | --- |
| Two jackets that fail the check draped | 2 (2) | Carhartt's Super Dux (jb8-superdux): on `jacket_hood` and on `puffer_hood` the tee under it shows between its hem and the top of his tool belt; it would need cutting longer, or the belt worn over its hem. The borg zip-through over a half-zip (g-casual-01): on `jacket` and on `puffer` the half-zip's collar comes through its collar at the back of his neck. |
| Shards beside the neck, open over open | (2) | Since the fix for an open overshirt under an open jacket (UPGRADE_PLAN, the last section), what is left of it is a few small shards of the shacket beside his neck in g-mod-11 and g-mod-13, where the shacket's collar meets the jacket's, and a dark hole at the back of g-casual-09's left shoulder (on `main` before the fix too). Measure with `tools/qa/through.js`. |
| Insulated and borg-lined overshirts | 2 (4) | Tog24's Adamson and Matalan's borg overshirt are `chore`'s cut, and were tried on it again with the open-over-open fix. Under open jackets (g-outdoor-05, -09) the padded shacket still came through the jacket's lower front and round his neck in jagged patches, and under a done-up gilet (g-outdoor-21) the gilet bulged and creased at his neck; only g-outdoor-19 was passable. Tried again with a padded layer's 14 mm gap under the jacket, a 12 cm size step and an 8 mm push back under it: `tools/qa/through.js` over the four fell from 1,008 to 457 pixels, but `main`'s flat shapes count 9, 0, 15 and 821 (g-outdoor-21's pocket flaps through the gilet), and g-outdoor-05 and -09 still show shards, so they stay. |
| Shirt-collared overcoat | (1) | The ASOS tobacco overcoat (cold-commute) has a shirt collar buttoned to the neck in its photo, a car coat's, but takes `overcoat`'s lapels. Sent to `carcoat` (a `collar` correction tried, then taken out), it came out worse. Looked at again: worn open, `carcoat`'s collar is there but lies flat and low, a narrow turn at his neck (ms-one-shop); the bigger miss is length, `carcoat` falls to mid-thigh and this coat to below the knee. It would need a long car coat (a balmacaan: `carcoat`'s collar and fly front on `overcoat`'s length and raglan sleeves). One outfit; low value. |
| Stringers, racer backs, drop-arm and cropped vests; raglan and baseball tees | 0 now | None are in the outfits now; `drapeArch` returns `null` for them so they keep `make3Dcore`'s shapes when one is added. A racer back and a raglan sleeve are not in the builder. |
| Tucked-in tops | many | Never draped (`TUCK0`): only with tailoring, a belt or a tie. A draped top would need its hem taken inside the trousers. Large job, modest gain. |

Also noticed, not fixed, on `main` too: on rv-black-smart the link chain is drawn as a straight bar across his neck;
in n4-stone-navy his chest shows through the shirt's front under the Harrington; in g-quiet-30 dark spikes stand out
round his neck under the jacket; in pub-lunch the scarf crumples at his neck inside the wax jacket.

### Lapels (the blazer, 15 Oct 2026)

Shipped as `blazer` and `blazer_up`; the full story is in `UPGRADE_PLAN.md`, "Draped blazers". The front's neckline is a
V 44 cm deep (`vneck`) to the top button. Two pieces make the collar:

- `lapel_stand` is sewn round the whole neckline. It is 3 cm high at the back and narrows down the V to half a centimetre
  at the button, so its top edge is the roll line. `close_seams` stands it straight up at the back and lays it in across
  his chest down the V, carried on from the front.
- `lapel_leaf` (`lapel` measure) is the collar and lapels in one. It is folded back over the stand and laid 7 mm out on
  the cloth; `relax` keeps it out over the front while the cloth is eased (its `over` argument).

The page turns the leaf's triangles round when it loads the template (`drapeTurn`): folded back, it faces in as cut.
A blazer keeps a shirt's collar inside it (`leafIn`), and its own lapels are never laid out over a coat. A notched lapel
is drawn as a shawl. The overcoat uses the same two pieces on a longer, roomier body.

## How to add or extend a template

1. **Measure**: add an entry to `MEAS` in `tools/build_garments.py`, with a comment on the cut, and on what was tried
   and failed. Keys: `chest, length, shoulder, armhole, neck_w, neck_f, neck_b, sh_drop, band, band_k`. Optional keys:
   - `sleeve, bicep, wrist, cuff, cuff_c` (leave `sleeve` out for none);
   - `collar` (a stand), `leaf, point` (a shirt collar folded over it);
   - `hood_h, hood_d`, `pad`;
   - `open` (the front in two);
   - `vneck`.
2. **Build it**: `python3 tools/build_garments.py --only <name>`. It takes about 1.5 minutes, and two can run at once.
   It is deterministic but chaotic: a small change to the cut can change how a collar settles, so render after every
   change.
3. **Wire the page** (`page.html`):
   - add the name to `DRAPEF`;
   - for a new shape, add `DRAPEK`, and add `DRAPEOPEN` if it opens;
   - add a rule in `drapeArch`, with a comment;
   - add details (buttons, plackets, zips, pockets, rib) in `drapeDetails`;
   - add rib materials in the mesh code near `knit=`.
   Search for an existing template's name (`sshirt`, `camp`) to find every place one is listed.
4. **Build the site**: `python3 tools/build_site.py --out docs`, which also copies `data/garments` into `docs/data`.
   Commit `data/garments/<name>.json` and `docs/` with the change.

## How to look and check

- **Serve a test copy**: `sh tools/qa/serve.sh /tmp/wardrobe-qa 8770 &`. The QA scripts read `QA_PORT`.
- **Survey**: `node tools/qa/drape_survey.js '^(blazer|coat)$'` lists each piece of those shapes, the template it gets
  (`-` for none), and the outfits it is in. Use it to find the work, and to confirm a new rule catches exactly the
  pieces you meant.
- **Render**: `node tools/qa/zoom.js out.png <outfit id or JSON list of pieces> "rotY,camY,camZ,lookY;..."`.
  - `rotY` is in radians (front 0, back 3.14, three-quarter 0.9).
  - `QA_BODY=athletic` uses another body; `QA_WEAR=zip=up,tuck=out` sets how the outfit is worn.
  - `QA_INIT='window.__drape=0'` shows `make3Dcore`'s shapes, for a before and after.
  - A JSON list of pieces renders a garment on its own: `'[{"col":"black","item":"<id>","shape":"vest","what":"Vest"}]'`.
- **Show-through under an open front**: `node tools/qa/through.js <outfit ids>` counts the pixels of small patches of
  any layer lying wholly inside the outermost draped top's outline, in flat colours from 8 directions. The 3D check
  misses these (see the pitfalls). Single outfits are noisy: compare totals over several outfits on all five bodies
  (`QA_BODY`). `THROUGH_SAVE=out.png` saves two views with the counted patches in red.
- **3D check**: `node tools/check_3d.js --site <dir> --ids @list.txt --body <b> [--wear zip=up,tuck=out] --out <dir> --debug`.
  - **Bodies**: run every affected outfit on all five bodies (dave, slim, athletic, heavier, loose) as worn, and done
    up (`--wear zip=up,tuck=out`) on dave and loose.
  - **Why locally**: CI checks only the gate set (`tools/qa/gate.txt`), so a new template's own outfits are checked
    only here.
  - **Running**: four to seven runs side by side are fine. Background shells are killed at 2 hours, so split long
    runs into waves.
  - **Waiting**: wait on an output file (`until [ -f done ]`), never on `pgrep -f` with a string from the waiter's
    own command line, which matches itself.
  - **Results**: a run's last line is JSON with `flagged`; each flagged outfit is listed above it with its numbers.
    See "What the 3D check measures" in `CONTRIBUTING.md`.

## Shipping (every change)

1. Branch, commit with `docs/` rebuilt, push, and open a pull request.
2. CI runs the data checks, stored specs and the 3D check (gate set, 5 bodies, 3 parts each), and takes about
   10 minutes. Merge only when everything is green and your own body checks are clean.
3. Merge to `main`; GitHub Pages updates itself.
4. Republish the artifact as a new version of the same link:
   - page `docs/index.html`, root `docs`;
   - in `files`, only the `docs/data/...` files that changed (`git diff --name-only <last merge> <new merge> -- docs/`);
   - never pass `capabilities`, which would drop the artifact's database and settings.
5. Add a line to the Log in `STATUS.md` (date, PR, what, artifact version), update **Now**, and add a section to
   `UPGRADE_PLAN.md` with what was tried and the **Checked** line.

## Pitfalls already paid for (do not repeat)

- **A stand on a scoop or V neck stands up.** It pulls the neckline into a shallow V at his throat. The tank `vest`
  has no binding at all; the knitted vest's rib is a strip laid on the cloth in `drapeDetails`, not a sewn piece.
- **A shirt collar needs about a 2.5 cm stand.** On a 1 cm stand the leaf will not fold down and crumples at the
  back of the neck. A plain short sleeve with no band does the same to the collar of an open short-sleeved shirt.
- **A deep V shows his chest** where the garment is worn with nothing under it (g-casual-16): the check counts skin.
  Keep a V to about 14 cm unless every outfit has a layer under it.
- **Straps of a tank**: cut 36 cm across the shoulders, it hangs as a sleeveless tee. A tank is about 29 cm across with
  a 19 cm neck.
- **A sleeveless tee cut to the tee's neckline** dips into a V at his throat, deeper than the tee's: with no sleeves,
  its front hangs from the neckband. `vest_tee` is cut 1.5 cm higher at the front (6.5 cm deep), which matches the tee.
  The tee's own crew dips a little at the front too; compare against it, not a perfect circle.
- **Layers over make3Dcore's shapes**: a draped layer over a knitted vest needs 8 mm more room (`innerCols`). A shirt
  or polo under a hoodie under a done-up stand collar keeps `make3Dcore`'s shapes. A top is draped only when
  everything over it is draped too.
- **A photo print on the back** of a draped top follows `make3Dcore`'s rule: on a shirt or polo, only when it is a
  big print, and never on a shirt worn open. Some photo crops are a model's arm.
- **XPBD substeps in `drapeSettle`** were tried and rejected: slower, and the cloth stretched more.
- **A long coat needs its thighs and to hang.** Bound to his hips only, a coat's skirt was placed by triangles far
  away, and the page swung it in. Pushed out only where something is under it, it stood out over his seat and fell back
  in below. A garment over 90 cm is bound to his thighs too (`write_template`) and hung straight in the page
  (`drapeHang`).
- **A piece folded back faces in.** A collar leaf or lapel is cut facing out and folded over, so its normals point in
  toward him. The page uses normals to hold the layers under a garment inside it, so a lapel facing in pushed a shirt's
  collar out through it. Turn such a piece round on load (`drapeTurn`), as the blazer's is.
- **The word rules in `drapeArch`** are matched against the item name plus the outfit's `what`. A word in either can
  send a piece to the wrong branch: "softshell work jacket" matched the chore jacket's words. Survey after every rule
  change.
- **A template that opens must be marked open.** The 3D check counts an inner layer showing through from the front
  only under a piece done up; it reads that from the mesh's `userData.open`, set in `drapeTops` by a list of template
  names. A new template that opens (or whose V shows what is under it) goes in that list, or the check flags what is
  seen beside its open fronts.
- **Details drawn as patches follow the cloth only at their rows.** `drapeDetails`' `patch` lays a grid on the cloth,
  6 rows unless given more: a long strip (a cardigan's front rib) cuts through the curve between rows and the cloth
  stands out through it. Give a long strip a row every centimetre or so. A patch has no texture coordinates, so a print
  laid on one comes out a single colour: draw a pocket on a print as its outline instead.
- **A garment is not settled against itself.** `drapeSettle` holds each garment off his body and the layers under it,
  not off its own pieces. A collar leaf lying wide over its own shoulders (the aviator's) had the jacket's shoulders,
  pushed out over the tee, come up through it; the page lays such a leaf out over the rest of its jacket after the settle
  (by `drapeTops`' first settle). In the builder, give a big leaf `relax`'s `over` too (a leaf of 8 cm or more gets it),
  or it starts the drape inside the body and self-collision keeps it there.
- **The 3D check does not see through an open front.** It counts an inner layer showing through from the front only
  under a piece done up (`openC` in `check_3d.js`), so an overshirt or a collar coming through an open jacket's fronts
  passes. Look at open layers close up, from the front and both three-quarter views, and measure them with
  `tools/qa/through.js`, before trusting a pass.
- **Two jacket-weight layers from one pattern at one size have nowhere to go.** A shacket on `chore` under a chore
  jacket, both 122 cm round, came out through the jacket in pleats however the hold-in pass was tuned. `drapeTops` cuts
  a jacket-weight layer over another a size up (8 cm round), fills both layers' creases out, and holds the one under
  in by a ray toward his body (`DRAPEJW`, `drapeFill`, `drapePress`, `drapeUnder`), only where two are worn.
- **Three.js is 0.186.1, the module build**, loaded by `loadThree` from `THREE_URL` and copied onto `window.THREE`.
  Colour management is off (`ColorManagement.enabled=false`), so a colour is taken as given and only a texture marked
  `colorSpace=T.SRGBColorSpace` is decoded, as r128 drew them; a new texture from a photo or canvas needs that line.
  A light's intensity is ×π of what r128 took (`PI` in the stage lights). `PCFSoftShadowMap` is gone (`PCFShadowMap`).
  A shader patched at `normal_fragment_maps` has `nonPerturbedNormal`, not `geometryNormal` (declared later now).
  A QA script that renders flat colours must set `outputColorSpace=T.LinearSRGBColorSpace` (`check_3d.js`, `through.js`).
- **Measured cloth is noisy.** A small change to a settle moves every crumple, and one outfit's count can halve or
  double either way. Judge a change by totals over several outfits on all five bodies, not by one render.
