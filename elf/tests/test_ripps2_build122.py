"""Build 122 (the user, 10/28): the default theme and RIPGRID show no disc on their main page, so the game's disc spins
in as it launches there; a new Launch Disc, Zoom, is RIPFLOW's (and Adapt's); a theme without the key pops it in. Bringing audio up right after _loadConfig was tried in this build and gave
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


for cfg, want in (('misc/conf_theme_OPL.cfg', 'spin'), ('misc/theme_ripgrid.cfg', 'spin'), ('misc/theme_coverflow.cfg', 'zoom')):
    if 'launch_disc=' + want not in (root / cfg).read_text(encoding='utf-8').splitlines():
        fail.append(cfg + ': launch_disc=' + want)

# Zoom (the user, 10/28): Pop In's arrival, then an eased zoom held to the end; a theme without the key pops the disc in
thm = rd('src/themes.c')
if 'newT->launchDiscDef = 1;' not in thm or '"zoom") ? 3' not in thm or '"off") ? 0' not in thm:
    fail.append('themes.c: launch_disc=zoom (3) and off (0); no key: Pop In (1)')
if '"Spin", "Zoom", NULL' not in rd('src/gui.c'):
    fail.append('gui.c: Zoom after Spin, so saved choices keep their numbers')
if '"ripps2_launch_disc", &value) && value >= 0 && value <= 4' not in rd('src/opl.c'):
    fail.append('opl.c: the saved Launch Disc takes 0..4')
ui = rd('src/ripps2ui.c')
if 'gRipps2LaunchDisc <= 4' not in ui or 'launchMode == 3 && t > DISC_ZOOM_AT' not in ui:
    fail.append('ripps2ui.c: Zoom drawn after the arrival, and chosen in Flow and Grid')

opl = rd('src/opl.c')
init = body(opl, 'static void init(void)')
if init.count('sfxBootStart();') != 1 or init.find('sfxBootStart();') < init.find('lngAddHomeLanguages();'):
    fail.append('init: audio up once, at its end (moving it earlier gained nothing)')

if fail:
    print('\n'.join(fail))
    sys.exit(1)
print('build 122: ok')
