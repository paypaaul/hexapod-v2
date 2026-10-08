# Studio dei componenti — versione MG996R

8 ottobre 2026, aggiornato la sera con le risposte dell'utente. Studio ridotto: copre solo ciò che cambia rispetto alla prima versione (servo, alimentazione, giunti, dimensionamento, stampa). Per ESP32, camera e SSC-32 valgono i dati già raccolti, riportati in `dimensioni-componenti.md`.

Legenda: **V** verificato su fonte primaria, **S** stimato o da fonte secondaria, **C** da confermare sul pezzo reale.

## In breve

- I servo dell'utente sono MG996R di AZDelivery: 55 g, 11 kgf·cm dichiarati a 6 V, **2,5 A di stallo** (18 servo: 45 A), tensione 4,8–7,2 V. La 2S diretta (8,4 V a piena carica) resta esclusa: serve un rail regolato.
- L'utente non può misurare né le quote né la corrente dei servo: si progetta sui dati dichiarati, prendendo sempre il caso peggiore, e con le sedi che non dipendono dalle quote in cui le fonti divergono. Un provino stampato della culla viene prima delle parti vere.
- Robot stimato a **2,6 kg**. Con il piede a 45 mm dall'asse del femore e l'asse a 100 mm da terra la coppia a tripode è il 50 % dello stallo dichiarato, con il ginocchio tra 63° e 78°: la marcia classica. Più bassa e larga costa di più (59 % a 90/55, 74 % a 70/70).
- **Alimentazione**: due regolatori Pololu da 6 V, uno per lato della SSC-32 (9 servo ciascuno), spenti di default e accesi dal firmware. La potenza entra nelle file degli header **dal retro della scheda**, non dai morsetti. Fusibile da 30 A, cavi da 12 AWG.
- **Batteria**: la OVONIC 2S 5200 mAh che l'utente ha già. 20–27 minuti di marcia classica, 15–17 in assetto basso.
- **Giunti**: cuscinetto flangiato 5 × 10 × 4 e perno Ø5 coassiali al servo, squadretta metallica a disco a 25 denti sull'albero.
- **Modello 3D del servo**: trovato (HowToMechatronics), coerente con il datasheet tranne l'altezza della cassa sotto le alette.

## Servo MG996R

Dati e fonti in `dimensioni-componenti.md`. Conseguenze per il progetto:

- **Tensione**: AZDelivery dichiara 4,8–7,2 V, Tower Pro 4,8–6,6 V. Rail a **6,0 V**: è la tensione a cui è dichiarata la coppia e sta dentro entrambi i campi.
- **Corrente**: 2,5 A di stallo e 0,5–0,9 A in movimento (V, datasheet AZDelivery). Tower Pro dichiara 1,4 A di stallo. Non potendo misurare, si dimensiona su **2,5 A**.
- **Quote**: le tre fonti (datasheet AZDelivery, tabella Tower Pro, modello STEP) concordano entro 0,5 mm dalle alette in su, cioè su tutto ciò che decide la posizione dell'albero; divergono di 2,2 mm sull'altezza della cassa sotto le alette. Le culle appoggiano il servo sulle alette e lasciano libero il fondo.
- **Squadrette**: in dotazione solo plastica. Per un robot da 2,6 kg si usano dischi in alluminio a 25 denti (il millerighe del modello è Ø6,0; i 25 denti sono il dato comune dei servo di questa taglia: S). Voce del BOM da approvare.
- **Fissaggio**: quattro fori nelle alette; i gommini si tolgono e il servo si avvita rigido, con viti M3 in inserti.
- **Corsa**: circa 180° dichiarati; le escursioni richieste stanno entro 110° per giunto.

## Alimentazione dei servo

### Quanto serve

Stima con la corrente proporzionale alla coppia richiesta: I ≈ 0,17 A + frazione dello stallo × (2,5 − 0,17) A. Sono stime (S): servono a scegliere i componenti, non a garantire i margini.

| Caso | Per lato (9 servo) | In tutto (rail a 6 V) |
|---|---|---|
| Fermo su sei zampe, assetto classico | circa 3 A | circa 6 A |
| Marcia classica a tripode (50 % dello stallo) | 5–6 A medi, picchi 12–15 A | 10–12 A medi |
| Marcia bassa (74 % dello stallo) | 8–9 A medi | 16–18 A medi |
| Tutti i servo in stallo | 22,5 A | 45 A: caso teorico, lo impedisce il firmware |

Il firmware deve limitare il tempo di sforzo a servo fermo e togliere il segnale (o spegnere il rail) se un giunto resta bloccato.

### Regolatori: due Pololu da 6 V, uno per lato

| Soluzione | Corrente | Costo indicativo | Pro | Contro |
|---|---|---|---|---|
| **2 × Pololu D42V110F6** (scelta) | 11 A tipici dichiarati a 42 V in ingresso; la famiglia va da 8 a 15 A e la corrente cresce al calare della tensione d'ingresso: con la 2S circa 13–14 A per regolatore (S) | circa 110 € | pin di abilitazione e power-good; **limita la corrente con gradualità** invece di spegnersi; protezione da inversione; dati e modello STEP del produttore | il dropout a corrente alta non è pubblicato in cifre: con la batteria quasi scarica il rail può scendere sotto 6 V |
| 2 × Pololu D24V150F6 | 15 A tipici, 32 A istantanei | circa 160 € | stesso ingombro, stessi fori, stessi pin: si monta al posto del D42V110F6 senza cambiare il corpo | costo; disponibilità razionata; Pololu indica la serie D42V110 come quella da preferire |
| 3 × Hobbywing UBEC 10A | 10 A, 15 A di picco | circa 60 € | economici, tensione selezionabile | nessun pin di abilitazione; dati solo da rivenditori; tre rail non si collegano alla SSC-32, che ne ha due |

Perché due e non tre: la SSC-32 ha due rail (VS1 e VS2). Con la potenza portata alle file degli header ogni rail è un solo nodo elettrico, quindi può avere un solo regolatore. Un regolatore per lato serve 9 servo: 5–9 A medi secondo l'assetto, contro circa 13 A disponibili. Se le prove al banco mostrano cali di tensione nella marcia bassa, si passa al D24V150F6 senza toccare il resto.

### Distribuzione: potenza dal retro della SSC-32

- I morsetti del clone hanno passo 3,5 mm (8–10 A, cavo fino a 1,5 mm²) e le piste non hanno dati; 9 MG996R per lato arrivano a 22,5 A di stallo. **La potenza non passa dai morsetti.**
- Le immagini dell'inserzione mostrano header a foro passante: sul retro, lungo la fila VS e lungo la fila di massa di ogni lato, si salda un filo di rame stagnato rigido da 1 mm (18 AWG) che tocca tutti i 16 pin. Il cavo del regolatore (16 AWG) arriva a metà della fila. Così ogni servo prende corrente dal proprio pin (circa 3 A ammessi per un pin da 0,64 mm) e le piste della scheda non portano quasi nulla.
- Si tolgono i due ponticelli "VS1 VS2" (i rail diventano indipendenti) e il ponticello "VS VL" (la logica ha la sua alimentazione).
- Lato sinistro del robot sui canali 0–15 (VS1), lato destro sui 16–31 (VS2).
- La SSC-32 va montata su distanziali da almeno 8 mm, per lasciare spazio ai fili sotto. Il retro della scheda non si vede in nessuna immagine: va controllato all'arrivo.
- Un condensatore da 2200 µF per lato, su una spina a tre poli in un canale libero, smorza i picchi.

### Accensione e protezioni

- **Rail spento di default** (principio della prima versione, D-019): i pin di abilitazione dei due regolatori sono tirati a massa da una resistenza e li accende l'ESP32 da GPIO42 attraverso un diodo. I servo ricevono tensione solo quando la SSC-32 sta già mandando impulsi: nessuno scatto all'accensione. Nel percorso di potenza non c'è nessun interruttore.
- **Fusibile principale F1** subito dopo la batteria: lama ATO/ATC da 30 A (15 A per le prime accensioni), portafusibile in linea da 12 AWG.
- **Cavi**: batteria → fusibile → derivazione a stella in 12 AWG; derivazione → ingresso di ciascun regolatore in 14 AWG; uscita del regolatore → file della SSC-32 in 16 AWG, il più corto possibile.
- **Connettore**: T-plug, come sul pacco. È anche il sezionamento di emergenza dei servo: deve restare a portata di mano.
- **Ramo logica** invariato: fusibile da 2 A, interruttore a pulsante Pololu #2813 con pin di spegnimento, regolatore da 5 V per l'ESP32, VL della SSC-32 dalla batteria (dopo l'interruttore), partitore sulla tensione di batteria, cicalino sulla presa di bilanciamento.

## Batteria

Scelta: **la OVONIC 2S 5200 mAh 50C hardcase che l'utente ha già.** Nessun acquisto.

| Criterio | Valore | Esito |
|---|---|---|
| Energia | 7,4 V × 5,2 Ah = 38,5 Wh; 30,8 Wh usabili (80 %) | |
| Marcia classica | 10–12 A a 6 V = 60–72 W; con il 90 % di rendimento e 2 W di logica, 69–82 W dalla batteria | **22–27 minuti** |
| Marcia bassa | 16–18 A a 6 V: 109–122 W | 15–17 minuti |
| Fermo in piedi | circa 6 A a 6 V: circa 42 W | circa 45 minuti |
| Scarica | picchi di 30–35 A contro 260 A continui ammessi | ampio margine |
| Massa | 245–259 g, il 10 % del robot | |
| Tensione | 6,0–8,4 V: regolatori in regolazione fino a circa 7 V; VL della SSC-32 (6–12 V) presa direttamente | compatibile |

Alternative scartate:

- **2S da 3000–4000 mAh**: 60–100 g in meno valgono 1–2 punti di coppia, ma tolgono il 25–40 % di autonomia e sono un acquisto.
- **3S**: i regolatori non andrebbero mai in dropout e i cavi porterebbero meno corrente, ma a piena carica (12,6 V) supera i 12 V ammessi sul VL della SSC-32, chiede un altro regolatore per la logica ed è un acquisto.

Da sapere: a fine carica, con il pacco sotto 7 V e corrente alta, i regolatori possono uscire di regolazione e il rail scendere un po' sotto 6 V. I servo funzionano fino a 4,8 V con meno coppia; il firmware ferma il robot a 3,5 V per cella. Un secondo pacco uguale, se si vuole cambiarlo al volo, è facoltativo.

## Controllo (invariato)

ESP32-S3-CAM UICPAL, camera OV3660 con flat da 75 mm, SSC-32 clone "V2.5". Assegnazione dei pin:

| Funzione | GPIO | Nota |
|---|---|---|
| UART1 TX → RX della SSC-32 | 21 | traslatore di livello a BSS138; nessun impulso spurio all'accensione |
| UART1 RX ← TX della SSC-32 | 14 | riserva: GPIO47 |
| Tensione di batteria | 1 (ADC1_CH0) | partitore 100 kΩ / 47 kΩ dopo l'interruttore |
| Abilitazione del rail servo | 42 | alto = acceso, attraverso un diodo; spento con il GPIO flottante |
| Spegnimento dell'interruttore | 41 | impulso alto = robot spento |
| Liberi | 2, 47 | 38/39/40 se non si usa la scheda TF |

Seriale a 115200 baud, 8N1 (da confermare sui LED della scheda). La SSC-32 si configura al banco via micro-USB prima di montarla.

Vincoli che il corpo nuovo deve rispettare: camera frontale con il flat da 61,5 mm utili tra testa e connettore; antenna dell'ESP32 fuori dal carbonio; USB, BOOT e RST raggiungibili da uno sportello; batteria sfilabile senza attrezzi; T-plug a portata di mano; SSC-32 su distanziali con spazio per i fili sul retro.

## Giunti

- Stesso principio della prima versione: giunto sostenuto su due lati, squadretta metallica sul lato dell'albero, perno e cuscinetto coassiali sul lato opposto, carico assiale sull'anello interno.
- Carichi: fino a circa 1,1 kgf per piede a tripode; momento flettente sul giunto della coxa fino a 13 kgf·cm, portato dalla coppia squadretta–perno: poche decine di newton sul perno.
- **Cuscinetto**: flangiato 5 × 10 × 4 (NMB LF-1050ZZ, venduto anche come MF105ZZ): carico statico 276 N, dinamico 714 N (V). La flangia dei generici varia da 11,2 a 11,7 mm: la sua sede è un parametro.
- **Perno**: spina cilindrica Ø5, lunghezza dal CAD; con tolleranza h8 se si trova, altrimenti m6 forzata e provata su un cuscinetto campione.
- Viteria: M3 con inserti a caldo per le parti strutturali e per i servo; M2 per i regolatori.

## Stampa

- Creator 5 Pro: volume 256 × 256 × 256 mm (S). Il corpo va pensato entro circa 250 mm di lunghezza, oppure diviso in due metà unite da una giunzione strutturale.
- Materiali come nella prima versione: PETG-CF per le parti strutturali, non caricato per le cover, TPU per i piedini.

## Cosa resta aperto

- Corrente reale e quote reali dei servo: non misurabili dall'utente. Si coprono con il caso peggiore e con un provino stampato.
- Retro della SSC-32: da guardare quando la scheda è sul banco, prima di saldare.
- Numero di prolunghe dei servo: dipende dalla lunghezza reale dei cavi (32 cm dichiarati da Tower Pro) e dai percorsi nel CAD.

## Fonti

- [AZDelivery, datasheet MG996R (PDF)](https://cdn.shopify.com/s/files/1/1509/1638/files/Servo_MG996R_Datenblatt.pdf)
- [AZDelivery, pagina prodotto MG996R](https://www.az-delivery.de/products/az-delivery-servo-mg996r)
- [Tower Pro, MG996R](https://www.towerpro.com.tw/product/mg996r/)
- [Modello STEP dell'MG996R (HowToMechatronics), copia su GitHub](https://github.com/Matthew-Garcia/SCARA-Robot/tree/main/3D_Models)
- [Pololu D42V110F6 (#5673)](https://www.pololu.com/product/5673) e [D24V150F6 (#2882)](https://www.pololu.com/product/2882)
- [Inserzione AliExpress della SSC32-V2.5](https://it.aliexpress.com/item/1005001888185034.html) (immagini della galleria)
- [Forum RobotShop: corrente massima della SSC-32](https://community.robotshop.com/forum/t/max-amp-draw-from-ssc-32/18267)
- [NMB LF-1050ZZ](https://product.minebeamitsumi.com/en/product/category/bearing/miniature_small/parts/LF1050ZZ.html)
- [Hobbywing UBEC 10A V2, scheda di un rivenditore](https://www.rcteam.com/en/products/hobbywing-ubec-10a-v2-2-6s-30603003)
- [FlashForge Creator 5 Pro, scheda di un rivenditore](https://eolasprints.com/products/flashforge-creator-5-pro-enclosed-industrial-3d-printer)
- [OVONIC 2S 5200 mAh, negozio del produttore](https://us.ovonicshop.com/products/ovonic-50c-7-4v-5200mah-2s1p-hardcase-deans-2pcs-lipo-battery) e [ampow.com](https://www.ampow.com/products/ovonic-50c-7-4v-5200mah-2s1p-hardcase-deans-lipo-battery)
