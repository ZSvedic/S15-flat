#!/usr/bin/env python3
"""S15-Hrneticka v14 -> v15 Home.xml: Zel's review of v14 (2026-11-19), items a-j.
 b desk: shelf with pucks -> ceiling work light (desk + picture)      c living east wall: wide painting + 2 wall lights
 d living south picture: 3 wall lights OR 3 ceiling spots (two option groups)   e kitchen: pucks -> LED light bar
 f bedroom NW corner: plant -> clothes hooks + quarter-round seat, up/down light above
 g room 5: desk 160x75 without drawer, wall lights symmetric            h Sara: wall lights symmetric about the desk
 i corridor niche: 5 shelves with art; back light OR shelf downlights (two option groups)
 j hall entrance: artwork + 2 wall lights
Light names decide the Blender light group (see blender/make_lights.py). "-> x,y,z" at the end of a name = aim point.
Usage: build_v15.py <v14 Home.xml> <out Home.xml>     (also needs v15/quarter_round.obj in the .sh3d, see make_sh3d.py extra files)"""
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
FRAME = copy.deepcopy(by_name('Picture 100×70 (hallway')[0]); HOOK = copy.deepcopy(by_name('Coat hook')[0])
VASE = copy.deepcopy(by_name('Vase')[0]); BOOKS = copy.deepcopy(by_name('Books')[0]); POT = copy.deepcopy(by_name('Herb pot')[0])
ANCHOR = by_name('Kitchen corner base')[0]
def group(name):
    g = ET.Element('furnitureGroup', id=nid('furnitureGroup'), name=name, x='0', y='0', width='1', depth='1', height='1')
    p = parent_of(ANCHOR); p.insert(list(p).index(ANCHOR) + 1, g); return g
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
BLACK, WHITE, WOOD, OAK, STEEL = 'FF2B2B2B', 'FFF2F2EE', 'FF3A3A3A', 'FFB08D62', 'FFB9BCC0'
N, S, E, W = (0, 1), (0, -1), (-1, 0), (1, 0)          # direction pointing from the wall into the room
def wall_light(g, tag, no, room, x, y, into, el=175, color=BLACK):
    """Up/down cylinder Ø7x16 with two GU10 lamps; (x, y) is the point on the wall face, el its centre height."""
    cx, cy = x + into[0] * 6.5, y + into[1] * 6.5
    box(g, f'{no} wall light up/down – {room} (centre {el} above floor)', cx, cy, 7, 7, 16, el - 8, color)
    box(g, f'{no} wall light bracket – {room}', x + into[0] * 1.5, y + into[1] * 1.5, 3 if into[0] else 4, 3 if into[1] else 4, 6, el - 3, color)
    src(g, f'{tag} up: {no} {room}', cx, cy, el + 10); src(g, f'{tag} down: {no} {room}', cx, cy, el - 13)
def ceil_spot(g, tag, no, room, x, y, aim, color=BLACK):
    """Surface ceiling spot Ø7x10 with one GU10 lamp, aimed at a point."""
    box(g, f'{no} ceiling spot – {room}', x, y, 7, 7, 10, 270, color); src(g, f'{tag} aim: {no} {room}', x, y, 266, aim)
def puck(g, tag, no, room, x, y, el, dia=7):
    box(g, f'{no} LED puck Ø{dia} – {room}', x, y, dia, dia, 1.5, el - 1.5, WHITE); src(g, f'{tag} puck: {no} {room}', x, y, el - 4)

# ---- removals -------------------------------------------------------------------------------------------------------
for g in by_name('AMBIENT A', 'furnitureGroup') + by_name('AMBIENT B', 'furnitureGroup'): parent_of(g).remove(g)
remove('Plant 40', 1); remove('Wall shelf 180 with books', 1); remove('Trailing plant on shelf', 1); remove('Vase', 1)
for e in by_name('Books'):
    if float(e.get('x')) > 1400: parent_of(e).remove(e)
remove('Desk 140×70', 1)

A = group("AMBIENT A – wall, art, desk and TV lights (Zel's points, v15)")
# ---- f  bedroom NW corner --------------------------------------------------------------------------------------------
wall_light(A, 'AmbA', 'A01', 'bedroom NW corner, north wall, above the clothes hooks', 265, 305.88, N, el=205)
box(A, 'Clothes rail 50×2×8 with 3 hooks – bedroom NW corner (top 170)', 265, 305.88 + 1.2, 50, 2, 8, 162, OAK)
for hx in (248, 265, 282): put(A, HOOK, 'Clothes hook (black)', hx, 305.88 + 4.5, 6.3, 5.5, 12.7, 158)
q = put(A, BOX, 'Corner seat, quarter round r 50, h 45 – bedroom NW corner (sit / lay clothes)', 232.9 + 25, 305.88 + 25, 50, 50, 45, 0, 'FF8C7B6B')
q.set('model', 'v15/quarter_round.obj'); q.set('modelSize', '2000'); q.set('backFaceShown', 'true'); q.attrib.pop('catalogId', None)
# ---- b  living desk: ceiling work light, two heads ---------------------------------------------------------------------
box(A, 'A05 ceiling track 40 – over the living-room desk (75 from the north wall)', 1121.64, 381, 4, 40, 3, 277, BLACK)
ceil_spot(A, 'Desk', 'A05a', 'living desk, straight down', 1121.64, 393, (1121.64, 393, 75))
ceil_spot(A, 'Desk', 'A05b', 'living desk, aimed at the picture', 1121.64, 369, (1121.64, 306, 183))
# ---- 6, 7  TV shelf (unchanged) ---------------------------------------------------------------------------------------
box(A, 'A06/07 shelf 250×25 over the TV panel (underside 186)', 1292.57, 305.88 + 12.5, 250, 25, 3, 186, WOOD)
puck(A, 'TV', 'A06', 'TV shelf W', 1190, 305.88 + 15, 186); puck(A, 'TV', 'A07', 'TV shelf E', 1395, 305.88 + 15, 186)
# ---- c  living east wall: wide painting + two wall lights -----------------------------------------------------------------
put(A, FRAME, 'Painting 150×70 – living east wall, over the sofa (placeholder)', 1463.5, 672, 150, 2.2, 70, 125, angle=1.5707964)
wall_light(A, 'ArtE', 'A08a', 'living east wall, above the painting N', 1464.71, 634, E, el=220)
wall_light(A, 'ArtE', 'A08b', 'living east wall, above the painting S', 1464.71, 710, E, el=220)
# ---- 10 laundry (unchanged) -------------------------------------------------------------------------------------------
wall_light(A, 'AmbA', 'A10', 'laundry east wall, between cabinet and terrace door', 821.85, 856, E, color=WHITE)
# ---- g  room 5: desk 160x75 without drawer, lights symmetric about the desk centre (y 1265) ----------------------------------
dx0, dx1, dy0, dy1 = 462, 536.97, 1185, 1345
box(A, 'Desk 160×75 without drawer – room 5 (top)', (dx0 + dx1) / 2, 1265, dx1 - dx0, 160, 3, 72, OAK)
for lx in (dx0 + 4, dx1 - 4):
    for ly in (dy0 + 4, dy1 - 4): box(A, 'Desk 160×75 – leg', lx, ly, 4, 4, 72, 0, BLACK)
for nm in ('Office chair room 5', 'Laptop room 5', 'Monitor room 5', 'Desk lamp room 5', 'Wall shelf print 45×90'):
    e = by_name(nm)[0]; e.set('y', F(float(e.get('y')) - 5))
wall_light(A, 'AmbA', 'A13', 'room 5 east wall, 62 north of the desk centre', 536.97, 1203, E, color=WHITE)
wall_light(A, 'AmbA', 'A14', 'room 5 east wall, 62 south of the desk centre', 536.97, 1327, E, color=WHITE)
# ---- h  Sara: lights symmetric about the desk centre (y 1174) --------------------------------------------------------------
wall_light(A, 'AmbA', 'A16', 'Sara east wall, 45 north of the desk centre', 821.85, 1129, E, color=WHITE)
wall_light(A, 'AmbA', 'A17', 'Sara east wall, 45 south of the desk centre', 821.85, 1219, E, color=WHITE)
# ---- j  hall entrance: artwork + two wall lights (south wall, between the front door and the mirror) -------------------------
p = by_name('Picture 100×70 (hallway')[0]
p.set('name', 'Artwork 100×70 – hall south wall (seen from the front door)'); p.set('elevation', '135')
wall_light(A, 'ArtH', 'A18', 'hall south wall, above the artwork W', 72, 766, S, el=222)
wall_light(A, 'ArtH', 'A19', 'hall south wall, above the artwork E', 122, 766, S, el=222)

# ---- d  living south picture: two options ---------------------------------------------------------------------------------
D1 = group('ART SOUTH option 1 – three wall lights above the Canadair picture')
for i, x in enumerate((802, 872, 942)): wall_light(D1, 'ArtSw', 'A09' + 'abc'[i], 'living south wall, above the picture', x, 773.84, S, el=222)
D2 = group('ART SOUTH option 2 – three ceiling spots, 60 from the wall, aimed at the picture')
for i, x in enumerate((802, 872, 942)): ceil_spot(D2, 'ArtSc', 'A09' + 'def'[i], 'living ceiling, aimed at the south picture', x, 714, (x, 773.84, 170))

# ---- e  kitchen light bar (as in the current flat): under the wall cabinets, at the back ------------------------------------
B = group('AMBIENT B – kitchen LED light bar under the wall cabinets')
def bar(axis, a0, a1, fixed, room):
    mid, ln = (a0 + a1) / 2, a1 - a0
    if axis == 'x': box(B, f'LED light bar {ln:.0f} – {room}', mid, fixed, ln, 2, 1.5, 148.5, STEEL)
    else: box(B, f'LED light bar {ln:.0f} – {room}', fixed, mid, 2, ln, 1.5, 148.5, STEEL)
    n = round(ln / 20)
    for i in range(n):
        a = a0 + (i + 0.5) * ln / n
        src(B, f'Kitchen bar {axis}: {room} {i + 1:02d}', a if axis == 'x' else fixed, fixed if axis == 'x' else a, 146.5)
bar('x', 656, 712, 313, 'north cabinets W'); bar('x', 794, 872, 313, 'north cabinets E'); bar('y', 372, 540, 620.5, 'west cabinets')

# ---- i  corridor niche: 5 shelves with art; two light options -------------------------------------------------------------
NX0, NX1, NY0, NY1 = 401.5, 435, 940.5, 1001.3; ncy = (NY0 + NY1) / 2
SH = (50, 95, 140, 185, 230)
G = group('NICHE – shelves with art pieces (corridor)')
for el in SH: box(G, f'Niche shelf 60×27, top {el + 2.5:.0f}', (NX0 + 4.5 + NX1 - 1.5) / 2, ncy, NX1 - NX0 - 6, NY1 - NY0 - 1, 2.5, el, OAK)
put(G, VASE, 'Art: vase', 419, ncy - 8, 16, 16, 34, 52.5); put(G, BOOKS, 'Art: books', 419, ncy + 12, 24, 17, 24, 52.5, angle=1.5707964)
put(G, BOX, 'Art: sculpture block', 419, ncy, 14, 14, 30, 97.5, 'FF9A6B4F'); put(G, VASE, 'Art: vase small', 419, ncy + 16, 11, 11, 22, 97.5)
put(G, VASE, 'Art: vase', 419, ncy + 5, 18, 18, 36, 142.5); put(G, BOX, 'Art: small frame', 419, ncy - 15, 3, 18, 24, 142.5, 'FFD9C9A8')
put(G, BOOKS, 'Art: books', 419, ncy - 10, 24, 17, 24, 187.5, angle=1.5707964); put(G, BOX, 'Art: bowl block', 419, ncy + 14, 16, 16, 10, 187.5, 'FF4F6D7A')
put(G, POT, 'Art: plant', 419, ncy, 18, 18, 30, 232.5)
I1 = group('NICHE option 1 – back light: two vertical LED strips behind the shelves')
for sy, side in ((NY0 + 2, 'N'), (NY1 - 2, 'S')):
    box(I1, f'LED strip 220 vertical – niche back, {side} side', NX0 + 1, sy, 1, 1.5, 220, 45, WHITE)
    for i in range(11): src(I1, f'Niche back z: {side} {i + 1:02d}', NX0 + 2.5, sy, 55 + 20 * i - 1.5, (NX0 + 100, ncy, 55 + 20 * i))
I2 = group('NICHE option 2 – small downlight under each shelf and in the niche ceiling')
for i, el in enumerate(SH[1:] + (280,)): puck(I2, 'Niche', f'A11{"abcde"[i]}', f'niche, under the shelf at {el}' if el < 280 else 'niche ceiling', 419, ncy, el, dia=5)

root.set('name', 'S15-Hrneticka-v15.sh3d')
tree.write(DST, encoding='UTF-8', xml_declaration=True)
print('lights', len(list(root.iter('light'))))
