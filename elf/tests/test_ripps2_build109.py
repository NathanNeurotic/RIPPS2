"""Build 109: testers' reports of 10/19-10/20. MMCE boots fast (the card's last game list, kept on the card, shows at
once and the card is read again in the background, pausing between games so the pads keep working: 180 games took
about 5 minutes with nothing to press). Settings > General > Save Settings To (Memory Card, Internal HDD, Custom
Path), each choice with its hint. A page's title stands clear of the line under it.

Static checks on the patched tree."""
import os
import re
import sys
from pathlib import Path

root = Path(os.environ.get('RIPTOPL_DIR', '.'))
rd = lambda p: (root / p).read_text(encoding='utf-8')
dia, sb, mmce = rd('src/dia.c'), rd('src/supportbase.c'), rd('src/mmcesupport.c')
ui, gui, dialogs, dialogsh, base = rd('src/ripps2ui.c'), rd('src/gui.c'), rd('src/dialogs.c'), rd('include/dialogs.h'), rd('lng_tmpl/_base.yml')
fail = []

# ---- a page's title, clear of the line under it
if '#define DIA_HEADER_GAP' not in dia or 'h += DIA_HEADER_GAP;' not in dia or '*h = spacingH + DIA_HEADER_GAP;' not in dia:
    fail.append("a page's title row must be taller by DIA_HEADER_GAP in both the layout and the drawing")

# ---- MMCE: the scan breathes for the pads
m = re.search(r'static void sbPadBreath\(const char \*path, int us\)\n\{(.*?)\n\}', sb, re.S)
if not m or 'strncmp(path, "mmce", 4)' not in m.group(1) or 'DelayThread(us)' not in m.group(1):
    fail.append('sbPadBreath must pause only an MMCE scan')
scan = sb[sb.index('static int scanForISO('):sb.index('int sbReadList(')]
if 'sbPadBreath(path, 1000);' not in scan or 'sbPadBreath(path, 17000);' not in scan:
    fail.append('scanForISO must pause after each entry and a frame after each disc read')
if scan.index('sbPadBreath(path, 17000);') < scan.index('fileXioUmount("iso:");\n                sbPadBreath'):
    fail.append('the frame pause comes after the disc is unmounted')

# ---- MMCE: the card's last list
for need, why in (('#define MMCE_LIST_FILE  "RIPPS2.LST"', 'the list is kept on the card as RIPPS2.LST'),
                  ('static int mmceListLoad(void)', 'the card list is loaded at boot'),
                  ('static void mmceListSave(void)', 'the card list is saved after the card was read'),
                  ('if (sum == mmceListSum)', 'an unchanged list is not written again'),
                  ('h.itemSize == (int)sizeof(base_game_info_t)', 'a list written by another build (another entry size) is not used'),
                  ('if (atRoot && !mmceListTried)', 'the list is looked for once a card, at the device root'),
                  ('if (mmceListShown) { // build 109', 'a list shown from the card is read again once, in the background'),
                  ('mmceListTried = mmceListShown = 0;', 'a card taken out has its list looked for again on the next card')):
    if need not in mmce:
        fail.append('mmcesupport.c: ' + why)
upd = mmce[mmce.index('static int mmceUpdateGameList('):mmce.index('static int mmceGetGameCount(')]
if upd.index('mmceListLoad()') > upd.index('sbReadList(&mmceGames'):
    fail.append('the card list comes before the scan')

# ---- Save Settings To
if 'UICFG_RIPPS2_SETTINGS_HOME' not in dialogsh or 'CFG_LBL_CUSTOMCFGPATH' not in dialogsh:
    fail.append('dialog ids for Save Settings To and the Custom Settings Path label')
if '{UI_ENUM, UICFG_RIPPS2_SETTINGS_HOME, 1, 1, _STR_HINT_RIPPS2_SETTINGS_HOME' not in dialogs or \
        '{UI_LABEL, CFG_LBL_CUSTOMCFGPATH, 1, 1, -1, -40, 0, {.label = {NULL, _STR_CUSTOM_SETTINGS_PATH}}}' not in dialogs:
    fail.append('the General page must have Save Settings To above the Custom Settings Path row')
if dialogs.index('UICFG_RIPPS2_SETTINGS_HOME') > dialogs.index('CFG_LBL_CUSTOMCFGPATH'):
    fail.append('Save Settings To sits above the Custom Settings Path')
for label in ('RIPPS2_SETTINGS_HOME', 'HINT_RIPPS2_SETTINGS_HOME'):
    if '- label: %s\n' % label not in base:
        fail.append('lng_tmpl/_base.yml needs %s' % label)
for need, why in (('snprintf(out, size, "mass%d:/RIPPS2", i);', 'the internal exFAT HDD (BDM ATA) is the first choice for Internal HDD'),
                  ('snprintf(out, size, "pfs:/RIPPS2");', "else the APA HDD's OPL partition"),
                  ('diaSetEnumHints(ui, UICFG_RIPPS2_SETTINGS_HOME, ripps2HomeHints);', 'every choice has its hint'),
                  ('gCustomSettingsPath[0] = \'\\0\';', 'Memory Card clears the Custom Settings Path (the card first, as before)'),
                  ('NO INTERNAL HDD FOUND: SETTINGS STAY WHERE THEY ARE', 'no internal HDD: say so, change nothing')):
    if need not in ui:
        fail.append('ripps2ui.c: ' + why)
if gui.count('ripps2SettingsHomeBegin(') != 2 or gui.count('ripps2SettingsHomeEnd(') != 2 or gui.count('ripps2SettingsHomeShow(') != 2:
    fail.append('both General editors (and their updaters) must run Save Settings To')
for ed in ('diaConfig', 'ui'):
    a = gui.index('diaGetString(%s, CFG_CUSTOMCFGPATH, gCustomSettingsPath' % ed)
    if gui.index('ripps2SettingsHomeEnd(%s)' % ed, a) - a > 200:
        fail.append('Save Settings To is applied right after the path is read back (%s)' % ed)

print('\n'.join(fail) or 'build109: page titles clear of their line, MMCE scan pauses for the pads, the MMCE card list, Save Settings To OK')
sys.exit(1 if fail else 0)
