# Fonts: a "mother font", weighed before anything changes

The user (10/22): "before we do any font weigh the pros and cons and make it so we keep the styles implemented fully if
we can before changing anything font related plan it". Nothing font related changes until this plan is agreed.

## What RIPPS2 has now

| Face | File | Size | Drawn by | Used for |
|---|---|---|---|---|
| Planet N Compact | assets/master.ttf | 34.6 KB | Iconian Fonts (not ours to change) | the main face: categories, titles, most theme text |
| RIPPS2 One | ripps2_one.ttf | 1 KB | RIPPS2 | Planet N's missing 1 (its 1 is its I) |
| RIPPS2 Sleek Regular | ripps2_sleek.ttf | 31.5 KB | make_sleek_font.py | hints, menus, settings |
| RIPPS2 Sleek Bold | ripps2_sleek_bold.ttf | 30.9 KB | make_sleek_font.py | labels beside big glyphs, the view word |
| RIPPS2 Sleek Bold Case | ripps2_sleek_case.ttf | 55.3 KB | make_sleek_font.py | typed text, the keyboard, descriptions (a true lowercase) |
| Roboto Condensed / Bold | ripflow.ttf, ripflow_bold.ttf | 30.4 / 19.3 KB | Google (Apache 2.0) | RIPFLOW |

About 200 KB of a 3.1 MB ELF. Every face is compiled in once, and a theme already picks them by name with a size per
slot (`font4=builtin:ripps2sleekbold`, `font4_size=15`), so no theme carries its own copy of a RIPPS2 face.

**The mother font already exists, at build time.** make_sleek_font.py draws every Sleek letter once, as polylines on a
grid, and builds each cut from that one drawing: Bold is the same drawing with a heavier stroke. That gives true drawn
weights from one source, with no runtime cost and nothing lost.

## The options

### A. Keep the faces as files (today), add role keys
Themes name a role ("header", "hint", "body", "title") and RIPPS2 maps it to a face it already ships; the defaults
reproduce today's choices exactly.
- **For:** nothing changes on screen unless a theme asks; every drawn style stays (Sleek Bold's own stroke, Bold
  Case's lowercase, Planet N untouched); no CPU or RAM cost; easy to test (a theme without the keys must look
  identical).
- **Against:** each new style still needs a drawn cut (for Sleek, one more run of the generator).

### B. A runtime mother font: one face per family, the engine makes the rest
FreeType emboldens outlines (FT_Outline_EmboldenXY) for bold, the text is upper-cased in code for caps, and the
advance is widened for tracking.
- **For:** a theme could ask for any weight, case or spacing of any face without a file; fewer files to keep.
- **Against:**
  - A synthetic bold is coarser than a drawn one. The counters close and letters touch (row 4 of
    mockups/b113-header-fonts.png: "LAUNCH DISC" runs together), so it needs tracking to compensate, and still
    looks heavier and blunter than Sleek Bold.
  - Bold Case cannot be derived: its lowercase is a separate design that Regular and Planet N do not have.
  - The savings are small: dropping Sleek Bold and Roboto Bold saves about 50 KB of a 3.1 MB ELF.
  - Every derived style is its own glyph cache, so RAM is not saved where it matters (the EE's 32 MB), only file
    size.
  - Widths change, so any theme laid out against the drawn bold can overflow its boxes: every built-in theme and
    the Adapt pack would need checking at 480p, 720p and 1080i.
  - Planet N belongs to Iconian Fonts. Emboldening it at runtime does not modify the file, but it changes how their
    face looks.

### C. Both, the drawn faces first (recommended)
- Keep every drawn face exactly as it is, and keep the build-time mother (make_sleek_font.py) for any new Sleek
  weight.
- Add role keys (option A) so themes reuse RIPPS2's faces by purpose, defaulting to today's choices.
- Offer runtime bold and tracking (option B) only as an opt-in key, for a font a theme brings that has no bold of
  its own. It is never applied to a RIPPS2 face unless a theme asks.

## The plan (when the user agrees)
1. Audit every place a face is chosen (fntsys ids, theme font slots, RIPPS2_DIA_FONT, the hint and badge code) and
   list it in this file.
2. Role keys with defaults identical to today. A test renders every built-in theme before and after, which must be
   pixel-identical without the new keys.
3. Build 113's sidebar header uses a role key (`header_font`), defaulting to Roboto Condensed Bold (the user's
   "easy to read" pick); Sleek Bold and Planet N are one key away.
4. Runtime bold and tracking behind an opt-in key, tested in the lab next to the drawn Sleek Bold at 480p, 720p and
   1080i before any theme uses it.
5. Only after that, consider whether any file can go (Roboto Bold, if a role can use synthetic bold acceptably).
   Sleek Bold and Bold Case stay.
