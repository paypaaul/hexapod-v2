# STL delle parti stampate

Esportati da Fusion il 9 ottobre 2026 (design "Hexapod v2 - MG996R", versione 24, dopo la passata estetica D-060…D-063) con `cad/script/esporta_stl.py`. Ogni file è nella terna del suo componente: terna della zampa per le parti della zampa, terna del robot per quelle del corpo. Vanno orientati nello slicer come indicato. Sono file di prova: le quote marcate C (squadretta, giochi, forzamenti) si confermano con il provino.

## Zampa (sei di ognuna)

| File | Materiale | Orientamento di stampa | Note |
|---|---|---|---|
| `Tibia.stl` | PETG-CF | faccia +Y (orlo della culla) sul piatto | **provino della culla**: contiene una culla completa. Lo stinco è simmetrico (D-062) e sale dal piatto fino a circa 10 mm alla punta: supporto a cuneo sotto lo stinco, con interfaccia nell'altro materiale |
| `Coxa.stl` | PETG-CF | faccia +Y (orlo della culla, braccio, anima) sul piatto | foro del perno orizzontale in stampa |
| `Coxa_Ponte.stl` | PETG-CF | faccia superiore sul piatto (sede del disco verso l'alto) | |
| `Femore_B.stl` | PETG-CF | faccia esterna della piastra dei perni sul piatto | blocco in piedi |
| `Femore_A.stl` | PETG-CF | faccia esterna sul piatto | sedi delle squadrette verso l'alto |
| `Cover_Femore_A.stl` | PETG bianco | faccia interna (piana) sul piatto, bombatura in alto | |
| `Cover_Femore_B.stl` | PETG bianco | **da decidere** | le due spine Ø3 × 3 sporgono dalla faccia interna, quindi quella faccia non può stare sul piatto: o si stampa con la faccia bombata in giù e un supporto d'interfaccia sotto i bordi (al massimo 1 mm), o le spine diventano fori e si usano spine separate (da decidere con il provino) |
| `Piedino.stl` | TPU 95A arancio | bocca sul piatto, punta in alto | calza la punta dello stinco; nel modello la stretta è zero, da tarare sul provino (0 / −0,2 / −0,4 mm) |
| `Cover_Tibia.stl` | PETG bianco | retro aperto sul piatto, fronte in alto | il fronte fa da ponte fra i due smussi; supporti piccoli sotto i due tappi e il bossolo della vite, da confermare nello slicer |

## Corpo

| File | Materiale | Orientamento di stampa | Note |
|---|---|---|---|
| `Corpo_Carapace.stl` + `Corpo_Fascia.stl` + `Corpo_Visiera.stl` + `Corpo_Gonne.stl` | PETG bianco (carapace), PETG nero (gli altri tre) | capovolto, faccia a z 36 sul piatto | **un solo pezzo a due colori**: caricare i quattro file insieme (sono già allineati) e assegnare il materiale per oggetto; senza supporti |
| `Corpo_Sportello_Servizio.stl` | PETG nero | faccia in vista sul piatto | |
| `Corpo_Sportello.stl` | PETG bianco | faccia esterna (smussata) sul piatto | |
| `Corpo_Base.stl` | PETG-CF | vedi le note di stampa in D-056 | |
| `Corpo_Chiglia.stl` | PETG-CF | fondo sul piatto | |
| `Corpo_Vassoio.stl` | PETG nero (non caricato: sta sotto l'antenna) | piano sul piatto | |
| `Corpo_Slitta_Regolatore.stl` | PETG-CF | due copie | |

Materiale strutturale: PETG-CF, ugello temprato 0,4, pareti 3 perimetri (1,2 mm), 4–5 strati sopra e sotto, riempimento 25 %. Cover e carapace in PETG non caricato (colori ancora da approvare: BOM, domanda 7).

## Provino della culla (da stampare per primo)

Stampare `Tibia.stl` e provare con un MG996R vero, senza gommini:

1. il servo deve scendere nella culla con il passacavo nella fessura dall'orlo alla finestra (D-049); la spina JR passa prima dalla finestra;
2. le due viti M3 × 8 lato coda negli inserti, le due lato albero nei fori pilota Ø2,5: il servo deve restare fermo senza gioco;
3. il cuscinetto LF-1050ZZ nella sede del fondo (Ø10 nominale): forzamento da regolare con il parametro `cus_sede_d`;
4. giochi della sede del servo (`gio_servo`, 0,2 per lato) e nervature di schiacciamento da decidere sul provino.

Il provino del giunto completo (ponte, squadretta, perni) aspetta la squadretta metallica comprata: le sue quote (`sq_*`) sono ancora stimate. Provini della passata estetica (specifica, sezione 6): tubo Ø5,4/5,6/5,7 su una testa M3, spina Ø2,9/3,0/3,1 nel foro, tappo a rombo, nervature dello sportellino, collare del cicalino.
