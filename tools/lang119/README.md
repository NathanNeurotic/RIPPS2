# Build 119 translation kit

The ART Pack's flow as the other long jobs have it (sizes, the time, the numbered bar, the room check): 14 strings in
`s119.json`, no labels, translated for all 32 languages in `batch.py` (writes `tr119/<Language>.json`) and merged with
`merge119.py`. The four strings the flow no longer shows are dropped from every language by the merge.

    python tools/lang119/batch.py
    python tools/lang119/merge119.py <Language> [<Language> ...] [--dry]
    python elf/lang/ripps2lang.py check

Every `%s` and `%d` keeps the English order. The upper-case strings are the progress bar's heading and line, as COPYING
and COMPRESSING are. ART and `art.tar` stay as they are: the folder's and the file's names on the drive.
