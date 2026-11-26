#!/usr/bin/env python3
"""Vector plan (SVG + PNG) of a Sweet Home 3D Home.xml: walls, openings with swings, rooms, furniture."""
import math, sys
import xml.etree.ElementTree as ET
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Arc
from matplotlib import patheffects

SRC, OUT, TITLE = sys.argv[1], sys.argv[2], sys.argv[3]
root = ET.parse(SRC).getroot()

def f(e, k, d=0.0):
    v = e.get(k)
    return float(v) if v is not None else d

def rot(px, py, a):
    c, s = math.cos(a), math.sin(a)
    return px * c - py * s, px * s + py * c

def rect(x, y, w, d, a):
    return [(x + u, y + v) for u, v in (rot(px, py, a) for px, py in
            ((-w / 2, -d / 2), (w / 2, -d / 2), (w / 2, d / 2), (-w / 2, d / 2)))]

fig, ax = plt.subplots(figsize=(16, 17.5))
ax.set_aspect('equal'); ax.invert_yaxis(); ax.axis('off')

FLOOR = {'Pozga-Lakirano-Arctic': '#E9DCC6'}
def room_color(rm):
    t = [c for c in rm if c.tag == 'texture' and c.get('attribute') == 'floorTexture']
    if t:
        return FLOOR.get(t[0].get('name'), '#D9D9D6')
    fc = rm.get('floorColor')
    return '#' + fc[-6:] if fc else '#EEEEEE'

for rm in root.iter('room'):
    pts = [(f(p, 'x'), f(p, 'y')) for p in rm.iter('point')]
    terrace = rm.get('name', '').startswith('Terasa')
    ax.add_patch(Polygon(pts, closed=True, fc='#EDEDEA' if terrace else room_color(rm), ec='none', zorder=0))
    area = abs(sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]))) / 2 / 1e4
    cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
    ax.text(cx, cy, f"{rm.get('name')}\n{area:.2f} m²".replace('.', ','), ha='center', va='center',
            fontsize=8.5, color='#555', zorder=6, style='italic',
            path_effects=[patheffects.withStroke(linewidth=3, foreground='white')])

walls = list(root.iter('wall'))
for w in walls:
    x1, y1, x2, y2, t = f(w, 'xStart'), f(w, 'yStart'), f(w, 'xEnd'), f(w, 'yEnd'), f(w, 'thickness')
    L = math.hypot(x2 - x1, y2 - y1); a = math.atan2(y2 - y1, x2 - x1)
    ax.add_patch(Polygon(rect((x1 + x2) / 2, (y1 + y2) / 2, L + (t if t > 20 else 0), t, a), closed=True,
                         fc='#3A3A3A' if t > 20 else '#6E6E6E', ec='#222', lw=0.4, zorder=3))

def in_wall(x, y):
    for w in walls:
        x1, y1, x2, y2, t = f(w, 'xStart'), f(w, 'yStart'), f(w, 'xEnd'), f(w, 'yEnd'), f(w, 'thickness')
        L = math.hypot(x2 - x1, y2 - y1)
        u = ((x - x1) * (x2 - x1) + (y - y1) * (y2 - y1)) / L
        dist = abs((x - x1) * (y2 - y1) - (y - y1) * (x2 - x1)) / L
        if -5 <= u <= L + 5 and dist <= t / 2 + 2:
            return True
    return False

def visible(e):
    return e.get('visible', 'true') != 'false'

for dw in root.iter('doorOrWindow'):
    x, y, w, d, a = f(dw, 'x'), f(dw, 'y'), f(dw, 'width'), f(dw, 'depth'), f(dw, 'angle')
    name = dw.get('name', '')
    if not in_wall(x, y):
        if 'balustrade' in name.lower() or 'glass' in name.lower():
            ax.add_patch(Polygon(rect(x, y, w, max(d, 2), a), closed=True, fc='#9CC9E0', ec='#5A9BBF', lw=0.6, zorder=4))
        continue
    ax.add_patch(Polygon(rect(x, y, w, d + 0.5, a), closed=True, fc='white', ec='none', zorder=4))
    sashes = [s for s in dw if s.tag == 'sash']
    is_frame = name.startswith('Door frame')
    el, h = f(dw, 'elevation'), f(dw, 'height')
    if is_frame:
        for sx in (-w / 2, w / 2):
            p = [(x + u, y + v) for u, v in (rot(sx, -d / 2, a), rot(sx, d / 2, a))]
            ax.plot(*zip(*p), color='#222', lw=0.8, zorder=5)
    else:
        for off in (-0.12, 0.12):
            p = [(x + u, y + v) for u, v in (rot(-w / 2, off * d, a), rot(w / 2, off * d, a))]
            ax.plot(*zip(*p), color='#2C6E9B', lw=0.9, zorder=5)
        p = [(x + u, y + v) for u, v in (rot(-w / 2, -d / 2, a), rot(w / 2, -d / 2, a), rot(w / 2, d / 2, a), rot(-w / 2, d / 2, a), rot(-w / 2, -d / 2, a))]
        ax.plot(*zip(*p), color='#222', lw=0.5, zorder=5)
    mirrored = dw.get('modelMirrored') == 'true'
    sg = -1 if mirrored else 1
    for s in (sashes if h >= 200 else []):
        hx = sg * f(s, 'xAxis') * w - sg * w / 2
        hy = f(s, 'yAxis') * d - d / 2
        r = f(s, 'width') * w
        st = math.degrees(f(s, 'startAngle'))
        if mirrored:
            st = 180 - st
        ext = sg * math.degrees(f(s, 'endAngle') - f(s, 'startAngle'))
        pts = []
        for k in range(31):
            t = math.radians(st + ext * k / 30)
            u, v = rot(hx + r * math.cos(t), hy - r * math.sin(t), a)
            pts.append((x + u, y + v))
        hu, hv = rot(hx, hy, a)
        ax.plot(*zip(*pts), color='#8A5BB5', lw=0.7, ls='--', zorder=5)
        ax.plot([x + hu, pts[-1][0]], [y + hv, pts[-1][1]], color='#8A5BB5', lw=0.8, zorder=5)
    if not is_frame or True:
        lab = f"{w:.0f}/{h:.0f}" + (f" p{el:.0f}" if el else '')
        nx, ny = rot(0, d / 2 + 9, a)
        ax.text(x - nx, y - ny, lab, ha='center', va='center', fontsize=5.5, color='#1F5E8C', zorder=7,
                rotation=-math.degrees(a) if abs(math.cos(a)) > 0.5 else 90,
                path_effects=[patheffects.withStroke(linewidth=2, foreground='white')])

SKIP_PREFIX = ('Floor option', 'Accent wall', 'Wall tiles', 'Oak backsplash', 'Shade sail')
def label_of(n):
    for sep in (' (', ' – ', ' -'):
        if sep in n and not n.startswith('Installation'):
            n = n.split(sep)[0]
    return n

items = []
def collect(e, vis=True):
    vis = vis and visible(e)
    if e.tag == 'furnitureGroup':
        if not vis:
            return
        for c in e:
            if c.tag in ('pieceOfFurniture', 'furnitureGroup', 'light'):
                collect(c, vis)
        return
    if vis:
        items.append(e)
for e in root:
    if e.tag in ('pieceOfFurniture', 'furnitureGroup', 'light'):
        collect(e)

items.sort(key=lambda e: (f(e, 'height') > 2, f(e, 'elevation')))
for e in items:
    n = e.get('name', '')
    if n.startswith(SKIP_PREFIX):
        continue
    x, y, w, d, a = f(e, 'x'), f(e, 'y'), f(e, 'width'), f(e, 'depth'), f(e, 'angle')
    if n.startswith('As built:'):                       # v17: switches, sockets etc. read from site photos -> small red dot
        ax.plot([x], [y], 'o', ms=2.2, mfc='#D0342C', mec='white', mew=0.3, zorder=8)
        continue
    if min(w, d) < 1.5 and max(w, d) > 50:
        continue
    if e.tag == 'light' and max(w, d) <= 3.1:          # bare light sources: the fixture piece is drawn instead
        continue
    if n.startswith(('Ceiling lamp', 'Recessed spot')) and f(e, 'elevation') >= 240:   # v19: ceiling fixture symbol, not a floor box
        r = max(w, d) / 2
        ax.add_patch(matplotlib.patches.Circle((x, y), r, fc='none', ec='#C98A12', lw=0.8, zorder=7.5))
        k = r * 0.7071
        ax.plot([x - k, x + k], [y - k, y + k], color='#C98A12', lw=0.6, zorder=7.5)
        ax.plot([x - k, x + k], [y + k, y - k], color='#C98A12', lw=0.6, zorder=7.5)
        continue
    if n.startswith('Beanbag'):                        # v19: round
        ax.add_patch(matplotlib.patches.Ellipse((x, y), w, d, fc='#FFFFFF', ec='#777', lw=0.5, alpha=0.9, zorder=4.5))
        ax.text(x, y, label_of(n), ha='center', va='center', fontsize=4.6, color='#333', zorder=6)
        continue
    shaft = n.startswith(('Installation shaft', 'WC installation', 'Terrace upstand', 'Balcony parapet'))
    rug = f(e, 'height') <= 1.5
    fc = '#8C8C8C' if shaft else ('#F3EEE4' if rug else '#FFFFFF')
    ax.add_patch(Polygon(rect(x, y, w, d, a), closed=True, fc=fc, ec='#777' if not shaft else '#444',
                         lw=0.5, alpha=0.55 if rug else 0.9, ls=':' if rug else '-', zorder=2 if rug else 4.5))
    nolabel = n.startswith(('Planter', 'Pendant', 'Flowers', 'Cushion', 'Kettle', 'Herb', 'Fruit', 'Oak chopping', 'Books', 'Vase', 'Trailing')) or (f(e, 'elevation') >= 100 and not n.startswith('Wall cabinet'))
    if ((w * d > 1500 and not rug and not shaft) or n.startswith('Installation shaft')) and not nolabel:
        lab = label_of(n).replace(' in planter', '')
        if len(lab) > 26:
            lab = lab[:25] + '…'
        rotlab = 90 if (d > w * 1.4) != (abs(math.sin(a)) > 0.7) else 0
        ax.text(x, y, lab, ha='center', va='center', fontsize=4.6, color='#333', rotation=rotlab, zorder=6)

ax.autoscale_view()
x0, x1 = ax.get_xlim(); y0, y1 = ax.get_ylim()
ax.set_xlim(x0 - 20, x1 + 20)
ax.set_title(TITLE, fontsize=12, loc='left')
# scale bar 2 m
sx, sy = 40, max(y0, y1) - 40
ax.plot([sx, sx + 200], [sy, sy], color='k', lw=2)
for k in range(0, 201, 100):
    ax.plot([sx + k, sx + k], [sy - 6, sy + 6], color='k', lw=1)
ax.text(sx + 100, sy - 14, '2 m', ha='center', fontsize=8)
ax.text(sx, sy + 26, 'Openings: width/height in cm, p = sill/threshold above floor. Grey = shafts, upstands, parapets. Red dots = as-built switches, sockets, thermostats, outlets. Amber ⊗ = ceiling lamps and spots.',
        fontsize=7, color='#444')
fig.tight_layout()
fig.savefig(OUT + '.svg')
fig.savefig(OUT + '.png', dpi=130)
print('ok')
