#!/usr/bin/env python3
"""Photoreal pass over Sweet Home 3D previews with Nano Banana 2 via OpenRouter.
Usage: nano_banana.py <previews_dir> <photos_dir> <out_dir> [view,view,...]
Key: OPENROUTER_API_KEY env var, else read from ~/LOCAL/CODE-2026/TamedTable/.env (never printed)."""
import base64, json, os, re, subprocess, sys, tempfile, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

MODEL = os.environ.get('NB_MODEL', 'google/gemini-3.1-flash-image')
PREV, PHOTOS, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
ONLY = sys.argv[4].split(',') if len(sys.argv) > 4 else None
os.makedirs(OUT, exist_ok=True)

def key():
    k = os.environ.get('OPENROUTER_API_KEY')
    if k:
        return k
    for line in open(os.path.expanduser('~/LOCAL/CODE-2026/TamedTable/.env')):
        m = re.match(r'\s*(?:export\s+)?OPENROUTER_API_KEY\s*=\s*["\']?([^"\'\s]+)', line)
        if m:
            return m.group(1)
    raise SystemExit('no OPENROUTER_API_KEY')
KEY = key()

def data_url(path, maxpx=1280):
    """Downscale to JPEG; sips on macOS, Pillow elsewhere."""
    import shutil, io
    if shutil.which('sips'):
        tmp = tempfile.mktemp(suffix='.jpg')
        subprocess.run(['sips', '-Z', str(maxpx), '-s', 'format', 'jpeg', '-s', 'formatOptions', '80', path, '--out', tmp],
                       check=True, capture_output=True)
        b = open(tmp, 'rb').read(); os.remove(tmp)
    else:
        from PIL import Image, ImageOps
        im = ImageOps.exif_transpose(Image.open(path)).convert('RGB'); im.thumbnail((maxpx, maxpx))
        buf = io.BytesIO(); im.save(buf, 'JPEG', quality=80); b = buf.getvalue()
    return 'data:image/jpeg;base64,' + base64.b64encode(b).decode()

COMMON = """You are given image 1: a low-quality 3D preview (Sweet Home 3D) of a new-build flat in Zagreb, Croatia, on the top (3rd) floor.
Turn image 1 into a photorealistic architectural interior/exterior photograph, as shot by a professional photographer with a full-frame camera and a wide lens, natural daylight, late afternoon.
STRICT RULES:
- Keep the exact camera position, framing, perspective and field of view of image 1.
- Keep every wall, window, door, opening and piece of furniture exactly where it is, at the same size and proportions. Do not add, remove, move or resize furniture, windows or doors. Do not add text, people or watermarks.
- You may improve materials, lighting, shadows, textures and small details so they look real; replace crude low-poly shapes with realistic versions of the same object in the same footprint.
- Windows and doors: anthracite-grey aluminium/PVC frames, as in the reference photo where given.
- Walls: warm off-white matte paint unless the preview clearly shows an accent colour.
- Indoors there is always a flat, closed, white painted ceiling 2.8 m high (the preview renders it dark and noisy; make it a normal bright white ceiling). Never show sky through an indoor ceiling.
- Remove the render noise/grain of the preview; light the room naturally with daylight from its windows.
"""
NOTES = {
    '01-living-from-kitchen': 'Open-plan kitchen + dining + living room. Floor: light Arctic-oak parquet. Kitchen: grey base units, cream upper units, oak worktop and oak backsplash. Dining table: oak, light wood chairs. Pendant lamps above the table. Corner sofa in beige fabric at the far end.',
    '02-kitchen-wall': 'Kitchen: grey base units, cream wall and tall units, oak worktop and oak backsplash, integrated fridge in a tall unit. Light Arctic-oak parquet. Oak dining table with light wood chairs and two pendant lamps.',
    '03-living-terrace-door': 'Living room: beige-fabric corner sofa with cushions in front of a large two-panel lift-and-slide door to the terrace (anthracite frame) whose frame starts 20 cm above the floor on a low sill and reaches close to the ceiling, with a roller-shutter box above. Outside: grey 60×60 stone-look terrace tiles, glass balustrade, trees and neighbouring buildings. Light Arctic-oak parquet.',
    '04-master-bedroom': 'Master bedroom: three-panel tall window (fixed - opening door - fixed) to the north balcony with a 15 cm sill, anthracite frames. Outside: balcony with grey tiles, a low parapet, and the green Sljeme hills in the distance. Bed with linen bedding, oak flooring. On the balcony: only a sunbed and a plant, exactly as in image 1; no table or bench.',
    '05-terrace-from-SE': 'Roof terrace, 46 m², grey 60×60 stone-look porcelain tiles; the beam across the top is a slim retractable shade-sail roller (aluminium, not concrete), a 60 cm grey-rendered upstand with frameless glass on top (see reference photo). Beige-rendered facade with anthracite window/door frames and a grey plinth strip. Outdoor lounge sofa with grey cushions, oval teak coffee table, outdoor dining table with chairs, planted trees in Corten planters, sunbed. Sky: clear blue with light clouds, low warm sun.',
    '06-terrace-inner-corner': 'Inner corner of the roof terrace (no beam or roof overhead apart from a slim aluminium shade-sail roller): beige-rendered facade, two narrow tall terrace doors with anthracite frames (laundry and bedroom), an outdoor sink with tap between them, a stainless/grey outdoor grill station. Grey 60×60 stone-look tiles. Match the reference photo for facade, frames and tiles. This is OUTDOORS on the terrace looking at the building facade: the open sky is above, the doors lead INTO the laundry and bedroom. Keep the sink cabinet and the grill station outside on the tiles exactly as in image 1.',
    '07-balcony-north': 'North balcony on the top floor: grey 60×60 stone-look tiles, solid rendered parapet 1 m high with a light grey metal coping and a dark grey plinth strip, a small normal-height bistro table with two outdoor chairs, a sunbed and olive trees in Corten planters. Beige-rendered facade with anthracite window frames. View north to the green Sljeme hills over Zagreb rooftops.',
    '08-hallway-from-front-door': 'Entrance hallway seen from the front door: light Arctic-oak parquet, warm off-white walls, white flush interior doors, a built-in wardrobe in the niche, an oak shoe bench with black hooks, a long corridor towards the bedrooms.',
    '09-bathroom': 'Bathroom seen from its door: tiled floor to ceiling in large-format beige stone-look porcelain tiles (see reference photo). White built-in bathtub across the back wall with a chrome shower set, white washbasin with chrome tap on the left wall, a narrow tiled pipe box between basin and bath. The bathtub and the washbasin MUST stay clearly visible in the same places as in image 1. Do not add a WC, shower glass or shower tray.',
    '10-ensuite': 'En-suite bathroom tiled floor to ceiling in large-format beige stone-look porcelain tiles (as in the reference photo): two white washbasins with chrome taps under a mirror, wall-hung WC on a tiled ledge, walk-in shower with a frameless glass panel and rain shower head. There is NO bidet and NO extra basin: the only sanitary items are the ones visible in image 1 (one wall-hung WC on a tiled ledge, one washbasin on the right, the walk-in shower on the left). Do not mirror or rearrange them.',
    '11-sara': "Teenage girl's (17) bedroom with two doors to the terrace: a narrow tall terrace door (anthracite frame) and a tall double French door (anthracite frame) on a 10 cm sill. Light oak floor, single bed with cushions against a dusty-rose accent wall, white desk with chair, wardrobe, two small tub chairs by the French door. Colourful rug.",
    '12-room5': 'Small home office / guest room: light oak floor, blue accent wall behind a grey sofa bed, desk with monitor and office chair, double window with anthracite frame, framed picture.',
}
REF = {
    '03-living-terrace-door': 'Terrace/IMG_2483.jpeg',
    '04-master-bedroom': 'Master-bedroom/IMG_2005.jpeg',
    '05-terrace-from-SE': 'Terrace/IMG_2027.jpeg',
    '06-terrace-inner-corner': 'Terrace/IMG_2483.jpeg',
    '07-balcony-north': 'Terrace/IMG_2010.jpeg',
    '09-bathroom': 'Other/IMG_2475.jpeg',
    '10-ensuite': 'Master-bedroom/IMG_2470.jpeg',
    '11-sara': 'Saras-room/IMG_2463.jpeg',
    '12-room5': 'Guest-room/IMG_2460.jpeg',
}

def run(name):
    content = [{'type': 'text', 'text': COMMON + '\nTHIS VIEW: ' + NOTES.get(name, '')},
               {'type': 'image_url', 'image_url': {'url': data_url(os.path.join(PREV, name + '.png'))}}]
    if name in REF:
        content.append({'type': 'text', 'text': 'Image 2 is a real site photo of this flat (unfinished, construction state). Use it ONLY as the reference for real materials and colours (frames, tiles, facade, railing). Keep the layout, camera and furniture of image 1.'})
        content.append({'type': 'image_url', 'image_url': {'url': data_url(os.path.join(PHOTOS, REF[name]), 1024)}})
    body = {'model': MODEL, 'modalities': ['image', 'text'],
            'messages': [{'role': 'user', 'content': content}]}
    req = urllib.request.Request('https://openrouter.ai/api/v1/chat/completions', data=json.dumps(body).encode(),
                                 headers={'Authorization': 'Bearer ' + KEY, 'Content-Type': 'application/json',
                                          'X-Title': 'S15 Hrneticka renders'})
    t0 = time.time()
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=240) as r:
                resp = json.load(r)
            msg = resp['choices'][0]['message']
            imgs = msg.get('images') or []
            if not imgs:
                raise RuntimeError('no image; text=' + str(msg.get('content'))[:200])
            url = imgs[0]['image_url']['url']
            ext = 'png' if url.startswith('data:image/png') else 'jpg'
            path = os.path.join(OUT, f'{name}.{ext}')
            open(path, 'wb').write(base64.b64decode(url.split(',', 1)[1]))
            cost = resp.get('usage', {}).get('cost')
            return f'{name}: ok {time.time() - t0:.0f}s cost={cost}'
        except Exception as e:
            err = e.read().decode()[:300] if hasattr(e, 'read') else str(e)[:300]
            last = f'{name}: attempt {attempt + 1} failed: {err}'
            time.sleep(3)
    return last

names = [n for n in sorted(NOTES) if (ONLY is None or n in ONLY) and os.path.exists(os.path.join(PREV, n + '.png'))]
with ThreadPoolExecutor(6) as ex:
    for line in ex.map(run, names):
        print(line, flush=True)
