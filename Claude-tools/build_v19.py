#!/usr/bin/env python3
"""S15-Hrneticka v18 -> v19 Home.xml: Zel's answers to the v18 review (2026-11-26).
 1a bedroom north window: the WEST panel opens to the balcony, not the middle one (IMG_1956, Zel). The opening panel and the
    fixed panel swap places; hinge on the west jamb, handle at the joint with the middle panel. C9 (bed vs balcony door) is gone.
 1b Sara south double door: only the WEST leaf opens (IMG_1962, Zel); the east leaf is fixed. Plan swing for the west leaf only.
 3  Sara: green desk lamp removed; pinboard on the east wall centred over the desk, half-way between the desk top (75) and the
    wall light A16 (bottom 167); side table -> C side table 50×32×62 (slides over the bed or next to the chair, like Zel's photo);
    east tub chair -> beanbag Ø75.
 C11 laundry ceiling drying rack 10 west, out of the terrace door's swing.
Usage: build_v19.py <v18 Home.xml> <out Home.xml>"""
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
BOX = copy.deepcopy(one('Laundry basket'))
def box(parent, before, name, x, y, w, d, h, el, color):
    b = copy.deepcopy(BOX); b.set('id', nid('pieceOfFurniture')); b.set('name', name)
    for k, v in dict(x=x, y=y, width=w, depth=d, height=h, elevation=el).items(): b.set(k, F(float(v)))
    b.set('color', color); b.attrib.pop('angle', None)
    parent.insert(list(parent).index(before), b); return b
OAK = 'FFD2AE7E'

# ---- 1a  bedroom: west panel opens ---------------------------------------------------------------------------------------------
west = [e for e in by_name('Bedroom window 300×245, sill 15 – fixed side panel', 'doorOrWindow') if float(e.get('x')) < 400]
mid = one('Bedroom window 300×245, sill 15 – middle, opens to balcony', 'doorOrWindow')
assert len(west) == 1; west = west[0]
xw, xm = west.get('x'), mid.get('x')
mid.set('x', xw); west.set('x', xm)
mid.set('name', 'Bedroom window 300×245, sill 15 – west panel, opens to the balcony (hinge west, handle at the middle panel; IMG_1956, Zel v19)')
west.set('name', 'Bedroom window 300×245, sill 15 – fixed middle panel (v19)')

# ---- 1b  Sara south double door: only the west leaf opens -------------------------------------------------------------------------
sd = one('Terrace door Sara south 160×250', 'doorOrWindow')
a = float(sd.get('angle', 0)); w = float(sd.get('width'))
sashes = [s for s in sd if s.tag == 'sash']; assert len(sashes) == 2
def hinge_x(s): return float(sd.get('x')) + (float(s.get('xAxis')) - 0.5) * w * math.cos(a)
east_sash = max(sashes, key=hinge_x); sd.remove(east_sash)
assert hinge_x([s for s in sd if s.tag == 'sash'][0]) < 670
sd.set('name', 'Terrace door Sara south 160×250, sill 10 (double; only the west leaf opens, inward, hinge west; east leaf fixed; IMG_1962, Zel v19)')

# ---- 3  Sara's room ---------------------------------------------------------------------------------------------------------------
lamp = one('Desk lamp Sara', 'light'); parent_of(lamp).remove(lamp)
desk = one('Desk 120×50'); top = float(desk.get('height'))                       # 75
a16 = one('A16 wall light up/down'); bottom = float(a16.get('elevation'))        # 167
mb = one('Memo board 100×60'); h = float(mb.get('height'))
mb.set('y', desk.get('y')); mb.set('elevation', F((top + bottom) / 2 - h / 2))
mb.set('name', f'Pinboard 100×60 – Sara east wall, centred over the desk, half-way between the desk top ({top:.0f}) and wall light A16 ({bottom:.0f}): {top + (bottom - top) / 2 - h / 2:.0f}-{(top + bottom) / 2 + h / 2:.0f} (v19)')

st = one('Side table Ø45'); p = parent_of(st)
# C table: open side to the west (towards the bed / the chair), upright on the east side
CX, CY, CW, CD, CH = 668, 1250, 50, 32, 62
box(p, st, 'C side table 50×32×62, oak – Sara, top (slides over the bed or sits by the chair; moves out of the terrace door swing) (v19)', CX, CY, CW, CD, 2, CH - 2, OAK)
box(p, st, 'C table upright – Sara', CX + CW / 2 - 1, CY, 2, CD, CH - 4, 2, OAK)
box(p, st, 'C table foot – Sara (slides under the bed)', CX - 1, CY, CW - 2, CD - 2, 2, 0, OAK)
p.remove(st)

chairs = by_name('Corner tub chair 56×56'); east = max(chairs, key=lambda e: float(e.get('x')))
bb = copy.deepcopy(BOX); bb.set('id', nid('pieceOfFurniture'))
bb.set('name', 'Beanbag Ø75×65 – Sara SE corner (v19, replaces the east tub chair)')
for k, v in dict(x=780, y=1305, width=75, depth=75, height=65, elevation=0).items(): bb.set(k, F(v))
bb.set('model', 'v19/beanbag.obj'); bb.set('color', 'FFB79A97'); bb.set('backFaceShown', 'true'); bb.set('modelSize', str(__import__('os').path.getsize('Claude-tools/models/beanbag.obj'))); bb.attrib.pop('angle', None)
bb.attrib.pop('catalogId', None)
pe = parent_of(east); pe.insert(list(pe).index(east), bb); pe.remove(east)

# ---- C11  laundry drying rack 10 west --------------------------------------------------------------------------------------------
rk = one('Ceiling drying rack 120×40'); rk.set('x', F(float(rk.get('x')) - 10))
rk.set('name', 'Ceiling drying rack 120×40 (v19: 10 west, out of the terrace door swing)')

root.set('name', 'S15-Hrneticka-v19.sh3d')
tree.write(DST, encoding='UTF-8', xml_declaration=True)
print('lights', len(list(root.iter('light'))), 'pinboard el', mb.get('elevation'))
