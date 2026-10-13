"""Build 101: the user's notes on the v1.0.0 beta (10/13/2026). Static checks on the patched tree."""
import os
import re
import sys
from pathlib import Path

root = Path(os.environ.get('RIPTOPL_DIR', '.'))
rd = lambda p: (root / p).read_text(encoding='utf-8').replace('\r\n', '\n')
fail = []

# RIPFLOW's info page: Left / Right are its games (as on its carousel), never a drive
menu = rd('src/menusys.c')
info = menu[menu.index('void menuHandleInputInfo()'):menu.index('void menuRenderGameMenu()')]
left, right, drive = (info.find('gTheme->coverflow && getKey(KEY_LEFT)'), info.find('gTheme->coverflow && getKey(KEY_RIGHT)'),
                      info.find('menuDriveStep(-1);'))
if left < 0 or right < 0 or drive < 0 or not (left < right < drive):
    fail.append("RIPFLOW's info page must take Left / Right for its games before the drive step")
elif 'menuPrevV();' not in info[left:right] or 'menuNextV();' not in info[right:drive]:
    fail.append("RIPFLOW's info page: Left must be the previous game, Right the next")

# the sound set's loads: the GUI touches no voice while one waits or runs, a held sound plays only in its moment
snd = rd('src/sound.c')
def body(name):  # a function's definition (its name, then its brace on the next line); '' when it is not there
    i = snd.find(name + '\n{')
    return snd[i:snd.index('\n}\n', i)] if i >= 0 else ''
init, play, flush, held, vol = body('int sfxInit(int bootSnd)'), body('void sfxPlay(int id)'), body('void sfxFlush(void)'), \
    body('static void sfxPlayHeld(void)'), body('void audioSetVolume(void)')
if 'return sfxReloadQueued || sfxReloadBusy || sfxLoading;' not in snd:
    fail.append('a load must count as busy while it is queued, while its reload runs and while sfxInit runs')
i_load, i_quiet, i_init = init.find('sfxLoading = 1;'), init.find('voicesSilence();'), init.find('audsrv_adpcm_init();')
if not (0 <= i_load < i_init and 0 <= i_quiet < i_init) or 'sfxLoading = 0;' not in init[i_init:]:
    fail.append('sfxInit must flag its load and quiet every voice before the init turns them up, and clear the flag at the end')
if 'sfxForgetPresses();' not in init[:i_init if i_init > 0 else 0]:
    fail.append('sfxInit must forget which voice the earlier sounds took before it keys them off')
busy = play.find('if (sfxSetBusy()) {')
if busy < 0 or 'sfxHold(asked);' not in play[busy:busy + 300] or busy > play.find('sfxPlayNow(id);'):
    fail.append('sfxPlay must hold a one-shot and drop the rest while the set loads, before any voice is touched')
if 'sfxHold(id);' not in flush or 'sfxPlayAfterLoad = id;' in flush:
    fail.append('the end-of-frame flush must hold a press caught by a load, never keep it to the end of the load')
if 'SFX_HELD_FRESH_MS' not in held:
    fail.append('a held sound must play after the load only within SFX_HELD_FRESH_MS of its press')
m = re.search(r'#define SFX_HELD_FRESH_MS (\d+)', snd)
if not m or not 100 <= int(m.group(1)) <= 500:
    fail.append('SFX_HELD_FRESH_MS must be a press-sized moment (100 to 500 ms)')
if 'static u32 lastCursorTicks' in body('static void sfxPlayNow(int id)'):
    fail.append("sfxPlayNow's memory of the last sounds must be file-wide, so a load can forget it")
if 'if (!sfxSetBusy()) {' not in vol:
    fail.append('the volume sliders must leave the voices alone while the set loads')
if '(sfxReloadBusy || sfxLoading) && i < 400' not in snd:
    fail.append("Memory Files' preview must wait for any load, the late AUDIO find included")
if 'if (thenPlay >= 0)' not in body('void sfxReload(int thenPlay)'):
    fail.append("a second reload must not drop the first one's sound (a rip's confirm)")

if fail:
    print('\n'.join(fail))
    sys.exit(1)
print("build101: RIPFLOW's info page steps games, the sound loads gate the GUI, held sounds only in their moment OK")
