<p align="center"><img src="https://raw.githubusercontent.com/akilluminati47/RIPPS2/v1.1.7-beta/media/ripps2-test-me.png" alt="RIPPS2: Rip it, build 117"></p>

## Rip it: RIPPS2 v1.1.7 beta (build 117)

**[Download RIPPS2.elf](https://github.com/akilluminati47/RIPPS2/releases/download/v1.1.7-beta/RIPPS2.elf)** (one file, 2,698 KB) and put it in place of your old one. Your settings stay where they were. **[RIPPS2-languages.zip](https://github.com/akilluminati47/RIPPS2/releases/download/v1.1.7-beta/RIPPS2-languages.zip)** puts RIPPS2 in your language: every release carries the language pack, and this one has build 117's new words in all 33 languages. The **[theme pack](https://github.com/akilluminati47/RIPPS2-themes/releases/latest)** is edition 117: it adds the `flowtilt` key and writes down the sidebar's keys.

Builds 116 and 117 come together: BOOT LOCK through the boot loader your console really starts, drive pages that show their games on Manual, the sidebar's keys the same on every theme, music that keeps playing on an SD2PSX, and RIPSHOT on MMCE.

### BOOT LOCK
- **FreeMcBoot and OSDMenu, not only PS2BBL.** BOOT LOCK finds the boot loader on your memory cards and writes its own config: FMCB's `LK_Auto_E1` (FREEMCB.CNF, or FMCB_CFG.CNF for 1.8), PS2BBL's `LK_AUTO_E1`, and for OSDMenu, RIPPS2 as the first item in its menu (OSDMenu starts nothing by itself). Turning it off puts back what your loader started before.
- **A game's EXIT comes back through your boot loader** (issue #3, thanks DarkNerdShawny): with BOOT LOCK on and Settings > General > IGR Path empty, EXIT goes to the browser, which starts your loader, which starts RIPPS2. BOOT LOCK no longer fills the IGR Path with RIPPS2's own ELF (that straight load after a game was the black screen).
- **Clear messages**: which configs were set, a loader with nothing to change, a write-protected card, and a loader BOOT LOCK cannot set.

### Drives on Manual
- **A drive's page shows its games before the drive starts**: BDM Games, HDD Games, MMCE Games and the rest on Manual show their part of All Games' list (with Fast Boot, from the first frame). SELECT, Refresh or Auto brings the art.
- **X on a game from a waiting drive starts that drive and launches the game**: no more "HDD not connected" or a wait that never ends.

<p align="center">
<img src="https://raw.githubusercontent.com/akilluminati47/RIPPS2/v1.1.7-beta/media/b117/new-01-boot-lock.jpg" width="48%" alt="BOOT LOCK's message after putting RIPPS2 first in OSDMenu's menu">
<img src="https://raw.githubusercontent.com/akilluminati47/RIPPS2/v1.1.7-beta/media/b117/new-04-ripdisc-flush.jpg" width="48%" alt="Launch Disc: the RIPDISC box starting right at the sidebar's edge">
</p>

### The sidebar, on every theme
- **One set of keys** with the categories as the sidebar (Layout > Category Layout > Sidebar), themes made for OPL included: **Circle** opens the sidebar on every page, **Left** does on a list, **Right** never changes the source. **L1 / R1 are the theme's own again**: a list turns whole pages like OPL, RIPFLOW walks its covers.
- **RIPFLOW and RIPGRID** walk their covers with Left / Right and go round from the first to the last; Left never opens the sidebar there, Circle does.
- **RIPFLOW's case tilt**: Up / Down or the left stick tip the centre case instead of changing the source (the sources are in the sidebar). Theme key `flowtilt`.
- **Launch Disc** ignores L1 / R1; **Memory Files** steps its orb formations with them. The RIPDISC and theme boxes start flush with the sidebar's bar, and the sidebar sits on top of everything.

<p align="center">
<img src="https://raw.githubusercontent.com/akilluminati47/RIPPS2/v1.1.7-beta/media/b117/new-03-ripgrid-drawer.jpg" width="48%" alt="RIPGRID with Circle's STORAGE drawer open over the covers">
<img src="https://raw.githubusercontent.com/akilluminati47/RIPPS2/v1.1.7-beta/media/b117/new-02-ripflow-tilt.jpg" width="48%" alt="RIPFLOW: the centre case tipped back with Up held">
</p>

### Music and sounds
- **Music keeps playing on an SD2PSX.** A missing file looked up anywhere on the card (a cover, a settings check) broke the other open files, so `.wav` and `.mp3` music stopped after a message box or a few menu changes. They now read like the Ogg music does, cached and opened again when the card drops them, loop included.
- **Menu sounds load whole**: a short read is read again and checked, so no more half-loaded sounds playing strangely. **BIOS Music rip** holds the background reads while it writes, so the rip and the music never race.

### RIPSHOT on MMCE
- Games from an SD2PSX or another MMCE device keep their roll on the SD (MEDIA/RIPSHOT), so the in-game screenshot works there instead of "not for this game". Games on the APA HDD still say that: its roll needs a partition of its own, coming in a later build.

### Thanks
Thanks to ripto, nuno6573, zackcage6, eliminator1403, FifthFox, Mr.sus.60 and lukeatmynose for the reports that got us here, and to DarkNerdShawny for issue #3. Special thanks to all the YouTube love as well: glad to help however you reach me.

The full list is in the [changelog](https://github.com/akilluminati47/RIPPS2/blob/main/CHANGELOG.md).
