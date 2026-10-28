"""Build 121: the boot sound's copy beside RIPPS2 on the memory card (BIOS Sounds > Rip offers it). Two strings for all
32 languages, each keeping its English's conversions in the same order. Run from the repo root:
python tools/lang121/batch.py (writes tr121/<Language>.json), then python tools/lang121/merge121.py <Language> ... and
python elf/lang/ripps2lang.py check."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'tr121')

# each language: the offer (%s the AUDIO folder, %d KB the file, %d KB free), and the copy that failed (%s where, %s from)
T = {
    'Albanian': ("%s nis pas shtyllave, kështu që tingulli i nisjes luhet vonë. START kopjon boot.adp (%d KB) pranë RIPPS2 në kartën e memories (%d KB të lira), ku luhet ndërsa ngrihen shtyllat.",
                 "Tingulli i nisjes nuk u kopjua dot në %s. Ai luhet ende nga %s."),
    'Arabic': ("يبدأ %s بعد الأعمدة، لذا يتأخر صوت الإقلاع. يضغط START لنسخ boot.adp (%d KB) بجانب RIPPS2 على بطاقة الذاكرة (%d KB متاحة)، حيث يُعزف مع ارتفاع الأعمدة.",
               "تعذر نسخ صوت الإقلاع إلى %s. ما زال يُعزف من %s."),
    'Bulgarian': ("%s стартира след колоните, затова звукът при стартиране закъснява. START копира boot.adp (%d KB) до RIPPS2 на картата памет (%d KB свободни), където звучи, докато колоните се издигат.",
                  "Звукът при стартиране не можа да се копира в %s. Той все още звучи от %s."),
    'Cebuano': ("Ang %s magsugod human sa mga haligi, mao nga ulahi ang tingog sa pagsugod. Ang START mokopya sa boot.adp (%d KB) tupad sa RIPPS2 sa memory card (%d KB ang bakante), diin kini motingog samtang mosaka ang mga haligi.",
                "Ang tingog sa pagsugod dili makopya sa %s. Motingog gihapon kini gikan sa %s."),
    'Croatian': ("%s se pokreće nakon stupova, pa zvuk pokretanja kasni. START kopira boot.adp (%d KB) uz RIPPS2 na memorijsku karticu (%d KB slobodno), gdje svira dok se stupovi dižu.",
                 "Zvuk pokretanja nije se mogao kopirati u %s. I dalje svira iz %s."),
    'Czech': ("%s se spouští až po sloupech, takže zvuk spuštění hraje pozdě. START zkopíruje boot.adp (%d KB) vedle RIPPS2 na paměťovou kartu (%d KB volno), kde hraje, když se sloupy zvedají.",
              "Zvuk spuštění se nepodařilo zkopírovat do %s. Stále hraje z %s."),
    'Danish': ("%s starter efter søjlerne, så opstartslyden spiller for sent. START kopierer boot.adp (%d KB) ved siden af RIPPS2 på hukommelseskortet (%d KB fri), hvor den spiller, mens søjlerne rejser sig.",
               "Opstartslyden kunne ikke kopieres til %s. Den spiller stadig fra %s."),
    'Dutch': ("%s start na de pilaren, dus het opstartgeluid klinkt te laat. START kopieert boot.adp (%d KB) naast RIPPS2 op de geheugenkaart (%d KB vrij), waar het klinkt terwijl de pilaren oprijzen.",
              "Het opstartgeluid kon niet naar %s worden gekopieerd. Het klinkt nog steeds vanaf %s."),
    'Filipino': ("Nagsisimula ang %s pagkatapos ng mga haligi, kaya huli ang tunog ng pag-boot. Kinokopya ng START ang boot.adp (%d KB) katabi ng RIPPS2 sa memory card (%d KB ang bakante), kung saan ito tumutunog habang umaangat ang mga haligi.",
                 "Hindi makopya ang tunog ng pag-boot sa %s. Tumutunog pa rin ito mula sa %s."),
    'French': ("%s démarre après les piliers, donc le son de démarrage arrive en retard. START copie boot.adp (%d Ko) à côté de RIPPS2 sur la carte mémoire (%d Ko libres), où il joue pendant que les piliers s'élèvent.",
               "Le son de démarrage n'a pas pu être copié vers %s. Il joue toujours depuis %s."),
    'Galician': ("%s arrinca despois dos piares, así que o son de arranque soa tarde. START copia boot.adp (%d KB) xunto a RIPPS2 na tarxeta de memoria (%d KB libres), onde soa mentres se erguen os piares.",
                 "Non se puido copiar o son de arranque a %s. Aínda soa desde %s."),
    'German': ("%s startet erst nach den Säulen, deshalb kommt der Startsound zu spät. START kopiert boot.adp (%d KB) neben RIPPS2 auf die Memory Card (%d KB frei), wo er spielt, während die Säulen aufsteigen.",
               "Der Startsound konnte nicht nach %s kopiert werden. Er spielt weiter von %s."),
    'Greek': ("Το %s ξεκινά μετά τις κολόνες, οπότε ο ήχος εκκίνησης παίζει αργά. Το START αντιγράφει το boot.adp (%d KB) δίπλα στο RIPPS2 στην κάρτα μνήμης (%d KB ελεύθερα), όπου παίζει καθώς υψώνονται οι κολόνες.",
              "Ο ήχος εκκίνησης δεν αντιγράφηκε στο %s. Παίζει ακόμα από το %s."),
    'Hungarian': ("A(z) %s az oszlopok után indul, ezért az indítási hang késik. A START a boot.adp fájlt (%d KB) a RIPPS2 mellé másolja a memóriakártyára (%d KB szabad), ahol az oszlopok emelkedésekor szól.",
                  "Az indítási hangot nem sikerült a(z) %s helyre másolni. Továbbra is innen szól: %s."),
    'Indonesian': ("%s mulai setelah pilar, jadi suara boot terlambat. START menyalin boot.adp (%d KB) di samping RIPPS2 di kartu memori (%d KB kosong), tempat suara itu diputar saat pilar naik.",
                   "Suara boot tidak dapat disalin ke %s. Suara itu masih diputar dari %s."),
    'Italian': ("%s parte dopo i pilastri, quindi il suono di avvio arriva in ritardo. START copia boot.adp (%d KB) accanto a RIPPS2 sulla memory card (%d KB liberi), dove suona mentre i pilastri si alzano.",
                "Non è stato possibile copiare il suono di avvio in %s. Suona ancora da %s."),
    'Japanese': ("%s は柱のあとに起動するため、起動音が遅れます。START で boot.adp（%d KB）をメモリーカードの RIPPS2 の横にコピーします（空き %d KB）。そこなら柱が立ち上がると同時に鳴ります。",
                 "起動音を %s にコピーできませんでした。引き続き %s から鳴ります。"),
    'Korean': ("%s은(는) 기둥보다 늦게 시작되어 부팅 소리가 늦게 납니다. START는 boot.adp(%d KB)를 메모리 카드의 RIPPS2 옆에 복사합니다(여유 %d KB). 그러면 기둥이 솟을 때 소리가 납니다.",
               "부팅 소리를 %s에 복사하지 못했습니다. 계속 %s에서 재생됩니다."),
    'Laotian': ("%s ເລີ່ມຫຼັງຈາກເສົາ, ສະນັ້ນສຽງເປີດເຄື່ອງດັງຊ້າ. START ສຳເນົາ boot.adp (%d KB) ໄວ້ຂ້າງ RIPPS2 ໃນເມມໂມຣີກາດ (ວ່າງ %d KB), ບ່ອນທີ່ມັນດັງຂຶ້ນເມື່ອເສົາຕັ້ງຂຶ້ນ.",
                "ບໍ່ສາມາດສຳເນົາສຽງເປີດເຄື່ອງໄປທີ່ %s ໄດ້. ມັນຍັງດັງຈາກ %s."),
    'Persian': ("%s پس از ستون‌ها راه می‌افتد، پس صدای راه‌اندازی دیر پخش می‌شود. START فایل boot.adp (%d KB) را کنار RIPPS2 روی کارت حافظه کپی می‌کند (%d KB آزاد)، جایی که با بالا آمدن ستون‌ها پخش می‌شود.",
                "صدای راه‌اندازی در %s کپی نشد. هنوز از %s پخش می‌شود."),
    'Polish': ("%s startuje po filarach, więc dźwięk startowy gra za późno. START kopiuje boot.adp (%d KB) obok RIPPS2 na kartę pamięci (%d KB wolne), gdzie gra, gdy filary się wznoszą.",
               "Nie udało się skopiować dźwięku startowego do %s. Nadal gra z %s."),
    'Portuguese': ("%s arranca depois dos pilares, por isso o som de arranque toca tarde. START copia boot.adp (%d KB) para junto do RIPPS2 no cartão de memória (%d KB livres), onde toca enquanto os pilares sobem.",
                   "Não foi possível copiar o som de arranque para %s. Continua a tocar a partir de %s."),
    'Portuguese_BR': ("%s inicia depois dos pilares, então o som de inicialização toca atrasado. START copia boot.adp (%d KB) ao lado do RIPPS2 no memory card (%d KB livres), onde ele toca enquanto os pilares sobem.",
                      "Não foi possível copiar o som de inicialização para %s. Ele ainda toca de %s."),
    'Romana': ("%s pornește după coloane, așa că sunetul de pornire se aude târziu. START copiază boot.adp (%d KB) lângă RIPPS2 pe cardul de memorie (%d KB liberi), unde se aude pe măsură ce coloanele se înalță.",
               "Sunetul de pornire nu a putut fi copiat în %s. Se aude în continuare din %s."),
    'Russian': ("%s запускается после колонн, поэтому звук запуска опаздывает. START копирует boot.adp (%d КБ) рядом с RIPPS2 на карту памяти (свободно %d КБ), где он звучит, пока поднимаются колонны.",
                "Не удалось скопировать звук запуска в %s. Он по-прежнему звучит из %s."),
    'SChinese': ("%s 在柱子之后才启动，所以开机音效会晚到。START 会把 boot.adp（%d KB）复制到记忆卡上 RIPPS2 旁边（剩余 %d KB），这样它会在柱子升起时响起。",
                 "无法将开机音效复制到 %s。它仍从 %s 播放。"),
    'Serbian': ("%s se pokreće posle stubova, pa zvuk pokretanja kasni. START kopira boot.adp (%d KB) pored RIPPS2 na memorijsku karticu (%d KB slobodno), gde svira dok se stubovi dižu.",
                "Zvuk pokretanja nije mogao da se kopira u %s. I dalje svira iz %s."),
    'Spanish': ("%s arranca después de los pilares, así que el sonido de inicio suena tarde. START copia boot.adp (%d KB) junto a RIPPS2 en la tarjeta de memoria (%d KB libres), donde suena mientras se alzan los pilares.",
                "No se pudo copiar el sonido de inicio a %s. Sigue sonando desde %s."),
    'Swedish': ("%s startar efter pelarna, så startljudet spelas för sent. START kopierar boot.adp (%d KB) bredvid RIPPS2 på minneskortet (%d KB ledigt), där det spelas när pelarna reser sig.",
                "Startljudet kunde inte kopieras till %s. Det spelas fortfarande från %s."),
    'TChinese': ("%s 在柱子之後才啟動，所以開機音效會晚到。START 會把 boot.adp（%d KB）複製到記憶卡上 RIPPS2 旁邊（剩餘 %d KB），這樣它會在柱子升起時響起。",
                 "無法將開機音效複製到 %s。它仍從 %s 播放。"),
    'Turkish': ("%s sütunlardan sonra başlıyor, bu yüzden açılış sesi geç çalıyor. START, boot.adp dosyasını (%d KB) hafıza kartında RIPPS2'nin yanına kopyalar (%d KB boş); orada sütunlar yükselirken çalar.",
                "Açılış sesi %s konumuna kopyalanamadı. Hâlâ %s konumundan çalıyor."),
    'Vietnamese': ("%s khởi động sau các cột trụ, nên âm thanh khởi động phát muộn. START sao chép boot.adp (%d KB) cạnh RIPPS2 trên thẻ nhớ (còn trống %d KB), nơi nó phát khi các cột trụ vươn lên.",
                   "Không thể sao chép âm thanh khởi động vào %s. Nó vẫn phát từ %s."),
}

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for lang, (a, b) in T.items():
        json.dump({'s': {'0': a, '1': b}, 'l': {}}, open(os.path.join(OUT, lang + '.json'), 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
    print(len(T), 'languages')
