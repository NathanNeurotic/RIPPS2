# Showcase for build 114: the reel, the first post's tour, the bump's pictures

The user (10/22): "when making the screenshots for the first post choose better images story board it nicer so its
not like a latest changelog showing the sidebar right away ... be thorough in the planning of video and images like
we have done with text." Nothing here is uploaded or posted: the user watches the reel, picks, uploads, and posts.

Rules every frame keeps (from the reel memories): show only what RIPPS2 does on this build, in the lab's real
captures; captions beside the picture, never on it, and readable at phone size; never a Cross on the game list (the
lab's games launch); one theme per section so the eye is not jumping; no em dashes.

## 1. Who sees what, in what order

| Where | Reader | What they need first |
|---|---|---|
| psx-place first post (the front door) | someone who has never seen RIPPS2 | what it looks like with games in it, then how deep it goes, then that it is alive |
| psx-place bump reply for v1.1.4 | a follower of the thread | what changed since v1.1.3, each in one picture |
| YouTube / the bump's video | both | the reel below: 114's story, framed by what RIPPS2 is |
| Discord Test me post (when the user says) | testers | the test list; the reel link if it is up |

## 2. The reel: "Rip it | v1.1.4", about 2:50, 2560x1440 50 fps

Built in the v108 reel kit (`plan114.py` on `reel109.py` / `reel_engine108.py`), on RIPPS2's own music: the PS2's menu
music (ripped by RIPPS2) under the title card and the hat, and **Pillars** (RIPPS2 original, 84 BPM, a bar is 2.857 s)
for the body, bars 0 to 48 and its outro. Every cut on a bar or a half bar. The story is build 114's naming, which
already reads as a narrative: the list summoned whole, the launchers found by a SEANCE, a game laid under a SHROUD,
and one given its LAST RITES.

| Bars | Section | On screen | Caption (head / body) | Why it is there |
|---|---|---|---|---|
| intro 12 s | Title | the blue hat drops beside "Rip it \| v1.1.4", under it "RIPPS2 beta / build 114" | | the series' opening, so 114 reads as the next chapter |
| 0 to 2 | I. The whole list | a boot on the reel drive, chapter card over it: "All Games, at once" / "before a single drive answers" | | the problem testers reported (MMCE and USB lists slow to appear) |
| 2 to 4 | | All Games at the first frame: six games listed, no covers yet | The master list / Every game you have, listed before its drive answers. | the feature in one look |
| 4 to 6 | | the covers arrive, the cursor has not moved | The handover / Each drive's games swap in as it answers. The cursor stays put. | proves it is the real list, not a picture of one |
| 6 to 8 | | the same list with the drives on Manual: whole, instant | Drives on Manual / Still instant: their games are listed too. | Manual is RIPPS2's default for BDM |
| 8 to 10 | II. SEANCE | chapter card: "SEANCE" / "the launchers you keep, found once" | | |
| 10 to 12 | | STATUS opening on DRIVES: the HDD, both cards' free space, MX4SIO off | Drives first / STATUS opens on what RIPPS2 sees, with free space. | the user's ask: drives and space before the homebrew |
| 12 to 14 | | LAUNCHERS: five lines, not found yet; LOOK FOR THEM | Launchers / POPSTARTER, the POPS files, Ember, its BIOS, Neutrino. | |
| 14 to 16 | | "Start every drive first?" then LOOKING FOR YOUR LAUNCHERS | LOOK FOR THEM / It starts every drive, then searches them all. | |
| 16 to 18 | | the summary: SEANCE found 5 of the 5 | Found / Wherever you keep them, remembered for every launch. | |
| 18 to 20 | | STATUS's lines now with their paths (BACKUP/PS1, APPS/Ember, TOOLS/neutrino) | Kept / By drive kind, so a stick in another port still matches. | odd paths prove it searched |
| 20 to 22 | | Settings > Game Sources > Cache: Found / Not found, Look now | On the Cache page / Found or not found. No switch: it only helps. | the user's wording |
| 22 to 24 | III. SHROUD | chapter card: "SHROUD" / "hide a game from every list" | | |
| 24 to 26 | | Triangle options, Hide Game, the question | Hide Game / In a game's options. One question: it can be undone. | |
| 26 to 28 | | HIDDEN toast, the list without the game | Gone from every list / All Games, Starred Games, Recents, Random Game. | |
| 28 to 30 | | Settings > Game Sources > Hidden Games, SHOW IT AGAIN | Hidden Games / Kept on the game's own drive. Show it again any time. | |
| 30 to 32 | IV. LAST RITES | chapter card: "LAST RITES" / "delete a game completely" | | |
| 32 to 34 | | the plan: Goes (the game, its settings, art, cheats) / Kept (its saves) | Everything of its / The game, its settings, its art and its cheats. | was: only the ISO went |
| 34 to 36 | | "Delete its saves and RIPSHOT pictures too?" | Saves stay / Unless you say so. | |
| 36 to 38 | | Last check, START, DELETED ...: ... FREED | START, and only START / Then a receipt in REMOVED.TXT. | |
| 38 to 40 | | the APA disk with a table cloned from a bigger drive: "Nothing was deleted" | Berion's check / A table written from another size of disk is refused. | the forum's own expert, credited |
| 40 to 42 | V. Lighter | text card over the lite boot: 2.69 MB / 1.97 MB | RIPPS2-lite.elf / Under 2 MB for memory cards: your Neutrino, found. | FifthFox's 2 MB |
| 42 to 44 | | STATUS in Japanese | Every word, 33 languages / The new pages too. | |
| 44 to 48 | Montage | half-bar cuts: covers, SEANCE summary, Hidden Games, the plan, STATUS, Adapt | | the energy before the outro |
| 60 to 62 | Outro | "Rip it." over the list | | |
| end | End card | v1.1.4 beta, build 114; github; psx-place; testers with lukeatmynose and the YouTube thanks; built on RiptOPL, Neutrino, POPSTARTER, Ember, PS2BBL; music line | | |

The iLink fixes from the RiptOPL merge are a line on the end card ("i.LINK: Neutrino and POPSTARTER, from RiptOPL"),
not a shot: the lab has no iLink and the reel only shows what was filmed.

### Takes (the reel kit's `tools/takes114.ps1`, hidden lab, `rec` captures)
Disk `t114-reel.raw`: a copy of the reel library (the six DVD backups with covers, themes, MEDIA) with the launchers
added in odd places (BACKUP/PS1 POPSTARTER and the POPS files, APPS/Ember with its bios.bin, TOOLS/neutrino), so
nothing on `ripps2-reel108.raw` changes. `t114-apa.raw` with an HDL game for the APA shots, and `t114-apa-clone.raw`,
the same table on a smaller disk, for the refusal.

| Take | Disk | Card | Walk |
|---|---|---|---|
| v_master | t114-reel | allgames.bin from a first boot | boot, rec from the first frame through the handover |
| v_manual | t114-reel | the same, usb_mode=1 | boot, rec, the list whole and still |
| v_seance | t114-reel | fresh | START, STATUS, scroll, LOOK FOR THEM, Cross, Cross, the summary, STATUS again |
| v_cache | t114-reel | after v_seance (KeepCard) | Settings > Game Sources > Cache, Look now |
| v_hide | t114-reel | fresh | Triangle on Burnout 3, Hide Game, Cross, the list, START > Settings > Game Sources > Hidden Games, SHOW IT AGAIN |
| v_delete | t114-reel | fresh | Triangle on a game with CFG, art and cheats, Delete, Cross, Circle, START |
| v_apa_no | t114-apa-clone | fresh | Triangle, Delete: the refusal |
| v_lite | t114-reel, lite ELF | fresh | boot, START, STATUS |
| v_lang_ja | t114-reel | language Japanese | START, STATUS |

## 3. The first post's gallery: a tour, not a changelog

Recaptured on build 114 in one sitting (same disk, same cards), cropped to the PS2 frame, 1284x962 JPEG, two to a row
in the spoiler. Order is what a newcomer should see, the newest feature last:

| # | Frame | Theme | Why here |
|---|---|---|---|
| 01 | Storage, All Games, covers and the info panel | RIPPS2 (the towers) | the first look: a front end full of games |
| 02 | the game's info page: badges, details, a RIPSHOT screenshot | RIPPS2 | how deep one game goes |
| 03 | Adapt with its frosted bar | Adapt | the house theme, a different mood |
| 04 | RIPGRID's cover wall | RIPGRID | the library at a glance |
| 05 | RIPFLOW's carousel | RIPFLOW | a third way to browse |
| 06 | Launch Disc with RIPDISC's panel | RIPPS2 | the disc pillar |
| 07 | Memory Files: the orbits and a save's 3D icon | RIPPS2 | the files pillar |
| 08 | the in-game menu over a game (RIPSHOT) | | it reaches into the game |
| 09 | STATUS: drives, launchers | RIPPS2 | what it sees, new in 114 |
| 10 | Settings > Game Sources with Hidden Games and Cache | RIPPS2 | the settings, plainly worded |
| 11 | the START menu or STATUS in Japanese | RIPPS2 | 33 languages |
| 12 | LAST RITES' plan screen | RIPPS2 | the newest, last |

Frames 01 to 07 and 09 to 12 are new grabs; 08 is a still from the v1.0.8 reel's in-game capture (the lab cannot
start a game for a still, and the in-game menu has not changed since 108). Files: `media/b114/tour-NN-*.jpg`.

## 4. The bump's pictures (the v1.1.4 reply)
Five, in the reel's order: All Games before the drive answered (no covers yet), SEANCE's summary, STATUS with the
launchers found, Hidden Games, LAST RITES' plan. Files: `media/b114/new-NN-*.jpg`.

## 5. Order of work
1. Disks (copy, launchers, APA game, the clone). 2. Takes, then contact sheets of each. 3. The tour grabs. 4.
`plan114.py`, stills to check every caption, the render, the mix, the thumbnail. 5. psxplace114.txt: the first post
with the tour, the bump with the reel slot left for the user's link.
