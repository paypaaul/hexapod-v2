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
        self.giunzioni = _yaml(os.path.join(cat, 'giunzioni.yaml'))
        self.pezzi = _yaml(os.path.join(cat, 'pezzi.yaml')) if os.path.exists(os.path.join(cat, 'pezzi.yaml')) else {}
        self.attrezzi = _yaml(os.path.join(cat, 'attrezzi.yaml')) if os.path.exists(os.path.join(cat, 'attrezzi.yaml')) else {}
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

    def matrice(self, chiave, terna='zampa', istanza='AS'):
        """Trasformata dell'occorrenza nella terna richiesta: 'zampa' (zampa come costruita) o 'robot'."""
        o = self.occ[chiave]
        istanza = o.get('istanza', istanza)
        if o['assieme'] == 'zampa':
            return o['T'] if terna == 'zampa' else geom.componi(self.manifest['istanze']['zampe'][istanza], o['T'])
        if terna == 'zampa':
            raise ValueError('%s sta nel corpo: non ha posto nella terna della zampa' % chiave)
        return geom.componi(self.manifest['istanze']['corpo'], o['T'])
