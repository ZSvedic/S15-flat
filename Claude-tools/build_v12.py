#!/usr/bin/env python3
"""S15-Hrneticka v10 -> v12 Home.xml. Shell changes confirmed by Zel on 2026-10-21.
Evidence order: site photos with measurements > architect plan (Building-docs/S15-architect-plan.pdf) > old files.
Usage: build_v12.py <v10 Home.xml> <out Home.xml>"""
import copy, sys, uuid
import xml.etree.ElementTree as ET

SRC, DST = sys.argv[1], sys.argv[2]
tree = ET.parse(SRC)
root = tree.getroot()
CEIL = 280.0
TERR = 16.0                # terrace/balcony tiles at +9.16 vs +9.00 inside
TILE = 'FFC9BEAE'          # installed beige stone-look bathroom tiles
WALL = 'FFF0EFE6'

def nid(p): return f'{p}-{uuid.uuid4()}'
def by_name(prefix, tag=None):
    return [e for e in root.iter() if (tag is None or e.tag == tag) and (e.get('name') or '').startswith(prefix)]
def one(prefix, tag=None):
    l = by_name(prefix, tag); assert len(l) == 1, (prefix, len(l)); return l[0]
def by_id(i):
    for e in root.iter():
        if e.get('id') == i: return e
    raise KeyError(i)
def setf(e, **kw):
    for k, v in kw.items():
        e.set(k, f'{v:.2f}'.rstrip('0').rstrip('.') if isinstance(v, float) else str(v))
def parent_of(e):
    for p in root.iter():
        if e in list(p): return p
def remove(e): parent_of(e).remove(e)
def add_after(ref, new):
    p = parent_of(ref); p.insert(list(p).index(ref) + 1, new); return new

BOX = copy.deepcopy(one('Laundry basket'))           # eTeks texturableBox
ANCHOR = one('Kitchen corner base')
def box(name, x, y, w, d, h, el=0.0, color=WALL):
    b = copy.deepcopy(BOX); b.set('id', nid('pieceOfFurniture')); b.set('name', name)
    setf(b, x=float(x), y=float(y), width=float(w), depth=float(d), height=float(h), color=color)
    if el: setf(b, elevation=float(el))
    return add_after(ANCHOR, b)

# 5. Ceiling 260 -> 280
root.set('wallHeight', str(CEIL))
for w in root.iter('wall'):
    w.set('height', str(CEIL))
for e in by_name('Accent wall'):
    e.set('height', str(CEIL - 1))
setf(one('Cooker hood 80'), height=130.0)            # still reaches the ceiling
for p in by_name('Pendant lamp'):
    setf(p, height=130.0)                             # cord to the 280 ceiling, shade stays 75 above table
bw = one('Built-in wardrobe')
setf(bw, height=CEIL - 2)
bw.set('name', 'Built-in wardrobe 181×56×278 (made to measure, niche)')

# 3. Windows 170 high on a 90 sill (plan widths)
for i, w, x in (('doorOrWindow-0578679c-8295-48c9-a177-38fa07e2a25f', 200.0, 977.0),   # living north
                ('doorOrWindow-a4474cc0-1c18-41b5-bb7a-323e48b6bcad', 220.0, None),    # living east
                ('doorOrWindow-8137f9b7-8b9a-43fa-a89a-da66be03e317', 160.0, 371.0)):  # room 5 south
    e = by_id(i)
    setf(e, width=w, height=170.0, elevation=90.0)
    if x: setf(e, x=x)
    e.set('name', f'Window {int(w)}×170, sill 90')

# 1. Living -> terrace sliding door: plan 300×240 on 20 threshold (width not measured on site)
sl = by_id('doorOrWindow-eb71b2d8-3d93-4135-9452-fa8bce81ff14')
setf(sl, width=300.0, height=240.0, elevation=20.0)
sl.set('name', 'Terrace lift-and-slide door 300×240, threshold 20 (width from plan, not measured)')

# 2. Laundry + Sara east terrace doors 80×240 on 20 threshold
for i, y, nm in (('doorOrWindow-58a7da34-0501-4c8f-9215-7d0e4a996316', 907.0, 'Terrace door – laundry 80×240, threshold 20'),
                 ('doorOrWindow-2f2824c7-6789-4b04-a522-847631ab77c5', None, "Terrace door – Sara east 80×240, threshold 20")):
    e = by_id(i)
    setf(e, width=80.0, height=240.0, elevation=20.0)
    if y: setf(e, y=y)
    e.set('name', nm)

# Q3. Sara south: double French door as built, 160×250, sill 10 (her second exit to the terrace)
sd = by_id('doorOrWindow-e19dc38c-04d3-4bfd-89f4-d45c5af69e3d')
setf(sd, x=728.0, width=160.0, height=250.0, elevation=10.0)
sd.set('name', 'Terrace door Sara south 160×250, sill 10 (double, opens inward)')

# 4. Bedroom north: 300×245 three-panel window on a 15 sill, middle panel opens to the balcony
old = by_id('doorOrWindow-c2f7c524-5888-4a0f-9653-55fcfeb701cb')
casement = by_id('doorOrWindow-58a7da34-0501-4c8f-9215-7d0e4a996316')
fixed = one('Shower glass panel', 'doorOrWindow')
prev = old
for x, kind in ((348.0, 'fixed'), (448.0, 'open'), (548.0, 'fixed')):
    e = copy.deepcopy(casement if kind == 'open' else fixed)
    e.set('id', nid('doorOrWindow'))
    e.set('name', 'Bedroom window 300×245, sill 15 – ' + ('middle, opens to balcony' if kind == 'open' else 'fixed side panel'))
    setf(e, x=x, y=290.59, angle=0.0, width=100.0, depth=31.76, height=245.0, elevation=15.0)
    e.attrib.pop('description', None)
    if kind == 'fixed':
        e.set('boundToWall', 'true'); e.set('wallThickness', '1.0'); e.set('wallDistance', '0.0')
    prev = add_after(prev, e)
remove(old)

# Q2. Header strip above the hallway -> living passage (no door), plan wall line x≈538, opening top 210
box('Header above hallway → living passage (no door)', 538.24, 718.24, 11.76, 111.77, CEIL - 210, el=210)

# 6. Ventilation shaft box in the master bedroom south wall, next to the door
box('Installation shaft (ventilation) 66×20 – bedroom south wall', 452.8, 640.6, 66, 20, CEIL)
pic = one('Picture 60×80 (bedroom south wall)')
setf(pic, x=540.0)

# 7. Second bathroom: door in the north wall (from the hallway), basin east wall, WC west wall, pipe box by the bath
bd = by_id('doorOrWindow-86d90032-ea6f-4a21-967a-493146e9162a')
setf(bd, x=325.0, y=772.94, angle=0.0, width=70.0)
bd.set('name', 'Door frame – bathroom 70 (north wall, from hallway)')
wcs = by_name('Toilet unit')
bath_wc = [w for w in wcs if float(w.get('x')) > 200][0]
setf(bath_wc, x=252.25, y=824.0, angle=4.712389)
wb = [w for w in by_name('Washbasin') if float(w.get('y')) > 700][0]
setf(wb, x=398.3, y=887.0, angle=1.5707964)
box('Pipe box 28×65 beside bath – bathroom, tiled', 406.5, 971.5, 28, 65, CEIL, color=TILE)
# hallway items that were on that wall
setf(one('Shoe bench'), x=455.0, y=678.35, angle=0.0)
for k, h in enumerate(by_name('Coat hook')):
    setf(h, x=416.0 + 26 * k, y=665.1, angle=0.0)
setf(one('Picture 100×70 (hallway'), x=92.0, y=765.9, angle=3.1415927)
box('Distribution board (elektroormar) 45×10×60', 255.0, 762.0, 45, 10, 60, el=110, color='FFF4F4F2')
box('Media box 35×8×35', 255.0, 763.0, 35, 8, 35, el=185, color='FFF4F4F2')

# 8. Ensuite: tiled installation ledge behind the WC
ens_wc = [w for w in wcs if float(w.get('x')) < 100][0]
setf(ens_wc, x=89.25, y=476.0)
box('WC installation ledge 21×72×115 – ensuite, tiled', 46.5, 476.0, 21, 72, 115, color=TILE)

# 9. Both bathrooms: beige stone-look tiles floor to ceiling
for rn in ('Kupaonica 2', 'Kupaonica'):
    rm = [r for r in root.iter('room') if r.get('name') == rn][0]
    for c in list(rm):
        if c.tag == 'texture' and c.get('attribute') == 'floorTexture': rm.remove(c)
    rm.set('floorColor', TILE)
for e in by_name('Wall tiles'):
    e.set('name', 'Wall tiles – beige stone-look, floor to ceiling (installed)')
    e.set('height', str(CEIL - 1))
    for c in list(e):
        if c.tag == 'texture': e.remove(c)
    e.set('color', TILE)
tiles = [t for t in by_name('Wall tiles') if abs(float(t.get('x')) - 320.3) < 0.5 and abs(float(t.get('y')) - 779.1) < 0.5]
north = tiles[0]
setf(north, x=255.0, width=70.0)                     # west of the door
n2 = copy.deepcopy(north); n2.set('id', nid('pieceOfFurniture'))
setf(n2, x=390.3, width=60.6)                         # east of the door
add_after(north, n2)
east = [t for t in by_name('Wall tiles') if abs(float(t.get('x')) - 420.3) < 0.5]
setf(east[0], y=891.1, depth=224.7)                   # old door gap is now wall
remove(east[1])

# 12. Terrace + balcony tiles at +16: raise everything standing outside
def inside(poly, x, y):
    c = False
    for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1: c = not c
    return c
T9 = [(849, 807), (1409, 807), (1409, 1573), (645, 1573), (645, 1384), (849, 1384)]
T10 = [(15, 29), (782, 29), (782, 275), (15, 275)]
SKIP = ('Balcony parapet', 'Glass balustrade', 'Outdoor wall lantern')
def raise_el(e): e.set('elevation', f"{float(e.get('elevation', '0')) + TERR:.2f}")
for e in list(root):
    if e.tag not in ('pieceOfFurniture', 'furnitureGroup', 'light'): continue
    nm = e.get('name') or ''
    if nm.startswith(SKIP): continue
    x, y = float(e.get('x')), float(e.get('y'))
    if nm.startswith(('TERRACE FLOOR', 'SHADE')) or inside(T9, x, y) or inside(T10, x, y):
        raise_el(e)
        if e.tag == 'furnitureGroup':
            for c in e.iter():
                if c is not e and c.tag in ('pieceOfFurniture', 'light', 'doorOrWindow', 'furnitureGroup'): raise_el(c)

# 10. Balcony parapet 100 above the tiles (IMG_2005)
for e in by_name('Balcony parapet'):
    e.set('height', str(TERR + 100))
    e.set('name', 'Balcony parapet, 100 above balcony tiles (measured)')
# Q4. Normal-height table + 2 outdoor chairs instead of bar table + stools
tbl = one('Bar-height bistro table')
tbl.set('name', 'Bistro table Ø60 (seated view of Sljeme over the 100 parapet)')
setf(tbl, height=75.0)
chair_tpl = by_name('Outdoor chair')[0]
for st, (x, ang) in zip(by_name('Bar stool'), ((168.0, 4.712389), (276.0, 1.5707964))):
    c = copy.deepcopy(chair_tpl); c.set('id', nid('pieceOfFurniture')); c.set('name', 'Outdoor chair (balcony)')
    setf(c, x=x, y=163.0, angle=ang, elevation=TERR)
    add_after(st, c); remove(st)

# 11. Terrace railing: 60 upstand + point-fixed glass, top 117 above tiles (IMG_2010)
UP = 'FFE6E1D8'
box('Terrace upstand, 60 above tiles – east', 1420.0, 1201.0, 22, 788, TERR + 60, color=UP)
box('Terrace upstand, 60 above tiles – south', 1027.0, 1584.0, 786, 22, TERR + 60, color=UP)
box('Terrace upstand, 60 above tiles – west of strip', 634.0, 1489.5, 22, 211, TERR + 60, color=UP)
for g in by_name('Glass balustrade panel'):
    x, y = float(g.get('x')), float(g.get('y'))
    if abs(x - 1411) < 1: x = 1432.0
    elif abs(y - 1575) < 1: y = 1596.0
    elif abs(x - 643) < 1: x = 622.0
    setf(g, x=x, y=y, elevation=TERR + 30, height=87.0)
    g.set('name', 'Glass balustrade panel (point-fixed to upstand, top 117 above tiles)')

# 13. Installed fixtures: tiles shown by default, tap, 2 terrace wall lights (IMG_2026, IMG_2029)
for e in root.iter('furnitureGroup'):
    n = e.get('name') or ''
    if n.startswith('TERRACE FLOOR A'): e.set('name', 'TERRACE FLOOR A – wood decking (off)')
    if n.startswith('TERRACE FLOOR B'): e.set('name', 'TERRACE FLOOR B – tiles 60×60, installed (on)')
one('Outdoor sink').set('name', 'Outdoor sink 60×50 at the installed tap (between laundry and Sara doors)')
lan = [l for l in by_name('Outdoor wall lantern', 'pieceOfFurniture') if 'balcony' not in l.get('name')]
setf(lan[0], x=1060.0, y=813.1, elevation=270.0, angle=0.0)
lan[0].set('name', 'Outdoor wall light (installed) – living facade, above the sliding door')
setf(lan[1], x=855.4, y=1135.0, elevation=270.0, angle=4.712389)
lan[1].set('name', "Outdoor wall light (installed) – east facade, south of Sara's door")

tree.write(DST, encoding='UTF-8', xml_declaration=True)
print('ok')
