# Build 115 translation kit

Build 115 added 102 strings RIPPS2 translates itself and 29 labels (14 new, 15 whose English changed). German is
done (`tr115/German.json`, merged into `elf/lang/German.yml`). The other 31 languages are still to do.

## Files

| File | What it is |
|---|---|
| `s115.json` | the 102 English strings, numbered 0 to 101 (the numbers the `s` keys use) |
| `labels115.json` | the 29 labels and their English |
| `tr115/<Language>.json` | one language's translations: `{"s": {"0": ..., "101": ...}, "l": {"LABEL": ...}}` |
| `merge115.py` | checks a language file and merges it into `elf/lang/<Language>.yml` |
| `glossary.txt` | per language, the words already used for Settings, All Games, Memory Files, STATUS, Theme, Auto... |
| `glossary2.txt` | per language, the button names (Circle/Cross), ACTIONS, PASTE, RIPPED, STORAGE, Regular, Shown |
| `stale.txt` | per language, the old translations of the strings whose English changed (reuse their wording) |
| `glossary.py` | makes glossary.txt again (`LNG_SRC=` a clone of github.com/ps2homebrew/Open-PS2-Loader-lang) |

## One language

1. Read its lines in `glossary.txt`, `glossary2.txt` and `stale.txt`.
2. Write `tr115/<Language>.json` in the shape of `German.json`, with the Write tool (a Git Bash heredoc mangles `\n`).
   - Keep every `%s`, `%d` in the same order, the same `\n` count (string 19 ends with `\n`, 15 and 18 have them
     inside), and the capitals of the English.
   - Names stay as they are: RIPPS2, BIBLE, PS2BBL, SD2PSX, MMCE, MX4SIO, POPSTARTER, Ember, Neutrino, RIPDISC,
     RIPFLOW, Fast Cache, Trust Cache, DIAG.TXT, BOOT LOCK, START, SELECT, the folder names (MEDIA, AUDIO).
   - STATUS rows hold 224 bytes and their right-hand notes 96 (`ripps2status.c` text[224], aside[96]): keep strings
     70 to 73, 80 to 82, 88, 89, 98 and 99 short, above all in Lao and CJK (3 bytes a letter).
   - Laotian: Lao letters only (its font has no Thai). Arabic and Persian: plain letters, never the presentation forms
     (U+FB50 to U+FDFF, U+FE70 to U+FEFF); RIPPS2 joins and lays them out itself.
3. `python tools/lang115/merge115.py <Language>` (from the repo root; `--dry` only checks). It refuses a file with a
   missing entry or different `%` conversions or line breaks, drops the strings the template no longer has, replaces
   labels in place, and writes CRLF.
4. `python elf/lang/ripps2lang.py check`: the language should read about 1117 of 1144 (what is left is credits, names,
   URLs and stick labels, kept English on purpose) with no "conversions differ" line.

Kept English, not in `s115.json`: the credit lines, LX:/LY:/RX:/RY:, PID:/VID:/REV:, USB, MX4SIO, iLink,
psx-place.com, github.com/rickgaiser/neutrino, ART, MEDIA.

`elf/lang/ripps2lang.py` has `REWORDED` (HINT_EXITPATH, HINT_BDM_START): Open PS2 Loader translates those two labels'
old English, so RIPPS2's own label translations win for them. Every language file needs both (the kit has them).
