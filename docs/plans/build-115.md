# Build 115: the first real-hardware run on the SD2PSXTD (the user's report, 10/25/2026)

Hardware: the user's PS2 with LinkRetro's SD2PSXTD v1.2 (sd2psx board) on sd2psXtd firmware 1.4.0, a 32 GB microSD
formatted MBR + exFAT (32 KB clusters) with the lean BOOT card (channel 1: sd2psXtd's PS2BBL Extended card, OPL and
uLaunchELF removed, RIPPS2/RIPPS2.ELF = the v1.1.4 hotfix ELF, PS2BBL AUTO -> RIPPS2), 9 PS2 games in DVD/, their art
and CFGs, EMBER (Digimon World) and POPS/POPSTARTER.ELF. RIPPS2 boots from the card; Burnout 3 from the internal HDD
launches fine.

Status: in progress (patch 0115 on main). The first sections below are the plan from 10/25 evening; the
lettered sections after them are the first run's notes, kept for their findings.

## The plan from here (10/25 evening, after the second hardware run)

The user tested the CI build of d4e9631 (run 40222153158) on the SD2PSXTD: the pad still lagged and jumped while MMCE
loaded, the right stick stopped tilting after the load, Burnout 3 from MMCE still hung (black screen a long time, the
logo's sound, nothing, a white screen 5 minutes later; from Memory Files the logo came sooner, then the same hang),
Digimon World (Ember) did not start, and copying a new RIPPS2.ELF onto the boot card failed with no message (the file
kept its old size; after erasing it, the new copy never arrived). Then a batch of navigation, sidebar and text requests.
Everything below is grouped into rounds so each build is tested as a group. Rounds 1 to 3 go into 115; round 4 releases.

### What the firmware source says (sd2psXtd main, read 10/25)
- **The device's own game switch is late.** With GameID on in the device, it watches the play history file: it sees the
  history write only when that sector is flushed to the SD (after 100 ms without card traffic) and acts only after 2 s
  more of quiet (`HISTORY_WRITE_HYST_US`). Build 115's wait (1.5 s for the busy bit) gave up before that, so the switch
  could start after RIPPS2 had handed off and the game was streaming. Creating or loading the game's card runs only
  while MMCE is idle (30 ms slices), and a streaming game never lets it. That fits the late logo and the hang.
- **The busy bit** (MMCE GET_STATUS) is set only while the device creates or loads a card. Card writes waiting to be
  flushed are not shown, and RIPPS2's own MMCE reads during a wait stop the device's progress.
- **The device's main loop** draws its OLED screen between MMCE requests; its README warns that long names that scroll
  make MMCE games stutter. The boot channel was named "PS2BBL + RIPPS2" (now "RIPPS2").
- **mmceman holds the SIO2 lock for a whole read** (all of a 16 KB fileXio piece, the device's SD time included); the
  pads share that lock. The menu's mmceman runs with no pacing; only the in-game mmcedrv gets RiptOPL's 5 wait cycles.
- **Card writes** go to the device's RAM at once and reach the SD later, in 100 ms slices that stall MMCE meanwhile.

### Round 1: MMCE, the pad, and launching (hardware first)
1. **GameID on by default** (`mmce_gameid` = 1, set once by a 115 migration, the user's choice kept after). Every MMCE
   launch (OPL core, Neutrino, Memory Files) stops RIPPS2's own MMCE reads (art, lists, caches), sends the game's ID,
   and waits on screen until the card is ready (the busy bit clear and the file system answering), with the seconds
   counting and no 3 s cap; START skips. With RIPPS2's GameID off, the wait covers the device's own switch (at least 4 s
   after the history write). This is "make the card before the game reads".
2. **Pad reads that miss keep the last buttons.** A frame whose pad read failed (the bus busy) counts today as nothing
   pressed, so one press becomes several: the cursor jumping. The last buttons are kept for up to 250 ms; past that,
   held buttons are let go and nothing repeats until a fresh read. The right stick also reads in padman's FINDCTP1 state,
   and DualShock is asked for again whenever the pad reports digital after a stall.
3. **MMCE reads paced in the menu.** Art and list files are read in pieces of at most 8 KB with a yield between them,
   none while a button is held or for 150 ms after a press (the pad breath MX4SIO has), and never two MMCE readers at
   once.
4. **No card writes during MMCE work.** Settings, recents, the master list and the play history wait until MMCE has
   been quiet a moment before they are written to the boot card.
5. **Lists load once.** Each list shows from its cache at once. A paced background check reads the drive. When the
   drive's list differs, the refresh glyph pulses and SELECT takes the new list. When it matches, nothing on screen
   moves.
6. **A hardware log.** A RAM log records pad misses, the longest pad gap, MMCE request times, the busy bit and each
   launch step. STATUS > SAVE DIAGNOSTICS writes it to the SD or a USB stick, so a hardware run can be read here.
7. **Memory Files copies are checked.** Each copy reads back its size and CRC and says when it fails. A copy to a card
   in an SD2PSX warns to wait a few seconds before power off, because the device writes the card to its SD later.
8. **Ember from MMCE.** Digimon World did not start: check which devices Ember reads (mmce paths, its BIOS, the games
   folder) and either make the launch work or say plainly what Ember needs.
9. **Control test (the user).** To tell a RIPPS2 problem from a device or SD one: the same Burnout 3 from the same SD
   with the ps2-mmce OPL and with NHDDL + Neutrino, and in RIPPS2 with the In-Game Menu off and with the Neutrino core.

### Round 1b: the SD2PSX as a home for RIPPS2 (the user, 10/25 evening)
1. **AUDIO beside RIPPS2 on the SD** (`mmce?:/RIPPS2/AUDIO`). It is RIPPS2's own folder now, so it is searched first;
   it is quicker to read than the card and has room for music. BIOS Sounds, BIOS Music and the CD player write there.
   The boot card keeps only PS2BBL and the settings save. Check that mmceman is up before the boot's sound load when
   RIPPS2 starts from MMCE.
2. **The device's cards in Memory Files.** `MemoryCards/PS2/<folder>/<name>-<channel>.mcd` are raw 8 MB cards, the same
   format as an OPL VMC, so they open like folders (copy saves in and out, export and import PSU). A CARD BANKS view
   lists the BOOT channels, the per-game cards and the named cards. From it: make a new card, copy a card, and move a
   card to the holding folder (never a hard delete).
3. **Card to card in MCKILLA.** A VMC or an SD2PSX card is written whole onto a physical card in slot 2 (and a physical
   card is backed up as a `.mcd` bank on the SD). Today MCKILLA writes a VMC's saves back one by one.
4. **Folder and file tooltips in Memory Files.** Say what each known folder and loose file is for: ART, CFG, CHT, CD,
   DVD, VMC, THM, LNG, APPS, POPS, EMBER, RA, RIPPS2, AUDIO, MEDIA, MemoryCards, BOOT, .sd2psx, RIPPS2.LST, games.bin,
   settings.ini, BootCard.ini, `*.mcd`, `*.crp`.
5. **MEDIA from MMCE.** A PNG opens and tilts with no pad lag, and AVI video plays without stutter. Reads ahead in paced
   pieces, with the pad reads kept clear (round 1).

### Round 2: navigation and the sidebar
1. **Layout > Sidebar Style**: Split (today's dark strip and the accent beside it) or One Piece (one bar, the same overall
   width, the glyphs centred in it). The lit tile slides to the new category and the glyphs crossfade when it changes.
2. **The bar and the drawer slide open** with RIPFLOW's cover easing (both the narrow bar and the opened drawer).
3. **Category Bar becomes "Category/Sidebar".** On the sidebar, Fade When Idle slides the bar away; any press brings it
   back, a little quicker than it left.
4. **Category Layout gets "Menu"** as its last choice: no bar and no sidebar; the categories are in the START menu, as
   on a legacy theme.
5. **Sidebar mode owns Left.** Left always goes to the sidebar. Right never cycles the sources, and Up/Down never
   changes the source on RIPFLOW. The cancel button (O) opens the Storage drawer on every page and view. With the
   sidebar off, Left/Right work as the theme sets them, with L1/R1 on the categories.
6. **Memory Files ORBITS in sidebar mode**: L1/R1 change the formation and Left opens the sidebar, as on Launch Disc.
7. **RIPFLOW: L1/R1 step one cover**, and repeat while held, like the D-pad.
8. **Hints and Glyphs fade.** A new option in Layout's top set, on by default for every theme (key `hints_fade`, written
   into Adapt and Adapt Rx). When the hint line's glyphs change it fades in with the covers' own fade at 0 ms; the same
   glyphs stay put; modals included. A **Guidance** choice fades the glyphs in after 4.2 s idle, with RIPFLOW's L1/R1
   glyphs beside the centre covers.
9. **Starred Games.** R3 held 4.2 s turns the star display off: no stars, no indent, no R3 hint, names from the left
   edge at full width. Held again turns it back on (Manual, stars as last set) and stars the game under the cursor.
   Default: Manual with the stars hidden; R3 still stars a game. The tooltip says all of this.

### Round 3: text and page polish
1. ACHIEVEMENTS and STATUS: the row names in Roboto on every theme (a theme's font keys can still override).
2. Notifications: one Roboto, the built-in bold. Text Weight's global choice becomes Normal or Bold (it shows no change
   today); theme keys keep all three weights.
3. One title position on every page of the same kind. The PS1 game settings title sat too close to the bar, and its
   sentence ran off.
4. Network: the title and its line spaced like the other pages. Audio: the divider lines moved to fit the text, which
   stays where it is.

### Round 4: release
- Translations: build 115's 58 strings and its new labels in the 32 languages.
- Lab rounds in PCSX2: navigation and sidebar, Recent Games, the list pulse, STATUS LOADING, the BIOS Sounds room check,
  art names, Neutrino on the exFAT HDD.
- A hardware round on the SD2PSX with the user: MMCE input, Burnout 3, Digimon World, the sounds rip, EXIT back to
  RIPPS2.
- Themes edition 115 (`hints_fade`, the sidebar style keys) and the glossary; CHANGELOG; README (the ELF is 2,641 KB,
  about 2.6 MB); the psx-place post built from the user's template (tools/discord/psxplace-post.bbcode); the Short
  (repo and release only); release v1.1.5-beta; the Discord "Test me | Build 115" post.

### The SD2PSX card as set up on 10/25 evening (D:)
- `RIPPS2/RIPPS2.ELF` on the SD: build 115 (e6f0a21). PS2BBL's AUTO starts `mmce?:/RIPPS2/RIPPS2.ELF` first, then
  `mc?:/RIPPS2/RIPPS2.ELF` (also on the boot card), then the browser. An update is one file copied on a PC.
- BOOT: BootCard-1/2/4/6/8.mcd all the same card (PS2BBL, RIPPS2's settings save, RIPPS2.ELF); BootCard.ini channel 1
  "RIPPS2", MaxChannels=1.
- THM: Adapt and Adapt Rx (edition 114). The holding folder keeps the old cards, the Burnout 3 card the device made and
  the APPS test build.

### Answers given to the user
- GameID on by default: yes. RIPPS2 sends it and waits until the card is ready before the game starts ("create
  before reading"). The device's own switch is too late for a streaming game.
- Where RIPPS2 lives on an SD2PSX: on the SD (`mmce?:/RIPPS2/RIPPS2.ELF`), started by PS2BBL from the boot card, which
  keeps PS2BBL and RIPPS2's settings save. Loading is quicker, an update is one copied file, and nothing has to be
  written into a card image. The boot card's own copy stays as the fallback.

## A. MMCE (first)

### A1. Input blocked and erratic while MMCE works
- Booting with the last used device = MMCE, the pad is dead or erratic until the card's list is in, even before the
  cache shows; the right stick tilt misbehaves too (the user: "it even blocks the right stick", "the controller is
  bugging terribly when mmce is loading stuff"). Browsing and menus should work while it loads, as on the HDD.
- Likely cause: MMCE and the pads share SIO2. Long MMCE transfers (mmceman) starve padman's reads, so presses are
  dropped and the stick reads stale or zero. To check: where the MMCE list read runs (mmcesupport.c on the IO thread?),
  how big each request is, and whether anything yields between them. Fix direction: show the cached list at once, read
  the card in small pieces with a DelayThread between them, never during a pad read window, and pause MMCE work while
  the user is pressing buttons (as MX4SIO got in build 110).
- The "right stick tilt bug on everything from covers to the PNG viewer" is probably this; confirm with the user what
  the tilt does (stuck, drifting, jumping) and whether it also happens with no MMCE inserted.

### A2. Games from MMCE: very slow, then a hang
- Burnout 3 from MMCE: the PS2 logo's sound came over 5 minutes late, then it hung, then a white screen.
- The game files are good: all 8 retail ISOs on the card match Redump byte for byte (size, CRC32, SHA-1, checked
  10/25 against libretro's Redump PS2 DAT: Auto Modellista, Aqua Teen, Burnout 3 (USA, Canada), Katamari Damacy,
  We Love Katamari, Ratchet & Clank, Going Commando v2.00, Up Your Arsenal; GTA VC Debug is a prototype, not in Redump).
  Card copies were checked by size after robocopy; hash them on the card next time it is in the PC.
- "The sizes are off from the ones on my HDD": the HDD copies came from another source; the card's are the Redump ones.
- To find: which core launched it (OPL core with mmcedrv, or Neutrino), the game-ID card switch at launch, and the
  read speed the console got. Next session: a debug ELF with EE SIO logging is not possible on hardware, so add a short
  on-screen or file log of the launch (core, mode, the MMCE slot, the switch result) and test the same game with each
  core. Also check sd2psXtd's own notes on MMCE game loading (settings for speed, known slow games).

### A2b. What the SD showed (10/25, card back in the PC)
- The microSD is not slow: through the PC's USB reader, random 2 KB reads 0.59 ms median (0.9 ms worst), sequential
  31 MB/s, an 8 MB card written in 512-byte write-through pieces in 16.7 s (490 KB/s, worst write 24 ms). All 9
  ISOs and the boot card are one extent each (no fragmentation).
- GameID cards: MemoryCards/PS2/SLUS-21050 (Burnout 3) and SLUS-20642 (Auto Modellista) are 4.2 and 4.6 MB, not 8, and
  Burnout 3 has two .crp files of ~88 KB (sd2psXtd renames a wrong-size card to .crp and makes it again). The
  firmware writes a new card only while ps2_mmceman_fs_idle(), 512 B at a time with a flush per slice; a game
  streaming over MMCE keeps it busy, so the card never finishes before power off. RIPPS2 has mmce_gameid=0, so these
  came from the device's own history-file tracking. Test MMCE launches with the device's GameID off, to take the
  switch and the card writes out of the picture.
- BOOT/BootCard-8.mcd exists (a blank formatted card): boot channel 8 was selected at some point (channel down from 1
  wraps to 8, and the device keeps the last boot channel). A power on on channel 8 has no PS2BBL: that is the likely
  "the exploit fails sometimes".
- The boot card (RIPPS2's settings live there): 3,811 KB free; RIPPS2/AUDIO was never made.
- The user's settings_riptopl.cfg: exit_path=mc1:/APPS/RIPPS2.elf (a stale value from the old setup: the "hardcoded
  mc1 path"), mmce_mode=0, mmce_slot=2, mmce_wait_cycles=5, mmce_use_alarms=1, default_core=0 (OPL core),
  popstarter_path=usb:/POPS/POPSTARTER.ELF, enable_pccf=0, ripps2_recents=0, last device 15.

### A3. Other card items
- BIOS Sounds rip: "The sounds could not be written to mc0:/RIPPS2/AUDIO/. Is the drive full or write protected?" on
  the BOOT card. sd2psXtd's card manager has no read-only BOOT card; the lean card had 3.98 MB free before RIPPS2's
  settings. Check the space left, how RIPPS2 makes the AUDIO folder on a card (mkdir of a nested path on mcman), and
  offer the MMCE's SD (mmce0:/AUDIO) when the card is short.

## B. The in-game menu's exit
- The user: the in-game menu should know the exit path to the RIPPS2.ELF that launched it, not a hardcoded mc1 path,
  and show it properly.
- Today: gExitPath empty means "Browser"; ee_core's exit loads only from mc and mass (USB) (padhook.c reloads
  SIO2MAN/MCMAN and, for mass, USBD from SYS-CONF); ripps2BootLockIgrPath fills it from the boot path only for mc/mass.
- Plan: fill the exit path from RIPPS2's own boot path at every launch unless the user set one, and show it in the
  menu. The catch on an SD2PSXTD: with GameID on, the device switches to the game's own card at launch, so
  mc0:/RIPPS2/RIPPS2.ELF is not on the card in the slot when the user exits. Options: switch the MMCE back to the BOOT
  card before loading the exit ELF (mmceman's switch is not in ee_core's exit path today), exit to the browser and let
  PS2BBL start RIPPS2 again, or keep a copy of RIPPS2 where the exit can reach it. Decide with the user.

## C. Cache: trust it, per device, and a light gate file
- The user: the cache lets the list show, but settings still take a while and the cached list then refreshes itself,
  a hitch. Show the cached list and trust it (launch from it, starting the game's drive on launch) until a refresh is
  asked for (SELECT) or a device's own refresh writes its cache.
- A Cache page per device that has one, in an order the user sets; boot stops at the first cache it finds.
- "Create master cache" in the Cache page: one very light file, suggested next to the ELF on the memory card, so boot
  reads it first. If it has to live elsewhere, a tiny gate file next to the ELF points to the settings and the caches.
- STATUS gets an optimisation part: where settings and caches are read from, which is fastest, and a button to put
  the master cache and settings next to the ELF. Tooltips that explain how to get the fastest boot.
- Drives on Manual (the default) start on launch while their list shows at once from the cache.
- STATUS and Cache link to each other; going back and forth does not stack (Back returns once, then to the parent).

## D. Storage sources
- PC Card CF: hide its page; it is the fat's HDD-bay CF adapter, so fold its detection into the HDD's.
- Recent Games: show it in the sidebar like the drives, with its own on/off; one row with a count 1 to 99
  (today ripps2_recents 0..9). Ask: "manual start for drives of whatever game chosen is in the list" means a recent
  game's drive starts when you launch it, as All Games does.

## D2. Art names from the OPL Manager database (issue akilluminati47/RIPPS2#2)
- The OPL Manager GameArt database (and tools built on it) names backgrounds `<ID>_BG_00.png` to `_BG_06.png` and
  screenshots `_SCR_00`, `_SCR_01`; RIPPS2 reads `<ID>_BG` and `_SCR`, `_SCR2`... only (png, then jpg). Fall back to
  `_BG_00` when `_BG` is missing, and `_SCR_00`, `_SCR_01` for `_SCR`, `_SCR2`, through the same artIndexMayExist
  check so a miss stays free.
- PS1 art keys: VCD file name without .VCD, Ember's EMBER/games/ folder name, apps' ELF name with .ELF (as mapped in
  Luden02/OrbitPS2-Manager#48, which OrbitPS2 Manager follows).

## E. Settings tooltips
- When the selected row is low on the page, the tooltip slides up so the rows above and below stay visible.

## F. Lab
- 10/25 night: the background driver's key presses stopped reaching PCSX2 for every ELF and drive (the same RIPGRID
  walk that worked at 01:28 failed at 03:14). Shift/Ctrl/Alt not stuck. Find out before the next lab run (does the
  foreground driver work, did the hidden desktop change, NVIDIA overlay or Xbox app focus).
- The 1080i info-page captures for the thumbnail (all 9 games, RIPPS2 theme) are still to do; t114-sdmirror.raw is a
  lab drive with the card's games, art and CFGs.

## Progress (10/25, end of session: usage limit reached)
Done in patch 0115 (pushed, CI building, NOT lab-tested yet as a whole):
- Art read under every name (index keeps real names: any case, .png/.jpg/.jpeg; decode by content, shrink big
  pictures; OPL Manager _BG_00/_SCR_00/_SCR_01 both ways; PS1 disc ID and XX.<name>.ELF keys). Host tests
  test_art_names.py + test_udpfs_art.py pass locally; issue #2 answered.
- Pad: DualShock mode asked for again in a quiet second when a pad is left digital (dead right stick).
- MMCE: nothing read while the card says busy (mmceCardBusy, devctl 0x2); OPL-core MMCE launch writes the play history
  first and waits (on screen) while the card makes the game's memory card (mmceReadyGameCard).
- SELECT refreshes coalesce (ioPutRequestUnlessWaiting); Trust Cache (gRipps2TrustCache=1, sbSnapTrusted) in MMCE,
  SMB, BDM: a cached list stands until a refresh.
- All Games starts at boot even when every source is Manual (lab repro on 1.1.4: empty "Start Device" for 45 s).
- Lab: ps2bg.ps1 closes PCSX2's hidden Error dialogs (the PC's audio device was gone).
Left: Trust Cache row + its strings on the Cache page (config key ripps2_trust_cache), exit path following the boot
path, PC Card CF fold, Recent Games source 1-99, tooltip slide, BIOS sounds space check, STATUS<->Cache link and the
STATUS loading section, translations for new _t strings, lab rounds, release v1.1.5-beta, the Short, Discord post,
the 1.1.5 ELF into the SD's boot cards (BootCard-1/2/4/6/8). SD card hash result: scratchpad isohash-card.tsv.
