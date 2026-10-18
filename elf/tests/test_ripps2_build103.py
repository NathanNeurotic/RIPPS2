"""Build 103: RiptOPL upstream 3cd7f89 merged, and a version line that names it. Static checks on the patched tree."""
import os
import re
import sys
from pathlib import Path
from r2src import unwrap, TR_STUBS  # noqa: E402

root = Path(os.environ.get('RIPTOPL_DIR', '.'))
here = Path(__file__).resolve().parents[1]  # elf/
rd = lambda p: unwrap((root / p).read_text(encoding='utf-8').replace('\r\n', '\n'))  # build 104: as before _t
fail = []

# 1. the version: the upstream merged (commit + revision) goes to make; the build number's digits to the header
up = (here / 'RIPTOPL_UPSTREAM').read_text().split()
if len(up) != 2 or not re.fullmatch(r'[0-9a-f]{40}', up[0]) or not up[1].isdigit():
    fail.append('elf/RIPTOPL_UPSTREAM must hold the full upstream commit and its revision')
build = (here / 'build.sh').read_text()
if 'REVISION="$UP_REV" GIT_HASH="$UP_HASH"' not in build or 'checkout -q FETCH_HEAD -- third_party/mbedtls' not in build:
    fail.append('build.sh must name the merged upstream in the version and take vendored mbedTLS from it')
if '#define RIPPS2_VERSION "%s"' not in build:
    fail.append('build.sh must write RIPPS2_VERSION from the build number')
gui, about = rd('src/gui.c'), rd('src/ripps2about.c')
if 'static const char *guiRipps2Version(void)' not in gui or gui.count('guiRipps2Version()') < 2:
    fail.append('the Settings hub and the boot screen must show RIPPS2 and the RiptOPL it carries')
if '"%s, BUILD %d", RIPPS2_VERSION, RIPPS2_BUILD' not in about:
    fail.append("About's release line must give the version and the build")

# 2. the in-game menu kept inside upstream's reworked IGR thread (RA builds use the VBLANK handler)
pad = rd('ee_core/src/padhook.c')
thread = pad[pad.index('static void IGR_Thread(void *arg)'):]
if thread.index('#ifdef IGR_VBLANK_HANDLER') > thread.index('choice = IGR_MenuRun(IGR_PadButtons);') or \
        pad.count('static void IGR_StopDmaAndGs(void)') != 1:
    fail.append('the in-game menu loop must sit in the VBLANK-handler branch, with one IGR_StopDmaAndGs')
if 'ra_count_unlocks(e); /* RIPPS2 build 87 */' not in rd('ee_core/src/ra_overlay.c'):
    fail.append("the in-game menu's unlock count must read every RA event before upstream's overlay branch")

# 3. RIPGRID keeps nThemes + 2 and its own colours; no built-in PSBBN Flow
th = rd('src/themes.c')
if '<PSBBN Flow>' in th or 'gLoadPsbbnFlowBuiltin' in th:
    fail.append('RIPPS2 has no built-in PSBBN Flow (nThemes + 2 is RIPGRID)')
if '} else if (guiThemeID == 0 || guiThemeID == nThemes + 1) {' not in th:
    fail.append("the settings' palette must never be laid over RIPGRID")

# 4. Show Recents on upstream's crash-safe favourites I/O
fav = rd('src/favsupport.c')
if 'return favReadPath(path, outCount, &complete, 0);' not in fav or 'ok = favWriteWhole(path, img, len);' not in fav:
    fail.append('recents.bin must be read and written through the whole-file reader and writer')

# 5. RIPPS2's words: Starred Games, and no label twice
base = rd('lng_tmpl/_base.yml')
labels = re.findall(r'^- label: ([A-Z0-9_]+)$', base, re.M)
dups = sorted({l for l in labels if labels.count(l) > 1})
if dups:
    fail.append('labels defined twice: %s' % ', '.join(dups[:6]))
if 'Saved to Favorites' in base:
    fail.append('upstream\'s favourites notices must say Starred Games')

if fail:
    print('\n'.join(fail))
    sys.exit(1)
print('build103: version names RIPPS2 and the RiptOPL merged, in-game menu in the new IGR thread, RIPGRID colours, '
      'recents on safe I/O, Starred Games words OK')
