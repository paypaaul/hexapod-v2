"""Ingombri semplificati dei componenti acquistati (fase 3).

Si esegue dentro Fusion sul design "Hexapod v2 - Assieme":
    import runpy; runpy.run_path('<repo>/cad/script/rif_componenti.py')['main']()

Le quote vengono lette dai parametri utente del design: per aggiornare un ingombro
si cambia il parametro e si rilancia lo script con rigenera=True (cancella e ricrea
i componenti "Rif_*" generati qui; non tocca servo e STEP Pololu).

Ogni ingombro e' un corpo in una BaseFeature (nessuno schizzo): sono parti comprate,
non progettate. Le quote che contano (fori, connettori, ingombri liberi) sono fedeli
a docs/dimensioni-componenti.md; il resto e' indicativo.
Unita' nello script: mm (convertiti in cm per l'API).
"""
import json
import math
import traceback

import adsk.core
import adsk.fusion

P3 = adsk.core.Point3D.create
V3 = adsk.core.Vector3D.create
GENERATI = ('Rif_SSC32_V25', 'Rif_ESP32_S3_CAM', 'Rif_Camera_OV3660_75', 'Rif_Batteria_2S2200',
            'Rif_Cuscinetto_F683ZZ', 'Rif_Perno_3x10', 'Rif_Interruttore_2813',
            'Rif_Condensatore_2200uF', 'Rif_Cicalino_BX100', 'Rif_Basetta_50x70')


def _tmp():
    return adsk.fusion.TemporaryBRepManager.get()


def box(cx, cy, z0, lx, ly, lz):
    """Parallelepipedo: centro (cx, cy) in pianta, base a z0, dimensioni lx, ly, lz (mm)."""
    obb = adsk.core.OrientedBoundingBox3D.create(
        P3(cx / 10, cy / 10, (z0 + lz / 2) / 10), V3(1, 0, 0), V3(0, 1, 0), lx / 10, ly / 10, lz / 10)
    return _tmp().createBox(obb)


def cyl(cx, cy, z0, d, h, asse='z'):
    """Cilindro di diametro d e altezza h con base in (cx, cy, z0), lungo l'asse dato."""
    a = P3(cx / 10, cy / 10, z0 / 10)
    if asse == 'z':
        b = P3(cx / 10, cy / 10, (z0 + h) / 10)
    elif asse == 'x':
        b = P3((cx + h) / 10, cy / 10, z0 / 10)
    else:
        b = P3(cx / 10, (cy + h) / 10, z0 / 10)
    return _tmp().createCylinderOrCone(a, d / 20, b, d / 20)


def unisci(a, b):
    _tmp().booleanOperation(a, b, adsk.fusion.BooleanTypes.UnionBooleanType)
    return a


def sottrai(a, b):
    _tmp().booleanOperation(a, b, adsk.fusion.BooleanTypes.DifferenceBooleanType)
    return a


def componente(root, nome, corpi, pos_mm):
    """Crea un componente con i corpi dati [(nome, brep)], in una sola BaseFeature."""
    t = adsk.core.Matrix3D.create()
    t.translation = V3(pos_mm[0] / 10, pos_mm[1] / 10, pos_mm[2] / 10)
    occ = root.occurrences.addNewComponent(t)
    comp = occ.component
    comp.name = nome
    bf = comp.features.baseFeatures.add()
    bf.name = 'Ingombro'
    bf.startEdit()
    for nome_corpo, brep in corpi:
        b = comp.bRepBodies.add(brep, bf)
        b.name = nome_corpo
    bf.finishEdit()
    return occ


def main(rigenera=False):
    out = {}
    try:
        app = adsk.core.Application.get()
        des = adsk.fusion.Design.cast(app.activeProduct)
        root = des.rootComponent

        def p(nome):
            """Valore in mm di un parametro utente di lunghezza."""
            return des.userParameters.itemByName(nome).value * 10.0

        esistenti = {o.component.name: o for o in root.occurrences}
        if rigenera:
            for n in GENERATI:
                if n in esistenti:
                    esistenti[n].deleteMe()
        else:
            gia = [n for n in GENERATI if n in esistenti]
            if gia:
                out['errore'] = 'componenti gia presenti: %s (usare rigenera=True)' % gia
                print(json.dumps(out))
                return

        fatti = {}

        # ---------------- SSC32-V2.5 (X = lato lungo, origine al centro, sotto del PCB a z = 0)
        L, W = p('ssc_l'), p('ssc_w')
        fx, fy, fd = p('ssc_fori_x') / 2, p('ssc_fori_y') / 2, p('ssc_fori_d')
        sp = 1.6
        pcb = box(0, 0, 0, L, W, sp)
        for sx in (-1, 1):
            for sy in (-1, 1):
                sottrai(pcb, cyl(sx * fx, sy * fy, -1, fd, sp + 2))
        # header servo: 4 gruppi da 4 canali x 3 pin per lato (passo 2,54), alti 8,5 sul PCB
        hdr = None
        for sy in (1, -1):
            for cx in (-20.3, -7.2, 6.0, 19.2):
                b = box(cx, sy * (W / 2 - 4.0), sp, 10.2, 7.7, 8.5)
                hdr = b if hdr is None else unisci(hdr, b)
        mors = box(L / 2 - 6.6, 0.0, sp, 7.0, 21.5, 8.5)          # morsettiera 6 poli passo 3,5
        ser = box(14.3, 3.2, sp, 7.7, 18.0, 8.5)                   # RX TX GND + ICSP + ABCD
        usb = box(-L / 2 + 2.0, -12.5, sp, 5.6, 7.5, 2.7)          # micro-USB, sporge 0,8 dal bordo
        xb = unisci(box(-25.7, 15.1, sp, 20.0, 2.0, 4.5), box(-25.7, -5.8, sp, 20.0, 2.0, 4.5))
        cap = unisci(cyl(22.3, 10.7, sp, 6.3, 7.7), cyl(22.3, 2.6, sp, 6.3, 7.7))
        alt = p('ssc_alt_libera')
        zona = unisci(box(0, W / 2 - 4.0, sp, 56.0, 8.0, alt), box(0, -(W / 2 - 4.0), sp, 56.0, 8.0, alt))
        fatti['Rif_SSC32_V25'] = componente(root, 'Rif_SSC32_V25', [
            ('pcb', pcb), ('header_servo', hdr), ('morsettiera', mors), ('header_seriale', ser),
            ('micro_usb', usb), ('zoccolo_xbee', xb), ('condensatori', cap), ('zona_spine_servo', zona)],
            (0, 300, 0))

        # ---------------- ESP32-S3-CAM (X = lunghezza, antenna a +X, USB a -X, sotto del PCB a z = 0)
        L, W, sp = p('esp_l'), p('esp_w'), p('esp_sp')
        pcb = box(0, 0, 0, L, W, sp)
        ant = p('esp_antenna')
        modulo = box(L / 2 + ant - 25.5 / 2, 0, sp, 25.5, 18.0, 3.2)
        usbc = unisci(box(-L / 2 + 2.7, 6.6, sp, 7.35, 8.94, 3.26), box(-L / 2 + 2.7, -6.6, sp, 7.35, 8.94, 3.26))
        fpc = box(-2.0, 0, sp, 4.5, 14.5, 2.0)
        fr = p('esp_file') / 2
        pin = unisci(box(2.9, fr, -8.5, 50.8, 2.54, 8.5), box(2.9, -fr, -8.5, 50.8, 2.54, 8.5))
        tf = box(-15.0, 0, -1.9, 15.0, 14.0, 1.9)
        fatti['Rif_ESP32_S3_CAM'] = componente(root, 'Rif_ESP32_S3_CAM', [
            ('pcb', pcb), ('modulo_antenna', modulo), ('usb_c', usbc), ('connettore_fpc', fpc),
            ('pin_header', pin), ('slot_tf', tf)], (100, 300, 0))

        # ---------------- Camera OV3660-75MM (flat nel piano XY, asse ottico +Z, origine sull'asse, retro della testa)
        t, h, ld = p('cam_testa'), p('cam_alt'), p('cam_lente_d')
        testa = unisci(box(0, 0, 0, t, t, h * 0.55), cyl(0, 0, h * 0.55, ld, h * 0.45))
        lung_flat = p('cam_flat_l') - t - p('cam_ling_l')
        flat = box(-t / 2 - lung_flat / 2, 0, 0, lung_flat, p('cam_flat_w'), 0.15)
        ling = box(-t / 2 - lung_flat - p('cam_ling_l') / 2, 0, 0, p('cam_ling_l'), p('cam_ling_w'), 0.3)
        fatti['Rif_Camera_OV3660_75'] = componente(root, 'Rif_Camera_OV3660_75', [
            ('testa', testa), ('flat', flat), ('linguetta', ling)], (200, 300, 0))

        # ---------------- Batteria 2S 2200 (origine al centro, fondo a z = 0, cavi a +X)
        bl, bw, bh = p('bat_l'), p('bat_w'), p('bat_h')
        pacco = box(0, 0, 0, bl, bw, bh)
        cavi = box(bl / 2 + 10, 0, bh / 2 - 3, 20, 14, 6)
        fatti['Rif_Batteria_2S2200'] = componente(root, 'Rif_Batteria_2S2200', [
            ('pacco', pacco), ('uscita_cavi', cavi)], (0, 400, 0))

        # ---------------- Cuscinetto F683ZZ (asse Z, origine al centro della faccia lato flangia)
        cus = unisci(cyl(0, 0, 0, p('cus_D'), p('cus_B')), cyl(0, 0, 0, p('cus_flangia_d'), p('cus_flangia_sp')))
        sottrai(cus, cyl(0, 0, -1, p('cus_d'), p('cus_B') + 2))
        fatti['Rif_Cuscinetto_F683ZZ'] = componente(root, 'Rif_Cuscinetto_F683ZZ', [('cuscinetto', cus)], (120, 400, 0))

        # ---------------- Perno
        fatti['Rif_Perno_3x10'] = componente(root, 'Rif_Perno_3x10', [('perno', cyl(0, 0, 0, p('perno_d'), p('perno_l')))], (140, 400, 0))

        # ---------------- Interruttore Pololu #2813, condensatore, cicalino, basetta
        fatti['Rif_Interruttore_2813'] = componente(root, 'Rif_Interruttore_2813', [('scheda', box(0, 0, 0, 25.4, 20.3, 4.1))], (170, 400, 0))
        fatti['Rif_Condensatore_2200uF'] = componente(root, 'Rif_Condensatore_2200uF', [('condensatore', cyl(0, 0, 0, 12.5, 20.0))], (200, 400, 0))
        fatti['Rif_Cicalino_BX100'] = componente(root, 'Rif_Cicalino_BX100', [('cicalino', box(0, 0, 0, 40.0, 25.0, 11.0))], (240, 400, 0))
        bas = box(0, 0, 0, 70.0, 50.0, 1.6)
        for sx in (-1, 1):
            for sy in (-1, 1):
                sottrai(bas, cyl(sx * 33.0, sy * 23.0, -1, 2.0, 3.6))
        fatti['Rif_Basetta_50x70'] = componente(root, 'Rif_Basetta_50x70', [('basetta', bas)], (300, 400, 0))

        rep = {}
        for nome, occ in fatti.items():
            bb = occ.boundingBox
            rep[nome] = {
                'ingombro_mm': [round((bb.maxPoint.x - bb.minPoint.x) * 10, 2), round((bb.maxPoint.y - bb.minPoint.y) * 10, 2),
                                round((bb.maxPoint.z - bb.minPoint.z) * 10, 2)],
                'corpi': [b.name for b in occ.component.bRepBodies],
            }
        out['creati'] = rep
    except Exception:
        out['errore'] = traceback.format_exc()
    print(json.dumps(out, indent=1))
