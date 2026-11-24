#!/usr/bin/env python3
"""S15-Hrneticka v15 -> v16 Home.xml: Zel's answers to the critique and new wishes (2026-11-19, evening).
 2 low lamps on switched sockets (IKEA PILSKOTT floor lamps, one table lamp)   3 kitchen bar at 1/3 of the cabinet depth from the wall
 4 laundry wall light -> south wall, above the position of Sara's socket            5 south picture: ceiling spots only
 6 niche: LED profile under the front edge of each shelf                               7 paintings: overhead picture lights, not GU10 cylinders
 9 hall: seat with shoe shelves + hanger panel + top cabinet with hidden light bar; large mirror opposite; vertical artwork on the T wall
 10 dining: one IKEA PILSKOTT pendant 97 (higher end west)
Light names decide the Blender light group (blender/make_lights.py). "-> x,y,z" at the end of a name = aim point.
Usage: build_v16.py <v15 Home.xml> <out Home.xml>"""
import copy, sys, uuid, xml.etree.ElementTree as ET
SRC, DST = sys.argv[1], sys.argv[2]
tree = ET.parse(SRC); root = tree.getroot()
def nid(p): return f'{p}-{uuid.uuid4()}'
def F(v): return f'{v:.2f}'.rstrip('0').rstrip('.')
def by_name(prefix, tag=None):
    return [e for e in root.iter() if (tag is None or e.tag == tag) and (e.get('name') or '').startswith(prefix)]
def parent_of(e):
    for p in root.iter():
        if e in list(p): return p
def remove(prefix, n=None):
    es = by_name(prefix)
    assert es and (n is None or len(es) == n), (prefix, len(es))
    for e in es: parent_of(e).remove(e)
BOX = copy.deepcopy(by_name('Laundry basket')[0]); SRC_L = copy.deepcopy(by_name('Light: spot', 'light')[0])
FRAME = copy.deepcopy(by_name('Photo frame 40×50')[0]); HOOK = copy.deepcopy(by_name('Coat hook')[0])
def group(name, after='Kitchen corner base'):
    g = ET.Element('furnitureGroup', id=nid('furnitureGroup'), name=name, x='0', y='0', width='1', depth='1', height='1')
    a = by_name(after)[0]; p = parent_of(a); p.insert(list(p).index(a) + 1, g); return g
def put(g, proto, name, x, y, w, d, h, el, color=None, angle=None):
    b = copy.deepcopy(proto); b.set('id', nid('pieceOfFurniture')); b.set('name', name)
    for k, v in dict(x=x, y=y, width=w, depth=d, height=h, elevation=el).items(): b.set(k, F(float(v)))
    if color: b.set('color', color)
    if angle is not None: b.set('angle', F(angle))
    g.append(b); return b
def box(g, name, x, y, w, d, h, el, color): return put(g, BOX, name, x, y, w, d, h, el, color)
def src(g, name, x, y, el, aim=None):
    l = copy.deepcopy(SRC_L); l.set('id', nid('light')); l.set('name', name + (' -> %s,%s,%s' % tuple(F(a) for a in aim) if aim else ''))
    for k, v in dict(x=x, y=y, elevation=el, power=0.1).items(): l.set(k, F(float(v)))
    g.append(l)
BLACK, WHITE, WOOD, OAK, STEEL, BRASS, CREAM, GREY = 'FF2B2B2B', 'FFF2F2EE', 'FF3A3A3A', 'FFB08D62', 'FFB9BCC0', 'FFB8975A', 'FFEDE6D6', 'FF6F6F72'
N, S, E, W = (0, 1), (0, -1), (-1, 0), (1, 0)          # direction pointing from the wall into the room
A = by_name('AMBIENT A', 'furnitureGroup')[0]; A.set('name', "AMBIENT A – wall, art, desk, TV and hall lights (v16)")
def wall_light(g, tag, no, room, x, y, into, el=175, color=BLACK):
    cx, cy = x + into[0] * 6.5, y + into[1] * 6.5
    box(g, f'{no} wall light up/down – {room} (centre {el} above floor)', cx, cy, 7, 7, 16, el - 8, color)
    box(g, f'{no} wall light bracket – {room}', x + into[0] * 1.5, y + into[1] * 1.5, 3 if into[0] else 4, 3 if into[1] else 4, 6, el - 3, color)
    src(g, f'{tag} up: {no} {room}', cx, cy, el + 10); src(g, f'{tag} down: {no} {room}', cx, cy, el - 13)
def picture_light(g, tag, no, room, x, y, into, length, el, aim_el):
    """Overhead picture light: tube on an arm 18 from the wall, LED strip shining down and back onto the picture. (x, y) = wall point at the tube centre."""
    cx, cy = x + into[0] * 18, y + into[1] * 18; along_x = into[0] == 0
    box(g, f'{no} picture light {length} – {room} (tube centre {el} above floor)', cx, cy, length if along_x else 3, 3 if along_x else length, 3, el - 1.5, BRASS)
    box(g, f'{no} picture light arm – {room}', x + into[0] * 9, y + into[1] * 9, 2 if along_x else 18, 18 if along_x else 2, 2, el - 1, BRASS)
    n = max(2, round(length / 20))
    for i in range(n):
        o = (i + 0.5) * length / n - length / 2
        sx, sy = (cx + o, cy) if along_x else (cx, cy + o)
        src(g, f'{tag} bar {"x" if along_x else "y"}: {no} {room} {i + 1}', sx, sy, el - 4.5, ((x + o, y, aim_el) if along_x else (x, y + o, aim_el)))
def vbar(g, no, room, x, y, aim):
    """IKEA PILSKOTT LED floor lamp (Inge's): vertical bar 112 high on a small base, light towards the wall."""
    box(g, f'{no} PILSKOTT LED floor lamp 112 – {room} (on a switched socket)', x, y, 3, 3, 110, 2, BLACK); box(g, f'{no} floor lamp base – {room}', x, y, 18, 12, 2, 0, BLACK)
    for i in range(5): src(g, f'Low bar z: {no} {room} {i + 1}', x + aim[0] * 2.5, y + aim[1] * 2.5, 16 + 20 * i - 1.5, (x + aim[0] * 100, y + aim[1] * 100, 16 + 20 * i))

# ---- 7  paintings: picture lights instead of GU10 cylinders -------------------------------------------------------------
remove('A08'); remove('ArtE '); remove('A18'); remove('A19'); remove('ArtH '); remove('Artwork 100×70', 1)
picture_light(A, 'ArtE', 'A08', 'living east wall, above the painting', 1464.71, 672, E, 60, 207, 160)
# ---- 4  laundry wall light: south wall, above Sara's socket (x 667 on the electrical plan) -------------------------------
remove('A10'); remove('AmbA up: A10', 1); remove('AmbA down: A10', 1)
wall_light(A, 'AmbA', 'A10', "laundry south wall, opposite Sara's socket", 667, 950, S, color=WHITE)
# ---- 5  south picture: ceiling spots only -----------------------------------------------------------------------------------
g1 = by_name('ART SOUTH option 1', 'furnitureGroup')[0]; parent_of(g1).remove(g1)
g2 = by_name('ART SOUTH option 2', 'furnitureGroup')[0]; g2.set('name', 'ART SOUTH – three ceiling spots, 60 from the wall, aimed at the Canadair picture')
for l in g2.iter('light'): l.set('name', l.get('name').replace('ArtSc aim', 'ArtS aim'))
# ---- 3  kitchen light bar at 1/3 of the wall-cabinet depth (12 from the wall) ----------------------------------------------
gb = by_name('AMBIENT B', 'furnitureGroup')[0]; parent_of(gb).remove(gb)
B = group('AMBIENT B – kitchen LED light bar under the wall cabinets, 12 from the wall')
def bar(g, tag, axis, a0, a1, fixed, el, room, color=STEEL, aimd=None):
    mid, ln = (a0 + a1) / 2, a1 - a0
    if axis == 'x': box(g, f'LED light bar {ln:.0f} – {room}', mid, fixed, ln, 2, 1.5, el - 1.5, color)
    else: box(g, f'LED light bar {ln:.0f} – {room}', fixed, mid, 2, ln, 1.5, el - 1.5, color)
    n = max(1, round(ln / 20))
    for i in range(n):
        a = a0 + (i + 0.5) * ln / n; px, py = (a, fixed) if axis == 'x' else (fixed, a)
        src(g, f'{tag} bar {axis}: {room} {i + 1:02d}', px, py, el - 3.5, (px + aimd[0], py + aimd[1], el - 3.5 + aimd[2]) if aimd else None)
bar(B, 'Kitchen', 'x', 656, 712, 318, 150, 'north cabinets W'); bar(B, 'Kitchen', 'x', 794, 872, 318, 150, 'north cabinets E'); bar(B, 'Kitchen', 'y', 372, 540, 625.5, 150, 'west cabinets')
# ---- 6  niche: LED profile under the front edge of each shelf, shining down and back ----------------------------------------
for nm in ('NICHE option 1', 'NICHE option 2'):
    g = by_name(nm, 'furnitureGroup')[0]; parent_of(g).remove(g)
NI = group('NICHE – LED profile under the front edge of each shelf')
ncy = (940.5 + 1001.3) / 2
for el in (95, 140, 185, 230, 280): bar(NI, 'Niche', 'y', ncy - 29, ncy + 29, 432, el, f'niche, under the {"shelf at %d" % el if el < 280 else "niche ceiling"}', WHITE, (-22, 0, -36))
# ---- 10 dining: one curved linear pendant, higher end west -------------------------------------------------------------------
remove('Pendant lamp Ø40', 2); remove('Light: dining pendant', 2)
P = group('DINING – IKEA PILSKOTT LED pendant 97 (higher end towards the kitchen)')
box(P, 'PILSKOTT pendant – west bar 42 (underside 168)', 844.5, 585, 42, 4, 2.5, 168, BLACK); box(P, 'PILSKOTT pendant – east bar 42 (underside 158)', 899.5, 585, 42, 4, 2.5, 158, BLACK)
for i in range(2): box(P, 'PILSKOTT pendant – curve', 868.75 + 6.5 * i, 585, 7, 4, 2.5, 164.7 - 3.4 * i, BLACK)
for x in (838, 906): box(P, 'PILSKOTT pendant – suspension wire', x, 585, 0.6, 0.6, 280 - (170.5 if x < 872 else 160.5), 170.5 if x < 872 else 160.5, GREY)
for i in range(2): src(P, f'Pendant bar x: W {i + 1}', 823.5 + (i + 0.5) * 21, 585, 165.5)
src(P, 'Pendant bar x: curve', 872, 585, 160.5)
for i in range(2): src(P, f'Pendant bar x: E {i + 1}', 878.5 + (i + 0.5) * 21, 585, 155.5)
# ---- 2  low lamps on switched sockets -----------------------------------------------------------------------------------------
remove('Floor lamp', 1)
L = group('LOW LAMPS – on switched sockets (three IKEA PILSKOTT floor lamps, one table lamp)')
vbar(L, 'L1', 'living SE corner, behind the sofa', 1440, 763, (0, 1)); vbar(L, 'L2', 'living NE corner, beside the TV', 1452, 318, (0, -1)); vbar(L, 'L4', 'bedroom SE corner', 592, 640, (0, 1))
src(L, 'Low lamp: L3 table lamp on the side table by the east window', 1420, 492, 98)
# ---- 9  hall ----------------------------------------------------------------------------------------------------------------------
remove('Built-in wardrobe 152', 1); remove('Shoe bench', 1); remove('Coat hook (black)', 4)
H = group('HALL – seat with shoe shelves, hanger panel, top cabinet, mirror, artwork (v16)')
x0, x1, yb = 70, 222, 605                                   # niche: 152 wide beside the shaft box, back wall at y 605, open to the hall at y 660
box(H, 'Hall seat 152×45×45: sliding doors, two shoe shelves inside', (x0 + x1) / 2, yb + 22.5, x1 - x0, 45, 45, 0, OAK)
box(H, 'Hall seat cushion 152×45×4', (x0 + x1) / 2, yb + 22.5, x1 - x0 - 2, 44, 4, 45, GREY)
box(H, 'Wooden hanger panel 152×141 (from 49 to 190)', (x0 + x1) / 2, yb + 1, x1 - x0, 2, 141, 49, OAK)
for hx, hel in ((88, 150), (108, 172), (128, 128), (150, 165), (172, 140), (192, 172), (208, 112)): put(H, HOOK, 'Low-profile hanger (black)', hx, yb + 4.5, 6.3, 5.5, 12.7, hel - 6)
box(H, 'Hall top cabinet 152×50×90 (from 190 to the ceiling)', (x0 + x1) / 2, yb + 25, x1 - x0, 50, 90, 190, CREAM)
bar(H, 'HallBench', 'x', x0 + 6, x1 - 6, yb + 46, 190, 'under the front of the hall top cabinet (hidden)', WHITE)
m = by_name('Full-length mirror 65×150')[0]
m.set('name', 'Large mirror 120×170 – hall south wall, opposite the seat'); m.set('x', '146'); m.set('width', '120'); m.set('height', '170'); m.set('elevation', '20')
put(H, FRAME, 'Vertical artwork 90×140 – hall north wall at the T (placeholder)', 459, 662.2, 90, 2.2, 140, 55, angle=0)
picture_light(H, 'ArtH', 'A18', 'hall north wall at the T, above the vertical artwork', 459, 661, N, 45, 207, 135)

root.set('name', 'S15-Hrneticka-v16.sh3d')
tree.write(DST, encoding='UTF-8', xml_declaration=True)
print('lights', len(list(root.iter('light'))))
