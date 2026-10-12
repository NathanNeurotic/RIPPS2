"""Build 98: RIPPS2's card folder icon. ripps2CardFolderIcon (src/ripps2boot.c) is compiled on the PC and run on a
folder: it must write ripps2.icn (the embedded misc/ripps2.icn, byte for byte) and an icon.sys made from OPL's
template that is titled RIPPS2, names ripps2.icn three times (list, copy, delete) and carries the night-to-blood
background; a second run keeps that icon.sys; an older RIPPS2 icon.sys (OPL's icon as bible.icn) is replaced and
anyone else's is kept. HAT_ICON_OUT=<dir> leaves the files there (for a lab card)."""
import os
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(os.environ.get('RIPTOPL_DIR', '.')).resolve()
boot = (root / 'src/ripps2boot.c').read_text(encoding='utf-8').replace('\r\n', '\n')
fail = []


def func(src, head):
    i = src.index(head)
    return src[i:src.index('\n}\n', i) + 3]


gcc = shutil.which('gcc')
if gcc:
    code = '\n'.join(func(boot, h) for h in ('static void blIconSysNamed(', 'int ripps2CardFolderIcon('))
    sysb = (root / 'misc/icon.sys').read_bytes()
    icn = (root / 'misc/ripps2.icn').read_bytes()
    harness = r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#ifndef O_BINARY
#define O_BINARY 0
#endif
static int hat_open(const char *p, int f) { return open(p, f | O_BINARY); }
#define open(p, f) hat_open(p, f)
static unsigned char icon_sys[] = {%s};
static unsigned int size_icon_sys = sizeof(icon_sys);
static unsigned char ripps2_icn[] = {%s};
static unsigned int size_ripps2_icn = sizeof(ripps2_icn);
static int blWrite(const char *path, const char *text, int len)
{
    FILE *f = fopen(path, "wb");
    if (f == NULL)
        return -1;
    int ok = (int)fwrite(text, 1, len, f) == len;
    return fclose(f) == 0 && ok ? 0 : -1;
}
%s
int main(int argc, char **argv) { return ripps2CardFolderIcon(argv[1]) ? 0 : 1; }
''' % (','.join(str(b) for b in sysb), ','.join(str(b) for b in icn), code)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / 'h.c').write_text(harness, encoding='utf-8')
        exe = tmp / 'h.exe'
        b = subprocess.run([gcc, '-std=gnu99', '-Wall', '-o', str(exe), str(tmp / 'h.c')], capture_output=True, text=True)
        if b.returncode != 0:
            fail.append('ripps2CardFolderIcon did not compile on the PC:\n' + b.stderr[-2000:])
        else:
            d = tmp / 'RIPPS2'
            d.mkdir()
            if subprocess.run([str(exe), str(d)]).returncode != 0:
                fail.append('ripps2CardFolderIcon failed on an empty folder')
            else:
                s = (d / 'icon.sys').read_bytes()
                if (d / 'ripps2.icn').read_bytes() != icn:
                    fail.append('ripps2.icn must be the embedded icon byte for byte')
                if len(s) != len(sysb) or s[:4] != b'PS2D':
                    fail.append('icon.sys must be the template\'s size and kind')
                names = [s[o:o + 64].split(b'\0')[0] for o in (0x104, 0x144, 0x184)]
                if names != [b'ripps2.icn'] * 3:
                    fail.append('icon.sys must name ripps2.icn for list, copy and delete: %r' % names)
                if s[0xC0:0xC0 + 7] != b'RIPPS2\0' or struct.unpack_from('<H', s, 6)[0] != 6:
                    fail.append('icon.sys must be titled RIPPS2 on one line: %r' % s[0xC0:0xC8])
                bg = [struct.unpack_from('<4i', s, 0x10 + 16 * i) for i in range(4)]
                if bg != [(18, 10, 34, 0), (18, 10, 34, 0), (110, 4, 16, 0), (110, 4, 16, 0)]:
                    fail.append('the background corners: %r' % bg)
                if s[0x50:0xC0] != sysb[0x50:0xC0]:
                    fail.append("the template's lights must be kept")
                out = os.environ.get('HAT_ICON_OUT')
                if out:
                    os.makedirs(out, exist_ok=True)
                    shutil.copy(d / 'icon.sys', out)
                    shutil.copy(d / 'ripps2.icn', out)
                # someone else's icon.sys stays; RIPPS2's older one (bible.icn) is replaced
                other = bytearray(sysb)
                other[0x104:0x144] = b'mine.icn'.ljust(64, b'\0')
                (d / 'icon.sys').write_bytes(bytes(other))
                subprocess.run([str(exe), str(d)])
                if (d / 'icon.sys').read_bytes() != bytes(other):
                    fail.append("an icon.sys RIPPS2 did not write must be kept")
                older = bytearray(sysb)
                older[0x104:0x144] = b'bible.icn'.ljust(64, b'\0')
                (d / 'icon.sys').write_bytes(bytes(older))
                subprocess.run([str(exe), str(d)])
                if (d / 'icon.sys').read_bytes() != s:
                    fail.append("RIPPS2's older icon.sys (OPL's icon) must give way to the hat")

if fail:
    print('\n'.join(fail))
    sys.exit(1)
print("RIPPS2 card folder icon: the hat, titled RIPPS2, others' icons kept OK" + ('' if gcc else ' (no gcc: skipped)'))
