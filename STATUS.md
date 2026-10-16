# Working status: read this first

**Paused 15 Oct 2026 after PR #68. The next engineer starts with [`UPGRADE_GUIDE.md`](UPGRADE_GUIDE.md):** where the
upgrade stands, what is left in order, how to add a template, how to check outfits on the five bodies, and the pitfalls.

The live working file for whoever picks up the wardrobe upgrade next (an agent or Emma). It says what is being
worked on right now, what comes next, and how to ship. Keep it current: update **Now** when you start or stop
something, tick the queue as items merge, and add a line to the **Log** every time `main` and the artifact change.
The long history and the reasons behind each rule are in `UPGRADE_PLAN.md`; how the code fits together is in
`HANDOFF.md`; the checks are in `CONTRIBUTING.md`.

- Live page (GitHub Pages, served from `main`): <https://emmachilds98-wq.github.io/Wardrobe/>
- claude.ai artifact (holds the shared database): <https://claude.ai/artifact/8uqcGr2eNmzbQv8UVBshY2>
- Emma's own copy of the artifact (republished from `docs/` the same way, its own database):
  <https://claude.ai/artifact/FtdHKgXdaBGrVmpbVYTrLn>. A session signed in to her account can only publish to this one.
  **Since 14 Oct this is the one Wardrobe artifact Emma keeps and comments on: republish it after every merge to `main`**
  (page `docs/index.html`, root `docs`, only the `docs/data` files that changed in `files`, no `capabilities`). She asked
  for the other copies to go; 8uqcGr2, B8UXnh and 5A3t39 belong to other accounts, so only their owners can delete them.
- Review and plan doc (Claude Doc): <https://claude.ai/code/artifact/a11be046-83a3-47dc-855c-67657c180e7e>
- From the drape session (this account's own artifact, no shared database: shortlist and Edit Dave save on the device):
  the GitHub build as it stands, published as `docs/` is (page `index.html`, the changed files under `data/` in
  `files`, root `docs`, no `capabilities`): <https://claude.ai/artifact/B8UXnhceKPAsHpTbyzFzek>. Since 14 Oct there is
  one version (draped clothes only, no switch, no preview build): the old drape preview
  (<https://claude.ai/artifact/5A3t39MwR6C9T5rHNED2iT>) carries the same build until the owner deletes it.

## Now

**16 Oct: skin tone on a slider, and more colours** (UPGRADE_PLAN SECN, section 5 item 2, its first half). Edit
Dave's Skin and colouring tab has Tone (very fair to very deep, through real skin tones, every step looking as big as
the next) and Undertone (cool and pink to olive) under a row of quick swatches, and eleven eye colours; his hair can be
black, brown, red or blond, with a Shade and a Grey slider. Each colour slider shows its colours on its track. Saved
looks load as they were. **Next:** the panel's layout (item 2's second half, for Emma to look at before it ships).

**16 Oct: a clear jawline** (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz, section 5 item 1). His face no longer runs softly into his
neck: the body build takes MakeHuman's fold of fat under the chin out, a little fat out of the face and squares the
angle of the jaw below the ear, moving only the face below the eyes (every body measurement below it is unchanged).
Edit Dave's Face tab has "Jawline" and "Under the chin". **Next:** item 2, skin tone on a slider and a tidier Edit Dave.

**16 Oct: ways back** (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz). No more dead ends: the fitting room closes again with Back and its
own buttons once its 3D model has run, and Edit Dave closes at all (a stale line in `Live3D`'s stop threw first); Back
closes Edit Dave and Compare; Edit Dave asks before dropping changes not saved; Compare has a way out on a phone; the
title goes to the start. A new check, `tools/qa/nav.js`, walks every view and dialog on a desktop and a phone screen
and runs on every pull request.

**16 Oct: the plan for the model from here** (UPGRADE_PLAN section 5). What is left on the 3D model, in order, with how
to tackle each item and when it is done: a clear jawline without the double-chin shadow, skin tone on a slider and a
tidier Edit Dave with more options, the shoes and how trouser hems meet them, a relaxed stance, tucked-in tops (a first
try is under way), draped trousers and shorts, then the remaining tops, the 3D check, fabrics, sizing and speed.
(Item 1, his jawline, is done: above.)

**16 Oct: Three.js 0.186.1** (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz). The page moved from r128 to the current release, the
module build from cdnjs, with colours, lights and shadows set to draw as before: card stills match `main`, and the
3D check reads the same numbers on 40 outfits compared. Every QA script loads it (`THREE_JS` is now a folder).
The insulated overshirts were tried once more with a thicker gap and held back.

**15 Oct: an open overshirt held inside an open jacket** (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz). The shacket came through the
jacket in g-mod-15, -11, -13 and g-casual-09 because the jacket was cut no bigger than the shacket. Where two draped
jacket-weight layers are worn, the one over is now cut a size up, both have their creases filled out, and the one under
is held under by a ray toward his body (83% less showing through, measured with a new tool, `tools/qa/through.js`).
The insulated and borg overshirts were tried again on `chore` and held back.

**15 Oct: a sleeveless tee, a mock-neck tee and the henleys** (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz). New templates, `vest_tee` (a
sleeveless tee: the tee's crew neck, no sleeves, deep armholes) for a vest top and a training tank, and `tee_mock` (a
long-sleeved tee with a mock neck); ASOS's mesh muscle vest on `vest`, HUF's baseball henley on `tee` with its placket
(6 pieces, 6 outfits). Draped top pieces 946, 6 left.

**15 Oct: two tries that did not ship** (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz). An open overshirt under an open jacket was
measured and four fixes tried; none held it in, and the diagnosis is written up. The ASOS tobacco overcoat was sent to
`carcoat` by a collar correction and taken back: worn open, `carcoat`'s collar hardly shows.

**15 Oct: collars inside open collared jackets** (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz). A shirt's or a polo's collar now sits
inside an open chore, denim, Harrington-style, car coat or aviator collar instead of crumpling over it (13 outfits
look better, 20 checked). The insulated and borg-lined overshirts were tried on `chore` and held back: under their jackets they show through, as open
overshirts under open jackets already do on `main` (g-casual-09, g-mod-11, -13, -15), which the 3D check misses.

**15 Oct: the last jackets** (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz). New templates, `gilet_hood` (a hooded gilet) and
`aviator` and `aviator_up` (a big shearling collar in its own colour); a borg zip-through on `puffer`, and a hybrid and a
longline waterproof filed as jackets on `jacket` and `parka` (6 outfits). Carhartt's Super Dux stays on `make3Dcore`.

**15 Oct: cardigans and a knit zip overshirt** (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz). A new template, `cardigan` and
`cardigan_up` (`jumper_v`'s knit with its front in two, rib up the fronts and round the V, buttons and pockets drawn),
and Closure London's knit zip overshirt on `chore` with a drawn zip (3 outfits).

**15 Oct: knitted, zip and rugby polos and V-neck jumpers** (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz). Zip polos on
`polo` with a drawn zip, knitted polo jumpers and a rugby shirt on `polo_ls`, and a new template, `jumper_v` (a V neck
with the knitted vest's rib; 11 outfits).

**15 Oct: the remaining jackets on their templates** (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz). 8 jackets whose shop
photos match a template (two shirt-jackets on `chore`, three stand-collar zip jackets on `jacket`, a hooded wax jacket
and a 3-in-1 on `jacket_hood`, a padded ski jacket on `puffer_hood`; 12 outfits).

**15 Oct: draped overcoats and a car coat** (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz). New templates, `overcoat` and
`overcoat_up` (the blazer's lapels on a coat to his knees) and `carcoat` and `carcoat_up` (a shirt collar, a fly front);
a coat over 90 cm is bound to his thighs too and hangs straight in the page (6 outfits).

**15 Oct: draped blazers** (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz). New templates, `blazer` and `blazer_up`: a tailored
jacket with a shawl collar, its collar and lapels one piece folded back over a stand that runs down the V to the button
(13 outfits; worn open or buttoned).

**15 Oct: softshell, shell, wax and wool-look jackets** (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz). Softshells and shells on
the track jacket's template, wax, Isthmus and button-up jackets on `chore`, a blouson on `jacket_coll` (9 outfits).

**15 Oct: draped resort shirts** (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz). New templates, `camp` and `camp_up`: a boxier
short-sleeved shirt with a camp collar lying open (in a V to the top button done up). 5 outfits; they had no collar before.

**15 Oct: draped knitted vests** (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz). A new template, `kvest`: no sleeves, a V neck with a rib
laid round it, the jumper's rib hem (6 outfits).

**15 Oct: draped vests (tank tops)** (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz). A new template, `vest`: a tank's 5 cm straps, a wide
scoop and deep armholes. Plain tanks are draped (3 outfits); muscle, racer, training and vest-top cuts keep
`make3Dcore`'s shapes.

**15 Oct: draped long-sleeved polos** (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz). A new template, `polo_ls` (8 outfits).

**15 Oct: more jackets on the templates they are cut like** (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz). A Carhartt Detroit on
`trucker`, workwear and wool fleece jackets on `chore`, zip microfleeces and smart zip jackets on the track jacket's
(12 outfits); a layer is held 8 mm further off a knitted vest.

**15 Oct: draped shackets** (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz). A jacket-weight overshirt (a shacket in
canvas, nylon or wool) is draped from the chore jacket's template (12 outfits). Insulated, padded and borg-lined ones
keep `make3Dcore`'s shapes.
**Next:** tucked-in shirts, the other jackets (38 outfits), jumpers (30), tees (24).

**14 Oct: draped short-sleeved shirts** (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz). New templates, `sshirt` and `sshirt_up`:
the shirt's cut and point collar, 76 cm long, 24 cm sleeves with a 2.5 cm turned band. 33 outfits are draped; camp,
Cuban, resort and bowling collars keep `make3Dcore`'s shapes. A draped shirt's back print follows `make3Dcore`'s rule
(a photo crop of a model's arm had lain on the back of an open shirt), and a shirt under a hoodie under a done-up stand
collar keeps `make3Dcore`'s shapes. The 33 outfits are clean as worn on all five bodies and done up on dave and loose.

**14 Oct: draped polos** (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz). A new template, `polo`: the tee's body, rib armbands, a knitted
collar closed round his neck and a two-button placket. Short-sleeved polos are draped (89 outfits have a polo). A
shirt's or polo's collar under a zipped-up Harrington or coach jacket no longer comes through the jacket's collar.
The 89 polo outfits are clean as worn on all five bodies and done up on dave and loose (q13-coastal on heavier flags
as on `main`).

**14 Oct: XPBD substeps in `drapeSettle`, tried and not adopted** (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz). Split into 8
substeps of one pass, the settle was 11 to 32% slower and the cloth's edges stretched more (mean 6.1 to 6.6% against
3.9%); the hoodies and jackets hung lower and bunched at the hem. Nothing on the page changed.

**14 Oct: a hoodie's hood over an open track jacket's collar** (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz). Before the hood
settles, an open zip jacket's stand collar is folded down and pressed under the hood, so the hood lies over it. The
last four hoodie-under-jacket flags are gone (x11-ellesse, jb10-winter-kx3, jb9-ukd-softshell, st-daily).

**14 Oct: a hoodie's hood over a jacket's collar** (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz). The hood no longer settles
against a shirt collar worn over it: it lies over the collar, which is pressed in under it. A chore or denim jacket
over a hoodie is draped again (hoodie-chore, n4-ravon).
**Next:** the front poke on three softshell or track jackets over a hoodie (x11-ellesse, jb10-winter-kx3,
jb9-ukd-softshell, as on `main`), then XPBD substeps in `drapeSettle`.

**14 Oct: draped bombers** (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz). There are two new templates, `bomber` and `bomber_up`:
the track jacket's cut with a rib collar, cuffs and hem band. Five bombers (five outfits) are now draped. Clean on all
five bodies, as worn and done up.
**Next, in order:** a hoodie's hood over a collar (so a chore or denim jacket can drape over a hoodie), then XPBD
substeps in `drapeSettle`.

**14 Oct: draped chore and denim jackets** (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz). There are four new templates, `chore` and
`trucker`, each open or done up: buttoned, with a shirt collar, the page drawing their buttons and pockets. Eight
jackets (eight outfits) are now draped; over a hoodie they keep `make3Dcore`'s (the hood crumpled over the collar). A
bag's strap now lies over draped tops (it was hidden under them). Clean on all five bodies, as worn and done up.
**Next, in order:** bombers, then a hood over a collar (so a chore jacket can drape over a hoodie). Then XPBD substeps
in `drapeSettle`.

**14 Oct: draped parkas** (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz). There are two new templates, `parka`
and `parka_up`: a long, roomy hooded zip jacket (78 cm). Hooded coats (four, in five outfits) are now draped; other
coats keep `make3Dcore`'s. The hem holes by his hand were the check's: it now counts a draped sleeve as his arm
(`sleeveMask`), as it does `make3Dcore`'s, and the six athletic and done-up cases are clean. Clean on all five bodies.
**Next, in order:** denim, bomber, field and chore jackets. Then XPBD substeps in `drapeSettle`.

**14 Oct: draped hooded padded jackets** (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz). There are two new
templates, `puffer_hood` and `puffer_hood_up`: the padded jacket's cut with a padded hood. Eight jackets (14 outfits)
are now draped; under a neck warmer one keeps `make3Dcore`'s shapes. The 14 outfits and all 21 with a scarf are clean
on all five bodies, as worn and done up.
**Next, in order:** parkas (a `parka` template is built and clean on his shape: five outfits), then denim, bomber,
field and chore jackets, and the hem holes by his hand. Then XPBD substeps in `drapeSettle`.

**14 Oct: draped hooded and collared zip jackets** (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz). There are four
new templates: `jacket_hood` and `jacket_hood_up` (the track jacket's cut with a hood), and `jacket_coll` and
`jacket_coll_up` (a Harrington's shirt collar). 25 hooded jackets (32 outfits) and 12 collared ones (17 outfits) are
now draped. A hoodie's hood under a hooded jacket is left out, and a hooded jacket is held 7 mm off a padded shacket.
g-mod-27's Duck and Cover "hoodie" is a quarter-zip, and its poke of 110 is gone. On his shape the 50 outfits are
clean as worn; done up there is one new flag, g-quiet-24 (back holes 29). On athletic three outfits show back holes
at the hem by his left hand.
**Next, in order:** padded hooded jackets and parkas (`make3Dcore`'s still: 16 jackets), then denim, bomber, field and
chore jackets, and the hem holes by his hand. Then XPBD substeps in `drapeSettle`.

**14 Oct: hoods the names do not mention** (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz). 25 jackets whose shop photos show
a hood get a `hood` correction in `data/fixes.json` (read before the name by `hoodOn`), so they are drawn hooded and
kept off the draped track and puffer templates. A hoodie's hood under a hooded jacket lies inside the jacket's hood
(three outfits' back pokes gone), a hood under a neck warmer is tucked under it, p6-mx-breeze is slate grey rather
than black, and the Sealskinz tee filed as a coat is a tee (g-outdoor-11 leaves it out). Against `main`, of 84 outfits:
as worn 8 flagged to 5, done up 1 to 0, nothing newly flagged.
**Next, in order:** draped templates for a hooded zip jacket and a collared zip jacket (`tools/build_garments.py`), the
two kinds most of item 0.1's remaining zip jackets are, then XPBD substeps in `drapeSettle`.

**14 Oct: PR #48's red 3D check fixed; FtdHKg republished from `main`** (v48, PR #48's build; UPGRADE_PLAN
2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz). PR #48 merged with w20261006-casual-04 red done up (front poke 53): a short-sleeved
"Stan Ray S - S" shirt read as long-sleeved, its collar showing inside a zipped puffer's stand collar. "S - S" and "SS"
shirts are now short-sleeved, and a collar under a draped stand collar done up is only its foot (also clears three
gilet outfits' neck pokes).
**Next, in order:** hoods on jackets whose names do not say so (25 found by looking at all 143 jackets, coats and gilets
in outfits beside their photos; most of "the other zip jackets" below are hooded or collared, so the track jacket
template does not fit them), then the zip jackets that are left.

**13 Oct, night: draped padded and puffer jackets** (PR #47, UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzz). **Behind the
drape switch: with it off the live page is unchanged.** The next of item 0.1's outer layers (21 outfits blocked):
- *Two templates,* `puffer` (worn open) and `puffer_up` (zipped): the track jacket's cut with a padded jacket's room
  (132 cm round the chest, sleeves 48 round the bicep), a 7.5 cm stand collar, an elastic hem and cuffs, every piece a
  little stiffer for its padding (`pad`). Hooded padded jackets and parkas keep `make3Dcore`'s shapes (o7-ski-jacket).
- *Worn open over two layers* (a quarter-zip over a shirt), the shirt showed through the quarter-zip in the opening:
  the layer turned in to hold what is under it (`inCol`) now leaves out the open front's edges, and each point is
  drawn back to its binding moved out of what is under it (`drapeOut`), so the jacket's edge lies over the quarter-zip
  rather than between it and the shirt.
- Checked, switch on, against `main` switch on: of the 22, 4 flagged (`main` 0: nothing is draped under them there),
  the shirt's collar at a hoodie's neck on two, a tucked shirt at the lower back on one, an armhole fleck on one
  (UPGRADE_PLAN has each). On the gate set and 30 more draped outfits **g-outdoor-05's back poke 493 and q13-coastal's
  front poke are gone** (the move out of what is under it also keeps a draped top outside a jacket-weight layer
  `make3Dcore` builds under it), and g-outdoor-21's back poke 619 too; g-outdoor-05 is clean on four bodies (back
  poke 31 on loose, was 580). On heavier, the same four padded-jacket outfits flag. Switch off: the gate set clean,
  specs unchanged.
**Next, in order:** the other zip jackets (item 0.1: 21 outfits), then XPBD substeps in `drapeSettle` (UPGRADE_PLAN
2zzzzzzzzzzzzzzzzzzzzzzzzzz, research). Once PR #47 is merged, republish B8UXnh and 5A3t39 (the page and
`data/garments/puffer.json`, `puffer_up.json`), as in the entry below.

**13 Oct: this account's two artifacts are current** (B8UXnh v5, 5A3t39 v4): both republished from `main` at 51ff9ed
(PRs #37 to #45), with the page and the twelve `data` files that changed since PR #36 (four new garment templates,
`gilet`, `scarf`, `shirt` and `shirt_up`, seven `data/items` files and `data/photos/shirt-p1.json`); the 2D/3D smoke
test is clean on both. To republish next time: `Artifact read` each, Read the saved page in full, `diff` it against
the last build (B8UXnh: `docs/index.html` but its first line; 5A3t39: a `--drape` build of the same commit), then
publish only the changed files (`git diff --stat 51ff9ed HEAD -- docs`).

**13 Oct, late night: the draped scarf wound a turn and a half; draped tops held off a bigger belly** (PR #45,
UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzzzz). **Behind the drape switch: with it off the live page is unchanged.** Emma asked to
continue the upgrades in this file's order:
- *The scarf's knot is gone:* the template (`tools/build_garments.py --only scarf`, `SCARF_WRAP`) is wound a turn and a
  half, each end turning down over his shoulder (flat on his chest, the band folded on itself into a knot), in a band
  11 cm wide so the ends stay long (loop 1.08 m, ends 0.66 m between them). The loop is as far out as he and the jumper
  are all round his neck (rays at its height), higher at the sides, the band's lower half bent out over his shoulders
  just enough to clear them, and the drape stops at frame 40, where it has settled.
- *Behind his neck* it now lies round his neck as a cowl rather than standing off it as a flat collar; its top is as
  high as before (lower cost the ends 14 to 32 cm).
- *g-outdoor-05's "under 4" is clear on every body:* the scarf's push-out did move it clear of the draped jacket's
  collar tip, and the settle after it drew it back; the points moved are now held. The push also reaches the loop's
  lower edge behind and at the sides, and comes from the side at the sides of his neck.
- *The heavier belly skin is gone* (h10-surf, jb11-cheapest, lazy-sunday, q7-fairisle, m5-argyle, q8-morden): not short
  templates, as item 0 below read it, but the trousers' waistband facing in under the belly's overhang and pressing the
  tops into it (`innerCols` turned each layer away from the nearest point of his body; it now faces the way his body
  does there).
- Checked, switch on, against `main` switch on: the 7 scarf outfits on five bodies, the belly set on heavier (5 flagged
  on `main`, 0 now), the gate set and item 0's five more on his shape (31): what is left is g-outdoor-05's back poke
  (the padded shacket through the draped jacket's back, on `main` too) and m5-argyle's front poke 31 (as `main`).
  Switch off: the gate set clean, specs unchanged.
**Next, in order:** the other outer layers still blocking the drape (item 0.1 below: g-outdoor-05's shacket is one),
then XPBD substeps in `drapeSettle` (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzz, research). For the scarf, still open: a
`strip` design runs 44 cm from each foot, so with the shorter ends it reaches 6 to 16 cm into the loop (round the back
of his neck on g-quiet-30); real printed scarves do carry it on, so left.

**13 Oct, evening: Emma's nine comments on her artifact** (PR #42, UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzzz). Live
page changes, all checked: straight and relaxed legs no longer widen below the thigh (`BOTCUT`, and the hem's own
fullness no longer spreads up the shin as a cone); cuffed joggers gather into a rib cuff at the ankle; "SikSilk" is no
longer read as silk (satin); six `data/fixes.json` corrections (the Matalan jeans' colour; the Mountain Warehouse shirt's
photo, now its dark grey colourway, and its check; the Brakeburn board shorts' flowers; the Admiral sweatshirt's side
panels; the Lambretta polo's band of checks; the Saltrock tee's print); two `data/cuts.json` lines. New correction
fields: `print` and `at` (a chest print from a flat photo when the shop's photo is on a model), `back: false` and
`slv` with `place`. A general denim rule for the jeans was tried and reverted (it moved 6 other pairs further from their
photos): see the plan entry. Merged 13 Oct; FtdHKg republished from it (v46) and all nine threads answered and
resolved (none left open on the artifact).

**13 Oct, late: a draped scarf, behind the drape switch** (PR #41, UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzz). **With
the switch off the live page is unchanged.** A scarf template (`tools/build_garments.py --only scarf`,
`data/garments/scarf.json`: 180 x 14 cm, once round his neck, both ends down his front, draped in Blender over his body
and the draped jumper) drawn by `drapeTops` last of all with the switch on (`dScarf` in `make3Dcore`, `drapeScarf`),
1 cm off what is under it and pushed in front of thin details by rays; its ends wear the `strip` design, with fringes.
Switch-on check of the 7 draped-scarf outfits on five bodies: as `main` with the switch on, but g-outdoor-05 "under 4"
on his shape (one speck of collar). *Items 1 to 3 below were done on 13 Oct, late night (PR #45, the entry above): (c)
with an 11 cm band. Kept for what was tried.* **Next engineer, start here for the scarf:**
1. The crossing on his chest bunches into a knot: in `scarf_path` try the ends leaving the loop under it (a tuck) rather
   than over it, or a gentler twist where each end leaves the loop (`join`: more points, the band's width turning over
   10 cm); look at each try with `node tools/garment_view.js <debug>/scarf-draped.json out.png` before the page.
   *Tried 13 Oct, evening (scratch only, nothing committed; each run about 2 minutes once Blender is unpacked):*
   (a) the band turning gradually from flat on his chest to upright round his neck along a join 16 cm long, the ends
   hung apart (8 cm left, 6 cm right of the middle) rather than crossing: laid out it looks right, but draped the
   front of the loop slides down his chest and opens into a shawl, the ends spread to his shoulders: the crossing ends
   are what hold the loop's front up. (b) The same with the whole first turn's top edge held, not only behind his neck:
   worse, an end swings round behind his shoulder. (c) "Once around" as it is usually tied (the middle across the
   front of his neck, the ends crossed behind it and brought forward over his shoulders, a turn and a half): no knot,
   but a turn and a half of a 14 cm band round his collar uses most of the 180 cm, so the ends reach only his upper
   chest, and draped the loop spreads over his shoulders. Untried: (c) with a narrower band (a 28 cm scarf folded in
   three, or 180 x 20 folded once) and a loop held by friction only at the back; or keeping the crossing and hiding it
   under the loop (the tuck).
2. The loop stands high behind his neck (the pinned edge, `pins` in `drape_scarf`): try pinning lower on the loop, or
   releasing the pins for the last 20 frames.
3. g-outdoor-05 "under 4" (switch on, his shape): the jacket collar's tip between the scarf's outer layer and its edge
   folded in. Either lower `make3Dcore`'s stand collar under a draped scarf (as the half-zip's is lowered under a scarf)
   or skip the fold-in rows in the push (`drapeTops`, the scarf block).
4. Then the other outer layers still blocking the drape (item 0.1 below), and XPBD substeps in `drapeSettle`
   (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzz, research).
**Emma's artifact (FtdHKg) is current:** republished 13 Oct from `main` at 7eaf1b5 (v47: PR #43, the page only),
after v46 from 5dd07f9 (PR #42: the page, five `data/items/*.json` and `data/photos/shirt-p1.json`), as described
below.
**The shared artifact (8uqcGr2) is current:** republished 13 Oct from `main` at 37fc3c4 (v52: PRs #40 to #43, the
same build as GitHub Pages and FtdHKg v47), its database and downloads kept. It belongs to another account, and a
session signed in to Emma's cannot publish to it: only one signed in to the account that owns it can. The Artifact
tool asks for the live page to be Read line by line first (about 8,200 lines, about 350k tokens), and for every data
file being replaced to be read first too (`Artifact read` with `paths`). To republish next time: `Artifact read`
8uqcGr2, Read the saved page in full (offset/limit, about 250 to 450 lines a call), confirm
`diff <(git show 37fc3c4:docs/index.html) <saved page>` differs only in the first line (the artifact's wrapper), read
and `cmp` the data files that changed (`git diff --stat 37fc3c4 HEAD -- docs`) against 37fc3c4's, then publish
`docs/index.html` with `files` = only those (files left out are kept), root `docs`, **no `capabilities`** (that keeps
its database and downloads). Then the Log's artifact column.
How to run: `python3 tools/build_garments.py --only scarf --debug <dir>` (Blender 4.5 LTS downloads itself; through this
environment's proxy the download was cut off twice at about 347 of 378 MB: fetch it with `curl -C -` into
`~/.cache/wardrobe-blender`, check it with the published sha256, and untar it there), then
`python3 tools/build_site.py --out <dir>`, serve it (`tools/qa/serve.sh`) and render with
`QA_INIT='window.__drape=1' node tools/qa/zoom.js ...`; check with
`QA_INIT='window.__drape=1' node tools/check_3d.js --site <dir> --ids q7-fairisle,pub-lunch,q9-matagalpa,q8-morden,od-event,g-outdoor-05,g-quiet-30 --body <body>`
on all five bodies against the same on `main`.

**13 Oct, night: jackets and coats rest on his chest; scarves hang like scarves** (PR #40, UPGRADE_PLAN
2zzzzzzzzzzzzzzzzzzzzzzzzzz). Emma flagged "the odd 3D model that shows the chest with a protruding chest" and the
scarves. **Live page change** (not behind the drape switch):
- *The chest:* measured on all 582 outfits, jackets (148 outfits), coats, blazers and gowns stood 3.3 to 4.3 cm off his
  skin at the chest (median), against 1.0 to 1.4 for tees and jumpers: their room was measured from his body and never
  halved at the front, so an open jacket stood 2.5 to 3 cm off the jumper under it and domed out in front of his armpits.
  An outer layer that is not padded now gets half its room over the front of his chest and belly (`fitTop`'s `F.rest`),
  and an open front still reaches as far forward as what shows between its edges (so a tie or roll neck never stands
  proud of it from the side, the fault that sank PR #31's try).
- *Scarves:* the ends are long soft bands with a thickness and a fringe, lying on what he wears and hanging straight
  below his chest, coming out from under the loop; the loop's top edge rolls over and its front lower edge is smooth.
  New correction `strip` (a scarf's end cut from its flat-lay photo): the Pretty Green Rainsford and Urban Excess scarves
  wear their designs.
- **Research and what Emma could get us:** UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzz, last part. Next for the drape: a
  scarf template (settled last, over every layer), XPBD substeps in `drapeTops`, patterns from PyGarment.

**13 Oct, evening: gilets are draped** (PR #39, UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzz), behind the drape switch:
**with the switch off the live page is unchanged** (but for the fitting room's tie note below). Gilets were the outer
layer that kept most draped tops from being draped (35 outfits). A new template, `gilet`: a bodywarmer done up, no
sleeves, deep armholes, a 3 cm hem band and a stand collar, its zip and a work bodywarmer's pockets drawn on the cloth;
hooded, tailored and open gilets keep `make3Dcore`'s shapes. Two rules found on the way: a shirt's collar leaf now
stays inside a stand collar done up over it (gilet, zipped jacket, half-zip, roll neck), and a plain belt is under
every draped top (it came through the gilet at his waist). Switch-on 3D check of the 40 gilet outfits on his shape:
see item 0. **Decisions made 13 Oct (Emma: "make any decisions needed"):** a shirt worn with a tie stays tucked, and
the fitting room now says so (queue item 5); the drape switch stays off until the outer layers are draped and the
full switch-on check is clean on all five bodies; sizing stays as Emma set it (model's shape right, sizing adjustable);
reference photos of Dave stay out of the repo. **Next engineer, start at item 0.1.**

**13 Oct, later: shirts are draped** (PR #38, UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzz), behind the drape switch like
the rest of the drape: **with the switch off the live page is unchanged.** Two new templates, `shirt` (worn open) and
`shirt_up` (done up), with a point collar folded over its stand, buttoned cuffs, and the placket and buttons drawn on
the cloth. A top is draped only when everything worn over it is too; a shirt's collar leaf lies out over a crew
jumper; each draped layer is held inside the draped bodies over it. Switch-on 3D check, gate set plus five shirt
outfits on his shape: **28 of 30 clean** (the gate set alone was 19 of 30 before). What is left is listed in item 0
below. **Next engineer, start at item 0.1.**

**13 Oct: PR #33's and #34's work is back on `main`** (PR #37, UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzz). Both were
closed unmerged when the drape proof went in, and republishing Emma's artifact from `main` rolled their fixes back; Emma
chose to bring them back first. On `main` again: every pair's cut read from its shop photo (`data/cuts.json`), the arm
joint limit (`ARMSUM`), the seat, polo collars, necklines at the base of his neck, collars grown from their tops,
scarves that wrap his neck. Fixed on the way: a hoodie's hood laid over an open jacket (the jacket's neckline no
longer climbs the hood rim, and its collar is pressed down under the hood at the back), and the scarf check's
far-side hits. **Emma's artifact (FtdHKg) is republished from `main` after each merge.**

**12 Oct, late: the garment drape proof is built, behind a switch, and waits on Emma** (PR #36, UPGRADE_PLAN
2zzzzzzzzzzzzzzzzzz; the start in 2zzzzzzzzzzzzzzzzz). Emma's design handoff (`design/garment-drape/`, its `README.md`
is the plan) replaces how garments get their shape with patterns draped in Blender and settled in the page in wearing
order. **Her decisions:** yes to the newer Three.js and to Blender-made templates; proof first, behind a switch, then
report back; a few seconds of settle on first opening is fine; assume the model's current shape is right but make the
sizing adjustable. **Done:** `tools/build_garments.py` drapes the hoodie (with its hood), the quarter-zip and the
jacket cleanly on him and writes `data/garments/`; with `window.__drape` set the page draws those three kinds from the
templates (`drapeTops`). **Proof:** g-mod-27 with its hood over the open jacket is clearly better than `main` from every
angle on all five bodies; as a quarter-zip the shape is better but its zip is missing and a few flecks show at the back
of the jacket's armholes on the bigger bodies. **Without the switch the page is unchanged.**

**Next agent, start here (in this order):**

0. **The garment drape upgrade** (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzz has everything: what was found, the checks, the
   commands). Merged to `main` 12 Oct (PR #36), all of it behind the drape switch: **the live page is unchanged**;
   the drape preview artifact shows it with a Draped clothes switch. Seven templates in `data/garments/` (hoodie with
   its hood, quarter-zip, track jacket open and zipped up, jumper, roll neck, tee) built by `tools/build_garments.py`
   (headless Blender); drawn in the page by `drapeTops` (bound to his warped body, settled inner to outer), with front
   details, photo fronts, prints and `place` maps on the cloth, a Size row in the fitting room and Cloth fit.
   **Where the switch-on 3D check stands** (`QA_INIT='window.__drape=1' node tools/check_3d.js ...`, the gate set plus
   wk-lounge, barrel-chore, c6-denim, m5-argyle and cold-commute; 13 Oct, PR #38): **28 of 30 clean on his shape** (was
   19 of 30 on the gate set alone: every flag then was a draped tee or knit coming through a top `make3Dcore` built over
   it, now never drawn so). Still flagged, with the switch on only:
   - m5-argyle (a shirt under a crew jumper), front poke 32 to 49 on every body: the shirt's collar lying out over the
     jumper's neckband, which close up looks right; the four-sides rule reads the leaf beside his neck as enclosed by
     the jumper. Look before changing the check.
   - Done 13 Oct: q7-fairisle's "under" is clean with the switch on (PR #40's live scarf; with PR #41 the scarf is
     draped too).
   - Done 13 Oct, late night (PR #45): heavier belly skin under draped tees and knits (h10-surf, jb11-cheapest,
     lazy-sunday, q7-fairisle, m5-argyle). Not short templates: the trousers' waistband, under the overhang of the
     belly, faced in (`innerCols`) and pressed the tops into it. Clean on heavier.
   - wk-lounge on heavier and loose (back poke 44, holes 29 to 31): its long-sleeved tee is not draped (the tee
     template is short-sleeved) and comes through the draped shirt's back. A long-sleeved tee template fixes it.
   - **Gilets (PR #39), switch on, the 40 gilet outfits on his shape:** **29 of 40 clean** (15 flagged at first; the
     collar and belt rules in UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzz cleared four and roughly halved most of the rest;
     the 25 clean at first are still clean). Still flagged, with the switch on only:
     - 8 at the base of his neck, front poke 38 to 83 (errands, g-job-11, g-job-15, g-outdoor-01, g-outdoor-03,
       g-quiet-13, g-quiet-18, g-quiet-26): the top under it seen inside the gilet's stand collar. Close up a roll neck
       there looks right; a shirt's leaf held inside the collar is crumpled and shows. Look before changing the check:
       the four-sides rule reads anything inside a stand collar as enclosed by it.
     - g-outdoor-21, front poke 151 and back 619: a borg-lined overshirt (jacket-weight, built by `make3Dcore`) under
       the gilet comes through its back; it goes when jacket-weight overshirts are draped.
     - g-job-13 back poke 40 (small marks near the back hem) and g-quiet-29 back holes 29: not looked at yet.
   **Next, in order:**
   1. Drape the outer layers too, so nothing `make3Dcore` builds sits over draped cloth. **Shirts done 13 Oct** (PR #38,
      UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzz: `shirt` and `shirt_up`, a folded point collar, laid out over a jumper),
      and a top is draped only when everything over it is. **Gilets done 13 Oct** (PR #39, UPGRADE_PLAN
      2zzzzzzzzzzzzzzzzzzzzzzzzz). **Padded and puffer jackets done 13 Oct** (PR #47, UPGRADE_PLAN
      2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzz: `puffer` and `puffer_up`, open or zipped; hooded ones and parkas still
      `make3Dcore`'s). **Hooded and collared zip jackets done 14 Oct** (PR #52, UPGRADE_PLAN
      2zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz: `jacket_hood`, `jacket_coll`, each open or zipped). **Hooded padded jackets done
      14 Oct** (PR #53, `puffer_hood`). **Parkas done 14 Oct** (PR #54, `parka`). **Chore and denim jackets done 14 Oct** (PR #55, `chore`, `trucker`). **Bombers done 14 Oct** (PR #56, `bomber`). Next: a shirt tucked in (into the waistband), a coat (long,
      lapels), Harrington and denim jackets, an overshirt's patch pockets (a jacket-weight overshirt under a gilet is
      what is left on g-outdoor-21).
      Also: q7-fairisle's draped half-zip collar comes over PR #34's tighter scarf ("under" 14, switch on only). Each: `MEAS` and pattern pieces in `build_garments.py`, a run with `--debug`, a look with
      `garment_view.js`, then `DRAPEK`/`DRAPEF` and `drapeArch`'s cut test in `page.html`. Until then, an option is to
      drape a tee or knit only when nothing `make3Dcore` builds is worn over it.
   2. Done 14 Oct (PR #48): not a switch turned on but the switch gone. The owner's decision: one version, the draped
      clothes, no "As before" and no going back (`window.__drape` stays for the checks alone).
   3. Compact storage before many more kinds (uint16 positions: about 0.6 of the size), and load only the kinds an
      outfit uses.
   4. A size per piece in the fitting room (now one size for all draped tops).
   5. Separately, its own pull request: the page's armpit tear (`warpMan` moves arm and chest skin apart by up to
      1.7 cm; blend them as the builder's `Body.armW` does, clothes by the nearest skin's blend; full 3D check).
   - Building: `python3 tools/build_garments.py --only <kind> --debug <dir>` (Blender 4.5 LTS downloads itself, and
     MakeHuman's assets from GitHub, both reachable from a claude.ai cloud session; or
     `pip install bpy` and run the script with that Python), about 3 minutes a kind; `--reuse` re-drapes a hood alone.
     Rules learnt: every sewn piece faces outward (the build stops otherwise: mirror the piece), rib bands and cuffs are
     pieces of their own, the relax smooths without shrinking, the body is blended at the armpits.
   - Also, a small data pull request: g-mod-27's Duck and Cover top is a quarter-zip with no hood (the shop's feed
     says so), so its piece should be `halfzip`, and `descOf` reads "quarter-zip hoodie" as a full zip ("zip hood").
   - Frozen while this goes on (the drape replaces that code): queue items 9 and 10, contrast collars (scarves were
     reworked on 13 Oct at Emma's request; the drape's own scarf template is still the way on).
     Data, photo reading and the weekly refresh carry on.

**Still open from PR #34's notes** (how to look close up is below):
1. jb-wet-day (a hoodie's hood out over the waterproof jacket, back poke 82 to 142, red on `main` too, not among the
   pull-request check's outfits): the jacket's back shows through the top of the hood, so the hood's estimate of how
   far out the jacket sits (`eTop`, `hOut` in `make3Dcore`) is short there.
2. Done 13 Oct (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzz; Emma asked, so the scarf freeze was lifted for it): the
   scarf's ends, the loop's rolled top edge and smooth front, all 8 scarf outfits checked close up. Left: the loop
   flares over a high jacket collar at the sides (pub-lunch); a `strip` scarf's design is not carried round the loop.
3. Sweep every kind of top and collar, alone and layered, close up from the front, ¾, side and back, against its
   shop photo: tee, oversized tee, crew jumper, roll neck, half-zip, hoodie, cardigan, shirt done up and open, polo,
   short-sleeve shirt, overshirt, zip jacket, Harrington, denim/trucker, bomber, puffer, coat, blazer, gilet. Then the
   common layers: shirt under jumper, polo under half-zip, tee under open shirt or jacket, hoodie under jacket (hood
   laid out over its back), scarf over coat. Fix what does not look like real clothes. The owner wants every garment
   to sit on him as it does in real life, at every angle and in every combination: fix each problem at the rule that
   makes it, never per outfit, and never by raising a check limit. The passing 3D checks do not catch collar faults.
4. Contrast collars (the Harrington's brown cord collar) are not read from the photo yet.
How to look: `sh tools/qa/serve.sh <dir> <port>` serves a test copy; `node tools/qa/zoom.js out.png <outfit id or
pieces JSON> "rotY,camY,camZ,lookY;..."` renders close-ups (for the neck: "0,1.56,0.9,1.47;0.8,1.56,0.9,1.47;
1.57,1.56,0.9,1.47;3.14,1.6,0.9,1.47"); `tools/qa/card.js` renders the outfit-card stills. To test a rule, copy the
built site, patch its `index.html` with a small script, serve it on its own port, and compare against main. Run
`node tools/check_3d.js --site docs --ids <ids> --body dave` before pushing.

1. **Slim and baggy bottoms:** done 12 Oct (UPGRADE_PLAN 2zzzzzzzzzzzzzzzz to 2zzzzzzzzzzzzzzzzzzzzz): `bottomCut`
   reads every pair's cut for the model, the drawing and the fitting room's words, shorts' length from their inseam;
   every bottom in an outfit was checked against its shop photo and 166 set in `data/cuts.json`. New picks: add them
   there (CONTRIBUTING, "The cut of trousers and shorts"). The numbers are in `BOTCUT`.
2. **Edit Dave's extremes:** the short sleeves are done 12 Oct (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzz: `ARMSUM`). Still open:
   w20261006-casual-04 on a heavy, muscular build (weight 0.6, muscle 0.6, arms and legs 1), the hood's rim through
   the padded jacket's collar at the back of his neck (back poke 33; there before 12 Oct too; check it again after
   PR #37's hood fix). jb-wet-day is item 1 above. To test a body the page
   has no button for, copy `docs/` and add an entry to `PRESETS` in the copy's `index.html`, e.g. `xbase:{weight:0.6,
   muscle:0.6,arms:1,legs:1}`, then `node tools/check_3d.js --site <copy> --ids w20261006-casual-04 --body xbase`.
3. **One set of model controls** (queue item 4, done 13 Oct, PR #43). Found 12 Oct: the builder's small model uses `Live3D`'s own bar
   (`opt.bar`, `.v3-bar`, `data-v3`: Front, Side, Back, Turn, Full, Top, Face, Zip up), Edit Dave has its own Front,
   Side, Back (`.ce-bot`, `data-ceang`), the fitting room the dock (`.fr-dock`, `data-frang`, `data-frcam`,
   `data-frspin`, lit in `frFrame`) and "How it's worn" (`frWearRows`, `frWear`). Plan: one function making the dock's
   markup, used by all three, each wired to its own `Live3D` (`turnTo`, `frameTo`, `spinning`, `framing`); the wear
   rows from `frWearRows` generalised to any wear object (`h.wear`). The page-wide click handler for `data-frang` only
   acts inside `#fr`, so a dock elsewhere needs its own handler.
4. The rest of the queue (5, 6, 8, 9, 10), and from earlier: folds on hats and a scarf's hanging ends; the light
   (`studioEnv`) tuned against shop photos; contact shade of a shirt collar on a jumper's neck and of a scarf; the
   Lambretta cap's stripe over the top to the back (the `crown` correction covers the front only).

Emma looks at the work in her copy of the artifact (FtdHKg) and leaves comments there; a session reads them with the
artifact comments tool (threads "sent to Claude"), acts, replies in the thread and resolves it.

If you stop part-way through something, write here: the branch, what is done, what is left, and anything you found
out that the next person needs. Push the branch, even unfinished, so the work is not lost when a session ends.

## Queue

In order. Each item is small enough for one pull request. Tick it and add a Log line when it merges.

1. [x] **Odd swaps in the fitting room.** Done 11 Oct: `guessShape` reads hats, caps, socks and gloves by their name
   before the shop's category; the build now stops on a hat filed under another category (`is_hat`), and
   `sweep_filter.category` knows a plain "hat" and files socks as basics.
2. [x] **A done-up blazer.** Done 11 Oct: buttoned at his waist, the shirt and tie in a V to the collar, lapels down
   to the button, fronts curving apart below it, his left front over his right; in 3D (`vDone`, `fitTop`'s
   `gapAt`) and 2D (`upperArt`). All 14 blazer outfits pass the 3D check done up and as worn.
3. [x] **Shirt collar and tie.** Done 11 Oct: the tie lies on the shirt itself (under a blazer done up too), its
   four-in-hand knot at his throat in the collar's notch (it hung 6 cm low, on his chest); the collar's points come
   down at the front and angle apart (`fold.spread`). Left: the blazer's own collar is still ragged at the sides of
   his neck.
4. [x] **One set of model controls.** Done 13 Oct (PR #43): the fitting room's camera dock (`camDock`) on every live
   model, the fitting room, Edit Dave (opened from the Fitting room fold) and the builder's small model, one handler
   for all of them, lit by `dockSync`; Edit Dave and the builder also get How it's worn as toggles in the dock (Done up,
   Tucked, Turned up: `dockWear`, from `wearRows`, the fitting room's rows for any wear). Compare keeps its own
   controls, which turn both models at once. The builder's model under 240 px wide (phones) has no dock, as it had
   no bar.
5. [x] **Untucked with a tie.** Decided 13 Oct: a shirt with a tie stays tucked (`tuckOn`, as a tie is worn); the
   fitting room's tuck row now shows only "Tucked", with the note "Worn with a tie, the shirt stays tucked in." (PR #39).
6. [x] **Newer Three.js.** Done 16 Oct: 0.186.1, the module build from cdnjs (`THREE_URL`, `loadThree`), colour
   management off so colours draw as under r128, `colorSpace` for textures and renderers, lights ×π, `PCFShadowMap`,
   the fold shader on `nonPerturbedNormal`. Card stills match `main` (mean brightness within 0.6 of 255); fine
   stripes blend a little lighter, as sRGB textures are now decoded before they are filtered.
7. [x] **Shoe lasts.** Done 11 Oct: a last per kind of shoe from its name (`lastK`, `LASTS`: dress, Chelsea,
   loafer, work and safety, hiking, boot, desert and chukka, skate) scaling the profile slice by slice; soles by kind
   (thin with a stacked heel, lugged, pale crepe); boot shafts by kind; a loafer's apron seam and penny strap or
   tassels; the upper on its own flat-based geometry with a rounded toe (`upperGeo`). Still to do: a real toe box and
   vamp (the upper is one smooth dome), a collar opening at the ankle, trainers' own panels.
8. [ ] **Fabric library.** Plan doc "Fabrics and photos": cord, waffle, fleece, quilting and denim as materials,
   not only colours.

9. [ ] (Frozen 12 Oct: the garment drape replaces this code.) **`od-event`: the scarf under a down jacket's shoulders** (check_3d "under 6"; on main before PR #25 too, and
   not in the gate set, so CI never saw it). Found 11 Oct: the rays hit the jacket's padded shoulders 16 to 20 cm out
   from his neck, 2 to 3 cm below the scarf's top; the scarf's lower edge is lifted onto the tops by at most 85% of its
   height (the `lifted` pass in the scarf code), so over a puffer it stays tucked under the padding. A scarf should
   drape over the shoulders there: let its lower edge flare out over them instead. (Measuring the outermost cloth over
   each ring's band of height, and widening the side allowance, did not fix it; reverted.)
10. [x] **Polo collars.** Done 12 Oct (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzz): its own folded rib band. The leaf lies flat on his shoulders with ragged edges and the stand is low; in the photos a
   polo collar is a distinct ribbed band round the neck, folded over. (Its tipping now lies on the leaf's edge: PR #27.)

11. [x] **Folds and creases in trousers** Done 12 Oct, for every garment (see UPGRADE_PLAN 2zzzzzzzzzzzz). (Emma, 12 Oct: "folds and creases as it sits on a body ... like the
   advertisements"). Shade them into the cloth: a height field over the garment's own texture coordinates (round the
   leg, metres up from the hem) added to the weave's bump in the shader (`onBeforeCompile`, replacing `dHdxy_fwd()` in
   `normal_fragment_maps`), so the geometry and the 3D check are unchanged. Tried on a scratch copy and it reads well:
   whiskers fanning from the crotch toward the hips, two or three slanting creases behind the knee, the break stacked
   over the shoe (off level, not rings), drag lines down the inside of the thigh, a soft smile under the seat, a pressed
   crease on tailored trousers, long vertical drape on wide legs. Amplitude about 4 mm, fold width 6 mm; seed each
   item so no two pairs fold alike. Check the `colour` count does not move.
12. [x] **Folds in tops.** Done 12 Oct (shader folds; the sleeve rings are gone). The same for tops: drag lines from the armpit, bunching inside the elbow and at the cuff,
   gathers above the waistband of a tucked shirt, and the side drape of a loose tee. The geometric `sleeveFolds` rings
   read as a spring; replace them.
13. [x] **Light that shows folds.** Done 12 Oct: `studioEnv` and `layerShade`. Soft studio light (a room environment through `PMREMGenerator`) and contact shade
   between layers, so folds read as they do in the shop photos.

Needs Emma (do not guess):
- The model's chest measures about 34in on his saved shape, which says S/M tops, while he buys L. Is his saved shape
  or the measurement off? (12 Oct: she said to take the model's shape as right and make the sizing adjustable. Note
  that `ceMeasure` may read 2 to 3% low: it scales by his height only, not by the 1.036 the page scales him by after
  his proportions; UPGRADE_PLAN 2zzzzzzzzzzzzzzzzz.)

## How to ship (every change)

1. Branch from `main`. Edit `page.html` (or the tools). Build: `python3 tools/build_site.py --out docs`.
2. Check: `node tools/specs.js`, then the 3D gate:
   `node tools/check_3d.js --site docs --ids @tools/qa/gate.txt --out /tmp/c3d` (Three.js from cdnjs; if cdnjs is
   blocked, `npm pack three@0.128.0` and set `THREE_JS` to its `build/three.min.js`, see `CONTRIBUTING.md`).
   Never raise a check limit to make something pass; fix the cause.
3. Commit with `docs/`, push, open a draft PR. When CI is green, mark it ready and merge with the full 40-character
   head SHA.
4. Republish the artifact from `docs/`: page `docs/index.html`, plus every file under `docs/data/` passed in `files`
   by its path relative to `docs/` (root `docs`). Never pass `capabilities` (that keeps the database). The artifact
   tool first asks you to read the live version in full: it is the previous `docs/index.html` with a one-line
   wrapper, so check that with `diff` against the last merged build, then publish.
5. Pages deploys `main` by itself; check the "pages build and deployment" run for the merge commit succeeded.
   **Emma, 12 Oct: whenever a change goes live on GitHub, update the artifact too**, in the same session: the artifact
   this account can publish to is <https://claude.ai/artifact/B8UXnhceKPAsHpTbyzFzek> (the GitHub build: `docs/`
   exactly, page `index.html`, every file under `docs/data/` in `files`, root `docs`, no `capabilities`), and the drape
   preview <https://claude.ai/artifact/5A3t39MwR6C9T5rHNED2iT> (`build_site.py --out <dir> --drape`). A session signed
   in to Emma's own account republishes FtdHKg as in step 4.
6. Update this file (Now, Queue, Log), add an entry to `UPGRADE_PLAN.md` for anything substantial, and the Status
   column in the plan doc.

Rules that never change are in `HANDOFF.md` ("Rules that never change"): his sizes and taste, no third-party relays
for shop requests, no photos of Dave in this repo, no model names in commits, PRs or code.

## Log

Newest first. Date · PR · what changed · artifact version.

| Date | PR | What | Artifact |
| --- | --- | --- | --- |
| 16 Oct 2026 | #PRN | Skin tone on two sliders (Tone through eleven real skin tones spaced evenly in OKLab, Undertone from cool to olive; `CHAR.skin` is still the colour, so saved looks load as they were), hair colours beyond brown (black, red, blond, and a Grey slider; his browns with no grey are the same colours as before), eleven eye colours; colour sliders show their colours on the track | FtdHKg vNEXT |
| 16 Oct 2026 | none | FtdHKg republished from `main` (8d918c3, PR #82's build: the page and 15 `docs/data` files changed since 0382659, the build it had) | FtdHKg v67 |
| 16 Oct 2026 | #82 | A clear jawline: the base body takes MakeHuman's `neck-double-decr` 1, `head-fat-decr` 0.65, `head-square` 0.55 and `chin-bones` 0.45, the jaw targets limited to the face below the eyes (`LOWER_FACE`, so the crown and the whole body's scale stay put); Edit Dave's "Jawline" and "Under the chin" (new morphs, last); FtdHKg still to be republished from Emma's account | B8UXnh v19 |
| 16 Oct 2026 | #81 | Ways back: the fitting room closes with Back and its buttons once its 3D model has run, and Edit Dave closes (a stale `bar` line in `Live3D`'s stop threw first); Edit Dave and Compare are steps in history (`dlgPush` / `dlgPop`); Edit Dave asks before dropping changes; Compare's header and a ‹ back on a phone; the title links to Shop; `tools/qa/nav.js` and its pull-request job; FtdHKg still to be republished from Emma's account | B8UXnh v18 |
| 16 Oct 2026 | #79 | Three.js r128 → 0.186.1 (the module build from cdnjs): colour management off, `colorSpace` for textures and renderers, lights ×π, `PCFShadowMap`, the fold shader's normal; QA scripts and the 3D check updated (`THREE_JS` is a folder now). Card stills match `main`. The insulated overshirts tried again with a thicker gap and held back. FtdHKg still to be republished from Emma's account | B8UXnh v17 |
| 15 Oct 2026 | #78 | An open overshirt held inside an open jacket: where two draped jacket-weight layers are worn, the one over is cut a size up, both have their creases filled out, and the one under is held under it by a ray toward his body (g-mod-15, -11, -13, g-casual-09; 83% less showing through over the four on five bodies). New `tools/qa/through.js` measures a layer showing through an open front. The insulated and borg overshirts tried again and held back. FtdHKg still to be republished from Emma's account | B8UXnh v16 |
| 15 Oct 2026 | #77 | A sleeveless tee, a mock-neck tee and the henleys: new `vest_tee` (the tee's crew neck, no sleeves, deep armholes) for Volcom's vest top and 4505's training tank, new `tee_mock` (`tee_ls` with a mock neck) for Uniqlo's, ASOS's mesh muscle vest on `vest`, HUF's baseball henley on `tee` with its placket (6 pieces, 6 outfits); draped top pieces 946, 6 left. FtdHKg still to be republished from Emma's account | B8UXnh v15 |
| 15 Oct 2026 | #75 | A shirt's or a polo's collar sits inside an open chore, denim, Harrington-style, car coat or aviator collar instead of crumpling over it (`leafIn`; 20 outfits checked, 13 better). The insulated and borg-lined overshirts were tried on `chore` and held back: open overshirts under open jackets show through them, on `main` too, which the 3D check misses. FtdHKg still to be republished from Emma's account | B8UXnh v14 |
| 15 Oct 2026 | #74 | The last jackets: a new `gilet_hood` (a hooded gilet) and `aviator` and `aviator_up` (a big shearling collar in its own colour, laid out over its own shoulders), a borg zip-through on `puffer` (not over a half-zip), and a hybrid and a longline waterproof filed as jackets on `jacket` and `parka` (7 uses, 6 outfits; Carhartt's Super Dux stays on `make3Dcore`); draped top pieces 940, 12 left. FtdHKg still to be republished from Emma's account | B8UXnh v13 |
| 15 Oct 2026 | #73 | Cardigans and a knit zip overshirt: a new `cardigan` and `cardigan_up` (`jumper_v`'s knit with its front in two, rib up the fronts and round the V, buttons and pockets drawn) for Route One's cardigan, and Closure London's knit zip overshirt on `chore` with a drawn zip (3 pieces, 3 outfits); draped top pieces 934, 18 left, counted piece by piece. FtdHKg still to be republished from Emma's account | B8UXnh v12 |
| 15 Oct 2026 | #72 | Knitted, zip and rugby polos and V-neck jumpers: zip polos on `polo` with a drawn zip, knitted polo jumpers and a rugby shirt on `polo_ls`, a new `jumper_v` (a V neck with the knitted vest's rib; 8 pieces, 11 outfits). FtdHKg still to be republished from Emma's account | B8UXnh v11 |
| 15 Oct 2026 | #71 | The remaining jackets whose shop photos match a template: two shirt-jackets on `chore`, Brakeburn Classic, Napapijri Bisenzio and Closure London's hybrid on `jacket`, a hooded wax jacket and a 3-in-1 on `jacket_hood`, a padded ski jacket on `puffer_hood` (8 jackets, 12 outfits). FtdHKg still to be republished from Emma's account | B8UXnh v10 |
| 15 Oct 2026 | #70 | Draped overcoats and a car coat (`overcoat`, `overcoat_up`: the blazer's lapels on a coat to his knees; `carcoat`, `carcoat_up`: a shirt collar, a fly front; 6 outfits); a coat over 90 cm bound to his thighs too and hung straight in the page; the blazer's lapel line drawn in front only. FtdHKg still to be republished from Emma's account | B8UXnh v9 |
| 15 Oct 2026 | #69 | Draped blazers (`blazer`, `blazer_up`: a shawl collar, its collar and lapels one piece folded back over a stand that runs down the V to the button; 13 outfits); a shirt's collar kept inside a blazer. FtdHKg still to be republished from Emma's account | B8UXnh v8 |
| 15 Oct 2026 | none | This account's B8UXnh republished from `main` (0382659, PR #68's build: the page and the 41 `docs/data` files changed since e8a471f). FtdHKg cannot be reached from this account | B8UXnh v7 |
| 15 Oct 2026 | #68 | Softshell and shell jackets on the track jacket's template, wax, Isthmus and button-up jackets on `chore`, a blouson on `jacket_coll` (9 outfits); `UPGRADE_GUIDE.md` for the next engineer | FtdHKg v66 |
| 15 Oct 2026 | #67 | Draped resort shirts (`camp`, `camp_up`: a camp collar lying open; 5 outfits) | FtdHKg v65 |
| 15 Oct 2026 | #66 | Draped knitted vests (`kvest`: a V neck, its rib laid round the V; 6 outfits) | FtdHKg v64 |
| 15 Oct 2026 | #65 | Draped vests (`vest`: a tank top's straps, scoop and armholes; 3 outfits); notes for #63 and #64 | FtdHKg v63 |
| 15 Oct 2026 | #64 | Draped long-sleeved polos (`polo_ls`; 8 outfits) | FtdHKg v62 |
| 15 Oct 2026 | #63 | More jackets on their templates (Detroit, workwear, wool fleece, zip microfleece, smart zip; 12 outfits); a layer held 8 mm off a knitted vest | FtdHKg v61 |
| 15 Oct 2026 | #62 | Shackets draped from the chore jacket template (12 outfits); notes for #61 | FtdHKg v60 |
| 15 Oct 2026 | #61 | Draped short-sleeved shirts (`sshirt`, `sshirt_up`; 33 outfits); a draped shirt's back print as `make3Dcore`'s | FtdHKg v59 |
| 14 Oct 2026 | #60 | Draped polos (`polo`: rib collar and armbands, two-button placket); a collar leaf held inside a done-up Harrington's stand, not its leaf | FtdHKg v58 |
| 14 Oct 2026 | #59 | Notes: XPBD substeps tried, not adopted (page unchanged) | (no change) |
| 14 Oct 2026 | #58 | A hoodie's hood lies over an open zip jacket's stand collar (folded down and pressed under it); the last 4 hoodie-under-jacket flags fixed | FtdHKg v57 |
| 14 Oct 2026 | #57 | A hoodie's hood lies over a jacket's shirt collar (the collar pressed in under it); a chore or denim jacket over a hoodie is draped again (2 outfits) | FtdHKg v56 |
| 14 Oct 2026 | #56 | Draped bombers (`bomber`, `bomber_up`: rib collar, cuffs and hem band; 5 bombers, 5 outfits) | FtdHKg v55 |
| 14 Oct 2026 | #55 | Draped chore and denim jackets (`chore`, `trucker`, each open or done up: 8 jackets, 8 outfits; over a hoodie `make3Dcore`'s); a bag's strap laid over draped tops | FtdHKg v54 |
| 14 Oct 2026 | #54 | Draped parkas (`parka`, `parka_up`: 4 hooded coats, 5 outfits); other coats keep `make3Dcore`'s | FtdHKg v53 |
| 14 Oct 2026 | #53 | Draped hooded padded jackets (`puffer_hood`, `puffer_hood_up`: 8 jackets, 14 outfits); one under a neck warmer keeps `make3Dcore`'s; held 14 mm off the draped layers under it and 12 mm off an overshirt | FtdHKg v52 |
| 14 Oct 2026 | #52 | Draped hooded zip jackets (`jacket_hood`, `jacket_hood_up`: 25 jackets, 32 outfits) and collared zip jackets (`jacket_coll`, `jacket_coll_up`: Harrington, coach, Capitol, Eisenhower; 12 jackets, 17 outfits); a hoodie's hood left out under a hooded jacket; g-mod-27's quarter-zip no longer a hoodie (front poke 110 gone) | FtdHKg v51 |
| 14 Oct 2026 | #51 | `hood` corrections for 25 jackets hooded in their photos (drawn hooded, off the track and puffer templates); a hoodie's hood under a hooded jacket inside its hood (jb-wet-day, jb8-wet-day, jb9-wet-dealer clean), a hood under a neck warmer tucked under it; p6-mx-breeze slate grey; the Sealskinz tee a tee | FtdHKg v50 |
| 14 Oct 2026 | #50 | "S - S" and "SS" shirts short-sleeved (23; three outfits' Stan Ray shirts now `sshirt`); a shirt's collar under a draped stand collar done up only its foot (w20261006-casual-04 done up, g-job-11, g-job-15, g-quiet-13 clean) | FtdHKg v49 |
| 14 Oct 2026 | none | FtdHKg republished from `main` (451852e, PR #48's build: draped clothes only), the page and four `data/garments` files; now the one artifact kept in step with `main` | FtdHKg v48 |
| 13 Oct 2026 | #47 | Behind the drape switch: padded and puffer jackets draped (`puffer` worn open, `puffer_up` zipped; hooded ones and parkas still `make3Dcore`'s); an open front's edges left out of the layer holding what is under it, and each draped point drawn back to its binding moved out of what is under it (g-outdoor-05's and q13-coastal's switch-on pokes gone); live page unchanged | not republished yet (B8UXnh v5, 5A3t39 v4 are on 51ff9ed) |
| 13 Oct 2026 | none | This account's artifacts republished from `main` (51ff9ed, PRs #37 to #45's build, as on GitHub Pages): B8UXnh the page and twelve `data` files (new garment templates `gilet`, `scarf`, `shirt`, `shirt_up`), 5A3t39 the same as a `--drape` build; 2D/3D smoke test clean on both | B8UXnh v5, 5A3t39 v4 |
| 13 Oct 2026 | #45 | Behind the drape switch: the draped scarf wound a turn and a half (no knot on his chest, a cowl behind his neck), g-outdoor-05's scarf clear on every body, draped tops held off a bigger belly (the waistband faced the way his body does); live page unchanged | B8UXnh v5, 5A3t39 v4 (row above) |
| 13 Oct 2026 | none | The shared-database artifact (8uqcGr2) republished from `main` (37fc3c4, PRs #40 to #43's build, as on GitHub Pages): the page, `data/garments/scarf.json` and eight `data/items` and `data/photos` files; 2D/3D smoke test clean | 8uqcGr2 v52 |
| 13 Oct 2026 | #43 | One set of model controls: the fitting room's camera dock (`camDock`) on Edit Dave and the builder's small model too, with How it's worn as toggles; the builder's old bar gone | FtdHKg v47 |
| 13 Oct 2026 | #42 | Emma's nine comments: straight and relaxed legs no longer widen below the thigh, cuffed joggers gather into a rib cuff, SikSilk no longer satin; six corrections (Matalan jeans' colour, the Holiday shirt's dark grey photo and check, board shorts' flowers, Admiral sweatshirt's panels, Lambretta polo's checks, Saltrock tee's print); new correction fields `print`/`at`, `back`, `slv` with `place` | FtdHKg v46 |
| 13 Oct 2026 | none | Emma's artifact (FtdHKg) republished from `main` (d4edbf9, PRs #39 to #41's build); 8uqcGr2 still on PR #39's | FtdHKg v45 |
| 13 Oct 2026 | #41 | A draped scarf behind the drape switch (`scarf` template, `drapeScarf`); live page unchanged | not republished (see below) |
| 13 Oct 2026 | #40 (merged) | Jackets, coats, blazers and gowns rest on his chest (`F.rest`, with an open front reaching as far forward as what shows between its edges); scarf ends as long fringed bands hanging from under the loop, the loop's top edge rolled and its front smooth; new correction `strip` (two scarves wear their designs) | not republished (see below) |
| 13 Oct 2026 | #39 | Gilets draped behind the switch (`gilet`: sleeveless, done up, stand collar, hem band; zip and work pockets on the cloth); a shirt's leaf stays inside a stand collar done up over it; belts under draped tops; the fitting room says a shirt with a tie stays tucked; live page otherwise unchanged | 8uqcGr2 v51 |
| 13 Oct 2026 | none | The shared-database artifact (8uqcGr2) republished from `main` (9c35b06, PR #38's build); five photo packs no longer in `docs/` removed from it | 8uqcGr2 v50 |
| 13 Oct 2026 | #38 | Shirts draped behind the switch (`shirt` open, `shirt_up` done up: a point collar folded over its stand, cuffs, placket and buttons); a top draped only when all over it is; a shirt's leaf out over a jumper; layers held in under the draped bodies over them; live page unchanged | FtdHKg v44 |
| 13 Oct 2026 | #37 | PR #33's and #34's work back on `main` (bottoms' cuts from their photos, `ARMSUM`, the seat, polo collars, necklines at the base of his neck, collars grown from their tops, scarves that wrap); a hood laid over an open jacket (the jacket's neckline no longer climbs the hood rim, its collar pressed down under the hood); the scarf check counts near-side hits only | FtdHKg v43 |
| 12 Oct 2026 | none | FtdHKg republished from `main` (e0bcb1d, PR #36's build, as on GitHub Pages), which rolled #33's and #34's fixes back on it until #37 | FtdHKg v42 |
| 12 Oct 2026 | #36 (merged) | Garment drape upgrade merged behind its switch: seven draped kinds (hoodie and hood, quarter-zip, track jacket open and zipped, jumper, roll neck, tee), photo looks and details on the cloth, Size row, layering; live page unchanged; drape preview artifact with a Draped clothes switch | B8UXnh v4 (GitHub build), 5A3t39 v4 (drape preview) |
| 12 Oct 2026 | #36 | Drape proof, continued: front details on draped cloth, rib bands, a Size row in the fitting room and Cloth fit, only track-type jackets worn open draped, draped tops kept in `up` and named as `main`'s layers, `check_3d.js` takes `QA_INIT`; unchanged without the switch | not republished |
| 12 Oct 2026 | #36 | Garment drape proof: the hoodie (with its hood), quarter-zip and jacket drape cleanly in `tools/build_garments.py`, templates in `data/garments/`, the page draws them with `window.__drape` set (`drapeTops`); unchanged without it | not republished (FtdHKg shows PR #33's build) |
| 12 Oct 2026 | #35 | Garment drape upgrade begun: Emma's design handoff in `design/garment-drape/`, her decisions, `tools/build_garments.py` (Blender templates, in progress) and `tools/garment_view.js`; no page change | not republished (FtdHKg shows PR #33's build) |
| 12 Oct 2026 | PR | Every bottom's cut checked against its shop photo: 166 pairs set in `data/cuts.json` (straight, slim, wide, tapered, cuffed or open, long shorts) | FtdHKg v40 |
| 12 Oct 2026 | PR | Loose legs as straight tubes (no bell from the side), shorts no longer flared, the seat shaped in fitted trousers, a polo's own folded rib collar | FtdHKg v39 |
| 12 Oct 2026 | PR | Biceps and forearms build on the arms within a joint limit (`ARMSUM`), so short sleeves hold on the biggest arms | FtdHKg v38 |
| 12 Oct 2026 | #32 | Bottoms: slim, regular, straight, relaxed, wide and baggy clearly different in 3D and the drawing, shorts at their own length (from the inseam), the cut in words in the fitting room | FtdHKg v37 |
| 12 Oct 2026 | #31 | Trouser legs meet where his thighs do (no V showing his thighs on bigger legs); Clear view in the fitting room (H); shirts and jumpers rest on his chest and span his back instead of standing off it; the Lambretta polo plain with its chest band, its cap with its racing stripe (`crown` correction) | FtdHKg v35 |
| 12 Oct 2026 | direct to `main` | Edit Dave: every slider back in the middle after Save (centred on his last saved look, within hard limits); biceps, forearms, thighs and calves sliders under "Arms and legs" | FtdHKg v34 |
| 12 Oct 2026 | direct to `main` | Folds on the back of a tucked shirt, a jacket's lower back, scarves and shoes' heel counters; contact shade at cuffs, above collars and on shoes under trouser hems | FtdHKg v33 |
| 12 Oct 2026 | #29 | Folds and creases shaded into every garment (trousers, shorts, tops, sleeves, shoes), soft studio light from a room of softboxes, shade under hems and inside open fronts; `legs` check heights follow Edit Dave's proportions | v46 |
| 12 Oct 2026 | #28 | Trousers cut as a pair: the legs part from a crotch seam instead of sticking together, no bulge at the front or cleft at the seat; the `legs` check looks from 7 cm below the crotch | v45 |
| 11 Oct 2026 | #27 | Contrast tipping on polos, tees and jumpers lies along the collar or neckband (it floated above the collar) | v44 |
| 11 Oct 2026 | #26 | Shoe lasts by kind: dress, loafer, Chelsea, safety, desert and more, each with its own sole | v43 |
| 11 Oct 2026 | #25 | Tie on the shirt with its knot at his throat; shirt collar points that come down and angle apart | v42 |
| 11 Oct 2026 | #24 | A blazer can be done up in the fitting room: buttoned at the waist, the shirt and tie in the V (3D and 2D) | v41 |
| 11 Oct 2026 | #23 | Swaps: hats, caps, socks and gloves read by their name, four hats refiled as accessories, build check made an error | v40 |
| 11 Oct 2026 | #22 | STATUS.md added (this file) | v39 (no page change) |
| 10 Oct 2026 | #21 | Fitting room upgrade: outfit view with pins, wear options and light, new Edit Dave, Compare, phone layouts | v39 |
