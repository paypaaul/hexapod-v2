// Prepara i modelli per l'app in public/modelli/: l'URDF generato (robot/generati/esapode.urdf, tools/genera_modelli.py)
// e le mesh dei segmenti (robot/mesh/*.stl, esportate dal CAD) convertite in GLB compatti.
//
// Compressione senza dipendenze: vertici saldati (l'STL ripete ogni vertice in ogni triangolo), posizioni intere a
// 16 bit con passo di 0,01 mm (KHR_mesh_quantization; il corpo arriva a 118 mm, il campo e' +-327 mm), indici a 16 bit
// quando bastano, niente normali (l'app usa l'ombreggiatura piatta). Le mesh restano in mm, come gli STL: la scala
// 0.001 dell'URDF le porta in metri. Uscita deterministica.

import { copyFileSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const APP = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const REPO = resolve(APP, '..');
const MESH = join(REPO, 'robot', 'mesh');
const URDF = join(REPO, 'robot', 'generati', 'esapode.urdf');
const USCITA = join(APP, 'public', 'modelli');
const PASSO_MM = 0.01;

function leggiStl(percorso) {
  const b = readFileSync(percorso);
  const n = b.readUInt32LE(80);
  if (b.length !== 84 + 50 * n) throw new Error(`${percorso}: non e' un STL binario (${n} triangoli, ${b.length} byte)`);
  const v = new Float32Array(n * 9);
  for (let t = 0; t < n; t++) {
    for (let k = 0; k < 9; k++) v[t * 9 + k] = b.readFloatLE(84 + t * 50 + 12 + k * 4);
  }
  return v;
}

function salda(v) {
  const indice = new Map();
  const pos = [];
  const tri = [];
  const limite = 32767;
  for (let t = 0; t < v.length / 9; t++) {
    const ids = [];
    for (let k = 0; k < 3; k++) {
      const q = [0, 1, 2].map((c) => Math.round(v[t * 9 + k * 3 + c] / PASSO_MM));
      if (q.some((x) => Math.abs(x) > limite)) throw new Error(`vertice fuori dal campo a 16 bit: ${q}`);
      const chiave = q.join(',');
      let i = indice.get(chiave);
      if (i === undefined) {
        i = pos.length / 3;
        indice.set(chiave, i);
        pos.push(...q);
      }
      ids.push(i);
    }
    if (ids[0] !== ids[1] && ids[1] !== ids[2] && ids[0] !== ids[2]) tri.push(...ids);
  }
  return { pos, tri };
}

function glb({ pos, tri }, nome) {
  const nv = pos.length / 3;
  // posizioni a passo di 8 byte (x, y, z e un riempimento): gli attributi vanno allineati a 4 byte
  const bufPos = Buffer.alloc(nv * 8);
  for (let i = 0; i < nv; i++) for (let c = 0; c < 3; c++) bufPos.writeInt16LE(pos[i * 3 + c], i * 8 + c * 2);
  const corti = nv <= 65535;
  const bufIdx = Buffer.alloc(tri.length * (corti ? 2 : 4) + (corti && tri.length % 2 ? 2 : 0));
  tri.forEach((x, i) => (corti ? bufIdx.writeUInt16LE(x, i * 2) : bufIdx.writeUInt32LE(x, i * 4)));
  const min = [0, 1, 2].map((c) => Math.min(...pos.filter((_, i) => i % 3 === c)));
  const max = [0, 1, 2].map((c) => Math.max(...pos.filter((_, i) => i % 3 === c)));
  const bin = Buffer.concat([bufPos, bufIdx]);
  const json = {
    asset: { version: '2.0', generator: 'app/scripts/modelli.mjs' },
    extensionsUsed: ['KHR_mesh_quantization'],
    extensionsRequired: ['KHR_mesh_quantization'],
    scene: 0,
    scenes: [{ nodes: [0] }],
    nodes: [{ name: nome, mesh: 0, scale: [PASSO_MM, PASSO_MM, PASSO_MM] }],
    meshes: [{ name: nome, primitives: [{ attributes: { POSITION: 0 }, indices: 1, mode: 4 }] }],
    accessors: [
      { bufferView: 0, componentType: 5122, count: nv, type: 'VEC3', min, max },
      { bufferView: 1, componentType: corti ? 5123 : 5125, count: tri.length, type: 'SCALAR' },
    ],
    bufferViews: [
      { buffer: 0, byteOffset: 0, byteLength: bufPos.length, byteStride: 8, target: 34962 },
      { buffer: 0, byteOffset: bufPos.length, byteLength: tri.length * (corti ? 2 : 4), target: 34963 },
    ],
    buffers: [{ byteLength: bin.length }],
  };
  let testo = Buffer.from(JSON.stringify(json), 'utf8');
  if (testo.length % 4) testo = Buffer.concat([testo, Buffer.alloc(4 - (testo.length % 4), 0x20)]);
  const intestazione = Buffer.alloc(12);
  intestazione.writeUInt32LE(0x46546c67, 0); // "glTF"
  intestazione.writeUInt32LE(2, 4);
  intestazione.writeUInt32LE(12 + 8 + testo.length + 8 + bin.length, 8);
  const pezzo = (dati, tipo) => {
    const h = Buffer.alloc(8);
    h.writeUInt32LE(dati.length, 0);
    h.writeUInt32LE(tipo, 4);
    return Buffer.concat([h, dati]);
  };
  return Buffer.concat([intestazione, pezzo(testo, 0x4e4f534a), pezzo(bin, 0x004e4942)]);
}

mkdirSync(USCITA, { recursive: true });
copyFileSync(URDF, join(USCITA, 'esapode.urdf'));
let totale = 0;
for (const f of readdirSync(MESH).filter((x) => x.endsWith('.stl')).sort()) {
  const nome = f.replace(/\.stl$/, '');
  const stl = leggiStl(join(MESH, f));
  const m = salda(stl);
  const dati = glb(m, nome);
  writeFileSync(join(USCITA, `${nome}.glb`), dati);
  totale += dati.length;
  console.log(`${nome}: ${stl.length / 9} triangoli, ${m.pos.length / 3} vertici, ${(dati.length / 1024).toFixed(0)} KB`);
}
console.log(`mesh in tutto ${(totale / 1024).toFixed(0)} KB`);
