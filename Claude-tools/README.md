# Hrnetička toolchain

Everything needed to edit, draw and render the Sweet Home 3D model without the GUI. All of it runs on the Mac (Claude Code's Bash). Older build scripts (v12–v17), the v14 render method and the Linux VM render script are in the git history.

| File | What it does |
|---|---|
| `build_vNN.py` | previous Home.xml → version NN (one script per version; the last two are kept: v21, v22) |
| `make_sh3d.py` | packs a Home.xml into a new `.sh3d` using the models of an existing one; extra files as `entry=path` (e.g. `v19/beanbag.obj=Claude-tools/models/beanbag.obj`, only when the model is new) |
| `models/` | own models: `quarter_round.obj` (v15), `beanbag.obj` (v19) |
| `S15Tool.java` | `check` (loads a .sh3d with SH3D's own reader), `plan`, `render` (SunFlow, LOW/HIGH) |
| `ExportObj.java` | headless OBJ export of a `.sh3d` for Blender |
| `plan_svg.py` | Home.xml → vector plan (`.svg` + `.png`): walls, openings, door swings, furniture, as-built points (red), ceiling lamps (amber ⊗) |
| `cams.txt` | **the one camera list** (SH3D and Blender): x y z(eye) yaw pitch fov; yaw 0 = looking south, 90 = west, 180 = north, 270 = east |
| `make_site.py` | writes `index.html` for one version from `blender/groups.json` and the result files; `REPO` at the top is the GitHub repository the page links to |
| `electrician.py` | files for the electrician in Croatian from one point table: outlet list (`Claude-vectors/Hrneticka-elektricar-vNN.md/.html`, PDF via headless Chrome) and a schematic (`…-shema.svg/.png/.pdf`: plan with cable routes, then one elevation per wall). Distances to the nearest corner or opening edge come from the model |
| `build_lightset.py` | fixture list → fixtures and lights with lamp data in the name (`XA:`/`XC:`), used for the v21 expert branches |
| `run_render_mac.sh` | SH3D render on the Mac, `ENGINE=yafaray` or `sunflow` |
| `lights_off.py` | day copy of a Home.xml for SH3D previews (kept for SH3D day previews) |
| `nano_banana.py` | SH3D previews → photoreal mood images via OpenRouter (never for lighting) |
| `overlay_architect.py`, `electrical_grid.py` | model over the architect plan / the electrical plan with a model grid (kept: needed when checking positions and wall materials) |
| `jars/` | Sweet Home 3D jars (git-ignored; copy from a Sweet Home 3D 7 installation) |

Java on the Mac: `/opt/homebrew/opt/openjdk/bin/java --add-exports java.desktop/com.apple.eio=ALL-UNNAMED -Duser.home=<writable dir> -Djava.awt.headless=true -Dj3d.rend=noop -cp "$(ls jars/*.jar | tr '\n' ':')" S15Tool.java check <file>` (source-file mode, run from `Claude-tools/`). `plan_svg.py` and `mix.py` need a venv with matplotlib, pillow, numpy and opencv-python-headless.

## Blender lighting pipeline (`blender/`)
| File | What it does |
|---|---|
| `groups.json` | lamp data per role; the **three light groups** (ambient, ceiling, day) with the lamp sets they contain; day settings (place, date, time, plan north, sun and sky lux); room boxes; views with their area and the rooms they see; sheet panels; presets |
| `make_lights.py` | Home.xml → `lights.json`: name prefix → lamp set and role (table `RULES`); `-> x,y,z` aims a lamp; `… bar x|y|z:` = 4 sources 5 cm apart; `{lm= beam= k= r=}` in any light name overrides the role's lamp data (v22: mirror border lights) |
| `s15_blender.py` | rebuilds the scene from the OBJ export and renders one linear picture per group and view (`<group>/<view>-<tag>.npy`); day = sun + calibrated sky, glass lets shadow rays through; skips files that exist |
| `rerender.py` | incremental renders: finds the views a model change makes stale and hard-links all other renders from the previous version |
| `render_version.sh` | one command: export, lights, inputs, `rerender.py`, Blender in the background |
| `mix.py`, `tm.py`, `mixer_template.html` | sums group renders into comparison sheets, lux maps, lux table and the self-contained light mixer |
| `calib.py` | unit check of the lux values against a scene with a known answer |

A new version: `Claude-tools/blender/render_version.sh v21 v22 64` → wait for `S15 done` in `render/blender/out/run-v22.log` → `mix.py render/blender/out Renders/blender-lighting "Hrnetička lighting – v22" v22` → `python3 Claude-tools/make_site.py v22`. Models are `Hrneticka-vNN.sh3d` from v21 on (the `S15` prefix was dropped on 2026-11-28; internal code names such as `S15Tool.java`, `s15_blender.py`, `S15_TAG` and the log line `S15 done` stay).

Day pictures use one fixed exposure, `DAYK = 0.0234` in `mix.py` (v22 on), so they compare between versions.

### Render speed (measured 2026-11-28, one view at 1440×1080, Apple M4 GPU, Metal)
| Setting | Time |
|---|---|
| 1 sample | 4 s |
| 64 samples (the default since v20) | 30 s |
| 256 samples | 134 s |
| 64 samples, denoiser off | 30 s |
| 64 samples, adaptive noise threshold 0.03 instead of 0.01 | 32 s |
| 64 samples on the CPU | 176 s |

So the time is path tracing (about 0.45 s per sample with about 560 light sources), not the denoiser or scene sync; the GPU is used. The earlier note "independent of samples" was wrong. The only cheap lever left is fewer samples (32 should halve the time; check the noise first), and the incremental renders of `rerender.py`.
