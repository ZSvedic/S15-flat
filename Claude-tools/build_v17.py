#!/usr/bin/env python3
"""S15-Hrneticka v16 -> v17 Home.xml: site photos of 2026-11-25 (Drive Hrneticka-photos, IMG_2455-2488) and Zel's new door.
 1 hall -> living passage: a door after all (Zel). Frame 82×210 like the other interior doors; swing drawn in the plan:
   hinged on the south jamb, opens into the living room (keeps the hall artwork and the corridor clear). Claude's choice.
 2 front door: hinge on the SOUTH jamb, opens against the hall south wall (IMG_2473, IMG_2474, IMG_1958). v16 had north.
 3 living south wall: AC indoor unit 85×20×33, x 853-937, 228-261 above floor (IMG_2482, IMG_2478). Not in v16.
 4 living facade wall light: x 1060 -> 1125 (just west of the sliding door's meeting stile, IMG_2483).
 5 AS BUILT group: switches, thermostats, sockets, outlets, manifold box, kitchen duct, read from the photos (±15 along
   the wall, ±10 in height unless the name says otherwise). Markers only; they do not change any design item.
Usage: build_v17.py <v16 Home.xml> <out Home.xml>"""
import copy, sys, uuid, xml.etree.ElementTree as ET
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
BOX = copy.deepcopy(one('Laundry basket'))
def group(name, after='Kitchen corner base'):
    g = ET.Element('furnitureGroup', id=nid('furnitureGroup'), name=name, x='0', y='0', width='1', depth='1', height='1')
    a = by_name(after)[0]; p = parent_of(a); p.insert(list(p).index(a) + 1, g); return g
def box(g, name, x, y, w, d, h, el, color):
    b = copy.deepcopy(BOX); b.set('id', nid('pieceOfFurniture')); b.set('name', name)
    for k, v in dict(x=x, y=y, width=w, depth=d, height=h, elevation=el).items(): b.set(k, F(float(v)))
    b.set('color', color); g.append(b); return b
BLACK, WHITE, GREY = 'FF2B2B2B', 'FFF2F2EE', 'FF9A9A9A'

# ---- 1  door hall -> living --------------------------------------------------------------------------------------------------
hdr = one('Header above hallway'); parent_of(hdr).remove(hdr)       # the wall itself now runs over the door
stub = [w for w in root.iter('wall') if w.get('id') == 'wall-s15-passage-north-stub'][0]
stub.set('id', 'wall-s15-hall-living-door'); stub.set('yEnd', '751.84')  # stub 659.71-669.71 -> full wall to 751.84, door cuts the 82×210 hole
lau = one('Door frame – laundry', 'doorOrWindow')
d = copy.deepcopy(lau); d.set('id', nid('doorOrWindow'))
d.set('name', 'Door frame – hall → living room 82×210 (new, Zel 2026-11-25; hinged on the south jamb, opens into the living room)')
d.set('x', '542'); d.set('y', F(670 + 41)); d.set('width', '82')
ET.SubElement(d, 'sash', xAxis='1', yAxis='0.5', width='1', startAngle='3.1415927', endAngle='1.5707964')
p = parent_of(lau); p.insert(list(p).index(lau) + 1, d)

# ---- 2  front door hinge on the south jamb -----------------------------------------------------------------------------------
fd = one('Front door', 'doorOrWindow')
fd.attrib.pop('modelMirrored', None)
fd.set('name', 'Front door 105×215 (security door, hinged on the south jamb, opens inward against the hall south wall; IMG_2473/2474)')

# ---- 3, 4, 5  as-built items --------------------------------------------------------------------------------------------------
G = group('AS BUILT – switches, thermostats, sockets, outlets, AC (site photos 2026-11-25, ±15 along the wall)')
box(G, 'AC indoor unit 85×20×33 – living south wall (as built, IMG_2482)', 895, 774.12 - 10, 85, 20, 33, 228, WHITE)
for e in by_name('Outdoor wall light (installed) – living facade') + by_name('Light: terrace wall lamp – living facade'):
    e.set('x', '1125')

N, S, E, W = (0, 1), (0, -1), (-1, 0), (1, 0)            # direction from the wall into the room
KIND = {'switch': (8, 8, BLACK), 'switch (white)': (8, 8, WHITE), 'thermostat': (9, 9, GREY), 'socket': (8, 8, BLACK),
        'double socket': (15, 8, BLACK), 'outlet cover': (10, 10, WHITE), 'wire box': (8, 8, GREY), 'water connections': (12, 6, GREY)}
def pt(kind, where, face, into, along, h, photo):
    w, hh, col = KIND[kind]
    if into[0] == 0: x, y, bw, bd = along, face + into[1] * 0.75, w, 1.5
    else:            x, y, bw, bd = face + into[0] * 0.75, along, 1.5, w
    box(G, f'As built: {kind} – {where}, centre {h:.0f} above floor ({photo})', x, y, bw, bd, hh, h - hh / 2, col)

LS, LN, LE, LW = 774.12, 306.47, 1464.71, 613.42
for k, a, h in (('wire box', 710, 152), ('thermostat', 724, 142), ('switch', 724, 111), ('socket', 724, 42)):
    pt(k, 'living south wall, west group' + (' (loose wires, purpose unknown)' if k == 'wire box' else ''), LS, S, a, h, 'IMG_2478, IMG_2482')
pt('switch', 'living south wall, west of the terrace door', LS, S, 967, 111, 'IMG_2482')
pt('socket', 'living south wall, east of the terrace door', LS, S, 1364, 44, 'IMG_2482')
pt('socket', 'living north wall, kitchen corner', LN, N, 652, 47, 'IMG_2480')
pt('switch', 'living north wall, east of the window', LN, N, 1105, 110, 'IMG_2480')
for a in (1347, 1378): pt('socket', 'living north wall, TV', LN, N, a, 43, 'IMG_2480')
pt('switch', 'living east wall, south of the window', LE, E, 607, 109, 'IMG_2481')
pt('socket', 'living east wall, south of the window', LE, E, 607, 35, 'IMG_2481')
pt('socket', 'kitchen west wall, worktop', LW, W, 379, 119, 'IMG_2479')
pt('socket', 'kitchen west wall, sink base', LW, W, 465, 58, 'IMG_2479')
pt('water connections', 'kitchen west wall, sink', LW, W, 490, 48, 'IMG_2479')
pt('socket', 'kitchen west wall, fridge', LW, W, 626, 57, 'IMG_2479')
box(G, 'As built: kitchen exhaust duct outlet Ø12 – north wall, 50 from the NW corner, under the ceiling (IMG_2479, IMG_2480)', 663, 312, 12, 12, 14, 262, GREY)
pt('switch', 'hall north wall, east of the bedroom door', 659.71, N, 392, 110, 'IMG_2473, IMG_2019')
pt('switch', 'hall south wall, under the distribution board', 765.73, S, 250, 100, 'IMG_1958, IMG_2475')
pt('switch', 'bedroom east wall, NE corner', 603.4, E, 320, 109, 'IMG_2467')
pt('socket', 'bedroom east wall, north bedside', 603.4, E, 356, 62, 'IMG_2467')
pt('socket', 'bedroom east wall, south bedside (behind the bed frame in v16)', 603.4, E, 569, 60, 'IMG_2467')
for k, h in (('thermostat', 140), ('switch', 110), ('socket', 30)): pt(k, 'bedroom south wall, between door and shaft', 649.77, S, 400, h, 'IMG_2468')
pt('switch', 'bedroom west wall, south of the ensuite door (inside the v16 wardrobe)', 232.93, W, 473, 110, 'IMG_2469')
pt('double socket', 'bedroom west wall (behind the v16 wardrobe)', 232.93, W, 517, 39, 'IMG_2469')
pt('outlet cover', 'ensuite north wall, mirror-light outlet above the west basin (±10)', 306.47, N, 95, 200, 'IMG_2471')
pt('switch (white)', 'ensuite east wall, north of the door (height ±20)', 222.93, E, 344, 130, 'IMG_2472')
pt('thermostat', 'ensuite east wall, north of the door (height ±20)', 222.93, E, 360, 120, 'IMG_2472')
pt('thermostat', 'bathroom north wall, west of the door', 778.25, N, 262, 140, 'IMG_2476')
pt('switch (white)', 'bathroom east wall, north of the basin (height ±20)', 424.9, E, 849, 130, 'IMG_2477')
pt('switch', 'laundry west wall, north of the door', 547.03, W, 858, 110, 'IMG_2459')
pt('outlet cover', 'laundry west wall, above the switch (purpose unknown)', 547.03, W, 858, 150, 'IMG_2459')
for a in (673, 734): pt('socket', 'laundry north wall, washer/dryer', 783.9, N, a, 100, 'IMG_2458')
pt('water connections', 'laundry north wall, washer tap', 783.9, N, 650, 88, 'IMG_2458')
pt('water connections', 'laundry north wall, washer drain', 783.9, N, 674, 36, 'IMG_2458')
box(G, 'As built: floor-heating manifold box 90×55 – laundry south wall, west end, 5-60 above floor (IMG_2456, IMG_2457)', 594, 949.52 - 1.5, 90, 3, 55, 5, WHITE)
pt('switch', 'room 5 south wall, east of the window', 1348, S, 483, 105, 'IMG_2460')
pt('double socket', 'room 5 east wall, under the desk', 536.97, E, 1286, 40, 'IMG_2462')
for k, h in (('thermostat', 140), ('switch', 110), ('socket', 30)): pt(k, 'room 5, wall face west of the door', 1070.7, N, 442, h, 'IMG_2461, IMG_2462')
pt('socket', 'room 5 west wall, north end', 224.93, W, 1080, 30, 'IMG_2461')
for k, h, a in (('thermostat', 139, 1072), ('switch', 110, 1068), ('socket', 39, 1065)): pt(k, 'Sara west wall, south of the door', 547.03, W, a, h, 'IMG_2464, IMG_2465')
pt('socket', 'Sara north wall', 962.06, N, 657, 30, 'IMG_2465')
pt('switch', 'Sara east wall, south of the terrace door (height ±15)', 821.85, E, 1120, 100, 'IMG_2466, IMG_2463')
pt('double socket', 'Sara east wall, under the desk', 821.85, E, 1215, 40, 'IMG_2466')
pt('switch', 'Sara south wall, west of the double door (±20)', 1348, S, 630, 110, 'IMG_2463, IMG_2464')

root.set('name', 'S15-Hrneticka-v17.sh3d')
tree.write(DST, encoding='UTF-8', xml_declaration=True)
print('as-built items', len(list(G)), 'lights', len(list(root.iter('light'))))
