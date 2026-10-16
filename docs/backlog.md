# Backlog

Lavori decisi o studiati ma non ancora pianificati in una versione. Quando uno entra in una versione si sposta nel suo
piano (`docs/piano-v2.1.0.md` o successivi) e si toglie da qui.

## PCB al posto delle millefori

- **Stato**: studio preliminare fatto il 16 ottobre 2026 (`docs/ricerca/pcb/studio.md`; requisiti, produzione, tre architetture e verifica nella stessa cartella). L'utente vuole disegnarle insieme in una versione dopo la 2.1.7; fino ad allora la guida resta sulle millefori, e poi la millefori resta come alternativa.
- **Proposta dello studio**: due schede.
  - Scheda madre sul vassoio, al posto della basetta, con orecchie e ali: assorbe la striscia dei partitori, il traslatore KAmod e l'ADC (come chip) e regge le prese.
  - Scheda del carapace nell'ingombro della 2.1.7.
  - Due strati, prima serie a mano (circa 14-30 €, 27-36 € con gli SMD montati), 3-6 settimane.
- **Prima di disegnare**:
  - le 4 domande per l'utente (SMD a mano o montati, prese sulle ali e D-069, banco S1 su PCB o millefori, KiCad 10);
  - gli 11 dubbi della verifica, in fondo a `studio.md`;
  - le impronte da confermare: S-02 (interasse dell'ESP32, prova a secco), S-03, S-26, P-012;
  - la base in due varianti, per le colonne delle ali.

## Pettini dei cavi dei servo

- Opzione 1 dell'utente: pezzi separati, a incastro o con una vite, sulla parete del tunnel sopra i Wago.
- Una fessura per cavo, il nome della zampa inciso, le anse del cavo in piu' fra un pettine e l'altro.
- Si disegnano dopo il montaggio di una zampa, con le lunghezze misurate; non vanno nella base.

## Predisposizioni in attesa

- X15, X18, X21, X22, X25-X30, X32, X33: `docs/predisposizioni.md`.
