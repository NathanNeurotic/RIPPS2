<p align="center"><img src="https://raw.githubusercontent.com/akilluminati47/RIPPS2/v1.1.2-beta/media/ripps2-test-me.png" alt="RIPPS2: Rip it, build 112"></p>

## Rip it: RIPPS2 v1.1.2 beta (build 112)

**[Download RIPPS2.elf](https://github.com/akilluminati47/RIPPS2/releases/download/v1.1.2-beta/RIPPS2.elf)** (one file, about 3 MB) and put it in place of your old one. Your settings stay where they were. **[RIPPS2-languages.zip](https://github.com/akilluminati47/RIPPS2/releases/download/v1.1.2-beta/RIPPS2-languages.zip)** puts RIPPS2 in your language. The **[theme pack](https://github.com/akilluminati47/RIPPS2-themes/releases/latest)** is still edition 108.

### The sounds walkthrough
<!-- ripps2-sounds-video -->
<p align="center"><a href="https://akilluminati47.github.io/RIPPS2/media/b112/ripps2-v112-sounds.mp4"><img src="https://raw.githubusercontent.com/akilluminati47/RIPPS2/v1.1.2-beta/media/b112/03-sounds-video.jpg" width="40%" alt="The v1.1.2 sounds walkthrough: one take, from the boot sound to a game launching"></a></p>

**[Play it](https://akilluminati47.github.io/RIPPS2/media/b112/ripps2-v112-sounds.mp4)** (it opens in your browser). One take, no cuts, the console's own audio: the boot sound, the drive answering, the menu music under everything, then every sound as you browse, in the order of the badges, and a game launching last.

### BIOS Music: the menu's own piece
- **The menu music is the menu's now.** Since build 100, BIOS Music ripped the red screen's music ("Please insert a PlayStation or PlayStation 2 format disc": the tense opening, then waves). The browser's main menu plays the clock's piece (5:04), and that is what BIOS Music rips first now.
- **Choose which:** the menu music (the clock), the red screen music (the disc warning), or both. The menu's is `bgm_00 Menu.wav`, the track RIPPS2 plays when no other is picked; the red screen's is `bgm_01 Red Screen.wav`, listed as Red Screen in Audio Settings > Music.
- **Ripped before?** Your `bgm_00 Menu.wav` is the red screen's piece: rip again with THE MENU MUSIC, or BOTH to keep the red screen's as its own track.

<p align="center">
<img src="https://raw.githubusercontent.com/akilluminati47/RIPPS2/v1.1.2-beta/media/b112/01-music-chooser.jpg" width="48%" alt="BIOS Music: WHICH MUSIC? The menu music (the clock) 5:04, the red screen music (disc warning) 5:31, both">
<img src="https://raw.githubusercontent.com/akilluminati47/RIPPS2/v1.1.2-beta/media/b112/02-both-ripped.jpg" width="48%" alt="Both ripped: bgm_00 Menu.wav (13.9 MB) and bgm_01 Red Screen.wav (15.1 MB)">
</p>

**Hotfix (10/22):** the lengths in the BIOS Music chooser ran out of its box; they sit inside it now (RIPPS2.elf replaced, still build 112).

Build 111 is in this release too: the ripped menu music plays at all (any 16-bit WAV, as 48 kHz stereo), music on every theme, sounds that no longer reload on every theme change, Save Settings To that keeps a drive with a memory card in, and the star and Settings highlight on their words. Thanks to **lukeatmynose** for the reports from a real console.

**[Full changelog](https://github.com/akilluminati47/RIPPS2/blob/main/CHANGELOG.md)** | **[Watch the v1.1.0 reel](https://youtu.be/Q8ZLd6ArV8s)** | **[Talk about it on psx-place](https://www.psx-place.com/threads/ripps2-a-ps2-front-end-in-one-elf-launch-disc-storage-memory-files.51316/)** | [RIPPCSX2](https://github.com/akilluminati47/RIPPCSX2/releases/latest) for seeing a theme in true 720p and 1080i

Beta: keep your usual loader close by, and tell us what breaks in [the psx-place thread](https://www.psx-place.com/threads/ripps2-a-ps2-front-end-in-one-elf-launch-disc-storage-memory-files.51316/) or [an issue](https://github.com/akilluminati47/RIPPS2/issues). This one wants consoles: does the menu music you rip sound like your PS2's main menu, and does it loop cleanly?
