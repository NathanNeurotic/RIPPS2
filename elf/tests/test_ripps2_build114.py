"""Build 114: RiptOPL 57c45b4 merged; the launchers RIPPS2 does not carry, found and remembered (ripps2seance.c); STATUS
with the drives first; All Games from a master list; Hide Game and Hidden Games; Delete with everything of a game
behind the APA table check; Neutrino named beside RiptOPL; one RIPPS2.elf (no lite variant); FreeType with the modules
RIPPS2 reads; the compiled-in fonts stripped.

Static checks on the patched tree, then two pieces compiled on the PC: the APA check against synthetic disks (a good
table, one written from a bigger disk, a partition too big for the disk, one off its alignment, a broken link, a
chain that does not close) and the master list's save and load (a round trip; a damaged or short file is not read)."""
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path
from r2src import unwrap, TR_STUBS  # noqa: E402

root = Path(os.environ.get('RIPTOPL_DIR', '.'))
repo = Path(__file__).resolve().parents[2]
rd = lambda p: unwrap((root / p).read_text(encoding='utf-8').replace('\r\n', '\n'))
raw = lambda p: (root / p).read_text(encoding='utf-8').replace('\r\n', '\n')
fail = []


def need(text, items, where):
    for s, why in items:
        if s not in text:
            fail.append('%s: %s' % (where, why))


def body(text, head):
    i = text.index(head)
    return text[i:text.index('\n}\n', i) + 3]


# ---- the merge
up = (repo / 'elf/RIPTOPL_UPSTREAM').read_text(encoding='utf-8').split()
if up[0] != '57c45b4fcc922ba00fed949c634caea0a2900c63' or up[1] != '4224':
    fail.append('RIPTOPL_UPSTREAM must name rebuild/main 57c45b4 (revision 4224)')
pad = rd('ee_core/src/padhook.c')
thread = pad[pad.index('static void IGR_Thread(void *arg)'):]
need(thread, (('while (Pad_Data.combo_type == 0x00 && !IGR_MenuOpen)', 'the IGR thread waits for the handler\'s latch or the menu'),
              ('choice = IGR_MenuRun(IGR_PadButtons);', 'the in-game menu still runs in it')), 'padhook.c')
if 'IGR_VBLANK_HANDLER' in pad or 'IGR_Poll_Alarm' in pad:
    fail.append('padhook.c: the alarm sampler is gone with upstream (#984): the VBLANK handler in every build')
tex = rd('include/textures.h')
if 'L1_ICON,          // Settings peer-page navigation hint' in tex or 'PSBBN_BACKGROUND' not in tex or 'RIPPS2_SIDEBAR_ICONS' not in tex:
    fail.append('textures.h: one L1/R1, both sides\' entries')
for leg in ('src/bdmsupport.c', 'src/hddsupport.c', 'src/mmcesupport.c', 'src/ethsupport.c', 'src/udpfssupport.c'):
    if 'cueEnsureEmber' in rd(leg):
        fail.append('%s: the launch legs call RiptOPL\'s cueResolveEmber' % leg)

# ---- SEANCE
sh = rd('include/ripps2seance.h')
need(sh, (('int seanceHook(int what, int mode, const char *devPrefix, char *path, int pathSize) __attribute__((weak));',
           'one weak way in, NULL in RiptOPL\'s host harnesses'),), 'ripps2seance.h')
se = rd('src/ripps2seance.c')
need(se, (('launchers.txt', 'remembered beside the settings'),
          ('"usb" : t == BDM_TYPE_ATA ? "ata" : t == BDM_TYPE_SDC ? "mx4sio" : t == BDM_TYPE_ILINK ? "ilink"', 'a drive by its kind, not its slot'),
          ('if (!gSeanceLaunching || what < 0', 'the hook does nothing outside a launch'),
          ('"CD", "DVD", "ART", "CFG", "VMC"', 'the search skips the game and art folders'),
          ('void seancePreLaunch(item_list_t *support, int id)', "Ember's files copied before the launch"),
          ('has[3] || (n >= 6 && !strncasecmp(dir + n - 6, "EMBER/", 6))', 'a bios.bin is Ember\'s only beside ember.elf or in an EMBER folder')), 'ripps2seance.c')
walk = body(se, 'static int seRoots(')
if 'opendir(more[k])' not in walk or 'bdmEnsure' in walk or 'LoadModules' in walk:
    fail.append('seRoots: only drives already started are searched (nothing is loaded to look)')
vcd = rd('src/vcdsupport.c')
res = body(vcd, 'int vcdResolvePopstarter(const char *devPrefix, char *out, int outSize)')
if res.index('vcdResolveCustomPopstarter()') > res.index('SEANCE_MODE_LOOKUP') or res.index('SEANCE_MODE_LOOKUP') > res.index('vcdResolvePopstarterMcElf(out, outSize)'):
    fail.append('POPSTARTER: Settings\' path and the game\'s drive first, then where SEANCE found it, then the cards')
need(vcd, (('seanceHook != NULL && seanceHook(SEANCE_POPS, SEANCE_MODE_LOOKUP', 'RIPPOPS copies from where SEANCE found the POPS files'),
           ('snprintf(src, sizeof(src), "%s%s", from, files[i]); // build 114: from is the folder', 'the copy reads the folder found')), 'vcdsupport.c')
sb = rd('src/supportbase.c')
nr = body(sb, 'const char *sbResolveNeutrinoPath(const char *activePrefix)')
if not (nr.index('sbProbeNeutrinoMc()') < nr.index('SEANCE_MODE_LOOKUP') < nr.index('SEANCE_MODE_LAST') < nr.index('ripps2NeutrinoOffer(')):
    fail.append('Neutrino: the cards, then where SEANCE found one, then the search, and only then RIPPS2\'s copy')
opl = rd('src/opl.c')
need(opl, (('gSeanceLaunching = 1; // build 114', 'a launch is marked for SEANCE'), ('seancePreLaunch(support, launchId);', 'the Ember pre-flight')), 'opl.c')
emb = rd('src/ripps2ember.c')
need(emb, (('install it once, where you pick, and every', 'RIPPS2\'s Neutrino is offered to install once, not more'),), 'ripps2ember.c')
if raw('src/cuesupport.c').count('seanceHook') or 'seanceHook' in body(raw('src/gui.c'), 'void guiMsgBoxMissing('):
    fail.append('cuesupport.c and guiMsgBoxMissing stay RiptOPL\'s (their harnesses copy them word for word)')

# ---- STATUS and Cache
st = rd('src/ripps2status.c')
if st.index('"DRIVES"') > st.index('"LAUNCHERS"') or st.index('"LAUNCHERS"') > st.index('"BIBLE"'):
    fail.append('STATUS: DRIVES first, then LAUNCHERS, then BIBLE')
need(st, (('"Internal HDD (APA): %s free of %s"', 'the APA drive\'s space'), ('"Memory card %d: %d KB free"', 'the cards\' space'),
          ('ACT_START_DRIVES', 'START EVERY DRIVE'), ('ACT_SEANCE_SEARCH', 'LOOK FOR THEM'), ('"only if you have none"', 'the install row says when')), 'ripps2status.c')
if 'aside[96]' not in st:
    fail.append('STATUS: a translated note runs to 73 bytes (Lao, Persian): aside[96]')
dlg = rd('src/dialogs.c')
need(dlg, (('RIPPS2_SEANCE_ROW0', 'Cache > Launchers lines'), ('RIPPS2_SEANCE_BUTTON', 'Look now'), ('RIPPS2_HIDDEN_BUTTON', 'Game Sources > Hidden Games')), 'dialogs.c')

# ---- All Games from the master list
mix = rd('src/mixsupport.c')
need(mix, (('#define MIX_MASTER_FILE  "allgames.bin"', 'the master list beside the settings'),
           ('mixAppend(&b, NULL, -1, -1, m->kind, 100 + m->family, m->text, m->startup, m->family);', 'a waiting row: no owner, ranked after live rows'),
           ('if (!settling)\n        mixMasterSave(b.arr, kept);', 'saved only once no started source is still to answer'),
           ('mixItemList.updateDelay = waiting ? MENU_UPD_DELAY_GENREFRESH : MENU_UPD_DELAY_NOUPDATE;', 'polled only while games wait'),
           ('if (ripps2ShroudHas(mode, 0, name)) // build 114: hidden', 'hidden games never reach the master list')), 'mixsupport.c')
upd = body(mix, 'static int mixUpdateItemList(')
if upd.index('mixMasterSave(') > upd.index('view == LIB_VIEW_PS1'):
    fail.append('mixUpdateItemList: the master list keeps every kind, saved before the view picks its rows')
need(opl, (('mixSourceAnswered(mod->support->mode);', 'a source\'s list replaces its saved games'),
           ('if (support->mode == MIX_MODE && mixIsWaiting(curMenu->current->item.id) && !mixWaitForRow(curMenu))', 'Cross on a waiting row starts and waits')), 'opl.c')

# ---- Hide, Hidden Games, Delete
gm = rd('src/ripps2games.c')
need(gm, (('#define SH_FILE "RIPPS2.HID"', 'the hidden list on the game\'s own drive'),
          ('ioBlockOps(1); // nothing else reads the drive while its table changes', 'nothing reads the drive during a remove'),
          ('if (!ripps2ApaCheck(apaWhy, sizeof(apaWhy))) {', 'the APA table is checked before a partition goes'),
          ('guiMsgBoxStartOption("DELETE FOR GOOD");', 'START is the last word, as the HDD MANAGER asks'),
          ('removeFavouriteByIdAndText(r.mode, r.id, r.name, r.kind);', 'the star goes with the game'),
          ('mc0:/RIPPS2/REMOVED.TXT', 'a receipt')), 'ripps2games.c')
lr = body(gm, 'void ripps2LastRites(item_list_t *support, int id)')
if lr.index('fileXioRemove(lrItems[0].path)') > lr.index('for (i = 1; i < lrCount; i++) {'):
    fail.append('LAST RITES: the image (or partition) first, the extras after')
if "g->partition_name[0] == '_' && g->partition_name[1] == '_'" not in lr or 'gOPLPart' not in lr:
    fail.append('LAST RITES: never a __ partition, never the one RIPPS2 keeps its settings on')
need(rd('src/menusys.c'), (('ripps2LastRites(support, id);', 'Delete is LAST RITES'), ('ripps2ShroudHide(support, id);', 'Hide Game'),
                           ('GAME_HIDE_GAME', 'the game options carry Hide Game'), ('APP_HIDE', 'and a PS1 game\'s')), 'menusys.c')
need(opl, (('if (!isFolderRow && ripps2ShroudRow(mdl->support, i))', 'a page leaves hidden games out'),), 'opl.c')
hm = rd('src/ripps2hdd.c')
if 'ripps2ApaCheck(apaWhy, sizeof(apaWhy))' not in hm or hm.index('ripps2ApaCheck(apaWhy') > hm.index('int r = fileXioRemove(path);'):
    fail.append('ripps2hdd.c: the HDD MANAGER walks the APA table before a partition goes, as LAST RITES does')

# ---- credits
ab = rd('src/ripps2about.c')
need(ab, (('"with rickgaiser\'s Neutrino inside as its second game core,"', 'the opening names Neutrino'),
          ('"BUILT ON RIPTOPL, WITH NEUTRINO"', 'Neutrino beside RiptOPL'), ('"Special thanks to all the YouTube love as well:"', 'the YouTube thanks')), 'ripps2about.c')
if ab.count('{\'H\', "NEUTRINO"}'):
    fail.append('ripps2about.c: Neutrino\'s old mid-page section went to the closing credits')

# ---- no background write runs into a launch (FifthFox, 10/22: damaged card images and a USB stick)
for head in ('void deinitEx(int exception, int modeSelected, int modeSelected2)', 'void deinit(int exception, int modeSelected)'):
    td = body(opl, head)
    if td.find('ioLaunchBegin();') < 0 or td.find('ioLaunchBegin();') > td.find('ioBlockOpsTimed('):
        fail.append('opl.c: %s raises the launch flag before anything else' % head.split('(')[0])
    if td.find('ioWaitWrites(') < td.find('ioBlockOpsTimed('):
        fail.append('opl.c: %s waits for the writes already started, after the drain' % head.split('(')[0])
need(rd('src/ioman.c'), (('int ioWriteBegin(void)', 'the write gate'), ('ok = !gIoLaunching;', 'closed once a launch begins')), 'ioman.c')
snapw = body(rd('src/supportbase.c'), 'void sbSnapScanned(')
if snapw.find('ioWriteBegin()') < 0 or snapw.find('ioWriteBegin()') > snapw.find('O_WRONLY'):
    fail.append('supportbase.c: RIPPS2.LST is written only through the write gate')
need(rd('src/supportbase.c'), (('if (ioCacheWriteBegin == NULL || ioCacheWriteBegin())', 'the games list cache through the gate'),), 'supportbase.c')
mw = body(mix, 'static void mixMasterSave(')
if mw.find('ioWriteBegin()') < 0 or mw.find('ioWriteBegin()') > mw.find('O_WRONLY'):
    fail.append('mixsupport.c: allgames.bin is written only through the write gate')
for f, needle in (('src/ripps2shot.c', 'ok = rsPngNow('), ('src/ripps2art.c', 'if (!ioWriteBegin())'), ('src/ripps2seance.c', '!ioWriteBegin()'),
                  ('src/ripps2games.c', 'if (!ioWriteBegin())')):
    if needle not in rd(f):
        fail.append('%s: its background write goes through the gate' % f)

# ---- the launch guard: every light-up has the guard in front of it (the user 10/23)
for f in ('src/opl.c', 'src/system.c', 'src/ripps2.c', 'src/ripps2files.c'):
    src_ = rd(f)
    for m in re.finditer(r'ripps2PlayLaunchSequence\(\);', src_):
        start = src_.rfind('\n{', 0, m.start())  # the function holding this light-up
        if 'ripps2LaunchGuard()' not in src_[start:m.start()]:
            fail.append('%s: a light-up at offset %d has no launch guard before it' % (f, m.start()))
sysd = body(rd('src/system.c'), 'int sysLaunchDisc(')
if sysd.find('ripps2LaunchGuard()') < 0 or sysd.find('ripps2LaunchGuard()') > sysd.find('mmceSendGameID('):
    fail.append("system.c: Launch Disc's guard comes before the MMCE GameID, so backing out leaves the card as it was")
need(rd('src/supportbase.c'), (('int ioScanCancelled(void) __attribute__((weak));', "the list read's stop is weak (host harness)"),
                               ('if (ioScanCancelled != NULL && ioScanCancelled())', 'a list read stops when asked')), 'supportbase.c')
lg = body(gm, 'int ripps2LaunchGuard(void)')
if not (lg.find('guiMsgBox(') < lg.find('ioLaunchBegin();') < lg.find('ioCancelScans();')):
    fail.append('ripps2games.c: the guard asks first, then stops writes and the list read')

# ---- one ELF (the user 10/23: no lite ELF), FreeType, fonts
mk = rd('Makefile')
need(mk, (('bible_xlf.o bible_mx4sio_xlf.o bible_hdd_xlf.o', 'BIBLE is carried'), ('neutrino_tgz.o', 'Neutrino is carried')), 'Makefile')
for f in ('Makefile', 'src/fntsys.c', 'src/ripps2boot.c', 'src/ripps2ember.c', 'src/ripps2status.c', 'src/textures.c'):
    if 'RIPPS2_LITE' in raw(f):
        fail.append('%s: one RIPPS2.elf, no lite variant' % f)
if '{INCEBTION_PICTURE, "incebtion", &incebtion_png}' not in rd('src/textures.c'):
    fail.append('textures.c: OPL\'s background is carried for its built-in look')
fnt = rd('src/fntsys.c')
if 'FT_Init_FreeType(' in fnt or 'static FT_Error fntNewLibrary(FT_Library *library)' not in fnt:
    fail.append('fntsys.c: FreeType starts with RIPPS2\'s own module list (FT_Init_FreeType links every module)')
for cls in ('tt_driver_class', 'sfnt_module_class', 'autofit_module_class', 'ft_smooth_renderer_class'):
    if '&%s' % cls not in fnt:
        fail.append('fntsys.c: %s is one RIPPS2 reads' % cls)
for gone in ('t1_driver_class', 'bdf_driver_class', 'pcf_driver_class', 'pfr_driver_class', 'winfnt_driver_class', 't42_driver_class'):
    if gone in fnt:
        fail.append('fntsys.c: %s stays out' % gone)
bsh = (repo / 'elf/build.sh').read_text(encoding='utf-8')
need(bsh, (('strip_fonts.py', 'the compiled-in fonts are stripped'),), 'build.sh')
wf = (repo / '.github/workflows/build-elf.yml').read_text(encoding='utf-8')
if 'RIPPS2_LITE' in bsh or 'lite' in wf.lower():
    fail.append('build.sh / build-elf.yml: one RIPPS2.elf, no lite build or artifact')

# ---- compiled: the APA check against synthetic disks
cc = shutil.which('gcc') or shutil.which('cc')
if cc is None:
    print('build114: no host C compiler, the compiled checks are skipped')
else:
    games = (root / 'src/ripps2games.c').read_text(encoding='utf-8').replace('\r\n', '\n')
    apa = body(games, 'static u32 lrLe32(') + body(games, 'static u32 lrApaMax(') + body(games, 'int ripps2ApaCheck(')
    harness = r'''
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
typedef unsigned char u8;
typedef unsigned int u32;
#define LR_APA_MAGIC 0x00415041
static u8 *disk; static long diskBytes; static u32 diskSectors;
static u32 hddGetTotalSectors(void) { return diskSectors; }
/* the synthetic disk is sparse: records of a sector number and the two sectors of a header found there */
static int hddReadSectors(u32 lba, u32 n, void *buf)
{
    long at;
    for (at = 0; at + 1028 <= diskBytes; at += 1028)
        if (*(u32 *)(disk + at) == lba && n <= 2) {
            memcpy(buf, disk + at + 4, n * 512);
            return 0;
        }
    return -1;
}
''' + TR_STUBS + apa + r'''
int main(int argc, char **argv)
{
    FILE *f = fopen(argv[1], "rb"); long size; char why[200];
    fseek(f, 0, SEEK_END); size = ftell(f); fseek(f, 0, SEEK_SET);
    disk = malloc(size); fread(disk, 1, size, f); fclose(f);
    diskBytes = size; diskSectors = strtoul(argv[2], NULL, 0);
    printf("%d %s\n", ripps2ApaCheck(why, sizeof(why)), why);
    return 0;
}
'''

    def header(start, length, nxt, prev, name):
        h = bytearray(1024)
        struct.pack_into('<IIII', h, 4, 0x00415041, nxt, prev, 0)
        h[16:16 + len(name)] = name.encode()
        struct.pack_into('<II', h, 64, start, length)
        s = sum(struct.unpack_from('<255I', h, 4)) & 0xFFFFFFFF
        struct.pack_into('<I', h, 0, s)
        return bytes(h)

    def table(parts):
        # parts: [(start, length, name)]; the chain in order, the last one's next 0, __mbr's prev the last one
        img = bytearray()
        for i, (s, l, n) in enumerate(parts):
            nxt = parts[i + 1][0] if i + 1 < len(parts) else 0
            prev = parts[i - 1][0] if i > 0 else parts[-1][0]
            img += struct.pack('<I', s) + header(s, l, nxt, prev, n)
        return bytes(img)

    M = 0x40000  # 128 MB
    good = [(0, M, '__mbr'), (M, M, '__net'), (2 * M, 2 * M, '__system'), (4 * M, 4 * M, 'PP.GAME')]
    disk40 = 0x04ffffff
    cases = [('a good table', good, disk40, 1),
             ('written from a bigger disk', good + [(8 * M, 8 * M, 'PP.BIG')], 12 * M, 0),
             ('a partition too big for the disk', [(0, M, '__mbr'), (0x2000000, 0x2000000, 'PP.HUGE')], disk40, 0),
             ('off its alignment', [(0, M, '__mbr'), (M, 2 * M, 'PP.ODD')], disk40, 0)]
    def patch(img, rec, off, value):  # rec: the record's index; its header starts 4 bytes in
        base = rec * 1028 + 4
        struct.pack_into('<I', img, base + off, value)
        struct.pack_into('<I', img, base, sum(struct.unpack_from('<255I', img, base + 4)) & 0xFFFFFFFF)
    broken = bytearray(table(good))
    patch(broken, 3, 12, 3 * M)  # PP.GAME's prev points nowhere
    open_chain = bytearray(table(good))
    patch(open_chain, 0, 12, 2 * M)  # __mbr's prev is not the last partition
    with tempfile.TemporaryDirectory() as tmp:
        src, exe = os.path.join(tmp, 'apa.c'), os.path.join(tmp, 'apa.exe')
        open(src, 'w').write(harness)
        cr = subprocess.run([cc, '-std=gnu99', '-Wall', '-Werror', '-Wno-unused-function', src, '-o', exe], capture_output=True, text=True)
        if cr.returncode != 0:
            fail.append('the APA check does not compile on its own:\n' + cr.stderr[-1500:])
        else:
            runs = [(n, table(p), d, want) for n, p, d, want in cases] + [('a broken link', bytes(broken), disk40, 0), ('a chain that does not close', bytes(open_chain), disk40, 0)]
            for name, img, sectors, want in runs:
                path = os.path.join(tmp, 'disk.bin')
                open(path, 'wb').write(img)
                out = subprocess.run([exe, path, str(sectors)], capture_output=True, text=True).stdout.strip()
                if not out.startswith('%d ' % want):
                    fail.append('APA check, %s: wanted %d, got "%s"' % (name, want, out))

    # ---- compiled: the master list, saved and read back; a damaged or short file is not read
    m = (root / 'src/mixsupport.c').read_text(encoding='utf-8').replace('\r\n', '\n')
    pick = ''.join(body(m, h) for h in ('static unsigned int mixLe32(', 'static void mixPutLe32(', 'static unsigned int mixFnv(',
                                        'static void mixMasterLoad(', 'static void mixMasterSave('))
    harness = r'''
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#ifndef O_BINARY
#define O_BINARY 0
#endif
#define open(p, f, ...) open((p), (f) | O_BINARY, ##__VA_ARGS__)
#define LOG(...) ((void)0)
enum { MIX_FAM_APA = 0, MIX_FAM_ATA, MIX_FAM_USB, MIX_FAM_MX4SIO, MIX_FAM_ILINK, MIX_FAM_BDM, MIX_FAM_MMCE, MIX_FAM_SMB, MIX_FAM_UDPFS, MIX_FAM_HTTP, MIX_FAM_COUNT };
#define MIX_MASTER_FILE  "allgames.bin"
#define MIX_MASTER_MAGIC "RIPALL01"
#define MIX_MASTER_MAX   8192
typedef struct { void *owner; int mode, id, kind, rank; char *text, *startup; int family; } mix_rec_t;
typedef struct { unsigned char kind, family; char *text, *startup; } mix_master_t;
static mix_master_t *mixMaster; static int mixMasterCount, mixMasterLoaded, mixMasterSaved = -1; static unsigned int mixMasterSum;
static int gRipps2FastCache = 1, gEnableWrite = 1;
static int ioWriteBegin(void) { return 1; } /* build 114's write gate: open, no launch here */
static void ioWriteEnd(void) {}
static char gPath[512];
static void mixMasterPath(char *out, int size) { snprintf(out, size, "%s", gPath); }
''' + pick + r'''
int main(int argc, char **argv)
{
    char *t[3] = {"Aqua Teen Hunger Force", "Burnout 3 - Takedown", "Spyro the Dragon"}, *s[3] = {"SLUS_216.56", "SLUS_210.50", "Spyro the Dragon"};
    mix_rec_t r[3]; int i;
    snprintf(gPath, sizeof(gPath), "%s", argv[1]);
    for (i = 0; i < 3; i++) { memset(&r[i], 0, sizeof(r[i])); r[i].text = t[i]; r[i].startup = s[i]; r[i].kind = i == 2 ? 2 : 0; r[i].family = i; }
    if (argc > 2) { mixMasterLoad(); printf("%d\n", mixMasterCount); return 0; }
    mixMasterSave(r, 3);
    mixMasterLoaded = 0; mixMasterCount = 0;
    mixMasterLoad();
    if (mixMasterCount != 3) { printf("read %d\n", mixMasterCount); return 1; }
    for (i = 0; i < 3; i++)
        if (strcmp(mixMaster[i].text, t[i]) || strcmp(mixMaster[i].startup, s[i]) || mixMaster[i].family != i || mixMaster[i].kind != (i == 2 ? 2 : 0)) { printf("row %d\n", i); return 1; }
    printf("ok\n");
    return 0;
}
'''
    with tempfile.TemporaryDirectory() as tmp:
        src, exe, path = os.path.join(tmp, 'mix.c'), os.path.join(tmp, 'mix.exe'), os.path.join(tmp, 'allgames.bin')
        open(src, 'w').write(harness)
        cr = subprocess.run([cc, '-std=gnu99', '-Wall', '-Wno-unused-function', '-Wno-unused-variable', src, '-o', exe], capture_output=True, text=True)
        if cr.returncode != 0:
            fail.append('the master list does not compile on its own:\n' + cr.stderr[-1500:])
        else:
            out = subprocess.run([exe, path], capture_output=True, text=True).stdout.strip()
            if out != 'ok':
                fail.append('master list round trip: %s' % out)
            data = bytearray(open(path, 'rb').read())
            data[30] ^= 0x55
            open(path, 'wb').write(data)
            if subprocess.run([exe, path, 'load'], capture_output=True, text=True).stdout.strip() != '0':
                fail.append('master list: a damaged file must not be read')
            open(path, 'wb').write(bytes(data[:40]))
            if subprocess.run([exe, path, 'load'], capture_output=True, text=True).stdout.strip() != '0':
                fail.append('master list: a short file must not be read')

if fail:
    print('\n'.join(fail))
    sys.exit(1)
print('build114: the merge, the launcher search, STATUS, the master list, hide and delete with the APA check, credits, launch write safety, the launch guard, one ELF, FreeType OK')
