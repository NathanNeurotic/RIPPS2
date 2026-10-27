# Build 118 is RIPPS2 v1.1.8 beta: the boot sound with the towers' first frame, and the ART Pack, every cover from one file on your fastest drive.

## Get it
- [Download the latest RIPPS2.elf](https://github.com/akilluminati47/RIPPS2/releases/latest/download/RIPPS2.elf) (always the newest build), [RIPPS2-languages.zip](https://github.com/akilluminati47/RIPPS2/releases/latest/download/RIPPS2-languages.zip) (every release carries it, all 33 languages); the [theme pack](https://github.com/akilluminati47/RIPPS2-themes/releases/latest/download/RIPPS2-themes.zip) is still edition 117

## The boot sound
- It is now the first thing read at boot, so it plays as the towers appear instead of with the list (2 s earlier on PCSX2). With **Fast Boot** on, the AUDIO folder beside RIPPS2 is known from the first moment. The README.txt in AUDIO and MEDIA now says where each belongs: AUDIO beside RIPPS2.ELF, MEDIA on your biggest drive.

## ART Pack
- **Settings > Game Sources > Cache > ART Pack** packs every started drive's ART folder into one `art.tar` on the drive you pick, the fastest offered first (measured). Your ART folders are not touched; the same button removes it.
- Covers then load from that one file through one index, and the games it was built for never have their ART folder asked one picture at a time: less reading on the drive your music streams from. JPG covers and OPL Manager's `_BG_00` / `_SCR_00` names work from it.

## Test list
- **Boot sound on an SD2PSX with Fast Boot on**: does it start with the towers now, not with the list?
- **Boot sound with Fast Boot off**, AUDIO beside RIPPS2: earlier than v1.1.7?
- **Menu sounds and music after the boot sound**: all there, nothing cut?
- **ART Pack on your SD2PSX**: which drive does it list first, and at what KB/s? How long does the build take, how many pictures and MB?
- **After the build**: covers appear faster while you scroll fast? Music smooth while they load?
- **A game with no art** in a packed list: no slowdown on it?
- **JPG covers** (old OPL art packs) from the pack: they show?
- **Fetch covers** (Settings > Network) or develop a RIPSHOT after packing: the new art shows at once?
- **Copy art in on a PC** after packing: it shows only after you build again (expected); tell us if that is a problem for you.
- **Two drives with art** (USB and SD2PSX): every game's cover from the pack?
- **REMOVE the pack**: art back from the folders, nothing missing?
- **PS1 games** in a packed list: their art still shows?

## Report
Please [open an issue on GitHub](https://github.com/akilluminati47/RIPPS2/issues) with your **console model**, your drives, your **boot loader**, where RIPPS2 starts from, your **DIAG.TXT** (STATUS > SAVE DIAGNOSTICS) and a **photo** of anything odd: an issue is the best way to get RIPPS2 updated. Thanks to ripto, nuno6573, zackcage6, eliminator1403, FifthFox, Mr.sus.60 and lukeatmynose for the reports that got us here, and to DarkNerdShawny for opening issues on GitHub: be like DarkNerdShawny. Special thanks to all the YouTube love as well: glad to help however you reach me.
