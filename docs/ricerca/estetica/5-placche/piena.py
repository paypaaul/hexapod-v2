#!/usr/bin/env python3
"""Render: Variante Piena. Quote in varianti.py (piena), costruzione in scena.py. Uso: python3 piena.py [viste]"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scena  # noqa: E402
import varianti  # noqa: E402

if __name__ == '__main__':
    scena.main(varianti.piena, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'piena'), 'Variante Piena')
