# Build 107 is RIPPS2 v1.0.7 beta: RIPDISC rips your discs, RIPPS2 in 33 languages, Power Off in the in-game menu, Search in Memory Files and the star on the left.

## Get it
- [Download the latest RIPPS2.elf](https://github.com/akilluminati47/RIPPS2/releases/latest/download/RIPPS2.elf) (this link always gets the newest build), [RIPPS2-languages.zip](https://github.com/akilluminati47/RIPPS2/releases/latest/download/RIPPS2-languages.zip) for your language, and [the theme pack](https://github.com/akilluminati47/RIPPS2-themes/releases/latest/download/RIPPS2-themes.zip) (edition 107: replace your Adapt folders)
- [The psx-place thread](https://www.psx-place.com/threads/ripps2-a-ps2-front-end-in-one-elf-launch-disc-storage-memory-files.51316/) and [the beta reel](https://youtu.be/LPjdK_E1jjM)

## RIPDISC
- **Launch Disc rips the disc in the drive.** After 4.2 s a glass panel offers RIPDISC; hold SELECT until its ring fills. The confirm step shows the size, **how long it should take** and where it goes; START rips.
- **PS2 games** become an ISO in your DVD or CD folder (over 4 GB on a stick: OPL's 1 GB parts with ul.cfg). **PS1 games** a BIN and CUE for Ember. **Audio CDs and DVD videos** go through Memory Files: the clipboard says RIPPED, PASTE where you want them (a new MEDIA folder by default).
- The time estimate learns your console's real speed from your first rip. Any WAV or OGG in AUDIO is now menu music by its own name.

## Everything else
- **33 languages**, Arabic and Persian right to left with joined letters, Lao in its own font: copy `LNG` from RIPPS2-languages.zip, then Settings > Display Settings > Language.
- **Power Off** is the in-game menu's last choice (second press turns the PS2 off).
- **SEARCH FILES** in Memory Files' settings grid (Start in the browser) finds any file or folder by name on every started drive.
- **The star sits at the start of the row** now; Settings > Game Sources > Starred Games Star moves it right or hides it. Themes get new list keys (star, highlight, row icons).
- RiptOPL brought up to 10/18/2026 underneath (548 upstream commits) and the version line tells the truth.

## Test list
- **Rip a PS2 DVD to a USB stick** (under 4 GB): was the estimate close? Does the game show and launch from Storage?
- **Rip a PS2 game over 4 GB to a USB stick:** does it land as ul.* parts and launch?
- **Rip to the internal exFAT HDD:** how long did it take, and did the next estimate match it?
- **Dual-layer DVD** (a big late-era game): is the size right and does the ISO boot?
- **Rip an audio CD:** MEDIA, PASTE, START. Do the WAVs play on a PC? Copy one into AUDIO: is it in Settings > Audio Settings > Music?
- **Rip a PS1 game:** does Ember start the BIN and CUE from the PS1 list?
- **Cancel a rip halfway:** is everything it wrote gone?
- **Power Off in the in-game menu** (In-Game Menu on in Settings > General): does the second press turn the console off cleanly? The lab could not show this one.
- **SEARCH FILES:** search a word from a save, a game and an ELF. Does Cross open the folder with the cursor on it?
- **The star:** star a few games. Do the titles stay lined up? Try Right and Hidden too.
- **Your language:** anything cut off, overlapping or untranslated? Arabic and Persian readers: does every line read right?
- **720p and 1080i:** any of the above looking wrong in an HD mode?

## Report
Post in the [psx-place thread](https://www.psx-place.com/threads/ripps2-a-ps2-front-end-in-one-elf-launch-disc-storage-memory-files.51316/) or here with your **console model**, your drives, and a **photo** of anything odd.
