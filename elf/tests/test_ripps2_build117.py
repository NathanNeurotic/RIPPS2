"""Build 117: the sidebar's keys alike on every theme (Circle and a list's Left open it, Right steps no source, L1 / R1 the
theme's own, RIPFLOW's and RIPGRID's covers round their ends), RIPFLOW's flowtilt, the RIPDISC and theme boxes flush with
the bar, the sidebar drawn over the page; every audio file read survives the SD2PSX losing a descriptor (.wav and .mp3
through the Ogg music's own source, a short sound read again, the rip writing with the IO worker held); a launch from a
waiting row asks its drive for its list while it waits.

Static checks on the patched tree."""
import os
import sys
from pathlib import Path
from r2src import unwrap  # noqa: E402

root = Path(os.environ.get('RIPTOPL_DIR', '.'))
rd = lambda p: unwrap((root / p).read_text(encoding='utf-8').replace('\r\n', '\n'))
fail = []


def need(text, items, where):
    for s, why in items:
        if s not in text:
            fail.append('%s: %s' % (where, why))


def body(text, head):
    i = text.index(head)
    return text[i:text.index('\n}\n', i) + 3]


# ---- audio
snd = rd('src/sound.c')
for name in ('static int wavOpen(const char *path)', 'static int mp3Open(const char *path)', 'static int wavNextFrame(short *out)',
             'static void mp3Fill(void)', 'static int mp3Decode(void)'):
    b = body(snd, name)
    if 'fopen(' in b or 'fread(' in b or 'fseek(' in b:
        fail.append('sound.c %s: reads through the music\'s source (bgmSource*), not a bare FILE*' % name.split('(')[0])
need(snd, (('static void *audSrcOpen(const char *path)', 'a source for a file the engine reads itself'),
           ('for (int tries = 0; ret != size && tries < 3; tries++) {', 'a sound read short is read again'),
           ('sfxHeaderMs((const unsigned char *)buffer, size) != ms', 'and checked whole')), 'sound.c')
rip = body(rd('src/ripps2biossnd.c'), 'void ripps2RipBiosMusicDialog(void)')
if rip.index('ioBlockOps(1);') > rip.index('rbsRipPiece(') or rip.index('ioBlockOps(0);') < rip.index('rbsRipPiece('):
    fail.append('ripps2biossnd.c: the music is written with the IO worker held')

# ---- keys
menu = rd('src/menusys.c')
need(menu, (('int sb = ripps2SidebarOn(), side = sb && !cf && !grid && !gTheme->sbLeftList, flowSide = sb && cf && !grid, gridSide = sb && grid;',
             'one rule for every theme with the sidebar on'),
            ('} else if (gridSide && getKey(KEY_LEFT)) {\n        menuPrevV();', "RIPGRID's Left walks its covers round the end"),
            ('if (!ripps2SidebarOn()) // build 117: with the sidebar on, the info page leaves L1 / R1 alone', 'the info page leaves L1 / R1 alone'),
            ("(pages == 1 && !ripps2SidebarOn()) ? ripps2StepCategory(-1) : menuFirstPage()", 'L2 / R2 never step the categories with the sidebar on')),
     'menusys.c')
keys = menu[menu.index('int sb = ripps2SidebarOn(), side'):menu.index('} else if ((menuSourceCycleActive() || ripps2SidebarOn())')]
if 'menuGridAtStart()' in keys:
    fail.append('menusys.c: RIPGRID\'s Left no longer opens the sidebar from its first column')
ui = rd('src/ripps2ui.c')
launch = body(ui, 'void ripps2HandleInputLaunch(void)')
if 'if (ripps2SidebarOn() && (getKeyOn(KEY_L1) || getKeyOn(KEY_R1))) {' not in launch:
    fail.append('ripps2ui.c: Launch Disc leaves L1 / R1 alone with the sidebar on')
need(ui, (('void ripps2TiltBeginFlow(int cx, int cy, int scalePct, float turn)', "RIPFLOW's flowtilt"),
          ('padGetLeftStick(&lx, &ly);', 'the left stick tips it too'),
          ('void ripps2BoxSpan(int *x, int *w)', 'a box flush with the bar')), 'ripps2ui.c')
if body(ui, 'static void tpDraw(').count('ripps2BoxSpan(&x, &w);') != 1 or body(ui, 'void ripps2ThemeHoldRender(void)').count('ripps2BoxSpan(&x, &w);') != 1:
    fail.append('ripps2ui.c: the themes box is flush with the bar, held and open')
if 'ripps2BoxSpan(&x, &w);' not in body(rd('src/ripps2disc.c'), 'void ripps2DiscRipRender(void)'):
    fail.append('ripps2disc.c: the RIPDISC box is flush with the bar')
side = rd('src/ripps2side.c')
need(side, (('void ripps2SidebarFlush(void)', 'the sidebar drawn after the page'), ('int ripps2SidebarEdge(void)', 'where the bar ends')), 'ripps2side.c')
gui = rd('src/gui.c')
if 'ripps2SidebarDefer(1); // build 117' not in gui or 'ripps2SidebarFlush();' not in gui:
    fail.append('gui.c: the page is drawn, then the sidebar over it')
th = rd('src/themes.c')
need(th, (('newT->flowTilt = configGetInt(themeConfig, "flowtilt", &intValue) && intValue == 1;', 'the flowtilt key'),
          ('ripps2TiltBeginFlow(posX, posY,', "RIPFLOW's centre case tips with it")), 'themes.c')
if 'flowtilt=1' not in rd('misc/theme_coverflow.cfg'):
    fail.append('theme_coverflow.cfg: RIPFLOW has flowtilt=1')

# ---- RIPSHOT on MMCE: the roll on the SD, handed over by the card's descriptor
cfg = rd('modules/iopcore/common/cdvd_config.h')
mmce_struct = cfg[cfg.index('struct cdvdman_settings_mmce'):]
mmce_struct = mmce_struct[:mmce_struct.index('} __attribute__((packed));')]
if 'int roll_fd1;' not in mmce_struct:
    fail.append('cdvd_config.h: the MMCE settings carry the roll\'s card descriptor (plus 1)')
dev = rd('modules/iopcore/cdvdman/device-mmce.c')
roll_io = body(dev, 'int DeviceRollIo(int write, u32 offset, void *buf, u32 size)')
if 'mmce_write_offset(fd, offset, size' not in roll_io or 'mmce_read_offset(fd, offset, size' not in roll_io:
    fail.append('device-mmce.c: the roll is read and written by offset, as the VMCs are')
if 'return cdvdman_settings.roll_fd1 > 0 ? RS_ROLL_BYTES : 0;' not in dev:
    fail.append('device-mmce.c: the roll\'s size once one was handed over')
shot = rd('src/ripps2shot.c')
prep = body(shot, 'void ripps2ShotPrepareMmce(')
need(prep, (('fileXioIoctl2(rsMmceFd, 0x80, NULL, 0, NULL, 0)', "the card's own descriptor"),
            ('settings->roll_fd1 = cardFd + 1;', 'handed over'),
            ('rsLaunch.state = RIPSHOT_READY;', 'ready for the menu')), 'ripps2ShotPrepareMmce')
if '!strncmp(mode, "MMCE", 4)' not in body(shot, 'void ripps2ShotFillConfig('):
    fail.append('ripps2ShotFillConfig: an MMCE launch gets its roll\'s state')
if 'if (!haveBlank && strncmp(root, "mmce", 4))' not in body(shot, 'static void rsJob(void)'):
    fail.append('rsJob: no blank roll written over the bus the pads share')
if 'ripps2ShotPrepareMmce(settings, mmcePrefix, game->startup, game->name);' not in rd('src/mmcesupport.c'):
    fail.append('mmcesupport.c: the launch prepares the roll')

# ---- the launch wait asks its drive
mix = rd('src/mixsupport.c')
wait = body(mix, 'int mixWaitForRow(struct menu_item *menu)')
if 'mixPokeFamily(fam);' not in wait:
    fail.append('mixWaitForRow: the drive is asked for its list while the launch waits')

if fail:
    print('\n'.join(fail))
    sys.exit(1)
print('build117: the sidebar keys on every theme, flowtilt, boxes flush with the bar, the sidebar on top, audio reads that survive a lost descriptor, the launch wait asks its drive OK')
