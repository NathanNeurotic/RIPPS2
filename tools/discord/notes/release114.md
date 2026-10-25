<p align="center"><img src="https://raw.githubusercontent.com/akilluminati47/RIPPS2/v1.1.4-beta/media/ripps2-test-me.png" alt="RIPPS2: Rip it, build 114"></p>

## Rip it: RIPPS2 v1.1.4 beta (build 114)

**[Download RIPPS2.elf](https://github.com/akilluminati47/RIPPS2/releases/download/v1.1.4-beta/RIPPS2.elf)** (one file, 2.7 MB) and put it in place of your old one. Your settings stay where they were. **[RIPPS2-languages.zip](https://github.com/akilluminati47/RIPPS2/releases/download/v1.1.4-beta/RIPPS2-languages.zip)** puts RIPPS2 in your language (Latin, Greek, Cyrillic and Vietnamese now in one Roboto). The **[theme pack](https://github.com/akilluminati47/RIPPS2-themes/releases/latest)** is edition 114: Adapt and Adapt Rx on RIPPS2's own fonts, less than half the size.

### All Games, whole from the first frame
- **Every game at once at boot**, from a list kept beside your settings, before the drives answer: a game whose drive is still waking is listed and waits for it. A drive on Manual is listed too; Cross on one of its games starts the drive and then the game.
- **Your launchers, found once.** RIPPS2 looks for POPSTARTER, the POPS files, Ember, its BIOS and Neutrino on your drives and remembers where each one is: **Settings > Game Sources > Cache > Look now**. **STATUS** opens on your drives (kind, format, free space) and the launchers it found.

<p align="center">
<img src="https://raw.githubusercontent.com/akilluminati47/RIPPS2/v1.1.4-beta/media/b114/new-01-all-games-at-once.jpg" width="48%" alt="All Games at boot: every game listed before the drive has answered">
<img src="https://raw.githubusercontent.com/akilluminati47/RIPPS2/v1.1.4-beta/media/b114/new-03-cache-found.jpg" width="48%" alt="Game Sources > Cache: each launcher with where it was found, and Look now">
</p>

### Hide, delete, compress
- **Hide Game** (Triangle options): out of every list until **Game Sources > Hidden Games > Show It Again**. The hidden list travels with the drive.
- **Delete, completely**: the image, its settings, art and cheats; its saves and RIPSHOT pictures only if you say Yes, and a last screen only START gets past. On the internal HDD (APA) the whole partition table is checked first (Berion's check): a table made for another disk size is refused before anything changes.
- **Compress to ZSO** (experimental): hold SELECT on the panel, say yes again, and a progress bar runs the whole way. The ISO stays until every piece of the ZSO has been read back and checked; then you are asked before it goes, and **Back (keeps both)** keeps the ISO and the ZSO. The room is checked first. A ZSO starts with the OPL core (Neutrino does not read ZSO), saves and all, and **Uncompress to ISO** gives the ISO back. Hidden games can be compressed from Hidden Games. In the lab a 1.2 GB game on the internal exFAT HDD took about 10 minutes and came out 82% of its size.

<p align="center">
<img src="https://raw.githubusercontent.com/akilluminati47/RIPPS2/v1.1.4-beta/media/b114/new-04-delete-plan.jpg" width="48%" alt="Delete's plan: the game, its settings, 7 art images and its cheats go; its saves are kept">
<img src="https://raw.githubusercontent.com/akilluminati47/RIPPS2/v1.1.4-beta/media/b114/new-06-compress-hold.jpg" width="48%" alt="Compress to ZSO: the game, its size and drive, about how long, hold SELECT">
</p>

### Safe launches and the launch guard
- **No write runs into a launch.** Picking a game stops RIPPS2's own background saving first and waits for one already started, so a card image or a stick is never cut mid write by the reset.
- **Writes in step with the drive.** Big writes now go in whole aligned pieces (the lab caught exFAT putting a cluster in the wrong place otherwise), RIPPS2 knows each drive's format, cluster size and free space, and it ships **RiptOPL's guarded exFAT driver** (a game on a damaged FAT chain is refused instead of writing its VMC to the wrong place). A game over 4 GB is split only on a drive that really is FAT32.
- **The launch guard.** Pick a game while a drive is still being read and a glass panel says what RIPPS2 is finishing; its notches fill toward when it will be done and the game starts by itself. **Start now** stops the work safely and goes; **Back** returns you, unchanged. A short wait shows only the loading icon.

<p align="center">
<img src="https://raw.githubusercontent.com/akilluminati47/RIPPS2/v1.1.4-beta/media/b114/new-05-launch-guard.jpg" width="48%" alt="The launch guard: Starts next, reading the game list of the internal HDD, about 7 s">
<img src="https://raw.githubusercontent.com/akilluminati47/RIPPS2/v1.1.4-beta/media/b114/new-08-theme-list.jpg" width="48%" alt="The theme list on a held SELECT, over Adapt">
</p>

### Colors, fonts and Settings
- **Color Themes**: **Tangerine**, **Flamingo**, **Turquoise**, **Moonlight** and **Custom** (your own Theme Color).
- **Color Sweep**: five colors the theme fades through, never fast enough to flash: Rainbow, one made from each Color Theme, or your own (Sweep Colors, kept under your name).
- **The theme list**: hold SELECT on a game list and pick a theme from a panel (Settings > Interface > Hold SELECT: List, Cycle or Off).
- **Every Settings page on one screen** but Network: **BDM Devices** and **Screen** have pages of their own, **Layout** and **Colors and Text** are named for what they hold, and a game's options end with one **Achievements** row.
- **One HDD**: HDD Start Mode covers the internal drive, APA or exFAT, and Storage shows it once.
- **One newer Roboto Condensed**, variable, with **Text Weight** (Regular, Medium, Bold) for the tooltips, STATUS and About; themes can set a weight for any font slot.
- **RiptOPL brought up to date** (192 commits): i.LINK after an IOP reset, **Mode 8 (Slow Reads)** for DVD games that fail on fast reads, VMC and ZSO fixes.

<p align="center">
<img src="https://raw.githubusercontent.com/akilluminati47/RIPPS2/v1.1.4-beta/media/b114/new-09-tangerine.jpg" width="32%" alt="The Tangerine Color Theme on Memory Files">
<img src="https://raw.githubusercontent.com/akilluminati47/RIPPS2/v1.1.4-beta/media/b114/new-10-custom.jpg" width="32%" alt="Interface in a Custom green">
<img src="https://raw.githubusercontent.com/akilluminati47/RIPPS2/v1.1.4-beta/media/b114/new-11-color-sweep.jpg" width="32%" alt="Storage in the Color Sweep, passing pink">
</p>

The new words are in all 33 languages.

**[Full changelog](https://github.com/akilluminati47/RIPPS2/blob/main/CHANGELOG.md)** | **[Watch the v1.1.0 reel](https://youtu.be/Q8ZLd6ArV8s)** | **[Talk about it on psx-place](https://www.psx-place.com/threads/ripps2-a-ps2-front-end-in-one-elf-launch-disc-storage-memory-files.51316/)** | [RIPPCSX2](https://github.com/akilluminati47/RIPPCSX2/releases/latest) for seeing a theme in true 720p and 1080i

Beta: keep your usual loader close by, and tell us what breaks in [the psx-place thread](https://www.psx-place.com/threads/ripps2-a-ps2-front-end-in-one-elf-launch-disc-storage-memory-files.51316/) or [an issue](https://github.com/akilluminati47/RIPPS2/issues). This one wants consoles: launches right after boot (the guard), compression on your own drives (how long did it take, and what did the panel say?), and Delete on a test game. Thanks to ripto, nuno6573, zackcage6, eliminator1403, FifthFox, Mr.sus.60 and lukeatmynose for the reports that got us here. Special thanks to all the YouTube love as well: glad to help however you reach me.
