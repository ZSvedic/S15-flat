#!/usr/bin/env python3
"""Builds comparison sheets (one per view, variants side by side), lux maps per variant and a lux table.
Usage: compare.py <out dir with one folder per variant> <result dir>"""
import sys, os, glob, json, re, numpy as np, cv2, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from PIL import Image, ImageDraw, ImageFont
OUT, RES = sys.argv[1], sys.argv[2]; os.makedirs(RES, exist_ok=True)
V = [v['id'] for v in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'variants.json')))['variants'] if os.path.isdir(os.path.join(OUT, v['id']))]
LABEL = {'V0-ceiling-only': 'V0  ceiling lamps + pendants only', 'V1-wall-narrow': 'V1  wall lights only, narrow up/down (40°)',
         'V2-wall-wide': 'V2  wall lights only, wide shielded type (110°)', 'V3-wall-narrow+kitchen+pendants': 'V3  V1 + kitchen under-cabinet + pendants',
         'V4-everything': 'V4  everything on'}
f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 20)
views = sorted(os.path.basename(p)[:-4] for p in glob.glob(os.path.join(OUT, V[0], '*.png')) if not os.path.basename(p).startswith('TOP'))
for view in views:
    w, h = 800, 600; sh = Image.new('RGB', (w * 3, (h + 30) * 2), 'white'); d = ImageDraw.Draw(sh)
    for i, v in enumerate(V):
        x, y = (i % 3) * w, (i // 3) * (h + 30)
        sh.paste(Image.open(os.path.join(OUT, v, view + '.png')).convert('RGB').resize((w, h), Image.LANCZOS), (x, y + 30)); d.text((x + 8, y + 4), LABEL.get(v, v), fill='black', font=f)
    d.text((w * 2 + 20, h + 60), view, fill='black', font=f); d.text((w * 2 + 20, h + 100), 'Same camera exposure in all pictures.', fill='black', font=f)
    sh.save(os.path.join(RES, 'compare_' + view + '.jpg'), quality=86)
top = glob.glob(os.path.join(OUT, V[0], 'TOP_*_lux.npy'))
if top:
    name = os.path.basename(top[0]); x0, y0, x1, y1 = [float(t) for t in re.findall(r'TOP_([\d.]+)_([\d.]+)_([\d.]+)_([\d.]+)', name)[0]]
    ROOMS = {'Living room (all)': (613, 1465, 306, 774), 'Kitchen worktop N (front edge)': (680, 870, 347, 368), 'Dining table': (780, 960, 535, 635), 'Sofa area': (1150, 1450, 520, 750),
             'Desk (living)': (1085, 1158, 310, 450), 'Bedroom': (233, 603, 306, 650), 'Hall': (41, 537, 660, 766), 'Corridor': (435, 537, 766, 1061),
             'Sara': (547, 822, 962, 1348), 'Sara desk': (772, 822, 1114, 1234), 'Room 5': (225, 537, 1071, 1348), 'Room 5 desk': (467, 537, 1200, 1340), 'Laundry': (547, 822, 784, 950)}
    levels = [0, 5, 10, 20, 30, 50, 75, 100, 150, 200, 300, 500, 1000]; rows = []
    fig, ax = plt.subplots(2, 3, figsize=(24, 12.5)); ax = ax.ravel()
    for i, v in enumerate(V):
        lux = np.load(os.path.join(OUT, v, name)); lux = cv2.blur(cv2.medianBlur(lux, 5), (9, 9)); sy, sx = lux.shape[0] / (y1 - y0), lux.shape[1] / (x1 - x0)
        im = ax[i].imshow(lux, extent=(x0, x1, y1, y0), cmap='turbo', norm=BoundaryNorm(levels, 256)); ax[i].set_title(LABEL.get(v, v), fontsize=13); ax[i].set_xticks([]); ax[i].set_yticks([])
        rows.append([v] + [float(np.median(lux[int((c - y0) * sy):int((d - y0) * sy), int((a - x0) * sx):int((b - x0) * sx)])) for a, b, c, d in ROOMS.values()])
    for j in range(len(V), 6): ax[j].axis('off')
    fig.colorbar(im, ax=ax[-1], ticks=levels, fraction=0.5, label='lux on floors and furniture tops'); plt.tight_layout(); plt.savefig(os.path.join(RES, 'luxmaps.png'), dpi=75)
    with open(os.path.join(RES, 'lux_table.md'), 'w') as fo:
        fo.write('| Median lux | ' + ' | '.join(r[0].split('-')[0] for r in rows) + ' |\n|---|' + '---|' * len(rows) + '\n')
        for k, n in enumerate(ROOMS): fo.write('| ' + n + ' | ' + ' | '.join('%.0f' % r[k + 1] for r in rows) + ' |\n')
    print(open(os.path.join(RES, 'lux_table.md')).read())
