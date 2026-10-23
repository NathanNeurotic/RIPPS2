"""RIPPS2's built-in Roboto Condensed (build 114, the font audit's A).

    python3 make_roboto.py <Roboto-VariableFont_wdth,wght.ttf> <out.ttf>

Roboto 3.015's variable font (fonts.google.com/specimen/Roboto, SIL OFL 1.1: ../fonts/ROBOTO-OFL.txt) pinned at width 75
(condensed), its weights 400 to 700 kept, cut to Latin-1 and the punctuation RIPPS2's words use. RIPPS2.elf carries it
as builtin:ripflow (400), builtin:ripflowbold (700) and builtin:roboto (a theme's font<N>_weight).
"""
import io
import sys

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

SRC, OUT = sys.argv[1], sys.argv[2]
LATIN1 = set(range(0x20, 0x7F)) | set(range(0xA0, 0x100)) | {0x2013, 0x2014, 0x2018, 0x2019, 0x201C, 0x201D, 0x2022,
                                                            0x2026, 0x20AC, 0x2122}
f = instancer.instantiateVariableFont(TTFont(SRC), {'wdth': 75, 'wght': (400, 700)}, inplace=False)
b = io.BytesIO()
f.save(b)
f = TTFont(io.BytesIO(b.getvalue()))
opts = subset.Options()
opts.layout_features = ['kern']
opts.name_IDs = [0, 1, 2, 3, 4, 5, 6]
opts.notdef_outline = True
opts.glyph_names = False
opts.hinting = True
opts.drop_tables += ['DSIG', 'GSUB', 'GDEF', 'FFTM', 'STAT']
s = subset.Subsetter(opts)
s.populate(unicodes=sorted(LATIN1))
s.subset(f)
for rec in f['name'].names:
    if rec.nameID in (1, 4):
        rec.string = 'Roboto Condensed'
    if rec.nameID == 6:
        rec.string = 'RobotoCondensed-Variable'
f.save(OUT)
t = TTFont(OUT)
print(OUT, len(open(OUT, 'rb').read()), 'bytes; axes', [(a.axisTag, a.minValue, a.defaultValue, a.maxValue) for a in t['fvar'].axes])
