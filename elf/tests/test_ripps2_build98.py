"""Build 98: Memory Files. Both card slots stay listed after START DRIVES; a delete is thorough (the music lets go
of a file it streams from, a failure names its reason and is never E0, a removal is checked gone); a copy to a
memory card says CARD FULL up front instead of E999 partway; sounds per event, the theme's first, then AUDIO's.

Static checks on the patched tree, and bgmHoldsPath run on the host."""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(os.environ.get('RIPTOPL_DIR', '.'))
rd = lambda p: (root / p).read_text(encoding='utf-8')
fb, snd = rd('src/ripps2files.c'), rd('src/sound.c')
fail = []

# --- the card slots: mcman's own answer, read more than once, never a single opendir
if 'static int fbCardType(int port, int *freeKb)' not in fb or 'mcGetInfo(port, 0, &type, &freeC, &format);' not in fb:
    fail.append('a card slot must be asked through mcGetInfo (it clears "changed card")')
if 'if (!fbCardListed(dev))' not in fb:
    fail.append('the drive list must list a card slot by fbCardListed, not one opendir')
sd = fb[fb.index('static void fbStartDrivesWork(void)'):]
sd = sd[:sd.index('\n}\n')]
if 'opendir("mc1:/")' in sd or 'fbCardType(1, NULL) != 0' not in sd:
    fail.append('MX4SIO must stay out while any card is in slot 2, by mcman\'s answer')
if sd.count('fbCardType(') < 3:
    fail.append('after the MMCE ping both slots must be asked again')

# --- delete: the call's own code, gone checked, the music let go
rr = fb[fb.index('static int fbRemoveRetry('):]
rr = rr[:rr.index('\n}\n')]
if 'r == 0 && !fbExists(path)' not in rr or 'errno = err;' not in rr:
    fail.append('a removal must be checked gone and keep its own error code')
if '"%s: %s %s"' not in fb or 'case EBUSY:' not in fb or '"IN USE"' not in fb:
    fail.append('a failure must name its reason in words (IN USE...) before what failed')
if fb.count('fbReleaseMusic(') < 3 or 'bgmHoldsPath(from)' not in fb:
    fail.append('delete, move and rename must let the music go of a file it streams from')
if 'fbMusicPaused = 0;' not in fb or 'bgmStart();' not in fb:
    fail.append('the music must come back after the operation')

# --- copy: short writes finished, a full drive said, a card's room checked first
cf = fb[fb.index('static int fbCopyFile('):]
cf = cf[:cf.index('\n}\n')]
if re.search(r'errno = [^;]*999', cf) or 'ENOSPC' not in cf or 'off += w;' not in cf:
    fail.append('a copy must finish short writes and call a write that takes nothing FULL (it was E999)')
if '"CARD FULL: NEEDS %u KB, %d KB FREE"' not in fb:
    fail.append('a paste onto a memory card that cannot fit must say so before writing')

# --- sounds: per event, theme first, then AUDIO
si = snd[snd.index('int sfxInit(int bootSnd)'):]
si = si[:si.index('\n}\n')]
if 'themeSfx' not in si or 'audioSfx' not in si or 'sfx_files[i].buffer == NULL && audioSfx' not in si or 'thmSfxEnabled' in si:
    fail.append('each sound must come from the theme, else from the AUDIO folder')

# --- bgmHoldsPath on the host
hp = snd[snd.index('int bgmHoldsPath(const char *path)'):]
hp = hp[:hp.index('\n}\n') + 3]
cc = shutil.which('gcc') or shutil.which('cc')
if cc:
    prog = '#include <stdio.h>\n#include <ctype.h>\n#include <string.h>\n#include <strings.h>\nstatic char bgmOpenPath[256];\n' + hp + r'''
#include <string.h>
static int t(const char *open, const char *path, int want)
{
    strcpy(bgmOpenPath, open);
    int got = bgmHoldsPath(path);
    if (got != want) { printf("'%s' vs '%s': %d, want %d\n", open, path, got, want); return 1; }
    return 0;
}
int main(void)
{
    int bad = 0;
    bad |= t("pfs0:AUDIO/bgm_03 Slideshow.ogg", "pfs0:/AUDIO/bgm_03 Slideshow.ogg", 1);
    bad |= t("mass0:/AUDIO/bgm_03.ogg", "mass0:/audio/BGM_03.OGG", 1);
    bad |= t("mass0:/AUDIO/bgm_03.ogg", "mass0:/AUDIO", 1);
    bad |= t("mass0:/AUDIO/bgm_03.ogg", "mass0:/AUDIO/", 1);
    bad |= t("mass0:/AUDIO/bgm_03.ogg", "mass0:/AUD", 0);
    bad |= t("mass0:/AUDIO/bgm_03.ogg", "mass1:/AUDIO/bgm_03.ogg", 0);
    bad |= t("mass0:/AUDIO/bgm_03.ogg", "mass0:/AUDIO/bgm_03.ogg.bak", 0);
    bad |= t("", "mass0:/AUDIO", 0);
    bad |= t("mass0:/AUDIO/bgm_03.ogg", "mass0:/", 1);
    return bad;
}
'''
    with tempfile.TemporaryDirectory() as td:
        open(td + '/h.c', 'w').write(prog)
        r = subprocess.run([cc, td + '/h.c', '-o', td + '/h.exe'], capture_output=True, text=True)
        if r.returncode:
            fail.append('bgmHoldsPath host build: ' + r.stderr[-300:])
        else:
            r = subprocess.run([td + '/h.exe'], capture_output=True, text=True)
            if r.returncode:
                fail.append('bgmHoldsPath: ' + r.stdout.strip())

# --- music with a top-bit Ogg serial: the reader clears it and corrects each page's CRC (run on the host)
if 'src->fixSerial = 1;' not in snd or 'return bgmFixedRead(src, (unsigned char *)ptr, size * nmemb) / size;' not in snd:
    fail.append('a top-bit serial must be spotted at the open and fixed as it is read')
if re.search(r'^[^#\n]*bgmOpenTrace', snd[snd.index('static size_t bgmSourceRead('):snd.index('static ov_callbacks bgmSourceCallbacks')], re.M) and \
        '#ifdef __DEBUG\n        if (bgmOpenTrace)' not in snd.replace('\r\n', '\n'):
    fail.append('the open trace must stay behind __DEBUG (a host test compiles the reader)')


def ogg_crc(b):
    tab = []
    for i in range(256):
        c = i << 24
        for _ in range(8):
            c = ((c << 1) ^ 0x04C11DB7) & 0xFFFFFFFF if c & 0x80000000 else (c << 1) & 0xFFFFFFFF
        tab.append(c)
    c = 0
    for x in b:
        c = ((c << 8) & 0xFFFFFFFF) ^ tab[((c >> 24) ^ x) & 0xFF]
    return c


def ogg_stream(serial, pages=40, seed=7):
    import random
    rnd = random.Random(seed)
    out = bytearray()
    for n in range(pages):
        nseg = rnd.choice([1, 3, 17, 60, 128, 255])
        segs = bytes(rnd.randint(0, 255) for _ in range(nseg))
        body = bytes(rnd.randint(0, 255) for _ in range(sum(segs)))
        h = bytearray(b'OggS\0' + bytes([2 if n == 0 else 0]) + (n * 1024).to_bytes(8, 'little') +
                      serial.to_bytes(4, 'little') + n.to_bytes(4, 'little') + b'\0\0\0\0' + bytes([nseg]) + segs)
        page = h + body
        page[22:26] = ogg_crc(page).to_bytes(4, 'little')
        out += page
    return bytes(out)


if cc:
    src = snd[snd.index('#define OGG_HDR_MAX'):snd.index('static size_t bgmSourceRead(')]
    src = src.replace('static int bgmSourceReopen(bgm_source_t *src);', '')
    neg, pos = ogg_stream(0x9234ABCD), ogg_stream(0x1234ABCD)
    prog = r'''#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#define BGM_REOPEN_TRIES 4
typedef struct { FILE *f; long pos; long size; char path[256]; int fixSerial; unsigned char serial[4]; } bgm_source_t;
static int bgmSourceReopen(bgm_source_t *src) { (void)src; return 0; }
''' + src + r'''
int main(int argc, char **argv)
{
    static unsigned char want[1 << 20], got[1 << 20];
    FILE *e = fopen(argv[2], "rb");
    long n = (long)fread(want, 1, sizeof(want), e), i;
    fclose(e);
    bgm_source_t s = {fopen(argv[1], "rb"), 0, n, "", 1, {0xCD, 0xAB, 0x34, 0x92}};
    size_t r;
    while ((r = bgmFixedRead(&s, got + s.pos, 2048)) > 0)
        ;
    if (s.pos != n || memcmp(got, want, n)) { printf("in 2 KB reads: %ld of %ld bytes, first difference at %ld\n", s.pos, n, (long)(memcmp(got, want, n) ? 0 : -1)); return 1; }
    srand(5);
    for (i = 0; i < 400; i++) { /* reads from anywhere, of any length, as the open's seeks make them */
        long at = rand() % n, len = 1 + rand() % 9000;
        if (at + len > n) len = n - at;
        s.pos = at;
        r = bgmFixedRead(&s, got, (size_t)len);
        if ((long)r != len || memcmp(got, want + at, len)) { printf("read %ld at %ld differs\n", len, at); return 1; }
    }
    return 0;
}
'''
    with tempfile.TemporaryDirectory() as td:
        open(td + '/neg.ogg', 'wb').write(neg)
        open(td + '/pos.ogg', 'wb').write(pos)
        open(td + '/f.c', 'w').write(prog)
        r = subprocess.run([cc, td + '/f.c', '-o', td + '/f.exe'], capture_output=True, text=True)
        if r.returncode:
            fail.append('the serial fix host build: ' + r.stderr[-400:])
        else:
            r = subprocess.run([td + '/f.exe', td + '/neg.ogg', td + '/pos.ogg'], capture_output=True, text=True)
            if r.returncode:
                fail.append('the serial fix: ' + r.stdout.strip())

# --- START DRIVES asks MMCE as Storage does (an MMCE ping on a plain card in slot 1 took mc1:/ away)
if 'if (gMMCEStartMode != START_MODE_DISABLED) {' not in sd or 'gMMCESlot == 2 && !fbMmceSlot[0]' not in sd:
    fail.append('START DRIVES must leave MMCE alone when it is off, and ping slot 1 only as Storage\'s Auto does')
if '"MEMORY CARD %c", dev[2]' not in fb or '"MEMORY CARD 2' in rd('src/ripps2status.c') or '"WRITE THE SAVES TO MEMORY CARD 2"' in rd('src/ripps2card.c'):
    fail.append('the cards are MEMORY CARD 0 and MEMORY CARD 1 (mc0:/, mc1:/)')

th, menu = rd('src/themes.c'), rd('src/menusys.c')
# --- the info page: the group waits for its background, late art fades, the show opens on slide 1
if '#define INFO_GROUP_WAIT_S 1.6f' not in th or 'SLIDE_FIRST_WAIT_S' not in th or 'artFadeIn(drawElem, item, texture) : 1.0f;' not in th:
    fail.append('the info page\'s background must come in with its disc and cover, late art fading on its own')
# --- the Grid's page buttons turn a page
if 'static int menuGridPage(int dir)' not in menu or 'if (menuGridPage(1))' not in menu or 'if (menuGridPage(-1))' not in menu:
    fail.append('L2 / R2 on the Grid must turn a whole page of covers')
# --- RIPFLOW tilts its centre cover; its info screenshots tip as one sheet
cf = rd('misc/theme_coverflow.cfg').replace('\r\n', '\n')
if 'int cfTilt = elem->tilt' not in th or cf.count('\ttype=Coverflow\n\ttilt=1\n') < 1 or cf.count('\ttilt_x=320\n\ttilt_y=330\n') != 2:
    fail.append('RIPFLOW: the centre cover tips with the stick, the two screenshots on one pivot')
# --- vignette levels, background blur, the widescreen grid
if 'fade *= gRipps2Vignette >= 2 ? 1.0f : gRipps2Vignette == 1 ? 0.5f : 0.0f;' not in th or 'w + 2, h + 2' not in th:
    fail.append('Vignette Other Covers: Off, Weak (half) and Full, a pixel past the cover')
if 'static int thmBlurPercent(void)' not in th or '"bg_blur"' not in th or 'bg_blur=weak' not in rd('misc/theme_ripgrid.cfg'):
    fail.append('Background Blur: Theme, Off, Weak, Normal, Strong, and bg_blur=weak on RIPGRID')
if 'static void gridUseLayout(void)' not in th or 'theme->gridWide = wide;' not in th or 'wide_columns=6' not in rd('misc/theme_ripgrid.cfg'):
    fail.append('the Grid keeps a 16:9 layout of its own (RIPGRID: 6 across)')
if 'int wide = rmWideScale(4) == 3;' not in th:
    fail.append("the Grid's 16:9 layout must follow the picture as drawn (720p is 16:9 whatever Widescreen says)")
gc = th.replace('\r\n', '\n')
gc = gc[gc.index('static void drawGridCover('):]
gc = gc[:gc.index('\n}\n')]
if '!gridSerial(src->itemGetStartup(src, it->item.id), serial, sizeof(serial))))\n                return;' not in gc:
    fail.append('with coverless=serial a tile is the game ID or nothing, never its name')
if 'RIPgrid' in th or '"<RIPGRID>"' not in th:
    fail.append('RIPGRID is written in capitals')

print('\n'.join(fail) or 'build98: card slots kept, thorough delete, CARD FULL up front, sounds theme then AUDIO, top-bit Ogg serials play, START DRIVES asks MMCE as Storage does, cards 0 and 1, info page fades as one, Grid pages, RIPFLOW tilt, vignette levels, background blur, widescreen grid, RIPGRID OK')
sys.exit(1 if fail else 0)
