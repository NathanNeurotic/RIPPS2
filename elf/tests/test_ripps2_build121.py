"""Build 121 (the user, 10/28: the boot sound with the pillars when the sounds live on a drive): BIOS Sounds > Rip offers a
copy of boot.adp beside RIPPS2 on its memory card, the boot reads that copy before a drive's AUDIO folder, and audio comes
up on the main thread with the settings read, before the IO worker has its first job (the boot sound's send stays the IO
worker's).

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
i = opl.index('sfxBootEarlyQueue(themeID);')
seg = opl[i - 300:i]
if 'sfxBootStart();' not in seg:
    fail.append('_loadConfig: audio up (sfxBootStart) before the boot sound is queued')
if opl.index('sfxBootStart();', i - 300) > opl.index('applyConfig(themeID, langID, 0);', i):
    fail.append('_loadConfig: audio up before applyConfig gives the IO worker the drives')
start = body(snd, 'void sfxBootStart(void)')
if 'if (done)\n        return;' not in start:
    fail.append('sfxBootStart: once (init\'s own call after the boot finds it done)')

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
