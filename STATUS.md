# Working status: read this first

The live working file for whoever picks up the wardrobe upgrade next (an agent or Emma). It says what is being
worked on right now, what comes next, and how to ship. Keep it current: update **Now** when you start or stop
something, tick the queue as items merge, and add a line to the **Log** every time `main` and the artifact change.
The long history and the reasons behind each rule are in `UPGRADE_PLAN.md`; how the code fits together is in
`HANDOFF.md`; the checks are in `CONTRIBUTING.md`.

- Live page (GitHub Pages, served from `main`): <https://emmachilds98-wq.github.io/Wardrobe/>
- claude.ai artifact (holds the shared database): <https://claude.ai/artifact/8uqcGr2eNmzbQv8UVBshY2>
- Review and plan doc (Claude Doc): <https://claude.ai/code/artifact/a11be046-83a3-47dc-855c-67657c180e7e>

## Now

Nothing in progress. `main`, the Pages site and the artifact all match (see the last Log line).

If you stop part-way through something, write here: the branch, what is done, what is left, and anything you found
out that the next person needs. Push the branch, even unfinished, so the work is not lost when a session ends.

## Queue

In order. Each item is small enough for one pull request. Tick it and add a Log line when it merges.

1. [ ] **Odd swaps in the fitting room.** `swapOpts` offers a denim hat for jeans: `guessShape` reads "Denim … Hat"
   as trousers (category before the word "hat"). Fix the reading by the item's name, not this case.
2. [ ] **A done-up blazer.** Buttoned at the waist, the shirt and tie showing in the V, lapels lying on the chest.
   Until then blazers stay as worn under Open / Done up (`zipBy`). The CI wear check (`--wear zip=up,tuck=out`) must
   still pass on the gate set.
3. [ ] **One set of model controls.** The Fitting room fold under Style guide and the builder's small model still
   have their own buttons; give them the fitting room's camera dock and wear options.
4. [ ] **Untucked with a tie.** A shirt with a tie always stays tucked (`tuckOn`), so Untucked is hidden then.
   Decide with Emma whether that is right (it is how a tie is worn) and say so on the button.
5. [ ] **Newer Three.js** (r128 now). Plan doc "Engine and body", still to do. Check every QA script and the 3D check
   still run, and that card stills look the same.
6. [ ] **Shoe lasts.** Every shoe is one generic shape: trainers, Derbies, loafers, Chelsea boots and work boots
   need their own. Plan doc "Footwear and accessories".
7. [ ] **Fabric library.** Plan doc "Fabrics and photos": cord, waffle, fleece, quilting and denim as materials,
   not only colours.

Needs Emma (do not guess):
- The model's chest measures about 34in on his saved shape, which says S/M tops, while he buys L. Is his saved shape
  or the measurement off?

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
| 10 Oct 2026 | #21 | Fitting room upgrade: outfit view with pins, wear options and light, new Edit Dave, Compare, phone layouts | v39 |
