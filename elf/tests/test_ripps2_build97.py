"""Build 97: Grid and Flow. The case flip on a 0.42 s hold of the right stick, on RIPFLOW's centre cover too; the
Grid turns its page at a row's edge instead of wrapping; RIPgrid centred on the screen with its name in RIPPS2 Sleek
Bold; RIPFLOW's info page screenshots tilt; every built-in theme cfg parses into the elements its page needs.

Static checks on the patched tree."""
import os
import re
import sys
from pathlib import Path

root = Path(os.environ.get('RIPTOPL_DIR', '.'))
rd = lambda p: (root / p).read_text(encoding='utf-8')
thm, menu = rd('src/themes.c'), rd('src/menusys.c')
fail = []

if '#define FLIP_HOLD_S 0.42f' not in thm:
    fail.append('the case flip must answer a 0.42 s hold')
if 'gridBacks[GRID_BACK_SLOTS]' not in thm or 'for (i = 0; i < 2; i++)\n        if (gridBacks' in thm:
    fail.append('the back covers need a place for every flipping element (GRID_BACK_SLOTS)')
cf = thm[thm.index('static void drawCoverFlow('):thm.index('// Grid (RIPPS2 build 78)')]
if 'gridFlipUpdate(' not in cf or 'ripps2TiltBeginTurn(posX, posY, 0,' not in cf or 'texture = cfBack;' not in cf:
    fail.append("RIPFLOW's centre cover must turn over to its back cover")
init = thm[thm.index('static void initCoverflow('):]
init = init[:init.index('\n}\n')]
if 'initGridBack(' not in init or 'elem->endElem = &endGrid;' not in init:
    fail.append("the coverflow must get back covers, and let them go with the theme")
if 'static int menuGridEdge(int dir)' not in menu or 'if (!menuGridEdge(1))' not in menu or 'if (!menuGridEdge(-1))' not in menu:
    fail.append("the Grid must turn its page at a row's edge")

# the built-in themes: each cfg parses, and its main page has what it needs
def elems(cfg):
    out, cur = {}, None
    for line in cfg.splitlines():
        if re.match(r'^[A-Za-z]\w*:\s*$', line):
            cur = line.strip()[:-1]
            out[cur] = {}
        elif cur and re.match(r'^\t\w+=', line):
            k, v = line.strip().split('=', 1)
            out[cur][k] = v
        elif line.strip() and not line.startswith('#') and not line.startswith('\t') and '=' not in line:
            fail.append('a line that is neither a key nor an element: %r' % line[:60])
    return out

for name, need in (('misc/theme_coverflow.cfg', 'Coverflow'), ('misc/theme_ripgrid.cfg', 'Grid')):
    e = elems(rd(name))
    if not any(v.get('type') == need for k, v in e.items() if k.startswith('main')):
        fail.append('%s must keep a main %s element' % (name, need))
grid = [v for k, v in elems(rd('misc/theme_ripgrid.cfg')).items() if v.get('type') == 'Grid']
if not grid or grid[0].get('x') != '320' or grid[0].get('title_font') != '7':
    fail.append('RIPgrid: centred (x=320), its name in font7')
if 'font7=builtin:ripps2sleekbold' not in rd('misc/theme_ripgrid.cfg'):
    fail.append("RIPgrid's font7 must be RIPPS2 Sleek Bold")
shots = [v for k, v in elems(rd('misc/theme_coverflow.cfg')).items() if k.startswith('info') and v.get('pattern') in ('SCR', 'SCR2')]
if len(shots) != 2 or any(v.get('tilt') != '1' for v in shots):
    fail.append("RIPFLOW's info page screenshots must tilt")

print('\n'.join(fail) or 'build97: 0.42 s flip on the Grid and RIPFLOW, page edges, RIPgrid centred with a Sleek Bold title, RIPFLOW tilt OK')
sys.exit(1 if fail else 0)
