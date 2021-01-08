# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 07:36:50 2021

@author: blan
"""

# fileIsAscii.py

def scanFileForOnlyAscii(fn):
    badLines = []
    with open(fn, "rt") as f:
        if hasattr(str, 'isascii'):
            badLines = [(linenum, line) for linenum, line in enumerate(f.readlines()) if not line.isascii()]
        else:
            for linenum, line in enumerate(f.readlines()):
                if not all(ord(char) < 128 for char in line):
                    badLines.append((linenum, line))

    return badLines

if __name__ == '__main__':
    import sys
    for fn in sys.argv[1:]:
        nonAsciiLines = scanFileForOnlyAscii(fn)

        print()
        print(fn)
        for lnum, line in nonAsciiLines:
            print(f"{lnum:5} - {line}", end='')
            print(f"{' ':5} - ", end='')
            print(''.join([' ' if c.isascii() else '^' for c in line]))

