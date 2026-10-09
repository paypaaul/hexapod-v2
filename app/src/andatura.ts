// Tripode e rotazione sul posto: stesse formule di cad/script/assieme.py -> pose_tripode e di sim/andatura.py, con la
// cinematica inversa di calc/statica_tripode.py -> ik_piano (soluzione a ginocchio alto). I test (test/) confrontano
// le pose con cad.json -> cicli_verificati entro 0,01 gradi, come per il generatore Python e il nucleo C++.

import type { Geometria } from './geometria.ts';

/** imbardata, alpha, gamma in gradi; null se il piede e' fuori portata */
export type Posa = [number, number, number] | null;

/** robot.yaml -> tripodi[0]: in appoggio nella prima meta' del ciclo (i test lo confrontano con robot.yaml) */
export const TRIPODE_A = ['AS', 'PS', 'MD'];
/** robot.yaml -> andatura: assetto di progetto, passo e alzata in mm */
export const ANDATURA = { h: 100, xf0: 45, passo: 60, alzata: 30 };

const RAD = Math.PI / 180;

/** (alpha, gamma) in gradi con il piede a xF dall'asse del femore e h sotto; null fuori portata */
export function ikPiano(lf: number, lt: number, xF: number, h: number): [number, number] | null {
  const d = Math.hypot(xF, h);
  if (d > lf + lt || d < Math.abs(lf - lt) || d === 0) return null;
  const c = Math.max(-1, Math.min(1, (lf * lf + d * d - lt * lt) / (2 * lf * d)));
  const alpha = Math.atan2(-h, xF) + Math.acos(c);
  const cg = (lf * lf + lt * lt - d * d) / (2 * lf * lt);
  return [alpha / RAD, Math.acos(Math.max(-1, Math.min(1, cg))) / RAD];
}

export function inAppoggio(zampa: string, fase: number): boolean {
  const u = TRIPODE_A.includes(zampa) ? fase : (fase + 0.5) % 1;
  return u < 0.5;
}

export function poseTripode(
  g: Geometria,
  h: number,
  xf0: number,
  passo: number,
  alzata: number,
  fase: number,
  giro = 0,
): Record<string, Posa> {
  const out: Record<string, Posa> = {};
  for (const n of g.zampe) {
    const { x, y, direzione } = g.coxe[n];
    let fx = x + (g.Lc + xf0) * Math.cos(direzione * RAD);
    let fy = y + (g.Lc + xf0) * Math.sin(direzione * RAD);
    const u = TRIPODE_A.includes(n) ? fase : (fase + 0.5) % 1;
    let k: number;
    let dz: number;
    if (u < 0.5) {
      k = 0.5 - u / 0.5;
      dz = 0;
    } else {
      const v = (u - 0.5) / 0.5;
      k = -0.5 + v;
      dz = alzata * Math.sin(Math.PI * v);
    }
    let dx: number;
    if (giro) {
      const r = giro * k * RAD;
      [fx, fy] = [fx * Math.cos(r) - fy * Math.sin(r), fx * Math.sin(r) + fy * Math.cos(r)];
      dx = 0;
    } else {
      dx = passo * k;
    }
    const px = fx + dx - x;
    const py = fy - y;
    let imb = Math.atan2(py, px) / RAD - direzione;
    imb = ((((imb + 180) % 360) + 360) % 360) - 180;
    const s = ikPiano(g.Lf, g.Lt, Math.hypot(px, py) - g.Lc, h - dz);
    out[n] = s ? [imb, s[0], s[1]] : null;
  }
  return out;
}

/** Valori dei giunti dell'URDF (rad) per una posa: q = imbardata, alpha, gamma - 90 */
export function valoriGiunti(zampa: string, p: [number, number, number]): Record<string, number> {
  return {
    ['g_coxa_' + zampa]: p[0] * RAD,
    ['g_femore_' + zampa]: p[1] * RAD,
    ['g_ginocchio_' + zampa]: (p[2] - 90) * RAD,
  };
}
