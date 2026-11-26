# S15 Hrnetička: v8 / v9 notes

Written 2026-10-20. v8 is built on `S15-Hrneticka-v3.sh3d` and follows `Zel-sketch-v1.jpeg`:
- dining without an island;
- standard furniture sizes, not specific products;
- your pictures and decor taken from the old flat model `GIK-Kotarnica.sh3d`.

## Files
- `S15-Hrneticka-v9.sh3d`: the current model (v8 plus finishes, toggles, glass balustrade and Sara's terrace door). `S15-Hrneticka-v8.sh3d` is kept for comparison.
  - It loads in Sweet Home 3D's own reader (`HomeFileRecorder.readHome`).
  - The ZIP holds `Home.xml` only.
- Top views with clearances in cm:
  - `S15-v9-top-full.png`, `S15-v9-top-living.png`, `S15-v9-top-rooms.png`, `S15-v9-top-terrace.png`.
  - Green means the clearance meets the rule; red means it is below.
  - Purple dashed lines are door swings. Blue dashed lines are the sails and the opened sofa bed.
- `S15-renders-v9/`: 15 3D views. Views 00–07 are high quality; 08–14 are quick renders, so they look grainy.
  - Colours come out paler than the real materials.
  - Trees, lamps and cushions are generic catalog models.

## Layout (from the sketch), standard sizes in cm

### Kitchen
- **Layout:** L-shape with the hob on the north run. Sink and dishwasher are on the west run, with two tall units (oven + microwave, fridge) at the hallway end.
- **Colours:** grey base units, cream wall and tall units, oak worktop and oak backsplash, as in your current kitchen.

### Dining
- Table 200×100 with 7 chairs: 3 + 3 along the sides and 1 at the east end.
- Two pendants hang 75 cm above the table.

### Desk
- Desk 150×75, perpendicular to the north wall, just east of the kitchen window.
- The ergonomic chair is on its west side.
- On the desk: monitor, laptop, desk lamp.

### TV wall
- TV 85" (centre about x 1292, as before) on a 240 TV unit.
- Your two speakers stand on the unit.
- Your wooden wall panel is behind the TV.

### Sofa
- Corner sofa 300×230, long leg along the south wall, short leg along the east wall.
- Oval coffee table 120×70 and a 260×200 rug.
- Cushions, a side table with a lamp, and a wall shelf with books, vase and a trailing plant above the east leg.
- Floor lamp in the north-east corner.

### Master bedroom
- **Bed:** 160×200, headboard on the east wall, with two nightstands and your two wall lights.
- **Wardrobe:** 180×65 with sliding doors, 5 cm south of the ensuite door.
- **Pictures:**
  - your two Desenio prints above the bed;
  - a 60×80 print on the south wall.
- **Also:** a 200×280 rug and a plant.
- **Balcony door:** the north window is now a 182×220 door to the balcony.

### Ensuite
- Walk-in shower 160×80 instead of the bath (as in the sketch).
- Mirror over the two basins.

### Hallway
- Made-to-measure built-in wardrobe in the 181×56 niche.
- Shoe bench 120×32, with 4 black hooks above it.
- Your NISSEDAL full-length mirror.
- A 100×70 picture you see from the front door.
- A runner and 2 photo frames in the corridor.

### Laundry
- From west to east: heat pump, washer, dryer, tall cabinet.
- Shelf over the machines, ceiling drying rack, and laundry basket.

### Room 5
- **Furniture:** wardrobe 200×60 on the north wall, sofa bed 195×95 on the west wall (opens to 140×200), and desk 140×70 on the east wall.
- **On the desk:** monitor, laptop and lamp.
- **Pictures:** your Gnijezdo shelf print and a 70×100 picture above the sofa bed.
- **Also:** a guest reading light.

### Sara's room
- **Furniture:** bed 90×200 along the west wall, wardrobe 150×60 on the north wall, and desk 120×50 on the east wall.
- **South window:** two corner tub chairs (56×56) with a Ø45 side table and lamp.
- **Pictures:** her old poster and memo board, with a shelf above the poster.
- **Also:** cushions and a reading light.

### Terrace
- **Along the house:**
  - BBQ by the house wall;
  - outdoor sink between the laundry door and Sara's door (water from the laundry);
  - two wall lanterns.
- **Dining:** table 180×90 for 5, with 2 + 2 chairs and 1 at the end.
- **Lounge:** outdoor sofa 220×100 with cushions, oval table, a lounge chair and a sunbed on a 200×300 rug.
- **Storage:** cushion box 130×50 in the south strip.
- **Plants:** 5 trees in 60×60 planters.
- **Shade:** two triangular sails on a diagonal roller beam (house corner to house corner) plus one post. The sails stay clear of the BBQ corner.

### North balcony
- Bar-height bistro table Ø60 with 2 bar stools. A seated person can't see Sljeme over the 1.2 m parapet.
- Sunbed, two olive trees, and a wall lantern.

## Switching options in Sweet Home 3D (update 2026-10-20)
Sweet Home 3D has no option picker. Instead, each option is a furniture group, and the furniture list has a **Visible** column: tick or untick the group's checkbox there. The plan, the 3D view and photo renders all follow it.

| Group in the furniture list | Default |
|---|---|
| TERRACE FLOOR A – wood decking | on |
| TERRACE FLOOR B – tiles 60×60 | off |
| TERRACE FLOOR C – artificial grass | off |
| SHADE – sails extended | on |
| SHADE – sails rolled up on the beam | off |

- **Floors:** keep exactly one floor group on. Each floor group covers the terrace and the balcony together. With all three off you see bare screed.
- **Sails:** to roll them up, turn "sails extended" off and "sails rolled up" on.
- **Renders:** `S15-renders-v8/` has the terrace with the tiles and rolled-up sails, and with grass (11–14).

## Finishes (palette from your current flat, GIK-Kotarnica)
- **Base walls:** warm off-white #F0EFE6, your current wall colour. Outside walls are a light render colour #E6E1D8.
- **Ceilings:** #F7F6F2.
- **Floors:**
  - Your Pozga Arctic oak parquet in every living space and bedroom.
  - Grey ceramic tiles in both bathrooms and the laundry.
- **Accent walls** (thin paint or wallpaper layers named "Accent wall – …"):
  - **TV wall:** your plum-grey #5C5860, so the oak TV unit and wooden panel stand out.
  - **Bed wall in the master bedroom:** your teal-grey feather wallpaper "373733", which goes with the two Desenio prints.
  - **Sara's bed wall:** dusty rose #D9B8B2. I didn't reuse the flamingo wallpaper because it is a child's pattern; she is 17.
  - **Room 5 sofa-bed wall:** your blue #6D91B0.
- **Bathroom walls** (220 high):
  - Ensuite: white marble.
  - Second bathroom: grey ceramic tiles.
- **Furniture materials:**
  - Your oak texture on all oak pieces.
  - Your beige fabric on the living-room sofa.
  - Bleached wood on the dining chairs.
  - Your old argentum rug under the coffee table.
  - Your old IKEA VINDERÖD rug in Sara's room.
  - All new surfaces are matte.
- **Kitchen:** grey base units, cream upper units, oak worktop and backsplash.
- **Sara's south opening:** now a 161×220 double terrace door opening inward, as in your sketch, replacing the developer's window.
  - The side table stays centred between the chairs, as in the sketch; move it aside to use the door.
  - The cushion box moved to the south end of the outdoor sofa, so it doesn't block the door from outside.
- **Terrace balustrade:** glass panels, 110 high. The north balcony keeps a solid 1.2 m parapet.
- **Curtains:** removed. The sofa still stands 24 cm off the terrace glass, as in your sketch.

## Changes after the review subagent (acting on your sketch, spec and rules)
- **Doors and windows:**
  - Added the bedroom → balcony door, and moved the bed 10 cm south so the door leaves swing clear.
  - Desk chair moved out of the north window's swing.
- **Clashes fixed:**
  - Sara's poster lowered under her shelf; corner chairs made smaller so they don't poke into the walls or the bed.
  - Cushion box moved where it can be opened.
- **Sizes:**
  - Tall kitchen units made 240 high, to line up with the wall cabinets.
  - Hallway bench made shallower (corridor 73 cm).
  - Sara's desk made 120 wide.
- **Pendants:** lowered to 75 cm above the table.
- **Decor added:** cushions, lamps, kitchen accessories, and pictures in the hallway, bedroom and room 5.

## Still to check (only you or the builder can confirm)
1. **Bedroom door:** if it is hinged on the west side, its open leaf rests against the wardrobe. The plan assumes the east side.
2. **Sara's terrace door:** if it is hinged at the north end, the open leaf blocks the wardrobe. The plan assumes the south end.
3. **Terrace sliding door:** the sofa's south leg covers its east 147 cm. The free opening is 155 cm, which is fine if the west panel is the one that slides.
4. **Room 5:** on guest nights the desk chair has to move when the bed is open.
5. **Sails:** retract the north-west sail while grilling. Mounting on the building likely needs co-owner approval.

## v10 (2026-10-20)
`S15-Hrneticka-v10.sh3d` = v9 plus:
- **Corner sofa:** one continuous L-shaped sofa, 300×230, instead of two couches pushed together.
  - Shared corner seat, one backrest around both legs, an arm at each end.
  - It is a single group in the furniture list.
- **Ensuite:** walk-in shower 160×80.
  - Glass panel 100×200 on the north side, walk-in opening at the east end.
  - Mixer, riser and rain head on the west wall.
- **Sara's room:** the lamp on the side table is gone.
- **Desk lamps:** Sara's and room 5's desk lamps are turned so they stay on the desk instead of poking into the wall.

The renders in `S15-renders-v9/` show v9. The sofa, shower and lamp changes are not in them.

## v12 (2026-10-21): v10 + shell fixes confirmed by Zel
`Interior-design/S15-Hrneticka-v12.sh3d`, plan `Claude-vectors/S15-v12-plan.svg/.png`, built by `Claude-tools/build_v12.py`.
Sources, in trust order: site photos with measurements > architect plan (`Building-docs/S15-architect-plan.pdf`) > old files.

| Item | v10 → v12 | Evidence |
|---|---|---|
| Ceiling | 260 → 280 | plan section; shutter boxes above openings |
| Living → terrace sliding door | 302×220 at floor → 300×240 on 20 threshold | plan; photos IMG_2011, IMG_2012 (width not measured) |
| Laundry and Sara east doors | 73×220 / 80×220 → 80×240 on 20 threshold | plan; IMG_2026, IMG_2030, IMG_1962 |
| Sara south | 161×220 door → 160×250 double door, sill 10 | plan; IMG_1962, IMG_2032 |
| Windows living N, living E, room 5 | 202/221/158 × 134, sill 87 → 200/220/160 × 170, sill 90 | plan; IMG_1960, IMG_2024, IMG_2035 |
| Bedroom north | 182×220 door → 300×245 three-panel window, sill 15, middle opens | plan; IMG_1956, IMG_2020 |
| Hallway → living | open, full height → open, header strip from 210 up | IMG_2019, IMG_2025 |
| Bedroom south wall | – → ventilation shaft box 66×20 by the door | plan; IMG_2007, IMG_2008 |
| Bathroom 2 | door east wall, basin north → door north wall (70), basin east, WC west, pipe box by bath | plan; IMG_1958, IMG_2019, IMG_2014, IMG_2022 |
| Ensuite | – → tiled WC ledge 115 high | IMG_2021 |
| Bathroom tiles | white marble / grey 220 high → beige stone-look floor to ceiling | IMG_2014, IMG_2015, IMG_2021 |
| Terrace + balcony floor | ±0 → +16 (all outdoor furniture raised) | plan +9.16 vs +9.00; IMG_2026 |
| Balcony parapet | 120 → 100 above tiles; bar table + stools → table + 2 chairs | IMG_2005 (tape) |
| Terrace railing | glass 110 → 60 upstand + glass, top 117 | IMG_2010 (tape), IMG_2027 |
| Fixtures | tiles shown by default; tap; 2 wall lights (living facade, east facade) | IMG_2026, IMG_2029 |

Hallway items moved because of the bathroom door: shoe bench and hooks to the north wall, 100×70 picture to the west end; distribution board + media box added beside the bathroom door.

## v13 (2026-11-18): v12 + shell per architect plan + lights
`Interior-design/S15-Hrneticka-v13.sh3d`, plan `Claude-vectors/S15-v13-plan.svg/.png`, built by `Claude-tools/build_v13.py`. Confirmed by Zel on 2026-11-18.

### Shell
| Item | v12 → v13 | Evidence |
|---|---|---|
| Living → terrace door | wall hole 132×210 → 300×240 (stale `widthInPlan`/`heightInPlan` removed); door stays two-panel | Home.xml; IMG_2026, IMG_2029; IMG_2011/2012 tape (east edge about 166 from east wall, plan 169) |
| Sara south door | wall hole 132 wide → 160; centre x 728 → 734 | Home.xml; plan 107 / 160 / 8 |
| Room 5 window | centre x 371 → 378 | plan 73 / 160 / 79 |
| Front door | 100×208 → 105×215 | plan |
| Bedroom, Sara, room 5 doors | 85×208 → 80×210, positions per plan | plan |
| Ensuite, bathroom, laundry doors | height 208 → 210, positions per plan | plan |
| Hallway → living passage | 112 wide with header → north stub 10, opening 82×210, south stub 22 | IMG_2019, IMG_2025 (estimate ±5); plan 16 + 90 + 8 |
| Corridor west wall | solid → open niche 60 wide × 33 deep, full height (replaces the bathroom pipe-box piece; the box is now walls) | IMG_2017, IMG_1961, IMG_2015; plan shows a closed 28×65 shaft |
| Living SE corner | – → pipe box 14×20 | IMG_2011; plan 23×21 |
| Laundry NW corner | – → shaft box 22×46; heat pump moved 22 east, laundry basket to the south wall | plan only |
| Wardrobe niche | – → shaft box 29×28 in the NW corner; wardrobe 181 → 152 | plan only |
| Walls | all re-snapped to plan (anchor: living NE inner corner); partitions 11.8 → 10 (12.5 for bathroom north wall and laundry/Sara wall) | vector overlay, `overlay_architect.py` |
| Room sizes | Sara N–S 394 → 386; laundry N–S 161 → 166; living E–W 854 → 851; bathroom 201×225 → 200×223; corridor 101 → 102 | plan dimension chains |
| Terrace upstand inner faces | west 645 → 654, east 1409 → 1402 (46.8 → 46.0 m²) | plan (46.16 m²) |
| Balcony west parapet inner face | 15 → 21 (18.86 → 18.73 m²) | plan (18.72 m²) |

Model room areas now: living 39.84 (plan 39.77), bedroom 12.74 (12.63), ensuite 5.26 (5.26), bathroom 4.27 (4.24), laundry 4.55 (4.46), Sara 10.61 (10.61), room 5 9.85 (9.85).

### Lights (28 new light sources, names start with `Light:`)
| Room | Points | Source |
|---|---|---|
| Kitchen / living | ceiling lamps at (734, 488), (1297, 536), (950, 735); the dining point feeds the two pendants | photos IMG_1959, 1960, 2024, 2025; electrical plan |
| Bedroom | ceiling lamp (418, 478) | IMG_1956; plan |
| Room 5 | ceiling lamp (382, 1211) | IMG_1963; plan |
| Sara | ceiling lamps (683, 1156) and (790, 1150) by the east door | IMG_1962, IMG_2032 |
| Hall | 5 recessed spots, y 713, x 90 / 195 / 300 / 405 / 510 | IMG_2018 (±20) |
| Corridor | 2 recessed spots (486, 870), (486, 990) | IMG_1961 (±20) |
| Laundry | 6 recessed spots, x 615 / 685 / 755, y 835 / 900 | IMG_2030 (±20) |
| Ensuite | IP44 ceiling lamp (132, 453); mirror light on the north wall at 200 | electrical plan (no ceiling photo) |
| Bathroom | IP44 ceiling lamp (326, 889); mirror light above the basin on the east wall at 200 | electrical plan; basin position as built |
| Terrace | the two installed wall lamps now give light | IMG_2026; electrical plan |

Fixtures are placeholders (white boxes Ø30 / 9×9). Powers were tuned for the night previews: ceiling lamps 0.25, spots 0.1 (laundry 0.05), bathrooms 0.07–0.08, mirror 0.03, pendants 0.18, terrace 0.2.

## v15 (2026-11-19): Zel's review of the v14 lighting

Built by `Claude-tools/build_v15.py` from v14. Zel's letters (a–j) are from his review message.

| Item | Before (v14) → after (v15) | Source |
|---|---|---|
| a | Up/down lamp: assumed 350 lm at 40° or 110° → IKEA LEDARE LED1931R5 GU10: 345 lm, 2700 K, 36°, 600 cd, dimmable. No narrow/wide variants. | Zel's photo of the lamp pack |
| b | Living desk: shelf 76×22 with 2 pucks → ceiling track with 2 GU10 heads, 75 from the north wall: one down on the desk, one on the picture | Zel |
| c | Living east wall: book shelf 180 with plant, books, vase and one wall light → painting 150×70 (placeholder, bottom at 125) with 2 up/down wall lights above it at 220 | Zel |
| d | Living south wall: one wall light overlapping the east end of the Canadair picture → two option groups: 3 up/down wall lights above the picture at 222, or 3 ceiling spots 60 from the wall | Zel ("from the wall or reflectors on the ceiling") |
| e | Kitchen: 8 pucks under the wall cabinets → LED light bars at the back edge (north 56 + 78 either side of the hood, west 168) | Zel's photo of his current kitchen |
| f | Bedroom NW corner: plant → clothes rail with 3 hooks on the north wall (top 170), quarter-round corner seat r 50, h 45, wall light raised from 175 to 205 | Zel |
| g | Room 5: desk 140×70 with drawer → desk 160×75 without drawer (3 cm from the south wall); wall lights moved to 62 either side of the desk centre | Zel |
| h | Sara: wall lights at 220 and 42 from the south wall → 45 either side of the desk centre (219 and 129 from the south wall); desk unchanged | Zel |
| i | Corridor niche: one ceiling puck → 5 oak shelves 60×27 (tops at 52, 97, 142, 187, 232) with art pieces; two option groups: 2 vertical LED strips behind the shelves, or a small downlight under each shelf | Zel |
| j | Hall entrance: picture 100×70 → renamed artwork, lowered 5 (bottom 135), 2 up/down wall lights above it at 222 | Zel |
| – | Fuse and network boxes: NOT moved. Model and photos IMG_1958 / IMG_2019 have them west of the bathroom door; Zel first wrote "east", then confirmed west. | photos, Zel |

SH3D groups: "AMBIENT A" (wall, art, desk, TV), "AMBIENT B" (kitchen bar), "ART SOUTH option 1/2", "NICHE – shelves", "NICHE option 1/2".

## v16 (2026-11-19): Zel's answers to the critique, hall reshuffle

Built by `Claude-tools/build_v16.py` from v15. Numbers are Zel's numbering in his message.

| Item | Before (v15) → after (v16) | Source |
|---|---|---|
| 1 | Dimmers on every group: no model change; groups listed in the light-points draft | critique, Zel |
| 2 | No low lamps → three IKEA PILSKOTT LED floor lamps (112 high, 700 lm) (living SE corner behind the sofa, living NE corner replacing the floor lamp, bedroom SE corner) and a lit table lamp on the side table, all on switched sockets | critique, Zel; lamp model from Inge (ikea.com/hr 904.781.20) |
| 3 | Kitchen light bar at the back edge (7 from the wall) → 12 from the wall (1/3 of the 37 cabinet depth) | Zel |
| 4 | Laundry wall light on the east wall between cabinet and terrace door → south wall, 120 from the west wall, at 175, opposite Sara's socket (electrical plan: socket at model x 667) | Zel, electrical plan |
| 5 | South picture: two options → 3 ceiling spots only | Zel |
| 6 | Niche: back strips or shelf downlights → LED profile under the front edge of each shelf and the niche ceiling, shining down and back | critique, Zel |
| 7 | Paintings lit by up/down GU10 cylinders → overhead picture lights (brass tube on an 18 cm arm): 60 wide over the east painting, 45 wide over the hall artwork | Zel's photo, Pooky guide (width 1/3–1/2 of the picture) |
| 8 | Circle 4 and a new laundry point are feeds for closet interior lights; no fixture in the model | Zel |
| 9a | Hall niche: built-in wardrobe 152×56×278 → seat 152×45×45 with sliding doors (shoe shelves), cushion, oak hanger panel 49–190 with 7 hangers at mixed heights, top cabinet 152×50 from 190 to the ceiling, LED bar hidden behind its front | Zel |
| 9b | Hall south wall: artwork 100×70 with 2 wall lights and mirror 65×150 → one mirror 120×170 opposite the seat (bottom at 20) | Zel |
| 9c | Hall north wall at the T: shoe bench and 4 coat hooks → vertical artwork 90×140 (placeholder, bottom at 55) with a picture light | Zel |
| 10 | Dining: 2 dome pendants → one IKEA PILSKOTT LED pendant 97 long (1,100 lm), west half at 168, east half at 158 (undersides) | Zel's photo, model from Inge (ikea.com/hr 304.778.78) |

SH3D groups: "AMBIENT A", "AMBIENT B" (kitchen bar), "ART SOUTH", "NICHE – shelves", "NICHE – LED profile", "DINING – curved linear pendant", "LOW LAMPS", "HALL – seat…".

## v17 (2026-11-25): site photos IMG_2455–2488, door hall → living

Built by `Claude-tools/build_v17.py` from v16. Photos are in Drive `Hrneticka-photos/<room>/`. Only facts from the photos and Zel's new door were changed; design conflicts the photos revealed are listed below and NOT changed (they wait for Zel).

| Item | Before (v16) → after (v17) | Source |
|---|---|---|
| 1 | Hall → living passage: open, wall header from 210 → door 82×210 (frame like the other interior doors; the wall now runs over it). Hinged on the south jamb, opens into the living room (Claude's choice: keeps the hall artwork and the corridor entrance clear) | Zel, 2026-11-25 |
| 2 | Front door hinged on the north jamb → **south** jamb, opens inward against the hall south wall | IMG_2473, IMG_2474, IMG_1958 |
| 3 | Living south wall: nothing → AC indoor unit 85×20×33, x 853–937, 228–261 above floor | IMG_2482, IMG_2478 |
| 4 | Terrace wall light on the living facade: x 1060 → 1125 (just west of the sliding door's meeting stile) | IMG_2483 |
| 5 | New group "AS BUILT": 53 markers for switches, thermostats, sockets, outlets, the laundry heating manifold and the kitchen exhaust duct (red dots in the plan) | photos, see each name |

Checked without change: bathroom WC centre about 44 from the north wall (IMG_2485 tape; model 45); laundry washer/dryer sockets match the machines; kitchen sink connections at y ≈ 490 (model sink centre 471, within the ±15 estimate); room 5 and Sara desk sockets are under the desks.

### Conflicts found in the photos (not changed, for Zel)
| # | Where | Conflict | Options |
|---|---|---|---|
| C1 | Bedroom west wall | Wardrobe 180 (y 465–645) covers the ensuite light switch (y ≈ 473, 110 high) and a double socket (y ≈ 517) | A wardrobe 160 (y 485–645) · B electrician moves the switch · C cut-out in the wardrobe side |
| C2 | Bedroom bed wall | Bedside sockets at y ≈ 356 and ≈ 569 (centre 462); bed centre is 488, so the south socket is behind the bed frame | A move bed, nightstands and lights 2/3 26 north · B move the south socket ~15 south |
| C3 | Hall | Front door opens against the south wall; the open leaf (x 41–146) overlaps the mirror 120×170 (x 86–206) | A narrower mirror at x 150–235 (left of the distribution board) · B door stop at about 80° · C mirror on another wall |
| C4 | Living south wall | AC unit (228–261) sits above the east half of the Canadair picture; spots 9e/9f light the AC's underside and the AC blows onto the picture | A move picture and spots west of the AC (wall points at x 710–728 are in the way) · B keep, spots further from the wall · C another place for the picture |
| C5 | Living east wall | Switch at y ≈ 607, 109 high, 11 below the painting's NW corner (painting y 597–747, bottom 125) and just above the sofa back | A painting 15 south · B painting higher |
| C6 | Sara west wall | Reading light 15 (y 1090, 128 high) is ~20 from the thermostat (y ≈ 1072, 139) and switch (y ≈ 1068, 110) at the bed head | A light 15 to y ≈ 1115 · B bed head to the south |
| C7 | Ensuite | Mirror-light outlet is above the west basin (x ≈ 95), not at the mirror centre (132); tiles are finished | A light off-centre on the outlet · B LED mirror covering the outlet · C cable behind the mirror |
| C8 | Living low lamps | Planned switched sockets L1 (south wall x 1440) and L3 (east wall y 492) are near existing sockets at x 1364 and y 607 | Rewire the existing sockets as switched instead of new ones |
| ? | Living south wall x 710, 152 high | Box with loose wires, purpose unknown (intercom?) | ask the electrician |
| ? | Laundry west wall, above the switch | Round cover at about 150, purpose unknown | ask the electrician |

### Photos replaced on 2026-11-25
The new photos of the same angle replaced these old ones (moved to the Mac Trash, `~/.Trash/S15-photos-replaced-2026-11-25/`). Evidence rows above that cite an old number now refer to the new one:
IMG_2030 → IMG_2455 · IMG_2035 → IMG_2460 · IMG_2032 → IMG_2463 · IMG_1957 and IMG_2021 → IMG_2470 · IMG_2023 → IMG_2478 · IMG_1960 → IMG_2482 · IMG_1961 → IMG_2484 · IMG_2022 → IMG_2477 · IMG_2026 → IMG_2483.
