"""Build 100: the build 99 notes (user, 10-12). Static checks on the patched tree."""
import os
import sys
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

if fail:
    print('\n'.join(fail))
    sys.exit(1)
print('build100: viewer turn, editor face, flip direction, menu face, clean replace, ISO where it sits, POPSTARTER answer, rips without noise pops, no beep, one press one sound OK')
