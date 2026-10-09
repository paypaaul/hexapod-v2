import { defineConfig } from 'vite';

export default defineConfig({
  // percorsi relativi: l'app deve funzionare servita dal robot (LittleFS) come da un PC, da qualunque cartella
  base: './',
  build: {
    outDir: 'dist',
    // three.js da solo supera i 500 KB minificati: il limite vero lo controlla scripts/dimensione.mjs
    chunkSizeWarningLimit: 1000,
  },
});
