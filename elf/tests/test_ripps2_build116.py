"""Build 116: BOOT LOCK writes the config of the boot loader the console really starts, not only PS2BBL's: FMCB's
LK_Auto_E1 (SYS-CONF/FREEMCB.CNF, FMCB_CFG.CNF for 1.8) and RIPPS2 as OSDMenu's first menu item (SYS-CONF/OSDMENU.CNF).
With the lock on, an empty IGR Path sends a game's EXIT through the browser and that loader (issue #3: a straight load
of RIPPS2's ELF after a game was a black screen), and the lock no longer fills the IGR Path with RIPPS2's own ELF.

Static checks on the patched tree, then the config editor compiled on the PC: a PS2BBL, an FMCB (CRLF) and an OSDMenu
config locked and unlocked again, byte for byte, with RIPPS2's lines where each loader reads them first."""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from r2src import unwrap, TR_STUBS  # noqa: E402

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


boot = rd('src/ripps2boot.c')
need(boot, (('"mc0:/SYS-CONF/FREEMCB.CNF",', "FMCB 1.9's config is one BOOT LOCK edits"),
            ('"mc1:/SYS-CONF/FMCB_CFG.CNF",', "and FMCB 1.8's"),
            ('"mc0:/SYS-CONF/OSDMENU.CNF",', "and OSDMenu's"),
            ('"LK_Auto_E1 = %s%s"', "FMCB's automatic entry in its own spelling"),
            ('"name_OSDSYS_ITEM_%d = RIPPS2%spath1_OSDSYS_ITEM_%d = %s%s"', "RIPPS2 as an OSDMenu item"),
            ('blApplyAll(1, BL_PS2BBL, &changed', "BIBLE's install sets PS2BBL configs only"),
            ('if (!gRipps2BootLocked && ripps2BootLockIgrPath(buf, size))', 'with the lock on, an empty IGR Path is the browser, then the loader'),
            ('blDialect(blConfigs[i2]) == BL_PS2BBL && blRead(blConfigs[i2]) >= 0 && blIsExtended(', "BIBLE's MMCE offer reads PS2BBL Extended's config, not OSDMenu's")),
     'ripps2boot.c')
check = body(boot, 'void ripps2ExitPathCheck(void)')
if 'stat(gExitPath' in check or '!blFileExists(gExitPath)' not in check:
    fail.append('ripps2ExitPathCheck: a memory card IGR Path is opened to be sure (stat() on mc says yes for a missing file)')
path_in = body(boot, 'static int blPathIn(')
if 'return dialect == BL_OSDMENU || !strncmp(out, "mc?:", 4) || !strncmp(out, "mass:", 5);' not in path_in:
    fail.append('blPathIn: FMCB is given memory card and USB paths only')
apply = body(boot, 'void ripps2BootLockApply(int on)')
if 'BOOT LOCK works only through PS2BBL' in apply or 'kind == BL_OTHER' not in apply:
    fail.append('ripps2BootLockApply: FMCB and OSDMenu are set, BIBLE is offered only for a loader RIPPS2 cannot set')
state = body(boot, 'int ripps2BootLockState(void)')
if 'blDialect(blConfigs[i]) == kind' not in state or 'blSetLocked(locked);' not in state:
    fail.append('ripps2BootLockState: the lock counts in the starting loader\'s own config, and is kept for EXIT')
gui = rd('src/gui.c')
if 'guiBootLockAutofill' in gui or 'ripps2BootLockIgrPath(gExitPath' in gui:
    fail.append('gui.c: turning the lock on no longer fills the IGR Path with RIPPS2\'s own ELF')
opl = rd('src/opl.c')
if opl.count('configGetInt(configOPL, "ripps2_bootlock", &gRipps2BootLocked);') != 2 or 'configSetInt(configOPL, "ripps2_bootlock", gRipps2BootLocked);' not in opl:
    fail.append('opl.c: ripps2_bootlock is read on both load paths (the menu and a launch from argv) and saved')
base = rd('lng_tmpl/_base.yml')
need(base, (('Best left empty with BOOT LOCK on (PS2BBL, FMCB or OSDMenu', 'the IGR Path hint says what an empty one does now'),
            ('PS2BBL and FMCB start it at once, OSDMenu puts it first in its menu', "BOOT LOCK's hint names the loaders")), '_base.yml')

# ---- Manual pages show their saved games; a launch starts only the game's drive; an empty pass is no answer
mix = rd('src/mixsupport.c')
need(mix, (('item_list_t *mixPageObject(int mode)', 'a drive page on Manual has a list of its saved games'),
           ('if (page >= 0 && mixFamilyMode(m->family) != pageMode)', "a drive page's list holds only its own drive's games"),
           ('if (save && !settling && !recent && page < 0)', 'only All Games writes the master list'),
           ('int fam = count > 0 ? mixModeFamily(mode) : -1, k;', 'an empty pass is no answer'),
           ('ripps2StartSourceMode(mixFamilyMode(fam));', "Cross on a waiting row starts only the game's drive")), 'mixsupport.c')
wait = body(mix, 'int mixWaitForRow(struct menu_item *menu)')
if 'ripps2StartSources();' in wait:
    fail.append('mixWaitForRow: every source started for one game (build 115)')
need(opl, (('static void pageCacheBuild(opl_io_module_t *mdl)', 'a Manual page builds its saved games'),
           ('ioPutRequest(IO_CUSTOM_SIMPLEACTION, &pageCacheAll);', 'at boot and on every Game Sources change'),
           ('if (shown != mdl->support && !mdl->support->enabled)\n        return;', 'the saved games stay until the drive is started'),
           ('support = curMenu->userdata; // build 116', 'a launch reads the page again after the wait')), 'opl.c')
need(rd('src/hddsupport.c'), (('nonSony == HDD_PROBE_READ_FAILED && tries < 6', 'a cold HDD is asked again before "not detected"'),), 'hddsupport.c')
need(rd('src/menusys.c'), (('return menuListMode(support);', 'a page of saved games is still its drive to the sidebar and Last Device'),), 'menusys.c')

# ---- compiled: lock, then unlock, in each loader's own config
cc = shutil.which('gcc') or shutil.which('cc')
if cc is None:
    print('build116: no host C compiler, the compiled checks are skipped')
else:
    raw = (root / 'src/ripps2boot.c').read_text(encoding='utf-8').replace('\r\n', '\n')
    pick = ''.join(body(raw, h) for h in ('static int blDialect(', 'static void blKey(', 'static int blTaken(', 'static int blOurs(',
                                          'static int blOsdFreeItem(', 'static int blUnlocked(', 'static int blLocked('))
    harness = r'''
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <strings.h>
#define BL_MAX    32768
#define BL_MARKER "#RIPPS2 BOOT LOCK"
#define BL_KEPT   "#RIPPS2# "
enum { BL_NONE = 0, BL_PS2BBL, BL_FMCB, BL_OSDMENU, BL_OTHER };
static char blText[BL_MAX + 1], blOut[BL_MAX + 512];
''' + TR_STUBS + pick + r'''
static int put(const char *path, const char *text, int len)
{
    FILE *f = fopen(path, "wb");
    if (f == NULL)
        return 1;
    fwrite(text, 1, len, f);
    fclose(f);
    return 0;
}

/* argv: the config's card path (its dialect), the file, RIPPS2's path, then where the locked, relocked and unlocked files go */
int main(int argc, char **argv)
{
    FILE *f = fopen(argv[2], "rb");
    int n, len, d = blDialect(argv[1]);
    char locked[BL_MAX + 512];
    if (argc < 7 || f == NULL)
        return 2;
    n = fread(blText, 1, BL_MAX, f);
    fclose(f);
    blText[n] = '\0';
    len = blUnlocked(blText);
    memcpy(blText, blOut, len + 1);
    if ((len = blLocked(blText, argv[3], d)) < 0)
        return 3;
    memcpy(locked, blOut, len + 1);
    put(argv[4], locked, len);
    memcpy(blText, locked, len + 1); /* locked again, as BOOT LOCK on twice does: unlocked first */
    len = blUnlocked(blText);
    memcpy(blText, blOut, len + 1);
    len = blLocked(blText, argv[3], d);
    put(argv[5], blOut, len);
    memcpy(blText, locked, strlen(locked) + 1);
    len = blUnlocked(blText);
    put(argv[6], blOut, len);
    printf("%d\n", d);
    return 0;
}
'''
    ps2bbl = ('# PlayStation2 Basic BootLoader config file\n'
              'SKIP_PS2LOGO = 0\nKEY_READ_WAIT_TIME = 4000\n\n'
              'NAME_AUTO = wLaunchELF\nLK_AUTO_E1 = mc?:/BOOT/BOOT.ELF\nLK_AUTO_E2 = $OSDSYS\n\n'
              'LK_START_E1 = $OSDSYS\nLK_CROSS_E1 = $CDVD\n')
    fmcb = ('CNF_version = 1\nDebug_Screen = 0\npad_delay = 1000\n'
            'LK_Auto_E1 = OSDSYS\nLK_Auto_E2 = mc?:/BOOT/BOOT.ELF\nLK_Auto_E3 = \n'
            'LK_R1_E1 = mc?:/APPS/ULE.ELF\nLK_R1_E2 = \n'
            'name_OSDSYS_ITEM_1 = uLaunchELF\npath1_OSDSYS_ITEM_1 = mc?:/BOOT/BOOT.ELF\n').replace('\n', '\r\n')
    osdm = ('OSDSYS_video_mode = AUTO\nOSDSYS_scroll_menu = 1\nOSDSYS_menu_x = 320\n'
            'name_OSDSYS_ITEM_1 = wLaunchELF\npath1_OSDSYS_ITEM_1 = mmce?:/APPS/WLE.ELF\n'
            'name_OSDSYS_ITEM_2 = OPL\npath1_OSDSYS_ITEM_2 = mc?:/APPS/OPNPS2LD.ELF\npath2_OSDSYS_ITEM_2 = mass:/APPS/OPNPS2LD.ELF\n'
            'name_OSDSYS_ITEM_4 = Neutrino\npath1_OSDSYS_ITEM_4 = mmce?:/neutrino/nhddl.elf\n')
    osdm_empty = 'OSDSYS_video_mode = AUTO\n'
    cases = (
        ('PS2BBL', 'mc0:/PS2BBL/CONFIG.INI', ps2bbl, 'mc?:/RIPPS2/RIPPS2.ELF', 1,
         '#RIPPS2 BOOT LOCK: RIPPS2 starts first. Turn BOOT LOCK off in RIPPS2 to bring back the lines marked #RIPPS2#.\n'
         'NAME_AUTO = RIPPS2\nLK_AUTO_E1 = mc?:/RIPPS2/RIPPS2.ELF\n#RIPPS2# NAME_AUTO = wLaunchELF\n#RIPPS2# LK_AUTO_E1 = mc?:/BOOT/BOOT.ELF\nLK_AUTO_E2 = $OSDSYS\n'),
        ('FMCB', 'mc0:/SYS-CONF/FREEMCB.CNF', fmcb, 'mc?:/BOOT/RIPPS2.elf', 2,
         ('pad_delay = 1000\n#RIPPS2 BOOT LOCK: RIPPS2 starts first. Turn BOOT LOCK off in RIPPS2 to bring back the lines marked #RIPPS2#.\n'
          'LK_Auto_E1 = mc?:/BOOT/RIPPS2.elf\n#RIPPS2# LK_Auto_E1 = OSDSYS\nLK_Auto_E2 = mc?:/BOOT/BOOT.ELF\n').replace('\n', '\r\n')),
        ('FMCB 1.8', 'mc1:/SYS-CONF/FMCB_CFG.CNF', fmcb, 'mass:/RIPPS2/RIPPS2.ELF', 2, 'LK_Auto_E1 = mass:/RIPPS2/RIPPS2.ELF\r\n#RIPPS2# LK_Auto_E1 = OSDSYS\r\n'),
        ('OSDMenu', 'mc0:/SYS-CONF/OSDMENU.CNF', osdm, 'mmce?:/RIPPS2/RIPPS2.ELF', 3,
         'OSDSYS_menu_x = 320\n#RIPPS2 BOOT LOCK: RIPPS2 is first in this menu. Turn BOOT LOCK off in RIPPS2 to take it out.\n'
         'name_OSDSYS_ITEM_3 = RIPPS2\npath1_OSDSYS_ITEM_3 = mmce?:/RIPPS2/RIPPS2.ELF\nname_OSDSYS_ITEM_1 = wLaunchELF\n'),
        ('OSDMenu, no items yet', 'mc1:/SYS-CONF/OSDMENU.CNF', osdm_empty, 'usb:/RIPPS2/RIPPS2.ELF', 3,
         'OSDSYS_video_mode = AUTO\n#RIPPS2 BOOT LOCK: RIPPS2 is first in this menu. Turn BOOT LOCK off in RIPPS2 to take it out.\n'
         'name_OSDSYS_ITEM_1 = RIPPS2\npath1_OSDSYS_ITEM_1 = usb:/RIPPS2/RIPPS2.ELF\n'),
    )
    with tempfile.TemporaryDirectory() as tmp:
        src, exe = os.path.join(tmp, 'lock.c'), os.path.join(tmp, 'lock.exe')
        open(src, 'w').write(harness)
        cr = subprocess.run([cc, '-std=gnu99', '-Wall', '-Werror', '-Wno-unused-function', src, '-o', exe], capture_output=True, text=True)
        if cr.returncode != 0:
            fail.append('the config editor does not compile on its own:\n' + cr.stderr[-1500:])
        else:
            for name, cfg, text, ripps2, dialect, want in cases:
                files = [os.path.join(tmp, x) for x in ('in.cfg', 'locked.cfg', 'relocked.cfg', 'unlocked.cfg')]
                open(files[0], 'wb').write(text.encode('ascii'))
                out = subprocess.run([exe, cfg, files[0], ripps2] + files[1:], capture_output=True, text=True)
                if out.returncode != 0 or out.stdout.strip() != str(dialect):
                    fail.append('%s: %s read as dialect %s (exit %d)' % (name, cfg, out.stdout.strip(), out.returncode))
                    continue
                locked, relocked, unlocked = (open(f, 'rb').read().decode('ascii') for f in files[1:])
                if want not in locked:
                    fail.append('%s: the locked config does not read\n%s\n---- it is\n%s' % (name, want, locked))
                if relocked != locked:
                    fail.append('%s: BOOT LOCK on again changes the config' % name)
                if unlocked != text:
                    fail.append('%s: off does not give back the config as it was\n%s' % (name, unlocked))
                if dialect == 3 and '#RIPPS2# ' in locked:
                    fail.append('%s: OSDMenu keeps every item; nothing is commented out' % name)

if fail:
    print('\n'.join(fail))
    sys.exit(1)
print('build116: BOOT LOCK through PS2BBL, FMCB and OSDMenu (locked, locked again and unlocked byte for byte), EXIT through the loader OK')
