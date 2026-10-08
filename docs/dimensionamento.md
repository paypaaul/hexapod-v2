# Dimensionamento preliminare — versione MG996R

8 ottobre 2026. Calcolo riproducibile: `python3 calc/statica_tripode.py` (punto di progetto), `calc/andature.py` (assetti e andature), `calc/assetti.py` (altezze possibili). Geometria e masse sono **stime di partenza**: si chiudono con il CAD e con le misure sui pezzi reali.

## Risultato in breve

- Massa di progetto **2,6 kg** (bilancio 2,57 kg).
- Punto di progetto proposto: **asse dei femori a 100 mm da terra, piede a 45 mm dall'asse**. Coppia massima a tripode 5,5 kgf·cm, il **50 %** degli 11 kgf·cm dichiarati a 6 V. Femore appena sopra l'orizzontale, ginocchio tra 63° e 78°.
- La coppia non dipende dalle lunghezze dei segmenti ma da massa, distanza orizzontale del piede e passo: femore e tibia si scelgono per portata, alzata e ingombro dei servo.
- Ogni 100 g valgono circa 2 punti percentuali. Se lo stallo reale fosse 9 kgf·cm invece di 11, tutte le percentuali salgono di un quinto.

## Bilancio di massa (preliminare)

| Voce | Massa (g) | Stato |
|---|---|---|
| 18 × MG996R | 990 | dichiarato (55 g l'uno): da pesare |
| Batteria OVONIC 2S 5200 mAh | 252 | 245–259 g ± 20 dichiarati |
| SSC-32 | 45 | stima |
| ESP32-S3-CAM + camera | 14 | stima |
| 3 regolatori servo | 102 | UBEC da 34 g l'uno (S) |
| Logica: regolatore 5 V, interruttore, traslatore, basetta | 25 | stima |
| Fusibili, connettori, distribuzione | 50 | stima |
| Cablaggio di potenza e prolunghe | 100 | stima |
| 18 cuscinetti, perni, squadrette metalliche | 110 | stima |
| Viteria e inserti | 90 | stima: si chiude dal modello |
| Parti stampate strutturali (6 zampe da circa 70 g, corpo 280 g) | 700 | stima: si chiude dal CAD |
| Cover | 90 | stima |
| **Totale** | **2568** | |

I soli servo valgono il 39 % della massa. Obiettivo per il CAD: parti stampate entro 790 g in tutto.

## Geometria di partenza

| Parametro | Valore | Nota |
|---|---|---|
| Assi delle coxe | angoli (±95, ±60) mm a 45°; medie (0, ±78) mm | da fissare con la disposizione del corpo |
| Coxa (asse coxa → asse femore) | 45 mm | tra 37 e 57 mm secondo il verso del servo di coxa |
| Femore | 70 mm | minimo circa 48 mm per far passare le due culle |
| Tibia | 115 mm | il servo del ginocchio con la culla ne occupa circa 40 |
| Passo / alzata | 60 mm / 30 mm | |

## Assetti a 2,6 kg

Stallo dichiarato 11 kgf·cm a 6 V. "Luce" con il fondo del corpo 30 mm sotto l'asse dei femori (stima). Escursioni: appoggio più volo con alzata a parabola.

| Asse / piede | Luce | Femore in appoggio | Ginocchio in appoggio | Coppia a tripode | Se lo stallo è 9 | A onda | Ribaltamento | Escursioni richieste (femore; ginocchio) |
|---|---|---|---|---|---|---|---|---|
| 130 / 25 mm | 100 mm | da −25° a −14° | 86–94° | 5,6 kgf·cm, 51 % | 63 % | 47 % | 20° | −25…+5; 62…94 |
| 110 / 40 mm | 80 mm | da −4° a +4° | 70–83° | 5,0, 45 % | 55 % | 39 % | 25° | −4…+28; 50…83 |
| **100 / 45 mm** | 70 mm | da +6° a +12° | 63–78° | **5,5, 50 %** | 61 % | 39 % | 28° | +6…+40; 45…78 |
| 90 / 55 mm | 60 mm | da +17° a +21° | 57–76° | 6,5, 59 % | 73 % | 46 % | 33° | +17…+51; 43…76 |
| 80 / 60 mm | 50 mm | da +28° a +30° | 52–73° | 7,1, 64 % | 78 % | 50 % | 37° | +28…+62; 39…73 |
| 70 / 70 mm | 40 mm | da +34° a +40° | 49–73° | 8,1, 74 % | 90 % | 57 % | 42° | +34…+70; 40…73 |

Lettura:

- A differenza della versione piccola, qui la marcia classica (ginocchio sotto i 90°, femore orizzontale o in salita) sta attorno al 50 %: 45 % a 110/40, 50 % a 100/45.
- Più bassa e larga resta possibile salendo sopra il 50 %, come l'utente accetta: l'assetto si sceglie a robot costruito.
- **Obiettivo per i giunti della zampa**: femore da −30° a +65°, ginocchio da 40° a 150°. È la lezione della prima versione: le escursioni si dimensionano sull'assetto più basso con il piede alzato.
- Con la squadretta montata a metà corsa nella posa femore orizzontale e ginocchio a 90°, le escursioni stanno entro i 160° utili del servo.

Sensibilità alla massa nell'assetto 90/55: 5,5 kgf·cm a 2,2 kg, 6,3 a 2,5 kg, 7,0 a 2,8 kg.

## Corrente e autonomia

Vedi `studio-componenti.md`: 12–14 A medi in marcia, 20–25 minuti con la batteria da 5200 mAh.

## Limiti

- Coppia reale dei servo non misurata: i cloni possono rendere meno del dichiarato.
- 1326 g su 2568 sono stime (tutto tranne servo e batteria).
- Modello statico: suolo piano, corpo orizzontale, baricentro al centro, nessuna accelerazione; il peso proprio delle zampe in appoggio non è sottratto (prudente).
