"""Build 122 (the user, 10/28): the default theme and RIPGRID show no disc on their main page, so the game's disc spins
in as it launches there too, as on RIPFLOW. Bringing audio up right after _loadConfig was tried in this build and gave
the boot sound no sooner in the lab (3.90 s after the sky either way), so audio still comes up at the end of init.

Static checks on the patched tree."""
import os
import sys
from pathlib import Path
from r2src import unwrap  # noqa: E402

root = Path(os.environ.get('RIPTOPL_DIR', '.'))
rd = lambda p: unwrap((root / p).read_text(encoding='utf-8').replace('\r\n', '\n'))
fail = []


def body(text, head):
    i = text.index(head)
    return text[i:text.index('\n}\n', i) + 3]


for cfg in ('misc/conf_theme_OPL.cfg', 'misc/theme_ripgrid.cfg', 'misc/theme_coverflow.cfg'):
    if 'launch_disc=spin' not in (root / cfg).read_text(encoding='utf-8').splitlines():
        fail.append(cfg + ': launch_disc=spin (no disc on the main page, so it spins in at a launch)')

opl = rd('src/opl.c')
init = body(opl, 'static void init(void)')
if init.count('sfxBootStart();') != 1 or init.find('sfxBootStart();') < init.find('lngAddHomeLanguages();'):
    fail.append('init: audio up once, at its end (moving it earlier gained nothing)')

if fail:
    print('\n'.join(fail))
    sys.exit(1)
print('build 122: ok')
