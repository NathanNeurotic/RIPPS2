<p align="center"><img src="https://raw.githubusercontent.com/akilluminati47/RIPPS2/v1.2.1-beta/media/ripps2-test-me.png" alt="RIPPS2: Rip it, build 121"></p>

## Rip it: RIPPS2 v1.2.1 beta (build 121)

**[Download RIPPS2.elf](https://github.com/akilluminati47/RIPPS2/releases/download/v1.2.1-beta/RIPPS2.elf)** (one file, 2,708 KB) and put it in place of your old one. Your settings stay where they were. **[RIPPS2-languages.zip](https://github.com/akilluminati47/RIPPS2/releases/download/v1.2.1-beta/RIPPS2-languages.zip)** puts RIPPS2 in your language: every release carries it, and this one has builds 119 to 121's new words in all 33 languages. The **[theme pack](https://github.com/akilluminati47/RIPPS2-themes/releases/latest)** is edition 119: Adapt and Adapt Rx keep the sidebar on their info pages (it needs this release).

v1.2.1 carries three builds since v1.1.8: 119 (the info page, the ART Pack's flow, the save icon, EXIT, the boot hang fix), 120 (RIPPS2 starts on its sky) and 121 (the boot sound from the memory card).

### The boot sound with the pillars (build 121)
- RIPPS2 started from a memory card (through FreeMcBoot, PS2BBL, OSDMenu or BIBLE) reads its card at once, but an AUDIO folder on the HDD or a USB drive only once that drive is up, so the boot sound came seconds after the pillars. After **BIOS Sounds > Rip** writes the sounds to a drive, RIPPS2 now says so in one line with the sizes, and **START copies just `boot.adp`** (about 360 KB) beside RIPPS2 on the card. The boot reads that copy first: on PCSX2 the boot sound came about 2 seconds sooner (BIBLE starting RIPPS2 from the card, the sounds on a USB drive). Ripping again offers it again, so the copy follows your set. RIPPS2.elf is no bigger.

<p align="center">
<img src="https://raw.githubusercontent.com/akilluminati47/RIPPS2/v1.2.1-beta/media/b121/new-02-rip-where.jpg" width="48%" alt="BIOS Sounds > Rip: beside RIPPS2 on the card, or a drive">
<img src="https://raw.githubusercontent.com/akilluminati47/RIPPS2/v1.2.1-beta/media/b121/new-01-boot-sound-copy.jpg" width="48%" alt="After a rip to a drive: START copies boot.adp beside RIPPS2 on the memory card">
</p>

### RIPPS2 starts on its sky (build 120)
- Before its settings load, RIPPS2 reads your Video Mode, Widescreen and its sky straight from its settings file, so the screen starts in your mode with your colours instead of black, Auto first and your mode a moment later. The towers fade up over the sky.

### Build 119
- **The info page is the game's.** The sidebar stays out of sight there on every theme: Left brings it out, Circle or Right put it away and the page stays, Up / Down step the games. A theme can keep it with `info_sidebar=1` (Adapt and Adapt Rx do, edition 119).
- **The ART Pack's flow** as the other long jobs have it: the pictures counted and sized, the drives fastest first with their free space and only where it fits, the panel with how long it should take, and RIPPS2's numbered progress bar.
- **RIPPS2's save no longer shows as corrupted data** on early consoles (a v1.60 browser calls any icon of more than one shape corrupted): the hat is one shape now, the title is Shift-JIS, and RIPPS2 repairs its folder when the settings load or save.
- **EXIT never black.** The in-game menu's EXIT goes to your boot (FreeMcBoot, PS2BBL, OSDMenu, BIBLE or the browser) unless the IGR Path names an ELF the reset can load. STATUS says when an IGR Path is passed over.
- **No boot stuck on the towers** (v1.1.8, a language file on the card with a sound set beside RIPPS2).
- **Your media plays with Music off**: the media player and the file CD player; Music off keeps only the menu music away.
- **Source Name: Pop In and Name**: the big name as the source changes and the name under the games. RIPFLOW's default is written as Shown; pick Pop In or Pop In and Name to bring the big name back there.
- **BIBLE's splash in your colours**: RIPPS2 saves its sky with its settings (`ripps2_bible_sky`) for BIBLE to read.
- No text past its box, no stretched art in 16:9, Roboto on the long jobs' panels, and the About page's testers.

### Thanks
Thanks to ripto, nuno6573, zackcage6, eliminator1403, FifthFox, Mr.sus.60, lukeatmynose and ahavasi for the reports that got us here, to DarkNerdShawny for opening issues on GitHub, and to everyone testing RIPPS2 on Discord and opening issues on GitHub: be like them. An issue is the best way to get RIPPS2 updated: [open one](https://github.com/akilluminati47/RIPPS2/issues). Special thanks to all the YouTube love as well: glad to help however you reach me.

The full list is in the [changelog](https://github.com/akilluminati47/RIPPS2/blob/main/CHANGELOG.md).
