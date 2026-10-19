"""Build 107: SEARCH in Memory Files, in MC EXPLOIT INSTALLER's tile (static checks, and the atlas's new icon)."""
import os
import sys
from pathlib import Path

root = Path(os.environ.get('RIPTOPL_DIR', '.'))
here = Path(__file__).resolve().parent
rd = lambda p: (root / p).read_text(encoding='utf-8').replace('\r\n', '\n')
fail = []


def check(ok, what):
    if not ok:
        fail.append(what)


def fn(src, sig):
    i = src.index(sig)
    return src[i:src.index('\n}\n', i) + 3]


files = rd('src/ripps2files.c')
check('FB_TILE_SEARCH' in files and 'FB_TILE_EXPLOIT' not in files, 'SEARCH has MC EXPLOIT INSTALLER\'s tile')
check('N_("SEARCH")' in files and 'N_("FILES")' in files, 'the tile reads SEARCH FILES')
check('fbRunInstaller' not in files and 'fbFindInstallers' not in files, 'the installer is gone')
walk = fn(files, 'static int fbFindWalk(void)')
check('fbDevCache[i].kind == FB_KIND_DEVICE' in walk and 'strcmp(fbDevCache[i].name, "hdd0:") != 0' in walk,
      'it searches the drives the browser lists, not raw APA partitions')
check(walk.count('opendir(') == 1 and walk.count('closedir(') == 1, 'one folder open at a time')
check('level < FB_FIND_DEPTH' in walk and 'fbFoundCount < FB_FIND_MAX' in walk, 'bounded depth and results')
check('getKeyOn(backKey)' in walk, 'back stops it')
check('fbNameHas(e->d_name, fbFindTerm)' in walk, 'names match what was typed')
res = fn(files, 'static int fbFindResults(void)')
check('fbOpenPath(parent, name);' in res and 'fbGridOpen = 0;' in res, 'a result opens the tree where it is, the cursor on it')
case = files[files.index('case FB_TILE_SEARCH:'):]
check('fbSearch();' in case[:200], 'the tile runs the search')

icons = (here.parent / 'theme' / 'make_grid_icons.py').read_text(encoding='utf-8')
check('ICONS = [browser, editor, orbits, search, power, exitb, hdd]' in icons, 'the atlas draws SEARCH in the fourth cell')
try:
    from PIL import Image
    im = Image.open(here.parent / 'theme' / 'gfx' / 'ripps2_grid_icons.png')
    check(im.mode == 'P' and im.size == (448, 128), 'the atlas is an 8-bit palette PNG, 7 cells of 64')
except ImportError:
    pass

if fail:
    print('build 107 FAILED:')
    for f in fail:
        print(' -', f)
    sys.exit(1)
print('build 107 ok')
