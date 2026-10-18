"""Build 98: the Memory Files text editor keeps a file as it was. Its own load and save code (ripps2edit.c, from
the line store to edSave) is compiled on the PC and round-trips files that used to lose data: a line longer than
255 characters (cut on load), more than 1000 lines (the rest dropped on save), blank lines at the end (the last
dropped), a missing final line break (one added), CRLF files, and a NUL byte (refused: a save would cut there)."""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from r2src import unwrap, TR_STUBS  # noqa: E402

root = Path(os.environ.get('RIPTOPL_DIR', '.'))
src = unwrap((root / 'src/ripps2edit.c').read_text(encoding='utf-8').replace('\r\n', '\n'))  # build 104: as before _t
fail = []

for needle, why in (('#define ED_MAX_LINES 4096', 'the editor holds 4096 lines'),
                    ('#define ED_LINE      1024', 'the keyboard edits lines up to 1023 characters'),
                    ('char *line = malloc(len + 1);', 'each line is stored at its own length'),
                    ('"LINE TOO LONG TO EDIT"', 'a longer line is kept whole and not opened on the keyboard'),
                    ('r == -2 ? "This file is not plain text', 'a file with a NUL byte is refused')):
    if needle not in src:
        fail.append('%s (%s missing)' % (why, needle))

gcc = shutil.which('gcc')
if gcc and not fail:
    block = src[src.index('static char *edLines[ED_MAX_LINES];'):]
    block = block[:block.index('\n}\n', block.index('static int edSave(')) + 3]
    harness = r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#ifndef O_BINARY
#define O_BINARY 0
#endif
#define ED_MAX_LINES 4096
#define ED_LINE 1024
#define ED_FILE_MAX (64 * 1024)
static int ed_open(const char *p, int f, ...) { return open(p, f | O_BINARY, 0666); }
#define open(...) ed_open(__VA_ARGS__)
''' + block + r'''
int main(int argc, char **argv)
{
    int crlf, endNl, r = edLoad(argv[1], &crlf, &endNl);
    printf("%d %d\n", r, edCount);
    if (r == 1 && !edSave(argv[2], crlf, endNl))
        printf("save failed\n");
    return 0;
}
'''
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / 'h.c').write_text(harness, encoding='utf-8')
        exe = tmp / 'h.exe'
        b = subprocess.run([gcc, '-std=gnu99', '-Wall', '-Wno-unused-function', '-o', str(exe), str(tmp / 'h.c')],
                           capture_output=True, text=True)
        if b.returncode != 0:
            fail.append('the editor code did not compile on the PC:\n' + b.stderr[-2000:])
        else:
            cases = {
                'long line': b'short\n' + b'x' * 5000 + b'\nend\n',
                '2000 lines': b''.join(b'line %d\n' % i for i in range(2000)),
                'blank lines at the end': b'a\n\nb\n\n\n',
                'no final break': b'a\nb',
                'crlf': b'a\r\nb\r\n\r\n',
                'empty': b'',
                'only a break': b'\n',
            }
            for name, data in cases.items():
                (tmp / 'in').write_bytes(data)
                if (tmp / 'out').exists():
                    (tmp / 'out').unlink()
                out = subprocess.run([str(exe), str(tmp / 'in'), str(tmp / 'out')], capture_output=True, text=True).stdout
                got = (tmp / 'out').read_bytes() if (tmp / 'out').exists() else None
                if not out.startswith('1 ') or got != data:
                    fail.append('%s: load said %r, saved %r' % (name, out.strip(), got[:60] if got else got))
            (tmp / 'in').write_bytes(b''.join(b'%d\n' % i for i in range(5000)))
            out = subprocess.run([str(exe), str(tmp / 'in'), str(tmp / 'out2')], capture_output=True, text=True).stdout
            if not out.startswith('-1 ') or (tmp / 'out2').exists():
                fail.append('5000 lines must be refused, not cut: %r' % out)
            (tmp / 'in').write_bytes(b'abc\0def\n')
            out = subprocess.run([str(exe), str(tmp / 'in'), str(tmp / 'out3')], capture_output=True, text=True).stdout
            if not out.startswith('-2 ') or (tmp / 'out3').exists():
                fail.append('a NUL byte must be refused: %r' % out)

if fail:
    print('\n'.join(fail))
    sys.exit(1)
print('text editor: files round-trip whole OK' + ('' if gcc else ' (static checks only, no gcc)'))
