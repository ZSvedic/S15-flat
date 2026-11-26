# v21-lighting-expert: a lighting expert's critique of v21

On 2026-11-26 a separate Claude agent (model Fable) acted as a residential lighting designer. It read the v21 plan, the wall-light draft, the v20 lux table and sheets, and the lamp data, then critiqued the design and proposed 15 changes. Its changes were built as `S15-Hrneticka-v21-lighting-expert.sh3d` (`Claude-tools/build_v21_lighting_expert.py`, plus `build_lightset.py` for the new fixtures in `S15-v21-lighting-expert-fixtures.txt`) and rendered next to v21. Nothing here is decided: it is input for Zel.

## Critique (expert's points, most important first)
1. **One dimmer cannot dim everything.** The PILSKOTT pendant and floor lamps (about 3,200 lm, the largest ambient share) ignore a wall dimmer. The 24 V strips and picture lights need phase-dimmable drivers. Either put the smart lamps and drivers on one IKEA scene, or accept that "30 %" dims only the GU10 lamps.
2. **No local off at the beds.** Lights 2, 3, 12 and 15 are on the flat-wide ambient switch, so nobody can switch a bedside light off from bed. Each needs a switch on the fixture.
3. **Bedside lights 2 and 3 are badly placed for reading.** At 158 high over the nightstands they sit about 65 cm to the side of the pillow. Lower them and move them inside the bed edges.
4. **Glare on the TV wall.** The two pucks at 182 graze the top of the 85" screen (top edge 181) and the wood panel. L2 is a 700 lm bar 65 cm from the screen edge. The shelf up-light alone is the right bias light.
5. **The sofa is too dark to read on:** 34 lx in scene 1. L1 only washes the corner wall, and L3 is a weak 400 lm.
6. **The balance between rooms is inverted.** In scene 1 the hall and corridor get 90–108 lx against 55 in the living room and 58 in the bedroom; in scene 2 the hall gets 359 against 120 in the living room. Cut the niche, the hall bar and the hall spots.
7. **The kitchen worktop is under-lit:** 175 lx (53 dimmed), and the ceiling lamp is behind the cook at the west run.
8. **Sara's desk light 16 is a glare source.** Its down lamp at 162 is in a seated child's line of sight and gives a 36° hot spot. Raise it.
9. **The bathrooms have no ambient light.** A night visit means 1,200 lm at 3000 K. Add one low strip in the ensuite.
10. **Colour and odd members.** Use 2700 K and CRI 90+ everywhere, CRI 95 for the picture lights. Laundry light 10 on the ambient switch lights an empty utility room. The terrace lamps and the desk lamp don't belong in the ceiling group; they need their own switches.
- Also suggested: dim-to-warm GU10 lamps (2700 → 2200 K, about 350 lm, 36°) for deeper evening dimming. Test one on the real dimmer first.

## Changes built
| # | Change | Done in the model |
|---|---|---|
| C1 | TV pucks 6, 7 removed (screen reflections); shelf up-light 7a stays | removed |
| C2 | L2 floor lamp beside the TV removed; its socket stays unswitched | removed |
| C3 | L1 → shaded floor reading lamp over the sofa corner, 800 lm | new lamp at x 1440, y 745, shade 150 |
| C4 | L3 table lamp 400 → 800 lm | new lamp at x 1420, y 492, shade 95 |
| C5, C6 | Bedside lights 2, 3 → adjustable wall reading lights 250 lm, 60°, 125 high, inside the bed edges (y 385 and 540), aimed at the pillows; own switch | old lights removed, new ones added |
| C7 | Sara light 16 175 → 195 high | moved up |
| C8, C9 | Room 5 lights 13, 14 → y 1220 and 1310 (clear of the curtain stack, symmetric about the desk) | moved |
| C10 | Laundry light 10 removed | removed |
| C11 | Niche profiles 350 → 150 lm/m | lamp data |
| C12 | Hall seat bar 600 → 300 lm/m, 2700 K | lamp data |
| C13 | Kitchen bar 600 → 1000 lm/m, 2700 K | lamp data |
| C14 | Ensuite: low toe-kick strip under the vanity, 100 lm/m (night light) | new strip, 20 high |
| C15 | Hall spots 400 → 230 lm, 2700 K | lamp data |
