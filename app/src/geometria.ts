// Geometria delle zampe letta dall'URDF generato (tools/genera_modelli.py): posizione e direzione delle coxe, Lc, Lf,
// Lt e limiti dei giunti. Lunghezze in mm, angoli in gradi, come in robot.yaml e cad.json.
// Il testo si legge con espressioni regolari (non con DOMParser) perche' la stessa funzione serve ai test in Node.

export interface Coxa {
  x: number;
  y: number;
  direzione: number;
}

export interface Geometria {
  zampe: string[];
  coxe: Record<string, Coxa>;
  Lc: number;
  Lf: number;
  Lt: number;
  /** campo di imbardata, alpha e gamma (gradi) dai limiti dei giunti */
  limiti: { imbardata: [number, number]; alpha: [number, number]; gamma: [number, number] };
}

interface Giunto {
  origine: number[];
  rpy: number[];
  limite?: [number, number];
}

const GRADI = 180 / Math.PI;

function giunti(urdf: string): Map<string, Giunto> {
  const out = new Map<string, Giunto>();
  for (const m of urdf.matchAll(/<joint name="([^"]+)" type="[^"]+">([\s\S]*?)<\/joint>/g)) {
    const corpo = m[2];
    const o = corpo.match(/<origin xyz="([^"]+)" rpy="([^"]+)"/);
    if (!o) throw new Error(`giunto ${m[1]} senza origin`);
    const l = corpo.match(/<limit lower="([^"]+)" upper="([^"]+)"/);
    out.set(m[1], {
      origine: o[1].split(/\s+/).map(Number),
      rpy: o[2].split(/\s+/).map(Number),
      limite: l ? [Number(l[1]), Number(l[2])] : undefined,
    });
  }
  return out;
}

export function geometriaDaUrdf(urdf: string): Geometria {
  const g = giunti(urdf);
  const zampe = [...g.keys()].filter((n) => n.startsWith('g_coxa_')).map((n) => n.slice('g_coxa_'.length));
  if (zampe.length !== 6) throw new Error(`URDF con ${zampe.length} zampe invece di 6`);
  const prendi = (nome: string): Giunto => {
    const x = g.get(nome);
    if (!x) throw new Error(`URDF senza il giunto ${nome}`);
    return x;
  };
  const coxe: Record<string, Coxa> = {};
  for (const z of zampe) {
    const c = prendi('g_coxa_' + z);
    coxe[z] = { x: c.origine[0] * 1000, y: c.origine[1] * 1000, direzione: c.rpy[2] * GRADI };
  }
  const z0 = zampe[0];
  const lim = (nome: string): [number, number] => {
    const l = prendi(nome).limite;
    if (!l) throw new Error(`giunto ${nome} senza limiti`);
    return [l[0] * GRADI, l[1] * GRADI];
  };
  const ginocchio = lim('g_ginocchio_' + z0);
  return {
    zampe,
    coxe,
    Lc: prendi('g_femore_' + z0).origine[0] * 1000,
    Lf: prendi('g_ginocchio_' + z0).origine[0] * 1000,
    Lt: -prendi('punta_' + z0).origine[2] * 1000,
    limiti: {
      imbardata: lim('g_coxa_' + z0),
      alpha: lim('g_femore_' + z0),
      gamma: [ginocchio[0] + 90, ginocchio[1] + 90],
    },
  };
}
