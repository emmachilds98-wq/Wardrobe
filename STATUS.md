# Working status: read this first

The live working file for whoever picks up the wardrobe upgrade next (an agent or Emma). It says what is being
worked on right now, what comes next, and how to ship. Keep it current: update **Now** when you start or stop
something, tick the queue as items merge, and add a line to the **Log** every time `main` and the artifact change.
The long history and the reasons behind each rule are in `UPGRADE_PLAN.md`; how the code fits together is in
`HANDOFF.md`; the checks are in `CONTRIBUTING.md`.

- Live page (GitHub Pages, served from `main`): <https://emmachilds98-wq.github.io/Wardrobe/>
- claude.ai artifact (holds the shared database): <https://claude.ai/artifact/8uqcGr2eNmzbQv8UVBshY2>
- Emma's own copy of the artifact (republished from `docs/` the same way, its own database):
  <https://claude.ai/artifact/FtdHKgXdaBGrVmpbVYTrLn>. A session signed in to her account can only publish to this one.
- Review and plan doc (Claude Doc): <https://claude.ai/code/artifact/a11be046-83a3-47dc-855c-67657c180e7e>
- From the drape session (this account's own artifacts, no shared database: shortlist and Edit Dave save on the device):
  the GitHub build as it stands (`docs/` at PR #36's latest commit, nothing changed):
  <https://claude.ai/artifact/B8UXnhceKPAsHpTbyzFzek>; and the drape preview, the same build with a Draped clothes switch
  (`python3 tools/build_site.py --out <dir> --drape`, never into `docs/`): <https://claude.ai/artifact/5A3t39MwR6C9T5rHNED2iT>.
  Both published as `docs/` is: page `index.html`, every file under `data/` in `files`, root the build folder, no
  `capabilities`.

## Now

**13 Oct, late: a draped scarf, behind the drape switch** (PR #41, UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzzz). **With
the switch off the live page is unchanged.** A scarf template (`tools/build_garments.py --only scarf`,
`data/garments/scarf.json`: 180 x 14 cm, once round his neck, both ends down his front, draped in Blender over his body
and the draped jumper) drawn by `drapeTops` last of all with the switch on (`dScarf` in `make3Dcore`, `drapeScarf`),
1 cm off what is under it and pushed in front of thin details by rays; its ends wear the `strip` design, with fringes.
Switch-on check of the 7 draped-scarf outfits on five bodies: as `main` with the switch on, but g-outdoor-05 "under 4"
on his shape (one speck of collar). **Next engineer, start here for the scarf:**
1. The crossing on his chest bunches into a knot: in `scarf_path` try the ends leaving the loop under it (a tuck) rather
   than over it, or a gentler twist where each end leaves the loop (`join`: more points, the band's width turning over
   10 cm); look at each try with `node tools/garment_view.js <debug>/scarf-draped.json out.png` before the page.
2. The loop stands high behind his neck (the pinned edge, `pins` in `drape_scarf`): try pinning lower on the loop, or
   releasing the pins for the last 20 frames.
3. g-outdoor-05 "under 4" (switch on, his shape): the jacket collar's tip between the scarf's outer layer and its edge
   folded in. Either lower `make3Dcore`'s stand collar under a draped scarf (as the half-zip's is lowered under a scarf)
   or skip the fold-in rows in the push (`drapeTops`, the scarf block).
4. Then the other outer layers still blocking the drape (item 0.1 below), and XPBD substeps in `drapeSettle`
   (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzzzzzzzzzz, research).
**The shared artifact (8uqcGr2) is behind `main`:** it still shows PR #39's build (v51); PRs #40 (live: jackets on his
chest, the new scarves) and #41 (drape switch only) are on GitHub Pages but not on the artifact. The session that merged
them could not republish: the Artifact tool asks for the live page to be Read line by line first (8198 lines, about 350k
tokens), more than was left. To republish: `Artifact read` 8uqcGr2, Read the saved page in full (offset/limit, about 400
lines a call), confirm `diff <(git show 29fbad8:docs/index.html) <saved page>` differs only in the first line (the
artifact's wrapper), then publish `docs/index.html` with `files` = only what changed since 29fbad8
(`git diff --stat 29fbad8 HEAD -- docs`: `data/items/acc-1.json`, `data/items/acc-2.json`, `data/garments/scarf.json`;
files left out are kept), root `docs`, **no `capabilities`** (that keeps its database and downloads). Then the Log's
artifact column.
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
   - heavier: belly skin under draped tees and knits (h10-surf, jb11-cheapest, lazy-sunday, q7-fairisle, m5-argyle),
     the same on `main`'s drape: the templates are short over the heavier belly (grade length with the belly, not
     only round him: `drapeGrade`'s `sy`).
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
      2zzzzzzzzzzzzzzzzzzzzzzzzz). Next: padded and puffer jackets (21 outfits blocked; the jacket template with more
      ease, quilting as a material), the other zip jackets (21), a shirt tucked in (into the waistband), a coat (long,
      lapels), Harrington and denim jackets, an overshirt's patch pockets (a jacket-weight overshirt under a gilet is
      what is left on g-outdoor-21).
      Also: q7-fairisle's draped half-zip collar comes over PR #34's tighter scarf ("under" 14, switch on only). Each: `MEAS` and pattern pieces in `build_garments.py`, a run with `--debug`, a look with
      `garment_view.js`, then `DRAPEK`/`DRAPEF` and `drapeArch`'s cut test in `page.html`. Until then, an option is to
      drape a tee or knit only when nothing `make3Dcore` builds is worn over it.
   2. Then turn the switch on for everyone (after the full 3D check with it on, all five bodies, and Emma's look).
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
3. **One set of model controls** (queue item 4). Found 12 Oct: the builder's small model uses `Live3D`'s own bar
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
4. [ ] **One set of model controls.** The Fitting room fold under Style guide and the builder's small model still
   have their own buttons; give them the fitting room's camera dock and wear options.
5. [x] **Untucked with a tie.** Decided 13 Oct: a shirt with a tie stays tucked (`tuckOn`, as a tie is worn); the
   fitting room's tuck row now shows only "Tucked", with the note "Worn with a tie, the shirt stays tucked in." (PR #39).
6. [ ] **Newer Three.js** (r128 now). Emma said yes on 12 Oct (the drape plan's step 1, `design/garment-drape/README.md`).
   Plan doc "Engine and body", still to do. Check every QA script and the 3D check still run, and that card stills
   look the same.
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
