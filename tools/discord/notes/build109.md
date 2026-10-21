# Build 109 is RIPPS2 v1.0.9 beta: an MMCE library lists at once, your settings can live on the internal HDD, and RIPSHOT (build 108) takes screenshots from the in-game menu. The lab has shown all it can; the test list is what only a real PS2 can tell us.

## Get it
- [Download the latest RIPPS2.elf](https://github.com/akilluminati47/RIPPS2/releases/latest/download/RIPPS2.elf) (this link always gets the newest build), [RIPPS2-languages.zip](https://github.com/akilluminati47/RIPPS2/releases/latest/download/RIPPS2-languages.zip) for your language, and [the theme pack](https://github.com/akilluminati47/RIPPS2-themes/releases/latest/download/RIPPS2-themes.zip) (edition 108: Adapt and Adapt Rx show every screenshot, replace your Adapt folders)
- [The psx-place thread](https://www.psx-place.com/threads/ripps2-a-ps2-front-end-in-one-elf-launch-disc-storage-memory-files.51316/)

## MMCE boots fast (109)
- **A big MMCE library lists at once.** The card keeps RIPPS2's last list of its games (`RIPPS2.LST`, beside CD and DVD): at boot the games show from it straight away, then the card is read again in the background and the list follows whatever changed. 180 games took about 5 minutes on every boot.
- **The pads keep working while the card is read.** MMCE shares its bus with the controllers; the scan now pauses after every game so you can move around while it works.

## Save Settings To (109)
- **Settings > General > Save Settings To:** Memory Card (as before), **Internal HDD** (a RIPPS2 folder on the internal exFAT HDD, else the APA HDD's OPL partition, read first at boot) or Custom Path. Each choice has its own hint; with no internal HDD it says so and changes nothing.
- **Settings pages:** a page's title stands clear of the line under it (it sat on the line and lost its descenders).

## RIPSHOT (108)
- **SCREENSHOT is the in-game menu's third choice** (L1+L2+R1+R2+SELECT+START): the exact frame that was up when the menu opened, no menu in it. **ART** (theme screenshot art), **MEDIA** (full-size PNG) or **BOTH**, then **SAVE**, **KEEP** or **DELETE**.
- 6 shots a game wait on its roll in `MEDIA/RIPSHOT`. **Develop Shots: Manual** develops them from Memory Files, **Auto** in the background once you are back in RIPPS2. For now: games on USB, the exFAT HDD, MX4SIO and iLink.
- **New theme key `SCRn`:** every shot a game has, in turn. The info page, RIPGRID, RIPFLOW, Adapt and Adapt Rx use it.

## Everything else
- **The in-game menu is on by default and silent**: the game's sound holds still while it is open, and RESUME gives back the exact frame. Settings > General > In-Game Menu is its own page; a row another setting switches off reads dimmed.
- The info page no longer blinks when a rescan rebuilds the list, and a shot developed while RIPPS2 runs shows at once.
- The new words in all 33 languages.

## Test list
- **MMCE, a big library (100+ games):** boot twice. On the second boot, do the games show at once? How long until the list stops changing?
- **MMCE while it reads:** on a first boot (or after adding games), can you move, open the START menu and change pages while the list fills?
- **MMCE changes:** add and remove a game on your PC, then boot. Does the list catch up by itself? Does a different card or a card switch show the right games?
- **Save Settings To > Internal HDD on the exFAT HDD:** change a setting, Save Changes, power off, take your memory cards out, boot. Are your settings still there?
- **Internal HDD on an APA HDD:** same test. Does it say SETTINGS SAVED, and do they come back after a power cycle?
- **Settings pages on your TV:** is every page title clear of its line, in 480i and in 480p/720p/1080i?
- **RIPSHOT on a console:** a game on USB, the exFAT HDD, MX4SIO or iLink. Is the developed shot the frame you paused on? How long does the menu take to open?
- **480p, 1080i and PAL games:** shots the right size, nothing torn or shifted?
- **The silent menu:** open and close it in a game with music and speech. Any skip, loop, crackle or desync after RESUME?
- **Menu music after RIPDISC or a game:** does the BGM come back every time? If it goes missing or glitches, tell us what you did just before.
- **Power Off in the in-game menu:** does the second press turn the console off cleanly?

## Report
Post in the [psx-place thread](https://www.psx-place.com/threads/ripps2-a-ps2-front-end-in-one-elf-launch-disc-storage-memory-files.51316/) or here with your **console model**, your drives (MMCE model and firmware too), and a **photo** of anything odd.
