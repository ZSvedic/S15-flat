# Measures Blender's light units: irradiance E (scene-linear) under a point/spot light of P watts at 1 m.
import bpy, math, json, sys
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.samples = 64; sc.cycles.use_denoising = False
sc.cycles.max_bounces = 0
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs[1].default_value = 0
bpy.ops.mesh.primitive_plane_add(size=0.2); pl = bpy.context.object
m = bpy.data.materials.new('d'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
d = nt.nodes.new('ShaderNodeBsdfDiffuse'); d.inputs['Color'].default_value = (0.5, 0.5, 0.5, 1)
o = nt.nodes.new('ShaderNodeOutputMaterial'); nt.links.new(d.outputs[0], o.inputs[0]); pl.data.materials.append(m)
cd = bpy.data.cameras.new('c'); cd.type = 'ORTHO'; cd.ortho_scale = 0.1; cam = bpy.data.objects.new('c', cd); sc.collection.objects.link(cam)
cam.location = (0, 0, 0.5); sc.camera = cam
sc.render.resolution_x = sc.render.resolution_y = 8
vl = sc.view_layers[0]; vl.use_pass_diffuse_direct = True
sc.render.image_settings.media_type = 'MULTI_LAYER_IMAGE'; sc.render.image_settings.file_format = 'OPEN_EXR_MULTILAYER'
res = {}
for kind in ('POINT', 'SPOT'):
    ld = bpy.data.lights.new(kind, kind); ld.energy = 10.0; ld.shadow_soft_size = 0
    if kind == 'SPOT': ld.spot_size = math.radians(60); ld.spot_blend = 0
    lo = bpy.data.objects.new(kind, ld); sc.collection.objects.link(lo); lo.location = (0, 0, 1.0)
    sc.render.filepath = '/tmp/s15_calib_' + kind + '.exr'; bpy.ops.render.render(write_still=True)
    import OpenImageIO as oiio
    inp = oiio.ImageInput.open(sc.render.filepath); parts = {}; i = 0
    while inp.seek_subimage(i, 0):
        sp = inp.spec(); parts[sp.channelnames[0].split('.')[1]] = inp.read_image(i, 0, 0, 3, 'float'); i += 1
    L = float(parts['Combined'][:, :, 0].mean()); Dd = float(parts['Diffuse Direct'][:, :, 0].mean())
    res[kind] = {'L': L, 'E_per_W': L * math.pi / 0.5 / 10.0, 'DiffDir': Dd, 'lux_from_pass': Dd * math.pi * 683, 'lux_expected': 683 * 10 / (4 * math.pi)}
    bpy.data.objects.remove(lo)
print('CALIB', json.dumps(res)); print('1/(4pi)=', 1 / (4 * math.pi), '1/(4pi^2)=', 1 / (4 * math.pi ** 2))
