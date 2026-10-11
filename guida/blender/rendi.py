"""Render dei passi della guida (D-075, docs/piano-guida.md) in Blender senza interfaccia.

    Blender -b --factory-startup -noaudio --python-exit-code 1 -P guida/blender/rendi.py -- LOTTO.json

Il lotto (scritto da guida/costruisci.py) ha la cartella delle mesh, la risoluzione e i lavori di guida/lib/scena.py.
Per ogni lavoro scrive il PNG (sfondo trasparente) e accanto un JSON con le frecce proiettate in pixel e la scala.
Stile: EEVEE con colori piatti a tre toni, contorni Freestyle (pezzi nuovi spessi e neri, pezzi gia' montati sottili e
grigi, viti medie), camera ortografica inquadrata su tutto quello che si vede, esplosi compresi.
"""
import json
import math
import os
import sys

import bmesh
import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Matrix, Vector

import numpy as np

LOTTO = json.load(open(sys.argv[sys.argv.index('--') + 1], encoding='utf-8'))
MESH = LOTTO['mesh']
MESH_CACHE, MAT_CACHE = {}, {}
# Margini delle frecce dei pezzi, in frazioni della larghezza inquadrata: stacco dai bordi e lunghezza minima (a occhio
# sulle prove F1: sotto il 6 % la punta si confonde con i contorni).
STACCO, MINIMA = 0.012, 0.06


# ------------------------------------------------------------------------------------------------ scena e stile
def stile_eevee(sc):
    sc.render.engine = 'BLENDER_EEVEE_NEXT'
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = True
    sc.view_settings.view_transform = 'Standard'
    sc.render.use_freestyle = True
    sc.render.line_thickness_mode = 'ABSOLUTE'


def scena():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    stile_eevee(sc)
    w = bpy.data.worlds.new('mondo')
    w.use_nodes = True
    w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.0
    sc.world = w
    sole = bpy.data.objects.new('sole', bpy.data.lights.new('sole', 'SUN'))
    sole.data.energy = 3.0
    sc.collection.objects.link(sole)
    cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam'))
    cam.data.type = 'ORTHO'
    cam.data.clip_end = 20000
    sc.collection.objects.link(cam)
    sc.camera = cam
    coll = {}
    for nome in ('NUOVI', 'VECCHI', 'VITI', 'ZONE'):
        c = bpy.data.collections.new(nome)
        sc.collection.children.link(c)
        coll[nome] = c
    fs = sc.view_layers[0].freestyle_settings
    fs.crease_angle = math.radians(140)
    for ls in list(fs.linesets):
        fs.linesets.remove(ls)
    for nome, spess, col in (('NUOVI', 2.8, (0, 0, 0)), ('VECCHI', 1.2, (0.55, 0.58, 0.63)), ('VITI', 1.8, (0, 0, 0))):
        ls = fs.linesets.new(nome)
        ls.select_by_collection = True
        ls.collection = coll[nome]
        ls.select_by_visibility = True
        ls.select_by_edge_types = True
        ls.select_silhouette = ls.select_border = ls.select_crease = True
        ls.linestyle.thickness = spess
        ls.linestyle.color = col
    return sc, cam, sole, coll


def materiale(rgb, attenuato=None, scuro=False):
    """Colore piatto a tre toni (diffuse -> shader to RGB -> rampa costante) moltiplicato per il colore del pezzo."""
    c = [v / 255 for v in rgb]
    if attenuato:
        t, k = [v / 255 for v in attenuato['verso']], attenuato['quanto']
        c = [c[i] * (1 - k) + t[i] * k for i in range(3)]
    if scuro:
        c = [v * 0.35 for v in c]
    chiave = tuple(round(v, 3) for v in c)
    if chiave in MAT_CACHE:
        return MAT_CACHE[chiave]
    m = bpy.data.materials.new('m%d' % len(MAT_CACHE))
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out, dif, s2r = nt.nodes.new('ShaderNodeOutputMaterial'), nt.nodes.new('ShaderNodeBsdfDiffuse'), nt.nodes.new('ShaderNodeShaderToRGB')
    rampa, mix, emis = nt.nodes.new('ShaderNodeValToRGB'), nt.nodes.new('ShaderNodeMix'), nt.nodes.new('ShaderNodeEmission')
    rampa.color_ramp.interpolation = 'CONSTANT'
    rampa.color_ramp.elements[0].position, rampa.color_ramp.elements[0].color = 0.0, (0.74, 0.74, 0.74, 1)
    rampa.color_ramp.elements[1].position, rampa.color_ramp.elements[1].color = 0.3, (0.9, 0.9, 0.9, 1)
    e = rampa.color_ramp.elements.new(0.7)
    e.color = (1.0, 1.0, 1.0, 1)
    mix.data_type, mix.blend_type = 'RGBA', 'MULTIPLY'
    mix.inputs['Factor'].default_value = 1.0
    mix.inputs[6].default_value = (*c, 1)
    nt.links.new(dif.outputs['BSDF'], s2r.inputs['Shader'])
    nt.links.new(s2r.outputs['Color'], rampa.inputs['Fac'])
    nt.links.new(rampa.outputs['Color'], mix.inputs[7])
    nt.links.new(mix.outputs[2], emis.inputs['Color'])
    nt.links.new(emis.outputs['Emission'], out.inputs['Surface'])
    MAT_CACHE[chiave] = m
    return m


def materiale_pieno(rgb):
    """Colore uniforme senza ombre (emissione), per le zone evidenziate."""
    chiave = ('pieno',) + tuple(rgb)
    if chiave in MAT_CACHE:
        return MAT_CACHE[chiave]
    m = bpy.data.materials.new('z%d' % len(MAT_CACHE))
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out, emis = nt.nodes.new('ShaderNodeOutputMaterial'), nt.nodes.new('ShaderNodeEmission')
    emis.inputs['Color'].default_value = (*[(v / 255) ** 2.2 for v in rgb], 1)
    nt.links.new(emis.outputs['Emission'], out.inputs['Surface'])
    MAT_CACHE[chiave] = m
    return m


# ------------------------------------------------------------------------------------------------ geometrie
def mesh_ply(nome):
    if nome not in MESH_CACHE:
        bpy.ops.wm.ply_import(filepath=os.path.join(MESH, nome), forward_axis='Y', up_axis='Z')
        ob = bpy.context.selected_objects[0]
        me = ob.data
        bm = bmesh.new()
        bm.from_mesh(me)
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.002)
        bm.to_mesh(me)
        bm.free()
        for p in me.polygons:
            p.use_smooth = False
        me.materials.clear()
        me.materials.append(None)
        bpy.data.objects.remove(ob)
        MESH_CACHE[nome] = me
    return MESH_CACHE[nome]


def _profilo(nome, punti, segmenti=24):
    """Solido di rivoluzione attorno a Z dal profilo [(r, z)] (r = 0 chiude gli estremi)."""
    bm = bmesh.new()
    anelli = []
    for r, z in punti:
        if r < 1e-6:
            anelli.append([bm.verts.new((0, 0, z))])
        else:
            anelli.append([bm.verts.new((r * math.cos(2 * math.pi * i / segmenti), r * math.sin(2 * math.pi * i / segmenti), z))
                           for i in range(segmenti)])
    for a, b in zip(anelli, anelli[1:]):
        if len(a) == 1 and len(b) == 1:
            continue
        for i in range(segmenti):
            j = (i + 1) % segmenti
            if len(a) == 1:
                bm.faces.new((a[0], b[i], b[j]))
            elif len(b) == 1:
                bm.faces.new((a[i], a[j], b[0]))
            else:
                bm.faces.new((a[i], a[j], b[j], b[i]))
    me = bpy.data.meshes.new(nome)
    bm.normal_update()
    bm.to_mesh(me)
    bm.free()
    me.materials.append(None)
    return me


def mesh_vite(v):
    """Vite con l'asse lungo +Z locale: l'origine e' il punto d'appoggio della testa (la faccia alta per le svasate)."""
    chiave = (v['forma'], v['d'], v['l'], v['testa_d'], v['testa_k'])
    if chiave in MESH_CACHE:
        return MESH_CACHE[chiave]
    r, R, k, L = v['d'] / 2, v['testa_d'] / 2, v['testa_k'], v['l']
    if v['forma'] == 'svasata':
        kc = R - r
        prof = [(0, 0), (R, 0), (r, kc), (r, L), (0, L)]
    elif v['forma'] == 'tonda':
        prof = [(0, -k), (R * 0.55, -k), (R * 0.9, -k * 0.55), (R, 0), (r, 0), (r, L), (0, L)]
    else:
        prof = [(0, -k), (R, -k), (R, 0), (r, 0), (r, L), (0, L)]
    MESH_CACHE[chiave] = _profilo('vite', [(a, b) for a, b in prof])
    return MESH_CACHE[chiave]


def mesh_cava(nome, r_est, r_int, alto, segmenti=32):
    """Cilindro cavo (rondella, inserto) lungo +Z da 0 ad alto."""
    bm = bmesh.new()
    giri = []
    for z in (0, alto):
        for r in (r_est, r_int):
            giri.append([bm.verts.new((r * math.cos(2 * math.pi * i / segmenti), r * math.sin(2 * math.pi * i / segmenti), z))
                         for i in range(segmenti)])
    ea, ia, eb, ib = giri
    for i in range(segmenti):
        j = (i + 1) % segmenti
        bm.faces.new((ea[i], ea[j], eb[j], eb[i]))
        bm.faces.new((ia[j], ia[i], ib[i], ib[j]))
        bm.faces.new((ea[j], ea[i], ia[i], ia[j]))
        bm.faces.new((eb[i], eb[j], ib[j], ib[i]))
    me = bpy.data.meshes.new(nome)
    bm.normal_update()
    bm.to_mesh(me)
    bm.free()
    me.materials.append(None)
    return me


def _base(asse, origine):
    z = Vector(asse).normalized()
    t = Vector((1, 0, 0)) if abs(z.x) < 0.9 else Vector((0, 1, 0))
    x = t.cross(z).normalized()
    y = z.cross(x)
    return Matrix(((x.x, y.x, z.x, origine[0]), (x.y, y.y, z.y, origine[1]), (x.z, y.z, z.z, origine[2]), (0, 0, 0, 1)))


def oggetto(nome, me, matrice, mat, coll):
    ob = bpy.data.objects.new(nome, me)
    coll.objects.link(ob)
    ob.matrix_world = matrice
    ob.material_slots[0].link = 'OBJECT'
    ob.material_slots[0].material = mat
    return ob


def matrice34(t):
    return Matrix(((t[0], t[1], t[2], t[3]), (t[4], t[5], t[6], t[7]), (t[8], t[9], t[10], t[11]), (0, 0, 0, 1)))


# ------------------------------------------------------------------------------------------------ un lavoro
def pulisci(coll):
    for c in coll.values():
        for ob in list(c.objects):
            bpy.data.objects.remove(ob)


def inquadra(sc, cam, oggetti, direzione, su, margine=1.05):
    d = Vector(direzione).normalized()
    pts = [o.matrix_world @ Vector(v) for o in oggetti for v in o.bound_box]
    centro = sum(pts, Vector()) / len(pts)
    cam.location = centro + d * 3000
    # terna della camera: X a destra, Y in alto (il "su" della vista proiettato), Z verso l'occhio
    alto = Vector(su).normalized()
    destra = alto.cross(d)
    if destra.length < 1e-6:
        destra = Vector((0, 1, 0)).cross(d)
    destra.normalize()
    alto = d.cross(destra)
    cam.rotation_euler = Matrix((destra, alto, d)).transposed().to_euler()
    bpy.context.view_layer.update()
    inv = cam.matrix_world.inverted()
    loc = [inv @ p for p in pts]
    xs, ys = [p.x for p in loc], [p.y for p in loc]
    larg, alt = max(xs) - min(xs), max(ys) - min(ys)
    W, H = sc.render.resolution_x, sc.render.resolution_y
    cam.data.ortho_scale = max(larg, alt * W / H) * margine
    cam.data.shift_x = (max(xs) + min(xs)) / 2 / cam.data.ortho_scale
    cam.data.shift_y = (max(ys) + min(ys)) / 2 / cam.data.ortho_scale
    return cam.data.ortho_scale


def _vertici_camera(cam, ob):
    """Vertici dell'oggetto nella terna della camera (x, y sul piano dell'immagine, in mm)."""
    n = len(ob.data.vertices)
    co = np.empty(n * 3)
    ob.data.vertices.foreach_get('co', co)
    m = cam.matrix_world.inverted() @ ob.matrix_world
    return co.reshape(-1, 3) @ np.array(m.to_3x3()).T + np.array(m.translation)


def _pixel(sc, cam, p):
    v = world_to_camera_view(sc, cam, p)
    return [v.x * sc.render.resolution_x, (1 - v.y) * sc.render.resolution_y]


def freccia(sc, cam, f, oggetti):
    """Freccia in pixel. Pezzi: parte dal bordo d'attacco del pezzo esploso e arriva dove quel bordo va a finire.
    Viti e inserti: dalla punta esplosa all'imbocco del foro. Sempre con uno stacco, mai piu' corta della minima."""
    inv = cam.matrix_world.inverted()
    pa, pb = inv @ Vector(f['da']), inv @ Vector(f['a'])
    u = Vector((pb.x - pa.x, pb.y - pa.y))
    lung = u.length
    if lung < 1e-6:
        return None
    u.normalize()
    scala = cam.data.ortho_scale
    stacco, minima = STACCO * scala, MINIMA * scala
    obs = [oggetti[k] for k in f.get('chiavi', []) if k in oggetti]
    if f['tipo'] == 'pezzo' and obs:
        xy = np.concatenate([_vertici_camera(cam, ob)[:, :2] for ob in obs])
        avanti = float(((xy - np.array([pa.x, pa.y])) @ np.array([u.x, u.y])).max())
        inizio = Vector((pa.x, pa.y)) + u * (avanti + stacco)
        fine = Vector((pa.x, pa.y)) + u * (avanti + lung - stacco)
    else:
        inizio = Vector((pa.x, pa.y)) + u * stacco
        fine = Vector((pb.x, pb.y)) - u * stacco
    if (fine - inizio).length < minima:
        fine = inizio + u * minima
    mondo = [cam.matrix_world @ Vector((q.x, q.y, pa.z)) for q in (inizio, fine)]
    scorcio = lung / max((Vector(f['a']) - Vector(f['da'])).length, 1e-6)
    return {'da': _pixel(sc, cam, mondo[0]), 'a': _pixel(sc, cam, mondo[1]), 'tipo': f['tipo'], 'scorcio': round(scorcio, 3)}


def visibili(sc, gruppi, uscita):
    """Pixel visibili di ogni oggetto nuovo: passata Workbench senza contorni, un colore piatto per oggetto (valori
    0 / 0,5 / 1 per canale, 26 colori) e tutto il resto nero. Torna {nome: pixel alla risoluzione piena}."""
    livelli = (0.0, 0.5, 1.0)
    colori = [(r, g, b) for r in livelli for g in livelli for b in livelli if (r, g, b) != (0, 0, 0)]
    for ob in sc.objects:
        if ob.type == 'MESH':
            ob.color = (0, 0, 0, 1)
    nomi = {}
    for i, (nome, obs) in enumerate(gruppi.items()):
        if i >= len(colori):
            break
        for ob in obs:
            ob.color = (*colori[i], 1)
        nomi[tuple(round(c * 255) for c in colori[i])] = nome
    sc.render.engine = 'BLENDER_WORKBENCH'
    sc.display.shading.light = 'FLAT'
    sc.display.shading.color_type = 'OBJECT'
    sc.display.render_aa = 'OFF'
    sc.render.use_freestyle = False
    sc.view_settings.view_transform = 'Raw'
    sc.render.resolution_percentage = 25
    sc.render.filepath = uscita
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(uscita)
    px = np.empty(im.size[0] * im.size[1] * 4, dtype=np.float32)
    im.pixels.foreach_get(px)
    bpy.data.images.remove(im)
    os.remove(uscita)
    px = np.rint(px.reshape(-1, 4)[:, :3] * 2) * 127.5
    conta = {n: 0 for n in gruppi}
    chiavi, numeri = np.unique(np.rint(px).astype(int), axis=0, return_counts=True)
    for c, n in zip(chiavi, numeri):
        nome = nomi.get(tuple(int(round(v)) for v in c))
        if nome:
            conta[nome] += int(n) * 16
    stile_eevee(sc)
    return conta


def rendi(sc, cam, sole, coll, lav):
    pulisci(coll)
    sc.render.resolution_x, sc.render.resolution_y = lav['risoluzione']
    att = lav['attenuato']
    oggetti, per_nome, gruppi = [], {}, {}
    d = Vector(lav['camera']['direzione']).normalized()
    for o in lav['oggetti']:
        if o['ruolo'] == 'zona':                    # facce di una lavorazione: colore pieno, senza contorni,
            m = matrice34(o['matrice'])             # appena verso la camera per non mescolarsi con la faccia sotto
            m.translation = m.translation + d * 0.15
            oggetti.append(oggetto(o['chiave'], mesh_ply(o['mesh']), m, materiale_pieno(o['colore']), coll['ZONE']))
            continue
        nuovo = o['ruolo'] == 'nuovo'
        ob = oggetto(o['chiave'], mesh_ply(o['mesh']), matrice34(o['matrice']),
                     materiale(o['colore'], None if nuovo else att), coll['NUOVI' if nuovo else 'VECCHI'])
        oggetti.append(ob)
        per_nome[o['chiave']] = ob
        if nuovo:
            gruppi[o['chiave']] = [ob]
    for i, v in enumerate(lav['viti']):
        ob = oggetto('vite%d' % i, mesh_vite(v), _base(v['asse'], v['testa']), materiale(lav['colori']['viti']), coll['VITI'])
        oggetti.append(ob)
        gruppi['vite%d' % i] = [ob]
        for j, r in enumerate(v['rondelle']):
            me = MESH_CACHE.setdefault('rondella', mesh_cava('rondella', 3.5, 1.6, 0.5))
            c = Vector(r['centro']) - Vector(r['asse']).normalized() * 0.25
            oggetti.append(oggetto('rondella%d_%d' % (i, j), me, _base(r['asse'], c), materiale(lav['colori']['rondelle']), coll['VITI']))
    for i, s in enumerate(lav['inserti']):
        me = MESH_CACHE.setdefault(('inserto', s['d'], s['l']), mesh_cava('inserto', s['d'] / 2 + 0.2, s['d'] / 2 - 0.6, s['l']))
        ob = oggetto('inserto%d' % i, me, _base(s['asse'], s['centro']), materiale(lav['colori']['inserti']), coll['VITI'])
        oggetti.append(ob)
        gruppi['inserto%d' % i] = [ob]
    sole.rotation_euler = (d + Vector((0.3, -0.4, 0.6))).normalized().to_track_quat('Z', 'Y').to_euler()
    scala = inquadra(sc, cam, oggetti, lav['camera']['direzione'], lav['camera'].get('su', [0, 0, 1]))
    sc.render.filepath = lav['uscita']
    bpy.ops.render.render(write_still=True)
    frecce = [x for x in (freccia(sc, cam, f, per_nome) for f in lav['frecce']) if x]
    vis = visibili(sc, gruppi, os.path.splitext(lav['uscita'])[0] + '_id.png') if lav.get('verifica', True) else {}
    W, H = lav['risoluzione']
    with open(os.path.splitext(lav['uscita'])[0] + '.json', 'w', encoding='utf-8') as fp:
        json.dump({'id': lav['id'], 'larghezza': W, 'altezza': H, 'mm_per_pixel': scala / W, 'frecce': frecce,
                   'visibili': vis}, fp)


sc, cam, sole, coll = scena()
for lav in LOTTO['lavori']:
    rendi(sc, cam, sole, coll, lav)
    print('SCRITTO', lav['uscita'], flush=True)
