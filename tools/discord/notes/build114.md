# Build 114 is RIPPS2 v1.1.4 beta: All Games from the first frame, hide and delete, your launchers found once, safe launches with the launch guard, every settings page on one screen, one HDD, new Color Themes and the Color Sweep, one newer Roboto, a theme list on SELECT, and games compressed to ZSO.

## Get it
- [Download the latest RIPPS2.elf](https://github.com/akilluminati47/RIPPS2/releases/latest/download/RIPPS2.elf) (this link always gets the newest build), [RIPPS2-languages.zip](https://github.com/akilluminati47/RIPPS2/releases/latest/download/RIPPS2-languages.zip) for your language, and [the theme pack](https://github.com/akilluminati47/RIPPS2-themes/releases/latest/download/RIPPS2-themes.zip) (edition 114: Adapt on the built-in fonts)

## Safe launches
- **No write runs into a launch.** A launch now stops RIPPS2's own background saving first and waits for one already started, so a card image or a stick is never left half written by the reset.
- **Writes in step with the drive.** The lab found big writes starting at odd places in a file could land a cluster off on exFAT. RIPPS2.LST (the list cache on every drive) is now one write, and compression, RIPDISC's audio rips, screenshots and BIOS Music write in whole aligned pieces.
- **One write at a time.** RIPPS2's own saving waits its turn, and stops while Memory Files copies, RIPDISC rips or a game is compressed.
- **RiptOPL's guarded exFAT driver**: a game on a damaged FAT chain refuses to start instead of writing its VMC to the wrong place.
- **The launch guard.** Pick a game while a drive is still being read and a glass panel says what RIPPS2 is finishing; its notches fill toward when it will be done, and the game starts by itself. **START NOW** stops the work safely and goes; **Back** returns to where you were. Music keeps playing. A short wait shows only the loading icon.

## Games
- **Mode 8 (Slow Reads)** from RiptOPL, in a game's Compatibility settings: for DVD games that stutter or fail on the OPL core.
- **All Games at once** at boot, from a saved list, even before the drives answer; a game on a drive still waking waits for it.
- **Hide Game** (Triangle options): gone from every list until you show it again from Game Sources > Hidden Games.
- **Delete, completely**: the image, its settings, art and cheats; its saves only if you say Yes. On the internal HDD (APA) the table is checked first and a damaged one is refused before anything changes.
- **Compress to ZSO** (experimental, Triangle > Hide Game and Compression): hold SELECT, say yes again, watch the progress bar. The ISO stays until every piece of the ZSO is checked; the ZSO starts with the OPL core, saves and all, and can be made an ISO again. Hidden games can be compressed too (Game Sources > Hidden Games). It checks the drive has room first, and works on OPL Manager's SCUS_XXX.XX.Name.iso names as well.
- **Your launchers, found once**: POPSTARTER, the POPS files, Ember, its BIOS and Neutrino are searched for on your drives and remembered (Game Sources > Cache > Look now).

## Settings and looks
- **Every page on one screen** but Network: BDM Devices and Screen have their own pages, Flow and Grid is Layout, Colors and More is Colors and Text.
- **One HDD**: HDD Start Mode covers the internal drive, APA or exFAT, and Storage shows it once.
- **Color Themes**: Tangerine, Flamingo, Turquoise, Moonlight and Custom (pick your own color).
- **Color Sweep**: five colors the theme fades through, gently. Rainbow, one made from each Color Theme, or your own (Sweep Colors).
- **The theme list**: hold SELECT on a game list and pick a theme from a panel (Settings > Interface > Hold SELECT: List, Cycle or Off).
- **Text Weight** for the Settings tooltips, STATUS and About; one newer Roboto Condensed everywhere, the language pack included.

## Test list
- **A launch right after boot** while a drive is still listing (MMCE, iLink, a big USB): does the guard panel show, fill, and start the game by itself?
- **START NOW** on the guard panel: does the game start cleanly, and are your drives and cards fine after?
- **Back** on the guard panel: back on the list where you were, nothing changed?
- **A launch a few seconds after boot**: only the loading icon, then the game, no panel?
- **Compress a test game** (one you have a copy of) on USB or the exFAT HDD: does it finish, does the ZSO start with the OPL core and keep its VMC save, and does Uncompress give the ISO back?
- **A nearly full drive**: try to compress a game bigger than the free space. Does it say how much it needs and leave the drive alone?
- **A new VMC on USB** (a game's VMC settings, Create): made, and the game saves to it?
- **Hold SELECT** on a game list: the theme list, your pick loaded? Cycle and Off in Settings > Interface?
- **All Games after a power cycle**: every game listed at once, the covers coming in as the drives answer?
- **Hide Game**, then Game Sources > Hidden Games > Show Again: back in every list?
- **Delete** a test game: everything of it gone, its VMC kept when you answer No?
- **Look now** (Game Sources > Cache): does it find your POPSTARTER, Ember and Neutrino where you keep them?
- **One HDD**: on an exFAT internal drive, one HDD Games in Storage (no empty APA page), and still there with BDM Devices Start Mode Off? On APA, still there?
- **Game Sources and Interface**: everything on one screen, OK visible without scrolling?
- **Colors and Text**: Tangerine, Flamingo, Turquoise, Moonlight; then Custom and your own Theme Color?
- **Color Sweep Rainbow**: smooth, never flashing, on your TV (480i, 720p, 1080i)?
- **Sweep Colors**: change a color, save under a new name, still there after a power cycle?
- **Text Weight Bold**: tooltips heavier and still sharp?
- **Your language**: Settings in one typeface (Russian, Greek, Polish, Vietnamese...)?

## Report
Post in the [psx-place thread](https://www.psx-place.com/threads/ripps2-a-ps2-front-end-in-one-elf-launch-disc-storage-memory-files.51316/) or here with your **console model**, your drives, where RIPPS2 starts from, and a **photo** of anything odd. Thanks to ripto, nuno6573, zackcage6, eliminator1403, FifthFox, Mr.sus.60 and lukeatmynose for the reports that got us here.
