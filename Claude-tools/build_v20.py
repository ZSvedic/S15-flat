#!/usr/bin/env python3
"""S15-Hrneticka v19 -> v20 Home.xml (Zel, 2026-11-26).
 TV shelf (250×25, living north wall, top 189): a raised lip along its south (front) edge hides an LED up-light bar on the shelf
 top, like the corridor niche profile but pointing up and dimmer (150 lm/m instead of 350, the shelf is long). Light group: ambient.
Usage: build_v20.py <v19 Home.xml> <out Home.xml>"""
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

sh = one('A06/07 shelf 250×25 over the TV panel')
x, y, w, d = (float(sh.get(k)) for k in ('x', 'y', 'width', 'depth'))
top = float(sh.get('elevation')) + float(sh.get('height'))          # 189
front = y + d / 2                                                   # south edge
p = parent_of(sh); i = list(p).index(sh) + 1
lip = copy.deepcopy(sh); lip.set('id', nid('pieceOfFurniture'))
lip.set('name', f'A06/07 shelf lip 250×2×5 – raised south edge of the TV shelf, hides the up-light bar (top {top + 5:.0f}) (v20)')
for k, v in dict(x=x, y=front - 1, width=w, depth=2, height=5, elevation=top).items(): lip.set(k, F(v))
p.insert(i, lip)
SRC_L = by_name('Niche bar y', 'light')[0]
n = int(w // 20)                                                     # one source per 20 cm of strip (make_lights splits it in 4)
x0 = x - n * 20 / 2 + 10
for k in range(n):
    l = copy.deepcopy(SRC_L); l.set('id', nid('light')); lx = x0 + 20 * k; ly = front - 4
    l.set('name', f'Shelf bar x: TV shelf up-light behind the lip {k + 1:02d} -> {F(lx)},{F(ly)},280')
    for kk, v in dict(x=lx, y=ly, elevation=top + 1.5).items(): l.set(kk, F(v))
    p.insert(i + 1 + k, l)
root.set('name', 'S15-Hrneticka-v20.sh3d')
tree.write(DST, encoding='UTF-8', xml_declaration=True)
print('shelf top', top, 'front', front, 'sources', n)
