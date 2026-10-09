# STL delle parti della zampa (v0.1)

Esportati da Fusion il 9 ottobre 2026 (design "Hexapod v2 - MG996R"), nella terna della zampa: vanno orientati nello slicer come indicato. Sono file di prova: le quote marcate C (squadretta, giochi, forzamenti) si confermano con il provino.

| File | Orientamento di stampa | Note |
|---|---|---|
| `Tibia.stl` | faccia +Y (orlo della culla e fianco dello stinco) sul piatto | **provino della culla**: contiene una culla completa |
| `Coxa.stl` | faccia +Y (orlo della culla, braccio, anima) sul piatto | foro del perno orizzontale in stampa |
| `Coxa_Ponte.stl` | faccia superiore sul piatto (sede del disco verso l'alto) | |
| `Femore_B.stl` | faccia esterna della piastra dei perni sul piatto | blocco in piedi |
| `Femore_A.stl` | faccia esterna sul piatto | sedi delle squadrette verso l'alto |

Materiale: PETG-CF, ugello temprato 0,4, pareti 3 perimetri (1,2 mm), 4–5 strati sopra e sotto, riempimento 25 %.

## Provino della culla (da stampare per primo)

Stampare `Tibia.stl` e provare con un MG996R vero, senza gommini:

1. il servo deve scendere nella culla con il passacavo nella fessura dall'orlo alla finestra (D-049); la spina JR passa prima dalla finestra;
2. le due viti M3 × 8 lato coda negli inserti, le due lato albero nei fori pilota Ø2,5: il servo deve restare fermo senza gioco;
3. il cuscinetto LF-1050ZZ nella sede del fondo (Ø10 nominale): forzamento da regolare con il parametro `cus_sede_d`;
4. giochi della sede del servo (`gio_servo`, 0,2 per lato) e nervature di schiacciamento da decidere sul provino.

Il provino del giunto completo (ponte, squadretta, perni) aspetta la squadretta metallica comprata: le sue quote (`sq_*`) sono ancora stimate.
