# Prompt for the v22 session (written 2026-11-28)

Paste this into a new Claude Code session opened in `~/LOCAL/CODE-2026/S15-flat`:

> Read `AGENTS.md`, `journal.md` (to the end) and `Claude-vectors/S15-v22-session-prompt.md`, then do the plan in that file. Show me a KISS list at the end.

---

## Goal
1. Clean the project.
2. Build v22: all of Zel's agreed changes.
3. Make the mixer work on a phone.
4. Write the electrician's files in Croatian.

Zel approved everything below on 2026-11-27/28. The sources are the table "Decided for the next version" in `Claude-vectors/S15-wall-light-points-DRAFT.md` (rows 1–17) and the journal.

Owner rules from `AGENTS.md` still apply:
- Short answers, metric units, options A/B/C.
- If a source conflicts, list it and ask; never pick silently.
- Each model version is a new file.
- **Commit and push only when Zel asks.**

## Ask Zel first (one message, options A/B/C)
1. **Bed switches** (still open): with smart dimmers,
   - A: a wired push button in a box at each bed side;
   - B: a battery remote stuck to the wall.
2. **Ambient dimmer:** one for the whole flat, or one per room. This sets how many dimmer boxes the electrician makes.

Start on the steps that don't depend on the answers (1, 3 and the mixer) while you wait.

## Plan

### Step 1: clean-up (Zel, v22 items v–vii)
Zel has seen v21 and asked for this. Delete with `git rm` for tracked files and plain delete for git-ignored ones, then list what went in the KISS list.
- **Variant v21-lighting-expert, all of it:**
  - `S15-Hrneticka-v21-lighting-expert.sh3d`
  - `Claude-tools/build_v21_lighting_expert.py`
  - `Claude-vectors/S15-v21-lighting-expert-{notes.md,fixtures.txt,plan.png,plan.svg}`
  - `Renders/blender-lighting/*-v21-lighting-expert[_.]*` (sheets, mixer, lux table, lux maps)
  - in `render/blender/out/`: the `*/<view>-v21-lighting-expert.npy`, `.blend`, `.blend1`, `state-`, `lumens-` and `run-` files
- **Variant v21-lighting-expert-blank:** the same set with `-blank`.
- **v19 and v20:**
  - `S15-Hrneticka-v19.sh3d` and `S15-Hrneticka-v20.sh3d`
  - `Claude-vectors/S15-v19-plan.*` and `S15-v20-plan.*`
  - `Renders/blender-lighting/*-v20*`
  - `Claude-tools/build_v18.py`, `build_v19.py` and `build_v20.py` (git keeps them)
  - in `render/`: the v20 `.npy` files (check first that no v21 file is a hard link that needs them; hard links keep the data anyway), the old `render/blender/in/obj*` folders except `obj21`, and old `Home-v*.xml` files.
- **Keep:**
  - v21 (the vPREV for incremental renders) until Zel has seen v22;
  - `build_lightset.py` (a general tool);
  - `S15-v15-critique.md` (AGENTS.md cites it).
- **Code:**
  - `make_site.py` has the "Alternative designs" block and the ALT names: keep the generic code, but no links may point to deleted files.
  - Check which tools nothing uses any more (`lights_off.py`, `run_render_mac.sh`, `nano_banana.py`, `overlay_architect.py`, `electrical_grid.py`). For each, delete it or keep it with a reason. Ask Zel before deleting anything not named above.
- **Faster iterations (time-box: 30 min):**
  - A render takes about 26 s, whatever the samples or persistent data (`AGENTS.md`, lighting workflow 8), so the time is not path tracing.
  - Measure where it goes: denoiser (OIDN on GPU or CPU), scene sync, EXR/npy writing. Fix it if it's cheap, and write the result in `Claude-tools/README.md`.
- **Update:** `AGENTS.md` (folder map, current state), `Claude-tools/README.md`, `.gitignore` if needed.

### Step 2: v22 model (`Claude-tools/build_v22.py`, v21 → v22)
Draft rows (the table "Decided for the next version"):

| Row | Change | How |
|---|---|---|
| 1 | Niche profiles **200 lm/m** | lamp data (`groups.json` → `lamps.niche`, or per light) |
| 2 | Hall seat bar **300 lm/m**, 2700 K | lamp data |
| 4 | Kitchen bar **900 lm/m**, 2700 K | lamp data |
| 5 | **Mirror border lights** in the en-suite and the guest bathroom | a mirror with a light strip round its edge (about 1,000 lm per mirror, 3000 K, ceiling group). En-suite: mirror top ≥ 207 to cover the outlet at 200, 54 from the west wall; guest bath: over the basin on the east wall. Check the existing mirror lights and replace them |
| 8 | All ambient lamps **2700 K** (TV pucks, kitchen bar and hall bar are 3000 K now) | lamp data |
| 9 | Laundry wall light 10 **off ambient**, on its own switch | renders: put it in the ceiling group (only 3 groups exist); note it in the draft |
| 10 | Terrace lamps on their own switch | renders: ceiling group as now; note it |
| 11 | **Wide-beam GU10, 60°, 345 lm** for Sara 16 and the new room 5 desk light | a new role (for example `gu10wide`) in `make_lights.py` RULES and `groups.json` |
| 13 | **Bedroom wardrobe top:** LED up-light bar behind a 5 cm raised lip on the **east** (front) edge; lights the west wall above it | wardrobe 160×65 at x 266, y 565, rotated (spans x 233–299, y 485–645), top 236, ceiling 280. Copy the TV-shelf up-light (v20 `Shelf bar x:` lights, role `shelfup`), about 300 lm/m, 2700 K, **ambient**; aim at the west wall and ceiling |
| 14 | **Wall lights rotated so the base is on the wall** | model `Wall light - up/down - 3dwarehouse`: bedroom 2 and 3 (x 597, angle ≈ 0, should face west), Sara 15 (angle π) and room 5 12 (x 231, angle π). Its depth (11.5) must point out of the wall. Find the right angle (±π/2) from a quick SH3D or Blender render of one; move the light sources with it |
| 15 | **Sara wardrobe top:** the same up-light bar on the **south** (front) edge; lights the north wall | wardrobe 150×60 at x 747, y 991 (spans x 672–822, y 961–1021), top 236; ambient |
| 16 | **Sara: 3 ambient lights:** keep 16 and the wardrobe bar; **remove 17** (A17 pieces and its 2 lights); **move 15** (model and 2 sources) south | new y about 1245 (about 103 from the south wall, about 283 from the north wall), same height 128. Check clearance from the wall shelf (y 1094–1244, at 200) and the poster (y 1138–1199, 95–186) |
| 17 | **Room 5: one desk light** centred over the desk, as in Sara's room; remove A13 and A14 (pieces and lights) | east wall at y 1265 (83 from the south wall), 175 high, wide beam (row 11). **Remove the Gnijezdo print 45×90** from room 5 (Zel, 2026-11-28: he won't have it), so the wall is clear |

Not model changes: rows 3 (hall spots stay), 6 (Xiaomi night lights), 7 (CRI ≥ 90, picture lights ≥ 95) and 12 (smart dimmers). They go into the electrician's files and the notes only.

Then:
- pack v22 with `make_sh3d.py`;
- run `S15Tool.java check`;
- draw the plan with `plan_svg.py` → `Claude-vectors/S15-v22-plan.svg/png`;
- update the draft's fixed-lights table (15 moved; 13, 14 replaced by one light; 17 removed; rows 13 and 15 as new entries).

### Step 3: render v22
1. `Claude-tools/blender/render_version.sh v21 v22`. Use `--full` if `groups.json` lamp data or roles changed in a way `rerender.py` can't see.
2. It runs in the background; wait for `S15 done`.
3. Then `mix.py` and `make_site.py v22`.
4. Fix the day exposure: `mix.py` computes DAYK per version. Make it one fixed constant, so day pictures compare between versions; note the value in `AGENTS.md`.
5. If a new view helps (for example Sara toward the bed head and chair), add it to `cams.txt` and `groups.json`.

### Step 4: mixer and site on a phone (Zel, v22 viii)
- **Target:** Chrome on an iPhone 15 Plus with the top and bottom bars showing. That is a viewport of 430 px wide and about 720–750 px tall (screen 430×932 CSS px).
- **Edit:** `Claude-tools/blender/mixer_template.html`. The page is a grid with a 340 px side panel and `@media(max-width:900px)` for one column.
- **Under about 700 px wide:**
  - presets (scenes) and views become `<select>` dropdowns at the top;
  - the picture is full width and visible without scrolling, together with the scene selector;
  - group sliders are compact;
  - touch targets are 44 px or more;
  - no horizontal scrolling;
  - use `dvh`, not `vh`.
- **Desktop:** must look as it does now.
- **Check:** headless Chrome at 430×740 (`--window-size=430,740`, mobile user agent) and 1500×1100, and in the built-in browser with `resize_window` 430×740. Check `index.html` (`make_site.py`) on the phone size too. Re-run `mix.py` so `light-mixer-v22.html` has the new template.

### Step 5: files for the electrician, in Croatian (Zel, v22 ix)
**Purpose:** the electrician adds the new wall outlets (izvodi) for the lights in v22. Every point comes from the v22 model and the draft. Use correct Croatian trade words:
- izvod za zidnu svjetiljku (outlet for a wall light);
- napajanje LED trake i mjesto za driver (LED strip feed and driver space);
- kutija za pametni dimer (duboka, s nulvodičem) (deep smart-dimmer box with neutral);
- razvodna kutija (junction box);
- instalacijska cijev ("buzir") (conduit);
- štemanje (chasing);
- gips-karton (drywall);
- AB zid / zidani zid (concrete wall / masonry wall);
- gotovi pod (finished floor).

**Outputs** (tracked, public, so nothing private: no names, no address beyond what the repo already shows):
1. `Claude-vectors/S15-elektricar-v22.md`, plus a printable PDF of it (headless Chrome from HTML), titled "Popis izvoda".
   - **One table per room,** columns:
     - br. (the draft's number);
     - prostorija, zid;
     - **udaljenost od najbližeg ruba**, and which edge (kut sobe, rub vrata, rub prozora), in cm;
     - **visina od gotovog poda** to the outlet's centre;
     - vrsta izvoda;
     - **zid: gips-karton / beton**;
     - strujni krug (ambijent / strop / vlastiti prekidač);
     - napomena.
   - **Status:** points that must wait are marked **"NE BUŠITI – čeka potvrdu"** (pictures not yet chosen, for example 8; anything still open).
   - **Also list:**
     - the dimmer boxes (deep box with neutral at each ambient switch);
     - the switched sockets (L1–L4; prefer rewiring the existing sockets the draft names);
     - the closet feeds (4 is not needed; T is in the laundry);
     - the bed switches per Zel's answer;
     - the note "CRI ≥ 90, slike ≥ 95, ambijent 2700 K".
2. `Claude-vectors/S15-elektricar-v22-shema.svg/.png/.pdf`: a floor plan with every new outlet and **a proposed cable route to it in two colours**:
   - **blue: gips-karton.** The cable drops through the wall cavity, so it needs only one hole at the outlet.
   - **red: beton or masonry.** A chase (štemanje) from the nearest existing cable or box.
   - **Wall elevations:** add one per wall that has new points, showing the vertical drops and the heights. A plan alone can't show heights.
   - **Legend:** scale, north arrow, model version and date.

**How to route:**
- **What the electrician said:** cables run from the ceiling junction boxes in conduits, mostly **diagonally in the ceiling**, then **vertically down** the wall to each outlet. Zel suspects some run **horizontally** too, for example on the living-room south wall (the AC wall) from its drywall part.
- **Mark all existing routes "pretpostavljeno" (assumed).**
- **New routes:**
  - go from the nearest existing point (ceiling box, switch, socket, ceiling light point);
  - run inside the usual installation zones: vertical 10–30 cm from corners and openings, horizontal 15–45 cm under the ceiling (the DIN 18015-3 practice, which Croatian electricians follow);
  - take the shortest chase.
- **Sheet note:** check with a cable detector before drilling.
- **Wall material:**
  - Find it per wall from the architect plan (`Building-docs/S15-architect-plan.pdf`: hatching, wall thickness), the electrical plan (`Mapa III`, p. 56; legend p. 74) and the site photos (`Hrneticka-photos/`).
  - List the walls you are unsure of and ask Zel; don't guess.
  - Known: the living south wall is part drywall, part concrete (light 9's feed is at the drywall, 17 west of the joint).
- **Existing points:** the group "AS BUILT" in the model (red dots in the plan) and the as-built table in the draft.

**Source files:** use the source files in place; nothing from the Drive root goes into a tracked path.

### Step 6: finish
1. Update `journal.md`, the draft, `S15-furnishing-notes.md` (v22) and `AGENTS.md` (current state: v22, the cleaned folder map, the electrician files).
2. KISS list for Zel:
   - what to look at in the mixer (phone and desktop);
   - the electrician files;
   - what was deleted;
   - open questions.
3. List the v21 files to delete once Zel has seen v22.
4. Don't push until Zel says so.

## Facts the new session needs (2026-11-28)
- **Dimming is decided:** smart dimmer modules (Matter, for example Shelly) behind normal push-button switches; plain dimmable LEDARE GU10s and phase-dimmable drivers. The PILSKOTT lamps stay IKEA smart, in one Matter app. Neutral wire plus a deep box at each dimmer.
- **Night lights:** Zel's Xiaomi motion lights, for now; no wiring.
- **Python:** system `python3` has no libraries. Make a venv in the scratchpad with matplotlib, pillow, numpy and opencv-python-headless for `plan_svg.py` and `mix.py`.
