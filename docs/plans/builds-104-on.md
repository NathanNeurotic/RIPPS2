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

## Build 113 (the user 10/21-10/22): done 10/22, released in v1.1.3-beta
- [x] Fast Cache: Game Sources > Cache holds Fast Cache (each source's RIPPS2.LST: on by default, off reads every list
      from its source first, as before 110), Cache Game List (HDD APA) and Automatic Refresh, each with a tooltip;
      the BDM/HDD/SMB read-ahead caches went to Game Launching (they act in game, not on lists). Not done: a line per
      source showing its saved list's state (each support module keeps its own sb_snap_t; needs an accessor each).
- [ ] All Games from the sources' saved lists before the drives answer (a master list), if Fast Cache is on. Moved to
      build 114 (10/22): every All Games row hands launch, config and art to its source's own list, so rows shown
      before the sources start need a saved master list, a wait for their source at launch, and a hand-over when the
      sources come up, inside mixsupport.c's rebuild locking (a rebuild race crashed the console in build 66).
- [x] Legacy theme key (lab pass on the release ELF, 10/22: Adapt Rx with categories=storage, takes113.ps1 legacy): `categories=three|storage`. Unset, a theme using any RIPPS2 key
      (towers, bg_blur, source_name, glyph_set, sounds, color_theme, category_*, page_buttons, launch_disc) keeps
      the three, so an older Adapt pack is not cut down; one made for OPL is legacy: no bar, no sidebar, LAUNCH DISC
      and MEMORY FILES first in the START menu, the cancel button (or L1 / R1) back to Storage, L1 / R1 turn the
      list's pages as in OPL. The built-ins always have the three; the Adapt pack (edition 113) sets three.
- [x] Adapt sidebar (two lab passes, 10/22): glyphs (elf/theme/make_sidebar_icons.py atlas) in Adapt's frosted bar,
      the bar a full strip on Launch Disc and Memory Files (sidebar_bar=pages), no page titles. Keys category_layout=
      sidebar (column means it too), sidebar_x/_width/_drawer/_bar/_color/_tint/_accent_color/_accent_tint; Colors and
      More > Category Layout (Theme, Across the Top, Sidebar) in every language. Drawer names in Roboto Condensed Bold.
- [x] Trim (the user 10/22: no stale bundled launchers; done: RIPPS2.elf 3,197,444 -> 2,738,756 bytes): RIPPS2.elf v1.1.2 is 3.1 MB packed, 5.1 MB stored before
      packing. Already-compressed blobs pack no smaller, so cutting one saves about its stored size: Ember 281 KB
      (gzip of the 1.6 MB Beta-2), POPSTARTER 164 KB, Neutrino 241 KB (1.8.0 tar.gz), BIBLE's PS2BBL KELFs 334 KB;
      OPL's default-theme background incebtion.png 76 KB; fonts 215 KB in all. Plan: POPSTARTER and Ember become
      finders only (the user's own copy, found where RIPPS2 already looks: Settings path, POPS / EMBER / APPS, the
      memory cards), the file type tied to its launcher (VCD to POPSTARTER, CUE/BIN to Ember), and a missing one
      says where to get it and where it goes, with no install from a bundled copy. Neutrino and BIBLE stay (the
      user). Done: the blobs, installs and STATUS install rows gone; a missing launcher names the path it looked at;
      elf/ember and elf/popstarter keep the credits and where to get each; About and the README credit both.
      incebtion.png stays for now: the built-in look's conf_theme_OPL.cfg still draws it (check before cutting).
- [x] Settings moves (the user agreed 10/22; done in two parts, both checked in the lab: docs/plans/lab/b113-settings-lab.png): Language kept on Interface (not General), Video Mode on Display (not
      Interface), GSM Defaults on Game Launching only, In-Game Menu on its page only (IGR Path joins it; the page goes
      under Game Launching); Game Sources > Cache (saved lists + their status, Cache Game List (HDD APA), Automatic
      Refresh with a tooltip); BDM/HDD/SMB Cache to Game Launching with a tooltip (in-game read-ahead, not lists);
      BDM/ETH Prefix Path and HDD Spindown to Game Sources; Show Recents beside the Starred Games rows; a Categories
      group in Colors and More (Category Bar, Category Layout = Theme / Across the Top / Sidebar, Category Order, Page
      Transition, Source Name); Hints and Glyphs moves under Interface with D-pad Glyphs and Button Hints.
- [x] Sidebar interaction (the user 10/22): Left on the list focuses the glyphs (the game let go, the hints Select /
      Back), Up/Down shows each glyph's drawer beside it (its name the first item, its list under it), Cross enters
      the list (the glyph keeps a dimmer frame), Cross on an item goes there; Circle on Storage opens the Storage
      drawer on the current source; the cancel button opens it on Launch Disc and Memory Files. The two HDD pages read
      HDD Games (exFAT) and (APA); the drawer widens to its longest name. Lab: tools takes113.ps1 sb_adapt.
- [x] RIPDISC's SELECT hold: 12 soft notches that fill clockwise (the one filling fades in), the ring given its own
      room so HOLD starts clear of it. Lab: takes113.ps1 rd_ring (a DVD video image).
- [ ] Game management (the user 10/22, maybe 114): hide games to a hidden list reachable only from Settings;
      delete a game completely and cleanly (on APA, the partition removed through the HDD's own calls, the PFS left
      whole).
      Hide can also compress (ISO to ZSO) into that hidden list; un-hide and un-compress when the drive has room.
- [ ] Fonts: no change to any face in 113 (the user, 10/22: weigh it first, keep every style). The weighing and
      the plan are in docs/plans/fonts-plan.md (recommended: the drawn faces stay, role keys reuse them, runtime
      bold only opt-in). The sidebar header reads a `header_font` key over the existing faces.
- [x] Mockup: docs/plans/mockups/b113-sidebar-sheet.png (make_b113_sidebar.py: the three glyphs drawn as vectors,
      the sidebar on real Adapt captures of Storage, Launch Disc, Memory Files, the Left focus and Circle's sources).

## Build 114 (the user 10/22: All Games before the drives answer, hide and delete games): built, not released
Where it stands (10/22 evening): every part below is in patch 0114 on `b114` with the RiptOPL merge, the launcher search, STATUS's
drives, the FreeType trim and the new words in all 33 languages; CI green, host tests clean, the hidden lab passes listed
under Tests and lab done. Not released and not posted: the user decides after the showcase. Decisions 1 to 5 were
taken as recommended (the user left them to me on 10/22, to recap): see the end of this section.
One patch, `elf/patches/0114-ripps2-games.patch`, on branch `b114`; test `elf/tests/test_ripps2_build114.py`. Three parts,
built in this order: A (the riskiest: All Games crashed a console in build 66 when its records were freed under a
cover lookup), then C (delete, which B's page uses), then B. Part D is a decision, not work yet.

### Field reports that shape 114 (10/22)
- **FifthFox, build 112** (SCPH-39001; iLink: Mobile Disk HD-338 enclosure, Prolific chipset, Seagate IDE drive, 6 to 4
  pin FireWire; MMCE; MX4SIO; APA on an SSD through a GameStar SATA network adapter). MMCE and its games show fast;
  USB, MX4SIO and iLink take a while to appear. Ember works from every device; iLink plays PS2 games with modes and
  logo; **Neutrino and POPSTARTER do not work from iLink** (ripto is on the drivers: with the right ones all of them
  have worked on this hardware). **Size**: 2 MB at most suggested; RIPPS2 runs from USB here, with LaunchStation,
  Neutrino and POPSTARTER on the memory card; several larger (over 8 MB, less reliable) card images crashed;
  3 MB and up is a tight squeeze.
  - The slow USB / MX4SIO / iLink lists: part A shows every game before they answer. RiptOPL upstream also skips
    the menu's USB and MX4SIO discovery settles (dde966b) and an unrelated iLink settle (a03b313).
  - Neutrino and POPSTARTER from iLink: upstream #1018 is exactly this (i.LINK logs back in after an IOP reset,
    e8b859c; RiptOPL's i.LINK driver in the Neutrino bundle, d954948; POPSTARTER's iLink after its IOP reset,
    4aa6c4a; the rebuilt usbhdfsd.irx.ilink, 7b07ff6). So the upstream merge is wanted sooner (decision 4).
  - **Size, measured on the v1.1.3 map** (RIPPS2.elf 2,714,228 bytes packed, 6.8 MB loaded): already-compressed
    blobs pack no smaller, so each saves its full size: Neutrino's tar 247 KB, BIBLE's three KELFs 342 KB (card
    83 KB, MX4SIO 133 KB, HDD 125 KB), OPL's incebtion.png 77 KB. Without all three: about 2.05 MB. FreeType's
    Type 1 modules (psaux, psnames: about 120 KB loaded) can go too if no face RIPPS2 reads is Type 1.
    Plan: CI builds **RIPPS2-lite.elf** beside RIPPS2.elf from the same code (no BIBLE install, Neutrino used
    where it is already installed on a card or drive, no OPL default background), under 2 MB, for memory card
    users; the full ELF stays as the user decided (decision 5).
- **Berion** (psx-place, on APA and PFS): "APA structure is bond to disk size. By writing disk image, you makes it
  wrong for your disk if size is different. This leads to APA chain corruption in future. The more partitions be
  created, the more mess is creating." What it means for RIPPS2: the driver's free-space merge on a delete
  (apaDeleteFixPrev / Next) joins neighbours by power-of-two size and alignment, capped at 1 GB, and the largest
  partition a disk takes comes from its own size (apaGetPartitionMax). The header does not record the size the
  table was made for (the formatter writes mbr.nsector = 0), so a cloned table cannot be read off one field.
  RIPPS2 never creates partitions (its driver refuses creates), so only part C's delete and the HDD MANAGER's
  remove touch the chain; both get the check in part C.

### Credits (the user 10/22, first: small and independent)
- [x] **Neutrino beside RiptOPL** on the About page: its own section sits mid-page while BUILT ON RIPTOPL closes it,
      so RiptOPL overshadows it. The opening lines name rickgaiser's Neutrino as the second game core with its
      link (github.com/rickgaiser/neutrino), and its section moves up beside BUILT ON RIPTOPL. (README done on main
      10/22: the intro, the on-board line and a credits entry right after RiptOPL's.)
- [x] **TESTERS** ends with "Special thanks to all the YouTube love as well: glad to help however you reach me."
      (the user's words), in all 33 languages; every tester list from now on carries it (README done 10/22).

### A. All Games from a master list
What is there now: each source keeps its own last list on itself (RIPPS2.LST, build 110), so a source's page fills
the moment that source answers. All Games (mixsupport.c) is built only from sources that answered, so at boot it
fills source by source, and with a Manual source it shows nothing until START is pressed.
- [x] **allgames.bin beside the settings** (where favourites.bin and recents.bin are: favGetNamedPath, so mc0:/RIPPS2
      or the drive Save Settings To chose; never on a game source, which is what has not answered yet). Header
      `RIPALL01`, count, FNV-1a sum; then per game: kind (PS2 ISO / VCD / CUE), source family (HDD APA, BDM by its
      driver type: usb, ata, sdc, ieee, udp; MMCE, SMB, UDPFS, HTTP), media (CD / DVD, for the icon), startup, name.
      About 50 bytes a game: 1,000 games is about 50 KB, a few hundred ms on a memory card. Written staged (a
      `.new` file, then renamed) as favourites.bin is (built: written in place, since a memory card has no rename
      and the lab found the `.new` copy left behind; a short or damaged file fails its sum and is not read), on the IO worker, only when the sum changed, only once
      every Auto source has answered (or 20 s after boot), never with Write Operations or Fast Cache off.
- [x] **Waiting rows.** The first All Games pass reads allgames.bin and shows every game at once, sorted and with
      duplicates dropped by the same rules as now (mixCompare). A row whose source has not answered has no owner
      list yet (owner NULL): mixRow, mixGetImage and mixGetArtMode already skip a NULL owner, so no reader can
      reach a source through it. Its art comes when its source does.
- [x] **The handover.** When a source publishes its list (opl.c already queues mixRequestUpdate behind it), its
      waiting rows are swapped for its real ones in the one locked publish mixUpdateItemList does now (mixSema
      held only for the pointer swap, never across a device read or a wait). The cursor stays on its game:
      updateMenuFromGameList keeps the selection by startup, and waiting rows carry their startup.
- [x] **Rows that go.** A source's waiting rows are dropped when its list comes (anything it no longer has is gone),
      or when it is known absent (built: start mode Off, or started and silent for 40 s): start mode Off, no HDD (hddCheck), no card in the MMCE slot, a BDM driver type
      with no device after BDM settles, SMB failing to connect. Before that, a moved stick only changes its BDM
      slot, and rows match by family and name, never by slot.
- [x] **Manual sources stay instant.** RIPPS2 defaults BDM to Manual for the instant boot. With the master list,
      All Games shows those games too: Cross on one starts that source (as All Games' START starts every source
      today), waits for its list, then launches. So boot stays instant and the list is still whole.
- [x] **Cross on a waiting row**: a message box "Starting USB Drive..." (the source's own name), Circle cancels. On
      the list's arrival the game is found by name (mixOwnerId already does this) and launched; a game the
      source no longer has says so and leaves the list; 30 s with no answer says the drive did not answer.
- [ ] (part, to 115) **Other buttons on a waiting row**: Delete and Hide refuse it; Square and R3 have nothing
      of their own yet.: Square shows the info page with what the master list knows (name,
      startup, source) and "starting"; R3 (star), Triangle's rename / hide / delete say to wait for the drive (a
      toast: this is the game list, where toasts draw).
- [ ] (to 115; the Cache page got the launcher lines instead) **Cache page lines** (carried from 113): under Fast Cache, one line per source with its saved list (games,
      date) and All Games' (games, where it is kept); each support module gets an accessor for its sb_snap_t.
- [x] The new words in all 33 languages (94 strings and 6 labels, 10/22).

### B. Hidden games
- [x] **Hide Game** in a game's Triangle options (and on All Games and Starred Games rows, proxied to the source).
      One confirm, since it can be undone. Stored **on the source**, as RIPPS2.HID beside RIPPS2.LST (the device
      root; on APA in +OPL; the SMB share root; the MMCE card), so a hidden game stays hidden when the drive goes
      to another console. Records: kind and name (the file name: two dumps of one game share a startup).
- [x] **Hidden everywhere** but one place: skipped when updateMenuFromGameList builds a source page (rows keep their
      ids into the source's own array, so launch, config and art are untouched), in mixCollect and allgames.bin,
      in Starred Games and Recents (the star is kept, so Show Again brings the game back starred), in RIPFLOW and
      RIPGRID (they draw the same submenu), in Random Game (L2 + R2) and in the game count.
- [x] **Settings > Game Sources > Hidden Games**: every started source's hidden games under their source's name,
      with size. Cross on one: Show Again, Delete (part C). Asks the Parental Lock password when one is set.
- [x] Rename and delete keep RIPPS2.HID in step (sbRename, part C).

### C. Delete a game completely and cleanly
What is there now: OPL's delete (Triangle > Delete) unlinks only the image's files (sbDelete, ul.cfg rebuilt for
UL); its CFG, art, cheats and VMC stay behind. APA games have no delete at all (hddsupport's itemDelete is NULL),
All Games' and Starred Games' are NULL too, and a starred game refuses ("Delete is not allowed while the game is starred.").
RIPPS2's APA driver already takes a user partition's delete for the HDD MANAGER (build 73, hddRemove: never a __
name, -EBUSY when open, every header write through the table fence).
- [x] **A removal plan first**, from one pure function (host-tested): the game and its source in, the list of
      what goes and what stays out, with sizes. On BDM, MMCE, SMB and UDPFS: every part of the image (sbDelete's
      paths, the browse subfolder included), ul.cfg rebuilt for a UL game; CFG/<startup>.cfg; ART/<startup>_*
      (COV, COV2, ICO, LAB, LGO, BG, SCR, SCR2 to SCR9); CHT/<startup>.cht. On APA: the game's partition (PP.*)
      through hddRemove, then its CFG, art and cheats inside +OPL (files in the PFS; the +OPL partition itself is
      never touched). PS1: the VCD (POPS) or the game's EMBER/games/<Title> folder.
- [x] **Kept unless ticked**: the game's VMC (it holds saves; named in its CFG), POPSTARTER's saves folder
      (POPS/<name>/), Ember's saves (where Ember keeps them: to check), RIPSHOT's MEDIA/<title> shots (built as one
      question, "Delete its saves and RIPSHOT pictures too? No keeps them."). A CFG or art
      another copy of the same startup on that source still uses is kept, and the screen says why.
- [x] **Two screens, as the HDD MANAGER**: what goes, what stays, and the space freed; then a last screen only START
      gets past (REMOVE FOR GOOD). Never with Write Operations off; Parental Lock asked first; refused for the
      partition RIPPS2 runs from or keeps its settings on (hmKept's rules) and for any __ partition.
- [x] **Order**: the image first (a cut-off delete leaves stray CFG or art, never a half game listed), then the rest;
      APA under ioBlockOps, then hddPartitionsChanged so games.bin is rebuilt. The star and the Recents entry go,
      RIPPS2.HID drops it, the source rescans (RIPPS2.LST follows), All Games and allgames.bin follow.
- [x] **The APA table checked before any partition goes** (Berion's warning; the HDD MANAGER's remove too): a
      read-only walk of the whole chain from __mbr: every header's magic and checksum, each start equal to the
      last one's next and each prev pointing back, every partition inside the disk (start + length within
      HDIOC_TOTALSECTOR), no length above what this disk allows (apaGetPartitionMax of its own size) or off its
      power-of-two alignment, and the chain closing at 0. Anything off: no delete, and the screen says the table
      does not fit this disk (written from an image of another size?) and to repair it on a PC first. The walk
      runs again after the delete, and the result goes into REMOVED.TXT. (The HDD MANAGER's remove runs the same
      walk first since 10/22 evening.)
- [x] **Delete on All Games and Starred Games** proxies to the source row found by name at that moment
      (mixOwnerId), never the stored id; refused on a waiting row.
- [x] **A receipt**: mc0:/RIPPS2/REMOVED.TXT gets what was removed, from where, and the bytes freed (as LAUNCH.TXT
      reports a launch), and the list shows "REMOVED <title>: 3.1 GB FREED".

### E. The launchers RIPPS2 does not carry, found and remembered (the user 10/22; plain words on screen since
10/23: the user found the code name SEANCE off-putting for a small feature, so the screen says RIPPS2)
- [x] **ripps2seance.c**: POPSTARTER, the POPS files, Ember, Ember's BIOS and Neutrino searched on the drives RIPPS2
      has started (never loading a driver to look), skipping the game and art folders; kept by drive kind (usb,
      ata, mx4sio, ilink, mmce, hdd, smb) in `launchers.txt` beside the settings, so a stick in another slot still
      matches. Every launch that finds one notes it.
- [x] **Used at launch**: POPSTARTER after Settings' path and the game's drive, before the cards; RIPPOPS copies the
      POPS files from the folder found; Neutrino after the cards, then a search, and RIPPS2's own copy offered once,
      only when none is found anywhere; Ember and its BIOS copied beside the games by a pre-flight before the
      launch (START), so RiptOPL's launch legs and guiMsgBoxMissing stay as upstream has them (their host
      harnesses copy them word for word: a weak seanceHook is NULL there).
- [x] **Settings > Game Sources > Cache**: five Found / Not found lines and **Look now** (no on/off: it only helps).
- [x] Lab 10/22: "knows 5 of the 5" on the 114 disk, each at its odd path; Cache rows and Look now.

### F. STATUS: the drives before the homebrew (the user 10/22)
- [x] **DRIVES** first: every started drive by kind, the internal HDD (APA)'s free space, each memory card's free
      KB (asked twice after START DRIVES: a changed card answers short once), the MMCE card, what is off; **START
      EVERY DRIVE**. Then **LAUNCHERS** (one line each, LOOK FOR THEM starting every drive first on Cross), then the
      homebrew and BIBLE. The subtitle reads Drives, launchers and homebrew (10/22 evening).

### G. The font trim, and no lite ELF (FifthFox's 2 MB; the user 10/23: "ideally there is no lite elf we just ship
the one that makes the most sense": the lite variant was built, then removed before release)
- [x] ~~RIPPS2-lite.elf~~ removed 10/23 (RIPPS2_LITE=1, its own CI artifact): no BIBLE KELFs, no Neutrino tar, no OPL background;
      under 2 MB. It says where Neutrino goes and that BIBLE installs once from the full ELF. Lab 10/22: boots,
      START menu, STATUS with DRIVES and LAUNCHERS.
- [x] **FreeType** started with RIPPS2's own module list (TrueType, sfnt, autofit, smooth; CFF and its helpers in
      the full ELF) and freed without ftinit.c, so Type 1, CID, Type 42, PFR, BDF, PCF, WinFNT, SDF, SVG and the mono
      rasteriser leave the link. **strip_fonts.py** strips the compiled-in fonts (render-checked identical).
- Where the rest of the size is: the fonts are about 75 KB packed, and the packer is near LZMA's best on what is
  left; the big wins were the carried blobs (lite) and FreeType. Next candidate: libjpeg-turbo's 12 and 16-bit
  decoders.

### D. Compress on hide (ISO to ZSO): the user's call before any code
The user's idea (10/22): hiding can compress the game into the hidden list; Show Again un-compresses when the
drive has room. What stands in the way:
- RiptOPL carries only LZ4's decoder (modules/isofs/lz4.c). Compressing needs LZ4's encoder (BSD-2-Clause, fine
  beside AFL with its licence).
- **Neutrino cannot run a ZSO** (RiptOPL docs/NEUTRINO.md: a .zso falls back to the OPL core), so a game set to
  Neutrino changes core once compressed. APA games are raw HDL partitions: no ZSO there at all.
- Speed: USB on the PS2 is USB 1.1 (about 1 MB/s): a 4 GB DVD is over an hour to compress and as long to restore.
  The internal HDD (exFAT) and MX4SIO are the only realistic targets.
- Safety: write NAME.zso.part, decode every block back and compare, only then rename it and remove the ISO; never
  start without room for the whole ZSO beside the ISO.
- The user skipped RIPCON (format conversion) on 10/18 for these same reasons.

Recommendation: ship A to C as 114. Put an LZ4 benchmark in a test build (`-f flags=RIPPS2_ZSO_BENCH=1`: MB/s in
the lab at EECycleRate -3, then on a console) and decide compression for 115, internal HDD and MX4SIO only, with
the time it will take shown before it starts and the game's core checked first.

### Tests and lab
- [x] Host (test_ripps2_build114.py, the module compiled with -DRIPPS2_MIX_HOST_TEST as earlier builds do):
      allgames.bin round trip; a short, corrupt or oversized file is ignored, never half read; the merge of
      waiting and live rows (live replaces, absent drops, Manual stays, cursor key kept); RIPPS2.HID filtering;
      the removal planner for every format and source (nothing outside the source's prefix, shared CFG kept,
      __ and kept partitions refused, APA = partition + PFS files).
- [x] Lab (ps2bg, hidden, 10/22): boot 1 writes allgames.bin on the card; boot 2 on a fresh card with only that
      file and BDM on Manual lists the game before its drive answers; Hide, Hidden Games and Show Again; delete
      on exFAT (ISO, CFG, art, cheats gone, VMC kept, read back with exfat_ls) and on a scratch APA disk (PP.TEST.HDL
      gone, the chain in order: apa_ls and REMOVED.TXT agree); the lite ELF's smoke run (since removed). Not in the lab: Cross on a
      waiting row (the lab's games are dummies, so nothing is launched there). The plan was: reel HDD with allgames.bin, grabs at 3 s (every game listed before the drive answers)
      and after the handover (same cursor); BDM on Manual: rows listed, Cross starts the drive and launches;
      hide and Show Again on exFAT (RIPPS2.HID read back with the exFAT tools); delete on a scratch copy of
      ripps2-apa.raw, then pfsshell: the PP partition gone, +OPL whole, the CFG and art gone from it.
- [ ] Consoles (the Discord test list): MMCE with a big library (lukeatmynose's 180 games), SMB, a real APA
      delete (after a backup), boot to a whole All Games with every source on Manual.

### Decisions (taken 10/22 as recommended, the user to review in the recap)
1. Compression (part D): measure first and decide for 115 (recommended), or build it into 114.
2. The hidden list on each drive (travels with it; recommended) or one list in the settings.
3. Delete keeps saves (VMC, POPS saves) and RIPSHOT shots unless ticked (recommended), or removes everything.
4. RiptOPL upstream: 192 commits since 3cd7f89 (i.LINK fixes #1018, IGR #984, Ember's starting disc from
   discs.txt, a ZSO probe fix, VMC fixes, USB / MX4SIO / iLink settles skipped, the newest menu sound cutting the
   last #504, the language registry locked). The language and sound changes touch what builds 104 and 111
   rewrote, so it is its own merge patch (as 72, 84 and 103 were). FifthFox's iLink report changes the
   recommendation: merge first, so testers get the iLink fixes a build sooner, and the games work follows; or
   keep 114 for the games and merge as 115.
5. Size: RIPPS2-lite.elf beside the full ELF (recommended: keeps Neutrino and BIBLE in the full one, as decided),
   or Neutrino and BIBLE found rather than carried in the one ELF.

Taken: 1. measure first, ZSO decided for 115 (no code in 114); 2. the hidden list on each drive (RIPPS2.HID);
3. saves and RIPSHOT pictures kept unless the one question gets Yes; 4. merged first, in 114 (57c45b4, so the
iLink fixes reach testers now); 5. RIPPS2-lite.elf beside the full ELF, built and then removed on 10/23 (the user:
one ELF; POPSTARTER and Ember found by association, as since 113).

### Console checks the lab cannot make
- IGR on the merged VBLANK path (#984) on a real game; the ee_core stack (0xC80, as v1.1.3).
- FifthFox's iLink: Neutrino and POPSTARTER from the HD-338 (the #1018 fixes).
- A real APA delete after a backup, and the HDD MANAGER refusing a cloned table of another size.
- Boot with every source on Manual to a whole All Games, then Cross on a waiting row: the drive starts, the game launches.
- MMCE with a big library (lukeatmynose's 180 games) for the master list's size and speed.

## Build 115 (the user 10/23: fonts, settings without scrolling, FifthFox's reports): planned

### Storage safety first (FifthFox, 10/22: "I crashed two .MCDs and my USB ... Maybe it was writing something in the
background while I was trying to launch a game and had to restart?")
His setup: SCPH-39001; slot 1 MMCE (its card images, .MCD, on its own SD card), slot 2 MX4SIO, USB, iLink (FAT32,
slow to list), APA through a GameStar adapter; RIPPS2 started from USB, Neutrino and POPSTARTER on the memory card.
Earlier: 10/12 (v1.0.0) POPSTARTER from MMCE crashed to wLE and the MMCE's boot card had to be restored; 10/14 the
POPSTARTER BDMA equip put usbd.irx and usbhdfsd.irx on the card with the exFAT variant for a FAT32 iLink drive.

What the code does (read 10/23, nothing run yet):
- A launch's teardown (deinitEx) waits for the IO worker at most LAUNCH_IO_DRAIN_TICKS, about 10 s, then goes on;
  ioEnd() only raises a flag. The worker keeps running the request in hand, and the queue behind it, while the
  launch unmounts and resets the IOP.
- A scan of a slow drive (MMCE libraries take minutes; FifthFox's USB, MX4SIO and iLink are slow) easily outlasts
  10 s, and RIPPS2's scans END IN A WRITE when the list changed: RIPPS2.LST on the drive itself (on an MMCE that is
  mmce0:/, the SD card holding the .MCD files) since builds 109 and 110, and in 114 allgames.bin beside the settings
  (mc0: on his console, which is the MMCE). Upstream's worker mostly reads, and a cut read is harmless; a cut write
  leaves FAT or exFAT half updated. A launch that then stalls and is power-cycled does the same.
- recents.bin and conf_last.cfg are written at launch on the GUI thread and closed before the teardown: finished.
- The PS1 launch copies POPSTARTER's files and the BDMA driver pair onto mc?:/POPSTARTER before POPSTARTER's own
  IOP reset (upstream RiptOPL). The iLink variant is RiptOPL's #1018 (merged in 114).

Plan:
- [ ] A launch stops RIPPS2's background writes before anything else: a flag raised at the top of deinit and
      deinitEx; RIPPS2.LST, allgames.bin, the hidden list, art and RIPSHOT writes check it and skip (each is a cache
      or can wait for the next boot).
- [ ] A write already started is waited for, whatever the 10 s drain does: a count of writes in flight, which the
      teardown waits on (writes are short; bounded at 20 s with a log line if one never ends).
- [ ] Scans give up when a launch begins, so the drain finishes and no worker is reading a drive into an IOP reset.
- [ ] RIPPS2.LST written so that a cut write cannot hurt the drive's file table: a new file beside it, renamed over
      it where the driver renames (USB, exFAT HDD, MX4SIO, iLink), and on the MMCE kept beside the settings rather
      than on the MMCE's SD card next to its .MCD files.
- [ ] Ask FifthFox: which build; what was launched, from which drive, by which core; did the launch stall; what
      exactly was lost on the cards and the stick; MMCE firmware and per-game cards (GameID) on or off.
- Until then he can turn Settings > Game Sources > Cache > Fast Cache off (no RIPPS2.LST writes) and let the lists
  finish before launching.

### Fonts (the user's answers to the font audit, 10/23)
- [ ] A: one variable Roboto Condensed 3.015 (the newest) in the ELF for Settings and RIPFLOW, weights 400 to 700,
      cut to Latin-1; Settings rows at 700 and 18 px.
- [ ] B: default_font_weight and font1_weight ... font15_weight (100 to 900): a variable face at that weight, a
      static face grown in code up to about 1 px.
- [ ] C: Text Weight (Regular, Medium, Bold) in Colors and More. And no settings page should need scrolling:
      rearrange the pages that do.
- [ ] D: Adapt and Adapt Rx: b.ttf and c.ttf become the built-in variable Roboto by weight keys, d.ttf becomes
      builtin:ripps2, and their conf_theme.cfg lists every built-in font in its comments so theme makers find them.
- [ ] E: the language pack on Roboto Condensed 3.015 cut per language, in step with the ELF's.
- F: all of it in 115; 114 ships with its reel, the forum post and the Discord post first.

## Skipped
- **RIPCON** (format conversion, as OrbitOPL Toolbox does on a PC): not done on PS2 hardware yet, likely failure
  prone, and a smaller format can be less supported by the loaders. Skipped by the user (2026-10-18).
