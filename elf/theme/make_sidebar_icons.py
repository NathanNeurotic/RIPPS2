"""RIPPS2 build 113: the category sidebar's glyphs and its drawer's source glyphs, one atlas (ripps2_sidebar_icons.png).

Row 0: the line icons, anti-aliased white strokes on transparency (tinted at draw time).
Row 1: the same icons blurred into a soft glow, drawn additively under the lit one.
Cells are 32 px, about the size the sidebar draws them at (the GS has no mipmaps, so a much bigger cell drawn small
samples unevenly). Shapes are drawn on a 400-unit design square, 8x supersampled, then reduced.

    0 LAUNCH DISC  a disc, its hub and the light on its face
    1 STORAGE      three drives in a stack, each with its light
    2 MEMORY FILES a PS2 memory card: the cut corner, the label, the connector
    3 All Games  4 USB / BDM  5 MMCE  6 Internal HDD  7 Network  8 Apps  9 Starred Games  10 Last Played

    python make_sidebar_icons.py [out.png]       (default: gfx/ripps2_sidebar_icons.png beside this script)
    python tools/png8.py gfx                     then, as for every theme image (it converts exactly: 255 colours)
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

CELL, SS, DESIGN = 32, 8, 400.0
BIG = CELL * SS
K = BIG / DESIGN
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'gfx', 'ripps2_sidebar_icons.png')


def S(v):
    return v * K


def box(x0, y0, x1, y1):
    return (S(x0), S(y0), S(x1), S(y1))


def canvas():
    im = Image.new('L', (BIG, BIG), 0)
    return im, ImageDraw.Draw(im)


def disc():
    im, d = canvas()
    d.ellipse(box(40, 40, 360, 360), outline=255, width=int(S(26)))
    d.ellipse(box(160, 160, 240, 240), outline=255, width=int(S(24)))
    d.arc(box(92, 92, 308, 308), 200, 250, fill=255, width=int(S(16)))
    d.arc(box(92, 92, 308, 308), 20, 70, fill=255, width=int(S(16)))
    return im


def storage():
    im, d = canvas()
    for k in range(3):
        y = 52 + k * 104
        d.rounded_rectangle(box(44, y, 356, y + 84), int(S(14)), outline=255, width=int(S(24)))
        d.ellipse(box(282, y + 28, 310, y + 56), fill=255)
        d.line([(S(84), S(y + 42)), (S(200), S(y + 42))], fill=255, width=int(S(16)))
    return im


def memory(slot=False):
    im, d = canvas()
    pts = [(150, 40), (320, 40), (320, 360), (80, 360), (80, 110)]
    pts = [(S(x), S(y)) for x, y in pts]
    d.line(pts + [pts[0]], fill=255, width=int(S(26)), joint='curve')
    for x, y in pts:  # round the corners the joint leaves square
        r = S(13)
        d.ellipse((x - r, y - r, x + r, y + r), fill=255)
    if slot:  # MMCE: the SD card it carries
        d.rectangle(box(150, 190, 250, 260), outline=255, width=int(S(16)))
    else:
        for y in (120, 160):
            d.line([(S(150), S(y)), (S(270), S(y))], fill=255, width=int(S(16)))
    for x in range(110, 300, 40):
        d.rectangle(box(x, 296, x + 20, 336), fill=255)
    return im


def grid():
    im, d = canvas()
    for r in range(3):
        for c in range(3):
            x, y = 50 + c * 105, 50 + r * 105
            d.rectangle(box(x, y, x + 80, y + 80), outline=255, width=int(S(20)))
    return im


def usb():
    im, d = canvas()
    d.rectangle(box(150, 30, 250, 120), outline=255, width=int(S(22)))
    d.rounded_rectangle(box(110, 120, 290, 360), int(S(24)), outline=255, width=int(S(26)))
    d.rectangle(box(170, 60, 190, 90), fill=255)
    d.rectangle(box(210, 60, 230, 90), fill=255)
    return im


def hdd():
    im, d = canvas()
    d.rounded_rectangle(box(60, 60, 340, 340), int(S(22)), outline=255, width=int(S(26)))
    d.ellipse(box(120, 110, 280, 270), outline=255, width=int(S(20)))
    d.ellipse(box(186, 176, 214, 204), fill=255)
    d.line([(S(200), S(190)), (S(300), S(300))], fill=255, width=int(S(18)))
    return im


def net():
    im, d = canvas()
    w = int(S(22))
    d.rectangle(box(150, 40, 250, 120), outline=255, width=w)
    for x in (60, 260):
        d.rectangle(box(x, 270, x + 80, 350), outline=255, width=w)
    for seg in ((200, 120, 200, 200), (100, 200, 300, 200), (100, 200, 100, 270), (300, 200, 300, 270)):
        d.line([(S(seg[0]), S(seg[1])), (S(seg[2]), S(seg[3]))], fill=255, width=int(S(18)))
    return im


def apps():
    im, d = canvas()
    d.rounded_rectangle(box(50, 50, 350, 350), int(S(30)), outline=255, width=int(S(26)))
    d.polygon([(S(160), S(120)), (S(160), S(280)), (S(290), S(200))], fill=255)
    return im


def star():
    im, d = canvas()
    pts = []
    for i in range(10):
        r = 165 if i % 2 == 0 else 70
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((S(200 + r * math.cos(a)), S(210 + r * math.sin(a))))
    d.line(pts + [pts[0]], fill=255, width=int(S(24)), joint='curve')
    return im


def recent():
    im, d = canvas()
    d.ellipse(box(50, 50, 350, 350), outline=255, width=int(S(26)))
    d.line([(S(200), S(200)), (S(200), S(105))], fill=255, width=int(S(24)))
    d.line([(S(200), S(200)), (S(275), S(245))], fill=255, width=int(S(24)))
    return im


ICONS = [disc, storage, memory, grid, usb, lambda: memory(True), hdd, net, apps, star, recent]


def main():
    sheet = Image.new('RGBA', (CELL * len(ICONS), CELL * 2), (255, 255, 255, 0))
    for i, f in enumerate(ICONS):
        big = f()
        a = big.resize((CELL, CELL), Image.LANCZOS)
        glow = big.filter(ImageFilter.GaussianBlur(S(30))).resize((CELL, CELL), Image.LANCZOS)
        glow = glow.point(lambda v: min(255, int(v * 2.2)))
        for row, alpha in ((0, a), (1, glow)):
            cell = Image.new('RGBA', (CELL, CELL), (255, 255, 255, 0))
            cell.putalpha(alpha)
            sheet.paste(cell, (i * CELL, row * CELL))
    sheet.save(OUT, optimize=True)
    print('wrote', OUT, sheet.size)


if __name__ == '__main__':
    main()
