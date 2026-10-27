<p align="center"><img src="https://raw.githubusercontent.com/akilluminati47/RIPPS2/v1.1.8-beta/media/ripps2-test-me.png" alt="RIPPS2: Rip it, build 118"></p>

## Rip it: RIPPS2 v1.1.8 beta (build 118)

**[Download RIPPS2.elf](https://github.com/akilluminati47/RIPPS2/releases/download/v1.1.8-beta/RIPPS2.elf)** (one file, 2,706 KB) and put it in place of your old one. Your settings stay where they were. **[RIPPS2-languages.zip](https://github.com/akilluminati47/RIPPS2/releases/download/v1.1.8-beta/RIPPS2-languages.zip)** puts RIPPS2 in your language: every release carries it, and this one has build 118's new words in all 33 languages. The **[theme pack](https://github.com/akilluminati47/RIPPS2-themes/releases/latest)** is still edition 117: nothing in it changed.

Build 118 is about speed at boot and while you browse: the boot sound with the first frame, and every cover from one file.

### The boot sound with the first frame
- The boot sound used to wait until every drive had started and listed its games, so it came in with the list. Now it is the first thing read at boot, as soon as the settings are, so it plays as the towers appear. On PCSX2 it starts 2 seconds earlier than in v1.1.7. With **Fast Boot** on (Settings > Game Sources > Cache), the AUDIO folder beside RIPPS2 is known from the first moment.
- **Where AUDIO and MEDIA go**: the README.txt RIPPS2 writes into each now says it. AUDIO beside RIPPS2.ELF, on the drive RIPPS2 starts from (the boot reads it first); MEDIA on your biggest drive (nothing in it is read at boot).

### ART Pack: every cover from one file
- **Settings > Game Sources > Cache > ART Pack** packs the ART folder of every started drive into one `art.tar` on the drive you pick. RIPPS2 measures how fast each drive reads its own art and lists the fastest first, so X takes it (an SD2PSX's SD, say).
- The pictures go in as they are (PNG and JPG are already compressed: the tar bundles them, and a PC opens it like any tar). **Your ART folders are not touched.** The same button removes the pack.
- From then on covers load from that one file through one index, written with the pack. A game the pack was built for never has its ART folder asked one picture at a time, missing pictures included: less reading on the drive your music streams from, and art that keeps up with the cursor.
- JPG covers and OPL Manager's names (`_BG_00`, `_SCR_00`) work from the pack. Art RIPPS2 fetches or shoots later shows at once; art you copy in on a PC shows after you build the pack again. You can copy `art.tar` to another drive's ART folder with Memory Files, but build it on the drive you browse from.

<p align="center">
<img src="https://raw.githubusercontent.com/akilluminati47/RIPPS2/v1.1.8-beta/media/b118/new-01-art-pack-chooser.jpg" width="48%" alt="ART Pack: the drive with the art, its read speed, the fastest first">
<img src="https://raw.githubusercontent.com/akilluminati47/RIPPS2/v1.1.8-beta/media/b118/new-02-art-pack-built.jpg" width="48%" alt="The ART Pack is built: 77 pictures, 6 MB, in mass0:/ART/art.tar">
</p>
<p align="center">
<img src="https://raw.githubusercontent.com/akilluminati47/RIPPS2/v1.1.8-beta/media/b118/new-03-art-pack-cache.jpg" width="48%" alt="Game Sources > Cache: the ART Pack in use">
<img src="https://raw.githubusercontent.com/akilluminati47/RIPPS2/v1.1.8-beta/media/b118/new-04-art-from-pack.jpg" width="48%" alt="A game's info page, its logo, background, disc and JPG cover read from the pack">
</p>

### Thanks
Thanks to ripto, nuno6573, zackcage6, eliminator1403, FifthFox, Mr.sus.60 and lukeatmynose for the reports that got us here, and to DarkNerdShawny for opening issues on GitHub (three so far): an issue is the best way to get RIPPS2 updated, so be like DarkNerdShawny and [open one](https://github.com/akilluminati47/RIPPS2/issues). Special thanks to all the YouTube love as well: glad to help however you reach me.

The full list is in the [changelog](https://github.com/akilluminati47/RIPPS2/blob/main/CHANGELOG.md).
