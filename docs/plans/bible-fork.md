# BIBLE fork: a RIPPS2 second-stage boot loader (plan, 10/27)

The user, 10/27: "fork the bble software so we can try to enable 0ms boot and change the splash to the ps2 logo and the
four face buttons under it in svg sony order horizontally ... if a button is pressed the bble hotkey menu opens with a
clear exit to auto boot as well; allow editing the paths here too with the ripps2 theme ... if this is too much and it
needs to read from the file outside to stay light as possible do that and have it written as a note on BIBLE; the idea
is so we can inject to mmce or other drives that bble has support for", and "allow in the bible config to hide the face
glyphs for users and have it set on show".

## What it is

A fork of saildot4k's PS2BBL Extended (GPL-3.0) in its own repository (proposed: akilluminati47/BIBLE). It never goes
into RIPPS2's source (AFL-3.0): RIPPS2 carries its release binary as data, with its licence and source link, the way
elf/bible carries El Isra's PS2BBL 1.2.0 today.

## The one hard limit

A fork cannot be signed. The console only starts a KELF signed with Sony's keys at power on, and those keys are never
obtained or used. So the fork is a **second stage**: an ELF that the console's existing boot path starts.

| Console has | First stage (signed, unchanged) | Second stage (the fork) |
| --- | --- | --- |
| BIBLE on a MagicGate card | El Isra's PS2BBL 1.2.0 KELF, its AUTO entry pointed at the fork | mc?:/BIBLE/BIBLE.ELF |
| An SD2PSX BOOT card | the card's own PS2BBL Extended, BOOT LOCK pointed at the fork | mmce?:/BIBLE/BIBLE.ELF |
| FreeMcBoot / OSDMenu | their own E1 / first item | mc?: or mass: copy |

What the second stage adds: the drives BBL 1.20 cannot read (MMCE, and with its own builds MX4SIO and the HDD), so a
1.20 card can boot RIPPS2 from an SD2PSX's SD.

## 0 ms

- In the fork: KEY_READ_WAIT_TIME's clamp to 500 ms goes (loader_config.c:44), and 0 means one pad read and straight on:
  no countdown (loader_launch.c:493). The rescue combo window (2 s, non-blocking, main.c:253) becomes the same single read.
- The first stage keeps its own wait: PS2BBL 1.2.0's fixed rescue window is in a signed KELF and cannot change. The
  whole boot is that window plus the fork's 0 ms. On an SD2PSX the card's PS2BBL Extended config can already go low.

## The splash

- The PS2 logo, drawn from a public SVG as RIPPS2's PS1 and PS2 marks already are (trademark of Sony, credited), and
  under it the four face buttons in Sony's order, left to right: triangle, circle, cross, square. Modern glyphs, the
  same ones RIPPS2 draws.
- `BIBLE_GLYPHS = 1` in its config shows them (the default); 0 hides them for anyone who wants the logo alone.
- Drawn with gsKit into the existing LOGO_DISPLAY path (LOGO_DISPLAY 3 already draws a hotkey graphic with NAME_<BUTTON>).

## The menu

- No button held: boot the AUTO entry at once (0 ms).
- A face button held at boot: its hotkey entry, as PS2BBL does. Any other press opens the hotkey menu: each button with
  its name and path, and a clear first row, BOOT RIPPS2 (AUTO), to leave the menu and boot.

## Paths: edited in RIPPS2, read from the file

Editing paths with a keyboard inside the loader would make it heavy. The fork stays light and only reads its
CONFIG.INI (mmce?:/BIBLE/CONFIG.INI, mc?:/BIBLE/CONFIG.INI, the same search order as PS2BBL Extended). RIPPS2's BIBLE
page edits that file in RIPPS2's own look: AUTO, the four face buttons, BIBLE_GLYPHS and the wait. The BIBLE page says
so in a note: "BIBLE's paths are edited here; the loader reads them at power on."

## Builds

As PS2BBL Extended does: one build per device set (MMCE=1 needs the homebrew SIO2MAN and leaves out MX4SIO), so
RIPPS2 installs the one that matches where RIPPS2 lives.

## Steps

1. Fork saildot4k/PlayStation2-Basic-BootLoader-Extended (public, GPL-3.0) as the BIBLE repo; CI builds every variant.
2. 0 ms and the single pad read; the splash with BIBLE_GLYPHS; the hotkey menu with BOOT RIPPS2 first.
3. RIPPS2: the BIBLE page edits the fork's CONFIG.INI; Manage installs the fork's ELF beside the 1.20 KELF (or on the
   SD2PSX's SD) and points the first stage at it; the note on the page.
4. Lab: PCSX2 with a MagicGate card image and BIBLE (1.20 -> fork -> RIPPS2 on MMCE is a hardware test: PCSX2 has no MMCE).

Needs the user's word before step 1 (a public repository).
