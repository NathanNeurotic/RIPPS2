"""Build 119 (the user, 10/27): the sidebar out of sight on the info page of every theme, Left bringing it out, Circle or
Right putting it away with the page staying, Up / Down stepping the games (info_sidebar=1 keeps it drawn); the ART Pack's flow as the other long jobs have it: the
sizes, the time it should take, RIPPS2's numbered progress bar, and only the drives it fits on; those panels in RIPPS2's
Roboto on every theme.

Static checks on the patched tree."""
import os
import sys
from pathlib import Path
from r2src import unwrap  # noqa: E402

root = Path(os.environ.get('RIPTOPL_DIR', '.'))
rd = lambda p: unwrap((root / p).read_text(encoding='utf-8').replace('\r\n', '\n'))
fail = []


def need(text, items, where):
    for s, why in items:
        if s not in text:
            fail.append('%s: %s' % (where, why))


def body(text, head):
    i = text.index(head)
    return text[i:text.index('\n}\n', i) + 3]


# ---- the info page
th = rd('src/themes.c')
need(th, (('newT->infoSidebar = configGetInt(themeConfig, "info_sidebar", &intValue) && intValue == 1;',
           'info_sidebar, off unless a theme asks for it'),), 'themes.c')
for cfg in ('misc/theme_ripgrid.cfg', 'misc/theme_coverflow.cfg', 'misc/conf_theme_OPL.cfg'):
    if 'info_sidebar=1' in rd(cfg):
        fail.append('%s: no built-in theme keeps the sidebar on its info page' % cfg)
menu = rd('src/menusys.c')
need(menu, (('return menuInfoSidebarReach() && gTheme != NULL && gTheme->infoSidebar;', 'drawn all the time only with info_sidebar=1'),
            ('return ripps2SidebarOn() && !ripps2Legacy();', 'brought out on every theme with the sidebar on')), 'menusys.c')
info = body(menu, 'void menuRenderInfo(void)')
if 'if (menuInfoSidebar() || (menuInfoSidebarReach() && ripps2SidebarFocused()))\n        ripps2SidebarRender();' not in info:
    fail.append('menuRenderInfo: the sidebar out of sight on the info page until it is brought out')
inp = body(menu, 'void menuHandleInputInfo()')
if 'if (menuInfoSidebarReach()) {' not in inp or 'ripps2SidebarOpen(0);' not in inp or 'ripps2SidebarInput();' not in inp:
    fail.append('menuHandleInputInfo: Left brings it out, its own Circle and Right put it away (the page stays)')
if 'if (menuInfoSidebar() &&' not in rd('src/gui.c'):
    fail.append('gui.c: the sidebar stays through the page morph only when the info page keeps it')

# ---- the ART Pack's flow
ap = rd('src/ripps2artpack.c')
need(ap, (('apSrc[s].bytes += st.st_size;', 'each picture sized as it is listed'),
          ('if (apSrc[i].freeBytes < need || (vol.fsType != RIPPS2_FS_EXFAT && need > 0xFFFFFFFFLL))', 'only where it fits (FAT: under 4 GB)'),
          ('if (apSrc[i].fits)\n                order[n++] = i;', 'drives it does not fit on are not offered'),
          ('No started drive has room for the ART Pack: it needs about %s.', 'and says so when none has room'),
          ('ripps2AskHold("ART PACK", pack, info, when,', "the long jobs' panel, SELECT held"),
          ('"Pictures: %d (%s). ART folders: %d."', 'the sizes on it'),
          ('return (int)(s + (double)apTotal / 1024.0 / apWriteKbs(apSrc[target].root) + 0.5);', 'how long: read as measured, written as the drive takes'),
          ('ripps2DrawProgress("PACKING THE ART", pack, done, apTotal, left, 1);', "RIPPS2's numbered progress bar"),
          ('snprintf(left, sizeof(left), "PICTURE %d OF %d", n, total);', 'which picture of how many'),
          ('"Stop? The unfinished pack is removed; the ART folders stay as they are."', 'the back key asks before it stops')), 'ripps2artpack.c')
gm = rd('src/ripps2games.c')
ask, bar = body(gm, 'int ripps2AskHold('), body(gm, 'void ripps2DrawProgress(')
if 'gTheme->fonts[' in ask or 'gTheme->fonts[' in bar:
    fail.append("ripps2games.c: the long jobs' panel and bar in RIPPS2's Roboto, not the theme's display face")
need(gm, (('int ripps2AskHold(const char *head, const char *name, const char *info, const char *when, const char *note)', 'the panel shared'),
          ('return ripps2AskHold(head, name, info, when, "Experimental: OPL core only (not Neutrino)");', 'ZSO keeps its note'),
          ('void ripps2SizeText(long long bytes, char *out, int size)', 'the sizes shared')), 'ripps2games.c')

if fail:
    print('\n'.join(fail))
    sys.exit(1)
print('build119: the sidebar on the info page only where it has room; the ART Pack sized, timed, numbered and offered only where it fits OK')
