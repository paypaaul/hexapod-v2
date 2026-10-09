#!/usr/bin/env python3
"""Render della variante 'base' della tibia (vedi varianti.py e comune.py). Uso: python3 tibia_base.py [robot] [zampa]"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comune  # noqa: E402

if __name__ == '__main__':
    comune.main('base', sys.argv[1:])
