"""Build 100: the build 99 notes (user, 10-12). Static checks on the patched tree."""
import math
import os
import shutil
import struct
import subprocess
import sys
import tempfile
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

# Sound: the boot and launch rips (user: "spitty pops"). Programs 60 to 62 were read as the SPU2 noise and played
# as a random level held for a tenth of a second; they are the bank's first sample (address 0)
rip = rd('src/ripps2biossnd.c')
studio = (Path(__file__).resolve().parents[2] / 'tools/audio-studio/ps2bios.py').read_text(encoding='utf-8')
if 'tn->noise' in rip or 'RBS_NOISE_BASE' in rip or 'noise_voice' in studio or "noise=not (t[15] & 1)" in studio:
    fail.append('no sequence tone is the SPU2 noise: programs 60 to 62 play the sample at address 0')

# Sound: the beep after the save modals. audsrv_adpcm_init turns every voice up to full, so every voice goes silent
# right after it, and only a sounding voice is turned up again
snd = rd('src/sound.c')
if snd.count('audsrv_adpcm_init();\n    voicesReset();\n    voicesSilence();') != 3 or 'if (!voiceMuted[v] && voiceBusy(v))' not in snd or \
        'if (voiceBusy(SFX_BOOT_VOICE))' not in snd:
    fail.append('after every audsrv init each voice must go silent, and audioSetVolume turn up only a sounding voice')

# Sound: one press, one sound
if 'void sfxFlush(void)' not in snd or 'sfxPendingId = id; // what it opens may still sound this frame' not in snd or \
        'sfxPendingId = -1; // what the press opened sounds instead' not in snd or 'SFX_DRIVE_ANSWER_MS' not in snd:
    fail.append('a confirm or cancel must wait for its frame, and what it opened sound instead')
pad = rd('src/pad.c')
if 'sfxFlush(); // build 100' not in pad[pad.index('int readPads()'):pad.index('int readPads()') + 400] or \
        'sfxFlush(); // build 100' not in gui[gui.index('void guiEndFrame(void)'):gui.index('void guiEndFrame(void)') + 200]:
    fail.append('readPads and guiEndFrame must play a waiting press sound')
prompt = gui[gui.index('static int guiSettingsPromptSave(void)'):gui.index('static void guiDrawSettingsIndexHints')]
if 'sfxPlay(SFX_CONFIRM)' in prompt or 'if (id != MENU_SAVE_CHANGES)' not in menu or 'if (selected != saveRow)' not in gui:
    fail.append('a save must sound once, with its own box')
note = gui[gui.index('static void guiShowNotifications(void)'):gui.index('static void guiShowNotifications(void)') + 900]
if 'sfxPlay(' in note or 'sfxPlay(SFX_PAGE_IN)' in th:
    fail.append('the drive scan notifications and the right stick case flip must be silent')
dia = rd('src/dia.c')
if 'diaResetValue(item);\n        sfxPlay(SFX_CANCEL);' not in dia:
    fail.append('Circle on a focused value must sound as a cancel')

# Sound: the menu music, a rip of its own (its size said first, beside RIPPS2 or OPL's resources AUDIO), and the music
# list reading OPL's resources AUDIO on each started drive
for name in ('ripps2BiosMusicFromImage', 'ripps2BiosMusicSamples', 'ripps2RipBiosMusicDialog', 'RBS_MUSIC_SEQ     "SNDWARNS"'):
    if name not in rip:
        fail.append('the menu music rip needs %s' % name)
if 'RIPPS2_RIP_MUSIC_BUTTON' not in rd('src/dialogs.c') or 'ripps2RipBiosMusicDialog();' not in gui or \
        'label: RIPPS2_BIOS_MUSIC' not in rd('lng_tmpl/_base.yml'):
    fail.append('Audio settings must offer BIOS Music > RIP')
for f in ('src/bdmsupport.c', 'src/hddsupport.c', 'src/mmcesupport.c'):
    if 'bgmAddMusicHome(' not in rd(f):
        fail.append('%s must register its OPL root for the music list' % f)
if 'void bgmAddMusicHome(const char *prefix)' not in snd or 'snprintf(sub, sizeof(sub), "%sAUDIO", bgmHomes[i]);' not in snd:
    fail.append('the music list must read OPL\'s resources AUDIO too')

# Save: RIPPS2's own save on the memory card, the hat lighter
opl = rd('src/opl.c')
if opl.count('ripps2CardSettingsHome(cardHome, sizeof(cardHome)') != 2 or 'configSetMove(prevHome);' not in opl:
    fail.append('the settings must load from and save to RIPPS2\'s own save on a memory card')
icn = (root / 'misc/ripps2.icn').stat().st_size
if icn > 60000:
    fail.append('the hat icon must stay small (%d bytes)' % icn)


def lz_literals(data):
    out = bytearray(struct.pack('<I', len(data)))
    for i in range(0, len(data), 30):
        out += b'\0\0\0\0' + data[i:i + 30]
    return bytes(out)


def adpcm_tone(loop=False):
    out = bytearray()
    for b in range(40):
        nibs = [int(round(7 * math.sin(2 * math.pi * (b * 28 + i) / 14))) & 0xF for i in range(28)]
        flags = (4 if loop and b == 0 else 0) | ((3 if loop else 1) if b == 39 else 0)
        out += bytes([0x08, flags]) + bytes(nibs[i] | nibs[i + 1] << 4 for i in range(0, 28, 2))
    return bytes(out)


def romdir(files):
    files = [('RESET', b'\0' * 16), ('ROMDIR', b'')] + files
    for _ in range(2):
        entries = b''.join(struct.pack('<10sHI', n.encode(), 0, len(d)) for n, d in files) + b'\0' * 16
        files[1] = ('ROMDIR', entries)
    img = bytearray()
    for _, d in files:
        img += d + b'\0' * (-len(d) % 16)
    return bytes(img)


def music_image():
    """A one-instrument bank and a 'menu piece' of 40 notes, 1.5 s apart (60 s), each held a second."""
    bank = bytearray(0x20 + 4 + 8 + 16)
    struct.pack_into('<I', bank, 0x10, 0x20)
    struct.pack_into('<HH', bank, 0x20, 0, 4)
    p = 0x24
    bank[p:p + 3] = bytes([0, 127, 64])
    t = p + 8
    bank[t + 1], bank[t + 2], bank[t + 3] = 127, 60, 0
    struct.pack_into('<HHH', bank, t + 4, 0, 0x000F, 0x0000)
    bank[t + 10], bank[t + 11], bank[t + 12], bank[t + 15] = 0, 127, 64, 1
    seq = bytearray(0x110)
    struct.pack_into('<HHH', seq, 0, 127, 480, 120)  # 120 quarter notes a minute: a quarter is 0.5 s
    for c in range(16):
        seq[0x10 + c * 16 + 1:0x10 + c * 16 + 5] = bytes([c, 0, 100, 64])
    ev = bytearray([0x90, 60, 100])
    for k in range(40):
        ev += bytes([0x87, 0x40, 0x80, 60, 0])         # a second (960 ticks), then off
        ev += bytes([0x83, 0x60, 0x90, 60 + k % 5, 100])  # half a second, then the next on
    ev += bytes([0x87, 0x40, 0x80, 60, 0, 0x00, 0xFF, 0x2F, 0x00])
    seq += ev
    return romdir([('SNDBOOTH', lz_literals(bytes(bank))), ('SNDBOOTB', lz_literals(adpcm_tone(loop=True))),
                   ('SNDWARNS', lz_literals(bytes(seq)))])


cc = shutil.which('gcc') or shutil.which('cc')
if cc and not fail:
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        (td / 'img.bin').write_bytes(music_image())
        (td / 'm.c').write_text(r"""
#include <stdio.h>
#include <stdlib.h>
#include "include/ripps2biossnd.h"
static long got, peakAt;
static int peak;
static int put(const short *pcm, int n, int done, int total, void *ctx)
{
    int k;
    (void)ctx;
    if (n <= 0 || done > total) return -1;
    for (k = 0; k < n; k++)
        if (abs(pcm[k]) > peak) { peak = abs(pcm[k]); peakAt = got + k; }
    got += n;
    return 0;
}
int main(int argc, char **argv)
{
    static unsigned char d[1 << 20];
    FILE *f = fopen(argv[1], "rb");
    int n = (int)fread(d, 1, sizeof(d), f), want, made;
    fclose(f);
    want = ripps2BiosMusicSamples(d, n);
    made = ripps2BiosMusicFromImage(d, n, put, NULL);
    printf("%d %d %ld %d\n", want, made, got, peak);
    return want > 24000 * 60 && made == want && got == want && peak > 100 ? 0 : 2; // the gain is the real piece's: a made-up one is quieter
}
""")
        exe = td / 'm.exe'
        r = subprocess.run([cc, '-DRIPPS2_BIOSSND_HOST_TEST', '-I', str(root), str(td / 'm.c'), str(root / 'src/ripps2biossnd.c'),
                            '-o', str(exe), '-lm'], capture_output=True, text=True)
        if r.returncode:
            fail.append('the music ripper must build on the PC: ' + r.stderr[-400:])
        else:
            r = subprocess.run([str(exe), str(td / 'img.bin')], capture_output=True, text=True)
            if r.returncode:
                fail.append('the music ripper must stream a made-up piece whole (%d): %s' % (r.returncode, r.stdout.strip()))

if fail:
    print('\n'.join(fail))
    sys.exit(1)
print('build100: viewer turn, editor face, flip direction, menu face, clean replace, ISO where it sits, POPSTARTER answer, rips without noise pops, no beep, one press one sound, the menu music rip, OPL AUDIO folders, the card save OK')
