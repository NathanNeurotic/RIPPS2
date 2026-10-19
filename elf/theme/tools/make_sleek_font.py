"""Builds RIPPS2 Sleek (elf/theme/fonts/ripps2_sleek.ttf) and RIPPS2 Sleek Bold
(ripps2_sleek_bold.ttf), the UI fonts for hints, glyph labels, menus and settings.

The letters take the PS2 logo's lettering as their model: one thin, even stroke, square corners,
letters built from horizontal and vertical bars on a grid, and the logo's own open forms -- the P
with no stem above its bowl, the zigzag 2 carried into the S. They are narrower than
the main font (Planet N Compact, assets/master.ttf), so a full hint bar fits the screen. The digits
are drawn the same way (the 2 is the logo's; the 5 takes clipped corners to stay apart from the S,
the 0 is narrower than the O and slashed). The S is the square form: the logo's stepped S (kept as
--s-variant logo) reads as a stray stroke inside words. Bold is the same drawing with a heavier
stroke, for labels that need the weight (the glyph pills and badges, text beside big glyphs).
Metrics match the main font, so the two sit on one baseline.

Each glyph is a set of polylines on a grid 6 units tall (the cap height); every segment becomes a
stroke rectangle, extended half a stroke past its ends so the corners close square.

    python elf/theme/tools/make_sleek_font.py [--weight regular|bold|both] [--s-variant logo|square]
"""
import argparse
import math
import os
import unicodedata

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
OUT = os.path.normpath(os.path.join(HERE, '..', 'fonts', 'ripps2_sleek.ttf'))

UPM = 1000
CAP = 680            # the main font's cap height
ASC, DESC = 894, -182
U = CAP / 6.0        # one grid unit
STROKE = 0.7 * U     # a thin, even line, as in the logo
STROKE_BOLD = 1.25 * U
SB = 60              # side bearing each side

# polylines per glyph, x in grid units from 0 to the glyph's width, y from 0 (baseline) to 6 (cap)
GLYPHS = {
    'A': [[(0, 0), (0, 6), (4, 6), (4, 0)], [(0, 3), (4, 3)]],
    'B': [[(0, 0), (0, 6), (3.2, 6), (3.2, 3), (0, 3)], [(3.2, 3), (4, 3), (4, 0), (0, 0)]],
    'C': [[(4, 6), (0, 6), (0, 0), (4, 0)]],
    'D': [[(0, 0), (0, 6), (3, 6), (4, 5), (4, 1), (3, 0), (0, 0)]],
    'E': [[(4, 6), (0, 6), (0, 0), (4, 0)], [(0, 3), (3.2, 3)]],
    'F': [[(4, 6), (0, 6), (0, 0)], [(0, 3), (3.2, 3)]],
    'G': [[(4, 6), (0, 6), (0, 0), (4, 0), (4, 3), (2.2, 3)]],
    'H': [[(0, 0), (0, 6)], [(4, 0), (4, 6)], [(0, 3), (4, 3)]],
    'I': [[(0, 0), (0, 6)]],
    'J': [[(4, 6), (4, 0), (0, 0), (0, 1.8)]],
    'K': [[(0, 0), (0, 6)], [(0, 3), (1.2, 3)], [(4, 6), (1.2, 3), (4, 0)]],
    'L': [[(0, 6), (0, 0), (3.6, 0)]],
    'M': [[(0, 0), (0, 6), (5, 6), (5, 0)], [(2.5, 6), (2.5, 2.2)]],
    'N': [[(0, 0), (0, 6), (4, 0), (4, 6)]],
    'O': [[(0, 0), (0, 6), (4, 6), (4, 0), (0, 0)]],
    'P': [[(0, 6), (4, 6), (4, 3), (0, 3)], [(0, 3), (0, 0)]],                  # the logo's P
    'Q': [[(0, 0), (0, 6), (4, 6), (4, 0), (0, 0)], [(2.8, 1.2), (4.6, -0.6)]],
    'R': [[(0, 6), (4, 6), (4, 3), (0, 3)], [(0, 3), (0, 0)], [(1.8, 3), (4, 0)]],
    'S_logo': [[(4, 6), (2, 6), (2, 0), (0, 0)]],                               # the logo's stepped S
    'S_square': [[(4, 6), (0, 6), (0, 3), (4, 3), (4, 0), (0, 0)]],             # the logo's 2, mirrored
    'T': [[(0, 6), (4, 6)], [(2, 6), (2, 0)]],
    'U': [[(0, 6), (0, 0), (4, 0), (4, 6)]],
    'V': [[(0, 6), (2, 0), (4, 6)]],
    'W': [[(0, 6), (0, 0), (5, 0), (5, 6)], [(2.5, 0), (2.5, 3.8)]],
    'X': [[(0, 6), (4, 0)], [(0, 0), (4, 6)]],
    'Y': [[(0, 6), (2, 3), (4, 6)], [(2, 3), (2, 0)]],
    'Z': [[(0, 6), (4, 6), (0, 0), (4, 0)]],
    ':': [[(0, 0), (0, 0.01)], [(0, 3.6), (0, 3.61)]],
    '.': [[(0, 0), (0, 0.01)]],
    ',': [[(0, 0.2), (0, -1.0)]],
    ';': [[(0, 3.6), (0, 3.61)], [(0, 0.2), (0, -1.0)]],
    "'": [[(0, 6), (0, 4.4)]],
    '"': [[(0, 6), (0, 4.4)], [(1.2, 6), (1.2, 4.4)]],
    '-': [[(0, 3), (2.6, 3)]],
    '_': [[(0, -0.8), (4, -0.8)]],
    '+': [[(0, 3), (3.2, 3)], [(1.6, 1.4), (1.6, 4.6)]],
    '=': [[(0, 2), (3.2, 2)], [(0, 4), (3.2, 4)]],
    '/': [[(0, 0), (3, 6)]],
    '\\': [[(0, 6), (3, 0)]],
    '(': [[(1.4, 6.6), (0, 6.6), (0, -0.6), (1.4, -0.6)]],
    ')': [[(0, 6.6), (1.4, 6.6), (1.4, -0.6), (0, -0.6)]],
    '[': [[(1.4, 6.6), (0, 6.6), (0, -0.6), (1.4, -0.6)]],
    ']': [[(0, 6.6), (1.4, 6.6), (1.4, -0.6), (0, -0.6)]],
    '<': [[(3, 5.4), (0, 3), (3, 0.6)]],
    '>': [[(0, 5.4), (3, 3), (0, 0.6)]],
    '!': [[(0, 6), (0, 1.8)], [(0, 0), (0, 0.01)]],
    '?': [[(0, 6), (4, 6), (4, 3), (2, 3), (2, 1.8)], [(2, 0), (2, 0.01)]],
    '&': [[(4, 0), (0, 0), (0, 3), (3, 3)], [(1, 3), (1, 6), (3.2, 6), (3.2, 4.4)], [(3, 3), (4, 3)]],
    '%': [[(0, 0), (4, 6)], [(0, 6), (0.8, 6), (0.8, 5.2), (0, 5.2), (0, 6)], [(3.2, 0.8), (4, 0.8), (4, 0), (3.2, 0), (3.2, 0.8)]],
    '#': [[(1.2, 0), (1.2, 6)], [(2.8, 0), (2.8, 6)], [(0, 2), (4, 2)], [(0, 4), (4, 4)]],
    '*': [[(0, 4.5), (2.4, 4.5)], [(1.2, 3.3), (1.2, 5.7)]],
    '@': [[(3, 2), (1.4, 2), (1.4, 4), (3, 4), (3, 1.2), (4, 1.2), (4, 6), (0, 6), (0, 0), (4, 0)]],
    '|': [[(0, -0.6), (0, 6.6)]],
    '~': [[(0, 3), (1, 3.8), (2, 3), (3, 3.8)]],
}
DIGITS = {
    '0': [[(0, 0), (0, 6), (3.4, 6), (3.4, 0), (0, 0)], [(1.1, 2.2), (2.3, 3.8)]],
    '1': [[(0, 3.9), (1.6, 6), (1.6, 0)]],                                      # a long flag: never an I
    '2': [[(0, 6), (4, 6), (4, 3), (0, 3), (0, 0), (4, 0)]],                    # the logo's 2
    '3': [[(0, 6), (4, 6), (1.8, 3.4), (4, 3.4), (4, 0), (0, 0)]],               # flat-topped: never a backwards E
    '4': [[(0, 6), (0, 2.4), (4, 2.4)], [(3, 6), (3, 0)]],
    '5': [[(4, 6), (0, 6), (0, 3.2), (3, 3.2), (4, 2.2), (4, 1), (3, 0), (0, 0)]],
    '6': [[(4, 6), (0, 6), (0, 0), (4, 0), (4, 3), (0, 3)]],
    '7': [[(0, 6), (4, 6), (4, 0)]],
    '8': [[(0, 0), (0, 6), (4, 6), (4, 0), (0, 0)], [(0, 3), (4, 3)]],
    '9': [[(4, 3), (0, 3), (0, 6), (4, 6), (4, 0), (0, 0)]],
}


# A true lowercase, for the case-true cut (ripps2_sleek_case.ttf: the on-screen keyboard and typed text,
# where a and A must differ). x-height 4, ascenders at the cap height, descenders to -1.6 (inside the
# font's descent). The l keeps a foot, so I, l and 1 are three different shapes.
LOWER = {
    'a': [[(0, 4), (3, 4), (3, 0), (0, 0), (0, 2), (3, 2)]],
    'b': [[(0, 6), (0, 0), (3, 0), (3, 4), (0, 4)]],
    'c': [[(3, 4), (0, 4), (0, 0), (3, 0)]],
    'd': [[(3, 6), (3, 0), (0, 0), (0, 4), (3, 4)]],
    'e': [[(0, 2), (3, 2), (3, 4), (0, 4), (0, 0), (3, 0)]],
    'f': [[(2.6, 6), (1, 6), (1, 0)], [(0, 4), (2.4, 4)]],
    'g': [[(3, 0), (0, 0), (0, 4), (3, 4), (3, -1.6), (0, -1.6)]],
    'h': [[(0, 6), (0, 0)], [(0, 4), (3, 4), (3, 0)]],
    'i': [[(0, 0), (0, 4)], [(0, 5.4), (0, 5.41)]],
    'j': [[(1.2, 4), (1.2, -1.6), (0, -1.6)], [(1.2, 5.4), (1.2, 5.41)]],
    'k': [[(0, 6), (0, 0)], [(0, 1.8), (0.9, 1.8)], [(3, 4), (0.9, 1.8), (3, 0)]],
    'l': [[(0, 6), (0, 0), (1.2, 0)]],
    'm': [[(0, 0), (0, 4), (4.4, 4), (4.4, 0)], [(2.2, 4), (2.2, 0)]],
    'n': [[(0, 0), (0, 4), (3, 4), (3, 0)]],
    'o': [[(0, 0), (0, 4), (3, 4), (3, 0), (0, 0)]],
    'p': [[(0, -1.6), (0, 4), (3, 4), (3, 0), (0, 0)]],
    'q': [[(3, -1.6), (3, 4), (0, 4), (0, 0), (3, 0)]],
    'r': [[(0, 0), (0, 4), (2.6, 4), (2.6, 3.2)]],
    's': [[(3, 4), (0, 4), (0, 2), (3, 2), (3, 0), (0, 0)]],
    't': [[(1, 6), (1, 0), (2.6, 0)], [(0, 4), (2.6, 4)]],
    'u': [[(0, 4), (0, 0), (3, 0), (3, 4)]],
    'v': [[(0, 4), (1.5, 0), (3, 4)]],
    'w': [[(0, 4), (0, 0), (4.4, 0), (4.4, 4)], [(2.2, 0), (2.2, 2.6)]],
    'x': [[(0, 4), (3, 0)], [(0, 0), (3, 4)]],
    'y': [[(0, 4), (0, 0.8), (3, 0.8)], [(3, 4), (3, -1.6), (0, -1.6)]],
    'z': [[(0, 4), (3, 4), (0, 0), (3, 0)]],
}


# Build 104 (languages): the rest of what RIPPS2's translations write, drawn the same way. Capitals only; the caps
# cut maps each lowercase letter to its capital, the case-true cut draws a lowercase that has no shape in LOWER as
# its capital at x-height (small caps).
CYRILLIC = {
    '\u0411': [[(4, 5.2), (4, 6), (0, 6), (0, 0), (4, 0), (4, 3.2), (0, 3.2)]],              # BE: a flag tells it from 6
    '\u0413': [[(3.6, 6), (0, 6), (0, 0)]],                                                  # GHE
    '\u0414': [[(-0.4, -1), (-0.4, 0), (4.6, 0), (4.6, -1)], [(0.6, 0), (0.6, 6), (4, 6), (4, 0)]],  # DE
    '\u0416': [[(0, 6), (2.5, 3), (0, 0)], [(5, 6), (2.5, 3), (5, 0)], [(2.5, 6), (2.5, 0)]],  # ZHE
    '\u0417': [[(0, 6), (4, 6), (1.8, 3.4), (4, 3.4), (4, 0), (0, 0)]],                      # ZE: the 3
    '\u0418': [[(0, 6), (0, 0), (4, 6), (4, 0)]],                                            # I
    '\u041B': [[(0, 0), (1, 0), (1, 6), (4, 6), (4, 0)]],                                    # EL
    '\u041F': [[(0, 0), (0, 6), (4, 6), (4, 0)]],                                            # PE
    '\u0423': [[(0, 6), (0, 3), (4, 3)], [(4, 6), (4, 0), (0, 0)]],                          # U
    '\u0424': [[(0, 4.8), (0, 1.2), (5, 1.2), (5, 4.8), (0, 4.8)], [(2.5, 6), (2.5, 0)]],    # EF
    '\u0426': [[(0, 6), (0, 0), (4, 0), (4, 6)], [(4, 0), (4.8, 0), (4.8, -1)]],             # TSE
    '\u0427': [[(0, 6), (0, 3), (4, 3)], [(4, 6), (4, 0)]],                                  # CHE
    '\u0428': [[(0, 6), (0, 0), (5, 0), (5, 6)], [(2.5, 0), (2.5, 6)]],                      # SHA
    '\u0429': [[(0, 6), (0, 0), (5, 0), (5, 6)], [(2.5, 0), (2.5, 6)], [(5, 0), (5.8, 0), (5.8, -1)]],  # SHCHA
    '\u042A': [[(0, 6), (1, 6), (1, 0), (4, 0), (4, 3), (1, 3)]],                            # HARD SIGN
    '\u042B': [[(0, 6), (0, 0), (3, 0), (3, 3), (0, 3)], [(5, 6), (5, 0)]],                  # YERU
    '\u042C': [[(0, 6), (0, 0), (4, 0), (4, 3), (0, 3)]],                                    # SOFT SIGN
    '\u042D': [[(0, 6), (4, 6), (4, 0), (0, 0)], [(1.6, 3), (4, 3)]],                        # E
    '\u042E': [[(0, 6), (0, 0)], [(0, 3), (1.6, 3)], [(1.6, 0), (1.6, 6), (5, 6), (5, 0), (1.6, 0)]],  # YU
    '\u042F': [[(4, 0), (4, 6), (0, 6), (0, 3), (4, 3)], [(2.2, 3), (0, 0)]],                # YA: the R turned round
    '\u0404': [[(4, 6), (0, 6), (0, 0), (4, 0)], [(0, 3), (2.4, 3)]],                        # UKRAINIAN IE
    '\u0490': [[(0, 0), (0, 6), (3.6, 6), (3.6, 7.2)]],                                      # GHE WITH UPTURN
    '\u0402': [[(0, 6), (4, 6)], [(1.2, 6), (1.2, 0)], [(1.2, 3.4), (4, 3.4), (4, 0), (3, 0)]],  # DJE
    '\u040B': [[(0, 6), (4, 6)], [(1.2, 6), (1.2, 0)], [(1.2, 3.4), (4, 3.4), (4, 0)]],      # TSHE
    '\u0409': [[(0, 0), (1, 0), (1, 6), (3.4, 6), (3.4, 0), (6, 0), (6, 3), (3.4, 3)]],      # LJE
    '\u040A': [[(0, 0), (0, 6)], [(0, 3), (3.4, 3)], [(3.4, 6), (3.4, 0), (6, 0), (6, 3), (3.4, 3)]],  # NJE
    '\u040F': [[(0, 6), (0, 0), (4, 0), (4, 6)], [(2, 0), (2, -1)]],                         # DZHE
}
# Cyrillic letters drawn as the Latin letter they look like
CYRILLIC_AS = {'\u0410': 'A', '\u0412': 'B', '\u0415': 'E', '\u041A': 'K', '\u041C': 'M', '\u041D': 'H',
               '\u041E': 'O', '\u0420': 'P', '\u0421': 'C', '\u0422': 'T', '\u0425': 'X', '\u0406': 'I',
               '\u0408': 'J', '\u0405': 'S'}
GREEK = {
    '\u0393': [[(3.6, 6), (0, 6), (0, 0)]],                                                  # GAMMA
    '\u0394': [[(0, 0), (2, 6), (4, 0), (0, 0)]],                                            # DELTA
    '\u0398': [[(0, 0), (0, 6), (4, 6), (4, 0), (0, 0)], [(1.2, 3), (2.8, 3)]],              # THETA
    '\u039B': [[(0, 0), (2, 6), (4, 0)]],                                                    # LAMDA
    '\u039E': [[(0, 6), (4, 6)], [(0.6, 3), (3.4, 3)], [(0, 0), (4, 0)]],                    # XI
    '\u03A0': [[(0, 0), (0, 6), (4, 6), (4, 0)]],                                            # PI
    '\u03A3': [[(4, 6), (0, 6), (2, 3), (0, 0), (4, 0)]],                                    # SIGMA
    '\u03A6': [[(0, 4.8), (0, 1.2), (5, 1.2), (5, 4.8), (0, 4.8)], [(2.5, 6), (2.5, 0)]],    # PHI
    '\u03A8': [[(0, 6), (0, 3), (4, 3), (4, 6)], [(2, 6), (2, 0)]],                          # PSI
    '\u03A9': [[(0, 0), (1.2, 0), (0, 1.4), (0, 6), (4, 6), (4, 1.4), (2.8, 0), (4, 0)]],    # OMEGA
}
GREEK_AS = {'\u0391': 'A', '\u0392': 'B', '\u0395': 'E', '\u0396': 'Z', '\u0397': 'H', '\u0399': 'I',
            '\u039A': 'K', '\u039C': 'M', '\u039D': 'N', '\u039F': 'O', '\u03A1': 'P', '\u03A4': 'T',
            '\u03A5': 'Y', '\u03A7': 'X'}
# Latin letters with no decomposition: the ligatures and the barred and stroked ones
LATIN_EXTRA = {
    '\u00C6': [[(0, 0), (0, 6), (5, 6)], [(2.6, 6), (2.6, 0), (5, 0)], [(0, 3), (4.4, 3)]],   # AE
    '\u0152': [[(5, 6), (0, 6), (0, 0), (5, 0)], [(2.6, 6), (2.6, 0)], [(2.6, 3), (4.4, 3)]],  # OE
    '\u00D8': [[(0, 0), (0, 6), (4, 6), (4, 0), (0, 0)], [(0, 0), (4, 6)]],                  # O WITH STROKE
    '\u0141': [[(0.8, 6), (0.8, 0), (4.4, 0)], [(0, 2.4), (1.8, 3.6)]],                      # L WITH STROKE
    '\u0110': [[(0.8, 0), (0.8, 6), (3.8, 6), (4.8, 5), (4.8, 1), (3.8, 0), (0.8, 0)], [(0, 3), (1.8, 3)]],  # D WITH STROKE
    '\u0126': [[(0, 0), (0, 6)], [(4, 0), (4, 6)], [(0, 3), (4, 3)], [(-0.6, 4.8), (4.6, 4.8)]],  # H WITH STROKE
    '\u0166': [[(0, 6), (4, 6)], [(2, 6), (2, 0)], [(1, 3), (3, 3)]],                        # T WITH STROKE
    '\u1E9E': [[(0, 0), (0, 6), (4, 6), (1.6, 3.4), (4, 3.4), (4, 0), (1.6, 0)]],            # CAPITAL SHARP S
    '\u00DE': [[(0, 0), (0, 6)], [(0, 4.6), (4, 4.6), (4, 1.6), (0, 1.6)]],                  # THORN
    '\u014A': [[(0, 0), (0, 6), (4, 6), (4, -1), (2.6, -1)]],                                # ENG
}
LATIN_EXTRA_AS = {'\u00D0': '\u0110', '\u0131': 'I'}  # ETH is drawn as D with stroke; dotless i is I
# the case-true cut: lowercase Cyrillic and Greek letters that look like a Latin lowercase are drawn as it
CASE_LOWER_AS = {'\u0430': 'a', '\u0435': 'e', '\u043E': 'o', '\u0440': 'p', '\u0441': 'c', '\u0445': 'x',
                 '\u0443': 'y', '\u0456': 'i', '\u0458': 'j', '\u0455': 's', '\u03BF': 'o'}
# the case-true cut: a lowercase whose small capital loses what tells it apart. Be shrunk to x-height kept its flag
# too small to see and read as ve ("Vyvrat" for Vybrat, lab 10/19), so it gets its ascender: a b with a top bar.
CASE_LOWER = {'\u0431': [[(2.8, 6), (0, 6), (0, 0), (3, 0), (3, 4), (0, 4)]]}
PUNCT_EXTRA = {
    '\u00A1': [[(0, 4.2), (0, 0)], [(0, 6), (0, 6.01)]],                                     # inverted !
    '\u00BF': [[(2, 6), (2, 6.01)], [(2, 4.2), (2, 3), (0, 3), (0, 0), (4, 0)]],             # inverted ?
    '\u00B7': [[(0, 3), (0, 3.01)]],                                                         # middle dot
    '\u2026': [[(0, 0), (0, 0.01)], [(1.2, 0), (1.2, 0.01)], [(2.4, 0), (2.4, 0.01)]],       # ellipsis
    '\u2013': [[(0, 3), (3.6, 3)]],                                                          # en dash
    '\u2014': [[(0, 3), (5.4, 3)]],                                                          # em dash (upstream texts)
    '\u2018': [[(0, 4.4), (0, 6)]],                                                          # quotes: straight, as '
    '\u2019': [[(0, 6), (0, 4.4)]],
    '\u201C': [[(0, 6), (0, 4.4)], [(1.2, 6), (1.2, 4.4)]],
    '\u201D': [[(0, 6), (0, 4.4)], [(1.2, 6), (1.2, 4.4)]],
    '\u00AB': [[(1.6, 4.6), (0, 3), (1.6, 1.4)], [(3.2, 4.6), (1.6, 3), (3.2, 1.4)]],        # guillemets
    '\u00BB': [[(0, 4.6), (1.6, 3), (0, 1.4)], [(1.6, 4.6), (3.2, 3), (1.6, 1.4)]],
    '\u00B0': [[(0, 6), (1.2, 6), (1.2, 4.8), (0, 4.8), (0, 6)]],                             # degree
    '\u00D7': [[(0, 1.6), (2.8, 4.4)], [(0, 4.4), (2.8, 1.6)]],                              # multiplication sign
    '\u2192': [[(0, 3), (4, 3)], [(2.6, 4.4), (4, 3), (2.6, 1.6)]],                          # arrow
}
ZERO_WIDTH = (0x200B, 0x200C, 0x200D, 0x200E, 0x200F, 0xFEFF)

# Marks, drawn above a letter (x from its centre, y up from the mark's line) or below it (y down from the baseline;
# 'ogonek' from its right side). Heights fit 0.7 of a unit; a bold cut draws them a little lower.
MARKS_ABOVE = {
    0x0300: [[(-0.4, 0.7), (0.4, 0)]],                                    # grave
    0x0301: [[(-0.4, 0), (0.4, 0.7)]],                                    # acute (and the Greek tonos)
    0x0302: [[(-0.8, 0), (0, 0.7), (0.8, 0)]],                            # circumflex
    0x0303: [[(-1, 0.1), (-0.35, 0.6), (0.35, 0.1), (1, 0.6)]],           # tilde
    0x0304: [[(-0.9, 0.35), (0.9, 0.35)]],                                # macron
    0x0306: [[(-0.8, 0.7), (-0.8, 0), (0.8, 0), (0.8, 0.7)]],             # breve, square as the letters
    0x0307: [[(0, 0.3), (0, 0.31)]],                                      # dot above
    0x0308: [[(-0.7, 0.3), (-0.7, 0.31)], [(0.7, 0.3), (0.7, 0.31)]],    # diaeresis
    0x0309: [[(-0.4, 0.7), (0.4, 0.7), (0.4, 0.35), (0, 0.35), (0, 0)]],  # hook above
    0x030A: [[(-0.45, 0), (-0.45, 0.8), (0.45, 0.8), (0.45, 0), (-0.45, 0)]],  # ring
    0x030B: [[(-0.9, 0), (-0.3, 0.7)], [(0.3, 0), (0.9, 0.7)]],           # double acute
    0x030C: [[(-0.8, 0.7), (0, 0), (0.8, 0.7)]],                          # caron
}
MARKS_BELOW = {
    0x0323: [[(0, -0.9), (0, -0.89)]],                                    # dot below
    0x0326: [[(0, -0.5), (0, -1.4)]],                                     # comma below
    0x0327: [[(0, 0), (0, -0.6), (0.6, -0.6), (0.6, -1.2), (-0.4, -1.2)]],  # cedilla
}
OGONEK = [[(-0.1, 0), (-0.6, -0.5), (-0.6, -1.2), (0.2, -1.2)]]


def _span(polys):
    xs = [x for p in polys for x, _ in p]
    ys = [y for p in polys for _, y in p]
    return min(xs), max(xs), min(ys), max(ys)


def compose(base, marks, stroke):
    """base's polylines with the marks of a decomposed letter (NFD) put on, or None for a mark not drawn here."""
    x0, x1, _, top = _span(base)
    cx, su = (x0 + x1) / 2.0, stroke / U
    h = 0.7 if su < 1 else 0.55
    out = [list(p) for p in base]
    level = top + su + 0.35
    for m in marks:
        cp = ord(m)
        if cp in MARKS_ABOVE:
            out += [[(cx + x, level + y * h / 0.7) for x, y in p] for p in MARKS_ABOVE[cp]]
            level += h + su + 0.2
        elif cp in MARKS_BELOW:
            out += [[(cx + x, y) for x, y in p] for p in MARKS_BELOW[cp]]
        elif cp == 0x0328:
            out += [[(x1 + x, y) for x, y in p] for p in OGONEK]
        elif cp == 0x031B:  # horn: up and out from the top right
            out += [[(x1, top - 0.4), (x1 + 0.8, top - 0.4), (x1 + 0.8, top + 0.5)]]
        else:
            return None
    return out


def small_caps(polys):
    return [[(x, y * 4.0 / 6.0) for x, y in p] for p in polys]


def stroke_rect(p, q, half):
    """The four corners of a stroke from p to q, extended half a stroke past each end."""
    (x0, y0), (x1, y1) = p, q
    dx, dy = x1 - x0, y1 - y0
    length = math.hypot(dx, dy)
    if length < 1e-6:
        dx, dy, length = 1.0, 0.0, 1.0
    ux, uy = dx / length, dy / length
    nx, ny = -uy, ux
    ax, ay = x0 - ux * half, y0 - uy * half
    bx, by = x1 + ux * half, y1 + uy * half
    pts = [(ax + nx * half, ay + ny * half), (bx + nx * half, by + ny * half),
           (bx - nx * half, by - ny * half), (ax - nx * half, ay - ny * half)]
    # TrueType outer contours run clockwise (negative signed area with y up)
    area = sum(pts[i][0] * pts[(i + 1) % 4][1] - pts[(i + 1) % 4][0] * pts[i][1] for i in range(4))
    return pts if area < 0 else pts[::-1]


def draw_polylines(polys, stroke):
    """One clean outline per glyph. Each polyline is stroked as a whole (mitred corners, flat ends); a
    free end gets a square cap, an end that runs into another stroke stays flat inside it (no nub, as
    the R's leg once poked through its bowl); everything is unioned into one outline, so joins carry no
    overlapping edges to smear when antialiased small; and the glyph is cut to its own box, the
    stroke's half width past its grid extremes, so a diagonal's end or a sharp corner never spills
    past the baseline, the cap line or the glyph's sides."""
    from shapely.geometry import LinearRing, LineString, Point, Polygon, box
    from shapely.geometry.polygon import orient
    from shapely.ops import unary_union

    pen = TTGlyphPen(None)
    xs = [x for poly in polys for x, _ in poly]
    ys = [y for poly in polys for _, y in poly]
    width_units = max(xs) - min(xs) if xs else 0
    half = stroke / 2
    ox = SB + half - min(xs) * U
    lines = [[(ox + x * U, y * U) for x, y in poly] for poly in polys]

    def body(pts):
        if len(pts) > 3 and pts[0] == pts[-1]:
            return Polygon(LinearRing(pts[:-1]).buffer(half, join_style='mitre', mitre_limit=5.0))
        return LineString(pts).buffer(half, cap_style='flat', join_style='mitre', mitre_limit=5.0)

    def cap(end, before):
        (ex, ey), (bx, by) = end, before
        dx, dy = ex - bx, ey - by
        n = math.hypot(dx, dy) or 1.0
        ux, uy = dx / n, dy / n
        return LineString([(ex - ux * 0.01, ey - uy * 0.01), (ex + ux * half, ey + uy * half)]).buffer(half, cap_style='flat')

    bodies = [body(pts) for pts in lines]
    shapes = list(bodies)
    for i, pts in enumerate(lines):
        if len(pts) > 3 and pts[0] == pts[-1]:
            continue  # a closed ring has no ends
        others = unary_union([b for j, b in enumerate(bodies) if j != i]) if len(bodies) > 1 else None
        for end, before in ((pts[0], pts[1]), (pts[-1], pts[-2])):
            joined = others is not None and others.buffer(-0.5).contains(Point(end))
            if not joined:
                shapes.append(cap(end, before))
    shape = unary_union(shapes).intersection(
        box(ox + min(xs) * U - half, min(ys) * U - half, ox + max(xs) * U + half, max(ys) * U + half))
    shape = shape.simplify(0.5)
    for poly in getattr(shape, 'geoms', [shape]):
        if poly.is_empty or poly.geom_type != 'Polygon':
            continue
        poly = orient(poly, sign=-1.0)  # TrueType: outer contours clockwise, holes anticlockwise
        for ring in [poly.exterior] + list(poly.interiors):
            pts = [(round(x), round(y)) for x, y in ring.coords[:-1]]
            pts = [p for k, p in enumerate(pts) if p != pts[k - 1]]
            if len(pts) < 3:
                continue
            pen.moveTo(pts[0])
            for p in pts[1:]:
                pen.lineTo(p)
            pen.closePath()
    advance = round(width_units * U + stroke + 2 * SB)
    return pen.glyph(), advance


def build(s_variant, bold=False, case=False):
    stroke = STROKE_BOLD if bold else STROKE
    order = ['.notdef', 'space']
    glyf, hmtx, cmap = {}, {}, {}

    empty = TTGlyphPen(None).glyph()
    glyf['.notdef'], hmtx['.notdef'] = empty, (400, 0)
    glyf['space'], hmtx['space'] = empty, (round(2.6 * U), 0)
    cmap[0x20] = 'space'
    cmap[0xA0] = 'space'

    defs = dict(GLYPHS)
    defs['S'] = defs.pop('S_logo') if s_variant == 'logo' else defs.pop('S_square')
    defs.pop('S_logo', None)
    defs.pop('S_square', None)
    defs.update(DIGITS)

    for ch, polys in defs.items():
        name = 'g%04X' % ord(ch)
        glyph, adv = draw_polylines(polys, stroke)
        glyf[name], hmtx[name] = glyph, (adv, 0)
        order.append(name)
        cmap[ord(ch)] = name
        if ch.isalpha() and not case:
            cmap[ord(ch.lower())] = name  # all capitals, as in the logo
    if case:  # the case-true cut: lowercase is lowercase
        for ch, polys in LOWER.items():
            name = 'g%04X' % ord(ch)
            glyph, adv = draw_polylines(polys, stroke)
            glyf[name], hmtx[name] = glyph, (adv, 0)
            order.append(name)
            cmap[ord(ch)] = name

    # build 104: Cyrillic, Greek, the special Latin letters and the punctuation translations use
    shapes = {}  # every capital's polylines, by character, for the accents below
    shapes.update({ch: p for ch, p in defs.items()})
    for table in (CYRILLIC, GREEK, LATIN_EXTRA):
        shapes.update(table)
    for table in (CYRILLIC_AS, GREEK_AS, LATIN_EXTRA_AS):
        for ch, like in table.items():
            shapes[ch] = shapes[like]

    def add(cp, polys):
        name = 'g%04X' % cp
        glyph, adv = draw_polylines(polys, stroke)
        glyf[name], hmtx[name] = glyph, (adv, 0)
        order.append(name)
        cmap[cp] = name
        return name

    def lower_of(ch):  # the lowercase this capital maps from (a capital whose lowercase is itself: None)
        lo = ch.lower()
        return lo if len(lo) == 1 and lo != ch else None

    for table in (CYRILLIC, GREEK, LATIN_EXTRA, PUNCT_EXTRA):
        for ch, polys in table.items():
            name = add(ord(ch), polys)
            lo = lower_of(ch)
            if lo is not None and table is not PUNCT_EXTRA:
                if case:
                    add(ord(lo), CASE_LOWER.get(lo) or small_caps(polys))
                else:
                    cmap[ord(lo)] = name
    for table in (CYRILLIC_AS, GREEK_AS, LATIN_EXTRA_AS):
        for ch, like in table.items():
            if ord(ch) not in cmap:
                cmap[ord(ch)] = cmap[ord(like)]
            lo = lower_of(ch)
            if lo is not None and ord(lo) not in cmap:
                if case and lo in CASE_LOWER_AS:
                    cmap[ord(lo)] = cmap[ord(CASE_LOWER_AS[lo])]
                elif case:
                    add(ord(lo), small_caps(shapes[like]))
                else:
                    cmap[ord(lo)] = cmap[ord(like)]
    if case:  # dotless i is its own lowercase
        add(0x0131, [[(0, 0), (0, 4)]])
    if ord('\u03C2') not in cmap:  # final sigma
        cmap[0x03C2] = cmap[0x03A3] if not case else cmap.get(0x03C3, cmap[0x03A3])
    if ord('\u00DF') not in cmap:  # sharp s: its capital in the caps cut, a small capital in the case cut
        cmap[0x00DF] = cmap[0x1E9E] if not case else add(0x00DF, small_caps(LATIN_EXTRA['\u1E9E']))
    glyf['zw'], hmtx['zw'] = empty, (0, 0)  # zero-width characters in the translations draw nothing
    order.append('zw')
    for cp in ZERO_WIDTH:
        cmap[cp] = 'zw'

    # accents: each letter its decomposition says is a base and marks, drawn with them
    dotless = {'i': [[(0, 0), (0, 4)]], 'j': [[(1.2, 4), (1.2, -1.6), (0, -1.6)]]}  # i and j lose their dot under a mark
    for cp in list(range(0xC0, 0x250)) + list(range(0x1E00, 0x1F00)) + list(range(0x370, 0x400)) + list(range(0x400, 0x530)):
        if cp in cmap:
            continue
        ch = chr(cp)
        d = unicodedata.normalize('NFD', ch)
        if len(d) < 2:
            continue
        base, marks = d[0], d[1:]
        if base.isupper() or not base.isalpha():
            polys = shapes.get(base)
        elif case and (base in LOWER or base in CASE_LOWER_AS):
            like = CASE_LOWER_AS.get(base, base)
            polys = dotless.get(like, LOWER[like])
        elif case:
            up = base.upper()
            polys = small_caps(shapes[up]) if len(up) == 1 and up in shapes else None
        else:  # the caps cut: a lowercase letter is its capital (the capital's own glyph when it has one)
            if len(ch.upper()) == 1 and ord(ch.upper()) in cmap:
                cmap[cp] = cmap[ord(ch.upper())]
                continue
            up = unicodedata.normalize('NFD', ch.upper())
            if len(up) < 2 or up[1:] != marks:
                up = base.upper() + marks
            base, marks = up[0], up[1:]
            polys = shapes.get(base)
        if polys is None:
            continue
        polys = compose(polys, marks, stroke)
        if polys is not None:
            add(cp, polys)

    # accented Latin letters fall back to their base letter, so other languages stay readable
    for cp in range(0xC0, 0x250):
        base = unicodedata.normalize('NFD', chr(cp))[0]
        if cp not in cmap and base.upper() in defs and base.isalpha():
            cmap[cp] = cmap[ord(base)] if case and base in LOWER else cmap[ord(base.upper())]

    fb = FontBuilder(UPM, isTTF=True)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyf)
    fb.setupHorizontalMetrics(hmtx)
    fb.setupHorizontalHeader(ascent=ASC, descent=DESC, lineGap=9)
    style = ('Bold' if bold else 'Regular') + (' Case' if case else '')
    fb.setupNameTable({'familyName': 'RIPPS2 Sleek', 'styleName': style,
                       'uniqueFontIdentifier': 'RIPPS2 Sleek ' + style, 'fullName': 'RIPPS2 Sleek ' + style,
                       'psName': 'RIPPS2Sleek-' + style.replace(' ', ''), 'version': 'Version 1.4'})
    fb.setupOS2(sTypoAscender=750, sTypoDescender=-170, sTypoLineGap=0, usWinAscent=ASC, usWinDescent=-DESC,
                sCapHeight=CAP, sxHeight=round(4 * U) if case else CAP)
    fb.setupPost()
    fb.setupMaxp()
    return fb.font


def preview(font_path, out):
    from PIL import Image, ImageDraw, ImageFont
    lines = ['MENU RUN INFO OPTIONS REFRESH FAVORITE PS1', 'SETTINGS GAME SOURCES START DEVICE BACK SELECT',
             'ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789', 'VIDEO MODE AUTO  H-POS 0  16:9 480P  4/8']
    im = Image.new('RGB', (1000, 30 + 2 * 44 * len(lines)), (12, 20, 60))
    d = ImageDraw.Draw(im)
    y = 10
    for size in (26, 13):
        f = ImageFont.truetype(font_path, size)
        for line in lines:
            d.text((14, y), line, font=f, fill=(232, 240, 255))
            y += size + 12
    im.save(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--s-variant', choices=('logo', 'square'), default='square')
    ap.add_argument('--weight', choices=('regular', 'bold', 'both'), default='both')
    ap.add_argument('--out-dir', default=os.path.dirname(OUT))
    ap.add_argument('--preview')
    a = ap.parse_args()
    os.makedirs(a.out_dir, exist_ok=True)
    weights = ('regular', 'bold') if a.weight == 'both' else (a.weight,)
    for w in weights:
        path = os.path.join(a.out_dir, 'ripps2_sleek_bold.ttf' if w == 'bold' else 'ripps2_sleek.ttf')
        build(a.s_variant, bold=(w == 'bold')).save(path)
        print('wrote', path)
        if a.preview:
            preview(path, a.preview.replace('.png', '_' + w + '.png'))
        if w == 'bold':  # and the case-true bold, for the keyboard and typed text
            path = os.path.join(a.out_dir, 'ripps2_sleek_case.ttf')
            build(a.s_variant, bold=True, case=True).save(path)
            print('wrote', path)


if __name__ == '__main__':
    main()
