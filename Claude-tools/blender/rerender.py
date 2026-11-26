#!/usr/bin/env python3
"""Incremental renders: finds which views a model change makes stale and hard-links every render that is still valid from the
previous version to the new version's name, so s15_blender.py (which skips existing files) renders only the stale ones.
A view is stale when an item (piece, light, door or window) changed, appeared or vanished in a room the view sees (groups.json
'views' -> 'rooms'; 'rooms' holds the room boxes), when its camera line changed, or when it is new. The top view (lux map) is
stale after any change. Walls, rooms, lamp data, groups or day settings changed -> everything is stale.
Limit: light that leaks through an open door into a room no stale view lists is not updated; use --full before a final version.
Usage: rerender.py <prev.sh3d> <new.sh3d> <prev tag> <new tag> <render out dir> [--full] [--dry]
Writes <out>/state-<new tag>.json (cameras and lamp-data hash), which the next run compares against."""
import sys, os, json, zipfile, hashlib, xml.etree.ElementTree as ET
HERE = os.path.dirname(os.path.abspath(__file__))
a = [x for x in sys.argv[1:] if not x.startswith('--')]; FULL = '--full' in sys.argv; DRY = '--dry' in sys.argv
PREV, NEW, PT, NT, OUT = a
cfg = json.load(open(os.path.join(HERE, 'groups.json'))); GID = [g['id'] for g in cfg['groups']]
cams = {l.split()[0]: ' '.join(l.split()[1:]) for l in open(os.path.join(HERE, '..', 'cams.txt')) if l.strip() and not l.startswith('#')}
lamp_hash = hashlib.sha1(json.dumps([cfg['lamps'], cfg['groups'], cfg.get('day'), cfg['top'], cfg.get('mirrors')], sort_keys=True).encode()).hexdigest()
state = {'cams': {v: cams[v] for v in cfg['views']}, 'lamps': lamp_hash}
ps = os.path.join(OUT, 'state-%s.json' % PT); prev = json.load(open(ps)) if os.path.exists(ps) else None
def home(p): return ET.fromstring(zipfile.ZipFile(p).read('Home.xml'))
LEAF = ('pieceOfFurniture', 'light', 'doorOrWindow')
def items(r):
    out, other = {}, []
    for e in r.iter():
        if e.tag in LEAF: out[e.get('id')] = e
        elif e.tag in ('wall', 'room', 'compass', 'level'): other.append(ET.tostring(e))
    return out, other
def sig(e):
    at = {k: v for k, v in e.attrib.items() if k not in ('description',) and not (k == 'name' and e.tag != 'light')}
    return json.dumps(at, sort_keys=True) + ''.join(ET.tostring(c, 'unicode') for c in e)
def rooms_of(e):
    x, y, w, d = (float(e.get(k, 0)) for k in ('x', 'y', 'width', 'depth')); h = max(w, d) / 2; hit = []
    for n, (x0, y0, x1, y1) in cfg['rooms'].items():
        if x + h > x0 - 20 and x - h < x1 + 20 and y + h > y0 - 20 and y - h < y1 + 20: hit.append(n)
    inside = any(x0 <= x <= x1 and y0 <= y <= y1 for x0, y0, x1, y1 in cfg['rooms'].values())
    return hit + ([] if inside else ['outside'])
why = []
if FULL: why.append('--full')
if prev is None: why.append('no state-%s.json' % PT)
elif prev['lamps'] != lamp_hash: why.append('lamp data, groups or day settings changed')
A, oa = items(home(PREV)); B, ob = items(home(NEW))
if oa != ob: why.append('walls, rooms or compass changed')
changed = set()
for i in set(A) | set(B):
    if i not in A or i not in B or sig(A[i]) != sig(B[i]):
        for e in (A.get(i), B.get(i)):
            if e is not None: changed.update(rooms_of(e))
stale = set()
for v, vc in cfg['views'].items():
    if why or changed & set(vc['rooms']) or prev is None or prev['cams'].get(v) != cams[v]: stale.add(v)
top_stale = bool(why or changed)
print('changed rooms:', sorted(changed) or '-', '| full render because:', '; '.join(why) or '-')
print('stale views (%d of %d): %s' % (len(stale), len(cfg['views']), ', '.join(sorted(stale)) or '-'), '| top view:', 'stale' if top_stale else 'kept')
linked = 0
for v in list(cfg['views']) + [cfg['top']]:
    if (v in stale) or (v == cfg['top'] and top_stale): continue
    sv = v.replace(':', '_').replace(',', '_')
    for g in GID:
        for suf in ('', '_lux'):
            src = os.path.join(OUT, g, '%s-%s%s.npy' % (sv, PT, suf)); dst = os.path.join(OUT, g, '%s-%s%s.npy' % (sv, NT, suf))
            if os.path.exists(src) and not os.path.exists(dst):
                if not DRY: os.link(src, dst)
                linked += 1
n = len(GID) * (len(stale) + (1 if top_stale else 0))
print('linked %d renders from %s; about %d to render' % (linked, PT, n) + (' (dry run)' if DRY else ''))
if not DRY: json.dump(state, open(os.path.join(OUT, 'state-%s.json' % NT), 'w'), indent=1)
