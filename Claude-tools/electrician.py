#!/usr/bin/env python3
"""Files for the electrician, in Croatian (v22 on): the outlet list (Markdown + printable HTML for a PDF) and a schematic
(plan with every new outlet and a proposed cable route, plus one elevation per wall with new points).
The point table POINTS below is the single source; positions are model coordinates (cm, y south) from the vNN model and
the draft Claude-vectors/Hrneticka-wall-light-points-DRAFT.md. Distances along the wall are measured to the nearest room
corner or opening edge, computed from the model.
Usage (repo root): <venv>/bin/python Claude-tools/electrician.py <Home.xml of vNN> vNN
Writes Claude-vectors/Hrneticka-elektricar-vNN.md/.html and Claude-vectors/Hrneticka-elektricar-vNN-shema.svg/.png/.pdf
(the PDF of the list: headless Chrome from the .html, see the end of this file)."""
import sys, math, datetime, html, xml.etree.ElementTree as ET
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Circle
from matplotlib.backends.backend_pdf import PdfPages

SRC, TAG = sys.argv[1], sys.argv[2]
root = ET.parse(SRC).getroot()
CEIL = 280
TODAY = datetime.date.today().strftime('%d. %m. %Y.')

# ---- rooms (inner faces) and their Croatian names ---------------------------------------------------------------------------
ROOMS = {  # key: (name, x0, y0, x1, y1)
    'living': ('Dnevni boravak i kuhinja', 613, 306, 1465, 774),
    'bedroom': ('Spavaća soba 1 (glavna)', 233, 306, 603, 650),
    'ensuite': ('Kupaonica 1 (uz spavaću sobu)', 41, 306, 223, 595),
    'hall': ('Hodnik – ulaz', 41, 660, 613, 766),
    'niche': ('Hodnik – niša za garderobu', 41, 605, 223, 660),
    'corridor': ('Hodnik – prema sobama', 435, 766, 537, 1061),
    'cniche': ('Hodnik – niša s policama', 410, 945, 435, 1000),
    'bathroom': ('Kupaonica 2', 225, 778, 425, 1001),
    'laundry': ('Praonica', 547, 784, 822, 950),
    'sara': ('Spavaća soba 3', 547, 962, 822, 1348),
    'room5': ('Spavaća soba 2 (gostinjska)', 225, 1011, 537, 1348),
    'room5d': ('Spavaća soba 2 (gostinjska)', 225, 1071.45, 445, 1348),   # wall face west of the room 5 door
}
SIDE = {'N': 'sjeverni zid', 'S': 'južni zid', 'E': 'istočni zid', 'W': 'zapadni zid'}
CORNER = {('N', 0): 'SZ kuta', ('N', 1): 'SI kuta', ('S', 0): 'JZ kuta', ('S', 1): 'JI kuta',
          ('W', 0): 'SZ kuta', ('W', 1): 'JZ kuta', ('E', 0): 'SI kuta', ('E', 1): 'JI kuta'}
def wall_line(room, side):
    _, x0, y0, x1, y1 = ROOMS[room]
    return {'N': ('y', y0, x0, x1), 'S': ('y', y1, x0, x1), 'W': ('x', x0, y0, y1), 'E': ('x', x1, y0, y1)}[side]

# ---- openings from the model -------------------------------------------------------------------------------------------------
OPEN = []
for e in root.iter('doorOrWindow'):
    a = e.attrib; n = a.get('name', '')
    if 'balustrade' in n or 'Shower' in n: continue
    ang = float(a.get('angle', 0)) % math.pi; w = float(a['width']); x, y = float(a['x']), float(a['y'])
    kind = 'prozora' if ('Window' in n or 'window' in n) else 'vrata'
    el = float(a.get('elevation') or 0); h = float(a['height'])
    if abs(ang) < 0.1 or abs(ang - math.pi) < 0.1: OPEN.append(('y', y, x - w / 2, x + w / 2, kind, el, h))
    else: OPEN.append(('x', x, y - w / 2, y + w / 2, kind, el, h))
def openings_on(room, side):
    ax, c, a, b = wall_line(room, side)
    return [o for o in OPEN if o[0] == ax and abs(o[1] - c) < 25 and o[3] > a and o[2] < b]
def reference(room, side, pos):
    """Nearest corner or opening edge along the wall: (distance, text)."""
    ax, c, a, b = wall_line(room, side)
    cands = [(abs(pos - a), 'od ' + CORNER[(side, 0)]), (abs(b - pos), 'od ' + CORNER[(side, 1)])]
    for o in openings_on(room, side):
        if o[2] - 1 <= pos <= o[3] + 1: continue
        cands += [(abs(pos - o[3]), 'od ruba ' + o[4]) if pos > o[3] else (abs(o[2] - pos), 'od ruba ' + o[4])]
    d, t = min(cands); return round(d), t

# ---- ceiling points (as built, from the model): start of the assumed existing routes -----------------------------------------
NODES = []
for l in root.iter('light'):
    n = l.get('name', '')
    if n.startswith(('Light: ceiling lamp', 'Light: spot')): NODES.append((float(l.get('x')), float(l.get('y'))))
NODES.append((1050, 540))                                                  # dining pendant point (D), as built
def node_for(x, y, room):
    _, x0, y0, x1, y1 = ROOMS[room]
    inside = [p for p in NODES if x0 - 5 <= p[0] <= x1 + 5 and y0 - 5 <= p[1] <= y1 + 5] or NODES
    return min(inside, key=lambda p: math.hypot(p[0] - x, p[1] - y))

# ---- the points -----------------------------------------------------------------------------------------------------------------
# no, room, side, pos (x for N/S walls, y for E/W), height, type, wall (GK/AB/?), circuit, status (ok/wait/exist), note
WL = 'izvod za zidnu svjetiljku'
POINTS = [
    ('1', 'bedroom', 'N', 265, 205, WL + ' (gore/dolje, 2× GU10)', 'AB', 'ambijent B', 'ok', 'iznad vješalica'),
    ('2', 'bedroom', 'E', 353.8, 158, WL + ' (uz krevet, zasjenjena)', 'GK', 'ambijent B + tipkalo TB1', 'ok', 'sjeverna strana kreveta'),
    ('3', 'bedroom', 'E', 571.2, 158, WL + ' (uz krevet, zasjenjena)', 'GK', 'ambijent B + tipkalo TB2', 'ok', 'južna strana kreveta'),
    ('20', 'bedroom', 'W', 565, 255, 'napajanje LED trake i mjesto za driver (traka 160 cm na vrhu ormara, iza ruba)', '?', 'ambijent B', 'ok', 'iznad ormara (vrh ormara 236); izvod skriven iza ruba'),
    ('L4', 'bedroom', 'S', 592, 30, 'uklopna utičnica (podna lampa)', '?', 'ambijent B', 'ok', 'nova utičnica uz JI kut'),
    ('5', 'living', 'N', 1121.6, 241, WL + ' za sliku (nosač 18 cm), iznad slike bicikla', 'AB', 'ambijent A', 'wait', 'visina ovisi o stvarnoj veličini slike'),
    ('7a', 'living', 'N', 1405, 192, 'napajanje LED trake i mjesto za driver (traka iza ruba TV police + LED točke 6, 7 ispod police)', 'AB', 'ambijent A', 'ok', 'točna visina prema polici (vrh police 189); izvod skriven iza ruba police'),
    ('8', 'living', 'E', 672, 217, WL + ' za sliku (nosač 18 cm)', 'AB', 'ambijent A', 'wait', 'slika još nije odabrana'),
    ('9', 'living', 'S', 871, 213, WL + ' za sliku 100 cm (kabel ide vodoravnom zidnom letvicom)', 'GK', 'ambijent A', 'wait', 'izvod u gips-kartonu, 17 cm zapadno od spoja s betonom; visina ovisi o stvarnoj veličini slike'),
    ('K', 'living', 'W', 379, 160, 'napajanje LED letvi ispod gornjih kuhinjskih elemenata i mjesto za driver', 'GK', 'ambijent A', 'ok', 'unutar gornjeg elementa (dno elementa 150), iznad postojeće utičnice'),
    ('L1', 'living', 'S', 1364, 44, 'uklopna utičnica – prespojiti postojeću na krug ambijenta', 'AB', 'ambijent A', 'exist', 'postojeća utičnica; bez bušenja ako se može prespojiti'),
    ('L2', 'living', 'N', 1378, 43, 'uklopna utičnica – prespojiti postojeću (iza TV elementa)', 'AB', 'ambijent A', 'exist', 'ili nova utičnica 13 cm od SI kuta'),
    ('L3', 'living', 'E', 607, 35, 'uklopna utičnica – prespojiti postojeću na krug ambijenta', 'AB', 'ambijent A', 'exist', 'postojeća utičnica ispod prekidača'),
    ('DA', 'living', 'S', 724, 111, 'kutija za pametni dimer (duboka, s nulvodičem) – ambijent A', 'GK', 'dimer A', 'exist', 'umjesto postojeće kutije prekidača uz vrata hodnika; zona A = dnevni boravak, kuhinja, hodnici'),
    ('18', 'hall', 'N', 459, 207, WL + ' za sliku 45 cm (nosač 18 cm)', '?', 'ambijent A', 'wait', 'slika još nije odabrana; iza zida je instalacijsko okno'),
    ('19', 'niche', 'N', 146, 200, 'napajanje LED trake (140 cm) i driver u gornjem ormariću', '?', 'ambijent A', 'ok', 'unutar gornjeg ormarića (190 – strop)'),
    ('11', 'cniche', 'W', 972, 265, 'napajanje LED profila (5 × 58 cm) i mjesto za driver 24 V', '?', 'ambijent A', 'ok', 'na vrhu niše, iznad gornje police'),
    ('10', 'laundry', 'S', 667, 175, WL + ' (gore/dolje, 2× GU10)', 'GK', 'vlastiti prekidač (S10)', 'ok', 'nasuprot utičnice u sobi 3'),
    ('S10', 'laundry', 'W', 858, 110, 'dvostruki prekidač (strop + svjetiljka 10)', '?', 'praonica', 'exist', 'umjesto postojećeg prekidača'),
    ('T', 'laundry', 'N', 790, 210, 'napajanje svjetla u ormaru (uključuje se otvaranjem vrata)', 'GK', 'praonica', 'wait', 'točno mjesto prema stolaru'),
    ('15', 'sara', 'W', 1250, 129, WL + ' (za čitanje, zasjenjena)', '?', 'ambijent C + tipkalo TC', 'ok', 'iznad uzglavlja, 98 cm od južnog zida'),
    ('16', 'sara', 'E', 1173.7, 175, WL + ' (gore/dolje, dolje široki snop 60°)', 'AB', 'ambijent C', 'ok', 'iznad sredine stola'),
    ('21', 'sara', 'N', 747, 255, 'napajanje LED trake i mjesto za driver (traka 150 cm na vrhu ormara, iza ruba)', 'GK', 'ambijent C', 'ok', 'iznad ormara (vrh ormara 236)'),
    ('TC', 'sara', 'W', 1228, 80, 'tipkalo uz krevet (kutija, žica do dimera C)', '?', 'dimer C', 'ok', 'ispod svjetiljke 15'),
    ('DC', 'sara', 'W', 1068, 110, 'kutija za pametni dimer (duboka, s nulvodičem) – ambijent C', '?', 'dimer C', 'exist', 'umjesto postojeće kutije prekidača uz vrata'),
    ('12', 'room5', 'W', 1175.3, 149, WL + ' (za čitanje, zasjenjena)', 'AB', 'ambijent D + tipkalo TD', 'ok', 'iznad kauča'),
    ('13', 'room5', 'E', 1265, 175, WL + ' (gore/dolje, dolje široki snop 60°)', '?', 'ambijent D', 'ok', 'iznad sredine stola; zamjenjuje stare točke 13 i 14'),
    ('TD', 'room5', 'W', 1155, 80, 'tipkalo uz krevet (kutija, žica do dimera D)', 'AB', 'dimer D', 'ok', 'ispod svjetiljke 12'),
    ('DD', 'room5d', 'N', 442, 110, 'kutija za pametni dimer (duboka, s nulvodičem) – ambijent D', '?', 'dimer D', 'exist', 'umjesto postojeće kutije prekidača uz vrata'),
    ('TB1', 'bedroom', 'E', 356, 80, 'tipkalo uz krevet (kutija, žica do dimera B)', 'GK', 'dimer B', 'ok', 'iznad postojeće utičnice uz krevet'),
    ('TB2', 'bedroom', 'E', 569, 80, 'tipkalo uz krevet (kutija, žica do dimera B)', 'GK', 'dimer B', 'ok', 'iznad postojeće utičnice uz krevet'),
    ('DB', 'bedroom', 'S', 400, 110, 'kutija za pametni dimer (duboka, s nulvodičem) – ambijent B', '?', 'dimer B', 'exist', 'umjesto postojeće kutije prekidača uz vrata'),
    ('M1', 'ensuite', 'N', 95, 200, 'postojeći izvod za ogledalo sa svjetlom – bez radova', 'GK', 'strop (kupaonica)', 'exist', 'ogledalo 140×95 (115–210) ga pokriva; driver iza ogledala'),
    ('M2', 'bathroom', 'E', 885, 200, 'izvod za ogledalo sa svjetlosnim rubom (driver iza ogledala)', '?', 'strop (kupaonica)', 'ok', 'iznad umivaonika; provjeriti postoji li već izvod (el. projekt)'),
]
ORDER = ['living', 'hall', 'niche', 'cniche', 'bedroom', 'ensuite', 'bathroom', 'laundry', 'sara', 'room5', 'room5d']
JOINTS = {('living', 'S'): [(888, 'spoj: zapadno gips-karton | istočno beton (275 od JZ kuta)')]}   # from the draft (row 9) and the architect plan
MAT = {'GK': ('gips-karton', '#1f6fd1'), 'AB': ('beton', '#d12a1f'), '?': ('provjeriti', '#8a3fd1')}
def xy(p):
    ax, c, a, b = wall_line(p[1], p[2]); return (p[3], c) if ax == 'y' else (c, p[3])

# ---- Markdown + HTML list ----------------------------------------------------------------------------------------------------------
def status(p): return {'ok': 'izvesti', 'wait': '**NE BUŠITI – čeka potvrdu**', 'exist': 'postojeće mjesto'}[p[8]]
groups = {}
for p in POINTS: groups.setdefault(ROOMS[p[1]][0], []).append(p)
md = [f'# Popis izvoda – rasvjeta (model {TAG}, {TODAY})', '',
      'Stan Hrnetička. Novi izvodi za zidnu i skrivenu rasvjetu, kutije za pametne dimere, tipkala uz krevete i uklopne utičnice. '
      'Strane svijeta prema tlocrtu (gore = sjever). Mjere u cm; visina = sredina izvoda od gotovog poda; udaljenost = vodoravno '
      'po zidu od najbližeg kuta sobe ili ruba otvora. Tolerancija ±5 cm dok se ne provjeri na licu mjesta.', '',
      '**Prije bušenja provjeriti trasu detektorom kabela.** Postojeće trase u nacrtu su pretpostavljene.', '',
      'Shema s trasama i pogledima zidova: `Hrneticka-elektricar-' + TAG + '-shema.pdf`. Plavo = gips-karton (kabel kroz šupljinu zida, '
      'jedna rupa na izvodu), crveno = beton/zid (štemanje od stropa ili najbliže kutije), ljubičasto = materijal zida treba provjeriti.', '']
for name, ps in groups.items():
    md += [f'## {name}', '', '| br. | zid | udaljenost | visina | vrsta izvoda | zid: materijal | strujni krug | status | napomena |', '|---|---|---|---|---|---|---|---|---|']
    for p in ps:
        d, t = reference(p[1], p[2], p[3])
        md.append(f'| {p[0]} | {SIDE[p[2]]} | {d} {t} | {p[4]} | {p[5]} | {MAT[p[6]][0]} | {p[7]} | {status(p)} | {p[9]} |')
    md.append('')
nwait = sum(p[8] == 'wait' for p in POINTS)
md += ['## Dimeri, tipkala i prekidači', '',
       '- **Pametni dimeri** (modul u kutiji iza običnog tipkala, npr. Shelly, Matter): četiri zone ambijenta, svaka sa svojim dimerom: '
       '**A** dnevni boravak + kuhinja + hodnici (DA), **B** spavaća soba 1 (DB), **C** spavaća soba 3 (DC), **D** spavaća soba 2 (DD). '
       'Na svakom mjestu duboka kutija (60 mm) i **nulvodič**. Svi ambijentalni izvodi jedne zone spajaju se na izlaz njenog dimera.',
       '- **Tipkala uz krevete** (žičana, u kutiji): TB1, TB2 (spavaća soba 1), TC (spavaća soba 3), TD (spavaća soba 2); spajaju se na dimer svoje sobe.',
       '- **Vlastiti prekidač:** zidna svjetiljka 10 u praonici (S10) i vanjske svjetiljke na terasi nisu u krugu ambijenta.',
       '- **Uklopne utičnice** (za podne i stolne lampe): L1–L3 u dnevnom boravku (prespojiti postojeće), L4 u spavaćoj sobi 1 (nova).',
       '- **Ormari:** svjetlo u ormaru spavaće sobe 1 napaja se iz postojeće dvostruke utičnice iza ormara (bez novog izvoda); u praonici izvod T prema stolaru.',
       '- **Rasvjeta s mrežnim upravljanjem:** viseća lampa nad stolom (D, postojeći stropni izvod) i podne lampe IKEA PILSKOTT imaju svoj daljinski; njihove utičnice i stropni izvod trebaju običan prekidač, ne dimer.',
       '- Ogledala sa svjetlosnim rubom (M1, M2) su na prekidaču stropnog svjetla kupaonice.', '',
       '## Rasvjetna tijela', '',
       '- **CRI (Ra) ≥ 90** za sve, **≥ 95** za svjetiljke za slike (5, 8, 9, 18).',
       '- **Ambijent 2700 K**; stropna svjetla mogu biti 3000 K.',
       '- Žarulje GU10: IKEA LEDARE 345 lm, 2700 K, 36°, prigušive; iznad stolova (13, 16) široki snop 60°.',
       '- LED trake i profili: driveri prigušivi faznim rezom (kompatibilni s dimerom). Prvo isprobati jedan dimer sa stvarnim žaruljama (mala LED opterećenja mogu treperiti).', '',
       f'## Ne bušiti još ({nwait})', '',
       '- 5, 9: potvrditi stvarnu veličinu slika (bicikl, Canadair).', '- 8, 18: slike još nisu odabrane.', '- T: mjesto prema stolaru.', '',
       '## Materijal zidova', '',
       'Iz arhitektonskog nacrta 1:50: šrafirani zidovi su AB (pročelja, zid prema susjednom stanu u spavaćoj sobi 2); zidovi s oznakom GK10/GK12 su gips-karton '
       '(spavaća soba 1 – kuhinja, praonica – hodnik, praonica – spavaća soba 3, zapadni dio južnog zida dnevnog boravka). '
       'Ostale pregrade (10 cm, bez oznake) označene su **provjeriti**.', '']
open(f'Claude-vectors/Hrneticka-elektricar-{TAG}.md', 'w').write('\n'.join(md))

def md_inline(s): return html.escape(s).replace('**', '\x00').replace('`', '')
def to_html(lines):
    out, intable = [], False
    for l in lines:
        if l.startswith('|---'): continue
        if l.startswith('|'):
            cells = [c.strip() for c in l.strip('|').split('|')]
            if not intable: out.append('<table><tr>' + ''.join(f'<th>{html.escape(c)}</th>' for c in cells) + '</tr>'); intable = True; continue
            cls = ' class="wait"' if 'NE BUŠITI' in l else ''
            out.append(f'<tr{cls}>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>'); continue
        if intable: out.append('</table>'); intable = False
        if l.startswith('# '): out.append(f'<h1>{html.escape(l[2:])}</h1>')
        elif l.startswith('## '): out.append(f'<h2>{html.escape(l[3:])}</h2>')
        elif l.startswith('- '): out.append(f'<li>{l[2:]}</li>')
        elif l: out.append(f'<p>{l}</p>')
    if intable: out.append('</table>')
    s = '\n'.join(out)
    import re
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s); s = re.sub(r'`(.+?)`', r'<code>\1</code>', s)
    return s
page = f'''<!DOCTYPE html><html lang="hr"><head><meta charset="utf-8"><title>Popis izvoda – Hrnetička {TAG}</title><style>
@page{{size:A4 landscape;margin:12mm}} body{{font:10pt/1.35 system-ui,-apple-system,"Segoe UI",sans-serif;color:#111}}
h1{{font-size:16pt;margin:0 0 6px}} h2{{font-size:12pt;margin:14px 0 4px;break-after:avoid}} p,li{{margin:3px 0}}
table{{border-collapse:collapse;width:100%;font-size:8.5pt;break-inside:auto}} th,td{{border:1px solid #999;padding:3px 5px;vertical-align:top;text-align:left}}
th{{background:#eee}} tr{{break-inside:avoid}} tr.wait td{{background:#fde2e0}} code{{font-size:9pt}}
</style></head><body>{to_html(md)}</body></html>'''
open(f'Claude-vectors/Hrneticka-elektricar-{TAG}.html', 'w').write(page)

# ---- schematic: plan ---------------------------------------------------------------------------------------------------------------
def wall_polys():
    for w in root.iter('wall'):
        a = w.attrib; x1, y1, x2, y2, t = [float(a[k]) for k in ('xStart', 'yStart', 'xEnd', 'yEnd', 'thickness')]
        L = math.hypot(x2 - x1, y2 - y1) or 1; nx, ny = -(y2 - y1) / L * t / 2, (x2 - x1) / L * t / 2
        yield [(x1 + nx, y1 + ny), (x2 + nx, y2 + ny), (x2 - nx, y2 - ny), (x1 - nx, y1 - ny)]
ASB = [(float(e.get('x')), float(e.get('y'))) for e in root.iter('pieceOfFurniture') if e.get('name', '').startswith('As built:')]
NEW = [p for p in POINTS if p[8] != 'exist' or p[0].startswith(('D', 'S'))]
fig_plan = plt.figure(figsize=(16.5, 11.7)); ax = fig_plan.add_axes([0.02, 0.06, 0.70, 0.88])
for poly in wall_polys(): ax.add_patch(Polygon(poly, closed=True, fc='#777', ec='#555', lw=0.3))
for o in OPEN:
    if o[0] == 'y': ax.plot([o[2], o[3]], [o[1], o[1]], color='#9ad', lw=3)
    else: ax.plot([o[1], o[1]], [o[2], o[3]], color='#9ad', lw=3)
for k, (n, x0, y0, x1, y1) in ROOMS.items():
    if k in ('niche', 'cniche', 'room5d'): continue
    ax.text((x0 + x1) / 2, (y0 + y1) / 2, n, ha='center', va='center', fontsize=8, color='#888', style='italic', wrap=True)
for x, y in ASB: ax.plot(x, y, 's', ms=2.5, color='#bbb')
for x, y in NODES: ax.plot(x, y, marker='$\\otimes$', ms=9, color='#999')
for p in POINTS:
    x, y = xy(p); col = MAT[p[6]][1]; nx, ny = node_for(x, y, p[1])
    if p[8] != 'exist' or p[0].startswith(('D', 'S')):
        ax.plot([nx, x], [ny, y], ls=(0, (4, 3)), color='#666', lw=0.9)                 # in the ceiling (assumed)
    fc = '#fff' if p[8] == 'exist' else ('#fde2e0' if p[8] == 'wait' else col)
    shape = 's' if p[0][0] in 'DTS' and p[0] not in ('T',) else 'o'
    ax.plot(x, y, shape, ms=11, mfc=fc, mec=col, mew=2)
    off = (-26, -14) if p[0].startswith('T') and p[0] != 'T' else ((8, -14) if p[0] in ('13', 'K', '3') else (6, 6))
    ax.annotate(p[0], (x, y), xytext=off, textcoords='offset points', fontsize=8.5, weight='bold', color='#111')
ax.set_xlim(20, 1490); ax.set_ylim(1380, 280); ax.set_aspect('equal'); ax.axis('off')
ax.plot([40, 140], [1370, 1370], color='k', lw=2); ax.text(90, 1362, '1 m', ha='center', fontsize=8)
ax.annotate('S', xy=(1440, 300), xytext=(1440, 360), ha='center', fontsize=12, weight='bold', arrowprops=dict(arrowstyle='-|>', color='k'))
lg = fig_plan.add_axes([0.73, 0.06, 0.26, 0.88]); lg.axis('off')
txt = [(f'Hrnetička – izvodi za rasvjetu', 13, 'bold'), (f'model {TAG}, {TODAY}', 9, 'normal'), ('', 6, 'normal'),
       ('Trasa u zidu (pogledi zidova na sljedećim stranicama):', 9, 'bold')]
y = 0.98
for t, s, w in txt: lg.text(0, y, t, fontsize=s, weight=w, va='top'); y -= 0.028 if s > 6 else 0.012
for k, (n, c) in MAT.items():
    lg.plot([0, 0.08], [y - 0.008] * 2, color=c, lw=3); lg.text(0.11, y, {'GK': 'gips-karton: kabel kroz šupljinu zida, jedna rupa na izvodu', 'AB': 'beton / zid: štemanje', '?': 'materijal zida provjeriti'}[k], fontsize=8, va='top'); y -= 0.03
for t in ['- - -  u stropu od najbližeg stropnog izvoda (pretpostavljeno;', '         stvarne trase nisu poznate)',
          '⊗  postojeći stropni izvod (svjetlo)', '▪  postojeći prekidač / utičnica (s fotografija)',
          '●  novi izvod (boja = materijal zida)', '■  dimer / tipkalo / prekidač',
          '○ □  postojeće mjesto (prespojiti / zamijeniti kutiju)', 'ružičasto: NE BUŠITI – čeka potvrdu', '',
          'Pravila: okomito od stropa ravno do izvoda; vodoravno', 'samo u zoni 15–45 cm ispod stropa; okomito uz kutove', 'i otvore u zoni 10–30 cm (DIN 18015-3).',
          'Prije bušenja provjeriti trasu detektorom kabela.', 'Strane svijeta prema tlocrtu (gore = sjever).', '']:
    lg.text(0, y, t, fontsize=8, va='top'); y -= 0.024
for p in POINTS:
    if y < 0.01: break
    lg.text(0, y, f'{p[0]:>4}  {p[5][:62]}', fontsize=6.3, va='top', family='DejaVu Sans Mono'); y -= 0.0165
lg.set_xlim(0, 1); lg.set_ylim(0, 1)
for ext in ('svg', 'png'): fig_plan.savefig(f'Claude-vectors/Hrneticka-elektricar-{TAG}-shema.{ext}', dpi=150)

# ---- schematic: wall elevations ----------------------------------------------------------------------------------------------------
walls = {}
for p in POINTS: walls.setdefault((p[1], p[2]), []).append(p)
def elevation(ax, room, side, ps):
    axn, c, a, b = wall_line(room, side); L = b - a
    # seen from inside the room: N wall west->east, S wall east->west, E wall north->south, W wall south->north
    flip = side in ('S', 'W')
    def u(pos): return (b - pos) if flip else (pos - a)
    ax.add_patch(Rectangle((0, 0), L, CEIL, fc='#f6f6f6', ec='#444', lw=1))
    for o in openings_on(room, side):
        u0, u1 = sorted((u(max(o[2], a)), u(min(o[3], b)))); ax.add_patch(Rectangle((u0, o[5]), u1 - u0, min(o[6], CEIL - o[5]), fc='#dbe9f5', ec='#7a9cc0', lw=0.8))
        ax.text((u0 + u1) / 2, o[5] + 8, o[4].replace('prozora', 'prozor'), ha='center', fontsize=6, color='#557')
    for jp, jt in JOINTS.get((room, side), []):
        ax.plot([u(jp)] * 2, [0, CEIL], color='#555', ls=':', lw=1); ax.text(u(jp), CEIL / 2, jt, rotation=90, fontsize=6.5, ha='right', va='center', color='#555')
    for e in root.iter('pieceOfFurniture'):
        if not e.get('name', '').startswith('As built:'): continue
        ex, ey = float(e.get('x')), float(e.get('y')); el = float(e.get('elevation') or 0) + float(e.get('height')) / 2
        on = abs((ey if axn == 'y' else ex) - c) < 4 and a <= (ex if axn == 'y' else ey) <= b
        if on: ax.plot(u(ex if axn == 'y' else ey), el, 's', ms=4, color='#aaa')
    for p in ps:
        uu = u(p[3]); col = MAT[p[6]][1]
        if p[8] != 'exist' or p[0].startswith(('D', 'S')):
            ax.plot([uu, uu], [CEIL, p[4]], color=col, lw=2.2, ls='-' if p[6] != '?' else (0, (3, 2)))
        fc = '#fff' if p[8] == 'exist' else ('#fde2e0' if p[8] == 'wait' else col)
        ax.plot(uu, p[4], 'o', ms=8, mfc=fc, mec=col, mew=2)
        d, t = reference(room, side, p[3])
        ax.annotate(f'{p[0]}\n{d} {t.replace("od ", "")}\nh {p[4]}', (uu, p[4]), xytext=(5, -4), textcoords='offset points', fontsize=6.5, va='top')
    ax.set_xlim(-10, L + 10); ax.set_ylim(-10, CEIL + 12); ax.set_aspect('equal'); ax.axis('off')
    ends = {'N': ('Z', 'I'), 'S': ('I', 'Z'), 'E': ('S', 'J'), 'W': ('J', 'S')}[side]
    ax.text(0, CEIL + 4, ends[0], fontsize=7, color='#666'); ax.text(L, CEIL + 4, ends[1], fontsize=7, color='#666', ha='right')
    mats = {MAT[p[6]][0] for p in ps}
    ax.set_title(f'{ROOMS[room][0]} – {SIDE[side]} (pogled iz sobe, dužina {L:.0f}, visina {CEIL}) – {", ".join(sorted(mats))}', fontsize=7.5, loc='left')
keys = sorted(walls, key=lambda k: (ORDER.index(k[0]), 'NESW'.index(k[1])))
figs = []
for i in range(0, len(keys), 6):
    f, axs = plt.subplots(3, 2, figsize=(16.5, 11.7)); f.subplots_adjust(left=0.02, right=0.98, top=0.94, bottom=0.03, hspace=0.25, wspace=0.05)
    f.suptitle(f'Hrnetička – pogledi zidova s novim izvodima (model {TAG}, {TODAY}); plavo gips-karton, crveno beton, ljubičasto provjeriti; mjere u cm od gotovog poda', fontsize=10, x=0.02, ha='left')
    for j, axx in enumerate(axs.flat):
        if i + j < len(keys): elevation(axx, keys[i + j][0], keys[i + j][1], walls[keys[i + j]])
        else: axx.axis('off')
    figs.append(f)
figs[0].savefig(f'Claude-vectors/Hrneticka-elektricar-{TAG}-zidovi.png', dpi=110)
with PdfPages(f'Claude-vectors/Hrneticka-elektricar-{TAG}-shema.pdf') as pdf:
    pdf.savefig(fig_plan)
    for f in figs: pdf.savefig(f)
chase = sum(CEIL - p[4] for p in POINTS if p[6] == 'AB' and p[8] == 'ok'); unk = sum(CEIL - p[4] for p in POINTS if p[6] == '?' and p[8] == 'ok')
print(f'{len(POINTS)} points ({nwait} wait), {len(keys)} walls, {len(figs)} elevation pages; vertical chase in concrete about {chase / 100:.1f} m, in walls to check {unk / 100:.1f} m')
# PDF of the list: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --no-pdf-header-footer
#   --print-to-pdf=Claude-vectors/Hrneticka-elektricar-vNN.pdf file://$PWD/Claude-vectors/Hrneticka-elektricar-vNN.html
