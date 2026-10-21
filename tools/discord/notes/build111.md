# Build 111 is RIPPS2 v1.1.1 beta: the menu music you rip from your BIOS plays, your music plays on every theme, sounds stop reloading on every theme change, and a drive you save your settings to stays chosen with a memory card in. Thanks to lukeatmynose for the reports from a real console.

## Get it
- [Download the latest RIPPS2.elf](https://github.com/akilluminati47/RIPPS2/releases/latest/download/RIPPS2.elf) (this link always gets the newest build), [RIPPS2-languages.zip](https://github.com/akilluminati47/RIPPS2/releases/latest/download/RIPPS2-languages.zip) for your language, and [the theme pack](https://github.com/akilluminati47/RIPPS2-themes/releases/latest/download/RIPPS2-themes.zip) (edition 108)
- The video above is the v1.1.1 sounds lesson: both BIOS rips on a fresh RIPPS2, then every sound in the order you meet it

## Music
- **BIOS Music's rip plays now.** It is a 24 kHz mono WAV and the PS2's audio driver plays neither, so the 15 MB file sat there and the menu stayed silent (lukeatmynose). Any 16-bit WAV in AUDIO now plays as 48 kHz stereo.
- **Adapt and Adapt Rx play your music** (Audio settings > Music, or the track called Menu) when the theme has no bgm.ogg of its own.

## Sounds
- **The same sounds are not loaded again** on a theme change or a SELECT hold: every change silenced all voices and rewrote all 15 sounds, seconds from a memory card. Now only a changed file reloads the set.

## Save Settings To
- **A drive stays chosen with a memory card in** (lukeatmynose): the card's save now carries a pointer to the drive, so its old settings no longer win at boot.
- **Memory Card chosen again sticks**: the pointer to the drive goes with it.

## Look
- The favourites star on its title's centreline, the Settings highlight centred on the word.

## Test list
- **BIOS Music on your console:** rip it (Audio Settings > BIOS Music), back out. Does the menu music start, and does it loop cleanly at the end (5:31)?
- **Your own WAVs:** a 44.1 kHz or mono 16-bit WAV in AUDIO. Does it play at the right speed and pitch?
- **Theme changes:** hold SELECT through your themes with your BIOS sounds. Any cut-off, late or doubled sound right after a change?
- **Save Settings To > USB Drive** (or MX4SIO, iLink, MMCE, Internal HDD) with a memory card in: change a setting, Save Changes, power off and on. Are the drive's settings back, and does Save Settings To still name the drive?
- **Then Memory Card again:** save, power cycle. Does it stay Memory Card?
- **MMCE first boot:** lukeatmynose's first list took about 2 minutes, later ones were fast. How long does your first boot take, and how many games?
- **Booting from the HDD (APA or exFAT) with a card in:** do the settings come from where you chose?

## Report
Post in the [psx-place thread](https://www.psx-place.com/threads/ripps2-a-ps2-front-end-in-one-elf-launch-disc-storage-memory-files.51316/) or here with your **console model**, your drives (MMCE or MX4SIO model and firmware too), where RIPPS2 starts from, and a **photo** of anything odd.
