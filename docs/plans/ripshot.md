# RIPSHOT: screenshots from the in-game menu (handoff plan)

Planned with the user 2026-10-19 and 10-20; built as build 108 (10/20, branch b108, patch 0108; steps 0-8 below).
Build N = patch N. Everything the player reads is written out below, word for word;
change wording here first, then in code. No em dashes anywhere (house rule).

## The user's decisions

- The screenshot is **the exact frame on screen when the in-game menu opens**. No "let the game run a few frames"
  (some games open their own pause screen from the combo's START).
- After choosing where it goes (ART, MEDIA or BOTH) the menu **fades off**, the frame shows as the preview with
  **KEEP / DELETE**, and it is saved then and there.
- **6 shots per game.** Leaving the game empties nothing by itself; developing a game's shots frees its roll, so a
  player can shoot, leave, come back and shoot again, over and over.
- **ART keeps numbering:** `_SCR`, `_SCR2`, `_SCR3`... and a new theme key, **`SCRn`**, shows them all.
- **ART copies are not full size; MEDIA copies are.** ART: OPL Manager's screenshot size, **250 x 188, 8-bit
  palette PNG** (the size and depth of the `_SCR` art already on the user's drives). MEDIA: **full resolution, 8-bit
  palette PNG**. No more than 8-bit colour anywhere.
- Menu order: **RESUME, EXIT GAME, SCREENSHOT, ACHIEVEMENTS, POWER OFF** (POWER OFF stays last).
- **In-Game Menu and RIPSHOT are On by default.** **Develop Shots defaults to Manual**, Auto is the second choice.
- **Every option of these rows has its own hint**, saying what that choice does.
- **Short words everywhere.**
- Developing never slows the boot (the user's worry): Manual does nothing on its own, Auto works in the background
  after the game list is up.
- **The in-game menu is silent, and RESUME gives back the exact frame** (the user, 10/20: "eliminate skipping or loop
  bugs or desync"). The SPU2 is hushed when the menu opens (both cores' master volumes 0, every voice's pitch 0 so it
  holds its place) and woken on RESUME; the pixels under the panel are written back before the game goes on (from
  the roll's hold, so only for games with a roll; without one the game's next frame draws over the panel).
- **Roll limit: 2000 rolls a drive**, the year the PS2 came out (the user: "the number/year PS2 released"). It is one
  constant, `RIPSHOT_ROLLS_MAX`; if 2000 was not what was meant, change it there. The drive's free space usually
  decides first (each waiting roll holds about 4 MB).

## What the player sees

### Settings > General > IN-GAME MENU (a button, like Hints and Glyphs, opening its own page)

| Row | Choices (default first) | Hint for each choice |
|---|---|---|
| In-Game Menu | **On**, Off | On: "L1+L2+R1+R2+SELECT+START pauses the game: resume, exit, take a screenshot, check achievements or power off." Off: "The combo leaves the game at once, as before." |
| RIPSHOT | **On**, Off | On: "Screenshots from the in-game menu, to ART for your themes or to MEDIA. 6 per game; each game with shots waiting holds 4 MB." Off: "No SCREENSHOT in the in-game menu, and no space kept for it." |
| Develop Shots | **Manual**, Auto | Manual: "Shots wait on each game's roll in Memory Files (MEDIA/RIPSHOT) until you develop them. Nothing runs on its own." Auto: "Shots turn into PNGs by themselves once you are back in RIPPS2, in the background while you browse." |

RIPSHOT and Develop Shots grey out while In-Game Menu is Off; Develop Shots greys out while RIPSHOT is Off.
The General page's button: "In-Game Menu" with hint "The in-game menu, RIPSHOT and how shots are developed."

### In the game (ee_core panel: 24 characters a line, upper case ASCII, English only)

Menu, cursor on SCREENSHOT:
```
RIPPS2        SLUS_209.46
  RESUME
  EXIT GAME
> SCREENSHOT
  ACHIEVEMENTS
  POWER OFF
-------------------------
SAVE THIS FRAME
6 OF 6 LEFT
X SELECT   O RESUME
```
SCREENSHOT's info lines in other states:
- the roll is full: `ROLL FULL` / `DEVELOP IN MEMORY FILES`
- no room for a roll: `DRIVE FULL`
- a source RIPSHOT cannot write to (disc, Neutrino, HTTP): `NOT FOR THIS GAME`
- RIPSHOT Off: the item is not in the list.

X on SCREENSHOT: the item list becomes the three paths; each shows name, size, place and what is left:
```
> ART                      ART
  MEDIA                    SLUS_209.46_SCR3.PNG
  BOTH                     250X188  ~20 KB
                           USB: ART
                           5 LEFT  12 GB FREE
X SAVE   O BACK

  MEDIA                    BOTH
  SHOT 03.PNG              SCR3 + SHOT 03
  640X448  ~150 KB         ~170 KB
  USB: MEDIA/AQUA TEEN H   USB: ART + MEDIA
  5 LEFT  12 GB FREE       5 LEFT  12 GB FREE
```
- `~` because the 8-bit PNG's size is only known when it is developed.
- `FREE` only where the drive can say it (the APA HDD: PFS reports free zones). Otherwise just `5 LEFT`.
- The place names the drive: USB, HDD, MX4SIO, ILINK, MMCE, SMB. Long folder names cut to the line.
- `SHOT 03` and `SCR3` are the next free names, worked out by RIPPS2 at launch (existing ART plus the roll's own
  ART shots), so what the menu says is what the file will be called.

X SAVE: the menu fades off over the frame (a few steps), the frame is written to the roll while it fades, then a
slim strip at the bottom:
```
X KEEP   O DELETE
```
While writing on a slow drive (USB, MMCE, SMB) the strip first reads `SAVING`. Then KEEP: `KEPT  4 LEFT`, DELETE:
`DELETED  5 LEFT`, and back to the menu.

### Back in RIPPS2 (RIPPS2's own words, translated into the 33 languages)

- Manual, at startup when any roll has shots: toast `3 SHOTS ON THE ROLL` (`1 SHOT ON THE ROLL`).
- Auto, once the game list is up: toast `DEVELOPING 2 OF 3`, then `3 SHOTS SAVED`; a shot that could not be
  written: `1 NOT SAVED: DRIVE FULL`. Launching a game stops it; the rest are developed next time.

### Memory Files: the rolls (opening `MEDIA/RIPSHOT`)

```
RIPSHOT                    3 ROLLS
> AQUA TEEN HUNGER FORCE   4 SHOTS
  BURNOUT 3                6 SHOTS
  KATAMARI DAMACY          1 SHOT
X OPEN   △ DEVELOP   O BACK
```
Inside a roll:
```
AQUA TEEN HUNGER FORCE     4 OF 6
> SHOT 1                   ART
  SHOT 2                   MEDIA
  SHOT 3                   BOTH
  SHOT 4                   ART
X VIEW   △ ACTIONS   O BACK
```
- X VIEW: the shot full screen, straight from the roll (a 16-bit texture), with `△ ACTIONS   O BACK`.
- △ ACTIONS: `DEVELOP`, `DEVELOP ALL`, `DELETE` ("Delete this shot?" asks first).
- Developing shows `DEVELOPING 2 OF 4` and ends `4 SHOTS SAVED`; the roll goes when it is empty.
- The blank roll and empty rolls never show.

### The MEDIA and AUDIO README.txt

MEDIA's README gains: "RIPSHOT: shots you take in the in-game menu wait in MEDIA/RIPSHOT, one roll per game,
until they are developed (Settings > General > In-Game Menu > Develop Shots). Developed shots land in
MEDIA/<game>/SHOT 01.png at full size, or as the game's ART/<ID>_SCR<n>.png for themes."

## How it works

### Rolls on the drive

- One file per game: `<drive top>MEDIA/RIPSHOT/<ID>.ROLL`, about 4.3 MB: a 512-byte header, then 6 slots of
  512 + 640 x 512 x 2 bytes (a header and up to a 640 x 512 frame at 16 bits, RGB555), then the **hold** area: the
  frame pixels under the panel (up to 320 x 232 at 32 bits) and under the KEEP strip (up to 640 x 24 at 32 bits), in
  the frame's own format so they go back exactly.
- **The blank roll:** `MEDIA/RIPSHOT/BLANK.ROLL`, one per drive, made in the background whenever RIPPS2 is idle and
  there is none (space reserved, not written: lseek past the end and one byte, so even a USB stick takes a moment).
  At launch a game without a roll gets the blank renamed to `<ID>.ROLL`, which is instant everywhere, so RIPSHOT adds
  nothing to launch time. A game with a roll uses its own. No blank and no room for one: `DRIVE FULL` in game.
- Rolls a drive: at most `RIPSHOT_ROLLS_MAX` (2000).
- A slot header: magic `RIPSHOT1`, state (empty / kept), path (ART / MEDIA / BOTH), the game ID and title, the
  ART and MEDIA names the menu showed, width, height, the frame's pixel format and field / frame flag.
- Returning to RIPPS2 removes rolls with no kept shot (an unused rename) and makes a new blank.

### At launch (RIPPS2)

For OPL-core launches from **USB, the exFAT HDD, MX4SIO, iLink (BDM), the APA HDD, MMCE and SMB**, with RIPSHOT
and In-Game Menu on: find or rename the roll; hand the in-game driver what it needs to write it, the way VMCs are
handed over today (BDM: the file's sector fragments; APA HDD: its PFS block map, as mcemu's vmcSpec; MMCE: the file
opened, its handle kept; SMB: its path); and pass in the ee_core config the next names (SCR n, SHOT nn), the title
(trimmed), the drive's short name, the kept count and the free space where known. Disc, Neutrino and HTTP launches:
no roll, the item says `NOT FOR THIS GAME`. (UDPBD rides the BDM path: check it.)

### In the game (ee_core, `ee_core/src/igrmenu.c` and new code)

1. The combo stops the game (as now). With RIPSHOT on, before anything is drawn, the frame pixels the panel will
   cover go to the roll's hold area: read from GS memory (a GS-to-EE image transfer: BITBLTBUF with the shown frame's
   base, width and format from GSM's records, TRXREG, TRXPOS, TRXDIR = 1, read through the VIF1 FIFO with BUSDIR
   reversed), a few KB at a time, sent to the IOP. **OPL's IGS (ee_core igs_api.c) is GPL-3: do not copy it**; write
   it fresh from the GS manual and ORBIT's AFL neutrino-igr. About a quarter of a second on a USB stick.
2. The menu draws as now (five items).
3. SAVE: the hold area is read back and the panel fades off over a few steps (each step blends the panel's colours
   into the restored pixels, line by line). While it fades, the whole frame is read from GS memory and written into
   the next slot (converted to RGB555; a half-height field frame is stored as it is, with its flag), then its header.
4. The KEEP strip's pixels go to the hold area, the strip draws; KEEP marks the slot kept, DELETE marks it empty;
   the strip's pixels go back and the menu returns.
5. The write path (changed 10/20, step 2): NOT an IGR RPC call. While the game is only paused ee_core cannot use
   SIF RPC (the game owns the SIF command table, so the reply lands in the game's handlers; ee_core's RPC only
   works at an IOP reset and on the way out). So, as RetroAchievements already does, plain SIF DMA
   (`modules/iopcore/common/ripshot_io.h`): at every IOP reset, while ee_core still drives the SIF, one IGR RPC
   call (fno 2) gives CDVDMAN the EE address of ee_core's ack and gets back the IOP address of CDVDMAN's request
   box (`ripshot_iop.c`, a thread that looks every 100 ms, every 2 ms between BEGIN and END). In the menu ee_core
   DMAs requests (BEGIN: an 8 KB IOP buffer for the session, WRITE, READ, END) and the thread answers by DMA.
   Each device serves `DeviceRollBytes` / `DeviceRollIo`: `device-bdm.c` walks the roll's fragments
   (`fragfile[1]`, handed over like the ISO's), `device-hdd.c` the ATA write over the block map, `device-mmce.c`
   mmce_write_offset / read_offset, `device-smb.c` WriteAndX (HDD, MMCE, SMB still stubs).
6. Room: ee_core has about 11 KB of stack room (build 103). The transfer buffer lives on the IGR thread's stack
   (4 to 8 KB) and is reused; keep the new code small (gc-sections is on).

### Developing (RIPPS2)

- Read a kept slot; MEDIA: full size; ART: shrink to 250 x 188 (box filter); field frames line-doubled.
- Quantize to 256 colours (median cut on a 15-bit histogram, refined once; no dither: what `png8.py` does, in C)
  and write an 8-bit palette PNG with libpng (already in the ELF: ripps2iconrip.c, ripps2art.c write PNGs).
- ART: `ART/<ID>_SCR<n>.png`, n the next free when developed. MEDIA: `MEDIA/<title>/SHOT <nn>.png`, next free.
- Mark the slot empty; remove the roll when it has none kept.
- **Manual:** from the roll pages in Memory Files. **Auto:** one job at a time on the IO worker, at the lowest
  priority, starting once the game list has loaded; stops for a launch.

### The `SCRn` theme key

- A GameImage with `pattern=SCRn` shows the game's `_SCR`, `_SCR2`, `_SCR3`... in turn, crossfading every 5 s, as a
  slide does. A second `SCRn` box starts one shot later, so two boxes never show the same one.
- RIPPS2, RIPGRID and RIPFLOW (their layouts in `elf/patches`) and Adapt / Adapt Rx (`RIPPS2-themes`
  `tools/gen_adapt_family.py`) switch their screenshot boxes to it. THEME_KEYS.md, the engine reference, the key
  glossary and `tools/check_theme.py` learn it together (RIPPS2-themes AGENTS.md rule 8).

### Settings and defaults

- Keys: `ripps2_igr_menu` (exists), `ripps2_ripshot`, `ripps2_ripshot_develop` (0 Manual, 1 Auto).
- **In-Game Menu On by default.** Configs saved by older builds already hold `ripps2_igr_menu=0`, so a new default
  alone would not reach them: switch it on once for configs from before this build (a one-time key such as
  `ripps2_igr_menu_v`). The build 87 note "off until consoles have shown it safe" is retired: say so in the
  changelog.
- **Per-choice hints:** the dialogs show one hint per row today (`dia.c`, `hintId`). Add a hint for each value of an
  enum row (e.g. `diaSetEnumHints(dialog, id, hints[])`), the hint box following the current value.
- New RIPPS2 words go through `_t` and the language template (`elf/lang/ripps2lang.py extract`), then all 33
  languages; the settings labels and hints as `lng_tmpl/_base.yml` labels where the dialogs need ids.

## Build order

0. [x] **Fix the PCSX2 lab's game-launch hang** (10/20, patch 108). The cause: ee_core reboots the IOP with UDNL
   reading the IOPRP image from imgdrv's device, named `host`, and PCSX2 serves every `host*:` open from its own
   host file system (IopBios.cpp `is_host`, HostFs on or off), so the log ended on `file 'host0:' can't open`. The
   device is `iprp` now (same length, the reset command is unchanged). Lab: Aqua Teen Hunger Force from the reel
   HDD reaches its title screen. The in-game menu needs the `RIPPS2_IGR_TEST=1` build in PCSX2 (no data
   breakpoints, so GSM never sees DISPFB and the menu leaves at once); with it the menu opens over the game and
   POWER OFF's second press turns the console off. Its first frame drew the panel's text garbled once (later frames
   clean): look again in step 4.
1. [x] GS readback in ee_core, with a host test of the pixel paths (16, 24, 32-bit frames to RGB555; field frames).
   10/20: `ee_core/src/ripshot.c`: rsFrame (the shown frame, now also the menu's igrmFindFrame), rsRead (local ->
   host after ps2sdk's AFL ee/debug screenshot.c: FINISH masked in IMR and the game's flag kept, FDR + BUSDIR, D1 to
   memory, bounded waits), rsToRgb555 (roll pixels = GS CT16 layout, A set), RS_READ_W (16-pixel widths keep
   every transfer whole quadwords). Host test test_ripps2_build108.py. rsRead has no caller yet: first proof is
   step 4's hold / restore. Room: a 640 CT32 line is 2.5 KB and the IGR stack is 4 KB (read half lines into the
   menu's packet buffer, or grow IGR_STACK_SIZE).
2. [ ] The roll read / write for BDM first (USB in the lab's exFAT HDD image is BDM too), then APA HDD, MMCE, SMB.
   10/20: BDM done (mailbox design in "How it works" 5; host test walks a three-fragment roll on a fake drive; CI
   green; ee_core stack room now 0x2940). First lab proof needs step 3's BDM handover. HDD, MMCE, SMB: stubs.
3. [ ] Rolls: blank roll, rename at launch, the handover per device, the ee_core config fields, the 2000 cap.
   10/20, BDM done (`src/ripps2shot.c`, layout `modules/iopcore/common/ripshot_roll.h`: 4 KB pieces, 4,321,280
   bytes): the background job makes MEDIA/RIPSHOT/BLANK.ROLL on each started drive (seek past the end and one
   byte) and turns rolls with nothing kept back into the blank; the launch finds the game's roll, else renames the
   blank, else makes one (DRIVE FULL when it cannot or at RS_ROLLS_MAX), hands its fragments over as fragfile[1]
   and fills ee_core's Ripshot, RipshotKept, RipshotScrNext, RipshotShotNext, RipshotFreeMB (-1 on BDM),
   RipshotDrive, RipshotTitle. Lab (IGR test build, ripps2-rip.raw, SCPS_150.13): the menu said ROLL OK; on the PC
   the roll reads RIPROLL1 / SCPS_150.13, six zero slots, and its hold is the frame under the panel. The reel HDD
   has 4.25 MB free (under a roll): DRIVE FULL there is expected. APA HDD, MMCE, SMB: with their step 2.
   Also done early (step 4): the hold is saved for every RIPSHOT game and written back on RESUME, and the menu is
   silent (see the user's decisions). ee_core stack room after it: 0x1FC0 (the IGR stack is 4 KB of it).
4. [x] The in-game screens: the item, the path step, hold / restore, the fade, KEEP / DELETE, the counts, the full and
   drive-full states. 10/20, lab-checked on a REAL frame (RIPPCSX2 2's data breakpoint, normal build, POINIES POIN on
   ripps2-rip.raw): SCREENSHOT third, SAVE THIS FRAME / n OF 6 LEFT, the path pages (names, sizes, place, left), SAVE
   fades the panel off in three passes (two blends, then the hold exactly), the frame goes to the first free slot,
   KEEP writes the slot header, the menu returns, RESUME gives the frame back; on the PC the slot reads as the frame
   the menu opened on with no menu in it. Found and fixed on the way:
   - GSM's data breakpoint trapped the menu's own GS stores (the readback's CSR and BUSDIR): the menu saves BPC,
     switches it off (BED) for its whole run and puts it back on the way out. A console would trap the same way.
   - A game may write DISPLAY DH past the TV's raster (POINIES POIN: 959 in NTSC FRAME mode): the shown height stops
     at 480 (NTSC) or 576 (PAL, DY >= 64) lines, or the panel sat off screen and the shot read below the picture.
   - ee_core ran out of room: the menu's 4 KB thread stack and its font (igrmfont.h) now sit after the modules
     (config->IgrStack / IgrFont, src/system.c), below 0xD0000 like LEFT TO HUNT; without that room the menu is off
     for the game. rsLinkIop's RPC buffers are static (the first IOP reset runs on ee_core's main stack, 3 KB floor).
     ee_core stack room after it: 0xC80. CI now uploads ee_core.map with the symbols, also when the link fails.
   - The panel is 126 units tall (five items); the hold holds 320 x 256, the strip 320 x 32 (roll 4,329,472 bytes; a
     shorter roll with nothing kept is made again at launch).
   - Not done: the SAVING strip (the clean frame stays up while it writes, about a second).
5. [x] Developing: quantizer, PNG writer, names; the Memory Files roll pages and viewer; Auto in the background; toasts.
   10/20, lab: Manual (the toast, the roll pages, VIEW, ACTIONS, DEVELOP to an 8-bit PNG) and Auto (DEVELOPING 1 OF 2,
   2 SHOTS SAVED, the roll back to the blank). Developed names are the ones the menu showed while still free.
6. [x] Settings page with per-choice hints, defaults and the one-time switch; translations (27 strings and 5 labels in
   the 32 language files). 10/20, lab: the General page's In-Game Menu button and hint, the page's three rows. Found
   there: a choice past the first never showed its hint (an enum row leaves intvalue.max at 0: the choices are counted
   now) and the hint comes in again when the choice changes; disabled rows looked like the rest (dialogs drew them in
   the same colour): a row that cannot be changed now reads at half strength, its label too, on every settings page.
7. [x] `SCRn` in the engine and the themes. Boxes (RIPGRID, RIPFLOW, Adapt): each shows its own shot, all crossfade
   every 6 s. Slides (RIPPS2's info page, which is `elf/theme/conf_theme.cfg`: build.sh writes it over RiptOPL's
   conf_theme_OPL.cfg): an SCRn slide shows the next shot each round, a slide shown this round asking for its next one
   early so the show fades into it. Lab: RIPGRID's boxes swap (pixel diffs 0 / 12), RIPPS2's slideshow runs _SCR,
   _SCR2, _SCR3, _SCR... Found there: _SCR2 can load before _SCR; the shots are now found strictly in order (a probe
   asks for the first unknown one) and only a shot known to be there is shown, else the show probed past the last.
   RIPPS2-themes edition 108: THEME_KEYS.md, the glossary, the checker, Adapt and Adapt Rx.
8. [x] Lab: shots from POINIES POIN to ripps2-rip.raw (ART, three of them), developed by Auto (and by hand in step 5),
   read back: ART 250 x 188 and MEDIA 640 x 480, 8-bit palette PNGs. MEDIA's README.txt explains RIPSHOT (written on
   every drive RIPSHOT uses). Then the console test list below for testers (tools/discord/notes/build108.md).
   Still open: the SAVING strip; APA HDD, MMCE and SMB rolls (NOT FOR THIS GAME there).

## Console test list (for the release post)

- Take shots in a game on USB, the exFAT HDD, the APA HDD and an MMCE. Is each picture the frame you paused on, with
  no menu in it?
- A game whose pause menu opens with START: does the shot catch that pause screen? (If so: press START last.)
- 480p, 1080i and PAL games: right size, right colours, nothing torn?
- Fill a roll (6). Does the menu say ROLL FULL? Develop by hand in Memory Files, play again: 6 left again?
- Auto: back in RIPPS2, do the shots develop while you browse, with the game list usable?
- ART shots: does the info page's slideshow show SCR3 and on?
- How long does the menu take to open with RIPSHOT on, on USB and on MMCE?

## Risks and open questions

- Reading GS memory back while a game is paused, across every frame format and display mode GSM sees.
- The ee_core room.
- Write speed on MMCE and SMB (the SAVING strip covers it).
- Whether the combo's START reaches a game before the pause (see the test list).
- `RIPSHOT_ROLLS_MAX` = 2000 is the reading of "the number/year PS2 released"; confirm with the user if in doubt.
