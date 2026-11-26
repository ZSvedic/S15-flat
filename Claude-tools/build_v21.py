#!/usr/bin/env python3
"""S15-Hrneticka v20 -> v21 Home.xml (Zel, 2026-11-26).
 a  living desk: the two ceiling spots on their track (A05) removed; overhead picture light 45 on an 18 cm arm over the bicycle
    picture on the north wall, like the other two pictures; light set artD in the ambient group.
 c  laundry less white: tall utility cabinet and the shelf over the machines in oak; the six as-built ceiling spots use the real
    GU10 lamp (IKEA LEDARE, 345 lm, 36°, the lamp Zel uses) instead of the assumed 400 lm wide spot (rule in make_lights.py).
 (b, day exposure, is in mix.py.)
Usage: build_v21.py <v20 Home.xml> <out Home.xml>"""
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
def remove(prefix, n=None):
    es = by_name(prefix); assert es and (n is None or len(es) == n), (prefix, len(es))
    for e in es: parent_of(e).remove(e)
BRASS, OAK = 'FFB8975A', 'FFC9A27A'

# ---- a  desk spots out, picture light over the bicycle picture ------------------------------------------------------------------
remove('A05', 3); remove('Desk aim:', 2)
pic = one('Picture: tandem bicycle patent'); PX = float(pic.get('x')); WALL = 305.88
top = float(pic.get('elevation')) + float(pic.get('height')); cz = float(pic.get('elevation')) + float(pic.get('height')) / 2
EL = top + 12                                                           # tube centre, as for the east painting
tube = copy.deepcopy(one('A08 picture light 60')); arm = copy.deepcopy(one('A08 picture light arm'))
src = copy.deepcopy(by_name('ArtE bar y: A08', 'light')[0])
amb = one('AMBIENT A', 'furnitureGroup')
for e, name, x, y, w, d, h, el in ((tube, f'A05 picture light 45 – living north wall, over the bicycle picture (tube centre {EL:.0f} above floor, 18 from the wall) (v21)', PX, WALL + 18, 45, 3, 3, EL - 1.5),
                                   (arm, 'A05 picture light arm – living north wall, over the bicycle picture (v21)', PX, WALL + 9, 2, 18, 2, EL - 1)):
    e.set('id', nid('pieceOfFurniture')); e.set('name', name)
    for k, v in dict(x=x, y=y, width=w, depth=d, height=h, elevation=el).items(): e.set(k, F(v))
    amb.append(e)
for i, o in enumerate((-10, 10)):
    l = copy.deepcopy(src); l.set('id', nid('light'))
    l.set('name', f'ArtD bar x: A05 living north wall, over the bicycle picture {i + 1} -> {F(PX + o)},{F(WALL)},{F(cz)}')
    for k, v in dict(x=PX + o, y=WALL + 18, elevation=EL - 4.5).items(): l.set(k, F(v))
    amb.append(l)

# ---- c  laundry ------------------------------------------------------------------------------------------------------------------
for n in ('Tall utility cabinet 59×60×200', 'Shelf over machines'):
    e = one(n); e.set('color', OAK); e.set('name', e.get('name') + ' – oak (v21)')
    for t in [c for c in e if c.tag == 'texture']: e.remove(t)

root.set('name', 'S15-Hrneticka-v21.sh3d')
tree.write(DST, encoding='UTF-8', xml_declaration=True)
print('bicycle picture top', top, 'tube', EL, 'lights', len(list(root.iter('light'))))
