# BOM — Hexapod v2

Versione 1.2 (8 ottobre 2026), **approvata dall'utente**: regolatori Pololu e batteria da 2200 mAh confermati, SSC-32 e camera identificate dai link d'acquisto (lente da 120° "GOOD"), stampante Creator 5 Pro con ugelli temprati da 0,4 mm.
La versione 1 è stata rivista da tre revisori indipendenti (elettrico, meccanico, acquisti): 47 rilievi, 1 bloccante, tutti integrati qui. I loro file sono in `docs/revisioni/`.
La viteria è provvisoria: misure, lunghezze e quantità esatte si ricavano dal modello in fase 5.

Legenda **dato**: V = verificato su fonte primaria (datasheet o pagina del produttore, vedi `research_notes/.../verifica_*.md`); S = stimato o da fonte secondaria; C = da confermare sul pezzo reale.
Legenda **stato**: P = già in tuo possesso; A = da comprare; ? = dimmi tu; — = non comprare per ora.
Prezzi letti l'8 ottobre 2026; vanno ricontrollati all'ordine.

## Schema di alimentazione

```
Batteria 2S ── T-plug ── fusibile F1 (20 A) ──┬── regolatore servo 6 V (sinistro) ── VS1 della SSC-32 (9 servo)
                                              ├── regolatore servo 6 V (destro)   ── VS2 della SSC-32 (9 servo)
                                              └── fusibile F2 (2 A) ── interruttore ──┬── regolatore 5 V ── ESP32
                                                                                      ├── VL della SSC-32 (logica)
                                                                                      └── partitore ── GPIO1
Presa di bilanciamento ── cicalino di sottotensione
```

- I due regolatori servo sono sempre collegati alla batteria ma **spenti di default**: li accende l'ESP32 dal pin di abilitazione. Nel percorso dei servo non c'è nessun interruttore, quindi nessun contatto da 18 A.
- L'interruttore generale sta sul ramo logica (meno di 1 A). Robot spento: restano meno di 0,5 mA sui regolatori disabilitati, più il cicalino. **A fine uso si staccano T-plug e presa di bilanciamento.**
- I negativi si uniscono in un solo punto (massa a stella) accanto ai regolatori.

## A. Componenti già decisi

| # | Componente | Q.tà | Modello / codice | Specifiche chiave | Dove | Dato | Stato |
|---|---|---|---|---|---|---|---|
| A1 | Servo | 18 + 4 di scorta, **stesso lotto** | Tower Pro MG90S | 13,4 g; 1,8 kgf·cm a 4,8 V, 2,2 a 6,6 V; tensione dichiarata 4,8 V; cavo 25 cm, spina JR | originali: Botland DNG-24408 (15,50 €, giacenza 0); clone con datasheet: TinyTronics "TianKongRC" 4,50 € da 20 pezzi | V (originale) | ? |
| A2 | Scheda di controllo | 1 | UICPAL "ESP32-S3-CAM N16R8 RE1.3" | ESP32-S3 N16R8; 62,6 × 28,3 mm (67,5 con l'antenna); 2 USB-C; FPC camera 24 pin; nessun foro di fissaggio | AliExpress 1005008519401021, 17,29 € | S (inserzione), C | P |
| A3 | Camera | 1 | UICPAL "OV3660-75MM", modulo DVP 24 pin con flat da 75 mm | variante con lente da 120° "GOOD" (testa compatta). 75 mm in tutto; testa 8,5 × 8,5 mm, alta circa 6 mm (da misurare); linguetta 12,5 × 5 mm; flat largo 6 mm; contatti sul lato opposto alla lente. Un acquirente segnala circa 90° di campo utile nel video | AliExpress 1005007456301694, 3,99 € | S (disegno del venditore), C | P |
| A4 | Servo controller | 1 | "SSC32-V2.5" (clone della Lynxmotion SSC-32U, con micro-USB e zoccolo XBee) | 32 canali; **PCB 72 × 55 mm, 4 fori a 65,5 × 48,5 mm**; morsettiera a 6 poli su un lato corto, micro-USB sul lato opposto; canali 0–15 su un lato lungo, 16–31 sull'altro; VL 6–12 V; logica 5 V | AliExpress 1005001888185034, 27,19 € | S (disegno quotato del venditore), C | P |
| A5 | Batteria | 2 (venduta in coppia) | **OVONIC 2S 2200 mAh 50C, T-plug** | 105 × 33 × 14 mm (tolleranza ±5 / ±2 / ±2); 120 g ± 20; 110 A continui; bilanciamento JST-XH 3 poli. La 5200 mAh che hai resta per le prove al banco | us.ovonicshop.com, 29,99 US$ la coppia; Amazon.it | V (pagina del produttore) | A |

## B. Alimentazione

| # | Componente | Q.tà | Modello / codice | Specifiche chiave | Dove | Dato | Stato |
|---|---|---|---|---|---|---|---|
| B1 | Regolatore del rail servo, 6,0 V | 2 (uno per lato della SSC-32) | **Pololu D42V110F6 (#5673)** | ingresso 6–60 V; uscita 6 V ±3 %; **11 A dichiarati** (con 42 V in ingresso); circa 13,5–14 A stimati per interpolazione con ingresso 7–8,4 V, in aria libera; caduta minima 0,27 V a 8 A; pin di abilitazione; protezione da inversione; 31,8 × 43,2 × 9 mm; 15 g; 4 fori per M2 a 38,9 × 25,4 mm; modello STEP sul sito Pololu | Kamami.pl 54,89 €; Exp-Tech 48,50 € + IVA | V; S per i 14 A | A |
| B2 | Regolatore 5 V per l'ESP32 | 1 | Pololu D24V22F5 (#2858) | ingresso 5,3–36 V; 5 V ±4 %; 2,5 A; 17,8 × 17,8 × 8 mm; 2 fori per M2; piazzole passo 2,54 mm; protezione da inversione | Botland 14,90 €; Exp-Tech 15,69 € + IVA | V | A |
| B3 | Interruttore generale (ramo logica) | 1 | Pololu Big Pushbutton Power Switch con protezione da inversione, HP (#2813) | a pulsante; pin OFF: un impulso alto lo spegne, così il firmware può spegnere tutto a batteria scarica; da spento assorbe meno di 0,2 µA; 20,3 × 25,4 × 4,1 mm; 2,7 g; nessun foro di fissaggio dichiarato | Exp-Tech, Eckstein, Botland | V (pagina Pololu) | A |
| B4 | Fusibile principale F1 | assortimento 5 / 10 / 15 / 20 / 25 A | lama MINI (ATM), 32 V | base 20 A; il valore definitivo (20 o 25 A) si fissa dopo aver misurato lo stallo su un servo reale. 5 e 10 A servono per la prima accensione | ricambi auto, Amazon.it | S | A |
| B5 | Portafusibile principale | 1 | Littelfuse FHM **0FHM0001ZXJ** (14 AWG) | 58 V DC; fusibili MINI 2–30 A; IP67; code da 94 mm in cavo GXL da giuntare; va fissato, non lasciato appeso ai cavi; fusibile non incluso | Mouser, RS, TME: prezzo e giacenza da controllare | V | A |
| B6 | Fusibile del ramo logica F2 | 1 + 1 | portafusibile in linea MINI con cavetti 18 AWG + fusibile MINI 2 A | il ramo logica usa cavo da 22 AWG: F1 da solo non lo proteggerebbe | ricambi auto, Amazon.it | S | A |
| B7 | Condensatore sul rail servo | 2 | elettrolitico 2200 µF 16 V a bassa ESR, es. Panasonic EEUFR1C222 | Ø12,5 × 20 mm, passo 5 mm; saldato a una spina servo a 3 poli e inserito nei canali liberi 15 e 31, con il verso segnato | RS, Mouser, TME | S | A |
| B8 | Condensatore ceramico | 3 | 100 nF 50 V | due in parallelo a B7, uno sull'ingresso ADC | qualunque | S | A |
| B9 | Allarme di sottotensione | 1 | cicalino LiPo 1–8S tipo "BX100" | sulla presa di bilanciamento JST-XH; soglia regolabile 2,7–3,8 V per cella; circa 8 g. **Assorbe sempre: va staccato a fine uso** | Amazon.it, negozi RC, circa 4 € | S | A |
| B10 | Partitore per la misura di batteria | 1 + 1 | resistenze 100 kΩ e 47 kΩ, 1 % | 8,4 V → 2,69 V su GPIO1 (ADC1), dentro il campo 0–2,9 V; preso dopo l'interruttore; la 100 kΩ dal lato batteria. Taratura a un punto contro il multimetro | qualunque | V (campo ADC) | A |
| B11 | Accensione del rail servo, spento di default | 1 + 1 | resistenza 47 kΩ (più una da 22 kΩ di riserva) e diodo 1N4148 | pin ENA dei due B1 uniti e tirati a massa dalla 47 kΩ (circa 0,7 V a riposo); GPIO42 → diodo → ENA per accendere. **La soglia di ENA non è pubblicata: valori da provare al banco** | qualunque | S, C | A |
| B12 | Connettore batteria lato robot | 1 conf. da 3 coppie | T-plug con codino 14 AWG | maschio sul robot (la batteria ha la femmina: da confermare guardando il pacco) | Amazon.it B0FVRHF7GW, 8,99 € | S, C | A |
| B13 | Derivazioni di potenza | 2 | morsetto a leva a 5 vie, tipo Wago 221-415 | fino a 4 mm², 32 A: uno per il positivo, uno per il negativo (punto a stella) | ferramenta, Amazon.it | S (scheda Wago da controllare) | A |
| B14 | Cavo di potenza | 0,5 m rosso + 0,5 m nero | siliconico 14 AWG | batteria → F1 → derivazione → ingressi dei B1 | Amazon.it B075M578PB, 9,99 € | S | A |
| B15 | Cavo verso la SSC-32 | 0,6 m + 0,6 m | siliconico 16 AWG | due coppie separate, una per VS1 e una per VS2. I morsetti del clone hanno passo di circa 3,5 mm: se il 16 AWG non entra, ultimo tratto in 18 AWG (16 A) | Amazon.it B0D9VDPG54, 11,99 € | S | A |
| B16 | Cavo logica | circa 2 m | siliconico 22 AWG, più colori | ramo logica, VL, 5 V, partitore, ENA | Amazon.it | S | A |
| B17 | Puntalini e pinza | 1 kit | puntalini 0,25–10 mm² (ne servono una decina fra 0,5 e 1,5 mm²) | sotto i morsetti a vite: puntalini, non trefoli stagnati | Amazon.it B0FPDZ8SGR, 15,99 € | S | A |
| B18 | Distanziali per i regolatori | 8 | M2, 5–6 mm, nylon o ottone | i B1 scaldano: sollevati dalla plastica, vicino a feritoie, ad almeno 10 mm dalla batteria | Amazon.it | — | A |
| B19 | Termorestringente, stagno, flussante | 1 assortimento | — | giunzioni saldate | qualunque | — | A |

Nota su B1: un solo D42V110F6 copre i picchi realistici ma non i 18 A dei 18 servo in stallo. Con due regolatori, uno per lato (9 servo, 9 A di stallo contro 11 A dichiarati), **il dimensionamento sullo stallo è rispettato per i regolatori**. Non è dimostrato per i morsetti e le piste della SSC-32, per i quali il clone non ha alcun dato (vedi catena elettrica).

## C. Controllo, segnali, cablaggio dei servo

| # | Componente | Q.tà | Modello / codice | Specifiche chiave | Dove | Dato | Stato |
|---|---|---|---|---|---|---|---|
| C1 | Traslatore di livello 3,3 V ↔ 5 V | 1 | modulo a 4 canali con BSS138 (tipo Adafruit 757) | per TX e RX tra ESP32 e SSC-32. Lato basso alimentato dal 3V3 dell'ESP32, lato alto dal 5 V della logica della SSC-32. Le sue resistenze di pull-up tengono la linea a riposo durante il reset | Melopero, Farnell 2301651 | S | A |
| C2 | Basetta di supporto | 1 + 2 + 1 | millefori 50 × 70 mm passo 2,54 con 4 fori; 2 strip femmina 1 × 20; 1 strip maschio 1 × 40 | zoccolo per l'ESP32 (che non ha fori di fissaggio) e supporto saldato per C1, B10, B11 e il ceramico. Interasse delle file dell'ESP32 da misurare (25,4 mm attesi) | Amazon.it | C | A |
| C3 | Ingresso del 5 V nell'ESP32: **alternativa** | 1 + 1 | spinotto USB-C maschio a 90° a saldare + diodo Schottky 1N5817 | Percorso di base: il 5 V di B2 entra dal pin "5V" della scheda. Se alla prova la scheda non si accende da lì (lo schema del venditore dice di no), il 5 V entra dalla porta USB-C "OTG" con il diodo in serie. Il corpo prevede lo spazio per lo spinotto in entrambi i casi | Amazon.it, AliExpress | C | A |
| C4 | Cavetti verso la SSC-32 | 1 conf. | Dupont femmina 10–20 cm | TX, RX, GND e 5 V tra basetta e SSC-32 | qualunque | — | A |
| C5 | Prolunghe servo | 20 | JR maschio-femmina 15 cm, 22 AWG | circa 10 per i servo di tibia e i femori delle zampe d'angolo, 2 per i condensatori B7; il numero dipende dalla lunghezza reale del cavo dei servo (250 o 175 mm) | Amazon.it B087289HFS, 10,99 € | S | A |
| C6 | Clip di blocco delle prolunghe | 1 conf. da 40 | clip per connettori servo | una per giunzione | Amazon.it B0C61PDHDF, 10,99 € | S | A |
| C7 | Prolunga di bilanciamento | 1 | JST-XH 3 poli (2S), 10–20 cm | porta la presa di bilanciamento a un punto raggiungibile senza togliere il pacco | negozi RC | S | A (se serve dal CAD) |
| C8 | Antenna esterna | 1 | 2,4 GHz con cavetto IPEX | solo se la prova di portata a guscio montato lo richiede; dipende dalla resistenza di selezione sulla scheda | Amazon.it | C | — |

Assegnazione dei pin dell'ESP32. Che siano liberi su questa scheda viene dall'inserzione e dal disegno Freenove (S, C); le proprietà elettriche dal datasheet Espressif (V).

| Funzione | GPIO | Nota |
|---|---|---|
| UART1 TX → RX della SSC-32 | 21 | nessun impulso spurio all'accensione; flottante al reset, lo tiene a riposo C1 |
| UART1 RX ← TX della SSC-32 | 14 | riserva: GPIO47, da provare al banco |
| Tensione di batteria | 1 (ADC1_CH0) | ADC2 non funziona con il Wi-Fi |
| Accensione rail servo | 42 | alto = acceso; spento con GPIO flottante |
| Spegnimento dell'interruttore B3 | 41 | impulso alto = robot spento |
| Liberi | 2, 47 | 38/39/40 se non si usa la scheda TF |

Seriale: 115200 baud, 8N1 (per il clone è solo dichiarazione del venditore). Messa in servizio: premere BAUD sulla SSC-32 e leggere i LED, misurare a riposo la tensione del suo pin TX, inviare `VER`. Quando si configura la SSC-32 dal PC via micro-USB, staccare il TX dell'ESP32.

## D. Giunti e meccanica

Come è fatto ogni giunto (da confermare con uno schizzo come primo passo del CAD):

- il servo è chiuso in una culla che lo stringe; sul fondo della culla, coassiale all'albero, sta il cuscinetto, con la flangia a battuta;
- la parte mobile è una forcella a due bracci: un braccio porta la squadretta, in una tasca aperta verso l'esterno e chiusa da un coperchietto; l'altro porta il perno;
- il perno si infila **per ultimo dall'esterno** e si blocca con una vite di fermo M2, così il giunto si monta e si smonta senza rompere nulla;
- nella coxa l'albero sta in alto e il cuscinetto in basso.

| # | Componente | Q.tà | Modello / codice | Specifiche chiave | Dove | Dato | Stato |
|---|---|---|---|---|---|---|---|
| D1 | Cuscinetto del lato opposto all'albero | 18 + 12 di scorta | **F683ZZ** flangiato schermato | 3 × 7 × 3 mm; flangia Ø8,1 × 0,8; carico statico 108–129 N contro circa 12 N di lavoro. Ordinare "ZZ": la versione aperta F683 è larga 2 mm | a tua cura (unica confezione da 20 trovata: eBay.de 157288484750, spedizione dagli USA) | V (NMB LF-730ZZ) | A |
| D2 | Perno del cuscinetto | 18 + scorta | spina cilindrica Ø3 × 10 mm con **tolleranza dichiarata h8** (ISO 2338), oppure asta rettificata Ø3 h6 tagliata a misura | con h8 l'accoppiamento va da 0,008 mm di interferenza a 0,014 di gioco. Le spine comuni sono m6 e nel cuscinetto entrano sempre forzate: vanno provate su un cuscinetto campione. Misurare tutte col micrometro | a tua cura | S, C | A |
| D3 | Squadretta lato albero | 18 | squadretta di plastica di serie dell'MG90S | inclusa con i servo; quote non pubblicate: vanno misurate (domanda 1) | — | C | con A1 |
| D3-opz | Squadretta metallica, solo come prova | 1 conf. | alluminio "21T, Ø4,9 mm, M2" per crawler 1/24 (es. RampCrab, 3 pezzi) | compatibilità con l'MG90S **non provata**: dipende dal numero di denti e dalla vite centrale. Non comprare prima della risposta alla domanda 1 | amazon.com B0D6GDBYGS | C | — |
| D4 | Inserti a caldo M2 | 100 | CNC Kitchen M2 × 3 (Ø3,6; foro 3,2) | gusci delle zampe, 18 fermi dei perni, 6 per i Pololu B1 e B2 | cnckitchen.store 9,90 € | S (quote), V (lunghezza) | A |
| D5 | Inserti a caldo M3 | 100 | CNC Kitchen M3 × 5,7 (Ø4,6; foro 4,0) | corpo, coperchi, vano batteria | cnckitchen.store 9,40 € | S, V | A |
| D6 | Viti M2 | assortimento + 40 + 40 | testa cilindrica con esagono incassato (ISO 4762), inox A2, 4–20 mm; in più M2 × 25 e M2 × 30 | alette dei servo (passanti con dado), gusci (passanti lunghe), coperchietti, fermi dei perni | Amazon.it, ferramenta | — | A |
| D7 | Dadi e rondelle M2 | 100 + 50 + 50 | dadi esagonali DIN 934, dadi quadri DIN 562, rondelle DIN 433 (Ø4,5) | sotto le alette non c'è parete per un inserto (0,6 mm contro 1,3): vite passante e dado in tasca aperta verso la cavità del servo | idem | S | A |
| D8 | Viti M3 | assortimento | ISO 4762 inox A2, 6–16 mm | corpo | idem | — | A |
| D9 | Fissaggio della SSC-32 | 4 + 4 | viti M2,5 × 10 e dadi M2,5 | i fori del clone sono circa 3,0 mm: una M3 può non passare. Sedi ad asola finché non arrivano le misure | idem | C | A |
| D10 | Piedini antiscivolo | 6 + 2 | stampati in TPU 95A oppure cappucci in silicone | il TPU 95A è duro sui pavimenti lisci: scelta dopo una prova | — | — | A |
| D11 | Fermo batteria | 2 + 1 + 1 | cinghie a strappo 20 × 250–300 mm; schiuma EVA adesiva 3–5 mm; foglio antiscivolo | battuta fissa da un lato, schiuma dall'altro: il pacco ha ±5 mm di tolleranza in lunghezza | Amazon.it | — | A |
| D12 | Guaina e fascette | 1 m + 1 conf. | guaina spiralata 6 mm, fascette 2,5 mm | fasci dei 3 cavi per zampa, due ancoraggi per giunto | qualunque | — | A |

Niente frenafiletti sulle squadrette di plastica: la vite centrale si controlla a ogni manutenzione da un foro d'accesso.

## E. Materiali di stampa

Dati di materiale da schede Bambu Lab (altra marca rispetto ai tuoi filamenti): dato S.

| # | Voce | Q.tà | Uso | Nota | Stato |
|---|---|---|---|---|---|
| E1 | PETG-CF | 1 bobina (ne servono circa 330 g) | corpo, zampe, culle dei servo | tiene 68–74 °C; la migliore adesione tra strati dei quattro; rigidezza nel piano simile al PLA normale | ? |
| E2 | PLA o PETG non caricato, altro colore | circa 200 g | cover non strutturali e finestra sopra l'antenna Wi-Fi | il carbonio scherma: almeno 15 mm liberi attorno all'antenna | ? |
| E3 | TPU 95A | pochi grammi | piedini | supportato dalla Creator 5 | ? |

Il PLA-CF è il più rigido (+35 %) ma cede a 54–55 °C come il PLA e ha l'adesione tra strati più bassa (26 MPa contro 38): i servo sotto carico scaldano, quindi non va nelle culle.

Stampante: Flashforge Creator 5 Pro, chiusa, con ugelli temprati da 0,4 mm usati anche per i caricati (dato dell'utente). Spessori del CAD in multipli di 0,4 mm, pareti strutturali da almeno 1,6 mm. Volume di stampa 256 × 256 × 256 mm verificato per la Creator 5 base: per la Pro da confermare.

## Catena elettrica: tensioni e correnti

Stallo di progetto 1,0 A per servo (D-005). Correnti lato batteria con rendimento 0,9, batteria a 6,6 V, logica inclusa. In appoggio a tripode i due lati della SSC-32 si dividono il carico 2/3 e 1/3 a turno.

| Tratto | Tensione | Media in marcia | Picco realistico | Tutti in stallo | Limite del componente | Esito |
|---|---|---|---|---|---|---|
| Batteria | 6,4–8,4 V (minimo d'uso 6,6 V) | circa 5 A | 11,4 A | 18,7 A | 110 A continui (50C × 2,2 Ah) | ok |
| T-plug | — | 5 A | 11,4 A | 18,7 A | 25 A (Amass AM-1015E; quello montato da OVONIC è di marca ignota) | ok, controllare che non scaldi |
| Fusibile F1, 20 A | — | 25 % | 57 % | 94 % | 20 A | ok per il cortocircuito; non protegge dallo stallo. Valore da confermare dopo la misura |
| Cavo 14 AWG | — | — | — | 18,7 A | 32 A | ok |
| Regolatore B1, ciascuno | ingresso ≥ 6,3 V per avere 6,0 V pieni | fino a 3 A | 7,2 A | 9 A | 11 A dichiarati; circa 14 A stimati | ok |
| Morsetto VS della SSC-32, per lato | 6,0 V | fino a 3 A | 7,2 A | 9 A | 15 A di picco e 3–5 A continui raccomandati (Lynxmotion); **per il clone nessun dato** | **da confermare** sul clone |
| Cavo 16 AWG, per lato | — | — | — | 9 A | 22 A | ok |
| Servo MG90S | 6,0 V (6,18 al massimo) | — | — | 1,0 A | 4,8 V dichiarati; coppia data a 6,6 V | ok |
| Ramo logica: F2, interruttore B3, cavo 22 AWG | 6,4–8,4 V | 0,2 A | 0,5 A | — | 2 A (F2); 7 A (cavo) | ok |
| Regolatore B2 | ingresso 6,4–8,4 V (minimo 5,3) | 0,15 A | 0,5 A | — | 2,5 A | ok |
| ESP32-S3-CAM | 5 V dal pin 5V; con l'alternativa C3 circa 4,65 V dopo il diodo | 0,14 A | 0,5 A | — | richiede ≥ 0,5 A; il suo regolatore vuole almeno 4,4–4,6 V | **da provare al banco** |
| Logica SSC-32 (VL) | 6,4–8,4 V dalla batteria | < 0,1 A | — | — | 6–12 V (venditore del clone); regolatore non identificato | **da confermare** a fine scarica |
| ESP32 TX → SSC-32 RX | 3,3 V → 5 V via C1 | — | — | — | soglia ATmega 3,0 V, uscita ESP garantita solo 2,64 V | ok con C1 |
| SSC-32 TX → ESP32 RX | 5 V → 3,3 V via C1 | — | — | — | massimo ESP 3,6 V | ok con C1 |
| Ingresso ADC | 2,69 V a 8,4 V | — | — | — | 2,9 V | ok |

Contromisure per ciò che l'hardware non copre:

- **Stallo prolungato**: il firmware limita il tempo di sforzo a servo fermo e spegne il rail (GPIO42). Senza firmware il rail è spento.
- **Lato della SSC-32**: se foto e misure del clone mostrano piste strette, due opzioni da decidere prima del CAD: un fusibile MINI da 10 A per lato tra B1 e morsetto, oppure una barra di alimentazione esterna per +V e massa dei servo, lasciando alla SSC-32 solo i segnali.
- **Scarica profonda**: allarme a 3,5 V per cella, arresto dei servo a 3,3 V, autospegnimento a 3,2 V (GPIO41 sull'interruttore B3), mai sotto 3,0 V. Soglie misurate sotto carico, media su 1–2 s. Il cicalino B9 funziona anche a firmware bloccato.

## Connettori: chi si accoppia con chi

| Da | A | Tipo | Nota |
|---|---|---|---|
| Batteria (T-plug femmina) | B12 (T-plug maschio) | Deans | genere da confermare sul pacco |
| Batteria, bilanciamento | B9 cicalino | JST-XH 3 poli | eventuale prolunga C7 |
| B12, B5, B6 | B13 derivazioni | cavo 14 AWG nei morsetti a leva | il negativo è il punto a stella |
| B13 | ingressi dei due B1 | saldatura o morsetti passo 5 mm | 14 AWG |
| Uscite dei B1 | morsetti VS1 e VS2 della SSC-32 | morsetto a vite con puntalino | 16 AWG. Ordine sul clone, dall'angolo del canale 0: VS1−, VS1+, VL−, VL+, VS2−, VS2+ (da rileggere sulla serigrafia). Verificare col tester che i tre negativi siano la stessa massa |
| B3 (uscita) | B2, morsetto VL, B10 | saldatura; puntalino su VL | 22 AWG |
| B2 (uscita) | ESP32 | pin 5V sulla basetta C2; in alternativa spinotto USB-C C3 con diodo | secondo la prova sulla scheda |
| ESP32 3V3 / 5 V della SSC-32 | C1, lato basso / lato alto | piazzole sulla basetta C2; Dupont verso la SSC-32 | — |
| ESP32 GPIO21, GPIO14 | C1 → RX, TX della SSC-32 | basetta + Dupont femmina | — |
| ESP32 GPIO42 | pin ENA dei due B1, tramite B11 | 22 AWG | — |
| ESP32 GPIO41 | pin OFF di B3 | 22 AWG | — |
| B7 condensatori | canali 15 e 31 della SSC-32 | spina JR femmina a 3 poli | verso segnato |
| Servo (JR femmina) | header a 3 pin della SSC-32 | passo 2,54 mm | massa verso il bordo, +V al centro, segnale verso l'interno; la spina non ha chiave. Una barra stampata trattiene le 18 spine |
| Servo lontani | C5 prolunghe | JR maschio-femmina | con clip C6 |
| OV3660 | connettore FPC della scheda | 24 poli passo 0,5 mm | — |
| PC | porta USB-C "TTL" dell'ESP32 | USB-C | accessibile dall'esterno |
| PC | micro-USB della SSC-32 | micro-USB | solo configurazione |

Ripartizione dei servo: zampe di sinistra sui canali 0–8 (lato VS1), zampe di destra sui canali 16–24 (lato VS2). I due ponticelli VS1=VS2 e il ponticello VL=VS vanno **tolti**.

## Attrezzi e materiali di consumo necessari

- Caricabatterie bilanciato per LiPo 2S e sacca ignifuga; cavo di carica con T-plug (da una coppia di B12).
- Saldatore a temperatura regolabile con punte per inserti M2 e M3; multimetro; calibro; **micrometro 0–25 mm** (per i perni); bilancia da 1 g.
- Chiavi esagonali 1,5 / 2 / 2,5 mm, cacciavite PH00, punta o alesatore da 3,0 mm, morsa piccola.
- Cavo USB-C dati e cavo micro-USB dati.

## Ordine degli acquisti consigliato

1. Subito: cuscinetti D1 (tempi lunghi) e ciò che serve per **una zampa di prova**: 3 servo, perni, inserti e viti M2, PETG-CF.
2. Dopo la zampa di prova e le misure sui servo: tutto il resto.

## Costo indicativo di ciò che è da comprare

Sezioni B–E più la coppia di batterie: circa **470 €**, più 40–70 € di spedizioni. Non tutte le righe hanno un prezzo letto: è una stima, non una somma. A parte i servo, se non li hai già.

## Aperto: serve una tua risposta o una misura

| # | Domanda | Cosa sblocca |
|---|---|---|
| 1 | Su un servo: numero di denti del millerighe, diametro della vite centrale (2,0 o 2,5 mm), diametro dei fori delle alette, quote di una squadretta (lunghezza del braccio, diametro del mozzo, diametro e passo dei fori), sporgenza delle viti del fondello. Sono originali o cloni? Quanto è lungo il cavo? | tasca della squadretta, viti delle alette, numero di prolunghe, coppia e corrente reali |
| 2 | SSC-32, quando l'hai in mano: sigla del regolatore accanto ai morsetti, larghezza delle piste dei morsetti VS, passo e foro dei morsetti (sembrano da 3,5 mm), conferma col calibro di 72 × 55 mm e dei fori a 65,5 × 48,5 mm, altezza del componente più alto | portata per lato (D-021); logica a fine scarica; quote definitive |
| 3 | Scheda ESP32: alimentata con 5 V sul pin "5V" si accende? (previsti entrambi i percorsi). Foto della zona del connettore d'antenna | scelta fra pin 5V e spinotto C3; antenna |
| 4 | Camera, quando arriva: altezza della testa e diametro della lente; funziona sulla scheda? | foro nel frontale |
| 5 | Peso reale di SSC-32, scheda ESP32 con camera e un servo, se hai una bilancia | bilancio di massa |

Nessuna di queste blocca l'inizio del CAD: le quote interessate sono parametri del modello. La 1 e la 4 servono prima di stampare.
