<p align="center"><img src="https://raw.githubusercontent.com/akilluminati47/RIPPS2/v1.1.5-beta/media/ripps2-test-me.png" alt="RIPPS2: Rip it, build 115"></p>

## Rip it: RIPPS2 v1.1.5 beta (build 115)

**[Download RIPPS2.elf](https://github.com/akilluminati47/RIPPS2/releases/download/v1.1.5-beta/RIPPS2.elf)** (one file, @SIZE@) and put it in place of your old one. Your settings stay where they were. **[RIPPS2-languages.zip](https://github.com/akilluminati47/RIPPS2/releases/download/v1.1.5-beta/RIPPS2-languages.zip)** puts RIPPS2 in your language: every release carries the language pack, kept up to date with each build. The **[theme pack](https://github.com/akilluminati47/RIPPS2-themes/releases/latest)** is edition 115: Adapt and Adapt Rx are each a config and one picture now (a theme of two files), so update it with this build.

**[Watch the v1.1.5 Short](https://akilluminati47.github.io/RIPPS2/media/b115/ripps2-v115-short.mp4)** (on GitHub, no YouTube needed).

Build 115 is the first build shaped on real hardware with an SD2PSX (LinkRetro's SD2PSXTD on sd2psXtd 1.4.0): MMCE and the controller share one bus, so most of what is below is about that.

### Fast Boot
- **Settings > Game Sources > Cache > Fast Boot.** The boot reads RIPPS2's own drive only: a small `RIPPS2.FB` beside RIPPS2.ELF says where your settings and sounds are, so there is no memory card scan and no search over every drive, and every list shows from its cache.
- **The other drives wait until you need them**: SELECT on a page starts its drives and brings their art (on All Games, every waiting drive), and a game from a waiting drive starts it. With Automatic Refresh on, they start at boot as before.
- **Your sounds beside RIPPS2**: turning it on copies them (and your music when there is room) into the AUDIO folder beside RIPPS2, the first place the boot looks.

<p align="center">
<img src="https://raw.githubusercontent.com/akilluminati47/RIPPS2/v1.1.5-beta/media/b115/new-02-fast-boot.jpg" width="48%" alt="Game Sources > Cache: Fast Boot and what it does">
<img src="https://raw.githubusercontent.com/akilluminati47/RIPPS2/v1.1.5-beta/media/b115/new-03-rip-places.jpg" width="48%" alt="BIOS Music: choose where the rip goes, beside RIPPS2 first">
</p>

### MMCE and the controller
- **Game ID on by default**: RIPPS2 sends the game's ID and waits on screen while your SD2PSX makes the game's memory card, so a streaming game never starts before its card is ready (START skips).
- **No jumping cursor**: a pad read the busy bus missed no longer counts as "nothing pressed" (one press became several). **Pad First** keeps covers coming in small pieces with the pad read between them.
- **Always analog**: a pad left in digital mode is asked for analog mode again while idle (an 8BitDo receiver too). If your right stick still does not tilt, tell us with your DIAG.TXT.
- **STATUS > SAVE DIAGNOSTICS** writes DIAG.TXT beside RIPPS2: pad gaps, MMCE timings, each launch's steps and now the boot's steps, so a hardware report shows what happened.

### Music
- **MP3**: Memory Files plays .mp3, and an .mp3 in AUDIO is music.
- **A CD player for your own tracks**: mark .wav, .ogg or .mp3 files in Memory Files and open them together: they play as one disc in Launch Disc's CD player, over the towers lit by the music, track after track. One track opens there too.
- **BIOS Music** plays clean all the way through, and the ripped track is your music at once and after a reboot. **Choose where a rip goes**: RIPPS2's own drive first (read first at boot), then each drive with its free space. WAV music no longer stutters from MMCE.

<p align="center">
<img src="https://raw.githubusercontent.com/akilluminati47/RIPPS2/v1.1.5-beta/media/b115/new-01-cd-player.jpg" width="48%" alt="Two marked MP3s playing as a disc in the CD player, the towers lit by the music">
<img src="https://raw.githubusercontent.com/akilluminati47/RIPPS2/v1.1.5-beta/media/b115/new-04-set-metadata.jpg" width="48%" alt="A PS1 game's options: Set Metadata (Rename) above Delete">
</p>

### BIBLE
- **RIPPS2 is never copied anywhere.** BBL 1.20 starts RIPPS2 where it is (a memory card, USB or MX4SIO). Running from MMCE on an SD2PSX BOOT card, whose PS2BBL Extended can read MMCE, BIBLE sets BOOT LOCK there instead.
- **"RIPPS2: Setting up BBL 1.20"**, for standard 8 MB memory cards, slots 1 and 2 by name, and **RESTORE** puts back what it replaced.
- **Your drives come back** after BIBLE restarts the I/O processor (USB, the HDD and MMCE stayed gone until a power cycle). If a card refuses the write, the message says so, and that an SD2PSX may protect itself until you turn the console off and on.

### Lists, sidebar and themes
- **Sidebar styles Classic and XL**, Left to the sidebar from lists and info pages, Up / Down along it, Circle to bring it out. **RIPGRID stops at the first and last row** (Circle or the sidebar changes the source).
- **Set Metadata (Rename)** just above Delete on every game, PS1 games and apps included, and the options no longer crowd the game's name. **R3** held 4.2 s hides or shows the stars. **Hold SELECT** opens the theme list without a freeze. **Recent Games** has its own page (1 to 99).
- **Themes of two files**, RIPPS2's own badges, the OSDSYS-style hints, Roboto option names on every theme. Art found under every name (OPL Manager's `_BG_00` and `_SCR_00` too), and **All Games shows PS1 and PS2 games together** (issue #4).
- **POPSTARTER**: RIPPS2 knows both of its file sets (POPS_IOX.PAK with POPS.PAK, or with POPS.ELF and IOPRP252.IMG) and RIPPOPS copies every one it finds.

### Thanks
Thanks to ripto, nuno6573, zackcage6, eliminator1403, FifthFox, Mr.sus.60 and lukeatmynose for the reports that got us here. Special thanks to all the YouTube love as well: glad to help however you reach me.

The full list is in the [changelog](https://github.com/akilluminati47/RIPPS2/blob/main/CHANGELOG.md).
