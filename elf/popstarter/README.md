# POPSTARTER (found, not carried)

**POPSTARTER** is the PlayStation 1 launcher for the PlayStation 2 by **krHACKen**. It is freeware.

RIPPS2 starts PS1 games (`.VCD` in a drive's `POPS` folder) with your own POPSTARTER, found where a launch
looks: the path in Settings, the drive's `POPS`, `APPS` and top folders, a game's own
`POPS/XX.<name>.ELF`, `__common/POPS` on the internal HDD, and the memory cards. When none of those has
one, RIPPS2 says so and names the path it looked at. STATUS on the START menu shows what it found.

From build 73 to build 112 RIPPS2.ELF carried `POPSTARTER.ELF` as released (167,700 bytes, CRC-32
`59ebabb9`, the copy the PSBBN Definitive Patch project ships) and wrote it to a drive's `POPS` folder when
you had none. Build 113 stopped carrying it; the copy you already use for your PS1 games is the one it
launches. Sony's POPS files (`POPS.ELF`, `POPS_IOX.PAK`) are yours to supply as before.

RIPPS2 contains no PS1 BIOS and no game data. RIPPS2 credits POPSTARTER in its About screen.
