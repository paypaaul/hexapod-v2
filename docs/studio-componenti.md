# Studio dei componenti — versione MG996R

8 ottobre 2026. Studio ridotto: copre solo ciò che cambia rispetto alla prima versione (servo, alimentazione, giunti, dimensionamento, stampa). Per ESP32, camera e SSC-32 valgono i dati già raccolti, riportati in `dimensioni-componenti.md`.

Legenda: **V** verificato su fonte primaria, **S** stimato o da fonte secondaria, **C** da confermare sul pezzo reale.

## In breve

- I servo dell'utente sono MG996R di AZDelivery: 55 g, 11 kgf·cm dichiarati a 6 V, **2,5 A di stallo** (18 servo: 45 A), tensione 4,8–7,2 V. La 2S diretta (8,4 V a piena carica) resta esclusa: serve un rail regolato.
- Robot stimato a **2,6 kg**. Con il piede a 45 mm dall'asse del femore e l'asse a 100 mm da terra la coppia a tripode è il 50 % dello stallo dichiarato, con il ginocchio tra 63° e 78°: è la marcia classica che l'utente si aspetta. Più bassa e larga costa di più (59 % a 90/55, 74 % a 70/70).
- L'alimentazione va rifatta: rail a 6,0 V, tre regolatori (uno per coppia di zampe), potenza distribuita **fuori** dalla SSC-32, fusibile da 30–40 A, cavi da 12 AWG. La batteria da 5200 mAh che l'utente ha è adeguata.
- Giunti: stessa idea (cuscinetto e perno coassiali al servo), con cuscinetti da 4 o 5 mm di foro e squadrette metalliche a 25 denti.
- Prima di disegnare servono alcune misure su un servo reale (vedi in fondo).

## Servo MG996R

Dati e fonti in `dimensioni-componenti.md`. Conseguenze per il progetto:

- **Tensione**: AZDelivery dichiara 4,8–7,2 V, Tower Pro 4,8–6,6 V. Rail a **6,0 V**: è la tensione a cui è dichiarata la coppia e sta dentro entrambi i campi. Salire a 6,6–7,2 V darebbe più coppia ma più calore e meno vita; resta una leva da provare al banco, quindi il regolatore conviene a tensione selezionabile.
- **Corrente**: 2,5 A di stallo e 0,5–0,9 A in movimento (V, datasheet AZDelivery). Tower Pro dichiara 1,4 A di stallo: il valore vero va misurato su uno dei 18.
- **Squadrette**: in dotazione solo plastica. Il millerighe dei servo di taglia standard di questo tipo è a 25 denti (S, da contare): esistono squadrette a disco in alluminio a 25 denti con fori M3, economiche. Per un robot da 2,6 kg sono la scelta consigliata; è una voce d'acquisto da approvare.
- **Fissaggio**: quattro fori nelle alette (due per parte) con gommini e boccole. Nelle sedi stampate i gommini si tolgono e si avvita in inserti o dadi: gioco zero.
- **Corsa**: circa 180° dichiarati; le escursioni richieste (vedi dimensionamento) stanno entro 110° per giunto.

## Alimentazione dei servo

### Quanto serve

| Caso | Corrente sul rail a 6 V | Come è calcolata |
|---|---|---|
| Fermo su sei zampe | circa 7 A | 12 giunti carichi a circa 0,6 A |
| Marcia a tripode | 12–14 A medi | 6 giunti in appoggio al 50 % dello stallo (1,3 A), 6 in volo a 0,5 A, 6 coxe a 0,3 A |
| Picchi (partenze, urti) | 20–25 A | stima |
| Tutti i 18 servo in stallo | 45 A | 18 × 2,5 A: caso teorico |

Sono stime (S): si chiudono misurando la corrente di un servo sotto carico noto.

Criterio proposto: **continui almeno 15 A, picchi almeno 30 A**, con limitazione di corrente che interviene oltre. Dimensionare sui 45 A continui raddoppierebbe costo e peso per un caso che il firmware deve comunque impedire (tempo massimo di sforzo a servo fermo, poi segnale tolto).

### Regolatori candidati

| Soluzione | Corrente | Costo indicativo | Pro | Contro |
|---|---|---|---|---|
| **3 × Hobbywing UBEC 10A V2** (2–6S; uscita 6,0 / 7,4 / 8,4 V) | 30 A continui, 45 A di picco | circa 60 € | uno per coppia di zampe (6 servo: 15 A di stallo = il suo picco); un guasto non ferma tutto; tensione selezionabile | nessun pin di abilitazione; dati da rivenditori (S); ingresso minimo 6 V: caduta minima da verificare con la 2S scarica |
| 2 × Pololu D42V110F6 | 22 A dichiarati (circa 27 stimati con ingresso basso) | circa 110 € | pin di abilitazione e power-good, protezione da inversione, dati completi e modello STEP | costo; tensione fissa a 6 V |
| 2 × Pololu D24V150F6 | 30 A continui, 64 A di picco | circa 160 US$ | la più robusta | costo; disponibilità razionata; il produttore consiglia la serie nuova |
| Modulo buck generico "300 W 20 A" (come nella v1) | 8–12 A reali senza ventola (S) | 5–10 € l'uno | economico, forse già in casa | ingombrante, dati inaffidabili, nessuna protezione dichiarata |

Proposta: **tre UBEC da 10 A**, uno per coppia di zampe (anteriori, medie, posteriori). Da decidere con l'utente nella fase 2, anche in base a com'è andato il buck della v1.

### Distribuzione

- I morsetti e le piste della SSC-32 non sono fatti per questa corrente: l'originale Lynxmotion è data per circa 15 A di picco per lato (S, forum del produttore), il clone ha morsetti a passo 3,5 mm da 8–10 A. Con 9 MG996R per lato lo stallo è 22 A.
- **La potenza dei servo non passa dai morsetti della SSC-32.** Due strade, da scegliere con una foto del lato saldature del clone:
  1. saldare i cavi di alimentazione direttamente sulle file di positivo e massa degli header, in più punti per lato (nessun componente in più; i singoli pin da 2,54 mm portano circa 3 A, uno per servo);
  2. tre basette di distribuzione, una per regolatore, con sei connettori a tre pin ciascuna: positivo e massa su sbarre di filo grosso, solo il segnale prosegue verso la SSC-32. Più cablaggio, ma la SSC-32 non porta corrente.
- La massa di segnale tra SSC-32 e rail dei servo resta comune.

### Protezioni e cavi

- **Fusibile principale** subito dopo la batteria: lama standard (ATO) da 30 A di base, 40 A se le misure lo chiedono; portafusibile da 12 AWG. Come nella v1, tra batteria e regolatori.
- **Cavi**: batteria → fusibile → derivazione in 12 AWG (quello dei cavi del pacco); verso ogni regolatore 14–16 AWG; dai regolatori alla distribuzione 16 AWG.
- **Connettore**: T-plug, come sul pacco (regge 40–60 A).
- **Accensione**: con gli UBEC il rail è vivo appena si collega la batteria. I servo restano molli finché la SSC-32 non manda impulsi, quindi non scattano all'accensione; lo spegnimento d'emergenza è togliere gli impulsi da firmware e staccare il T-plug, che deve restare a portata di mano. Se si vuole il rail spento di default come nella prima versione servono regolatori con il pin di abilitazione (Pololu).
- **Ramo logica** invariato: fusibile da 2 A, interruttore a pulsante con pin di spegnimento, regolatore da 5 V per l'ESP32, VL della SSC-32 dalla batteria, partitore sulla tensione di batteria, cicalino sulla presa di bilanciamento.

### Batteria

La OVONIC 2S 5200 mAh 50C che l'utente ha: 38 Wh, 260 A continui ammessi contro 45 A di caso peggiore. Autonomia stimata in marcia: 12–14 A a 6 V sono circa 85–95 W con le perdite, cioè 11–13 A dalla batteria: **20–25 minuti** con l'80 % della capacità. Pesa circa 250 g, il 10 % del robot.

## Controllo (invariato)

ESP32-S3-CAM UICPAL, camera OV3660 con flat da 75 mm, SSC-32 clone "V2.5". Assegnazione dei pin:

| Funzione | GPIO | Nota |
|---|---|---|
| UART1 TX → RX della SSC-32 | 21 | traslatore di livello a BSS138; nessun impulso spurio all'accensione |
| UART1 RX ← TX della SSC-32 | 14 | riserva: GPIO47 |
| Tensione di batteria | 1 (ADC1_CH0) | partitore 100 kΩ / 47 kΩ dopo l'interruttore |
| Abilitazione del rail servo | 42 | solo se i regolatori hanno il pin di abilitazione |
| Spegnimento dell'interruttore | 41 | impulso alto = robot spento |
| Liberi | 2, 47 | 38/39/40 se non si usa la scheda TF |

Seriale a 115200 baud, 8N1 (da confermare sui LED della scheda). La SSC-32 si configura al banco via micro-USB prima di montarla.

Vincoli che il corpo nuovo deve rispettare: camera frontale con il flat da 61,5 mm utili tra testa e connettore; antenna dell'ESP32 fuori dal carbonio; USB, BOOT e RST raggiungibili da uno sportello; batteria sfilabile senza attrezzi; T-plug a portata di mano.

## Giunti

- Stesso principio della prima versione: giunto sostenuto su due lati, squadretta sul lato dell'albero, perno e cuscinetto coassiali sul lato opposto, carico assiale sull'anello interno.
- Carichi: fino a circa 1,1 kgf per piede a tripode; momento flettente sul giunto della coxa fino a 13 kgf·cm, portato dalla coppia squadretta–perno a circa 50 mm di distanza: poche decine di newton sul perno.
- Candidati: cuscinetto flangiato **MF105ZZ** (5 × 10 × 4) con perno Ø5, oppure **F684ZZ** (4 × 9 × 4) con perno Ø4. Entrambi abbondanti per i carichi; il perno più grosso lavora meglio nella plastica. Quote da verificare su scheda del produttore nella fase 2; l'acquisto lo cura l'utente.
- Viteria: M3 con inserti a caldo per le parti strutturali, M2/M2,5 dove lo spazio manca.

## Stampa

- Creator 5 Pro: volume 256 × 256 × 256 mm (S). Il corpo va pensato entro circa 250 mm di lunghezza, oppure diviso in due metà unite da una giunzione strutturale.
- Materiali come nella prima versione: PETG-CF per le parti strutturali, non caricato per le cover.

## Misure e risposte che servono dall'utente

1. **Su un servo**: peso; lunghezza, larghezza e altezza della cassa; distanza dell'asse dell'albero dalle due estremità; quota e spessore delle alette; interasse e diametro dei quattro fori; numero di denti e diametro del millerighe; vite centrale; da dove esce il cavo e quanto è lungo.
2. **Corrente di stallo** di un servo a 6 V (alimentatore o batteria con il buck della v1, multimetro in serie, squadretta bloccata per un paio di secondi).
3. **Buck della v1**: modello o foto, e se scaldava o cedeva.
4. **SSC-32**: foto del lato saldature, per decidere come portare la potenza.
5. **Batteria**: misure e peso del pacco reale, genere del T-plug.
6. Un modello 3D dell'MG996R, se ne ha uno.

## Fonti

- [AZDelivery, datasheet MG996R (PDF)](https://cdn.shopify.com/s/files/1/1509/1638/files/Servo_MG996R_Datenblatt.pdf)
- [AZDelivery, pagina prodotto MG996R](https://www.az-delivery.de/products/az-delivery-servo-mg996r)
- [Tower Pro, MG996R](https://www.towerpro.com.tw/product/mg996r/)
- [Pololu, D24V150Fx (#2885 e famiglia)](https://www.pololu.com/product/2885)
- [Hobbywing UBEC 10A V2, scheda di un rivenditore](https://www.rcteam.com/en/products/hobbywing-ubec-10a-v2-2-6s-30603003) e [altra scheda](https://ozrc.com.au/products/hobbywing-ubec-10a-2-6s-6-0v-8-4v-external-bec-30603003)
- [Hobbywing, UBEC 10A HV (modello diverso, 3–14S)](https://www.hobbywing.com/en/products/ubec-10a-hv289)
- [Forum RobotShop: corrente massima della SSC-32](https://community.robotshop.com/forum/t/max-amp-draw-from-ssc-32/18267)
- [Lynxmotion SSC-32U, guida utente (PDF)](https://cdn.robotshop.com/media/d/dsp/rb-dsp-07/pdf/lynxmotion_ssc-32u_usb_user_guide.pdf)
- [FlashForge Creator 5 Pro, scheda di un rivenditore](https://eolasprints.com/products/flashforge-creator-5-pro-enclosed-industrial-3d-printer)
- [OVONIC 2S 5200 mAh, negozio del produttore](https://us.ovonicshop.com/products/ovonic-50c-7-4v-5200mah-2s1p-hardcase-deans-2pcs-lipo-battery) e [ampow.com](https://www.ampow.com/products/ovonic-50c-7-4v-5200mah-2s1p-hardcase-deans-lipo-battery)
