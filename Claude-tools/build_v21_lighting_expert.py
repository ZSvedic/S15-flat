#!/usr/bin/env python3
"""v21 -> v21-lighting-expert: the changes C1-C15 of the lighting-expert critique (2026-11-26), see
Claude-vectors/S15-v21-lighting-expert-notes.md. Removals, moves and lamp-data changes are here; new fixtures (C3, C4, C5, C6,
C14) come from the fixture list via build_lightset.py afterwards. Lamp-data changes rename the lights to "XA:"/"XC:" with the
new data in the name (one source per 20 cm of strip instead of four), so the shared lamp roles stay unchanged.
Usage: build_v21_lighting_expert.py <v21 Home.xml> <out Home.xml>"""
import re, sys, xml.etree.ElementTree as ET
tree = ET.parse(sys.argv[1]); root = tree.getroot()
par = {c: p for p in root.iter() for c in p}
def F(v): return f'{v:.2f}'.rstrip('0').rstrip('.')
def find(rx, tag=None): return [e for e in root.iter() if (tag is None or e.tag == tag) and re.match(rx, e.get('name', ''))]
def drop(rx, n=None, tag=None):
    es = find(rx, tag); assert es and (n is None or len(es) == n), (rx, len(es))
    for e in es: par[e].remove(e)
def shift(es, dy=0, dz=0):
    for e in es:
        if dy: e.set('y', F(float(e.get('y')) + dy))
        if dz: e.set('elevation', F(float(e.get('elevation')) + dz))
def relamp(rx, prefix, data):
    es = find(rx, 'light'); assert es, rx
    for e in es:
        n = e.get('name'); aim = re.search(r'(-> *[-\d.]+,[-\d.]+,[-\d.]+)$', n); body = re.sub(r'^[^:]*:\s*', '', re.sub(r'\s*->.*$', '', n))
        e.set('name', f'{prefix} expert {body} {data}' + (' ' + aim.group(1) if aim else ''))
    return len(es)
drop(r'A0[67] LED puck', 2); drop(r'TV puck:', 2, 'light')                       # C1
drop(r'L2 ', 2); drop(r'Low bar z: L2', 5, 'light')                              # C2
drop(r'L1 ', 2); drop(r'Low bar z: L1', 5, 'light')                              # C3 (new floor lamp from the list)
drop(r'Low lamp: L3', 1, 'light')                                                # C4 (new 800 lm table lamp from the list)
for g in find(r'Wall light [LR]$', 'furnitureGroup'): par[g].remove(g)           # C5, C6 (new lights from the list)
shift(find(r'A16 ') + find(r'AmbA (up|down): A16'), dz=20)                       # C7
shift(find(r'A14 ') + find(r'AmbA (up|down): A14'), dy=-17)                      # C8
shift(find(r'A13 ') + find(r'AmbA (up|down): A13'), dy=17)                       # C9
drop(r'A10 ', 2); drop(r'AmbA (up|down): A10', 2, 'light')                       # C10
print('C11 niche', relamp(r'Niche bar', 'XA:', '{lm=30 beam=120 k=2700 r=1}'))            # 150 lm/m
print('C12 hall bar', relamp(r'HallBench bar', 'XA:', '{lm=60 beam=120 k=2700 r=1}'))     # 300 lm/m
print('C13 kitchen bar', relamp(r'Kitchen bar', 'XA:', '{lm=200 beam=120 k=2700 r=1}'))   # 1000 lm/m
print('C15 hall spots', relamp(r'Light: spot – hall', 'XC:', '{lm=230 beam=60 k=2700 r=3}'))
root.set('name', 'S15-Hrneticka-v21-lighting-expert.sh3d')
tree.write(sys.argv[2], encoding='UTF-8', xml_declaration=True)
