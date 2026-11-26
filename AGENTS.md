# AGENTS.md: S15 Hrnetićka interior design

Read this file and `journal.md` (to the end) before doing anything. At the end of every session, add an entry to `journal.md`.

## Current state (2026-11-26)
- **Latest model: `S15-Hrneticka-v20.sh3d`** (2026-11-26) = v19 + an up-light bar behind a raised lip on the TV shelf. v19 = Zel's review of the v18 plan: bedroom balcony door = west panel, Sara's south door opens only its west leaf (photos), Sara's desk lamp out, pinboard, C side table, beanbag, laundry rack 10 west; C9–C11 solved. v18 = interior doors drawn open, wardrobe 160, bed centred, south picture light on a wall strip.
- **Current task:** find positions for ambient lights so Zel can tell the electrician where to drill. The deliverable at the end is a drill sheet (wall, distance from a corner, height). Draft: `Claude-vectors/S15-wall-light-points-DRAFT.md` (fixed lights, switched sockets, dimming groups, closet feeds).
- **How Zel reviews lighting:** `Renders/blender-lighting/light-mixer-v20.html` (3 groups: ambient with dimmer, ceiling, day; 16 views; lux map) plus the `compare-v20_*.jpg` sheets and `luxmaps-v20.png`. He can't judge light in SH3D.
- **Waiting for Zel:** review of v20 (new views 19 and 22, day scene, TV shelf up-light, three groups), confirmation of the interior door hinges. Then delete the v19 model and plan (v18 files are already gone). Open in the draft: real picture sizes (they set the picture-light heights), curtain positions near lights 1, 14, 17, low-lamp corners, lamp data for everything except the GU10 and the two PILSKOTT lamps.
- **Layout (2026-11-25):** all design work lives in one place, `~/LOCAL/CODE-2026/S15-flat/` on the Mac. That folder is the git repo and the working folder. The Drive folder `Interior-design/` is retired. See "Folder map".
- **Published:** public repo `github.com/ZSvedic/S15-flat`, site `https://zsvedic.github.io/S15-flat/` (mixer, sheets, lux table of the latest version). The site changes only when someone pushes. See "Publishing" below.
- **Critique of v15:** `Claude-vectors/S15-v15-critique.md`. Zel accepted points 1–7 with changes (journal 2026-11-19 c). Not taken up: softer up-lamps, bedside reading lights, room 5 light spacing, night light.

## Owner rules (Zel)
- Ask for confirmation before any drastic change to models or files. Propose a before → after list with the evidence for each item, then wait.
- **When sources conflict, trust them in this order:**
  1. Zel's latest site photos with measurements (Drive: `Hrneticka-photos/`): the real flat as built.
  2. Architect and engineer drawings (Drive: `Building-docs/`).
  3. Old files, the marketing catalogue and screenshots.
- If a conflict can't be settled by evidence, list it and ask. Never pick silently.
- Short answers, metric units, options labelled A/B/C, steps 1/2/3.
- Never edit a model in place: each version is a new file, `S15-Hrneticka-vNN.sh3d`.
- **Folder names stay fixed; the version goes in the file name** (Zel, 2026-11-25), for example `Renders/blender-lighting/light-mixer-v16.html`. Never make a `…-vNN/` folder. Once the vNN files are done and Zel has seen them, delete the v(NN−1) files (`git rm` for tracked ones; git keeps the history). List the deletions for Zel first.

## Folder map
Two roots. Claude Code on the Mac reaches both.

**Repo root: `~/LOCAL/CODE-2026/S15-flat/`** (on the Mac; git repo `ZSvedic/S15-flat`, public). All design work lives here, and relative paths in this file start here.
| Path | What |
|---|---|
| `S15-Hrneticka-vNN.sh3d` | Sweet Home 3D model. The latest version is the source of truth. |
| `Claude-tools/` | Toolchain: build scripts, plan drawing, headless renderer, Nano Banana. See its README. |
| `Claude-tools/jars/` | Sweet Home 3D jars. Git-ignored; if missing, copy them from a Sweet Home 3D 7 installation. |
| `Claude-tools/blender/` | Blender lighting pipeline: `groups.json`, `make_lights.py`, `s15_blender.py`, `rerender.py`, `render_version.sh`, `mix.py`, `tm.py`, `mixer_template.html`, `calib.py`. See `Claude-tools/README.md` |
| `Claude-vectors/` | Plan drawings (`S15-vNN-plan.svg/png`), `S15-interior-spec.md` (Zel's wishes), `S15-furnishing-notes.md` (design decisions per version) |
| `Claude-vectors/S15-wall-light-points-DRAFT.md` | All proposed light points (Zel's 17 circles plus the later additions), with wall distances, heights and open points |
| `Renders/` | Results for the current version, with the version in each file name: `blender-lighting/` (`compare-vNN_<view>.jpg` sheets, `luxmaps-vNN.png`, `lux_table-vNN.md`, `light-mixer-vNN.html`); `sh3d-low/` previews and `nano-banana-2/` photoreal renders when they are made |
| `render/` | Raw render work, git-ignored. `render/blender/in/` holds the Blender inputs (`objNN/` OBJ export, `Home-vNN.xml`, `lights.json`, copies of `groups.json`, `cams.txt`, `s15_blender.py`); `render/blender/out/<group>/<view>-vNN.npy` the raw renders (groups ambient, ceiling, day) and `state-vNN.json` for `rerender.py`. Holds v20 now. |
| `private/` | Git-ignored. Holds `Zel-sketch-v1.jpeg`, Zel's furniture sketch. |
| `README.md`, `index.html`, `.nojekyll` | Landing page and site files for GitHub Pages |

**Drive root: `My Drive/Zeljko/Real estate/Hrneticka/`** (private inputs; never copy them into a tracked path).
| Path | What |
|---|---|
| `Building-docs/S15-architect-plan.pdf` | Architect plan of the flat, vector, 1:50, cropped from p. 4 of `Hrnetička-all-floors.pdf` |
| `Building-docs/Electrical Installation Plan S15.png` | Electrical plan, lights and sockets (from `Mapa III_Elektrotehnički projekt.pdf`, which also has the legend) |
| `Hrneticka-photos/<room>/` | Site photos, many with tape measures |
| `Interior-design-OLD/` | The old working folder, retired on 2026-11-25. Don't use it; Zel deletes it when he is satisfied. |
| `Interior-design` | Symlink to the repo root (2026-11-25). Google Drive lists it as a single file and did not upload the folder behind it. |

## Fixed facts (confirmed by Zel; don't re-litigate)
- **Hallway → living room:** a door 82×210 after all (Zel, 2026-11-25); in the model hinged on the south jamb, opening into the living room.
- **Interior doors (v18):** bathroom hinged west, opens clockwise into the bathroom, floor stop before the WC (Zel). Front door gets a floor stop off the mirror (Zel). Other hinges are Claude's choice (latch side at the as-built switch) until Zel says otherwise.
- **Second bathroom:**
  - The door is in the north wall, from the hallway, 70 wide. Both the architect and electrical plans show it wrong.
  - WC on the west wall, basin on the east wall, bath across the south.
- **Ceiling:** 280.
- **Windows:** 170 high with a 90 cm sill.
- **Bedroom north opening:** 300×245 three-panel window on a 15 cm sill; the **west** panel opens to the balcony (hinge west), the other two are fixed (IMG_1956, Zel 2026-11-26).
- **Sara's room:** two terrace exits:
  - east door 80×240 on a 20 cm threshold;
  - south double door 160×250 on a 10 cm sill; only the west leaf opens (inward, hinge west), the east leaf is fixed (IMG_1962, Zel 2026-11-26).
- **Laundry terrace door:** 80×240 on a 20 cm threshold.
- **Terrace and balcony floor:** +16 cm above inside.
- **Balcony parapet:** 100 cm.
- **Terrace railing:** 60 cm upstand plus glass, 117 cm total.
- **Bathrooms:** beige stone-look tiles from floor to ceiling.
- **Balcony furniture:** normal-height table with chairs; no bar furniture.
- **Living → terrace door:** 300×240, two panels (not three as on the plan).
- **Lights:** as-built ceiling points from the photos, not the electrical plan count (hall 5 spots, corridor 2, laundry 6, Sara 2, living 3 + dining). Positions confirmed by Zel in v13.
- **Lighting tool:** Blender (Cycles) for judging light; Sweet Home 3D stays the only source of truth and the Blender scene is rebuilt by script. Zel found SH3D renders (old engine and YafaRay) and Nano Banana unusable for lighting decisions.
- **Wall-light style (Zel's current flat):** up/down cylinders (black, white in Sara's room), wider shielded up/down lights at the bed, LED pucks under the TV shelf, an LED light bar under the kitchen wall cabinets.
- **GU10 lamp (Zel's photo, 2026-11-19):** IKEA LEDARE LED1931R5, 4.1 W, 345 lm, 2700 K, 36°, 600 cd, dimmable. Zel wants no narrow-beam variant. The lamp is modelled as a narrow core plus wide spill (half its light falls outside the 36° cone), which matches his remark that it gives a wide beam.
- **Other real lamps (links from Inge, 2026-11-19):** IKEA PILSKOTT LED pendant 97 cm, 1,100 lm, 16.5 W (304.778.78) over the dining table; IKEA PILSKOTT LED floor lamp 112 cm, 700 lm, 14.5 W (904.781.20). Both are smart lamps dimmed by IKEA remote; IKEA lists no colour temperature (2700 K assumed).
- **Paintings get overhead picture lights** (tube on an arm, as in Zel's Pooky example), not GU10 cylinders. Zel: the GU10 lamps are not good for paintings.
- **Circle 4 (bedroom west wall) and a point on the laundry north wall** are feeds for closet interior lights that switch on when the door opens, not wall lights.
- **Video intercom:** living south wall, x 710, 152 high (Zel, 2026-11-26).
- **Fuse and network boxes:** hall south wall, west of the bathroom door (photos IMG_1958, IMG_2019). Confirmed by Zel on 2026-11-19.

## Coordinates (model, v13 and later)
Units are cm; y points south; angles are in radians. From v13 the walls follow the architect plan exactly; the anchor is the living room NE inner corner (1464.71, 305.88). Room inner faces:
- Living + kitchen x 613–1465, y 306–774
- Bedroom x 233–603, y 306–650
- Ensuite x 41–223, y 306–595
- Hall strip x 41–613, y 660–766 (wardrobe niche y 605–660); corridor x 435–537, y 766–1061
- Bathroom x 225–425, y 778–1001
- Laundry x 547–822, y 784–950
- Sara x 547–822, y 962–1348
- Room 5 x 225–537, y 1011–1348
- Terrace x 654–1402, y 807–1573
- Balcony x 21–782, y 29–275

Mappings (verified 2026-11-18):
- Architect plan PDF points → model: `pt_x = 843.6 + (x − 1464.71)·0.56693`, `pt_y = 207.7 + (y − 305.88)·0.56693`. Tool: `Claude-tools/overlay_architect.py`.
- Electrical plan (`Mapa III` p. 56, set page rotation to 0; legend p. 74): `x = 32.08 + (Y − 595.08)/0.28346`, `y = 296.88 + (621.36 − X)/0.28346`. Tool: `Claude-tools/electrical_grid.py`.

## Environment notes
- **Everything runs on the Mac** in Claude Code's own Bash (since 2026-11-25): Java, Blender, git, `gh`, and reading the Drive folder. The old Linux VM bridge and the separate Mac shell are no longer used.
- **Java (SH3D tools):** `/opt/homebrew/opt/openjdk/bin/java --add-exports java.desktop/com.apple.eio=ALL-UNNAMED -Duser.home=<writable dir> -Djava.awt.headless=true -Dj3d.rend=noop -cp "$(ls jars/*.jar | tr '\n' ':')" S15Tool.java …` from `Claude-tools/` (source-file mode; same for `ExportObj.java`). In zsh keep the command in a function or array, not a string.
- **Python:** system `python3` has no libraries; `plan_svg.py` and `mix.py` need a venv with matplotlib, pillow, numpy and opencv-python-headless (make one in the session scratchpad).
- **Installed:** Blender 5.3 (`/Applications/Blender.app/Contents/MacOS/Blender`, Metal GPU), OpenJDK, `pdftoppm`, ImageMagick, headless Chrome. Mac is an Apple M4.
- **Long jobs:** run Blender in the background with `caffeinate -i` (the Mac sleeps otherwise) and wait for the task notification.
- **Nano Banana (OpenRouter):** key in `~/LOCAL/CODE-2026/TamedTable/.env`; never print it. Mood pictures only.
- **Google Drive sync** can serve a stale copy of a file you've just written; check the content before using it.
- **SH3D rendering:** `S15Tool.java` sets the observer camera (otherwise ceilings are missing) and a fixed time (`-Dt=<epoch ms>`; 23:00 = `1792616400000`); `run_render_mac.sh` on the Mac. Never leave `widthInPlan`/`depthInPlan`/`heightInPlan` on a resized door or window: SH3D cuts the wall hole from them.
- **Sun and north (2026-11-26):** the flat is in Zagreb, Stenjevec (k.o. Stenjevec Jug). Plan north (up, −y) points to bearing 25° (NNE): site plan in `Mapa 1_arhitektura`, p. 131. The SH3D compass still has the default Berlin values; the Blender day scene takes place and north from `groups.json` → `day`.

## Workflow for lighting (Blender; three groups from v20)
Light adds up, so each light group is rendered once per view and any on/off or dimmed mix is the sum. Never render fixed variants.
1. Lights live in the `.sh3d`. The name prefix decides the lamp set and type (table `RULES` in `blender/make_lights.py`): `AmbA up/down:` (wall), `ArtE/ArtH/ArtS bar`, `Desk aim:`, `TV puck:`, `Shelf bar x:` (TV shelf up-light), `Kitchen bar x|y:`, `Niche bar`, `Low bar/lamp`, `Pendant bar`, `Light: …` (ceiling, spots, mirror, terrace). A name ending in `-> x,y,z` aims the lamp at that model point.
2. `blender/groups.json` maps the lamp sets to **three groups (Zel, 2026-11-26): 1 ambient** (all wall, picture, TV, kitchen bar, dining pendant, floor/table lamps, hall bar, niche: one switch, one dimmer), **2 ceiling** (all other lamps; scene 2 = ambient + ceiling), **3 day** (no lamps; sun and clear sky on 15 May at 13:00, sky calibrated to 15,000 lx on open ground, sun 95,000 lx). Only the GU10 and PILSKOTT data are real.
3. Views (16 + the top view for lux maps) and the rooms each one sees are in `groups.json` → `views`; cameras in `Claude-tools/cams.txt` (the only camera list).
4. One command per version: `Claude-tools/blender/render_version.sh vPREV vNN [samples]` (export, lights, inputs, `rerender.py`, Blender in the background). `rerender.py` re-renders only the views that see a changed room (plus the top view) and hard-links the rest from vPREV; `--full` as 4th argument renders everything. Wait for `S15 done` in `render/blender/out/run-vNN.log`.
5. `<venv>/bin/python Claude-tools/blender/mix.py render/blender/out Renders/blender-lighting "S15 lighting – vNN" vNN` writes the sheets, `luxmaps-vNN.png`, `lux_table-vNN.md` and `light-mixer-vNN.html`. Then `python3 Claude-tools/make_site.py vNN` writes `index.html`.
6. Check the mixer with headless Chrome: `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --screenshot=x.png --window-size=1500,1100 --virtual-time-budget=8000 "file://…/light-mixer-vNN.html#view=lux"`.
7. Units are verified (`calib.py`): lux values are exact for the given lamp data. Night pictures use one fixed exposure and white balance (`blender/tm.py`); the day pictures get a neutral white balance and their own exposure (factor printed by `mix.py`).
8. Speed: about 25 s per render at 1440×1080 (v20: 51 renders). From v21 `s15_blender.py` keeps the scene between renders (persistent data), which should cut that further; not measured yet.
9. Known limits: lamps are invisible sources (fixtures don't glow, LED sources show as dots in mirrors); no IES beam files; the kitchen worktop is partly hidden from the top view by the wall cabinets; `rerender.py` ignores light leaking through open doors into rooms no stale view lists.

## Publishing (GitHub, public)
- Repo `github.com/ZSvedic/S15-flat`, branch `main`; GitHub Pages serves it at `https://zsvedic.github.io/S15-flat/`. Zel sends that link to other people.
- This folder is the repo. Everything that `.gitignore` does not list becomes public on push, including `journal.md` and this file: keep private matters out of them (no lock hardware, keys, e-mail addresses).
- **Git-ignored, never publish:** `render/`, `private/`, `Claude-tools/jars/`, `Claude-tools/blender/lights.json`, `*.exr`, `*.blend`. Nothing from the Drive root (`Building-docs/`, `Hrneticka-photos/`, `Ugovori/`) goes into a tracked path.
- **Commit and push only when Zel asks.** `gh` (`/opt/homebrew/bin/gh`) is logged in as ZSvedic.
- **To update:** 1. `make_site.py vNN` (index) and the version in `README.md`; 2. `git status`, check nothing private is listed; 3. `git add -A && git commit && git push`; 4. wait for `gh api repos/ZSvedic/S15-flat/pages/builds/latest` to say `built`, then `curl` the site and the mixer for 200.

## Workflow for a model change
1. Write `Claude-tools/build_vNN.py` that turns the previous version's Home.xml into the new one.
2. Zip it into a new `.sh3d` with `Claude-tools/make_sh3d.py` from the previous `.sh3d` (it keeps all models, including `v15/quarter_round.obj` and `v19/beanbag.obj`; add a new own model as `entry=path`).
3. Load it with `S15Tool.java check`.
4. Make the plan with `plan_svg.py` into `Claude-vectors/`.
5. Make low-quality previews into `Renders/sh3d-low/` with the version in the file names, then show Zel the overview. For lighting questions use the Blender workflow instead.
6. Only after Zel approves the previews: Nano Banana renders (mood pictures only; never for lighting).
7. Update `journal.md`, and `S15-furnishing-notes.md` if design decisions changed.
