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

print('\n'.join(fail) or 'build98: card slots kept, thorough delete, CARD FULL up front, sounds theme then AUDIO OK')
sys.exit(1 if fail else 0)
