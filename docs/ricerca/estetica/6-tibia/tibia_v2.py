#!/usr/bin/env python3
"""Render della variante 'v2' della tibia (vedi varianti.py e comune.py). Uso: python3 tibia_v2.py [robot] [zampa]"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comune  # noqa: E402

if __name__ == '__main__':
    comune.main('v2', sys.argv[1:])
