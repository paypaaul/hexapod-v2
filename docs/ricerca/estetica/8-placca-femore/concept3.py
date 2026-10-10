"""Placche del femore, terza idea dell'utente (10 ottobre 2026): lame laterali nello stile del guscio della tibia (piano
esterno, smussi a 45 gradi da 4 mm tutt'attorno, chiuse anche sulle teste dei bulloni) e in cima solo strisce strette e
appena bombate sull'uscita dei cavi dei servo. Le lame stanno fra |y| 31 (fianco del femore a 30,6) e 35 (teste dei bulloni
fino a 33,5, 0,4 di gioco e 1,1 di pelle sopra le tasche); si alzano verso il ginocchio e si stringono verso l'anca. Terna della zampa: anca a x 55, ginocchio a x 120, z 0 sugli assi.
Ginocchio: striscia da lama a lama con l'interno a z >= 25 (il guscio della tibia arriva a 24 dall'asse); le lame si alzano
per raggiungerla. Anca: il ponte e la cima della coxa occupano |y| <= 12 da 116 gradi in su attorno all'asse; la striscia si
riduce a una linguetta dalla lama B sull'uscita del cavo (y -14), da y -34,4 a -13."""
import math, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'cad', 'render'))
from render import Scena, terna_piano

BIANCO = '#f2f2f2'
OUT = os.path.dirname(os.path.abspath(__file__)) + '/'
Y0, YE, SM, SP = 31.0, 35.0, 4.0, 1.6   # bordo interno, faccia esterna, smusso, spessore delle strisce

def lastra(s, contorno, lato):
    """Lastra sfaccettata: contorno (x, z) convesso al bordo interno |y| = Y0, faccia piana a |y| = YE rientrata di SM."""
    c = np.array(contorno, float)
    x2 = lambda a, b: a[0] * b[1] - a[1] * b[0]
    if x2(c[1] - c[0], c[2] - c[1]) < 0:
        c = c[::-1]                                                  # antiorario: l'interno sta a sinistra dei lati
    n = len(c)
    rette = []                                                       # lati spostati verso l'interno di SM
    for i in range(n):
        d = c[(i + 1) % n] - c[i]; d /= np.linalg.norm(d)
        rette.append((c[i] + SM * np.array([-d[1], d[0]]), d))
    faccia = []
    for i in range(n):
        (p1, d1), (p2, d2) = rette[i - 1], rette[i]
        t = x2(p2 - p1, d2) / x2(d1, d2)
        faccia.append(p1 + t * d1)
    pts = [(x, lato * Y0, z) for x, z in c] + [(x, lato * YE, z) for x, z in faccia]
    s.solido(pts, BIANCO, zampe=True)

def lame(s, feritoia):
    for lato in (1, -1):
        # corpo: si stringe verso l'anca con smussi lunghi, come la tibia verso il piede
        # alta al ginocchio (porta la striscia a z 25), si stringe verso l'anca come la tibia verso il piede
        lastra(s, [(52, -14.5), (129, -14.5), (135.5, -8), (135.5, 23), (131, 27.6), (109, 27.6), (48, 20), (40, 12), (40, -3.5)], lato)
        if feritoia:                                                                                   # come la finestra della tibia
            p = [(74 + 3.5 * math.cos(math.radians(a)), 3 + 3.5 * math.sin(math.radians(a))) for a in range(90, 271, 15)]
            p += [(104 + 3.5 * math.cos(math.radians(a)), 3 + 3.5 * math.sin(math.radians(a))) for a in range(-90, 91, 15)]
            y0, y1 = sorted((lato * (YE - 0.3), lato * (YE + 0.6)))
            s.prisma(p, y0, y1, '#1e1f22', asse='y', zampe=True)
    # striscia sul ginocchio, appena bombata, da lama a lama
    T = terna_piano((113.0, -YE + 1.0, 25.0), (1, 0, 0), (0, 1, 0))
    s.piastra([(0, 0), (14, 0), (14, 2 * YE - 2.0), (0, 2 * YE - 2.0)], T, spessore=SP, colore=BIANCO, bombatura=1.0, raggio_bordo=1.5, zampe=True)
    # linguetta sull'uscita del cavo dell'anca, solo dal lato B: fuori dal ponte della coxa, e la coxa in questa fascia
    # (y -24 .. -13) arriva al massimo a r 19,1 dall'asse dell'anca; segue la pendenza del bordo della lama
    T = terna_piano((48.0, -YE + 1.0, 20.4), (math.cos(math.radians(7)), 0, math.sin(math.radians(7))), (0, 1, 0))
    s.piastra([(0, 0), (14, 0), (14, 20.4), (0, 20.4)], T, spessore=SP, colore=BIANCO, bombatura=0.8, raggio_bordo=1.5, zampe=True)

if __name__ == '__main__':
    varianti = (('3-lame-tibia-feritoia', True), ('3-lame-tibia-lisce', False))
    for nome, fer in [v for v in varianti if len(sys.argv) < 2 or v[0] == sys.argv[1]]:  # 'confronto' non ne sceglie nessuna
        s = Scena()
        s.nascondi('zampe_struttura_cover_tibia_diffusore', 'zampe_struttura_cover_femore')
        lame(s, fer)
        s.render(OUT + nome + '_zampa', viste=[(28, 55, 4.2), (10, 100, 4.2), (60, 100, 4.0)], centro=(0, 136, 0), larghezza=1100, altezza=800, lato=2.5)
        s.render(OUT + nome, viste=('iso_ant',), larghezza=1500, altezza=1000, lato=4.0)
        print('fatto', nome)


def confronto():
    """Foglio di confronto: una riga per variante, tre viste ravvicinate ritagliate al centro."""
    from PIL import Image, ImageDraw, ImageFont
    righe = (('3-lame-tibia-feritoia', 'lame come la tibia, con la feritoia'), ('3-lame-tibia-lisce', 'lame come la tibia, lisce'))
    viste = ('28_55', '10_100', '60_100')
    W, H = 700, 640
    foglio = Image.new('RGB', (W * 3, (H + 50) * 2), '#e9eaed')
    d = ImageDraw.Draw(foglio)
    try:
        f = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 30)
    except OSError:
        f = ImageFont.load_default()
    for r, (nome, titolo) in enumerate(righe):
        d.text((20, r * (H + 50) + 10), titolo, fill='#222', font=f)
        for c, v in enumerate(viste):
            im = Image.open(OUT + '%s_zampa_vista_%s.png' % (nome, v)).convert('RGB')
            x0, y0 = (im.width - W) // 2, (im.height - H) // 2
            foglio.paste(im.crop((x0, y0, x0 + W, y0 + H)), (c * W, r * (H + 50) + 50))
    foglio.save(OUT + 'confronto_lame_tibia.png')


if __name__ == '__main__' and sys.argv[1:] == ['confronto']:
    confronto()
