# Builds 95 to 99: the 2026-10-11 notes, sorted into passes

The notes came in out of order; here they are grouped so each build needs one lab session in PCSX2, and real
hardware only twice: **build 95** (the sound and stability fixes testers are hitting now) and **build 99**
(everything else). Each pass: patch, host tests, CI, one scripted lab run, fixes folded into the same patch,
then tick it here. ripto's RiptOPL reference (device handling, artwork keys, GameIDs, launch handoffs) drives
build 99. FifthFox's build 94 report (SCPH-39001: APA SSD, MMCE, MX4SIO, iLink with a Seagate HDD, USB, HDMI
converter) added the regressions now in build 95, the POPSTARTER and iLink items in build 99, and build 100.

## Build 95: sound and stability (released v0.0.95-alpha, hardware session 1)
- [x] **Boot freeze with ripped sounds in AUDIO.** Reproduce in the lab (rip on PCSX2's BIOS, reboot), find
      why (suspects: the long boot/launch rips overflowing SPU2 RAM, the early boot sound, two loads at once),
      and make loading foolproof: a size and SPU2 budget check per sound, a bad or oversized file skipped and
      named, never a hang.
- [x] **No built-in sounds.** OPL's eight built-in `.adp` leave the ELF. Sounds come only from `AUDIO`
      (BIOS Sounds > Rip, or RIPPS2 Audio Studio); without them RIPPS2 is silent, and STATUS says how to get
      them.
- [x] **Clean, snappy sound effects.** One voice per sound, a new press cuts the old one, a held cursor never
      stacks, mutes in waves or lets stale sounds play later. Measured from lab captures (gaps and overlaps in
      the recorded audio), not by ear.
- [x] **Rip quality.** No beeps, pops or clicks: the rip's synthesis run on the PC against a BIOS dump and
      compared with the reference recordings (click detector, envelope ends, loop points, noise voices).
- [x] **`.adp` preview** in Memory Files: Cross plays it, Back stops it.
- [x] **The trusted IGR stays primary.** With In-Game Menu off (the default) the combo is exactly OPL's IGR and
      nothing of the pause menu or the hunt list is involved. The menu's tooltip calls it experimental and
      warns about cutscene audio; look at the cutscene skip and crash reports for anything that can be made
      safer without hardware.
- [x] **RIPFLOW is a plain list** with only background art (the user's ELF and FifthFox on hardware): find what
      broke its built-in theme, and a test that parses every built-in theme cfg.
- [x] **MX4SIO shows up nowhere** (it does in RiptOPL and did in earlier builds): find the regression.
      REOPENED in build 98: FifthFox on build 95 still has no MX4SIO (patch 0095 changed nothing there).
- [x] **JPG loads stop partway** (a quarter of the picture, not always the same file): read the whole file before
      decoding (a short device read ends libjpeg's input early). Same for RIPGRID, which shows JPG covers as
      text.

## Build 96: settings and menus
- [x] Backing out of any submenu lands on the row that opened it, not the page's top.
- [x] Colors and More: a tooltip on every row, a **Theme** value on most rows, and the Grid backgrounds tinted
      by the color theme.
- [x] Flow and Grid: **Flow Cover Count** and **Flow Cover Size** (the flow's own rows say so).
- [x] STATUS scrolls like the settings pages; the support line naming the user is removed.
- [x] Neutrino: a clear description of the automatic arguments.
- [x] Settings pages read in one plain face on every theme (Adapt's settings face), not each theme's styled
      fonts.
- [x] Devices: auto start can be **Last Used**, the device and page you were on.
- [x] Page buttons: Theme, L1 / R1 or L2 / R2; theme key `page_buttons=l2r2`, which RIPGRID uses.

## Build 97: Grid and Flow
- [x] RIPGRID: the name under the grid in RIPPS2 Sleek Bold; the grid centered on the content, ignoring the
      sidebar; Right at the right edge goes to the next page and Left at the left edge to the previous one
      (no wrapping).
- [x] Case flip on a 0.42 s right-stick hold (was 2 s), on RIPFLOW too, where it replaces the automatic front
      and back crossfade.
- [x] RIPFLOW info page: right-stick tilt on the screenshots.
- [x] RIPGRID on HDMI and HD modes (FifthFox: "optimized for a CRT"): check every video mode and fix its layout.
      480p, 720p and 1080i lay out centred. 720p FROZE the release build: a lab save state read against the
      build's symbols showed the GUI thread blocked in a pad actuator-align RPC the IOP never answered (the pad
      still busy with its init), holding the GUI lock. The align now waits for an idle pad. Also fixed on the
      way: fntFitString walked past the end of its string (a stray letter under a coverless tile).
- [x] Older OPL themes: load a set of classic themes in the lab and fix what draws wrong next to RiptOPL.
      Grunge and Adapt RiptOPL draw their lists, menus and settings as RiptOPL does on build 97.
- [x] Found in the lab: a list opened on the remembered game as its top row, so near the end of a list it
      showed a few games over empty rows (it looked as if games were missing). A list page is always full now.

## Build 98: Memory Files
- [x] **A memory card slot disappears after START DRIVES** in Memory Files: both cards must stay reachable.
      A slot is asked through mcGetInfo (it clears the "changed card" the MMCE ping leaves) and read more than
      once; MX4SIO stays out while any card is in slot 2. (PCSX2 has no MMCE or MX4SIO: hardware confirms.)
- [x] **Deleting can fail and must never corrupt**: error 16 deleting `bgm_03` from the HDD's AUDIO folder, e0
      deleting the file itself. Stop the music (or anything else) holding a file before it goes, retry, and
      say plainly what could not be removed. E16 was the music's open file; E0 a remove whose code never
      reached errno. Now: the music lets go and comes back, a removal is checked gone, reasons in words.
- [x] **Copying an ELF from USB to the memory card gave e999**: find what that code is and make the copy work.
      999 was RIPPS2's own stand-in for a short write: the card was full. Short writes finish, and a paste
      that cannot fit says CARD FULL with the KB it needs before it writes anything.
- [x] Sounds per event: a disk theme's own first, then the AUDIO folder's (Adapt ships 6 of 15, so ripped
      launch, disc and save sounds were silent on it).
- [ ] **Stability while art loads** (user, 10-11): pressing anything while the list and the info page are still
      loading art must never crash (the HDD list on the RIPPS2 theme, into the info page, navigating while its
      images come in). Reproduce in the lab with a button storm, catch any freeze or crash in a save state.
- [ ] **The game's background art fades in as soon as it is decoded** on the main view: nothing ahead of it
      delays the fade. (Build 99 may take this further with RiptOPL's art loading round-up.)
- [x] **The music under load** (user: the BGM stutters and freezes too). Found in the lab: the PS2's Vorbis
      library refuses any stream whose Ogg serial has its top bit set (ov_open -132); ffmpeg picks serials at
      random, so about half of all music never played, Audio Studio's included. The reader now clears the bit
      and corrects each page's CRC; Audio Studio writes serials under 2^31 (its exe needs a rebuild). With a
      pilot-tone track (made by Audio Studio) the lab's music held through a button storm: no dropout, no stop.
      Hardware stutter is device contention: pass 99.
- [ ] **`.adp` preview cancel is robust**: a frantic press of play / stop / move never loops a load or leaves a
      voice playing.
- [ ] **MX4SIO missing** (FifthFox, build 95: SCPH-39001 with APA SSD, MMCE, MX4SIO, iLink HDD, USB; works on
      RiptOPL). Walk every MX4SIO path against RiptOPL 65d4b89 and its later fixes (load gates, the second
      probe, Game Sources, page visibility, MMCE sharing SIO2, slot 2 card access). PCSX2 has no MX4SIO:
      FifthFox confirms on hardware.
- [ ] **Grid tiles without a cover** (FifthFox, 95): the ISO's file name in very large text, sometimes past the
      tile, while game IDs are much smaller. A tile shows only the game ID (the name is under the grid), one
      size on every tile, always inside it; a game with no ID shows a clear tile.
- [ ] **A video that loads forever** (FifthFox, 95: an AVI "from web"): asked whether it was on a local or a
      network device. Reproduce, and make the player give up with a message instead of hanging.
- [ ] Flow and Grid settings text too large and cramped (FifthFox, 95): check it on the build 96 settings face.
- [ ] **mc1:/ must never vanish after START DRIVES** (user, 10-12, again: copying from USB or HDD to that slot is
      impossible; the only way round is starting the drives on Storage first). And the cards are MEMORY CARD 0 and
      MEMORY CARD 1 (mc0:/, mc1:/), never 1 and 2.
- [ ] **REGRESSION: the info page's background no longer fades in with the disc and the cover**, and its
      slideshow does not fade properly (user, on the RIPPS2 theme). Find what changed and restore it.
- [ ] **L2 / R2 on the Grid turn a whole page** (the set of covers on screen slides over, as at a row's edge);
      today they move one cover.
- [ ] **RIPFLOW tilts and flips like RIPGRID**: the centre cover on the main page tips with the right stick and
      turns over on a 0.42 s hold; on the info page the two screenshots tip as ONE sheet (today askew, each on
      its own pivot); the main page has no tilt at all.
- [ ] **Vignette Other Covers: Off, Weak, Full.** Weak is the default at half of today's strength (Full); no bright
      1 px line down a vignetted cover's side.
- [ ] **Background art blur** (Artwork settings): Theme, Off, Weak (33 %), Normal (66 %), Strong (100 %, today's
      RIPGRID frost). A theme key; Adapt and RIPGRID default to Weak.
- [ ] **Widescreen Grid layout**: its own rows under the Grid's in Flow and Grid (columns, rows, cover size)
      that apply only to the 16:9 HD modes (720p, 1080i) and widescreen, independent of the standard ones.
- [ ] **RIPGRID in capitals everywhere** (the theme's name on screen, in docs and in the themes repo), like
      RIPPS2 and RIPFLOW; a saved `<RIPGRID>` still finds it.
- [ ] **File tooltip**: resting on a file for 0.42 s shows its date, size and the other details wLE shows.
- [ ] **Paste overwrites when asked**: a name already there asks Yes / No / Yes to All (the choice highlighted
      in the modal), and an overwrite succeeds (it is skipped today).
- [ ] Devices show as `mc0:/` and `mc1:/`.
- [ ] Hold to scroll: after 0.42 s the cursor repeats at the Storage list's scroll speed.
- [ ] Card manager: hints with glyphs on its Actions modal.
- [ ] Picture viewer: Adapt's face, glyph hints that fit, no distortion zoomed in close.
- [ ] PS2 3D save icons (`.ico` / `.icn`) open in a viewer: the model, its texture and its animation.
- [ ] Text editor input bugs: reproduce first.
- [ ] Rip a save's 3D icon to the PC: the model as OBJ with its texture as PNG, one OBJ per animation shape.
- [ ] RIPPS2's own save icon: the bloody elf hat ringing its bell, animated, in the PS2 icon format (under the
      icon vertex limit, one texture), on RIPPS2's memory card folder.
- [ ] Launch from Memory Files: `.iso` / `.zso` with RIPPS2's loader or Neutrino, `.cue` / `.bin` in an
      `EMBER/games/<folder>` with Ember (`.vcd` with POPSTARTER already works). CHD: neither core reads it.

## Build 99: RiptOPL's identity contract (ripto's reference), then release (hardware session 2)
- [ ] **Loading and cancel round-up** (user, 10-11): every device's load speed tuned; the music on a path of its own
      so it never competes with art and lists (from RAM, or its own IOP stream), measured on hardware; RiptOPL's
      art loading performance; every cancel (art, previews, scans) robust to frantic input.
- [x] **Grid in widescreen** (FifthFox, 95): moved to build 98 (the Widescreen Grid layout rows).
- Noted, no change: RIPFLOW puts MEMORY FILES left and LAUNCH DISC right on purpose (category_order, a user
  setting). POPSTARTER from iLink crashes on 95 while Ember works (FifthFox): the POPS item below.
- [ ] Device names by driver, not slot: `mass0:` on the internal exFAT HDD says HDD, not USB (YOUR ACCOUNT
      said "on USB" in the lab). Same in Memory Files, STATUS, toasts and the launch report.
- [ ] Artwork and config keys exactly as RiptOPL: VCD basename, Ember folder name, ELF basename with `.ELF`;
      a PS1 GameID never replaces them. Check RIPPS2's own paths: Grid back covers, All Games, Starred,
      metadata, art fetch, recents.
- [ ] Grid's coverless serial: the PS2 startup ID or a verified PS1 disc ID only; a VCD or Ember name is never
      shown as a serial.
- [ ] PS1 identities never truncated to the PS2 startup field in RIPPS2's own buffers.
- [ ] POPSTARTER from the APA HDD (logo, then nothing) and from iLink (crashes once the BDM files are there): the
      BDMA driver must follow the transport, not the `massN:` slot.
- [ ] iLink PS2 games: Neutrino fails where the OPL core with the right modes and the PS2 logo works.
- [ ] Handoffs: Ember keeps the mounted device state (Memory Files launches too), Neutrino across devices,
      the MMCE GameID switch.
- [ ] PR #869 (PS1 disc IDs for VCD and Ember): port once it is merged and validated upstream.
- [ ] Release, Test me post, and a Short (the build 94 Short is folded into this one).

## Build 100: media
- [ ] MP3 in Memory Files, and a Coverflow-style music player: albums from the tags, their cover art, play and
      pause, next and previous.
- [ ] More video: what libsmslite can play beyond XviD and DivX AVI (MPEG-1 and MPEG-2 from DVDs), and a page
      in the README with the exact formats, resolutions and bitrates.
- [ ] A converter on the PC (RIPPS2 Audio Studio grows into a media studio): any video or music to what RIPPS2
      plays.

## After build 99
- Gather testing data from the build 99 release, then move from alpha to **beta** and prepare the beta launch on
  psx-place.com.
