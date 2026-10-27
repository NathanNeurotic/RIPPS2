# Build 116 translation kit

BOOT LOCK through FMCB and OSDMenu, and a game's EXIT through the boot loader: 13 strings in `s116.json` and 2 labels
(HINT_EXITPATH, HINT_RIPPS2_BOOT_LOCK) in `labels116.json`, translated for all 32 languages in `batch1.py` to `batch4.py`
(each writes `tr116/<Language>.json`) and merged with `merge116.py`.

    python tools/lang116/batch1.py            (and batch2, batch3, batch4)
    python tools/lang116/merge116.py <Language> [<Language> ...] [--dry]
    python elf/lang/ripps2lang.py check

Every `%s` and `%d` keeps the English order: printf takes the arguments in that order, so a translation builds its sentence
around them. Each language names the IGR Path row as Open PS2 Loader's own translation does (its EXITTO label), and keeps
"Browser" as the word typed into it.
