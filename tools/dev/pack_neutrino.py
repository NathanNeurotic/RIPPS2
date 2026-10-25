"""Repack a Neutrino release folder as RIPPS2 carries it: a gzip'd ustar of the PS2-side files (udpfs_server/ left out),
Neutrino's licence added, entries sorted with fixed owner and time, so the same folder always gives the same bytes.

    python pack_neutrino.py <unpacked release folder> <LICENSE> <out.tar.gz>
Prints the tar's size (NEUTRINO_TAR_SIZE) and both SHA-256s.
"""
import gzip
import hashlib
import io
import sys
import tarfile
from pathlib import Path

src, lic, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
files = sorted(p for p in src.rglob('*') if p.is_file() and 'udpfs_server' not in p.relative_to(src).parts)
buf = io.BytesIO()
with tarfile.open(fileobj=buf, mode='w', format=tarfile.USTAR_FORMAT) as t:
    def add(name, data):
        ti = tarfile.TarInfo(name)
        ti.size = len(data)
        ti.mtime = 1772668800  # 2026-03-05, fixed
        ti.mode = 0o644
        ti.uid = ti.gid = 0
        ti.uname = ti.gname = ''
        t.addfile(ti, io.BytesIO(data))
    add('LICENSE', lic.read_bytes())
    for p in files:
        add(p.relative_to(src).as_posix(), p.read_bytes())
tar = buf.getvalue()
gz = io.BytesIO()
with gzip.GzipFile(fileobj=gz, mode='wb', mtime=0, compresslevel=9) as g:
    g.write(tar)
out.write_bytes(gz.getvalue())
print('files', len(files) + 1)
print('tar size', len(tar))
print('tar sha256', hashlib.sha256(tar).hexdigest())
print('tgz size', len(gz.getvalue()))
print('tgz sha256', hashlib.sha256(gz.getvalue()).hexdigest())
