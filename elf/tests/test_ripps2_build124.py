"""Build 124 (the user, 10/28): Screen's position (H-POS, V-POS, Overscan) kept for each video mode, the three hints
ending with the same note; and a test build's watchdog (RIPPS2_HANG_WATCH) for the full-library freeze.

Static checks on the patched tree."""
import os
import sys
from pathlib import Path
from r2src import unwrap  # noqa: E402

root = Path(os.environ.get('RIPTOPL_DIR', '.'))
rd = lambda p: unwrap((root / p).read_text(encoding='utf-8').replace('\r\n', '\n'))
fail = []

opl = rd('src/opl.c')
for want in ('void ripps2PosRecall(int vmode)', 'void ripps2PosStore(int vmode)', '"xoff_%d"', '"yoff_%d"', '"overscan_%d"',
             'ripps2PosRecall(gVMode);', 'ripps2PosStore(gVMode); // build 124: the mode in use keeps what it shows now'):
    if want not in opl:
        fail.append('opl.c: ' + want)
# the shared keys are still written, so an older build and BIBLE's early read see the mode in use's position
if 'configSetInt(configOPL, CONFIG_OPL_XOFF, gXOff);' not in opl:
    fail.append('opl.c: xoff still written')

gui = rd('src/gui.c')
if 'if (gVMode != keepVMode && gXOff == keepX && gYOff == keepY && gOverscan == keepOver)\n        ripps2PosRecall(gVMode);' not in gui:
    fail.append('gui.c: a new mode alone brings back its own position')
if 'gXOff = keepX; // build 124: and its position with it' not in gui:
    fail.append('gui.c: a refused mode puts its position back')

base = (root / 'lng_tmpl' / '_base.yml').read_text(encoding='utf-8')
for k in ('HINT_XOFF', 'HINT_YOFF', 'HINT_MENU_OVERSCAN'):
    i = base.index('- label: %s\n' % k)
    if 'Kept for each video mode."' not in base[i:base.index('\n', base.index('string:', i))]:
        fail.append(k + ': ends with the same note')

mk = (root / 'Makefile').read_text(encoding='utf-8')
if 'ifeq ($(RIPPS2_HANG_WATCH),1)' not in mk or '#ifdef RIPPS2_HANG_WATCH\n    hangWatchStart();' not in opl:
    fail.append('the hang watchdog: test builds only')

if fail:
    print('\n'.join(fail))
    sys.exit(1)
print('build 124: ok')
