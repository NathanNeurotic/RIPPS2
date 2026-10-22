"""Build 113 mockup: Adapt's vertical category sidebar on real lab captures of Storage, Launch Disc and Memory Files.

The three category glyphs are drawn here as vectors (RIPPS2's thin, even stroke), at 4x and scaled down. The old
horizontal category words (and the view logo under the current one) are masked and filled from what is around them; the freed band shows the page's full name as a header in Roboto Condensed Bold (RIPFLOW's face).

    python make_b113_sidebar.py <frames dir>      writes b113-sidebar-*.png beside this script
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
FONTS = HERE.parents[2] / 'elf' / 'theme' / 'fonts'
W, H = 1920, 1536  # the capture (640x512 at upscale 3)
WHITE = (236, 242, 255)
SOFT = (170, 188, 236)
CYAN = (143, 227, 255)
BLUE = (74, 114, 220)


# ---------------------------------------------------------------- the glyphs (drawn on a 400 px canvas, stroke 22)
def _canvas():
    return Image.new('L', (400, 400), 0)


def glyph_disc():
    im = _canvas()
    d = ImageDraw.Draw(im)
    d.ellipse((40, 40, 360, 360), outline=255, width=22)        # the disc
    d.ellipse((160, 160, 240, 240), outline=255, width=22)      # its hub
    d.arc((92, 92, 308, 308), 200, 250, fill=255, width=14)     # the light on its face
    d.arc((92, 92, 308, 308), 20, 70, fill=255, width=14)
    return im


def glyph_storage():
    im = _canvas()
    d = ImageDraw.Draw(im)
    for k in range(3):                                          # three drives in a stack, each with its light
        y = 52 + k * 104
        d.rounded_rectangle((44, y, 356, y + 84), 14, outline=255, width=22)
        d.ellipse((286, y + 30, 310, y + 54), fill=255)
        d.line((84, y + 42, 200, y + 42), fill=255, width=12)
    return im


def glyph_memory():
    im = _canvas()
    d = ImageDraw.Draw(im)
    # a PS2 memory card: taller than wide, its top-left corner cut, the label lines, the connector along the foot
    pts = [(150, 40), (320, 40), (320, 360), (80, 360), (80, 110)]
    d.line(pts + [pts[0]], fill=255, width=22, joint='curve')
    for y in (120, 160):
        d.line((150, y, 270, y), fill=255, width=12)
    for x in range(110, 300, 40):
        d.rectangle((x, 300, x + 18, 340), fill=255)
    return im


def glyph_star():
    im = _canvas()
    d = ImageDraw.Draw(im)
    import math
    pts = []
    for i in range(10):
        r = 165 if i % 2 == 0 else 70
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((200 + r * math.cos(a), 210 + r * math.sin(a)))
    d.line(pts + [pts[0]], fill=255, width=20, joint='curve')
    return im


def glyph_grid():
    im = _canvas()
    d = ImageDraw.Draw(im)
    for r in range(3):
        for c in range(3):
            x, y = 50 + c * 105, 50 + r * 105
            d.rectangle((x, y, x + 80, y + 80), outline=255, width=16)
    return im


def glyph_usb():
    im = _canvas()
    d = ImageDraw.Draw(im)
    d.rectangle((150, 30, 250, 120), outline=255, width=18)    # the plug
    d.rounded_rectangle((110, 120, 290, 360), 24, outline=255, width=22)  # the stick
    d.rectangle((172, 62, 188, 88), fill=255)
    d.rectangle((212, 62, 228, 88), fill=255)
    return im


def glyph_hdd():
    im = _canvas()
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((60, 60, 340, 340), 22, outline=255, width=22)
    d.ellipse((120, 110, 280, 270), outline=255, width=16)
    d.ellipse((188, 178, 212, 202), fill=255)
    d.line((200, 190, 300, 300), fill=255, width=14)
    return im


def glyph_mmce():
    im = glyph_memory()
    d = ImageDraw.Draw(im)
    d.rectangle((150, 200, 250, 260), outline=255, width=12)   # the SD slot it carries
    return im


def glyph_net():
    im = _canvas()
    d = ImageDraw.Draw(im)
    d.rectangle((150, 40, 250, 120), outline=255, width=18)
    for x in (60, 270):
        d.rectangle((x, 270, x + 80, 350), outline=255, width=18)
    d.line((200, 120, 200, 200), fill=255, width=16)
    d.line((100, 200, 310, 200), fill=255, width=16)
    d.line((100, 200, 100, 270), fill=255, width=16)
    d.line((310, 200, 310, 270), fill=255, width=16)
    return im


def glyph_apps():
    im = _canvas()
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((50, 50, 350, 350), 30, outline=255, width=22)
    d.polygon([(160, 120), (160, 280), (290, 200)], fill=255)
    return im


def glyph_recent():
    im = _canvas()
    d = ImageDraw.Draw(im)
    d.ellipse((50, 50, 350, 350), outline=255, width=22)
    d.line((200, 200, 200, 110), fill=255, width=20)
    d.line((200, 200, 270, 240), fill=255, width=20)
    return im


def tint(mask, size, colour, alpha=1.0):
    m = mask.resize((size, size), Image.LANCZOS)
    out = Image.new('RGBA', (size, size), colour + (0,))
    out.putalpha(m.point(lambda v: int(v * alpha)))
    return out


def glow(layer, radius, colour, strength=1.6):
    a = layer.split()[3].filter(ImageFilter.GaussianBlur(radius))
    a = a.point(lambda v: min(255, int(v * strength)))
    g = Image.new('RGBA', layer.size, colour + (0,))
    g.putalpha(a)
    return g


# ---------------------------------------------------------------- the page
def text_out(img, regions):
    """The old category words and the view logo taken out: within each region, the pixels that are text (light and
    grey, or the logo's cyan glow), grown a little, filled from what is around them (normalized blur, then smoothed)."""
    from scipy import ndimage
    a = np.asarray(img, np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    mx, mn = a.max(2), a.min(2)
    sat = (mx - mn) / np.maximum(mx, 1)
    texty = ((lum > 95) & (sat < 0.38)) | ((b > r + 35) & (lum > 110))
    mask = np.zeros(lum.shape, bool)
    for (x0, y0, x1, y1) in regions:
        mask[y0:y1, x0:x1] = texty[y0:y1, x0:x1]
    mask = ndimage.binary_dilation(mask, iterations=7)
    keep = (~mask).astype(np.float32)
    out = a.copy()
    for sigma in (40, 16, 6):  # coarse to fine: the fill takes the colours around it, then their shape
        num = np.stack([ndimage.gaussian_filter(out[..., c] * keep, sigma) for c in range(3)], 2)
        den = ndimage.gaussian_filter(keep, sigma)[..., None]
        fill = num / np.maximum(den, 1e-4)
        out[mask] = fill[mask]
    for _ in range(60):
        avg = (np.roll(out, 1, 0) + np.roll(out, -1, 0) + np.roll(out, 1, 1) + np.roll(out, -1, 1)) / 4
        out[mask] = avg[mask]
    soft = ndimage.gaussian_filter(mask.astype(np.float32), 2)[..., None]
    res = a * (1 - soft) + out * soft
    return Image.fromarray(np.clip(res, 0, 255).astype(np.uint8))


def glass(img, box, colour, alpha, blur=18):
    """Adapt's Ripps2PanelGlass, frosted (blur=1) with a tint: the page under it blurred, then the tint over it"""
    x0, y0, x1, y1 = box
    region = img.crop(box).filter(ImageFilter.GaussianBlur(blur))
    img.paste(Image.blend(region, Image.new('RGB', region.size, colour), alpha), (x0, y0))


# Adapt's side bar, in the capture's pixels (640x512 at 3x): main2 x 0..26 tint 88 #01040F, main3 x 28..40 tint 22
BAR_W, ACCENT = 78, (84, 120)
BAR_TINT, ACCENT_TINT = ((1, 4, 15), 88 / 128), ((40, 197, 249), 22 / 128)


def draw_bar(img, width=BAR_W):
    """The bar where the page has none of its own (Launch Disc, Memory Files): full height, its accent beside it"""
    glass(img, (0, 0, width, H), *BAR_TINT)
    glass(img, (width + 6, 0, width + 42, H), *ACCENT_TINT, blur=10)


GLYPH, PITCH, MID = 50, 118, 768  # each glyph's size, the stack's pitch, its middle (the screen's)


def bar_glyphs(img, current, focus=None):
    """The three category glyphs inside the bar: the page you are on lit, Left's focus framed as RIPGRID's covers"""
    glyphs = [glyph_disc(), glyph_storage(), glyph_memory()]  # LAUNCH DISC, STORAGE, MEMORY FILES
    rgba = img.convert('RGBA')
    cx = BAR_W // 2
    for k, g in enumerate(glyphs):
        cy = MID + (k - 1) * PITCH
        x, y = cx - GLYPH // 2, cy - GLYPH // 2
        if k == current:
            t = Image.new('RGBA', rgba.size, (0, 0, 0, 0))
            ImageDraw.Draw(t).rounded_rectangle((6, cy - 36, BAR_W - 6, cy + 36), 12, fill=(30, 60, 150, 215))
            rgba = Image.alpha_composite(rgba, t)
            layer = Image.new('RGBA', rgba.size, (0, 0, 0, 0))
            layer.paste(tint(g, GLYPH, WHITE), (x, y))
            rgba = Image.alpha_composite(rgba, glow(layer, 8, CYAN))
            rgba = Image.alpha_composite(rgba, layer)
        else:
            layer = Image.new('RGBA', rgba.size, (0, 0, 0, 0))
            layer.paste(tint(g, GLYPH, SOFT, 0.8), (x, y))
            rgba = Image.alpha_composite(rgba, layer)
        if k == focus:
            f = Image.new('RGBA', rgba.size, (0, 0, 0, 0))
            ImageDraw.Draw(f).rounded_rectangle((3, cy - 39, BAR_W - 3, cy + 39), 14, outline=CYAN + (255,), width=5)
            rgba = Image.alpha_composite(rgba, glow(f, 8, CYAN, 1.3))
            rgba = Image.alpha_composite(rgba, f)
    return rgba.convert('RGB')


def header(img, name):
    """Launch Disc's and Memory Files' title, centred in the band the old category words left (Storage has none)"""
    f = ImageFont.truetype(str(FONTS / 'ripflow_bold.ttf'), 92)
    shadow = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).text((W // 2 + 5, 52), name, font=f, fill=(0, 0, 0, 170), anchor='mt')
    s = shadow.filter(ImageFilter.GaussianBlur(6))
    img.paste(s, (0, 0), s)
    ImageDraw.Draw(img).text((W // 2, 46), name, font=f, fill=WHITE, anchor='mt')


DRAWER = 606  # the bar opened as far as the list panel (Adapt's main4 starts at x 216, 648 here)


def sources(img):
    """Circle on Storage: the bar slides open into a drawer, the sources down it, its accent along the new edge"""
    rows = [(glyph_grid(), 'All Games'), (glyph_usb(), 'USB'), (glyph_mmce(), 'MMCE'), (glyph_hdd(), 'Internal HDD'),
            (glyph_net(), 'Network (SMB)'), (glyph_apps(), 'Apps'), (glyph_star(), 'Starred Games'), (glyph_recent(), 'Last Played')]
    glass(img, (BAR_W, 0, DRAWER, H), *BAR_TINT)                     # the bar, wider
    glass(img, (ACCENT[0], 0, ACCENT[1], H), *BAR_TINT)               # the old accent under it
    glass(img, (DRAWER + 6, 0, DRAWER + 42, H), *ACCENT_TINT, blur=10)  # the accent at the drawer's edge
    rgba = img.convert('RGBA')
    f = ImageFont.truetype(str(FONTS / 'ripflow_bold.ttf'), 46)
    rh = 92
    y0 = MID - len(rows) * rh // 2
    for i, (g, name) in enumerate(rows):
        y = y0 + i * rh
        lit = i == 0
        if lit:
            t = Image.new('RGBA', rgba.size, (0, 0, 0, 0))
            ImageDraw.Draw(t).rounded_rectangle((BAR_W + 10, y + 6, DRAWER - 14, y + rh - 6), 12, fill=(30, 60, 150, 215))
            ImageDraw.Draw(t).rectangle((BAR_W + 10, y + 6, BAR_W + 16, y + rh - 6), fill=(106, 154, 255, 255))
            rgba = Image.alpha_composite(rgba, t)
        layer = Image.new('RGBA', rgba.size, (0, 0, 0, 0))
        layer.paste(tint(g, 52, WHITE if lit else SOFT, 1.0 if lit else 0.8), (BAR_W + 32, y + 20))
        rgba = Image.alpha_composite(rgba, layer)
        ImageDraw.Draw(rgba).text((BAR_W + 104, y + 46), name, font=f, fill=(WHITE if lit else SOFT) + (255,), anchor='lm')
    return rgba.convert('RGB')


def hints_on_top(img, original, band=(1390, 1530)):
    """The hint row draws over the drawer (as the engine draws hints last): its text and glyphs put back"""
    a = np.asarray(original, np.float32)
    lum = a.mean(2)
    sat = (a.max(2) - a.min(2)) / np.maximum(a.max(2), 1)
    keep = np.zeros(lum.shape, bool)
    keep[band[0]:band[1], :DRAWER + 42] = (lum > 120)[band[0]:band[1], :DRAWER + 42] | ((sat > 0.45) & (lum > 90))[band[0]:band[1], :DRAWER + 42]
    m = Image.fromarray((keep * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
    return Image.composite(original, img, m)


ADAPT_LIST_FONT = Path('C:/Users/Mini PC/Desktop/Webpages - Projects/RIPPS2-themes/themes/thm_Adapt/b.ttf')


def unselect_row(img, title='Burnout 3 - Takedown', box=(640, 344, 1845, 403), above=338, below=408, sample=(405, 455)):
    """The game you left, no longer shown as chosen: the row rebuilt as the panel's glass (blended from the rows either
    side) with its title redrawn in the list's own face (Adapt's b.ttf) and colour, where the cyan title stood"""
    a = np.asarray(img, np.float32).copy()
    x0, y0, x1, y1 = box
    reg = a[y0:y1, x0:x1]
    cyan = ((reg[..., 2] - reg[..., 0]) > 70) & (reg.mean(2) >= 130)
    cyan[:, :40] = False  # the bar's own notch at its left end is not the title
    ys, xs = np.nonzero(cyan)
    tx0, ty0, ty1 = x0 + xs.min(), y0 + ys.min(), y0 + ys.max()
    from scipy import ndimage
    k = np.linspace(0, 1, y1 - y0)[:, None, None]
    # the glass either side, with the letters that touch those rows filtered out along the row
    up = ndimage.median_filter(a[above - 3:above + 1, x0:x1].mean(0), size=(41, 1))
    down = ndimage.median_filter(a[below:below + 4, x0:x1].mean(0), size=(41, 1))
    a[y0:y1, x0:x1] = up[None] * (1 - k) + down[None] * k
    rows = a[sample[0]:sample[1], 700:1500]
    lit = rows[rows.mean(2) > 150]
    colour = tuple(int(v) for v in np.median(lit, 0)) if len(lit) else (200, 206, 226)
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    size, f = 40, None
    for size in range(30, 90):  # the face's size whose letters stand as tall as the chosen title's did
        f = ImageFont.truetype(str(ADAPT_LIST_FONT), size)
        bb = ImageDraw.Draw(im).textbbox((0, 0), title, font=f)
        if bb[3] - bb[1] >= ty1 - ty0:
            break
    d = ImageDraw.Draw(im)
    bb = d.textbbox((0, 0), title, font=f)
    d.text((tx0 - bb[0], ty0 - bb[1]), title, font=f, fill=colour)
    return im


def sidebar_hints(img, original, band=(1396, 1470)):
    """While the bar has the focus the hints say what the bar does: choose a page, open it, back to the games"""
    from scipy import ndimage
    a = np.asarray(img, np.float32)
    mask = np.zeros(a.shape[:2], bool)
    mask[band[0]:band[1], 130:1905] = True
    keep = (~mask).astype(np.float32)
    out = a.copy()
    sigma = 40  # wide enough that the band's middle still sees its edges
    num = np.stack([ndimage.gaussian_filter(out[..., c] * keep, sigma) for c in range(3)], 2)
    den = ndimage.gaussian_filter(keep, sigma)[..., None]
    out[mask] = (num / np.maximum(den, 1e-4))[mask]
    im = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).convert('RGBA')
    disc = original.crop((381, 1400, 449, 1468)).convert('RGBA')        # the capture's own cross button
    m = Image.new('L', disc.size, 0)
    ImageDraw.Draw(m).ellipse((2, 2, 65, 65), fill=255)
    disc.putalpha(m)

    def button(symbol):
        b = Image.new('RGBA', (68, 68), (0, 0, 0, 0))
        d = ImageDraw.Draw(b)
        d.ellipse((2, 2, 65, 65), fill=(28, 32, 44, 235), outline=(70, 78, 96, 255), width=2)
        if symbol == 'circle':
            d.ellipse((19, 19, 48, 48), outline=(232, 84, 104, 255), width=5)
        else:  # the D-pad's up and down
            d.polygon([(34, 12), (23, 27), (45, 27)], fill=(236, 242, 255, 255))
            d.polygon([(34, 56), (23, 41), (45, 41)], fill=(236, 242, 255, 255))
        return b
    f = ImageFont.truetype(str(FONTS / 'ripps2_sleek_case.ttf'), 50)
    x, y = 170, 1400
    d = ImageDraw.Draw(im)
    for glyph, word in ((button('dpad'), 'Choose'), (disc, 'Open'), (button('circle'), 'Back')):
        im.alpha_composite(glyph, (x, y))
        d.text((x + 74, y + 34), word, font=f, fill=(255, 255, 255, 255), anchor='lm')
        x += 74 + int(d.textlength(word, font=f)) + 54
    return im.convert('RGB')


# the old horizontal words, and the view logo under whichever is current
TOP = [(130, 30, 640, 225), (740, 30, 1180, 225), (1230, 30, 1850, 225)]


def main():
    src = Path(sys.argv[1])
    storage = Image.open(src / 'f_23.5.png').convert('RGB')
    launch = Image.open(src / 'f_29.5.png').convert('RGB')
    memory = Image.open(src / 'f_38.png').convert('RGB')
    pages = []
    s = text_out(storage, TOP)  # Adapt draws its own bar on Storage: the glyphs go into it, no title
    pages.append(('storage', bar_glyphs(s, 1)))
    sf = sidebar_hints(unselect_row(s), storage)
    pages.append(('storage-focus', bar_glyphs(sf, 1, focus=2)))
    l = text_out(launch, TOP)
    draw_bar(l)
    header(l, 'LAUNCH DISC')
    pages.append(('launch-disc', bar_glyphs(l, 0)))
    m = text_out(memory, TOP)
    draw_bar(m)
    header(m, 'MEMORY FILES')
    pages.append(('memory-files', bar_glyphs(m, 2)))
    c = text_out(storage, TOP)
    c = sources(c)
    c = hints_on_top(c, storage)
    pages.append(('storage-sources', bar_glyphs(c, 1)))
    for name, im in pages:
        im.save(HERE / ('b113-sidebar-%s.png' % name))
    tw, th = 960, 768
    sheet = Image.new('RGB', (tw * 3, th * 2 + 60), (6, 10, 28))
    d = ImageDraw.Draw(sheet)
    lab = ImageFont.truetype(str(FONTS / 'ripflow.ttf'), 30)
    order = [('storage', 'Storage: the glyphs inside the Adapt bar, no title'), ('launch-disc', 'Launch Disc: the bar as a full strip, title centred'),
             ('memory-files', 'Memory Files: the same'), ('storage-focus', 'Storage: Left on the list: bar focused, game let go, hints for the bar'),
             ('storage-sources', 'Storage: Circle, the bar opens into a drawer of sources')]
    ims = dict(pages)
    for i, (k, label) in enumerate(order):
        x, y = (i % 3) * tw, (i // 3) * (th + 30)
        sheet.paste(ims[k].resize((tw, th), Image.LANCZOS), (x, y + 30))
        d.text((x + 12, y + 2), label, font=lab, fill=SOFT)
    sheet.save(HERE / 'b113-sidebar-sheet.png')
    print('saved', len(pages), 'pages and the sheet')


if __name__ == '__main__':
    main()
