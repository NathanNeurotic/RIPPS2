"""Build 95: sound and stability. Sound effects that never stack, stall or come back stale (voices that know
when they end), no built-in sounds, every sound file read on the IO worker; libsmslite no longer replacing the C
library's string functions (RIPFLOW, a boot hang, a console strchr miscount); pictures decoded from memory and
game art as JPG; an .adp preview in Memory Files; the In-Game Menu marked experimental.

Static checks on the patched tree and on elf/libsmslite; then, with a C compiler, the .adp header's length
maths run on the PC."""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(os.environ.get('RIPTOPL_DIR', '.'))
elf = Path(__file__).resolve().parents[1]
rd = lambda p: (root / p).read_text(encoding='utf-8')
snd, mk, media, tex, st = rd('src/sound.c'), rd('Makefile'), rd('src/ripps2media.c'), rd('src/textures.c'), rd('src/ripps2status.c')
fail = []

# ---- libsmslite must not export the C library's names (it links ahead of libc)
utils = (elf / 'libsmslite' / 'src' / 'ps2' / 'utils.S').read_text(encoding='utf-8')
libc = ['strlen', 'strcat', 'strcpy', 'strncmp', 'strncpy', 'strchr', 'strcmp', 'strrchr', 'strstr', 'strpbrk', 'memmove',
        'memcpy', 'memset', 'malloc', 'free']
exported = [n for n in libc if re.search(r'^\s*\.globl\s+%s\s*$' % n, utils, re.M)]
if exported:
    fail.append('libsmslite exports C library names again: %s' % ', '.join(exported))
build = (elf / 'build.sh').read_text(encoding='utf-8')
if 'symbols that shadow a later library' not in build or 'exit 1' not in build.split('symbols that shadow a later library')[1][:600]:
    fail.append('build.sh must fail a build where libsmslite shadows a later library')

# ---- sounds: none built in, voices, the IO worker
if re.search(r'EE_OBJS\s*\+=.*\$\(AUDIO_OBJS\)', mk) or 'boot_adp' in snd:
    fail.append('no sound may be built into the ELF')
if 'static int sfxStart(int id, int volume)' not in snd or 'voiceBusy' not in snd:
    fail.append('sounds must take only a voice that has ended (sfxStart, voiceBusy)')
m = re.search(r'static int sfxStart\(int id, int volume\)\n\{(.*?)\n\}', snd, re.S)
if m and m.group(1).find('audsrv_ch_play_adpcm') > m.group(1).find('audsrv_adpcm_set_volume_and_pan'):
    fail.append('a voice gets its volume only after audsrv accepted the play (else an old tail is unmuted)')
callers = [p.name for p in (root / 'src').glob('*.c') if p.name != 'sound.c' and re.search(r'\bsfxInit\(0\)', p.read_text(encoding='utf-8', errors='replace'))]
if callers:
    fail.append('sfxInit(0) outside the IO worker (use sfxReload): %s' % ', '.join(callers))
if 'sfxBootStartEarly' in rd('src/opl.c') or 'sfxRead(' in snd[snd.index('void sfxBootStart(void)'):snd.index('void sfxBootStart(void)') + 600]:
    fail.append('the boot sound must not be read on the main thread')
if 'SifAllocIopHeap(sfxData->size + SFX_IOP_MARGIN)' not in snd:
    fail.append('the IOP must be checked for room before audsrv takes a sound')
if 'RIPPS2_MEDIA_SOUND' not in media or 'sfxPreviewStart(path)' not in media or 'sfxPreviewStop()' not in media:
    fail.append('Memory Files must play an .adp (and load the sounds again after)')
if 'ACT_SOUNDS_RIP' not in st or 'sfxLoadedSounds' not in st:
    fail.append('STATUS must say where the sounds come from')
if 'Experimental' not in rd('lng_tmpl/_base.yml').split('HINT_RIPPS2_IGR_MENU')[1][:200]:
    fail.append("the In-Game Menu's tooltip must call it experimental")

# ---- pictures
if 'jpeg_stdio_src' in media or 'static jmp_buf' in media:
    fail.append('pictures decode from memory, with no decoder state kept between calls')
if 'viewReadAll' not in media or 'jpeg_mem_src' not in media:
    fail.append('a picture is read whole before it is decoded')
if 'static int texLoadJpg' not in tex or '"%s.jpg", path' not in tex:
    fail.append('game art must fall back to a JPG of the same name')

# ---- the .adp header's length on the PC
cc = shutil.which('gcc') or shutil.which('cc')
if cc and not fail:
    le = re.search(r'static unsigned int sfxLe32\(.*?\n\}\n', snd, re.S).group(0)
    hm = re.search(r'static int sfxHeaderMs\(.*?\n\}\n', snd, re.S).group(0)
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        (td / 't.c').write_text('#include <string.h>\n#include <stdio.h>\n' + le + hm + r'''
static void put32(unsigned char *p, unsigned int v) { p[0] = v; p[1] = v >> 8; p[2] = v >> 16; p[3] = v >> 24; }
int main(void)
{
    unsigned char h[16] = "APCM";
    h[4] = 1; h[5] = 1;
    put32(h + 8, 4096);   /* pitch 4096: 48 kHz */
    put32(h + 12, 48000); /* one second */
    if (sfxHeaderMs(h, 30000) < 999 || sfxHeaderMs(h, 30000) > 1001) return 1;
    put32(h + 8, 2048);   /* 24 kHz: two seconds */
    if (sfxHeaderMs(h, 30000) < 1999 || sfxHeaderMs(h, 30000) > 2001) return 2;
    put32(h + 8, 0);      /* no pitch: not playable */
    if (sfxHeaderMs(h, 30000) != 0) return 3;
    put32(h + 8, 4096);
    h[0] = 'X';           /* not an .adp */
    if (sfxHeaderMs(h, 30000) != 0) return 4;
    h[0] = 'A';
    if (sfxHeaderMs(h, 20) != 0) return 5; /* shorter than a header and a block */
    put32(h + 12, 0);     /* no count: from the blocks, 28 samples in each 16 bytes */
    if (sfxHeaderMs(h, 16 + 16 * 1715) < 999 || sfxHeaderMs(h, 16 + 16 * 1715) > 1002) return 6;
    printf("ok\n");
    return 0;
}
''')
        exe = td / 't.exe'
        r = subprocess.run([cc, str(td / 't.c'), '-o', str(exe)], capture_output=True, text=True)
        if r.returncode:
            fail.append('sfxHeaderMs must build on the PC: ' + r.stderr[-300:])
        else:
            r = subprocess.run([str(exe)], capture_output=True, text=True)
            if r.returncode:
                fail.append('sfxHeaderMs failed check %d' % r.returncode)

print('\n'.join(fail) or 'build95: voices that know when they end, no built-in sounds, libc unshadowed, pictures from memory, JPG art OK')
sys.exit(1 if fail else 0)
