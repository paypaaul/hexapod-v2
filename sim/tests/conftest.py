import importlib.util
import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
for p in (REPO, os.path.join(REPO, 'tools')):
    if p not in sys.path:
        sys.path.insert(0, p)

# Un pytest lanciato dalla radice in un ambiente senza MuJoCo (il job "python" di ci.yml non lo installa) salta i test
# che lo usano invece di fallire all'import; nel job "sim" di sim.yml MuJoCo c'e' e girano tutti.
collect_ignore = [] if importlib.util.find_spec('mujoco') else ['test_modelli.py', 'test_sil.py']


@pytest.fixture(scope='session')
def descrizione():
    from descrizione import Descrizione
    return Descrizione()
