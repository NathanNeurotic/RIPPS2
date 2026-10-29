"""Build 124's languages: the three Screen position hints (H-POS, V-POS, Overscan) end with the same note, that the
position is kept for each video mode. Each language's own hint is kept and its sentence added. Writes s124.json (no new
strings), labels124.json and tr124/<Language>.json for merge124.py.    python batch124.py"""
import json
import os

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
LANG = os.path.join(HERE, '..', '..', 'elf', 'lang')
KEYS = {'HINT_XOFF': 'Moves the menu left or right on screen. Kept for each video mode.',
        'HINT_YOFF': 'Moves the menu up or down on screen. Kept for each video mode.',
        'HINT_MENU_OVERSCAN': 'Shrinks the menu inward if the TV cuts off its edges. Kept for each video mode.'}
NOTE = {
    'Albanian': ' Ruhet për çdo mënyrë video.', 'Arabic': ' يُحفظ لكل وضع فيديو.', 'Bulgarian': ' Запазва се за всеки видеорежим.',
    'Cebuano': ' Gitipigan para sa matag video mode.', 'Croatian': ' Pamti se za svaki video način.',
    'Czech': ' Uloží se pro každý režim videa.', 'Danish': ' Gemmes for hver videotilstand.', 'Dutch': ' Bewaard per videomodus.',
    'Filipino': ' Naka-save para sa bawat video mode.', 'French': ' Conservé pour chaque mode vidéo.',
    'Galician': ' Gárdase para cada modo de vídeo.', 'German': ' Wird für jeden Videomodus gespeichert.',
    'Greek': ' Αποθηκεύεται για κάθε λειτουργία βίντεο.', 'Hungarian': ' Minden videómódhoz külön megmarad.',
    'Indonesian': ' Disimpan untuk setiap mode video.', 'Italian': ' Memorizzato per ogni modalità video.',
    'Japanese': 'ビデオモードごとに保存されます。', 'Korean': ' 비디오 모드마다 따로 저장됩니다.',
    'Laotian': ' ຈື່ໄວ້ສຳລັບແຕ່ລະໂໝດວິດີໂອ.', 'Persian': ' برای هر حالت ویدیو جداگانه نگه داشته می‌شود.',
    'Polish': ' Zapamiętywane dla każdego trybu wideo.', 'Portuguese': ' Guardado para cada modo de vídeo.',
    'Portuguese_BR': ' Salvo para cada modo de vídeo.', 'Romana': ' Se păstrează pentru fiecare mod video.',
    'Russian': ' Сохраняется для каждого видеорежима.', 'SChinese': '每种视频模式各自保存。',
    'Serbian': ' Pamti se za svaki video režim.', 'Spanish': ' Se guarda para cada modo de vídeo.',
    'Swedish': ' Sparas för varje videoläge.', 'TChinese': '每種視訊模式各自儲存。',
    'Turkish': ' Her video modu için ayrı saklanır.', 'Vietnamese': ' Được lưu riêng cho từng chế độ video.',
}

json.dump([], open(os.path.join(HERE, 's124.json'), 'w', encoding='utf-8'))
json.dump(KEYS, open(os.path.join(HERE, 'labels124.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
os.makedirs(os.path.join(HERE, 'tr124'), exist_ok=True)
missing = []
for lang, note in NOTE.items():
    labels = yaml.safe_load(open(os.path.join(LANG, lang + '.yml'), encoding='utf-8'))['labels']
    out = {}
    for k, en in KEYS.items():
        old = labels.get(k)
        if old is None:  # never translated: the English, as the template has it
            missing.append('%s %s' % (lang, k))
            old = en[:-len(' Kept for each video mode.')]
        old = old.rstrip()
        out[k] = old + note
    json.dump({'s': {}, 'l': out}, open(os.path.join(HERE, 'tr124', lang + '.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
print(len(NOTE), 'languages written;', 'untranslated before:', missing or 'none')
