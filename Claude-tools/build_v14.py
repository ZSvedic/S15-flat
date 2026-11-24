#!/usr/bin/env python3
"""S15-Hrneticka v13 -> v14 Home.xml: ambient wall-light variants as switchable groups.
Group A = Zel's red circles on the electrical plan sent to the electrician (2026-11-18), read at +-10 cm.
Group B = Claude's suggestion (kitchen under-cabinet light). Fixtures are placeholders; lamp data lives in
Claude-tools/blender/variants.json. Usage: build_v14.py <v13 Home.xml> <out Home.xml>"""
import copy, sys, uuid, xml.etree.ElementTree as ET
SRC, DST = sys.argv[1], sys.argv[2]
tree = ET.parse(SRC); root = tree.getroot()
def nid(p): return f'{p}-{uuid.uuid4()}'
def F(v): return f'{v:.2f}'.rstrip('0').rstrip('.')
def by_name(prefix, tag=None):
    return [e for e in root.iter() if (tag is None or e.tag == tag) and (e.get('name') or '').startswith(prefix)]
BOX = copy.deepcopy(by_name('Laundry basket')[0]); SRC_L = copy.deepcopy(by_name('Light: spot', 'light')[0])
ANCHOR = by_name('Kitchen corner base')[0]
def parent_of(e):
    for p in root.iter():
        if e in list(p): return p
def group(name):
    g = ET.Element('furnitureGroup', id=nid('furnitureGroup'), name=name, x='0', y='0', width='1', depth='1', height='1')
    p = parent_of(ANCHOR); p.insert(list(p).index(ANCHOR) + 1, g); return g
def box(g, name, x, y, w, d, h, el, color):
    b = copy.deepcopy(BOX); b.set('id', nid('pieceOfFurniture')); b.set('name', name)
    for k, v in dict(x=x, y=y, width=w, depth=d, height=h, elevation=el).items(): b.set(k, F(float(v)))
    b.set('color', color); g.append(b)
def src(g, name, x, y, el, power=0.1):
    l = copy.deepcopy(SRC_L); l.set('id', nid('light')); l.set('name', name)
    for k, v in dict(x=x, y=y, elevation=el, power=power).items(): l.set(k, F(float(v)))
    g.append(l)
BLACK, WHITE, WOOD = 'FF2B2B2B', 'FFF2F2EE', 'FF3A3A3A'
N, S, E, W = (0, 1), (0, -1), (-1, 0), (1, 0)          # direction pointing from the wall into the room
def wall_light(g, no, room, x, y, into, el=175, color=BLACK):
    """Up/down cylinder Ø7x16 on a wall; (x, y) is the point on the wall face, el its centre height."""
    cx, cy = x + into[0] * 6.5, y + into[1] * 6.5
    box(g, f'A{no:02d} wall light up/down – {room} (centre {el} above floor)', cx, cy, 7, 7, 16, el - 8, color)
    box(g, f'A{no:02d} wall light bracket – {room}', x + into[0] * 1.5, y + into[1] * 1.5, 3 if into[0] else 4, 3 if into[1] else 4, 6, el - 3, color)
    src(g, f'AmbA up: {no:02d} {room}', cx, cy, el + 10); src(g, f'AmbA down: {no:02d} {room}', cx, cy, el - 13)
def puck(g, tag, no, room, x, y, el):
    box(g, f'{tag[-1]}{no:02d} LED puck Ø7 – {room}', x, y, 7, 7, 1.5, el - 1.5, WHITE)
    src(g, f'{tag} puck: {no:02d} {room}', x, y, el - 5)

A = group("AMBIENT A – Zel's wall-light points for the electrician (on)")
# 1  bedroom NW corner, on the north wall between the corner and the window
wall_light(A, 1, 'bedroom NW corner, north wall', 265, 305.88, N)
# 2, 3, 15, 12 are the bedside / reading lights that already exist in the model (v12 groups); 4 conflicts with the wardrobe
# 5  shelf over the desk with two pucks (as in the current flat)
box(A, 'A05 shelf 76×22 over the desk (underside 150)', 1121.64, 305.88 + 11, 76, 22, 3, 150, WOOD)
puck(A, 'AmbA', 5, 'desk shelf W', 1100, 305.88 + 13, 150); puck(A, 'AmbA', 5, 'desk shelf E', 1143, 305.88 + 13, 150)
# 6, 7  shelf over the TV panel with two pucks
box(A, 'A06/07 shelf 250×25 over the TV panel (underside 186)', 1292.57, 305.88 + 12.5, 250, 25, 3, 186, WOOD)
puck(A, 'AmbA', 6, 'TV shelf W', 1190, 305.88 + 15, 186); puck(A, 'AmbA', 7, 'TV shelf E', 1395, 305.88 + 15, 186)
wall_light(A, 8, 'living east wall, south of the window', 1464.71, 597, E, el=185)
wall_light(A, 9, 'living south wall, west of the terrace door', 963, 773.84, S)
wall_light(A, 10, 'laundry east wall, between cabinet and terrace door', 821.85, 856, E, color=WHITE)
puck(A, 'AmbA', 11, 'corridor niche ceiling', 418.4, 970.9, 280)
wall_light(A, 13, 'room 5 east wall, north of the desk', 536.97, 1184, E, color=WHITE)
wall_light(A, 14, 'room 5 east wall, south end of the desk', 536.97, 1320, E, color=WHITE)
wall_light(A, 16, 'Sara east wall, north end of the desk', 821.85, 1128, E, color=WHITE)
wall_light(A, 17, 'Sara east wall, south', 821.85, 1306, E, color=WHITE)

B = group("AMBIENT B – kitchen under-cabinet light, Claude's suggestion (on)")
for i, x in enumerate((628, 678, 798, 838, 868)): puck(B, 'AmbB', i + 1, 'under north wall cabinets', x, 305.88 + 22, 150)
for i, y in enumerate((395, 455, 515)): puck(B, 'AmbB', i + 6, 'under west wall cabinets', 613.42 + 22, y, 150)

root.set('name', 'S15-Hrneticka-v14.sh3d')
tree.write(DST, encoding='UTF-8', xml_declaration=True)
print('lights', len(list(root.iter('light'))), 'A pieces', len(A), 'B pieces', len(B))
