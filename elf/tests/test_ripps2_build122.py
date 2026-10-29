"""Build 122 (the user, 10/28: the boot sound sooner): audio comes up right after _loadConfig, once applyConfig's
bgmMute / bgmUnMute are done, instead of after the fonts and the languages at the end of init. Never before applyConfig
(build 121 stopped on the sky that way: audsrv from two threads).

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


opl = rd('src/opl.c')
load = body(opl, 'static void _loadConfig()')
if 'sfxBootStart();' in load:
    fail.append('_loadConfig: no audio start in it (applyConfig\'s bgmMute / bgmUnMute and the IO worker\'s send met in audsrv)')
init = body(opl, 'static void init(void)')
cfg = init.find('_loadConfig();')
early = init.find('sfxBootStart();', cfg)
fonts = init.find('lngInitFallbackFont();')
if cfg < 0 or early < 0 or fonts < 0 or not cfg < early < fonts:
    fail.append('init: audio up right after _loadConfig, before the fonts and the languages')
if init.count('sfxBootStart();') != 2:
    fail.append('init: the end-of-init call stays for a boot with the settings skipped (START)')

snd = rd('src/sound.c')
start = body(snd, 'void sfxBootStart(void)')
if 'static int done' not in start:
    fail.append('sfxBootStart: runs once (the second call is a no-op)')

if fail:
    print('\n'.join(fail))
    sys.exit(1)
print('build 122: ok')
