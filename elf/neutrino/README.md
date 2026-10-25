# Neutrino (bundled)

**Neutrino** is a small, fast and modular PS2 device emulator by **rickgaiser**, licensed **AFL-3.0**
(`LICENSE.txt`, beside this file). Releases: <https://github.com/rickgaiser/neutrino/releases>

`neutrino-1.8.0-61-g7be8de2.tar.gz` is Neutrino's development build of 31 August 2026,
`neutrino_v1.8.0-61-g7be8de2.7z` from the `latest` release (SHA-256
`fcec9c78c8cfd844a298d16341ae6885e0ae47835070ce84e374da006c024d12`, master `7be8de2`), repacked, unmodified, as a
gzip'd ustar (573,440 bytes of tar, 71 files, SHA-256 `e4a71529db9b1c5a366c5fa52e8521d8f1761c36ee4ef174646a415112bb7fab`)
with Neutrino's licence added. Its PC-side `udpfs_server/` folder is left out: it is not for the PS2.

Build 115 moved to it from 1.8.0 (March 2026): 61 commits of fixes since, among them MMCE, CDVDMAN and CDVDFSV
(a streaming callback, a read race, retries on lock contention), more games in `compat.toml`, the PS2 logo patch,
576p on more models, and cheats. Its `version.txt` says `v1.8.0-61-g7be8de2`. 1.8.0 (official
`neutrino_v1.8.0.7z`, SHA-256 `17f760f9293d3cba6e9e3fbf601801d0784fe7048d16b4e68c3358aff589910a`) is in this folder's
history: `git log -- elf/neutrino/neutrino-1.8.0.tar.gz`.

RIPPS2 carries it inside RIPPS2.elf. When a game starts through Neutrino and no Neutrino is found where
RIPPS2 looks (the path in Settings, the game's drive, the memory cards, any started drive), RIPPS2 asks where to
install this one: the game's drive (`<drive>/neutrino/`) or a memory card (`mc0:/neutrino/`, `mc1:/neutrino/`).
Your own Neutrino always comes first, whatever its version: RIPPS2 reads its `version.txt` (or, for an older kit,
its `config/` files) and sends it only the options it knows. `config/system.toml` is written last, so an
interrupted copy is never taken for a complete install.

Repack a newer release the same way with `tools/dev/pack_neutrino.py <unpacked folder> <LICENSE> <out.tar.gz>`; it
prints the tar's size, which goes into `NEUTRINO_TAR_SIZE` (src/ripps2ember.c).
