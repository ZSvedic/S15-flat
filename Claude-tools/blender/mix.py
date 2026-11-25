#!/usr/bin/env python3
"""Builds everything Zel looks at from the per-group renders of s15_blender.py (light adds up, so a mix = a sum):
 compare_<view>.jpg sheets, luxmaps.png, lux_table.md and light-mixer.html (switches + dimmers, self-contained).
Usage: mix.py <out dir with one folder per group> <result dir> [title] [version tag, e.g. v16]
With a version tag the files are compare-v16_<view>.jpg, luxmaps-v16.png, lux_table-v16.md and light-mixer-v16.html."""
import sys, os, json, re, io, base64, numpy as np, cv2, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); from tm import WB, EV, tone
OUT, RES = sys.argv[1], sys.argv[2]; TITLE = sys.argv[3] if len(sys.argv) > 3 else 'S15 lighting'
TAG = '-' + sys.argv[4] if len(sys.argv) > 4 else ''
os.makedirs(RES, exist_ok=True)
cfg = json.load(open(os.path.join(HERE, 'groups.json'))); GID = [g['id'] for g in cfg['groups']]; GL = {g['id']: g['label'] for g in cfg['groups']}
lum = json.load(open(os.path.join(OUT, 'lumens.json')))
safe = lambda v: v.replace(':', '_').replace(',', '_')
def load(g, v, suffix=''):
    p = os.path.join(OUT, g, safe(v) + suffix + '.npy')
    return np.load(p).astype('float32') if os.path.exists(p) else None
f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20); fs = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)

# ---- comparison sheets ---------------------------------------------------------------------------------------------
for view, st in cfg['views'].items():
    imgs = {g: load(g, view) for g in cfg['sets'][st]}
    if any(v is None for v in imgs.values()): print('missing renders for', view); continue
    w, h = 800, 600; panels = cfg['sheets'][st]; cols = 3; rows = (len(panels) + 1 + cols - 1) // cols
    sh = Image.new('RGB', (w * cols, (h + 30) * rows), 'white'); d = ImageDraw.Draw(sh)
    for i, (label, on) in enumerate(panels):
        x, y = (i % cols) * w, (i // cols) * (h + 30)
        sh.paste(Image.fromarray(tone(sum(imgs[g] for g in on))).resize((w, h), Image.LANCZOS), (x, y + 30)); d.text((x + 8, y + 4), label, fill='black', font=f)
    i = len(panels); x, y = (i % cols) * w + 20, (i // cols) * (h + 30) + 40
    for k, t in enumerate([view, 'Same camera exposure in all pictures.', 'Real lamp data: IKEA LEDARE GU10 (345 lm, 36°),', 'PILSKOTT pendant (1,100 lm) and floor lamp (700 lm).', 'Other lamp data is assumed (see groups.json).', 'Try any other mix in light-mixer' + TAG + '.html.']): d.text((x, y + 30 * k), t, fill='black', font=f)
    sh.save(os.path.join(RES, 'compare' + TAG + '_' + view + '.jpg'), quality=86)

# ---- lux maps and table ----------------------------------------------------------------------------------------------
top = cfg['top']; x0, y0, x1, y1 = [float(t) for t in top[4:].split(',')]
ROOMS = {'Living room (all)': (613, 1465, 306, 774), 'Kitchen worktop N (front edge)': (680, 870, 347, 368), 'Dining table': (780, 960, 535, 635), 'Sofa area': (1150, 1450, 520, 750),
         'Desk (living)': (1085, 1158, 310, 450), 'Bedroom': (233, 603, 306, 650), 'Hall entrance part': (41, 435, 660, 766), 'Corridor to the rooms': (435, 537, 766, 1061),
         'Sara': (547, 822, 962, 1348), 'Sara desk': (772, 822, 1114, 1234), 'Room 5': (225, 537, 1071, 1348), 'Room 5 desk': (462, 537, 1185, 1345), 'Laundry': (547, 822, 784, 950)}
levels = [0, 5, 10, 20, 30, 50, 75, 100, 150, 200, 300, 500, 1000]
luxg = {}
for g in GID:
    a = load(g, top, '_lux')
    if a is not None: luxg[g] = cv2.blur(cv2.medianBlur(a, 5), (9, 9))
if len(luxg) == len(GID):
    sy, sx = next(iter(luxg.values())).shape[0] / (y1 - y0), next(iter(luxg.values())).shape[1] / (x1 - x0); rows = []
    P = cfg['presets']; fig, ax = plt.subplots(2, 3, figsize=(24, 12.5)); ax = ax.ravel()
    for i, p in enumerate(P):
        lux = sum(luxg[g] for g in p['on']) * p.get('w', 100) / 100
        im = ax[i].imshow(lux, extent=(x0, x1, y1, y0), cmap='turbo', norm=BoundaryNorm(levels, 256)); ax[i].set_title(p['id'] + '  ' + p['label'], fontsize=12); ax[i].set_xticks([]); ax[i].set_yticks([])
        rows.append([p['id']] + [float(np.median(lux[int((c - y0) * sy):int((d - y0) * sy), int((a - x0) * sx):int((b - x0) * sx)])) for a, b, c, d in ROOMS.values()])
    for j in range(len(P), 6): ax[j].axis('off')
    fig.colorbar(im, ax=ax[-1], ticks=levels, fraction=0.5, label='lux on floors and furniture tops'); plt.tight_layout(); plt.savefig(os.path.join(RES, 'luxmaps' + TAG + '.png'), dpi=75); plt.close()
    with open(os.path.join(RES, 'lux_table' + TAG + '.md'), 'w') as fo:
        fo.write('\n'.join('- **%s**: %s' % (p['id'], p['label']) for p in P) + '\n\n| Median lux | ' + ' | '.join(r[0] for r in rows) + ' |\n|---|' + '---|' * len(rows) + '\n')
        for k, n in enumerate(ROOMS): fo.write('| ' + n + ' | ' + ' | '.join('%.0f' % r[k + 1] for r in rows) + ' |\n')
    print(open(os.path.join(RES, 'lux_table' + TAG + '.md')).read())

# ---- HTML mixer -------------------------------------------------------------------------------------------------------
GAMMA = 2.4
def enc_rgb(lin):
    x = np.maximum(lin * WB, 0); M = float(min(x.max(), max(np.percentile(x, 99.9), 4.0 / EV))) or 1e-6
    b = (np.clip(x / M, 0, 1) ** (1 / GAMMA) * 255 + 0.5).astype('uint8'); buf = io.BytesIO(); Image.fromarray(b).save(buf, 'JPEG', quality=82, optimize=True)
    return {'m': round(M, 6), 'src': 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()}
def enc_lux(a):
    M = float(a.max()) or 1e-6; b = (np.clip(a / M, 0, 1) ** (1 / GAMMA) * 255 + 0.5).astype('uint8'); buf = io.BytesIO(); Image.fromarray(b).save(buf, 'PNG', optimize=True)
    return {'m': round(M, 3), 'src': 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()}
NAMES = {'living': 'Living room + kitchen', 'room': 'Bedrooms', 'bed': 'Bedrooms', 'hall': 'Hall + corridor', 'plan': 'Whole flat'}
views = []
for view, st in cfg['views'].items():
    imgs = {g: load(g, view) for g in cfg['sets'][st]}
    if any(v is None for v in imgs.values()): continue
    views.append({'id': view, 'label': view[3:].replace('-', ' '), 'area': NAMES[st], 'kind': 'photo', 'g': {g: enc_rgb(a) for g, a in imgs.items()}})
tops = {g: load(g, top) for g in GID}
if all(v is not None for v in tops.values()) and len(luxg) == len(GID):
    views.append({'id': 'top', 'label': 'top view (ceiling removed)', 'area': NAMES['plan'], 'kind': 'photo', 'g': {g: enc_rgb(a) for g, a in tops.items()}})
    views.append({'id': 'lux', 'label': 'lux map', 'area': NAMES['plan'], 'kind': 'lux', 'g': {g: enc_lux(a) for g, a in luxg.items()}})
cm = plt.get_cmap('turbo'); pal = [[int(c * 255) for c in cm(i / (len(levels) - 1))[:3]] for i in range(len(levels))]
data = {'title': TITLE, 'groups': [{'id': g['id'], 'label': g['label'], 'lm': lum.get(g['id'], 0)} for g in cfg['groups']], 'presets': cfg['presets'], 'views': views,
        'wb': [float(v) for v in WB], 'ev': EV, 'gamma': GAMMA, 'levels': levels, 'pal': pal, 'rect': [x0, y0, x1, y1], 'zones': {k: list(v) for k, v in ROOMS.items()},
        'lamp': cfg['lamps']['gu10']['source']}
html = open(os.path.join(HERE, 'mixer_template.html')).read().replace('/*DATA*/null', json.dumps(data))
open(os.path.join(RES, 'light-mixer' + TAG + '.html'), 'w').write(html); print('light-mixer' + TAG + '.html', round(len(html) / 1e6, 1), 'MB,', len(views), 'views')
