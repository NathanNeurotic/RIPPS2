# Build 117 is RIPPS2 v1.1.7 beta: BOOT LOCK through FreeMcBoot and OSDMenu, drive pages that show their games on Manual, the sidebar's keys the same on every theme, RIPFLOW's case tilt, music that keeps playing on an SD2PSX, and RIPSHOT on MMCE.

## Get it
- [Download the latest RIPPS2.elf](https://github.com/akilluminati47/RIPPS2/releases/latest/download/RIPPS2.elf) (always the newest build), [RIPPS2-languages.zip](https://github.com/akilluminati47/RIPPS2/releases/latest/download/RIPPS2-languages.zip) (every release carries it, all 33 languages) and [the theme pack](https://github.com/akilluminati47/RIPPS2-themes/releases/latest/download/RIPPS2-themes.zip) (edition 117: the new `flowtilt` key)

## BOOT LOCK
- **Your own loader**: BOOT LOCK now writes FreeMcBoot's config (`LK_Auto_E1`) and puts RIPPS2 first in OSDMenu's menu, as well as PS2BBL's. With the IGR Path empty, a game's **EXIT** goes to the browser and back through your loader (issue #3).

## Drives on Manual
- A drive's page shows **its games before the drive starts** (its part of All Games), and **X on one starts the drive and the game**: no more "HDD not connected".

## The sidebar, on every theme
- **Circle** opens it everywhere, **Left** on a list, **Right** never changes the source; **L1 / R1** are the theme's own again (a list's pages like OPL, RIPFLOW's covers). **RIPFLOW and RIPGRID** loop their covers on Left / Right. **RIPFLOW**: Up / Down or the left stick tilt the centre case (`flowtilt`). Launch Disc ignores L1 / R1, Memory Files steps its orbs with them, boxes sit flush with the bar.

## Music, sounds and RIPSHOT
- **.wav and .mp3 music keep playing** on an SD2PSX after message boxes and menu changes, **menu sounds load whole**, the **BIOS Music rip** no longer races the music. **RIPSHOT works for MMCE games** (the APA HDD comes later).

## Test list
- **BOOT LOCK with FreeMcBoot** (1.9x or 1.8) on your card: turn it on, power off and on. Does RIPPS2 start? Turn it off: your old auto-start back?
- **BOOT LOCK with OSDMenu**: is RIPPS2 the first item in its menu?
- **A game's EXIT** with BOOT LOCK on and the IGR Path empty: browser, then your loader, then RIPPS2? Any black screen?
- **A drive on Manual** (Game Sources): does its page show its games right after boot? SELECT brings the covers?
- **X on a game from a drive on Manual** (HDD, USB, MMCE): does the game start without a "not connected" message?
- **A .wav or .mp3 as menu music on an SD2PSX**: still playing after a message box and five or six menu changes?
- **BIOS Music > Rip**, then keep browsing: the music keeps going?
- **Menu sounds** on an SD2PSX: any that cut short or sound wrong?
- **RIPSHOT in a game from your SD2PSX**: take a shot with ART and MEDIA. Is it in Memory Files > MEDIA/RIPSHOT after?
- **An OPL theme with the sidebar on**: L1 / R1 turn pages, Circle opens the sidebar, Right never changes the source?
- **RIPFLOW**: Up / Down and the left stick tilt the case; Left on the first cover goes to the last?
- **RIPGRID**: Left on the first cover goes to the last, Circle opens the sidebar?
- **Launch Disc with a disc in**: L1 / R1 do nothing, and the RIPDISC box starts right at the bar's edge?
- **Memory Files**: L1 / R1 change the orb formation?
- **Theme pack edition 117**: Adapt and Adapt Rx look right with this build?

## Report
Post in the [psx-place thread](https://www.psx-place.com/threads/ripps2-a-ps2-front-end-in-one-elf-launch-disc-storage-memory-files.51316/) or here with your **console model**, your drives, your **boot loader**, where RIPPS2 starts from, your **DIAG.TXT** and a **photo** of anything odd. Thanks to ripto, nuno6573, zackcage6, eliminator1403, FifthFox, Mr.sus.60 and lukeatmynose for the reports that got us here, and to DarkNerdShawny for issue #3. Special thanks to all the YouTube love as well: glad to help however you reach me.
