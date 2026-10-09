// Gemello digitale cinematico: il robot dall'URDF generato, con le mesh compresse di public/modelli/, riproduce il
// tripode e la rotazione sul posto calcolati in andatura.ts. Le pose sono comandate, non misurate (software.md 6.6).

import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import URDFLoader, { type URDFRobot } from 'urdf-loader';

import { ANDATURA, type Posa, poseTripode, valoriGiunti } from './andatura.ts';
import { type Geometria, geometriaDaUrdf } from './geometria.ts';

const $ = <T extends HTMLElement>(id: string) => document.getElementById(id) as T;

// ------------------------------------------------------------------------------------------------ scena
const contenitore = $('scena');
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
contenitore.appendChild(renderer.domElement);

const scena = new THREE.Scene();
scena.background = new THREE.Color(0x1b1d21);
const camera = new THREE.PerspectiveCamera(40, 1, 0.01, 50);
camera.position.set(0.55, 0.4, 0.65);
const controlli = new OrbitControls(camera, renderer.domElement);
controlli.enableDamping = true;

scena.add(new THREE.HemisphereLight(0xdfe6f0, 0x2a2622, 1.6));
const sole = new THREE.DirectionalLight(0xffffff, 2.2);
sole.position.set(1, 2, 1.5);
scena.add(sole);
// pavimento a quadretti da 10 cm disegnati in una texture: le linee sottili di GridHelper non si vedono con tutti i
// driver (nella prova con Chrome senza schermo mancavano del tutto)
function quadretto(): THREE.CanvasTexture {
  const c = document.createElement('canvas');
  c.width = c.height = 128;
  const g = c.getContext('2d') as CanvasRenderingContext2D;
  g.fillStyle = '#2b2f36';
  g.fillRect(0, 0, 128, 128);
  g.strokeStyle = '#5a606b';
  g.lineWidth = 4;
  g.strokeRect(0, 0, 128, 128);
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.repeat.set(200, 200);
  t.anisotropy = 8;
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
}
const griglia = new THREE.Mesh(new THREE.PlaneGeometry(20, 20), new THREE.MeshStandardMaterial({ map: quadretto() }));
griglia.rotation.x = -Math.PI / 2;
scena.add(griglia);

const telefono = window.matchMedia('(max-width: 560px)');

function adatta() {
  const w = contenitore.clientWidth;
  const h = contenitore.clientHeight;
  renderer.setSize(w, h);
  camera.aspect = w / h;
  // schermo stretto: campo orizzontale di almeno 40 gradi, e il robot sopra il pannello, che occupa il fondo
  camera.fov = camera.aspect < 1 ? Math.min(80, (2 * Math.atan(Math.tan((20 * Math.PI) / 180) / camera.aspect) * 180) / Math.PI) : 40;
  if (telefono.matches) camera.setViewOffset(w, h, 0, 0.2 * h, w, h);
  else camera.clearViewOffset();
  camera.updateProjectionMatrix();
}
window.addEventListener('resize', adatta);
adatta();

// ------------------------------------------------------------------------------------------------ robot
const materiale = new THREE.MeshStandardMaterial({ color: 0x8d929c, roughness: 0.7, metalness: 0.1, flatShading: true });

async function caricaRobot(): Promise<{ robot: URDFRobot; geo: Geometria }> {
  const risposta = await fetch('modelli/esapode.urdf');
  if (!risposta.ok) throw new Error(`modelli/esapode.urdf: ${risposta.status}. Lanciare "npm run modelli".`);
  const testo = await risposta.text();
  const gestore = new THREE.LoadingManager();
  const caricate = new Promise<void>((ok) => {
    gestore.onLoad = () => ok();
  });
  const gltf = new GLTFLoader(gestore);
  const caricatore = new URDFLoader(gestore);
  caricatore.parseCollision = false;
  // l'URDF punta agli STL della repo (../mesh/<segmento>.stl): qui si usano i GLB compressi da scripts/modelli.mjs
  caricatore.loadMeshCb = (percorso, _gestore, _materiale, fatto) => {
    const nome = (percorso.split('/').pop() ?? '').replace(/\.stl$/i, '');
    gltf.load(
      `modelli/${nome}.glb`,
      (g) => {
        g.scene.traverse((o) => {
          if (o instanceof THREE.Mesh) o.material = materiale;
        });
        fatto(g.scene);
      },
      undefined,
      (e) => fatto(new THREE.Object3D(), e instanceof Error ? e : new Error(String(e))),
    );
  };
  const robot = caricatore.parse(testo);
  await caricate;
  return { robot, geo: geometriaDaUrdf(testo) };
}

// ------------------------------------------------------------------------------------------------ comandi
const cursori = {
  h: $<HTMLInputElement>('h'),
  xf0: $<HTMLInputElement>('xf0'),
  giro: $<HTMLInputElement>('giro'),
  periodo: $<HTMLInputElement>('periodo'),
};
const scelta = $<HTMLSelectElement>('andatura');
const stato = $<HTMLParagraphElement>('stato');
const corpoTabella = $<HTMLTableElement>('angoli').querySelector('tbody') as HTMLTableSectionElement;

cursori.h.value = String(ANDATURA.h);
cursori.xf0.value = String(ANDATURA.xf0);
cursori.giro.value = '30';
cursori.periodo.value = '1';
// valori iniziali anche dall'indirizzo, per condividere una vista: ?andatura=rotazione&h=70&xf0=70&giro=20&fase=0.3
const parametri = new URLSearchParams(location.search);
for (const [k, c] of Object.entries(cursori)) {
  const v = parametri.get(k);
  if (v !== null) c.value = v;
}
if (parametri.get('andatura') === 'rotazione') scelta.value = 'rotazione';

function valori() {
  const v = {
    h: Number(cursori.h.value),
    xf0: Number(cursori.xf0.value),
    giro: Number(cursori.giro.value),
    periodo: Number(cursori.periodo.value),
    rotazione: scelta.value === 'rotazione',
  };
  $('v-h').textContent = String(v.h);
  $('v-xf0').textContent = String(v.xf0);
  $('v-giro').textContent = String(v.giro);
  $('v-periodo').textContent = v.periodo.toFixed(1);
  cursori.giro.disabled = !v.rotazione;
  return v;
}

let inPausa = false;
let fase = Math.min(Math.max(Number(parametri.get('fase') ?? 0) || 0, 0), 0.999);
let avanzamento = { x: 0, z: 0, imbardata: 0 };
$('pausa').addEventListener('click', () => {
  inPausa = !inPausa;
  $('pausa').textContent = inPausa ? 'riprendi' : 'pausa';
});
$('inizio').addEventListener('click', () => {
  fase = 0;
  avanzamento = { x: 0, z: 0, imbardata: 0 };
});

function fuoriLimite(geo: Geometria, p: [number, number, number]): boolean[] {
  const l = geo.limiti;
  return [l.imbardata, l.alpha, l.gamma].map(([lo, hi], k) => p[k] < lo || p[k] > hi);
}

function aggiornaTabella(geo: Geometria, pose: Record<string, Posa>) {
  corpoTabella.innerHTML = '';
  for (const z of geo.zampe) {
    const p = pose[z];
    const riga = corpoTabella.insertRow();
    riga.insertCell().textContent = z;
    if (!p) {
      const c = riga.insertCell();
      c.colSpan = 3;
      c.className = 'fuori';
      c.textContent = 'fuori portata';
      continue;
    }
    const fuori = fuoriLimite(geo, p);
    p.forEach((a, k) => {
      const c = riga.insertCell();
      c.textContent = a.toFixed(1);
      if (fuori[k]) c.className = 'fuori';
    });
  }
}

// ------------------------------------------------------------------------------------------------ ciclo
async function avvia() {
  const { robot, geo } = await caricaRobot();
  const base = new THREE.Group(); // Y in alto in three.js, Z in alto nel robot
  robot.rotation.x = -Math.PI / 2;
  base.add(robot);
  scena.add(base);

  const orologio = new THREE.Timer();
  orologio.connect(document);
  let ultimaTabella = 0;
  renderer.setAnimationLoop((ora) => {
    orologio.update(ora);
    const dt = Math.min(orologio.getDelta(), 0.1);
    const v = valori();
    const giro = v.rotazione ? v.giro : 0;
    const pose = poseTripode(geo, v.h, v.xf0, ANDATURA.passo, ANDATURA.alzata, fase, giro);
    const mancanti = geo.zampe.filter((z) => !pose[z]);
    const fuori = geo.zampe.filter((z) => {
      const p = pose[z];
      return p !== null && fuoriLimite(geo, p).some((x) => x);
    });
    if (mancanti.length) {
      stato.className = 'stato errore';
      stato.textContent = `Assetto fuori portata per ${mancanti.join(', ')}: animazione ferma.`;
    } else {
      for (const z of geo.zampe) robot.setJointValues(valoriGiunti(z, pose[z] as [number, number, number]));
      stato.className = fuori.length ? 'stato errore' : 'stato';
      stato.textContent = fuori.length
        ? `Oltre i fine corsa dell'URDF: ${fuori.join(', ')} (il modello si ferma al limite).`
        : `fase ${fase.toFixed(2)} · ${v.rotazione ? `${((2 * giro) / v.periodo).toFixed(0)} °/s` : `${((2 * ANDATURA.passo) / v.periodo).toFixed(0)} mm/s`} comandati`;
      if (!inPausa) {
        fase = (fase + dt / v.periodo) % 1;
        // corpo mosso come se i piedi in appoggio restassero fermi: un passo (o un giro) ogni mezzo ciclo
        avanzamento.imbardata += ((2 * giro) / v.periodo) * dt;
        const d = v.rotazione ? 0 : ((2 * ANDATURA.passo) / v.periodo) * dt;
        const psi = (avanzamento.imbardata * Math.PI) / 180;
        avanzamento.x += d * Math.cos(psi);
        avanzamento.z -= d * Math.sin(psi);
      }
    }
    base.position.set(avanzamento.x / 1000, v.h / 1000, avanzamento.z / 1000);
    base.rotation.y = (avanzamento.imbardata * Math.PI) / 180;
    // la camera segue il robot; la griglia si sposta a celle intere, cosi' i piedi in appoggio restano fermi su di essa
    camera.position.add(base.position.clone().sub(controlli.target));
    controlli.target.copy(base.position);
    griglia.position.set(Math.round(base.position.x * 10) / 10, 0, Math.round(base.position.z * 10) / 10);
    const t = orologio.getElapsed();
    if (t - ultimaTabella > 0.1) {
      aggiornaTabella(geo, pose);
      ultimaTabella = t;
    }
    controlli.update();
    renderer.render(scena, camera);
  });
}

valori();
avvia().catch((e: unknown) => {
  stato.className = 'stato errore';
  stato.textContent = `Errore nel caricare il modello: ${e instanceof Error ? e.message : String(e)}`;
});
