# STL delle parti stampate

Esportati da Fusion il 10 ottobre 2026 (design "Hexapod v2.1.0", dopo D-066) con `cad/script/esporta_stl.py`. Ogni file è nella terna del suo componente: terna della zampa per le parti della zampa, terna del robot per quelle del corpo. Gli orientamenti qui sotto sono proposte: li confermi tu nello slicer. Sono file di prova: le quote marcate C (squadretta, giochi, forzamenti) si confermano con il provino.

Materiali (scelta dell'utente, D-065): **PETG-CF nero** per le parti funzionali, **PLA** per le placche (bianco per ora; fascia, visiera, gonne e sportellino in un secondo colore, nero), **TPU 95A arancio** per i piedini.

## Zampa (sei di ognuna)

| File | Materiale | Orientamento di stampa proposto | Note |
|---|---|---|---|
| `Tibia.stl` | PETG-CF | fondo della culla (faccia −Y) sul piatto, apertura della culla in alto | **provino della culla**: contiene una culla completa. Lo stinco è simmetrico sul piano della zampa (D-065) e si stacca dal piatto verso la punta (fino a circa 17 mm): serve un supporto a cuneo sotto lo stinco. Dalla 2.1.1 c'è la gola dei fili sulla parete +X della culla con tre ponticelli: in questa posizione crescono come pareti in piedi, senza supporti (D-067) |
| `Coxa.stl` | PETG-CF | faccia +Y (orlo della culla, braccio, anima) sul piatto | foro del perno orizzontale in stampa |
| `Coxa_Ponte.stl` | PETG-CF | faccia superiore sul piatto (sede del disco verso l'alto) | |
| `Femore_B.stl` | PETG-CF | faccia esterna della piastra dei perni sul piatto | blocco in piedi; due fori per inserti M2 sulla faccia esterna (lama B) |
| `Femore_A.stl` | PETG-CF | faccia esterna sul piatto | sedi delle squadrette verso l'alto |
| `Cover_Femore_A.stl` | PLA | faccia interna (piana) sul piatto, bombatura in alto | si incastra sulle teste M3 del blocco |
| `Cover_Femore_B.stl` | PLA | faccia interna (piana) sul piatto, bombatura in alto | due fori svasati per viti M2 × 6 a testa piana (D-065) |
| `Cover_Tibia.stl` | PLA | retro aperto sul piatto, fronte in alto | il fronte fa da ponte fra i due smussi; supporti piccoli sotto i due tappi e il bossolo della vite |
| `Piedino.stl` | TPU 95A | bocca sul piatto, punta in alto | calza la punta dello stinco; nel modello la stretta è zero, da tarare sul provino (0 / −0,2 / −0,4 mm). Dalla 2.1.0 la suola è piana, con il pistoncino per l'FSR dentro e la tacca dei fili (D-066) |
| `Cover_Tibia_Diffusore.stl` | PLA bianco (o PETG traslucido fumé) | lastra sul piatto, bordino in alto | solo con le luci nelle tibie: si incastra da dentro nella finestra del guscio (D-066) |

## Corpo

| File | Materiale | Orientamento di stampa proposto | Note |
|---|---|---|---|
| `Corpo_Carapace.stl` + `Corpo_Fascia.stl` + `Corpo_Visiera.stl` + `Corpo_Gonne.stl` | PLA bianco (carapace) e PLA nero (gli altri tre) | capovolto, faccia a z 36 sul piatto | **un solo pezzo a due colori**: caricare i quattro file insieme (sono già allineati) e assegnare il materiale per oggetto; senza supporti |
| `Corpo_Sportello_Servizio.stl` | PLA nero | faccia in vista sul piatto | |
| `Corpo_Sportello.stl` | PETG-CF | faccia esterna (smussata) sul piatto | |
| `Corpo_Base.stl` | PETG-CF | vedi le note di stampa in D-056 | |
| `Corpo_Chiglia.stl` | PETG-CF | fondo sul piatto | |
| `Corpo_Vassoio.stl` | PLA (sta sotto l'antenna: niente carbonio) | piano sul piatto | |
| `Corpo_Slitta_Regolatore.stl` | PETG-CF | due copie | |
| `Corpo_Supporto_INA260_S.stl`, `Corpo_Supporto_INA260_D.stl` | PETG-CF | piastra sul piatto | solo con gli INA260 (X7): si appoggiano alla slitta e prendono la sua vite (M3 più lunga di 2,4) |
| `Corpo_Tappo_ToF.stl` | PLA nero | flangia sul piatto | chiude la finestra del ToF frontale finché il sensore manca |
| `Corpo_Fondo_Anello.stl` | PLA nero | disco sul piatto, gonna e sedi dei pixel in alto | chiude da sotto la camera nera dell'anello del pulsante: si infila sul corpo del pulsante dopo il dado e calza la parete della camera (forzamento leggero, D-067). Nelle due sedi va un pixel di striscia ciascuna, LED in su |
| `Corpo_Sportello_Servizio_Zaino.stl` | PLA nero | come lo sportellino | al posto dello sportellino, solo con il computer a zaino (tacca per l'USB-C) |

Parti in PETG-CF: ugello temprato 0,4, pareti 3 perimetri (1,2 mm), 4–5 strati sopra e sotto, riempimento 25 %.

## Attrezzi da banco (`attrezzi/`, D-066)

| File | Materiale | Orientamento di stampa proposto | Note |
|---|---|---|---|
| `attrezzi/Dima_Posa_1.stl`, `attrezzi/Dima_Posa_2.stl` | PLA o PETG | piastra sul piatto, denti in alto | dime di taratura: si infilano sui perni del femore dal lato B (lama B tolta); posa 1: imbardata 0, femore 0, ginocchio 90; posa 2: 30, 45, 135 |
| `attrezzi/Attrezzo_Cavalletto.stl` | PETG-CF | base sul piatto | regge il robot sotto la chiglia con le zampe libere; alto 137 mm |

## Provino della culla (da stampare per primo)

Stampare `Tibia.stl` e provare con un MG996R vero, senza gommini:

1. il servo deve scendere nella culla con il passacavo nella fessura dall'orlo alla finestra (D-049); la spina JR passa prima dalla finestra;
2. le due viti M3 × 8 lato coda negli inserti, le due lato albero nei fori pilota Ø2,5: il servo deve restare fermo senza gioco;
3. il cuscinetto LF-1050ZZ nella sede del fondo (Ø10 nominale): forzamento da regolare con il parametro `cus_sede_d`;
4. giochi della sede del servo (`gio_servo`, 0,2 per lato) e nervature di schiacciamento da decidere sul provino.

Il provino del giunto completo (ponte, squadretta, perni) aspetta la squadretta metallica comprata: le sue quote (`sq_*`) sono ancora stimate. Provini della passata estetica: tubo Ø5,4/5,6/5,7 su una testa M3 (lama A), tappo a rombo, nervature dello sportellino, collare del cicalino, stretta del piedino, inserti del kit Temu nei fori `ins_m3_d` e `ins_m2_d`.
