"""Make a lab memory card: a copy of an EMPTY formatted card with save folders added (FAT chains, directory
entries and every page's ECC written the way the card's own pages are). Lab use only.

    python -I mcadd.py empty.ps2 out.ps2 FOLDER=path/to/dir [FOLDER=dir ...]
"""
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcecc import spare  # noqa: E402

RAW = 528
src, out = sys.argv[1], sys.argv[2]
d = bytearray(open(src, 'rb').read())
page_len, ppc = struct.unpack_from('<HH', d, 0x28)
assert page_len == 512 and ppc == 2
clusters, alloc_off, alloc_end, root = struct.unpack_from('<IIII', d, 0x30)
ifc = struct.unpack_from('<32I', d, 0x50)
CS = 1024
TOD = bytes([0, 0, 0, 12, 12, 10]) + struct.pack('<H', 2026)  # 2026-10-12 12:00:00


def rd_cl(c):
    return bytes(b''.join(d[(c * 2 + p) * RAW:(c * 2 + p) * RAW + 512] for p in range(2)))


def wr_cl(c, data):
    data = data.ljust(CS, b'\0')
    for p in range(2):
        pg = data[p * 512:(p + 1) * 512]
        o = (c * 2 + p) * RAW
        d[o:o + 512] = pg
        d[o + 512:o + RAW] = spare(pg)


def fat_loc(n):
    fi = n // 256
    ind = rd_cl(ifc[fi // 256])
    return struct.unpack_from('<I', ind, 4 * (fi % 256))[0], n % 256


def fat_get(n):
    c, i = fat_loc(n)
    return struct.unpack_from('<I', rd_cl(c), 4 * i)[0]


def fat_set(n, v):
    c, i = fat_loc(n)
    buf = bytearray(rd_cl(c))
    struct.pack_into('<I', buf, 4 * i, v)
    wr_cl(c, bytes(buf))


def alloc(count):
    got, n = [], 0
    while len(got) < count:
        assert n < alloc_end - alloc_off, 'card full'
        if not (fat_get(n) & 0x80000000):
            got.append(n)
        n += 1
    for a, b in zip(got, got[1:] + [None]):
        fat_set(a, 0xFFFFFFFF if b is None else 0x80000000 | b)
    return got


def chain(first):
    out_, c = [first], first
    while True:
        v = fat_get(c)
        if v == 0xFFFFFFFF or not (v & 0x80000000):
            return out_
        c = v & 0x7FFFFFFF
        out_.append(c)


def entry(mode, length, cl, de, name):
    e = bytearray(512)
    struct.pack_into('<HxxI', e, 0, mode, length)
    e[8:16] = TOD
    struct.pack_into('<II', e, 0x10, cl, de)
    e[0x18:0x20] = TOD
    nm = name.encode('ascii')
    assert len(nm) < 32
    e[0x40:0x40 + len(nm)] = nm
    return bytes(e)


def write_chain(cls, data):
    for i, c in enumerate(cls):
        wr_cl(c + alloc_off, data[i * CS:(i + 1) * CS])


# the root as it is
rootdata = b''.join(rd_cl(c + alloc_off) for c in chain(root))
count = struct.unpack_from('<I', rootdata, 4)[0]
ents = [rootdata[i * 512:(i + 1) * 512] for i in range(count)]
for arg in sys.argv[3:]:
    name, path = arg.split('=', 1)
    files = sorted(f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)))
    de = len(ents)
    sub = [entry(0x8427, 0, 0, de, '.'), entry(0x8427, 0, 0, 0, '..')]
    for f in files:
        blob = open(os.path.join(path, f), 'rb').read()
        fc = alloc(max(1, (len(blob) + CS - 1) // CS))
        write_chain(fc, blob)
        sub.append(entry(0x8497, len(blob), fc[0], 0, f))
    dc = alloc((len(sub) + 1) // 2)
    write_chain(dc, b''.join(sub))
    ents.append(entry(0x8427, len(sub), dc[0], 0, name))
    print('added', name, files, 'dir clusters', dc)

# the root again, longer: "." counts its entries; extend its chain when it needs more clusters
dot = bytearray(ents[0])
struct.pack_into('<I', dot, 4, len(ents))
dot[0x18:0x20] = TOD
ents[0] = bytes(dot)
rc = chain(root)
need = (len(ents) + 1) // 2
if need > len(rc):
    more = alloc(need - len(rc))
    fat_set(rc[-1], 0x80000000 | more[0])
    rc += more
write_chain(rc, b''.join(ents))
open(out, 'wb').write(bytes(d))
print('root entries', len(ents), 'chain', rc, '->', out)
