"""psx-place drafts, the user's 10/28 notes: the first post shows RIPGRID in Japanese on Ratchet & Clank instead of the
1080i shot, and Adapt Rx's info page on Aqua Teen instead of Adapt's list; the bump shows only 1080i pictures of what
the first post does not (the CD player, the media player, RIPPS2's save icon, the browser on a picture, the picture
viewer), all in a spoiler as psx-place's rules ask. Writes psxplace-post.bbcode, psxplace-bump.bbcode and the notes."""
P = r'B:\Webpages - Projects\ps2-pillars\tools\discord'
RAW = 'https://raw.githubusercontent.com/akilluminati47/RIPPS2/main/media/'


def rw(path, fn):
    s = open(path, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in s else '\n'
    s = fn(s.replace('\r\n', '\n'))
    open(path, 'w', encoding='utf-8', newline='').write(s.replace('\n', nl))
    return s


def first(s):
    for a, b in ((RAW + 'b114/tour-03-adapt.jpg', RAW + 'b119/tour-adaptrx-info.jpg'),
                 ('[IMG]' + RAW + 'b119/1080i-storage.jpg[/IMG]\n', '[IMG]' + RAW + 'b119/tour-ripgrid-japanese.jpg[/IMG]\n')):
        assert s.count(a) == 1, a
        s = s.replace(a, b)
    return s


BUMP = """[CENTER][MEDIA=youtube]RECAP_VIDEO_ID[/MEDIA][/CENTER]

[SIZE=5][B]RIPPS2: the tour[/B][/SIZE]
A new video for anyone just finding the thread: where RIPPS2 came from (a web page that drew the PS2's menu) and what it does now, start to end, over the console's own music ripped from its BIOS. The first post has the download and everything RIPPS2 does.

[B]What's new is always on GitHub[/B]
[LIST]
[*][URL='https://github.com/akilluminati47/RIPPS2/releases/latest']The latest release[/URL]: what changed, with the newest RIPPS2.elf, the theme pack and the languages.
[*][URL='https://github.com/akilluminati47/RIPPS2/blob/main/CHANGELOG.md']The changelog[/URL]: every build, from the first alpha to now.
[*][URL='https://github.com/akilluminati47/RIPPS2/issues'][B]Issues[/B][/URL]: found a bug, or want something? Open an issue. It is the best way to get RIPPS2 updated: each one is tracked until it is fixed. Add your console model, your drives, your boot loader and your DIAG.TXT (STATUS > SAVE DIAGNOSTICS).
[/LIST]

[SPOILER="Screenshots, in 1080i"]
In 1080i (Settings > Interface > Video Mode, widescreen on), the art keeps its shape:
[IMG]""" + RAW + """b119/1080i-storage.jpg[/IMG]
[IMG]""" + RAW + """b119/1080i-info-page.jpg[/IMG]
Memory Files: your own tracks, marked and played together as one CD, the towers lit by the music:
[IMG]""" + RAW + """b119/1080i-cd-player.jpg[/IMG]
Video, full screen (the player sets the screen to the video's own size):
[IMG]""" + RAW + """b119/media-player.jpg[/IMG]
RIPPS2's own save on the memory card, and its icon in 3D:
[IMG]""" + RAW + """b119/1080i-save.jpg[/IMG]
[IMG]""" + RAW + """b119/1080i-save-icon.jpg[/IMG]
The file browser on a picture, and the picture viewer:
[IMG]""" + RAW + """b119/1080i-browser-picture.jpg[/IMG]
[IMG]""" + RAW + """b119/1080i-picture-viewer.jpg[/IMG]
[/SPOILER]

Thanks to everyone testing RIPPS2 on Discord and opening issues on GitHub: be like them. Special thanks to all the YouTube love as well: glad to help however you reach me.
"""

if __name__ == '__main__':
    f = rw(P + r'\psxplace-post.bbcode', first)
    rw(P + r'\psxplace-bump.bbcode', lambda s: BUMP)
    notes = open(P + r'\notes\psxplace-recap.txt', encoding='utf-8').read().replace('\r\n', '\n')
    head = notes[:notes.index('=== 1. FIRST POST')]
    out = head + '=== 1. FIRST POST (edit the thread\'s first post: replace it all with this) ===\n\n' + f.rstrip('\n') + \
        '\n\n=== 2. BUMP (a new reply in the thread) ===\n\n' + BUMP
    open(P + r'\notes\psxplace-recap.txt', 'w', encoding='utf-8', newline='\r\n').write(out)
    assert '\u2014' not in out
    print('ok')
