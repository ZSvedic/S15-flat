# S15 toolchain (fast iteration)

Everything needed to edit, draw and render the Sweet Home 3D model without the GUI.

| File | What it does | Where it runs |
|---|---|---|
| `build_v12.py` | v10 Home.xml → v12 Home.xml (confirmed shell fixes). Pattern to copy for later versions. | any Python 3 |
| `plan_svg.py` | Home.xml → vector plan (`.svg` + `.png`): walls, openings with w/h/sill, swings, rooms, furniture | Python 3 + matplotlib |
| `S15Tool.java` | `check` (loads .sh3d with SH3D's own reader), `plan`, `render` (SunFlow photo renderer, LOW/HIGH) | Java 11 + `jars/` (copied from the SH3D app) |
| `run_render.sh` | wraps `S15Tool.java render` in a virtual display (Linux: needs `xvfb-run`) | Linux |
| `cams.txt` | named camera views: x y z(eye) yaw pitch fov. yaw 0 = looking south, 90 = west, 180 = north, 270 = east | |
| `nano_banana.py` | SH3D previews → photoreal images with Nano Banana 2 (`google/gemini-3.1-flash-image`) via OpenRouter; adds a site photo as material reference per view. Key from `OPENROUTER_API_KEY` or TamedTable/.env | Mac (python3 + sips) |

## Typical loop (≈2 min for 12 views)
1. Edit Home.xml (script), zip back into `.sh3d` (drop `Home` and `ContentDigests` entries).
2. `python3 plan_svg.py Home.xml S15-vNN-plan "title"` → ~5 s
3. `./run_render.sh S15-vNN.sh3d cams.txt outdir 1024 768 LOW [view,view]` → 10–30 s per view
4. `python3 nano_banana.py outdir ../Hrneticka-photos ../Renders-vNN/nano-banana-2 [view,...]` → ~10 s and ~$0.07 per view (6 in parallel)

Gotchas: renders need `home.setCamera(observerCamera)` (already in S15Tool) or ceilings are missing; `-Dj3d.rend=noop` avoids native GL libs.

Note (2026-11-18): `nano_banana.py` now falls back to Pillow when `sips` is missing. It still needs network access to openrouter.ai (see `../AGENTS.md`). Paths in the loop above are relative to the repo root (`~/LOCAL/CODE-2026/S15-flat/`, the former `Interior-design/`); the photos are in the Drive folder `Hrneticka/Hrneticka-photos`.

## Added for v13 (2026-11-18)
| File | What it does |
|---|---|
| `build_v13.py` | v12 Home.xml → v13 Home.xml: walls per architect plan, opening fixes, niche, shaft boxes, lights |
| `lights_off.py` | makes a day copy of Home.xml with the v13 lights off (spots in windowless rooms stay on) |
| `cams-v13.txt` | the 12 views plus `13-hall-to-living` and `14-corridor-niche` |
| `overlay_architect.py` | draws a Home.xml over the architect plan (needs `arch300.png`: the plan PDF rendered at 300 dpi, in the working folder) |
| `electrical_grid.py` | renders the S15 part of the electrical plan with a model-coordinate grid; arguments `32.08 296.88` |

`run_render.sh` now passes `$JOPT` to Java, for example `JOPT="-Dt=1792616400000"` for a night render.

## Added for v14 and lighting (2026-11-18/19)
| File | What it does |
|---|---|
| `build_v14.py` | v13 Home.xml → v14: light groups "AMBIENT A" (Zel's wall-light points) and "AMBIENT B" (kitchen under-cabinet) |
| `make_sh3d.py` | packs a Home.xml into a new `.sh3d` using the models of an existing one |
| `ExportObj.java` | headless OBJ export of a `.sh3d` for Blender (run like `S15Tool.java`, with xvfb) |
| `run_render_mac.sh` | Mac-native SH3D render, `ENGINE=yafaray` or `sunflow` (needs OpenJDK) |
| `blender/` | lighting pipeline; see "Workflow for lighting variants" in `../AGENTS.md` |

## Added for v15 (2026-11-19)
| File | What it does |
|---|---|
| `build_v15.py` | v14 Home.xml → v15: Zel's review items a–j (art lights, kitchen bar, niche shelves, desk work light, bedroom corner) |
| `models/quarter_round.obj` | quarter-round seat model; pack it with `make_sh3d.py … v15/quarter_round.obj=models/quarter_round.obj` |
| `make_sh3d.py` | now takes extra files as `entry=path` |
| `blender/groups.json` | replaces `variants.json`: lamp data, light groups, which groups each view needs, sheet panels, presets |
| `blender/s15_blender.py` | now renders one linear picture per light group and view (`<group>/<view>.npy`); resumable |
| `blender/mix.py`, `tm.py`, `mixer_template.html` | sums group renders into comparison sheets, lux maps, lux table and the self-contained light mixer page; a version tag as the 4th argument goes into the file names (`light-mixer-v16.html`) |

`blender/variants.json`, `compare.py` and `luxmap.py` are the v14 method (one render per fixed variant) and are no longer used.

## Added for v16 (2026-11-19)
- `build_v16.py`: v15 Home.xml → v16 (picture lights, low lamps, hall seat and mirror, niche profiles, curved pendant).
- `blender/make_lights.py`: any light named `<Group> bar x|y|z:` is expanded into 4 sources 5 cm apart; rules table updated.
- `blender/groups.json`: new lamp roles (`piclight`, `profile`, `pbar`, `lowbar`, `tablelamp`), `mirrors` (points where a frame's glass becomes a real mirror in Blender), presets can carry a dim level `w`.
- Renders are now 1440×1080 (about 27 s each).
