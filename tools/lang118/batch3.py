"""Build 118 strings (s118.json) and labels: Russian, Bulgarian, Greek, Turkish, Albanian, Indonesian, Vietnamese, Filipino.
Run from the repo root: python tools/lang118/batch3.py (writes tr118/<Language>.json)."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'tr118')

T = {}

T['Russian'] = [
    "%d изображений из %d папок ART попадут в один файл, %s. Папки ART останутся как есть: пакет является копией. Ты можешь скопировать art.tar в папку ART другого накопителя через Memory Files, но быстрее всего собрать его на том накопителе, с которого ты просматриваешь игры, поэтому самый быстрый накопитель стоит первым. Собрать сейчас?",
    "%sART/art.tar: там %d изображений, чтение %d КБ/с",
    "%sART/art.tar: там %d изображений, чтение %d КБ/с, самый быстрый",
    "Используется: %s, %d изображений, %d МБ",
    "Просмотр папок ART на запущенных накопителях",
    "Замер скорости, с которой каждый накопитель читает свои изображения: %s",
    "Нет: каждое изображение читается из своей папки ART.",
    "Упаковка изображений в %s: %d из %d изображений, %d МБ. Нажми кнопку «назад», чтобы остановить.",
    "УДАЛИТЬ пакет в %s (папки ART останутся как есть)",
    "Удалить пакет ART в %s? Папки ART останутся как есть.",
    "Остановлено. Незаконченный пакет удалён, а изображения загружаются из папок ART, как раньше.",
    "Не удалось записать пакет ART в %s (есть ли место на этом накопителе?). Больше ничего не изменилось: изображения загружаются из папок ART, как раньше.",
    "Пакет ART в %s удалён. Изображения снова загружаются из папок ART.",
    "Пакет ART собран: %d изображений, %d МБ, в %s (%d с). Теперь изображения загружаются из него, и для %d игр, для которых он собран, их папка ART больше никогда не опрашивается по одному изображению. Изображения, которые RIPPS2 загружает или снимает, появляются сразу; скопированные с ПК появятся, когда ты снова соберёшь пакет.",
    "На запущенных накопителях нет папки ART с изображениями. Запусти накопители, на которых лежат твои изображения (SELECT на их странице), и вернись.",
]
T['Russian_l'] = {
    'RIPPS2_ART_PACK': "Пакет ART",
    'RIPPS2_ART_PACK_BUILD': "Собрать или удалить",
    'HINT_RIPPS2_ART_PACK': "Упаковывает папку ART каждого запущенного накопителя в один art.tar на выбранном накопителе (самый быстрый предлагается первым). Обложки затем загружаются из одного файла с одним индексом, без поиска для каждой игры, поэтому меню и музыка идут плавно. Папки ART остаются как есть.",
}

T['Bulgarian'] = [
    "%d изображения от %d папки ART отиват в един файл, %s. Папките ART остават каквито са: пакетът е копие. Можеш да копираш art.tar в папката ART на друго устройство с Memory Files, но най-бързо е да го изградиш на устройството, от което разглеждаш, затова най-бързото устройство е първо. Да се изгради ли сега?",
    "%sART/art.tar: %d изображения там, чете %d KB/s",
    "%sART/art.tar: %d изображения там, чете %d KB/s, най-бързото",
    "В употреба: %s, %d изображения, %d MB",
    "Преглед на папките ART на стартираните устройства",
    "Измерване колко бързо всяко устройство чете изображенията си: %s",
    "Няма: всяко изображение се чете от собствената си папка ART.",
    "Пакетиране на изображенията в %s: %d от %d изображения, %d MB. Натисни бутона за назад, за да спреш.",
    "ПРЕМАХНИ пакета в %s (папките ART остават каквито са)",
    "Да се премахне ли пакетът ART в %s? Папките ART остават каквито са.",
    "Спряно. Недовършеният пакет е премахнат, а изображенията се зареждат от папките ART както преди.",
    "Пакетът ART не можа да се запише в %s (има ли място на това устройство?). Нищо друго не се промени: изображенията се зареждат от папките ART както преди.",
    "Пакетът ART в %s е премахнат. Изображенията отново се зареждат от папките ART.",
    "Пакетът ART е готов: %d изображения, %d MB, в %s (%d s). Отсега изображенията се зареждат от него, а за %d игри, за които е изграден, папката им ART никога повече не се пита изображение по изображение. Изображенията, които RIPPS2 изтегля или заснема, се показват веднага; копираните от компютър се показват, когато изградиш пакета отново.",
    "На стартираните устройства няма папка ART с изображения. Стартирай устройствата, на които са изображенията ти (SELECT на страницата им), и се върни.",
]
T['Bulgarian_l'] = {
    'RIPPS2_ART_PACK': "Пакет ART",
    'RIPPS2_ART_PACK_BUILD': "Изгради или премахни",
    'HINT_RIPPS2_ART_PACK': "Пакетира папката ART на всяко стартирано устройство в един art.tar на устройството, което избереш (най-бързото се предлага първо). Обложките се зареждат тогава от един файл с един индекс, никога с търсене за всяка игра, така че менютата и музиката остават гладки. Папките ART остават каквито са.",
}

T['Greek'] = [
    "%d εικόνες από %d φακέλους ART μπαίνουν σε ένα αρχείο, %s. Οι φάκελοι ART μένουν όπως είναι: το πακέτο είναι αντίγραφο. Μπορείς να αντιγράψεις το art.tar στον φάκελο ART άλλης μονάδας με το Memory Files, αλλά το πιο γρήγορο είναι να το φτιάξεις στη μονάδα από την οποία περιηγείσαι, γι' αυτό η πιο γρήγορη μονάδα είναι πρώτη. Να φτιαχτεί τώρα;",
    "%sART/art.tar: %d εικόνες εκεί, διαβάζει %d KB/s",
    "%sART/art.tar: %d εικόνες εκεί, διαβάζει %d KB/s, η πιο γρήγορη",
    "Σε χρήση: %s, %d εικόνες, %d MB",
    "Έλεγχος των φακέλων ART στις μονάδες που ξεκίνησαν",
    "Μέτρηση του πόσο γρήγορα διαβάζει κάθε μονάδα τις εικόνες της: %s",
    "Κανένα: κάθε εικόνα διαβάζεται από τον δικό της φάκελο ART.",
    "Πακετάρισμα των εικόνων στο %s: %d από %d εικόνες, %d MB. Πάτησε το κουμπί επιστροφής για διακοπή.",
    "ΑΦΑΙΡΕΣΗ του πακέτου στο %s (οι φάκελοι ART μένουν όπως είναι)",
    "Να αφαιρεθεί το πακέτο ART στο %s; Οι φάκελοι ART μένουν όπως είναι.",
    "Διακόπηκε. Το μισοτελειωμένο πακέτο αφαιρέθηκε και οι εικόνες φορτώνονται από τους φακέλους ART όπως πριν.",
    "Το πακέτο ART δεν μπόρεσε να γραφτεί στο %s (υπάρχει χώρος σε αυτή τη μονάδα;). Τίποτε άλλο δεν άλλαξε: οι εικόνες φορτώνονται από τους φακέλους ART όπως πριν.",
    "Το πακέτο ART στο %s αφαιρέθηκε. Οι εικόνες φορτώνονται ξανά από τους φακέλους ART.",
    "Το πακέτο ART είναι έτοιμο: %d εικόνες, %d MB, στο %s (%d s). Από τώρα οι εικόνες φορτώνονται από αυτό, και για τα %d παιχνίδια για τα οποία φτιάχτηκε ο φάκελος ART τους δεν ερωτάται ποτέ ξανά εικόνα προς εικόνα. Οι εικόνες που κατεβάζει ή τραβά το RIPPS2 εμφανίζονται αμέσως· όσες αντιγράφεις από υπολογιστή εμφανίζονται όταν ξαναφτιάξεις το πακέτο.",
    "Δεν υπάρχει φάκελος ART με εικόνες στις μονάδες που ξεκίνησαν. Ξεκίνα τις μονάδες όπου είναι οι εικόνες σου (SELECT στη σελίδα τους) και μετά γύρισε εδώ.",
]
T['Greek_l'] = {
    'RIPPS2_ART_PACK': "Πακέτο ART",
    'RIPPS2_ART_PACK_BUILD': "Δημιουργία ή αφαίρεση",
    'HINT_RIPPS2_ART_PACK': "Βάζει τον φάκελο ART κάθε μονάδας που ξεκίνησε σε ένα art.tar στη μονάδα που διαλέγεις (η πιο γρήγορη προτείνεται πρώτη). Τα εξώφυλλα φορτώνονται τότε από ένα αρχείο με ένα ευρετήριο, ποτέ με αναζήτηση ανά παιχνίδι, ώστε τα μενού και η μουσική να μένουν ομαλά. Οι φάκελοι ART μένουν όπως είναι.",
}

T['Turkish'] = [
    "%d resim, %d ART klasöründen tek bir dosyaya gidiyor: %s. ART klasörleri olduğu gibi kalır: paket bir kopyadır. art.tar dosyasını Memory Files ile başka bir sürücünün ART klasörüne kopyalayabilirsin, ama en hızlısı onu göz attığın sürücüde oluşturmaktır, bu yüzden en hızlı sürücü en üstte. Şimdi oluşturulsun mu?",
    "%sART/art.tar: orada %d resim, %d KB/s okur",
    "%sART/art.tar: orada %d resim, %d KB/s okur, en hızlısı",
    "Kullanımda: %s, %d resim, %d MB",
    "Başlatılan sürücülerdeki ART klasörlerine bakılıyor",
    "Her sürücünün resimlerini ne kadar hızlı okuduğu ölçülüyor: %s",
    "Yok: her resim kendi ART klasöründen okunur.",
    "Resimler %s içine paketleniyor: %d / %d resim, %d MB. Durdurmak için geri düğmesine bas.",
    "%s içindeki paketi KALDIR (ART klasörleri olduğu gibi kalır)",
    "%s içindeki ART paketi kaldırılsın mı? ART klasörleri olduğu gibi kalır.",
    "Durduruldu. Bitmemiş paket kaldırıldı ve resimler önceki gibi ART klasörlerinden yükleniyor.",
    "ART paketi %s konumuna yazılamadı (o sürücüde yer var mı?). Başka hiçbir şey değişmedi: resimler önceki gibi ART klasörlerinden yükleniyor.",
    "%s içindeki ART paketi kaldırıldı. Resimler yeniden ART klasörlerinden yükleniyor.",
    "ART paketi hazır: %d resim, %d MB, %s içinde (%d sn). Resimler artık ondan yükleniyor ve oluşturulduğu %d oyunun ART klasörüne bir daha asla resim resim sorulmuyor. RIPPS2'nin indirdiği ya da çektiği resimler hemen görünür; PC'den kopyaladıkların paketi yeniden oluşturduğunda görünür.",
    "Başlatılan sürücülerde resim içeren bir ART klasörü yok. Resimlerinin bulunduğu sürücüleri başlat (sayfalarında SELECT), sonra geri gel.",
]
T['Turkish_l'] = {
    'RIPPS2_ART_PACK': "ART Paketi",
    'RIPPS2_ART_PACK_BUILD': "Oluştur veya kaldır",
    'HINT_RIPPS2_ART_PACK': "Başlatılan her sürücünün ART klasörünü seçtiğin sürücüde tek bir art.tar dosyasına paketler (en hızlısı ilk sunulur). Kapaklar böylece tek dosyadan tek bir dizinle yüklenir, asla oyun başına bir aramayla değil; menüler ve müzik akıcı kalır. ART klasörleri olduğu gibi kalır.",
}

T['Albanian'] = [
    "%d figura nga %d dosje ART shkojnë në një skedar të vetëm, %s. Dosjet ART mbeten siç janë: paketa është një kopje. Mund ta kopjosh art.tar në dosjen ART të një disku tjetër me Memory Files, por më e shpejta është ta ndërtosh në diskun nga i cili shfleton, prandaj disku më i shpejtë del i pari. Ta ndërtoj tani?",
    "%sART/art.tar: %d figura atje, lexon %d KB/s",
    "%sART/art.tar: %d figura atje, lexon %d KB/s, më i shpejti",
    "Në përdorim: %s, %d figura, %d MB",
    "Po shikohen dosjet ART në disqet e nisura",
    "Po matet sa shpejt lexon çdo disk figurat e veta: %s",
    "Asnjë: çdo figurë lexohet nga dosja e vet ART.",
    "Po paketohen figurat në %s: %d nga %d figura, %d MB. Shtyp butonin e kthimit për ta ndalur.",
    "HIQ paketën në %s (dosjet ART mbeten siç janë)",
    "Të hiqet paketa ART në %s? Dosjet ART mbeten siç janë.",
    "U ndal. Paketa e papërfunduar u hoq dhe figurat ngarkohen nga dosjet ART si më parë.",
    "Paketa ART nuk mund të shkruhej në %s (a ka vend në atë disk?). Asgjë tjetër nuk ndryshoi: figurat ngarkohen nga dosjet ART si më parë.",
    "Paketa ART në %s u hoq. Figurat ngarkohen sërish nga dosjet ART.",
    "Paketa ART është gati: %d figura, %d MB, në %s (%d s). Tani e tutje figurat ngarkohen prej saj, dhe për %d lojërat për të cilat u ndërtua, dosja e tyre ART nuk pyetet më kurrë figurë pas figure. Figurat që RIPPS2 shkarkon ose kap shfaqen menjëherë; ato që kopjon nga një PC shfaqen kur e ndërton paketën sërish.",
    "Nuk ka asnjë dosje ART me figura në disqet e nisura. Nis disqet ku janë figurat e tua (SELECT në faqen e tyre), pastaj kthehu.",
]
T['Albanian_l'] = {
    'RIPPS2_ART_PACK': "Paketa ART",
    'RIPPS2_ART_PACK_BUILD': "Ndërto ose hiq",
    'HINT_RIPPS2_ART_PACK': "Paketon dosjen ART të çdo disku të nisur në një art.tar të vetëm në diskun që zgjedh (më i shpejti ofrohet i pari). Kopertinat ngarkohen pastaj nga një skedar me një indeks, kurrë me një kërkim për çdo lojë, kështu që menytë dhe muzika mbeten të rrjedhshme. Dosjet ART mbeten siç janë.",
}

T['Indonesian'] = [
    "%d gambar dari %d folder ART masuk ke satu berkas, %s. Folder ART tetap seperti adanya: paket ini salinan. Kamu bisa menyalin art.tar ke folder ART drive lain dengan Memory Files, tetapi membuatnya di drive tempat kamu menjelajah adalah yang tercepat, karena itu drive tercepat ada di atas. Buat sekarang?",
    "%sART/art.tar: %d gambar di sana, membaca %d KB/s",
    "%sART/art.tar: %d gambar di sana, membaca %d KB/s, yang tercepat",
    "Dipakai: %s, %d gambar, %d MB",
    "Melihat folder ART di drive yang sudah dimulai",
    "Mengukur seberapa cepat tiap drive membaca gambarnya: %s",
    "Tidak ada: tiap gambar dibaca dari folder ART-nya sendiri.",
    "Mengemas gambar ke %s: %d dari %d gambar, %d MB. Tekan tombol kembali untuk berhenti.",
    "HAPUS paket di %s (folder ART tetap seperti adanya)",
    "Hapus paket ART di %s? Folder ART tetap seperti adanya.",
    "Dihentikan. Paket yang belum selesai sudah dihapus, dan gambar dimuat dari folder ART seperti sebelumnya.",
    "Paket ART tidak bisa ditulis ke %s (apakah ada ruang di drive itu?). Tidak ada yang lain berubah: gambar dimuat dari folder ART seperti sebelumnya.",
    "Paket ART di %s sudah dihapus. Gambar dimuat lagi dari folder ART.",
    "Paket ART sudah jadi: %d gambar, %d MB, di %s (%d dtk). Mulai sekarang gambar dimuat darinya, dan %d game yang menjadi sasarannya tidak pernah lagi ditanyakan ke folder ART-nya gambar demi gambar. Gambar yang diunduh atau diambil RIPPS2 langsung tampil; gambar yang kamu salin dari PC tampil setelah kamu membuat paket lagi.",
    "Tidak ada folder ART berisi gambar di drive yang sudah dimulai. Mulai drive tempat gambarmu berada (SELECT di halamannya), lalu kembali.",
]
T['Indonesian_l'] = {
    'RIPPS2_ART_PACK': "Paket ART",
    'RIPPS2_ART_PACK_BUILD': "Buat atau hapus",
    'HINT_RIPPS2_ART_PACK': "Mengemas folder ART setiap drive yang dimulai ke satu art.tar di drive yang kamu pilih (yang tercepat ditawarkan lebih dulu). Sampul lalu dimuat dari satu berkas dengan satu indeks, tidak pernah dengan pencarian per game, sehingga menu dan musik tetap lancar. Folder ART tetap seperti adanya.",
}

T['Vietnamese'] = [
    "%d hình từ %d thư mục ART sẽ vào một tệp duy nhất, %s. Các thư mục ART giữ nguyên: gói chỉ là bản sao. Bạn có thể chép art.tar sang thư mục ART của ổ khác bằng Memory Files, nhưng tạo gói ngay trên ổ bạn duyệt là nhanh nhất, vì vậy ổ nhanh nhất đứng đầu. Tạo ngay?",
    "%sART/art.tar: có %d hình, đọc %d KB/s",
    "%sART/art.tar: có %d hình, đọc %d KB/s, nhanh nhất",
    "Đang dùng: %s, %d hình, %d MB",
    "Đang xem các thư mục ART trên các ổ đã khởi động",
    "Đang đo tốc độ mỗi ổ đọc hình của nó: %s",
    "Không có: mỗi hình được đọc từ thư mục ART riêng của nó.",
    "Đang gói hình vào %s: %d trên %d hình, %d MB. Nhấn nút quay lại để dừng.",
    "XÓA gói trong %s (các thư mục ART giữ nguyên)",
    "Xóa gói ART trong %s? Các thư mục ART giữ nguyên.",
    "Đã dừng. Gói dở dang đã bị xóa, và hình được tải từ các thư mục ART như trước.",
    "Không ghi được gói ART vào %s (ổ đó còn chỗ không?). Không có gì khác thay đổi: hình được tải từ các thư mục ART như trước.",
    "Gói ART trong %s đã bị xóa. Hình lại được tải từ các thư mục ART.",
    "Gói ART đã xong: %d hình, %d MB, trong %s (%d giây). Từ giờ hình được tải từ gói, và với %d trò chơi mà gói được tạo cho, thư mục ART của chúng không bao giờ bị hỏi từng hình nữa. Hình RIPPS2 tải về hoặc chụp hiện ngay; hình bạn chép vào từ PC sẽ hiện khi bạn tạo lại gói.",
    "Không có thư mục ART nào chứa hình trên các ổ đã khởi động. Hãy khởi động các ổ chứa hình của bạn (SELECT trên trang của chúng), rồi quay lại.",
]
T['Vietnamese_l'] = {
    'RIPPS2_ART_PACK': "Gói ART",
    'RIPPS2_ART_PACK_BUILD': "Tạo hoặc xóa",
    'HINT_RIPPS2_ART_PACK': "Gói thư mục ART của mọi ổ đã khởi động vào một art.tar trên ổ bạn chọn (ổ nhanh nhất được đề xuất trước). Bìa khi đó được tải từ một tệp với một chỉ mục, không bao giờ tìm từng trò chơi, nên menu và nhạc luôn mượt. Các thư mục ART giữ nguyên.",
}

T['Filipino'] = [
    "%d larawan mula sa %d ART folder ang mapupunta sa iisang file, %s. Mananatili ang mga ART folder: kopya lang ang pack. Puwede mong kopyahin ang art.tar sa ART folder ng ibang drive gamit ang Memory Files, pero pinakamabilis kung bubuuin ito sa drive na binabrowse mo, kaya nauuna ang pinakamabilis na drive. Buuin na ngayon?",
    "%sART/art.tar: %d larawan doon, bumabasa ng %d KB/s",
    "%sART/art.tar: %d larawan doon, bumabasa ng %d KB/s, ang pinakamabilis",
    "Ginagamit: %s, %d larawan, %d MB",
    "Tinitingnan ang mga ART folder sa mga sinimulang drive",
    "Sinusukat kung gaano kabilis binabasa ng bawat drive ang mga larawan nito: %s",
    "Wala: binabasa ang bawat larawan mula sa sarili nitong ART folder.",
    "Pinapack ang mga larawan sa %s: %d sa %d larawan, %d MB. Pindutin ang back button para huminto.",
    "TANGGALIN ang pack sa %s (mananatili ang mga ART folder)",
    "Tanggalin ang ART Pack sa %s? Mananatili ang mga ART folder.",
    "Itinigil. Tinanggal ang hindi tapos na pack, at nilo-load ang mga larawan mula sa mga ART folder gaya ng dati.",
    "Hindi maisulat ang ART Pack sa %s (may puwang ba sa drive na iyon?). Wala nang ibang nagbago: nilo-load ang mga larawan mula sa mga ART folder gaya ng dati.",
    "Natanggal na ang ART Pack sa %s. Nilo-load ulit ang mga larawan mula sa mga ART folder.",
    "Buo na ang ART Pack: %d larawan, %d MB, sa %s (%d s). Mula ngayon dito na nilo-load ang mga larawan, at ang %d laro na pinagbuuan nito ay hindi na tatanungin sa kanilang ART folder nang isa-isang larawan. Lumalabas agad ang mga larawang kinukuha o kinukunan ng RIPPS2; ang kinokopya mo mula sa PC ay lalabas kapag binuo mo ulit ang pack.",
    "Walang ART folder na may mga larawan sa mga sinimulang drive. Simulan ang mga drive kung nasaan ang mga larawan mo (SELECT sa kanilang page), saka bumalik.",
]
T['Filipino_l'] = {
    'RIPPS2_ART_PACK': "ART Pack",
    'RIPPS2_ART_PACK_BUILD': "Buuin o tanggalin",
    'HINT_RIPPS2_ART_PACK': "Pinagsasama ang ART folder ng bawat sinimulang drive sa iisang art.tar sa drive na pipiliin mo (unang inaalok ang pinakamabilis). Nilo-load na ang mga cover mula sa iisang file na may iisang index, hindi kailanman sa paghahanap sa bawat laro, kaya maayos ang takbo ng mga menu at musika. Mananatili ang mga ART folder.",
}

os.makedirs(OUT, exist_ok=True)
for lang in [k for k in T if not k.endswith('_l')]:
    s = {str(i): v for i, v in enumerate(T[lang])}
    json.dump({'s': s, 'l': T[lang + '_l']}, open(os.path.join(OUT, lang + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('wrote', lang)
