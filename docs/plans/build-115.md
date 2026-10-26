# Build 115: the first real-hardware run on the SD2PSXTD (the user's report, 10/25/2026)

Hardware: the user's PS2 with LinkRetro's SD2PSXTD v1.2 (sd2psx board) on sd2psXtd firmware 1.4.0, a 32 GB microSD
formatted MBR + exFAT (32 KB clusters) with the lean BOOT card (channel 1: sd2psXtd's PS2BBL Extended card, OPL and
uLaunchELF removed, RIPPS2/RIPPS2.ELF = the v1.1.4 hotfix ELF, PS2BBL AUTO -> RIPPS2), 9 PS2 games in DVD/, their art
and CFGs, EMBER (Digimon World) and POPS/POPSTARTER.ELF. RIPPS2 boots from the card; Burnout 3 from the internal HDD
launches fine.

Status: in progress (patch 0115 on main). The first sections below are the plan from 10/25 evening; the
lettered sections after them are the first run's notes, kept for their findings.

## The plan from here (10/25 evening, after the second hardware run)

The user tested the CI build of d4e9631 (run 40222153158) on the SD2PSXTD: the pad still lagged and jumped while MMCE
loaded, the right stick stopped tilting after the load, Burnout 3 from MMCE still hung (black screen a long time, the
logo's sound, nothing, a white screen 5 minutes later; from Memory Files the logo came sooner, then the same hang),
Digimon World (Ember) did not start, and copying a new RIPPS2.ELF onto the boot card failed with no message (the file
kept its old size; after erasing it, the new copy never arrived). Then a batch of navigation, sidebar and text requests.
Everything below is grouped into rounds so each build is tested as a group. Rounds 1 to 3 go into 115; round 4 releases.

### What the firmware source says (sd2psXtd main, read 10/25)
- **The device's own game switch is late.** With GameID on in the device, it watches the play history file: it sees the
  history write only when that sector is flushed to the SD (after 100 ms without card traffic) and acts only after 2 s
  more of quiet (`HISTORY_WRITE_HYST_US`). Build 115's wait (1.5 s for the busy bit) gave up before that, so the switch
  could start after RIPPS2 had handed off and the game was streaming. Creating or loading the game's card runs only
  while MMCE is idle (30 ms slices), and a streaming game never lets it. That fits the late logo and the hang.
- **The busy bit** (MMCE GET_STATUS) is set only while the device creates or loads a card. Card writes waiting to be
  flushed are not shown, and RIPPS2's own MMCE reads during a wait stop the device's progress.
- **The device's main loop** draws its OLED screen between MMCE requests; its README warns that long names that scroll
  make MMCE games stutter. The boot channel was named "PS2BBL + RIPPS2" (now "RIPPS2").
- **mmceman holds the SIO2 lock for a whole read** (all of a 16 KB fileXio piece, the device's SD time included); the
  pads share that lock. The menu's mmceman runs with no pacing; only the in-game mmcedrv gets RiptOPL's 5 wait cycles.
- **Card writes** go to the device's RAM at once and reach the SD later, in 100 ms slices that stall MMCE meanwhile.

### Round 1: MMCE, the pad, and launching (hardware first)
1. **GameID on by default** (`mmce_gameid` = 1, set once by a 115 migration, the user's choice kept after). Every MMCE
   launch (OPL core, Neutrino, Memory Files) stops RIPPS2's own MMCE reads (art, lists, caches), sends the game's ID,
   and waits on screen until the card is ready (the busy bit clear and the file system answering), with the seconds
   counting and no 3 s cap; START skips. With RIPPS2's GameID off, the wait covers the device's own switch (at least 4 s
   after the history write). This is "make the card before the game reads".
2. **Pad reads that miss keep the last buttons.** A frame whose pad read failed (the bus busy) counts today as nothing
   pressed, so one press becomes several: the cursor jumping. The last buttons are kept for up to 250 ms; past that,
   held buttons are let go and nothing repeats until a fresh read. The right stick also reads in padman's FINDCTP1 state,
   and DualShock is asked for again whenever the pad reports digital after a stall.
3. **MMCE reads paced in the menu.** Art and list files are read in pieces of at most 8 KB with a yield between them,
   none while a button is held or for 150 ms after a press (the pad breath MX4SIO has), and never two MMCE readers at
   once.
4. **No card writes during MMCE work.** Settings, recents, the master list and the play history wait until MMCE has
   been quiet a moment before they are written to the boot card.
5. **Lists load once.** Each list shows from its cache at once. A paced background check reads the drive. When the
   drive's list differs, the refresh glyph pulses and SELECT takes the new list. When it matches, nothing on screen
   moves.
6. **A hardware log.** A RAM log records pad misses, the longest pad gap, MMCE request times, the busy bit and each
   launch step. STATUS > SAVE DIAGNOSTICS writes it to the SD or a USB stick, so a hardware run can be read here.
7. **Memory Files copies are checked.** Each copy reads back its size and CRC and says when it fails. A copy to a card
   in an SD2PSX warns to wait a few seconds before power off, because the device writes the card to its SD later.
8. **Ember from MMCE.** Digimon World did not start: check which devices Ember reads (mmce paths, its BIOS, the games
   folder) and either make the launch work or say plainly what Ember needs.
9. **Control test (the user).** To tell a RIPPS2 problem from a device or SD one: the same Burnout 3 from the same SD
   with the ps2-mmce OPL and with NHDDL + Neutrino, and in RIPPS2 with the In-Game Menu off and with the Neutrino core.

**Round 1 progress (10/25 night):** done in 0115: items 1 (Game ID on by default; the send waits to see the switch start,
then waits it out on screen, START skips; the history-only path waits 4.5 s), 2 (missed pad reads hold the last
buttons for 250 ms, no repeats on old data; right stick in FINDCTP1), 3 (MMCE art reads wait while a button is down,
with a gap between pieces), 5 (MMCE only so far: one quiet background check of a trusted list; a change pulses SELECT's
hint), 6 (the hardware log, SAVE DIAGNOSTICS, written beside RIPPS2 before MMCE and Ember launches), 7 (case-only name
matches on a card are the same file; an SD2PSX card write says how long to wait before power off). Left: 4 (card writes
during MMCE work: decide from the first hardware log), 5 for BDM and SMB (a drive can go while its check is
queued: needs the device data kept alive or the check keyed by slot), 8 (Ember on MMCE: the setup on the SD checks
out, SCPH-1001 BIOS and a good CUE; Ember never made its MC1.vmc, so the log decides), 9 (the user's control test: OPL
MMCE beta 2 is on the SD as PS2BBL's R1).

### Round 1b: the SD2PSX as a home for RIPPS2 (the user, 10/25 evening)
1. **AUDIO beside RIPPS2 on the SD** (`mmce?:/RIPPS2/AUDIO`). It is RIPPS2's own folder now, so it is searched first;
   it is quicker to read than the card and has room for music. BIOS Sounds, BIOS Music and the CD player write there.
   The boot card keeps only PS2BBL and the settings save. Check that mmceman is up before the boot's sound load when
   RIPPS2 starts from MMCE.
2. **The device's cards in Memory Files.** `MemoryCards/PS2/<folder>/<name>-<channel>.mcd` are raw 8 MB cards, the same
   format as an OPL VMC, so they open like folders (copy saves in and out, export and import PSU). A CARD BANKS view
   lists the BOOT channels, the per-game cards and the named cards. From it: make a new card, copy a card, and move a
   card to the holding folder (never a hard delete).
3. **Card to card in MCKILLA.** A VMC or an SD2PSX card is written whole onto a physical card in slot 2 (and a physical
   card is backed up as a `.mcd` bank on the SD). Today MCKILLA writes a VMC's saves back one by one.
4. **Folder and file tooltips in Memory Files.** Say what each known folder and loose file is for: ART, CFG, CHT, CD,
   DVD, VMC, THM, LNG, APPS, POPS, EMBER, RA, RIPPS2, AUDIO, MEDIA, MemoryCards, BOOT, .sd2psx, RIPPS2.LST, games.bin,
   settings.ini, BootCard.ini, `*.mcd`, `*.crp`.
5. **MEDIA from MMCE.** A PNG opens and tilts with no pad lag, and AVI video plays without stutter. Reads ahead in paced
   pieces, with the pad reads kept clear (round 1).

### Round 2: navigation and the sidebar
1. **Layout > Sidebar Style**: Split (today's dark strip and the accent beside it) or One Piece (one bar, the same overall
   width, the glyphs centred in it). The lit tile slides to the new category and the glyphs crossfade when it changes.
2. **The bar and the drawer slide open** with RIPFLOW's cover easing (both the narrow bar and the opened drawer).
3. **Category Bar becomes "Category/Sidebar".** On the sidebar, Fade When Idle slides the bar away; any press brings it
   back, a little quicker than it left.
4. **Category Layout gets "Menu"** as its last choice: no bar and no sidebar; the categories are in the START menu, as
   on a legacy theme.
5. **Sidebar mode owns Left.** Left always goes to the sidebar. Right never cycles the sources, and Up/Down never
   changes the source on RIPFLOW. The cancel button (O) opens the Storage drawer on every page and view. With the
   sidebar off, Left/Right work as the theme sets them, with L1/R1 on the categories.
6. **Memory Files ORBITS in sidebar mode**: L1/R1 change the formation and Left opens the sidebar, as on Launch Disc.
7. **RIPFLOW: L1/R1 step one cover**, and repeat while held, like the D-pad.
8. **Hints and Glyphs fade.** A new option in Layout's top set, on by default for every theme (key `hints_fade`, written
   into Adapt and Adapt Rx). When the hint line's glyphs change it fades in with the covers' own fade at 0 ms; the same
   glyphs stay put; modals included. A **Guidance** choice fades the glyphs in after 4.2 s idle, with RIPFLOW's L1/R1
   glyphs beside the centre covers.
9. **Starred Games.** R3 held 4.2 s turns the star display off: no stars, no indent, no R3 hint, names from the left
   edge at full width. Held again turns it back on (Manual, stars as last set) and stars the game under the cursor.
   Default: Manual with the stars hidden; R3 still stars a game. The tooltip says all of this.

### Round 3: text and page polish
1. ACHIEVEMENTS and STATUS: the row names in Roboto on every theme (a theme's font keys can still override).
2. Notifications: one Roboto, the built-in bold. Text Weight's global choice becomes Normal or Bold (it shows no change
   today); theme keys keep all three weights.
3. One title position on every page of the same kind. The PS1 game settings title sat too close to the bar, and its
   sentence ran off.
4. Network: the title and its line spaced like the other pages. Audio: the divider lines moved to fit the text, which
   stays where it is.

### Round 3b: slim themes and the theme engine (the user, 10/26)
1. A theme of two files: an image a theme names but does not ship is RIPPS2's own of that name (badge folder names read
   as RIPPS2's: rating/0_Rating is Rating_0), unless use_default=0. Planet N Condensed built in
   (builtin:ripps2condensed). Adapt and Adapt Rx edition 115 are conf_theme.cfg + SCR43.png (themes repo b31725b,
   pushed with the release: it needs this build).
2. RIPPS2's badge set: badge_set=ripps2 and Hints and Glyphs > Badge Set (Theme / RIPPS2, config ripps2_badge_set);
   Players_1..4 drawn in RIPFLOW's style (make_glyphs.py), Parental_* from Adapt; all 8-bit.
3. loading_mark=corner|center places the busy mark; load0..7 never drawn.
4. category_layout=row|sidebar|menu is the one key; unset is menu for disk themes; categories=three|storage read only
   where it is unset; Layout > Category Layout's Across the Top / Sidebar bring the bar onto a menu theme.
5. PS1 rows' covers in the square PS1 case on every theme (thmItemIsPs1).
6. Held SELECT on List: the THEMES window fades in empty at 1 s with the notch wheel filling to 4.2 s, where the
   themes fill it; let go and it fades, the list refreshes (ripps2ThemeHold / ripps2ThemeHoldRender).
7. Every message box and wait screen in Roboto Condensed 400, its own case (RIPPS2_MSG_FONT, message_font=<slot>).
8. Boot: a black frame while the settings load, then the towers in the Color Theme from their first pose;
   ripps2PaletteSync every pillars frame, so the Color Sweep moves through the boot zoom.
9. Themes releases: one rolling release, "RIPPS2 Themes" on tag `rolling` (10/26; the numbered ones deleted, tags kept,
   notes in B:/Webpages - Projects/RIPPS2-themes-releases-archive-2026-10-26). Update it in place for edition 115.
Site (pushed 10/26): the shelf's ten hats, each a Color Theme wave on the towers; portrait phones get the letterboxed
player (letterbox.js).

### Round 3c: the user's hardware notes of 10/26 (round 3b ELF on the SD2PSX)
Working on hardware: games from MMCE storage (OPL core); Neutrino installed by RIPPS2 and booting Burnout 3 from MMCE
(no in-game menu: Neutrino has none, like Ember; it showed an MMCE message too small to read); Ember Digimon World over
MMCE; POPSTARTER from the app list and from Memory Files' ELF; the USB VMC prompt (FAT32) and IGR back; BGM on boot;
the Color Sweep through boot.

Crashes and data first:
1. CRASH: held SELECT, the theme panel never reaches the screen and the console hangs: a race with the cache
   setting dropping the list (instead of the lazy refresh) while the panel comes up.
2. "Could not write settings to mmce0:/RIPPS2 (error 19)".
3. Manual sources (MMCE, HDD): All Games shows no HDD art until HDD is started by hand; then the list loaded,
   vanished, loaded again; the art came but not the CFG metadata (the HDD page has it). Auto boots faster but the
   list still refreshes instead of trusting the cache.
4. The MMCE controller bug (pad input lost while MMCE loads): research a wait or fix; a note in the MMCE menu and an
   experimental fix on by default there. Game Sources / STATUS / Cache: say Auto on the drives that are connected
   is fastest.
5. POPSTARTER: a VCD's launch says POPS files are missing (STATUS's search says so too) though it launches fine.
Sound:
6. Menu and red screen music: not playing after the rip until toggled off and on (quick fix); STATUS says 14 sounds
   after ripping two; a reboot still had neither. The BGM is set per theme: the ripped BGM goes to every built-in
   theme at once (Menu the default when both are ripped).
7. The BGM plays on every screen but the CD player, the media player and the audio pickers' previews; it is unloaded
   there and brought back (not just silenced).
8. Media: the ripped music CD and BGM .wav in MEDIA (HDD) do not play; WAV playback in the media player. Rips may go to
   the MMCE's MEDIA too. (Answer: which other video and audio formats are possible.)
9. Ripping: a modal that explains Memory Files opens with the rip to paste where it goes (Triangle for actions,
   Paste, then RIPDISC confirms and writes with the laser): O OK alone, a message not a choice. Other messages that are
   only information get the same single button.
Sidebar and navigation:
10. Sidebar styles renamed Classic (Split) and XL (One Piece); on Adapt the one piece showed the split bar on the
    list and info pages and none in the morph between them: transition frames for either style, the icons staying put;
    Adapt keys the sidebar drawn throughout.
11. Info pages with the sidebar: Left reaches the icons; Up / Down move in the list; Right no longer cycles games
    (Left / Right are the sidebar's, as on the list); Circle backs out to the list.
12. RIPFLOW: Left is the covers' (the sidebar ignores it); a sidebar on by the theme's default hides itself; on by the
    user's choice it is their flow.
13. Memory Files: Left / Right the sidebar, L1 / R1 the formations only.
14. Vertical moves along the sidebar: from STORAGE up to LAUNCH DISC, from Storage's last source to MEMORY FILES.
    Circle with the sidebar hidden pulls it out to the icons, lit, not the drawer.
15. Layout: Category Order before Hints and Glyphs Fade; its tooltip says it swaps the icons too.
16. Hints: Cross RUN left of the source name, Circle SOURCE right of it (OSDSYS style); keys so RIPFLOW has it and a
    theme can space its hints like the OSDSYS (Adapt shows how).
17. Adapt: the text beside a glyph (font6) in RIPPS2 Sleek Case, as its hints.
18. Tilt (right stick) not working, even with Auto sources.
From the round before (10/26 morning):
19. The SD2PSX "getting this game's memory card ready" screen: wrapped and padded like the message boxes (every
    guiRenderTextScreen).
20. IGR back to RIPPS2 from the in-game menu is less safe than the BIBLE / PS2 browser boot path: the IGR Path tooltip
    and the README say leave it off and set up BIBLE; the issue gets a three-step answer.
21. BIBLE's PS2BBL 1.2.0 install message titled "RIPPS2 BIBLE: BBL 1.20", naming its 0 ms start (which PS2BBL Extended
    does not allow); the install failed over an existing PS2BBL Extended install on the boot card.
22. Game settings: Set Metadata merged into the Change Name row, reading "Set Metadata (Rename)", spacing as is.
23. POPSTARTER's own in-game menu (a lite RIPPS2-themed one): POPSTARTER is closed, so only its own IGR is possible;
    noted, not planned.
24. Issues (build 114 reports): #3 Exit Game black (IGR Path set to RIPPS2.ELF): answered with three steps. #4 Ember
    PS1 and PS2 games never together in All Games: fixed (sources fill their PS1 lists while All Games shows PS1).
25. BIOS Music turned to noise from 2:33: a retriggered key never ended its note (rbsSequence); fixed, levels
    re-measured, rendered clean on the PC (C:/msys64/mingw64/bin/gcc, -DRIPPS2_BIOSSND_HOST_TEST).

Round 3c progress (10/26, pushed): 1 (guiLock taken inside a frame), 2, 4 (Pad First on; the DIAG shows the pad's
misses), 5 (asks once a drive, says POPSTARTER may find them), 6 (pick goes to Menu, restart, never "playing" with
nothing playing, own homes, STATUS counts tracks), 8 (.wav / .ogg play in Memory Files; MP3 would need a decoder),
9, 10 (names, the bar through the morph, Adapt draws none of its own: one piece), 11, 12, 13, 14, 15, 16 (hints_flank),
17, 19, 20, 21 (title, 0 ms, the rename lets go of a protected folder, DIAG lines), 22, 24, 25.
3: a source's first answer clears the metadata and cover memos; the boot refresh against Trust Cache still to check.
7: the CD and video players already stop and restart the music; checked, nothing else silences it.
18: tilt needs the pad in DualShock mode; RIPPS2 re-asks only in a clean poll, which MMCE traffic rarely gives (the
ANALOG button works).

### Round 4: release
- Translations: build 115's 58 strings and its new labels in the 32 languages.
- Lab rounds in PCSX2: navigation and sidebar, Recent Games, the list pulse, STATUS LOADING, the BIOS Sounds room check,
  art names, Neutrino on the exFAT HDD.
- A hardware round on the SD2PSX with the user: MMCE input, Burnout 3, Digimon World, the sounds rip, EXIT back to
  RIPPS2.
- Themes edition 115 (`hints_fade`, the sidebar style keys) and the glossary; CHANGELOG; README (the ELF is 2,641 KB,
  about 2.6 MB); the psx-place post built from the user's template (tools/discord/psxplace-post.bbcode); the Short
  (repo and release only); release v1.1.5-beta; the Discord "Test me | Build 115" post.

### The SD2PSX card as set up on 10/25 evening (D:)
- `RIPPS2/RIPPS2.ELF` on the SD: build 115 (e6f0a21). PS2BBL's AUTO starts `mmce?:/RIPPS2/RIPPS2.ELF` first, then
  `mc?:/RIPPS2/RIPPS2.ELF` (also on the boot card), then the browser. An update is one file copied on a PC.
- BOOT: BootCard-1/2/4/6/8.mcd all the same card (PS2BBL, RIPPS2's settings save, RIPPS2.ELF); BootCard.ini channel 1
  "RIPPS2", MaxChannels=1.
- THM: Adapt and Adapt Rx (edition 114). The holding folder keeps the old cards, the Burnout 3 card the device made and
  the APPS test build.

### Answers given to the user
- GameID on by default: yes. RIPPS2 sends it and waits until the card is ready before the game starts ("create
  before reading"). The device's own switch is too late for a streaming game.
- Where RIPPS2 lives on an SD2PSX: on the SD (`mmce?:/RIPPS2/RIPPS2.ELF`), started by PS2BBL from the boot card, which
  keeps PS2BBL and RIPPS2's settings save. Loading is quicker, an update is one copied file, and nothing has to be
  written into a card image. The boot card's own copy stays as the fallback.

## A. MMCE (first)

### A1. Input blocked and erratic while MMCE works
- Booting with the last used device = MMCE, the pad is dead or erratic until the card's list is in, even before the
  cache shows; the right stick tilt misbehaves too (the user: "it even blocks the right stick", "the controller is
  bugging terribly when mmce is loading stuff"). Browsing and menus should work while it loads, as on the HDD.
- Likely cause: MMCE and the pads share SIO2. Long MMCE transfers (mmceman) starve padman's reads, so presses are
  dropped and the stick reads stale or zero. To check: where the MMCE list read runs (mmcesupport.c on the IO thread?),
  how big each request is, and whether anything yields between them. Fix direction: show the cached list at once, read
  the card in small pieces with a DelayThread between them, never during a pad read window, and pause MMCE work while
  the user is pressing buttons (as MX4SIO got in build 110).
- The "right stick tilt bug on everything from covers to the PNG viewer" is probably this; confirm with the user what
  the tilt does (stuck, drifting, jumping) and whether it also happens with no MMCE inserted.

### A2. Games from MMCE: very slow, then a hang
- Burnout 3 from MMCE: the PS2 logo's sound came over 5 minutes late, then it hung, then a white screen.
- The game files are good: all 8 retail ISOs on the card match Redump byte for byte (size, CRC32, SHA-1, checked
  10/25 against libretro's Redump PS2 DAT: Auto Modellista, Aqua Teen, Burnout 3 (USA, Canada), Katamari Damacy,
  We Love Katamari, Ratchet & Clank, Going Commando v2.00, Up Your Arsenal; GTA VC Debug is a prototype, not in Redump).
  Card copies were checked by size after robocopy; hash them on the card next time it is in the PC.
- "The sizes are off from the ones on my HDD": the HDD copies came from another source; the card's are the Redump ones.
- To find: which core launched it (OPL core with mmcedrv, or Neutrino), the game-ID card switch at launch, and the
  read speed the console got. Next session: a debug ELF with EE SIO logging is not possible on hardware, so add a short
  on-screen or file log of the launch (core, mode, the MMCE slot, the switch result) and test the same game with each
  core. Also check sd2psXtd's own notes on MMCE game loading (settings for speed, known slow games).

### A2b. What the SD showed (10/25, card back in the PC)
- The microSD is not slow: through the PC's USB reader, random 2 KB reads 0.59 ms median (0.9 ms worst), sequential
  31 MB/s, an 8 MB card written in 512-byte write-through pieces in 16.7 s (490 KB/s, worst write 24 ms). All 9
  ISOs and the boot card are one extent each (no fragmentation).
- GameID cards: MemoryCards/PS2/SLUS-21050 (Burnout 3) and SLUS-20642 (Auto Modellista) are 4.2 and 4.6 MB, not 8, and
  Burnout 3 has two .crp files of ~88 KB (sd2psXtd renames a wrong-size card to .crp and makes it again). The
  firmware writes a new card only while ps2_mmceman_fs_idle(), 512 B at a time with a flush per slice; a game
  streaming over MMCE keeps it busy, so the card never finishes before power off. RIPPS2 has mmce_gameid=0, so these
  came from the device's own history-file tracking. Test MMCE launches with the device's GameID off, to take the
  switch and the card writes out of the picture.
- BOOT/BootCard-8.mcd exists (a blank formatted card): boot channel 8 was selected at some point (channel down from 1
  wraps to 8, and the device keeps the last boot channel). A power on on channel 8 has no PS2BBL: that is the likely
  "the exploit fails sometimes".
- The boot card (RIPPS2's settings live there): 3,811 KB free; RIPPS2/AUDIO was never made.
- The user's settings_riptopl.cfg: exit_path=mc1:/APPS/RIPPS2.elf (a stale value from the old setup: the "hardcoded
  mc1 path"), mmce_mode=0, mmce_slot=2, mmce_wait_cycles=5, mmce_use_alarms=1, default_core=0 (OPL core),
  popstarter_path=usb:/POPS/POPSTARTER.ELF, enable_pccf=0, ripps2_recents=0, last device 15.

### A3. Other card items
- BIOS Sounds rip: "The sounds could not be written to mc0:/RIPPS2/AUDIO/. Is the drive full or write protected?" on
  the BOOT card. sd2psXtd's card manager has no read-only BOOT card; the lean card had 3.98 MB free before RIPPS2's
  settings. Check the space left, how RIPPS2 makes the AUDIO folder on a card (mkdir of a nested path on mcman), and
  offer the MMCE's SD (mmce0:/AUDIO) when the card is short.

## B. The in-game menu's exit
- The user: the in-game menu should know the exit path to the RIPPS2.ELF that launched it, not a hardcoded mc1 path,
  and show it properly.
- Today: gExitPath empty means "Browser"; ee_core's exit loads only from mc and mass (USB) (padhook.c reloads
  SIO2MAN/MCMAN and, for mass, USBD from SYS-CONF); ripps2BootLockIgrPath fills it from the boot path only for mc/mass.
- Plan: fill the exit path from RIPPS2's own boot path at every launch unless the user set one, and show it in the
  menu. The catch on an SD2PSXTD: with GameID on, the device switches to the game's own card at launch, so
  mc0:/RIPPS2/RIPPS2.ELF is not on the card in the slot when the user exits. Options: switch the MMCE back to the BOOT
  card before loading the exit ELF (mmceman's switch is not in ee_core's exit path today), exit to the browser and let
  PS2BBL start RIPPS2 again, or keep a copy of RIPPS2 where the exit can reach it. Decide with the user.

## C. Cache: trust it, per device, and a light gate file
- The user: the cache lets the list show, but settings still take a while and the cached list then refreshes itself,
  a hitch. Show the cached list and trust it (launch from it, starting the game's drive on launch) until a refresh is
  asked for (SELECT) or a device's own refresh writes its cache.
- A Cache page per device that has one, in an order the user sets; boot stops at the first cache it finds.
- "Create master cache" in the Cache page: one very light file, suggested next to the ELF on the memory card, so boot
  reads it first. If it has to live elsewhere, a tiny gate file next to the ELF points to the settings and the caches.
- STATUS gets an optimisation part: where settings and caches are read from, which is fastest, and a button to put
  the master cache and settings next to the ELF. Tooltips that explain how to get the fastest boot.
- Drives on Manual (the default) start on launch while their list shows at once from the cache.
- STATUS and Cache link to each other; going back and forth does not stack (Back returns once, then to the parent).

## D. Storage sources
- PC Card CF: hide its page; it is the fat's HDD-bay CF adapter, so fold its detection into the HDD's.
- Recent Games: show it in the sidebar like the drives, with its own on/off; one row with a count 1 to 99
  (today ripps2_recents 0..9). Ask: "manual start for drives of whatever game chosen is in the list" means a recent
  game's drive starts when you launch it, as All Games does.

## D2. Art names from the OPL Manager database (issue akilluminati47/RIPPS2#2)
- The OPL Manager GameArt database (and tools built on it) names backgrounds `<ID>_BG_00.png` to `_BG_06.png` and
  screenshots `_SCR_00`, `_SCR_01`; RIPPS2 reads `<ID>_BG` and `_SCR`, `_SCR2`... only (png, then jpg). Fall back to
  `_BG_00` when `_BG` is missing, and `_SCR_00`, `_SCR_01` for `_SCR`, `_SCR2`, through the same artIndexMayExist
  check so a miss stays free.
- PS1 art keys: VCD file name without .VCD, Ember's EMBER/games/ folder name, apps' ELF name with .ELF (as mapped in
  Luden02/OrbitPS2-Manager#48, which OrbitPS2 Manager follows).

## E. Settings tooltips
- When the selected row is low on the page, the tooltip slides up so the rows above and below stay visible.

## F. Lab
- 10/25 night: the background driver's key presses stopped reaching PCSX2 for every ELF and drive (the same RIPGRID
  walk that worked at 01:28 failed at 03:14). Shift/Ctrl/Alt not stuck. Find out before the next lab run (does the
  foreground driver work, did the hidden desktop change, NVIDIA overlay or Xbox app focus).
- The 1080i info-page captures for the thumbnail (all 9 games, RIPPS2 theme) are still to do; t114-sdmirror.raw is a
  lab drive with the card's games, art and CFGs.

## Progress (10/25, end of session: usage limit reached)
Done in patch 0115 (pushed, CI building, NOT lab-tested yet as a whole):
- Art read under every name (index keeps real names: any case, .png/.jpg/.jpeg; decode by content, shrink big
  pictures; OPL Manager _BG_00/_SCR_00/_SCR_01 both ways; PS1 disc ID and XX.<name>.ELF keys). Host tests
  test_art_names.py + test_udpfs_art.py pass locally; issue #2 answered.
- Pad: DualShock mode asked for again in a quiet second when a pad is left digital (dead right stick).
- MMCE: nothing read while the card says busy (mmceCardBusy, devctl 0x2); OPL-core MMCE launch writes the play history
  first and waits (on screen) while the card makes the game's memory card (mmceReadyGameCard).
- SELECT refreshes coalesce (ioPutRequestUnlessWaiting); Trust Cache (gRipps2TrustCache=1, sbSnapTrusted) in MMCE,
  SMB, BDM: a cached list stands until a refresh.
- All Games starts at boot even when every source is Manual (lab repro on 1.1.4: empty "Start Device" for 45 s).
- Lab: ps2bg.ps1 closes PCSX2's hidden Error dialogs (the PC's audio device was gone).
Left: Trust Cache row + its strings on the Cache page (config key ripps2_trust_cache), exit path following the boot
path, PC Card CF fold, Recent Games source 1-99, tooltip slide, BIOS sounds space check, STATUS<->Cache link and the
STATUS loading section, translations for new _t strings, lab rounds, release v1.1.5-beta, the Short, Discord post,
the 1.1.5 ELF into the SD's boot cards (BootCard-1/2/4/6/8). SD card hash result: scratchpad isohash-card.tsv.

## Handoff (10/26, end of session)
The next session starts from `build-115-handoff.md`: where things stand, the user's last requests, the steps to the
release in order, and the translation kit in `tools/lang115/`.
