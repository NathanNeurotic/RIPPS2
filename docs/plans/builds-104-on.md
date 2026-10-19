# Builds 104 on: languages, RIPDISC, RIPSHOT, the browser search

The user's requests of 2026-10-18, in the order they are built. Each build: patch, host tests, CI, one scripted lab
run (warn before PCSX2 runs), fixes folded into that build's patch, then tick it here. No release unless asked.

## Build 104: languages (all major ones at once)
Asked for by Algol (French, psx-place). One ELF; the words come from a language pack.
- [x] `_t("English")` for every on-screen string in RIPPS2's own files (N_ for tables, `_t` where shown), and the
      RIPPS2 strings in RiptOPL's files.
- [x] Keyed language files (`#!RIPPS2LANG 1`: FNV-1a of the English, a tab, the translation) carry Open PS2 Loader's
      strings and RIPPS2's, so a pack made for one build keeps working in the next. Old line-numbered files still load.
- [x] A letter a font lacks comes from the language font, then font_CJK, at that font's own size; caps fonts, the
      hints' sentence case and the source toast handle accented, Greek and Cyrillic letters; CJK lines break
      between characters.
- [x] `RIPPS2-languages.zip` (LNG/lang_<Name>.lng plus the fonts a script needs) built in CI from
      `elf/lang/<Language>.yml`, OPL's translations and RiptOPL's overlays; licences checked for every font.
      CI's pack report (10/19): every language's letters are in its font except Laotian (no free Lao font) and
      Persian (upstream's pre-joined letters; the font_Arabic DejaVu subset has no presentation forms).
- [x] Translations: French first and complete, then every language in RiptOPL's list (33 of 33; Ryukyuan's gaps come
      from Japanese, `STRINGS_FROM`). Laotian (10/19) in Noto Sans Lao, fetched with the user's OK; Lao/Thai lines
      break between syllables (`trSea` in ripps2tr.c).
- [x] Arabic and Persian drawn right to left with joined letters (10/19). DejaVu Sans with the presentation forms
      (user's OK), cut by `elf/lang/make_lang_fonts.py`; `ripps2Rtl` (ripps2tr.c) shapes from a Unicode-made table
      (`make_arabic_forms.py`) and orders each line (simplified bidi: L runs kept, brackets mirrored) in
      fntRenderString, measuring the shaped text; zero-advance marks centre over their letter. Persian's 249
      pre-joined upstream lines dropped by the pack and translated. Left: right alignment of RTL lines.
- [x] Lab: French and one non-Latin language on RIPPS2, RIPGRID, RIPFLOW and Adapt (long words, wraps, hints).
      10/19: French and German (RIPPS2), Russian (all four), Japanese (RIPPS2: STATUS, Launch Disc, settings
      hints). Fixed from it: Sleek Case lowercase б (read as в), CJK settings hints wrapping a clause whole, a theme
      hint row overflowing both edges (now a size smaller). Not seen yet: Arabic/Persian (left to right still),
      Greek, Turkish, Vietnamese on screen (the pack report shows their fonts have every letter).

## Build 105: RIPDISC (a disc to storage or files)
The user's design:
- On the launch disc page, after **4.2 s** on the page, a clean glass panel fades in at the centre as a modal, only
  when the disc can be ripped: a short header **RIPDISC** and one line ("add this game to your storage" for a game,
  "add this media to your files" for audio/video), with the SELECT glyph and **Hold**.
- Holding SELECT for 4.2 s opens a confirm step with the **size and the location**.
  - A game: Cross/Circle confirm, back cancels, then START rips the game to storage (an ISO in the drive's DVD/CD
    folder, so it shows in the games list).
  - Media: confirm, then pick the place by navigating the file tree in the browser, the clipboard reading
    **RIPPED** where it says CUT or COPIED. Then confirm and START rips the media to files.
- An audio CD gets a folder named after its title; after the rip is placed, a rename/confirm of the name opens by
  itself. The default place for ripped media is a new `/MEDIA` folder beside `/AUDIO`, so the rips stay apart from
  the sounds and music in AUDIO.
- A `README.txt` in AUDIO and in MEDIA, written by RIPPS2 and user friendly: what the BIOS sound effects and the CD
  player's music are, what RIPDISC puts in MEDIA, and that any track copied from a CD into AUDIO shows in the BGM
  selection (per theme) without renaming it to bgm_04. Combine with the notes RIPPS2 already has (STATUS, hints).

How it maps onto the code (read 10/19):
- **What is in the drive** is already known: `discPollWorker` (ripps2ui.c) sorts the disc on the IO worker (PS1 game,
  PS2 game with its ID and metadata title, ESR, DVD video, audio CD, a CD with sound tracks). It gains a kind and the
  ID/title as data, and a game's size from its ISO 9660 primary volume descriptor (sector 16, offset 80: the volume's
  sectors), so the modal can say "rippable" without asking the drive again.
- **The modal** draws in `ripps2RenderLaunch` over START LASER (glass via `ripps2DrawPanelGlass`, as the CD player);
  a launch-page clock starts when the disc line settles and the page is shown. SELECT is free on that page; the hold
  reuses the game list's theme-cycle timing (menusys.c, 4.2 s), with a ring filling round the glyph.
- **Reading and writing** follows the CD player's copy (`cdCopy`, ripps2cd.c): chunked `sceCdRead` with retries on
  the IO-free GUI path, a progress frame with cancel, the file removed on failure. Games: 2048-byte sectors to
  `<drive>/DVD|CD/<ID>.<Title>.iso` (a DVD over 4 GB needs exFAT or the internal HDD: refused up front on a FAT32
  stick). PS1 games: 2352-byte sectors to `EMBER/<Title>/<Title>.bin` plus a `.cue` (Ember plays CUE/BIN). Audio
  CDs: one WAV a track (cdWavHeader) in `MEDIA/<name>/`. DVD video: VIDEO_TS's files copied through cdrom0:.
- **Placing media** goes through Memory Files (ripps2files.c): the clipboard (`fbClip*`) gets a RIPPED kind that
  names the disc instead of files; PASTE in the chosen folder starts the rip there. MEDIA beside AUDIO is the folder
  the browser opens on.
- Lab: PCSX2 mounts an ISO or a CUE as the disc, so a PS2 ISO, a PS1 CUE/BIN and an audio-CD CUE can each be ripped
  to the lab's exFAT HDD image and the result compared byte for byte (md5) with the source.

## Build 106: RIPSHOT (screenshots in game)
- In the in-game pause menu: a screenshot item. Taking one flashes the pause menu and shows a preview with
  **Delete** and **Keep**; only Keep saves.
- Saved neatly and plainly named, to either or both (a setting): an individual game folder in MEDIA, or OPL's
  ART folder as the game's screenshot (`<ID>_SCR.png`, then the next free `_SCR2`, ...), so themes that show
  screenshots show the player's own.
- OPL's IGS (ee_core igs_api.c) is GPL-3: write it fresh. ORBIT's AFL neutrino-igr shows how the frame under the
  menu is read (BITBLTBUF/TRXDIR). ee_core room is tight (build 103: gc-sections, stack 0x2C80).
- **Power off from the in-game menu** (user, 10/19): a shutdown item as the menu's LAST choice, confirmed like Exit
  (the first press arms it and says so, the second powers the console off), so a player can turn the PS2 off right
  there in the game.

## Build 107: search in Memory Files
- The Memory Files settings tiles: **MC EXPLOIT INSTALLER becomes SEARCH**, with a new icon. It finds any file
  (media, saves, games, ELFs) by name on the started drives and opens the file tree where it is.

## Skipped
- **RIPCON** (format conversion, as OrbitOPL Toolbox does on a PC): not done on PS2 hardware yet, likely failure
  prone, and a smaller format can be less supported by the loaders. Skipped by the user (2026-10-18).
