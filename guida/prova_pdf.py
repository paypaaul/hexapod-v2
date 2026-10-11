"""Prova di fattibilita' del PDF (F0, docs/piano-guida.md): tre pagine A4 orizzontali con un passo, la viteria 1:1 e
l'apertura di una sezione, stampate da Chrome senza interfaccia. Uso: .venv/bin/python guida/prova_pdf.py"""
import os
import subprocess

from PIL import Image

QUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(QUI), 'build', 'guida', 'prova')
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'


def piatta(png, uscita):
    """Alfa appiattita su bianco e colori quantizzati senza dithering: i colori piatti si comprimono bene."""
    im = Image.open(png).convert('RGBA')
    fondo = Image.new('RGBA', im.size, (255, 255, 255, 255))
    fondo.alpha_composite(im)
    fondo.convert('RGB').quantize(colors=96, dither=Image.Dither.NONE).save(uscita, optimize=True)


def vite_iso4762(d, lung, testa_d, testa_k):
    """Vite a testa cilindrica vista di fianco, in mm (SVG 1:1): testa a sinistra, gambo verso destra."""
    w = testa_k + lung + 2
    h = testa_d + 2
    y0 = 1 + (testa_d - d) / 2
    passo = 0.5 if d >= 3 else 0.4
    filetto = ''.join('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"/>' % (1 + testa_k + i * passo, y0, 1 + testa_k + i * passo + passo / 2,
                                                                         y0 + d) for i in range(int(lung / passo)))
    return ('<svg class="vite" width="%.1fmm" height="%.1fmm" viewBox="0 0 %.2f %.2f">'
            '<rect x="1" y="1" width="%.2f" height="%.2f" rx="0.4" class="testa"/>'
            '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" class="gambo"/><g class="filetto">%s</g></svg>'
            % (w, h, w, h, testa_k, testa_d, 1 + testa_k, y0, lung, d, filetto))


def righello(mm):
    tacche = ''.join('<line x1="%d" y1="0" x2="%d" y2="%s"/>' % (i, i, '3' if i % 10 == 0 else ('2' if i % 5 == 0 else '1.2'))
                     for i in range(mm + 1))
    numeri = ''.join('<text x="%d" y="5.6">%d</text>' % (i, i) for i in range(0, mm + 1, 10))
    return ('<svg class="righello" width="%dmm" height="6mm" viewBox="-0.5 0 %d 6"><g class="tacche">%s</g>%s</svg>'
            % (mm + 1, mm + 1, tacche, numeri))


CSS = """
@page { size: 297mm 210mm; margin: 0 }
* { box-sizing: border-box }
body { margin: 0; font-family: -apple-system, 'Helvetica Neue', Arial, sans-serif; color: #1d2026 }
.pagina { width: 297mm; height: 210mm; position: relative; overflow: hidden; break-after: page; padding: 12mm 14mm 14mm 14mm }
.fascia { position: absolute; left: 0; top: 0; width: 297mm; height: 7mm; background: var(--sezione) }
.numero { font-size: 30pt; font-weight: 800; position: absolute; left: 14mm; top: 11mm }
.titolo { position: absolute; left: 36mm; top: 15mm; font-size: 15pt; font-weight: 600 }
.volte { position: absolute; right: 14mm; top: 12mm; font-size: 22pt; font-weight: 800; border: 0.6mm solid #1d2026;
         border-radius: 2mm; padding: 1mm 4mm }
.pezzi { position: absolute; left: 14mm; top: 32mm; width: 62mm; border: 0.5mm solid #1d2026; border-radius: 3mm;
         padding: 3mm; background: #fffbea }
.pezzi h3 { margin: 0 0 2mm; font-size: 9pt; text-transform: uppercase; letter-spacing: 0.06em }
.riga { display: flex; align-items: center; gap: 2mm; margin: 1.5mm 0; font-size: 10pt }
.qta { font-weight: 800; font-size: 12pt; min-width: 9mm }
.vite .testa { fill: #9aa0a8; stroke: #1d2026; stroke-width: 0.15 }
.vite .gambo { fill: #c3c8ce; stroke: #1d2026; stroke-width: 0.15 }
.vite .filetto line { stroke: #4b5058; stroke-width: 0.08 }
.righello .tacche line { stroke: #1d2026; stroke-width: 0.12 } .righello text { font-size: 1.8px }
.immagine { position: absolute; left: 80mm; top: 26mm; width: 203mm; height: 140mm; object-fit: contain }
.testo { position: absolute; left: 14mm; top: 100mm; width: 62mm; font-size: 10.5pt; line-height: 1.35 }
.avviso { border-left: 2mm solid #e8590c; background: #fff4e6; padding: 2mm 3mm; margin-top: 3mm; font-size: 9.5pt }
.piede { position: absolute; left: 14mm; right: 14mm; bottom: 7mm; font-size: 7.5pt; color: #6b7280; display: flex;
         justify-content: space-between }
.controllo { width: 100mm; height: 4mm; background: #1d2026; margin: 4mm 0 1mm }
"""


def main():
    os.makedirs(OUT, exist_ok=True)
    piatta(os.path.join(OUT, 'coxa.png'), os.path.join(OUT, 'coxa_piatta.png'))
    m3x8 = vite_iso4762(3, 8, 5.5, 3)
    pagina_passo = f"""
<section class="pagina" style="--sezione:#ff6a13"><div class="fascia"></div>
 <div class="numero">6.04</div><div class="titolo">Servo del femore nella coxa</div><div class="volte">× 6</div>
 <div class="pezzi"><h3>Pezzi necessari</h3>
  <div class="riga"><span class="qta">1×</span> servo MG996R</div>
  <div class="riga"><span class="qta">2×</span> {m3x8} <span>M3 × 8</span></div>
  <div class="riga">{righello(20)}</div></div>
 <div class="testo"><p>Cala il servo nella culla con il passacavo nella fessura.</p>
  <p>Accosta le due viti delle alette lato coda.</p>
  <div class="avviso"><b>IMPORTANTE</b> — non stringere ancora: le alette si stringono a femore montato (D-049).</div></div>
 <img class="immagine" src="coxa_piatta.png">
 <div class="piede"><span>Hexapod v2.1.6 — guida di montaggio, prova F0</span><span>pagina 1</span></div></section>"""
    pagina_viti = f"""
<section class="pagina" style="--sezione:#3b5bdb"><div class="fascia"></div>
 <div class="numero">A</div><div class="titolo">Viti in scala 1:1 — stampa al 100 % (dimensioni effettive)</div>
 <div style="position:absolute;left:14mm;top:34mm">
  <div class="controllo"></div><div style="font-size:9pt">Questa barra deve misurare 100 mm.</div>
  <div class="riga" style="margin-top:8mm"><span class="qta">M3 × 5</span> {vite_iso4762(3, 5, 5.5, 3)}</div>
  <div class="riga"><span class="qta">M3 × 6</span> {vite_iso4762(3, 6, 5.5, 3)}</div>
  <div class="riga"><span class="qta">M3 × 8</span> {m3x8}</div>
  <div class="riga"><span class="qta">M3 × 10</span> {vite_iso4762(3, 10, 5.5, 3)}</div>
  <div class="riga"><span class="qta">M3 × 16</span> {vite_iso4762(3, 16, 5.5, 3)}</div>
  <div class="riga"><span class="qta">M2 × 5</span> {vite_iso4762(2, 5, 3.8, 2)}</div>
  <div class="riga">{righello(50)}</div></div>
 <div class="piede"><span>Hexapod v2.1.6 — guida di montaggio, prova F0</span><span>pagina 2</span></div></section>"""
    pagina_sezione = """
<section class="pagina" style="--sezione:#ff6a13;background:#fff7f0"><div class="fascia" style="height:30mm"></div>
 <div style="position:absolute;left:14mm;top:8mm;color:white;font-size:34pt;font-weight:800">6 · La zampa</div>
 <div style="position:absolute;left:14mm;top:40mm;font-size:12pt;width:120mm">
  <p><b>Obiettivo:</b> una zampa completa, da rifare uguale sei volte.</p><p><b>Tempo:</b> circa 2 ore la prima, 1 ora le altre (S).</p>
  <p><b>Stato elettrico:</b> T-plug staccato.</p></div>
 <div class="piede"><span>Hexapod v2.1.6 — guida di montaggio, prova F0</span><span>pagina 3</span></div></section>"""
    html = f'<!doctype html><html lang="it"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{pagina_sezione}{pagina_passo}{pagina_viti}</body></html>'
    p_html = os.path.join(OUT, 'prova.html')
    with open(p_html, 'w', encoding='utf-8') as f:
        f.write(html)
    p_pdf = os.path.join(OUT, 'prova.pdf')
    subprocess.run([CHROME, '--headless', '--no-pdf-header-footer', '--disable-gpu', '--print-to-pdf=' + p_pdf,
                    'file://' + p_html], check=True, capture_output=True, timeout=120)
    print('PDF', p_pdf, os.path.getsize(p_pdf))


if __name__ == '__main__':
    main()
