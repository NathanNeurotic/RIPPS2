"""Build 96: settings and menus. Backing out of a submenu lands on the row that opened it; Colors and More gets a
Theme value on its RIPPS2 rows, a tooltip on every row and a frosted backdrop shaded by the Color Theme; the flow's
rows say Flow; STATUS scrolls; About drops the financial support line; the Neutrino arguments page explains every
row; settings pages read in Adapt's plain faces on every theme; Default Menu > Last Used; Page Buttons.

Static checks on the patched tree."""
import os
import re
import sys
from pathlib import Path

root = Path(os.environ.get('RIPTOPL_DIR', '.'))
rd = lambda p: (root / p).read_text(encoding='utf-8')
dia, dlg, gui, lng = rd('src/dia.c'), rd('src/dialogs.c'), rd('src/gui.c'), rd('lng_tmpl/_base.yml')
fail = []

# focus back on the button that opened a submenu, one memory per page
if 'diaReturnRemember(ui, cur->id)' not in dia or 'diaReturnSlot(ui)' not in dia:
    fail.append('a page shown again after one of its buttons must land on that button')

# Colors and More
if '"Theme", "Hidden", "Shown"' not in gui or 'gRipps2UserSet &= ~bit;' not in gui:
    fail.append('the RIPPS2 rows of Colors and More must offer Theme, which gives a row back to the theme')
block = dlg[dlg.index('struct UIItem diaColorsConfig[]'):]
block = block[:block.index('{UI_TERMINATOR}')]
untipped = re.findall(r'\{UI_(?:ENUM|INT|BOOL|COLOUR|BUTTON), (\w+), 1, 1, -1,', block)
if untipped:
    fail.append('every Colors and More row needs a tooltip: %s' % ', '.join(untipped))
if 'mod = GS_SETREG_RGBA(0x6C, 0x74, 0x8C' not in rd('src/ripps2ui.c'):
    fail.append('the Color Theme must shade the frosted backdrop')

# labels and descriptions
for label, text in (('COVERFLOW_COUNT', 'Flow Cover Count'), ('COVERFLOW_SCALE', 'Flow Cover Size')):
    if not re.search(r'label: %s\s+string: %s' % (label, text), lng):
        fail.append('%s must read "%s"' % (label, text))
nb = dlg[dlg.index('struct UIItem diaNeutrinoArgs[]'):]
nb = nb[:nb.index('{UI_TERMINATOR}')]
if re.findall(r'\{UI_(?:BOOL|STRING), NARGS_\w+, 1, 1, -1,', nb):
    fail.append('every Neutrino argument row needs its description')
if 'FINANCIAL SUPPORT' in rd('src/ripps2about.c'):
    fail.append('About must not carry the financial support line')
st = rd('src/ripps2status.c')
if 'padGetRightStick(&sx, &sy)' not in st or 'a scroll bar when the page runs past the screen' not in st:
    fail.append('STATUS must scroll with the right stick and show a scroll bar')

# settings faces
if 'RIPPS2_UI_FONT' in dia or 'builtin:ripflowbold", 19' not in rd('src/themes.c'):
    fail.append('settings pages must draw in the built-in Roboto faces on every theme')

# Last Used and Page Buttons
if '_STR_RIPPS2_LAST_USED' not in gui or 'gRipps2StartLast && gRipps2LastDevice' not in rd('src/opl.c'):
    fail.append('Default Menu must offer Last Used and the boot must open that page')
if 'ripps2_last_device' not in rd('src/opl.c') or 'gRipps2StartLast && gBDMStartMode == START_MODE_MANUAL' not in rd('src/bdmsupport.c'):
    fail.append('Last Used must be remembered and start its drive')
if 'CFG_RIPPS2_PAGE_BUTTONS' not in dlg or 'page_buttons' not in rd('src/themes.c') or 'ripps2PageButtons()' not in rd('src/menusys.c'):
    fail.append('Page Buttons must exist as a setting, a theme key, and on the game list')
if 'page_buttons=l2r2' not in rd('misc/theme_ripgrid.cfg'):
    fail.append('the built-in RIPgrid must turn its pages on L2 / R2')

print('\n'.join(fail) or 'build96: focus memory, Colors and More Theme + tooltips, Flow labels, STATUS scroll, Neutrino help, plain settings faces, Last Used, Page Buttons OK')
sys.exit(1 if fail else 0)
