"""Build 97: Grid and Flow. The case flip on a 0.42 s hold of the right stick, on RIPFLOW's centre cover too; the
Grid turns its page at a row's edge instead of wrapping; RIPGRID centred on the screen with its name in RIPPS2 Sleek
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
if 'gridFlipUpdate(' not in cf or ('ripps2TiltBeginTurn(posX, posY, 0,' not in cf and 'ripps2TiltBeginTurn(posX, posY, cfTilt ? elem->tiltScale : 0,' not in cf and
                                   'ripps2TiltBeginFlow(posX, posY, cfTilt && elem->tilt ? elem->tiltScale : 0,' not in cf) or 'texture = cfBack;' not in cf:  # build 117: flowtilt
    fail.append("RIPFLOW's centre cover must turn over to its back cover")
init = thm[thm.index('static void initCoverflow('):]
init = init[:init.index('\n}\n')]
if 'initGridBack(' not in init or 'elem->endElem = &endGrid;' not in init:
    fail.append("the coverflow must get back covers, and let them go with the theme")
if 'static int menuGridEdge(int dir)' not in menu or 'if (!menuGridEdge(1))' not in menu or 'if (!menuGridEdge(-1))' not in menu:
    fail.append("the Grid must turn its page at a row's edge")

dl = thm[thm.index('static void drawItemsList('):]
dl = dl[:dl.index('\n}\n')]
if 'while (rows < itemsList->displayedItems && ps->prev != NULL)' not in dl or 'menu->item->pagestart = ps;' not in dl:
    fail.append('a list page must be full: rows come down from above when the end of the list is short')

# fntFitString on the host: it never reads or writes past the string's terminator
import shutil, subprocess, tempfile
fnt = rd('src/fntsys.c')
fit = fnt[fnt.index('void fntFitString(int id, char *string, size_t width)'):]
fit = fit[:fit.index('\n}\n') + 3]
cc = shutil.which('gcc') or shutil.which('cc')
if 'if (osp == \'\\0\')\n            break;' not in fit.replace('\r\n', '\n'):
    fail.append('fntFitString must stop at the end of the string')
elif cc:
    prog = r"""
#include <stdio.h>
#include <string.h>
#define rmScaleX(x) (x)
static size_t fntCalcDimensions(int id, const char *s) { (void)id; return strlen(s) * 10; }
""" + fit + r"""
static int check(const char *text, size_t width, const char *want)
{
    char buf[64];
    memset(buf, 'X', sizeof(buf));
    buf[sizeof(buf) - 1] = '\0';
    memcpy(buf, text, strlen(text) + 1);
    fntFitString(0, buf, width);
    if (strcmp(buf, want) != 0) { printf("'%s' at %u: got '%s', want '%s'\n", text, (unsigned)width, buf, want); return 1; }
    for (size_t i = strlen(text) + 1; i < sizeof(buf) - 1; i++)
        if (buf[i] != 'X') { printf("'%s' at %u: wrote past the end at %u\n", text, (unsigned)width, (unsigned)i); return 1; }
    return 0;
}
int main(void)
{
    int bad = 0;
    bad |= check("TEST GAME", 200, "TEST GAME");
    bad |= check("TEST GAME", 60, "TEST\nGAME");
    bad |= check("TEST GAME", 30, "TEST\nGAME");
    bad |= check("SUPERCALIFRAGILISTIC", 50, "SUPERCALIFRAGILISTIC");
    bad |= check("A VERYLONGWORD B", 40, "A\nVERYLONGWORD\nB");
    bad |= check("ONE TWO THREE", 75, "ONE TWO\nTHREE");
    return bad;
}
"""
    with tempfile.TemporaryDirectory() as td:
        open(td + '/f.c', 'w').write(prog)
        r = subprocess.run([cc, td + '/f.c', '-o', td + '/f.exe'], capture_output=True, text=True)
        if r.returncode:
            fail.append('fntFitString host build: ' + r.stderr[-300:])
        else:
            r = subprocess.run([td + '/f.exe'], capture_output=True, text=True)
            if r.returncode:
                fail.append('fntFitString: ' + r.stdout.strip())

# padSetActAlign is a blocking RPC: only to a pad that is stable with nothing in flight (the 720p freeze)
pad = rd('src/pad.c')
calls = pad.count('padSetActAlign(pad->port, pad->slot, pad->actAlign)')
guarded = pad.count('padIdleForCommand(pad) ? padSetActAlign(') + pad.count('padIdleForCommand(pad) && padSetActAlign(')
if 'static int padIdleForCommand(struct pad_data_t *pad)' not in pad or 'padGetReqState(pad->port, pad->slot) != PAD_RSTAT_BUSY' not in pad:
    fail.append('padIdleForCommand must read the pad state and its request state fresh')
elif calls == 0 or guarded != calls:
    fail.append('every padSetActAlign must wait for an idle pad (%d of %d guarded)' % (guarded, calls))

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
    fail.append('RIPGRID: centred (x=320), its name in font7')
if 'font7=builtin:ripps2sleekbold' not in rd('misc/theme_ripgrid.cfg'):
    fail.append("RIPGRID's font7 must be RIPPS2 Sleek Bold")
shots = [v for k, v in elems(rd('misc/theme_coverflow.cfg')).items() if k.startswith('info') and v.get('pattern') in ('SCR', 'SCR2', 'SCRn')]  # SCRn from build 108
if len(shots) != 2 or any(v.get('tilt') != '1' for v in shots):
    fail.append("RIPFLOW's info page screenshots must tilt")

print('\n'.join(fail) or 'build97: 0.42 s flip on the Grid and RIPFLOW, page edges, RIPGRID centred with a Sleek Bold title, RIPFLOW tilt, full list pages, fntFitString stops at the end of its string, the pad align waits for an idle pad OK')
sys.exit(1 if fail else 0)
