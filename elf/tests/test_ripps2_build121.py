"""Build 121 (the user, 10/28: the boot sound with the pillars when the sounds live on a drive): BIOS Sounds > Rip offers a
copy of boot.adp beside RIPPS2 on its memory card, and the boot reads that copy before a drive's AUDIO folder. Audio still
comes up at the end of init (bringing it up before applyConfig stopped the boot on the sky in the lab).

Static checks on the patched tree."""
import os
import sys
from pathlib import Path
from r2src import unwrap  # noqa: E402

root = Path(os.environ.get('RIPTOPL_DIR', '.'))
rd = lambda p: unwrap((root / p).read_text(encoding='utf-8').replace('\r\n', '\n'))
fail = []


def body(text, head):
    i = text.index(head)
    return text[i:text.index('\n}\n', i) + 3]


snd = rd('src/sound.c')
path = body(snd, 'int sfxCardBootPath(char *out, int size)')
if 'strncmp(dir, "mc", 2) != 0' not in path or "dir[2] == '?'" not in path:
    fail.append('sfxCardBootPath: only RIPPS2 started from a memory card, mc? resolved to the card with its folder')
early = body(snd, 'static void sfxBootEarlyWork(void)')
card, drive = early.find('sfxCardBootPath(path'), early.find('ripps2AudioBase(base')
if card < 0 or drive < 0 or card > drive:
    fail.append('sfxBootEarlyWork: the card copy is read before a drive\'s AUDIO folder')
if 'sfxLoad(' in early.replace('sfxBootEarlyUpload', ''):
    fail.append('sfxBootEarlyWork: the send to the SPU stays sfxBootEarlyUpload\'s')

opl = rd('src/opl.c')
# audio up only at the end of init: with it up during applyConfig, bgmMute / bgmUnMute called audsrv from the main thread
# while the IO worker sent the boot sound through the same RPC client (the lab: stuck on the sky)
q = opl.index('sfxBootEarlyQueue(themeID);')
if 'sfxBootStart();' in opl[q - 300:opl.index('applyConfig(themeID, langID, 0);', q)]:
    fail.append('_loadConfig: no audio start before applyConfig (audsrv from two threads)')
if 'sfxBootStart(); // RIPPS2: the boot sound, as the towers start to rise' not in opl:
    fail.append('init: audio up at its end, after applyConfig')

bs = rd('src/ripps2biossnd.c')
offer = body(bs, 'static void rbsOfferCardBoot(const char *dir)')
for s, why in (('!strncmp(dir, "mc", 2) || !sfxCardBootPath(dst, sizeof(dst))', 'only sounds on a drive, RIPPS2 on a card'),
               ('freeKb < needKb', 'no offer without the room'),
               ('"COPY"', 'START copies'),
               ('remove(dst);', 'a short write is removed')):
    if s not in offer:
        fail.append('rbsOfferCardBoot: ' + why)
rip = body(bs, 'void ripps2RipBiosSoundsDialog(void)')
if 'rbsOfferCardBoot(dir);' not in rip:
    fail.append('ripps2RipBiosSoundsDialog: the offer after the rip')

if fail:
    print('\n'.join(fail))
    sys.exit(1)
print('build 121: ok')
