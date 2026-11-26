# S15 toolchain

Everything needed to edit, draw and render the Sweet Home 3D model without the GUI. All of it runs on the Mac (Claude Code's Bash). Older build scripts (v12–v17), the v14 render method and the Linux VM render script are in the git history.

| File | What it does |
|---|---|
| `build_vNN.py` | previous Home.xml → version NN (one script per version; the last two are kept) |
| `make_sh3d.py` | packs a Home.xml into a new `.sh3d` using the models of an existing one; extra files as `entry=path` (e.g. `v19/beanbag.obj=Claude-tools/models/beanbag.obj`, only when the model is new) |
| `models/` | own models: `quarter_round.obj` (v15), `beanbag.obj` (v19) |
| `S15Tool.java` | `check` (loads a .sh3d with SH3D's own reader), `plan`, `render` (SunFlow, LOW/HIGH) |
| `ExportObj.java` | headless OBJ export of a `.sh3d` for Blender |
| `plan_svg.py` | Home.xml → vector plan (`.svg` + `.png`): walls, openings, door swings, furniture, as-built points (red), ceiling lamps (amber ⊗) |
| `cams.txt` | **the one camera list** (SH3D and Blender): x y z(eye) yaw pitch fov; yaw 0 = looking south, 90 = west, 180 = north, 270 = east |
| `make_site.py` | writes `index.html` for one version from `blender/groups.json` and the result files |
| `run_render_mac.sh` | SH3D render on the Mac, `ENGINE=yafaray` or `sunflow` |
| `lights_off.py` | day copy of a Home.xml for SH3D previews |
| `nano_banana.py` | SH3D previews → photoreal mood images via OpenRouter (never for lighting) |
| `overlay_architect.py`, `electrical_grid.py` | model over the architect plan / the electrical plan with a model grid |
| `jars/` | Sweet Home 3D jars (git-ignored; copy from a Sweet Home 3D 7 installation) |

Java on the Mac: `/opt/homebrew/opt/openjdk/bin/java --add-exports java.desktop/com.apple.eio=ALL-UNNAMED -Duser.home=<writable dir> -Djava.awt.headless=true -Dj3d.rend=noop -cp "$(ls jars/*.jar | tr '\n' ':')" S15Tool.java check <file>` (source-file mode, run from `Claude-tools/`). `plan_svg.py` and `mix.py` need a venv with matplotlib, pillow, numpy and opencv-python-headless.

## Blender lighting pipeline (`blender/`)
| File | What it does |
|---|---|
| `groups.json` | lamp data per role; the **three light groups** (ambient, ceiling, day) with the lamp sets they contain; day settings (place, date, time, plan north, sun and sky lux); room boxes; views with their area and the rooms they see; sheet panels; presets |
| `make_lights.py` | Home.xml → `lights.json`: name prefix → lamp set and role (table `RULES`); `-> x,y,z` aims a lamp; `… bar x|y|z:` = 4 sources 5 cm apart |
| `s15_blender.py` | rebuilds the scene from the OBJ export and renders one linear picture per group and view (`<group>/<view>-<tag>.npy`); day = sun + calibrated sky, glass lets shadow rays through; skips files that exist |
| `rerender.py` | incremental renders: finds the views a model change makes stale and hard-links all other renders from the previous version |
| `render_version.sh` | one command: export, lights, inputs, `rerender.py`, Blender in the background |
| `mix.py`, `tm.py`, `mixer_template.html` | sums group renders into comparison sheets, lux maps, lux table and the self-contained light mixer |
| `calib.py` | unit check of the lux values against a scene with a known answer |

A new version: `Claude-tools/blender/render_version.sh v20 v21` → wait for `S15 done` in `render/blender/out/run-v21.log` → `mix.py render/blender/out Renders/blender-lighting "S15 lighting – v21" v21` → `python3 Claude-tools/make_site.py v21`.
