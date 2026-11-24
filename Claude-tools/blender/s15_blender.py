# S15 lighting scene for Blender (Cycles). Rebuilt from the Sweet Home 3D export every time; never edit the .blend by hand.
# One render per light group and view (linear, denoised). Light is additive, so mix.py and the HTML mixer build any on/off
# combination by summing these renders.
# Usage: Blender -b -P s15_blender.py -- <src dir> <obj subdir> <outdir> W H samples [views, comma] [groups, comma]
#   src dir holds lights.json (make_lights.py), groups.json (lamp data, groups, views) and cams.txt
#   output: <outdir>/<group>/<view>.npy (float16 RGB, scene-linear) and for the top view also <view>_lux.npy. Existing files are skipped.
import bpy, sys, json, math, os, time, functools
from mathutils import Vector
print = functools.partial(print, flush=True)
argv = sys.argv[sys.argv.index('--') + 1:]
SRC, OBJ, OUT = argv[0], argv[1], argv[2]
W, H, SAMPLES = int(argv[3]), int(argv[4]), int(argv[5])
ONLYV = argv[6].split(',') if len(argv) > 6 and argv[6] != '-' else None
ONLYG = argv[7].split(',') if len(argv) > 7 else None
K = 683.0                      # lm/W convention; cancels out in lux results (measured: E = P / (4 pi d^2), see calib.py)
def P3(x, y, z): return Vector((x / 100.0, -y / 100.0, z / 100.0))     # model cm (x, y south, elevation) -> Blender m

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
bpy.ops.wm.obj_import(filepath=os.path.join(SRC, OBJ, 's15.obj'), forward_axis='NEGATIVE_Z', up_axis='Y', global_scale=0.01, use_split_groups=True)
print('S15 imported objects:', len(bpy.data.objects))
lights = json.load(open(os.path.join(SRC, 'lights.json')))
cfg = json.load(open(os.path.join(SRC, 'groups.json')))

lp = [P3(l['x'], l['y'], l['z']) for l in lights]; n = 0
for o in list(bpy.data.objects):                       # SH3D's light-source marker meshes would swallow the light
    if o.type == 'MESH' and max(o.dimensions) < 0.06:
        c = sum((o.matrix_world @ Vector(b) for b in o.bound_box), Vector()) / 8
        if any((c - p).length < 0.08 for p in lp): bpy.data.objects.remove(o); n += 1
print('S15 removed light markers:', n)
lights = [l for l in lights if l['set'] != 'other']          # mirror, terrace and desk lamps are not part of the comparison

g = 0                                                  # window glass: SH3D exports half-transparent grey; make it real glass
for m in bpy.data.materials:
    if not m.use_nodes: continue
    b = m.node_tree.nodes.get('Principled BSDF')
    if b and b.inputs['Alpha'].default_value < 0.9 and not b.inputs['Base Color'].is_linked:
        b.inputs['Alpha'].default_value = 1.0; b.inputs['Base Color'].default_value = (1, 1, 1, 1)
        b.inputs['Roughness'].default_value = 0.0; b.inputs['Transmission Weight'].default_value = 1.0; b.inputs['IOR'].default_value = 1.0
        b.inputs['Specular IOR Level'].default_value = 0.5; g += 1
print('S15 glass materials:', g)
mm = bpy.data.materials.new('S15 mirror'); mm.use_nodes = True; mb = mm.node_tree.nodes['Principled BSDF']         # real mirrors (points in groups.json)
mb.inputs['Metallic'].default_value = 1.0; mb.inputs['Roughness'].default_value = 0.02; mb.inputs['Base Color'].default_value = (0.92, 0.92, 0.92, 1); n = 0
for o in bpy.data.objects:
    if o.type == 'MESH' and 'window_mirror' in o.name and not o.name.split('window_mirror')[1].startswith('_1_'):
        c = sum((o.matrix_world @ Vector(b) for b in o.bound_box), Vector()) / 8
        if any((c - P3(*p)).length < 0.3 for p in cfg.get('mirrors', [])):
            for sl in o.material_slots: sl.material = mm
            n += 1
print('S15 mirrors:', n)

col = bpy.data.collections.new('Lights'); sc.collection.children.link(col)
objs = []; flux = {}
def add(l, tag, kind, energy, cone=None, blend=None):
    lamp = cfg['lamps'][l['role']]
    ld = bpy.data.lights.new(l['name'][:40], kind); o = bpy.data.objects.new('%s %s' % (tag, l['name'][:50]), ld); col.objects.link(o)
    o.location = P3(l['x'], l['y'], l['z'])
    d = Vector((l['dir'][0], -l['dir'][1], l['dir'][2])); o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    ld.energy = energy; ld.shadow_soft_size = lamp['radius'] / 100.0
    if cone: ld.spot_size = math.radians(cone); ld.spot_blend = blend
    try: ld.use_temperature = True; ld.temperature = lamp['kelvin']
    except Exception: pass
    objs.append((l['set'], o))
for i, l in enumerate(lights):
    lamp = cfg['lamps'][l['role']]
    if 'profile' in lamp:          # sum of soft cones: peak candela I over a full cone angle, falling smoothly to zero at the edge (blend 1)
        lm = 0
        for j, (cd, cone) in enumerate(lamp['profile']):
            add(l, '%03d.%d' % (i, j), 'SPOT', cd * 4 * math.pi / K, cone, 1.0); lm += cd * 2 * math.pi * (1 - math.cos(math.radians(cone) / 2)) * 0.5
    elif lamp['beam']:             # beam angle = half-intensity cone
        beam = lamp['beam']; size = min(beam * 1.25, 179); omega = 2 * math.pi * (1 - math.cos(math.radians(beam) / 2))
        cd = min(lamp['lumens'] / omega, lamp['lumens'] / (0.55 * 2 * math.pi * (1 - math.cos(math.radians(size) / 2))))
        add(l, '%03d' % i, 'SPOT', cd * 4 * math.pi / K, size, 0.45); lm = lamp['lumens']
    else:
        add(l, '%03d' % i, 'POINT', lamp['lumens'] / K); lm = lamp['lumens']
    flux[l['set']] = flux.get(l['set'], 0) + lm
print('S15 lumens per group:', json.dumps({k: round(v) for k, v in flux.items()}))
os.makedirs(OUT, exist_ok=True); json.dump({k: round(v) for k, v in flux.items()}, open(os.path.join(OUT, 'lumens.json'), 'w'))

w = bpy.data.worlds.new('night'); sc.world = w; w.use_nodes = True
bg = w.node_tree.nodes['Background']; bg.inputs[0].default_value = (0.05, 0.07, 0.12, 1); bg.inputs[1].default_value = 0.0      # black outside: group renders must add up exactly
sc.render.engine = 'CYCLES'
try:
    pr = bpy.context.preferences.addons['cycles'].preferences; pr.compute_device_type = 'METAL'; pr.get_devices()
    for d in pr.devices: d.use = (d.type == 'METAL')
    sc.cycles.device = 'GPU'
except Exception as e: print('S15 GPU setup failed, using CPU:', e)
sc.cycles.use_denoising = True; sc.cycles.max_bounces = 8; sc.cycles.diffuse_bounces = 6; sc.cycles.transmission_bounces = 8
vl = sc.view_layers[0]; vl.use_pass_diffuse_direct = True; vl.use_pass_diffuse_indirect = True
im = sc.render.image_settings
if hasattr(im, 'media_type'): im.media_type = 'MULTI_LAYER_IMAGE'      # Blender 5+
im.file_format = 'OPEN_EXR_MULTILAYER'; im.color_depth = '32'

cams = {}
for line in open(os.path.join(SRC, 'cams.txt')):
    t = line.split()
    if t and not line.startswith('#'): cams[t[0]] = [float(x) for x in t[1:7]]
camobj = {}
def set_cam(name):
    if name not in camobj:
        cd = bpy.data.cameras.new(name); o = bpy.data.objects.new(name, cd); sc.collection.objects.link(o); camobj[name] = o
        if name.startswith('TOP:'):
            x0, y0, x1, y1 = [float(v) for v in name[4:].split(',')]
            cd.type = 'ORTHO'; cd.ortho_scale = max(x1 - x0, y1 - y0) / 100.0; cd.clip_start = 0.01
            o.location = P3((x0 + x1) / 2, (y0 + y1) / 2, 255)                  # below the ceiling and its lamps
        else:
            x, y, z, yaw, pitch, fov = cams[name]; yaw, pitch = math.radians(yaw), math.radians(pitch)
            d = Vector((-math.sin(yaw) * math.cos(pitch), -math.cos(yaw) * math.cos(pitch), -math.sin(pitch)))
            o.location = P3(x, y, z); o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
            cd.sensor_fit = 'HORIZONTAL'; cd.angle = math.radians(fov); cd.clip_start = 0.05
    sc.camera = camobj[name]
    if name.startswith('TOP:'):
        x0, y0, x1, y1 = [float(v) for v in name[4:].split(',')]
        sc.render.resolution_x = int((x1 - x0) / 2); sc.render.resolution_y = int((y1 - y0) / 2); sc.cycles.samples = SAMPLES * 2
    else:
        sc.render.resolution_x, sc.render.resolution_y = W, H; sc.cycles.samples = SAMPLES

import OpenImageIO as oiio, numpy as np
jobs = [(v, cfg['sets'][s]) for v, s in cfg['views'].items()] + [(cfg['top'], [g['id'] for g in cfg['groups']])]
todo = [(v, g) for v, gs in jobs for g in gs if (not ONLYV or v in ONLYV or (v.startswith('TOP') and 'TOP' in ONLYV)) and (not ONLYG or g in ONLYG)]
print('S15 renders to do:', len(todo)); done = 0
for view, grp in todo:
    safe = view.replace(':', '_').replace(',', '_'); out = os.path.join(OUT, grp); os.makedirs(out, exist_ok=True)
    npy = os.path.join(out, safe + '.npy'); done += 1
    if os.path.exists(npy): continue
    for st, o in objs: o.hide_render = (st != grp)
    set_cam(view); exr = os.path.join(out, safe + '.exr'); sc.render.filepath = exr
    t0 = time.time(); bpy.ops.render.render(write_still=True); dt = time.time() - t0
    inp = oiio.ImageInput.open(exr); parts = {}; i = 0
    while inp.seek_subimage(i, 0):
        sp = inp.spec(); parts[sp.channelnames[0].split('.')[1]] = inp.read_image(i, 0, 0, 3, 'float'); i += 1
    inp.close()
    if view.startswith('TOP'):
        def ch(p): return sum(c * parts[p][:, :, j] for j, c in enumerate((0.2126, 0.7152, 0.0722)))
        lux = (ch('Diffuse Direct') + ch('Diffuse Indirect')) * math.pi * K          # these passes are irradiance / pi
        np.save(os.path.join(out, safe + '_lux.npy'), lux.astype('float32'))
    np.save(npy + '.tmp.npy', np.clip(parts['Combined'], 0, 60000).astype('float16')); os.replace(npy + '.tmp.npy', npy); os.remove(exr)
    print('S15 rendered %d/%d' % (done, len(todo)), grp, view, 'in', round(dt), 's')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, 's15.blend'))
print('S15 done')
