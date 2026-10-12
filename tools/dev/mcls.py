"""List a PS2 memory card image's folders and files (read-only): mcls.py card.ps2 [FOLDER/FILE to print it]"""
import struct
import sys

d = open(sys.argv[1], 'rb').read()
assert d[:28] == b'Sony PS2 Memory Card Format ', d[:28]
page_len, ppc, ppb = struct.unpack_from('<HHH', d, 0x28)
clusters, alloc_off, alloc_end, root = struct.unpack_from('<IIII', d, 0x30)
ifc = struct.unpack_from('<32I', d, 0x50)
raw = page_len + (16 if len(d) % (page_len + 16) == 0 and len(d) % page_len != 0 or len(d) > clusters * ppc * page_len else 0)
csize = page_len * ppc
epc = csize // 4


def cluster(abs_c):
    out = b''
    for p in range(ppc):
        o = (abs_c * ppc + p) * raw
        out += d[o:o + page_len]
    return out


def fat(n):
    fi = n // epc
    ind = cluster(ifc[fi // epc])
    fc = struct.unpack_from('<I', ind, 4 * (fi % epc))[0]
    return struct.unpack_from('<I', cluster(fc), 4 * (n % epc))[0]


def chain(first, size):
    out, c, seen = b'', first, 0
    while len(out) < size and seen < 100000:
        out += cluster(c + alloc_off)
        v = fat(c)
        seen += 1
        if v & 0x7FFFFFFF == 0x7FFFFFFF:
            break
        c = v & 0x7FFFFFFF
    return out[:size]


def entries(first, count):
    data = chain(first, count * 512)
    for i in range(count):
        e = data[i * 512:(i + 1) * 512]
        mode, length = struct.unpack_from('<HxxI', e, 0)
        cl = struct.unpack_from('<I', e, 0x10)[0]
        name = e[0x40:0x60].split(b'\0')[0].decode('latin-1')
        yield mode, length, cl, name


rootdot = chain(root, 512)
count = struct.unpack_from('<I', rootdot, 4)[0]
if len(sys.argv) > 2:  # mcls.py card.ps2 FOLDER/FILE: the file's bytes to stdout
    want = sys.argv[2].split('/')
    for mode, length, cl, name in entries(root, count):
        if name == want[0] and mode & 0x20:
            for m2, l2, c2, n2 in entries(cl, length):
                if n2 == want[1] and m2 & 0x10:
                    sys.stdout.buffer.write(chain(c2, l2))
                    sys.exit(0)
    sys.exit('not found')
for mode, length, cl, name in entries(root, count):
    if name in ('.', '..') or not (mode & 0x8000):
        continue
    if mode & 0x20:
        print(name + '/')
        for m2, l2, c2, n2 in entries(cl, length):
            if n2 in ('.', '..') or not (m2 & 0x8000):
                continue
            print('    %s %d' % (n2, l2))
