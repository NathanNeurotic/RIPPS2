"""Build 122's languages: the Launch Disc choice Zoom, and its clause added to each language's own Launch Disc hint
(its words for Pop In and Spin kept as they are). Writes s122.json, labels122.json and tr122/<Language>.json for
merge122.py.    python batch122.py"""
import json
import os

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
LANG = os.path.join(HERE, '..', '..', 'elf', 'lang')
HINT = "A game's disc comes in as it launches. Pop In settles and fades; Spin turns faster and faster until the game starts; Zoom settles, then grows to read clearly and stays."

# language: (Zoom, the clause that follows the hint, 'end' = the hint's last character is dropped first)
ZOOM = {
    'Albanian': ('Zmadhim', '; Zmadhimi qetësohet, pastaj rritet që të lexohet qartë dhe mbetet.', True),
    'Arabic': ('تكبير', '؛ والتكبير يستقر ثم يكبر ليُقرأ بوضوح ويبقى.', True),
    'Bulgarian': ('Увеличение', '; Увеличение каца, после нараства, за да се чете ясно, и остава.', True),
    'Cebuano': ('Zoom', '; mohunong ang Zoom, unya modako aron klaro nga mabasa ug magpabilin.', True),
    'Croatian': ('Zumiranje', '; Zumiranje se smiri, zatim naraste da se jasno čita i ostane.', True),
    'Czech': ('Přiblížení', '; Přiblížení dosedne, pak se zvětší, aby se dobře četlo, a zůstane.', True),
    'Danish': ('Zoom', '; Zoom lander og vokser derefter, så det kan læses tydeligt, og bliver.', True),
    'Dutch': ('Inzoomen', '; Inzoomen landt, groeit dan zodat het goed leesbaar is en blijft staan.', True),
    'Filipino': ('Zoom', '; tumitigil ang Zoom, saka lumalaki para malinaw na mabasa at nananatili.', True),
    'French': ('Zoom', ' ; Zoom se pose puis grandit pour être bien lisible et reste affiché.', True),
    'Galician': ('Zoom', '; Zoom asenta e logo medra para lerse ben e queda.', True),
    'German': ('Zoomen', '; Zoomen setzt sich, wird dann groß genug zum Lesen und bleibt stehen.', True),
    'Greek': ('Μεγέθυνση', '· η Μεγέθυνση κάθεται, μετά μεγαλώνει για να διαβάζεται καθαρά και μένει.', True),
    'Hungarian': ('Nagyítás', '; a Nagyítás leül, majd jól olvashatóra nő, és ott marad.', True),
    'Indonesian': ('Zoom', '; Zoom mendarat, lalu membesar agar jelas terbaca dan tetap tampil.', True),
    'Italian': ('Zoom', '; Zoom si posa, poi si ingrandisce per leggersi bene e resta.', True),
    'Japanese': ('ズーム', '「ズーム」は落ち着いてから読みやすい大きさまで拡大し、そのまま表示されます。', False),
    'Korean': ('줌', ' 줌은 자리 잡은 뒤 또렷이 읽히도록 커지고 그대로 남습니다.', False),
    'Laotian': ('ຂະຫຍາຍ', ' ຂະຫຍາຍ ຢຸດ ແລ້ວ ໃຫຍ່ຂຶ້ນ ໃຫ້ອ່ານໄດ້ຊັດ ແລະ ຢູ່ຕໍ່.', False),
    'Persian': ('بزرگ‌نمایی', '؛ بزرگ‌نمایی آرام می‌گیرد، سپس بزرگ می‌شود تا واضح خوانده شود و می‌ماند.', True),
    'Polish': ('Przybliżenie', '; Przybliżenie osiada, potem rośnie, by dało się je wyraźnie odczytać, i zostaje.', True),
    'Portuguese': ('Ampliar', '; Ampliar pousa e depois cresce para se ler bem e fica.', True),
    'Portuguese_BR': ('Ampliar', '; Ampliar pousa e depois cresce para ficar legível e permanece.', True),
    'Romana': ('Mărire', '; Mărire se așază, apoi crește ca să se citească clar și rămâne.', True),
    'Russian': ('Приближение', '; «Приближение» опускается, затем увеличивается, чтобы его было хорошо видно, и остаётся.', True),
    'SChinese': ('放大', '；“放大”落定后变大到清晰可读，并一直显示。', True),
    'Serbian': ('Zumiranje', '; Zumiranje se smiri, zatim naraste da se jasno čita i ostane.', True),
    'Spanish': ('Zoom', '; Zoom se posa y luego crece para leerse bien y se queda.', True),
    'Swedish': ('Zooma', '; Zooma landar och växer sedan så att den syns tydligt och står kvar.', True),
    'TChinese': ('放大', '；「放大」落定後變大到清晰可讀，並一直顯示。', True),
    'Turkish': ('Yakınlaştır', '; Yakınlaştır yerine oturur, sonra rahat okunacak kadar büyür ve kalır.', True),
    'Vietnamese': ('Phóng to', '; Phóng to hạ xuống rồi lớn dần cho dễ đọc và giữ nguyên.', True),
}

json.dump(['Zoom'], open(os.path.join(HERE, 's122.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump({'HINT_RIPPS2_LAUNCH_DISC': HINT}, open(os.path.join(HERE, 'labels122.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
os.makedirs(os.path.join(HERE, 'tr122'), exist_ok=True)
for lang, (word, clause, drop) in ZOOM.items():
    old = yaml.safe_load(open(os.path.join(LANG, lang + '.yml'), encoding='utf-8'))['labels']['HINT_RIPPS2_LAUNCH_DISC']
    hint = (old[:-1] if drop else old) + clause
    json.dump({'s': {'0': word}, 'l': {'HINT_RIPPS2_LAUNCH_DISC': hint}},
              open(os.path.join(HERE, 'tr122', lang + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(ZOOM), 'languages written')
