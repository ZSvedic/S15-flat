#!/usr/bin/env python3
"""Writes index.html (the GitHub Pages landing page) for one version from groups.json and Renders/blender-lighting/*-<tag>*.
Usage (repo root): python3 Claude-tools/make_site.py v22"""
import sys, os, json, html, datetime
TAG = sys.argv[1]; R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cfg = json.load(open(os.path.join(R, 'Claude-tools', 'blender', 'groups.json')))
B = 'Renders/blender-lighting/'
REPO = 'ZSvedic/Hrneticka-flat'                     # GitHub repository (owner/name); the site is https://<owner>.github.io/<name>/
def ex(p): return os.path.exists(os.path.join(R, p))
lux = open(os.path.join(R, B, 'lux_table-%s.md' % TAG)).read().split('\n')
rows = [l for l in lux if l.startswith('|') and not l.startswith('|---')]
head = [c.strip() for c in rows[0].strip('|').split('|')]
table = '<table><thead><tr>' + ''.join('<th>%s</th>' % html.escape(c) for c in head) + '</tr></thead><tbody>'
for r in rows[1:]:
    c = [x.strip() for x in r.strip('|').split('|')]
    table += '<tr><th scope="row">%s</th>' % html.escape(c[0]) + ''.join('<td>%s</td>' % x for x in c[1:]) + '</tr>'
table += '</tbody></table>'
def label(v): return v[3:].replace('-', ' ').capitalize()
figs = ''
for v, vc in cfg['views'].items():
    p = B + 'compare-%s_%s.jpg' % (TAG, v)
    if ex(p): figs += '<figure><a href="%s"><img loading="lazy" src="%s" alt="%s: the four scenes side by side"></a><figcaption>%s · %s</figcaption></figure>\n' % (p, p, html.escape(label(v)), html.escape(vc['area']), html.escape(label(v)))
pre = ''.join('<li><strong>%s</strong>: %s</li>' % (html.escape(p['id']), html.escape(p['label'])) for p in cfg['presets'])
grp = ''.join('<li>%s</li>' % html.escape(g['label']) for g in cfg['groups'])
hero = B + 'compare-%s_19-living-from-sofa-corner.jpg' % TAG
plan = 'Claude-vectors/Hrneticka-%s-plan.png' % TAG
d = cfg['day']
import glob
ALT = {'lighting-expert': 'Lighting expert: critique of this design, with its changes', 'lighting-expert-blank': 'Lighting expert from scratch: only the light points of the electrical plan, no knowledge of the owner\'s design'}
alts = ''
for f in sorted(glob.glob(os.path.join(R, B, 'light-mixer-%s-*.html' % TAG))):
    t = os.path.basename(f)[len('light-mixer-'):-5]; k = t[len(TAG) + 1:]
    notes = 'Claude-vectors/Hrneticka-%s-notes.md' % t
    alts += '<li><strong>%s</strong> (%s): <a href="%s">light mixer</a> · <a href="%slux_table-%s.md">lux table</a> · <a href="Claude-vectors/Hrneticka-%s-plan.png">plan</a>%s</li>' % (
        html.escape(t), html.escape(ALT.get(k, k)), B + os.path.basename(f), B, t, t, (' · <a href="https://github.com/%s/blob/main/%s">notes</a>' % (REPO, notes)) if ex(notes) else '')
altsec = ('<h2>Alternative designs (%s)</h2><ul>%s</ul>' % (TAG, alts)) if alts else ''
page = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Hrnetička flat: lighting study</title>
<style>
:root{{--bg:#15171a;--panel:#1e2125;--line:#2e3238;--text:#e8e6e1;--dim:#a3a39c;--accent:#f2b561}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--text);font:16px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif}}
main{{max-width:1100px;margin:0 auto;padding:40px 20px 80px}}
h1{{font-size:30px;line-height:1.2;margin:0 0 10px;letter-spacing:-.01em}}
h2{{font-size:20px;margin:48px 0 12px}}
p{{max-width:68ch;margin:0 0 14px}}
.lede{{color:var(--dim);font-size:18px}}
a{{color:var(--accent)}}
.cta{{display:inline-block;margin:14px 0 6px;padding:12px 18px;border-radius:8px;background:var(--accent);color:#1a1205;font-weight:600;text-decoration:none}}
.cta:hover{{filter:brightness(1.08)}}
.hero img,figure img{{width:100%;height:auto;display:block;border-radius:8px;border:1px solid var(--line)}}
.hero{{margin:26px 0 0}}
.tablewrap{{overflow-x:auto;border:1px solid var(--line);border-radius:8px}}
table{{border-collapse:collapse;width:100%;min-width:560px;font-variant-numeric:tabular-nums}}
th,td{{padding:8px 12px;border-bottom:1px solid var(--line);text-align:right}}
th:first-child{{text-align:left;font-weight:500}}
thead th{{background:var(--panel);font-weight:600}}
tbody tr:last-child th,tbody tr:last-child td{{border-bottom:0}}
ul{{padding-left:20px;margin:0 0 16px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:18px}}
figure{{margin:0}}figcaption{{color:var(--dim);font-size:14px;margin-top:6px}}
.note{{color:var(--dim);font-size:14px}}
footer{{margin-top:56px;padding-top:18px;border-top:1px solid var(--line);color:var(--dim);font-size:14px}}
</style></head>
<body><main>
<h1>Hrnetička flat: lighting study</h1>
<p class="lede">Where should the wall lights go before the electrician drills? The flat is rendered with real light units and compared room by room, at night and by day.</p>
<a class="cta" href="{B}light-mixer-{TAG}.html">Open the light mixer</a>
<p class="note">The mixer switches and dims the light groups in every view. It is a large page, so give it a moment to load.</p>
<div class="hero"><a href="{hero}"><img src="{hero}" alt="Living room from the sofa corner: the four scenes"></a></div>

<h2>Light groups</h2>
<ul>{grp}</ul>
<h2>Scenes</h2>
<ul>{pre}</ul>
<p class="note">Day: {html.escape(d['place'])}, {d['date'][5:]} at {d['time']}, clear sky; sun and sky light from the real direction (plan north points to bearing {d['plan_north_bearing']}°).</p>

<h2>Light levels</h2>
<p>Median illuminance in lux on floors and furniture tops, measured in the render. Lamp strengths are assumptions except where a real product was chosen, so read the night numbers as a comparison between scenes.</p>
<div class="tablewrap">{table}</div>
<p class="note" style="margin-top:10px"><a href="{B}luxmaps-{TAG}.png">Lux maps of the whole flat</a> · <a href="{plan}">Floor plan ({TAG})</a></p>

{altsec}

<h2>Room by room</h2>
<p>Each sheet shows one camera view in the four scenes. The night pictures share one camera exposure; the day picture has its own.</p>
<div class="grid">
{figs}</div>

<h2>How it is made</h2>
<p>The flat is modelled in Sweet Home 3D, which stays the only source of truth. A script exports the model, places every lamp in Blender with its lumens, colour temperature and beam angle, adds the sun and sky for the day scene, and renders each light group with Cycles. Light adds up, so every scene is a sum of these renders. Nothing in Blender is edited by hand.</p>
<p>The scripts, the model and the full work journal are in the <a href="https://github.com/{REPO}">GitHub repository</a>.</p>
<footer>Model {TAG}, rendered {datetime.date.today():%d %B %Y}.</footer>
</main></body></html>
'''
open(os.path.join(R, 'index.html'), 'w').write(page)
missing = [v for v in cfg['views'] if not ex(B + 'compare-%s_%s.jpg' % (TAG, v))] + [p for p in (hero, plan, B + 'light-mixer-%s.html' % TAG, B + 'luxmaps-%s.png' % TAG) if not ex(p)]
print('index.html written;', 'missing: ' + ', '.join(missing) if missing else 'all links present')
