# Build 114 is RIPPS2 v1.1.4 beta: All Games from the first frame, hide and delete, your launchers found once, safe launches with the launch guard, every settings page on one screen, one HDD, new Color Themes and the Color Sweep, a theme list on SELECT, and games compressed to ZSO.

## Get it
- [Download the latest RIPPS2.elf](https://github.com/akilluminati47/RIPPS2/releases/latest/download/RIPPS2.elf) (always the newest build), [RIPPS2-languages.zip](https://github.com/akilluminati47/RIPPS2/releases/latest/download/RIPPS2-languages.zip) for your language, and [the theme pack](https://github.com/akilluminati47/RIPPS2-themes/releases/latest/download/RIPPS2-themes.zip) (edition 114, on the built-in fonts)

## Safe launches
- **No write runs into a launch.** Picking a game stops RIPPS2's own background saving and waits for one already started, so the reset never cuts a card image or a stick mid write.
- **Writes in step with the drive**: whole aligned pieces, one at a time, and **RiptOPL's guarded exFAT driver** (a game on a damaged FAT chain is refused instead of writing its VMC to the wrong place).
- **The launch guard.** Pick a game while a drive is still being read and a glass panel says what RIPPS2 is finishing; its notches fill and the game starts by itself. **Start now** stops the work safely and goes; **Back** returns you. A short wait shows only the loading icon.

## Games
- **All Games at once** at boot, before the drives answer; a game on a drive still waking waits for it.
- **Hide Game** (Triangle options): gone from every list until Game Sources > Hidden Games shows it again.
- **Delete, completely**: the image, its settings, art and cheats; its saves only if you say Yes. On the internal HDD (APA) a damaged table is refused before anything changes.
- **Compress to ZSO** (experimental): hold SELECT, say yes again, watch the bar. The ISO stays until every piece of the ZSO is checked, then you are asked (Back keeps both). The ZSO starts with the OPL core, saves and all, and can be made an ISO again; hidden games too.
- **Your launchers, found once**: Game Sources > Cache > Look now. **Mode 8 (Slow Reads)** from RiptOPL for DVD games that fail on fast reads.

## Settings and looks
- **Every page on one screen** but Network (BDM Devices and Screen have their own), **one HDD** (APA or exFAT, shown once), **Color Themes** Tangerine, Flamingo, Turquoise, Moonlight and Custom, the **Color Sweep**, the **theme list** on a held SELECT, and **Text Weight** with one newer Roboto.

## Test list
- **A launch right after boot** while a drive is still listing (MMCE, iLink, a big USB): does the guard panel show, fill, and start the game by itself?
- **Start now** and **Back** on the guard panel: a clean start, or back where you were, drives and cards fine?
- **A launch a few seconds after boot**: only the loading icon, then the game?
- **Compress a test game** on USB or the exFAT HDD: does it finish, does the ZSO start with its VMC save, does Uncompress give the ISO back? How long, against the panel's guess?
- **A nearly full drive**: compressing a game bigger than the free space says what it needs and changes nothing?
- **A new VMC on USB** (a game's VMC settings, Create): made, and the game saves to it?
- **Hold SELECT** on a game list: the theme list, your pick loaded?
- **All Games after a power cycle**: every game at once, covers coming in as drives answer?
- **Hide Game**, then Hidden Games > Show It Again: back in every list?
- **Delete** a test game: everything of it gone, its VMC kept when you answer No?
- **Look now**: your POPSTARTER, Ember and Neutrino found where you keep them?
- **One HDD** on exFAT: one HDD Games in Storage, still there with BDM Devices Start Mode Off?
- **Color Themes and the Color Sweep** on your TV (480i, 720p, 1080i): smooth, never flashing?
- **Your language**: Settings in one typeface (Russian, Greek, Polish, Vietnamese...)?

## Report
Post in the [psx-place thread](https://www.psx-place.com/threads/ripps2-a-ps2-front-end-in-one-elf-launch-disc-storage-memory-files.51316/) or here with your **console model**, your drives, where RIPPS2 starts from, and a **photo** of anything odd. Thanks to ripto, nuno6573, zackcage6, eliminator1403, FifthFox, Mr.sus.60 and lukeatmynose for the reports that got us here. Special thanks to all the YouTube love as well: glad to help however you reach me.
