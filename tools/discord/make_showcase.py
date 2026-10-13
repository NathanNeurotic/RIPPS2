"""RIPPS2's showcase post: what RIPPS2 does, for any Discord (users, not testers).

Builds, from one notes file (notes/showcase-beta.md, itself the message to paste):
  kill-it-ripps2.png      the banner: "Kill it | RIPPS2" over the pillars, the repo's pun under it
  ripps2-at-a-glance.png  nine screenshots from media/beta, each labelled with what it shows
  post-showcase.json      the same post as a webhook payload (banner, the features as fields, the grid),
                          kept with its icon in the ignored out/showcase

    python make_showcase.py [--notes notes/showcase-beta.md] [--out ../../media/showcase] [--work ../../out/showcase] [--post]

The notes file is Discord markdown under 2000 characters, so it pastes as one message with the two
images attached:
    # <title>
    -# <the line under it>
    <the pitch: one paragraph>
    ### <feature>                 (one heading and one paragraph per feature)
    <text>
    <blank line, then the link lines>

--post sends the webhook version to RIPPS2_DISCORD_WEBHOOK, as make_test_embed.py does (never stored,
never printed). Discord shows no video player for a link in a webhook message with embeds, so the reel
stays a plain link there; pasted by hand, the link plays.
"""
import argparse
import json
import os

from PIL import Image, ImageDraw

from make_test_embed import BLUE, HERE, banner, font, icon, post

BETA = os.path.join(HERE, '..', '..', 'media', 'beta')
LATEST = 'https://github.com/akilluminati47/RIPPS2/releases/latest'

# the grid, in the order the reel tells it: your games, then your files, then what rides along
TILES = [('06-launch-disc', 'Launch Disc'), ('01-adapt', 'Storage'), ('02-ripgrid-flip', 'RIPGRID'),
         ('03-ripflow', 'RIPFLOW'), ('04-info-page', 'Info pages'), ('05-color-blood', 'Color themes'),
         ('07-memory-files', 'Memory Files'), ('08-3d-save-icon', '3D save icons'), ('10-status', 'All on board')]


def grid(w=1280, cols=3, pad=22, gap=14, strip=52):
    """The screenshots at their own 5:4, each over a dark strip with its name, rounded and edged in RIPPS2 blue.
    The names sit under the pictures, never on them: every screen has its own text along the bottom."""
    tw = (w - 2 * pad - (cols - 1) * gap) // cols
    sh = tw * 4 // 5
    th = sh + strip
    rows = (len(TILES) + cols - 1) // cols
    h = 2 * pad + rows * th + (rows - 1) * gap
    im = Image.new('RGBA', (w, h), (0, 0, 0, 255))
    px = im.load()
    for y in range(h):  # the same night as the banner, deepening downward
        t = y / h
        c = (int(3 + 6 * t), int(8 + 16 * t), int(24 + 44 * t), 255)
        for x in range(w):
            px[x, y] = c
    label = font('ripps2_sleek_case.ttf', 30)
    mask = Image.new('L', (tw, th), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, tw - 1, th - 1), radius=14, fill=255)
    for i, (name, text) in enumerate(TILES):
        x, y = pad + (i % cols) * (tw + gap), pad + (i // cols) * (th + gap)
        card = Image.new('RGBA', (tw, th), (6, 13, 36, 255))
        card.paste(Image.open(os.path.join(BETA, name + '.jpg')).convert('RGBA').resize((tw, sh), Image.LANCZOS), (0, 0))
        cd = ImageDraw.Draw(card)
        cd.line((0, sh, tw, sh), fill=(60, 110, 240, 255), width=2)
        cd.rectangle((16, sh + 13, 21, th - 13), fill=(90, 140, 255, 255))
        cd.text((32, sh + 9), text, font=label, fill=(245, 248, 255, 255))
        tile = Image.new('RGBA', (tw, th), (0, 0, 0, 0))
        tile.paste(card, (0, 0), mask)
        im.alpha_composite(tile, (x, y))
        ImageDraw.Draw(im).rounded_rectangle((x, y, x + tw - 1, y + th - 1), radius=14, outline=(60, 110, 240, 255), width=2)
    return im.convert('RGB')


def parse(path):
    title, under, pitch, feats, links, cur, done = '', '', [], [], [], None, False
    for raw in open(path, encoding='utf-8').read().splitlines():
        line = raw.strip()
        if line.startswith('# '):
            title = line[2:]
        elif line.startswith('-# '):
            under = line[3:]
        elif line.startswith('### '):
            cur = [line[4:], []]
            feats.append(cur)
        elif not line:
            if cur is not None:
                done = True
        elif done:
            links.append(line)
        elif cur is not None:
            cur[1].append(line)
        else:
            pitch.append(line)
    return title, under, ' '.join(pitch), feats, links


def payload(notes):
    title, under, pitch, feats, links = parse(notes)
    head = {
        'color': BLUE,
        'author': {'name': 'RIPPS2', 'icon_url': 'attachment://ripps2-icon.png'},
        'title': title, 'url': LATEST,
        'description': '*%s*\n\n%s\n\n%s' % (under, pitch, '\n'.join(links)),
        'image': {'url': 'attachment://kill-it-ripps2.png'},
    }
    body = {'color': BLUE, 'url': LATEST,
            'fields': [{'name': n, 'value': ' '.join(t)[:1024], 'inline': False} for n, t in feats],
            'image': {'url': 'attachment://ripps2-at-a-glance.png'},
            'footer': {'text': 'RIPPS2 v0.1.0 beta  |  one .elf, every drive', 'icon_url': 'attachment://ripps2-icon.png'}}
    return {'content': '', 'embeds': [head, body], 'allowed_mentions': {'parse': []},
            'attachments': [{'id': 0, 'filename': 'kill-it-ripps2.png'}, {'id': 1, 'filename': 'ripps2-at-a-glance.png'},
                            {'id': 2, 'filename': 'ripps2-icon.png'}]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--notes', default=os.path.join(HERE, 'notes', 'showcase-beta.md'))
    ap.add_argument('--out', default=os.path.join(HERE, '..', '..', 'media', 'showcase'))
    ap.add_argument('--work', default=os.path.join(HERE, '..', '..', 'out', 'showcase'))
    ap.add_argument('--post', action='store_true')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    os.makedirs(a.work, exist_ok=True)
    title, under, _, _, _ = parse(a.notes)
    left, right = [t.strip() for t in title.split('|')]
    bn, gr, ic = os.path.join(a.out, 'kill-it-ripps2.png'), os.path.join(a.out, 'ripps2-at-a-glance.png'), os.path.join(a.work, 'ripps2-icon.png')
    banner(100, words=(left, right, under.split('. ', 1)[-1].rstrip('.')), halo=True).save(bn, optimize=True)
    grid().save(gr, optimize=True)
    icon().save(ic, optimize=True)
    data = payload(a.notes)
    jp = os.path.join(a.work, 'post-showcase.json')
    json.dump(data, open(jp, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    text = open(a.notes, encoding='utf-8').read()
    print(bn, gr, jp, 'message %d of 2000 characters, embeds about %d of 6000'
          % (len(text.rstrip('\n').encode('utf-16-le')) // 2, sum(len(json.dumps(e)) for e in data['embeds'])))  # Discord counts UTF-16
    if a.post:
        post(data, [bn, gr, ic])


if __name__ == '__main__':
    main()
