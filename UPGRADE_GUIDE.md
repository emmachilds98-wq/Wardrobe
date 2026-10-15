# Continuing the upgrade: a guide for the next engineer

Written 15 Oct 2026, when work paused after PR #68. Read this first, then `STATUS.md` (what is happening now and the
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
- **Coverage**: 890 top pieces across the outfits are draped. Only 62 still use `make3Dcore`'s shapes, plus every top
  worn tucked in, which is never draped (`TUCK0`). Run `tools/qa/drape_survey.js` (below) for the live list.
- **Templates** (`DRAPEF` in `page.html`; `_up` is the same garment done up, and the plain name is worn open where it
  can open, per `DRAPEOPEN`):
  - Knits and tees: `tee`, `tee_ls`, `jumper`, `rollneck`, `halfzip`, `hoodie`, `kvest`, `vest`.
  - Shirts and polos: `shirt(_up)`, `sshirt(_up)`, `camp(_up)`, `polo`, `polo_ls`.
  - Jackets: `jacket(_up)` (the track jacket's cut), `jacket_hood(_up)`, `jacket_coll(_up)`, `bomber(_up)`,
    `chore(_up)`, `trucker(_up)`, `puffer(_up)`, `puffer_hood(_up)`, `parka(_up)`, `gilet`.
  - Accessories: `scarf`.
- **Which template a piece gets**: `drapeArch(p)` in `page.html` decides, from the piece's shape and the words in its
  item name and `what`. It returns `null` for anything a template would draw wrongly; that piece keeps `make3Dcore`'s
  shapes. Every rule there has a comment saying why.

## What is left, in a sensible order

| Item | Pieces (outfits) | What it needs |
| --- | --- | --- |
| Blazers and suits | 10 (15) | A template with lapels. See "Blazers: the idea parked" below. The biggest visible gain left. |
| Wool overcoats, car coat | 5 (6) | The blazer's lapels on a long coat (95 to 105 cm), once blazers work. |
| Other jackets | 13 (14) | Hooded wax, borg, sherpa-lined, faux leather with a shearling collar, padded ski, 3-in-1; and 4 whose cut is unknown from the name (Folk Zaki, Brakeburn Classic Navy, Patrick Finn, Napapijri Bisenzio): look at the shop photos before choosing a template. |
| Knitted, zip and rugby polos | 6 (9) | A knitted polo jumper could use `polo_ls` with the jumper's rib; a zip polo needs the half-zip's zip on the polo collar. |
| V-neck jumpers | 2 (2) | `jumper` with the `vneck` measure and the rib V that `drapeDetails` lays on `kvest`. Small. |
| Cardigans | 2 (4) | A buttoned knit, open: the `kvest` V with sleeves, its front in two. |
| Muscle, racer and mesh vests, vest tops | 3 (3) | Variants of `vest` (deeper armholes, a racer back). Low value. |
| Baseball henley, mock-neck tee | 2 (3) | Raglan sleeves are not in the builder; low value. |
| Tucked-in tops | many | Never draped (`TUCK0`): only with tailoring, a belt or a tie. A draped top would need its hem taken inside the trousers. Large job, modest gain. |
| Newer Three.js | | Queue item 6 in `STATUS.md` (r128 now). Emma said yes on 12 Oct. |

Also noticed, not fixed: on rv-black-smart the link chain is drawn as a straight bar across his neck, on `main` too.

### Blazers: the idea parked

Not shipped; tried for a few minutes before the pause, never rendered. The builder now has a `vneck` measure (the
front's neckline runs straight down to its point, `bodice`), and `camp_up` showed that a shirt collar (stand plus
folded leaf) sewn round a V neckline lies open down both sides of the V like a small lapel. So a first blazer could be:
the jacket's body (about 112 cm round the chest, 76 long), `vneck` with `neck_f` about 30 (to the top button at his
waist), `collar=3, leaf=5.5, point=9`, `open=1` for worn open and a `blazer_up` without it. That gives a **shawl
lapel** (no notch), which may be close enough on screen. Then render it and check whether the leaf lies flat on the
chest or stands up. The placement in `close_seams` drops a leaf "down and out" from the ring's centre, which is right
at the back of the neck but not low on the chest, where a lapel should fall sideways. A notched lapel would need a
lapel piece of its own sewn along the V and placed folded back. `make3Dcore`'s blazer has much behaviour to keep
(done up at the waist, the shirt and tie in the V: `vDone`, `fitTop`'s `gapAt`, `upperArt`); read those first.

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
- **The word rules in `drapeArch`** are matched against the item name plus the outfit's `what`. A word in either can
  send a piece to the wrong branch: "softshell work jacket" matched the chore jacket's words. Survey after every rule
  change.
