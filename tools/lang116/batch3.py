"""Build 116 strings (s116.json) and labels: Russian, Bulgarian, Greek, Turkish, Albanian, Indonesian, Vietnamese, Filipino.
Run from the repo root: python tools/lang116/batch3.py (writes tr116/<Language>.json)."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'tr116')

T = {}

T['Russian'] = [
    " (Найденные конфигурации настроены: %s.)",
    " Один раз сохраните его настройки в его собственном конфигураторе, затем снова включите BOOT LOCK.",
    "%s не может запустить RIPPS2 оттуда, где он сейчас (%s), а RIPPS2 не копирует себя. Положите RIPPS2.ELF на карту памяти или USB-накопитель и запустите его оттуда.",
    "BOOT LOCK не смог записать конфигурацию загрузчика. Проверьте, что карта памяти или накопитель не защищены от записи, и попробуйте снова.",
    "BOOT LOCK не нашёл конфигурации загрузчика для изменения.",
    "BOOT LOCK выключен. Ваш загрузчик запускает то, что запускал раньше (%s).",
    "BOOT LOCK включён. Теперь %s запускает RIPPS2 при включении (%s), а при пустом поле «ELF при вызове IGR» EXIT из игры возвращается тем же путём. Удерживайте одну из его кнопок при запуске консоли, чтобы попасть в другое место.%s",
    "BOOT LOCK поставил RIPPS2 первым в меню OSDMenu (%s). OSDMenu сам ничего не запускает: выберите там RIPPS2, и EXIT из игры вернётся в это меню. Чтобы консоль сразу запускала RIPPS2, BIBLE устанавливает PS2BBL 1.2.0 на карту памяти («Загрузчик»).",
    "BOOT LOCK работает через загрузчик на карте памяти (PS2BBL, FMCB или OSDMenu), а здесь его нет.",
    "Карта памяти в слоте %d при включении запускает %s, а BOOT LOCK не нашёл его конфигурации для изменения (ищет %s).",
    "Карта памяти в слоте %d при включении запускает %s, который BOOT LOCK настроить не может: он работает через PS2BBL, FMCB и OSDMenu.",
    "На этой консоли есть загрузчик с блокировкой RIPPS2.",
    "EXIT из игры: браузер, затем ваш загрузчик (BOOT LOCK)",
]
T['Russian_l'] = {
    'HINT_EXITPATH': "Куда ведёт EXIT в Игровом меню. Лучше оставить пустым при включённом BOOT LOCK (PS2BBL, FMCB или OSDMenu, или настроенном BIBLE): тогда EXIT идёт через браузер, который запускает ваш загрузчик и RIPPS2, как при включении, это самый надёжный путь назад. Пусто без блокировки: собственный ELF RIPPS2 на карте памяти или USB-накопителе FAT32, загружаемый сразу после перезагрузки, к которой не каждая игра оставляет консоль готовой. Browser: браузер PS2. ELF на MMCE тогда вообще недоступен.",
    'HINT_RIPPS2_BOOT_LOCK': "Запускает RIPPS2 при включении через ваш загрузчик: PS2BBL и FMCB запускают его сразу, OSDMenu ставит его первым в своём меню, а EXIT из игры возвращается тем же путём. Выкл. возвращает то, что было раньше. Ещё нет ни одного? «Загрузчик» устанавливает BIBLE.",
}

T['Bulgarian'] = [
    " (Намерените конфигурации бяха настроени: %s.)",
    " Запазете веднъж настройките му с неговия собствен конфигуратор, след което включете BOOT LOCK отново.",
    "%s не може да стартира RIPPS2 от мястото, където е сега (%s), а RIPPS2 не се копира сам. Сложете RIPPS2.ELF на карта с памет или USB устройство и го стартирайте оттам.",
    "BOOT LOCK не успя да запише конфигурацията на зареждащия модул. Проверете дали картата с памет или устройството не е защитено от запис и опитайте отново.",
    "BOOT LOCK не намери конфигурация на зареждащ модул за промяна.",
    "BOOT LOCK е изключен. Вашият зареждащ модул стартира това, което стартираше преди (%s).",
    "BOOT LOCK е включен. Сега %s стартира RIPPS2 при включване (%s), а празен път за IGR връща EXIT от игра по същия път. Задръжте един от бутоните му, докато конзолата стартира, за да стигнете до нещо друго.%s",
    "BOOT LOCK постави RIPPS2 първи в менюто на OSDMenu (%s). OSDMenu не стартира нищо само: изберете RIPPS2 там и EXIT от игра се връща в това меню. За конзола, която стартира RIPPS2 веднага, BIBLE слага PS2BBL 1.2.0 на карта с памет (Зареждащ модул).",
    "BOOT LOCK работи чрез зареждащ модул на карта с памет (PS2BBL, FMCB или OSDMenu), а тук няма такъв.",
    "Картата памет в слот %d стартира %s при включване, а BOOT LOCK не намери негова конфигурация за промяна (търси %s).",
    "Картата памет в слот %d стартира %s при включване, който BOOT LOCK не може да настрои: работи чрез PS2BBL, FMCB и OSDMenu.",
    "На тази конзола има зареждащ модул с ключалката на RIPPS2.",
    "EXIT от игра: браузърът, после вашият зареждащ модул (BOOT LOCK)",
]
T['Bulgarian_l'] = {
    'HINT_EXITPATH': "Накъде води EXIT в Менюто в играта. Най-добре оставете празно с включен BOOT LOCK (PS2BBL, FMCB или OSDMenu, или настроен BIBLE): тогава EXIT минава през браузъра, който стартира вашия зареждащ модул и RIPPS2 като при включване, най-сигурният път обратно. Празно без ключалката: собственият ELF на RIPPS2 на карта с памет или FAT32 USB устройство, зареден веднага след рестарта, за който не всяка игра оставя конзолата готова. Browser: браузърът на PS2. ELF на MMCE тогава изобщо не е достъпен.",
    'HINT_RIPPS2_BOOT_LOCK': "Стартира RIPPS2 при включване чрез вашия зареждащ модул: PS2BBL и FMCB го стартират веднага, OSDMenu го слага първи в менюто си, а EXIT от игра се връща по същия път. Изкл. връща това, което беше преди. Още нямате? Зареждащ модул инсталира BIBLE.",
}

T['Greek'] = [
    " (Οι ρυθμίσεις που βρέθηκαν ορίστηκαν: %s.)",
    " Αποθηκεύστε μία φορά τις ρυθμίσεις του με τον δικό του διαμορφωτή και ενεργοποιήστε ξανά το BOOT LOCK.",
    "Το %s δεν μπορεί να ξεκινήσει το RIPPS2 από εκεί που βρίσκεται τώρα (%s), και το RIPPS2 δεν αντιγράφει τον εαυτό του. Βάλτε το RIPPS2.ELF σε κάρτα μνήμης ή σε δίσκο USB και ξεκινήστε το από εκεί.",
    "Το BOOT LOCK δεν μπόρεσε να γράψει τις ρυθμίσεις του φορτωτή εκκίνησης. Ελέγξτε ότι η κάρτα μνήμης ή ο δίσκος δεν έχει προστασία εγγραφής και δοκιμάστε ξανά.",
    "Το BOOT LOCK δεν βρήκε ρυθμίσεις φορτωτή εκκίνησης για αλλαγή.",
    "Το BOOT LOCK είναι ανενεργό. Ο φορτωτής εκκίνησής σας ξεκινά ό,τι ξεκινούσε πριν (%s).",
    "Το BOOT LOCK είναι ενεργό. Το %s ξεκινά τώρα το RIPPS2 στο άναμμα (%s), και με κενό «Προορισμός Μετά Από IGR» το EXIT ενός παιχνιδιού επιστρέφει από τον ίδιο δρόμο. Κρατήστε ένα από τα κουμπιά του όσο ξεκινά η κονσόλα για να φτάσετε κάπου αλλού.%s",
    "Το BOOT LOCK έβαλε το RIPPS2 πρώτο στο μενού του OSDMenu (%s). Το OSDMenu δεν ξεκινά τίποτα μόνο του: επιλέξτε εκεί το RIPPS2, και το EXIT ενός παιχνιδιού επιστρέφει σε εκείνο το μενού. Για κονσόλα που ξεκινά αμέσως το RIPPS2, το BIBLE βάζει το PS2BBL 1.2.0 σε κάρτα μνήμης (Φορτωτής εκκίνησης).",
    "Το BOOT LOCK λειτουργεί μέσω ενός φορτωτή εκκίνησης σε κάρτα μνήμης (PS2BBL, FMCB ή OSDMenu), και εδώ δεν υπάρχει κανένας.",
    "Η κάρτα μνήμης στην υποδοχή %d ξεκινά στο άναμμα το %s, και το BOOT LOCK δεν βρήκε ρυθμίσεις του για αλλαγή (ψάχνει το %s).",
    "Η κάρτα μνήμης στην υποδοχή %d ξεκινά στο άναμμα το %s, που το BOOT LOCK δεν μπορεί να ρυθμίσει: λειτουργεί μέσω PS2BBL, FMCB και OSDMenu.",
    "Σε αυτή την κονσόλα υπάρχει φορτωτής εκκίνησης με το κλείδωμα του RIPPS2.",
    "EXIT παιχνιδιού: ο περιηγητής, μετά ο φορτωτής εκκίνησής σας (BOOT LOCK)",
]
T['Greek_l'] = {
    'HINT_EXITPATH': "Πού πηγαίνει το EXIT στο Μενού μέσα στο παιχνίδι. Καλύτερα κενό με ενεργό το BOOT LOCK (PS2BBL, FMCB ή OSDMenu, ή ρυθμισμένο το BIBLE): τότε το EXIT περνά από τον περιηγητή, που ξεκινά τον φορτωτή εκκίνησής σας και το RIPPS2 όπως στο άναμμα, ο πιο ασφαλής δρόμος πίσω. Κενό χωρίς το κλείδωμα: το δικό ELF του RIPPS2 σε κάρτα μνήμης ή σε δίσκο USB FAT32, φορτωμένο αμέσως μετά την επαναφορά, για την οποία δεν αφήνει κάθε παιχνίδι την κονσόλα έτοιμη. Browser: ο περιηγητής του PS2. Ένα ELF στο MMCE τότε δεν είναι καθόλου προσβάσιμο.",
    'HINT_RIPPS2_BOOT_LOCK': "Ξεκινά το RIPPS2 στο άναμμα μέσω του φορτωτή εκκίνησής σας: το PS2BBL και το FMCB το ξεκινούν αμέσως, το OSDMenu το βάζει πρώτο στο μενού του, και το EXIT ενός παιχνιδιού επιστρέφει από τον ίδιο δρόμο. Το Ανενεργό επαναφέρει ό,τι υπήρχε πριν. Κανένας ακόμα; Ο Φορτωτής εκκίνησης εγκαθιστά το BIBLE.",
}

T['Turkish'] = [
    " (Bulunan yapılandırmalar ayarlandı: %s.)",
    " Ayarlarını bir kez kendi yapılandırıcısıyla kaydedin, ardından BOOT LOCK'u yeniden açın.",
    "%s, RIPPS2'yi şu anki yerinden (%s) başlatamıyor ve RIPPS2 kendini kopyalamaz. RIPPS2.ELF'i bir hafıza kartına ya da USB sürücüye koyun ve oradan başlatın.",
    "BOOT LOCK önyükleyicinin yapılandırmasını yazamadı. Hafıza kartının ya da sürücünün yazmaya karşı korumalı olmadığını kontrol edip yeniden deneyin.",
    "BOOT LOCK değiştirilecek bir önyükleyici yapılandırması bulamadı.",
    "BOOT LOCK kapalı. Önyükleyiciniz önceden başlattığını başlatıyor (%s).",
    "BOOT LOCK açık. %s artık açılışta RIPPS2'yi başlatır (%s) ve boş bir IGR Yolu, bir oyunun EXIT'ini aynı yoldan geri gönderir. Başka bir şeye ulaşmak için konsol başlarken düğmelerinden birine basılı tutun.%s",
    "BOOT LOCK, RIPPS2'yi OSDMenu'nün menüsünde en başa koydu (%s). OSDMenu kendi kendine hiçbir şey başlatmaz: orada RIPPS2'yi seçin, bir oyunun EXIT'i de o menüye döner. RIPPS2'yi hemen başlatan bir konsol için BIBLE, PS2BBL 1.2.0'ı bir hafıza kartına kurar (Önyükleyici).",
    "BOOT LOCK bir hafıza kartındaki önyükleyici üzerinden çalışır (PS2BBL, FMCB ya da OSDMenu) ve burada hiç yok.",
    "%d. yuvadaki hafıza kartı açılışta şunu başlatıyor: %s; BOOT LOCK onun değiştirilecek bir yapılandırmasını bulamadı (%s dosyasını arar).",
    "%d. yuvadaki hafıza kartı açılışta şunu başlatıyor: %s; BOOT LOCK bunu ayarlayamaz: PS2BBL, FMCB ve OSDMenu üzerinden çalışır.",
    "Bu konsolda RIPPS2'nin kilidini taşıyan bir önyükleyici var.",
    "Bir oyunun EXIT'i: tarayıcı, sonra önyükleyiciniz (BOOT LOCK)",
]
T['Turkish_l'] = {
    'HINT_EXITPATH': "Oyun İçi Menü'deki EXIT'in nereye gittiği. En iyisi BOOT LOCK açıkken boş bırakmak (PS2BBL, FMCB ya da OSDMenu veya BIBLE kurulu): EXIT o zaman önyükleyicinizi ve RIPPS2'yi açılıştaki gibi başlatan tarayıcıdan geçer; en güvenli dönüş yolu budur. Kilit olmadan boş: RIPPS2'nin kendi ELF'i, bir hafıza kartında ya da FAT32 USB sürücüde, sıfırlamanın hemen ardından yüklenir ve her oyun konsolu buna hazır bırakmaz. Browser: PS2 tarayıcısı. MMCE'deki bir ELF'e o zaman hiç ulaşılamaz.",
    'HINT_RIPPS2_BOOT_LOCK': "Açılışta RIPPS2'yi önyükleyiciniz üzerinden başlatır: PS2BBL ve FMCB onu hemen başlatır, OSDMenu menüsünde en başa koyar, bir oyunun EXIT'i de aynı yoldan döner. Kapalı, önceden olanı geri koyar. Henüz yok mu? Önyükleyici BIBLE'ı kurar.",
}

T['Albanian'] = [
    " (Konfigurimet e gjetura u vendosën: %s.)",
    " Ruaji cilësimet e tij një herë me konfiguruesin e vet, pastaj ndize sërish BOOT LOCK.",
    "%s nuk mund ta nisë RIPPS2 nga vendi ku është tani (%s), dhe RIPPS2 nuk e kopjon veten. Vendose RIPPS2.ELF në një kartë memorieje ose në një njësi USB dhe nise prej andej.",
    "BOOT LOCK nuk mundi ta shkruajë konfigurimin e ngarkuesit të nisjes. Kontrollo që karta e memories ose njësia të mos jetë e mbrojtur nga shkrimi, pastaj provo sërish.",
    "BOOT LOCK nuk gjeti asnjë konfigurim ngarkuesi nisjeje për të ndryshuar.",
    "BOOT LOCK është fikur. Ngarkuesi yt i nisjes nis atë që niste më parë (%s).",
    "BOOT LOCK është ndezur. %s tani nis RIPPS2 në ndezje (%s), dhe një Shteg IGR bosh e kthen EXIT-in e një loje nga e njëjta rrugë. Mbaj një nga butonat e tij ndërsa konsola niset për të arritur diçka tjetër.%s",
    "BOOT LOCK e vuri RIPPS2 të parin në menynë e OSDMenu (%s). OSDMenu nuk nis asgjë vetë: zgjidh atje RIPPS2, dhe EXIT-i i një loje kthehet te ajo meny. Për një konsolë që nis RIPPS2 menjëherë, BIBLE vendos PS2BBL 1.2.0 në një kartë memorieje (Ngarkuesi i nisjes).",
    "BOOT LOCK punon përmes një ngarkuesi nisjeje në një kartë memorieje (PS2BBL, FMCB ose OSDMenu), dhe këtu nuk ka asnjë.",
    "Karta e memories në folenë %d nis %s në ndezje, dhe BOOT LOCK nuk gjeti asnjë konfigurim të tij për të ndryshuar (kërkon %s).",
    "Karta e memories në folenë %d nis %s në ndezje, të cilin BOOT LOCK nuk mund ta vendosë: punon përmes PS2BBL, FMCB dhe OSDMenu.",
    "Në këtë konsolë ka një ngarkues nisjeje me kyçin e RIPPS2.",
    "EXIT-i i një loje: shfletuesi, pastaj ngarkuesi yt i nisjes (BOOT LOCK)",
]
T['Albanian_l'] = {
    'HINT_EXITPATH': "Ku shkon EXIT në Menynë në lojë. Më mirë bosh me BOOT LOCK të ndezur (PS2BBL, FMCB ose OSDMenu, ose BIBLE të përgatitur): EXIT atëherë kalon përmes shfletuesit, që nis ngarkuesin tënd të nisjes dhe RIPPS2 si në ndezje, rruga më e sigurt mbrapsht. Bosh pa kyçin: ELF-i i vetë RIPPS2 në kartë memorieje ose në njësi USB FAT32, i ngarkuar menjëherë pas rivendosjes, për të cilën jo çdo lojë e lë konsolën gati. Browser: shfletuesi i PS2. Një ELF në MMCE atëherë nuk arrihet fare.",
    'HINT_RIPPS2_BOOT_LOCK': "Nis RIPPS2 në ndezje përmes ngarkuesit tënd të nisjes: PS2BBL dhe FMCB e nisin menjëherë, OSDMenu e vë të parin në menynë e vet, dhe EXIT-i i një loje kthehet nga e njëjta rrugë. Fikur kthen atë që ishte më parë. Ende asnjë? Ngarkuesi i nisjes instalon BIBLE.",
}

T['Indonesian'] = [
    " (Konfigurasi yang ditemukan sudah diatur: %s.)",
    " Simpan pengaturannya sekali dengan konfiguratornya sendiri, lalu nyalakan BOOT LOCK lagi.",
    "%s tidak bisa menjalankan RIPPS2 dari tempatnya sekarang (%s), dan RIPPS2 tidak menyalin dirinya. Taruh RIPPS2.ELF di kartu memori atau drive USB lalu jalankan dari sana.",
    "BOOT LOCK tidak bisa menulis konfigurasi boot loader. Pastikan kartu memori atau drive tidak dilindungi dari penulisan, lalu coba lagi.",
    "BOOT LOCK tidak menemukan konfigurasi boot loader untuk diubah.",
    "BOOT LOCK mati. Boot loader-mu menjalankan apa yang dijalankannya sebelumnya (%s).",
    "BOOT LOCK menyala. %s sekarang menjalankan RIPPS2 saat menyala (%s), dan Pintasan IGR yang kosong mengirim EXIT dari game kembali lewat jalan yang sama. Tahan salah satu tombolnya saat konsol mulai untuk menuju hal lain.%s",
    "BOOT LOCK menaruh RIPPS2 di urutan pertama menu OSDMenu (%s). OSDMenu tidak menjalankan apa pun sendiri: pilih RIPPS2 di sana, dan EXIT dari game kembali ke menu itu. Untuk konsol yang langsung menjalankan RIPPS2, BIBLE memasang PS2BBL 1.2.0 di kartu memori (Boot Loader).",
    "BOOT LOCK bekerja lewat boot loader di kartu memori (PS2BBL, FMCB, atau OSDMenu), dan di sini tidak ada.",
    "Kartu memori di slot %d menjalankan %s saat menyala, dan BOOT LOCK tidak menemukan konfigurasinya untuk diubah (yang dicari: %s).",
    "Kartu memori di slot %d menjalankan %s saat menyala, yang tidak bisa diatur BOOT LOCK: ia bekerja lewat PS2BBL, FMCB, dan OSDMenu.",
    "Ada boot loader dengan kunci RIPPS2 di konsol ini.",
    "EXIT dari game: peramban, lalu boot loader-mu (BOOT LOCK)",
]
T['Indonesian_l'] = {
    'HINT_EXITPATH': "Ke mana EXIT di Menu Dalam Game pergi. Sebaiknya dikosongkan dengan BOOT LOCK menyala (PS2BBL, FMCB, atau OSDMenu, atau BIBLE terpasang): EXIT lalu lewat peramban, yang menjalankan boot loader-mu dan RIPPS2 seperti saat menyala, jalan pulang paling aman. Kosong tanpa kunci: ELF milik RIPPS2 sendiri di kartu memori atau drive USB FAT32, dimuat tepat setelah reset, yang tidak semua game siapkan. Browser: peramban PS2. ELF di MMCE sama sekali tidak bisa dijangkau saat itu.",
    'HINT_RIPPS2_BOOT_LOCK': "Menjalankan RIPPS2 saat menyala lewat boot loader-mu: PS2BBL dan FMCB langsung menjalankannya, OSDMenu menaruhnya pertama di menunya, dan EXIT dari game kembali lewat jalan yang sama. Mati mengembalikan yang ada sebelumnya. Belum ada? Boot Loader menginstal BIBLE.",
}

T['Vietnamese'] = [
    " (Đã đặt các cấu hình tìm thấy: %s.)",
    " Hãy lưu cài đặt của nó một lần bằng trình cấu hình riêng của nó, rồi bật lại BOOT LOCK.",
    "%s không thể chạy RIPPS2 từ chỗ nó đang ở (%s), và RIPPS2 không tự sao chép. Hãy đặt RIPPS2.ELF lên thẻ nhớ hoặc ổ USB rồi chạy từ đó.",
    "BOOT LOCK không ghi được cấu hình của trình khởi động. Hãy kiểm tra thẻ nhớ hoặc ổ không bị chống ghi, rồi thử lại.",
    "BOOT LOCK không tìm thấy cấu hình trình khởi động nào để thay đổi.",
    "BOOT LOCK đang tắt. Trình khởi động của bạn chạy thứ nó đã chạy trước đây (%s).",
    "BOOT LOCK đang bật. Giờ %s chạy RIPPS2 khi bật máy (%s), và khi Vá IGR để trống, EXIT của trò chơi quay về theo cùng đường đó. Giữ một trong các nút của nó trong lúc máy khởi động để vào thứ khác.%s",
    "BOOT LOCK đã đặt RIPPS2 lên đầu menu của OSDMenu (%s). OSDMenu không tự chạy gì cả: hãy chọn RIPPS2 ở đó, và EXIT của trò chơi quay về menu ấy. Để máy chạy RIPPS2 ngay, BIBLE cài PS2BBL 1.2.0 lên thẻ nhớ (Trình khởi động).",
    "BOOT LOCK hoạt động qua một trình khởi động trên thẻ nhớ (PS2BBL, FMCB hoặc OSDMenu), và ở đây không có.",
    "Thẻ nhớ ở khe %d chạy %s khi bật máy, và BOOT LOCK không tìm thấy cấu hình nào của nó để thay đổi (nó tìm %s).",
    "Thẻ nhớ ở khe %d chạy %s khi bật máy, thứ mà BOOT LOCK không thể đặt: nó hoạt động qua PS2BBL, FMCB và OSDMenu.",
    "Máy này có một trình khởi động mang khóa của RIPPS2.",
    "EXIT của trò chơi: trình duyệt, rồi trình khởi động của bạn (BOOT LOCK)",
]
T['Vietnamese_l'] = {
    'HINT_EXITPATH': "EXIT trong Menu trong trò chơi đi đâu. Tốt nhất để trống khi BOOT LOCK bật (PS2BBL, FMCB hoặc OSDMenu, hoặc BIBLE đã thiết lập): khi đó EXIT đi qua trình duyệt, nơi chạy trình khởi động của bạn và RIPPS2 như lúc bật máy, cách quay về an toàn nhất. Để trống khi không khóa: ELF của chính RIPPS2 trên thẻ nhớ hoặc ổ USB FAT32, được tải ngay sau khi đặt lại, việc mà không phải trò chơi nào cũng để máy sẵn sàng. Browser: trình duyệt PS2. Một ELF trên MMCE lúc đó hoàn toàn không truy cập được.",
    'HINT_RIPPS2_BOOT_LOCK': "Chạy RIPPS2 khi bật máy qua trình khởi động của bạn: PS2BBL và FMCB chạy nó ngay, OSDMenu đặt nó lên đầu menu, và EXIT của trò chơi quay về theo cùng đường. Tắt sẽ trả lại thứ có trước đây. Chưa có? Trình khởi động sẽ cài BIBLE.",
}

T['Filipino'] = [
    " (Naitakda ang mga nakitang config: %s.)",
    " I-save nang isang beses ang settings nito gamit ang sarili nitong configurator, saka i-on muli ang BOOT LOCK.",
    "Hindi masisimulan ng %s ang RIPPS2 mula sa kinalalagyan nito ngayon (%s), at hindi kinokopya ng RIPPS2 ang sarili nito. Ilagay ang RIPPS2.ELF sa memory card o USB drive at simulan ito mula roon.",
    "Hindi maisulat ng BOOT LOCK ang config ng boot loader. Tingnan kung hindi naka-write protect ang memory card o drive, saka subukan ulit.",
    "Walang nahanap na boot loader config ang BOOT LOCK na babaguhin.",
    "Naka-off ang BOOT LOCK. Sinisimulan ng boot loader mo ang dati nitong sinisimulan (%s).",
    "Naka-on ang BOOT LOCK. Sinisimulan na ng %s ang RIPPS2 sa pag-on (%s), at ibinabalik ng walang lamang IGR path ang EXIT ng laro sa parehong daan. Pindutin nang matagal ang isa sa mga button nito habang nagsisimula ang console para makapunta sa iba.%s",
    "Inilagay ng BOOT LOCK ang RIPPS2 sa una sa menu ng OSDMenu (%s). Walang sinisimulan ang OSDMenu nang kusa: piliin doon ang RIPPS2, at bumabalik sa menu na iyon ang EXIT ng laro. Para sa console na agad nagsisimula ng RIPPS2, inilalagay ng BIBLE ang PS2BBL 1.2.0 sa memory card (Boot Loader).",
    "Gumagana ang BOOT LOCK sa pamamagitan ng boot loader sa memory card (PS2BBL, FMCB o OSDMenu), at wala nito rito.",
    "Sinisimulan ng memory card sa slot %d ang %s sa pag-on, at walang nahanap ang BOOT LOCK na config nito na babaguhin (hinahanap nito ang %s).",
    "Sinisimulan ng memory card sa slot %d ang %s sa pag-on, na hindi kayang itakda ng BOOT LOCK: gumagana ito sa pamamagitan ng PS2BBL, FMCB at OSDMenu.",
    "May boot loader na may lock ng RIPPS2 sa console na ito.",
    "EXIT ng laro: ang browser, saka ang boot loader mo (BOOT LOCK)",
]
T['Filipino_l'] = {
    'HINT_EXITPATH': "Kung saan papunta ang EXIT sa Menu sa laro. Mas mabuting iwanang walang laman nang naka-on ang BOOT LOCK (PS2BBL, FMCB o OSDMenu, o naka-set up ang BIBLE): dadaan ang EXIT sa browser, na nagsisimula ng boot loader mo at ng RIPPS2 gaya ng sa pag-on, ang pinakaligtas na pabalik. Walang laman nang walang lock: ang sariling ELF ng RIPPS2 sa memory card o FAT32 USB drive, nilo-load agad pagkatapos ng reset, na hindi lahat ng laro ay nag-iiwan ng console na handa. Browser: ang PS2 browser. Hindi maaabot ang ELF sa MMCE noon.",
    'HINT_RIPPS2_BOOT_LOCK': "Sinisimulan ang RIPPS2 sa pag-on sa pamamagitan ng boot loader mo: agad itong sinisimulan ng PS2BBL at FMCB, inilalagay ito ng OSDMenu sa una sa menu nito, at bumabalik ang EXIT ng laro sa parehong daan. Ibinabalik ng Off ang dati. Wala pa? Nag-i-install ng BIBLE ang Boot Loader.",
}

os.makedirs(OUT, exist_ok=True)
for lang in [k for k in T if not k.endswith('_l')]:
    s = {str(i): v for i, v in enumerate(T[lang])}
    json.dump({'s': s, 'l': T[lang + '_l']}, open(os.path.join(OUT, lang + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(lang, len(s))
