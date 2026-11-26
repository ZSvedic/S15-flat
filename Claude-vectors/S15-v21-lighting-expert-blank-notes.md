# v21-lighting-expert-blank: a lighting design from scratch

On 2026-11-26 a separate Claude agent (model Fable), briefed as a residential lighting designer, designed the whole flat's lighting without seeing Zel's design.

**What it saw.** It was given a sandbox folder with only two files:
- a plan of v21 with Zel's lights removed, keeping only the light points of the electrical plan (ceiling points, mirror points, facade lamps, and the as-built spots in the hall, corridor and laundry);
- a facts file: rooms, openings, existing points, switches and sockets, furniture with positions, and the camera views.

Its brief told it to open nothing else. The sandbox is by instruction only, not enforced, but the agent reported opening only those two files, and its tool use (2 calls) matches that.

**Fixed for it:** the owner's switching, with one ambient group on one switch and dimmer, and one ceiling group.

Built as `S15-Hrneticka-v21-lighting-expert-blank.sh3d`: the stripped v21, plus the 45 fixtures in `S15-v21-lighting-expert-blank-fixtures.txt`, added by `Claude-tools/build_lightset.py`.

## Concept (the expert's)
- **Three layers in every room**, all on the dimmed ambient circuit and all low-glare: indirect strips on furniture tops, shielded task light, and picture lights as accents.
- **No dropped ceiling.** Every new light is a wall point, a furniture strip or a plug-in lamp. The one exception is the dining pendant: it needs a 190 cm ceiling chase.
- **Ceiling points become plain opal diffusers** (800–2,500 lm), used for cleaning and homework. The as-built spots stay.
- **All light at 2700 K, CRI 90+, dimmable**, with strips in opal profiles.
- **Task lights have their own switch on the fixture**: bed reading, desk lamps and mirrors.
- **Night orientation is the ambient group at 5–10 %**: an under-seat strip in the hall, picture lights in the corridor, and the niche.
- **The facade lamps are on the ambient group**, so the lit terrace replaces the black glass of the 3 m door.
- **Left out because of the 45-fixture limit:** a laundry worktop strip, a light for the bedroom corner seat, and strips on the wardrobe tops in Sara's room and room 5.

## Its notes
- It read the two Desenio prints as hanging over the bed (bedroom east wall), and lit them there (B3).
- It needs new sockets for the desk lamp on the living north wall and for the strip drivers on the cabinet and wardrobe tops.

## Fixtures (summary; full list in the fixtures file)
| Room | Fixtures |
|---|---|
| Living + kitchen | 3 ceiling diffusers (1,500–2,500 lm) · worktop strips 900 lm/m on 3 runs · up-light strip on the wall-cabinet tops · dining pendant 1,100 lm · picture lights on all 3 pictures (500 lm/m) · TV-wall up-light strip · table lamp at the sofa · desk lamp · wall up-light behind the sofa |
| Bedroom | ceiling diffuser · 2 adjustable reading spots at the bed · picture light over the 2 prints · picture light on the 60×80 picture · up-light strip on the wardrobe top |
| Bathrooms | ceiling diffusers · mirror light strips 1,200 lm/m · glow strip in the guest bath's niche |
| Hall + corridor | picture light at the T · 2 wall lights beside the mirror · strip under the top cabinet · night floor strip at the entrance · 2 picture lights in the corridor |
| Sara | 2 ceiling diffusers · strip under the wall shelf over the bed · strip over the desk and pinboard · night lamp on the C table |
| Room 5 | ceiling diffuser · picture lights over the sofa bed and the desk · desk lamp · floor lamp |
| Terrace | the 2 facade lamps as shielded down-lights on the ambient group |
