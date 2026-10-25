"""Strip the built-in fonts of what RIPPS2's FreeType never reads (build 114), in place.

    python3 strip_fonts.py <font.ttf> ...

The fonts compiled into RIPPS2.elf are drawn by FreeType with fntsys.c: outlines (glyf, loca, cmap, hmtx, hhea, head,
maxp, OS/2), hinting where a face has it (fpgm, prep, cvt, gasp, hdmx, LTSH, VDMX) and kerning (kern, GPOS): every one
of those stays, so no letter moves. What goes is only what nothing reads on the console: the PostScript glyph names
(post becomes format 3), the name table's records past the six that identify a face, a DSIG, FontForge's FFTM, and the
substitution tables (GSUB, GDEF: fntsys shapes nothing). Each font is checked after: every glyph's outline, advance
and cmap entry are the same, or the file is left as it was. Prints the bytes saved.
"""
import io
import sys

from fontTools.ttLib import TTFont

DROP = ("DSIG", "FFTM", "GSUB", "GDEF")


def outlines(font):
    glyf = font["glyf"] if "glyf" in font else None
    hmtx = font["hmtx"].metrics
    cmap = font.getBestCmap() or {}
    out = {}
    for name in font.getGlyphOrder():
        g = glyf[name] if glyf is not None else None
        data = g.compile(glyf) if g is not None and g.numberOfContours != 0 else b""
        out[name] = (data, hmtx.get(name))
    return out, dict(cmap)


def strip(path):
    raw = open(path, "rb").read()
    font = TTFont(io.BytesIO(raw))
    before = outlines(font)
    for tag in DROP:
        if tag in font:
            del font[tag]
    if "post" in font:
        font["post"].formatType = 3.0
        font["post"].extraNames = []
        font["post"].mapping = {}
    if "name" in font:
        font["name"].names = [n for n in font["name"].names if n.nameID <= 6]
    buf = io.BytesIO()
    font.save(buf)
    new = buf.getvalue()
    check = TTFont(io.BytesIO(new))
    # format 3 post renames the glyphs; compare by glyph order, which the strip leaves alone
    after = outlines(check)
    same = list(before[0].values()) == list(after[0].values()) and \
        [before[1].get(c) is not None for c in sorted(before[1])] == [after[1].get(c) is not None for c in sorted(before[1])] and \
        len(before[1]) == len(after[1])
    if not same or len(new) >= len(raw):
        print("%s: left as it was (%s)" % (path, "an outline would change" if not same else "nothing to save"))
        return 0
    open(path, "wb").write(new)
    print("%s: %d -> %d bytes" % (path, len(raw), len(new)))
    return len(raw) - len(new)


if __name__ == "__main__":
    total = sum(strip(p) for p in sys.argv[1:])
    print("fonts stripped: %d bytes saved" % total)
