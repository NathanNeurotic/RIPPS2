<p align="center"><img src="https://raw.githubusercontent.com/akilluminati47/RIPPS2/v1.1.0-beta/media/ripps2-test-me.png" alt="RIPPS2: Rip it, build 110"></p>

## Rip it: RIPPS2 v1.1.0 beta (build 110)

**[Download RIPPS2.elf](https://github.com/akilluminati47/RIPPS2/releases/download/v1.1.0-beta/RIPPS2.elf)** (one file, about 3 MB) and put it in place of your old one. Your settings stay where they were. **[RIPPS2-languages.zip](https://github.com/akilluminati47/RIPPS2/releases/download/v1.1.0-beta/RIPPS2-languages.zip)** puts RIPPS2 in your language (copy its `LNG` folder to the top of a USB drive, the HDD's OPL partition or an MMCE card, then Settings > Display Settings > Language). The **[theme pack](https://github.com/akilluminati47/RIPPS2-themes/releases/latest)** is still edition 108; RIPGRID and RIPFLOW are built in.

<p align="center">
<img src="https://raw.githubusercontent.com/akilluminati47/RIPPS2/v1.1.0-beta/media/b110/01-save-settings-usb.jpg" width="48%" alt="Settings > General: Save Settings To on USB Drive, its hint below">
<img src="https://raw.githubusercontent.com/akilluminati47/RIPPS2/v1.1.0-beta/media/b110/02-info-metadata.jpg" width="48%" alt="The info page reached with Right: Burnout 3 with its badges, five stars, genre, developer, release and size">
</p>

### Every source lists at once
- **Every source shows its last list the moment it answers.** Build 109 kept an MMCE card's game list on the card; now MMCE, USB, the internal exFAT HDD, MX4SIO, iLink and SMB all keep `RIPPS2.LST` beside their CD and DVD folders. The drive is read again the next time you are idle on Storage, and the list follows whatever changed. With Write Operations Off no list is written.
- **The APA HDD's own list cache is on** (Cache Game List (HDD APA), switched on once for older settings), and the APA table is read again the next time you are idle, so a game installed from a PC still appears without a refresh.
- **MX4SIO pauses for the pads while it is read**, as MMCE does: both share the controllers' bus.

### Save Settings To, every drive
- **Settings > General > Save Settings To** offers USB Drive, MX4SIO, iLink and MMCE as well as Memory Card, Internal HDD and Custom Path, each with its own hint. A drive is saved by its type (`usb0:/RIPPS2`, `mx4sio0:/RIPPS2`, `ilink0:/RIPPS2`, `mmce0:/RIPPS2`) with its RIPPS2 folder made for it, so at boot only that drive's driver loads. A drive that is not connected says so and nothing changes.
- SMB and UDPBD cannot hold the settings: reaching them needs the settings.

### Info page
- **A game reached with the d-pad on the info page shows its size** (every game after the first read 0 MiB).

### Underneath
- The new words in all 33 languages.

**[Full changelog](https://github.com/akilluminati47/RIPPS2/blob/main/CHANGELOG.md)** | **[Watch the v1.1 reel](https://youtu.be/Q8ZLd6ArV8s)** | **[Talk about it on psx-place](https://www.psx-place.com/threads/ripps2-a-ps2-front-end-in-one-elf-launch-disc-storage-memory-files.51316/)** | [RIPPCSX2](https://github.com/akilluminati47/RIPPCSX2/releases/latest) for seeing a theme in true 720p and 1080i

Beta: keep your usual loader close by, and tell us what breaks in [the psx-place thread](https://www.psx-place.com/threads/ripps2-a-ps2-front-end-in-one-elf-launch-disc-storage-memory-files.51316/) or [an issue](https://github.com/akilluminati47/RIPPS2/issues). This one wants big libraries on real drives above all: how fast does your list show on the second boot, and do settings saved to a USB drive, MX4SIO, iLink or MMCE come back after a power cycle?
