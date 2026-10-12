"""RIPPS2's own memory card icon: the dead elf's hat (media/deadelf, the blue-hat logo) in the PS2 save icon format.

The blue felt cone curls over toward its gold bell, the fur brim is soaked from below, and the hat stands in its
blood pool. Three morph shapes (at rest, the curl swung one way, the other way) with keys that ring the bell four
times, dying away, then rest: a 1.5 s loop. One 128 x 128 texture (felt, fur, bell and blood side by side),
RLE-packed as the icons RiptOPL ships are (texture type 0x0E, alpha bit clear).

    python make_hat_icon.py OUT.icn [--png preview.png]

The format (as saveicon.c reads it): a 20-byte header (0x00010000, shapes, texture type, 1.0, vertices), per
vertex one 8-byte position per shape, an 8-byte normal, a 4-byte UV and a 4-byte RGBA (4.12 fixed point; the
fourth short 0x400 as in the shipped icons), the animation header (1, frame length, speed, 0, shape count), per
shape its id, key count and (time, value) keys, then the packed texture. Icon space: +x right, +y DOWN, +z into
the screen; models stand with their foot near y = -1, as the shipped ones do.
"""
import math
import struct
import sys

import numpy as np

TEX = 128
RNG = np.random.default_rng(98)

# ---- the texture atlas -------------------------------------------------------------------------------------
# x 0..63 felt (v runs brim 127 -> tip 0), 64..95 fur, 96..127 bell (y 0..63) and blood (y 64..127)
FELT = (0, 0, 64, 128)
FUR = (64, 0, 32, 128)
BELL = (96, 0, 32, 64)
POOL = (96, 64, 32, 64)


def make_texture():
    img = np.zeros((TEX, TEX, 3), np.float32)
    # felt: the logo's blue, fibres, darker toward the tip's shade; blood wicks up from the brim, ragged
    x0, y0, w, h = FELT
    base = np.array([58, 92, 176], np.float32)
    yy, xx = np.mgrid[0:h, 0:w]
    shade = 0.82 + 0.18 * (yy / h)  # a touch darker toward the tip
    fib = RNG.normal(0, 9, (h, w))
    felt = base[None, None, :] * shade[..., None] + fib[..., None]
    reach = h * (0.30 + 0.12 * np.sin(xx[0] * 0.21 + 1.7) * np.sin(xx[0] * 0.5) + 0.05 * RNG.random(w))
    up = (h - 1 - yy)  # distance up from the brim row
    soak = np.clip(1.0 - up / reach[None, :], 0, 1) ** 0.6
    blood = np.array([70, 0, 8], np.float32)
    felt = felt * (1 - soak[..., None]) + blood * soak[..., None]
    img[y0:y0 + h, x0:x0 + w] = felt
    # fur: cream, noisy; its lower side (larger v) soaked
    x0, y0, w, h = FUR
    yy, xx = np.mgrid[0:h, 0:w]
    fur = np.array([232, 220, 196], np.float32)[None, None, :] + RNG.normal(0, 16, (h, w))[..., None]
    soak = np.clip((yy / h - 0.55) / 0.35, 0, 1)
    fur = fur * (1 - soak[..., None]) + np.array([96, 6, 12], np.float32) * soak[..., None]
    img[y0:y0 + h, x0:x0 + w] = fur
    # bell: dark gold, lit from the top left
    x0, y0, w, h = BELL
    yy, xx = np.mgrid[0:h, 0:w]
    lit = np.clip(1.15 - yy / h * 1.1, 0.15, 1.0)
    bell = np.array([210, 150, 52], np.float32)[None, None, :] * lit[..., None]
    img[y0:y0 + h, x0:x0 + w] = bell
    # blood: deep red with a few glossy streaks
    x0, y0, w, h = POOL
    yy, xx = np.mgrid[0:h, 0:w]
    pool = np.array([92, 0, 10], np.float32)[None, None, :] * (0.85 + 0.15 * np.sin(xx * 0.4 + yy * 0.25))[..., None]
    pool += (np.sin(xx * 0.9 - yy * 0.6) > 0.96)[..., None] * np.array([70, 40, 40], np.float32)
    img[y0:y0 + h, x0:x0 + w] = pool
    return np.clip(img, 0, 255).astype(np.uint8)


def texel(u, v, region):
    """A region-relative (0..1, 0..1) point to the 4.12 UV the format stores (32 per texel), kept half a texel in."""
    x0, y0, w, h = region
    x = x0 + 0.5 + u * (w - 1)
    y = y0 + 0.5 + v * (h - 1)
    return int(round(x * 32)), int(round(y * 32))


# ---- the model, built y-up (as the logo scene) and turned into icon space at the end ---------------------------
H, R0 = 3.05, 1.0
BEND_T, BEND_ANG = 0.42, 1.45
BEND_Y = BEND_T * H
BEND_R = (H - BEND_Y) / BEND_ANG
SWING = 0.75  # radians the curl swings at full weight (a ring you can see from any side)


def bend(x, y, z):
    t = y / H
    if t > BEND_T:
        th = (y - BEND_Y) / BEND_R
        r = BEND_R - x
        x, y = BEND_R - r * math.cos(th), BEND_Y + r * math.sin(th)
    return x, y, z


def swing(p, s, amount):
    """The curl turned about the hat's own axis, more toward the tip (s: 0 at the bend .. 1 at the tip)."""
    a = SWING * amount * s ** 1.3
    x, y, z = p
    c, si = math.cos(a), math.sin(a)
    return (x * c - z * si, y, x * si + z * c)


tris = []  # each: three (pos_by_shape[3], normal, uv)


def add_grid(points, uvs, swings):
    """A grid of quads: points[i][j] (j's last column repeats the first, so the texture seam has its own UVs).
    Smooth normals, shared by every vertex at the same spot (the seam, a torus's closing ring)."""
    ni, nj = len(points), len(points[0])
    P = np.array(points, np.float64)
    acc = {}
    key = lambda q: (round(q[0], 5), round(q[1], 5), round(q[2], 5))
    quads = [((i, j), (i, j + 1), (i + 1, j), (i + 1, j + 1)) for i in range(ni - 1) for j in range(nj - 1)]
    for a, b, c, d in quads:
        for t in ((a, c, b), (b, c, d)):
            p0, p1, p2 = (P[k] for k in t)
            n = np.cross(p1 - p0, p2 - p0)
            for k in t:
                acc[key(P[k])] = acc.get(key(P[k]), 0) + n
    for a, b, c, d in quads:
        for t in ((a, c, b), (b, c, d)):
            if np.linalg.norm(np.cross(P[t[1]] - P[t[0]], P[t[2]] - P[t[0]])) < 1e-9:
                continue  # a sliver where a pole closes
            tri = []
            for k in t:
                rest = tuple(P[k])
                n = acc[key(P[k])]
                n = n / (np.linalg.norm(n) or 1)
                sv = swings[k[0]][k[1]]
                tri.append(((rest, swing(rest, sv, 1.0), swing(rest, sv, -1.0)), tuple(n), uvs[k[0]][k[1]]))
            tris.append(tri)


# hat cone: 12 around, 11 rings up the profile
AROUND, RINGS = 12, 11
pts, uvs, sw = [], [], []
for i in range(RINGS + 1):
    t = i / RINGS
    r = R0 * (1 - t) ** 1.15 + 0.03
    ring = [bend(r * math.cos(2 * math.pi * j / AROUND), t * H + 0.18, r * math.sin(2 * math.pi * j / AROUND)) for j in range(AROUND)]
    pts.append(ring + [ring[0]])
    uvs.append([texel(j / AROUND, 1 - t, FELT) for j in range(AROUND + 1)])
    sw.append([max(0.0, (t - BEND_T) / (1 - BEND_T))] * (AROUND + 1))
add_grid(pts, uvs, sw)

# fur brim: a fat torus round the cone's foot, 12 around, 6 round the tube (rows = around, columns = the tube)
TUBE, TR = 6, 0.2
pts, uvs, sw = [], [], []
for i in range(AROUND + 1):
    a = 2 * math.pi * (i % AROUND) / AROUND
    ring = []
    for j in range(TUBE):
        b = 2 * math.pi * j / TUBE
        rr = R0 + 0.05 + TR * math.cos(b)
        ring.append((rr * math.cos(a), 0.2 + TR * 1.1 * math.sin(b), rr * math.sin(a)))
    pts.append(ring + [ring[0]])
    uvs.append([texel(j / TUBE, 0.5 - 0.5 * math.sin(2 * math.pi * j / TUBE), FUR) for j in range(TUBE)] + [texel(1.0, 0.5, FUR)])
    sw.append([0.0] * (TUBE + 1))
add_grid(pts, uvs, sw)

# the bell at the end of the curl, a little below it
tip = bend(0.03, H + 0.18, 0.0)
bc = (tip[0] + 0.06, tip[1] - 0.16, tip[2])
BR, BLAT, BLON = 0.22, 5, 8
pts, uvs, sw = [], [], []
for i in range(BLAT + 1):
    phi = math.pi * i / BLAT
    ring = [(bc[0] + BR * math.sin(phi) * math.cos(2 * math.pi * j / BLON), bc[1] + BR * math.cos(phi),
             bc[2] + BR * math.sin(phi) * math.sin(2 * math.pi * j / BLON)) for j in range(BLON)]
    pts.append(ring + [ring[0]])
    uvs.append([texel(j / BLON, i / BLAT, BELL) for j in range(BLON + 1)])
    sw.append([1.3] * (BLON + 1))  # it swings a little past the felt holding it: it rings
add_grid(pts, uvs, sw)

# the blood pool: an irregular disc under it
POOLN = 14
rest_c = (0.0, 0.02, 0.0)
edge = []
for j in range(POOLN):
    a = 2 * math.pi * j / POOLN
    r = 1.85 * (1 + 0.16 * math.sin(3 * a + 0.7) + 0.08 * math.sin(5 * a + 2.1))
    edge.append((r * math.cos(a) + 0.15, 0.02, r * math.sin(a) * 0.8))
for j in range(POOLN):
    k = (j + 1) % POOLN
    tri = []
    for q in (rest_c, edge[k], edge[j]):
        u = 0.5 + (q[0] - 0.15) / 4.6
        v = 0.5 + q[2] / 3.8
        tri.append(((q, q, q), (0.0, 1.0, 0.0), texel(u, v, POOL)))
    tris.append(tri)
# its swollen edge (the meniscus), so a level camera sees a puddle and not a line
for j in range(POOLN):
    k = (j + 1) % POOLN
    a, b = edge[j], edge[k]
    lo_a, lo_b = (a[0] * 1.04, -0.06, a[2] * 1.04), (b[0] * 1.04, -0.06, b[2] * 1.04)
    out_n = (math.cos(2 * math.pi * (j + 0.5) / POOLN), 0.3, math.sin(2 * math.pi * (j + 0.5) / POOLN))
    for t in ((a, lo_a, b), (b, lo_a, lo_b)):
        tris.append([((q, q, q), out_n, texel(0.5 + 0.4 * math.cos(2 * math.pi * j / POOLN), 0.85, POOL)) for q in t])

# ---- into icon space and out ---------------------------------------------------------------------------------
FOOT = -1.05  # where y = 0 (the pool) lands


def to_icon(p):
    x, y, z = p
    return (x - 0.25, FOOT - y, -z)


def fx(v):
    return max(-32768, min(32767, int(round(v * 4096))))


def rle(px):
    out, i, n = [], 0, len(px)
    while i < n:
        j = i
        while j < n and px[j] == px[i] and j - i < 0x7FFF:
            j += 1
        if j - i >= 2:
            out.append(struct.pack('<HH', j - i, px[i]))
            i = j
            continue
        k = i
        while k < n and k - i < 0x7FFF and not (k + 1 < n and px[k + 1] == px[k]):
            k += 1
        if k == i:
            k = i + 1
        out.append(struct.pack('<H', 0x10000 - (k - i)) + struct.pack('<%dH' % (k - i), *px[i:k]))
        i = k
    return b''.join(out)


def build():
    verts = [v for t in tris for v in t]
    shapes = 3
    out = [struct.pack('<IIIfI', 0x00010000, shapes, 0x0E, 1.0, len(verts))]
    for shapes_pos, n, uv in verts:
        for s in range(shapes):
            x, y, z = to_icon(shapes_pos[s])
            out.append(struct.pack('<hhhh', fx(x), fx(y), fx(z), 0x400))
        nx, ny, nz = n[0], -n[1], -n[2]
        out.append(struct.pack('<hhhh', fx(nx), fx(ny), fx(nz), 0x400))
        out.append(struct.pack('<hh', uv[0], uv[1]))
        out.append(bytes([0x7F, 0x7F, 0x7F, 0x80]))
    times = [0, 6, 12, 18, 24, 30, 36, 42, 48, 90]
    keys = [[1, 0, 1, 0, 1, 0.4, 1, 0.65, 1, 1],  # at rest
            [0, 1, 0, 0, 0, 0.6, 0, 0, 0, 0],  # swung one way
            [0, 0, 0, 1, 0, 0, 0, 0.35, 0, 0]]  # the other
    out.append(struct.pack('<IIfII', 1, 90, 1.0, 0, shapes))
    for s in range(shapes):
        out.append(struct.pack('<II', s, len(times)))
        for t, v in zip(times, keys[s]):
            out.append(struct.pack('<ff', float(t), float(v)))
    img = make_texture()
    px = [((int(r) >> 3) | ((int(g) >> 3) << 5) | ((int(b) >> 3) << 10)) for r, g, b in img.reshape(-1, 3)]
    packed = rle(px)
    out.append(struct.pack('<I', len(packed)) + packed)
    return b''.join(out), img, len(verts)


if __name__ == '__main__':
    data, img, nv = build()
    open(sys.argv[1], 'wb').write(data)
    if '--png' in sys.argv:
        from PIL import Image
        Image.fromarray(img).resize((512, 512), Image.NEAREST).save(sys.argv[sys.argv.index('--png') + 1])
    print('%s: %d vertices (%d triangles), 3 shapes, %d bytes' % (sys.argv[1], nv, nv // 3, len(data)))
