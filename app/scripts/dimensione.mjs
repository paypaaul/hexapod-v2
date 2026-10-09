// Controllo della dimensione della build (dist/). Limiti da software.md 6.6: modelli 3D sotto 1-2 MB (qui il valore
// basso, 1 MB); l'app intera sotto 2 MB, perche' va nella partizione LittleFS del robot (7,8 MB, software.md 2.8)
// insieme a modelli ESP-DL, pesi della politica e scatola nera.

import { readdirSync, statSync } from 'node:fs';
import { dirname, join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const DIST = resolve(dirname(fileURLToPath(import.meta.url)), '..', 'dist');
const LIMITE_MODELLI = 1024 * 1024;
const LIMITE_TOTALE = 2 * 1024 * 1024;

function file(cartella) {
  return readdirSync(cartella, { withFileTypes: true }).flatMap((e) =>
    e.isDirectory() ? file(join(cartella, e.name)) : [join(cartella, e.name)],
  );
}

let tutti;
try {
  tutti = file(DIST);
} catch {
  console.error(`manca ${DIST}: lanciare prima "npm run build"`);
  process.exit(1);
}
let totale = 0;
let modelli = 0;
for (const f of tutti.sort()) {
  const n = statSync(f).size;
  const rel = relative(DIST, f);
  totale += n;
  if (rel.startsWith('modelli')) modelli += n;
  console.log(`${(n / 1024).toFixed(0).padStart(6)} KB  ${rel}`);
}
const kb = (n) => `${(n / 1024).toFixed(0)} KB`;
console.log(`modelli ${kb(modelli)} (limite ${kb(LIMITE_MODELLI)}), totale ${kb(totale)} (limite ${kb(LIMITE_TOTALE)})`);
if (modelli > LIMITE_MODELLI || totale > LIMITE_TOTALE) {
  console.error('build troppo grande');
  process.exit(1);
}
