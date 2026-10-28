"""Build 119's third round: Source Name's Pop In and Name (the big name as the source changes, and the name over the
games too). For all 32 languages: the option's name, and the Source Name hint with one sentence added before its
"Themes can..." sentence, built from each language's own hint (elf/lang/<Language>.yml) so its words for Pop In and the
other options stay as they are. Run from the repo root: python tools/lang119c/batch.py (writes tr119c/<Language>.json),
then python tools/lang119c/merge119c.py <Language> ... and python elf/lang/ripps2lang.py check."""
import json
import os
import re

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'tr119c')
LANG = os.path.join(HERE, '..', '..', 'elf', 'lang')

# each language: the option's name, and the sentence that goes before "Themes can make Pop In their Shown."
T = {
    'Albanian': ("Shfaqje e menjëhershme dhe emri", "Shfaqje e menjëhershme dhe emri bën të dyja."),
    'Arabic': ("ظهور مفاجئ مع الاسم", "والظهور المفاجئ مع الاسم يفعل الأمرين معاً."),
    'Bulgarian': ("Изскачане и име", "Изскачане и име прави и двете."),
    'Cebuano': ("Pop in ug ngalan", "Ang Pop in ug ngalan mobuhat sa duha."),
    'Croatian': ("Iskakanje i naziv", "Iskakanje i naziv radi oboje."),
    'Czech': ("Vyskočení a název", "Vyskočení a název dělá obojí."),
    'Danish': ("Pop ind og navn", "Pop ind og navn gør begge dele."),
    'Dutch': ("Inspringen en naam", "Inspringen en naam doet allebei."),
    'Filipino': ("Pop in at pangalan", "Ginagawa ng Pop in at pangalan ang dalawa."),
    'French': ("Apparition et nom", "Apparition et nom fait les deux."),
    'Galician': ("Emerxer e nome", "Emerxer e nome fai as dúas cousas."),
    'German': ("Einblendung und Name", "Einblendung und Name macht beides."),
    'Greek': ("Αναπήδηση και όνομα", "Η Αναπήδηση και όνομα κάνει και τα δύο."),
    'Hungarian': ("Felugrás és név", "A Felugrás és név mindkettőt teszi."),
    'Indonesian': ("Muncul dan nama", "Muncul dan nama melakukan keduanya."),
    'Italian': ("Comparsa e nome", "Comparsa e nome fa entrambe le cose."),
    'Japanese': ("ポップインと名前", "「ポップインと名前」はその両方を行います。"),
    'Korean': ("팝인과 이름", "팝인과 이름은 둘 다 합니다."),
    'Laotian': ("ປາກົດຂຶ້ນທັນທີ ແລະ ຊື່", "ປາກົດຂຶ້ນທັນທີ ແລະ ຊື່ ເຮັດທັງສອງຢ່າງ."),
    'Persian': ("ظاهر شدن ناگهانی و نام", "ظاهر شدن ناگهانی و نام هر دو کار را می‌کند."),
    'Polish': ("Wyskakiwanie i nazwa", "Wyskakiwanie i nazwa robi jedno i drugie."),
    'Portuguese': ("Aparecer e nome", "Aparecer e nome faz as duas coisas."),
    'Portuguese_BR': ("Aparecer e nome", "Aparecer e nome faz as duas coisas."),
    'Romana': ("Apariție bruscă și nume", "Apariție bruscă și nume le face pe amândouă."),
    'Russian': ("Всплытие и название", "«Всплытие и название» делает и то, и другое."),
    'SChinese': ("弹出和名称", "“弹出和名称”两者都做。"),
    'Serbian': ("Iskakanje i ime", "Iskakanje i ime radi oboje."),
    'Spanish': ("Emergente y nombre", "Emergente y nombre hace ambas cosas."),
    'Swedish': ("Poppa in och namn", "Poppa in och namn gör båda."),
    'TChinese': ("彈出和名稱", "「彈出和名稱」兩者都做。"),
    'Turkish': ("Açılır ve ad", "Açılır ve ad ikisini de yapar."),
    'Vietnamese': ("Bật ra và tên", "Bật ra và tên làm cả hai."),
}
END = re.compile(r'。|\.(?=\s|$)')


def with_sentence(hint, sentence):
    """the hint with sentence before its last two (Themes can..., Theme: ...)"""
    ends = [m.end() for m in END.finditer(hint)]
    assert len(ends) >= 3, hint
    cut = ends[-3]
    gap = '' if hint[cut - 1] == '。' else ' '
    return hint[:cut] + gap + sentence + hint[cut:]


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for lang, (name, sentence) in T.items():
        cur = yaml.safe_load(open(os.path.join(LANG, lang + '.yml'), encoding='utf-8'))
        hint = cur['labels']['HINT_RIPPS2_SOURCE_NAME']
        data = {'s': {'0': name}, 'l': {'HINT_RIPPS2_SOURCE_NAME': with_sentence(hint, sentence)}}
        json.dump(data, open(os.path.join(OUT, lang + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(len(T), 'languages')
