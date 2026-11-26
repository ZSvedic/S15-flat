#!/usr/bin/env python3
"""Home.xml -> lights.json for Blender: position, direction, light group ("set") and lamp role of every light source.
Lamp data (lumens, beam, colour) is NOT here: it is in groups.json.  Usage: make_lights.py Home.xml lights.json
Name rules (prefix -> set, role):  a name ending in "-> x,y,z" is aimed at that model point; "up" shines up; everything else down.
Bars and strips: each SH3D source stands for 20 cm of LED strip and becomes 4 sources 5 cm apart along the named axis."""
import sys, json, math, re, xml.etree.ElementTree as ET
RULES = [  # prefix, set, role
    ('AmbA up', 'wall', 'gu10'), ('AmbA down', 'wall', 'gu10'), ('White light source', 'wall', 'shield'),
    ('ArtE bar', 'artE', 'piclight'), ('ArtH bar', 'artH', 'piclight'), ('ArtS aim', 'artS', 'gu10'), ('ArtS bar', 'artS', 'piclight'), ('Desk aim', 'desk', 'gu10'),
    ('TV puck', 'tv', 'puck'), ('Kitchen bar', 'kitchen', 'bar'), ('Niche bar', 'niche', 'profile'), ('HallBench bar', 'hallbench', 'bar'),
    ('Pendant bar', 'pendant', 'pbar'), ('Low bar', 'low', 'lowbar'), ('Low lamp', 'low', 'tablelamp'),
    ('Light: spot – hall', 'hallspots', 'spot'), ('Light: spot – corridor', 'corrspots', 'spot'), ('Light: spot', 'ceiling', 'spot'),
    ('Light: ceiling lamp', 'ceiling', 'ceiling'),
    ('Light: mirror', 'other', 'mirror'), ('Light: terrace', 'other', 'terrace'), ('Desk lamp', 'other', 'desk')]
out = []
for l in ET.parse(sys.argv[1]).getroot().iter('light'):
    a = l.attrib; name = a.get('name', '')
    hit = next(((s, r) for p, s, r in RULES if name.startswith(p)), None)
    if hit is None: print('unclassified light:', name); continue
    st, role = hit
    if role == 'ceiling' and 'IP44' in name: role = 'bath'
    x, y, el = float(a['x']), float(a['y']), float(a.get('elevation', 0))
    w, d, h, ang = float(a['width']), float(a['depth']), float(a['height']), float(a.get('angle', 0))
    aim = re.search(r'-> *([-\d.]+),([-\d.]+),([-\d.]+)$', name)
    words = name.split(':')[0].split()
    for s in l.findall('lightSource'):
        dx, dy = (float(s.get('x')) - 0.5) * w, (float(s.get('y')) - 0.5) * d
        px, py, pz = x + dx * math.cos(ang) - dy * math.sin(ang), y + dx * math.sin(ang) + dy * math.cos(ang), el + float(s.get('z')) * h
        up = 'up' in words or name.endswith(' up')
        if name.startswith('White light source'): pz += 6 if up else -7       # move out of the fixture body
        if aim:
            t = [float(v) for v in aim.groups()]; v = [t[0] - px, t[1] - py, t[2] - pz]; n = math.sqrt(sum(c * c for c in v)); dr = [c / n for c in v]
        else: dr = [0, 0, 1 if up else -1]
        pts = [(px, py, pz)]
        if words[-1] in ('x', 'y', 'z') and words[-2] == 'bar':
            ax = 'xyz'.index(words[-1]); pts = []
            for o in (-7.5, -2.5, 2.5, 7.5):
                p = [px, py, pz]; p[ax] += o; pts.append(tuple(p))
        for p in pts: out.append(dict(name=name, set=st, role=role, x=round(p[0], 1), y=round(p[1], 1), z=round(p[2], 1), dir=[round(c, 4) for c in dr]))
json.dump(out, open(sys.argv[2], 'w'), indent=0, ensure_ascii=False)
from collections import Counter; print(len(out), 'lights', dict(Counter((o['set'], o['role']) for o in out)))
