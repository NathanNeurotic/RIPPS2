# Build 110 is RIPPS2 v1.1.0 beta: every source shows its games the moment it answers, and your settings can live on any drive: the internal HDD, USB, MX4SIO, iLink or MMCE. The lab has shown all it can; the test list is what only a real PS2 can tell us.

## Get it
- [Download the latest RIPPS2.elf](https://github.com/akilluminati47/RIPPS2/releases/latest/download/RIPPS2.elf) (this link always gets the newest build), [RIPPS2-languages.zip](https://github.com/akilluminati47/RIPPS2/releases/latest/download/RIPPS2-languages.zip) for your language, and [the theme pack](https://github.com/akilluminati47/RIPPS2-themes/releases/latest/download/RIPPS2-themes.zip) (edition 108)
- [The psx-place thread](https://www.psx-place.com/threads/ripps2-a-ps2-front-end-in-one-elf-launch-disc-storage-memory-files.51316/)

## Every source lists at once
- **MMCE, USB, the exFAT HDD, MX4SIO, iLink and SMB** keep their last game list (`RIPPS2.LST`, beside CD and DVD): the games show the moment the drive answers, then the drive is read again the next time you are idle on Storage and the list follows whatever changed.
- **The APA HDD's list cache is on** (switched on once for older settings) and checked against the drive the next time you are idle, so a game installed from a PC still appears.
- **MX4SIO pauses for the pads while it is read**, as MMCE does.

## Save Settings To, every drive
- **Settings > General > Save Settings To:** Memory Card, Internal HDD, **USB Drive, MX4SIO, iLink, MMCE** or Custom Path, each with its own hint. A drive is saved by its type, so at boot only that drive's driver loads. A drive that is not connected says so and nothing changes.
- **Build 109's hotfix is in:** Internal HDD is saved by the drive's type too. If you chose it on the first v1.0.9 ELF, choose it again and Save Changes.

## Everything else
- **The info page shows the size** of every game you reach with the d-pad (it read 0 MiB after the first).
- Build 109: the MMCE card list, page titles off their line. Build 108: RIPSHOT, the silent in-game menu, SCRn.
- The new words in all 33 languages.

## Test list
- **Boot with your biggest library** on MMCE, USB, MX4SIO or SMB: on the second boot, do the games show at once? How many seconds until you can move?
- **Add or remove a game on your PC**, then boot: the old list first, then does it catch up by itself after a few idle seconds on Storage?
- **MX4SIO while it reads:** can you move and open menus while the list fills?
- **APA HDD:** install a game with your PC tools, boot. Does it appear after a few idle seconds, without pressing Refresh?
- **Save Settings To > USB Drive** (then MX4SIO, iLink, MMCE if you have them): change a setting, Save Changes, power off, take the memory cards out, boot. Are your settings back?
- **Internal HDD** the same way, on exFAT and on APA.
- **A USB stick plugged in with Internal HDD chosen:** do the settings still come from the HDD?
- **Info page:** press Left / Right through your games. Does every one show its size?
- **RIPSHOT on a console:** a game on USB, the exFAT HDD, MX4SIO or iLink. Is the developed shot the frame you paused on, in 480p, 1080i and PAL games too?
- **The silent menu:** any skip, loop, crackle or desync after RESUME?
- **Menu music after RIPDISC or a game:** does the BGM come back every time?
- **Power Off in the in-game menu:** does the second press turn the console off cleanly?

## Report
Post in the [psx-place thread](https://www.psx-place.com/threads/ripps2-a-ps2-front-end-in-one-elf-launch-disc-storage-memory-files.51316/) or here with your **console model**, your drives (MMCE or MX4SIO model and firmware too), how many games, and a **photo** of anything odd.
