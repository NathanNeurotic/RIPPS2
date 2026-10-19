"""Build 105: RIPDISC. The rip's own logic compiled on the host (safe names, SYSTEM.CNF keys, the CUE sheet, a PS1
sector's sync put back, a refused read retried a sector at a time), plus static checks on the tree: the panel on
LAUNCH DISC, the RIPPED clipboard in Memory Files, Open PS2 Loader's split-game names, music in AUDIO by any name."""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r2src import TR_STUBS  # noqa: E402

root = Path(os.environ.get('RIPTOPL_DIR', '.'))
rd = lambda p: (root / p).read_text(encoding='utf-8').replace('\r\n', '\n')
fail = []


def check(ok, what):
    if not ok:
        fail.append(what)


def fn(src, sig):
    """The function starting at sig, to its closing brace at the start of a line."""
    i = src.index(sig)
    j = src.index('\n}\n', i)
    return src[i:j + 3]


disc = rd('src/ripps2disc.c')
ui = rd('src/ripps2ui.c')
files = rd('src/ripps2files.c')
sound = rd('src/sound.c')
make = rd('Makefile')
sb = rd('src/supportbase.c')

# 1. wired in
check(re.search(r'FRONTEND_OBJS =[^\n]*\bripps2disc\.o\b', make) is not None, 'ripps2disc.o is in FRONTEND_OBJS')
launch = ui[ui.index('void ripps2RenderLaunch(void)'):ui.index('void ripps2HandleInputLaunch(void)')]
check('ripps2DiscRipRender();' in launch, 'LAUNCH DISC draws the RIPDISC panel')
inp = ui[ui.index('void ripps2HandleInputLaunch(void)'):]
check(inp.index('ripps2DiscRipInput()') < inp.index('getKeyOn(KEY_R1)'), 'the panel takes SELECT before the page does')
worker = fn(ui, 'static void discPollWorker(void)')
check(worker.rindex('discKind =') > worker.index('snprintf(discName'), 'the disc kind is set after its ID and title')
check('RIPPS2_DISC_PS1' in worker and 'RIPPS2_DISC_ESR' in worker and 'RIPPS2_DISC_VIDEO' in worker, 'every disc kind is told')

# 2. the panel and the hold: 4.2 s each, as the design says
check(re.search(r'#define RD_HOLD_S\s+4\.2f', disc) is not None, 'RD_HOLD_S is 4.2 s')
render = fn(disc, 'void ripps2DiscRipRender(void)')
check('RD_HOLD_S' in render and 'rdIsGame(kind) && !rdIsMedia(kind)' in render, 'the panel waits 4.2 s and shows only for a disc RIPDISC rips')
hold = fn(disc, 'int ripps2DiscRipInput(void)')
check('getKeyPressed(KEY_SELECT)' in hold and 'RD_HOLD_S' in hold, 'SELECT is held 4.2 s')
confirm = fn(disc, 'static int rdConfirm(int drives, const char *place)')
check('_t("SIZE")' in confirm and '_t("TO")' in confirm and 'KEY_START' in confirm, 'the confirm step says the size and the place, then START rips')

# 3. a game over 4 GB on a drive that may be FAT32: Open PS2 Loader's split parts, named as supportbase.c reads them
target = fn(disc, 'static int rdGameTarget(char *path, int size)')
check('rdBytes > RD_FAT32_MAX && rdSlotType[rdSlotSel] != BDM_TYPE_ATA' in target, 'only a drive that may be FAT32 splits a big game')
check('"%sul.%08X.%s.%02x"' in sb, 'supportbase.c still names the parts "%sul.%08X.%s.%02x"')
check('"%sul.%08X.%s.", prefix, USBA_crc32(nm), rdId' in disc and '"%s%02x", rdPartBase' in disc, 'RIPDISC names its parts the same way')
check('e.media = rdKind == RIPPS2_DISC_PS2CD ? 0x12 : 0x14;' in disc and 'e.Byte08 = 0x08;' in disc, 'the ul.cfg record is a USBExtreme one')
check(re.search(r'#define RD_UL_PART\s+0x40000000u', disc) is not None, 'parts are 1 GB')

# 4. media through Memory Files
check('fbRipWhat[0] && !inVmc && !fbIsMc(fbPath)' in files, 'PASTE offers RIPPED media outside memory cards')
check('_t("RIPPED")' in fn(files, 'static void fbClipWhat(char *out, int size)'), 'the clipboard reads RIPPED')
paste = fn(files, 'static void fbPasteRipped(void)')
check('ripps2DiscRipHere(fbPath' in paste and 'r == 2 && guiShowKeyboard' in paste, 'PASTE rips, then an audio CD is named on the keyboard')
check('"%sMEDIA", base' in disc, 'media go to MEDIA, beside AUDIO')

# 5. AUDIO lists any .ogg / .wav as music; README.txt in AUDIO and MEDIA
check('bgmMusicScan(dir, "AUDIO", 0,' in sound, "RIPPS2's AUDIO lists every .ogg and .wav")
check('bgmMusicScan("", sub, 1,' not in sound, 'no AUDIO scan keeps to bgm* names')
for f, n in (('src/ripps2cd.c', 1), ('src/ripps2biossnd.c', 2), ('src/ripps2disc.c', 2)):
    check(rd(f).count('ripps2WriteReadme(') >= n, f + ' writes the README')
check('—' not in disc, 'no em dash in ripps2disc.c')

# 6. compiled: the pure parts of the rip
HARNESS = r'''
#include <assert.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
typedef unsigned char u8;
typedef unsigned int u32;
#define RD_RAW 2352
#define RD_XA 2340
#define RD_TRACKS 99
#define SCECdSecS2340 2
static int rdTracks;
static u32 rdStart[RD_TRACKS + 2];
static unsigned char rdAudio[RD_TRACKS + 2];
static u8 rdOne[RD_RAW + 64];
static int made = 0;
static void rdMadeAdd(const char *p, int d) { (void)p; (void)d; made++; }
static int refuse = -1, cdda = 0;
static int rdRead(u32 lsn, u32 n, void *buf, int pattern)
{
    u32 i;
    assert(pattern == SCECdSecS2340);
    if (refuse >= 0 && (u32)refuse >= lsn && (u32)refuse < lsn + n)
        return 0;
    for (i = 0; i < n; i++)
        memset((u8 *)buf + i * RD_XA, (int)((lsn + i) & 0xFF), RD_XA);
    return 1;
}
static int ripps2CdReadAudio(u32 lsn, u32 n, void *buf) { (void)lsn; cdda++; memset(buf, 0xAA, n * RD_RAW); return 1; }
'''
MAIN = r'''
int main(int argc, char **argv)
{
    char out[64], v[64], cue[2048];
    static u8 raw[16 * RD_RAW];
    int i, n;
    FILE *f;
#ifdef _WIN32
    _fmode = O_BINARY;
#endif
    rdSafeName("Ratchet: Deadlocked / \"Gladiator\"?", out, sizeof(out));
    assert(strpbrk(out, "\\/:*?\"<>|") == NULL && out[strlen(out) - 1] != ' ' && !strncmp(out, "Ratchet", 7));
    rdSafeName("..hidden. ", out, sizeof(out));
    assert(!strcmp(out, "hidden"));

    const char *ps2 = "BOOT2 = cdrom0:\\SLUS_200.62;1\r\nVER = 1.00\r\nVMODE = NTSC\r\n";
    assert(discCnfValue(ps2, "BOOT2", v, sizeof(v)) && !strcmp(v, "cdrom0:\\SLUS_200.62;1"));
    assert(!discCnfValue(ps2, "BOOT", v, sizeof(v))); // BOOT2 is not BOOT
    const char *ps1 = "BOOT = cdrom:\\SCUS_944.26;1\r\nTCB = 4\r\nEVENT = 10\r\n";
    assert(discCnfValue(ps1, "BOOT", v, sizeof(v)) && !strcmp(v, "cdrom:\\SCUS_944.26;1"));

    rdTracks = 3;
    rdStart[1] = 0;
    rdStart[2] = 20000;
    rdStart[3] = 25000;
    rdStart[4] = 30000;
    rdAudio[1] = 0;
    rdAudio[2] = rdAudio[3] = 1;
    assert(rdWriteCue(argv[1], "Game.bin"));
    f = fopen(argv[1], "rb");
    n = (int)fread(cue, 1, sizeof(cue) - 1, f);
    fclose(f);
    cue[n] = '\0';
    assert(!strcmp(cue, "FILE \"Game.bin\" BINARY\r\n"
                        "  TRACK 01 MODE2/2352\r\n    INDEX 01 00:00:00\r\n"
                        "  TRACK 02 AUDIO\r\n    INDEX 00 04:24:50\r\n    INDEX 01 04:26:50\r\n"
                        "  TRACK 03 AUDIO\r\n    INDEX 01 05:33:25\r\n"));

    assert(rdReadRaw(100, 3, raw)); // a whole read: each sector's sync put back in front of its 2340 bytes
    for (i = 0; i < 3; i++) {
        assert(!memcmp(raw + i * RD_RAW, rdSync, 12));
        assert(raw[i * RD_RAW + 12] == (u8)(100 + i) && raw[i * RD_RAW + RD_RAW - 1] == (u8)(100 + i));
    }
    refuse = 101; // one sector the drive will not give as data: asked for raw, the others still read as data
    memset(raw, 0, sizeof(raw));
    assert(rdReadRaw(100, 3, raw) && cdda == 1);
    assert(!memcmp(raw, rdSync, 12) && raw[12] == 100 && raw[RD_RAW] == 0xAA && raw[2 * RD_RAW + 12] == 102);
    puts("ok");
    return 0;
}
'''
cc = shutil.which('gcc') or shutil.which('cc')
if cc is None:
    print('SKIP compile (no host C compiler)')
else:
    sync = disc.index('static const u8 rdSync[12]')
    body = '\n'.join([
        disc[sync:disc.index(';', sync) + 1],
        fn(disc, 'static int rdReadRaw(u32 lsn, u32 n, u8 *out)'),
        fn(disc, 'static void rdSafeName(const char *in, char *out, int size)'),
        fn(disc, 'static void rdCueTime(u32 lsn, char *out, int size)'),
        fn(disc, 'static int rdWriteCue(const char *path, const char *binName)'),
        fn(ui, 'static int discCnfValue(const char *cnf, const char *key, char *out, int size)'),
    ])
    with tempfile.TemporaryDirectory() as tdn:
        td = Path(tdn)
        (td / 't.c').write_text(TR_STUBS + HARNESS + body + MAIN, encoding='utf-8')
        exe = td / 't.exe'
        r = subprocess.run([cc, '-std=gnu99', '-Wall', '-Werror', str(td / 't.c'), '-o', str(exe)], capture_output=True, text=True)
        if r.returncode != 0:
            fail.append('the RIPDISC harness does not build:\n' + r.stderr[-2000:])
        else:
            r = subprocess.run([str(exe), str(td / 'game.cue')], capture_output=True, text=True)
            check(r.returncode == 0 and 'ok' in r.stdout, 'the RIPDISC harness runs: ' + (r.stdout + r.stderr)[-800:])

if fail:
    print('build 105 FAILED:')
    for f in fail:
        print(' -', f)
    sys.exit(1)
print('build 105 ok')
