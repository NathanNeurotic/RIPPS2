# The build 114 reel (v1.1.4): storyboard

The user (10/23): a calm preface that shows the plain things first, then a montage of the features on Queen's
"Don't Stop Me Now" (its upbeat part and beats; the title phrase may be on screen, no lyric lines), faded out early
into mr.msa's "Money Longer (Instrumental)" with stronger effects: it opens on the pepecook picture and the
larry-themaliciouslarry clip, carries into a colour party (the new Color Themes, Custom, the Color Sweep), then the
most interesting features. No photos of the sidebar this time: the sidebar moves, in footage. No upload.

Music: the console's menu wave (menu_rip.wav, ripped from the BIOS by RIPPS2) under the preface and the end card;
Queen for the montage; Money Longer for the colours and the finale. Every cut on a measured beat (tools/beats.py).

## 0. Preface, menu wave (about 25 s)
- Title card: Rip it | v1.1.4, "RIPPS2 beta / build 114".
- The Settings hub, then each page with nothing below the fold: Game Sources (one HDD Start Mode, BDM Devices as
  its own page), Interface (Screen, Layout, Colors and Text), Network, Audio. Caption: every page on one screen.
- STATUS: drives with free space, launchers found, BIBLE's line. About: Neutrino beside RiptOPL in the credits.

## 1. Don't Stop Me Now (the montage)
- The upbeat entry: the Storage sidebar with every source on (All Games, USB, HDD Games, MMCE, Network, Apps,
  Starred), cut on the beat to Game Sources where Network Connectivity and BDM Devices Start Mode go Off, then the
  sidebar again with them gone. One HDD Games, APA or exFAT, never two.
- All Games: every drive's games in one list (v_master), kept for the next boot.
- Hide Game and Show Again (v_hide), Delete completely (v_delete: ISO, CFG, ART, CHT, the VMC kept), the APA
  check refusing a damaged table (v_apa_no).
- Look now: the launchers found on the started drives (Cache page, STATUS handover).
- The launch guard (a RIPPS2_GUARD_TEST build): a game picked while a drive's list is read; the glass panel
  fades in, the notches fill toward the estimate, the game starts by itself; once more with START NOW.
- Text Weight Regular to Bold on the Settings tooltips; Japanese in the same faces (v_lang_ja).
- The title phrase on the chorus hit, then Queen fades early.

## 2. Money Longer (the colours, then the finale)
- The drop: pepecook.png and the larry clip, glitch cuts into the colours.
- Color Theme: Tangerine, Flamingo, Turquoise, Moonlight (the ghostly white), Custom with its own picker.
- Color Sweep: Rainbow over the towers, Flamingo's all-pink sweep, the Sweep Colors page, a sweep saved under a new
  name; the sweep on RIPFLOW and RIPGRID.
- The finale on the hardest beats: the guard panel, the sidebar, the themes (t_ripps2, t_adapt, t_ripgrid,
  t_ripflow, t_disc), fast cuts with RGB split and punch zooms.

## 3. End card, menu wave
- v1.1.4, github.com/akilluminati47/RIPPS2, the dead elf's hat.

## Takes needed on the final ELF (takes114v.ps1)
p_hub, p_sources, p_bdm, p_interface, p_screen, p_layout, p_colors, p_status, p_about (preface); s_all_on,
s_off_settings, s_after (sidebar); g_wait, g_now (guard, test ELF); w_weight (Text Weight); c_tangerine,
c_flamingo, c_turquoise, c_moonlight, c_custom, c_sweep_rainbow, c_sweep_flamingo, c_sweep_page, c_sweep_ripflow;
plus the 114 takes kept (v_master, v_hide, v_delete, v_apa_no, v_cache, v_handover, v_lang_ja, t_*).
