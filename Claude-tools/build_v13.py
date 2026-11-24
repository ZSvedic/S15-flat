#!/usr/bin/env python3
"""S15-Hrneticka v12 -> v13 Home.xml. Changes confirmed by Zel on 2026-11-18.
A) Shell: walls re-snapped to Building-docs/S15-architect-plan.pdf (anchor: living room NE inner corner),
   wall holes of the two terrace doors fixed (stale *InPlan attributes), door sizes/positions per plan,
   hallway->living passage with stubs, corridor niche, shaft boxes, terrace/balcony edges.
B) Lights: as-built ceiling points estimated from the site photos (+-20 cm), mirror outlets and
   terrace wall lamps from the electrical plan (Mapa III p. 56).
Evidence order: site photos > architect/electrical plans > old files.
Usage: build_v13.py <v12 Home.xml> <out Home.xml>"""
import copy, re, sys, uuid
import xml.etree.ElementTree as ET

SRC, DST = sys.argv[1], sys.argv[2]
tree = ET.parse(SRC); root = tree.getroot()
WALL = 'FFF0EFE6'; TILE = 'FFC9BEAE'; WHITE = 'FFF7F6F2'
H = 280.0

def nid(p): return f'{p}-{uuid.uuid4()}'
def F(v): return f'{v:.2f}'.rstrip('0').rstrip('.')
def setf(e, **kw):
    for k, v in kw.items(): e.set(k, F(v) if isinstance(v, float) else str(v))
def by_name(prefix, tag=None):
    return [e for e in root.iter() if (tag is None or e.tag == tag) and (e.get('name') or '').startswith(prefix)]
def one(prefix, tag=None):
    l = by_name(prefix, tag); assert len(l) == 1, (prefix, len(l)); return l[0]
def by_id(i):
    for e in root.iter():
        if e.get('id') == i: return e
    raise KeyError(i)
def parent_of(e):
    for p in root.iter():
        if e in list(p): return p
def remove(e): parent_of(e).remove(e)
def fx(e, k): return float(e.get(k, '0'))

# ---------- plan-true faces (cm, model frame) ----------
XW, XE = 40.87, 1464.71            # west / east exterior inner faces
YN, YS = 305.88, 1347.99           # north / south exterior inner faces
ENS_E, BED_W, BED_E, LIV_W = 222.93, 232.93, 603.40, 613.42
ENS_S, NICHE_N = 594.80, 604.86
BED_S, HALL_N = 649.77, 659.71
HALL_S, BATH_N = 765.73, 778.25
LIV_S, LAU_N = 773.84, 783.90
PARTY, BATH_E, COR_W, COR_E, SARA_W, EAST_I = 224.93, 424.90, 434.84, 536.97, 547.02, 821.85
LAU_S, SARA_N = 949.52, 962.05
BATH_S, R5_N = 1000.90, 1010.90
R5D_N, R5D_S = 1060.65, 1070.70

# ---------- 1. furniture: move with its room (old room bbox -> new room bbox) ----------
OLD = {r.get('name'): [(float(p.get('x')), float(p.get('y'))) for p in r.findall('point')] for r in root.iter('room')}
def inside(poly, x, y):
    c = False
    for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1: c = not c
    return c
MAPS = {  # name: (old x0,x1,y0,y1) -> (new x0,x1,y0,y1)
 'Kuhinja i dnevni boravak': ((610.59, 1464.71, 305.88, 774.12), (LIV_W, XE, YN, LIV_S)),
 'Spavaća soba 1': ((228.24, 598.82, 305.88, 650.59), (BED_W, BED_E, YN, BED_S)),
 'Kupaonica 2': ((35.29, 217.65, 305.88, 594.12), (XW, ENS_E, YN, ENS_S)),
 'Kupaonica': ((220.0, 421.18, 778.82, 1003.53), (PARTY, BATH_E, BATH_N, BATH_S)),
 'Praonica': ((543.53, 818.82, 785.88, 947.06), (SARA_W, EAST_I, LAU_N, LAU_S)),
 'Spavaća soba 3': ((543.53, 818.82, 958.82, 1352.94), (SARA_W, EAST_I, SARA_N, YS)),
 'Spavaća soba 2': ((220.0, 532.94, 1015.29, 1352.94), (PARTY, COR_E, R5_N, YS)),
 'hall': ((35.29, 610.59, 605.88, 767.06), (XW, LIV_W, NICHE_N, HALL_S)),
 'corridor': ((431.76, 532.94, 767.06, 1070.59), (COR_W, COR_E, HALL_S, R5D_N)),
}
def room_of(x, y):
    for n, poly in OLD.items():
        if n.startswith('Terasa'): continue
        if inside(poly, x, y):
            if n == 'Hodnik': return 'corridor' if y > 767.06 and x < 532.94 else 'hall'
            return n
    return None
def remap(x, y):
    n = room_of(x, y)
    if n is None: return x, y, None
    (ox0, ox1, oy0, oy1), (nx0, nx1, ny0, ny1) = MAPS[n]
    return nx0 + (x - ox0) * (nx1 - nx0) / (ox1 - ox0), ny0 + (y - oy0) * (ny1 - ny0) / (oy1 - oy0), n
def leaves(e):
    for c in e:
        if c.tag in ('pieceOfFurniture', 'light', 'doorOrWindow', 'furnitureGroup'): yield c
        if c.tag == 'furnitureGroup': yield from leaves(c)
moved = 0
for e in leaves(root):
    nm = e.get('name', '')
    if e.tag == 'doorOrWindow' and not nm.startswith('Shower glass'): continue   # openings are set explicitly
    x, y, n = remap(fx(e, 'x'), fx(e, 'y'))
    if n: setf(e, x=float(x), y=float(y)); moved += 1
print('furniture moved with rooms:', moved)

# ---------- 2. walls ----------
W = {w.get('id'): w for w in root.iter('wall')}
def wall(i, xs, ys, xe, ye, t=None):
    w = W['wall-s15-%d' % i]; setf(w, xStart=float(xs), yStart=float(ys), xEnd=float(xe), yEnd=float(ye))
    if t: setf(w, thickness=float(t))
    return w
xw7, x5, x3 = XW - 10.0, PARTY - 12.355, EAST_I + 15.295       # centre lines of west, party and east exterior walls
y6, y4 = HALL_S + 13.53, YS + 15.295
wall(0, xw7 - 10, 290.59, 1496.47, 290.59)
wall(2, EAST_I, 790.59, 1496.47, 790.59)
wall(3, x3, 774.12, x3, y4 + 15.295)
wall(4, x5 - 12.355, y4, x3 + 15.295, y4)
wall(5, x5, HALL_S, x5, y4 + 15.295)
wall(6, xw7 - 10, y6, PARTY, y6)
wall(7, xw7, 275.29, xw7, y6 + 13.53)
wall(8, 227.93, YN, 227.93, HALL_N, 10)
wall(9, XW, 599.83, ENS_E, 599.83, 10)
wall(10, ENS_E, 654.74, LIV_W, 654.74, 9.94)
wall(11, 608.41, YN, 608.41, HALL_N, 10.02)
wall(12, PARTY, 771.99, COR_W, 771.99, 12.52)
wall(14, PARTY, 1005.9, 429.87, 1005.9, 10)
wall(15, 429.87, 1065.68, 542.0, 1065.68, 10.05)
wall(17, COR_E, 778.87, EAST_I, 778.87, 10.06)
wall(18, 542.0, 955.79, EAST_I, 955.79, 12.53)
# corridor east wall: starts 22 north of the laundry corner = south stub of the hallway->living passage
PASS_N0, PASS_N1, PASS_S0 = HALL_N, HALL_N + 10.0, LIV_S - 22.0     # N stub 10, opening 82.1, S stub 22
wall(16, 542.0, PASS_S0, 542.0, YS, 10.05)
# bathroom east wall, interrupted by the corridor niche (60 wide x 33 deep, as built: IMG_2017, IMG_1961)
NI_N, NI_S, NI_BACK = BATH_S - 60.0, BATH_S, COR_W - 33.0
wall(13, 429.87, HALL_S, 429.87, NI_N - 2.5, 9.94)
def new_wall(name, xs, ys, xe, ye, t):
    w = copy.deepcopy(W['wall-s15-15']); w.set('id', 'wall-s15-' + name)
    for k in ('wallAtStart', 'wallAtEnd'):
        if k in w.attrib: del w.attrib[k]
    setf(w, xStart=float(xs), yStart=float(ys), xEnd=float(xe), yEnd=float(ye), thickness=float(t))
    p = parent_of(W['wall-s15-18']); p.insert(list(p).index(W['wall-s15-18']) + 1, w); return w
new_wall('13b', 429.87, 1005.9, 429.87, 1065.68, 9.94)
new_wall('niche-back', NI_BACK - 2.5, NI_N - 5, NI_BACK - 2.5, 1005.9, 5)
new_wall('niche-north', NI_BACK - 5, NI_N - 2.5, COR_W, NI_N - 2.5, 5)
new_wall('passage-north-stub', 542.0, PASS_N0, 542.0, PASS_N1, 10.05)
for w in root.iter('wall'):
    for k in ('wallAtStart', 'wallAtEnd'):
        if k in w.attrib: del w.attrib[k]

# ---------- 3. rooms ----------
def room(name, pts):
    r = [r for r in root.iter('room') if r.get('name') == name][0]
    for p in r.findall('point'): r.remove(p)
    for x, y in pts:
        ET.SubElement(r, 'point', x=F(float(x)), y=F(float(y)))
room('Kuhinja i dnevni boravak', [(LIV_W, YN), (XE, YN), (XE, LIV_S), (LIV_W, LIV_S)])
room('Hodnik', [(XW, NICHE_N), (ENS_E, NICHE_N), (ENS_E, HALL_N), (LIV_W, HALL_N), (LIV_W, LIV_S), (COR_E, LIV_S),
                (COR_E, R5D_N), (COR_W, R5D_N), (COR_W, NI_S), (NI_BACK, NI_S), (NI_BACK, NI_N), (COR_W, NI_N),
                (COR_W, HALL_S), (XW, HALL_S)])
room('Kupaonica 2', [(XW, YN), (ENS_E, YN), (ENS_E, ENS_S), (XW, ENS_S)])
room('Spavaća soba 1', [(BED_W, YN), (BED_E, YN), (BED_E, BED_S), (BED_W, BED_S)])
room('Kupaonica', [(PARTY, BATH_N), (BATH_E, BATH_N), (BATH_E, NI_N - 5), (NI_BACK - 5, NI_N - 5), (NI_BACK - 5, BATH_S), (PARTY, BATH_S)])
room('Spavaća soba 2', [(PARTY, R5_N), (BATH_E, R5_N), (BATH_E, R5D_S), (COR_E, R5D_S), (COR_E, YS), (PARTY, YS)])
room('Spavaća soba 3', [(SARA_W, SARA_N), (EAST_I, SARA_N), (EAST_I, YS), (SARA_W, YS)])
room('Praonica', [(SARA_W, LAU_N), (EAST_I, LAU_N), (EAST_I, LAU_S), (SARA_W, LAU_S)])
TER_W, TER_E, FAC_E, FAC_S = 653.6, 1402.1, x3 + 15.295, y4 + 15.295
room('Terasa 9', [(FAC_E, 807.06), (TER_E, 807.06), (TER_E, 1572.94), (TER_W, 1572.94), (TER_W, FAC_S), (FAC_E, FAC_S)])
BAL_W = 20.7
room('Terasa 10', [(BAL_W, 29.41), (782.35, 29.41), (782.35, 275.29), (BAL_W, 275.29)])

# ---------- 4. openings ----------
n_inplan = 0
for e in root.iter():
    for k in ('widthInPlan', 'depthInPlan', 'heightInPlan'):
        if k in e.attrib: del e.attrib[k]; n_inplan += 1   # stale: made SH3D cut a 132x210 hole for the 300x240 door
print('stale *InPlan attributes removed:', n_inplan)
D = {(round(fx(e, 'x')), round(fx(e, 'y'))): e for e in root.iter('doorOrWindow')}
def door(key, name, **kw):
    e = D[key]; e.set('name', name); setf(e, **kw); return e
door((26, 715), 'Front door 105×215', x=xw7, y=(HALL_N + HALL_S) / 2 - 0.2, width=105.0, height=215.0)
door((223, 421), 'Door frame – ensuite 80×210', x=227.93, y=YN + 74 + 40, width=80.0, height=210.0, depth=10.0)
door((338, 656), 'Door frame – bedroom 80×210', x=BED_W + 69 + 40, y=654.74, width=80.0, height=210.0, depth=9.94)
door((325, 773), 'Door frame – bathroom 70×210 (north wall, from hallway)', x=PARTY + 70 + 35, y=771.99, width=70.0, height=210.0, depth=12.52)
door((482, 1071), 'Door frame – room 5 80×210', x=COR_W + 10 + 40, y=1065.68, width=80.0, height=210.0, depth=10.05)
door((538, 912), 'Door frame – laundry 70×210', x=542.0, y=LAU_N + 46 + 43 + 35, width=70.0, height=210.0, depth=10.05)
door((538, 1009), 'Door frame – Sara 80×210', x=542.0, y=SARA_N + 8 + 40 - 0.3, width=80.0, height=210.0, depth=10.05)
door((371, 1368), 'Window 160×170, sill 90', x=PARTY + 73 + 80, y=y4)
door((728, 1368), 'Terrace door Sara south 160×250, sill 10 (double, opens inward)', x=SARA_W + 107 + 80, y=y4)
door((834, 907), 'Terrace door – laundry 80×240, threshold 20', x=x3)
door((834, 1065), 'Terrace door – Sara east 80×240, threshold 20', x=x3)
door((1146, 791), 'Terrace lift-and-slide door 300×240, threshold 20 (two panels; east edge 169 from east wall, IMG_2011/2012)')

# ---------- 5. boxes, passage, niche ----------
BOX = copy.deepcopy(one('Laundry basket')); ANCHOR = one('Kitchen corner base')
def box(name, x, y, w, d, h, el=0.0, color=WALL):
    b = copy.deepcopy(BOX); b.set('id', nid('pieceOfFurniture')); b.set('name', name)
    setf(b, x=float(x), y=float(y), width=float(w), depth=float(d), height=float(h), color=color)
    if el: setf(b, elevation=float(el))
    elif 'elevation' in b.attrib: del b.attrib['elevation']
    p = parent_of(ANCHOR); p.insert(list(p).index(ANCHOR) + 1, b); return b
remove(one('Header above hallway'))
box('Header above hallway → living passage (no door), opening 82×210', 542.0, (PASS_N1 + PASS_S0) / 2, 10.05, PASS_S0 - PASS_N1, 70, el=210)
remove(one('Pipe box 28×65'))                      # now built from walls (corridor niche)
box('Pipe box – living room SE corner 14×20 (IMG_2011)', XE - 7, LIV_S - 10, 14, 20, H)
box('Shaft box – laundry NW corner 22×46 (plan)', SARA_W + 11, LAU_N + 23, 22, 46, H)
box('Shaft box – wardrobe niche NW corner 29×28 (plan)', XW + 14.5, NICHE_N + 14, 29, 28, H)
bw = one('Built-in wardrobe'); bw.set('name', 'Built-in wardrobe 152×56×278 (made to measure, niche, beside the shaft)')
setf(bw, x=(XW + 29 + ENS_E) / 2 - 0.5, width=ENS_E - XW - 30.0, y=NICHE_N + 28.0)
setf(one('Heat pump indoor unit'), x=SARA_W + 22 + 30.5)
setf(one('Laundry basket'), x=690.0, y=LAU_S - 20.5)
sh = one('Installation shaft (ventilation)'); setf(sh, x=BED_W + 69 + 80 + 42 + 33.0, y=BED_S - 10.0)
for p in by_name('Photo frame 40×50'):
    if NI_N - 25 < fx(p, 'y') < NI_S + 5: setf(p, y=NI_N - 60.0)       # was on the wall that is now the niche
    elif NI_S <= fx(p, 'y') < R5D_N: setf(p, y=(BATH_S + 5 + R5D_N) / 2)  # centred on the 60 cm wall south of the niche

# ---------- 6. tiles and accent walls on the new wall faces ----------
for e in by_name('Wall tiles'): remove(e)
def tile(x, y, w, d): box('Wall tiles – beige stone-look, floor to ceiling (installed)', x, y, w, d, H - 1, color=TILE)
def tiles_h(x0, x1, y, side): tile((x0 + x1) / 2, y + side * 0.3, x1 - x0, 0.6)     # side +1: tile south of line y
def tiles_v(x, y0, y1, side): tile(x + side * 0.3, (y0 + y1) / 2, 0.6, y1 - y0)
ed = YN + 74                                             # ensuite door 74..154 from the north wall
tiles_h(XW, ENS_E, YN, 1); tiles_h(XW, ENS_E, ENS_S, -1); tiles_v(XW, YN, ENS_S, 1)
tiles_v(ENS_E, YN, ed, -1); tiles_v(ENS_E, ed + 80, ENS_S, -1)
bd = PARTY + 70                                          # bathroom door 70..140 from the party wall
tiles_h(PARTY, bd, BATH_N, 1); tiles_h(bd + 70, BATH_E, BATH_N, 1); tiles_h(PARTY, NI_BACK - 5, BATH_S, -1)
tiles_v(PARTY, BATH_N, BATH_S, 1); tiles_v(BATH_E, BATH_N, NI_N - 5, -1)
tiles_v(NI_BACK - 5, NI_N - 5, BATH_S, -1); tiles_h(NI_BACK - 5, BATH_E, NI_N - 5, -1)
def accent(prefix, **kw): setf(one(prefix), **kw)
accent('Accent wall – bed wall', x=BED_E - 0.3, y=(YN + BED_S) / 2, depth=BED_S - YN)
accent('Accent wall – room 5 sofa wall', x=PARTY + 0.3, y=(R5_N + YS) / 2, depth=YS - R5_N)
a = one('Accent wall – Sara bed wall'); setf(a, x=SARA_W + 0.3, depth=fx(a, 'depth') * (YS - SARA_N) / 394.12)

# ---------- 7. terrace and balcony edges ----------
setf(one('Terrace upstand, 60 above tiles – west'), x=TER_W - 11, y=(FAC_S + 1595) / 2, depth=1595 - FAC_S)
setf(one('Terrace upstand, 60 above tiles – south'), x=(TER_W - 22 + TER_E + 22) / 2, width=TER_E - TER_W + 44)
setf(one('Terrace upstand, 60 above tiles – east'), x=TER_E + 11)
for g in by_name('Glass balustrade panel'):
    if abs(fx(g, 'x') - 1432) < 1: setf(g, x=TER_E + 23.0)
    elif abs(fx(g, 'x') - 622) < 1: setf(g, x=TER_W - 23.0)
    elif abs(fx(g, 'y') - 1596) < 1: setf(g, x=TER_W - 22 + (fx(g, 'x') - 642) * (TER_E - TER_W + 44) / 766.0, width=fx(g, 'width') * (TER_E - TER_W + 44) / 766.0)
for e in root.iter('pieceOfFurniture'):
    nm = e.get('name', '')
    if nm.startswith('Floor option') and nm.endswith('– terrace'): setf(e, x=(FAC_E + TER_E) / 2, width=TER_E - FAC_E, y=(807.06 + FAC_S) / 2, depth=FAC_S - 807.06)
    if nm.startswith('Floor option') and nm.endswith('– terrace strip'): setf(e, x=(TER_W + TER_E) / 2, width=TER_E - TER_W, y=(FAC_S + 1573) / 2, depth=1573 - FAC_S)
    if nm.startswith('Floor option') and nm.endswith('– balcony'): setf(e, x=(BAL_W + 782) / 2, width=782 - BAL_W)
for p in by_name('Balcony parapet'):
    if abs(fx(p, 'x') - 7.5) < 1: setf(p, x=BAL_W - 7.5)
    elif abs(fx(p, 'y') - 21.5) < 1: setf(p, x=(BAL_W - 15 + 797) / 2, width=797 - BAL_W + 15)
for e in by_name('Outdoor wall light (installed) – east facade'): setf(e, x=FAC_E + 6.0)

# ---------- 8. lights ----------
SRC_L = copy.deepcopy(by_name('White light source down', 'light')[0])
def source(name, x, y, el, power, color='00FFE9C8'):
    l = copy.deepcopy(SRC_L); l.set('id', nid('light')); l.set('name', name)
    setf(l, x=float(x), y=float(y), elevation=float(el), power=float(power)); l.set('angle', '0')
    l.find('lightSource').set('color', color)
    p = parent_of(ANCHOR); p.insert(list(p).index(ANCHOR) + 1, l); return l
def ceiling_lamp(room, x, y, power=0.25, note='as built, from photos ±20'):
    box(f'Ceiling lamp Ø30 – {room} ({note})', x, y, 30, 30, 6, el=H - 6, color=WHITE)
    source(f'Light: ceiling lamp – {room}', x, y, H - 11, power)
def spot(room, x, y, power=0.1):
    box(f'Recessed spot – {room} (as built, from photos ±20)', x, y, 9, 9, 1, el=H - 1, color=WHITE)
    source(f'Light: spot – {room}', x, y, H - 5, power)
ceiling_lamp('kitchen', 734, 488); ceiling_lamp('living', 1297, 536)
ceiling_lamp('living, by the terrace door', 950, 735, 0.18)
ceiling_lamp('bedroom', 418, 478); ceiling_lamp('room 5', 382, 1211)
ceiling_lamp('Sara', 683, 1156); ceiling_lamp('Sara, by the east door', 790, 1150, 0.15)
ceiling_lamp('ensuite, IP44', 132, 453, 0.08, 'electrical plan'); ceiling_lamp('bathroom, IP44', 326, 889, 0.07, 'electrical plan')
for x in (90, 195, 300, 405, 510): spot('hall', x, 712.7)
for y in (870, 990): spot('corridor', 486, y)
for x in (615, 685, 755):
    for y in (835, 900): spot('laundry', x, y, 0.05)
for p in by_name('Pendant lamp'):                           # dining point feeds the two pendants over the table
    source('Light: dining pendant', fx(p, 'x'), fx(p, 'y'), fx(p, 'elevation') + 3, 0.18)
box('Mirror light 60 – ensuite (outlet at 200, electrical plan)', 131.9, YN + 3.3, 60, 5, 4, el=198, color=WHITE)
source('Light: mirror – ensuite', 131.9, YN + 12, 194, 0.03)
wb = [e for e in by_name('Washbasin') if PARTY < fx(e, 'x') < BATH_E][0]
box('Mirror light 50 – bathroom, above the basin on the east wall (outlet at 200)', BATH_E - 3.3, fx(wb, 'y'), 5, 50, 4, el=198, color=WHITE)
source('Light: mirror – bathroom', BATH_E - 12, fx(wb, 'y'), 194, 0.03)
for e in by_name('Outdoor wall light (installed)'):
    ang = fx(e, 'angle'); x, y = fx(e, 'x'), fx(e, 'y')
    if abs(ang) < 0.1: source('Light: terrace wall lamp – living facade', x, y + 14, 262, 0.2)
    else: source('Light: terrace wall lamp – east facade', x + 14, y, 262, 0.2)

root.set('name', 'S15-Hrneticka-v13.sh3d')
tree.write(DST, encoding='UTF-8', xml_declaration=True)
print('walls', len(list(root.iter('wall'))), 'lights', len(list(root.iter('light'))))
