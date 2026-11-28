#!/usr/bin/env python3
"""Hrneticka v21 -> v22 Home.xml (Zel, 2026-11-27/28; draft "Decided for the next version", rows 1-17).
 5  mirror border lights (light strip round the mirror edge, about 1,000 lm per mirror, 3000 K, ceiling group):
    en-suite mirror 140x70 -> 140x95 (bottom 115, top 210: covers the outlet at 200); the guest bathroom gets a mirror
    55x95 over the basin on the east wall (bottom 115, top 210). The old mirror lights (pieces and sources) are removed.
 9  laundry wall light 10 (A10): lights renamed AmbL -> own lamp set 'laundrywall', rendered in the ceiling group.
 11 wide-beam GU10 (60 deg) for the down lamps over the desks: Sara 16 and room 5 13 (lights renamed AmbW down).
 13 bedroom wardrobe top: 5 cm lip on the east (front) edge, LED up-light bar behind it aimed at the west wall (ambient).
 14 the 3dwarehouse up/down wall lights turned so the base plate is on the wall (bedroom 2, 3; Sara 15; room 5 12).
    The model's base plate is at its front (+depth), so: east wall angle 3pi/2, west wall angle pi/2. Sources moved to the
    cylinder centre (1.75 from the piece centre, away from the wall).
 15 Sara wardrobe top: the same lip and bar on the south (front) edge, aimed at the north wall (ambient).
 16 Sara: A17 removed; reading light 15 moved south to y 1250 (98 from the south wall), same height.
 17 room 5: A13 and A14 replaced by one light over the desk centre (east wall, y 1265, 175 high); Gnijezdo print removed.
 Rows 1, 2, 4, 8 (lamp data) are in groups.json and make_lights.py.
Usage: build_v22.py <v21 Home.xml> <out Home.xml>"""
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
def remove(prefix, n=None, tag=None):
    es = by_name(prefix, tag); assert es and (n is None or len(es) == n), (prefix, len(es))
    for e in es: parent_of(e).remove(e)
def setf(e, **kv):
    for k, v in kv.items(): e.set(k, F(v))
amb = one('AMBIENT A', 'furnitureGroup')
BAR = copy.deepcopy(by_name('Shelf bar x:', 'light')[0])               # template for one 4-source bar element
def bar(name, x, y, z, parent):
    l = copy.deepcopy(BAR); l.set('id', nid('light')); l.set('name', name); setf(l, x=x, y=y, elevation=z); parent.append(l); return l
log = []

# ---- 14 + 16  3dwarehouse wall lights: base on the wall; Sara 15 moved south ------------------------------------------------
HALF, CYL = 11.5 / 2, 1.75                                               # half depth; cylinder centre offset from the piece centre
for gname, wall_x, side, newy in (('Wall light L', 603, +1, None), ('Wall light R', 603, +1, None),
                                  ('Wall reading light (guests)', 225, -1, None), ('Bed reading light', 547, -1, 1250)):
    g = one(gname, 'furnitureGroup'); piece = [c for c in g if c.tag == 'pieceOfFurniture'][0]
    ang = 3 * math.pi / 2 if side > 0 else math.pi / 2                   # base plate (model front) towards the wall
    px = wall_x - side * HALF; py = newy if newy is not None else float(piece.get('y'))
    cx = px - side * CYL                                                 # cylinder centre, off the wall
    for e in (g, piece): setf(e, x=px, y=py, angle=ang)
    setf(g, width=8, depth=11.5)
    for l in [c for c in g if c.tag == 'light']: setf(l, x=cx, y=py, angle=ang)
    log.append(f'{gname}: piece x {px:.2f} y {py:.2f} angle {ang:.4f}, sources x {cx:.2f}')

# ---- 16  Sara: A17 out ------------------------------------------------------------------------------------------------------
remove('A17', 2, 'pieceOfFurniture'); remove('AmbA up: A17', 1); remove('AmbA down: A17', 1)

# ---- 17  room 5: one desk light at y 1265; A14 and the Gnijezdo print out ---------------------------------------------------
remove('A14', 2, 'pieceOfFurniture'); remove('AmbA up: A14', 1); remove('AmbA down: A14', 1)
remove('Wall shelf print 45×90 (Gnijezdo)', 1)
DY = 1265
for e in by_name('A13', 'pieceOfFurniture'):
    e.set('name', e.get('name').split(' – ')[0] + ' – room 5 east wall, over the desk centre, 83 from the south wall' + (' (centre 175 above floor)' if 'bracket' not in e.get('name') else '') + ' (v22)')
    setf(e, y=DY)
for pre in ('AmbA up: A13', 'AmbA down: A13'):
    l = one(pre); setf(l, y=DY)
    l.set('name', pre.replace('AmbA down', 'AmbW down') + ' room 5 east wall, over the desk centre (v22)')

# ---- 11  Sara 16: wide-beam down lamp -----------------------------------------------------------------------------------------
l = one('AmbA down: A16'); l.set('name', l.get('name').replace('AmbA down', 'AmbW down', 1))

# ---- 9  laundry light 10: own switch (rendered in the ceiling group) ------------------------------------------------------------
for pre in ('AmbA up: A10', 'AmbA down: A10'):
    l = one(pre); l.set('name', l.get('name').replace('AmbA', 'AmbL', 1) + ' (v22: own switch)')

# ---- 13 + 15  wardrobe tops: lip on the front edge + up-light bar aimed at the wall behind ---------------------------------------
LIP = one('A06/07 shelf lip')
def wardrobe_top(tag, room, axis, front, wall, c0, length, n, top=236):
    lip = copy.deepcopy(LIP); lip.set('id', nid('pieceOfFurniture'))
    lip.set('name', f'{tag} wardrobe lip {length:.0f}×2×5 – raised front edge of the {room} wardrobe top, hides the up-light bar (top {top + 5}) (v22)')
    step = length / n; src = front - math.copysign(2.5, front - wall)    # bar 2.5 behind the lip, on the wardrobe top
    if axis == 'y':                                                      # wardrobe runs north-south, front faces east/west
        setf(lip, x=front - math.copysign(1, front - wall), y=c0, width=2, depth=length, elevation=top)
    else:
        setf(lip, x=c0, y=front - math.copysign(1, front - wall), width=length, depth=2, elevation=top)
    amb.append(lip)
    for i in range(n):
        t = c0 - length / 2 + step * (i + 0.5)
        if axis == 'y': x, y, aim = src, t, (wall, t, 275)
        else: x, y, aim = t, src, (t, wall, 275)
        bar(f'Top bar {axis}: {tag} {room} wardrobe top up-light {i + 1:02d} -> {F(aim[0])},{F(aim[1])},{F(aim[2])}', x, y, top + 1.5, amb)
    log.append(f'{tag}: lip + {n} bar elements ({4 * n} sources) along {axis}, front {front}, aimed at wall {wall}')
wb = one('Wardrobe 160×65'); assert abs(float(wb.get('angle')) - 3 * math.pi / 2) < 1e-3
wardrobe_top('A20', 'bedroom', 'y', float(wb.get('x')) + 32.5, 233, float(wb.get('y')), 160, 8)
ws = one('Wardrobe 150×60'); assert ws.get('angle') is None
wardrobe_top('A21', 'Sara', 'x', float(ws.get('y')) + 30, 962, float(ws.get('x')), 150, 7)

# ---- 5  mirror border lights ------------------------------------------------------------------------------------------------------
remove('Mirror light 60', 1); remove('Mirror light 50', 1); remove('Light: mirror', 2)
me = one('Mirror 140×70 over washbasins'); setf(me, height=95, elevation=115)
me.set('name', 'Mirror 140×95 with border light – ensuite, over the washbasins (top 210 covers the outlet at 200) (v22)')
mb = copy.deepcopy(me); mb.set('id', nid('pieceOfFurniture')); parent_of(me).append(mb)
setf(mb, x=424, y=885.44, width=55, depth=2, height=95, elevation=115, angle=math.pi / 2)
mb.set('name', 'Mirror 55×95 with border light – guest bathroom, east wall over the basin (top 210) (v22)')
def border(tag, w, h, el, along, fixed, normal, centre, lm_total):
    """Light strip round the mirror edge, 2.5 in from the edge, 1.5 in front; elements of 4 sources aimed straight out."""
    els = []
    ih, iv = w - 5, h - 5; nh, nv = max(2, round(ih / 20)), max(2, round(iv / 20))
    for zz in (el + 2.5, el + h - 2.5):
        for i in range(nh): els.append(('x' if along == 'x' else 'y', centre - ih / 2 + ih / nh * (i + 0.5), zz))
    for s in (-1, 1):
        for i in range(nv): els.append(('z', centre + s * (w / 2 - 2.5), el + 2.5 + iv / nv * (i + 0.5)))
    lm = lm_total / (4 * len(els)); pos = fixed + 1.5 * normal
    for k, (ax, t, zz) in enumerate(els):
        if along == 'x': x, y, aim = t, pos, (t, pos + 100 * normal, zz)
        else: x, y, aim = pos, t, (pos + 100 * normal, t, zz)
        bar(f'Mirror bar {ax}: {tag} mirror border light {k + 1:02d} {{lm={lm:.2f} beam=120 k=3000 r=1}} -> {F(aim[0])},{F(aim[1])},{F(aim[2])}', x, y, zz, root)
    log.append(f'{tag} mirror border: {len(els)} elements, {4 * len(els)} sources x {lm:.2f} lm = {lm_total} lm')
border('ensuite', 140, 95, 115, 'x', 308.51 + 1, +1, float(me.get('x')), 1000)
border('bathroom', 55, 95, 115, 'y', 424 - 1, -1, 885.44, 1000)

root.set('name', 'Hrneticka-v22.sh3d')
tree.write(DST, encoding='UTF-8', xml_declaration=True)
print('\n'.join(log)); print('lights', len(list(root.iter('light'))), 'pieces', len(list(root.iter('pieceOfFurniture'))))
