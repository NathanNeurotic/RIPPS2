# RIPPS2 changelog

## Build 109 (beta, v1.0.9-beta), changes since build 108

From testers' reports (10/19-10/20).

### MMCE boots fast
- **A big MMCE library lists at once.** RIPPS2 keeps the card's game list on the card (`RIPPS2.LST`, beside its CD and DVD folders): at boot the games show from it straight away, then the card is read again in the background and the list follows whatever changed. A tester's 180 games took about 5 minutes to list on every boot, with nothing to press until then.
- **The pads keep working while a card is read.** An MMCE card shares its bus (SIO2) with the controllers; the list scan used to hold it from the first game to the last. It now pauses after each entry, and a frame after each game whose disc has to be read, so you can move around while it works.

### Save Settings To
- **Settings > General > Save Settings To:** Memory Card (RIPPS2's own save, as before), **Internal HDD** (a RIPPS2 folder on the internal exFAT HDD, else the APA HDD's OPL partition; the settings are read from there first) or Custom Path (the Custom Settings Path row, which now shows only for this choice). Every choice has its own hint. With no internal HDD it says so and changes nothing.

### Settings pages
- **A page's title stands clear of the line under it.** It sat on the line, which cut its descenders.

### Languages
- The new words read in all 33 languages.

### Hotfix (10/21/2026, still build 109)
- **Internal HDD is saved by the drive's type** (`ata0:/RIPPS2`), not by its mass slot (`mass0:/RIPPS2`). A slot number is only the order the drives came up in, so a USB stick could take it, and at boot an untyped slot made RIPPS2 try USB, MX4SIO, iLink and the HDD in turn (in PCSX2 the MX4SIO step froze the boot). Now only the HDD's own driver loads. If you chose Internal HDD on the first v1.0.9 ELF, choose it once more and Save Changes.

## Build 108 (beta, in v1.0.9-beta), changes since build 107

### RIPSHOT: screenshots from the in-game menu
- **SCREENSHOT is the in-game menu's third choice** (L1+L2+R1+R2+SELECT+START: RESUME, EXIT GAME, SCREENSHOT, ACHIEVEMENTS, POWER OFF). It takes **the exact frame that was on screen when the menu opened**, never a frame after it, and never the menu itself.
- **Pick where it goes:** ART (the game's screenshot art for your themes, at OPL Manager's 250 x 188), MEDIA (full size, in a folder named for the game) or BOTH. Each choice shows the file it will become (`SLUS_209.46_SCR3.PNG`, `SHOT 03.PNG`), its size, the drive and how many shots are left.
- **SAVE fades the menu off over the frame** and writes it then and there; **X KEEP / O DELETE** at the bottom decides, and the menu comes back with the count: `KEPT  4 LEFT`.
- **6 shots a game, on the game's roll.** Shots wait in `MEDIA/RIPSHOT` on the drive the game is on (each game with shots waiting holds about 4 MB; a blank roll is kept ready so a game starts at once) until they are developed. Developing frees the roll, so you can shoot, leave, come back and shoot again. A full roll says `ROLL FULL / DEVELOP IN MEMORY FILES`; a drive without room for a roll says `DRIVE FULL`.
- **Developing** turns a shot into an 8-bit palette PNG: `ART/<ID>_SCR.png`, then `_SCR2`, `_SCR3`... (the next free number, the one the menu showed), or `MEDIA/<game>/SHOT 01.png` at full size.
  - **Manual** (the default): open `MEDIA/RIPSHOT` in Memory Files. Each game's roll lists its shots; **VIEW** shows one full screen straight from the roll, **ACTIONS** develops it, develops them all or deletes it ("Delete this shot?" asks first). At startup a toast says `3 SHOTS ON THE ROLL` when any are waiting.
  - **Auto:** back in RIPPS2, once the game list is up, they develop in the background while you browse (`DEVELOPING 1 OF 2`, then `2 SHOTS SAVED`). Launching a game stops it; the rest go next time.
- **Where it works:** games on USB, the internal exFAT HDD, MX4SIO and iLink. A game on the APA HDD, an MMCE card or SMB, or from a disc, says `NOT FOR THIS GAME` for now.
- MEDIA's README.txt explains RIPSHOT (an older RIPPS2 README there is brought up to date).

### The in-game menu
- **It is silent now, and RESUME gives back the exact frame.** The game's sound stops while the menu is open (every voice held where it was) and starts again on RESUME, so nothing skips, loops or drifts out of sync; for a game with a roll the picture under the panel is put back before the game goes on.
- **On by default.** Build 87 kept it off "until consoles have shown it safe": it is no longer experimental, and a config saved by an older build gets it switched on once.
- **Settings > General > In-Game Menu** is a page of its own: **In-Game Menu** (On, Off), **RIPSHOT** (On, Off: no SCREENSHOT and no roll kept) and **Develop Shots** (Manual, Auto). Every choice has its own hint, which changes as you change the choice; RIPSHOT and Develop Shots grey out when they cannot apply.
- **Every settings page:** a row that cannot be changed now (a setting another one switches off) reads at half strength, its label too. It used to look like the rest and the cursor simply skipped it.
- **Found and fixed in the lab:** a game that sets its picture taller than the TV shows (POINIES POIN) put the panel off screen and the shot below the picture; the menu now stops at the raster's 480 (NTSC) or 576 (PAL) lines. GSM's data breakpoint caught the menu's own GS reads and froze it: the menu switches it off while it is open and back on as it closes.

### The `SCRn` theme key (RIPPS2-themes edition 108)
- **`pattern=SCRn` shows every screenshot a game has**, `_SCR` to `_SCR9`, each for 5 s with a 1 s crossfade. A second `SCRn` box on the page starts one shot later, so two boxes never show the same one; as a slide it shows the next shot each time the show comes round.
- **RIPPS2's info page slideshow, RIPGRID's and RIPFLOW's screenshot boxes, and Adapt and Adapt Rx use it**, so your RIPSHOT ART shows up as soon as it is developed. THEME_KEYS.md, the key glossary and the checker know it.

### Underneath
- **Games launch in PCSX2 with its host filesystem on.** PCSX2 answers every `host` device itself, so the image the game's IOP reboots from could not be found and the launch hung; RIPPS2 names that device `iprp` now.
- The in-game menu's stack and font sit after the game's modules (below 0xD0000, as LEFT TO HUNT's list does), which keeps ee_core inside its room.

### Found while making the reel
- **The info page no longer blinks** when a device rescan rebuilds the game list under it (all its art faded in again and the slideshow started over): it knows a game by its id and title, not by its row.
- **Shots developed while RIPPS2 runs show at once** in a theme's `SCRn` boxes and slides (an earlier "no such art" answer is asked again).
- **A developed PNG is checked on the drive** (its size must be what was written) and written once more if not. Once, an ART PNG came out empty and held its number; an empty file now counts as free and is written over.
- **`SCRn` finds the shots in order**, `_SCR` first, whatever order the reads come back in, and a slide or box shows only a shot known to be there.

### Languages
- RIPSHOT's words, the In-Game Menu page and its hints read in all 33 languages (ART and MEDIA stay as the folders are named). The in-game menu itself stays English.

## Build 107 (beta, v1.0.7-beta), changes since build 106

### Search in Memory Files
- **SEARCH FILES takes MC EXPLOIT INSTALLER's place** in Memory Files' settings grid (START in the browser), with a magnifier for its icon. Type part of a name on the keyboard: every drive the browser lists (memory cards, USB, the exFAT HDD, MX4SIO, iLink, MMCE, the HDD's OPL home) is searched for files and folders whose name holds it, in any case: media, saves, games, ELFs, art.
- **Results open where they are.** The list shows each name with the folder it is in under it; Cross (or Circle, with Circle as confirm) opens the file tree in that folder with the cursor on it, ready to copy, run or rename. L1 / R1 page through the results.
- **It keeps out of the drives' way:** one folder is open at a time (a memory card or MMCE driver never holds two), it goes ten folders deep and stops at 150 results, and the screen shows how many folders it has read. Back stops it and keeps what it found. A drive that is not started is not searched: START DRIVES in the drive list starts the rest.
- The memory card exploit installer launcher is gone (keep your installer ELF in APPS and run it from the browser, as any ELF).

### Fix
- **Build 105's time estimate** failed to build (a function used before it was declared); found by CI, fixed here.

## Build 106 (beta, in v1.0.7-beta), changes since build 105

### POWER OFF from the game
- **The in-game menu's last choice is POWER OFF** (L1+L2+R1+R2+SELECT+START opens the menu, with In-Game Menu on in Settings > General). Like EXIT GAME it asks first: the first press arms it and the panel says "PRESS X AGAIN TO TURN THE PS2 OFF" in red, the second turns the console off, the same way the power button's single press does. Unsaved progress is lost, and it says so.
- A game started from a disc keeps the console's own power button (the disc driver in the BIOS has no power-off call RIPPS2 can make); POWER OFF says so instead of doing nothing.

### The star on the left
- **A starred game's star now sits at the start of its row**, in a column of its own, so every title lines up whether it is starred or not. That is the default on every built-in theme and on Adapt.
- **Settings > Game Sources > Starred Games Star** (under Starred Games Page Start Mode): Theme, Left, Right (after the title, as before) or Hidden. Kept with your settings.
- **A theme's row icon moves out of its way:** with the star on the left, a list's per-game icon (the `decorator`) is drawn at the row's right end, so the two never overlap.

### New theme keys for the games list (RIPPS2-themes has them, in THEME_KEYS.md, the key glossary and the checker)
- `star`: `left` (the default), `right` or `hidden`. The user's setting wins.
- `star_image`: the star's own picture for that list (else the theme's `fav_mark.png`, else RIPPS2's).
- `highlight`: the selected row as `bar` (the PS2-blue bar, the default), `line` (a line under the row) or `none`.
- `decorator_all`: one picture as every row's icon; `decorator_ps2`, `decorator_ps1`, `decorator_app`: one for each kind of row. A game's own icon (`decorator=ICO`) comes first, then its kind's, then the one for all.

## Build 105 (beta, in v1.0.7-beta), changes since build 104

### RIPDISC: your disc, kept
- **Launch Disc offers to rip what is in the drive.** After 4.2 seconds on the page, when the disc can be ripped, a glass panel fades in at the centre: RIPDISC, "add this game to your storage" (or "this media to your files") and SELECT Hold. Hold SELECT for 4.2 seconds (a ring fills round the glyph) to open the confirm step.
- **The confirm step says what it will do before it starts:** what the disc is, its size, how long it should take and where it goes. Confirm, then START rips; back cancels at any point before. Left / Right picks the drive a game goes to when more than one is started.
- **How long, said up front.** The time comes from what the kind of storage can take: the PS2's USB is USB 1.1, about 1 MB a second at best, so a 4 GB DVD to a USB stick is over an hour, while the internal exFAT HDD keeps up with the drive (a DVD at up to 4x, a CD at up to 24x). After your first rip RIPPS2 remembers the speed it really got for that kind of drive and disc, so the next estimate is your console's own. While it runs: how much is done, the percentage and the time left (hours past 90 minutes). Cancelling asks first, then removes everything written.
- **PS2 games** become an ISO in the drive's DVD or CD folder (`<ID>.<Title>.iso`, or `<ID>.iso` when there is no title), where the games list finds it. A game over 4 GB going to a drive that may be FAT32 (USB, MX4SIO, iLink: the PS2 cannot tell FAT32 from exFAT) is saved as Open PS2 Loader's 1 GB parts with its ul.cfg entry instead, which every drive takes; on the internal exFAT HDD it stays one ISO. Dual-layer DVDs are measured layer by layer. An ESR disc rips as the game it is.
- **PS1 games** become a BIN and CUE (2352-byte sectors, every track, each data sector's sync put back) in `EMBER/games/<Title>/`, in the PS1 games list for Ember.
- **Audio CDs and DVD videos go to your files.** Confirm opens Memory Files on a new **MEDIA** folder (beside AUDIO), with the disc on the clipboard reading **RIPPED** where it would say COPIED. Go to any folder, Triangle, **PASTE**: the confirm step again, then START. An audio CD becomes a folder of WAVs (Track 01.wav..., CD quality) and the keyboard opens by itself to name the folder; a DVD video becomes its VIDEO_TS files (1 GB at most each, so FAT32 takes them). A bought film is copy protected: the drive refuses its video and the rip says so.
- **Checked in the lab:** a 1.2 GB PS2 game ripped from PCSX2's drive to an exFAT HDD came out byte for byte the source (same MD5).

### AUDIO and MEDIA explain themselves
- **Any .ogg or .wav in AUDIO is music**, listed in Settings > Audio Settings > Music by its own name: a track copied in from a ripped CD needs no renaming to `bgm_04`. (`bgm_01 Title.ogg` names still set the order and the title.)
- **README.txt in AUDIO and MEDIA**, written by RIPPS2 the first time it uses the folder (a CD track copy, the BIOS sound and music rips, RIPDISC): what goes where, the event names, how the music list works, how to rip a disc. Never written to a memory card.

### Languages
- RIPDISC's 42 new lines read in all 33 languages.

## Build 104 (beta, in v1.0.7-beta), changes since build 103

### RIPPS2 in your language
- **RIPPS2's own words translate now**, not only Open PS2 Loader's settings: the category pages, Storage, Memory Files and the card manager, the CD player, BIBLE and BOOT LOCK, the achievements pages, About, every hint and message. One ELF for every language; the words come from a language pack.
- **`RIPPS2-languages.zip`**, built with every RIPPS2: copy its `LNG` folder to the top of a USB drive, the HDD's OPL partition or an MMCE card (or its files to `mc0:/RIPPS2`), then pick the language in Settings > Display Settings > Language. The settings home's own `LNG` folder (mc?:/RIPPS2 first) is read too.
- **33 languages read RIPPS2 whole** (779 of its 800 strings; the other 21 are names that stay as they are): French, Spanish, German, Italian, Portuguese, Brazilian Portuguese, Dutch, Danish, Swedish, Polish, Czech, Hungarian, Romanian, Croatian, Serbian, Albanian, Galician, Greek, Russian, Bulgarian, Turkish, Indonesian, Vietnamese, Filipino, Cebuano, Laotian, Simplified and Traditional Chinese, Japanese, Korean, Ryukyuan (upstream's Okinawan, with Japanese for the rest), Arabic and Persian. Every one of them also fills the Open PS2 Loader settings its upstream file lacked (up to 650 of them for Galician).
- **The files are keyed by the English** (`#!RIPPS2LANG 1`: a hash of each English string, a tab, its translation), so a pack keeps working with the builds after it; a string a later build adds shows in English until the next pack. A translation whose `%d`/`%s` differ from its English is refused and shows in English rather than crash. Older line-numbered language files still load.
- **Every script draws:** a letter RIPPS2's fonts lack comes from the language's own font at that font's size; the capitals fonts, the hints' sentence case and the source toast handle accented, Greek and Cyrillic letters; Chinese, Japanese and Korean lines break between characters. The pack carries each language's font (a large CJK one cut to the letters it uses) and its licence.
- **Long words fit:** a theme's hint row that a translation makes too long even with its gaps closed up reads a size smaller instead of running off the screen (Russian on RIPGRID), and a settings hint in Chinese, Japanese or Korean fills each line instead of starting its first clause on a line of its own. RIPPS2 Sleek's lowercase б has its ascender (it read as в in the hints).
- **Arabic and Persian read right to left, their letters joined.** Each line is shaped into the joined letter forms (lam-alef as one letter, the vowel marks over and under their letter) and laid out right to left, with English words, numbers, sizes and paths kept in their own order inside it. Upstream's Arabic was always drawn left to right in loose letters; upstream's Persian file stored 249 of its lines already joined and reversed, which RIPPS2 now replaces with its own translations. The pack's `font_Arabic` and `font_Persian` are DejaVu Sans cut to the Arabic letters and their joined forms.
- **Laotian** is translated whole, in Noto Sans Lao (in the pack with its licence). Lao, like Chinese, has no spaces between words: its lines break between syllables, never before a vowel sign or tone mark nor after a leading vowel.
- Not yet: Arabic and Persian lines start from the left edge as the theme places them (a right-aligned layout for them is still to come). The in-game menu stays English.

## Build 103 (beta, in v1.0.7-beta), changes since build 102

### RiptOPL, brought up to date
- **RIPPS2 now carries RiptOPL up to 10/18/2026** (rebuild/main 3cd7f89, 548 commits since build 84's merge). Among them: in-game reset input that a busy game can no longer starve (#973), settings saves that survive a failed write (#971), safer IOP resets and VMC handling, UDPFS reconnects, RetroAchievements fixes and its achievement card, CFG Titles shown in lists (#918), a CJK title fallback font (#917), per-game parental locks, the option to hide logo art, and 3D save icons for PS1 games.
- **RIPPS2's own look and features stay as they were** where the two met: the in-game menu runs inside upstream's new reset thread, Show Recents sits on the new crash-safe favourites file code, the star stays after a game's title, RIPGRID keeps its own colours, and upstream's new favourites notices say Starred Games.
- Not taken up yet: upstream's built-in PSBBN Flow theme (its slot is RIPGRID's; its element types are in, for themes on a drive), and its achievement browser and network RA rows (RIPPS2's Achievements page covers them).
- **The in-game core keeps room for RIPPS2's in-game menu.** Upstream's fixes made the core (ee_core) 2.4 KB bigger, past the space under 0x97000 that the in-game menu and its 4 KB thread stack need. The core now leaves out functions and data nothing uses, which more than made up for it (11.4 KB of stack room, against 5.3 KB in build 102), and upstream's experimental Caduceus achievement card, which RIPPS2 has no setting for, is not built into it.
- The ELF is about 150 KB bigger (3.10 MB): upstream's RA edition now carries mbedTLS for its HTTPS game-ID lookup.

### The version tells the truth
- **About now reads "v1.0.3-beta, BUILD 103"**, and the Settings hub and the boot screen read **"RIPPS2 v1.0.3-beta (build 103) on RiptOPL v1.2.0-Beta-4032-3cd7f89"**. Every RIPPS2 up to build 102 said "RiptOPL v1.2.0-Beta-3-65d4b89" whatever upstream it carried, because the build only ever cloned the one pinned commit; the version now names the upstream actually merged (`elf/RIPTOPL_UPSTREAM`).

## Build 102 (beta, v1.0.2-beta), changes since build 101

### Sound
- **No more beeping while a read is stuck.** When the music's file read stalls (a drive still coming back after an in-game reset, a busy card, the ripped menu music read straight from a drive), audsrv ran out of music and played the last tenth of a second over and over: the beeping. The music now keeps audsrv fed with silence until its next piece arrives.
- **Switching away from stuck music no longer hangs the menu.** Stopping the music waited up to 3.2 seconds for each of its two threads while one sat in that read. A thread inside a read now gets 0.4 seconds; after that it is left to finish on its own, and the next music start waits for it and cleans up after it instead of starting a second stream over the same buffers.
- **The console boot sound starts with the towers**, on the intro's first frame, instead of the moment the sound had loaded (which could be before anything was on screen).
- **`sounds=audio`, a new theme key:** the theme always plays your AUDIO folder's sounds (your ripped map) and never a sound folder of its own. Adapt and Adapt Rx set it, so an Adapt copied over an older one (which shipped six sounds up to build 99) plays your rips.

### Every theme
- **No info page switches the source any more.** Left, Right, Up and Down go through the games on every theme (build 101 did it for RIPFLOW only).
- **The Colours page works on every theme.** On RIPGRID and on themes from a drive the colour rows were greyed out, so the cursor skipped them. Now they edit that theme's own colours, kept for that theme alone; Reset gives it back its own.
- **Reflections fade with their covers**, and a cover inside a case fades in with the rest of the page (a JPG cover popped in at full strength while its case faded; RIPPS2's info page case was the one you saw).
- **Long text slides smoothly**, a pixel at a time every frame, where it jumped a letter every fifth of a second; a long description rolls to the pixel too.
- **Two theme element keys (`blur`, `widecrop`) start off on every element** unless the theme sets them; they were never cleared, so an element could pick up a value left in memory.
- **About and STATUS read in RIPPS2's own faces on every theme**, as Settings has since build 96 (RIPFLOW's STATUS heading was in its capitals), their hint rows included. **About's credits wrap** to the column between words, so no line runs out of the panel.
- **An app's case is a PS1 square by default**, on every theme. Triangle on an app opens its menu (now also where RIPPS2 may not write, for this line alone) with **Case Shape: PS1 (square) / PS2 (tall) / Theme**, kept for that app.

### Memory Files
- **A game started from the file browser starts its drive's games itself.** A drive opened only through START DRIVES had its files readable but its games not started, so a launch from there failed until the drive was opened once in Storage. RIPPS2 now starts them and waits for the drive's list before launching.

### RIPFLOW
- **The White glyph set** (L3 and R3 included), and **the hints in RIPPS2 Sleek Case**, as on every other theme.
- **Badges and the rating at their images' own shapes:** badges 44 x 22, six apart, starting on the text's edge (they were 32 x 16 and overlapped by a pixel); the rating 143 x 18, ending on the description's right edge.

### RIPGRID
- **The Standard glyph set** (L3 and R3 included).
- **The grid sits 4 higher**, so the space above its first row (from the PS2 mark) matches the space under its last (to the game's name).
- **The info page lines up:** the screenshots stand flush with the text's glass, top and bottom, centred in the room beside it; the release date sits evenly between the developer and the genre.
- **The logo stands just above the text's glass**, every game's at the same height (a new key, `valign=bottom`, finds where each logo image's visible part ends, since some come with a lot of clear space round them and others with none).
- **The CD player and file tree read like RIPFLOW's, Launch Disc and Memory Files like RIPPS2's** (START LASER, START BROWSER and the disc line). RIPGRID's own text keeps its look.

### Adapt and Adapt Rx (RIPPS2-themes, edition 102)
- **The Standard glyph set**, **your ripped sounds** (`sounds=audio`) and **hints in RIPPS2 Sleek Case** on every page, the menus' hints included.
- **The apps page fits:** the games' glass and list (the apps' own glass ran up into the category bar), with the app's case under LAUNCH DISC as a PS1 square. The apps info page shows the case square too.
- **The info page's screenshots stand flush with the text's glass, and the logo just above it** (`valign=bottom`).
- **The disc and case line up with the list:** at real-life proportions to each other (a 120 mm disc over a 135 x 190 mm case), the disc's top level with the list glass's top and the case's foot with its foot. The disc no longer stands up by the category bar.

## Build 101 (beta, v1.0.1-beta), changes since build 100

### Sound that stays where it belongs
- **No sound turns up after its moment, and none plays from a half-loaded set.** Changing the theme (in Interface or by holding SELECT), an IOP reboot, a rip and the AUDIO folder found late on a drive all load the sounds again: every voice is keyed off and the sounds are written back one by one, which takes seconds when your rips are on a memory card. The menu kept playing through that, so cursor and page sounds were asked of a half-loaded set, and a confirm caught by the load was kept until its end and sounded seconds later, outside the menu it came from. Now nothing touches a voice while a load waits or runs: a cursor tick is dropped, and the newest confirm, cancel or page sound plays when the set is in only if it was pressed within the last 0.3 seconds. Every load also forgets which voice the sounds before it took, and the voices are turned down before the load's reset turns them all up, so no ringing tail flares.

### RIPFLOW
- **Left and Right go through the games on RIPFLOW's info page**, as on its carousel, and the info page stays; they no longer switch drives there. Other themes keep Left and Right for the drives.

### Hotfix (10/13/2026, still build 101)
- **The README and RIPPS2's About page credit xeRAbora by [hacan359](https://github.com/hacan359), and pin the release.** The RetroAchievements PC client and the console-side RA code RIPPS2 inherits through RiptOPL (MIT / AFL-3.0). **LEFT TO HUNT** reads the interface page's `GET /state` (port 18280), which is xeRAbora's own UI endpoint, not part of the documented console protocol, and can change between alphas, so it was pinned to **v0.1.0-alpha.10** (moved to alpha.18 on 10/17, below).

### Hotfix (10/17/2026, still build 101)
- **LEFT TO HUNT is pinned to xeRAbora [v0.1.0-alpha.18](https://github.com/hacan359/xerabora/releases/tag/v0.1.0-alpha.18)**, on its author's advice: alpha.10 is unstable and fixes land in every alpha. alpha.10 could not have worked anyway: the `checked_only` key RIPPS2 finds the game's set by is in `/state` only from alpha.11 on. alpha.18's `/state` was checked against RIPPS2's reader (the `game` object with `serial` and `checked_only`, then `achievements` with title, description, points and state); its new keys (`mode`, `rp`) are skipped. The About page names alpha.18.

## Build 100 (beta, v1.0.0-beta), changes since build 99

RIPPS2 leaves alpha: build 100 is the first beta, released as **v1.0.0-beta** (About reads BUILD 100 (BETA); first tagged v0.1.0-beta, renamed when the version came to follow the build number).

### Sound, cleaned up
- **The ripped boot and launch music no longer pop.** Three of the boot bank's instruments (the PS2 logo, the boot's low swells) were read as the SPU2's noise generator and played as a random level held for a tenth of a second: a pop at every step. They are a real recording at the start of the bank. Checked on the PC against a real console's recordings: boot went from 274 click points to 2, launch from 50 to 0. RIPPS2 Audio Studio's renderer is fixed the same way.
- **The beep after saving settings is gone.** Reloading the sounds (leaving Interface did it every time) let audsrv turn a still ringing voice back up to full while new sounds were written under it. Every voice now goes silent the moment a reload starts, only a voice with a sound playing is turned up, and only a new theme reloads the sounds at all.
- **One press, one sound.** A press that opens something (a message, the save prompt, a page) used to play its confirm and, a few milliseconds later, the sound of what it opened, cutting the first one off: a tick, then the second sound. Now the press waits for the end of its frame and what it opened sounds instead. Saving sounds once, with its own box. Circle on a setting sounds as a cancel, not a confirm.
- **Nothing sounds without a press.** The notices a drive scan raises (settings, themes or languages found) are silent, a drive that comes up because you pressed Start Device adds no connect sound, and turning a case over with the right stick is silent like its tilt.
- **No double sounds:** your AUDIO folder fills only what the theme's sounds leave silent. Adapt and Adapt Rx now ship no sounds of their own, so your rips play as they are.

### The menu music, ripped on its own
- **Audio settings > BIOS Music > RIP** writes your console's menu music, the browser's ambient piece (5:31), as `bgm_00 Menu.wav`, made from the BIOS's own notes. Its size (15.1 MB) is shown first and you pick where it goes: beside RIPPS2, or OPL's AUDIO folder on a started drive. A memory card is never offered (none has room). **BIOS Sounds > RIP** now makes only the sounds, under 1 MB.
- **The music plays from OPL's AUDIO folder too:** every started drive's OPL folder (USB, HDD, MMCE) adds its `bgm` tracks to the Music list beside RIPPS2's own, in file name order, and a drive that brings music starts it when nothing is playing.

### RIPPS2's own save
- **RIPPS2 keeps its settings in its own memory card save, `mc0:/RIPPS2`** (or the card you boot from): the dead elf's hat ringing its bell, the settings files and nothing else, about 55 KB. No more sharing settings files with another OPL beside the ELF. Your current settings are read once from where they were and saved there from then on; a Custom Settings Path still wins, and without a card nothing changes.
- **The hat icon is lighter:** 51 KB instead of 90 KB, and a card holding the old one gets the new one.

### Memory Files
- **Replacing a file is a clean erase, then the copy, then a check** that the new file is whole; the music lets go of a file being replaced, and a failure says so.
- **An ISO or ZSO starts where it is.** Outside the CD and DVD folders, or not yet in the drive's list, it starts all the same, with no "move it" message.
- **The text editor** draws every line in RIPPS2 Sleek's true case (Planet N's capitals were hard to tell apart). **The 3D icon viewer** turns the way you press.

### Storage and menus
- **POPSTARTER from USB remembers** whether your drive is FAT32 or exFAT and stops asking (and stops sounding as if it had never been set up) while the drive still matches.
- **A case turns over from the side you push**, to its back and home again.
- **The START menu, the game and app menus and the Settings hub** use Adapt's clear face on every theme.
- **Hotfix (10/12/2026, still build 100): RIPGRID's info page** draws its stars and badges at the default theme's sizes, side by side inside the glass panel, the stars starting at the text's edge. At the images' own sizes the badges (480P, 16:9, NTSC...) overlapped each other and covered the last stars of the rating (seen at 3:46 in the beta reel).

## Build 99 (testing), changes since build 98

### The music has a road of its own
- **The music no longer waits in line for the drive.** It used to ask the drive for 2 KB at a time, every few hundred milliseconds, each request queued behind whatever cover or list was loading, and under a burst of those it fell behind (the stutter and freezes on real consoles). Now the music file is read into memory in big pieces, 64 KB growing to 256 KB (about 16 seconds of a typical track per request), and a track up to 512 KB is held whole, so its loop never touches the drive again. A 1.1 MB track now takes 6 requests instead of 552. In the lab a pilot tone played 90 seconds through a button storm, tab switches and the track's loop without a single dropout.

### Names that mean what they say
- **Drives are named by what they are, not by their slot.** `mass0:` can be a USB stick, the internal exFAT hard drive, iLink or MX4SIO. YOUR ACCOUNT said a game was "on USB" when it was on the HDD, and STATUS offered the "USB" POPS and EMBER folders and a "USB" Neutrino whatever the drive was. They now say USB, HDD, iLINK, MX4SIO or UDPBD, MMCE reads 0 and 1 like the cards, and the PS1 launch report says which drive `mass0:` was.
- **A Grid tile without a cover shows a PS2 game ID or nothing.** A PS1 game named like a serial (`SCUS_949.00.Crash...`) showed its whole file name as one.
- **Checked against RiptOPL's rules** for art and settings names: a PS2 game by its ID, a VCD by its file name, an Ember game by its folder name, an app by its ELF name, and a PS1 disc ID never in their place. RIPPS2's own pages (Grid back covers, All Games, Starred, Recents, metadata, art fetch) follow them.

### From RiptOPL
- **PS1 games flash their real disc ID** for Pixel FX / RetroGEM / PS2Digital (RiptOPL #869), for POPSTARTER and Ember alike, read from the disc itself. The menu no longer flashes a PS1 game's file name as its ID.
- **A slow iLink drive is waited for** at start (RiptOPL d8b5016): a drive still spinning up is looked for again for 3 seconds instead of being missed.

## Build 98 (testing), changes since build 97

### Memory Files
- **Both memory cards stay after START DRIVES.** It pinged both card slots with MMCE commands whatever Game Sources said, and a plain card in slot 1 then dropped out for the session. It now asks exactly as Storage does. Cards read **MEMORY CARD 0** and **MEMORY CARD 1** everywhere, beside `mc0:/` and `mc1:/`.
- **Deleting is thorough and honest.** The music now lets go of a file you delete (error 16 was its open file) and comes back after; every removal is checked gone, and a failure says why in words, never a bare code.
- **Copying to a full card says so first:** CARD FULL with the KB it needs, before anything is written (error 999 was a full card), and a slow write is finished instead of stopping short.
- **Paste asks before it replaces:** YES, REPLACE IT / NO, KEEP IT / YES TO ALL. A folder merges, file by file.
- **Rest on a file for 0.42 s** to see its size and its created and modified times. Hold Up or Down and the list scrolls at your Storage scroll speed.
- **Games start right from Memory Files:** an ISO or ZSO in a drive's CD or DVD folder starts as it does from Storage (your Loader Core, VMCs and cheats), and a CUE or BIN in `EMBER/games/<game>/` starts with Ember. A CHD explains what to make instead.
- **3D save icons:** an `.ico` or `.icn` opens in 3D, textured, lit and animated over its own background. Turn it with the D-pad or right stick, L2/R2 zoom, Square stops the spin. **Actions > RIP 3D ICON** writes it out for a PC: an OBJ for each animation shape, the material and the texture as PNG, in `mass0:/RIPPS2/ICONS/`.
- **RIPPS2's own memory card folder has an icon:** the dead elf's hat ringing its bell. It used to show as corrupted data in the PS2 browser.
- **The text editor keeps your file as it was:** long lines, long files, blank lines at the end and missing final line breaks all come back exactly; a file it cannot hold is refused instead of cut.
- **The picture viewer** stays sharp zoomed right in (it used to shear), and both viewers show their buttons as glyphs.

### Sound and music
- **Half of all music never played, and now it does.** The PS2's Vorbis library refuses any Ogg stream whose serial number has its top bit set, and encoders pick that number at random. RIPPS2 now fixes it as it reads, and RIPPS2 Audio Studio no longer writes such files.
- Each sound comes from your theme first, then from your AUDIO folder (a theme with only a few sounds used to leave the rest silent).
- Previewing `.adp` sounds stands up to frantic play, stop and move.

### Grid, Flow and art
- **The game's background fades in as soon as it is decoded**, asked for right behind its cover instead of after everything else. The info page's background, disc and cover fade in together again, and its slideshow opens on the background.
- **L2 / R2 on the Grid turn a whole page.** **Widescreen Grid layout:** its own columns, rows and cover size for 720p, 1080i and widescreen.
- **Vignette Other Covers:** Off, Weak (new default, half as strong) or Full, without the bright line down a cover's side. **Background art blur:** Theme, Off, Weak, Normal or Strong.
- **RIPFLOW tilts and flips like RIPGRID:** the centre cover leans with the right stick and turns over on a hold; the info page's screenshots tip as one sheet.
- **Covers missing on a Grid** show the game's ID in one size, inside the tile, or a clear tile. RIPGRID is in capitals everywhere.
- **STATUS > DRIVES** names every drive RIPPS2 sees and what became of MX4SIO (off, not started, refused with its code, no card, or mounted).
- The theme pack is Adapt and Adapt Rx, each with a full key glossary at the top (RIPGRID is built in).

## Build 97 (testing), changes since build 96

### Grid and Flow
- **RIPGRID froze at 720p and is fixed.** A save state read against the build's symbols showed the menu waiting on a pad command the controller never answered while it was still starting up. Pad commands now wait for an idle pad. 480p, 720p and 1080i all lay out centred.
- **RIPGRID:** the name under the grid in RIPPS2 Sleek Bold, the grid centred on the content, and Right at the last column turns to the next page (Left to the previous) without wrapping.
- **Case flip on a 0.42 s right-stick hold** (was 2 s), RIPFLOW too, where it replaces the automatic crossfade. RIPFLOW's info page tilts its screenshots with the right stick.
- **A list page is always full.** It opened on your remembered game as its top row, so near the end of a list it showed a few games over empty rows, as if games were missing.
- Older OPL themes (Grunge, Adapt RiptOPL) draw their lists, menus and settings as RiptOPL does.

## Build 96 (testing), changes since build 95

### Settings and menus
- **Backing out of a submenu lands on the row that opened it**, not at the top of the page.
- **Settings read in one plain face on every theme** (Adapt's settings face), not each theme's styled fonts.
- **Colors and More:** a tooltip on every row, a **Theme** value on most rows, and the Grid backgrounds take the color theme.
- **Flow Cover Count** and **Flow Cover Size** for RIPFLOW. STATUS scrolls like the settings pages.
- **Devices:** auto start can be **Last Used**, the device and page you were on.
- **Page buttons:** Theme, L1 / R1 or L2 / R2 (theme key `page_buttons=l2r2`, which RIPGRID uses).
- Neutrino's automatic arguments are described plainly.

## Build 95 (testing), changes since build 94

### Sound effects that never stack, stall or come back
- **A held cursor no longer goes quiet in waves**, and old sounds no longer come back after. The console plays a sound only on a voice that has finished, and RIPPS2 used to set a voice's volume before asking: with the BIOS rips' long tails, a press often landed on a voice still ringing, lost its own sound and turned the old one back up. Now RIPPS2 knows when every voice ends, a sound takes only a finished one, and its volume is set once it is playing. In the lab, a held cursor went from six ticks and 0.8 s of silence, over and over, to every tick 60 ms apart.
- **No sounds are built in any more.** RIPPS2's sounds come from your `AUDIO` folder: **Audio Settings > BIOS Sounds > Rip** makes them from your own console, and RIPPS2 Audio Studio on a PC makes any others. Without them RIPPS2 is silent, and **STATUS** has a new **SOUNDS** section that says how many are loaded and where from, with **RIP THIS CONSOLE'S SOUNDS** right there.
- **The boot no longer reads the boot sound on its own.** Every sound file is read by the one worker that reads the drives. A ripped `boot.adp` (a few hundred KB) used to be read at boot while that worker was busy with the same memory card, which can hang a console. Each file is also checked first (a real `.adp`, at most 1 MB) and RIPPS2 makes sure the IOP has room for it before handing it over, so a bad or oversized file is skipped instead of stopping anything.
- **Ripped sounds end at silence:** each one fades out over its last 30 ms instead of stopping in its hall's tail. Rip again to get the new endings.
- **Memory Files plays `.adp` sounds:** Cross plays one (again), Back closes. Handy for checking a rip.

### Fixed
- **RIPFLOW is back**, and so is anything else that broke from build 93: libsmslite (the video player) carried its own copies of the C library's string functions, and they replaced the real ones for all of RIPPS2. RIPFLOW's theme stopped loading (a plain list over its background art), build 93 could hang at boot, and a count went wrong on the console. libsmslite keeps those to itself now, and the build fails if it ever does that again. MX4SIO, which FifthFox found missing everywhere, is identified by those same string functions: please check whether it is back.
- **JPG pictures open whole.** RIPPS2 reads the file completely before decoding it: a short read from a drive used to end a JPG early, leaving the top part only.
- **Game art can be JPG.** A cover (or any art) with no PNG is looked for as a JPG of the same name, so old OPL art packs show on every theme instead of the game's name.

### In-Game Menu
- Its tooltip now says it is experimental: some games skip their sound, or stop, if paused during a cutscene. With it **off (the default) the combo is OPL's trusted IGR**, and nothing of the pause menu or its achievement list is involved.

## Build 94 (testing), changes since build 93

### Spirit of RA: what is left to hunt
- **CHECK GAME SUPPORT now brings the game's whole set home.** With xeRAbora's **OPEN TO THE NETWORK** on (its settings), the check also asks xeRAbora's interface page for the game's achievements and keeps them beside the game's list as `RA/<serial>.ach`: each one's title, points, how it is earned and whether your account has it. With it off, the check works as before and nothing else changes.
- **Achievements > YOUR ACCOUNT:** a game's card says how many are left to hunt. Cross (or Circle, with Circle as confirm) opens **LEFT TO HUNT**: every locked achievement with its points and how to earn it, Up and Down to choose, L1 and R1 to page, Back to return.
- **In-game menu (Settings > General > In-Game Menu):** ACHIEVEMENTS says how many are left, and the confirm button opens LEFT TO HUNT in the pause menu itself: one achievement at a time, its title, its points and how it is earned, Up and Down (or confirm) for the next, Back to return to the menu, START back to the game. The list is the one the last CHECK GAME SUPPORT saw: run it again to bring it up to date.
- The pause menu's list travels with the game in the memory the game leaves alone, up to 8 KB of it (well over a hundred achievements). A game that needs that memory for itself, or a launch whose modules leave too little room, plays without the page.

## Build 93 (testing), changes since build 92

### Memory Files opens pictures and video
- **Pictures (PNG and JPG):** Cross opens one full screen, fitted to the screen. Hold R2 to zoom in and L2 to zoom out, move round with the D-pad, tilt it with the right stick, Triangle fits it again, Back closes it. A picture of any size opens: a big one is made smaller as it is read (up to 720 x 512 is kept), a row at a time, so it needs little memory. (Interlaced PNGs are the exception: save them without interlacing.)
- **Video (AVI, XviD or DivX, with MP3 or MP2 sound):** Cross plays it full screen, letterboxed to its own shape. **START pauses** and carries on; Back or SELECT stops. Nothing else on the pad is taken. The menu music stops for it and comes back after.
- The video player is **libsmslite**, the SMS player's core (Eugene Plotnikov and contributors), in RIPPS2's own fork (elf/libsmslite) with the pause added. Its core is AFL 2.0; its MPEG-4 and MP3 decoders come from ffmpeg and mpg123 under the LGPL 2.1, and it is built as a library of its own. About credits it.
- To make a video it plays: `ffmpeg -i in.mp4 -c:v libxvid -vf scale=640:-2 -r 25 -c:a libmp3lame -ar 48000 -b:a 128k out.avi`.

## Build 92 (testing), changes since build 91

### The category bar
- **LAUNCH DISC, STORAGE and MEMORY FILES look the same on every theme now**, in RIPPS2's own face. A theme that wants its own sets `category_font=theme`.
- **Themes can move and reword it:** `category_layout=column` stacks the three down the side (a sidebar) from `category_x` and `category_y`, `category_spacing` apart, with the mark riding beside them; in a row, `category_y` moves the bar down. `category_label_launch`, `category_label_storage` and `category_label_files` change the words.

### Page Transition
- **Colors and More > Page Transition:** Theme, None, Fade or Flash. Going to another category, the new page comes in from the theme's background colour (Fade) or out of a quick flash (Flash); the bar stays put. Themes pick their own with `category_transition=none|fade|flash`.

### The Grid look
- **A game with no cover shows its serial** (SLUS-20482) on its case, in the in-game menu's own pixel font, sized to fit: one line, or the code over the number. Themes ask for it with `coverless=serial` on their Grid.
- **The chosen game's name under the grid**, on its own line, with the highlight staying on the case (`title=1`, `title_y`, `title_font` on the Grid).
- **RIPgrid uses both.** Its info page shows the developer and the genre in RIPPS2 Sleek Bold (capitals) and the date in Planet N, as Adapt does. The theme pack's RIPgrid carries Planet N; the built-in `<RIPgrid>` uses RIPPS2 Sleek in its place, as Planet N (Iconian Fonts) is not RIPPS2's to build into the ELF.

## Build 91 (testing), changes since build 90

### The launch disc
- **As a game launches, its disc comes in** over the middle of the screen, where the launch's Please Wait used to sit. It is the game's own disc art (ICO) when you have it, else RIPPS2's disc.
- **Pop In** arrives the way the L3 logos do (a touch large, settling, with a glow), holds and fades. **Spin** arrives the same way, then turns faster and faster up to a steady spin and never fades: it is still turning when the game takes the screen.
- **RIPgrid pops its disc in; RIPFLOW spins its.** Other themes can ask for either with `launch_disc=pop` or `launch_disc=spin`. Off everywhere else unless you pick it in Flow and Grid.
- Real discs (Launch Disc, the DVD player) and PS1 disc images get RIPPS2's disc too. Programs (ELFs) get none.

### Interface > Flow and Grid (was Coverflow Settings)
- **Vignette Other Covers** replaces Dim Side Covers, in Flow and on the Grid: every cover but the chosen one darkens towards its edges, so the chosen one looks lit. On unless you turn it off.
- **Grid Layout:** Theme, 4 x 2, 5 x 2, 3 x 2 Large or 6 x 3 Compact, with RIPPS2's spacing. The grid keeps the theme's place on the page.
- **Launch Disc:** Theme, Off, Pop In or Spin.
- **RIPgrid is built in** as `<RIPgrid>`, next to `<RIPPS2>` and `<RIPFLOW>`: no theme folder needed.

### Settings pages
- **PS Emulation's USB BDMA Driver row is back.** It showed "<no values>" floating under VCD BDMA Apply on Launch: its ids were the same numbers as the VCD buttons beside it, so the page filled the buttons instead. Every settings id and every game's option id are now apart, and a test checks that no two ids match.
- **Rows that are hidden take no space.** With VCD BDMA Apply on Launch on, BDMA Source and Mode go away without leaving a gap, so USB BDMA Driver sits right under it. The same goes for HTTP's rows on Network when the share is SMB.
- **An empty value reads Default**, not "<no values>".
- **Network:** a line under the share's password, then POPSTARTER Network Settings, NBD Server, Cover Art and Achievements together, then one clear row before OK. Achievements opens the same page as from the Settings list.

### Memory Files
- **A folder is called a folder.** Copy, cut and paste say "FOLDER AND CONTENTS COPIED", "2 FOLDERS AND CONTENTS MOVED" or "1 FOLDER, 2 FILES PASTED", never counting what is inside.
- **The progress bar counts every file** as a paste goes, down every folder's tree: "12 / 48 FILES".

## Build 90 (testing), changes since build 89

### Hints and Glyphs (Controller Settings)
- **A new page for the button hints and glyphs.** Every row starts on **Theme**, which shows what the theme chose. Pick anything else and it is yours, and it wins over every theme.
- **Hint Layout:** Row (one line, as before) or Column (one hint a line, a list down the side).
- **Hint Labels:** Glyph and Label, Glyph Only for glyphs that carry their own words (a hint whose glyph the theme does not have keeps its label), or **Badges**: each hint's glyph and title together on one pill, in the glyph set's style. Badges are never on unless a theme asks for them or you pick them.
- **Menu (START), Refresh (SELECT), Star (R3) and View (L3)** each get a row to show or hide that hint. The buttons work either way.
- **Hint Order:** Theme, or your own order. Pick a hint for a place and the one that was there swaps into the picked hint's old place, so every hint is always there once.
- **Glyph Set:** the theme's own glyphs, RIPPS2's, **Standard** or **White**, on every page.

### Two new glyph sets, built in
- **Standard** is the Adapt theme's glyphs: dark glossy buttons with coloured symbols.
- **White** is the Grunge theme's: solid white with the symbols cut out.
- Both now have everything RIPPS2 draws, made to match their set: L1, R1, L2+R2, L3, R3 and the four D-pad directions.
- Every set, RIPPS2's own included, has a badge pill for Badges.

### For theme makers
- New `conf_theme.cfg` keys, each a default the user can override in Hints and Glyphs:
  - `hints_hide=star,view` leaves hints off the bar;
  - `hints_order=run,info,menu` puts the named hints first, with the rest after;
  - `hints_labels=0` shows glyphs only, and `hints_labels=badge` draws each hint as one badge (ship a `hint_badge.png` to give the pill your own look);
  - `hints_layout=column` (with `hints_spacing=28`) gives one hint a line from the hint element's x and y;
  - `glyph_set=theme|ripps2|standard|white` picks the glyphs.
- Hint names are `menu run info options refresh star view source`; the buttons' own names (`start select r3 l3 cross circle square triangle`) work too.
- The D-pad Up and Down glyphs now load with every theme, so Coverflow's drive glyphs show when D-Pad Glyphs is on.

### Tested
- Ember from an APA HDD partition (`__.EMBER`) boots Digimon World in PCSX2 on this build. FifthFox's report that Ember fails only on the HDD is for real hardware; a `LAUNCH.TXT` from that console would show what it saw.

## Build 89 (testing), changes since build 88

### Your console's sounds, all of them
- **BIOS Sounds > Rip now makes the boot and the game launch too.** On the console those are system music: notes played on the BIOS's own instruments. RIPPS2 plays them the way the console does (every instrument layer, its envelope, the noise voices, each channel's volume and pan, then a hall) and saves them as `boot.adp` and `launch.adp`. Fifteen sounds in all; a few seconds of work, with the progress on screen.

### PS1 games
- **RIPPOPS.** Sony's `POPS.ELF` and `POPS_IOX.PAK` are not in any PS2's BIOS, so they cannot be ripped from the console. When POPSTARTER finds them missing beside your games but you have them in a `POPS` folder on another drive (USB, MMCE, the HDD or a memory card), RIPPS2 offers to copy them over and start the game.

### Settings
- **A scroll bar** on any page that runs past the screen.
- **The right stick slides the page** up and down on its own, without moving the cursor and without the cursor sound. The D-pad (or the first confirm) brings the view back to the cursor.

### Neutrino
- The automatic `-logo` now comes after the `-bsd` options and before `-dvd`, as FifthFox asked for his iLink test. Neutrino reads all of its options before it does anything, so the position does not change when the logo plays; the argument preview just reads in that order.

### About
- Credits updated: ORBIT's Neutrino fork (the in-game menu's pause and drawing), the console-ripped sounds and RIPPS2 Audio Studio, Roboto Condensed (RIPFLOW's type), and MCKILLA, RIPPS2's card manager fork.

## Build 88 (testing), changes since build 87

### Audio
- **Audio settings > BIOS Sounds > Rip** writes your console's own menu sounds into the AUDIO folder as RIPPS2's sounds: cursor, confirm, cancel, pages in and out, category, messages, disc, error, save, drive in and out, and random. RIPPS2 reads them from the BIOS of the console it runs on, plays each one the way the console does (its envelope, its volume, a little of the hall the browser runs under its menus) and saves it as a sound file, so no one has to pass sound files around. It asks first, because files of those names in AUDIO are replaced.
- Boot and game launch stay as they are: on the console those are system music, not menu sounds.
- Consoles from SCPH-30000 on carry the sounds this way; the first models (BIOS 1.00) keep them elsewhere and are told so.
- **Music** plays the track called Menu first when you have not picked one (`bgm_03 Menu.ogg` in a pack that has it); otherwise the first track, as before.

## Build 87 (testing), changes since build 86

### In-game menu
- **Settings > General > In-Game Menu** (off until consoles have shown it safe: turn it on to test). With it on, **L1+L2+R1+R2+SELECT+START pauses the game** under a plain panel (no animation) instead of leaving it at once:
  - **Resume** goes back to the game.
  - **Achievements** is SpiritofRA for the game you are in: how many achievements you have (as your last CHECK GAME SUPPORT left them, plus the ones unlocked this session) and whether tracking is on.
  - **Exit Game** leaves for your Exit To path, as the combo always did: RIPPS2, the boot lock's loader or the browser. It takes a second press, so a slip does not cost your progress.
- Up and down choose, confirm picks, and the other face button or START resumes. The power button and L1+L2+R1+R2+L3+R3 (power off) work as before.
- For games RIPPS2 starts with its own loader (USB, internal HDD, SMB, MMCE, iLink, MX4SIO, and discs from Launch Disc with achievements). Neutrino games keep the old combo for now.
- The panel is drawn into the frame the game is showing. A game that shows its frame in a way RIPPS2 cannot see gets the old behavior: the combo leaves it. PCSX2 cannot show the menu (it has no data breakpoints), so this is for real consoles.

## Build 86 (testing), changes since build 85

### Memory Files: the CARD MANAGER
- **Square on a memory card** in the drive list opens the CARD MANAGER (as Square on the internal HDD opens the HDD MANAGER); a card image (VMC) has it in its Triangle actions. Every save with what it takes, the space left, and the card tools:
  - **Delete** a save.
  - **Back up the card to a VMC** on a drive (`VMC/CARD1-01.bin` and on): a blank 8 MB card image with every folder on the card copied in, the way Memory Files copies saves. The card stays as it is.
  - **Write a card image's saves to memory card 1 or 2.** A save already on the card is left as it is.
  - **Erase every game save**, keeping the folders that are not saves: boot loaders (BOOT, PS2BBL, FMCB, OSDMENU), SYS-CONF, APPS, RIPPS2, POPSTARTER and the folder RIPPS2 was started from.
  - **Format the card** (never the card RIPPS2 was started from).
- Delete, erase and format each take two screens, and the last one only START gets past.

### Neutrino
- The automatic `-logo` is sent first, right after `neutrino.elf`, NHDDL's order (for FifthFox's iLink test; Neutrino reads every option before it acts, so it is not a fix in itself).

## Build 85 (testing), changes since build 84

### PS1 games on a real console
- **A launch report.** Just before POPSTARTER or Ember takes over, RIPPS2 writes what it is about to do to `mc0:/RIPPS2/LAUNCH.TXT`: the file it is starting (its size and CRC, which tell which version it is), its arguments, Sony's POPS files or Ember's BIOS beside it, both cards' POPSTARTER folders, and the settings that steer it. A PS1 game that will not start says nothing on screen, and PCSX2 starts them fine, so this file is how a tester can show us what the console saw: open it in Memory Files, or post a photo.
- **POPS files, asked about first.** On USB, iLink, MX4SIO, exFAT HDD and MMCE, a POPSTARTER launch without POPS.ELF and POPS_IOX.PAK (the PS1 emulator from your own console) in the game's POPS folder now says so before the memory card is prepared, instead of going to a black screen. START launches anyway.

### Video modes
- **The 704-wide modes draw in one pass**, 16-bit like the HD modes. They were the last on gsKit's two-pass hires renderer, the one RIPPS2's towers overran in HD: confirming one, or letting the prompt time out, could freeze the console. The list no longer says HIRES.

### Launch Disc
- The CD player's button hints stay inside the TV-safe area; CLOSE no longer sits at the screen's edge (and a tight row says COPY for COPY TO AUDIO).

## Build 84 (testing), changes since build 83

### From RiptOPL
- **RiptOPL's latest** (33 commits, to e74ddce) is merged in. For PS1 games: the memory card's POPSTARTER folder is only made when there are modules to put in it, and never by just looking (an empty one was being made on every PS1 launch); PS1 "missing" messages name the file they looked for. Also: cheats on both cores, a VMC created on a game's first launch, Neutrino's argument preview, PS1/PS2 list labels you can turn off (Interface), and fixes for MX4SIO ZSO games.

## Build 83 (testing), changes since build 82

### Star your games
- **Favorite is now Star.** R3's hint says Star, and the list it fills is **Starred Games**: the source, its Pop In toast, L3's caption and the Settings rows. Only the words change; your starred games and settings carry over.

### YOUR ACCOUNT
- **Laid out like a RetroAchievements profile.** Unlocked, games and mastered across the top with one bar for everything; each game's count beside its name in the list; the chosen game's card with its unlocked / total, a bar, and Mastered, % complete or Not started. Long titles scroll and messages wrap, so nothing is cut off.
- Fixed: the card showed leftover text after a short title (KATAMARI DAMACY NTS 5 GAMES...), and the big total drew as a broken block.

### Any theme, any font
- **List titles sit in the middle of the highlight bar**, whatever font a theme uses: RIPPS2 measures the font's own centerline instead of a nudge tuned to its own face. Adapt's bar no longer rides above its titles, and your own themes need no adjusting.

### RIPgrid (theme pack)
- The covers sit a little lower and smaller, so the chosen one clears the category bar and the PS2 mark and the rest never touch it; the hints (list and info page), tooltips and YOUR ACCOUNT use RIPPS2 Sleek's lowercase face.

## Build 82 (testing), changes since build 81

### HD text fixed
- **720p and 1080i text is the right size again.** Since build 75 drew those modes 640 wide for the GS to stretch, the fonts took the pixel shape upside down: text came out four times too wide at 720p (two and a quarter at 1080i) and spilled over every panel. Now it matches 480p, as it should.

### RIPgrid
- **Turn the case over.** Hold the right stick to one side for 2 seconds and the chosen case flips to its back cover, the way you lean. It stays turned on the grid when you move on and when you come back; hold again to turn it home. The back cover is asked for as soon as the front is in, and the flip waits for it.
- **Pages slide.** The grid moves by whole pages now, and a new page slides in as the old one slides away, eased like RIPFLOW's carousel (off when Coverflow's animation speed is 0).
- Themes: a Grid's new `back_pattern` key picks what a turned case shows (`COV2`, the back cover, unless a theme says otherwise; `SCR` puts a screenshot there; `0` turns the flip off). The back covers get a cache of their own, a page and two deep.

### Theme pack
- **RIPPS2-themes for build 82**: everything since the build 80 pack in one download. Adapt's case shows the front, then the back; its info page sits opposite the list; Adapt Rx keeps its side bar on the left, and both keep the disc under LAUNCH DISC; RIPgrid is set in RIPPS2 Sleek with the Grunge theme's button glyphs; every image is an 8-bit PNG.

### US spellings
- What the menus say is in US English: canceled (the CD copy too), color, license, behavior, center.

## Build 81 (testing), changes since build 80

### Game list
- **Source Name: Pop In is now a toast.** The source's name is no longer drawn over the list: it plays in the middle of the page the way L3 names the list, in the same big letters, the whole name in capitals (ALL GAMES, HDD GAMES, BDM GAMES; the GAMES tells it apart from L3's ALL). It comes on the first list after boot, whenever the source changes and when you come back to Storage from another tab, then holds and fades. Closing an info page or Settings does not repeat it. Themes with `source_name=pop` (Adapt, Adapt Rx, RIPgrid) get it too, so their static source line is gone.
- Long names (UDPFSBD GAMES) close their letters up to stay on screen.
- **One big face for the view word, on every theme**: L3's ALL / PS1 / PS2 and the Pop In toast both draw in RIPPS2 Sleek Bold at 64 px (they used to take a theme's `font14`), RIPFLOW included, so they look and move the same everywhere. A theme without a `font14` of its own also gets that face for the Achievements page's big numbers, instead of its small text font.

### Themes set the look, you keep the last word
- **A theme can now choose Colors and More for itself** in its `conf_theme.cfg`: `color_theme` (RIPPS2, Ember, Blood, Ectoplasm, Amethyst, Bone), `category_bar` and `button_hints` (shown, fade, hidden), `dpad_glyphs` (hidden, shown, fade_in, fade_out), `category_order` (launch_disc_first, memory_files_first), and `source_name` (shown, fade, hidden as well as pop). No rebuild of the ELF: any theme folder can do it.
- **Your settings always win.** RIPPS2 now remembers which Colors and More rows you have changed. A theme's choice shows only on a row you have never touched that is still at its default, so anything you pick, the default included, stays yours on every theme. Colors and More shows what is in effect.
- **RIPFLOW puts Memory Files first** on the category bar, unless you have picked an order.

## Build 80 (testing), changes since build 79

### STATUS
- **A new STATUS page** on the START menu, where Achievements was: the homebrew RIPPS2 carries (Neutrino 1.8.0, POPSTARTER, Ember Beta-2, BIBLE), each under its own name, with where it is installed now, a way to install RIPPS2's copy, and its settings from around the menus (Neutrino's, PS1 Settings, POPSTARTER's network files, MANAGE for the boot loader).

### Achievements
- **Achievements moved to Settings**, the last page after Audio Settings.
- **YOUR ACCOUNT**, its last row: every game you have checked, from every drive, with what your RetroAchievements account has unlocked (a bar per game, your totals, mastered games), as xeRAbora reported it at each game's last CHECK GAME SUPPORT. Opens with START, closes with BACK or START, and lets go of its list when it closes. Counts are kept from this build's checks on; xeRAbora versions that do not send the unlocked count show the total only.
- **Badges** stay on by default: they cost nothing until TELEMETRY is on and xeRAbora answers on your PC (then a quick file check per game when a list refreshes, in the background). The page says so.

### Settings
- **Network**: RIPPS2's rows (NBD server, Cover Art) under their own RIPPS2 header; the RA switches left for the Achievements page; a clear row before OK.
- **Colors and More**: Source Name sits under the D-pad glyphs; the Color Theme heads the colour pickers.

### Game list
- **Source Name: Pop In**: the source's name rises in letter by letter, the way L3's view word does, when the page opens or the source changes. Themes can make it their default (`source_name=pop`).
- **Coverflow and Grid themes: Circle cycles the sources** (Cross, with Circle to select), since every arrow browses games there; the hint row says Source. Inside a folder it climbs out first; on the info page it is still Back.
- **Grid**: with tilt on, only the chosen cover tips with the right stick.

## Build 79 (testing), changes since build 78

For the reworked Adapt, Adapt Rx, RIPgrid and RIPgrid Rx themes (RIPPS2-themes kit).

### Switch themes with SELECT
- **Hold SELECT for 4.2 seconds** on the game list and RIPPS2 steps to the next theme, once per hold, and remembers it. A shorter press still refreshes the list, when you let go; a hold that switched the theme does not refresh.
- The Theme setting's tip says so.

### Grid
- **No stock disc or case**: each cover eases in as its art arrives. A game with no cover shows as a clear glass tile with its name.
- **The selection breathes**: a soft glow in the theme's selection colour swells and eases under a crisp frame.

### Glass and art
- **Clear glass**: a theme can give a panel one even tint (`tint`, `tint_color`) and drop its frame (`frame=0`), for a full-screen frosted layer or a side bar.
- The frost **eases in with the art** under it instead of appearing at once.
- **`widecrop`**: on a 16:9 picture, a theme's background art shows its middle three quarters (a zoom) instead of stretching; frosted glass over it follows.
- Page morphs use the first framed glass panel, so frameless layers don't count.

## Build 78 (testing), changes since build 77

For the new themes: Adapt, Adapt Rx, RIPgrid and RIPgrid Rx (in the RIPPS2-themes kit).

### Theme engine
- **Grid** element: the game list as a page of covers in rows (columns, rows and spacing set by the theme). Left / Right step one cover, Up / Down one row, and past the top or bottom row a new press switches drive.
- **Frosted glass**: `blur=1` on a glass panel softens the game's own background art behind it, made again as you move between games.
- **`towers=0`**: a theme can keep the pillars off the game pages (its own colour shows where there is no art); Settings still show the pillars behind glass.

## Build 77 (alpha), changes since build 76

### Neutrino is built in
- **RIPPS2 carries Neutrino 1.8.0** (rickgaiser's PS2 device emulator, AFL-3.0), unmodified. When a game starts through Neutrino and there is no Neutrino where RIPPS2 looks, it asks: install it **on the game's drive** or **on memory card 1 or 2**, your pick. Then the game starts.
- Your own Neutrino always comes first (the path in Settings, the game's drive, the memory cards). Network game sources offer the memory cards.
- The copy is checked: an install cut short is never taken for a complete one.

## Build 76 (alpha), changes since build 75

### Guard rails (nothing on screen changes)
- **Every build now runs RiptOPL's 34 host checks** on RIPPS2's patched tree, plus RIPPS2's own: HD modes stay single-pass, every drawn shape checks the draw queue, All Games and Favorites never free a list under a reader, the AUDIO search order, BIBLE's HDD fallback and the quiet-boot marker. Where RIPPS2 differs from RiptOPL on purpose, `elf/tests/expected_failures.txt` says why; anything else that breaks fails the build.
- **A new compiler warning in a RIPPS2 file fails the build.**

## Build 75 (alpha), changes since build 74

### 720p and 1080i, drawn in one pass
- **HD is drawn the way 480p is**: one full frame, every animation at full detail, 60 fps. It used to be drawn three times over in bands from a small buffer (gsKit's "hires" mode), which is what crashed. Now RIPPS2 draws a 640-wide frame and the PS2's own video output stretches it to 1280 or 1920 wide, with all 720 lines kept (1080i: 540 per field, as before).
- Nothing is simplified for HD, and the towers stay alive behind every prompt.

### Booting from the HDD
- **The boot sound starts right away**, before the HDD's drivers come up to read your settings. If you turned the boot sound off, RIPPS2 leaves a small `RIPPS2/QUIETBOOT` marker on memory card 1 so it stays quiet then too.

### Neutrino (from RiptOPL)
- **Show Launch Arguments** (Settings > Game Launching > Neutrino Defaults): see every argument Neutrino will get before a launch, and go back if it looks wrong.

## Build 74 (alpha), changes since build 73

### 720p and 1080i
- **No more crashes in the HD modes.** They draw into a quarter of the memory the other modes get, and a busy RIPPS2 frame (towers, orbs, glass) could write past it. Now the towers draw simpler in HD, and a frame that still runs out drops detail instead of the console.
- **The menu no longer starves the drives and the music in HD.** Switching to 720p or 1080i left the menu running above everything else for the rest of the session (a gsKit setting that was never undone); it is put back now.

### Storage
- **Fixed a hang on the info page** (All Games and Favorites): the page could read a list that was being rebuilt in the background just as the disc and cover came in. Both lists are now swapped in whole.

### Your AUDIO folder, wherever it is
- RIPPS2 looks for `AUDIO` beside itself first, then on the memory cards, every started drive (its top or its `APPS` folder) and the HDD's OPL folder (where its ART is). Start RIPPS2 from a memory card for a quick boot and keep the music on the HDD or a USB drive: it starts as soon as that drive is up.

### BIBLE on the internal HDD
- **Works on HDDs without a `__sysconf` partition** ("could not open __sysconf" in build 73): RIPPS2 goes on `__common` instead and the config on a memory card, which PS2BBL reads first anyway.
- **RIPPS2 on a memory card stays first**: when you install from a card or USB drive, PS2BBL starts that copy (quicker than the HDD) and the HDD copy is the fallback.
- Errors now say which partition and error code.

## Build 73 (alpha), changes since build 72

### Cover Art (Settings > Network, after NBD Server)
- **Download** fetches a cover for every PS2 game in your started lists that has none, straight from the PS2 over HTTPS (xlenore's ps2-covers, the collection ORBIT's launcher uses), into that drive's own ART folder. Covers you already have are never touched.
- Each one is decoded on the PS2 and saved the way OPL's art collections are: a 140x200, 256-colour PNG of about 20 KB.
- Under the hood: BearSSL 0.6 (MIT) for TLS, and RIPPS2's network module no longer drops the end of a reply it could not carry in one piece.

### PS1 games
- **POPSTARTER is built in too.** Your own copy always comes first (the path in Settings, the drive's POPS, APPS or top folder, a game's own `XX.<name>.ELF`, the memory cards). Only when there is none does RIPPS2 write the POPSTARTER it carries to the drive's `POPS` folder (`__common/POPS` on the HDD), then start the game. It never writes over a file that is there.
- **PS1 games start from Memory Files**: a `.VCD` in a drive's `POPS` folder shows as a disc, and Cross plays it the way Storage does (USB and MMCE).

### BIBLE on the internal HDD
- **Boot Loader > Manage** now offers the **internal HDD** beside the memory cards: PS2BBL 1.2.0's HDD build goes in the HDD's boot area, RIPPS2 is copied to `__sysconf`, and the console is set to start its HDD at power on, so a fat PS2 with the network adapter boots straight into RIPPS2 with no card at all.
- The HDD's old boot program is read out first and kept (`__sysconf/RIPPS2/MBR-BACKUP.KELF`); **Restore** in the same list puts it back.
- RIPPS2's HDD driver allows exactly those writes (the boot area inside `__mbr`, and its pointer). The partition table stays fenced.

### HDD Manager
- **Removing a partition works.** It always said COULD NOT REMOVE: the HDD driver refused every delete. It now lets a user's own partition go (two screens and START, as before). System partitions (`__` names), RIPPS2's settings home and the partition RIPPS2 started from still stay, and one in use says so.

## Build 72 (alpha), changes since build 70

### PS1 games
- **Ember is built in.** RIPPS2 carries Ember (Gageformer's PS1 emulator) unmodified. The first time you start an Ember game from a drive, it writes Ember and its licence into that drive's `EMBER` folder, then starts the game. Ember games are listed even before Ember is there. Bring your own PS1 BIOS as `EMBER/bios.bin`.
- POPSTARTER still starts from your own copy, which RIPPS2 finds on your drives.
- **Ember Game Settings** save per game from Triangle, and PS1 rows explain their save-card menu (from RiptOPL).

### Memory Files
- **.elf and .ELF programs start from the internal HDD** (APA) as well as every other drive.

### Smoother
- **The music no longer stutters through big loads**: the decoder takes the CPU first whenever its reserve runs low, and frames give way instead.
- **The towers cost about half as much per frame**: far towers are drawn simpler, and every tower simpler still for a moment while the PS2 is busy.
- **One press, one sound**: with a custom AUDIO pack, a press that opens or leaves a page plays the page's sound alone.

### Colors and More (Settings > Interface)
- **Source Name**: Shown, Fade When Idle (with the category bar) or Hidden.
- **Show Recents**: 0 to 9 of your last launched games at the top of Favorites, newest first (0 turns it off).
- Every button hint reads in lowercase: the save prompt, the START menu and message boxes too.

### Neutrino (from RiptOPL)
- Every Neutrino argument can be edited from the game's settings, video modes are explained, and RIPPS2 warns before the arguments get too long to pass.

### Under the hood
- RiptOPL's latest `rebuild/main` (31 commits, to dc6206f) is merged in.

## Build 70 (alpha), changes since build 66

### Boot Lock and BIBLE
- **Settings > General & System > Boot Loader > Manage** shows what each memory card starts at power on (PS2BBL, FMCB, OSDMenu).
- **BIBLE** is El Isra's PS2BBL 1.2.0, set up by RIPPS2: no wait at power on, RIPPS2 first. It installs on the card you pick; whatever was there before is kept in a backup folder, and CIRCLE at power on still starts it.
- **Boot Lock** only edits a real PS2BBL now (it finds one beside itself and in the system-update folder), and cleans up the file build 68 wrote for FMCB cards.

### Achievements (SpiritofRA)
- **Achievements** in the START menu (where Start NBD Server was): telemetry and badges, a PC link test, and RetroAchievements for the disc in the tray. The PC side is the xeRAbora client on your network.
- **NBD Server** moved to **Settings > Network**, with the same status screen.

### Controls
- **L1 / R1** switch Launch Disc, Storage and Memory Files from any of them, the info page included.
- **Left / Right** switch drives on Storage and orb formations on Memory Files.
- **Scrolling is Fast** by default.

### RIPFLOW (Settings > Interface > Theme)
- The built-in cover carousel, renamed from Coverflow: just the covers, the source at the bottom centre, its own Roboto type, and its console frame on every tab and on the info page, with the drive's icons kept.
- **Left / Right** run the covers (hold to scroll); **Up / Down** switch sources.

### Colors and More (Settings > Interface)
- **Color Theme** for all three tabs: RIPPS2, Ember, Blood, Ectoplasm, Amethyst, Bone.
- **D-pad Glyphs** beside drive and formation names: Hidden (the new default), Shown, Fade In, Fade Out.
- **Button Hints** and **Category Bar**: Shown, Fade When Idle, Hidden.
- **Category Order**: Memory Files first and Launch Disc last (made for RIPFLOW).

### Look and feel
- Tooltips and button hints read in lowercase, and tooltips fade away after 4.2 seconds. Menus keep their capitals.
- Many shorter tooltips.
- **720p and 1080i turn Widescreen on by themselves** (4:3 modes turn it off; you can still set it by hand), and the towers and orbs keep their shape in widescreen.
- The orbs and towers are much lighter on the PS2 (the busiest formations went from 23 ms a frame to 7), for a steadier 60 fps.
- Launching keeps the towers and the loading mark moving until the game takes over.

### Memory Files
- **Orbit Settings** (START grid): cycle, speed, path lines, height, and which formations are in use, all live.
- **HDD Manager** is Square on an APA hard drive: fast now, and removing a partition takes two screens.
- Drives have real names (USB, MX4SIO, iLink, exFAT HDD), and **START DRIVES** starts them whatever Storage's start modes say.
- **The orbs, towers and CD visualiser no longer break after 72 minutes**: leave it on overnight.
- Ember started from the file browser works.

### Storage
- Saves and launches go ahead of background work, and art and game details never wait behind the music.
- The All Games list loads once, and the info page's art, logo, disc and cover come in together.
- MMCE: START copies to a memory-card home.

### Discs and PS1
- The CD player takes any CD with sound tracks (CD-Extra, mixed mode, burned CDs).
- The POPSTARTER path fills itself in from a POPSTARTER.ELF on your drives (POPS, APPS or the drive's top, or a game's own POPS/XX.name.ELF).

## Build 66 (alpha), changes since build 55

### Launch Disc
- **START LASER** (was START DISC). The drive is read once after boot and again when you close the tray, so moving between tabs never waits on the disc.
- **CD player:** put in an audio CD and press START LASER. A panel opens on the page, with the tabs still on top:
  - Cross plays and pauses, Square stops, Up / Down pick a track, Left / Right skip, L1 / R1 jump 10 seconds, Circle closes.
  - Triangle copies the picked track into the AUDIO folder as music, named on the keyboard.
- **The towers become a spectrum analyser** while a CD plays. Low notes stand on the left, high notes on the right, and the last second of music rolls back across the field. Hits send a ring of light back from the front; the loudest moments fire the launch beams. The right stick turns the view (slowly and steadily) and zooms.
- **DVD video** starts the player straight away (no ESR question). A disc with no DVD video on it, or one for another DVD region, says it is not compatible instead of hanging. ESR-patched games start through your own ESR.

### Sound and music
- **One AUDIO folder** beside RIPPS2.ELF holds your own sounds and music:
  - **RiptOPL's sound names:** `boot`, `cancel`, `confirm`, `cursor`, `message`, `transition`, `bd_connect`, `bd_disconnect` (.adp files).
  - **RIPPS2's new events:** `page_in`, `page_out`, `error`, `save`, `launch`, `disc`, `random`.
  - **Music:** bgm files in name order (`bgm_01 Title.ogg`, `bgm_02 Title.ogg`...).
  - Anything you leave out plays RIPPS2's own sound.
- **Settings > Audio Settings > Music** picks the track.
- **The boot sound plays as the towers rise**, plays out, and hands over to the music.
- **The music plays on every tab.** The CD player takes over only while it plays.
- New sounds for going into and out of pages, errors, saves, game launches, a disc going in and the random game pick.

### Storage
- **Settings saves no longer get stuck** behind background loading. A save goes to the front of the queue; if the background worker still does not pick it up, RIPPS2 saves it directly. The message then says what the worker was doing: send us a photo of it.
- Storage is home: the background drive checks slow down on the other tabs and pause while a CD plays or the file browser is in a drive.
- **L2 + R2** picks a random game on the info page too.
- Game art and the info page slideshow fade in instead of popping.
- Long descriptions scroll slowly so you can read them all.

### Settings
- **BOOT LOCK** (General & System, above IGR Path): with PS2BBL or PS2BBL Extended installed, the console starts straight into RIPPS2. Off puts back what PS2BBL started before. Turning it on fills an empty IGR Path with RIPPS2's path. Hold a PS2BBL hotkey at power on to reach anything else.

### Memory Files
- **EDIT** is the first action on a file and opens the text editor.
- Cleaner grid icons (the exit door and power symbol redrawn).

### Look
- The PS2 mark is thicker and drawn from the SVG. While something loads, it breathes in the corner (the swirl is gone). It flies smoothly between the tabs, with the coin flip end to end.
- **RIPPS2 Sleek:**
  - True lowercase on the keyboard and in typed text.
  - A flagged 1 (no more I/1 mix-ups).
  - Clean letter shapes: no nubs on R, no stray corners on the diagonals.
- Towers are drawn with softer, steadier edges for CRTs; the orbs' plasma tails grow out of the orb.
- Error messages put BACK where every other screen does.
- **About** shows the build number, and credits PS2BBL and the CD player.

### Known issues and asks
- If a settings save still shows "device busy", or "Settings saved ... (SAVED DIRECTLY: ...)", please send a photo: it says what the background worker was doing.
- If an audio CD says its table of contents could not be read, please send a photo: the message carries the disc's own bytes.
- The CD player's sound can only be checked on a console (PCSX2 cannot play audio CDs from images).
- BOOT LOCK needs PS2BBL already installed; writing its config can only be checked on a console.
