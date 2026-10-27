"""Build 119 (the user, 10/27): the sidebar off the info page of a theme whose info page has no room for it (RIPPS2's own,
the themes made for OPL), kept where it has (Adapt, RIPGRID: info_sidebar); the ART Pack's flow as the other long jobs
have it: the sizes, the time it should take, RIPPS2's numbered progress bar, and only the drives it fits on.

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
need(th, (('newT->infoSidebar = configGetInt(themeConfig, "info_sidebar", &intValue) ? intValue == 1 : newT->catSidebar;',
           'info_sidebar, by default where the theme puts its categories in the sidebar itself (Adapt)'),), 'themes.c')
if 'info_sidebar=1' not in rd('misc/theme_ripgrid.cfg'):
    fail.append('theme_ripgrid.cfg: RIPGRID keeps the sidebar on its info page')
menu = rd('src/menusys.c')
need(menu, (('return ripps2SidebarOn() && !ripps2Legacy() && gTheme != NULL && gTheme->infoSidebar;', 'the rule'),), 'menusys.c')
info = body(menu, 'void menuRenderInfo(void)')
if 'if (menuInfoSidebar())\n        ripps2SidebarRender();' not in info:
    fail.append('menuRenderInfo: the sidebar drawn only where the info page has room')
inp = body(menu, 'void menuHandleInputInfo()')
if not inp.lstrip('void menuHandleInputInfo()\n{').count('if (menuInfoSidebar()) {'):
    fail.append('menuHandleInputInfo: Left opens the sidebar only where it is drawn (else Left / Right step the games)')
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
need(gm, (('int ripps2AskHold(const char *head, const char *name, const char *info, const char *when, const char *note)', 'the panel shared'),
          ('return ripps2AskHold(head, name, info, when, "Experimental: OPL core only (not Neutrino)");', 'ZSO keeps its note'),
          ('void ripps2SizeText(long long bytes, char *out, int size)', 'the sizes shared')), 'ripps2games.c')

if fail:
    print('\n'.join(fail))
    sys.exit(1)
print('build119: the sidebar on the info page only where it has room; the ART Pack sized, timed, numbered and offered only where it fits OK')
