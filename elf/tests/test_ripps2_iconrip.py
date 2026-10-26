"""Build 98: RIP 3D ICON. A save's icon (.ico / .icn) goes to the PC as an OBJ per animation shape, an MTL and the
texture as a PNG. The writer (src/ripps2iconrip.c) is compiled on the PC with the real icon reader (src/saveicon.c)
and its OBJ checked against an independent reading of RiptOPL's own shipped icons: every vertex, turned 180
degrees about x (y up, z toward the viewer, a turn so the winding holds), its normal turned the same, its texture
coordinate with v running up, its colour, one face per three vertices; and the A1B5G5R5 texture to RGB."""
import os
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path
from r2src import unwrap, TR_STUBS  # noqa: E402

root = Path(os.environ.get('RIPTOPL_DIR', '.')).resolve()
rd = lambda p: unwrap((root / p).read_text(encoding='utf-8').replace('\r\n', '\n'))  # build 104: as before _t
fail = []

files = rd('src/ripps2files.c')
if 'FB_ACT_RIPICON' not in files or '"RIP 3D ICON"' not in files or 'ripps2RipSaveIcon(from, out, sizeof(out))' not in files:
    fail.append('Memory Files must offer RIP 3D ICON on an icon file and run the rip')
if 'ripps2MediaKind(fbList[fbCursor].name) == RIPPS2_MEDIA_ICON' not in files:
    fail.append('RIP 3D ICON is offered on .ico / .icn files only')
if 'ripps2iconrip.o' not in rd('Makefile'):
    fail.append('ripps2iconrip.o must be built')
rip = rd('src/ripps2iconrip.c')
if 'snprintf(outDir, outSize, "mass0:/RIPPS2/ICONS/%s", folder);' not in rip:
    fail.append('the rip goes to mass0:/RIPPS2/ICONS/<the save folder>/')


def parse_icon(data):
    _, shapes, textype, _, verts = struct.unpack_from('<IIIfI', data, 0)
    off, out = 20, []
    for _ in range(verts):
        pos = [struct.unpack_from('<hhh', data, off + 8 * s) for s in range(shapes)]
        off += 8 * shapes
        nrm = struct.unpack_from('<hhh', data, off)
        off += 8
        uv = struct.unpack_from('<hh', data, off)
        off += 4
        rgba = data[off:off + 4]
        off += 4
        out.append((pos, nrm, uv, rgba))
    return shapes, verts, out


HARNESS = r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "include/saveicon.h"
int ripps2IconWriteObj(FILE *f, const saveicon_model_t *m, int shape, const char *mtl, const char *material);
int ripps2IconWriteMtl(FILE *f, const char *material, const char *png);
void ripps2IconTexRgb(const unsigned short *texels, unsigned char *rgb);
int main(int argc, char **argv)
{
    FILE *in = fopen(argv[1], "rb");
    static unsigned char d[512 * 1024];
    int n = (int)fread(d, 1, sizeof(d), in), s;
    saveicon_model_t m;
    fclose(in);
    if (saveIconParseModel(d, n, &m) != 0)
        return 2;
    for (s = 0; s < m.shapes; s++) {
        char name[512];
        snprintf(name, sizeof(name), "%s_%d.obj", argv[2], s);
        FILE *f = fopen(name, "w");
        if (!ripps2IconWriteObj(f, &m, s, "x.mtl", "x"))
            return 3;
        fclose(f);
    }
    if (m.texels != NULL) {
        unsigned short t[128 * 128];
        unsigned char *rgb = malloc(128 * 128 * 3);
        memset(t, 0, sizeof(t));
        t[0] = 0x001F; t[1] = 0x03E0; t[2] = 0x7C00; t[3] = 0xFFFF; t[4] = 0x0421;
        ripps2IconTexRgb(t, rgb);
        printf("tex %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d\n", rgb[0], rgb[1], rgb[2], rgb[3], rgb[4], rgb[5], rgb[6], rgb[7],
               rgb[8], rgb[9], rgb[10], rgb[11], rgb[12], rgb[13], rgb[14]);
    }
    if (ripps2IconWriteObj(stdout, &m, m.shapes, NULL, NULL) != 0) // a shape it does not have
        return 4;
    saveIconFreeModel(&m);
    return 0;
}
'''

gcc = shutil.which('gcc')
if gcc and not fail:
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / 'h.c').write_text(HARNESS, encoding='utf-8')
        exe = tmp / 'h.exe'
        b = subprocess.run([gcc, '-std=gnu99', '-Wall', '-Werror', '-DSAVEICON_HOST_TEST', '-DRIPPS2_ICONRIP_HOST_TEST', '-I', str(root),
                            '-o', str(exe), str(tmp / 'h.c'), str(root / 'src/saveicon.c'), str(root / 'src/ripps2iconrip.c')],
                           capture_output=True, text=True)
        if b.returncode != 0:
            fail.append('the rip writer did not compile on the PC:\n' + b.stderr[-2000:])
        else:
            for rel in ('misc/list.icn', 'POPS/list.icn', 'POPS/del.icn', 'misc/ripps2.icn'):  # the last: RIPPS2's own hat, 3 shapes
                data = (root / rel).read_bytes()
                shapes, verts, ref = parse_icon(data)
                r = subprocess.run([str(exe), str(root / rel), str(tmp / 'o')], capture_output=True, text=True)
                if r.returncode != 0:
                    fail.append('%s: the rip stopped (%d)' % (rel, r.returncode))
                    continue
                if 'tex 255 0 0 0 255 0 0 0 255 255 255 255 8 8 8' not in r.stdout:
                    fail.append('texels to RGB: %r' % r.stdout.strip())
                for s in range(shapes):
                    lines = (tmp / ('o_%d.obj' % s)).read_text().splitlines()
                    v = [l.split()[1:] for l in lines if l.startswith('v ')]
                    vt = [l.split()[1:] for l in lines if l.startswith('vt ')]
                    vn = [l.split()[1:] for l in lines if l.startswith('vn ')]
                    f = [l.split()[1:] for l in lines if l.startswith('f ')]
                    if not (len(v) == len(vt) == len(vn) == verts and len(f) == verts // 3) or 'mtllib x.mtl' not in lines:
                        fail.append('%s shape %d: %d v, %d vt, %d vn, %d f for %d vertices' % (rel, s, len(v), len(vt), len(vn), len(f), verts))
                        continue
                    for i in (0, verts // 2, verts - 1):
                        pos, nrm, uv, rgba = ref[i]
                        want = (pos[s][0] / 4096, -pos[s][1] / 4096, -pos[s][2] / 4096)
                        got = tuple(float(x) for x in v[i][:3])
                        col = tuple(float(x) for x in v[i][3:])
                        wcol = tuple(min(c, 0x80) / 128 for c in rgba[:3])
                        wn = (nrm[0] / 4096, -nrm[1] / 4096, -nrm[2] / 4096)
                        wt = (uv[0] / 4096, 1 - uv[1] / 4096)
                        if any(abs(a - b) > 1e-4 for a, b in zip(got + col, want + wcol)) or \
                                any(abs(float(a) - b) > 1e-4 for a, b in zip(vn[i], wn)) or \
                                any(abs(float(a) - b) > 1e-4 for a, b in zip(vt[i], wt)):
                            fail.append('%s shape %d vertex %d: %r %r %r' % (rel, s, i, v[i], vn[i], vt[i]))
                    if f[0] != ['1/1/1', '2/2/2', '3/3/3'] or f[-1][2] != '%d/%d/%d' % (verts, verts, verts):
                        fail.append('%s: faces must take the vertices three at a time in order: %r %r' % (rel, f[0], f[-1]))

hat = (root / 'misc/ripps2.icn').read_bytes()
_, hshapes, htype, _, hverts = struct.unpack_from('<IIIfI', hat, 0)
if hshapes != 3 or htype != 0x0E or hverts % 3 or hverts > 2000:
    fail.append('misc/ripps2.icn: %d shapes, type %#x, %d vertices (want 3 shapes, packed texture, at most 2000)' % (hshapes, htype, hverts))
boot = rd('src/ripps2boot.c')
if 'int ripps2CardFolderIcon(const char *dir)' not in boot or 'ripps2CardFolderIcon(' not in rd('src/opl.c') or \
        'ripps2CardFolderIcon("mc0:/RIPPS2");' not in rd('src/ripps2status.c') or 'ripps2_icn.o' not in rd('Makefile'):
    fail.append("RIPPS2's card folder must get its hat icon wherever RIPPS2 makes the folder")
if fail:
    print('\n'.join(fail))
    sys.exit(1)
print('icon rip: OBJ per shape, MTL, PNG texture OK' + ('' if gcc else ' (static checks only, no gcc)'))
