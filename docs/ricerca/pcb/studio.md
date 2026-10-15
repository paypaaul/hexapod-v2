# Circuiti stampati al posto delle millefori: studio preliminare

Sintesi del 16 ottobre 2026 dello studio chiesto in D-076 (`docs/decisioni.md:684`: "l'utente prevede di far stampare un PCB al posto delle millefori e lo disegneremo insieme in una versione successiva"). È il documento da leggere; i dettagli stanno nei file della stessa cartella:

- `requisiti.md`: cosa devono fare le schede e dove stanno (requisiti R-01…R-20, righe 302-321);
- `produzione.md`: produttori, costi, dogana, regole, KiCad;
- `architettura-una-per-una.md`, `architettura-scheda-madre.md`, `architettura-integrazione.md`: le tre proposte.

**Niente è approvato né comprato.** Ogni voce nuova è una proposta. Il CAD, la guida e i documenti esistenti non sono stati toccati.

- Quote in mm nella terna del robot: X avanti, Y a sinistra, Z in alto, origine al centro del corpo sul piano dei femori.
- Stato di ogni dato: **V** verificato (fonte primaria o modello CAD), **S** stimato (calcolo, catalogo non riletto, proposta), **C** da confermare (sul pezzo, nel CAD, nel preventivo o con l'utente).
- Il CAD di oggi è la 2.1.6. La 2.1.7 è in bozza (`docs/piano-v2.1.0.md:343-566`).

## In breve

1. **Due schede**, il minimo possibile, perché il carapace si toglie staccando una sola spina (R-02, `requisiti.md:217`):
   - la **scheda madre (SM)**, al posto della basetta dell'ESP32 sul vassoio;
   - la **scheda del carapace (SC)**, sotto il dorso.
2. **La SM assorbe** la basetta, la striscia dei partitori, l'ADC, il traslatore e le prese dei piedi e delle luci. Il corpo della scheda resta 56 × 35 alle quote di oggi; ci sono in più due orecchie per i fili e due ali per le prese. È l'idea di `architettura-scheda-madre.md`, con alcune correzioni (capitolo 1.4).
3. **La SC** resta nell'inviluppo della 2.1.7. Cambia il supporto: rame al posto di fili e ponticelli. In più ha una presa Qwiic vera e un posto predisposto per l'espansore.
4. **Spariscono** due moduli (traslatore KAmod e ADS7830 Adafruit), la terza millefori e circa 120 fili e ponticelli. Le saldature della sezione 4 scendono da 6–7 ore a circa 3,5–4,5, scheda del carapace compresa [S].
5. **Restano moduli** l'ESP32 (estraibile), il regolatore 5 V, gli INA260, l'IMU, i ToF, i microfoni, l'amplificatore e l'espansore TCA9534. Il firmware non cambia: stessi GPIO, stessi indirizzi I2C.
6. **Si fa in due serie.**
   - **Prima serie (r1)**: schede nude a 2 strati, componenti a reoforo, SMD da 0805 e un solo chip a passo fine (l'ADC). Netto per il robot circa 14–30 € tutto a mano, 27–36 € se JLCPCB monta gli SMD [S]. Servono 3–6 settimane dall'inizio del disegno.
   - **Serie definitiva (r2)**: dopo la prova della r1 sul robot. Corregge gli errori trovati e, se l'utente vuole, aggiunge le idee di `architettura-integrazione.md`: montaggio completo, spine con chiave, chip al posto di altri moduli.
7. **CAD**: una versione dopo la 2.1.7. Si aggiungono due colonne della base sotto le ali e il componente della SM. La 2.1.7 si fa com'è, perché la millefori resta l'alternativa. **[corretto dalla verifica]** Le colonne proposte non convivono con l'ADC e l'asola della 2.1.7 (+Y) né con le sedi delle prese: la base va in due varianti, e il PTC cerca un posto fuori dall'ala −Y (capitoli 1.4, 2.1, 2.2).
8. **Quattro domande per l'utente** (capitolo 8): chi salda gli SMD, le prese sulle ali, il banco S1 sulla r1 o sulla millefori, KiCad 10.

## 1. Raccomandazione

### 1.1 Quante schede, quali, dove

| Scheda | Dove | Sagoma | Cosa fa | Fonte |
|---|---|---|---|---|
| **SM, scheda madre** | sul vassoio, al posto della basetta, sotto l'ESP32; z 5,9…7,5 | corpo 56 × 35 (x 22…78, \|y\| ≤ 17,5) più due orecchie di coda e due ali laterali: inviluppo 56 × 52, circa 25,6 cm² | zoccolo dell'ESP32, regolatore 5 V, buffer dei LED e della TX, partitore della RX, pull-up del bus, ADC con gli 8 partitori, prese dei piedi, delle luci e delle NTC, partenza di tutti i fili del corpo | S; `architettura-scheda-madre.md:47-54` |
| **SC, scheda del carapace** | sotto il dorso, davanti all'ottagono; faccia alta a z 30,9 | circa 23 × 30, \|y\| ≤ 15, come la 2.1.7 | testata 2 × 8 a 90° verso la SM, condensatore della catena LED, presa Qwiic, piazzole dei moduli del carapace | S; `piano-v2.1.0.md:473-489`; `requisiti.md:197` |

### 1.2 Perché questa, e non le altre

| | Una per una | Scheda madre | Integrazione | **Raccomandata** |
|---|---|---|---|---|
| Schede | 3 (basetta, carapace, partitori) | 2 | 3 (logica, sensori, carapace) | **2** |
| Moduli che spariscono | nessuno | KAmod, ADS7830 | KAmod, ADS7830, TCA9534, MAX98357A, GY-6500 (opzione) | **KAmod, ADS7830** |
| Montaggio | a mano | a mano o SMD da JLCPCB | tutto da JLCPCB | **a mano o SMD da JLCPCB** (domanda 1) |
| Cambi al CAD | due bugne per i partitori | colonne delle ali, componente nuovo | vano, carapace, spine sui bordi | **colonne delle ali, componente nuovo** |
| Costo netto per il robot [S] | 10–20 € | 14–36 € | circa 100–110 € | **14–36 €** |
| Punteggio dell'autore (su 30) | 24 | 22 | 19 | — |
| Fonte | `architettura-una-per-una.md:305-318` | `architettura-scheda-madre.md:462-473` | `architettura-integrazione.md:417-430` | capitoli 2-5 |

La una per una ha il punteggio più alto perché non tocca il CAD. Raccomando la scheda madre per quattro motivi:

- **Meno componenti**, che è la preferenza dell'utente. La SM toglie due moduli e una scheda. La una per una li tiene tutti: il KAmod, il modulo ADC con i suoi 8 fili verso la striscia, e una terza scheda da fissare.
- **Chiude problemi che le altre lasciano aperti.** Le prese dei piedi e delle luci non hanno ancora un supporto disegnato (P-012, `requisiti.md:145`): sulle ali della SM le spine sono saldate sulla scheda. La striscia dei partitori non ha un posto dimostrato nel CAD (S-28, S-29, `requisiti.md:112`): sulla SM sparisce.
- **Costa come la una per una** al netto dei moduli che non si comprano (`architettura-scheda-madre.md:347-351`). La integrazione costa da 3 a 7 volte tanto e non si ripara con il saldatore (`architettura-integrazione.md:425-427`).
- **Il costo della una per una sul CAD non è zero**: le due bugne dei partitori vanno disegnate comunque (`architettura-una-per-una.md:247`).

Il punto debole della SM è il CAD: le ali hanno margini di 1–2 mm verso il servo di coxa anteriore e le colonnine del carapace, e le spine arrivano a 4 mm dal carapace (`architettura-scheda-madre.md:58-61`). Per questo la prima cosa da fare nella versione del CAD è la verifica delle ali, con due ripieghi in ordine:

1. **SM senza ali**: corpo e orecchie come sopra. Le prese restano sul tetto e i loro fili si saldano su piazzole della SM. P-012 resta da risolvere.
2. **Una per una**: tre schede con la sagoma di oggi (`architettura-una-per-una.md`).

### 1.3 Due serie

| | Prima serie, r1 | Serie definitiva, r2 |
|---|---|---|
| Quando | nella versione dopo la 2.1.7, con l'utente | dopo la r1 provata sul robot (banco S1 e almeno P4) |
| Scopo | togliere le millefori senza cambiare il circuito; provare impronte, ingombri e schema | correggere gli errori della r1; rendere la SM smontabile senza saldatore, se l'utente lo vuole |
| Montaggio | THT e 0805 a mano; ADC in TSSOP-16 a mano o montato da JLCPCB | a mano come la r1, oppure tutti gli SMD da JLCPCB |
| Cosa può aggiungere | — | prese XH con chiave per 2813, seriale e abilitazione; seconda testata 2 × 8 per staccare il cavo piatto anche dalla SM; TCA9534 come chip; amplificatore come chip sulla SC allungata fino a x 70; PTC in 1812. Ognuna è una scelta separata (`architettura-integrazione.md:110-133`, `:147-204`) |
| Cosa non cambia | GPIO, indirizzi I2C, piedinatura del cavo a 16 poli, quote verticali | idem |

Il regolatore 5 V resta un modulo anche nella r2. Un convertitore da 2,5 A disegnato sotto l'ESP32 è il pezzo più rischioso, e prima va misurato il calore in P4 (`architettura-integrazione.md:135-137`; `requisiti.md:235`).

### 1.4 Correzioni e scelte rispetto alle tre proposte

| Punto | Proposta | Scelta qui | Perché | Stato |
|---|---|---|---|---|
| Misura RMT al banco su GPIO38 | integrazione: canale 4 dell'AHCT125 verso GPIO38 (`architettura-integrazione.md:84`) | **partitore** da due 0805 non montate, con un ponticello a saldare verso GPIO38 | l'AHCT125 alimentato a 5 V dà 5 V in uscita: su GPIO38 viola R-09. Gli impulsi della SSC-32 sono a 5 V e vanno abbassati come la RX | S |
| Partitore della RX (SSC-32 → GPIO14) | 10 k / 20 k, cioè 3,33 V (scheda madre, `:160`); 2,2 k / 3,3 k (integrazione, `:105`); 10 k / 15 k (una per una, `:168`) | **10 kΩ / 15 kΩ**: 3,0 V con 5,0 V in ingresso, 2,76 V con 4,6 V | 3,33 V sta al limite dell'alimentazione dell'ESP32. 3,0 V restano sopra la soglia alta di 2,5 V (0,75 × 3,3) | S; la tensione d'uscita della SSC-32 va misurata (C, S-22) |
| Modifica 8 della 2.1.7 (asola del bus con l'ala del vassoio) | la scheda madre la salta (`:357`) | **resta** | la millefori resta l'alternativa della guida: la 2.1.7 si fa com'è e la versione con la PCB aggiunge solo cose. **[corretto dalla verifica]** Con la colonna +Y a (47,5; 20,5) la modifica 8 non convive: l'asola (x 46,5…53,5, y 18…22) e l'ala del vassoio (fino a circa y 23,5, z 1,0…2,6) stanno dentro la colonna Ø6 (x 44,5…50,5, y 17,5…23,5, z −9,4…5,9) (`piano-v2.1.0.md:424-431`). O si sposta la colonna (riga sotto), o l'ala +Y della SM si appoggia su una colonnina dell'ala del vassoio invece che sulla base | S |
| Bugne dell'ADC e sedi delle prese nella base | la scheda madre le toglie (`:362`) | **restano**, se la verifica trova posto per le colonne delle ali | servono alla strada con le millefori; sotto la SM non danno fastidio. Con la colonna a (47,5; ±20,5) l'angolo della sede (48,25; ±22,1) entra di circa 1,2 mm nella colonna Ø6: va spostata una delle due, oppure si fanno due varianti della base con un parametro di `corpo.py`. **[corretto dalla verifica]** La colonna +Y tocca anche il modulo ADC della strada con le millefori (y fino a 18,45 fra x 39 e 69,5; la colonna parte da y 17,5), oltre all'asola della modifica 8. Con ADC, sedi delle prese, colonnine del carapace e asola al loro posto, una colonna Ø6 resta fuori da tutto solo verso x 67-68 (+Y fra ADC e sede dei piedi, −Y oltre la sede delle luci, che arriva a x 64,95), a margine zero e in punta d'ala: la base unica per le due strade è improbabile, e la variante con il parametro è la strada di partenza | S, conto mio, ricontrollato sulle mesh 2.1.6 (`build/guida/cad/mesh/`, manifest): colonna +Y contro ADC, sede e base: si toccano; C nel CAD |
| Pull-up 3V3 e regolatore X3 | ponticello J1 più piazzole di X3 (scheda madre); ponticello a tre vie (integrazione) | **ponticello a tre piazzole**: al centro il 3V3S, ai lati il 3V3 dell'ESP32 o l'uscita di X3 | "mai J1 e X3 insieme" (D-076) diventa più difficile da sbagliare: si chiude un lato solo. **[corretto dalla verifica]** Non è impossibile per costruzione: una goccia di stagno su tutte e tre le piazzole unisce le due uscite. Serve la serigrafia ("un lato solo") e la prova al multimetro fra le due piazzole esterne (aperto) | S |
| TCA9534 | modulo sulla presa Qwiic (scheda madre); chip (integrazione) | **modulo nella r1** (X20, già in arrivo), più un'**impronta SOIC-16 non montata** sulla SC | costo zero oggi; se il modulo non trova posto (S-17) si monta il chip, che si salda a mano a passo 1,27 | S |
| Cavo piatto sulla SM | griglia 3 × 5 nell'orecchia −Y (scheda madre); due file sfalsate (una per una) | **griglia nell'orecchia −Y** | tiene i poli a 5 V lontani dai pin dell'ESP32 (R-09) | S |

## 2. Scheda madre (SM)

### 2.1 Sagoma, fori, posizione

```
 y +26                    ┌───── ala +Y ─────┐
 y +25   ┌─ orecchia ─┐   │ spine: 6 FSR,    │
         │ +Y: 2813,  │   │ NTC sinistra     │
         │ ENA, seriale│  │                  │
 y +17,5 ├────────────┴───┴──────────────────┴─────────┐
         │   corpo: come la basetta, sotto l'ESP32     │ x ≥ 74
         │   (file dei pin a |y| 12,7)                 │ niente rame
 y −17,5 ├────────────┬───┬──────────────────┬─────────┘ (antenna)
         │ orecchia −Y│   │ spine: 6 luci,   │
 y −25   └ cavo piatto┘   │ NTC destra, PTC  │
 y −26                    └───── ala −Y ─────┘
        x 22  22,5  35,5  44,5               68,5      78
```

Pianta vista dall'alto, non in scala (`architettura-scheda-madre.md:31-45`). **[corretto dalla verifica]** Il PTC sull'ala −Y non ci sta: vedi Z4 qui sotto e PTC1 in 2.2.

| Dato | Valore | Stato, fonte |
|---|---|---|
| Corpo | x 22…78, \|y\| ≤ 17,5, z 5,9…7,5, spessore 1,6 come la basetta | V; `requisiti.md:158`; R-03 |
| Orecchie di coda | x 22,5…35,5, \|y\| 17,5…25: fra la SSC-32 (fino a x 22) e la colonnina del carapace (da x 36,3) | S; `architettura-scheda-madre.md:50` |
| Ali | x 44,5…68,5, \|y\| 17,5…26: sopra le sedi delle prese di oggi; il camino dei regolatori (\|y\| 27…33,4) resta libero | S; `architettura-scheda-madre.md:51` |
| Fori | 4 × Ø2,2 non metallizzati sulle colonnine del vassoio, a (29; ±6,8) e (75,5; ±6,5), M2 × 5; **2 × Ø2,2 in più**, uno per ala, su colonne nuove della base (proposta a (47,5; ±20,5), da spostare: tocca le sedi delle prese e, sul lato +Y, ADC e asola della 2.1.7, capitolo 1.4). **[corretto dalla verifica]** Senza rame: sulla faccia alta l'impronta della testa (Ø4) più 1 mm, cioè Ø6 (`produzione.md:190`); sulla faccia bassa l'appoggio della colonnina (Ø5,8) più 1 mm, come le zone vietate di oggi (`schemi.md:33-36`). Prima diceva un anello di 1 mm attorno al foro, cioè Ø4,2: più piccolo della testa | V colonnine (`requisiti.md:159`); S colonne nuove, C nel CAD |
| Faccia dei componenti | in alto, verso l'ESP32; sotto restano 3,3 mm fino al vassoio (2.1.7) | V 2.1.6, bozza 2.1.7 (`requisiti.md:160`) |
| Altezze libere | 8,5 sotto l'ESP32, 6,6 sotto la sede della microSD (x 22,5…37,5, \|y\| ≤ 7), meno i componenti sul retro dell'ESP32 (S-08); spine delle ali fino a circa z 24,5, contro il carapace a z 28,4 | S; `architettura-scheda-madre.md:91-100` |
| Zona dell'antenna | x 74…78: niente rame su nessuna faccia, solo i fori delle colonnine anteriori | S, regola generale dei moduli con antenna stampata, non riletta su Espressif (R-15) |
| Vicinanze | servo di coxa anteriore a circa 1,9 dall'angolo dell'ala; colonnina del carapace a 0,8; INA260 a 4 dalle orecchie | S, stime sul manifest 2.1.6 (`architettura-scheda-madre.md:58-61`); C con la verifica d'interferenza |

Zone di montaggio (`architettura-scheda-madre.md:67-73`):

| Zona | Quote | Cosa ci va |
|---|---|---|
| Z1, sotto l'ESP32 | x 22…74, \|y\| ≤ 11,4 | U2, U3, U5, D1, D2, resistenze e condensatori 0805, ponticelli. Occupazione circa 62 % con U3 in SOIC, 75 % in DIP [S] |
| Z2, strisce fuori dall'ombra dell'ESP32 | \|y\| 14,2…17,5 | +Y: partitori, piazzole del ToF frontale; −Y: piazzole di IMU e INA260 destro; punti di prova |
| Z3, orecchie | come sopra | +Y: 2813, abilitazione, seriale, INA260 sinistro; −Y: cavo piatto |
| Z4, ali | come sopra | spine; PTC sull'ala −Y. **[corretto dalla verifica]** Il PTC non ci sta: l'ala è lunga 24 (x 44,5…68,5); 7 posti a passo 2,54 occupano 17,8 e le spine coprono tutta la larghezza utile in Y (\|y\| 18,2…25,9 su 17,5…26); il foro della colonna con la testa (Ø6 senza rame) prende altri 6. Restano circa 0, contro i 3,0 di spessore del MF-R075 (`schemi.md:48`) più i 3 mm liberi chiesti in 2.5. Posto del PTC da decidere: vedi PTC1 in 2.2 |
| Z5, antenna | x 74…78 | niente |

### 2.2 Componenti

| Sigla | Cosa | Contenitore | Voce, stato | Note |
|---|---|---|---|---|
| U1 | ESP32-S3-CAM UICPAL N16R8 RE1.3 su 2 strip femmina 1 × 20 | THT, file a 25,4 | A2, C2: in casa | resta estraibile (R-01); file a 25,4 solo dopo la prova a secco (P-005) |
| U2 | Pololu D24V22F5, 5 V 2,5 A | modulo THT, 5 pin in fila | B2: approvato | resta modulo; sotto solo solder mask, senza Kapton; ordine dei pin da leggere (S-03, C) |
| U3 | SN74AHCT125, 4 canali | **SOIC-14** (DIP-14 di ripiego) | X9 in DIP approvato; SOIC **nuovo** | canale 1: anello e lobi; 2: luci delle tibie; **3: TX verso la SSC-32** (al posto del KAmod); 4: libero, ingresso a massa |
| U5 | ADS7830IPW, ADC a 8 canali, 0x48 (A0 e A1 a massa) | TSSOP-16, passo 0,65 | **nuovo**, al posto di X6 | VDD e REF dal 3V3S, che alimenta anche i partitori: lettura in rapporto (R-05); funzionamento del REF da rileggere sulla scheda TI (C). **[corretto dalla verifica]** COM a massa (ingressi riferiti a massa), come sul modulo Adafruit (`schemi.md:431`; `docs/ricerca/dati-moduli.md:62`) |
| D1 | Schottky fra 5V_REG e pin 5V dell'ESP32 | 1N5819 THT | C3: approvato | la USB non alimenta il resto (R-11, S-07) |
| D2 | 1N4148 sull'abilitazione | THT | già nello schema | entra sulla scheda; le R3 restano su ogni regolatore (R-12) |
| PTC1 | fusibile ripristinabile del 5 V dei LED | radiale in piedi sull'ala −Y, a più di 8 mm dall'ESP32 | X9 (MF-R075): approvato | impronta adatta anche a MF-R090 o MF-R110: il valore si decide con S-06 dopo P4 [S, catalogo Bourns non riletto]. **[corretto dalla verifica]** Sull'ala −Y non c'è posto (Z4 in 2.1); nell'orecchia −Y c'è la griglia del cavo piatto (11,9 × 6,8 su 13 × 7,5) e Z2 sta a meno di 3,4 mm dall'ESP32. Strade possibili, da scegliere nel disegno: PTC in linea fuori dalla scheda (alternativa di S-08); ala −Y con 6 posti e la NTC destra su piazzole; PTC SMD 1812 della r2 già nella r1 (voce nuova) |
| R1 | 10 kΩ, pull-down di GPIO48 | 0805 | — | come oggi |
| R2, R9 | 330 Ω, dato verso il carapace e verso le tibie | 0805 | — | R9 entra sulla scheda (oggi è nella guaina) |
| R4, R5 | pull-up di SCL e SDA, **3,3 kΩ** | 0805 | — | senza la resistenza del modulo ADC l'equivalente torna a 1,25–1,42 kΩ, nella finestra 1,0–1,4 (S-13) [S; `architettura-scheda-madre.md:178`] |
| R7 | 47 kΩ 1 %, lato basso del partitore della batteria | 0805 | — | R6 resta alla 2813 (R-12) |
| R10 | 10 kΩ, pull-up all'ingresso del canale 3 | 0805 | — | tiene la TX a riposo mentre l'ESP32 si avvia |
| R11, R12 | 10 kΩ e 15 kΩ, partitore della RX | 0805 | — | capitolo 1.4 |
| R13, R14, JP-RMT | partitore e ponticello verso GPIO38 | 0805, **non montate**; ponticello aperto | — | misura RMT al banco in P2 (`requisiti.md:254`) |
| RP1–RP8 | 10 kΩ 1 %, partitori di FSR e NTC | a reoforo in piedi in Z2 +Y se si salda a mano; 0805 se monta JLCPCB | X5, X14: approvate | |
| CP1–CP8, CS1, CS2, CU5 | 100 nF: partitori, GPIO1, U3, U5 | 0805 | B8: in casa (taglia da guardare, S-30) | CU5 oggi sta sul modulo ADC |
| JP-3V3 | ponticello a tre piazzole: 3V3 dell'ESP32 o X3 → 3V3S | rame | — | chiuso verso l'ESP32; X3 si collega senza ridisegnare (R-17) |
| JF, JL | spine delle ali: 7 posti × 3 file per lato | strip maschio 2,54 in piedi | come le prese di oggi (X5, X31) | posto 7: NTC, senza il pin centrale |
| TP | punti di prova | piazzole nude Ø1,5 | — | capitolo 2.5 |

Parti attive: 2 moduli (ESP32, regolatore) e 2 integrati (buffer, ADC). Oggi sono 4 moduli e 1 integrato (`architettura-scheda-madre.md:195`).

### 2.3 Connettori e piazzole

**Strip dell'ESP32.** Pin usati, 15 su 40 (`schemi.md:93`; `piano-elettronica-software.md:79-105`):

| Pin | Rete | Verso |
|---|---|---|
| 5V | 5V_ESP, dopo D1 | U2 |
| 3V3 | 3V3 dell'ESP32 | JP-3V3 → 3V3S |
| GND | massa | piano |
| GPIO1 | SENSE (R7, CS1) | 2813, lato alto R6 |
| GPIO2 | AMP, dati verso l'amplificatore | cavo piatto, polo 13 |
| GPIO3, GPIO47 | SCL, SDA | pull-up, rami del bus, poli 6 e 8 |
| GPIO14 | RX3, dal partitore R11/R12 | TX della SSC-32 |
| GPIO21 | TX3, verso il canale 3 di U3 | RX della SSC-32 |
| GPIO38, 39, 40 | BCLK, WS, MIC | poli 10, 11, 12; GPIO38 anche JP-RMT |
| GPIO41 | OFF | 2813 |
| GPIO42 | abilitazione, poi D2 | ENA dei D42V110F6 |
| GPIO48 | LED_IN, con R1 | canali 1 e 2 di U3 |

Il pin 5V della scheda è accanto a GPIO14 (piedinatura Freenove, S sulla UICPAL): la pista del 5 V esce dal lato opposto (`architettura-integrazione.md:232`). **[corretto dalla verifica]** Dal lato opposto c'è il bordo di coda: fra la piazzola del pin (bordo a x 22,9) e il bordo della scheda (x 22) restano 0,9 mm, meno 0,5 di distanza dal bordo. La pista esce verso l'interno, in Z1, perpendicolare alla fila, e resta a 0,84 mm dalla piazzola di GPIO14 come oggi.

Un foro della fila +Y di un pin non usato (P-2 della basetta di oggi) è **non metallizzato**, per far passare la pista del VBAT verso U2 (`architettura-una-per-una.md:43`). **[corretto dalla verifica]** Un posto solo non basta: fra le piazzole O-2 e Q-2 (Ø1,7, `produzione.md:189`) restano 3,4 mm con il foro di P-2 in mezzo, cioè due varchi da 1,2 mm, contro 1,5 di pista più 1 mm per lato (2.5). Servono **due posti vicini senza foro e senza contatto**, per esempio O-2 e P-2 (GPIO7 e GPIO6, non usati): i due contatti si sfilano dalla strip femmina e fra N-2 e Q-2 restano 5,9 mm. Lo stesso vale per ogni pista a 5 V che attraversa una fila (2.5, "5 V e GPIO").

**Piazzole e spine verso il resto.** Fili saldati come oggi, salvo le spine delle ali: un connettore in più è un componente in più, e la r1 non ne aggiunge (`architettura-scheda-madre.md:249`).

| Gruppo | Zona | Poli, nell'ordine | Filo, altro capo | Stato |
|---|---|---|---|---|
| 2813 | orecchia +Y | VBAT, GND, SENSE, OFF; accanto a VBAT un posto vuoto | 4 × 26 AWG (VBAT siliconico se c'è, S-27), saldati sulla 2813; circa 25 cm | V reti (`requisiti.md:61-64`); S posizione |
| Abilitazione | orecchia +Y | ENA, dopo D2 | 26 AWG, poi due rami ai D42V110F6 con R3 | V |
| Seriale | orecchia +Y | TX5 (5 V dal canale 3), RX5 (verso il partitore), GND | 3 × 26 AWG, Dupont femmina (C4) sulla SSC-32; il GND si lascia vuoto se la misura dice doppia massa (S-22) | V reti; C massa |
| INA260 sinistro | orecchia +Y | GND, 3V3S, SDA, SCL (ordine Qwiic) | cavo Qwiic tagliato (X1) | V |
| INA260 destro, IMU | Z2 −Y | GND, 3V3S, SDA, SCL, due gruppi | Qwiic tagliato; 30 AWG verso la GY-6500 | S |
| ToF frontale | Z2 +Y | GND, 3V3S, SDA, SCL | 30 AWG lungo la torretta | S |
| Riserva del bus | Z2 +Y | GND, 3V3S, SDA, SCL | per X15, X32, X33 | S |
| Cavo piatto | orecchia −Y, griglia 3 × 5 a passo 2,54 | poli 1–14: 1-2 +5V_LED, 3 GND, 4 DATA (dopo R2), 5 GND, 6 SCL, 7 3V3S, 8 SDA, 9 GND, 10 BCLK, 11 WS, 12 MIC, 13 AMP, **14 su una piazzola** (riserva, X25). I poli 15-16 si separano prima della scheda e vanno ai pin A e B della 2813, come oggi | cavo IDC 16 vie, circa 15 cm, spina con chiave sulla SC | V piedinatura (`requisiti.md:92`; `cablaggio.md:132-143`) |
| Spine dei piedi, JF | ala +Y | posti 1–6: FSR AS, MS, PS, AD, MD, PD (canali 0–5); posto 7: NTC sinistra (canale 6). Segnale e massa, fila centrale senza pin | femmine JR delle zampe e della NTC | S ordine; C misura della spina JR (P-012) |
| Spine delle luci, JL | ala −Y | posti 1–6: massa, +5V_LED, DATA2 (dopo R9), come un servo; posto 7: NTC destra (canale 7), senza pin centrale | femmine JR delle luci delle tibie | S |

Le spine delle ali non hanno chiave. Girate di 180° non fanno danni: FSR e NTC sono resistenze; sulle luci massa e dato si scambiano e il buffer vede circa 14 mA attraverso R9 (`architettura-scheda-madre.md:269-273`). Contromisura: zampa, canale e colore della massa in serigrafia, e la prova al multimetro della guida.

### 2.4 Schema a blocchi

```
 F2 2 A ─ 2813 (R6 100 kΩ, 100 kΩ su OFF) ── VBAT, GND, SENSE, OFF ──┐
 ┌──────────────────────────── SM, scheda madre ──────────────────────┼────────────────────────┐
 │ [orecchia +Y] VBAT ─ U2 D24V22F5 ─ 5V_REG ─┬─ D1 ─ 5V_ESP ─ pin 5V   U1 ESP32-S3-CAM       │
 │                                            ├─ U3 VCC                                        │
 │                                            └─ PTC1 ─ 5V_LED ─┬─ [cavo piatto, poli 1-2]    │
 │                                                              └─ [ala −Y: +5 V delle luci]  │
 │ 3V3 ESP32 ─┐                                                                                │
 │ X3 (vuoto) ┴─ JP-3V3 ─ 3V3S ─┬─ R4, R5 ─ SDA, SCL ─ [rami del bus] [poli 6, 7, 8]           │
 │                              └─ U5 ADS7830 (VDD = REF) ─ 8 partitori ─ [JF: 6 FSR, NTC S]   │
 │                                                                       [JL posto 7: NTC D]  │
 │ GPIO48 ─ R1 ─ U3 can. 1 ─ R2 ─ [polo 4]                                                    │
 │                U3 can. 2 ─ R9 ─ [JL: dato delle 6 luci]                                     │
 │ GPIO21 ─ R10 ─ U3 can. 3 ─ [RX della SSC-32]                                               │
 │ GPIO14 ─ R11/R12 ──────── [TX della SSC-32]      GPIO38 ─ JP-RMT ─ R13/R14 (vuote, banco)  │
 │ GPIO1 ─ R7, CS1 ─ [SENSE]   GPIO41 ─ [OFF]   GPIO42 ─ D2 ─ [ENA] ─ R3 su ogni D42V110F6    │
 │ GPIO38-40, GPIO2 ─ [poli 10-13]                  polo 14 ─ [piazzola di riserva]           │
 └────────────────────────────────────────────────┬───────────────────────────────────────────┘
                                                  │ cavo piatto 16 vie, poli 15-16 alla 2813
                                                  ▼ SC
```

Reti e GPIO uguali a oggi (`schemi.md:62-91`). Cambiano tre cose (`architettura-scheda-madre.md:158-161`):

- la TX esce dal canale 3 del buffer: con il buffer a 5 V i 3,3 V bastano come livello alto (soglia TTL di 2 V) e l'uscita è a 5 V pieni [S, scheda TI non riletta]. La soglia della seriale del clone non conta più;
- la RX passa dal partitore;
- l'ADC è un chip sulla scheda.

### 2.5 Strati, piste, punti di prova

| Voce | Scelta | Fonte |
|---|---|---|
| Strati | 2, 1,6 mm, rame 1 oz, HASL senza piombo. Sopra componenti e piste di potenza, sotto un riempimento di massa intero, interrotto solo per x ≥ 74 | `produzione.md:278`; le correnti dei servo non passano sulle schede (`produzione.md:19`). **[corretto dalla verifica]** Vale solo se la massa della seriale non chiude un secondo giro: se sul clone VL− e la massa dei servo sono comuni, con il Dupont di massa una parte del ritorno dei servo passa per il riempimento della SM e i 26 AWG di seriale e 2813 (S-22). Finché S-22 non è misurato, la piazzola di massa della seriale resta vuota |
| VBAT | pista da **1,5 mm**, isola sola fra la piazzola dell'orecchia e il VIN di U2, sul lato inferiore nel varco del foro non metallizzato; **1 mm** da ogni altro rame, massa compresa. **[corretto dalla verifica]** Il varco è di due posti senza foro, non di un foro non metallizzato (2.3) | 2,3 A con il pacco a 6 V, 3 A se F2 sale a 3 A; 1,37 mm per 3 A a +10 °C (`produzione.md:171`) [S] |
| 5V_REG | 1,5 mm o area di rame, da U2 a D1, PTC1, U3 | 2,5 A, limite di U2 |
| 5V_LED | 1,0 mm, dal PTC alle piazzole dei poli 1-2 e all'ala −Y | 0,86 A di esercizio (S-06) |
| 5V_ESP | 0,6 mm | 0,25/0,5 A |
| 3V3S | 0,5 mm | circa 0,2 A |
| Segnali | 0,25 mm; pista e spazio minimi 0,20; via 0,3 / 0,6; rame a 0,5 dal bordo | `produzione.md:185-191` |
| Masse | piano sotto; stella sul GND di U2; i ritorni dei LED (poli 3, 5, 9, massa delle luci) arrivano con una pista da 1,5 mm fino al GND di U2, senza passare sotto i pin dell'ESP32, l'ADC o i partitori | `requisiti.md:233`; `architettura-una-per-una.md:217` |
| 5 V e GPIO | nessuna piazzola o pista a 5 V a meno di 1 mm da un pin dell'ESP32 senza massa in mezzo (R-09). **[corretto dalla verifica]** Con U2 e U3 in Z1, fra le due file, le reti a 5 V devono attraversare una fila per uscire: TX5 verso l'orecchia +Y; DATA verso l'orecchia −Y; DATA2 e il 5 V verso l'ala −Y (o verso il PTC, dovunque vada); il VBAT entra dalla fila +Y. Fra due piazzole vicine (0,84 mm di vuoto) la regola non si rispetta e non ci sta una massa. Ogni attraversamento a 5 V passa quindi da un varco di posti senza foro, come il VBAT (2.3). Posti non usati vicini: fila +Y C…H, J…R; fila −Y B-C, G-H, I-J-K, S-T (`schemi.md:93`). Il partitore della RX (R11, R12) va nell'orecchia +Y, così attraversa solo il segnale a 3,0 V | `architettura-scheda-madre.md:306` |
| Analogico | ADC e partitori lontani da U2; piste dei partitori corte, sopra, con la massa sotto | `requisiti.md:244` |
| Serigrafia | "HEX2 SM r1" e la data; "LATO COMPONENTI" e la freccia verso la testa; pin 1, polarità di D1, D2 e PTC1; nome di ogni piazzola; zampa e canale su ogni spina | `produzione.md:251`, `:260` |

**Punti di prova**, tutti fuori dall'ombra dell'ESP32 (\|y\| > 14,15), quindi raggiungibili con l'ESP32 inserito: VBAT, 5V_REG, 5V_LED, 3V3S, due masse, SDA, SCL, TX5, RX3 (dopo il partitore), DATA, DATA2, SENSE, ENA, OFF. Il 5V_ESP si misura nella presa della strip, come oggi. Le prove 1–20 della guida (`schemi.md` 1.5) si rifanno su questi punti.

## 3. Scheda del carapace (SC)

### 3.1 Sagoma, fori, posizione

| Dato | Valore | Stato, fonte |
|---|---|---|
| Sagoma | circa 23 × 30, \|y\| ≤ 15, allungata verso la coda (x circa 26,5…49,5): in avanti toccherebbe l'amplificatore, che parte da x 51,85 | S; `requisiti.md:197-198`; la 2.1.7 decide il verso (C) |
| Piano | faccia alta a z 30,9, componenti in basso; 3,5 di aria fino al dorso (z 34,4) | V; `requisiti.md:190-192` |
| Fori | 4 fori non metallizzati Ø2,2 sulle bugne Ø5,5 della 2.1.7, con le due di coda spostate davanti alla testata (x ≥ 41,5). Sulla PCB non c'è la griglia da 2,54: non servono i fori allargati a Ø2,6 della millefori | V bugne di oggi (`fori.json` `ins_sch_*`); C posizioni della 2.1.7 |
| Sotto | 11,7 fino all'ESP32; 9,7 sul connettore del flat della camera (x 40,75…45,25) | S; `requisiti.md:193` |
| Aperto della 2.1.7 | il fondo della spina orizzontale (z 20,3) sta 0,6 sotto la cima della USB-C nel tratto x 17,5…20,1. **[corretto dalla verifica]** Quel tratto vale con il bordo di coda a x 29,5 (`bloccanti-arresto2.md`, P-002). Con la scheda allungata verso la coda, come qui (bordo a x 26,5), la spina da 10-12 arriva a x 14,5-16,5 e il tratto sopra la USB-C (x 12,7…20,1, fino a z 20,9) diventa x 14,5…20,1: il conflitto si allunga da 2,6 a circa 5,6 mm. Il verso dell'allungamento e la spina vanno decisi insieme | S; `requisiti.md:198` |

La SC prende sagoma e fori dalla 2.1.7, come chiede `piano-v2.1.0.md:475`.

### 3.2 Componenti

| Sigla | Cosa | Contenitore | Voce, stato | Note |
|---|---|---|---|---|
| J2 | testata 2 × 8 a 90° con chiave, sul bordo di coda | THT | X2 (Würth 61201621721): approvata, non comprata | codice e chiave da confermare sul disegno (S-26, C) |
| CE1 | 470 µF 10 V, Ø6,3 × al più 8 | radiale sdraiato | X2: approvato | D-076 |
| JQ | presa Qwiic JST SH 4 poli orizzontale (SM04B-SRSS-TB) | SMD, passo 1,0 | **nuova**, al posto del cavo 4210 tagliato | si salda a mano con il flussante (`produzione.md:136`) |
| U6 | TCA9534, 0x20 (A0–A2 a massa; **non** la variante "A", 0x38) | SOIC-16, **non montato** nella r1 | — | predisposizione: si monta se il modulo X20 non trova posto (S-17) |
| R-MIC | pull-down della linea dei microfoni | 0805, **non montata** | — | valore da decidere al banco con il pull-up da 10 kΩ della scheda su GPIO40 (S-21) |
| TP | 5V, 3V3, GND, SDA, SCL, DATA | piazzole nude Ø1,5 | — | prove di 13.18 |

R8 da 100 kΩ resta al microfono (`schemi.md:261`).

### 3.3 Connettori e piazzole

| Gruppo | Poli, nell'ordine | Verso | Filo | Fonte |
|---|---|---|---|---|
| J2 | 1-2 +5 V, 3 GND, 4 DATA, 5 GND, 6 SCL, 7 +3,3 V, 8 SDA, 9 GND, 10 BCLK, 11 WS, 12 MIC, 13 AMP, 14 riserva, 15-16 pulsante; tacca dal lato dei poli dispari | SM | cavo piatto, spina IDC Würth 61201623021 con chiave | V; `requisiti.md:84`, `:92` |
| Catena LED | +5 V, DATA, GND | anello del pulsante, poi i lobi | 3 × 30 AWG (X31) | V; `requisiti.md:99` |
| Microfoni | 3V3, GND, BCLK, WS, MIC | due MS3625 uniti fra loro | 5 × 30 AWG, circa 8 cm | V; `requisiti.md:100` |
| Amplificatore | +5 V, GND, BCLK, WS, AMP | modulo MAX98357A | 5 × 30 AWG | V; `requisiti.md:101` |
| ToF posteriore | 3V3, GND, SDA, SCL, XSHUT | VL53L1X; XSHUT dal TCA9534 | 5 × 30 AWG, circa 20 cm | V; `requisiti.md:102` |
| Pulsante | BTN_A, BTN_B (poli 15-16) | pulsante Ø12 | 2 × 26 AWG | V; `requisiti.md:103` |
| Riserva | polo 14 | XSHUT del ToF del mento (X25) | — | S |
| JQ | GND, 3V3, SDA, SCL (ordine Qwiic) | modulo TCA9534 ed espansione | cavo Qwiic intero | V ordine Qwiic |

Una piazzola per filo, con il nome in serigrafia, raggruppate per modulo. Il dato dei LED e il pulsante non si saldano più sui pin della testata (`architettura-una-per-una.md:188`).

### 3.4 Schema a blocchi

```
 [J2 2 x 8 a 90°, chiave] ─┬─ 5 V ─ CE1 470 µF ─┬─ [catena LED: +5 V, DATA, GND]
       │                   │                    └─ [amplificatore: +5 V, GND]
       │                   ├─ 3,3 V ─ [microfoni] [ToF posteriore] [JQ Qwiic] (U6 TCA9534, vuoto)
       │                   ├─ SDA, SCL ─ [ToF posteriore] [JQ] (U6)
       │                   ├─ BCLK, WS ─ [microfoni] [amplificatore]
       │                   ├─ MIC ─ [microfoni] (R-MIC vuota)   AMP ─ [amplificatore]
       │                   ├─ polo 14 ─ [riserva X25]
       │                   └─ poli 15-16 ─ [pulsante]
```

### 3.5 Strati, piste, punti di prova

Due strati, 1,6 mm, 1 oz, HASL; componenti sotto, riempimento di massa sopra. +5 V da 1,0 mm (catena LED fino a 600 mA, amplificatore fino a circa 200 mA: 0,86 A in tutto, `requisiti.md:46`); 3,3 V da 0,5 mm; segnali da 0,25 mm. Il gruppo I2S separato dal bus con una pista di massa, come nel cavo (`requisiti.md:240`). Pulsante su due piste isolate, lontane dalle altre reti: la tensione dei pin A e B della 2813 non è nota (S-10). Serigrafia "HEX2 SC r1", "LATO COMPONENTI", polo 1 e chiave di J2. Punti di prova in 3.2.

## 4. Cosa sparisce e cosa si aggiunge

### 4.1 Sparisce

| Cosa | Dove oggi | Stato, fonte |
|---|---|---|
| Taglio e foratura delle millefori, croci a pennarello, fori allargati a Ø2,6 | passi 4.06, 4.22 | V; `schemi.md:251` |
| 37 fili isolati, 44 incroci, circa 50 ponticelli e la barra di massa della basetta | passi 4.11–4.14 | V; `schemi.md:102-149` |
| 12 fili e 4 ponticelli della scheda del carapace; DIN e pulsante saldati sui pin della testata | passo 4.24 | V; `schemi.md:282-301` |
| La striscia dei partitori: 22 ponticelli, 26 fili (**[corretto dalla verifica]** 16 da prese e NTC, 8 verso gli ingressi dell'ADC, 2 per il 3,3 V e la massa dall'ADC: prima erano contati 26 + 8), il ramo del bus verso l'ADC, il fissaggio senza posto | passi 8.09, 8.10, 8.22, 8.24 | V; `schemi.md:460-467`, `:511-524`; S-28, S-29 |
| Spine JR piegate senza supporto e fili delle prese verso striscia e basetta | passi 8.22–8.24 | V; P-012 |
| Giunzioni in guaina di R9 e D2 | 4.17, 4.18 | V; `schemi.md:60` |
| Nastro Kapton sotto U2 e sopra U3 | 4.07 | S; S-24 |
| **Modulo KAmod Level Shift x4** (C1) | basetta | V; 2,51 €, da comprare (`BOM.md:70`) |
| **Modulo Adafruit ADS7830** (X6) | vano sotto il vassoio | V; 6,37 €, approvato e non comprato (`BOM.md:170`) |
| Le tre millefori C2 | — | in casa: restano per i provini |

In tutto circa 120 fili e ponticelli in meno (`architettura-scheda-madre.md:469`). Le saldature della sezione 4 scendono da 6–7 ore (`04-banco.yaml:33`) a circa 2,5–3,5 ore per la SM e circa 1 ora per la SC [S].

Restano saldati, come oggi: i fili verso 2813, abilitazione, seriale, rami del bus e cavo piatto sulla SM; i fili dei moduli sulla SC. Questo è il limite della r1: la SM non si toglie senza dissaldare (capitolo 1.3).

### 4.2 Si aggiunge (proposte da approvare)

| Voce | Per | Quantità | Costo | Stato |
|---|---|---|---|---|
| PCB a 2 strati, SM e SC | — | 5 + 5 (minimo di JLCPCB) | capitolo 5 | S |
| ADS7830IPW, TSSOP-16 | U5 | 1 + 1 di scorta, solo se si salda a mano | 1,65–1,72 $ su LCSC; 3–5 € da Mouser o DigiKey | S; `architettura-integrazione.md:118`, `architettura-scheda-madre.md:239` |
| SN74AHCT125 in SOIC-14 | U3 | 1 + 1, solo a mano | circa 0,5 € | S; facoltativo, il DIP-14 di X9 entra con meno spazio |
| Resistenze 0805 1 % (10 k, 15 k, 3,3 k, 47 k, 330), kit o valori singoli | R1–R14 | — , solo a mano | circa 5–10 € il kit | S; con il montaggio di JLCPCB sono parti Basic |
| JST SH 4 poli SMD orizzontale (SM04B-SRSS-TB) | JQ sulla SC | 2 | circa 0,5 € l'uno | S |
| PTC più grande (MF-R090 o MF-R110), se S-06 lo chiede | PTC1 | 1–2 | meno di 1 € | S, C |

Non si comprano: X3 (piazzole e ponticello sulla SM), il TCA9534 in chip (impronta vuota), resistenze e condensatori a reoforo dei partitori se monta JLCPCB (X5, X14, circa 1,50 €).

### 4.3 Resta fuori dalle schede, apposta

Il principio di R-12 resta: un filo staccato lascia tutto spento o al sicuro (`requisiti.md:313`).

- R6 da 100 kΩ, saldata sull'uscita della 2813.
- La 100 kΩ fra OFF e massa, sulla 2813 (S-11).
- R3 da 22 kΩ su ciascun D42V110F6 (S-05, S-20).
- R8 al microfono.
- I poli 15-16 del cavo piatto: non passano dalla logica (S-10).

### 4.4 Problemi del registro

`guida/problemi/schemi.yaml`:

- **Chiusi o allentati**:
  - S-04 (passo del KAmod), S-31 (piedinatura del modulo ADC): i moduli spariscono;
  - S-08 in parte: niente PTC sopra il buffer;
  - S-09 e S-25 (piazzole vicine): le decide il disegno;
  - S-24 (Kapton);
  - S-28 e S-29 (posto e altezza dei partitori);
  - S-17 in parte: la presa Qwiic c'è, l'espansore ha un'impronta.
- **Da chiudere prima di disegnare**: S-02 (interasse dell'ESP32), S-03 (pin del D24V22F5), S-26 (testata a 90°), P-012 (misura della spina JR), S-22 (tensione e massa della seriale della SSC-32).
- **Restano aperti, con impronte o ponticelli che li lasciano decidere dopo**: S-06 (PTC), S-10 (pin A e B), S-13 (pull-up), S-21 (pull-down dei microfoni), S-30 (taglia del kit B8).

## 5. Costi e tempi

Prezzi, dogana e cambio (1 $ ≈ 0,86 €) da `produzione.md` (righe 7, 27-33, 44-53, 81-92, 264-274). Totali consegnati in Italia, IVA compresa. Tutti **S**, da rifare con il preventivo vero il giorno dell'ordine (C).

### 5.1 Prima serie (r1)

5 SM e 5 SC (Aisler a gruppi di 3, quindi 6). Aree: SM 56 × 52 = 29,1 cm² come rettangolo, SC 23 × 30 = 6,9 cm².

| Strada | Schede | Parti o montaggio | Si risparmia (C1, X6) | **Netto per il robot** | Fonte |
|---|---|---|---|---|---|
| **JLCPCB, nude, tutto a mano** | 13–19 € (due disegni nello stesso carrello; 8–22 € in un pannello) | 10–20 € di parti (4.2) | 8,88 € | **circa 14–30 €** | `architettura-scheda-madre.md:330-349` |
| **JLCPCB, SMD della SM montati** (Economic, 2 SM montate su 5) | 13–19 € | 22–25 € più circa 1 € per le JST SH | 8,88 € | **circa 27–36 €** | `architettura-scheda-madre.md:340`, `:350` |
| Aisler (UE, niente dogana), un pannello, tutto a mano | circa 34 € | 10–20 € | 8,88 € | circa 35–45 € | `architettura-scheda-madre.md:333`, `:351` |

Oggi le millefori costano zero (in casa) ma chiedono 6–7 ore di saldature nella sola sezione 4.

Proposta: **JLCPCB, un solo ordine** con i due disegni. Due voci doganali al più (3 € l'una), e dal 1° dicembre 2026 i 2 € del contributo italiano (`produzione.md:48-50`). Aisler costa 10–20 € in più e toglie la dogana: si sceglie all'ordine, non serve deciderlo ora.

### 5.2 Serie definitiva (r2)

Dipende da cosa si aggiunge (capitolo 1.3):

| Strada | Totale consegnato | Fonte |
|---|---|---|
| Come la r1, con le correzioni, a mano | circa 15–30 € | come 5.1 |
| SM e SC in un pannello, tutti gli SMD da JLCPCB, 2 serie montate su 5, componenti come la r1 più il TCA9534 | circa 50–65 €: pannello 2–10 $, avvio 10,16 $, pannello di più disegni 8,21 $, 4 codici Extended 12,28 $, componenti per 2 serie circa 8 $, spedizione 3–6 $ = 44–55 $; con l'IVA 54–67 $, cioè 46–58 €; più 3 € di dazio e 2 € | S, conto mio con le voci di `produzione.md:83-92` |
| In più: amplificatore come chip sulla SC allungata, prese GH con aggancio | verso i 100–110 € | `architettura-integrazione.md:304` (tre schede) |
| In più: prese XH, seconda testata 2 × 8, codini GH crimpati | 10–15 € | `architettura-integrazione.md:275-277` |

Oltre i 170 $ JLCPCB non incassa più l'IVA alla cassa: IVA e dazio passano al corriere, con la sua commissione (10–20 €, `produzione.md:47`, `:51`). Un ordine si tiene sotto questa soglia.

### 5.3 Tempi

| Fase | Chi | Durata [S] | Fonte |
|---|---|---|---|
| Dati prima del disegno (capitolo 7.1) | utente e agente | qualche giorno, quando i pezzi sono in casa | R-20 |
| Versione del CAD con la SM | agente, Fusion | 1–2 blocchi di lavoro, dopo la 2.1.7 | `architettura-scheda-madre.md:455` |
| Schema e PCB in KiCad, revisioni, STEP in Fusion | agente e utente | 4–6 sessioni (la SM è i due terzi del lavoro) | `architettura-una-per-una.md:299`, `architettura-scheda-madre.md:456` |
| Dima stampata 1:1 con i moduli veri | utente | 1 giorno | `produzione.md:250` |
| Fabbricazione e spedizione | JLCPCB | 1–3 settimane (linea economica 8–15 giorni; con il montaggio 1–3 giorni in più) | `produzione.md:71`, `:96` |
| **Dall'inizio del disegno alle schede in mano** | | **circa 3–6 settimane di calendario** | |
| Montaggio della r1 | utente | SM circa 2–3 ore, SC circa 1 ora | `architettura-scheda-madre.md:459` |
| Serie definitiva | | 1–2 sessioni di correzioni, poi 2–3 settimane | S |

Nel frattempo si può costruire sulle millefori: reti e GPIO non cambiano, il firmware non se ne accorge (`architettura-scheda-madre.md:460`).

## 6. Impatto

### 6.1 CAD

Tutto in **una versione dopo la 2.1.7** (la 2.1.8, se non ne arrivano altre prima), con il piano in `docs/piano-v2.1.0.md` come le altre. La 2.1.7 si fa com'è, compresa la modifica 8. La versione con la PCB **aggiunge** e non toglie, così la stessa base serve anche alla strada con le millefori.

| N. | Dove | Cosa | Verifica | Stato, fonte |
|---|---|---|---|---|
| 1 | `corpo.py`, `fai_base` | due colonne Ø6 dal tetto del tunnel (z −9,4) a z 5,9 sotto le ali, con inserto M2 in cima. La proposta è a (47,5; ±20,5) ma tocca l'angolo delle sedi delle prese, che restano: si cerca un posto per tutte e due, oppure un parametro sceglie fra base per la PCB e base per le millefori. **[corretto dalla verifica]** Sul lato +Y la colonna tocca anche il modulo ADC e l'asola e l'ala del vassoio della modifica 8 (capitolo 1.4): il parametro è la strada di partenza. In alternativa, per l'ala +Y, una colonnina sull'ala del vassoio | colonna contro vassoio (atteso 1,0), colonnina del carapace (1,1), sede della presa, freccia dell'IMU | S; `architettura-scheda-madre.md:361`; capitolo 1.4 |
| 2 | `rif_componenti.py`, `assieme.py` | nuovo `Rif_Scheda_Madre`: corpo, orecchie e ali dai parametri, più l'ingombro delle spine (z 7,5…24,5, \|y\| 18,2…25,9) e delle femmine innestate. `Rif_Basetta_50x70` resta per la strada con le millefori | interferenze: SM contro colonnine del carapace, morsettiera VS/VL della SSC-32, INA260, servo di coxa anteriori a tutta l'escursione, colonne nuove; spine contro il carapace (sfilamento) e contro i cavi dei servo a z 25 | S; `architettura-scheda-madre.md:364` |
| 3 | `corpo.py`, `fai_vassoio` | solo se servono: passaggio per i 4 fili dell'IMU verso le piazzole −Y | i fili non passano sotto i pin dell'ESP32 | C; `architettura-scheda-madre.md:363` |
| 4 | scheda del carapace | niente oltre la modifica 12 della 2.1.7; restano da chiudere spina contro USB-C e verso dell'allungamento | come la 2.1.7 | S; `requisiti.md:198` |
| 5 | dopo il disegno KiCad | lo STEP delle due schede (`kicad-cli pcb export step`, origine ausiliaria in (22; 0)) entra in libreria come i `Rif_*` al posto delle scatole; il contorno passa da Fusion a KiCad in DXF, oppure si genera dalle quote di `rif_componenti.py` e `fori.json` | interferenze con i modelli veri di ESP32 e Pololu | S; `produzione.md:238-244` |
| 6 | esportazioni | `fori.json`, `manifest.json`, masse in `esporta_robot.py`, `viste.py`, `colori.py` | CI `ci` e `sim` verdi | S |

Viteria: +2 M2 × 5 a testa tonda e +2 inserti M2 per le ali. Documenti da aggiornare quando l'utente sceglie: D-053 (basetta), D-069 (prese sul tetto), `cablaggio.md` 3.3-3.4, `predisposizioni.md` 2.8, `BOM.md` (escono C1 e X6, entrano le voci di 4.2).

### 6.2 Guida

D-076: la guida resta sulle millefori, con una nota che l'alternativa arriverà, senza dettagli (`docs/decisioni.md:684`). **[corretto dalla verifica]** "Finché la PCB non è ordinata e provata" non è nella decisione: è la proposta di questo studio. Dopo la prova della r1 la PCB diventa la **strada A** e la millefori resta la **strada B**, scelta all'inizio della sezione 4. I passi di oggi restano come sono, marcati come strada B. Il meccanismo (un campo nei passi o un'appendice con la strada B intera) si decide con il formato della guida (`guida/schema.md`) [S].

| Sezione | Strada A, con le PCB | Fonte |
|---|---|---|
| **4, banco** (oggi circa 12 ore, 6–7 di saldature) | 4.06: controllo della PCB (revisione in serigrafia, continuità fra massa, 5 V e VBAT) al posto di taglio e croci. 4.07: prova a secco, già fatta prima dell'ordine sulla dima. 4.08–4.10: SMD (si saltano se li monta JLCPCB), poi D1, D2, partitori, U2, PTC, strip e spine delle ali. **4.11–4.14 spariscono.** 4.15–4.19: cavo piatto nella griglia, bus, seriale, 2813 e VBAT sulle piazzole con il nome; D2 è già sulla scheda; le luci non si saldano più. 4.20–4.21: prove sui punti di prova; spariscono quelle delle vicinanze (S-09, S-25). 4.22–4.25: SC con CE1, J2, JQ e i fili; **4.24 sparisce**. 4.26–4.28: uguali, sui punti di prova | `architettura-scheda-madre.md:384-401` |
| **8, elettronica nel corpo** | 8.07: solo i fili dell'IMU. **8.09 e 8.10 spariscono** (ADC e striscia). 8.12: SM con 6 viti. 8.17–8.21: uguali ai capi lontani. **8.22–8.24 diventano spine da innestare** sulle ali, senza saldature. 8.25–8.26: più corti, sui punti di prova | `architettura-scheda-madre.md:403-413` |
| **13, carapace** | 13.16: un filo per piazzola con il nome, niente cavo Qwiic tagliato. 13.17: senza fori da allargare. 13.18: sui punti di prova. Nuovo passo: modulo TCA9534 sulla presa Qwiic con i pull-up tagliati (S-13, S-17) | `architettura-scheda-madre.md:415-423` |
| 9, 10 (zampa sul corpo), 15 (smontaggio) | le spine di FSR e luci si innestano sulle ali, a carapace tolto come oggi; per togliere il vassoio si staccano 12 spine e 2 NTC e si tolgono 2 viti in più | `architettura-scheda-madre.md:426-427` |
| **Appendici** | A.02 (ADC dei piedi e prese): canali sulle spine delle ali. A.15–A.19: disegni della PCB (stampe di KiCad, lato componenti e lato rame) per la strada A; quelli delle millefori restano per la strada B | `90-appendici.yaml:48`, `:356-449` |

Disegni e generatori: le netlist di `guida/schemi/sorgenti/*_def.py` restano la fonte delle reti. Proposta: un controllo che confronta la netlist di KiCad con quella dei `*_def.py`, nello stile di `verifica.py`, così le due strade non divergono (`architettura-una-per-una.md:274`) [S].

### 6.3 Firmware

Nessun cambio obbligato: stessi GPIO (`piano-elettronica-software.md:79-105`), stessi indirizzi I2C (`:111-131`), stessa piedinatura del cavo a 16 poli. Oggi il firmware usa solo il rail su GPIO42 (`firmware/main/main.cpp:13-25`); i driver dei sensori arrivano in S1 e vanno scritti uguali per le due strade.

| Punto | Effetto | Stato |
|---|---|---|
| TX dal buffer, RX dal partitore | nessuno: il buffer non inverte; R10 tiene la linea a riposo durante l'avvio | S; stato di GPIO21 al reset da leggere (C) |
| ADS7830 chip al posto del modulo | stesso indirizzo 0x48 (A0, A1 a massa) e stessi canali. Il byte di comando sceglie riferimento interno o esterno (bit PD): va scelto quello che fa del 3V3S il riferimento, e lo stesso deve valere per il modulo della strada B | C, scheda TI e schema Adafruit da rileggere |
| Pull-up del bus a 3,3 kΩ | nessuno; il tempo di salita si misura in P2 come previsto (`piano-elettronica-software.md:256`) | S |
| Misura RMT su GPIO38 | si chiude JP-RMT e si montano R13 e R14 al banco; si riapre prima dell'audio | S |
| TCA9534 chip (se montato) | stesso indirizzo 0x20 | S |
| Revisione della scheda | non serve leggerla: le due strade sono uguali per il firmware | S |

## 7. Piano per la versione con il disegno vero

### 7.1 Prima di partire: dati

| Dato | Chi | Serve per | Fonte |
|---|---|---|---|
| Quale delle 4 schede è la RE1.3, e prova a secco delle strip a 25,4 | utente | impronta dell'ESP32 (S-02, P-005) | `CLAUDE.md`, "Da guardare sui pezzi" |
| Ordine dei pin del D24V22F5 dalla pagina Pololu 2858 | agente | impronta di U2 (S-03) | `requisiti.md:288` |
| Disegno della testata Würth 61201621721: altezza, chiave, polo 1 | agente | impronta di J2 (S-26) | `requisiti.md:291` |
| Tensione a riposo del pin TX della SSC-32, con il multimetro | utente, al banco | partitore della RX (S-22) | `requisiti.md:289` |
| Misura della spina JR, maschio e femmina | utente | spine delle ali (P-012) | `requisiti.md:293` |
| Schede TI di ADS7830 (REF, bit PD) e SN74AHCT125 (soglie) | agente | U5, U3 | `architettura-scheda-madre.md:446` |
| KiCad 10.0.x sul Mac al posto della 9.0.6 | utente | progetto (un file aperto con la 10 non si riapre con la 9) | `produzione.md:201-206` |

### 7.2 Progetto KiCad nella repo

```
pcb/
  README.md                  revisioni, errata, come si esporta
  librerie/hex2.kicad_sym    simboli dei moduli
  librerie/hex2.pretty/      impronte: ESP32 a 25,4, D24V22F5, testata a 90°, spine JR, punti di prova
  regole/hex2.kicad_dru      regole di produzione.md 3.3, uguali per tutti i produttori
  scheda-madre/              .kicad_pro, .kicad_sch, .kicad_pcb
  scheda-carapace/           idem
  verifica_netlist.py        confronto con guida/schemi/sorgenti/*_def.py
  ordini/r1/                 Gerber, distinta e posizioni effettivamente inviati
```

- In git i file di testo di KiCad; fuori da git `*-backups/`, `.history/`, `*.kicad_prl`, `fp-info-cache`, `*.lck` (`produzione.md:231-233`).
- Ogni ordine ha un tag (`pcb-r1`, `pcb-r2`), così si sa cosa è stato fabbricato.
- Nella CI, `kicad-cli sch erc` e `kicad-cli pcb drc --exit-code-violations`: la CI resta verde solo con ERC e DRC puliti (`produzione.md:204`, `:235`). Il tempo sul runner è da provare (C).
- Le quote vengono da `rif_componenti.py` e `fori.json`, come per il CAD: una sola fonte (`produzione.md:215`).

### 7.3 Passi del disegno

1. **Librerie**: impronte dei moduli dai dati di 7.1. Stampa 1:1 e moduli veri appoggiati sopra.
2. **Schema** della SM e della SC dalle reti di `schemi.md` 1.2, 2.2, 6.2, con le modifiche di questo studio. ERC a zero, confronto con i `*_def.py`.
3. **Contorno e fori** dal CAD della versione con la SM, origine ausiliaria in (22; 0).
4. **Piazzamento** per zone (2.1). Lo STEP va in Fusion per la verifica d'interferenza.
5. **Sbroglio**: prima VBAT e potenza, poi la massa, poi i segnali. DRC a zero, serigrafia.
6. **Dima**: lo STEP della sola scheda (`--board-only`) stampato a 1,6 mm con i fori. Si infilano ESP32, D24V22F5, testata e spine veri.
7. **Uscite**: Gerber controllati in GerbView e nell'anteprima del produttore, distinta, tag, ordine.

### 7.4 Revisioni con l'utente

| Revisione | Dopo il passo | Cosa guarda l'utente |
|---|---|---|
| R1 | 2, schema | reti, componenti, voci nuove del BOM da approvare |
| R2 | 4, piazzamento | posto di spine e piazzole rispetto al montaggio; render e interferenze in Fusion |
| R3 | 6, dima | prova a secco sulla dima: ESP32, regolatore, testata, spine |
| R4 | 7, prima dell'ordine | lista di controllo: antenna, isola del VBAT, 5 V lontano dai GPIO, punti di prova, polarità, chiave di J2, faccia dei componenti, preventivo |

Ogni revisione è un commit; la R4 approvata è il tag e l'ordine.

### 7.5 Prima serie di prova

1. Si ordinano 5 SM e 5 SC; si monta **una** scheda per gradi:
   - solo U2 e l'alimentazione, misure senza ESP32 sui punti di prova;
   - poi buffer, ADC, passivi e ponticelli;
   - infine l'ESP32.
2. **Banco S1** (P2) sulla r1: seriale a 115200 e 230400, bus e tempo di salita, ADC e partitori, LED, misura RMT, calore di U2 (P4).
3. **Nel robot**: interferenze vere, spine delle ali a carapace chiuso, 30 minuti di marcia.
4. Gli errori vanno in un **errata** in `pcb/README.md`. Si correggono sulla r1 con fili e ponticelli, e nella r2 nel disegno.
5. La guida passa alla strada A quando i punti 2 e 3 sono superati.

## 8. Domande per l'utente

1. **Gli SMD della scheda madre li saldi tu o li monta JLCPCB?** A mano c'è un solo chip a passo fine, l'ADC (TSSOP-16, passo 0,65), più gli 0805 che saldi già. Con JLCPCB il robot costa circa 10 € in più e non serve il kit di resistenze (capitolo 5.1) [S].
2. **Le prese dei piedi e delle luci passano sulle ali della scheda madre?** Cambia D-069, che le mette sul tetto del tunnel (`docs/decisioni.md:445`). In cambio le spine hanno un supporto (P-012) e la striscia dei partitori sparisce.
3. **Il banco S1 si fa sulla r1 o sulla millefori?**
   - Sulla r1: non saldi mai le millefori, ma aspetti le schede, 3–6 settimane dall'inizio del disegno.
   - Sulla millefori: parti subito, e la r1 arriva dopo.
4. **Passi a KiCad 10.0.x prima del disegno?** È gratuito; un progetto aperto con la 10 non si riapre più con la 9.0.6 che hai.

Il resto ha una proposta di default che si può cambiare durante il disegno: JLCPCB invece di Aisler, fili saldati invece di connettori nella r1, TCA9534 come modulo.

## 9. Rischi e come ridurli

| Rischio | Effetto | Come si riduce | Stato |
|---|---|---|---|
| **Impronta sbagliata** (interasse dell'ESP32, pin del D24V22F5, testata a 90°, spina JR) | serie da rifare | dati di 7.1 prima del disegno; stampa 1:1; dima stampata con i moduli veri (revisione R3) | S; `produzione.md:250` |
| **Le ali non stanno nel CAD** (servo di coxa a 1,9 mm, colonnina del carapace a 0,8, colonne contro le sedi delle prese, **[corretto dalla verifica]** colonna +Y contro ADC e asola della 2.1.7, PTC senza posto sull'ala −Y, spine a 4 mm dal carapace) | la SM cambia forma | verifica d'interferenza come primo passo della versione del CAD, con le spine innestate e la zampa a tutta l'escursione; ripieghi del capitolo 1.2 (SM senza ali, poi una per una) | S, C |
| **Fili piegati sopra le spine delle ali** | fili schiacciati dal carapace o dai cavi dei servo | prova di sfilamento del carapace nel CAD; femmine JR più corte o fila più bassa | C |
| **ADC in TSSOP-16 saldato a mano** | ponti fra i pin, ADC muto | flussante e treccia, 4 schede di scorta; oppure montaggio JLCPCB (domanda 1) | S |
| **Seriale della SSC-32**: uscita più bassa di 5 V, o massa doppia | RX non letta, disturbi | misura prima del disegno (7.1); piazzola di massa che si può lasciare vuota; ripiego con un 74LVC1G17 in SOT-23-5 | C; S-22 |
| **Circuito non ancora provato al banco** | errore scoperto sulla r1 | ponticelli e impronte vuote sulle scelte aperte (JP-3V3, JP-RMT, R-MIC, U6, PTC); passivi 0805 per tagliare una pista e mettere un filo | S |
| **5 V su un GPIO** | ESP32 danneggiato | regola di 1 mm o una massa in mezzo; misura RMT con il partitore, non dal buffer (capitolo 1.4); prima accensione senza ESP32 | S |
| **Antenna** sopra il rame | portata Wi-Fi più corta | niente rame per x ≥ 74; prova di portata in P2 | S; quota da rileggere sul modulo (C) |
| **Calore di U2** chiuso sotto l'ESP32 | ESP32 e PLA caldi | piano di massa sotto U2; misura in P4 come previsto | S |
| **PTC** troppo stretto o troppo largo (S-06) | scatti o nessuna protezione | impronta per MF-R075/090/110; valore scelto dopo P4 | S, C |
| **Una sola scheda per tutto il corpo** | un guasto ferma tutto | ESP32 e regolatore restano moduli; 4 schede di scorta; punti di prova | S |
| **Faccia sbagliata** (specchiatura) | spine o moduli dal lato sbagliato | "LATO COMPONENTI" e freccia della testa in serigrafia; controllo nel 3D di KiCad e in Fusion | S; `produzione.md:251` |
| **Le due strade della guida divergono** | errori in una delle due | netlist confrontata con i `*_def.py` nella CI | S |
| **Dogana e prezzi** | costi più alti delle schede | un solo ordine sotto i 170 $; Aisler se le regole cambiano ancora | V regola; `produzione.md:47`, `:65` |

## Fonti

- Studio: `docs/ricerca/pcb/requisiti.md`, `produzione.md`, `architettura-una-per-una.md`, `architettura-scheda-madre.md`, `architettura-integrazione.md` (16 ottobre 2026).
- Progetto: `guida/schemi/schemi.md`, `guida/problemi/schemi.yaml`, `docs/cablaggio.md`, `docs/predisposizioni.md`, `docs/piano-elettronica-software.md`, `docs/piano-v2.1.0.md`, `docs/BOM.md`, `docs/decisioni.md` (D-053, D-069, D-076), `firmware/main/main.cpp`, `guida/passi/*.yaml`.
- Prezzi, dogana e regole dei produttori: link in `produzione.md`, letti il 16 ottobre 2026.

## Verifica

Verifica avversaria del 16 ottobre 2026 su questo file e sulle sue fonti. Gli errori certi sono corretti nel testo, segnati "[corretto dalla verifica]". Qui c'è il riepilogo e i dubbi che restano.

### Come è stata fatta

- Reti, poli e GPIO confrontati con `guida/schemi/schemi.md` 1.2, 1.6, 2.2 e con D-076 (`docs/decisioni.md:676-705`).
- Conti rifatti: partitori, pull-up, larghezze delle piste, aree, costi di 5.1 e 5.2.
- Ingombri provati sulle mesh del CAD 2.1.6 (`build/guida/cad/mesh/*.ply` con le trasformate di `guida/dati/manifest.json`), con un controllo triangolo-scatola sulle sagome proposte. Le mesh delle parti comprate sono scatole o STEP dei venditori: risultati S.
- Non riletti in rete: prezzi dei produttori, versioni di KiCad, schede tecniche TI e Bourns. Valgono gli stati delle fonti.

### Risultati che tengono

| Controllo | Risultato | Stato |
|---|---|---|
| Orecchie e ali (z 5,9…7,5) | più vicini: colonnine del carapace 0,8; servo di coxa anteriore 1,85 (stima dello studio 1,9); vassoio 3,3 | S, mesh 2.1.6 |
| Spine sulle ali (z fino a 24,5) | carapace a 3,9; coxa anteriore ruotata da −40° a +40°: almeno 7,0 (Coxa_Ponte, in Z) | S, mesh 2.1.6 |
| SC 2.1.7 (x 26,5…49,5, \|y\| ≤ 15) | amplificatore a 2,35; nel carapace solo le bugne di coda di oggi, che la 2.1.7 sposta | S, mesh 2.1.6 |
| J2 con la scatola (x 26,5…35,5, z 20,3…29,3) | ESP32 a 2,7, carapace a 1,6 | S |
| Reti e GPIO | 15 pin, poli 1–16, chiave dal lato dei poli dispari, R6, D2, R3, 100 kΩ di OFF all'estremo lontano: come oggi | V |
| Funzioni delle millefori | tutte presenti: zoccolo, U2, D1, buffer a due uscite, traslatore (ora canale 3 e partitore), PTC, pull-up, R7 e CS1, J1, 4 rami del bus, seriale, 2813, abilitazione, luci delle tibie con R9, misura RMT, 8 partitori con 100 nF, J2, CE1, piazzole dei moduli del carapace, polo 14 | V |
| Partitore della RX 10 k / 15 k | 3,0 V a 5,0 V, 2,76 V a 4,6 V, sopra 0,75 × 3,3 | S, conto |
| Pull-up 3,3 kΩ | 1,25–1,42 kΩ con 4 o 5 moduli da 10 kΩ | S, conto |
| Piste | VBAT e 5V_REG 1,5 mm contro 1,37 a 3 A; 5V_LED 1,0 contro 0,78 a 2 A | S, tabella di `produzione.md:167-172` |
| Costi | JLCPCB nude 13–19 €; Aisler 46,95 e 34,26 €; SMD montati 22–25 €; netti 14–30, 27–36, 35–45 €; r2 46–58 € più dazio | S, aritmetica giusta sulle fonti |
| Area della SM | 1960 + 195 + 408 = 2563 mm² | S |

### Correzioni fatte nel testo

1. **Colonna +Y dell'ala** (1.4, 2.1, 6.1, 9, In breve): oltre alla sede delle prese tocca l'ADC della strada con le millefori, l'asola e l'ala del vassoio della modifica 8. "La modifica 8 resta" e "la base serve tutte e due le strade" non stanno insieme con le colonne proposte; una Ø6 entra solo verso x 67-68, a margine zero.
2. **VBAT fra i pin** (2.3, 2.5): un foro non metallizzato lascia due varchi da 1,2 mm, contro i 3,5 mm di pista e distanze. Servono due posti senza foro (per esempio O-2 e P-2).
3. **Piste a 5 V fra i pin** (2.5): TX5, DATA, DATA2 e il 5 V verso il PTC devono attraversare una fila. La regola di 1 mm si rispetta solo con varchi di posti senza foro; il partitore della RX va nell'orecchia.
4. **PTC1 sull'ala −Y** (2.1, 2.2): non ci sta. L'ala ha 7 posti e il foro della colonna, e l'orecchia −Y ha la griglia del cavo piatto.
5. **Uscita del pin 5V verso la coda** (2.3): fra il pin e il bordo restano 0,9 mm. La pista esce verso Z1.
6. **Rame attorno ai fori** (2.1): la zona senza rame è Ø6 (testa più 1 mm, `produzione.md:190`), non un anello di 1 mm attorno al foro.
7. **COM dell'ADS7830 a massa** (2.2): mancava.
8. **JP-3V3** (1.4): rende J1 e X3 insieme più difficili da fare, non impossibili.
9. **Spina della SC sopra la USB-C** (3.1): con la scheda allungata verso la coda, il tratto in conflitto è x 14,5…20,1, non 17,5…20,1.
10. **Correnti dei servo** (2.5): non passano sulla SM solo se la massa della seriale non chiude un giro (S-22).
11. **Fili della striscia** (4.1): 26 in tutto, di cui 8 verso l'ADC; non 26 + 8.
12. **D-076** (6.2): "finché la PCB non è ordinata e provata" è una proposta dello studio, non una frase della decisione.

### Dubbi aperti

1. **Z2 +Y troppo piena.** In una fila sola (larga 3,3) vanno gli 8 partitori in piedi (16 fori), il ToF frontale (4) e la riserva del bus (4): 24 posti a 2,54 sono circa 61 mm, contro 52 (x 22…74). Due file non ci stanno. Si risolve spostando la riserva nell'orecchia, oppure con i partitori in 0805 sotto l'ESP32 (voce nuova o montaggio JLCPCB). S.
2. **Ritorno dei LED a U2.** La pista di massa da 1,5 mm dall'orecchia −Y e dall'ala −Y a U2 attraversa anch'essa la fila −Y. Serve un varco, oppure il ritorno passa dal piano. Con il piano, la "stella" diventa una scelta di disegno da spiegare. S.
3. **J2 e presa Qwiic sulla SC.** Una testata 2 × 8 con la scatola è lunga circa 28 mm [S, formula di catalogo, disegno Würth non letto], su 30 di larghezza: il bordo di coda resta tutto suo. Il posto di JQ, raggiungibile dall'ottagono, non è indicato: della SC solo x 26,5…28 sta sotto l'apertura. C.
4. **Indirizzo del modulo SparkFun DEV-17047.** Il progetto lo dà a 0x20. Mi risulta che il Qwiic GPIO esca di fabbrica a 0x27, con ponticelli per 0x20…0x27. Da rileggere sulla guida SparkFun prima dello schema: U6 con A0–A2 a massa è 0x20. C.
5. **Condensatore sulle prese delle luci** (S-23; D-076: "solo se serve, con quelli che l'utente ha già"). Sulla SM non è prevista un'impronta, e l'ala −Y è già piena. Va trovato un posto vicino a JL, o si accetta il filo. S.
6. **Spine delle NTC.** Il posto 7 delle ali vuole una femmina JR su ogni NTC, oggi saldata. Le femmine vengono dalle prolunghe C5 avanzate: ne restano 16, ne servono 14 (6 + 6 + 2) (`predisposizioni.md:166`). Va scritto, e la crimpatura del 28 AWG va provata. S.
7. **Punto di prova del VBAT nudo.** Va tenuto lontano almeno 1 mm da ogni altra piazzola, e non accanto ai punti di prova dei GPIO: il puntale che scivola fa lo stesso danno di un ponte. In alternativa si misura sul VIN di U2. S.
8. **Dogana del montaggio.** Le SM montate possono contare come una voce doganale diversa dalle SC nude: +3 € nella riga JLCPCB con il montaggio. C.
9. **Tempi.** Le fonti non concordano. Saldature della sezione 4: scheda madre `:401` dice 2,5–3,5 ore per tutta la sezione, `:459` dice SM 2–3 ore più SC 1 ora; qui 3,5–4,5 ore. Disegno: 2–4 blocchi (`architettura-scheda-madre.md:456`), 5–6 sessioni (`architettura-una-per-una.md:299`); qui 4–6. Restano stime. S.
10. **Spine sulle ali e cavi delle zampe.** Il carapace sta a 3,9 dalla cima delle femmine, ma la piega dei fili e il passaggio dei cavi dei servo a z 25 sopra le ali non sono nel CAD. Da provare nella verifica di `sfilamento` con l'ingombro dei fili. C.
11. **Varchi senza contatti nelle strip femmina.** Sfilare i contatti dei posti non usati (per VBAT e 5 V) va provato sulla strip vera: la prova a secco di P-005 va fatta con la strip già preparata così. C.
