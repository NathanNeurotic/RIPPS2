# Handoff: RIPSHOT, cloud session (2026-10-20) to a local session

The cloud session only read the plans. No code was written, nothing was committed, and no lab exists. Start here.

## Read first
- `docs/plans/ripshot.md`: the full RIPSHOT plan. Every on-screen word, the roll format, the build order and the
  console test list. It is the source of truth; change wording there first, then in code.
- `docs/plans/builds-104-on.md`: builds 104 to 107 (done) and the 10/19 findings on why RIPSHOT was split out.
- `HANDOFF.md`: house rules (still valid) and the older build 80 to-do list.
- Your Claude memories for this project: the cloud session could not reach them (they sit in Claude's own data
  folder), so a local session should check them before starting.

## Where things stand
- Builds 104 to 107 are done; 105 and 107 shipped in v1.0.7-beta. 106 (POWER OFF in the in-game menu, the star on
  the left) is done but POWER OFF was never seen in the lab because of the launch hang.
- RIPSHOT is the next build after 107 (build 108, patch 108, unless another build lands first). Not started.
- `RIPSHOT_ROLLS_MAX` = 2000 ("the number/year PS2 released"): confirmed by the user, do not ask again.

## What a local session needs
- The patched RiptOPL tree: the work is in `ee_core/src/igrmenu.c`, `ee_core/src/cd_igr_rpc.c`,
  `modules/iopcore/cdvdman/device-{bdm,hdd,mmce,smb}.c` and RIPPS2's `src/ripps2*.c`. Get it with
  `elf/build.sh --prepare-only` or your RiptOPL clone; `tools/dev/regen_patch.sh` folds changes back into the last
  patch in `elf/patches/`.
- The PCSX2 lab still exists on the user's computer: the portable PCSX2 at
  `B:/Emulation/PlayStation/PCSX2/ripps2-lab` (own ini, test cards, PINE 28012), driven in the background by
  `ps2bg.ps1`. Never use the user's own PCSX2. Only the cloud sessions' scratch copies are gone, so do not rebuild it.
  Warn the user before each PCSX2 run (house rule from builds-104-on).

## Next steps (ripshot.md "Build order")
0. [x] **Fix the PCSX2 lab's game-launch hang.** Done 10/20 (patch 108, branch `b108`): imgdrv's device was
   `host`, which PCSX2 takes for its own host file system; it is `iprp` now. Games launch in the lab; build 106's
   POWER OFF seen with the `RIPPS2_IGR_TEST=1` build. Details in ripshot.md step 0.
   For later steps: real frames in the lab need DISPFB, which stock PCSX2 never shows ee_core (no EE data
   breakpoints). The IGR test build fakes a frame at FBP 0; a RIPPCSX2 data breakpoint on the GS registers would
   give the real one.
1. [x] (10/20, see ripshot.md) GS readback in ee_core (written fresh from the GS manual and ORBIT's AFL neutrino-igr; OPL's `igs_api.c` is
   GPL-3, do not copy it), with a host test of the pixel paths (16, 24, 32-bit frames to RGB555; field frames).
   This step does not need the lab and can start in parallel with step 0.
2. Roll read / write: BDM done 10/20 over SIF DMA, not the IGR RPC (ripshot.md "How it works" 5); then APA HDD,
   MMCE, SMB.
3. Rolls: BDM done 10/20 and lab-checked (ripshot.md step 3); the silent menu and the exact frame on RESUME too.
   Then blank roll, rename at launch, handover for APA HDD, MMCE, SMB.
4. In-game screens. 5. Developing (quantizer, PNG, Memory Files roll pages, Auto). 6. Settings page with
   per-choice hints, defaults, the one-time `ripps2_igr_menu` switch, translations (33 languages).
7. `SCRn` in the engine and the themes (RIPPS2-themes rules apply). 8. Lab run, then the console test list.

## Watch for
- ee_core has about 11 KB of room (build 103: gc-sections, stack 0x2C80). Keep the transfer buffer on the IGR
  thread's stack and reuse it.
- Each build per builds-104-on: patch, host tests (`python elf/tests/run_host_tests.py <patched riptopl dir>`, new
  ones in `elf/tests/test_ripps2_*.py`), CI, one scripted lab run, fixes folded into the patch, tick it in the plan.
  No release unless asked.

## House rules (from HANDOFF.md, unchanged)
- One commit per build on `main` as akilluminati47 <acaradimos@gmail.com>, with the Co-Authored-By / Claude-Session
  trailers. No model names anywhere else in the repo.
- No em dashes anywhere.
- Never write the Discord webhook into a file.
- CI fails on a new warning in `src/ripps2*.c`.
