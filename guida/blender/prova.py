"""Prova di fattibilita' (F0, docs/piano-guida.md): pezzi della coxa nello stile delle istruzioni, con il servo del
femore nuovo ed esploso. Uso:
    Blender -b --factory-startup -noaudio --python-exit-code 1 -P guida/blender/prova.py -- MANIFEST MESH USCITA.png
"""
import json
import os
import sys

import bpy
from mathutils import Matrix, Vector

arg = sys.argv[sys.argv.index('--') + 1:]
MANIFEST, MESH, USCITA = arg[0], arg[1], arg[2]
PASSO = {
    'vecchi': ['zampa/Coxa', 'zampa/Coxa_Ponte', 'zampa/Squadretta_coxa', 'zampa/Perno_coxa', 'zampa/Cuscinetto_femore'],
    'nuovi': ['zampa/Servo_femore'],
    'esploso': {'zampa/Servo_femore': (0, 45, 0)},
    'vista': (0.72, 0.58, 0.36),
}
SCHIARISCI = {'Esa PETG-CF nero': (78, 82, 90)}      # nero su nero non si legge: il PETG-CF si schiarisce


def pulisci():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def materiale(nome, rgb, attenuato):
    m = bpy.data.materials.new(nome)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    dif = nt.nodes.new('ShaderNodeBsdfDiffuse')
    s2r = nt.nodes.new('ShaderNodeShaderToRGB')
    rampa = nt.nodes.new('ShaderNodeValToRGB')
    mix = nt.nodes.new('ShaderNodeMix')
    mix.data_type = 'RGBA'
    emis = nt.nodes.new('ShaderNodeEmission')
    c = [v / 255 for v in rgb]
    if attenuato:
        c = [v * 0.35 + 0.95 * 0.65 for v in c]
    dif.inputs['Color'].default_value = (1, 1, 1, 1)
    rampa.color_ramp.interpolation = 'CONSTANT'
    rampa.color_ramp.elements[0].position = 0.0
    rampa.color_ramp.elements[0].color = (0.72, 0.72, 0.72, 1)
    rampa.color_ramp.elements[1].position = 0.35
    rampa.color_ramp.elements[1].color = (1, 1, 1, 1)
    e = rampa.color_ramp.elements.new(0.75)
    e.color = (1.12, 1.12, 1.12, 1)
    mix.blend_type = 'MULTIPLY'
    mix.inputs['Factor'].default_value = 1.0
    mix.inputs[6].default_value = (*c, 1)
    nt.links.new(dif.outputs['BSDF'], s2r.inputs['Shader'])
    nt.links.new(s2r.outputs['Color'], rampa.inputs['Fac'])
    nt.links.new(rampa.outputs['Color'], mix.inputs[7])
    nt.links.new(mix.outputs[2], emis.inputs['Color'])
    nt.links.new(emis.outputs['Emission'], out.inputs['Surface'])
    return m


def carica(man, chiave, attenuato, coll):
    occ = next(o for o in man['occorrenze'] if o['chiave'] == chiave)
    comp = man['componenti'][occ['componente']]
    bpy.ops.wm.ply_import(filepath=os.path.join(MESH, comp['mesh']), forward_axis='Y', up_axis='Z')
    ob = bpy.context.selected_objects[0]
    ob.name = chiave
    for c in ob.users_collection:
        c.objects.unlink(ob)
    coll.objects.link(ob)
    nome_asp, rgb = comp['aspetti'][0]
    rgb = SCHIARISCI.get(nome_asp, rgb)
    ob.data.materials.clear()
    ob.data.materials.append(materiale(chiave, rgb, attenuato))
    t = occ['T']
    m = Matrix(((t[0], t[1], t[2], t[3]), (t[4], t[5], t[6], t[7]), (t[8], t[9], t[10], t[11]), (0, 0, 0, 1)))
    d = PASSO['esploso'].get(chiave)
    if d:
        m = Matrix.Translation(Vector(d)) @ m
    ob.matrix_world = m
    bpy.ops.object.select_all(action='DESELECT')
    ob.select_set(True)
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.shade_flat()
    return ob


def scena():
    sc = bpy.context.scene
    sc.render.engine = 'BLENDER_EEVEE_NEXT'
    sc.render.resolution_x, sc.render.resolution_y = 1800, 1250
    sc.render.film_transparent = True
    sc.view_settings.view_transform = 'Standard'
    sc.render.use_freestyle = True
    sc.render.line_thickness_mode = 'ABSOLUTE'
    w = bpy.data.worlds.new('mondo')
    w.use_nodes = True
    w.node_tree.nodes['Background'].inputs['Color'].default_value = (1, 1, 1, 1)
    w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.0
    sc.world = w
    sole = bpy.data.objects.new('sole', bpy.data.lights.new('sole', 'SUN'))
    sole.data.energy = 3.0
    sole.rotation_euler = (0.9, 0.2, -0.6)
    sc.collection.objects.link(sole)
    return sc


def linee(sc, coll_nuovi, coll_vecchi):
    fs = sc.view_layers[0].freestyle_settings
    fs.crease_angle = 2.44
    for ls in list(fs.linesets):
        fs.linesets.remove(ls)
    for nome, coll, spess, col in (('NUOVI', coll_nuovi, 2.6, (0, 0, 0)), ('VECCHI', coll_vecchi, 1.3, (0.42, 0.45, 0.5))):
        ls = fs.linesets.new(nome)
        ls.select_by_collection = True
        ls.collection = coll
        ls.select_by_visibility = True
        ls.select_by_edge_types = True
        ls.select_silhouette = ls.select_border = ls.select_crease = True
        ls.linestyle.thickness = spess
        ls.linestyle.color = col


def camera(sc, oggetti, direzione):
    d = Vector(direzione).normalized()
    cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam'))
    cam.data.type = 'ORTHO'
    sc.collection.objects.link(cam)
    sc.camera = cam
    pts = [o.matrix_world @ Vector(v) for o in oggetti for v in o.bound_box]
    centro = sum(pts, Vector()) / len(pts)
    cam.location = centro + d * 1000
    cam.rotation_euler = (-d).to_track_quat('-Z', 'Z').to_euler()
    cam.data.clip_end = 5000
    bpy.context.view_layer.update()
    inv = cam.matrix_world.inverted()
    loc = [inv @ p for p in pts]
    xs, ys = [p.x for p in loc], [p.y for p in loc]
    larg, alt = max(xs) - min(xs), max(ys) - min(ys)
    asp = sc.render.resolution_x / sc.render.resolution_y
    cam.data.ortho_scale = max(larg, alt * asp) * 1.12
    cam.data.shift_x = (max(xs) + min(xs)) / 2 / cam.data.ortho_scale
    cam.data.shift_y = (max(ys) + min(ys)) / 2 / cam.data.ortho_scale


pulisci()
man = json.load(open(MANIFEST, encoding='utf-8'))
sc = scena()
cn = bpy.data.collections.new('NUOVI')
cv = bpy.data.collections.new('VECCHI')
sc.collection.children.link(cn)
sc.collection.children.link(cv)
ogg = [carica(man, k, True, cv) for k in PASSO['vecchi']] + [carica(man, k, False, cn) for k in PASSO['nuovi']]
linee(sc, cn, cv)
camera(sc, ogg, PASSO['vista'])
sc.render.filepath = USCITA
bpy.ops.render.render(write_still=True)
print('SCRITTO', USCITA)
