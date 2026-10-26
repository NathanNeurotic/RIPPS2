# Build 115 is RIPPS2 v1.1.5 beta: shaped on a real SD2PSX. Fast Boot, MMCE and the controller sharing the bus, a CD player for your own tracks, MP3, BIBLE that never copies RIPPS2 and brings your drives back, and themes of two files.

## Get it
- [Download the latest RIPPS2.elf](https://github.com/akilluminati47/RIPPS2/releases/latest/download/RIPPS2.elf) (always the newest build), [RIPPS2-languages.zip](https://github.com/akilluminati47/RIPPS2/releases/latest/download/RIPPS2-languages.zip) (every release carries it, all 33 languages), [the theme pack](https://github.com/akilluminati47/RIPPS2-themes/releases/latest/download/RIPPS2-themes.zip) (edition 115: update it with this build) and [the v1.1.5 Short](https://akilluminati47.github.io/RIPPS2/media/b115/ripps2-v115-short.mp4)

## Fast Boot
- **Game Sources > Cache > Fast Boot**: the boot reads RIPPS2's own drive only (RIPPS2.FB beside the ELF says where your settings and sounds are), every list from its cache. Other drives wait until SELECT on their page or one of their games starts them. Your sounds are copied beside RIPPS2.

## MMCE and the controller
- **Game ID on by default**: RIPPS2 waits while your SD2PSX makes the game's card. **No jumping cursor** while MMCE reads, **Pad First** on, **always analog** (8BitDo too), and DIAG.TXT now logs the boot.

## Music
- **MP3**, a **CD player for marked tracks** in Memory Files (one disc, track after track, towers lit), BIOS Music clean all the way and set as your music at once, rips go where you choose (RIPPS2's own drive first).

## BIBLE and the rest
- **BIBLE never copies RIPPS2**: BBL 1.20 starts it where it is, or BOOT LOCK on an SD2PSX's PS2BBL Extended for MMCE. Drives come back after its IOP restart. **RESTORE** puts back what it replaced.
- **Set Metadata (Rename)** above Delete on every game, RIPGRID stops at the list's ends, Classic and XL sidebars, themes of two files, All Games with PS1 and PS2 together.

## Test list
- **Power on from your SD2PSX**: how long until the menu? Then turn **Fast Boot** on, power off and on: how long now?
- **With Fast Boot on**: All Games at once? SELECT on a drive's page starts it and brings the covers?
- **Scroll fast while MMCE loads covers**: does the cursor jump or stick?
- **Your right stick** (DualShock, DS4, 8BitDo receiver): does the cover tilt? If not, STATUS > SAVE DIAGNOSTICS and send DIAG.TXT.
- **A game from MMCE** (OPL core and Neutrino): does it wait for its card, then start?
- **BIOS Music > Rip** to RIPPS2's own drive: does it play right after the rip, and after a reboot?
- **Mark two or three tracks** (.wav, .ogg, .mp3) in Memory Files and open them: one disc, next track by itself?
- **A CD track (.wav) as menu music from MMCE**: smooth now while covers load?
- **BIBLE** on a card with PS2BBL Extended while RIPPS2 runs from MMCE: does it offer BOOT LOCK? Your drives all still there after?
- **BIBLE > RESTORE** on a card BIBLE set up: the old loader back?
- **A PS1 game and an app**: Triangle, Set Metadata (Rename): the editor, then Rename from its ACTIONS?
- **RIPGRID**: Up on the first row and Down on the last stay put; Circle changes the source?
- **POPSTARTER from MMCE** with POPS.PAK or POPS.ELF + IOPRP252.IMG: no false "missing files" ask?
- **Theme pack edition 115**: Adapt and Adapt Rx look right with this build?

## Report
Post in the [psx-place thread](https://www.psx-place.com/threads/ripps2-a-ps2-front-end-in-one-elf-launch-disc-storage-memory-files.51316/) or here with your **console model**, your drives, where RIPPS2 starts from, your **DIAG.TXT** and a **photo** of anything odd. Thanks to ripto, nuno6573, zackcage6, eliminator1403, FifthFox, Mr.sus.60 and lukeatmynose for the reports that got us here. Special thanks to all the YouTube love as well: glad to help however you reach me.
