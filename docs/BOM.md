# BOM — Hexapod v2 (MG996R)

Versione 2.0 (8 ottobre 2026), **approvata dall'utente** l'8 ottobre 2026. Le domande in fondo restano aperte: non bloccano il CAD. Nasce dallo studio in `studio-componenti.md`; il perché delle scelte è lì e in `decisioni.md` (D-043, D-045).
La viteria è provvisoria: misure, lunghezze e quantità esatte si ricavano dal modello nella fase 5.

Legenda **dato**: V = verificato su fonte primaria; S = stimato o da fonte secondaria; C = da confermare sul pezzo reale.
Legenda **stato**: P = già in tuo possesso; A = da comprare; ? = dimmi tu; — = non comprare per ora.
Prezzi indicativi, letti l'8 ottobre 2026 o ripresi dalla prima versione: vanno ricontrollati all'ordine.

## Schema di alimentazione

```
Batteria 2S ── T-plug ── F1 (30 A) ── derivazione + ──┬── regolatore 6 V sinistro ── file VS1 e massa della SSC-32, dal retro (9 servo)
                                                      ├── regolatore 6 V destro   ── file VS2 e massa della SSC-32, dal retro (9 servo)
                                                      └── F2 (2 A) ── interruttore ──┬── regolatore 5 V ── ESP32
                                                                                     ├── VL della SSC-32 (logica)
                                                                                     └── partitore ── GPIO1
GPIO42 ── diodo ── pin di abilitazione dei due regolatori 6 V (tirati a massa: rail spento di default)
Presa di bilanciamento ── cicalino di sottotensione
```

- I due regolatori servo sono sempre collegati alla batteria ma **spenti di default**: li accende l'ESP32 quando la SSC-32 sta già mandando impulsi. Nel percorso dei servo non c'è nessun interruttore.
- La potenza dei servo entra nelle file degli header **dal retro della SSC-32**, con un filo stagnato saldato lungo i pin: i morsetti e le piste della scheda non la portano. Ponticelli "VS1 VS2" e "VS VL" tolti.
- L'interruttore sta sul ramo logica (meno di 1 A). **A fine uso si staccano T-plug e presa di bilanciamento**: il T-plug è anche il sezionamento d'emergenza dei servo.
- I negativi si uniscono in un solo punto (massa a stella) accanto ai regolatori.

## A. Già in possesso

| # | Componente | Q.tà | Modello / codice | Specifiche chiave | Dato | Stato |
|---|---|---|---|---|---|---|
| A1 | Servo | 18 | AZDelivery MG996R (confezioni da 5) | 55 g; 9,4 kgf·cm a 4,8 V, 11 a 6 V; 4,8–7,2 V; 2,5 A di stallo a 6 V; 40,7 × 19,7 × 42,9 mm; due cuscinetti; squadrette di plastica e viteria incluse | V (datasheet AZDelivery) | P |
| A2 | Scheda di controllo | 1 | UICPAL "ESP32-S3-CAM N16R8 RE1.3" | ESP32-S3 N16R8; 62,6 × 28,3 mm (67,5 con l'antenna); 2 USB-C; nessun foro di fissaggio | S, C | P (da confermare) |
| A3 | Camera | 1 | UICPAL "OV3660-75MM", lente 120° "GOOD" | flat da 75 mm; testa 8,5 × 8,5 mm, alta circa 6 mm | S, C | P (da confermare) |
| A4 | Servo controller | 1 | clone "SSC32-V2.5" (AliExpress 1005001888185034) | 32 canali; PCB 72 × 55 mm, fori a 65,5 × 48,5 mm; header a foro passante; VL 6–12 V | S (disegno del venditore) | P |
| A5 | Batteria | 1 | OVONIC 2S 5200 mAh 50C hardcase, T-plug | 137–139 × 46–47 × 24–25 mm; 245–259 g; 260 A continui; cavi 12 AWG; bilanciamento JST-XH. Autonomia stimata 22–27 minuti in marcia classica | V (pagine del produttore) | P |

## B. Alimentazione

| # | Componente | Q.tà | Modello / codice | Specifiche chiave | Dove | Dato | Stato |
|---|---|---|---|---|---|---|---|
| B1 | Regolatore del rail servo, 6,0 V | 2 (uno per lato) | **Pololu D42V110F6 (#5673)** | ingresso fino a 60 V; 11 A tipici dichiarati a 42 V, di più con ingresso basso (circa 13–14 A con la 2S: S); limita la corrente con gradualità; pin di abilitazione e power-good; protezione da inversione; 43,2 × 31,8 × 9 mm; 4 fori M2. Se al banco non basta, al suo posto va il D24V150F6 (#2882), stesso ingombro | Kamami.pl circa 55 €; Exp-Tech circa 49 € + IVA; pololu.com 59,95 US$ | V | A |
| B2 | Regolatore 5 V per l'ESP32 | 1 | Pololu D24V22F5 (#2858) | 5 V, 2,5 A; 17,8 × 17,8 mm; 2 fori M2 | Botland circa 15 € | V | A |
| B3 | Interruttore generale (ramo logica) | 1 | Pololu Big Pushbutton Power Switch HP (#2813) | a pulsante; pin OFF per lo spegnimento da firmware; meno di 0,2 µA da spento; 20,3 × 25,4 mm | Exp-Tech, Eckstein, Botland, circa 10 € | V | A |
| B4 | Fusibile principale F1 | assortimento 15 / 20 / 25 / 30 A | lama ATO/ATC, 32 V | 30 A in uso; 15 A per le prime accensioni | ricambi auto, Amazon.it | S | A |
| B5 | Portafusibile principale | 1 | in linea per lame ATO/ATC, cavi 12 AWG, con coperchio | da fissare al corpo, non appeso ai cavi | Amazon.it, circa 6 € | S | A |
| B6 | Fusibile del ramo logica F2 | 1 + 1 | portafusibile in linea MINI 18 AWG + fusibile MINI 2 A | il ramo logica usa cavo da 22 AWG: F1 da solo non lo proteggerebbe | ricambi auto, Amazon.it | S | A |
| B7 | Condensatore sul rail servo | 2 + 2 | elettrolitico 2200 µF 16 V a bassa ESR, es. Panasonic EEUFR1C222 | Ø12,5 × 20 mm; saldato a una spina servo e inserito in un canale libero, uno per lato | RS, Mouser, TME | S | A |
| B8 | Condensatore ceramico | 3 | 100 nF 50 V | due in parallelo a B7, uno sull'ingresso dell'ADC | qualunque | S | A |
| B9 | Allarme di sottotensione | 1 | cicalino LiPo 1–8S tipo "BX100" | sulla presa di bilanciamento; soglia regolabile; assorbe sempre: si stacca a fine uso | Amazon.it, circa 4 € | S | A |
| B10 | Partitore per la misura di batteria | 1 + 1 | resistenze 100 kΩ e 47 kΩ, 1 % | 8,4 V → 2,69 V su GPIO1 | qualunque | V (campo ADC) | A |
| B11 | Accensione del rail servo | 1 + 1 | resistenza 47 kΩ (più una da 22 kΩ di riserva) e diodo 1N4148 | pin di abilitazione dei due B1 uniti e tirati a massa; GPIO42 → diodo → abilitazione. La soglia bassa non è pubblicata: valori da provare al banco | qualunque | S, C | A |
| B12 | Connettore batteria lato robot | 1 conf. | T-plug maschio con codino **12 AWG** | la batteria ha la femmina (dalle immagini del produttore: da guardare sul pacco) | Amazon.it, circa 8 € | S, C | A |
| B13 | Derivazioni di potenza | 2 | morsetto a leva a 5 vie Wago 221-415 | fino a 4 mm², 32 A: uno per il positivo, uno per il negativo (massa a stella) | ferramenta, Amazon.it | S | A |
| B14 | Cavo di potenza principale | 0,5 m rosso + 0,5 m nero | siliconico 12 AWG | T-plug → F1 → derivazioni | Amazon.it, circa 10 € | S | A |
| B15 | Cavi verso i regolatori e la SSC-32 | 0,5 m + 0,5 m di 14 AWG; 0,6 m + 0,6 m di 16 AWG | siliconico | 14 AWG dalle derivazioni agli ingressi dei B1; 16 AWG dalle uscite dei B1 alle file della SSC-32 | Amazon.it, circa 20 € | S | A |
| B16 | Barre sulle file degli header | 1 m | filo di rame stagnato rigido Ø1 mm (18 AWG) | saldato sul retro della SSC-32 lungo le file VS e di massa di ogni lato | elettronica, Amazon.it, circa 5 € | — | A |
| B17 | Cavo logica | circa 2 m | siliconico 22 AWG, più colori | ramo logica, VL, 5 V, partitore, abilitazione | Amazon.it | S | A |
| B18 | Distanziali | 8 + 4 | M2 da 5–6 mm per i B1; M2,5 (o M3) da almeno 8 mm per la SSC-32 | i B1 scaldano: sollevati dalla plastica, vicino alle feritoie; sotto la SSC-32 passano le barre di B16 | Amazon.it, circa 10 € | — | A |
| B19 | Termorestringente, stagno, flussante | 1 assortimento | — | giunzioni saldate | qualunque | — | A |

Nota su B1: un regolatore serve 9 servo. Corrente stimata per lato: 5–6 A medi nella marcia classica, 8–9 A in quella bassa, picchi di 12–15 A, contro circa 13 A disponibili; oltre, il regolatore limita la corrente e il rail cala, senza spegnersi. Lo stallo contemporaneo di 9 servo (22,5 A) lo impedisce il firmware.

## C. Controllo, segnali, cablaggio dei servo

| # | Componente | Q.tà | Modello / codice | Specifiche chiave | Dove | Dato | Stato |
|---|---|---|---|---|---|---|---|
| C1 | Traslatore di livello 3,3 V ↔ 5 V | 1 | modulo a 4 canali con BSS138 (tipo Adafruit 757) | TX e RX tra ESP32 e SSC-32 | Melopero, Farnell | S | A |
| C2 | Basetta di supporto | 1 + 2 + 1 | millefori 50 × 70 mm; 2 strip femmina 1 × 20; 1 strip maschio 1 × 40 | zoccolo per l'ESP32 (che non ha fori) e supporto per C1, B10, B11 | Amazon.it | C | A |
| C3 | Ingresso del 5 V nell'ESP32: alternativa | 1 + 1 | spinotto USB-C maschio a 90° a saldare + diodo Schottky 1N5817 | solo se la scheda non si accende dal pin 5V | Amazon.it, AliExpress | C | A |
| C4 | Cavetti verso la SSC-32 | 1 conf. | Dupont femmina 10–20 cm | TX, RX, massa, VL | qualunque | — | A |
| C5 | Prolunghe servo | da 0 a 12 | JR maschio-femmina 15 cm, 22 AWG | dipende dalla lunghezza reale dei cavi (32 cm dichiarati) e dai percorsi nel CAD; con 2,5 A una prolunga da 15 cm in 22 AWG perde circa 40 mV | Amazon.it B087289HFS, 10,99 € (20 pezzi) | S | ? (dopo il CAD) |
| C6 | Clip di blocco delle prolunghe | 1 conf. | clip per connettori servo | una per giunzione | Amazon.it B0C61PDHDF, 10,99 € | S | ? (con C5) |
| C7 | Prolunga di bilanciamento | 1 | JST-XH 3 poli, 10–20 cm | porta la presa di bilanciamento dove si raggiunge senza togliere il pacco | negozi RC | S | ? (dopo il CAD) |
| C8 | Antenna esterna | 1 | 2,4 GHz con cavetto IPEX | solo se la portata a guscio montato non basta | Amazon.it | C | — |

## D. Giunti e meccanica

Ogni giunto: il servo è stretto in una culla e appoggia sulle alette; l'albero porta una squadretta metallica avvitata alla parte mobile; sul lato opposto, coassiale, un cuscinetto flangiato e un perno.

| # | Componente | Q.tà | Modello / codice | Specifiche chiave | Dove | Dato | Stato |
|---|---|---|---|---|---|---|---|
| D1 | Cuscinetto del lato opposto all'albero | 18 + 6 | flangiato schermato **5 × 10 × 4** (NMB LF-1050ZZ, venduto come MF105ZZ) | flangia Ø11,6 × 0,8 nella versione NMB (nei generici da 11,2 a 11,7); carico statico 276 N, dinamico 714 N, contro poche decine di newton di lavoro. Ordinare "ZZ" | a tua cura | V (NMB) | A |
| D2 | Perno del cuscinetto | 18 + 6 | spina cilindrica **Ø5 × 12**, tolleranza h8 se si trova (ISO 2338), altrimenti m6 (ISO 8734); lunghezza fissata dal CAD della zampa (D-047) | le m6 entrano forzate nel cuscinetto: provarle su un cuscinetto campione | a tua cura | S, C | A |
| D3 | Squadretta lato albero | 18 + 2 | disco in alluminio per servo a **25 denti** con fori M3, dichiarato compatibile MG996R | sostituisce la squadretta di plastica: niente gioco e niente deformazione con 2,6 kg. I 25 denti dell'MG996R sono il dato comune dei servo di questa taglia: prima di ordinarne 20, provarne una su un tuo servo | Amazon.it, confezioni da 5–10, circa 10–15 € | S, C | A |
| D4 | Inserti a caldo M3 | 200 | CNC Kitchen M3 × 5,7 (Ø4,6; foro 4,0) | alette dei servo (72), zampe, corpo, coperchi | cnckitchen.store circa 9 € ogni 100 | S, V | A |
| D5 | Inserti a caldo M2 | 50 | CNC Kitchen M2 × 3 (Ø3,6; foro 3,2) | regolatori, interruttore, piccole cover | cnckitchen.store circa 10 € | S, V | A |
| D6 | Viti M3 | assortimento + 100 | testa cilindrica con esagono incassato (ISO 4762), inox A2, 6–25 mm; **in più 12 × M3 × 5** per le squadrette della coxa (D-049: proposta, da approvare) | alette dei servo, squadrette metalliche, zampe, corpo | Amazon.it, ferramenta | — | A |
| D7 | Dadi e rondelle M3 | 50 + 100 | dadi esagonali DIN 934, rondelle DIN 125 | dove un inserto non entra | idem | — | A |
| D8 | Viti M2 e M2,5 | assortimento | ISO 4762 inox | regolatori (M2), SSC-32 (M2,5: i suoi fori sono circa 3,0 mm) | idem | — | A |
| D9 | Piedini antiscivolo | 6 + 2 | stampati in TPU 95A oppure cappucci in silicone | scelta dopo una prova sui tuoi pavimenti | — | — | — |
| D10 | Fermo batteria | 2 + 1 | cinghie a strappo 20 × 300 mm; schiuma EVA adesiva 3–5 mm | il pacco ha ±5 mm di tolleranza in lunghezza: battuta fissa da un lato, schiuma dall'altro | Amazon.it | — | A |
| D11 | Guaina e fascette | 2 m + 1 conf. | guaina spiralata 6–8 mm, fascette 2,5 mm | fasci dei 3 cavi per zampa, ancoraggi ai giunti | qualunque | — | A |

## E. Materiali di stampa

| # | Voce | Q.tà | Uso | Nota | Stato |
|---|---|---|---|---|---|
| E1 | PETG-CF | 2 bobine da 1 kg | corpo, zampe, culle | servono circa 700 g di pezzi più provini, supporti e scarti | ? |
| E2 | PETG o PLA non caricato | 1 bobina | cover, sportelli, zona sopra l'antenna Wi-Fi | il carbonio scherma l'antenna | ? |
| E3 | TPU 95A | pochi grammi | piedini | | ? |

## Attrezzi necessari

Saldatore con punta per inserti a caldo (o kit di punte dedicate), multimetro, pinza spelafili, termosoffiatore o accendino per il termorestringente, chiavi a brugola da 1,5 / 2 / 2,5 mm, calibro per controllare i pezzi stampati. Al banco, per le prime accensioni: un alimentatore regolabile con limite di corrente sarebbe utile ma non indispensabile (si parte con F1 da 15 A).

## Ordine degli acquisti consigliato

1. **Una squadretta metallica** (D3), qualche cuscinetto e perno (D1, D2), inserti e viti M3: servono per il provino stampato della culla e del giunto, che conferma le quote del servo prima di tutto il resto.
2. Alimentazione (B1–B19) e controllo (C1–C4): per la prova al banco della SSC-32 con un lato di servo.
3. Il resto delle squadrette, cuscinetti e perni nella lunghezza decisa dal CAD.
4. Filamento quando si stampano le parti vere; prolunghe e prolunga di bilanciamento dopo il CAD.

## Costo indicativo

Circa 380 € di componenti (di cui 110 € i due regolatori) più circa 100 € di filamento. Servo, SSC-32, batteria, ESP32 e camera esclusi perché già in possesso. Stima S: i prezzi vanno ricontrollati all'ordine.

## Aperto: serve una tua risposta

| # | Domanda | Cosa decide |
|---|---|---|
| 1 | ESP32-S3-CAM e camera OV3660: le hai già? (prima avevi detto di sì; ora hai scritto che hai comprato solo servo e SSC-32) | voci A2, A3 |
| 2 | Quanti MG996R hai? Ne servono 18; qualcuno di scorta aiuta | voce A1 |
| 3 | Hai già prolunghe servo, inserti, viteria, filamento o attrezzi dalla v1? | si tolgono dal BOM |
| 4 | Squadrette metalliche: va bene comprarne una per prova prima delle altre 19? | voce D3 |
