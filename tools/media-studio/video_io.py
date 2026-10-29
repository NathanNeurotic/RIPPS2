"""Turning any video into the AVI RIPPS2 plays in Memory Files.

RIPPS2's player (libsmslite, the SMS core) reads one container and two codecs: an AVI with MPEG-4 ASP video
(XviD, DivX) and MPEG-1 layer III or II sound. So a video is made 640 pixels wide at most (no taller than 480),
at no more than 30 frames a second, as XviD at about 1.5 Mbps with MP3 at 48 kHz stereo: well inside what the
PS2's USB reads (about 1 MB a second). Everything goes through ffmpeg, which reads almost any video there is.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

import audio_io as aio

VIDEO_EXT = {'.mp4', '.m4v', '.mkv', '.mov', '.webm', '.avi', '.wmv', '.flv', '.mpg', '.mpeg', '.ts', '.m2ts', '.mts',
             '.vob', '.3gp', '.ogv', '.divx', '.xvid', '.asf'}
MAX_W, MAX_H = 640, 480
MAX_FPS = 30.0
VIDEO_KBPS = 1500
AUDIO_KBPS = 128

_ENCODERS = {}


def ffprobe_path():
    ff = aio.ffmpeg_path()
    if ff:
        p = Path(ff).with_name('ffprobe' + Path(ff).suffix)
        if p.exists():
            return str(p)
    return shutil.which('ffprobe')


def has_encoder(name):
    """Whether this ffmpeg was built with an encoder (libxvid, libmp3lame); asked once."""
    ff = aio.ffmpeg_path()
    if ff not in _ENCODERS:
        try:
            out = subprocess.run([ff, '-hide_banner', '-encoders'], capture_output=True, text=True).stdout
        except (OSError, TypeError):
            out = ''
        _ENCODERS[ff] = {ln.split()[1] for ln in out.splitlines() if len(ln.split()) > 1 and len(ln.split()[0]) == 6}
    return name in _ENCODERS[ff]


def _rate(s):
    try:
        a, b = s.split('/') if '/' in s else (s, '1')
        return float(a) / float(b) if float(b) else 0.0
    except (ValueError, AttributeError):
        return 0.0


def probe(path):
    """A video's length, size, frame rate and whether it has sound: dict, or None when ffmpeg cannot read it."""
    fp = ffprobe_path()
    if fp:
        p = subprocess.run([fp, '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)],
                           capture_output=True, text=True)
        if p.returncode != 0:
            return None
        d = json.loads(p.stdout or '{}')
        v = next((s for s in d.get('streams', []) if s.get('codec_type') == 'video'), None)
        if v is None:
            return None
        w, h = int(v.get('width', 0)), int(v.get('height', 0))
        rot = 0
        for sd in v.get('side_data_list', []):
            rot = int(float(sd.get('rotation', 0) or 0))
        rot = rot or int(v.get('tags', {}).get('rotate', 0) or 0)
        if abs(rot) % 180 == 90:
            w, h = h, w
        return dict(duration=float(d.get('format', {}).get('duration', 0) or v.get('duration', 0) or 0), width=w, height=h,
                    fps=_rate(v.get('avg_frame_rate', '0')) or _rate(v.get('r_frame_rate', '0')), codec=v.get('codec_name', ''),
                    audio=any(s.get('codec_type') == 'audio' for s in d.get('streams', [])))
    ff = aio.ffmpeg_path()
    if not ff:
        return None
    err = subprocess.run([ff, '-hide_banner', '-i', str(path)], capture_output=True, text=True).stderr
    m = re.search(r'Video: (\w+).*?, (\d{2,5})x(\d{2,5})', err)
    if not m:
        return None
    t = re.search(r'Duration: (\d+):(\d+):([\d.]+)', err)
    f = re.search(r'([\d.]+) fps', err)
    return dict(duration=(int(t[1]) * 3600 + int(t[2]) * 60 + float(t[3])) if t else 0.0, width=int(m[2]), height=int(m[3]),
                fps=float(f[1]) if f else 0.0, codec=m[1], audio='Audio:' in err)


def plan(info):
    """What the PS2 version will be: its size, frame rate and about how big the file comes out."""
    w, h = max(16, info['width']), max(16, info['height'])
    k = min(1.0, MAX_W / w, MAX_H / h)
    # whole 16 x 16 blocks, as the decoder and the IPU work in them (a few percent of stretch at most)
    ow, oh = max(16, int(round(w * k / 16)) * 16), max(16, int(round(h * k / 16)) * 16)
    ow, oh = min(ow, MAX_W), min(oh, MAX_H)
    fps = info['fps'] or 25.0
    while fps > MAX_FPS + 0.5:
        fps /= 2
    kbps = VIDEO_KBPS + (AUDIO_KBPS if info['audio'] else 0)
    return dict(width=ow, height=oh, fps=round(fps, 3), bytes=int(info['duration'] * kbps * 1000 / 8 * 1.02))


def out_name(src, folder):
    """A file name the PS2's drives all take: the video's own name, plain, as .avi, never over one already there."""
    stem = ''.join(c if c.isalnum() or c in ' -_()&,.' else ' ' for c in Path(src).stem)
    stem = ' '.join(stem.split())[:60].strip(' .') or 'Video'
    dst, n = Path(folder) / (stem + '.avi'), 2
    while dst.exists():
        dst, n = Path(folder) / ('%s (%d).avi' % (stem, n)), n + 1
    return dst


def convert(src, dst, progress=None):
    """src -> dst, the AVI RIPPS2 plays. Returns dst; a failed run removes what it wrote."""
    ff = aio.ffmpeg_path()
    if not ff:
        raise ValueError('making a PS2 video needs ffmpeg (put ffmpeg.exe beside the app)')
    info = probe(src)
    if info is None:
        raise ValueError('ffmpeg could not find a picture in this file')
    pl = plan(info)
    if has_encoder('libxvid'):
        vcodec = ['-c:v', 'libxvid']
    else:  # ffmpeg's own MPEG-4 ASP, marked as XviD as the player expects
        vcodec = ['-c:v', 'mpeg4', '-vtag', 'XVID']
    vcodec += ['-b:v', '%dk' % VIDEO_KBPS, '-maxrate', '%dk' % (VIDEO_KBPS * 2), '-bufsize', '%dk' % (VIDEO_KBPS * 2),
               '-g', str(int(pl['fps'] * 10)), '-pix_fmt', 'yuv420p']
    if has_encoder('libmp3lame'):
        acodec = ['-c:a', 'libmp3lame', '-b:a', '%dk' % AUDIO_KBPS]
    else:
        acodec = ['-c:a', 'mp2', '-b:a', '192k']
    acodec += ['-ar', '48000', '-ac', '2']
    dst = Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    part = dst.with_name(dst.stem + '.part.avi')
    cmd = [ff, '-v', 'error', '-y', '-i', str(src), '-map', '0:v:0', '-map', '0:a:0?', '-sn', '-dn', '-map_metadata', '-1',
           '-vf', 'scale=%d:%d,setsar=1' % (pl['width'], pl['height']), '-r', str(pl['fps'])] + vcodec + acodec + \
          ['-f', 'avi', '-progress', 'pipe:1', '-nostats', str(part)]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    total = max(info['duration'], 0.001)
    for line in p.stdout:
        if line.startswith('out_time_us=') or line.startswith('out_time_ms='):
            try:
                us = int(line.split('=', 1)[1])
            except ValueError:
                continue
            if progress:
                progress(min(0.999, us / 1e6 / total))
    err = p.stderr.read()
    if p.wait() != 0 or not part.exists() or part.stat().st_size == 0:
        part.unlink(missing_ok=True)
        raise ValueError('ffmpeg stopped: %s' % (err.strip().splitlines() or ['no reason given'])[-1])
    part.replace(dst)
    if progress:
        progress(1.0)
    return dst
