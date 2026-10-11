# Build 95: a stability build. Sound effects rebuilt (no more quiet waves or stale sounds), a safer boot with ripped sounds, and RIPFLOW fixed.

## Sound effects (95)
- A held cursor ticks cleanly, never goes quiet in waves, and old sounds never come back. No sounds are built in: **BIOS Sounds > Rip** or RIPPS2 Audio Studio fill `AUDIO`. **STATUS > SOUNDS** shows what is loaded. Ripped sounds end at silence (rip again).

## Safer boot (95)
- Sound files are read only by the drive worker and checked before use. If ripped sounds froze your boot before, this is the build to try.

## Fixed (95)
- **RIPFLOW** works again (a string-function clash from the video player, since build 93). **MX4SIO** may be back. **JPG** pictures open whole, and JPG game art shows.

## Test list
- Boot with your ripped `AUDIO` folder: no freeze? Where are RIPPS2 and `AUDIO` (memory card, USB, HDD)?
- Hold Up or Down on a long list for a few seconds: steady ticks, no quiet gaps, nothing playing afterwards?
- Open and close info pages and menus quickly: one clean sound each time?
- **STATUS > SOUNDS**: the right count and folder? Try RIP THIS CONSOLE'S SOUNDS, then reboot.
- **MX4SIO** (FifthFox): does it show up again?
- **RIPFLOW**: covers in a flow again?
- A big **JPG** photo in Memory Files: whole every time?
- JPG covers (`<ID>_COV.jpg` in ART, no PNG): do they show?
- An `.adp` in Memory Files: Cross plays it, Back closes, menu sounds come back?
- POPSTARTER from HDD and iLink, Neutrino on iLink: any better? (Not changed directly; the string fix touched everything.)

## Report
Post here with your **console model**, where RIPPS2 and your `AUDIO` folder live, and a **photo** of anything odd.
