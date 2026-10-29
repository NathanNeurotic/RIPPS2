# RIPPS2 Media Studio

A small PC app that makes the `AUDIO` and `MEDIA` folders for RIPPS2: your own sounds and music, and your videos, in the formats the PS2 plays. (It was RIPPS2 Audio Studio until it learned video.)

- **Browse** to any sound, song or video (WAV, FLAC, Ogg, MP3, MP4, MKV, MOV, WebM and more). Play a sound as it is, or as the PS2 will play it (mono SPU2 ADPCM at 44.1 kHz), before you convert it.
- **Convert a sound** into one of RIPPS2's sounds (RiptOPL's `boot`, `cursor`, `confirm`, `cancel`, `message`, `transition`, `bd_connect`, `bd_disconnect`, then RIPPS2's `page_in`, `page_out`, `error`, `save`, `launch`, `disc`, `random`) or into a music track.
- **Convert a video** into the AVI RIPPS2's Memory Files plays: XviD video at 1.5 Mbps with MP3 sound at 48 kHz stereo, at most 640 x 480 and 30 frames a second, its shape kept (a phone's upright video stays upright). The info panel shows what it will become and about how big before you start. A video's sound can also be made into music or a sound.
- **Start** converts a whole folder: files named for an event become that sound, long ones become music, videos become PS2 videos.
- **Your BIOS:** pick the BIOS dump of your own PS2 (the file PCSX2 uses) and the app renders the console's own menu sounds and system music from it, the way its sound chip plays them: the boot, the tower tunnel, the PS2 logo, the clock and the ambient music. Start rips the lot into a full AUDIO folder. Nothing from any BIOS ships with RIPPS2 or this app; it reads only the dump you give it, on your PC. (RIPPS2 can also rip them on the console itself: Audio Settings > BIOS Sounds and BIOS Music.)

Sounds and music land in `output/AUDIO` beside the app, videos in `output/MEDIA`. Copy them to a USB stick, then with RIPPS2's **Memory Files** put `AUDIO` beside `RIPPS2.ELF` and `MEDIA` on your biggest drive. In RIPPS2, Audio Settings > Music picks the track, and Cross on a video in Memory Files plays it full screen (START pauses, Circle or SELECT stops).

The AUDIO FOLDER tab shows how much of the PS2's sound RAM your sounds use: RIPPS2 loads every sound into the SPU2's 2 MB at once (the music streams, so it does not count). The MEDIA FOLDER tab lists your PS2 videos with their length and size; Cross opens one in your PC's own player to check it.

## Why convert video at all

The PS2 cannot play what phones and websites make (H.264 in an MP4): its processor is far too slow for that, and RIPPS2 will not try. It plays MPEG-4 ASP (XviD, DivX) in an AVI well, so the PC does the heavy lifting once and the PS2 just plays the result.

## Run it

- **Windows app: [download RIPPS2-Media-Studio.zip](https://github.com/akilluminati47/RIPPS2/releases/download/media-studio/RIPPS2-Media-Studio.zip)**, unzip it anywhere and double-click `RIPPS2 Media Studio.exe`. No install and no Python: ffmpeg and ffprobe are in the zip beside it (keep them there: they read more audio formats, write Ogg music and do all the video work). The zip is rebuilt by GitHub Actions whenever the studio changes ([its release page](https://github.com/akilluminati47/RIPPS2/releases/tag/media-studio)); `build_exe.bat` builds the .exe yourself.
- **From source:** Python 3.10 or newer, then `pip install -r requirements.txt` and `python studio.py` (or double-click `run_studio.bat`). ffmpeg on the PATH or beside `studio.py`.
- **Without the window:** `python studio.py --video <file>` writes one PS2 video into `output/MEDIA`.

Controls: arrows move, Enter opens or converts, Backspace goes back, Space plays, P plays the PS2 version (or deletes, on the folder tabs), Tab (or Q / E) switches tabs, S converts a folder or rips a BIOS, O opens the output folder. The mouse works (double-click), and so does a gamepad: Cross, Circle, Square, Triangle, L1 / R1, Start.

## Files

- `studio.py`: the app (pygame).
- `adpcm.py`: the `.adp` encoder and decoder (the same as `elf/theme/tools/make_adp.py`).
- `audio_io.py`: reading audio, writing `.adp` and music.
- `video_io.py`: reading a video's size, length and frame rate, and making the PS2 video with ffmpeg (libxvid and libmp3lame when the ffmpeg has them, its own MPEG-4 and MP2 otherwise).
- `ps2bios.py`: reads a PS2 BIOS dump's sound image (its ROM directory, the BIOS's LZ compression, the SSHD sound banks and SSSQ sequences) and renders them with an SPU2 voice model (ADPCM, the ADSR envelope, pitch, pan). `python ps2bios.py <bios.bin> <folder>` writes every menu sound as a WAV.
- `test_studio.py`: drives the app off screen and checks its output (a phone video included, when ffmpeg is there).
- `build_exe.bat`: builds the Windows app with PyInstaller.
