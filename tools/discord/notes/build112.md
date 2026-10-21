# Build 112 is RIPPS2 v1.1.2 beta: BIOS Music rips your PS2's real menu music now, the clock's ambient piece, and lets you pick the red screen's piece or both. Build 111 rode along with it: ripped music that plays, sounds that stop reloading, and Save Settings To that keeps a drive with a memory card in.

## Get it
- [Download the latest RIPPS2.elf](https://github.com/akilluminati47/RIPPS2/releases/latest/download/RIPPS2.elf) (this link always gets the newest build), [RIPPS2-languages.zip](https://github.com/akilluminati47/RIPPS2/releases/latest/download/RIPPS2-languages.zip) for your language, and [the theme pack](https://github.com/akilluminati47/RIPPS2-themes/releases/latest/download/RIPPS2-themes.zip) (edition 108)
- The video above is the v1.1.2 sounds walkthrough: one take from the boot sound to a game launching, every sound in turn

## BIOS Music
- **The menu's own piece.** BIOS Music ripped the red screen's music since build 100 (the "insert a PlayStation disc" screen). The main menu plays the clock's piece (5:04), and that is the default now.
- **Choose:** the menu music (the clock), the red screen music (the disc warning), or both. `bgm_00 Menu.wav` plays by default; `bgm_01 Red Screen.wav` is listed as Red Screen in Audio Settings > Music.
- **Ripped before?** Rip again with THE MENU MUSIC: your old Menu file is the red screen's.

## Build 111, here too
- **Ripped menu music plays** (any 16-bit WAV as 48 kHz stereo), **music on every theme**, **sounds load once per set** instead of on every theme change.
- **Save Settings To keeps a drive with a memory card in**, and Memory Card chosen again sticks.
- The favourites star on its title's centreline, the Settings highlight on its word. Thanks to lukeatmynose for the console reports.

## Test list
- **BIOS Music > THE MENU MUSIC** on your console: does it sound like your PS2's main menu? Does it loop cleanly after 5:04?
- **BOTH:** do both files land in AUDIO, and does Audio Settings > Music list Menu and Red Screen?
- **Theme changes** with your BIOS sounds: any cut-off, late or doubled sound right after a SELECT hold?
- **Save Settings To > a drive** with a memory card in: power cycle. Are the drive's settings back?

## Report
Post in the [psx-place thread](https://www.psx-place.com/threads/ripps2-a-ps2-front-end-in-one-elf-launch-disc-storage-memory-files.51316/) or here with your **console model**, your drives, where RIPPS2 starts from, and a **photo** of anything odd.
