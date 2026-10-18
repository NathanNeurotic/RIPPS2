"""RIPPS2's languages (build 104): the string template, the translations' checks, and the language pack.

    python3 elf/lang/ripps2lang.py extract <riptopl> [--check]   _strings.yml from _t("...") and N_("...") in the tree
    python3 elf/lang/ripps2lang.py check                          every <Language>.yml against the template
    python3 elf/lang/ripps2lang.py pack <riptopl> <out>           <out>/RIPPS2-languages.zip (after `make languages`)

A RIPPS2 language file (LNG/lang_<Language>.lng) is keyed by the English: a line is the FNV-1a hash of an English string
(8 hex digits), a tab, and its translation, with \\n, \\t and \\\\ escaped. It carries Open PS2 Loader's strings (their
English from lng_tmpl/_base.yml, their translations from Open PS2 Loader's language files and RiptOPL's lng_fork) and
RIPPS2's own (elf/lang/<Language>.yml). src/ripps2tr.c reads it; a string with no line, or whose printf conversions differ
from its English's, shows in English.
"""
import io
import json
import os
import re
import struct
import sys
import zipfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, '_strings.yml')
MARK = '#!RIPPS2LANG 1'

# ---- C sources ----

ESC = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\', '"': '"', "'": "'", 'a': '\a', 'b': '\b', 'f': '\f', 'v': '\v', '?': '?'}


def c_unescape(raw):
    b, i = bytearray(), 0
    while i < len(raw):
        c = raw[i]
        if c != '\\':
            b.extend(c.encode('utf-8'))
            i += 1
            continue
        n = raw[i + 1]
        if n == 'x':
            j = i + 2
            while j < len(raw) and raw[j] in '0123456789abcdefABCDEF':
                j += 1
            b.append(int(raw[i + 2:j], 16) & 0xFF)
            i = j
        elif n in '01234567':
            j = i + 1
            while j < len(raw) and j < i + 4 and raw[j] in '01234567':
                j += 1
            b.append(int(raw[i + 1:j], 8) & 0xFF)
            i = j
        else:
            b.extend(ESC.get(n, n).encode('utf-8'))
            i += 2
    return b.decode('utf-8')


def strip_comments(src):
    """The source with comments blanked (strings and char literals kept), so a commented-out _t is not read."""
    out, i, n = [], 0, len(src)
    while i < n:
        if src.startswith('//', i):
            j = src.find('\n', i)
            j = n if j < 0 else j
            out.append(' ' * (j - i))
            i = j
        elif src.startswith('/*', i):
            j = src.find('*/', i + 2)
            j = n if j < 0 else j + 2
            out.append(re.sub(r'[^\n]', ' ', src[i:j]))
            i = j
        elif src[i] in '"\'':
            q, j = src[i], i + 1
            while j < n and src[j] != q:
                j += 2 if src[j] == '\\' else 1
            out.append(src[i:j + 1])
            i = j + 1
        else:
            out.append(src[i])
            i += 1
    return ''.join(out)


LITS = r'((?:"(?:[^"\\\n]|\\.)*"\s*)+)'
MARKED = re.compile(r'\b(_t|N_)\(\s*' + LITS + r'\)')
DIA_LABEL = re.compile(r'\.label = \{' + LITS + r',\s*-1\}')


def literal_value(group):
    return ''.join(c_unescape(m) for m in re.findall(r'"((?:[^"\\\n]|\\.)*)"', group))


def extract(tree):
    """{English: sorted list of the files it is in}, from every src/*.c."""
    found = {}
    src_dir = os.path.join(tree, 'src')
    for name in sorted(os.listdir(src_dir)):
        if not name.endswith('.c') or name == 'lang_internal.c':
            continue
        text = strip_comments(open(os.path.join(src_dir, name), encoding='utf-8').read())
        pats = [MARKED]
        if name == 'dialogs.c':  # dia.c translates a label given as English text (diaGetLocalisedText)
            pats.append(DIA_LABEL)
        for pat in pats:
            for m in pat.finditer(text):
                v = literal_value(m.group(m.lastindex))
                if not re.search(r'[A-Za-z]', v) or len(v.strip()) < 2:
                    continue
                found.setdefault(v, set()).add(name)
    return {k: sorted(v) for k, v in found.items()}


def template_dump(strings):
    head = ('# RIPPS2\'s own words, as the code shows them in English: made by elf/lang/ripps2lang.py extract from\n'
            '# every _t("...") and N_("...") in the RiptOPL tree with RIPPS2\'s patches applied. Do not edit by hand.\n'
            '# A translation (<Language>.yml) maps each of these to its words; see README.md.\n')
    items = [{'en': k, 'in': v} for k, v in sorted(strings.items(), key=lambda kv: (kv[1][0], kv[0]))]
    return head + yaml.safe_dump({'strings': items}, allow_unicode=True, sort_keys=False, width=1000)


def template_load():
    data = yaml.safe_load(open(TEMPLATE, encoding='utf-8'))
    return [it['en'] for it in data['strings']]


# ---- printf conversions (as src/ripps2tr.c trConv reads them) ----

def conversions(s):
    out, i = [], 0
    while i < len(s):
        if s[i] != '%':
            i += 1
            continue
        i += 1
        if i < len(s) and s[i] == '%':
            i += 1
            continue
        sig = ''
        while i < len(s) and s[i] in '-+ #0':
            i += 1
        while i < len(s) and (s[i].isdigit() or s[i] in '*.$'):
            if s[i] == '$':
                return None
            if s[i] == '*':
                sig += '*'
            i += 1
        while i < len(s) and s[i] in 'hljztLq':
            sig += s[i]
            i += 1
        if i >= len(s):
            return None
        out.append(sig + s[i])
        i += 1
    return out


def same_conversions(en, tr):
    a, b = conversions(en), conversions(tr)
    if a is None or b is None:
        return '%' not in en and '%' not in tr
    return a == b


def fnv1a(s):
    h = 2166136261
    for byte in s.encode('utf-8'):
        h = ((h ^ byte) * 16777619) & 0xFFFFFFFF
    return h


def escape_line(s):
    return s.replace('\\', '\\\\').replace('\n', '\\n').replace('\t', '\\t').replace('\r', '')


# ---- fonts: which letters a TrueType/OpenType face has, and its name records ----

def font_tables(data):
    num = struct.unpack('>H', data[4:6])[0]
    t = {}
    for k in range(num):
        tag, _, off, ln = struct.unpack('>4sIII', data[12 + 16 * k:28 + 16 * k])
        t[tag.decode('latin-1')] = (off, ln)
    return t


def font_cmap(data):
    off, _ = font_tables(data)['cmap']
    n = struct.unpack('>H', data[off + 2:off + 4])[0]
    best = None
    for k in range(n):
        pid, eid, sub = struct.unpack('>HHI', data[off + 4 + 8 * k:off + 12 + 8 * k])
        fmt = struct.unpack('>H', data[off + sub:off + sub + 2])[0]
        if (pid, eid, fmt) in ((3, 10, 12), (0, 4, 12), (0, 6, 12)):
            best = (off + sub, 12)
            break
        if fmt == 4 and (pid in (0, 3)) and best is None:
            best = (off + sub, 4)
    cps = set()
    if best is None:
        return cps
    p, fmt = best
    if fmt == 4:
        segx2 = struct.unpack('>H', data[p + 6:p + 8])[0]
        seg = segx2 // 2
        ends = struct.unpack('>%dH' % seg, data[p + 14:p + 14 + segx2])
        starts = struct.unpack('>%dH' % seg, data[p + 16 + segx2:p + 16 + 2 * segx2])
        deltas = struct.unpack('>%dh' % seg, data[p + 16 + 2 * segx2:p + 16 + 3 * segx2])
        ro_at = p + 16 + 3 * segx2
        ros = struct.unpack('>%dH' % seg, data[ro_at:ro_at + segx2])
        for k in range(seg):
            for c in range(starts[k], ends[k] + 1):
                if c == 0xFFFF:
                    continue
                if ros[k] == 0:
                    g = (c + deltas[k]) & 0xFFFF
                else:
                    ga = ro_at + 2 * k + ros[k] + 2 * (c - starts[k])
                    g = struct.unpack('>H', data[ga:ga + 2])[0]
                    if g:
                        g = (g + deltas[k]) & 0xFFFF
                if g:
                    cps.add(c)
    else:
        ngroups = struct.unpack('>I', data[p + 12:p + 16])[0]
        for k in range(ngroups):
            a, b, g = struct.unpack('>III', data[p + 16 + 12 * k:p + 28 + 12 * k])
            if b - a < 0x30000:
                cps.update(range(a, b + 1))
    return cps


def font_names(data):
    off, _ = font_tables(data)['name']
    _, count, sto = struct.unpack('>HHH', data[off:off + 6])
    out = {}
    for k in range(count):
        pid, eid, lid, nid, ln, so = struct.unpack('>HHHHHH', data[off + 6 + 12 * k:off + 18 + 12 * k])
        raw = data[off + sto + so:off + sto + so + ln]
        if pid == 3 or pid == 0:
            v = raw.decode('utf-16-be', 'replace')
        else:
            v = raw.decode('latin-1')
        if nid not in out or pid == 3:
            out[nid] = v
    return out


# ---- the pack ----

def opl_translations(path):
    if not os.path.exists(path):
        return {}
    data = yaml.safe_load(open(path, encoding='utf-8')) or {}
    return {k: v for k, v in (data.get('translations') or {}).items() if isinstance(v, str)}


def ripps2_translations(lang):
    path = os.path.join(HERE, lang + '.yml')
    if not os.path.exists(path):
        return {}, {}
    data = yaml.safe_load(open(path, encoding='utf-8')) or {}
    return dict(data.get('strings') or {}), dict(data.get('labels') or {})


def build_language(tree, lang, base, english_template, report):
    """(the .lng text, every character it uses) for one language."""
    opl = opl_translations(os.path.join(tree, 'lng_src', lang + '.yml'))
    mine, label_fill = ripps2_translations(lang)
    entries, chars, refused = {}, set(), []

    def add(en, tr, origin, override):
        if not tr or tr == en or not en:
            return
        if not same_conversions(en, tr):
            refused.append((origin, en))
            return
        h = fnv1a(en)
        if h in entries and not override:
            return
        entries[h] = tr
        chars.update(tr)

    for d in base['gui_strings']:  # Open PS2 Loader's labels, by their English here; RIPPS2's labels: only the gaps
        label, en = d['label'], d['string']
        tr = opl.get(label) or label_fill.get(label)
        add(en, tr, label, False)
    known = set(english_template)
    n_mine = 0
    for en, tr in mine.items():  # RIPPS2's: they win over a label with the same English
        if en not in known:
            report.append('%s: "%s" is not in the template any more (RIPPS2 no longer shows it)' % (lang, en[:60]))
            continue
        if tr:
            n_mine += 1
        add(en, tr, 'RIPPS2', True)
    for origin, en in refused:
        report.append('%s: %s refused, its %% conversions differ from the English "%s"' % (lang, origin, en[:60]))
    lines = ['# RIPPS2 language file: %s. Made by RIPPS2\'s build from Open PS2 Loader\'s translations, RiptOPL\'s and' % lang,
             '# RIPPS2\'s own (ps2-pillars elf/lang). Each line: the FNV-1a hash of an English string, a tab, its translation.',
             MARK]
    for h in sorted(entries):
        lines.append('%08x\t%s' % (h, escape_line(entries[h])))
    stats = (len(entries), n_mine, len(english_template))
    return '\n'.join(lines) + '\n', chars, stats


def pack(tree, out):
    base = yaml.safe_load(open(os.path.join(tree, 'lng_tmpl', '_base.yml'), encoding='utf-8'))
    english_template = template_load()
    langs = sorted(f[:-4] for f in os.listdir(os.path.join(tree, 'lng_src')) if f.endswith('.yml') and f != 'English.yml')
    builtin = font_cmap(open(os.path.join(tree, 'thirdparty', 'PoeVeticaNew.ttf'), 'rb').read())
    report, notes, licences = [], [], []
    os.makedirs(out, exist_ok=True)
    zpath = os.path.join(out, 'RIPPS2-languages.zip')
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
        for lang in langs:
            text, chars, (n, n_mine, n_tmpl) = build_language(tree, lang, base, english_template, report)
            z.writestr('LNG/lang_%s.lng' % lang, text.encode('utf-8'))
            need = sorted(c for c in chars if ord(c) >= 0x80 and ord(c) not in builtin and not c.isspace())
            font_note = 'built-in fonts'
            if need:
                font = None
                for ext in ('ttf', 'otf'):
                    p = os.path.join(tree, 'lng_src', 'thirdparty', 'font_%s.%s' % (lang, ext))
                    if os.path.exists(p):
                        font = p
                        break
                if font is None:
                    font_note = 'NO FONT: %d letters the built-in fonts lack' % len(need)
                else:
                    data = open(font, 'rb').read()
                    have = font_cmap(data)
                    lack = [c for c in need if ord(c) not in have]
                    names = font_names(data)
                    z.writestr('LNG/' + os.path.basename(font), data)
                    font_note = '%s (%s)%s' % (os.path.basename(font), names.get(4, '?'),
                                               ', lacks %d: %s' % (len(lack), ''.join(lack[:20])) if lack else '')
                    licences.append('%s\n  name: %s\n  copyright: %s\n  licence: %s\n  licence URL: %s\n' % (
                        os.path.basename(font), names.get(4, ''), names.get(0, ''), names.get(13, ''), names.get(14, '')))
            notes.append('%-14s %4d strings (%3d of RIPPS2\'s %d), %s' % (lang, n, n_mine, n_tmpl, font_note))
        z.writestr('LNG/README.txt', README_PACK.encode('utf-8'))
        if licences:
            z.writestr('LNG/FONTS.txt', ('The fonts in this folder come from Open PS2 Loader\'s language pack\n'
                                         '(github.com/ps2homebrew/Open-PS2-Loader-lang, thirdparty/). What each says of itself:\n\n'
                                         + '\n'.join(licences)).encode('utf-8'))
    for line in notes:
        print('lang: ' + line)
    for line in report:
        print('lang note: ' + line)
    print('lang: wrote %s (%d languages)' % (zpath, len(langs)))


README_PACK = '''RIPPS2 languages
================

Copy this LNG folder to the top of a USB drive, the HDD's OPL partition or an MMCE card (or the files in it to
mc0:/RIPPS2 on a memory card), then pick the language in Settings > Display Settings > Language.

A language that needs letters RIPPS2's own fonts do not have (Greek, Cyrillic, Arabic, Chinese, Japanese, Korean...)
has its font_<Language> file here too: keep it beside its lang_<Language>.lng.

These files are keyed by the English, so they keep working with later RIPPS2 builds: a string a later build adds shows
in English until the next pack. Corrections and new languages: github.com/akilluminati47/ps2-pillars (elf/lang).
'''


def check():
    english_template = template_load()
    known = set(english_template)
    bad = 0
    for f in sorted(os.listdir(HERE)):
        if not f.endswith('.yml') or f.startswith('_'):
            continue
        mine, _ = ripps2_translations(f[:-4])
        done = 0
        for en, tr in mine.items():
            if en not in known:
                print('%s: not in the template: %s' % (f, en[:70]))
                continue
            if tr and not same_conversions(en, tr):
                print('%s: %% conversions differ: %s' % (f, en[:70]))
                bad += 1
            done += bool(tr)
        print('%-20s %d of %d' % (f, done, len(english_template)))
    return bad


def main():
    cmd = sys.argv[1]
    if cmd == 'extract':
        text = template_dump(extract(sys.argv[2]))
        if '--check' in sys.argv:
            now = open(TEMPLATE, encoding='utf-8').read() if os.path.exists(TEMPLATE) else ''
            if now != text:
                print('elf/lang/_strings.yml is out of date: run ripps2lang.py extract <riptopl>')
                return 1
            return 0
        open(TEMPLATE, 'w', encoding='utf-8', newline='\n').write(text)
        print('wrote', TEMPLATE, text.count('\n- en:'))
        return 0
    if cmd == 'check':
        return 1 if check() else 0
    if cmd == 'pack':
        pack(sys.argv[2], sys.argv[3])
        return 0
    print(__doc__)
    return 2


if __name__ == '__main__':
    sys.exit(main())
