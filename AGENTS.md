# AGENTS.md: S15 Hrnetićka interior design

Read this file and `journal.md` (to the end) before doing anything. At the end of every session, add an entry to `journal.md`.

## Current state (2026-11-19, late evening)
- **Latest model: `S15-Hrneticka-v16.sh3d`** = v15 + Zel's answers to the critique: picture lights over paintings, low lamps on switched sockets, kitchen bar 12 from the wall, laundry light on the south wall, niche shelf profiles, hall seat + mirror + T-wall artwork, IKEA PILSKOTT pendant. Waiting for his review.
- **Current task:** find positions for ambient lights so Zel can tell the electrician where to drill. The deliverable at the end is a drill sheet (wall, distance from a corner, height). Draft: `Claude-vectors/S15-wall-light-points-DRAFT.md` (fixed lights, switched sockets, dimming groups, closet feeds).
- **How Zel reviews lighting:** `Renders-v16/blender-lighting/light-mixer.html` (switches and dimmers per light group, any view, lux map) plus the `compare_*.jpg` sheets and `luxmaps.png`. He can't judge light in SH3D.
- **Waiting for Zel:** review of v16. Open in the draft: real picture sizes (they set the picture-light heights), curtain positions near lights 1, 14, 16, low-lamp corners, lamp data for everything except the GU10 and the two PILSKOTT lamps.
- **Critique of v15:** `Claude-vectors/S15-v15-critique.md`. Zel accepted points 1–7 with changes (journal 2026-11-19 c). Not taken up: softer up-lamps, bedside reading lights, room 5 light spacing, night light.

## Owner rules (Zel)
- Ask for confirmation before any drastic change to models or files. Propose a before → after list with the evidence for each item, then wait.
- **When sources conflict, trust them in this order:**
  1. Zel's latest site photos with measurements (`../Hrneticka-photos/`): the real flat as built.
  2. Architect and engineer drawings (`../Building-docs/`).
  3. Old files, the marketing catalogue and screenshots.
- If a conflict can't be settled by evidence, list it and ask. Never pick silently.
- Short answers, metric units, options labelled A/B/C, steps 1/2/3.
- Never edit a model in place: each version is a new file, `S15-Hrneticka-vNN.sh3d`.

## Folder map (root = `My Drive/Zeljko/Real estate/Hrneticka/`)
| Path | What |
|---|---|
| `Interior-design/S15-Hrneticka-vNN.sh3d` | Sweet Home 3D model. The latest version is the source of truth. |
| `Interior-design/Claude-tools/` | Toolchain: build scripts, plan drawing, headless renderer, Nano Banana. See its README. |
| `Interior-design/Claude-vectors/` | Plan drawings (`S15-vNN-plan.svg/png`), `S15-interior-spec.md` (Zel's wishes), `S15-furnishing-notes.md` (design decisions per version) |
| `Interior-design/Renders-vNN/` | `sh3d-low/` previews and `nano-banana-2/` photoreal renders; from v14 also `blender-lighting/` (comparison sheets, lux maps, lux table; from v15 also `light-mixer.html`) |
| `Interior-design/Claude-tools/blender/` | Blender lighting pipeline: `make_lights.py`, `groups.json`, `s15_blender.py`, `mix.py`, `tm.py`, `mixer_template.html`, `calib.py` (`variants.json`, `compare.py`, `luxmap.py` are the old v14 method) |
| `Interior-design/Claude-vectors/S15-wall-light-points-DRAFT.md` | All proposed light points (Zel's 17 circles plus the v15 additions), with wall distances, heights and open points |
| `~/LOCAL/S15-render/` (on the Mac, not in Drive) | Hand-over folder for Mac-side rendering. Must be connected to the session together with the Drive folder. |
| `Interior-design/Zel-sketch-v1.jpeg` | Zel's furniture sketch |
| `Building-docs/S15-architect-plan.pdf` | Architect plan of the flat, vector, 1:50, cropped from p. 4 of `Hrnetička-all-floors.pdf` |
| `Building-docs/Electrical Installation Plan S15.png` | Electrical plan, lights and sockets (from `Mapa III_Elektrotehnički projekt.pdf`, which also has the legend) |
| `Hrneticka-photos/<room>/` | Site photos, many with tape measures |
| `Claude-vectors/S15-handoff-prompt.md` | Obsolete (old paths and brief). Ignore it. |

## Fixed facts (confirmed by Zel; don't re-litigate)
- **Hallway → living room:** no door; open passage with a wall header from 210 cm up. The architect plan's 90/210 door was not built.
- **Second bathroom:**
  - The door is in the north wall, from the hallway, 70 wide. Both the architect and electrical plans show it wrong.
  - WC on the west wall, basin on the east wall, bath across the south.
- **Ceiling:** 280.
- **Windows:** 170 high with a 90 cm sill.
- **Bedroom north opening:** 300×245 three-panel window on a 15 cm sill; the middle panel opens to the balcony.
- **Sara's room:** two terrace exits:
  - east door 80×240 on a 20 cm threshold;
  - south double door 160×250 on a 10 cm sill.
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
- **Zel's Mac** (Drive folder): reachable through the device bridge. If `~/LOCAL/S15-render` is not connected, ask for it with the folder-access tool. The bridge shell (`device_bash`) is a Linux VM with Java 11, xvfb, Python and Pillow, and the folders mounted under `$HOME/mnt/`. Run the SH3D tools there. It has no GPU and no internet. Files cannot be deleted in connected folders: write to a new folder name instead.
- **Mac-native shell** (`MacOS-MCP Shell` tool): needed for Blender and YafaRay.
  - It cannot read the Google Drive folder (macOS privacy). Copy inputs to `~/LOCAL/S15-render/` from the VM (`$HOME/mnt/S15-render`), run on the Mac, copy results back to Drive from the VM.
  - A call times out after about 80 s: start jobs with `nohup … &` and poll the log (the VM can read it with `sleep 170; grep …`).
  - Installed: Blender 5.3 (`/Applications/Blender.app/Contents/MacOS/Blender`), OpenJDK (`/opt/homebrew/opt/openjdk/bin/java`). Mac is an Apple M4.
- **Nano Banana (OpenRouter):** `openrouter.ai` is not reachable from the VM or the cloud container. It needs a Mac-native shell (Desktop Commander) or openrouter.ai on the allowed-domains list. The key is in `~/LOCAL/CODE-2026/TamedTable/.env` on the Mac; never print it.
- **Google Drive sync** can serve a stale copy of a file you've just written. After copying, check the content (grep for a new line) before using it.
- **SH3D rendering:**
  - `S15Tool.java` sets the observer camera (otherwise ceilings are missing) and a fixed daytime: Java property `-Dt=<epoch ms>`.
  - Light sources render at LOW and HIGH. Night: `JOPT="-Dt=1792616400000" ./run_render.sh …` (23:00). Day previews: build a copy with `lights_off.py` first.
  - A bridge call lasts at most 180 s and background jobs die when it returns: render 3–4 views per call.
  - Never leave `widthInPlan`/`depthInPlan`/`heightInPlan` on a resized door or window: SH3D cuts the wall hole from them.

## Workflow for lighting (Blender, from v15)
Light adds up, so each light group is rendered once per view and any on/off or dimmed mix is the sum. Never render fixed variants.
1. Lights live in the `.sh3d`. The name prefix decides the light group and lamp type (table `RULES` in `blender/make_lights.py`): `AmbA up/down:` (wall), `ArtE/ArtH/ArtSw up/down:`, `ArtSc aim:`, `Desk aim:`, `TV puck:`, `Kitchen bar x|y:`, `Niche back z:`, `Niche puck:`, `Light: …` (ceiling, spots, pendants). A name ending in `-> x,y,z` aims the lamp at that model point.
2. Lamp data, groups, which groups each view needs, sheet panels and presets are in `blender/groups.json`. Only the GU10 data is real; the rest is assumed.
3. In the VM: `ExportObj.java <model.sh3d> <new dir>/s15.obj`, then `blender/make_lights.py Home.xml lights.json`.
4. Copy the obj folder, `lights.json`, `groups.json`, `cams.txt` and `s15_blender.py` to `~/LOCAL/S15-render/blender/vNN/`. On the Mac: `nohup Blender -b -P s15_blender.py -- . <obj dir> ../outNN 1024 768 128 [views] [groups] > log &`. At 1440×1080 about 27 s per render (v16: 97 renders, 45 minutes); Zel asked for this resolution or higher. Finished renders are skipped, so a new view needs a new name.
5. In the VM: `blender/mix.py ~/mnt/S15-render/blender/outNN <Renders-vNN/blender-lighting> "<title>"` writes the sheets, `luxmaps.png`, `lux_table.md` and `light-mixer.html` (self-contained, 4 MB).
6. Check the page with headless Chrome on the Mac: `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --screenshot=x.png --window-size=1500,1100 --virtual-time-budget=8000 "file://…/light-mixer.html#view=lux"`.
7. Units are verified (`calib.py`): lux values are exact for the given lamp data. Pictures use one fixed exposure and white balance (`blender/tm.py`).
8. Known limits: lamps are invisible sources (fixtures don't glow, but LED sources show as dots in mirrors); if a new lamp changes a fixture's shape, re-render every group for the views that see it; no manufacturer beam files (IES); the kitchen worktop is partly hidden from the top view by the wall cabinets.

## Workflow for a model change
1. Write `Claude-tools/build_vNN.py` that turns the previous version's Home.xml into the new one.
2. Zip it into a new `.sh3d` with `Claude-tools/make_sh3d.py` (drops the `Home` and `ContentDigests` entries). From v15 add `v15/quarter_round.obj=models/quarter_round.obj`.
3. Load it with `S15Tool.java check`.
4. Make the plan with `plan_svg.py` into `Claude-vectors/`.
5. Make low-quality previews into `Renders-vNN/sh3d-low/`, then show Zel the overview. For lighting questions use the Blender workflow instead.
6. Only after Zel approves the previews: Nano Banana renders (mood pictures only; never for lighting).
7. Update `journal.md`, and `S15-furnishing-notes.md` if design decisions changed.
