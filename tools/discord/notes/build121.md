# Build 121 is RIPPS2 v1.2.1 beta: the boot sound with the pillars from your memory card, RIPPS2 starting on its sky, and build 119's fixes.

## Get it
- [Download the latest RIPPS2.elf](https://github.com/akilluminati47/RIPPS2/releases/latest/download/RIPPS2.elf) (always the newest build), [RIPPS2-languages.zip](https://github.com/akilluminati47/RIPPS2/releases/latest/download/RIPPS2-languages.zip) (all 33 languages), and the [theme pack](https://github.com/akilluminati47/RIPPS2-themes/releases/latest/download/RIPPS2-themes.zip), edition 119

## The boot sound from your memory card
- Started from a memory card with your sounds on the HDD or USB, the boot sound came seconds after the pillars: the drive is not up yet. After **BIOS Sounds > Rip** to a drive, RIPPS2 now says so in one line with the sizes, and **START copies just boot.adp** (about 360 KB) beside RIPPS2 on the card. The next boot plays it from there, about 2 s sooner on PCSX2.

## Since v1.1.8
- RIPPS2 starts on its sky in your video mode and colours, not black.
- The info page is the game's: the sidebar stays away until Left. The ART Pack counts, sizes and times its job, with RIPPS2's progress bar.
- RIPPS2's save no longer shows as corrupted data on early consoles. EXIT never goes black. No boot stuck on the towers. Your media plays with Music off. Source Name has Pop In and Name.

## Test list
- **Card boot, sounds on a drive**: Rip BIOS Sounds to the drive. Does the COPY question come, with the right sizes?
- **After COPY, reboot**: does the boot sound start with the pillars now? How much sooner than before?
- **Back instead of COPY**: nothing written to the card?
- **Rip again** after a COPY: the question comes again, and the new boot sound is the one that plays?
- **A nearly full card**: no question, nothing half written?
- **RIPPS2 started from USB or the HDD**: no question at all, boot sound as before?
- **The boot from BIBLE or your loader**: sky, then the towers, no black frame in RIPPS2?
- **Your video mode and Widescreen** (720p, 1080i, 480p): the first frame already in them?
- **The info page** on your theme: Left brings the sidebar, Circle or Right put it away?
- **RIPPS2's save** in the console's browser: the hat icon, no corrupted data?
- **EXIT in a game** with an empty IGR Path: back to your boot, never black?
- **A language file on the card** with sounds beside RIPPS2: the boot reaches the menu every time?
- **Music off**: your own tracks and the CD player still play?

## Report
Please [open an issue on GitHub](https://github.com/akilluminati47/RIPPS2/issues) with your **console model**, your drives, your **boot loader**, where RIPPS2 starts from, your **DIAG.TXT** (STATUS > SAVE DIAGNOSTICS) and a **photo** of anything odd: an issue is the best way to get RIPPS2 updated. Thanks to ripto, nuno6573, zackcage6, eliminator1403, FifthFox, Mr.sus.60, lukeatmynose and ahavasi for the reports that got us here, to DarkNerdShawny for opening issues on GitHub, and to everyone testing RIPPS2 on Discord and opening issues on GitHub: be like them. Special thanks to all the YouTube love as well: glad to help however you reach me.
