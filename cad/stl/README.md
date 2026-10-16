# STL delle parti stampate

Esportati da Fusion il 10 ottobre 2026 (design "Hexapod v2.1.0", dopo D-066) con `cad/script/esporta_stl.py`; rigenerati il 16 ottobre 2026 con le modifiche della 2.1.7 (D-076). Ogni file è nella terna del suo componente: terna della zampa per le parti della zampa, terna del robot per quelle del corpo. Gli orientamenti qui sotto sono proposte: li confermi tu nello slicer. Sono file di prova: le quote marcate C (squadretta, giochi, forzamenti) si confermano con il provino.

Materiali (scelta dell'utente, D-065): **PETG-CF nero** per le parti funzionali, **PLA** per le placche (bianco per ora; fascia, visiera, gonne e sportellino in un secondo colore, nero), **TPU 95A arancio** per i piedini.

## Zampa (sei di ognuna)

| File | Materiale | Orientamento di stampa proposto | Note |
|---|---|---|---|
| `Tibia.stl` | PETG-CF | fondo della culla (faccia −Y) sul piatto, apertura della culla in alto | **provino della culla**: contiene una culla completa. Lo stinco è simmetrico sul piano della zampa (D-065) e si stacca dal piatto verso la punta (fino a circa 17 mm): serve un supporto a cuneo sotto lo stinco. Dalla 2.1.1 c'è la gola dei fili sulla parete +X della culla con tre ponticelli: in questa posizione crescono come pareti in piedi, senza supporti (D-067); dalla 2.1.7 la gola è larga 4,5 e la sede delle luci è lunga 50,5 (P-063, P-062); il foro dell'inserto del guscio è profondo 7,7 |
| `Coxa.stl` | PETG-CF | faccia +Y (orlo della culla, braccio, anima) sul piatto | foro del perno orizzontale in stampa |
| `Coxa_Ponte.stl` | PETG-CF | faccia superiore sul piatto (sede del disco verso l'alto) | |
| `Femore_B.stl` | PETG-CF | faccia esterna della piastra dei perni sul piatto | blocco in piedi; due fori per inserti M2 sulla faccia esterna (lama B) |
| `Femore_A.stl` | PETG-CF | faccia esterna sul piatto | sedi delle squadrette verso l'alto |
| `Cover_Femore_A.stl` + `Cover_Femore_A_Feritoia.stl` | PLA bianco + PLA nero, in un solo pezzo | faccia interna (piana) sul piatto, faccia esterna e intarsio in alto | dalla 2.1.3 (D-070, sagoma del femore D-071): le 12 tasche delle teste sono fori ciechi dal piatto; si incastra sulle teste M3 del blocco. L'intarsio della feritoia è profondo 0,6 e si stampa insieme alla lama, come la fascia del carapace |
| `Cover_Femore_B.stl` + `Cover_Femore_B_Feritoia.stl` | PLA bianco + PLA nero, in un solo pezzo | faccia interna (piana) sul piatto, faccia esterna e intarsio in alto | tasche dei perni dal piatto; due fori per viti M2 × 5 a testa piana (D-073) a Z 1,5 (X 81 e 89, D-071), con le svasature tutte nell'intarsio nero (profondo 1,0) |
| `Cover_Tibia.stl` | PLA | retro aperto sul piatto, fronte in alto | il fronte fa da ponte fra i due smussi; supporti piccoli sotto i due tappi e il bossolo della vite. Dalla 2.1.7 una lamatura piana Ø6 sotto la testa della M3 × 10 (P-014) |
| `Piedino.stl` | TPU 95A | bocca sul piatto, punta in alto | calza la punta dello stinco; nel modello la stretta è zero (`pied_stretta`), da tarare sul provino 6: tre file in `attrezzi/Piedino_stretta_0.stl`, `_0.2.stl` e `_0.4.stl` (stretta 0 / 0,2 / 0,4 mm, P-016); per le zampe si stampa un solo valore, sempre `Piedino.stl` del modello. Dalla 2.1.0 la suola è piana, con il pistoncino per l'FSR dentro e la tacca dei fili (D-066) |
| `Cover_Tibia_Diffusore.stl` | PLA bianco (o PETG traslucido fumé) | lastra sul piatto, bordino in alto | solo con le luci nelle tibie: si incastra da dentro nella finestra del guscio (D-066) |

## Corpo

| File | Materiale | Orientamento di stampa proposto | Note |
|---|---|---|---|
| `Corpo_Carapace.stl` + `Corpo_Fascia.stl` + `Corpo_Visiera.stl` + `Corpo_Gonne.stl` | PLA bianco (carapace) e PLA nero (gli altri tre) | capovolto, faccia a z 36 sul piatto | **un solo pezzo a due colori**: caricare i quattro file insieme (sono già allineati) e assegnare il materiale per oggetto; senza supporti. Dalla 2.1.7: sede della scheda con testata a 90°, ganci della catena in più (x ±75 e davanti), fori pilota del ToF posteriore e costole dell'altoparlante |
| `Corpo_Sportello_Servizio.stl` | PLA nero | faccia in vista sul piatto | |
| `Corpo_Sportello.stl` | PETG-CF | faccia esterna (smussata) sul piatto | rebbi da 22,5 dalla 2.1.7 (P-007) |
| `Corpo_Base.stl` | PETG-CF | vedi le note di stampa in D-056 | dalla 2.1.7: colonne del vassoio Ø6 con inserto M2, fessure del tetto aperte verso la coda (P-001, P-003) |
| `Corpo_Chiglia.stl` | PETG-CF | fondo sul piatto | |
| `Corpo_Vassoio.stl` | PLA, colore libero (sta sotto l'antenna: niente carbonio; D-076, P-088) | piano sul piatto | dalla 2.1.7 si avvita sulle quattro colonne della base con M2 × 5 svasate a filo (fori Ø2,4 con svasatura da 0,9); asola del bus 7 × 4 in un'ala del piano (P-003, P-019) |
| `Corpo_Slitta_Regolatore.stl` | PETG-CF | faccia piana sul piatto, bugne in alto [C]; due copie | le due slitte sono lo stesso pezzo: la destra è la sinistra ruotata (P-099, P-100) |
| `Corpo_Supporto_INA260_S.stl`, `Corpo_Supporto_INA260_D.stl` | PETG-CF | piastra sul piatto | solo con gli INA260 (X7): si appoggiano alla slitta e prendono la sua vite (M3 più lunga di 2,4) |
| `Corpo_Tappo_ToF.stl` | PLA nero | flangia sul piatto | chiude la finestra del ToF frontale finché il sensore manca |
| `Corpo_Fondo_Anello.stl` | PLA nero | disco sul piatto, gonna e sedi dei pixel in alto | chiude da sotto la camera nera dell'anello del pulsante: si infila sul corpo del pulsante dopo il dado e calza la parete della camera (forzamento leggero, D-067). Nelle due sedi vanno due pixel di striscia ciascuna (16,7 mm a 120 LED/m, D-068; quattro in tutto, come X11), LED in su |
| `Corpo_Sportello_Servizio_Zaino.stl` | PLA nero | come lo sportellino | al posto dello sportellino, solo con il computer a zaino (tacca per l'USB-C) |
| `Corpo_Piastrina_IMU.stl` | PETG-CF | faccia inferiore sul piatto, svasature in alto | IMU GY-6500 (X4, D-074): si avvita sulle due bugne della Pololu con due M2 × 5 svasate (a filo, la scheda ci passa sopra); la scheda, con i pin verso +Y, prende due M2 × 6 nei fori pilota Ø1,7. Per montare la Pololu si toglie |
| `Corpo_Lunette_Microfoni.stl` | PLA, colore libero (D-076, P-078) | piatte sul piatto | quattro lunette, due per microfono MS3625 (X16, D-074): si posano alle estremità del telaio del microfono e centrano la scheda tonda sul foro. Sono simmetriche; per la Adafruit 3421 si tolgono |

Parti in PETG-CF: ugello temprato 0,4, pareti 3 perimetri (1,2 mm), 4–5 strati sopra e sotto, riempimento 25 %.

## Attrezzi da banco (`attrezzi/`, D-066)

| File | Materiale | Orientamento di stampa proposto | Note |
|---|---|---|---|
| `attrezzi/Dima_Posa_1.stl`, `attrezzi/Dima_Posa_2.stl` | PLA o PETG | piastra sul piatto, denti in alto | dime di taratura: si infilano sui perni del femore dal lato B (lama B tolta); posa 1: imbardata 0, femore 0, ginocchio 90; posa 2: 30, 45, 135 |
| `attrezzi/Dima_Calettamento.stl` | PLA o PETG | piastra sul piatto, denti in alto | terza dima di taratura (P-015): calettamento di robot.yaml, imbardata 0, femore 20, ginocchio 100; segue `robot.yaml` (rifarla se cambia) |
| `attrezzi/Attrezzo_Cavalletto.stl` | PETG-CF | base sul piatto | regge il robot sotto la chiglia con le zampe libere; alto 137 mm |
| `attrezzi/Attrezzo_Provino_Inserti.stl` | PETG-CF | faccia con le scritte in alto | provino degli inserti (P-057): 4 fori M3 Ø3,9 / 4,0 / 4,1 / 4,2 profondi 6,7 e 4 fori M2 Ø2,9 / 3,0 / 3,1 / 3,4 profondi 4,0, con il diametro inciso sopra ogni foro (scritte da 0,6: da guardare sul primo pezzo). Dopo la prova il valore va in `ins_m3_d`, `ins_m2_d` (e `_l`) |
| `attrezzi/Attrezzo_Bussola_Perno.stl` | PETG-CF | faccia con la tasca sul piatto | bussola di battuta (P-065): appoggia sulla faccia interna del mozzo del femore B (tasca Ø6,8 per il rialzo) e il perno Ø5 × 12 premuto nel foro cieco Ø5,5 si ferma con la sporgenza giusta di 1,4 |
| `attrezzi/Attrezzo_Estrattore_Asta.stl` + `attrezzi/Attrezzo_Estrattore_Tubo.stl` | PETG-CF | asta in piedi sulla testa; tubo sul piatto | estrazione di cuscinetti e perni (P-065): l'asta passa nel foro Ø7,2 della culla e spinge l'anello interno o il perno; il tubo si appoggia al mozzo e riceve il pezzo. Si stampano solo se il forzamento del provino non è leggero |
| `attrezzi/Attrezzo_Provino_Luce_Nero.stl` + `attrezzi/Attrezzo_Provino_Luce_Bianco.stl` | PLA nero + PLA bianco, in una stampa a due colori | fondo sul piatto, bianco in alto (le strisce di bianco fanno ponte sulle camere) | provino di luce (X10, D-069): camere da 2, 4 e 6 mm sotto bianchi da 0,4 a 1,6 e l'anello del pulsante con l'intarsio nero; uno spezzone di striscia da 120 LED/m nei canali sotto |
| `attrezzi/Attrezzo_Provino_Tasche_Base.stl` + `attrezzi/Attrezzo_Provino_Tasche_Lama.stl` | PETG-CF (base) e PLA bianco (lamina), stampe separate | base sul piatto; lamina con le tasche sul piatto, come la lama A | provino delle tasche della lama A (D-072). Nella base si avvita una vite M3 × 6 ISO 4762 nel foro pilota. La lamina, spessa 4,0 come la lama A, ha sei tasche profonde 3,2; da 1 a 6 puntini accanto a ognuna: 1–4 lisce da Ø5,4, 5,5, 5,6 e 5,7; 5 e 6 da Ø6,0 con tre costole che stringono a 5,3 e 5,4. Si preme ogni tasca sulla testa: quella che tiene bene senza forzare va in `cov_testa_d`, o si passa alle costole |

## Provino della culla (da stampare per primo)

Stampare `Tibia.stl` e provare con un MG996R vero, senza gommini:

1. il servo deve scendere nella culla con il passacavo nella fessura dall'orlo alla finestra (D-049); la spina JR passa prima dalla finestra;
2. le due viti M3 × 8 lato coda negli inserti, le due lato albero nei fori pilota Ø2,5: il servo deve restare fermo senza gioco;
3. il cuscinetto LF-1050ZZ nella sede del fondo (Ø10 nominale): forzamento da regolare con il parametro `cus_sede_d`;
4. giochi della sede del servo (`gio_servo`, 0,2 per lato) e nervature di schiacciamento da decidere sul provino.

Il provino del giunto completo (ponte, squadretta, perni) aspetta la squadretta metallica comprata: le sue quote (`sq_*`) sono ancora stimate. Provini della passata estetica: tubo Ø5,4/5,6/5,7 su una testa M3 (lama A), tappo a rombo, nervature dello sportellino, collare del cicalino, stretta del piedino, inserti del kit Temu nei fori `ins_m3_d` e `ins_m2_d`.
