"""PS2 memory card page ECC (Hamming code per 128-byte chunk, as the card's own spare area holds it)."""


def _parityb(a):
    a ^= a >> 1
    a ^= a >> 2
    a ^= a >> 4
    return a & 1


PARITY = [_parityb(b) for b in range(256)]
_CPM = [0x55, 0x33, 0x0F, 0x00, 0xAA, 0xCC, 0xF0]
COLMASK = []
for _b in range(256):
    m = 0
    for _i, _c in enumerate(_CPM):
        m |= PARITY[_b & _c] << _i
    COLMASK.append(m)


def ecc128(chunk):
    cp, lp0, lp1 = 0x77, 0x7F, 0x7F
    for i, b in enumerate(chunk):
        cp ^= COLMASK[b]
        if PARITY[b]:
            lp0 ^= ~i
            lp1 ^= i
    return bytes([cp & 0xFF, lp0 & 0x7F, lp1 & 0xFF])


def spare(page):
    """The 16-byte spare for a 512-byte page: four 3-byte codes, then four zero bytes."""
    return b''.join(ecc128(page[i:i + 128]) for i in range(0, 512, 128)) + b'\0' * 4


if __name__ == '__main__':
    import sys
    d = open(sys.argv[1], 'rb').read()
    bad = 0
    pages = len(d) // 528
    for p in range(pages):
        pg = d[p * 528:p * 528 + 512]
        sp = d[p * 528 + 512:p * 528 + 528]
        if sp != spare(pg) and sp != b'\xff' * 16:
            bad += 1
            if bad < 4:
                print('page', p, sp.hex(), spare(pg).hex())
    print(pages, 'pages,', bad, 'mismatched')
