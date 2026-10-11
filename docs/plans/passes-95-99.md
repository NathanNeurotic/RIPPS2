# Builds 95 to 99: the 2026-10-11 notes, sorted into passes

The notes came in out of order; here they are grouped so each build needs one lab session in PCSX2, and real
hardware only twice: **build 95** (the sound and stability fixes testers are hitting now) and **build 99**
(everything else). Each pass: patch, host tests, CI, one scripted lab run, fixes folded into the same patch,
then tick it here. ripto's RiptOPL reference (device handling, artwork keys, GameIDs, launch handoffs) drives
build 99.

## Build 95: sound and stability (release, hardware session 1)
- [ ] **Boot freeze with ripped sounds in AUDIO.** Reproduce in the lab (rip on PCSX2's BIOS, reboot), find
      why (suspects: the long boot/launch rips overflowing SPU2 RAM, the early boot sound, two loads at once),
      and make loading foolproof: a size and SPU2 budget check per sound, a bad or oversized file skipped and
      named, never a hang.
- [ ] **No built-in sounds.** OPL's eight built-in `.adp` leave the ELF. Sounds come only from `AUDIO`
      (BIOS Sounds > Rip, or RIPPS2 Audio Studio); without them RIPPS2 is silent, and STATUS says how to get
      them.
- [ ] **Clean, snappy sound effects.** One voice per sound, a new press cuts the old one, a held cursor never
      stacks, mutes in waves or lets stale sounds play later. Measured from lab captures (gaps and overlaps in
      the recorded audio), not by ear.
- [ ] **Rip quality.** No beeps, pops or clicks: the rip's synthesis run on the PC against a BIOS dump and
      compared with the reference recordings (click detector, envelope ends, loop points, noise voices).
- [ ] **`.adp` preview** in Memory Files: Cross plays it, Back stops it.
- [ ] **The trusted IGR stays primary.** With In-Game Menu off (the default) the combo is exactly OPL's IGR and
      nothing of the pause menu or the hunt list is involved. The menu's tooltip calls it experimental and
      warns about cutscene audio; look at the cutscene skip and crash reports for anything that can be made
      safer without hardware.

## Build 96: settings and menus
- [ ] Backing out of any submenu lands on the row that opened it, not the page's top.
- [ ] Colors and More: a tooltip on every row, a **Theme** value on most rows, and the Grid backgrounds tinted
      by the color theme.
- [ ] Flow and Grid: **Flow Cover Count** and **Flow Cover Size** (the flow's own rows say so).
- [ ] STATUS scrolls like the settings pages; the support line naming the user is removed.
- [ ] Neutrino: a clear description of the automatic arguments.
- [ ] Settings pages read in one plain face on every theme (Adapt's settings face), not each theme's styled
      fonts.
- [ ] Devices: auto start can be **Last Used**, the device and page you were on.
- [ ] Page buttons: Theme, L1 / R1 or L2 / R2; theme key `page_buttons=l2r2`, which RIPgrid uses.

## Build 97: Grid and Flow
- [ ] RIPgrid: the name under the grid in RIPPS2 Sleek Bold; the grid centered on the content, ignoring the
      sidebar; Right at the right edge goes to the next page and Left at the left edge to the previous one
      (no wrapping).
- [ ] Case flip on a 0.42 s right-stick hold (was 2 s), on RIPFLOW too, where it replaces the automatic front
      and back crossfade.
- [ ] RIPFLOW info page: right-stick tilt on the screenshots.
- [ ] RIPFLOW main page broken on the user's ELF: find the fault (its built-in cfg or a key that changed), and a
      test that parses every built-in theme cfg.
- [ ] Older OPL themes: load a set of classic themes in the lab and fix what draws wrong next to RiptOPL.

## Build 98: Memory Files
- [ ] Devices show as `mc0:/` and `mc1:/`.
- [ ] Hold to scroll: after 0.42 s the cursor repeats at the Storage list's scroll speed.
- [ ] Card manager: hints with glyphs on its Actions modal.
- [ ] Picture viewer: Adapt's face, glyph hints that fit, no distortion zoomed in close.
- [ ] PS2 3D save icons (`.ico` / `.icn`) open in a viewer: the model, its texture and its animation.
- [ ] Text editor input bugs: reproduce first.
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
- [ ] Handoffs: Ember keeps the mounted device state (Memory Files launches too), Neutrino across devices,
      the MMCE GameID switch.
- [ ] PR #869 (PS1 disc IDs for VCD and Ember): port once it is merged and validated upstream.
- [ ] Release, Test me post, and a Short (the build 94 Short is folded into this one).
