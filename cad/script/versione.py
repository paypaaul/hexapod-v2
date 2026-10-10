"""Versione del robot su cui lavorano gli script: il design Fusion di lavoro (storico in docs/versioni.md).

Gli script che modificano o esportano il modello si rifiutano di girare su un altro documento: le versioni precedenti
restano congelate nei loro file Fusion e non si toccano per errore.
"""
VERSIONE = '2.1.2'
# le correzioni piccole (2.1.1, 2.1.2) restano sul design della 2.1.0, senza copia del file
NOME_DESIGN = 'Hexapod v2.1.0'
PROGETTO = 'Hexabot v2'


def controlla(app):
    """Errore se il documento attivo non e' il design di lavoro (Fusion aggiunge al nome il numero di versione)."""
    nome = app.activeDocument.name
    if nome != NOME_DESIGN and not nome.startswith(NOME_DESIGN + ' v'):
        raise RuntimeError('documento attivo "%s": attivare "%s" (versione %s; le altre sono congelate, docs/versioni.md)'
                           % (nome, NOME_DESIGN, VERSIONE))
