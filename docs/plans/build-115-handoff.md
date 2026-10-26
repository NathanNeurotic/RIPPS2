# Build 115 handoff (2026-10-26)

The session that built rounds 3b and 3c ended here (the user's account is out of usage for the week; another local
account resumes). This page is everything the next session needs; `build-115.md` has the full round notes.

## Where things stand

- **ps2-pillars `main`**: everything pushed. CI run 40304161582 (be0b9a0) is green, build and host tests. The handoff
  commit adds the German translations, `REWORDED` in `elf/lang/ripps2lang.py` and the kit in `tools/lang115/`.
- **RiptOPL clone** (`B:/Webpages - Projects/RiptOPL`): every patch applied and staged, no engine edit pending.
  `0115-ripps2-hardware.patch` (10,032 lines) was regenerated at the end and the series reproduces the tree.
- **This session's build 115 commits**: 5c91575 (BIOS music stuck notes, issue #4), ad51a46 (a Manual drive's first
  answer, OSDSYS-style hints, the include order), 4d2d6cb (MP3, always analog, quiet All Games), be0b9a0 (the build
  114 test reads mixBuildRows).
- **RIPPS2-themes**: 3 commits ahead of origin, NOT pushed (b31725b, 2903ea4, c1ec32c: edition 115, two files a
  theme, one-piece sidebar, hints_flank keys). They need the 1.1.5 ELF, so they go out with the release.
- **Tested**: the round 3b ELF ran on the user's SD2PSX (their notes are round 3c). Nothing after it has run on
  hardware or as a whole in the lab: round 3c, MP3, the analog re-ask and the quiet All Games are host-tested and
  CI-built only.
- **Staged for the SD**: `B:\Emulation\PlayStation\RIPPS2\RIPPS2-115-round3c` (CI 40301042094) is older than MP3 and
  the rest. Take the ELF from the newest green CI run instead.

## The user's last requests (10/26)

1. "add mp3 decoder": done in 4d2d6cb. minimp3 (lieff, CC0) is in `RiptOPL/thirdparty/minimp3`, unchanged. In
   `src/sound.c`, mp3Open/mp3Read decode a frame at a time to 48 kHz stereo the .wav way and skip an ID3v2 tag. Memory
   Files plays .mp3; an .mp3 in AUDIO is music; the "could not be played" message names MP3s. libmad was not used
   (GPL).
2. "analog mode on in RIPPS2 always" (8BitDo adapter plus DS4, no ANALOG button): done in 4d2d6cb. `src/pad.c` asks
   a pad left digital for DualShock mode (locked) every 2 s while it is idle, instead of only in a clean poll, which
   MMCE traffic rarely gave. Check on hardware: the right stick tilts.
3. "get auto to be dry with the trust fast cache": done in 4d2d6cb. `src/mixsupport.c` mixQuietUpdate: when a source
   answers with the titles All Games (and Recent Games) already shows, the rows take their live source in place and
   the list is not rebuilt (no blank, no art reload). DIAG.TXT then says "all games: source N answered with the titles
   on screen: no rebuild".
4. "go ahead and do all the work; I'll hand the video job to another session so we can focus on testing the software
   and publishing the release". The video job is NOT ours. The user asked for the release to be published after
   testing.

## Next, in order

1. **Translations** (in progress): German done, 31 languages to go. Follow `tools/lang115/README.md`. Then
   `python elf/lang/ripps2lang.py check`, commit, push, CI green.
2. **Lab round in PCSX2** (the lab rules below). First see `build-115.md` section F: on 10/25 night the background
   driver's key presses stopped reaching PCSX2. Check:
   - Boot with Fast Cache and Trust Cache on: All Games never blanks or reloads art when sources answer; the DIAG line
     above appears. Ember PS1 and PS2 games together in All Games (issue #4).
   - Held SELECT: the theme window comes up, no freeze. Sidebar: Left/Right, Up/Down across categories, Circle with it
     hidden; info pages (Left to the icons, Right does not cycle); Memory Files L1/R1; RIPFLOW Left.
   - MP3: plays in Memory Files (MEDIA), as music from AUDIO, one with an ID3 tag with a cover, a mono or 22 kHz one;
     a broken file gives the message, not a hang.
   - BIOS Music rip: plays at once after the rip, clean past 2:33 (pieces are 5:04 and 5:31). The sounds room check
     on a full card (the drive offer).
   - Message boxes that only inform have one OK; the rip explainer modal; STATUS LOADING and CACHE SETTINGS both ways;
     Recent Games 1 to 99 (a Manual drive's game starts its drive); Neutrino on the exFAT HDD and the older-than-1.3
     message on APA.
3. **Hardware round with the user** (SD2PSX on their PS2): MMCE input with Pad First on, the right stick with the
   8BitDo and DS4, Burnout 3 through Neutrino from MMCE, Digimon World through Ember, the sounds and BIOS Music rip,
   EXIT back to RIPPS2 through BIBLE, BIBLE over an existing PS2BBL Extended (DIAG.TXT logs each step), MP3 from MEDIA.
4. **Release prep**: CHANGELOG (a Build 115 section in the shape of 114's), README (the ELF size from the real
   release build in PS2 KB: 2,641 KB was before minimp3, measure again), release notes, the psx-place post built from
   `tools/discord/psxplace-post.bbcode`, `tools/discord/notes/build115.md` for make_test_embed.py. Credit the testers
   as memory `ripps2-testers` says.
5. **Publish v1.1.5-beta** (version = build digits): a full release (never a pre-release) with RIPPS2.elf. Then the
   themes: push RIPPS2-themes, `git tag -f rolling && git push -f origin rolling`,
   `gh release upload rolling RIPPS2-themes.zip --clobber`, the notes say edition 115 (title has no build number).
   Reply on issue akilluminati47/RIPPS2#4 that 1.1.5 fixes it. The Discord post only when the user says so.
6. **SD deploy** when the card is in the PC (D:): the new `RIPPS2/RIPPS2.ELF`, the edition 115 THM Adapt pair, the
   ELF into BootCard-1/2/4/6/8. Old files move to `B:\Emulation\PlayStation\RIPPS2\RIPPS2-holding-2026-10-25`, never
   deleted, nothing old left on the MMCE.

## Open items

- Tilt on hardware (item 2 above). BIBLE over BBLE: read the user's DIAG.TXT if it fails again.
- Round 3c item 3: the boot refresh against Trust Cache (the quiet update should cover it; confirm in the lab).
- The user's hardware results for everything since round 3b.

## Rules that stand

- No em dashes anywhere (code comments, docs, posts).
- The Discord webhook lives only in `~/.ripps2/discord.env`, loaded into `RIPPS2_DISCORD_WEBHOOK`: never in a file in
  a repo, a log or memory, never printed. Post only when the user says.
- The lab: the portable PCSX2 at `B:/Emulation/PlayStation/PCSX2/ripps2-lab` with its own ini and test cards, run
  through `tools/dev/ps2bg.ps1` (background). Never the user's PCSX2 or their Mcd001/Mcd002.
- Never hard-delete the user's files: move them to a holding folder. Raw disk formats only after a verified backup
  and the user's yes.
- Never copy GPL code into RIPPS2 (AFL-3.0); never obtain or use Sony keys; never open upstream PCSX2 PRs; never
  `git stash` in the RiptOPL clone. The psx-place bump is posted by the user.
- Downloads need the user's permission unless it is already given for the task.

## Handy commands

- New engine change: edit the RiptOPL clone (edit scripts written with the Write tool), then from ps2-pillars
  `TMPDIR=<scratch> bash tools/dev/regen_patch.sh`.
- Strings: `python elf/lang/ripps2lang.py extract ../RiptOPL`, then `check`.
- Host tests locally: from `elf/tests`, `export PATH=/c/msys64/mingw64/bin:$PATH` and
  `RIPTOPL_DIR=../../../RiptOPL python test_ripps2_build114.py` (any test file).
- CI: `gh run list -R akilluminati47/RIPPS2 -L 3`, `gh run watch <id> -R akilluminati47/RIPPS2 --exit-status`.
- The BIOS music PC render: `build-115.md` round 3c item 25 and memory `ripps2-build115-r3`.
