# Simulazione (sim/)

Gemello fisico del robot in MuJoCo, comandato come il robot vero: comandi ASCII della SSC-32, impulsi ogni 20 ms,
servo senza retroazione. È la parte "SIL" della fase S0 (`docs/software.md`, 6.5 e 7).

## Cosa c'è

| File | Contenuto |
|---|---|
| `modello/esapode.xml` | MJCF **generato** da `tools/genera_modelli.py`: non si modifica a mano |
| `ssc32_emu.py` | emulatore della SSC-32 (`SSC32`) e conversione impulsi ↔ angoli con `robot.yaml` (`Canali`) |
| `servo.py` | modello dei servo attorno agli attuatori dell'MJCF: banda morta, servo liberi, coppia all'uscita |
| `andatura.py` | tripode e rotazione sul posto in Python: porting di `cad/script/assieme.py` → `pose_tripode` |
| `simulazione.py` | catena completa: comandi → emulatore → servo → fisica a passi di 2 ms |
| `sil.py` | prova SIL del tripode a comandi aperti, con le misure; si lancia anche da riga di comando |
| `tests/` | test con pytest, senza schermo |
| `requirements.txt` | versioni fissate (MuJoCo 3.14.0) |

## Come si usa

Dalla radice della repo, con un ambiente virtuale (`.venv`, ignorato da git):

```
python3 -m venv .venv && printf '*\n' > .venv/.gitignore
.venv/bin/pip install -r sim/requirements.txt
.venv/bin/python tools/genera_modelli.py            # rigenera URDF e MJCF dopo un cambio di robot.yaml o cad.json
.venv/bin/python tools/genera_modelli.py --controlla
.venv/bin/python -m pytest sim/tests -q              # circa 3 s
.venv/bin/python sim/sil.py                          # 20 s di tripode a 100/45, stampa le misure
.venv/bin/python sim/sil.py --giro 30                # rotazione sul posto
.venv/bin/python sim/sil.py --h 70 --xf0 70          # altri assetti
.venv/bin/python -m mujoco.viewer --mjcf sim/modello/esapode.xml   # per guardarlo (con lo schermo)
```

Nel visualizzatore i gruppi 2 e 3 sono le mesh e le primitive di collisione; la posa "in_piedi" è fra i keyframe.

## Il modello

- Un corpo libero e tre segmenti per zampa, con lo zero dei giunti nella posa "come costruita" del CAD:
  `g_coxa_<z>` = imbardata, `g_femore_<z>` = alpha (asse −Y), `g_ginocchio_<z>` = gamma − 90 (asse −Y). Fine corsa
  meccanici da `cad.json`; la tabella del ginocchio minimo non c'è, la applica la guardia.
- Masse e inerzie: somma delle parti di `cad.json` per segmento, con il trasporto al baricentro; i 360 g non modellati
  sul corpo, distribuiti come il corpo. Massa totale 2943,2 g (`robot.yaml` dice 2945).
- Collisioni con primitive ricavate da `cad.json` e dalle mesh: chiglia, scafo, carapace e sei lobi per il corpo; la
  culla del servo del femore per la coxa; due capsule (una per fianco) per il femore; culla, stinco e sfera del piede
  (raggio 5,6 mm) per la tibia. Riproducono il CAD: due vicine si toccano fra 31 e 32 gradi ciascuna, il ginocchio
  minimo sta da 1 grado sotto a 4 sopra la tabella del CAD, nessun urto nelle 64 pose verificate.
- Sensori: contatto (`touch`) per ogni piede, IMU (accelerometro, giroscopio, assetto) al centro del vano sotto il
  vassoio (`predisposizioni.md`, X4; la x esatta è da fissare, C).
- Contatti: attrito 0,8 (centro della randomizzazione di `software.md` 4.4, S) e `solref` 0,005 s. Con il valore di
  MuJoCo (0,02 s) il contatto è cedevole e cambia i risultati: vedi sotto.

### Servo

| Grandezza | Valore | Da dove |
|---|---|---|
| Coppia massima (`forcerange`) | 1,079 N·m | stallo 11 kgf·cm a 6 V (V) |
| Smorzamento del giunto | 0,144 N·m·s/rad | stallo / velocità a vuoto (0,14 s/60° = 7,48 rad/s, V): la retta coppia-velocità del motore a piena tensione |
| `kp` | 12,4 N·m/rad | stallo raggiunto a 5° di errore (S, da identificare: `software.md` 4.6) |
| Banda morta | ±2,5 µs = ±0,225° | larga 5 µs (V), in gradi con 11,1 µs/° (S); applicata da `servo.py` |

Mancano ritardo proprio del servo, gioco, offset di taratura e variazione con la tensione: arrivano con
l'identificazione dei servo (S4). Il ritardo degli impulsi (un fotogramma da 20 ms) c'è già, dall'emulatore.

## Emulatore della SSC-32

Comandi ASCII: gruppi `#<ch>P<us>[S<us/s>]…[T<ms>]`, `#<ch>P0`, `STOP <ch>` e `#<ch>STOP`, `Q`, `QP <ch>`, `VER`;
`<esc>` annulla la riga. Interpolazione lineare dei gruppi, un fotogramma di impulsi ogni 20 ms, campo 500–2500 µs.
Uscita verso i servo con canali, versi, calettamento e µs per grado di `robot.yaml`.

Da confrontare con il clone al banco (S1, passo B1): comportamento dopo `P0`, troncamento di `QP`, stringa di `VER`,
tempi di risposta. Il modo binario e il tempo di trasmissione sulla seriale non ci sono ancora.

## Prova SIL (tests/test_sil.py)

Un "firmware" Python manda ogni 20 ms un gruppo con i 18 canali e `T20`; nessuna retroazione. Assetto 100/45, passo
60, alzata 30, periodo 1,0 s (120 mm/s; velocità comandate fino a 215°/s, sotto i 250 della guardia), rampa di passo
e giro sul primo ciclo, poi 20 s. Si prova il tripode dritto e la rotazione sul posto di 30° a passo.

| Verifica | Soglia e perché | Dritto | Giro 30 |
|---|---|---|---|
| Non cade | asse dei femori sopra h − alzata/2 = 85 mm; inclinazione sotto la posa sicura a 100/45 (25°, `software.md` 2.6); solo i piedi a terra | 97,8–99,2 mm; 0,20° | 97,7–99,2 mm; 0,14° |
| Urti fra parti | nessuno | nessuno | nessuno |
| Scivolamento dopo l'atterraggio | spostamento del piede lasciato libero dalla banda morta dei tre servo: 1,26 mm | 0,53 mm | 0,54 mm |
| Scivolamento per appoggio intero | 10 % del passo, 6 mm | 2,73 mm | 4,03 mm |
| Avanzamento o rotazione | entro il 10 % del comandato | 2305 mm su 2340 | 1143° su 1170 |
| Coppia | sotto il 60 % dello stallo (`robot.yaml` → guardia) | coxa 43 %, femore 51 %, ginocchio 49 % | 52 %, 52 %, 35 % |

Numeri del 9 ottobre 2026, macOS. Il femore al 51 % coincide con `calc/statica_tripode.py` (51,4 %).

Cose da sapere:

- **Atterraggio**: il volo di `pose_tripode` torna avanti a velocità costante e il piede arriva a terra ancora in moto
  (240 mm/s rispetto al pavimento): striscia 2–3 mm nei primi 50 ms dell'appoggio, poi resta fermo. Il generatore del
  firmware, con una Bézier che arriva a velocità zero (`software.md` 4.2), dovrebbe toglierlo.
- **Partenza**: senza la rampa (`sil.py --avvio 0`) il tripode d'appoggio passa da fermo a 120 mm/s in un fotogramma e
  il ginocchio posteriore tocca il 76 % dello stallo per qualche decina di millisecondi; a regime resta sotto il 50 %.
- **Rigidezza dei contatti**: con il `solref` di MuJoCo (0,02 s) il corpo cede di più, i piedi caricati strisciano fino
  a 3 mm e il femore tocca l'83 % agli atterraggi: la prova non passerebbe. Con 0,01 s: 1,5 mm e 58 %. Il valore
  scelto (0,005 s) è il più rigido stabile con il passo di 2 ms; va confermato confrontando simulazione e robot (S4).
- Altri assetti, senza asserzioni (stessa prova, `sil.py --h … --xf0 …`): nessuno cade né urta, ma negli assetti bassi
  la coppia sale e i piedi caricati strisciano oltre la soglia di 100/45 (in tutti la soglia vale 1,26 mm calcolata
  a 100/45):

  | Assetto | Coppia massima coxa / femore / ginocchio | Scivolamento dopo l'atterraggio, massimo |
  |---|---|---|
  | 130/25 | 41 / 51 / 50 % | 1,63 mm |
  | 80/60 | 41 / 59 / 56 % | 1,36 mm |
  | 70/70 | 35 / 81 / 66 % | 2,18 mm |

  A 70/70 il tripode supera il 60 % (in `docs/software.md` 4.2 il calcolo statico dà 75 %): conferma che negli assetti
  bassi serve l'andatura a coppie o a onda.
