# Discord website embed: boot to empty games

This is a local preview of the website's existing Discord rich embed. It keeps the original title and description, uses the RIPPS2 brand icon, adds a general project introduction below the GIF, and provides Website, PSX-Place, GitHub, and guns.lol buttons. Nothing has been posted.

## GIF sequence

The loop uses a fresh launch of the RIPPS2 ELF in the isolated PCSX2 lab. It opens on the close tower animation, settles on the empty All Games list, pauses on the Start menu for about 10 seconds, then returns to the list before looping. It does not enter the Settings page. The capture shows 60 fps source video with no HDD error; the Discord GIF is 800 px wide at 12 fps to keep the full loop within a practical attachment size.

## Lab and source capture

- PCSX2 lab: `B:\Emulation\PlayStation\PCSX2\ripps2-lab-emptygames-capture`
- ELF: `RIPPS2.elf` in the lab folder.
- Virtual HDD: zero-filled `hdd-blank-2gb.raw`, enabled in this lab's `PCSX2.ini`.
- Memory cards: lab scratch cards only; the user's original cards and reel disks are not used.
- Source video: `videos\RIPPS2 [_]_RIPPS2_20261025000556.mp4`, 1920x1080, 60 fps, 28.05 seconds.
- GIF: `media/b114/ripps2-boot-empty-games.gif`, 560x315, 12 fps, 28 seconds, 11,056,703 bytes.

Recreate the GIF with:

```powershell
python tools/discord/make_boot_gif.py `
  --video 'B:\Emulation\PlayStation\PCSX2\ripps2-lab-emptygames-capture\videos\RIPPS2 [_]_RIPPS2_20261025000556.mp4' `
  --trim-start 0 --duration 28 --fps 12 --width 560 `
  --out media/b114/ripps2-boot-empty-games.gif
```

## Preview files

- `out/boot-empty-games/embed-preview.html` — rendered local preview.
- `out/boot-empty-games/component-embed.json` — Discord Component Embed payload for review.
- `out/boot-empty-games/ripps2-boot-empty-games.gif` — copied GIF attachment.
- `tools/discord/make_boot_embed.py` — rebuilds the preview and payload from the website embed copy.

## Website link preview

`index.html` contains Discord's inline `<script id="discord:component-embed" type="application/json">` payload. Discord reads it when someone posts the website URL and renders the title, existing description, brand icon, GIF gallery, general introduction bullets, and four URL buttons as a Component Embed. The payload is under Discord's 3,000-byte limit. The Open Graph and Twitter tags remain as fallbacks.

The Component Embed and GIF are published from `main` in commit `f0f0e8b`. GitHub Pages reports the build as complete. A live fetch using Discordbot's user agent returned the inline payload and the GIF with HTTP 200; the payload is 1,544 bytes and the GIF is 11,056,703 bytes. Component previews require Discord's crawler to reach the page and all media within 10 seconds; the GIF was reduced to 560x315 while retaining the 12 fps, 28-second sequence. The live asset fetched in about one second from the build host; Discord's Embed Debugger can be used to inspect the rendered card if needed.
