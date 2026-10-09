"""Test in Python della descrizione del robot, della statica di calc/ e dei vettori del nucleo C++.

    python3 -m pytest tests
"""
import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'tools'))

from descrizione import Descrizione  # noqa: E402


@pytest.fixture(scope='session')
def d():
    return Descrizione()
