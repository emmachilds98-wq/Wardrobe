# Handoff: garment drape upgrade for Dave's Wardrobe

Repo: `emmachilds98-wq/Wardrobe` (branch `main`). Target file: `page.html` (built to `docs/` by `tools/build_site.py`).
Read `STATUS.md`, `HANDOFF.md` and `CONTRIBUTING.md` in the repo first. Their rules still apply, apart from the
garment-geometry work this brief replaces.

## Overview

Clothes on Dave's 3D model are misshapen and keep failing the 3D check in new places, especially on Edit Dave's
other body types. The cause is how garments get their shape, not the body or the photo reading. Today every top
is a set of offsets from radial maps of his body (`fitTop`, `fitCollar`). Layers are pushed apart point by point
(`occPushPt` / `occAddMesh`), and everything is warped to his proportions after fitting (`warpMan`). Each garment
detail needs its own rule, rules contradict each other (PR #34: the collar rule against the hood rule), and the
post-fit warp moves layers relative to each other.

The upgrade replaces the garment builder with garments that are cut from patterns, draped as cloth and
settled in wearing order. It keeps everything else: the body, Edit Dave, the photo and listing reader,
`fixes.json`, `specs.json`, the checks and the QA scripts.

## About the files in this bundle

These are **reference prototypes made in HTML**, not production code to paste in. Rebuild the approach inside
`page.html` and the repo's tools, following the repo's own patterns. That means plain functions in `page.html`,
Python tools under `tools/`, data under `data/`, and checks in `tools/check_3d.js`.

| File | What it is |
| --- | --- |
| `Drape Test.html` + `drape.js` + `three-d-stage.js` | Working proof of concept. Loads `data/body.json` from the repo, shapes it with Edit Dave's presets, and settles a hoodie, an open navy jacket and the hoodie's hood as cloth in wearing order. Toggles: body (Dave, slim, athletic, heavier), size (M, L, XL), hood (out over the jacket, or tucked under). Measures the result with rays like `check_3d.js`'s `under`. |
| `3D Fit Review.dc.html` (+ `support.js`) | The written review and recommendation. Open in a browser. |

Open `Drape Test.html` over http (any static server), because it fetches `body.json` from
`raw.githubusercontent.com`. Wait about 7 s for the settle.

**What it shows.** With "Out over jacket", 19 of 20 horizontal rays at the collar's height from behind meet the
hood first. With "Tucked under", 15 meet the collar first and 1 the hood. There is no hood or collar rule: the
result comes only from the order the layers are settled in. It holds on all four body presets.

**What it is not.** The garments are simple grids built round the body and sized from illustrative chart
numbers, not sewn patterns. There is no self-collision, no friction and no texture. Dave's length sliders
(`legLen`, `torsoLen`, …, applied by `propWarp` / `warpMan`) are not applied. A few hoodie pixels poke through
the jacket at its back on the heavier build. Treat it as proof of the layering and body-type behaviour, not of
garment shape.

## How the proof of concept works (`drape.js`)

1. **Body**: `body.json` decoded exactly as `loadBody()` in `page.html` does it. Morphs are applied as `bodyPos()`
   applies them (`k_n` weight −v below zero, `k_p` weight v above). Normals are averaged across the duplicated
   seam vertices. The presets are copied from `page.html` (`CHAR_DEF` body keys for Dave, `PRESETS` for the others).
2. **Colliders** (`collider`, `push`): a 1 cm voxel grid holding the nearest surface point within 4 cm. A
   particle closer than the thickness along that point's normal is pushed out. There is one for the body core
   (arms below the shoulder excluded), one for the arms, and one per settled garment (normals oriented away from
   the garment's own axis).
3. **Starting shell** (`hRing`, `eRing`): radial maps of the body plus the layers already on, made convex. Torso
   rows are horizontal, yoke rows are rays from the chest centre at rising elevation, and the neckline is a ring
   round the neck. Extra width from the size chart (`chest − shell circumference`) mostly goes to the sides, so
   the cloth hangs from the shoulders. This only places the cloth; the settle decides the shape.
4. **Cloth** (`addGrid`): particles with structural, shear and bending distance constraints (rest = pattern
   length). Rib rows (hem, cuffs) have shorter rest lengths, so they gather. Tethers stop the cloth stretching
   under its own weight. The neckline and sleeve heads are pinned (they stand in for seams). The collar has low
   gravity and stiff bending.
5. **Settle** (`settle`): Verlet position-based dynamics, 140–150 steps × 10 iterations, collisions twice per step.
6. **Wearing order**: hoodie, then jacket, then hood (out), or hoodie, then hood, then jacket (tucked). Each
   settled layer becomes a collider for the next.
7. **Check** (`rays`): horizontal rays round the back of the neck across the collar's height, counting which
   cloth each meets first.

## The plan (one pull request per step, each passing the repo's full check)

### 0. Before starting
- Leave PR #34 red, and don't raise limits. Park it unless the "lower the collar under a hood" rule is one
  contained change.
- Freeze garment-geometry rules: the scarf edge, polo collars, contrast collars and STATUS queue items 9 and 10.
  Data, photo reading and the weekly refresh carry on.
- Ask Emma for the two listed decisions (newer Three.js and Blender-made templates) and Dave's measurements.

### 1. Engine: Three.js r128 → current
- Done 16 Oct 2026: 0.186.1 from cdnjs (UPGRADE_PLAN, the Three.js section). Integrity hashes were left out: a
  dynamic `import()` cannot carry one, and the version is pinned in the URL.
- `loadThree()` loads `three.min.js` r128 from cdnjs. Move to the module build (current release, pinned with
  integrity hashes).
- `encoding` becomes `colorSpace`; replace the `if(T.sRGBEncoding)` guards. Light intensities need about ×π.
- Update every QA script that routes `**/three.js/r128/three.min.js` (`zoom.js`, `check_3d.js`, `specs.js`, …) and the `THREE_JS` fallback in CONTRIBUTING.md.
- **Accept when** the full 3D check is as clean as on `main`, and `tools/qa/card.js` stills look the same.

### 2. Garment templates (offline, headless Blender)
- New `tools/build_garments.py`, run like `tools/build_body.py`. It reads `data/body.json`'s base pose and
  writes `data/garments/<archetype>.json`.
- About 45 archetypes covering every shape in CONTRIBUTING.md's table and the gate set (`tools/qa/gate.txt`):
  tee, long tee, vest, polo, short-sleeved shirt, shirt, overshirt, roll neck, jumper, knitted vest, hoodie
  (body + separate hood), half zip, cardigan, waistcoat, Harrington, bomber, denim/trucker, fleece, shell, parka,
  puffer, blazer, coat, mac, gilet, gown, trousers by `BOTCUT` cut, shorts.
- Each one is made from flat pattern pieces sewn on the base body and simulated with Blender cloth, then baked.
  Store per vertex: position, UV from the pattern (so stripes and checks follow the cloth, replacing the by-height
  texture rules) and body binding (nearest body triangle and offset), so each Edit Dave morph moves it with him.
- Make collars, hoods, cuffs, plackets, pockets and waistbands separate pieces with seam indices.
- Grading: a shape key per measurement (chest, length, sleeve, shoulder, waist, inseam, leg opening).
- Keep it under about 8 MB in all (UPGRADE_PLAN section 4), loaded per archetype.
- **Accept when** each archetype, worn alone on Dave, passes `check_3d.js`, and sits beside its shop photos
  with `tools/qa/multi.js` (front and side) better than `main` on the same items.

### 3. Sizing from charts
- Set each piece's shape keys from `data/sizecharts.json` (garment measurements where the shop gives them, body
  measurements plus standard ease otherwise) for size L, or his size rule. Choose the cut and length keys from
  the listing's words (`descOf`, `bottomCut`).
- Show the numbers used in the fitting room.
- The model's chest (about 34 in on his saved shape) against his L tops is an open question in STATUS.md.
  Resolve it with Emma before judging fit.

### 4. Settle in the page (replaces `fitTop`, `fitCollar`, `occPushPt` / `occAddMesh`, and `warpMan` for clothes)
- Port `drape.js`'s solver (`settle`, `collider`, `push`, tethers) into `page.html`.
- Order: shape the body first (morphs and `propWarp` proportions). Bind each template to that body, then settle
  layers inner to outer in `layRank` / `OUTERK` order, each colliding with the body and the settled layers.
- The fitting room's wear options become settle inputs, not new geometry rules:
  - tucked (`TUCKM`): the hem pinned inside the waistband;
  - done up (`ZIPM`): the front seam closed;
  - hood out or in: the hood settled after or before the outer layer;
  - turn-ups (`TURNM`): a hem shape key.
- Cards: settle once per outfit, cache the result per body key (`bodyKey()`), and reuse it for `snap3D` stills.
- **Accept when** the gate set passes on all five bodies (`--body dave|slim|athletic|heavier|loose`) and both
  `--wear` runs. g-mod-27, w20261006-casual-04 and hoodie-coat (PR #34's failures) must pass on all five bodies
  with no hood or collar special case.

### 5. Materials and design
- Lay the existing readings (`sampleLook`, `pieceLook`, `fixes.json`: `swatch`, `place`, `crown`, `front`, `decal`)
  onto the pattern UVs. Keep `studioEnv` and contact shade.
- Turn down `FOLD_GLSL`'s painted folds wherever the cloth now folds for real. Compare with `card.js`.
- The fabric library (STATUS queue 8) fits here.
- **Accept when** `node tools/specs.js` and `specs_diff.py --ci` show no moved readings, and the colour count
  doesn't move.

### 6. Checks
- Keep every `check_3d.js` count and limit.
- Generalise `under` to any outer collar against a hood or scarf, so it measures which cloth is outermost from
  behind and the sides, as `drape.js`'s `rays` does.
- Add the planned photo score: render outline overlap ≥ 0.8 and colour ΔE ≤ 5 for 90% of pieces, with an approve
  page. Wrong shapes should then fail, which the current counts can't catch.
- Add g-mod-27, w20261006-casual-04 and hoodie-coat to `tools/qa/gate.txt`.

## Proof first

Before step 2 at scale, build the hoodie, the hood and one open jacket archetype the new way. Render g-mod-27
with `tools/qa/zoom.js` on all five bodies, front, ¾, side and back (`0,1.3,1.4,1.25` and `3.14159,…`), beside
`main`. If it doesn't clearly beat `main` from every angle, stop and report back.

## Rules that still apply (from the repo)

- Fix the rule that causes a fault, never one outfit. Never raise a check limit to make something pass.
- Check every outfit that uses a shape you touched, from all five views. Run the full check for builder changes.
- Dave's sizes and taste, workwear rules and GBP prices are unchanged. Shop requests are direct only.
- No photos of Dave in the repo. No model names in commits, PRs or code.
- Ship as STATUS.md says: build `docs/`, open a draft PR, merge on green with the full head SHA, republish the
  artifact (never pass `capabilities`), then update STATUS.md, UPGRADE_PLAN.md and the plan doc.

## Needed from Emma

- A yes to the newer Three.js and to Blender-made templates (both her decisions in HANDOFF.md).
- Dave's measurements: chest, waist, hips, inside leg, shoulder and sleeve. Also confirm 1.83 m.
- Whether a few seconds of settle on first opening an outfit is acceptable (cards can use cached results).
