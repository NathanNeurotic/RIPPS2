# Build 118 translation kit

The ART Pack (Settings > Game Sources > Cache): 15 strings in `s118.json` and 3 labels (RIPPS2_ART_PACK,
RIPPS2_ART_PACK_BUILD, HINT_RIPPS2_ART_PACK) in `labels118.json`, translated for all 32 languages in `batch1.py` to
`batch4.py` (each writes `tr118/<Language>.json`) and merged with `merge118.py`.

    python tools/lang118/batch1.py            (and batch2, batch3, batch4)
    python tools/lang118/merge118.py <Language> [<Language> ...] [--dry]
    python elf/lang/ripps2lang.py check

Every `%s` and `%d` keeps the English order: printf takes the arguments in that order, so a translation builds its sentence
around them (the first string's pictures come before its folders in every language). ART and `art.tar` stay as they are:
they are the folder's and the file's names on the drive.
