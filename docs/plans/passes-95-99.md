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
- [x] **JPG loads stop partway** (a quarter of the picture, not always the same file): read the whole file before
      decoding (a short device read ends libjpeg's input early). Same for RIPgrid, which shows JPG covers as
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
- [x] Page buttons: Theme, L1 / R1 or L2 / R2; theme key `page_buttons=l2r2`, which RIPgrid uses.

## Build 97: Grid and Flow
- [ ] RIPgrid: the name under the grid in RIPPS2 Sleek Bold; the grid centered on the content, ignoring the
      sidebar; Right at the right edge goes to the next page and Left at the left edge to the previous one
      (no wrapping).
- [ ] Case flip on a 0.42 s right-stick hold (was 2 s), on RIPFLOW too, where it replaces the automatic front
      and back crossfade.
- [ ] RIPFLOW info page: right-stick tilt on the screenshots.
- [ ] RIPgrid on HDMI and HD modes (FifthFox: "optimized for a CRT"): check every video mode and fix its layout.
- [ ] Older OPL themes: load a set of classic themes in the lab and fix what draws wrong next to RiptOPL.

## Build 98: Memory Files
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
