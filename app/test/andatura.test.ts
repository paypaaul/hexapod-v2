// Le formule dell'app contro il CAD: geometria dell'URDF uguale a cad.json, pose del tripode uguali a
// cad.json -> cicli_verificati entro 0,01 gradi, costanti uguali a robot.yaml. Si lancia con "npm test" (Node toglie i
// tipi da solo, niente compilazione).

import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';

import { ANDATURA, poseTripode, TRIPODE_A } from '../src/andatura.ts';
import { geometriaDaUrdf } from '../src/geometria.ts';

const REPO = join(dirname(fileURLToPath(import.meta.url)), '..', '..');
const cad = JSON.parse(readFileSync(join(REPO, 'robot', 'cad.json'), 'utf8'));
const yaml = readFileSync(join(REPO, 'robot', 'robot.yaml'), 'utf8');
const geo = geometriaDaUrdf(readFileSync(join(REPO, 'robot', 'generati', 'esapode.urdf'), 'utf8'));

const vicino = (a: number, b: number, tol: number, cosa: string) =>
  assert.ok(Math.abs(a - b) <= tol, `${cosa}: ${a} invece di ${b} (tolleranza ${tol})`);

test("geometria dell'URDF uguale a cad.json", () => {
  vicino(geo.Lc, cad.zampa.Lc, 1e-6, 'Lc');
  vicino(geo.Lf, cad.zampa.Lf, 1e-6, 'Lf');
  vicino(geo.Lt, cad.zampa.Lt, 1e-6, 'Lt');
  assert.deepEqual(geo.zampe.sort(), Object.keys(cad.coxe).sort());
  for (const [z, c] of Object.entries(cad.coxe) as [string, { x: number; y: number; direzione: number }][]) {
    vicino(geo.coxe[z].x, c.x, 1e-6, `${z} x`);
    vicino(geo.coxe[z].y, c.y, 1e-6, `${z} y`);
    vicino(geo.coxe[z].direzione, c.direzione, 1e-6, `${z} direzione`);
  }
  const lim = cad.limiti_meccanici;
  for (const k of ['imbardata', 'alpha', 'gamma'] as const) {
    vicino(geo.limiti[k][0], lim[k][0], 1e-3, `${k} minimo`);
    vicino(geo.limiti[k][1], lim[k][1], 1e-3, `${k} massimo`);
  }
});

test('pose del tripode uguali ai cicli verificati nel CAD', () => {
  let n = 0;
  for (const c of cad.cicli_verificati) {
    for (const p of c.pose) {
      const calc = poseTripode(geo, c.h, c.xf0, c.passo, c.alzata, p.fase, c.giro);
      for (const [z, atteso] of Object.entries(p.zampe) as [string, number[]][]) {
        const v = calc[z];
        assert.ok(v, `${z} fuori portata a ${c.h}/${c.xf0} fase ${p.fase}`);
        for (let k = 0; k < 3; k++) vicino(v[k], atteso[k], 0.01, `${c.h}/${c.xf0} giro ${c.giro} fase ${p.fase} ${z}[${k}]`);
        n++;
      }
    }
  }
  assert.ok(n >= 300, `solo ${n} pose confrontate`);
});

test('costanti uguali a robot.yaml', () => {
  const tripodi = yaml.match(/^tripodi:\s*\[\[([^\]]+)\]/m);
  assert.ok(tripodi, 'robot.yaml senza tripodi');
  assert.deepEqual(tripodi[1].split(',').map((s) => s.trim()), TRIPODE_A);
  const assetto = yaml.match(/^\s+assetto:\s*\{h:\s*([\d.]+),\s*xf0:\s*([\d.]+)\}/m);
  assert.ok(assetto, 'robot.yaml senza andatura.assetto');
  assert.equal(Number(assetto[1]), ANDATURA.h);
  assert.equal(Number(assetto[2]), ANDATURA.xf0);
  for (const k of ['passo', 'alzata'] as const) {
    const m = yaml.match(new RegExp(`^\\s+${k}:\\s*([\\d.]+)`, 'm'));
    assert.ok(m, `robot.yaml senza andatura.${k}`);
    assert.equal(Number(m[1]), ANDATURA[k]);
  }
});
