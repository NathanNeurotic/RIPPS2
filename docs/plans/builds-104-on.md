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

## Build 105: RIPDISC (a disc to storage or files): done 10/19, released in v1.0.7-beta
- [x] Panel after 4.2 s, SELECT held 4.2 s, confirm (size, TIME, place), START; games to ISO / UL parts (over 4 GB on
      a drive that may be FAT32) / PS1 BIN+CUE in EMBER/games; media via Memory Files (RIPPED clipboard, PASTE, MEDIA
      beside AUDIO, audio CD folder named on the keyboard after); README.txt in AUDIO and MEDIA; any .ogg/.wav in
      AUDIO is music. Time estimate before START, learned per storage kind (ripdisc_kbs_<storage>_<cd|dvd>).
- [x] Lab 10/19: POINIES POIN (1.2 GB) from PCSX2's drive to a fresh exFAT HDD image (scratchpad mkexfat.py) is
      byte for byte the source. Not lab-checked: DVD video, audio CD (PCSX2 types no image as an audio CD), PS1,
      UL parts, dual layer: on the testers' list.
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

## Build 106 (as built): POWER OFF in the in-game menu, the star on the left, list keys: done 10/19
- [x] POWER OFF, the in-game menu's last item, second press (not for a disc game). The panel is drawn on the host
      by test_ripps2_build87.py; the lab could not reach a game (its known launch hang), so consoles confirm it.
      10/20: the hang is fixed (ripshot.md step 0) and POWER OFF was seen in the lab (IGR test build).
- [x] Star left by default (own column), Settings > Game Sources > Starred Games Star (Theme/Left/Right/Hidden); a
      left star sends the decorator to the row end. ItemsList keys star, star_image, highlight (bar/line/none),
      decorator_all, decorator_ps2/_ps1/_app; RIPPS2-themes has them (THEME_KEYS.md, glossary, checker, Adapt).

## RIPSHOT (screenshots in game): built as build 108, released in v1.0.9-beta
**The full plan, decided with the user 10/20: [ripshot.md](ripshot.md)** (6 shots a game on per-game rolls, Manual
developing by default, ART 250x188 and MEDIA full size as 8-bit PNG, the SCRn theme key, every word on screen).
The notes below are the first findings, kept for the record.
Findings 10/19 (why it did not fit in 106 under the usage limit): nothing in-game can create a file unless the
IOP has a file system driver live for that drive (OPL's GPL IGS writes with fioOpen after the pause); the frame
must be read back from GS memory (a GS-to-EE transfer the menu does not do yet) and ee_core has about 11 KB
of room. Paths: keep a small image in RAM the game is not using and write it when RIPPS2 is back, or
pre-allocate a file before launch and write its sectors as VMC writes do. The design stays as below.
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

## Build 107: search in Memory Files: done 10/19, released in v1.0.7-beta
- [x] SEARCH FILES in MC EXPLOIT INSTALLER's tile (magnifier icon), breadth first over the browser's drives, one
      folder open at a time, 10 deep, 150 results; a result opens the tree with the cursor on it. Lab: the tile.
- The Memory Files settings tiles: **MC EXPLOIT INSTALLER becomes SEARCH**, with a new icon. It finds any file
  (media, saves, games, ELFs) by name on the started drives and opens the file tree where it is.

## Build 109 (testers' reports, 10/19-10/20): done 10/21, released in v1.0.9-beta
- [x] MMCE boots fast: the card's last list (`RIPPS2.LST`) shows at once, the card is read again in the background.
      The lab has no MMCE: testers time it.
- [x] The MMCE scan pauses after each entry (1 ms) and a frame after each disc read, so the pads keep working.
- [x] Settings > General > Save Settings To: Memory Card, Internal HDD (`mass<n>:/RIPPS2` on BDM ATA, else
      `pfs:/RIPPS2`), Custom Path. Lab: saved to mass0:/RIPPS2. Load after a power cycle and the APA HDD: testers.
- [x] A settings page's title clear of its line (DIA_HEADER_GAP 8). Lab: every page.
- [x] Hotfix 10/21: Internal HDD saved as `ata0:/RIPPS2` (typed), config.path keeps a typed path's spelling. The
      untyped `mass0:/RIPPS2` made the boot walk USB, MX4SIO (froze PCSX2: debug log ends at MX4SIO start), iLink,
      ATA. Lab: saved on a drive with no RIPPS2 folder, restart read the HDD settings (theme from the HDD, not the card).
- [ ] Open: "simplify the audio approach for 0 bugs on real hardware" and the menu music missing after a rip:
      waiting on reports with steps (the build 109 test list asks for them).
- [ ] Open: FifthFox's folders suggestion (Browse Folders in Game List already exists; ask what is missing).

## Build 110 (the user, 10/21: "speed them all up", "add them or any other source"): done 10/21, released in v1.1.0-beta
- [x] supportbase.c sbSnapShow / sbSnapScanned / sbSnapForget: build 109's MMCE list for every source (MMCE, every BDM
      drive, SMB): RIPPS2.LST beside CD and DVD, shown when the source answers, read again on the next idle poll (BDM and
      MMCE are polled every 10 s idle on Storage; SMB joins that poll until read, its timed rescans need Automatic
      Refresh). Lab: the reel HDD wrote RIPPS2.LST (6 games, 1160 bytes) and the second boot listed from it, unchanged.
- [x] MX4SIO scans pause for the pads (sbSetPadBreath around the BDM scan of an SDC drive). Lab has no MX4SIO.
- [x] APA HDD: games.bin cache on by default (ripps2_hddcache_v 110, once for older configs) and the APA table read once
      more on the next idle poll (updateDelay GENREFRESH until then). Lab has no APA image: testers.
- [x] Save Settings To: USB Drive, MX4SIO, iLink, MMCE (typed usb0:/mx4sio0:/ilink0:, mmceN:/RIPPS2; MMCE loads its
      driver at boot through prepareMmceSettingsPath). Lab: the choices and hints; USB with no USB drive keeps the card.
- [x] The info page asks for the size of a game the d-pad reaches (it read 0 MiB). Lab: Burnout 3 2734 MiB.
- [x] Settings pages run their own dialog loop, which draws neither guiShowToast nor the RA notice line (favourites'
      toasts on Storage did not show in the lab either): a missing drive is said in a message box. Lab: shown, OK.

## Build 111 (the user's notes and lukeatmynose's build 110 report, 10/21): done 10/21, released in v1.1.1-beta
- [x] The BIOS Music rip (24 kHz mono) played nothing: audsrv_set_format refuses it ("BGM: audsrv cannot play 24000
      Hz, 1 ch"). wavRead converts any 16-bit WAV to 48 kHz stereo (mono to both sides, linear between frames). Lab:
      the capture correlates 0.69 with the WAV's start (build 110: 0.31, silence).
- [x] bgmLoad: RIPPS2's music pick on every theme (Adapt and Adapt Rx played nothing without a bgm.ogg). Lab: both.
- [x] sfxInit skips a load when every event's file (path, size, date, chosen as the load chooses) and audsrv's start
      are the same. Lab: a SELECT cycle Adapt > Adapt Rx > RIPPS2 > RIPGRID > RIPFLOW > Adapt reloads nothing.
- [x] Save Settings To with a memory card in: an explicit save leaves mcN:/RIPPS2/config.path, read when config.path
      beside the ELF is out of reach; Memory Card chosen again removes both. Lab: four boots (HDD kept with the
      ELF's config.path hidden; Memory Card stuck after).
- [x] The star at its row's centre (themes.c), the Settings highlight centred on the font's centreline (dia.c).
- [x] lukeatmynose on the About page and in the README.
- [x] The sounds lesson (media/b111/ripps2-v111-sounds.mp4): takes111.ps1 + short111.py in the reel kit.

## Build 112 (the user, 10/21: "the error red screen menu instead of the standard osdsys menu theme"): done 10/21, released in v1.1.2-beta
- [x] BIOS Music's piece: SNDWARNS (build 100's) is the red screen's (its tonal 8 s opening, then waves); the main menu
      plays SNDCLOKS, the clock's (5:04). Timing correlation could not match either to the "02 Menu" recording; the
      PS2's own screens decided it (the main menu's orbs are the clock).
- [x] rbsMusicOpen(seq); ripps2BiosMusicSamplesOf/FromImageOf(piece) with per-piece hall and gain (the clock's
      0.0781 / 1.5812 by ripps2BiosMusicMeasure; the red screen's reproduce build 100's 0.0807 / 1.3875 exactly).
- [x] rbsPickMusic: THE MENU MUSIC (THE CLOCK) first and chosen, THE RED SCREEN MUSIC (DISC WARNING), BOTH; then
      the folder question; bgm_00 Menu.wav and bgm_01 Red Screen.wav. Lab: menu only 14,592,044 bytes, both, the
      capture plays the clock (0.85 against the WAV).
- [x] 9 new sentences in all 32 translations.
- [x] The sounds walkthrough, one take (media/b112): takes111.ps1 tut_c2 + short112.py.

## Build 113 (planned, the user 10/21)
- [ ] Fast Cache: a Game Sources > Cache submenu showing each source's list (RIPPS2.LST, APA games.bin) and its
      state, the old BDM/HDD/SMB/APA cache rows moved in with tooltips saying what still matters; outdated rows go.
- [ ] All Games from the sources' saved lists before the drives answer (a master list), if Fast Cache is on.
- [ ] Legacy theme key: a theme without it shows Storage only, Launch Disc and Memory Files in the START menu
      (backing out returns to its Storage); the built-ins and the Adapt pack set it and keep the three categories.
- [ ] Adapt sidebar: vertical icon glyphs for the categories (Left from the list, RIPGRID-style highlight, select to
      switch), an overlay on Launch Disc and Memory Files, the freed top space showing the full name as a header,
      Circle's sources in the same style; theme keys; in the Adapt pack. Header font: the user picks from
      docs/plans/mockups/b113-header-fonts.png.
- [ ] Mother font: one master font with per-element bold / case / tracking keys (FreeType emboldening).

## Skipped
- **RIPCON** (format conversion, as OrbitOPL Toolbox does on a PC): not done on PS2 hardware yet, likely failure
  prone, and a smaller format can be less supported by the loaders. Skipped by the user (2026-10-18).
