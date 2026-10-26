"""Per language: how the words the build 115 strings use are already translated (ours first, then upstream OPL).
Upstream's files: LNG_SRC=<a clone of github.com/ps2homebrew/Open-PS2-Loader-lang> (glossary.txt holds a run of this)."""
import json
import os
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
LANG = os.path.join(HERE, '..', '..', 'elf', 'lang')
R = os.environ.get('RIPTOPL_DIR', os.path.join(HERE, '..', '..', '..', 'RiptOPL'))
UP = os.environ.get('LNG_SRC', os.path.join(HERE, 'lng_src'))

base = {e['label']: e['string'] for e in yaml.safe_load(open(R + '/lng_tmpl/_base.yml', encoding='utf-8'))['gui_strings'] if 'label' in e}
LABELS = ['SETTINGS', 'RIPPS2_ALL_GAMES', 'RIPPS2_LAUNCH_DISC', 'RIPPS2_RECENTS', 'GAME_LAUNCHING', 'INTERFACE_SETTINGS', 'MENU_AUDIO',
          'RIPPS2_BIOS_MUSIC', 'RIPPS2_BOOT_LOADER', 'RIPPS2_IGR_MENU', 'HDD_GAMES', 'THEME', 'MANUAL', 'AUTO', 'OFF', 'ON', 'NORMAL',
          'RIPPS2_CACHE', 'RIPPS2_CATEGORY_LAYOUT', 'MENU', 'RIPPS2_FAST_CACHE', 'RIPPS2_CATEGORY_BAR', 'RIPPS2_STARSIDE',
          'RIPPS2_TEXT_WEIGHT', 'EXITPATH', 'AUTO_CREATE_VMC', 'RIPPS2_HIDDEN_GAMES', 'RIPPS2_FADE_IDLE', 'RIPPS2_SIDEBAR_STYLE']
STRINGS = ['Memory Files', 'Storage', 'STATUS', 'Starred', 'Hidden', 'Left', 'Right', 'Bold', 'Cache', 'Fade When Idle', 'Sidebar',
           'Theme', 'Recent', 'Layout', 'Name', 'Audio', 'Screen', 'Controllers', 'Classic', 'RENAME', 'Rename']

langs = sys.argv[1:] or sorted(f[:-4] for f in os.listdir(LANG) if f.endswith('.yml') and not f.startswith('_'))
for lang in langs:
    d = yaml.safe_load(open(os.path.join(LANG, lang + '.yml'), encoding='utf-8')) or {}
    mine_s, mine_l = d.get('strings') or {}, d.get('labels') or {}
    up = {}
    if os.path.exists(os.path.join(UP, lang + '.yml')):
        up = (yaml.safe_load(open(os.path.join(UP, lang + '.yml'), encoding='utf-8')) or {}).get('translations') or {}
    out = {}
    for k in LABELS:
        v = mine_l.get(k) or (up.get(k) if isinstance(up.get(k), str) else None)
        if v:
            out[base.get(k, k)] = v
    for s in STRINGS:
        if mine_s.get(s):
            out[s] = mine_s[s]
    print('== %s: %s' % (lang, json.dumps(out, ensure_ascii=False)))
