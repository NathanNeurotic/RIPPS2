"""Build 111: the user's notes of 10/21 and tester lukeatmynose's build 110 report. Music on every theme (a disk theme
without its own bgm.ogg played nothing) and the ripped Menu music at all (24 kHz mono, which audsrv refuses: the reader
gives it 48 kHz stereo); Save Settings To keeps a drive with a memory card in; the same sound set is not loaded again
(every load keys every voice off and writes the sounds back one by one, seconds from a memory card: "simplify the audio
approach for 0 bugs on real hardware"); the favourites star on its title's centreline; the Settings highlight centred
on the word.

Static checks on the patched tree."""
import os
import re
import sys
from pathlib import Path

root = Path(os.environ.get('RIPTOPL_DIR', '.'))
rd = lambda p: (root / p).read_text(encoding='utf-8')
sound, themes, dia = rd('src/sound.c'), rd('src/themes.c'), rd('src/dia.c')
fail = []

# ---- music on every theme
load = sound[sound.index('static int bgmLoad(void)'):sound.index('static int bgmInit(void)')]
if 'thmPath == NULL && bgmMusicPath(' in load or 'if (bgmMusicPath(bgmPath, sizeof(bgmPath))) {' not in load:
    fail.append("bgmLoad: RIPPS2's music pick on every theme, not only the built-in ones")
if load.index('"theme"') > load.index('bgmMusicPath(bgmPath') or load.index('"configured"') > load.index('bgmMusicPath(bgmPath'):
    fail.append("bgmLoad: a disk theme's own bgm.ogg and the configured file still come first")

# ---- music audsrv cannot take is converted as it plays (the BIOS Music rip: 24 kHz mono, "no music")
wav = sound[sound.index('static int wavNextFrame(short *out)'):sound.index('static void wavClose(void)')]
if 'static int wavRead(char *buf, int size)' not in wav or 'out[1] = wavSrcCh == 2 ?' not in wav:
    fail.append('wavRead: a mono frame goes to both sides')
if '((unsigned long long)wavSrcRate << 16) / 48000' not in wav or 'wavPrev[0] + (int)(((long long)(wavCur[0] - wavPrev[0]) * f) >> 16)' not in wav:
    fail.append('wavRead: another rate is interpolated to 48 kHz')
wopen = sound[sound.index('static int wavOpen(const char *path)'):sound.index('// PCM bytes the stream plays per millisecond')]
if 'wavSrcRate = bgmPcmRate;' not in wopen or 'bgmPcmRate = 48000;\n            bgmPcmChannels = 2;' not in wopen:
    fail.append('wavOpen: audsrv is given 48 kHz stereo whatever the file holds')
if 'bgmPcmRate < 4000 || bgmPcmRate > 96000' not in wopen:
    fail.append('wavOpen: a rate outside 4-96 kHz is refused')

# ---- Save Settings To keeps the chosen home with a card in (tester lukeatmynose)
opl, ui = rd('src/opl.c'), rd('src/ripps2ui.c')
rcp = opl[opl.index('static int readConfigPathRedirect('):opl.index('static int writeConfigPathRedirect(')]
if 'fd = ripps2CardRedirectOpen(); // RIPPS2 build 111' not in rcp:
    fail.append("readConfigPathRedirect: a card's RIPPS2 pointer is read when config.path is out of reach")
wcp = opl[opl.index('static int writeConfigPathRedirect('):opl.index('static int prepareCustomApaSettingsPath(')]
if 'ripps2CardRedirectWrite(path); // RIPPS2 build 111' not in wcp:
    fail.append('writeConfigPathRedirect: a save to another home leaves the pointer in each RIPPS2 card save')
if 'if (onCard && lscret > 0 && gRipps2HomeBackToCard) {\n        ripps2ForgetRedirect();' not in opl:
    fail.append('_saveConfig: Memory Card chosen again takes config.path and the card pointers away')
if 'gRipps2HomeBackToCard = 1;' not in ui:
    fail.append('ripps2SettingsHomeEnd: a drive changed back to Memory Card is remembered for the save')

# ---- the same sound set is not loaded again
init = sound[sound.index('int sfxInit(int bootSnd)'):sound.index('// Build 95: a fresh load of the sounds')]
if 'static unsigned int sfxSetSignature(const char *themeDir, const char *audioDir)' not in sound:
    fail.append("sound.c: the set signature (each event file's path, size and date)")
sig = sound[sound.index('static unsigned int sfxSetSignature('):sound.index('int sfxInit(int bootSnd)')]
if 'covered = fromTheme[f];' not in sig or 'found = fromTheme[i] = stat(path, &st) == 0;' not in sig:
    fail.append('sfxSetSignature: the file each event loads, chosen as sfxInit chooses (two disk themes playing the AUDIO folder are one set)')
m = re.search(r'if \(!bootSnd && sfxSetGen == audioGen && sig == sfxSetSig\) \{', init)
if not m:
    fail.append('sfxInit: the same set, with audsrv not started again since, is not loaded again')
elif init.index('audsrv_adpcm_init();') < m.start():
    fail.append('sfxInit: the check comes before anything is keyed off')
if 'sfxSetSig = sig;' not in init or 'sfxSetGen = audioGen;' not in init:
    fail.append('sfxInit: a load remembers its set')
if 'audioGen++;' not in sound:
    fail.append('audioInit: an audsrv start (an IOP reboot) means every sound loads again')
if sound.count('audsrv_adpcm_init();') - 1 != sound.count('sfxSetGen = (unsigned int)-1; // build 111'):
    fail.append('every audsrv_adpcm_init outside sfxInit (the preview, its close, the late init) forgets the set')

# ---- the star on its title's centreline
if 'rowTop + (rowStep - MENU_ITEM_HEIGHT) / 2, elem->aligned,' not in themes:
    fail.append("drawItemsList: the star is centred on its row (the title's centreline), not at the icons' posY")

# ---- the Settings highlight on the word
box = dia[dia.index('static void diaDrawBoundingBox('):dia.index('static int diaKeybTextWidth(')]
if 'fntCenterOffset(RIPPS2_DIA_FONT, ALIGN_NONE)' not in box or 'rmDrawRect(x - 5, y - 3' in box:
    fail.append("diaDrawBoundingBox: the highlight is centred on the letters' centreline")

print('\n'.join(fail) or 'build111: music on every theme and any .wav, Save Settings To with a card in, the same sound set '
      'not loaded again, the star and the Settings highlight on their words OK')
sys.exit(1 if fail else 0)
