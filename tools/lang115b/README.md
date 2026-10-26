# Build 115 evening translation kit

The strings and labels build 115 added on 10/26 evening (Fast Boot, the rip destinations, BIBLE's "RIPPS2: Setting up BBL
1.20" wording and RESTORE, POPSTARTER's two file sets, the file CD player's heading): 32 strings in `s115b.json` and 2
labels in `labels115b.json`, translated for all 32 languages in `batch1.py` to `batch4.py` (each writes
`tr115b/<Language>.json`) and merged with `merge115b.py` (`tools/lang115/merge115.py` pointed at these files).

    python tools/lang115b/batch1.py            (and batch2, batch3, batch4)
    python tools/lang115b/merge115b.py <Language> [--dry]
    python elf/lang/ripps2lang.py check

Every `%s` and `%d` keeps the English order: printf takes the arguments in that order, so a translation builds its sentence
around them (the merge checks the conversions, not their order). Lao uses Lao letters only; Arabic and Persian plain letters.
