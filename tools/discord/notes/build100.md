# Build 100 is the first beta: RIPPS2 v0.1.0. Clean sound from your own console, the menu music ripped on its own, and RIPPS2's own memory card save. The beta reel and a psx-place thread are up.

## Watch and talk
- **[The beta reel](https://youtu.be/LPjdK_E1jjM)** (9:45, every chapter in the description)
- **[The psx-place thread](https://www.psx-place.com/threads/ripps2-a-ps2-front-end-in-one-elf-launch-disc-storage-memory-files.51316/)**: RIPPS2 goes public there
- [Download the latest RIPPS2.elf](https://github.com/akilluminati47/RIPPS2/releases/latest/download/RIPPS2.elf) (this link always gets the newest build) and [the theme pack](https://github.com/akilluminati47/RIPPS2-themes/releases/latest/download/RIPPS2-themes.zip)

## Sound, cleaned up
- The ripped boot and launch music no longer pop (three instruments were misread as the SPU2's noise). **Rip again** (Audio settings > BIOS Sounds) to get the clean ones.
- The beep after saving settings is gone; every press makes one sound; nothing sounds without a press (no sound when art loads or a drive is scanned). Adapt and Adapt Rx ship no sounds now, so your rips play.

## The menu music, ripped on its own
- **Audio settings > BIOS Music > RIP**: your console's ambient menu piece (5:31) as a WAV, its size (15.1 MB) shown first, beside RIPPS2 or in OPL's AUDIO folder on a drive. The Music list reads OPL's AUDIO folder on every started drive too.

## RIPPS2's own save, and more
- Settings live in **mc0:/RIPPS2** (the hat, the settings, nothing else), apart from any other OPL.
- Replace is a clean erase, copy and check; an ISO or ZSO starts wherever it is; the text editor reads in RIPPS2 Sleek; POPSTARTER from USB remembers your drive's format; cases flip from the side you push; the menus read in one clear face.

## Test list
- **The beep**: change something in Interface (a new theme), back out, save. Any tone after the save message?
- **Clean rips**: rip BIOS Sounds again, reboot, launch a game. Do the boot and launch sounds play without pops?
- **One press, one sound**: open menus and message boxes, save settings. Do you ever hear two sounds for one press, or a sound when cover art appears?
- **Your card**: after a save, look in the PS2 browser. Is there a RIPPS2 save with the hat ringing its bell, and does a reboot keep your settings?
- **BIOS Music**: rip it to a USB drive or OPL's AUDIO folder, then pick Menu in Audio settings. Does it play and loop?
- **ISO anywhere**: start an ISO from any folder in Memory Files.
- **POPSTARTER from USB**: does it stop asking FAT32 or exFAT on the second game?

## Report
Post in the [psx-place thread](https://www.psx-place.com/threads/ripps2-a-ps2-front-end-in-one-elf-launch-disc-storage-memory-files.51316/) or here with your **console model**, your drives, and a **photo** of anything odd.
