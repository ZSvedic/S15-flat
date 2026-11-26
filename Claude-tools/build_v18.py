#!/usr/bin/env python3
"""S15-Hrneticka v17 -> v18 Home.xml: Zel's answers to the v17 review (2026-11-26).
 3  all interior doors drawn open: a 4 cm leaf at 90° in 3D plus the swing in the plan (sash). Bathroom: hinge west, opens
    clockwise into the bathroom (Zel), floor stop between the leaf and the WC. Front door: floor stop to keep the leaf off the
    mirror (C3). Hinge sides of the other doors follow the as-built switches (switch on the latch side), see DOORS.
 C1 bedroom wardrobe 180 -> 160 (y 485-645): the ensuite switch (y 473) is free, the double socket (y 517) stays behind it.
 C2 bed + nightstands + bedside lights + pictures + rug 25 north: bed centred between the bedside sockets (y 356 / 569).
 C4 south picture: three ceiling spots -> overhead picture light 100 on two arms, on a horizontal wall strip whose west end sits
    on the drywall (laundry/living wall, x < 822) where the feed comes in. Indoor plant by the terrace door removed.
 C5 east painting 10 higher (bottom 135), its picture light with it (217).
 C6 Sara: reading light 20 south; wall light 16 -> east wall over the desk centre; 17 -> south wall, west pier.
 Boxes: living south wall box = video intercom; laundry west wall cover = covered outlet or floor-heating control (Zel).
Usage: build_v18.py <v17 Home.xml> <out Home.xml>"""
import copy, math, sys, uuid, xml.etree.ElementTree as ET
SRC, DST = sys.argv[1], sys.argv[2]
tree = ET.parse(SRC); root = tree.getroot()
def nid(p): return f'{p}-{uuid.uuid4()}'
def F(v): return f'{v:.2f}'.rstrip('0').rstrip('.')
def by_name(prefix, tag=None):
    return [e for e in root.iter() if (tag is None or e.tag == tag) and (e.get('name') or '').startswith(prefix)]
def one(prefix, tag=None):
    es = by_name(prefix, tag); assert len(es) == 1, (prefix, len(es)); return es[0]
def parent_of(e):
    for p in root.iter():
        if e in list(p): return p
def remove(prefix, n=None):
    es = by_name(prefix); assert es and (n is None or len(es) == n), (prefix, len(es))
    for e in es: parent_of(e).remove(e)
def shift(e, dx=0.0, dy=0.0, dz=0.0):
    """Move a piece, light or group (with everything inside it)."""
    for x in e.iter():
        if x.tag in ('pieceOfFurniture', 'light', 'furnitureGroup', 'doorOrWindow'):
            x.set('x', F(float(x.get('x')) + dx)); x.set('y', F(float(x.get('y')) + dy))
            if dz: x.set('elevation', F(float(x.get('elevation', 0)) + dz))
BOX = copy.deepcopy(one('Laundry basket')); SRC_L = copy.deepcopy(by_name('Light: spot', 'light')[0])
def group(name, after='Kitchen corner base'):
    g = ET.Element('furnitureGroup', id=nid('furnitureGroup'), name=name, x='0', y='0', width='1', depth='1', height='1')
    a = by_name(after)[0]; p = parent_of(a); p.insert(list(p).index(a) + 1, g); return g
def box(g, name, x, y, w, d, h, el, color, angle=None):
    b = copy.deepcopy(BOX); b.set('id', nid('pieceOfFurniture')); b.set('name', name)
    for k, v in dict(x=x, y=y, width=w, depth=d, height=h, elevation=el).items(): b.set(k, F(float(v)))
    b.set('color', color)
    if angle: b.set('angle', F(angle))
    else: b.attrib.pop('angle', None)
    g.append(b); return b
def src(g, name, x, y, el, aim=None):
    l = copy.deepcopy(SRC_L); l.set('id', nid('light')); l.set('name', name + (' -> %s,%s,%s' % tuple(F(a) for a in aim) if aim else ''))
    for k, v in dict(x=x, y=y, elevation=el, power=0.1).items(): l.set(k, F(float(v)))
    g.append(l)
BLACK, WHITE, BRASS, LEAF = 'FF2B2B2B', 'FFF2F2EE', 'FFB8975A', 'FFE9E6DF'
N, S, E, W = (0, 1), (0, -1), (-1, 0), (1, 0)          # direction from the wall into the room

# ---- 3  doors open -------------------------------------------------------------------------------------------------------------
# (frame name prefix, hinge jamb (compass side), direction the open leaf points (compass), opening angle in degrees, reason)
COMPASS = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}
DOORS = [
    ('Door frame – bathroom',     'W', 'S', 90, 'hinge west, opens clockwise into the bathroom (Zel); floor stop so it misses the WC'),
    ('Door frame – bedroom',      'W', 'N', 90, 'hinge west: the as-built switches (hall and bedroom) are east of the door, on the latch side'),
    ('Door frame – ensuite',      'S', 'W', 90, 'hinge south, opens into the ensuite: the switch inside the ensuite is north of the door, on the latch side; hinge north would park the leaf 24 from the basin'),
    ('Door frame – room 5',       'E', 'S', 90, 'hinge east, opens into room 5: the room 5 switch is west of the door'),
    ('Door frame – laundry',      'S', 'E', 90, 'hinge south, opens into the laundry: the laundry switch is north of the door'),
    ('Door frame – Sara',         'N', 'E', 90, "hinge north, opens into Sara's room: her switch is south of the door"),
    ('Door frame – hall → living', 'S', 'E', 90, 'hinge south, opens into the living room (v17)'),
]
G = group('DOOR LEAVES – interior doors drawn open (v18; SH3D cannot open a door model, so the leaf is a separate box)')
for prefix, jamb, to, deg, why in DOORS:
    into = COMPASS[to]
    d = one(prefix, 'doorOrWindow')
    cx, cy, w, dep, a = (float(d.get(k, 0)) for k in ('x', 'y', 'width', 'depth', 'angle'))
    ax_ = (math.cos(a), math.sin(a)); ay_ = (-math.sin(a), math.cos(a))              # local x and y axes in the world
    # local hinge x: the jamb whose world direction matches 'jamb'
    jw = COMPASS[jamb]
    sx = 1 if ax_[0] * jw[0] + ax_[1] * jw[1] > 0 else -1
    sy = 1 if ay_[0] * into[0] + ay_[1] * into[1] > 0 else -1                         # local y side the leaf opens to
    hu, hv = sx * (w / 2 - 2), sy * dep / 2                                          # hinge (2 cm inside the jamb, at the wall face)
    L = w - 4
    # sash for the plan: point on the arc (local) = hinge + r (cos t, -sin t); closed leaf points to -sx along x, open to sy along y
    t0 = math.atan2(0, -sx); t1 = math.atan2(-sy, 0)
    if t1 - t0 > math.pi: t1 -= 2 * math.pi
    if t0 - t1 > math.pi: t1 += 2 * math.pi
    t1 = t0 + (t1 - t0) * deg / 90
    for s in [s for s in d if s.tag == 'sash']: d.remove(s)
    ET.SubElement(d, 'sash', xAxis=F((hu + w / 2) / w), yAxis=F((hv + dep / 2) / dep), width=F(L / w), startAngle=f'{t0:.7f}', endAngle=f'{t1:.7f}')
    # 3D leaf: from the hinge along the open direction, 4 thick towards the opening
    hx, hy = cx + hu * ax_[0] + hv * ay_[0], cy + hu * ax_[1] + hv * ay_[1]
    ox, oy = into; tx, ty = -sx * ax_[0], -sx * ax_[1]                               # tx,ty: from the hinge jamb into the opening
    lx, ly = hx + ox * L / 2 + tx * 2, hy + oy * L / 2 + ty * 2
    ang = math.atan2(oy, ox) % (2 * math.pi)
    room = prefix.replace('Door frame – ', '')
    box(G, f'Door leaf {L:.0f} open {deg}° – {room} ({why})', lx, ly, L, 4, 205, 0, LEAF, ang)
    d.set('name', d.get('name') + f' – {why}' if why not in d.get('name') else d.get('name'))
box(G, 'Door stop Ø3 – bathroom floor, west of the open leaf near the hinge, out of the way of feet at the WC (leaf stops at 90°, 7.7 cm before the WC)', 293, 800, 3, 3, 3, 0, BLACK)
box(G, 'Door stop Ø3 – hall floor, 80 from the hinge, keeps the open front door and its handle off the mirror (C3; opens about 82°)', 112, 748, 3, 3, 3, 0, BLACK)
fs = [s for s in one('Front door', 'doorOrWindow') if s.tag == 'sash'][0]; fs.set('endAngle', F(-math.radians(82)))   # plan: swing to the stop

# ---- C1  bedroom wardrobe 160 ----------------------------------------------------------------------------------------------------
wd = one('Wardrobe 180×65'); wd.set('name', 'Wardrobe 160×65 sliding doors (v18: shortened from 180 so the ensuite switch at y 473 is free; the double socket at y 517 stays behind it and feeds the wardrobe light)')
wd.set('width', '160'); wd.set('y', F(645.41 - 80))

# ---- C2  bed centred between the bedside sockets (356 / 569 -> 462.5) -------------------------------------------------------------
bed = one('Bed 160×200 (frame 170×210)'); DY = 462.5 - float(bed.get('y'))
moved = [bed, one('Bedroom rug'), one('Picture: Desenio patent plane'), one('Picture: Desenio Ride until dawn'),
         one('Wall light L', 'furnitureGroup'), one('Wall light R', 'furnitureGroup')] + \
        [e for e in by_name('Nightstand 45×40') if float(e.get('x')) > 560 and 300 < float(e.get('y')) < 650]
assert len(moved) == 8, len(moved)
for e in moved: shift(e, dy=DY)
bed.set('name', bed.get('name') + f' – v18: centred between the bedside sockets ({DY:+.0f})')

# ---- C4  south picture: picture light on a wall strip; plant removed ---------------------------------------------------------------
remove('ART SOUTH', 1); remove('Floor plant 60', 1)
A = group('ART SOUTH – picture light 100 over the Canadair picture, on a horizontal wall strip fed from the drywall (v18)')
PX, WALL, TOP = 871.97, 774.12, 200            # picture centre x, wall face, picture top (140 + 60)
EL = TOP + 10                                   # tube centre
box(A, f'A09 wall strip 132×3 – living south wall, x 800-932, centre {EL + 3} above floor; feed at its west end, x 805, in the drywall (laundry/living wall ends at x 822)', 866, WALL - 0.75, 132, 1.5, 3, EL + 1.5, BRASS)
for ax in (842, 902):
    box(A, 'A09 picture light arm – living south wall', ax, WALL - 9, 2, 18, 4, EL - 1, BRASS)
box(A, f'A09 picture light 100 – living south wall, over the Canadair picture (tube centre {EL} above floor, 18 from the wall)', PX, WALL - 18, 100, 3, 3, EL - 1.5, BRASS)
for i in range(5):
    o = (i + 0.5) * 20 - 50
    src(A, f'ArtS bar x: A09 living south wall, over the Canadair picture {i + 1}', PX + o, WALL - 18, EL - 4.5, (PX + o, WALL, 170))

# ---- C5  east painting 10 higher ---------------------------------------------------------------------------------------------------
p = one('Painting 150×70 – living east wall'); p.set('elevation', '135')
for e in by_name('A08 ') + by_name('ArtE bar y: A08'):
    e.set('elevation', F(float(e.get('elevation')) + 10))
    n = e.get('name').replace('tube centre 207', 'tube centre 217')
    if '->' in n: n = n.rsplit(',', 1)[0] + ',170'
    e.set('name', n)

# ---- C6  Sara -----------------------------------------------------------------------------------------------------------------------
rl = one('Bed reading light', 'furnitureGroup'); shift(rl, dy=20)
col = one('A16 wall light up/down').get('color')
remove('A16 ', 2); remove('A17 ', 2); remove('AmbA up: A16', 1); remove('AmbA down: A16', 1); remove('AmbA up: A17', 1); remove('AmbA down: A17', 1)
AMB = one('AMBIENT A', 'furnitureGroup')
def wall_light(g, no, room, x, y, into, el=175, color=BLACK):
    cx, cy = x + into[0] * 6.5, y + into[1] * 6.5
    box(g, f'{no} wall light up/down – {room} (centre {el} above floor)', cx, cy, 7, 7, 16, el - 8, color)
    box(g, f'{no} wall light bracket – {room}', x + into[0] * 1.5, y + into[1] * 1.5, 3 if into[0] else 4, 3 if into[1] else 4, 6, el - 3, color)
    src(g, f'AmbA up: {no} {room}', cx, cy, el + 10); src(g, f'AmbA down: {no} {room}', cx, cy, el - 13)
desk = one('Desk 120×50'); dyc = float(desk.get('y'))
wall_light(AMB, 'A16', "Sara east wall, over the desk centre", 821.85, dyc, E, color=col)
wall_light(AMB, 'A17', "Sara south wall, west pier, 51 from the west wall (above the corner chair)", 598, 1348, S, color=col)

# ---- boxes named by Zel ------------------------------------------------------------------------------------------------------------
wb = one('As built: wire box – living south wall'); wb.set('name', 'As built: video intercom (portafon) – living south wall, west group, centre 152 above floor (IMG_2478, IMG_2482; Zel)')
oc = one('As built: outlet cover – laundry west wall'); oc.set('name', 'As built: round cover – laundry west wall, above the switch, centre 150: covered outlet or planned floor-heating control (Zel) (IMG_2459)')

root.set('name', 'S15-Hrneticka-v18.sh3d')
tree.write(DST, encoding='UTF-8', xml_declaration=True)
print('bed dy', round(DY, 2), 'lights', len(list(root.iter('light'))))
