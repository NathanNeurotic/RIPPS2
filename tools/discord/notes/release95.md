## Kill it: RIPPS2 build 95 (alpha)

**Hear it, fix it.** A stability build: the sound effects rebuilt so they never go quiet in waves or bring old sounds back, the boot no longer reading a ripped boot sound behind the drives' back, and the bug that broke RIPFLOW (and more) from build 93 found and fixed.

**[Download RIPPS2.elf](https://github.com/akilluminati47/RIPPS2/releases/download/v0.0.95-alpha/RIPPS2.elf)**, and the **[theme pack](https://github.com/akilluminati47/RIPPS2-themes/releases/latest)** if you like (unchanged since build 94).

### Sound effects, rebuilt
- **A held cursor no longer goes quiet in waves, and old sounds no longer come back after.** RIPPS2 now knows when every voice has finished and only plays on one that has. In the lab a held cursor went from bursts of six ticks and 0.8 s of silence to a clean tick every 60 ms.
- **No sounds are built in.** They come from your `AUDIO` folder: **Audio Settings > BIOS Sounds > Rip** makes your own console's, and RIPPS2 Audio Studio makes any others. **STATUS > SOUNDS** says how many are loaded and where from, and can rip them for you.
- **Safer at boot:** every sound file is read by the worker that reads the drives (a ripped `boot.adp` used to be read at boot alongside it, which can hang a memory card), and each file is checked before use, so a bad one is skipped instead of stopping anything.
- **Ripped sounds end at silence** (rip again for the new endings), and **Memory Files plays `.adp` files** so you can check them.

### Fixed
- **RIPFLOW works again.** The video player added in build 93 carried its own copies of the C library's string functions, and they replaced the real ones for all of RIPPS2. That broke RIPFLOW's theme, could hang build 93 at boot, and threw off a count on the console. It cannot happen again: the build now fails if it would.
- **MX4SIO** is identified with those same functions, so it may be back too: tell us.
- **JPG pictures open whole** (no more top quarter only), and **game art can be JPG**: old OPL art packs now show their covers on every theme.

### In-Game Menu
- Now marked **experimental**: some games skip their sound or stop if paused in a cutscene. Off (the default) the combo is OPL's trusted IGR, untouched.

Full list: [CHANGELOG.md](https://github.com/akilluminati47/RIPPS2/blob/main/CHANGELOG.md). Alpha: keep your usual loader close by.
