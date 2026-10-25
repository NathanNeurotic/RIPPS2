"""Turn a real RIPPS2 PCSX2 capture into a Discord GIF.

For a smooth animated scene, record with PCSX2 and use --video. The still-image option remains
available for a tower frame blended into captures of the empty All Games screen.

    python make_boot_gif.py --video out/recording.mp4 --trim-start 0 --duration 28 \
      --fps 12 --width 560 --out ../../media/b114/ripps2-boot-empty-games.gif

    python make_boot_gif.py --intro out/boot.png --list-frame out/allgames-1.png \
      --list-frame out/allgames-2.png --list-frame out/allgames-3.png \
      --out ../../media/b114/ripps2-boot-empty-games.gif
"""
import argparse
import os
import shutil
import subprocess

from PIL import Image


def load(path, size):
    im = Image.open(path).convert('RGB')
    if abs(im.width / im.height - 4 / 3) > 0.002:
        raise ValueError('%s is %s, expected a 4:3 PCSX2 capture' % (path, im.size))
    return im.resize(size, Image.Resampling.LANCZOS)


def gif_frames(intro, stills):
    # Build frames in RGB first, then derive one palette from all of them to avoid color banding
    # where a per-frame palette would make the night-sky gradient jump during the dissolve.
    frames = [intro] * 4
    first = stills[0]
    for i in range(1, 13):
        frames.append(Image.blend(intro, first, i / 12.0))
    frames.extend(stills)
    frames.extend([stills[-1]] * 10)
    composite = Image.new('RGB', (intro.width, intro.height * len(frames)))
    for i, frame in enumerate(frames):
        composite.paste(frame, (0, i * intro.height))
    palette = composite.quantize(colors=256, method=Image.Quantize.FASTOCTREE)
    return [f.quantize(palette=palette, dither=Image.Dither.FLOYDSTEINBERG) for f in frames]


def main():
    ap = argparse.ArgumentParser()
    source = ap.add_mutually_exclusive_group(required=True)
    source.add_argument('--video', help='native PCSX2 capture; keeps the animated towers smooth')
    source.add_argument('--intro', help='tower frame for the still-based boot-to-list version')
    ap.add_argument('--list-frame', action='append', default=[])
    ap.add_argument('--out', required=True)
    ap.add_argument('--trim-start', type=float, default=0, help='seconds to trim from the video head')
    ap.add_argument('--duration', type=float, default=28, help='video seconds to include')
    ap.add_argument('--fps', type=int, default=12, help='GIF frames per second in video mode')
    ap.add_argument('--width', type=int, default=560, help='GIF width in video mode')
    args = ap.parse_args()
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    if args.video:
        ffmpeg = shutil.which('ffmpeg')
        if not ffmpeg:
            ap.error('ffmpeg is required for --video')
        if args.fps < 1 or args.width < 1 or args.duration <= 0 or args.trim_start < 0:
            ap.error('video timing, fps, and width must be positive')
        graph = (
            '[0:v]fps=%d,scale=%d:-1:flags=lanczos,split[s0][s1];'
            '[s0]palettegen=max_colors=256:stats_mode=diff[p];'
            '[s1][p]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle[v]'
        ) % (args.fps, args.width)
        cmd = [ffmpeg, '-hide_banner', '-loglevel', 'error', '-y', '-ss', str(args.trim_start),
               '-t', str(args.duration), '-i', os.path.abspath(args.video), '-filter_complex', graph,
               '-map', '[v]', '-an', '-loop', '0', '-gifflags', '+transdiff', os.path.abspath(args.out)]
        subprocess.run(cmd, check=True)
        print(args.out, '(%d bytes)' % os.path.getsize(args.out))
        return
    if not args.list_frame:
        ap.error('--list-frame is required with --intro')
    size = (800, 600)
    intro = load(args.intro, size)
    stills = [load(p, size) for p in args.list_frame]
    frames = gif_frames(intro, stills)
    frames[0].save(args.out, save_all=True, append_images=frames[1:], duration=90, loop=0,
                   optimize=False, disposal=2)
    print(args.out, '(%d frames, %d bytes)' % (len(frames), os.path.getsize(args.out)))


if __name__ == '__main__':
    main()
