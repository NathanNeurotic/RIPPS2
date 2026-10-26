# Build 115: the user's notes of 10/26 evening, and the decisions taken

The user went to work and asked for the build to be finished, tested in the lab, released and posted, with the
decisions made for them. This page is the list, what was decided, and where each item stands. It follows
`build-115-handoff.md` (translations: done in 4818733).

## The notes and the decisions

1. **Game settings, PS1 games and apps.** They still offered RENAME. Decision: PS1 games (POPSTARTER and Ember) and
   apps get the PS2 games' row, "Set Metadata (Rename)", in Rename's place, just above Delete, so every game menu reads
   the same and nothing new sits at the top under the title. It opens the same editor; the details go to the item's
   own CFG (a PS1 game's `CFG/<name>.cfg`, an app's `title.cfg`); its ACTIONS rename. Where the page cannot rename,
   "Set Metadata".
2. **RIPFLOW cover flip.** RIPFLOW's centre cover has turned over since build 97 (the right stick held to one side,
   0.42 s, once its back cover COV2 is in). Decision: check it in the lab with the 115 sidebar keys; fix what broke.
3. **RIPGRID source cycling.** Up on the first row and Down on the last row changed the source. Decision: they stop
   there; sources change through Circle (the Storage drawer) or the sidebar.
4. **8BitDo receiver (v1.05 to v1.13).** The ps2-home thread is behind a bot check (not readable from here). RIPPS2
   asks a pad left digital for DualShock mode every 2 s while idle (4d2d6cb). A pad in digital mode sends no stick data
   at all, so there is nothing to translate; pads are polled by padman on the IOP, so a separate EE thread would not
   help either (the bus is the IOP's). Decision: keep 4d2d6cb, log the pad's mode changes in DIAG.TXT so a hardware run
   shows what the receiver does.
5. **POPSTARTER files.** POPSTARTER from MMCE worked once the user added POPS.ELF and IOPRP252.IMG (AnimMouse's
   POPS-binaries; POPSLoader's layout). Decision: RIPPS2's POPS check knows both sets: POPS.PAK + POPS_IOX.PAK, or
   POPS.ELF + IOPRP252.IMG (+ POPS_IOX.PAK), and the message names them.
6. **Fast Boot.** Decision: a Fast Boot row on the Cache page. On: a light gate file beside RIPPS2.ELF
   (`RIPPS2.FB`, text) names the settings home and the AUDIO folder, so boot reads them straight from RIPPS2's own
   drive (no card scan, no redirect, no AUDIO search); RIPPS2's drive is always started; every other source starts on
   demand with its list shown from the cache (Trust Cache, All Games); a SELECT refresh starts that page's drive(s) and
   loads their art; Automatic Refresh on starts them at boot as before. Turning it on copies the sound set (and the
   picked track when the drive has room) into RIPPS2's own AUDIO, so the sounds load from the fastest drive every
   time. The tooltip says all of this. DIAG.TXT gets the boot's phase times so the next hardware run measures it.
7. **Music after a rip.** Decision: the ripped track is the pick (Menu when both), saved at once, shown on the Audio
   page, playing now and after a reboot.
8. **Where rips go.** Decision: BIOS Sounds and BIOS Music ask where first, RIPPS2's own drive first ("beside RIPPS2,
   read first at boot"), then each started drive's AUDIO with its free space.
9. **WAV stutter in the menus (fine in the media player).** The music reader took WAV in 4 KB pieces: 43 MMCE
   requests a second for CD audio, each waiting behind art reads on the shared bus. Decision: 32 KB pieces.
10. **Rip to Ogg?** Decision: no, WAV stays. An Ogg encoder adds about 1 MB to the ELF and encodes slower than real
    time on the EE, so a CD would rip several times slower; WAV is lossless and plays everywhere. The stutter was the
    reader (item 9).
11. **A CD player for marked tracks.** Decision: in Memory Files, opening a marked set of .wav / .ogg / .mp3 files
    plays them as a CD in the CD player screen (track list, next / previous); one file opens there too.
12. **BIBLE.** Decisions: never copies RIPPS2 anywhere; PS2BBL 1.2.0 starts RIPPS2 where it is (memory card, USB,
    MX4SIO). Running from MMCE or the HDD, which 1.2.0 cannot read: a card with PS2BBL Extended (an SD2PSX BOOT card)
    gets BOOT LOCK (its config starts RIPPS2 from MMCE), else the message says where to put RIPPS2. Every step reads
    "RIPPS2: Setting up BBL 1.20". The panel says BIBLE is for standard 8 MB PS2 memory cards (a MagicGate card or an
    SD2PSX / MMCE BOOT card), names the slot, and that PS2BBL reads slot 2's config before slot 1's. Background reads
    stop before any card write. A failed write says the card refused it and was put back, and that an SD2PSX may
    protect its card until the console is turned off and on. RESTORE puts back what BIBLE moved aside. A signed
    PS2BBL with MMCE does not exist (PS2BBL's dev builds are plain ELFs; signing needs Sony's keys), so BIBLE stays 1.2.0.
13. **Navigation sound bugs back.** Decision: find them in the lab before release.
14. **RIPPS2 on the SD2PSX.** Decision: consolidate on the SD: `mmce?:/RIPPS2/` holds RIPPS2.ELF, the settings, the
    caches and AUDIO; the boot card keeps only PS2BBL and its config (no RIPPS2.ELF, no RIPPS2 save). A RIPPS2 folder
    or APPS on the SD read the same; RIPPS2/ keeps everything together.
15. **Release.** v1.1.5-beta after the lab; themes rolling release (edition 115); issue #4 reply; Discord Test me;
    a Short rendered into the repo (no YouTube); psx-place: the first post (edit), the languages post (edit: every
    release carries the language pack, not 1.0.7), and the bump (links the repo video); the SD updated last.

## Progress

(filled in as the work lands)
