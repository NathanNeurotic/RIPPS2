"""Build 100: the build 99 notes (user, 10-12). Static checks on the patched tree."""
import os
import sys
from pathlib import Path

root = Path(os.environ.get('RIPTOPL_DIR', '.'))
rd = lambda p: (root / p).read_text(encoding='utf-8').replace('\r\n', '\n')
fail = []

# quick fixes
media, ed, th, menu, gui = rd('src/ripps2media.c'), rd('src/ripps2edit.c'), rd('src/themes.c'), rd('src/menusys.c'), rd('src/gui.c')
if '            yaw += dt * (rx < -24 ? -rx / 127.0f : 1.0f) * 2.5f;' not in media or \
        '            yaw -= dt * (rx > 24 ? rx / 127.0f : 1.0f) * 2.5f;' not in media:
    fail.append('the 3D icon viewer must turn the way pressed')
if '#define ED_FONT RIPPS2_CASE_FONT' not in ed or 'gTheme->fonts[' in ed:
    fail.append('the text editor must draw every word in RIPPS2 Sleek true case')
if 'gridFlips[k].side = gridFlips[k].target ? side : -side;' not in th:
    fail.append('the case flip must turn the way the stick pushes, to the back and home')
if '#define RIPPS2_MENU_FONT RIPPS2_DIA_FONT' not in rd('include/themes.h') or menu.count('RIPPS2_MENU_FONT') < 5 or \
        gui.count('RIPPS2_MENU_FONT') < 6:
    fail.append("the START menu, the Settings hub, its save prompt and the game / app menus must use Adapt's face")

# Memory Files
fb = rd('src/ripps2files.c')
if '(fbReplacing ? O_TRUNC : 0)' not in fb or 'fbNoteFail("CHECK", dst);' not in fb or \
        'if (fbClipReplace[n]) { // build 100: a replace erases the file there first: the music lets it go too' not in fb:
    fail.append('a replace must erase cleanly, let the music go and read the new file back')
if 'fbRunIsoAt(src, e); // build 100: anywhere else, it starts where it sits' not in fb or 'bdmLaunchIsoAt(src, full, startup, dvd, cfg);' not in fb:
    fail.append('an ISO or ZSO must start where it sits, with no move-it message')
sb, bdm = rd('src/supportbase.c'), rd('src/bdmsupport.c')
if 'snprintf(path, 256, "%s", sbPathOverride); // build 100: the file where it sits' not in sb or 'int sbIsoStartup(' not in sb:
    fail.append('the path builder must take the one-shot path, and an image its boot file')
if 'game = &bdmPathGame;' not in bdm or '!bdmPathLaunch && game != NULL && (bdmGetItemView(itemList, id) == LIB_VIEW_PS1)' not in bdm:
    fail.append('the BDM launch must take the path game, never as a PS1 row')
if 'configGetInt(configOPL, "ripps2_vcd_usb", &last);' not in bdm or 'vcdBdmaEnvironmentValid(VCD_BDMA_USBEXFAT))' not in bdm:
    fail.append('a USB PS1 launch must remember the fat32 / exFAT answer while the card still matches it')

if fail:
    print('\n'.join(fail))
    sys.exit(1)
print('build100: viewer turn, editor face, flip direction, menu face, clean replace, ISO where it sits, POPSTARTER answer OK')
