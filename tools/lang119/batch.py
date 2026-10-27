"""Build 119 strings (s119.json, no labels) for all 32 languages: the ART Pack's flow as the other long jobs have it.
Run from the repo root: python tools/lang119/batch.py (writes tr119/<Language>.json). The order of each list is s119.json's:
  0 "%s free"  1 "%sART/art.tar: reads %s/s, %s"  2 "... the fastest, %s"  3 "ART PACK"  4 "About %d min"
  5 "Looking at the ART folders: %d pictures, %s"  6 "No started drive has room ..."  7 "PACKING THE ART"
  8 "PICTURE %d OF %d"  9 "Pictures: %d (%s). ART folders: %d."  10 "Stop? ..."  11 "The ART folders stay ..."
  12 "Under a minute"  13 "free space unknown"."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'tr119')

T = {
    'German': [
        "%s frei", "%sART/art.tar: liest %s/s, %s", "%sART/art.tar: liest %s/s, das schnellste, %s", "ART-PAKET", "Etwa %d Min.",
        "Die ART-Ordner werden angesehen: %d Bilder, %s",
        "Kein gestartetes Laufwerk hat Platz für das ART-Paket: Es braucht etwa %s. Schaffe Platz auf dem Laufwerk, auf dem du stöberst, und versuche es dann erneut.",
        "BILDER WERDEN GEPACKT", "BILD %d VON %d", "Bilder: %d (%s). ART-Ordner: %d.",
        "Anhalten? Das unfertige Paket wird entfernt; die ART-Ordner bleiben, wie sie sind.",
        "Die ART-Ordner bleiben, wie sie sind: Das Paket ist eine Kopie.", "Unter einer Minute", "freier Platz unbekannt"],
    'French': [
        "%s libres", "%sART/art.tar : lit %s/s, %s", "%sART/art.tar : lit %s/s, le plus rapide, %s", "PACK ART", "Environ %d min",
        "Lecture des dossiers ART : %d images, %s",
        "Aucun périphérique démarré n'a la place pour le pack ART : il lui faut environ %s. Libère de la place sur le périphérique où tu navigues, puis réessaie.",
        "MISE EN PACK DES IMAGES", "IMAGE %d SUR %d", "Images : %d (%s). Dossiers ART : %d.",
        "Arrêter ? Le pack inachevé est supprimé ; les dossiers ART restent tels quels.",
        "Les dossiers ART restent tels quels : le pack est une copie.", "Moins d'une minute", "place libre inconnue"],
    'Spanish': [
        "%s libres", "%sART/art.tar: lee %s/s, %s", "%sART/art.tar: lee %s/s, la más rápida, %s", "PAQUETE ART", "Unos %d min",
        "Revisando las carpetas ART: %d imágenes, %s",
        "Ninguna unidad iniciada tiene espacio para el paquete ART: necesita unos %s. Libera espacio en la unidad desde la que navegas y vuelve a intentarlo.",
        "EMPAQUETANDO LAS IMÁGENES", "IMAGEN %d DE %d", "Imágenes: %d (%s). Carpetas ART: %d.",
        "¿Detener? Se quita el paquete sin terminar; las carpetas ART quedan como están.",
        "Las carpetas ART quedan como están: el paquete es una copia.", "Menos de un minuto", "espacio libre desconocido"],
    'Italian': [
        "%s liberi", "%sART/art.tar: legge %s/s, %s", "%sART/art.tar: legge %s/s, la più veloce, %s", "PACCHETTO ART", "Circa %d min",
        "Controllo delle cartelle ART: %d immagini, %s",
        "Nessuna unità avviata ha spazio per il pacchetto ART: servono circa %s. Libera spazio sull'unità da cui navighi, poi riprova.",
        "CREAZIONE DEL PACCHETTO", "IMMAGINE %d DI %d", "Immagini: %d (%s). Cartelle ART: %d.",
        "Fermare? Il pacchetto incompleto viene rimosso; le cartelle ART restano come sono.",
        "Le cartelle ART restano come sono: il pacchetto è una copia.", "Meno di un minuto", "spazio libero sconosciuto"],
    'Portuguese': [
        "%s livres", "%sART/art.tar: lê %s/s, %s", "%sART/art.tar: lê %s/s, a mais rápida, %s", "PACOTE ART", "Cerca de %d min",
        "A ver as pastas ART: %d imagens, %s",
        "Nenhuma unidade iniciada tem espaço para o pacote ART: precisa de cerca de %s. Liberta espaço na unidade onde navegas e tenta de novo.",
        "A JUNTAR AS IMAGENS", "IMAGEM %d DE %d", "Imagens: %d (%s). Pastas ART: %d.",
        "Parar? O pacote inacabado é removido; as pastas ART ficam como estão.",
        "As pastas ART ficam como estão: o pacote é uma cópia.", "Menos de um minuto", "espaço livre desconhecido"],
    'Portuguese_BR': [
        "%s livres", "%sART/art.tar: lê %s/s, %s", "%sART/art.tar: lê %s/s, a mais rápida, %s", "PACOTE ART", "Cerca de %d min",
        "Olhando as pastas ART: %d imagens, %s",
        "Nenhuma unidade iniciada tem espaço para o pacote ART: ele precisa de cerca de %s. Libere espaço na unidade em que você navega e tente de novo.",
        "JUNTANDO AS IMAGENS", "IMAGEM %d DE %d", "Imagens: %d (%s). Pastas ART: %d.",
        "Parar? O pacote inacabado é removido; as pastas ART ficam como estão.",
        "As pastas ART ficam como estão: o pacote é uma cópia.", "Menos de um minuto", "espaço livre desconhecido"],
    'Dutch': [
        "%s vrij", "%sART/art.tar: leest %s/s, %s", "%sART/art.tar: leest %s/s, het snelst, %s", "ART-PAKKET", "Ongeveer %d min",
        "De ART-mappen worden bekeken: %d afbeeldingen, %s",
        "Geen gestart station heeft ruimte voor het ART-pakket: het heeft ongeveer %s nodig. Maak ruimte vrij op het station waar je doorheen bladert en probeer het opnieuw.",
        "AFBEELDINGEN INPAKKEN", "AFBEELDING %d VAN %d", "Afbeeldingen: %d (%s). ART-mappen: %d.",
        "Stoppen? Het onvoltooide pakket wordt verwijderd; de ART-mappen blijven zoals ze zijn.",
        "De ART-mappen blijven zoals ze zijn: het pakket is een kopie.", "Minder dan een minuut", "vrije ruimte onbekend"],
    'Galician': [
        "%s libres", "%sART/art.tar: le %s/s, %s", "%sART/art.tar: le %s/s, a máis rápida, %s", "PAQUETE ART", "Uns %d min",
        "Revisando os cartafoles ART: %d imaxes, %s",
        "Ningunha unidade iniciada ten espazo para o paquete ART: precisa uns %s. Libera espazo na unidade desde a que navegas e téntao de novo.",
        "EMPAQUETANDO AS IMAXES", "IMAXE %d DE %d", "Imaxes: %d (%s). Cartafoles ART: %d.",
        "Deter? Quítase o paquete sen rematar; os cartafoles ART quedan como están.",
        "Os cartafoles ART quedan como están: o paquete é unha copia.", "Menos dun minuto", "espazo libre descoñecido"],
    'Swedish': [
        "%s ledigt", "%sART/art.tar: läser %s/s, %s", "%sART/art.tar: läser %s/s, den snabbaste, %s", "ART-PAKET", "Cirka %d min",
        "Tittar på ART-mapparna: %d bilder, %s",
        "Ingen startad enhet har plats för ART-paketet: det behöver cirka %s. Frigör plats på enheten du bläddrar från och försök igen.",
        "PACKAR BILDERNA", "BILD %d AV %d", "Bilder: %d (%s). ART-mappar: %d.",
        "Stoppa? Det ofärdiga paketet tas bort; ART-mapparna förblir som de är.",
        "ART-mapparna förblir som de är: paketet är en kopia.", "Under en minut", "ledigt utrymme okänt"],
    'Danish': [
        "%s ledig", "%sART/art.tar: læser %s/s, %s", "%sART/art.tar: læser %s/s, det hurtigste, %s", "ART-PAKKE", "Ca. %d min",
        "Kigger på ART-mapperne: %d billeder, %s",
        "Intet startet drev har plads til ART-pakken: den skal bruge ca. %s. Frigør plads på det drev, du browser fra, og prøv igen.",
        "PAKKER BILLEDERNE", "BILLEDE %d AF %d", "Billeder: %d (%s). ART-mapper: %d.",
        "Stop? Den ufærdige pakke fjernes; ART-mapperne forbliver, som de er.",
        "ART-mapperne forbliver, som de er: pakken er en kopi.", "Under et minut", "ledig plads ukendt"],
    'Polish': [
        "%s wolne", "%sART/art.tar: czyta %s/s, %s", "%sART/art.tar: czyta %s/s, najszybszy, %s", "PACZKA ART", "Około %d min",
        "Sprawdzanie folderów ART: %d obrazów, %s",
        "Żaden uruchomiony dysk nie ma miejsca na paczkę ART: potrzebuje około %s. Zwolnij miejsce na dysku, z którego przeglądasz, i spróbuj ponownie.",
        "PAKOWANIE OBRAZÓW", "OBRAZ %d Z %d", "Obrazy: %d (%s). Foldery ART: %d.",
        "Zatrzymać? Niedokończona paczka zostanie usunięta; foldery ART zostają bez zmian.",
        "Foldery ART zostają bez zmian: paczka jest kopią.", "Mniej niż minuta", "wolne miejsce nieznane"],
    'Czech': [
        "%s volno", "%sART/art.tar: čte %s/s, %s", "%sART/art.tar: čte %s/s, nejrychlejší, %s", "BALÍČEK ART", "Asi %d min",
        "Prohlížení složek ART: %d obrázků, %s",
        "Žádný spuštěný disk nemá místo na balíček ART: potřebuje asi %s. Uvolni místo na disku, ze kterého procházíš, a zkus to znovu.",
        "BALENÍ OBRÁZKŮ", "OBRÁZEK %d Z %d", "Obrázky: %d (%s). Složky ART: %d.",
        "Zastavit? Nedokončený balíček se odstraní; složky ART zůstanou, jak jsou.",
        "Složky ART zůstanou, jak jsou: balíček je kopie.", "Méně než minuta", "volné místo neznámé"],
    'Croatian': [
        "%s slobodno", "%sART/art.tar: čita %s/s, %s", "%sART/art.tar: čita %s/s, najbrži, %s", "PAKET ART", "Oko %d min",
        "Pregled mapa ART: %d slika, %s",
        "Nijedan pokrenuti pogon nema mjesta za paket ART: treba mu oko %s. Oslobodi mjesto na pogonu s kojeg pregledavaš, pa pokušaj ponovno.",
        "PAKIRANJE SLIKA", "SLIKA %d OD %d", "Slike: %d (%s). Mape ART: %d.",
        "Zaustaviti? Nedovršeni paket se uklanja; mape ART ostaju kakve jesu.",
        "Mape ART ostaju kakve jesu: paket je kopija.", "Manje od minute", "slobodno mjesto nepoznato"],
    'Serbian': [
        "%s slobodno", "%sART/art.tar: čita %s/s, %s", "%sART/art.tar: čita %s/s, najbrži, %s", "PAKET ART", "Oko %d min",
        "Pregled fascikli ART: %d slika, %s",
        "Nijedan pokrenuti disk nema mesta za paket ART: treba mu oko %s. Oslobodi mesto na disku sa kog pregledaš, pa pokušaj ponovo.",
        "PAKOVANJE SLIKA", "SLIKA %d OD %d", "Slike: %d (%s). Fascikle ART: %d.",
        "Zaustaviti? Nedovršeni paket se uklanja; fascikle ART ostaju kakve jesu.",
        "Fascikle ART ostaju kakve jesu: paket je kopija.", "Manje od minuta", "slobodno mesto nepoznato"],
    'Romana': [
        "%s liber", "%sART/art.tar: citește %s/s, %s", "%sART/art.tar: citește %s/s, cea mai rapidă, %s", "PACHET ART", "Cam %d min",
        "Se cercetează folderele ART: %d imagini, %s",
        "Nicio unitate pornită nu are loc pentru pachetul ART: are nevoie de cam %s. Fă loc pe unitatea de pe care navighezi, apoi încearcă din nou.",
        "SE ÎMPACHETEAZĂ IMAGINILE", "IMAGINEA %d DIN %d", "Imagini: %d (%s). Foldere ART: %d.",
        "Oprești? Pachetul neterminat este șters; folderele ART rămân cum sunt.",
        "Folderele ART rămân cum sunt: pachetul este o copie.", "Sub un minut", "spațiu liber necunoscut"],
    'Hungarian': [
        "%s szabad", "%sART/art.tar: %s/s olvasás, %s", "%sART/art.tar: %s/s olvasás, a leggyorsabb, %s", "ART CSOMAG", "Kb. %d perc",
        "Az ART mappák átnézése: %d kép, %s",
        "Egyik elindított meghajtón sincs hely az ART csomagnak: kb. %s kell neki. Szabadíts fel helyet azon a meghajtón, amelyről böngészel, aztán próbáld újra.",
        "A KÉPEK CSOMAGOLÁSA", "KÉP: %d / %d", "Képek: %d (%s). ART mappák: %d.",
        "Leállítod? A félkész csomag törlődik; az ART mappák maradnak, ahogy vannak.",
        "Az ART mappák maradnak, ahogy vannak: a csomag másolat.", "Egy percen belül", "a szabad hely ismeretlen"],
    'Russian': [
        "свободно %s", "%sART/art.tar: чтение %s/с, %s", "%sART/art.tar: чтение %s/с, самый быстрый, %s", "ПАКЕТ ART", "Около %d мин",
        "Просмотр папок ART: изображений %d, %s",
        "Ни на одном запущенном накопителе нет места для пакета ART: нужно около %s. Освободи место на накопителе, с которого просматриваешь игры, и попробуй снова.",
        "УПАКОВКА ИЗОБРАЖЕНИЙ", "ИЗОБРАЖЕНИЕ %d ИЗ %d", "Изображений: %d (%s). Папок ART: %d.",
        "Остановить? Незаконченный пакет удаляется; папки ART останутся как есть.",
        "Папки ART останутся как есть: пакет является копией.", "Меньше минуты", "свободное место неизвестно"],
    'Bulgarian': [
        "%s свободни", "%sART/art.tar: чете %s/s, %s", "%sART/art.tar: чете %s/s, най-бързото, %s", "ПАКЕТ ART", "Около %d мин",
        "Преглед на папките ART: %d изображения, %s",
        "Никое стартирано устройство няма място за пакета ART: нужни са около %s. Освободи място на устройството, от което разглеждаш, и опитай отново.",
        "ПАКЕТИРАНЕ НА ИЗОБРАЖЕНИЯТА", "ИЗОБРАЖЕНИЕ %d ОТ %d", "Изображения: %d (%s). Папки ART: %d.",
        "Да се спре ли? Недовършеният пакет се премахва; папките ART остават каквито са.",
        "Папките ART остават каквито са: пакетът е копие.", "Под минута", "свободното място е неизвестно"],
    'Greek': [
        "%s ελεύθερα", "%sART/art.tar: διαβάζει %s/s, %s", "%sART/art.tar: διαβάζει %s/s, η πιο γρήγορη, %s", "ΠΑΚΕΤΟ ART", "Περίπου %d λεπτά",
        "Έλεγχος των φακέλων ART: %d εικόνες, %s",
        "Καμία μονάδα που ξεκίνησε δεν έχει χώρο για το πακέτο ART: χρειάζεται περίπου %s. Ελευθέρωσε χώρο στη μονάδα από την οποία περιηγείσαι και δοκίμασε ξανά.",
        "ΠΑΚΕΤΑΡΙΣΜΑ ΤΩΝ ΕΙΚΟΝΩΝ", "ΕΙΚΟΝΑ %d ΑΠΟ %d", "Εικόνες: %d (%s). Φάκελοι ART: %d.",
        "Διακοπή; Το μισοτελειωμένο πακέτο αφαιρείται· οι φάκελοι ART μένουν όπως είναι.",
        "Οι φάκελοι ART μένουν όπως είναι: το πακέτο είναι αντίγραφο.", "Κάτω από ένα λεπτό", "ο ελεύθερος χώρος είναι άγνωστος"],
    'Turkish': [
        "%s boş", "%sART/art.tar: %s/s okur, %s", "%sART/art.tar: %s/s okur, en hızlısı, %s", "ART PAKETİ", "Yaklaşık %d dk",
        "ART klasörlerine bakılıyor: %d resim, %s",
        "Başlatılan hiçbir sürücüde ART paketi için yer yok: yaklaşık %s gerekiyor. Göz attığın sürücüde yer aç ve yeniden dene.",
        "RESİMLER PAKETLENİYOR", "RESİM %d / %d", "Resimler: %d (%s). ART klasörleri: %d.",
        "Durdurulsun mu? Bitmemiş paket kaldırılır; ART klasörleri olduğu gibi kalır.",
        "ART klasörleri olduğu gibi kalır: paket bir kopyadır.", "Bir dakikadan az", "boş alan bilinmiyor"],
    'Albanian': [
        "%s të lira", "%sART/art.tar: lexon %s/s, %s", "%sART/art.tar: lexon %s/s, më i shpejti, %s", "PAKETA ART", "Rreth %d min",
        "Po shikohen dosjet ART: %d figura, %s",
        "Asnjë disk i nisur nuk ka vend për paketën ART: i duhen rreth %s. Liro vend në diskun nga i cili shfleton, pastaj provo sërish.",
        "PO PAKETOHEN FIGURAT", "FIGURA %d NGA %d", "Figura: %d (%s). Dosje ART: %d.",
        "Të ndalet? Paketa e papërfunduar hiqet; dosjet ART mbeten siç janë.",
        "Dosjet ART mbeten siç janë: paketa është një kopje.", "Më pak se një minutë", "hapësira e lirë e panjohur"],
    'Indonesian': [
        "%s kosong", "%sART/art.tar: membaca %s/s, %s", "%sART/art.tar: membaca %s/s, yang tercepat, %s", "PAKET ART", "Sekitar %d mnt",
        "Melihat folder ART: %d gambar, %s",
        "Tidak ada drive yang dimulai yang punya ruang untuk paket ART: perlu sekitar %s. Kosongkan ruang di drive tempat kamu menjelajah, lalu coba lagi.",
        "MENGEMAS GAMBAR", "GAMBAR %d DARI %d", "Gambar: %d (%s). Folder ART: %d.",
        "Hentikan? Paket yang belum selesai dihapus; folder ART tetap seperti adanya.",
        "Folder ART tetap seperti adanya: paket ini salinan.", "Kurang dari semenit", "ruang kosong tidak diketahui"],
    'Vietnamese': [
        "còn trống %s", "%sART/art.tar: đọc %s/s, %s", "%sART/art.tar: đọc %s/s, nhanh nhất, %s", "GÓI ART", "Khoảng %d phút",
        "Đang xem các thư mục ART: %d hình, %s",
        "Không ổ nào đã khởi động còn chỗ cho gói ART: cần khoảng %s. Hãy dọn chỗ trên ổ bạn duyệt rồi thử lại.",
        "ĐANG GÓI HÌNH", "HÌNH %d TRÊN %d", "Hình: %d (%s). Thư mục ART: %d.",
        "Dừng lại? Gói dở dang sẽ bị xóa; các thư mục ART giữ nguyên.",
        "Các thư mục ART giữ nguyên: gói chỉ là bản sao.", "Dưới một phút", "không rõ dung lượng trống"],
    'Filipino': [
        "%s bakante", "%sART/art.tar: bumabasa ng %s/s, %s", "%sART/art.tar: bumabasa ng %s/s, ang pinakamabilis, %s", "ART PACK", "Mga %d min",
        "Tinitingnan ang mga ART folder: %d larawan, %s",
        "Walang sinimulang drive na may puwang para sa ART Pack: kailangan nito ng mga %s. Magbakante ng puwang sa drive na binabrowse mo, saka subukan ulit.",
        "PINAPACK ANG MGA LARAWAN", "LARAWAN %d SA %d", "Mga larawan: %d (%s). Mga ART folder: %d.",
        "Ihinto? Tatanggalin ang hindi tapos na pack; mananatili ang mga ART folder.",
        "Mananatili ang mga ART folder: kopya lang ang pack.", "Wala pang isang minuto", "hindi alam ang bakanteng puwang"],
    'Japanese': [
        "空き %s", "%sART/art.tar：読み込み %s/s、%s", "%sART/art.tar：読み込み %s/s、最速、%s", "ART パック", "約 %d 分",
        "ART フォルダーを確認しています：画像 %d 枚、%s",
        "起動したドライブに ART パックを置く空きがありません：約 %s 必要です。ふだん閲覧するドライブの空きを増やしてから、もう一度どうぞ。",
        "画像をまとめています", "画像 %d / %d", "画像：%d 枚（%s）。ART フォルダー：%d 個。",
        "中止しますか？作りかけのパックは削除され、ART フォルダーはそのまま残ります。",
        "ART フォルダーはそのまま残ります：パックはコピーです。", "1 分以内", "空き容量は不明"],
    'Korean': [
        "%s 여유", "%sART/art.tar: 읽기 %s/s, %s", "%sART/art.tar: 읽기 %s/s, 가장 빠름, %s", "ART 팩", "약 %d분",
        "ART 폴더를 살펴보는 중: 이미지 %d개, %s",
        "시작된 드라이브에 ART 팩을 둘 공간이 없습니다: 약 %s이(가) 필요합니다. 평소 탐색하는 드라이브의 공간을 비운 뒤 다시 시도하세요.",
        "이미지를 모으는 중", "이미지 %d / %d", "이미지: %d개 (%s). ART 폴더: %d개.",
        "멈출까요? 만들다 만 팩은 삭제되고, ART 폴더는 그대로 남습니다.",
        "ART 폴더는 그대로 남습니다: 팩은 사본입니다.", "1분 이내", "여유 공간 알 수 없음"],
    'SChinese': [
        "剩余 %s", "%sART/art.tar：读取 %s/s，%s", "%sART/art.tar：读取 %s/s，最快，%s", "ART 包", "约 %d 分钟",
        "正在查看 ART 文件夹：%d 张图片，%s",
        "已启动的驱动器都没有空间放 ART 包：约需 %s。请在你平时浏览的驱动器上腾出空间，然后再试。",
        "正在打包图片", "图片 %d / %d", "图片：%d 张（%s）。ART 文件夹：%d 个。",
        "要停止吗？未完成的包会被删除；ART 文件夹保持原样。",
        "ART 文件夹保持原样：包只是副本。", "不到一分钟", "剩余空间未知"],
    'TChinese': [
        "剩餘 %s", "%sART/art.tar：讀取 %s/s，%s", "%sART/art.tar：讀取 %s/s，最快，%s", "ART 包", "約 %d 分鐘",
        "正在查看 ART 資料夾：%d 張圖片，%s",
        "已啟動的磁碟都沒有空間放 ART 包：約需 %s。請在你平常瀏覽的磁碟上騰出空間，然後再試。",
        "正在打包圖片", "圖片 %d / %d", "圖片：%d 張（%s）。ART 資料夾：%d 個。",
        "要停止嗎？未完成的包會被刪除；ART 資料夾保持原樣。",
        "ART 資料夾保持原樣：包只是副本。", "不到一分鐘", "剩餘空間未知"],
    'Arabic': [
        "%s متاحة", "%sART/art.tar: يقرأ %s/s، %s", "%sART/art.tar: يقرأ %s/s، الأسرع، %s", "حزمة ART", "نحو %d دقيقة",
        "جارٍ فحص مجلدات ART: %d صورة، %s",
        "لا يوجد محرك بدأ فيه متسع لحزمة ART: تحتاج إلى نحو %s. أفرغ مساحة على المحرك الذي تتصفح منه، ثم حاول من جديد.",
        "جارٍ حزم الصور", "الصورة %d من %d", "الصور: %d (%s). مجلدات ART: %d.",
        "إيقاف؟ تُزال الحزمة غير المكتملة؛ وتبقى مجلدات ART كما هي.",
        "تبقى مجلدات ART كما هي: الحزمة نسخة.", "أقل من دقيقة", "المساحة الفارغة غير معروفة"],
    'Persian': [
        "%s آزاد", "%sART/art.tar: خواندن %s/s، %s", "%sART/art.tar: خواندن %s/s، سریع‌ترین، %s", "بسته ART", "حدود %d دقیقه",
        "در حال بررسی پوشه‌های ART: %d تصویر، %s",
        "هیچ درایو راه‌اندازی‌شده‌ای برای بسته ART جا ندارد: حدود %s لازم است. روی درایوی که از آن مرور می‌کنی جا باز کن و دوباره امتحان کن.",
        "در حال بسته‌بندی تصاویر", "تصویر %d از %d", "تصاویر: %d (%s). پوشه‌های ART: %d.",
        "متوقف شود؟ بسته نیمه‌کاره حذف می‌شود؛ پوشه‌های ART همان‌طور که هستند می‌مانند.",
        "پوشه‌های ART همان‌طور که هستند می‌مانند: بسته یک رونوشت است.", "کمتر از یک دقیقه", "فضای آزاد نامعلوم"],
    'Laotian': [
        "ຫວ່າງ %s", "%sART/art.tar: ອ່ານ %s/s, %s", "%sART/art.tar: ອ່ານ %s/s, ໄວທີ່ສຸດ, %s", "ແພັກ ART", "ປະມານ %d ນາທີ",
        "ກຳລັງເບິ່ງໂຟນເດີ ART: ຮູບ %d ຮູບ, %s",
        "ບໍ່ມີໄດຣຟ໌ທີ່ເລີ່ມແລ້ວໃດມີບ່ອນສຳລັບແພັກ ART: ຕ້ອງການປະມານ %s. ເຮັດບ່ອນຫວ່າງໃນໄດຣຟ໌ທີ່ທ່ານເປີດເບິ່ງ ແລ້ວລອງໃໝ່.",
        "ກຳລັງລວມຮູບ", "ຮູບ %d ຈາກ %d", "ຮູບ: %d (%s). ໂຟນເດີ ART: %d.",
        "ຢຸດບໍ? ແພັກທີ່ຍັງບໍ່ສຳເລັດຈະຖືກລຶບ; ໂຟນເດີ ART ຄົງຢູ່ຄືເກົ່າ.",
        "ໂຟນເດີ ART ຄົງຢູ່ຄືເກົ່າ: ແພັກເປັນສຳເນົາ.", "ບໍ່ເຖິງໜຶ່ງນາທີ", "ບໍ່ຮູ້ບ່ອນຫວ່າງ"],
    'Cebuano': [
        "%s bakante", "%sART/art.tar: mobasa og %s/s, %s", "%sART/art.tar: mobasa og %s/s, ang pinakapaspas, %s", "ART PACK", "Mga %d min",
        "Gitan-aw ang mga ART folder: %d ka hulagway, %s",
        "Walay gisugdang drive nga adunay luna para sa ART Pack: kinahanglan niini og mga %s. Pagbakante og luna sa drive nga imong gi-browse, unya sulayi pag-usab.",
        "GI-PACK ANG MGA HULAGWAY", "HULAGWAY %d SA %d", "Mga hulagway: %d (%s). Mga ART folder: %d.",
        "Hunongon? Tangtangon ang wala mahuman nga pack; magpabilin ang mga ART folder.",
        "Magpabilin ang mga ART folder: kopya lang ang pack.", "Ubos sa usa ka minuto", "wala mahibal-an ang bakanteng luna"],
}

os.makedirs(OUT, exist_ok=True)
for lang, strings in T.items():
    assert len(strings) == 14, (lang, len(strings))
    json.dump({'s': {str(i): v for i, v in enumerate(strings)}, 'l': {}}, open(os.path.join(OUT, lang + '.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
print('wrote', len(T), 'languages')
