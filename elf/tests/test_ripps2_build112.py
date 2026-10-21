"""Build 112: BIOS Music rips the menu's own piece. Build 100 ripped SNDWARNS, the red screen's (the "Please insert
a PlayStation or PlayStation 2 format disc" warning: its tense opening chord, then waves); the browser's main menu
plays SNDCLOKS, the clock's (user: "i think were using the error red screen menu instead of the standard osdsys menu
theme ... make it so you can select one other or both ripped ... make the osdsys one the default").

Static checks on the patched tree, and the new words in every language."""
import os
import re
import sys
from pathlib import Path

root = Path(os.environ.get('RIPTOPL_DIR', '.'))
rd = lambda p: (root / p).read_text(encoding='utf-8')
rip, hdr = rd('src/ripps2biossnd.c'), rd('include/ripps2biossnd.h')
fail = []

# ---- the two pieces, the menu's first
if '#define RBS_MENU_SEQ      "SNDCLOKS"' not in rip or 'RBS_MUSIC_SEQ     "SNDWARNS"' not in rip:
    fail.append('ripps2biossnd.c: the menu is SNDCLOKS (the clock), the red screen SNDWARNS')
m = re.search(r'rbsPiece\[RIPPS2_BIOSMUSIC_COUNT\] = \{\{(\w+), (\w+), (\w+)\}, \{(\w+), (\w+), (\w+)\}\};', rip)
if not m or m.groups() != ('RBS_MENU_SEQ', 'RBS_MENU_WET', 'RBS_MENU_GAIN', 'RBS_MUSIC_SEQ', 'RBS_MUSIC_WET', 'RBS_MUSIC_GAIN'):
    fail.append('ripps2biossnd.c: rbsPiece lists the menu, then the red screen, each with its own hall and gain')
if 'enum { RIPPS2_BIOSMUSIC_MENU = 0, RIPPS2_BIOSMUSIC_RED, RIPPS2_BIOSMUSIC_COUNT };' not in hdr:
    fail.append('ripps2biossnd.h: the pieces, the menu first')
for f in ('int ripps2BiosMusicSamplesOf(const unsigned char *img, int size, int piece);',
          'int ripps2BiosMusicFromImageOf(const unsigned char *img, int size, int piece, ripps2_biosmusic_put_t put, void *ctx);'):
    if f not in hdr:
        fail.append('ripps2biossnd.h: ' + f.split('(')[0])
# the clock's levels, measured as build 100 measured the red screen's (its own numbers reproduce exactly)
if '#define RBS_MENU_WET      0.0781f' not in rip or '#define RBS_MENU_GAIN     1.5812f' not in rip:
    fail.append("ripps2biossnd.c: the clock's hall 0.0781 and gain 1.5812 (ripps2BiosMusicMeasure)")
if '#define RBS_MUSIC_WET     0.0807f' not in rip or '#define RBS_MUSIC_GAIN    1.3875f' not in rip:
    fail.append("ripps2biossnd.c: the red screen's levels stay build 100's")
if 'return ripps2BiosMusicSamplesOf(img, size, RIPPS2_BIOSMUSIC_RED);' not in rip or \
        'return ripps2BiosMusicFromImageOf(img, size, RIPPS2_BIOSMUSIC_RED, put, ctx);' not in rip:
    fail.append("ripps2biossnd.c: build 100's two calls are the red screen's")
if 'rbsMusicOpen(img, size)' in rip or 'static rbs_music_t *rbsMusicOpen(const unsigned char *img, int size, const char *seq)' not in rip:
    fail.append('ripps2biossnd.c: the piece is opened by its sequence')

# ---- the files: the menu's is the Menu track the list plays by default
if '#define RBS_MUSIC_FILE "bgm_00 Menu.wav"' not in rip or '#define RBS_RED_FILE   "bgm_01 Red Screen.wav"' not in rip:
    fail.append('ripps2biossnd.c: bgm_00 Menu.wav (the default track) and bgm_01 Red Screen.wav')

# ---- the chooser: the menu first and chosen, the red screen, both
pick = rip[rip.index('static int rbsPickMusic('):rip.index('static int rbsRipPiece(')]
if 'N_("THE MENU MUSIC (THE CLOCK)"), N_("THE RED SCREEN MUSIC (DISC WARNING)"), N_("BOTH")' not in pick or 'int sel = 0,' not in pick:
    fail.append('rbsPickMusic: THE MENU MUSIC first and highlighted, THE RED SCREEN MUSIC, BOTH')
dlg = rip[rip.index('void ripps2RipBiosMusicDialog(void)'):]
if 'if ((want = rbsPickMusic(len)) == 0) {' not in dlg:
    fail.append('ripps2RipBiosMusicDialog: the chooser comes before the folder question, and backing out rips nothing')
if 'rbsRipPiece(img, imgSize, k, len[k], dirs[pick - 1], done[k], sizeof(done[k]));' not in dlg:
    fail.append('ripps2RipBiosMusicDialog: each chosen piece is ripped into the folder picked')
if 'bgmStop(); // the music may be playing this very file' not in dlg:
    fail.append('ripps2RipBiosMusicDialog: the music lets go of a file it may be playing before it is rewritten')
if 'remove(path); // never a short WAV left behind' not in rip:
    fail.append('rbsRipPiece: a failed piece leaves no short WAV')

# ---- the new words, every language
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'lang'))
import ripps2lang  # noqa: E402
new = ['WHICH MUSIC?', 'THE MENU MUSIC (THE CLOCK)', 'THE RED SCREEN MUSIC (DISC WARNING)',
       "Ripping this console's red screen music: %d%%",
       'The red screen music (%s) is in %s as %s. Audio settings > Music lists it as Red Screen.']
langdir = Path(__file__).resolve().parents[1] / 'lang'
for f in sorted(langdir.glob('*.yml')):
    if f.name.startswith('_'):
        continue
    mine, _ = ripps2lang.ripps2_translations(f.stem)
    missing = [k for k in new if not mine.get(k)]
    reds = [k for k in mine if k.startswith("RIPPS2 plays this console's red screen music") or
            k.startswith("RIPPS2 plays this console's menu music (%d:%02d) and its red screen music")]
    if missing or len(reds) != 4:
        fail.append('%s: the chooser, the progress, the result and the four rip questions (%d missing, %d of 4)' % (f.stem, len(missing), len(reds)))

print('\n'.join(fail) or 'build112: the menu music is the clock\'s, the red screen\'s beside it, chosen per rip, in every language OK')
sys.exit(1 if fail else 0)
