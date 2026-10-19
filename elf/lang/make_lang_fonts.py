"""The language fonts RIPPS2 ships beside Open PS2 Loader's (RIPPS2 build 104), in elf/lang/fonts:

- DejaVuSans-Arabic.ttf: DejaVu Sans 2.37 cut to Latin-1, the Arabic block and both presentation-form blocks. RIPPS2
  joins Arabic and Persian letters itself (ripps2Rtl in RiptOPL's src/ripps2tr.c) into those presentation forms, so
  the font must carry all of them; upstream's font_Arabic is a cut without them.
- NotoSansLao-Regular.ttf: Noto Sans Lao 2.003 (hinted), as released.

Both come from their projects' own GitHub releases (downloaded once by hand; the user approved the sources on
2026-10-19): github.com/dejavu-fonts/dejavu-fonts (dejavu-sans-ttf-2.37.zip) and github.com/notofonts/lao
(NotoSansLao-v2.003.zip). Their licences go beside them and into the language pack.

    python3 elf/lang/make_lang_fonts.py <dejavu-sans-ttf-2.37.zip> <NotoSansLao-v2.003.zip>
"""
import io
import os
import sys
import zipfile

from fontTools import subset
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'fonts')
ARABIC = (list(range(0x20, 0x100)) + list(range(0x0600, 0x0700)) + list(range(0xFB50, 0xFE00)) +
          list(range(0xFE70, 0xFF00)) + list(range(0x2010, 0x2028)) + [0x200C, 0x200D])


def main(dejavu_zip, lao_zip):
    os.makedirs(OUT, exist_ok=True)
    z = zipfile.ZipFile(dejavu_zip)
    font = TTFont(io.BytesIO(z.read('dejavu-sans-ttf-2.37/ttf/DejaVuSans.ttf')))
    opts = subset.Options()
    opts.layout_features = []  # RIPPS2 draws the presentation forms themselves, no GSUB/GPOS
    opts.name_IDs = ['*']
    opts.name_languages = ['*']
    opts.notdef_outline = True
    opts.hinting = False
    sub = subset.Subsetter(opts)
    sub.populate(unicodes=ARABIC)
    sub.subset(font)
    font.save(os.path.join(OUT, 'DejaVuSans-Arabic.ttf'))
    with open(os.path.join(OUT, 'LICENSE-DejaVu.txt'), 'wb') as f:
        f.write(z.read('dejavu-sans-ttf-2.37/LICENSE'))

    z = zipfile.ZipFile(lao_zip)
    with open(os.path.join(OUT, 'NotoSansLao-Regular.ttf'), 'wb') as f:
        f.write(z.read('NotoSansLao/hinted/ttf/NotoSansLao-Regular.ttf'))
    with open(os.path.join(OUT, 'OFL-NotoSansLao.txt'), 'wb') as f:
        f.write(z.read('OFL.txt'))
    for name in sorted(os.listdir(OUT)):
        print('%-28s %7d bytes' % (name, os.path.getsize(os.path.join(OUT, name))))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
