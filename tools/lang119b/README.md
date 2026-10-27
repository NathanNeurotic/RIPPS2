# Build 119 translation kit, second round

EXIT goes to the browser unless the IGR Path can be loaded after the reset (STATUS says when a path is passed over, and the
IGR Path hint says so), and the About page's testers and credits: 7 strings in `s119b.json` and the `HINT_EXITPATH`
label in `labels119b.json`, translated for all 32 languages in `batch.py` (writes `tr119b/<Language>.json`) and merged
with `merge119b.py`. The two strings the source no longer has ("A game's EXIT: the browser" and "RIPFLOW's type") are
dropped from every language by the merge.

    python ../../elf/lang/ripps2lang.py extract <RiptOPL>
    python tools/lang119b/batch.py
    python tools/lang119b/merge119b.py <Language> [<Language> ...] [--dry]
    python elf/lang/ripps2lang.py check

EXIT, IGR Path, BOOT LOCK, BIBLE, the boot loaders' names, FAT32, USB, ELF, Discord, GitHub and the libraries' names stay
as they are. Every `%s` keeps the English order.
