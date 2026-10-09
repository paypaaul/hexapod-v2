"""Emulatore della SSC-32 (clone "SSC32-V2.5") per le prove SIL e per i test del firmware (software.md 2.4 e 6.5).

Comandi ASCII, chiusi da <cr> (13); <esc> (27) annulla la riga in corso; spazi e minuscole ammessi:

    #<ch>P<us>[S<us/s>] ... [T<ms>]   gruppo: i canali partono insieme e arrivano insieme dopo T (o piu' tardi, se uno
                                       con S ci mette di piu'); senza S e T l'impulso salta subito al valore nuovo
    #<ch>P0                           niente impulsi sul canale: il servo si libera
    STOP <ch>   oppure  #<ch>STOP     il canale si ferma dove si trova
    Q                                 risponde "+" se un movimento e' in corso, "." se no
    QP <ch> [QP <ch> ...]             un byte per canale: impulso attuale / 10 (risoluzione 10 us)
    VER                               versione, chiusa da <cr>

Impulsi: un fotogramma ogni 20 ms (fotogramma()); durante un movimento l'impulso avanza in linea retta fotogramma per
fotogramma. Campo 500-2500 us: i valori fuori campo si portano al limite e si registrano in avvisi.

Ipotesi da confrontare con le risposte del clone registrate al banco (S1, passo B1), che diventeranno i dati di prova:
- un canale mai comandato, o liberato con P0, salta al primo valore ignorando S e T (per la SSC-32U e' documentato, V);
- QP tronca alla decina (1503 -> 150);
- la stringa di VER e' quella del costruttore qui sotto.
Il modo binario non c'e' ancora.

Canali traduce tra impulsi e angoli dei giunti con canali, versi, calettamento e us per grado di robot.yaml.
"""
PERIODO_MS = 20                 # V: la scheda rinnova gli impulsi ogni 20 ms
CANALI = 32
US_MIN, US_MAX = 500, 2500      # V: campo dei comandi P


class SSC32:
    def __init__(self, versione='SSC32-EMU'):
        self.versione = versione
        self.impulso = [None] * CANALI        # us attuali; None = nessun impulso
        self.obiettivo = [None] * CANALI
        self.restante_ms = [0.0] * CANALI     # tempo che manca alla fine del movimento
        self.riga = bytearray()
        self.uscita = bytearray()
        self.avvisi = []
        self.errori = []
        self.tempo_ms = 0

    # ---------------------------------------------------------------------------------------------- seriale
    def scrivi(self, dati):
        """Byte in arrivo dalla UART; ogni <cr> esegue la riga."""
        for b in bytes(dati):
            if b == 13:
                self._esegui(self.riga.decode('ascii', 'replace').upper())
                self.riga.clear()
            elif b == 27:
                self.riga.clear()
            else:
                self.riga.append(b)

    def leggi(self):
        """Byte di risposta accumulati (e li toglie)."""
        out = bytes(self.uscita)
        self.uscita.clear()
        return out

    # ---------------------------------------------------------------------------------------------- impulsi
    def fotogramma(self):
        """Avanza di un periodo e restituisce gli impulsi dei 32 canali (us, None se spento)."""
        self.tempo_ms += PERIODO_MS
        for ch in range(CANALI):
            r = self.restante_ms[ch]
            if r <= 0 or self.obiettivo[ch] is None:
                continue
            if r <= PERIODO_MS:
                self.impulso[ch] = self.obiettivo[ch]
                self.restante_ms[ch] = 0.0
            else:
                self.impulso[ch] += (self.obiettivo[ch] - self.impulso[ch]) * PERIODO_MS / r
                self.restante_ms[ch] = r - PERIODO_MS
        return list(self.impulso)

    def in_movimento(self):
        return any(r > 0 for r in self.restante_ms)

    # ---------------------------------------------------------------------------------------------- comandi
    def _esegui(self, s):
        gruppo = []                     # [(canale, us, velocita us/s o None)]
        tempo = None
        i, n = 0, len(s)

        def intero(j):
            k = j
            while k < n and s[k] == ' ':
                k += 1
            inizio = k
            while k < n and s[k].isdigit():
                k += 1
            if k == inizio:
                raise ValueError('numero mancante alla posizione %d' % j)
            return int(s[inizio:k]), k

        try:
            while i < n:
                c = s[i]
                if c in ' \t\n':
                    i += 1
                elif c == '#':
                    ch, i = intero(i + 1)
                    if ch >= CANALI:
                        raise ValueError('canale %d inesistente' % ch)
                    us, vel, ferma = None, None, False
                    while True:
                        while i < n and s[i] == ' ':
                            i += 1
                        if s.startswith('STOP', i):
                            ferma, i = True, i + 4
                        elif i < n and s[i] == 'P':
                            us, i = intero(i + 1)
                        elif i < n and s[i] == 'S':
                            vel, i = intero(i + 1)
                        else:
                            break
                    if ferma:
                        self._ferma(ch)
                    elif us is not None:
                        gruppo.append((ch, us, vel))
                    else:
                        raise ValueError('#%d senza P' % ch)
                elif c == 'T':
                    tempo, i = intero(i + 1)
                elif s.startswith('QP', i):
                    ch, i = intero(i + 2)
                    p = self.impulso[ch] if ch < CANALI else None
                    self.uscita.append(0 if p is None else int(p) // 10)
                elif s.startswith('VER', i):
                    self.uscita += (self.versione + '\r').encode('ascii')
                    i += 3
                elif s.startswith('STOP', i):
                    ch, i = intero(i + 4)
                    self._ferma(ch)
                elif c == 'Q':
                    self.uscita += b'+' if self.in_movimento() else b'.'
                    i += 1
                else:
                    raise ValueError('carattere inatteso %r alla posizione %d' % (c, i))
        except ValueError as e:
            self.errori.append('%s: %s' % (s, e))
            return
        if gruppo:
            self._muovi(gruppo, tempo)

    def _ferma(self, ch):
        self.obiettivo[ch] = self.impulso[ch]
        self.restante_ms[ch] = 0.0

    def _muovi(self, gruppo, tempo_ms):
        durata = float(tempo_ms or 0)
        validi = []
        for ch, us, vel in gruppo:
            if us == 0:
                self.impulso[ch] = self.obiettivo[ch] = None
                self.restante_ms[ch] = 0.0
                continue
            if not US_MIN <= us <= US_MAX:
                limitato = min(max(us, US_MIN), US_MAX)
                self.avvisi.append('canale %d: %d us fuori campo, portato a %d' % (ch, us, limitato))
                us = limitato
            validi.append((ch, us, vel))
            if vel and self.impulso[ch] is not None:
                durata = max(durata, abs(us - self.impulso[ch]) / vel * 1000.0)
        for ch, us, _ in validi:
            if self.impulso[ch] is None or durata <= 0:
                self.impulso[ch] = float(us)
                self.restante_ms[ch] = 0.0
            else:
                self.restante_ms[ch] = durata
            self.obiettivo[ch] = float(us)


GIUNTI = ('coxa', 'femore', 'ginocchio')
ANGOLI = {'coxa': 'imbardata', 'femore': 'alpha', 'ginocchio': 'gamma'}


class Canali:
    """Impulsi <-> angoli dei giunti (imbardata, alpha, gamma in gradi) con robot.yaml -> canali e servo:

        angolo = calettamento + verso * (us - centro_us) / us_per_grado
    """

    def __init__(self, descrizione):
        s = descrizione.yaml['servo']
        self.centro = float(s['centro_us'])
        self.us_grado = float(s['us_per_grado'])
        self.verso = {g: float(s['verso'][g]) for g in GIUNTI}
        self.calettamento = {g: float(s['calettamento'][ANGOLI[g]]) for g in GIUNTI}
        self.zampe = list(descrizione.zampe)
        self.canale = {(z, g): int(descrizione.yaml['canali'][z][g]) for z in self.zampe for g in GIUNTI}
        self.da_canale = {ch: zg for zg, ch in self.canale.items()}
        if len(self.da_canale) != len(self.canale):
            raise ValueError('robot.yaml -> canali: due giunti sullo stesso canale')

    def us(self, giunto, angolo):
        return self.centro + self.verso[giunto] * (angolo - self.calettamento[giunto]) * self.us_grado

    def angolo(self, giunto, us):
        return self.calettamento[giunto] + self.verso[giunto] * (us - self.centro) / self.us_grado

    def gruppo(self, pose, tempo_ms=PERIODO_MS):
        """Comando ASCII di un gruppo con i 18 canali (us interi, canali in ordine) per le pose {zampa: (imb, a, g)}."""
        parti = []
        for ch in sorted(self.da_canale):
            z, g = self.da_canale[ch]
            parti.append('#%dP%d' % (ch, round(self.us(g, pose[z][GIUNTI.index(g)]))))
        coda = 'T%d' % tempo_ms if tempo_ms else ''
        return (''.join(parti) + coda + '\r').encode('ascii')

    def angoli(self, impulsi):
        """{zampa: [imbardata, alpha, gamma]} dagli impulsi dei 32 canali; None dove il canale e' spento."""
        out = {z: [None, None, None] for z in self.zampe}
        for (z, g), ch in self.canale.items():
            p = impulsi[ch]
            out[z][GIUNTI.index(g)] = None if p is None else self.angolo(g, p)
        return out
