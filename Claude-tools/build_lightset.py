#!/usr/bin/env python3
"""Adds a list of light fixtures to a Home.xml (used for the lighting-expert branches, 2026-11-26).
Fixture lines, pipe-separated:  id | action | room | type | x | y | z | lumens | beam | kelvin | aim | group | reason
 action add (change = give an existing ceiling point named in 'reason' this lamp: the point's own light is removed and the
 new one is placed at the point). Types: WALL_UPDOWN, WALL_UP, WALL_DOWN, DOWNLIGHT, CEILING_DIFFUSE, PENDANT, STRIP, PICTURE,
 FLOOR_LAMP, TABLE_LAMP, SPOT. Lamp data goes into the light name ("XA:"/"XC:" + {lm= beam= k=}), read by make_lights.py.
Usage: build_lightset.py <in Home.xml> <fixtures.txt> <out Home.xml> <model name> <rooms json (groups.json)>"""
import copy, sys, uuid, json, math, re, xml.etree.ElementTree as ET
SRC, FX, DST, NAME, GJ = sys.argv[1:6]
tree = ET.parse(SRC); root = tree.getroot(); ROOMS = json.load(open(GJ))['rooms']
def nid(p): return f'{p}-{uuid.uuid4()}'
def F(v): return f'{v:.2f}'.rstrip('0').rstrip('.')
BOX = copy.deepcopy(next(e for e in root.iter('pieceOfFurniture') if e.get('model') == '20/texturableBox.obj'))
for k in ('angle', 'color', 'visible'): BOX.attrib.pop(k, None)
for c in list(BOX): BOX.remove(c)
SRCL = copy.deepcopy(next(e for e in root.iter('light') if e.get('name', '').startswith('Light: ')))
G = ET.SubElement(root, 'furnitureGroup', id=nid('furnitureGroup'), name=f'LIGHTSET – {NAME}', x='0', y='0', width='1', depth='1', height='1')
# furnitureGroup must come before other top-level elements of the same kind order? SH3D accepts groups anywhere among furniture
furn = [i for i, e in enumerate(list(root)) if e.tag in ('pieceOfFurniture', 'furnitureGroup', 'light', 'doorOrWindow')]
root.remove(G); root.insert(furn[-1] + 1 if furn else len(root), G)
def box(name, x, y, w, d, h, el, color='FF2B2B2B'):
    b = copy.deepcopy(BOX); b.set('id', nid('pieceOfFurniture')); b.set('name', name)
    for k, v in dict(x=x, y=y, width=w, depth=d, height=h, elevation=el).items(): b.set(k, F(v))
    b.set('color', color); G.append(b)
def src(name, x, y, z, aim=None):
    l = copy.deepcopy(SRCL); l.set('id', nid('light')); l.set('name', name + (' -> %s,%s,%s' % tuple(F(a) for a in aim) if aim else ''))
    for k, v in dict(x=x, y=y, elevation=z, power=0.1).items(): l.set(k, F(v))
    for k in ('width', 'depth', 'height'): l.set(k, '3')
    G.append(l)
def shade(label, x, y, el, h=22, w=30, color='FFEDE6D6'):
    """Open lampshade: four thin sides, open at top and bottom (a solid box would swallow the light)."""
    for dx, dy, ww, dd in ((0, -w / 2, w, 1), (0, w / 2, w, 1), (-w / 2, 0, 1, w), (w / 2, 0, 1, w)):
        box(label, x + dx, y + dy, ww, dd, h, el, color)
def wall_normal(x, y):
    """Into-room direction of the nearest room face to (x, y)."""
    best = None
    for n, (x0, y0, x1, y1) in ROOMS.items():
        for d, nrm, inside in ((abs(x - x0), (1, 0), y0 - 5 <= y <= y1 + 5), (abs(x - x1), (-1, 0), y0 - 5 <= y <= y1 + 5),
                               (abs(y - y0), (0, 1), x0 - 5 <= x <= x1 + 5), (abs(y - y1), (0, -1), x0 - 5 <= x <= x1 + 5)):
            if inside and (best is None or d < best[0]): best = (d, nrm)
    return best[1] if best and best[0] < 30 else (0, 1)
def fnum(s, d=None):
    s = (s or '').strip().replace('lm/m', '').replace('lm', '').replace('°', '').replace('K', '')
    try: return float(s)
    except ValueError: return d
rows = []
for line in open(FX):
    t = [c.strip() for c in line.strip().strip('|').split('|')]
    if len(t) < 12 or not t[1].lower() in ('add', 'change'): continue
    rows.append(t)
n = 0
for t in rows:
    fid, act, room, typ, x, y, z, lm, beam, k, aim, grp = t[:12]; why = t[12] if len(t) > 12 else ''
    typ = typ.upper(); x, y = fnum(x), fnum(y); z = fnum(z, 175); lm = fnum(lm, 300); bm = fnum(beam); kel = fnum(k, 2700)
    P = 'XA:' if grp.lower().startswith('amb') else 'XC:'
    tag = f'{fid} {room} {typ}'
    def data(lumens, b=bm, r=2): return '{lm=%s%s k=%s r=%s}' % (F(lumens), (' beam=%s' % F(b)) if b else '', F(kel), F(r))
    label = f'{NAME} {fid} – {room}, {typ}, {why}'[:150]
    if act.lower() == 'change':                           # existing ceiling point: drop its light, keep its position
        m = re.search(r'(ceiling lamp|spot)[^,;]*', why, re.I)
        key = 'Light: ' + why.split(';')[0].strip(); L = [e for e in root.iter('light') if e.get('name', '').startswith('Light: ')]
        cands = [e for e in L if e.get('name') == key] or [e for e in L if e.get('name', '').startswith(key)][:1] or \
                [e for e in L if abs(float(e.get('x')) - x) < 40 and abs(float(e.get('y')) - y) < 40]
        if not cands: print('change: no existing point found for', fid, why)
        for e in cands:
            for p in root.iter():
                if e in list(p): p.remove(e); break
    if typ in ('WALL_UPDOWN', 'WALL_UP', 'WALL_DOWN'):
        nx, ny = wall_normal(x, y); cx, cy = x + nx * 6.5, y + ny * 6.5
        box(label + ' (fixture)', cx, cy, 7, 7, 16, z - 8)
        if typ != 'WALL_DOWN': src(f'{P} {tag} up {data(lm, bm or 36)}', cx, cy, z + 10, (cx, cy, z + 200))
        a3 = [fnum(v) for v in re.findall(r'[-\d.]+', aim)[:3]]
        if typ != 'WALL_UP': src(f'{P} {tag} down {data(lm, bm or 36)}', cx, cy, z - 13, a3 if len(a3) == 3 else (cx, cy, 0))
    elif typ == 'DOWNLIGHT':
        box(label + ' (fixture)', x, y, 8, 8, 1, 279, 'FFF2F2EE'); src(f'{P} {tag} {data(lm, bm or 40)}', x, y, 275, (x, y, 0))
    elif typ == 'CEILING_DIFFUSE':
        box(label + ' (fixture)', x, y, 30, 30, 6, 274, 'FFF7F6F2'); src(f'{P} {tag} {data(lm, None, 12)}', x, y, 269)
    elif typ == 'PENDANT':
        shade(label + ' (shade)', x, y, z, 22, 35, 'FF2B2B2B'); box(label + ' (cord)', x, y, 1, 1, 280 - z - 22, z + 22)
        src(f'{P} {tag} {data(lm, bm, 8)}', x, y, z + 8, (x, y, 0) if bm else None)
    elif typ in ('FLOOR_LAMP', 'TABLE_LAMP'):
        base = 0 if typ == 'FLOOR_LAMP' else max(z - 45, 0)
        box(label + ' (stem)', x, y, 3, 3, z - base - 15, base); shade(label + ' (shade)', x, y, z - 10)
        src(f'{P} {tag} {data(lm, None, 8)}', x, y, z)
    elif typ == 'SPOT':
        a = [fnum(v) for v in re.findall(r'[-\d.]+', aim)[:3]]
        box(label + ' (fixture)', x, y, 7, 7, 10, z); src(f'{P} {tag} {data(lm, bm or 36)}', x, y, z - 2, a if len(a) == 3 else (x, y, 0))
    elif typ in ('STRIP', 'PICTURE'):
        nums = [fnum(v) for v in re.findall(r'[-\d.]+', aim)]
        if typ == 'PICTURE':
            w = nums[0] if nums else 60; nx, ny = wall_normal(x - 0, y); wx, wy = x - nx * 18, y - ny * 18    # wall face behind
            ax, ay = -ny, nx; pts = [(x + ax * (o - w / 2), y + ay * (o - w / 2)) for o in [i * 10 + 5 for i in range(int(w // 10))]]
            box(label + ' (tube)', x, y, w if ax else 3, 3 if ax else w, 3, z - 1.5, 'FFB8975A'); box(label + ' (arm)', (x + wx) / 2, (y + wy) / 2, 18 if nx else 2, 2 if nx else 18, 2, z - 1)
            for i, (px, py) in enumerate(pts): src(f'{P} {tag} {i + 1:02d} {data(lm * 0.1, bm or 110, 1)}', px, py, z - 3, (px - nx * 18, py - ny * 18, z - 45))
        else:
            x2, y2 = (nums[0], nums[1]) if len(nums) >= 2 else (x + 100, y)
            L = math.hypot(x2 - x, y2 - y); m = max(int(L // 10), 1); dirw = aim.lower()
            box(label + ' (profile)', (x + x2) / 2, (y + y2) / 2, max(abs(x2 - x), 2), max(abs(y2 - y), 2), 2, z - 1, 'FFF2F2EE')
            nx, ny = wall_normal((x + x2) / 2, (y + y2) / 2)
            for i in range(m):
                f = (i + 0.5) / m; px, py = x + (x2 - x) * f, y + (y2 - y) * f
                tgt = (px, py, z + 100) if 'up' in dirw else (px - nx * 50, py - ny * 50, z) if 'wall' in dirw else (px, py, 0)
                oz = 2.5 if 'up' in dirw else 0 if 'wall' in dirw else -2.5          # just outside the 2 cm profile
                ox, oy = (-nx * 2.5, -ny * 2.5) if 'wall' in dirw else (0, 0)
                src(f'{P} {tag} {i + 1:02d} {data(lm * L / 100 / m, bm or 120, 1)}', px + ox, py + oy, z + oz, tgt)
    else:
        print('unknown type, skipped:', t); continue
    n += 1
root.set('name', NAME + '.sh3d')
tree.write(DST, encoding='UTF-8', xml_declaration=True)
print('fixtures added:', n, 'lights now:', len(list(root.iter('light'))))
