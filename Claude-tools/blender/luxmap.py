#!/usr/bin/env python3
"""Colour a top-view lux array (from s15_blender.py) and print per-room statistics.
Usage: luxmap.py out/TOP_x0_y0_x1_y1_lux.npy out/TOP_..png result.png"""
import sys, re, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from PIL import Image
lux = np.load(sys.argv[1]); x0, y0, x1, y1 = [float(v) for v in re.findall(r'TOP_([\d.]+)_([\d.]+)_([\d.]+)_([\d.]+)', sys.argv[1])[0]]
import cv2
lux = cv2.medianBlur(lux.astype('float32'), 5); lux = cv2.blur(lux, (15, 15))          # passes are not denoised: smooth over 15 cm
levels = [0, 10, 20, 30, 50, 75, 100, 150, 200, 300, 500, 1000]
fig, ax = plt.subplots(1, 2, figsize=(22, 5.2), gridspec_kw=dict(width_ratios=[1, 1.08]))
ax[0].imshow(Image.open(sys.argv[2]), extent=(x0, x1, y1, y0)); ax[0].set_title('Top view, night, all lights on (ceiling removed)')
im = ax[1].imshow(lux, extent=(x0, x1, y1, y0), cmap='turbo', norm=BoundaryNorm(levels, 256)); ax[1].set_title('Illuminance on visible surfaces (lux)')
cs = ax[1].contour(np.linspace(x0, x1, lux.shape[1]), np.linspace(y0, y1, lux.shape[0]), lux, levels=[50, 100, 200], colors='k', linewidths=0.6)
ax[1].clabel(cs, fmt='%d', fontsize=7); fig.colorbar(im, ax=ax[1], ticks=levels, fraction=0.025)
for a in ax: a.set_xlabel('model x (cm)'); a.set_ylabel('model y (cm)')
plt.tight_layout(); plt.savefig(sys.argv[3], dpi=110)
ROOMS = {'Living + kitchen': (613, 1465, 306, 774), 'Bedroom': (233, 603, 306, 650), 'Dining table area': (780, 960, 535, 635), 'Sofa area': (1150, 1450, 520, 750), 'Kitchen worktop north': (620, 900, 310, 370)}
for n, (a, b, c, d) in ROOMS.items():
    r = lux[int(c - y0):int(d - y0), int(a - x0):int(b - x0)]
    if r.size: print('%-24s mean %4.0f  median %4.0f  min(p5) %4.0f  max(p95) %4.0f lux' % (n, r.mean(), np.median(r), np.percentile(r, 5), np.percentile(r, 95)))
