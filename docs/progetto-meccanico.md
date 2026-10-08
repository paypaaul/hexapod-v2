# Progetto meccanico — versione MG996R

Stato al 9 ottobre 2026: **zampa v0 modellata e verificata in Fusion** con i giunti veri (D-047, D-048). Il corpo viene dopo.

![Zampa v0, femore a +12°, ginocchio a 75°](immagini/zampa-v0.png)

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
| Ponte della coxa | mozzo Z da +17,05 a +23,5; braccio da +19,6 a +23,5 (appoggio sulla testa dell'anima) |
| Blocco del femore (terna del femore) | X da 21,5 a 44, Z da −2 a +20, smussi in basso verso il ginocchio e in alto verso l'anca |

### Modello in Fusion (zampa v0)

Script `cad/script/zampa.py`, passi `parametri`, `coxa`, `ponte`, `femore_b`, `femore_a`, `tibia`, `istanze`, `controllo`, `giunti`, `limiti`, `misura`, `scansione`, `interferenze`, `stato`. Tutte le parti hanno la terna della zampa e le quote come espressioni dei parametri (`zam_`, `cul_`, `cox_`, `fem_`, `tib_`, `zy_`, `cz_`, …): cambiando un parametro si rigenera la parte. Dopo aver rigenerato una parte vanno rifatti `giunti` e `limiti` (cancellare una parte cancella i giunti che la usano).

| Parte | Volume pieno | Massa stimata | Note |
|---|---|---|---|
| Coxa | 20,7 cm³ | 24,7 g | culla, anima con tasca a rombo, testa per il ponte, braccio con nervatura |
| Coxa_Ponte | 4,1 cm³ | 5,1 g | |
| Femore_B | 33,0 cm³ | 23,3 g | piastra dei perni e blocco pieno (lo slicer lo stampa a pareti e riempimento) |
| Femore_A | 7,1 cm³ | 9,2 g | |
| Tibia | 22,2 cm³ | 27,1 g | culla con finestre, stinco 12 × 18,9 con tre finestre |
| **Totale** | **87,1 cm³** | **89,4 g** | stima: PETG-CF 1,3 g/cm³, pareti e fondi 1,2 mm, riempimento 25 % |

La massa supera i 70 g del bilancio: sei zampe pesano circa 115 g in più, cioè circa 2 punti di coppia al femore (da 49 a circa 51 % al punto di progetto). Il dato vero viene dallo slicer.

Dentro `Zampa`: 2 servo, 3 squadrette (anche quella della coxa, che gira con la zampa), 2 cuscinetti (quello della coxa sta nella gondola del corpo), 3 perni; 12 giunti rigidi e 2 di rivoluzione (`G_femore`, `G_ginocchio`). Verso misurato: α = −(valore di G_femore), γ = 90° − (valore di G_ginocchio). Limiti impostati: α da −45° a +85°, γ da 30° a 175°.

Verifiche fatte sul modello (9 ottobre 2026):

- posa di riferimento: nessuna interferenza (escluso il mozzo pieno della squadretta sul millerighe, voluto);
- tutte le copie di servo, squadrette, cuscinetti e perni nella posizione prevista (scarto 0,000);
- scansione con i giunti veri ogni 5°, femore da −50° a +90°, ginocchio da 20° a 170°: femore libero da −45° a +85° (a −50° la piastra tocca la culla, a +90° il ponte tocca il blocco); ginocchio libero fino ad almeno 170°, minimo 30° con il femore sopra +35°, 40° con il femore tra 0 e +15°, 45° tra −30° e −5°, 50° sotto −30°;
- tutte le 212 pose di appoggio e volo delle sei andature (`calc/andature.py`, alzata 30) libere;
- manca ancora il corpo: la gondola del servo di coxa limiterà il femore sopra circa +80° (modello 2D) e la rotazione della coxa va verificata con il corpo.

### Escursioni (modello 2D, gioco minimo 1 mm)

- Femore da −46° a +80°. Ginocchio fino a 180°; il minimo dipende dal femore: 49° con α = −30°, 42° con α = 0°, 36° con α = 17,5°, 30° con α ≥ 40°.
- Tutte le pose di appoggio e volo delle sei andature di `calc/andature.py` (da 130/25 a 70/70, alzata 30) sono libere, con gioco minimo 1,6 mm.
- Il firmware deve limitare γ in funzione di α e l'imbardata relativa delle zampe vicine (contatto se ruotano entrambe di 30° una verso l'altra).

### Da fare nella zampa

- Nervature di schiacciamento nelle culle (da tarare sul provino), ganci e passaggi dei cavi, piedino in TPU, raccordi.
- Viti delle squadrette della coxa (M3 × 6 con rondella sotto la testa, D-048) da controllare quando si sceglie la squadretta: altezze e posizione dei fori sono stimate (`sq_`).
- Verifica con il corpo: gondola, rotazione della coxa, zampe vicine.
