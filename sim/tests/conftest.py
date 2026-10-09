import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
for p in (REPO, os.path.join(REPO, 'tools')):
    if p not in sys.path:
        sys.path.insert(0, p)


@pytest.fixture(scope='session')
def descrizione():
    from descrizione import Descrizione
    return Descrizione()
