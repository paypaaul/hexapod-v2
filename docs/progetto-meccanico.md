# Progetto meccanico — versione MG996R

Stato al 9 ottobre 2026: architettura della zampa decisa (D-047), modellazione in Fusion in corso. Il corpo viene dopo la zampa.

## Zampa

### Come è nata

Tre architetture indipendenti, ciascuna con una priorità diversa, giudicate da tre revisori. Dettagli, numeri e calcoli dei revisori in `ricerca/zampa-architetture.json`.

| Proposta | Idea | Massa stimata | Esito |
|---|---|---|---|
| scalata | prima versione portata in scala: servo di coxa nel corpo, coxa a C, femore in due piastre, servo del ginocchio nella tibia; coda del servo del femore girata in basso | 84 g (90–98 secondo il revisore geometrico) | **base**: 7,5 / 6 / 7,5 |
| compatta | coxa corta (34 mm) con il servo di coxa girato, femore 60 | 64 g | 5,5 / 4,5 / 6,5: coxa senza registro assiale, femore chiuso da 2 viti |
| robusta | femore a cassone con dentro i servo di anca e ginocchio | 117 g | 6 / 7 / 4,5: femore e ginocchio oltre il 50 % per architettura |

### Architettura

Terna della zampa (componente `Zampa`): origine sull'asse della coxa, all'altezza dell'asse del femore; X verso l'esterno, Y lungo l'asse del femore verso la piastra delle squadrette, Z in alto. Posa di riferimento: femore orizzontale (α = 0), tibia verticale (γ = 90°).

| Parte | Cosa fa | Come si stampa |
|---|---|---|
| `Coxa` | culla del servo del femore (coda in basso), anima verso il corpo che gira fuori dalla gondola, braccio inferiore sotto la gondola con il perno della coxa | orlo della culla (+Y) sul piano, senza supporti |
| `Coxa_Ponte` | braccio superiore della C: porta la squadretta del servo di coxa, avvitato all'anima con 2 M3 e centrato da una linguetta | faccia superiore sul piano |
| `Femore_B` | piastra dei perni (perni di anca e ginocchio forzati) con il blocco cavo che chiude la sezione | faccia esterna sul piano, blocco in piedi |
| `Femore_A` | piastra delle squadrette: porta tutta la coppia tra anca e ginocchio; 8 M3 nelle squadrette, 4 M3 nel blocco | faccia esterna sul piano |
| `Tibia` | culla del servo del ginocchio (coda verso il piede) e stinco cavo | orlo della culla sul piano |
| `Piedino` | cappuccio in TPU | punta in alto |

Quote principali (dal modello di verifica `calc/zampa_escursioni.py`, da confermare nel CAD):

| Grandezza | Valore |
|---|---|
| Lunghezze coxa / femore / tibia | 55 / 65 / 110 mm |
| Larghezza della zampa lungo Y | 61,1 mm (da −30,55 a +30,55) |
| Piano delle alette dei servo di femore e ginocchio (orlo delle culle) | Y = +9,45 |
| Fondo della culla, faccia esterna / flangia del cuscinetto | Y = −24,15 / −24,95 |
| Disco della squadretta | Y da +24,85 a +27,35 |
| Culla nella terna del servo | x da −12,45 a +32,95, semilarghezza 12,45; bugne degli inserti fino a −17,85 e +38,35 |
| Anima della coxa | X da 40,15 a 44,55 (gioco 0,8 dalla gondola, raggio 39,32) |
| Braccio inferiore della coxa | Z da −38,35 a −33,15, più la nervatura sotto |
| Ponte della coxa | Z da +17,05 a +22,75 |
| Blocco del femore (terna del femore) | X da 21,5 a 44, Z da −2 a +20, smussi in basso verso il ginocchio e in alto verso l'anca |

### Escursioni (modello 2D, gioco minimo 1 mm)

- Femore da −46° a +80°. Ginocchio fino a 180°; il minimo dipende dal femore: 49° con α = −30°, 42° con α = 0°, 36° con α = 17,5°, 30° con α ≥ 40°.
- Tutte le pose di appoggio e volo delle sei andature di `calc/andature.py` (da 130/25 a 70/70, alzata 30) sono libere, con gioco minimo 1,6 mm.
- Il firmware deve limitare γ in funzione di α e l'imbardata relativa delle zampe vicine (contatto se ruotano entrambe di 30° una verso l'altra).

### Da fare nel CAD della zampa

- Parti nell'ordine: coxa, femore B, femore A, tibia, ponte; poi istanze di servo, squadrette, cuscinetti e perni; giunti veri; interferenze sulla posa di riferimento e scansione delle escursioni con i giunti.
- Rifiniture dopo la prima verifica: nervature di schiacciamento nelle culle, alleggerimenti, ganci dei cavi, piedino.
