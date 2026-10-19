"""Build 104: languages. ripps2tr.c compiled on the host against a keyed language file, plus static checks on the tree."""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(os.environ.get('RIPTOPL_DIR', '.'))
here = Path(__file__).resolve().parent
lang_dir = here.parent / 'lang'
sys.path.insert(0, str(lang_dir))
import ripps2lang  # noqa: E402

rd = lambda p: (root / p).read_text(encoding='utf-8').replace('\r\n', '\n')
fail = []

# 1. the lookup, compiled as the ELF has it
STUB_OPL = r'''
#include <stdint.h>
#include <tamtypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define LOG(...)
'''
STUB_TAM = r'''
#include <stdint.h>
typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;
'''
samples = {
    'COPY': 'COPIER',
    'Delete %d items?': 'Supprimer %d éléments ?',
    '%d new, %d not in the collection, %d failed': '%d nouvelles, %s absentes',  # refused: a %s for a %d
    'Line one\nLine two': 'Ligne un\nLigne deux\tfin \\ ok',
    'Ripping: 0%': 'Extraction : 0%',
}
keyed = ['# a test file', ripps2lang.MARK]
for en, tr in samples.items():
    keyed.append('%08x\t%s' % (ripps2lang.fnv1a(en), ripps2lang.escape_line(tr)))
keyed_text = '\r\n'.join(keyed) + '\r\n'  # CR LF, as a file saved on Windows

HARNESS = r'''
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "include/ripps2tr.h"
static char *slurp(const char *path, int *n)
{
    FILE *f = fopen(path, "rb");
    assert(f != NULL);
    fseek(f, 0, SEEK_END);
    *n = (int)ftell(f);
    fseek(f, 0, SEEK_SET);
    char *b = malloc(*n);
    assert(fread(b, 1, *n, f) == (size_t)*n);
    fclose(f);
    return b;
}
int main(int argc, char **argv)
{
    int n;
    char *buf = slurp(argv[1], &n);
    char out[64];
    assert(ripps2TrIsKeyed(buf, n));
    assert(!ripps2TrIsKeyed("LANG\nline two\n", 14));
    assert(strcmp(_t("COPY"), "COPY") == 0); // no catalogue: English
    ripps2TrCat_t *c = ripps2TrParse(buf, n, "mass:/LNG/lang_French.lng");
    assert(c != NULL);
    ripps2TrUse(c);
    assert(strcmp(_t("COPY"), "COPIER") == 0);
    assert(strcmp(_t("Delete %d items?"), "Supprimer %d \xc3\xa9l\xc3\xa9ments ?") == 0);
    assert(strcmp(_t("%d new, %d not in the collection, %d failed"), "%d new, %d not in the collection, %d failed") == 0);
    assert(strcmp(_t("Line one\nLine two"), "Ligne un\nLigne deux\tfin \\ ok") == 0);
    assert(strcmp(_t("NOT THERE"), "NOT THERE") == 0);
    assert(strcmp(_t("Ripping: 0%"), "Extraction : 0%") == 0); // a lone % at the end is text
    assert(ripps2TrLabel(c, "COPY") != NULL && ripps2TrLabel(c, "NOT THERE") == NULL);
    // the same file again: the catalogue it already has (pointers given out stay good)
    int n2;
    char *again = slurp(argv[1], &n2);
    assert(ripps2TrParse(again, n2, "mass:/LNG/lang_French.lng") == c);
    ripps2TrUse(NULL);
    assert(strcmp(_t("COPY"), "COPY") == 0);
    // letter case
    assert(ripps2Upper(0xE9) == 0xC9 && ripps2Lower(0xC9) == 0xE9); // e acute
    assert(ripps2Upper(0x142) == 0x141 && ripps2Lower(0x141) == 0x142); // l stroke (Polish)
    assert(ripps2Upper(0x15F) == 0x15E && ripps2Upper(0x131) == 'I'); // s cedilla, dotless i (Turkish)
    assert(ripps2Upper(0x219) == 0x218); // s comma (Romanian)
    assert(ripps2Upper(0x1EA1) == 0x1EA0 && ripps2Lower(0x1EA0) == 0x1EA1); // a dot below (Vietnamese)
    assert(ripps2Upper(0x3B1) == 0x391 && ripps2Upper(0x3C2) == 0x3A3 && ripps2Upper(0x3AC) == 0x386); // Greek
    assert(ripps2Upper(0x436) == 0x416 && ripps2Upper(0x451) == 0x401 && ripps2Lower(0x416) == 0x436); // Cyrillic
    assert(ripps2Upper(0x3042) == 0x3042); // kana: no case
    ripps2Utf8Upper("\xc3\xa9" "cran \xc5\x82\xc3\xb3" "d\xc5\xba", out, sizeof(out));
    assert(strcmp(out, "\xc3\x89" "CRAN \xc5\x81\xc3\x93" "D\xc5\xb9") == 0);
    // a copy never ends inside a letter
    ripps2Utf8Copy(out, 4, "ab\xc3\xa9");
    assert(strcmp(out, "ab") == 0);
    ripps2Utf8Copy(out, 5, "ab\xc3\xa9");
    assert(strcmp(out, "ab\xc3\xa9") == 0);
    // CJK lines break between characters, not before a closing mark, never inside a character
    const char *ja = "\xe3\x83\x95\xe3\x82\xa1\xe3\x82\xa4\xe3\x83\xab\xe3\x80\x82"; // fairu + ideographic full stop
    assert(ripps2Utf8BreakAt(ja, ja + 3) && !ripps2Utf8BreakAt(ja, ja + 4) && !ripps2Utf8BreakAt(ja, ja + 12));
    const char *latin = "abc def";
    assert(!ripps2Utf8BreakAt(latin, latin + 2));
    unsigned int cp;
    assert(ripps2Utf8Next("\xc3\xa9x", &cp) == 2 && cp == 0xE9);
    assert(ripps2Utf8Next("\xc3", &cp) == 1);
    puts("ok");
    return 0;
}
'''
cc = shutil.which('gcc') or shutil.which('cc')
if cc is None:
    fail.append('no host C compiler')
else:
    with tempfile.TemporaryDirectory(prefix='r2tr-') as td:
        td = Path(td)
        (td / 'include').mkdir()
        (td / 'include' / 'opl.h').write_text(STUB_OPL)
        (td / 'include' / 'ioman.h').write_text('')  # LOG comes from the stub opl.h
        (td / 'tamtypes.h').write_text(STUB_TAM)
        shutil.copy(root / 'include' / 'ripps2tr.h', td / 'include' / 'ripps2tr.h')
        shutil.copy(root / 'include' / 'utf8.h', td / 'include' / 'utf8.h')
        shutil.copy(root / 'src' / 'ripps2tr.c', td / 'ripps2tr.c')
        (td / 'harness.c').write_text(HARNESS)
        exe = td / ('h.exe' if os.name == 'nt' else 'h')
        r = subprocess.run([cc, '-std=gnu99', '-Wall', '-Werror', '-I', str(td), str(td / 'ripps2tr.c'), str(td / 'harness.c'), '-o', str(exe)],
                           capture_output=True, text=True)
        if r.returncode != 0:
            fail.append('ripps2tr.c does not build on the host:\n' + r.stdout + r.stderr)
        else:
            (td / 'lang.lng').write_bytes(keyed_text.encode('utf-8'))
            r = subprocess.run([str(exe), str(td / 'lang.lng')], capture_output=True, text=True)
            if r.returncode != 0 or 'ok' not in r.stdout:
                fail.append('the lookup harness failed:\n' + r.stdout + r.stderr)

# 2. the language loader reads keyed files, and keeps the line-numbered ones
lang = rd('src/lang.c')
for need in ('ripps2TrIsKeyed(buf, size)', 'ripps2TrLabel(cat, internalEnglish[strId])', 'ripps2TrUse(cat);', 'ripps2TrUse(NULL); // and RIPPS2',
             'readFileBuffer(fileBuffer, &newL[strId])'):
    if need not in lang:
        fail.append('lang.c: ' + need)

if 'lngAddHomeLanguages(); //' not in rd('src/opl.c') or 'void lngAddHomeLanguages(void)' not in lang:
    fail.append('the settings home and its LNG folder are scanned for languages once the config has chosen the home')

# 3. a letter a font lacks comes from the language font, then the fallback, at the font's own size
fnt = rd('src/fntsys.c')
for need in ('static FT_Face fntAltFace(font_t *font, int k)', 'fntDropAltFacesLocked(0);', 'fntDropAltFacesLocked(1);',
             '#define FNT_CAPS(f, c) ((f)->caps ? ripps2Upper(c) : (c))'):
    if need not in fnt:
        fail.append('fntsys.c: ' + need)
if 'font = &fonts[fallbackFontID];' in fnt:
    fail.append('fntsys.c: a missing letter must not switch to the fallback slot at its own size')

# 4. the shared draws translate what they are handed
if 'return _t(def);' not in rd('src/dia.c') or '_t(item->intvalue.enumvalues[eidx])' not in rd('src/dia.c'):
    fail.append('dia.c: English labels and enum values go through _t')
dia = rd('src/dia.c')
if 'cjk = diaHintHasCjk(wordStart, wordLen);' not in dia or 'if (wordLen < 256 && !cjk) {' not in dia \
        or 'if (lineW > 0 && cjk) {' not in dia:
    fail.append('dia.c: a settings hint\'s CJK run fills its line and breaks between characters (lab 10/19)')
ui = rd('src/ripps2ui.c')
if 'hintCase(_t(text), b, sizeof(b))' not in ui or 'ripps2Utf8Upper(text, word, sizeof(word))' not in ui:
    fail.append('ripps2ui.c: hints translate and sentence-case in UTF-8; the source toast capitalises in UTF-8')
if 'ch[0] = viewWord[i];' in ui:
    fail.append('ripps2ui.c: the view word lands a character at a time, not a byte')

# 5. every RIPPS2 file that draws words includes the header; the template matches the code
for f in sorted((root / 'src').glob('ripps2*.c')):
    t = f.read_text(encoding='utf-8')
    if ('_t(' in t or 'N_(' in t) and 'include/ripps2tr.h' not in t:
        fail.append(f.name + ' uses _t without include/ripps2tr.h')
tmpl = ripps2lang.template_dump(ripps2lang.extract(str(root)))
if (lang_dir / '_strings.yml').read_text(encoding='utf-8') != tmpl:
    fail.append('elf/lang/_strings.yml is out of date: python3 elf/lang/ripps2lang.py extract <riptopl>')

# 6. every translation's printf conversions match its English (a mismatch would be refused on the console)
for f in sorted(lang_dir.glob('*.yml')):
    if f.name.startswith('_'):
        continue
    mine, labels = ripps2lang.ripps2_translations(f.stem)
    for en, tr in mine.items():
        if tr and not ripps2lang.same_conversions(en, tr):
            fail.append('%s: %% conversions differ for "%s"' % (f.name, en[:50]))

# 7. a language that fills its gaps from another (Ryukyuan from Japanese) gets that one's RIPPS2 strings in its pack
for lang, via in ripps2lang.STRINGS_FROM.items():
    if not (lang_dir / (via + '.yml')).exists():
        fail.append('STRINGS_FROM: %s fills from %s, which has no elf/lang file' % (lang, via))
        continue
    with tempfile.TemporaryDirectory() as t:
        (Path(t) / 'lng_src').mkdir()
        empty = {'gui_strings': [{'label': 'SETTINGS', 'string': 'Settings'}]}
        text, _, (_, n_mine, n_tmpl) = ripps2lang.build_language(t, lang, empty, ripps2lang.template_load(), [])
        via_mine, _ = ripps2lang.ripps2_translations(via)
        want = sum(1 for en, tr in via_mine.items() if tr and en in set(ripps2lang.template_load()))
        if n_mine != want:
            fail.append('%s: %d of RIPPS2\'s strings from %s, expected %d' % (lang, n_mine, via, want))

if fail:
    print('\n'.join(fail))
    sys.exit(1)
print('build 104 ok')
