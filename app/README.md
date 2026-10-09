# Gemello digitale nel browser (app/)

Il robot in 3D, dall'URDF generato (`robot/generati/esapode.urdf`) con le mesh dei segmenti esportate dal CAD, che
riproduce il **tripode** e la **rotazione sul posto**. Cursori per h (altezza dell'asse dei femori), xf0 (distanza del
piede dall'asse del femore), giro (gradi di rotazione del corpo a ogni passo) e periodo del ciclo. È la prima forma del
gemello di `docs/software.md` 6.6; poi l'app servita dal robot mostrerà le pose comandate e previste che arrivano dalla
telemetria.

**Le pose sono comandate, non misurate**: le calcola il generatore d'andatura e l'app lo scrive in cima al pannello. Il
corpo si sposta come farebbe se i piedi in appoggio non scivolassero. La guardia (ginocchio minimo, somma tra vicine,
velocità) qui non c'è: l'app segnala in rosso solo gli angoli oltre i fine corsa meccanici dell'URDF.

## Come si usa

Serve Node.js 22.18 o più recente (`brew install node`). Nessun servizio esterno: tutto è nella build.

```
cd app
npm ci
npm run dev          # http://localhost:5173, ricarica a ogni modifica
npm test             # formule contro il CAD (node:test, senza compilazione)
npm run build        # dist/, da servire come file statici (anche dal robot)
npm run dimensione   # controlla la dimensione di dist/
```

Una vista si può condividere con l'indirizzo: `?andatura=rotazione&h=70&xf0=70&giro=20&periodo=1.5&fase=0.3`.

## Cosa c'è

| Percorso | Contenuto |
|---|---|
| `src/andatura.ts` | tripode e rotazione sul posto, con la cinematica inversa: stesse formule di `cad/script/assieme.py` → `pose_tripode` e di `sim/andatura.py` |
| `src/geometria.ts` | coxe, Lc, Lf, Lt e limiti letti dall'URDF |
| `src/main.ts` | scena three.js, caricamento con urdf-loader, comandi, animazione |
| `scripts/modelli.mjs` | prepara `public/modelli/` (generata, ignorata da git): copia l'URDF e converte gli STL in GLB compatti |
| `scripts/dimensione.mjs` | limiti della build: modelli sotto 1 MB, totale sotto 2 MB |
| `test/andatura.test.ts` | geometria uguale a `cad.json`, pose uguali a `cad.json` → `cicli_verificati` entro 0,01°, costanti uguali a `robot.yaml` |

### Perché le pose le calcola il TypeScript

I cursori sono continui: con le pose precalcolate in Python servirebbe una griglia di h × xf0 × giro × fasi, pesante
e comunque a scatti. Le formule sono poche righe e restano uguali alle altre grazie al test, che le confronta con le
stesse pose del CAD usate per il generatore Python e per il nucleo C++. Le costanti che l'URDF non contiene (tripodi,
assetto, passo, alzata) sono in `src/andatura.ts` e il test le confronta con `robot.yaml`.

### Mesh

Gli STL dei segmenti pesano 2,4 MB (il corpo 2 MB). `scripts/modelli.mjs` salda i vertici ripetuti, scrive le
posizioni come interi a 16 bit con passo di 0,01 mm (estensione glTF KHR_mesh_quantization) e lascia fuori le normali
(ombreggiatura piatta): 444 KB in tutto, senza decimare e senza dipendenze. Build intera: circa 1,2 MB (three.js è
quasi tutto il resto).
