# Build 115: the first real-hardware run on the SD2PSXTD (the user's report, 10/25/2026)

Hardware: the user's PS2 with LinkRetro's SD2PSXTD v1.2 (sd2psx board) on sd2psXtd firmware 1.4.0, a 32 GB microSD
formatted MBR + exFAT (32 KB clusters) with the lean BOOT card (channel 1: sd2psXtd's PS2BBL Extended card, OPL and
uLaunchELF removed, RIPPS2/RIPPS2.ELF = the v1.1.4 hotfix ELF, PS2BBL AUTO -> RIPPS2), 9 PS2 games in DVD/, their art
and CFGs, EMBER (Digimon World) and POPS/POPSTARTER.ELF. RIPPS2 boots from the card; Burnout 3 from the internal HDD
launches fine.

Status: plan, nothing built yet. Talk it over with the user first ("we can go over it tomorrow").

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
