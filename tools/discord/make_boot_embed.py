"""Build a Discord Component Embed payload and a local visual preview for RIPPS2."""
import argparse
import html
import json
import os
import shutil

from make_test_embed import HERE

GIF_NAME = 'ripps2-boot-empty-games.gif'
GIF_URL = 'https://akilluminati47.github.io/RIPPS2/media/b114/ripps2-boot-empty-games.gif?v=20261025'
ICON_URL = 'https://akilluminati47.github.io/RIPPS2/media/deadelf/ripps2-deadelf-bluehat.png'
WEBSITE_TITLE = 'Here lies an idea . . .'
WEBSITE_DESCRIPTION = ('RIPPS2 | rest in pieces. Launch physical media, rip it into your library to enjoy, '
                       'and manage files with ease. Homebrew Game Loader for Sony PlayStation 2 '
                       '(Supports 33 World Languages)')
WEBSITE = 'https://akilluminati47.github.io/RIPPS2/'
PSX_PLACE = 'https://www.psx-place.com/threads/ripps2-a-ps2-front-end-in-one-elf-launch-disc-storage-memory-files.51316/'
GITHUB = 'https://github.com/akilluminati47/RIPPS2'
GUNS_LOL = 'https://guns.lol/akilluminati47'
INTRO = [
    'A PlayStation 2 front end that brings games, discs, memory cards, files and themes together.',
    'Built for real PS2 hardware, with live animated towers and a clean, easy-to-navigate interface.',
    'Explore the project, get the latest release, or join the community using the links below.',
]
LINKS = [('Website', WEBSITE), ('PSX-Place', PSX_PLACE), ('GitHub', GITHUB), ('guns.lol', GUNS_LOL)]
GIF_ALT = ('The RIPPS2 towers rise into an empty All Games list, pause on the Start menu, '
           'then return to the list')


def make_payload(gif_url):
    """Return the website-unfurl schema documented by Discord's Component Embeds reference."""
    header = f'# [{WEBSITE_TITLE}]({WEBSITE})'
    about = '**About RIPPS2**\n' + '\n'.join('- ' + line for line in INTRO)
    return {
        'component': {
            'type': 17,
            'accent_color': 0x3C6EF0,
            'components': [
                {
                    'type': 9,
                    'components': [
                        {'type': 10, 'content': header},
                        {'type': 10, 'content': WEBSITE_DESCRIPTION},
                    ],
                    'accessory': {
                        'type': 11,
                        'media': {'url': ICON_URL},
                        'description': 'RIPPS2 brand icon',
                    },
                },
                {
                    'type': 12,
                    'items': [{'media': {'url': gif_url}, 'description': GIF_ALT}],
                },
                {'type': 10, 'content': about},
                {
                    'type': 1,
                    'components': [
                        {'type': 2, 'style': 5, 'label': label, 'url': url}
                        for label, url in LINKS
                    ],
                },
            ],
        },
    }


def make_preview(path, gif_src, icon_src):
    esc = html.escape
    bullets = ''.join('<li>%s</li>' % esc(line) for line in INTRO)
    buttons = ''.join(
        '<a class="button" href="%s">%s</a>' % (esc(url, quote=True), esc(label))
        for label, url in LINKS
    )
    doc = '''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>RIPPS2 Discord Component Embed preview</title>
<style>*{box-sizing:border-box}body{margin:0;background:#313338;color:#dbdee1;font:16px/1.5 Arial,sans-serif;padding:28px}main{max-width:720px;margin:auto}.note{color:#b5bac1;font-size:14px;margin:0 0 16px}.component{background:#2b2d31;border:1px solid #3c6ef0;border-radius:8px;padding:16px;color:#dbdee1}.head{display:flex;align-items:center;gap:16px}.head-copy{flex:1;min-width:0}h1{font-size:20px;line-height:1.3;margin:0 0 8px;color:#f2f3f5}.head-copy a{color:inherit;text-decoration:none}.description{margin:0}.icon{width:64px;height:64px;object-fit:cover;border-radius:8px}.gif{width:100%;height:auto;max-height:460px;object-fit:contain;display:block;border-radius:4px;margin:16px 0}.about{margin:0 0 14px;padding-left:24px}.about li{margin:3px 0}.buttons{display:flex;gap:8px;flex-wrap:wrap;border-top:1px solid #45474f;padding-top:12px}.button{background:#4e5058;color:#fff;padding:7px 12px;border-radius:4px;text-decoration:none;font-weight:600;font-size:14px}</style></head><body><main><p class="note">Local preview of Discord's website Component Embed — not posted.</p><article class="component"><section class="head"><div class="head-copy"><h1><a href="__WEBSITE__">__TITLE__</a></h1><p class="description">__DESCRIPTION__</p></div><img class="icon" src="__ICON__" alt="RIPPS2 brand icon"></section><img class="gif" src="__GIF__" alt="__ALT__"><ul class="about">__BULLETS__</ul><nav class="buttons">__BUTTONS__</nav></article></main></body></html>'''
    for key, value in {
        '__WEBSITE__': esc(WEBSITE, quote=True), '__TITLE__': esc(WEBSITE_TITLE),
        '__DESCRIPTION__': esc(WEBSITE_DESCRIPTION), '__ICON__': esc(icon_src, quote=True),
        '__GIF__': esc(gif_src, quote=True), '__ALT__': esc(GIF_ALT, quote=True),
        '__BULLETS__': bullets, '__BUTTONS__': buttons,
    }.items():
        doc = doc.replace(key, value)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(doc)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--gif', required=True, help='the boot-to-empty-games GIF to copy into the preview folder')
    ap.add_argument('--out', default=os.path.join(HERE, '..', '..', 'out', 'boot-empty-games'))
    ap.add_argument('--gif-url', default=GIF_URL, help='public GIF URL used by Discord; defaults to the GitHub Pages asset')
    args = ap.parse_args()

    gif_path = os.path.abspath(args.gif)
    if not os.path.isfile(gif_path):
        ap.error('GIF not found: ' + gif_path)
    os.makedirs(args.out, exist_ok=True)
    gif_copy = os.path.join(args.out, GIF_NAME)
    if os.path.abspath(gif_path) != os.path.abspath(gif_copy):
        shutil.copy2(gif_path, gif_copy)
    data = make_payload(args.gif_url)
    json_path = os.path.join(args.out, 'component-embed.json')
    json_text = json.dumps(data, indent=2, ensure_ascii=False)
    payload_bytes = len(json_text.encode('utf-8'))
    if payload_bytes > 3000:
        ap.error(f'Component Embed payload is {payload_bytes} bytes; Discord limit is 3000')
    with open(json_path, 'w', encoding='utf-8') as f:
        f.write(json_text + '\n')
    preview_path = os.path.join(args.out, 'embed-preview.html')
    make_preview(preview_path, GIF_NAME, os.path.join('..', '..', 'media', 'deadelf', 'ripps2-deadelf-bluehat.png'))
    print('GIF:', gif_copy)
    print('Payload:', json_path, f'({payload_bytes} bytes)')
    print('Preview:', preview_path)


if __name__ == '__main__':
    main()
