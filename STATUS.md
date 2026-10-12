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

Shipped 12 Oct (PR #31, artifact FtdHKg v35): trousers meet where his thighs do, Clear view in the fitting room, shirts
and jumpers rest on his chest, the Lambretta polo and cap as in their photos (UPGRADE_PLAN 2zzzzzzzzzzzzzzz). Before
that: Edit Dave's sliders centred on the last save, and biceps, forearms, thighs and calves sliders (2zzzzzzzzzzzzzz).

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

**Open pull requests, as left:** PR #34 (collars and the hood case; draft, red on the hood "back poke", see its comment)
and PR #33 (bottoms' cuts from their photos, arm joint limit, the seat, polo collars; draft). **Emma's artifact (FtdHKg)
currently shows PR #33's build** (`claude/exciting-albattani-megf52`, 05efecd), not `main`: republishing from `main`
would roll that back, so this session did not republish it.

**Next agent, start here (in this order):**

0. **The garment drape proof** (UPGRADE_PLAN 2zzzzzzzzzzzzzzzzzz has what was found, the proof, the checks and the
   commands). Built, behind `window.__drape`: the hoodie (with its hood), quarter-zip and track-type jacket draped in
   Blender and drawn from templates, their front details on the cloth, rib bands, a Size row in the fitting room (and
   Edit Dave's Cloth fit), and the 3D check run with the switch on (gate set 28 of 30 clean on his shape).
   1. Show Emma the proof (PR #36) and ask whether to go on.
   2. If she goes on, in order: shop-photo fronts, decals and `place` maps on draped cloth; then more kinds, the
      layers worn over these first (coats, other jackets, scarves: every remaining switch-on flag is one of those
      built by `make3Dcore` over a draped top), then tees, jumpers and roll necks; a size per piece; compact storage.
   3. Separately, its own pull request: the page's armpit tear. `warpMan` moves arm and chest skin apart by up to 1.7 cm
      at the front of each armpit on his saved shape (a ridge on his bare chest). Blend the two as the builder does
      (`Body.armW`), clothes by the nearest skin's blend, with the full 3D check: it moves every render.
   - Also, a small data pull request: g-mod-27's Duck and Cover top is a quarter-zip with no hood (the shop's feed
     says so), so its piece should be `halfzip`, and `descOf` reads "quarter-zip hoodie" as a full zip ("zip hood").
   - Frozen while this goes on (the drape replaces that code): queue items 9 and 10, scarf edges, contrast collars.
     Data, photo reading and the weekly refresh carry on.

1. **Slim and baggy bottoms:** done 12 Oct (UPGRADE_PLAN 2zzzzzzzzzzzzzzzz): `bottomCut` reads every pair's cut for the
   model, the drawing and the fitting room's words, shorts' length from their inseam. Look at them with Emma; the
   numbers are in `BOTCUT`.
2. **Edit Dave's extremes** (UPGRADE_PLAN 2zzzzzzzzzzzzzzz, Check): with weight 0.6, muscle 0.6, arms and legs 1 and
   the four new sliders at 1.8 all at once, short sleeves poke at the back of the armpit (ca-beer-garden,
   h10-resort, back poke about 100), w20261006-casual-04 back poke 34, joggers sunk at the shin (g-lounge-04). Each
   slider alone at its limit passes. Fix the sleeves' room for big arms (the sleeve sections and `se`), or lower
   `CE_LIM` for the arm sliders. To test a body the page has no button for, copy `docs/` and add an entry to `PRESETS`
   in the copy's `index.html`, e.g. `xbig:{weight:0.6,muscle:0.6,arms:1,legs:1,bicep:1.8,forearm:1.8,thigh:1.8,
   calf:1.8}`, then `node tools/check_3d.js --site <copy> --ids @tools/qa/gate.txt --body xbig`.
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
5. [ ] **Untucked with a tie.** A shirt with a tie always stays tucked (`tuckOn`), so Untucked is hidden then.
   Decide with Emma whether that is right (it is how a tie is worn) and say so on the button.
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
10. [ ] (Frozen 12 Oct: the garment drape replaces this code.) **Polo collars.** The leaf lies flat on his shoulders with ragged edges and the stand is low; in the photos a
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
6. Update this file (Now, Queue, Log), add an entry to `UPGRADE_PLAN.md` for anything substantial, and the Status
   column in the plan doc.

Rules that never change are in `HANDOFF.md` ("Rules that never change"): his sizes and taste, no third-party relays
for shop requests, no photos of Dave in this repo, no model names in commits, PRs or code.

## Log

Newest first. Date · PR · what changed · artifact version.

| Date | PR | What | Artifact |
| --- | --- | --- | --- |
| 12 Oct 2026 | #36 | Drape proof, continued: front details on draped cloth, rib bands, a Size row in the fitting room and Cloth fit, only track-type jackets worn open draped, draped tops kept in `up` and named as `main`'s layers, `check_3d.js` takes `QA_INIT`; unchanged without the switch | not republished |
| 12 Oct 2026 | #36 | Garment drape proof: the hoodie (with its hood), quarter-zip and jacket drape cleanly in `tools/build_garments.py`, templates in `data/garments/`, the page draws them with `window.__drape` set (`drapeTops`); unchanged without it | not republished (FtdHKg shows PR #33's build) |
| 12 Oct 2026 | #35 | Garment drape upgrade begun: Emma's design handoff in `design/garment-drape/`, her decisions, `tools/build_garments.py` (Blender templates, in progress) and `tools/garment_view.js`; no page change | not republished (FtdHKg shows PR #33's build) |
| 12 Oct 2026 | PR | Bottoms: slim, regular, straight, relaxed, wide and baggy clearly different in 3D and the drawing, shorts at their own length (from the inseam), the cut in words in the fitting room | FtdHKg v37 |
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
