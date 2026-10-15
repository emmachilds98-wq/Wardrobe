# Continuing the upgrade: a guide for the next engineer

Written 15 Oct 2026, when work paused after PR #68; updated for the draped blazers, overcoats and remaining jackets. Read this first, then `STATUS.md` (what is happening now and the
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
- **Coverage**: 921 top pieces across the outfits are draped. Only 31 still use `make3Dcore`'s shapes, plus every top
  worn tucked in, which is never draped (`TUCK0`). Run `tools/qa/drape_survey.js` (below) for the live list.
- **Templates** (`DRAPEF` in `page.html`; `_up` is the same garment done up, and the plain name is worn open where it
  can open, per `DRAPEOPEN`):
  - Knits and tees: `tee`, `tee_ls`, `jumper`, `rollneck`, `halfzip`, `hoodie`, `kvest`, `vest`.
  - Shirts and polos: `shirt(_up)`, `sshirt(_up)`, `camp(_up)`, `polo`, `polo_ls`.
  - Jackets: `jacket(_up)` (the track jacket's cut), `jacket_hood(_up)`, `jacket_coll(_up)`, `bomber(_up)`,
    `chore(_up)`, `trucker(_up)`, `puffer(_up)`, `puffer_hood(_up)`, `parka(_up)`, `gilet`.
  - Tailoring: `blazer(_up)` (a shawl collar: the collar and lapels in one, rolled down the V to the button).
  - Coats: `overcoat(_up)` (the blazer's lapels on a coat to his knees), `carcoat(_up)` (a shirt collar, a fly front).
  - Accessories: `scarf`.
- **Which template a piece gets**: `drapeArch(p)` in `page.html` decides, from the piece's shape and the words in its
  item name and `what`. It returns `null` for anything a template would draw wrongly; that piece keeps `make3Dcore`'s
  shapes. Every rule there has a comment saying why.

## What is left, in a sensible order

| Item | Pieces (outfits) | What it needs |
| --- | --- | --- |
| Knitted, zip and rugby polos | 6 (9) | A knitted polo jumper could use `polo_ls` with the jumper's rib; a zip polo needs the half-zip's zip on the polo collar. The biggest visible gain left. |
| Last jackets | 4 (6) | A hooded padded gilet (a `gilet` with `puffer_hood`'s hood), a faux-leather aviator with a shearling collar (a big contrast collar), and two that failed the check once draped: the borg zip-through over a half-zip done up (g-casual-01, its collar) and Carhartt's Super Dux (jb8-superdux, the jumper under it bunched over his tool belt). |
| Shirt-collared overcoat | (1) | The ASOS tobacco overcoat has a shirt collar in its photo but takes `overcoat`'s lapels (nothing in its name says otherwise): a `collar` correction in `data/fixes.json` could send it to `carcoat`. |
| V-neck jumpers | 2 (2) | `jumper` with the `vneck` measure and the rib V that `drapeDetails` lays on `kvest`. Small. |
| Cardigans | 2 (4) | A buttoned knit, open: the `kvest` V with sleeves, its front in two. |
| Muscle, racer and mesh vests, vest tops | 3 (3) | Variants of `vest` (deeper armholes, a racer back). Low value. |
| Baseball henley, mock-neck tee | 2 (3) | Raglan sleeves are not in the builder; low value. |
| Tucked-in tops | many | Never draped (`TUCK0`): only with tailoring, a belt or a tie. A draped top would need its hem taken inside the trousers. Large job, modest gain. |
| Newer Three.js | | Queue item 6 in `STATUS.md` (r128 now). Emma said yes on 12 Oct. |

Also noticed, not fixed: on rv-black-smart the link chain is drawn as a straight bar across his neck, on `main` too.

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
