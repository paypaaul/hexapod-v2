# Dati dei moduli da fonti pubbliche (Q-18, Q-21, Q-30..Q-34)

Ricerca del 15 ottobre 2026, per chiudere senza l'utente le domande di `guida/problemi.md` che hanno risposta in datasheet, file di progetto dei produttori, pagine dei venditori o schemi. Stato dei dati: **V** verificato su fonte primaria (file di progetto, disegno quotato o schema del produttore), **S** stimato (fonte indiretta, immagine misurata, scheda gemella, regola generale), **C** da confermare sul pezzo. Le quote ricavate misurando un'immagine sono dichiarate come tali. I file scaricati per la ricerca non sono nel repository.

## Riepilogo

| Domanda | Dato trovato | Stato | Sblocca | Differenza con CAD / schemi |
|---|---|---|---|---|
| Q-31 KAmod | serigrafia HV,1,2,3,4,G e LV,1,2,3,4,G; 15,7 × 10,7; 4,7 kΩ su ogni canale gia' a bordo | V (passo fra le file S) | P-033, S-04 | ordine dei pin **coincide**; la serigrafia dice "G" e canali 1-4 (non H1/L1); i 4,7 kΩ a bordo non erano considerati |
| Q-32 ADS7830 | scheda 30,48 × 17,78; 4 fori Ø2,5 a 25,4 × 12,7; fila A7...A0 e fila VIN, GND, SCL, SDA, REF, COM, AD0, AD1 | V (file .brd di Adafruit) | P-017, S-31 | CAD ok (30,5 × 17,7, fori a 25,4); mancano 2 fori e i pin |
| Q-33 VL53L7CX | 12,7 × 17,78; 2 fori Ø2,18 a 12,7 di interasse, a 2,54 dai bordi | V (disegno quotato Pololu), posizione dei fori S | P-018 | CAD 18 × 13 arrotondato; sensore **non al centro** (circa 1 mm); fori assenti nel CAD |
| Q-34 BX100 | dimensioni **discordi** fra venditori (40 × 25 × 11 oppure 40 × 30 × 15); presa di bilanciamento sul lato corto; display sulla faccia superiore; soglia 2,7-3,8 V a passi di 0,1 V | C (venditori) | P-066, P-132 (in parte) | il CAD usa 40 × 25 × 11: e' una delle due versioni |
| Q-30 INA260 | morsettiera a vite 5,08 mm, **sezione non pubblicata da Adafruit**; scheda 22,86 × 22,86; fori a 17,78 | V (scheda), C (sezione) | P-025 (in parte) | CAD ok; altezza della morsettiera (8,5) sospetta |
| Q-18 ESP32 | interasse 25,4; nessun diodo sul 5V (solo un PTC da 0,5 A); 10 kΩ su GPIO40 verso 3V3; FPC 24 poli a ribalta | V su Freenove e Keyestudio, **S sulla UICPAL** | P-005, P-026, P-035, P-039, P-040, P-079, P-086 (in parte) | CAD ha 24,7 (C) contro 25,4; D1 non impedisce il ritorno del 5V verso la USB |
| Q-21 | inserti: punta a 210 °C (PLA) e 245 °C (PETG-CF) come partenza; saldatura 14 AWG: 315-350 °C (Sn-Pb), 350-380 °C (senza piombo); bismuto: non per la potenza | S | P-058, P-079 | nessuno stava scritto |

Da misurare ancora sul pezzo: interasse e lunghezza dell'ESP32 UICPAL, lato dei contatti del flat, altezze dei componenti sul retro dell'ESP32, tre quote del BX100 e quale estremo della presa e' il negativo, posizione del sensore del VL53L7CX, altezza e sezione massima della morsettiera dell'INA260 (con un tratto di 14 AWG), lettura della lega dello stagno.

---

## Q-31. Traslatore KAmod Level Shift x4 (Kamami)

Fonti primarie:
- pagina del produttore: [kamamilabs.com/?p=1569](https://kamamilabs.com/?p=1569);
- scheda tecnica (wiki Kamami, rev. 24 febbraio 2025): [wiki.kamamilabs.com, KAmod Level Shift x4](https://wiki.kamamilabs.com/index.php?title=KAmod_Level_Shift_x4_(PL));
- disegno quotato [_wym.png](https://wiki.kamamilabs.com/images/1/1c/KAmod_Level_Shift_x4_wym.png), serigrafia [_syg.png](https://wiki.kamamilabs.com/images/4/48/KAmod_Level_Shift_x4_syg.png), schema [_sch.png](https://wiki.kamamilabs.com/images/6/63/KAmod_Level_Shift_x4_sch.png), modello STEP: [KAmod_Level_Shift_x4.zip](https://wiki.kamamilabs.com/images/0/06/KAmod_Level_Shift_x4.zip).

| Dato | Valore | Stato |
|---|---|---|
| Dimensioni | 15,7 × 10,7 mm; tutti i pin sulla griglia da 2,54 | V |
| Pin | due file da 6 sui lati lunghi; il modulo e' fornito con due listelle goldpin da 6 | V |
| Interasse fra le due file | 7,62 mm (3 passi): letto sul disegno quotato, 7,7 mm con l'errore di lettura; il produttore dice "griglia da 2,54" | S |
| Serigrafia lato HV, dall'alto | **HV, 1, 2, 3, 4, G** | V |
| Serigrafia lato LV, dall'alto | **LV, 1, 2, 3, 4, G** | V |
| Nomi nello schema | J1: HV, H1, H2, H3, H4, GND; J2: LV, L1, L2, L3, L4, GND (stesso ordine, stessi pin della serigrafia) | V |
| Massa | le due G sono la stessa massa (comune a HV e LV) | V |
| Canali | 4 bidirezionali con MMBT7002; **resistenza da 4,7 kΩ verso HV su ogni canale lato alto e da 4,7 kΩ verso LV lato basso**, gia' sul modulo | V (schema) |
| Tensioni | 1,8-5 V per sezione, con HV > LV; I2C a 1 MHz | V |
| Alimentazione | HV e LV sono ingressi: vanno alimentati tutti e due | V |

Confronto con `guida/schemi/schemi.md` (riga 47, S-04): l'ordine dei pin **coincide** (HV, H1...H4, GND a sinistra; LV, L1...L4, GND a destra). Differenze:
- la scheda stampa **"G"**, non "GND", e i canali sono **1...4** (le sigle H1/L1 sono quelle dello schema elettrico): nei testi per l'utente scrivere "pin 1 del lato HV", non "H1";
- "sigle e passo fra le file (7,62) [C]": le sigle passano a V; il passo resta S (coerente con la griglia dichiarata);
- ci sono **4,7 kΩ a bordo su ogni canale, verso HV e verso LV**: TX (canale 1) e RX (canale 3) hanno gia' i pull-up verso 5 V e 3,3 V. Pull-up aggiunti sulla basetta su questi canali vanno evitati; i canali 2 e 4 liberi non hanno effetto.

Sblocca **P-033** (Q-31) e S-04. Resta da vedere sul pezzo solo che le listelle siano state montate dal lato giusto.

---

## Q-32. ADS7830 Adafruit #5836 (STEMMA QT)

Fonti primarie:
- file di progetto aperti di Adafruit (EagleCAD): [github.com/adafruit/Adafruit-ADS7830-PCB](https://github.com/adafruit/Adafruit-ADS7830-PCB), `Adafruit ADS7830 Breakout PCB.brd`. Le quote che seguono sono **lette dal file della scheda** (contorno, fori, piazzole), non misurate su una foto;
- pagina del prodotto [adafruit.com/product/5836](https://www.adafruit.com/product/5836) (la foto conferma la serigrafia) e guida [ADS7830 pinouts](https://learn.adafruit.com/adafruit-ads7830-8-channel-8-bit-adc/pinouts).

| Dato | Valore | Stato |
|---|---|---|
| Scheda | **30,48 × 17,78 mm** (1,2 × 0,7 in), angoli arrotondati; 4,7 mm di spessore con i connettori (Adafruit) | V |
| Fori di fissaggio | **4 fori Ø2,5 passanti, pad Ø3,2**, a 2,54 mm da ogni bordo: interasse **25,4 (lato lungo) × 12,7 (lato corto)** | V |
| Pin | due file da 8 fori (foro Ø1,0, piazzola Ø1,78), passo 2,54, centrate sul lato lungo (da 6,35 a 24,13 dal bordo corto); le due file distano **12,7 mm** | V |
| Fila superiore, scheda con la serigrafia leggibile e il chip in alto, da sinistra | **A7, A6, A5, A4, A3, A2, A1, A0** | V (.brd e foto) |
| Fila inferiore, da sinistra | **VIN, GND, SCL, SDA, REF, COM, AD0, AD1** | V (.brd e foto) |
| Connettori STEMMA QT | due JST SH a 4 poli, uno su ogni lato corto, a meta' altezza | V |
| Fornitura | striscia di pin maschio 0,1″ non montata (la scheda ha solo i fori) | V (foto) |

Orientamento: A0 e' la piazzola vicina al foro di fissaggio in alto a destra; VIN quella vicina al foro in basso a sinistra.

Confronto con il CAD (`rif_componenti.py`, `sen_ads_*`):
- `sen_ads_l` 30,5 e `sen_ads_w` 17,7: coerenti con 30,48 e 17,78 (stato V);
- `sen_ads_fori` 25,4 (C): **confermato**, V. La scheda ha altri due fori a 12,7 mm in direzione corta: il CAD ne usa due (quelli su un lato lungo);
- il CAD non ha i pin: se i fori della fila A7...A0 ricevono una listella 1 × 8 maschio, la fila A-2...H-2 della striscia dei partitori (S-31) puo' stare **a diretto contatto con la fila A0-A7**: lo schema potrebbe saltare 8 fili. E' una possibilita' geometrica (passo 2,54, 8 pin consecutivi), non una scelta fatta.

Confronto con `schemi.md` e S-31: **A0-A7 stanno in una sola fila da 8** sul lato lungo, **VIN e GND stanno agli estremi di sinistra dell'altra fila**. Nell'ordine in x la fila A e' invertita (A7 a sinistra) rispetto alla fila inferiore: attenzione quando si ribalta la scheda.

Sblocca **P-017** (Q-32) e **S-31** (posizione e ordine dei pin, fori di fissaggio). Resta da definire solo l'altezza dei pin saldati (dipende dalla listella scelta).

---

## Q-33. Pololu VL53L7CX #3418

Fonti primarie:
- pagina Pololu: [pololu.com/product/3418](https://www.pololu.com/product/3418) ("two mounting holes spaced 0.5″ apart that work with #2 and M2 screws");
- disegno quotato, vista dal lato inferiore: [0J11642.1200.jpg](https://a.pololu-files.com/picture/0J11642.1200.jpg) (didascalia "VL53L5CX/VL53L7CX ... bottom view with dimensions"); piedinatura: [0J12241.1200.jpg](https://a.pololu-files.com/picture/0J12241.1200.jpg).

| Dato | Valore | Stato |
|---|---|---|
| Scheda | 0,5″ × 0,7″ = **12,7 × 17,78 mm**; 3 mm di spessore (0,1″) | V |
| Fori di fissaggio | **2 fori Ø0,086″ = Ø2,18 mm**, interasse **0,5″ = 12,7 mm** lungo il lato da 17,78 | V (disegno quotato) |
| Posizione dei fori | sul lato lungo opposto alla fila dei pin, a 0,1″ = **2,54 mm** da quel bordo e da ciascun bordo corto | S: letta sul disegno (685 px/″), coerente con 0,7″ - 0,5″ = 0,2″, cioe' 0,1″ per parte |
| Pin | 7 fori in colonna a passo 2,54: **VDD (uscita 3,3 V), VIN (3,3-5,5 V), GND, SDA, SCL, LPn, INT**; **I2C_RST** in un foro a parte, spostato di un passo verso l'interno accanto all'ultimo | V |
| Sensore | rettangolo nero circa 6,4 × 3,1 mm, col lato lungo **perpendicolare** alla fila dei pin; centro a circa **7,3 mm dal bordo dei pin** (il centro della scheda sarebbe a 6,35) e a circa 0,3 mm dal centro nell'altra direzione | S: misurato sulla foto della piedinatura (40 px/mm); C |

Confronto con il CAD (`rif_componenti.py`):
- `sen_tof_l` 18 e `sen_tof_w` 13: arrotondamenti per eccesso della scheda vera (17,78 × 12,7); differenza 0,22 e 0,30 mm, dalla parte sicura;
- `sen_tof_chip_*` "al centro della scheda" (C): la dimensione coincide (6,4 × 3), la posizione **no**: circa 1 mm verso il lato dei fori. Conta per la finestra nella visiera (X8) e la mensola: da verificare il margine nel CAD;
- il CAD non ha i fori: servono 2 fori Ø2,18 a 2,54 dal bordo (la testa di una vite M2, raggio 1,9, ci sta).

Sblocca **P-018** (Q-33). Resta da misurare sul pezzo la posizione del sensore (C). Pololu dichiara le stesse dimensioni esterne (0,5″ × 0,7″) per tutta la famiglia di carrier VL53L*CX; i fori del #3415 (VL53L5CX, X19) non sono stati verificati.

---

## Q-34. Allarme di sottotensione BX100 (B9)

Fonti (il BX100 e' un prodotto generico senza scheda tecnica del costruttore: i dati sono dei venditori, **tutti C**):
- [Origin Hobbies, 1-8S LiPo Battery Voltage Tester / Low Voltage Buzzer Alarm](https://originhobbies.com/fi/shop/charging/battery-monitors/1-8s-lipo-battery-voltage-tester-low-voltage-buzzer-alarm/) (specifiche e foto);
- [Robu.in, BX100 1-8S](https://robu.in/?p=835784) (dimensioni diverse);
- la foto del prodotto di Kamami (rivenditore del BOM, `110893-large_default`; la pagina risponde 403 da qui), coerente con le foto di Origin Hobbies.

| Dato | Valore | Stato |
|---|---|---|
| Dimensioni | **Origin Hobbies: 40 × 25 × 11 mm, 8 g**; **Robu: 40 × 30 × 15 mm**. Non conciliabili | C: scarto di 5 mm in larghezza e 4 in altezza |
| Rapporto dei lati nella foto dall'alto | circa 0,71 (larghezza/lunghezza), fra 25/40 = 0,63 e 30/40 = 0,75: non decide | S |
| Presa di bilanciamento | **sul lato corto** (faccia da circa 25 × 11), una fila di **9 pin** (1-8S) a passo JST-XH, in una finestra aperta sul lato corto | V per il lato (foto), S per il passo |
| Display | **3 cifre a 7 segmenti rosse sulla faccia superiore**, nella parte centrale; i due fori dei cicalini e il tasto tattile stanno dal lato corto **opposto** alla presa | V per la faccia, S per la posizione |
| Soglia dell'allarme | **OFF oppure da 2,7 a 3,8 V per cella a passi di 0,1 V**, impostata col tasto: 3,3 V e 3,5 V sono entrambi regolabili | V (Origin Hobbies) |
| Campo e precisione | per cella 0,5-4,5 V; totale 0,5-36 V; precisione ±0,01 V (Origin Hobbies) contro ±0,05 V (Robu); **per un 1S il campo e' limitato a 3,7-30 V**, per un 2S non conta | C |
| Connettore | JST-XH di bilanciamento; il cavo non e' fornito (Robu) | V |

Confronto con il CAD (`cic_*`, `Rif_Cicalino_BX100` = box 40 × 25 × 11) e `cablaggio.md`:
- 40 × 25 × 11 e' la versione di Origin Hobbies; se arriva quella di Robu (40 × 30 × 15) il collare tagliato su quote stimate non regge. Finche' non si misura il pezzo, il caso peggiore dei dati dichiarati e' 40 × 30 × 15;
- la presa e' sul lato corto: il collare aperto in coda va bene solo se **quel lato corto guarda in coda**; il verso dipende dal CAD, non dal modulo;
- il display e' sulla faccia superiore: serve una finestra sopra il display nel coperchio, o il display si vede solo a coperchio aperto;
- il tasto di impostazione e' sul lato corto opposto alla presa, non sulla faccia: la soglia si imposta prima del montaggio, o con il collare aperto da quel lato.

Non trovato in nessuna fonte pubblica: **quale pin della fila da 9 e' il negativo** e come si innesta una presa a 3 poli (2S) in una finestra da 9. Si legge sul pezzo (tronchetto di polarizzazione) e si controlla con il tester prima di collegare.

Sblocca in parte **P-066** (soglia: 3,3 o 3,5 V sono entrambi impostabili) e **P-132**. Da misurare sul pezzo: le tre quote, il verso della presa, quanto sporge la spina innestata.

---

## Q-30. INA260 Adafruit #4226: morsettiera

Fonti primarie:
- file di progetto aperti: [github.com/adafruit/Adafruit-INA260-PCB](https://github.com/adafruit/Adafruit-INA260-PCB), `Adafruit INA260.brd` (contorno, fori, impronta della morsettiera);
- pagina del prodotto [adafruit.com/product/4226](https://www.adafruit.com/product/4226) e guida [learn.adafruit.com, INA260](https://learn.adafruit.com/adafruit-ina260-current-voltage-power-sensor-breakout).

| Dato | Valore | Stato |
|---|---|---|
| Morsettiera | **a vite, passo 5,08 mm, 2 poli** ("extra chunky"); dal 15 maggio 2024 e' gia' saldata; va rivolta verso l'esterno | V |
| Sezione di filo accettata | **non pubblicata da Adafruit** (ne' pagina, ne' guida, ne' file di progetto). I blocchi generici a vite da 5,08 mm dichiarano 22-12 AWG (Robu, 6 A) o 26-14 AWG (iFuturetech, 10 A); un tipo "medio" arriva a 16 AWG (Protosupplies) | C per il 14 AWG |
| Corrente | il sensore misura fino a 15 A continui (shunt da 2 mΩ); i blocchi da 5,08 mm sono dati per 6-10 A | V (sensore), S (blocco) |
| Scheda | **22,86 × 22,86 mm**; 2,7 mm di spessore (Adafruit) | V |
| Fori | **2 fori Ø2,5** (pad Ø3,2) a (2,54; 20,32) e (20,32; 20,32): interasse **17,78 mm**, a 2,54 mm dal bordo della morsettiera e dai lati; la scheda non ha altri fori | V |
| Impronta della morsettiera | due fori lunghi Ø1,1 a passo 5,08; contorno **10,16 × 8,5 mm** in pianta, a filo del bordo | V; altezza non pubblicata |
| Fila di pin 1 × 8 (bordo opposto), da sinistra con la morsettiera in alto | Vcc, GND, SCL, SDA, Alert, VBus, Vin+, Vin- | V (foto) |
| Terminali | Vin+ a sinistra, Vin- a destra | V (foto) |

Il 14 AWG ha 2,08 mm² (conduttore di circa 1,6-1,8 mm): entra in un blocco da 22-12 o 26-14 AWG, non in uno da 16 AWG massimo. Risposta: **probabile si, non garantita**: si verifica con un tratto di 14 AWG spelato di 6-7 mm infilato nel blocco senza stringere, appena arriva il pezzo. Un puntale (ferrule) da 2,5 mm² sarebbe una voce in piu' nel BOM, da chiedere.

Confronto con il CAD (`sen_ina_*`):
- `sen_ina_l` 22,9 e `sen_ina_w` 22,8 (S): coerenti con 22,86 (V); `sen_ina_sp` 2,7: coerente con Adafruit;
- `sen_ina_fori` 17,8 (C): **confermato**, 17,78 (V). La scheda ha solo questi due fori, dal lato della morsettiera;
- `sen_ina_mors_h` 8,5 "altezza della morsettiera sopra il circuito" (C): 8,5 mm e' nel file la **profondita' dell'impronta in pianta**; l'altezza non e' pubblicata (blocchi a vite da 5,08 mm tipici: 9-10,5 mm, S). Sospetto che il valore sia un'altra quota: verificare, e fino alla misura usare 10 mm.

Sblocca in parte **P-025**: la sezione e' da provare con un tratto di filo, non da una fonte.

---

## Q-18. Scheda UICPAL "ESP32-S3-CAM N16R8 RE1.3"

**Fonti.** La UICPAL non ha documentazione pubblica raggiungibile (la pagina AliExpress 1005008519401021 restituisce solo lo script della pagina). Le schede "gemelle" hanno dati primari, ma **non sono la stessa scheda**:

| Scheda | Fonte | Dimensioni | Layout |
|---|---|---|---|
| Freenove ESP32-S3-WROOM (FNK0085) | [store.freenove.com/products/fnk0085](https://store.freenove.com/products/fnk0085) (disegno della confezione), [disegno dei pin](https://github.com/Freenove/Freenove_ESP32_S3_WROOM_Board), schema [SCH_for_ESP32-S3.pdf](https://github.com/Freenove/Freenove_Media_Kit_for_ESP32-S3/blob/main/Schematic_diagram/SCH_for_ESP32-S3.pdf) ("CB8201_ESP32S3_Dev", 29 aprile 2025) | **57 × 28 mm** con l'antenna | due USB-C affiancate sul lato corto opposto all'antenna, FPC al centro, nessun foro di fissaggio |
| Keyestudio MB0184 | [docs.keyestudio.com/projects/MB0184](https://docs.keyestudio.com/projects/MB0184/en/latest/README.html) | 67 × 29 mm | USB-C sul lato corto, due fori, CH340, SD e regolatore sul retro |
| Keyestudio MB0200 | [docs.keyestudio.com/projects/MB0200](https://docs.keyestudio.com/projects/MB0200/en/latest/docs/MB0200%20S3%20CAM.html) | 67,2 × 30,8 mm | USB-C sul lato corto, quattro fori |
| UICPAL RE1.3 (CAD) | inserzione, lettura dell'8 ottobre | 62,6 × 28,3 PCB + 4,8 di antenna = 67,4 (S) | USB-C affiancate, FPC al centro, nessun foro |

Le tre schede hanno la **stessa piedinatura e lo stesso ordine dei pin** (a sinistra 3V3, EN, 4, 5, 6, 7, 15, 16, 17, 18, 8, 3, 46, 9, 10, 11, 12, 13, 14, 5V; a destra TX, RX, 1, 2, 42, 41, 40, 39, 38, 37, 36, 35, 0, 45, 48, 47, 21, 20, 19, GND; antenna in alto): le tabelle di `dimensioni-componenti.md` valgono per tutte. **Le lunghezze differiscono** (57 contro 67): per la UICPAL il layout e' quello descritto dall'inserzione, non quello del Freenove.

| Dato richiesto | Valore | Fonte | Stato |
|---|---|---|---|
| **Interasse fra le due file di pin** | **25,4 mm** (10 passi) | Keyestudio MB0184 e MB0200: "the two rows of pin headers have a spacing of 25.4mm". Freenove: letto sul disegno dei pin del produttore (passo verticale 27,1 px = 2,54 mm, distanza orizzontale dei fori 271 px = 25,4 mm) | V (Keyestudio), S (Freenove, misura sul disegno), **S per la UICPAL** |
| Serigrafia 5V, GND, 3V3 | Freenove: **5V**, **GND**, **3V3**; GPIO come numeri nudi, "TX" e "RX" per 43 e 44, **"EN"** vicino al 3V3. Keyestudio: "5V", "3V3", "EN", "G4"..."G14", "TXD", "RXD", "G1"...; la massa e' **"G"** | foto dei produttori | V per Freenove e Keyestudio; UICPAL: C |
| Tensione sul pin 5V con la sola USB | nello schema Freenove la rete V-USB (le due VBUS) arriva al pin 5V attraverso un **PTC MF-PSMF050X-2 (0,5 A, Rmin 0,15 Ω)**, **nessun diodo**. Caduta = corrente × resistenza: da alcune decine di mV a circa 0,3 V con 100-300 mA, quindi **4,7-5,0 V** con USB a 5 V. Il pin 5V e il regolatore AMS1117-3.3 stanno sulla stessa rete a valle del PTC | schema Freenove; Rmin da [elenchi dei distributori](https://www.masterelectronics.com/bourns/mfpsmf050x2-10751651.html) | V sul Freenove, S sulla UICPAL |
| C'e' un diodo? | **No**: il pin e' collegato alla USB dal solo PTC, **in entrambe le direzioni**. Un 5 V esterno sul pin raggiunge le VBUS delle due USB-C attraverso il PTC (0,5 A di tenuta) | schema Freenove | V sul Freenove, S sulla UICPAL |
| Pull-up o componenti su **GPIO40** | **10 kΩ verso 3V3** (R18) sulla linea SD DAT0, come su GPIO38 (CMD, R16) e GPIO39 (CLK, R17); DAT0 e' anche sul contatto dello zoccolo microSD | schema Freenove | V sul Freenove, S sulla UICPAL |
| Altri carichi sui pin | GPIO2: LED blu "ON" con 1 kΩ verso massa; GPIO48: ingresso del WS2812B di bordo; GPIO4 e 5: 10 kΩ verso 3V3 (SCCB della camera, non usati dal progetto); EN: 10 kΩ verso 3V3, 1 µF e pulsante; GPIO0: pulsante BOOT; GPIO43/44: CH343 con i LED TX/RX; GPIO19/20: USB-C "OTG". **Nessun componente su GPIO1, 3, 14, 21, 41, 42, 45, 46, 47** | schema Freenove | V sul Freenove, S sulla UICPAL |
| Alimentazione di bordo | AMS1117-3.3 (ingresso = rete del pin 5V), XC6206 da 2,8 V e da 1,2 V per la camera. Il pin **3V3 e' l'uscita dell'AMS1117**: da usare come uscita, non da alimentare dall'esterno | schema Freenove | V sul Freenove |
| Componenti sul lato inferiore | oltre alla microSD: **AMS1117 in SOT-223** e un **condensatore al tantalio da 100 µF** (vicino alle USB), alcune decine di SMD 0402-0603, i due XC6206. Le altezze non sono pubblicate; valori tipici: microSD 1,9 mm, tantalio 2,8 mm, SOT-223 1,7 mm | schema Freenove (elenco dei componenti); foto del retro Keyestudio (posizioni) | S; altezze C |
| Connettore FPC | **24 poli** ("Connector-24P"; passo 0,5 mm, tipico), piedinatura DVP da OV2640/OV3660: 1 NC, 2 AGND, 3 SDA, 4 AVDD, 5 SCL, 6 RST, 7 VSYNC, 8 PWDN, 9 HREF, 10 DVDD, 11 DOVDD, 12 D9, 13 XCLK, 14 D8, 15 DGND, 16 D7, 17 PCLK, 18 D6, 19 D2, 20 D5, 21 D3, 22 D4, 23 D1 (non collegato), 24 D0 (non collegato); piedino di schermo a massa | schema Freenove | V sul Freenove (la UICPAL dichiara lo stesso tipo di connettore: S) |
| Levetta del connettore | **a ribalta ("flip lock")**: l'attuatore scuro sta sul lato dell'**antenna**, i terminali di saldatura sul lato delle USB; il flat entra dal lato dell'antenna (coerente con `dimensioni-componenti.md`) | foto del prodotto Freenove ingrandita | S |
| Lato dei contatti del flat | non si ricava da una foto: dipende dal tipo di presa | – | **C** (sul pezzo, con il flat della camera gia' montato) |

**Differenze con il repository**
- `esp_file` in `rif_componenti.py` e' **24,7 mm** (C): le fonti dicono **25,4 mm**. `guida/schemi/schemi.md` (riga 44) usa 25,4 e segnala la differenza (S-02): e' la scelta giusta; il CAD va portato a 25,4, salvo che la quota "24,7" dell'inserzione sia un'altra distanza (il disegno non e' raggiungibile da qui). La prova a secco di P-005 resta la verifica sul pezzo: 0,7 mm di differenza fra le file non si perdona con le strip femmina.
- `dimensioni-componenti.md` riga 62 ("probabile interasse ... standard DevKitC 25,4"): si puo' aggiornare con la fonte.
- `dimensioni-componenti.md` riga 95 ("nessun foro di fissaggio"): coerente con il Freenove, non con le Keyestudio (due o quattro fori).
- Il Freenove stampa **"EN"**, schemi e guida dicono "RST": nei testi per l'utente scrivere "EN (RST)".
- `schemi.md` 4.03 e 4.08, domanda aperta di S-07 ("se la porta USB riceve il 5 V del pin"): **si**, attraverso il PTC da 0,5 A (Freenove; UICPAL da confermare). D1 impedisce il percorso verso il regolatore, non quello verso la USB. Con D1 il pin sta a 4,55-4,7 V e la VBUS di un host e' in genere piu' alta, quindi la corrente va dalla USB alla scheda; una alimentazione alla volta resta la regola.
- `schemi.md`, 1.5, prova 5: "resistenza fra GPIO40 e 3V3 a scheda spenta" si aspetta **circa 10 kΩ** (R18), non un circuito aperto.
- Pin senza alcun componente di bordo: GPIO1, 14, 21, 41, 42, 47 (V sul Freenove); GPIO3, 45, 46 sono di strapping, senza componenti.

Sblocca in parte **P-005** (interasse; resta la prova a secco), **P-026, P-035, P-039, P-040, P-079, P-086**: i dati richiesti (interasse, tensione e diodo sul 5V, pull-up su GPIO40, componenti sotto, levetta) hanno ora una risposta, con le riserve della tabella. Restano da guardare sul pezzo: la sigla RE1.3, il lato dei contatti del flat, le altezze sul retro, e se la UICPAL ha il PTC (si vede misurando la tensione sul pin 5V con la sola USB, 5 V sulla VBUS contro il pin).

---

## Q-21. Inserti a caldo e saldatura

Le fonti danno una regola e un intervallo, non un valore: **il valore di partenza va confermato dal provino 1.03 (D-076)**. Dove non c'e' una fonte primaria lo stato e' S.

### Inserti a caldo

Fonti:
- [CNC Kitchen, Tips & Tricks for Heat-Set Inserts](https://cnckitchen.com/blog/tips-and-tricks-for-heat-set-inserts) (letta il 15 ottobre 2026): punta da **10 a 20 °C sopra la temperatura di stampa**, cioe' "circa 225 °C per il PLA, 245 °C per il PETG, 265 °C per l'ABS", "i valori possono variare di poco"; fondere solo fino a circa il 90 % della profondita', poi spingere a filo con un attrezzo e **tenere fermo un momento**; foro cieco circa **1 mm piu' profondo** dell'inserto; "i fori stampati escono quasi sempre piu' piccoli del CAD";
- [Albany County Fasteners, heat set insert specs](https://www.albanycountyfasteners.com/media/64/3d/5a/1764619189/heat-set-insert-specs.pdf): **PLA 350-400 °F (177-204 °C), PETG 425-475 °F (218-246 °C)**, nylon 450-500 °F; posa di 3-4 s, raffreddamento di 45 s; se l'inserto non entra il materiale e' troppo freddo, se affonda troppo e' troppo caldo;
- [Prusa](https://www.prusa3d.com/product/heat-set-inserts-set-standard-200-pcs/): temperatura di stampa piu' 10 °C; per gli inserti a marchio (Ruthex) non c'e' una scheda tecnica raggiungibile, un rivenditore ([3DJake](https://www.3djake.ch/de-CH/ruthex/loetspitzen-einschmelzhilfe-set)) dice 10-15 °C sopra la temperatura dell'ugello;
- foro M3: [TU Dresden, Fakultaetswerkstatt, Waermeeinbettung bei FDM-3D-Drucken](https://tu-dresden.de/ing/elektrotechnik/die-fakultaet/fakultaetswerkstatt/werkstattteil-praezisionsmechanik/waermeeinbettung-bei-fdm-3d-drucken) (PLA, ToughPLA e PETG provati): **foro Ø4,0**, profondita' minima **6,7 mm** per l'inserto standard e 5,0 per quello corto, parete minima 1,6 mm, area piana minima Ø6,5; stesso Ø4,0 (inserto Ø4,6) nella tabella [Accu](https://accu.co.uk/p/488-threaded-insert-hole-size-charts-for-3d-printing-pla-petg-resin).

| Materiale | Temperatura di stampa | Punta (regola +10...+20 °C) | Da provare | Stato |
|---|---|---|---|---|
| **PLA** | 190-220 °C (tipico) | 215-225 °C (CNC Kitchen 225; Albany 177-204) | da 200 a 225 °C, partire da **210 °C** | S |
| **PETG-CF** (FlashForge) | 200-240 °C (pagina del prodotto) o 220-270 °C (pagina enterprise): non concordano | 245-260 °C (regola del PETG piu' un margine per le fibre) | da 240 a 260 °C a passi di 10, partire da **245 °C** | S: nessuna fonte parla di PETG-CF; il margine e' una mia stima |

Conseguenze:
- **P-058** (temperatura e tempo di posa nel PETG-CF e nel PLA): c'e' un valore di partenza con la fonte, da confermare con il provino 1.03. Gli inserti del kit Temu non hanno una scheda tecnica: possono comportarsi in modo diverso da quelli a marchio.
- Foro M3 **Ø4,0**: i provini 3,9 / 4,0 / 4,1 sono centrati sul valore indicato dalle fonti. La profondita' dei fori nel repository e' **6,7 mm** (la quota TU Dresden per l'inserto standard da 5,7): con un M3 × 5 restano 1,7 mm, con × 6 restano **0,7 mm, meno del millimetro** di CNC Kitchen. Il provino 1.03 con × 6 sul foro piu' sottile e' la verifica giusta.
- il PLA va posato **piu' freddo** del PETG-CF (circa 30-40 °C) e si tiene fermo l'inserto piu' a lungo: se gli inserti stanno anche in parti di PLA (placche, carapace), temperatura e tempo non sono quelli del PETG-CF.

### Saldatura del 14 AWG

Nessuna fonte primaria dichiara una temperatura per il 14 AWG; la scheda tecnica Kester [245](https://www.mouser.com/datasheet/2/213/TDS_245_flux-cored_wire-1131870.pdf) dà solo il liquidus (Sn63Pb37, 183 °C). Le temperature sono pratica generale ([LCSC, Solder Melting Point Guide](https://www.lcsc.com/blog/solder-melting-point-guide/), [bestpcbs](https://www.bestpcbs.com/blog/2026/09/soldering-temperature/); [Adafruit](https://learn.adafruit.com/adafruit-guide-excellent-soldering/tools): "il senza piombo puo' richiedere piu' calore e piu' flussante"). Stato **S** per tutta la tabella.

| Lega | Fusione | Punta | Per il 14 AWG (2,08 mm²) |
|---|---|---|---|
| Sn60Pb40 (LC60, B19) | 183-190 °C | 315-350 °C | punta a scalpello da 3-5 mm, **350 °C**, stagnare prima filo e capocorda |
| Sn99,3Cu0,7 senza piombo (20 g in casa) | circa 227 °C (liquidus) | 350-380 °C, piu' flussante | punta grossa, **370-380 °C**, preriscaldare il filo |
| Sn42Bi58 (se lo stagno "a bassa temperatura" e' questo) | 138 °C | 190-230 °C | vedi sotto |

**Stagno "a bassa temperatura": la scritta sulla bobina decide, i due casi sono gia' risolti.**
- **Al bismuto (Sn42Bi58, 138 °C):** non per i giunti di potenza e di vibrazione. Fonde a 138 °C (un giunto da 10-15 A puo' scaldarsi quanto basta); e' piu' fragile di Sn-Pb ([JLCPCB](https://jlcpcb.com/blog/low-temperature-solder-paste-sn-bi-guide): "piu' fragile del SAC305, da evitare dove c'e' caduta"; il produttore [AIM](https://aimsolder.com/products/sn42-bi58-low-temperature-solder-alloy/) dichiara una buona fatica e un allungamento del 55 %, senza prove indipendenti); **mai misto con Sn-Pb**: Bi, Sn e Pb formano un eutettico che fonde vicino a 95 °C (JLCPCB). Quindi non si usa in questo robot, e **B19 mantiene l'acquisto di LC60 (7,47 €)**.
- **Sn63Pb37 o Sn60Pb40 (183 °C, a volte venduto come "bassa temperatura"):** vale come LC60: si puo' **togliere dal BOM l'acquisto di LC60 (7,47 €)**; il diametro da 0,8 mm e' un po' sottile per il 14 AWG ma va bene.
- Altre leghe (Sn-Bi-Ag, In-Sn): valgono le regole del bismuto.

Conseguenza per **P-079**: la temperatura per il 14 AWG ha un valore di partenza (350 °C Sn-Pb, 370-380 °C senza piombo, punta grossa); la lega dello stagno "a bassa temperatura" resta all'utente **solo come lettura della scritta sulla bobina**, e il risultato per il BOM e' scritto qui. Il valore esatto si regola sul primo giunto: buono se e' lucido, il filo e' bagnato per tutta la spellatura e non c'e' stagno sulla guaina.
