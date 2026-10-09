#!/usr/bin/env python3
"""Render: Kabuto corretto (riferimento). Quote in varianti.py (kabuto), costruzione in scena.py. Uso: python3 kabuto.py [viste]"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scena  # noqa: E402
import varianti  # noqa: E402

if __name__ == '__main__':
    scena.main(varianti.kabuto, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kabuto'), 'Kabuto corretto (riferimento)')
