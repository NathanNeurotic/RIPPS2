# POPS / PS1 MMCE audit

Prepared 2026-10-26 from `B:\Backups\FATWOOD\POPS` and `B:\Backups\FATWOOD\ART`. Installed and verified on 2026-10-26 after the user made space. All 21 games are selected and on the SD2PSX.

## Capacity

- SD2PSX (D:) free after installation: **3.63 GiB** (3,903,815,680 bytes).
- POPS folder: **10.94 GiB** total: **21 VCD game images**, common PopStarter support files and per-game companion files.
- FATWOOD ART: **236 files**, 0.009 GiB total.
- All POPS + matching ART were installed; about **3.63 GiB** remains free.

The full set is installed: 21 VCDs, common PopStarter files, per-game companions, and 164 matching art files. POPSTARTER.ELF matches the FATWOOD source hash; the prior card copy is preserved at `B:\Emulation\PlayStation\RIPPS2\RIPPS2-holding-2026-10-25\SD2PSX\POPS\POPSTARTER.ELF.pre-FATWOOD`. All 21 copied VCDs resolve to the same embedded serial IDs as their source files. Twenty-one title-keyed CFG files in `CFG/` now include title, genre, developer, publisher, release date, players, region/video mode, aspect, scan mode, rating badge, language and description. All 97 POPS files and 164 matching artwork files are present with matching sizes. 3.63 GiB remains free.

## Game selection

Mark `[x]` for games you want on MMCE. Per-game companion files in `POPS/<same game name>/` are included when present. Sizes are source file sizes; exFAT allocation and future card use can shift the final free-space figure.

| Keep | Game | VCD GiB | Companion files |
|---|---|---:|---|
| [x] | Ape Escape (USA) | 0.40 | none |
| [x] | Digimon World (USA) | 0.36 | SLOT0.VMC, SLOT1.VMC |
| [x] | Digimon World 2003 (Europe) (En,Fr,De,Es,It) | 0.65 | CHEATS.TXT, PATCH_6.BIN, SLOT0.VMC, SLOT1.VMC, TROJAN_0.BIN, TROJAN_2.BIN, TROJAN_8.BIN |
| [x] | Final Fantasy IX (USA) (Disc 1) (v1.1) | 0.69 | CHEATS.TXT, PATCH_4.BIN, SLOT0.VMC, SLOT1.VMC, TROJAN_1.BIN, TROJAN_2.BIN, TROJAN_7.BIN, TROJAN_8.BIN |
| [x] | Grand Theft Auto - London 1969 (Europe) (En,Fr,De,It) | 0.65 | none |
| [x] | Grand Theft Auto (USA) | 0.67 | SLOT0.VMC, SLOT1.VMC |
| [x] | Grand Theft Auto 2 (USA) | 0.51 | SLOT0.VMC, SLOT1.VMC |
| [x] | Klonoa - Door to Phantomile (USA) | 0.69 | SLOT0.VMC, SLOT1.VMC |
| [x] | LSD - Dream Emulator (English v1) | 0.60 | none |
| [x] | Mega Man Legends (USA) | 0.49 | PATCH_4.BIN, SLOT0.VMC, SLOT1.VMC, TROJAN_1.BIN, TROJAN_7.BIN, TROJAN_8.BIN |
| [x] | Mega Man Legends 2 | 0.61 | PATCH_4.BIN, SLOT0.VMC, SLOT1.VMC, TROJAN_1.BIN, TROJAN_7.BIN, TROJAN_8.BIN |
| [x] | Misadventures of Tron Bonne, The (USA) | 0.34 | PATCH_1.BIN, PATCH_4.BIN, TROJAN_5.BIN, TROJAN_7.BIN, TROJAN_8.BIN |
| [x] | MTV Celebrity Deathmatch (USA) | 0.22 | SLOT0.VMC, SLOT1.VMC |
| [x] | Skullmonkeys (USA) | 0.61 | none |
| [x] | Spider-Man (USA) | 0.68 | PATCH_1.BIN, SLOT0.VMC, SLOT1.VMC, TROJAN_0.BIN, TROJAN_2.BIN, TROJAN_7.BIN, TROJAN_8.BIN |
| [x] | Spyro - Year of the Dragon (USA) (v1.1) | 0.48 | CHEATS.TXT, leeme.txt, PATCH_1.BIN, SLOT0.VMC, SLOT1.VMC, TROJAN_0.BIN, TROJAN_7.BIN, TROJAN_8.BIN |
| [x] | Spyro 2 - Ripto's Rage! (USA) | 0.53 | SLOT0.VMC, SLOT1.VMC |
| [x] | Spyro the Dragon (USA) | 0.49 | SLOT0.VMC, SLOT1.VMC |
| [x] | Tomba! 2 - The Evil Swine Return (USA) | 0.41 | PATCH_4.BIN, TROJAN_1.BIN, TROJAN_2.BIN, TROJAN_5.BIN, TROJAN_7.BIN, TROJAN_8.BIN |
| [x] | Tomba! | 0.26 | none |
| [x] | Toy Story 2 - Buzz Lightyear to the Rescue! (USA) (Rev 1) | 0.59 | SLOT0.VMC, SLOT1.VMC |

Common POPS files to include with the selection: `POPSTARTER.ELF`, `POPS.PAK`, `POPS_IOX.PAK`, `IOPRP252.IMG`, `IGR_BG.TM2`, `IGR_NO.TM2`, and `IGR_YES.TM2`. The measured combined common-file size is 2.52 MB.

## Art

FATWOOD ART contains 236 PNG files (~0.009 GiB), mostly keyed by game/disc IDs and OPL artwork suffixes. Build 115 notes say RIPPS2 can use PS1 disc IDs and PS1 name keys; after you select games, we can make a second checklist showing which available art keys match each selected game. All art is small enough that space is negligible.

## On-card layout to review

Installed at `D:\POPS\` with the source companion folders and support files, matching art at `D:\ART\`, and per-title metadata at `D:\CFG\<VCD basename>.cfg`. The SD config now uses `popstarter_path=mmce?:/POPS/POPSTARTER.ELF`, so POPSTARTER resolves from either MMCE slot. The previous USB setting file is preserved in the RIPPS2 holding folder.

## Next step

Full package and metadata installed; the POPSTARTER path now points to MMCE. Hardware launch testing is the remaining check.




