# Ember (found, not carried)

**Ember** is a PlayStation 1 emulator for the PlayStation 2 by **Gageformer**.
Official releases: <https://github.com/Gageformer/Ember/releases>

RIPPS2 launches Ember games with your own copy of Ember: `ember.elf` in the `EMBER` folder at the top of
the drive the games are on (`EMBER/games/<Title>/` beside it), with your own PS1 BIOS as `EMBER/bios.bin`.
When a launch finds no `ember.elf` there, RIPPS2 says so and names the path it looked at. STATUS on the
START menu shows whether the first drive has one.

From build 71 to build 112 RIPPS2.ELF carried the Beta-2 build unmodified, under the Ember Public Beta
Testing Licence, and wrote it into a drive's `EMBER` folder the first time an Ember game was launched
from there. Build 113 stopped carrying it (the ELF is smaller, and the copy you get from Ember's releases
is always the current one). The last commit with the bundled build and its licence is in this
repository's history.

Ember contains no PlayStation BIOS and no game data. RIPPS2 credits Ember in its About screen with the
link above.
