"""Dati della guida: manifest e fori esportati dal CAD, catalogo e passi in YAML (D-075)."""
import fnmatch
import glob
import json
import os

import yaml

from . import geom

RADICE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GUIDA = os.path.join(RADICE, 'guida')


def _yaml(percorso):
    with open(percorso, encoding='utf-8') as f:
        return yaml.safe_load(f)


class Dati:
    def __init__(self, radice=GUIDA):
        self.radice = radice
        with open(os.path.join(radice, 'dati', 'manifest.json'), encoding='utf-8') as f:
            self.manifest = json.load(f)
        with open(os.path.join(radice, 'dati', 'fori.json'), encoding='utf-8') as f:
            self.fori_grezzi = json.load(f)['componenti']
        cat = os.path.join(radice, 'catalogo')
        self.viteria = _yaml(os.path.join(cat, 'viteria.yaml'))
        self.regole_fori = _yaml(os.path.join(cat, 'fori.yaml'))['regole']
        for r in self.regole_fori:                  # diametri dati con il nome di un parametro del CAD
            if isinstance(r.get('d'), str):
                r['d'] = self.manifest['parametri'][r['d']]
        self.giunzioni = _yaml(os.path.join(cat, 'giunzioni.yaml'))
        self.pezzi = _yaml(os.path.join(cat, 'pezzi.yaml')) if os.path.exists(os.path.join(cat, 'pezzi.yaml')) else {}
        self.attrezzi = _yaml(os.path.join(cat, 'attrezzi.yaml')) if os.path.exists(os.path.join(cat, 'attrezzi.yaml')) else {}
        # aggiunte per sezione (catalogo/attrezzi.d/<sezione>.yaml): chi scrive una sezione non tocca il file comune
        for p in sorted(glob.glob(os.path.join(cat, 'attrezzi.d', '*.yaml'))):
            try:
                self.attrezzi.update(_yaml(p) or {})
            except yaml.YAMLError:
                continue
        self.occ = {o['chiave']: o for o in self.manifest['occorrenze']}
        self.basi = list(self.occ)
        # Nelle sezioni nella terna del robot i pezzi della zampa si citano con l'istanza: 'zampa/Coxa@AS'
        for ist in self.manifest['istanze']['zampe']:
            for k in self.basi:
                if self.occ[k]['assieme'] == 'zampa':
                    self.occ['%s@%s' % (k, ist)] = dict(self.occ[k], chiave='%s@%s' % (k, ist), istanza=ist)
        # Piu' estrattori scrivono i loro file in parallelo: un file degli altri a meta' non deve fermare chi lavora.
        # Gli errori di lettura restano in errori_yaml e il controllo li riporta.
        self.sezioni, self.errori_yaml = [], []
        for p in sorted(glob.glob(os.path.join(radice, 'passi', '*.yaml'))):
            try:
                z = _yaml(p)
                z['sezione']['id'], z['passi']
            except (yaml.YAMLError, KeyError, TypeError) as e:
                self.errori_yaml.append('%s: %s' % (os.path.basename(p), str(e).splitlines()[0]))
                continue
            z['_file'] = os.path.basename(p)
            self.sezioni.append(z)

    # -------------------------------------------------------------------------------------- occorrenze e terne
    def chiavi(self, modello):
        """Chiavi del manifest che corrispondono al glob (es. 'corpo/Servo_Coxa_*', 'zampa/*@AS'). Le chiavi con
        l'istanza escono solo se il glob ha la '@'."""
        con = '@' in modello
        return sorted(k for k in self.occ if ('@' in k) == con and fnmatch.fnmatchcase(k, modello))

    def corrisponde(self, chiave, modello):
        """La chiave (con o senza istanza) e' del glob scritto senza istanza, come nel catalogo delle giunzioni."""
        return fnmatch.fnmatchcase(chiave.split('@')[0], modello.split('@')[0])

    @staticmethod
    def base(chiave):
        return chiave.split('@')[0]

    def componente(self, chiave):
        return self.manifest['componenti'][self.occ[chiave]['componente']]

    # ------------------------------------------------------------------------------------------ pose della zampa
    def _asse_servo(self, chiave):
        """(punto, direzione) dell'albero di un servo della zampa: terna del servo con l'origine sull'asse e +Z
        verso la cima dell'albero (cad/CLAUDE.md, modello dell'MG996R)."""
        t = self.occ[chiave]['T']
        return geom.punto(t, [0, 0, 0]), geom.direzione(t, [0, 0, 1])

    def _centro_zampa(self, chiave):
        lo, hi = self.componente(chiave)['bbox']
        return geom.punto(self.occ[chiave]['T'], [(lo[i] + hi[i]) / 2 for i in range(3)])

    def matrici_posa(self, posa):
        """{segmento: trasformata} della zampa in posa, nella sua terna. posa: {alfa, gamma, coxa} in gradi, rispetto
        alla zampa come costruita (alfa 0, gamma 90, coxa 0). alfa positivo alza il ginocchio, gamma oltre 90 porta il
        piede in fuori, coxa positivo gira la zampa in senso antiorario vista dall'alto. Il verso di ogni rotazione si
        ricava dal modello (ginocchio e piedino), cosi' non dipende da come e' orientato l'albero del servo."""
        if not posa:
            return {}
        pf, uf = self._asse_servo('zampa/Servo_femore')
        pg, ug = self._asse_servo('zampa/Servo_ginocchio')
        ginocchio, piede = self._centro_zampa('zampa/Servo_ginocchio'), self._centro_zampa('zampa/Piedino')
        sf = 1 if geom.punto(geom.rotazione(pf, uf, 1), ginocchio)[2] > ginocchio[2] else -1
        sg = 1 if geom.punto(geom.rotazione(pg, ug, 1), piede)[0] > piede[0] else -1
        mf = geom.rotazione(pf, uf, sf * posa.get('alfa', 0))
        mg = geom.rotazione(pg, ug, sg * (posa.get('gamma', 90) - 90))
        mc = geom.rotazione([0, 0, 0], [0, 0, 1], posa.get('coxa', 0))
        return {'coxa': mc, 'femore': geom.componi(mc, mf), 'tibia': geom.componi(mc, geom.componi(mf, mg))}

    def matrice(self, chiave, terna='zampa', istanza='AS'):
        """Trasformata dell'occorrenza nella terna richiesta: 'zampa' (zampa come costruita) o 'robot'. Con una posa
        attiva (self.posa, da matrici_posa) i pezzi della zampa la seguono."""
        o = self.occ[chiave]
        istanza = o.get('istanza', istanza)
        if o['assieme'] == 'attrezzo':              # attrezzi stampati: sempre nella loro terna, da soli
            return o['T']
        if o['assieme'] == 'zampa':
            t = o['T']
            posa = getattr(self, 'posa', None)
            if posa and o.get('segmento') in posa:
                t = geom.componi(posa[o['segmento']], t)
            return t if terna == 'zampa' else geom.componi(self.manifest['istanze']['zampe'][istanza], t)
        if terna == 'zampa':
            raise ValueError('%s sta nel corpo: non ha posto nella terna della zampa' % chiave)
        return geom.componi(self.manifest['istanze']['corpo'], o['T'])
