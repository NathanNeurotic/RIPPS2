## Kill it: RIPPS2 build 99 (alpha)

**Four builds since 95.** The music gets a road of its own (and half of all music, which never played, plays now), Memory Files grows into a real file manager with games, 3D save icons and its own icon on your card, the Grid and Flow catch up with HD screens, and RIPPS2 calls your drives by what they are.

**[Download RIPPS2.elf](https://github.com/akilluminati47/RIPPS2/releases/download/v0.0.99-alpha/RIPPS2.elf)**, and the **[theme pack](https://github.com/akilluminati47/RIPPS2-themes/releases/latest)** if you like (Adapt and Adapt Rx, each with its full key glossary; RIPGRID and RIPFLOW are built in).

### Music
- **Half of all music never played.** The PS2's Vorbis library refuses an Ogg stream whose serial number has its top bit set, and encoders pick that number at random. RIPPS2 fixes it as it reads, and RIPPS2 Audio Studio no longer writes such files.
- **The music no longer waits in line for the drive:** it is read into memory in big pieces (about 16 seconds of music per request instead of a request every few hundred milliseconds), so loading covers cannot starve it. In the lab a pilot tone ran 90 seconds through a button storm without a dropout.

### Memory Files
- **Both memory cards stay after START DRIVES**, named MEMORY CARD 0 and MEMORY CARD 1. Paste asks YES, REPLACE IT / NO, KEEP IT / YES TO ALL; a full card says so before writing; deletes are checked and explained.
- **Games start right here:** ISO or ZSO in a drive's CD or DVD folder, as from Storage (your Loader Core, VMCs, cheats), and CUE or BIN in `EMBER/games/<game>/` with Ember.
- **3D save icons** open textured and animated; **RIP 3D ICON** writes OBJ, MTL and PNG for a PC. **RIPPS2's own card folder** now has an icon (the dead elf's hat ringing its bell) instead of showing as corrupted data.
- Rest on a file for its details, hold to scroll, the text editor keeps files exactly as they were, and the picture viewer stays sharp zoomed in.

### Grid and Flow
- **RIPGRID's 720p freeze is fixed** (a pad command waited on a controller still starting up). Lists always show a full page.
- **Widescreen Grid layout** for 720p, 1080i and widescreen; L2 / R2 turn a whole page; Vignette Other Covers Off / Weak / Full; Background art blur; RIPFLOW tilts and flips like RIPGRID.
- The game's background fades in right behind its cover; the info page fades in as one again.

### Settings and names
- Back lands on the row you came from, settings read in one plain face on every theme, auto start can be Last Used, page buttons L1 / R1 or L2 / R2.
- **Drives are named by what they are:** USB, HDD, iLINK, MX4SIO, not "USB" for every `mass0:`. **STATUS > DRIVES** lists them and what became of MX4SIO.
- **From RiptOPL:** PS1 games flash their real disc ID for Pixel FX / RetroGEM (#869), and a slow-spinning iLink drive is waited for at start.

Full list: [CHANGELOG.md](https://github.com/akilluminati47/RIPPS2/blob/main/CHANGELOG.md). Alpha: keep your usual loader close by.
