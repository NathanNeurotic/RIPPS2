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

## E. Settings tooltips
- When the selected row is low on the page, the tooltip slides up so the rows above and below stay visible.

## F. Lab
- 10/25 night: the background driver's key presses stopped reaching PCSX2 for every ELF and drive (the same RIPGRID
  walk that worked at 01:28 failed at 03:14). Shift/Ctrl/Alt not stuck. Find out before the next lab run (does the
  foreground driver work, did the hidden desktop change, NVIDIA overlay or Xbox app focus).
- The 1080i info-page captures for the thumbnail (all 9 games, RIPPS2 theme) are still to do; t114-sdmirror.raw is a
  lab drive with the card's games, art and CFGs.
