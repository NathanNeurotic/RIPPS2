# Build 114: the settings audit answers, the fonts and the new launch guard (plan, 10/23, nothing coded yet)

Audit: https://claude.ai/artifact/8QRQ1DU2cu2eohZ94BsY1o. Guard CI 39908371655 passed (build + host tests).

## The user's answers
Yes: 1 BDM Devices sub-page (6 device rows, no indent, Modify row under BDM Devices Start Mode), 2 drop Game Sources'
greyed Protocol row (guiSourcesNetRows*), 3 diaConfig header _STR_GENERAL_SYSTEM, 7 POPS notice "No POPSTARTER SMB setup
found yet. Fill in the rows below." (literal in both dialogs + gui.c:2384 _t), 8 title "POPSTARTER Network", rows
"POPSTARTER UDPFS Network" / "POPSTARTER SMB Network", 9 Screen sub-page (diaDisplayConfig without Show GameID Barcode,
which moves to diaUIConfig; Interface composes diaUIConfig only, updater NULL; guiShowScreenConfig keeps live offsets,
restores on Back, asks about a new video mode), 10 drop VCD row from Interface, 11 five category rows (CATLAYOUT, CATBAR,
CATSWAP, TRANSITION, SRCNAME) to diaCoverflowConfig renamed "Layout" (live read + revert there), 12 "Colors and Text"
with Text Weight (Regular/Medium/Bold), 13 "HDD POPS partitions" + hint without "--", 14 Neutrino page header literal
"Neutrino Advanced Arguments", note "RIPPS2 adds the drive, ISO, VMCs and video mode itself.", 16 hub _t("PS Emulation"),
_t("Controllers"), _t("Audio") (hub only), 17 STATUS "What each card starts; install or repair BIBLE.", 18 MMCE alarms
enum _l(_STR_OFF)/_l(_STR_ON), 19 one game-options row _STR_RIPPS2_ACHIEVEMENTS -> ripps2PickList of the 3 RA rows
(gameMenu and VCD appMenu; GAME_RA_MENU mapped before the dispatch).
No: 4, 5, 15. 6 = both: Network keeps Cover Art; Artwork Settings gets "Missing Covers" + Download (ripps2ArtDownload).
Network still scrolls after this: measure after the 18 px font, then offer another fix.
New ids after RIPPS2_HIDDEN_BUTTON (300+ range). Changed OPL labels: use literals/_t (translated by English) or new
HINT_RIPPS2_* labels (labels: fill), never reword an old label's meaning.

## Launch guard, the user's redesign (10/23)
A RIPDISC-style glass panel (ripps2DrawHintBoxA fade 0.6 s, fonts[4] heading, fonts[5] line, rdRing's 12 notches exported
from ripps2disc.c). The launch waits at the END of the queue and starts by itself when reads and writes finish: art loads
removed, ioBlockOpsTimed(1, 0) so the queue has an end, unblocked before returning (deinit's drain unchanged). Notches fill
by estimate: ioman records each list read's last duration per mode; unknown = a chase. Cross = start now (ioLaunchBegin,
ioCancelScans, remove list reads, "STOPPING" on the same panel); Circle = back out (unblock). Music streams on its own
threads (bgmThread/bgmIoThread), not the IO worker: never guarded, keeps playing. Update test_ripps2_build114.py.

## Fonts (A-E, all into 114)
A: misc/ripps2roboto.ttf = Roboto-VariableFont_wdth,wght instanced wdth 75, wght 400-700, Latin-1 cut, strip_fonts;
builtin:ripflow -> 400, builtin:ripflowbold -> 700, builtin:roboto; diaFont 18 px; OFL replaces ROBOTO-LICENSE.
B: font_t weight/embolden; fntSetWeight (wght design coords; static faces FT_Outline_EmboldenXY scaled by ppem, about
1 px at 18 ppem per +300, advance grows); alt faces take the weight when variable; theme keys default_font_weight,
fontN_weight in thmLoadFonts. C: gRipps2TextWeight (config ripps2_text_weight): diaTipFont 400/500/600, STATUS/About page
faces own+0/100/200 (load page faces on the RIPPS2 theme too when > 0). D: RIPPS2-themes Adapt/Adapt Rx b,c ->
builtin:roboto + weights, d -> builtin:ripps2, comments list every built-in. E: ripps2lang.py pick_font tries the variable
Roboto (elf/lang/fonts) first, cut per language, OFL text in the pack.

Then: translations (32 languages), regen patch, CI, lab (pages fit, guard), retakes, Queen reel.
