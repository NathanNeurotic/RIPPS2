"""Build 118 strings (s118.json) and labels: Japanese, Korean, SChinese, TChinese, Arabic, Persian, Laotian, Cebuano.
Run from the repo root: python tools/lang118/batch4.py (writes tr118/<Language>.json)."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'tr118')

T = {}

T['Japanese'] = [
    "%d 枚の画像（%d 個の ART フォルダーから）を 1 つのファイル %s にまとめます。ART フォルダーはそのまま残ります：パックはコピーです。art.tar は Memory Files で別のドライブの ART フォルダーにコピーできますが、ふだん閲覧するドライブで作るのがいちばん速いので、最速のドライブを先頭に出しています。今すぐ作りますか？",
    "%sART/art.tar：画像 %d 枚、読み込み %d KB/s",
    "%sART/art.tar：画像 %d 枚、読み込み %d KB/s、最速",
    "使用中：%s、画像 %d 枚、%d MB",
    "起動したドライブの ART フォルダーを確認しています",
    "各ドライブが画像を読む速さを測っています：%s",
    "なし：画像はそれぞれの ART フォルダーから読み込みます。",
    "画像を %s にまとめています：%d / %d 枚、%d MB。戻るボタンで中止します。",
    "%s のパックを削除（ART フォルダーはそのまま残ります）",
    "%s の ART パックを削除しますか？ART フォルダーはそのまま残ります。",
    "中止しました。作りかけのパックは削除され、画像はこれまでどおり ART フォルダーから読み込みます。",
    "ART パックを %s に書き込めませんでした（そのドライブに空きはありますか？）。ほかは何も変わっていません：画像はこれまでどおり ART フォルダーから読み込みます。",
    "%s の ART パックを削除しました。画像は再び ART フォルダーから読み込みます。",
    "ART パックができました：画像 %d 枚、%d MB、%s（%d 秒）。これからは画像をパックから読み込み、作成の対象になった %d 本のゲームは ART フォルダーに 1 枚ずつ問い合わせることがなくなります。RIPPS2 が取得・撮影した画像はすぐに表示されます。PC からコピーした画像は、パックを作り直すと表示されます。",
    "起動したドライブに画像のある ART フォルダーがありません。画像のあるドライブを起動してから（そのページで SELECT）、もう一度どうぞ。",
]
T['Japanese_l'] = {
    'RIPPS2_ART_PACK': "ART パック",
    'RIPPS2_ART_PACK_BUILD': "作成または削除",
    'HINT_RIPPS2_ART_PACK': "起動したすべてのドライブの ART フォルダーを、選んだドライブの art.tar 1 つにまとめます（最速のドライブを先に提案します）。カバーは 1 つのファイルから 1 つの索引で読み込まれ、ゲームごとの検索は一切ないので、メニューも音楽もなめらかです。ART フォルダーはそのまま残ります。",
}

T['Korean'] = [
    "이미지 %d개(ART 폴더 %d개에서)가 하나의 파일 %s에 들어갑니다. ART 폴더는 그대로 남습니다: 팩은 사본입니다. Memory Files로 art.tar를 다른 드라이브의 ART 폴더에 복사할 수도 있지만, 평소 탐색하는 드라이브에서 만드는 것이 가장 빠르므로 가장 빠른 드라이브가 맨 위에 있습니다. 지금 만들까요?",
    "%sART/art.tar: 이미지 %d개, 읽기 %d KB/s",
    "%sART/art.tar: 이미지 %d개, 읽기 %d KB/s, 가장 빠름",
    "사용 중: %s, 이미지 %d개, %d MB",
    "시작된 드라이브의 ART 폴더를 살펴보는 중",
    "각 드라이브가 이미지를 읽는 속도를 재는 중: %s",
    "없음: 각 이미지는 자기 ART 폴더에서 읽습니다.",
    "이미지를 %s에 모으는 중: %d / %d개, %d MB. 뒤로 버튼을 누르면 멈춥니다.",
    "%s의 팩 삭제 (ART 폴더는 그대로 남습니다)",
    "%s의 ART 팩을 삭제할까요? ART 폴더는 그대로 남습니다.",
    "멈췄습니다. 만들다 만 팩은 삭제되었고, 이미지는 전처럼 ART 폴더에서 읽습니다.",
    "ART 팩을 %s에 쓸 수 없었습니다(그 드라이브에 공간이 있나요?). 그 밖에는 바뀐 것이 없습니다: 이미지는 전처럼 ART 폴더에서 읽습니다.",
    "%s의 ART 팩을 삭제했습니다. 이미지는 다시 ART 폴더에서 읽습니다.",
    "ART 팩이 완성되었습니다: 이미지 %d개, %d MB, %s (%d초). 이제부터 이미지는 팩에서 읽으며, 팩이 만들어진 대상인 게임 %d개는 ART 폴더에 이미지를 하나씩 묻지 않습니다. RIPPS2가 받아 오거나 찍은 이미지는 바로 나타나고, PC에서 복사해 넣은 이미지는 팩을 다시 만들면 나타납니다.",
    "시작된 드라이브에 이미지가 있는 ART 폴더가 없습니다. 이미지가 있는 드라이브를 시작한 뒤(해당 페이지에서 SELECT) 다시 오세요.",
]
T['Korean_l'] = {
    'RIPPS2_ART_PACK': "ART 팩",
    'RIPPS2_ART_PACK_BUILD': "만들기 또는 삭제",
    'HINT_RIPPS2_ART_PACK': "시작된 모든 드라이브의 ART 폴더를 고른 드라이브의 art.tar 하나로 묶습니다(가장 빠른 드라이브를 먼저 제안). 커버는 하나의 파일에서 하나의 색인으로 읽히고 게임마다 찾는 일이 없어서 메뉴와 음악이 매끄럽습니다. ART 폴더는 그대로 남습니다.",
}

T['SChinese'] = [
    "%d 张图片（来自 %d 个 ART 文件夹）将放进一个文件 %s。ART 文件夹保持原样：包只是副本。你可以用 Memory Files 把 art.tar 复制到其他驱动器的 ART 文件夹，但在你平时浏览的驱动器上生成最快，所以最快的驱动器排在最前。现在生成吗？",
    "%sART/art.tar：%d 张图片，读取 %d KB/s",
    "%sART/art.tar：%d 张图片，读取 %d KB/s，最快",
    "使用中：%s，%d 张图片，%d MB",
    "正在查看已启动驱动器上的 ART 文件夹",
    "正在测量每个驱动器读取图片的速度：%s",
    "无：每张图片都从它自己的 ART 文件夹读取。",
    "正在把图片打包到 %s：%d / %d 张，%d MB。按返回键停止。",
    "删除 %s 中的包（ART 文件夹保持原样）",
    "删除 %s 中的 ART 包吗？ART 文件夹保持原样。",
    "已停止。未完成的包已删除，图片照旧从 ART 文件夹读取。",
    "无法把 ART 包写入 %s（该驱动器还有空间吗？）。其他没有任何变化：图片照旧从 ART 文件夹读取。",
    "%s 中的 ART 包已删除。图片重新从 ART 文件夹读取。",
    "ART 包已生成：%d 张图片，%d MB，位于 %s（%d 秒）。今后图片从包中读取，它所针对的 %d 款游戏再也不会逐张查询各自的 ART 文件夹。RIPPS2 下载或拍下的图片会立即显示；从电脑复制进去的图片在重新生成包后显示。",
    "已启动的驱动器上没有含图片的 ART 文件夹。请先启动存放图片的驱动器（在其页面按 SELECT），然后再回来。",
]
T['SChinese_l'] = {
    'RIPPS2_ART_PACK': "ART 包",
    'RIPPS2_ART_PACK_BUILD': "生成或删除",
    'HINT_RIPPS2_ART_PACK': "把每个已启动驱动器的 ART 文件夹打包成你所选驱动器上的一个 art.tar（最快的驱动器优先推荐）。封面随后从一个文件凭一个索引读取，不再逐个游戏查找，菜单和音乐都保持流畅。ART 文件夹保持原样。",
}

T['TChinese'] = [
    "%d 張圖片（來自 %d 個 ART 資料夾）將放進一個檔案 %s。ART 資料夾保持原樣：包只是副本。你可以用 Memory Files 把 art.tar 複製到其他磁碟的 ART 資料夾，但在你平常瀏覽的磁碟上建立最快，所以最快的磁碟排在最前面。現在建立嗎？",
    "%sART/art.tar：%d 張圖片，讀取 %d KB/s",
    "%sART/art.tar：%d 張圖片，讀取 %d KB/s，最快",
    "使用中：%s，%d 張圖片，%d MB",
    "正在查看已啟動磁碟上的 ART 資料夾",
    "正在測量每個磁碟讀取圖片的速度：%s",
    "無：每張圖片都從它自己的 ART 資料夾讀取。",
    "正在把圖片打包到 %s：%d / %d 張，%d MB。按返回鍵停止。",
    "刪除 %s 中的包（ART 資料夾保持原樣）",
    "要刪除 %s 中的 ART 包嗎？ART 資料夾保持原樣。",
    "已停止。未完成的包已刪除，圖片照舊從 ART 資料夾讀取。",
    "無法把 ART 包寫入 %s（該磁碟還有空間嗎？）。其他沒有任何改變：圖片照舊從 ART 資料夾讀取。",
    "%s 中的 ART 包已刪除。圖片重新從 ART 資料夾讀取。",
    "ART 包已建立：%d 張圖片，%d MB，位於 %s（%d 秒）。今後圖片從包中讀取，它所對應的 %d 款遊戲再也不會逐張查詢各自的 ART 資料夾。RIPPS2 下載或拍下的圖片會立即顯示；從電腦複製進去的圖片在重新建立包之後顯示。",
    "已啟動的磁碟上沒有含圖片的 ART 資料夾。請先啟動存放圖片的磁碟（在其頁面按 SELECT），然後再回來。",
]
T['TChinese_l'] = {
    'RIPPS2_ART_PACK': "ART 包",
    'RIPPS2_ART_PACK_BUILD': "建立或刪除",
    'HINT_RIPPS2_ART_PACK': "把每個已啟動磁碟的 ART 資料夾打包成你所選磁碟上的一個 art.tar（最快的磁碟優先推薦）。封面隨後從一個檔案憑一個索引讀取，不再逐個遊戲查找，選單和音樂都保持流暢。ART 資料夾保持原樣。",
}

T['Arabic'] = [
    "%d صورة من %d مجلد ART تدخل في ملف واحد، %s. تبقى مجلدات ART كما هي: الحزمة نسخة. يمكنك نسخ art.tar إلى مجلد ART في محرك آخر بواسطة Memory Files، لكن بناءها على المحرك الذي تتصفح منه هو الأسرع، لذلك يأتي أسرع محرك أولًا. هل تبنيها الآن؟",
    "%sART/art.tar: %d صورة هناك، يقرأ %d KB/s",
    "%sART/art.tar: %d صورة هناك، يقرأ %d KB/s، الأسرع",
    "قيد الاستخدام: %s، %d صورة، %d MB",
    "جارٍ فحص مجلدات ART على المحركات التي بدأت",
    "جارٍ قياس سرعة قراءة كل محرك لصوره: %s",
    "لا شيء: تُقرأ كل صورة من مجلد ART الخاص بها.",
    "جارٍ حزم الصور في %s: %d من %d صورة، %d MB. اضغط زر الرجوع للإيقاف.",
    "إزالة الحزمة في %s (تبقى مجلدات ART كما هي)",
    "إزالة حزمة ART في %s؟ تبقى مجلدات ART كما هي.",
    "توقّف. أُزيلت الحزمة غير المكتملة، وتُحمَّل الصور من مجلدات ART كما كانت.",
    "تعذّرت كتابة حزمة ART في %s (هل توجد مساحة على ذلك المحرك؟). لم يتغير شيء آخر: تُحمَّل الصور من مجلدات ART كما كانت.",
    "أُزيلت حزمة ART في %s. تُحمَّل الصور من مجلدات ART من جديد.",
    "حزمة ART جاهزة: %d صورة، %d MB، في %s (%d ث). من الآن تُحمَّل الصور منها، والألعاب الـ %d التي بُنيت لها لن يُسأل مجلد ART الخاص بها صورةً صورةً أبدًا. الصور التي يجلبها RIPPS2 أو يلتقطها تظهر فورًا؛ والتي تنسخها من حاسوب تظهر بعد أن تبني الحزمة من جديد.",
    "لا يوجد مجلد ART فيه صور على المحركات التي بدأت. ابدأ المحركات التي عليها صورك (SELECT في صفحتها)، ثم عُد.",
]
T['Arabic_l'] = {
    'RIPPS2_ART_PACK': "حزمة ART",
    'RIPPS2_ART_PACK_BUILD': "بناء أو إزالة",
    'HINT_RIPPS2_ART_PACK': "يحزم مجلد ART لكل محرك بدأ في ملف art.tar واحد على المحرك الذي تختاره (يُعرض الأسرع أولًا). تُحمَّل الأغلفة بعدها من ملف واحد بفهرس واحد، دون بحث لكل لعبة، فتبقى القوائم والموسيقى سلسة. تبقى مجلدات ART كما هي.",
}

T['Persian'] = [
    "%d تصویر از %d پوشه ART در یک فایل قرار می‌گیرد، %s. پوشه‌های ART همان‌طور که هستند می‌مانند: بسته یک رونوشت است. می‌توانی art.tar را با Memory Files در پوشه ART درایو دیگری کپی کنی، اما ساختن آن روی درایوی که از آن مرور می‌کنی سریع‌تر است، برای همین سریع‌ترین درایو اول می‌آید. اکنون ساخته شود؟",
    "%sART/art.tar: %d تصویر آنجا، خواندن %d KB/s",
    "%sART/art.tar: %d تصویر آنجا، خواندن %d KB/s، سریع‌ترین",
    "در حال استفاده: %s، %d تصویر، %d MB",
    "در حال بررسی پوشه‌های ART روی درایوهای راه‌اندازی‌شده",
    "در حال سنجش سرعت خواندن تصاویر هر درایو: %s",
    "هیچ: هر تصویر از پوشه ART خودش خوانده می‌شود.",
    "در حال بسته‌بندی تصاویر در %s: %d از %d تصویر، %d MB. برای توقف دکمه بازگشت را بزن.",
    "حذف بسته در %s (پوشه‌های ART همان‌طور که هستند می‌مانند)",
    "بسته ART در %s حذف شود؟ پوشه‌های ART همان‌طور که هستند می‌مانند.",
    "متوقف شد. بسته نیمه‌کاره حذف شد و تصاویر مثل قبل از پوشه‌های ART بارگذاری می‌شوند.",
    "بسته ART در %s نوشته نشد (روی آن درایو جا هست؟). چیز دیگری تغییر نکرد: تصاویر مثل قبل از پوشه‌های ART بارگذاری می‌شوند.",
    "بسته ART در %s حذف شد. تصاویر دوباره از پوشه‌های ART بارگذاری می‌شوند.",
    "بسته ART آماده است: %d تصویر، %d MB، در %s (%d ثانیه). از این پس تصاویر از آن بارگذاری می‌شوند و از پوشه ART آن %d بازی که بسته برایشان ساخته شده دیگر هرگز تصویر به تصویر پرسیده نمی‌شود. تصاویری که RIPPS2 دریافت می‌کند یا می‌گیرد فوراً نمایش داده می‌شوند؛ تصاویری که از رایانه کپی می‌کنی پس از ساختن دوباره بسته نمایش داده می‌شوند.",
    "روی درایوهای راه‌اندازی‌شده هیچ پوشه ART تصویرداری نیست. درایوهایی را که تصاویرت روی آن‌هاست راه‌اندازی کن (SELECT در صفحه‌شان) و بعد برگرد.",
]
T['Persian_l'] = {
    'RIPPS2_ART_PACK': "بسته ART",
    'RIPPS2_ART_PACK_BUILD': "ساختن یا حذف",
    'HINT_RIPPS2_ART_PACK': "پوشه ART هر درایو راه‌اندازی‌شده را در یک art.tar روی درایوی که انتخاب می‌کنی بسته‌بندی می‌کند (سریع‌ترین اول پیشنهاد می‌شود). جلدها سپس از یک فایل با یک فهرست بارگذاری می‌شوند، هرگز با جست‌وجو برای هر بازی، تا منوها و موسیقی روان بمانند. پوشه‌های ART همان‌طور که هستند می‌مانند.",
}

T['Laotian'] = [
    "ຮູບ %d ຮູບ ຈາກໂຟນເດີ ART %d ໂຟນເດີ ຈະເຂົ້າໄປໃນໄຟລ໌ດຽວ, %s. ໂຟນເດີ ART ຄົງຢູ່ຄືເກົ່າ: ແພັກເປັນສຳເນົາ. ທ່ານສາມາດສຳເນົາ art.tar ໄປໃສ່ໂຟນເດີ ART ຂອງໄດຣຟ໌ອື່ນດ້ວຍ Memory Files, ແຕ່ການສ້າງມັນໃນໄດຣຟ໌ທີ່ທ່ານເປີດເບິ່ງແມ່ນໄວທີ່ສຸດ, ສະນັ້ນໄດຣຟ໌ທີ່ໄວທີ່ສຸດຈຶ່ງຢູ່ກ່ອນ. ສ້າງດຽວນີ້ບໍ?",
    "%sART/art.tar: ມີຮູບ %d ຮູບ, ອ່ານ %d KB/s",
    "%sART/art.tar: ມີຮູບ %d ຮູບ, ອ່ານ %d KB/s, ໄວທີ່ສຸດ",
    "ກຳລັງໃຊ້: %s, ຮູບ %d ຮູບ, %d MB",
    "ກຳລັງເບິ່ງໂຟນເດີ ART ໃນໄດຣຟ໌ທີ່ເລີ່ມແລ້ວ",
    "ກຳລັງວັດແທກວ່າແຕ່ລະໄດຣຟ໌ອ່ານຮູບຂອງມັນໄວປານໃດ: %s",
    "ບໍ່ມີ: ແຕ່ລະຮູບຖືກອ່ານຈາກໂຟນເດີ ART ຂອງມັນເອງ.",
    "ກຳລັງລວມຮູບເຂົ້າໃນ %s: %d ຈາກ %d ຮູບ, %d MB. ກົດປຸ່ມກັບຄືນເພື່ອຢຸດ.",
    "ລຶບແພັກໃນ %s (ໂຟນເດີ ART ຄົງຢູ່ຄືເກົ່າ)",
    "ລຶບແພັກ ART ໃນ %s ບໍ? ໂຟນເດີ ART ຄົງຢູ່ຄືເກົ່າ.",
    "ຢຸດແລ້ວ. ແພັກທີ່ຍັງບໍ່ສຳເລັດຖືກລຶບແລ້ວ, ແລະຮູບຖືກໂຫຼດຈາກໂຟນເດີ ART ຄືເກົ່າ.",
    "ບໍ່ສາມາດຂຽນແພັກ ART ລົງ %s ໄດ້ (ໄດຣຟ໌ນັ້ນມີບ່ອນຫວ່າງບໍ?). ບໍ່ມີຫຍັງອື່ນປ່ຽນ: ຮູບຖືກໂຫຼດຈາກໂຟນເດີ ART ຄືເກົ່າ.",
    "ແພັກ ART ໃນ %s ຖືກລຶບແລ້ວ. ຮູບຖືກໂຫຼດຈາກໂຟນເດີ ART ອີກຄັ້ງ.",
    "ແພັກ ART ສ້າງແລ້ວ: ຮູບ %d ຮູບ, %d MB, ໃນ %s (%d ວິນາທີ). ຕໍ່ຈາກນີ້ຮູບຖືກໂຫຼດຈາກມັນ, ແລະເກມ %d ເກມທີ່ມັນຖືກສ້າງໃຫ້ ຈະບໍ່ຖືກຖາມໂຟນເດີ ART ຂອງມັນເທື່ອລະຮູບອີກເລີຍ. ຮູບທີ່ RIPPS2 ດຶງມາ ຫຼື ຖ່າຍ ຈະສະແດງທັນທີ; ຮູບທີ່ທ່ານສຳເນົາມາຈາກຄອມພິວເຕີ ຈະສະແດງເມື່ອທ່ານສ້າງແພັກໃໝ່.",
    "ບໍ່ມີໂຟນເດີ ART ທີ່ມີຮູບໃນໄດຣຟ໌ທີ່ເລີ່ມແລ້ວ. ເລີ່ມໄດຣຟ໌ທີ່ມີຮູບຂອງທ່ານກ່ອນ (SELECT ໃນໜ້າຂອງມັນ), ແລ້ວກັບມາ.",
]
T['Laotian_l'] = {
    'RIPPS2_ART_PACK': "ແພັກ ART",
    'RIPPS2_ART_PACK_BUILD': "ສ້າງ ຫຼື ລຶບ",
    'HINT_RIPPS2_ART_PACK': "ລວມໂຟນເດີ ART ຂອງທຸກໄດຣຟ໌ທີ່ເລີ່ມແລ້ວ ເຂົ້າເປັນ art.tar ດຽວໃນໄດຣຟ໌ທີ່ທ່ານເລືອກ (ໄດຣຟ໌ທີ່ໄວທີ່ສຸດຖືກສະເໜີກ່ອນ). ໜ້າປົກຈະຖືກໂຫຼດຈາກໄຟລ໌ດຽວດ້ວຍດັດຊະນີດຽວ, ບໍ່ເຄີຍຊອກຫາເທື່ອລະເກມ, ສະນັ້ນເມນູ ແລະ ເພງຈຶ່ງລື່ນໄຫຼ. ໂຟນເດີ ART ຄົງຢູ່ຄືເກົ່າ.",
}

T['Cebuano'] = [
    "%d ka hulagway gikan sa %d ka ART folder ang mosulod sa usa ka file, %s. Magpabilin ang mga ART folder: kopya lang ang pack. Mahimo nimong kopyahon ang art.tar ngadto sa ART folder sa laing drive gamit ang Memory Files, apan pinakapaspas kung buhaton kini sa drive nga imong gi-browse, mao nga una ang pinakapaspas nga drive. Buhaton na karon?",
    "%sART/art.tar: %d ka hulagway didto, mobasa og %d KB/s",
    "%sART/art.tar: %d ka hulagway didto, mobasa og %d KB/s, ang pinakapaspas",
    "Gigamit: %s, %d ka hulagway, %d MB",
    "Gitan-aw ang mga ART folder sa mga gisugdang drive",
    "Gisukod kung unsa kapaspas mobasa ang matag drive sa iyang mga hulagway: %s",
    "Wala: ang matag hulagway basahon gikan sa kaugalingon niining ART folder.",
    "Gi-pack ang mga hulagway ngadto sa %s: %d sa %d ka hulagway, %d MB. Pindota ang back button aron mohunong.",
    "TANGTANGA ang pack sa %s (magpabilin ang mga ART folder)",
    "Tangtangon ang ART Pack sa %s? Magpabilin ang mga ART folder.",
    "Gihunong. Gitangtang ang wala mahuman nga pack, ug ang mga hulagway gikan gihapon sa mga ART folder sama kaniadto.",
    "Dili masulat ang ART Pack sa %s (naa bay luna sa maong drive?). Wala nay laing nausab: ang mga hulagway gikan gihapon sa mga ART folder sama kaniadto.",
    "Natangtang na ang ART Pack sa %s. Ang mga hulagway gikan na usab sa mga ART folder.",
    "Nahuman na ang ART Pack: %d ka hulagway, %d MB, sa %s (%d s). Sukad karon gikan na niini ang mga hulagway, ug ang %d ka dula nga gibuhatan niini dili na pangutan-on sa ilang ART folder sa matag hulagway. Ang mga hulagway nga gikuha o gi-shoot sa RIPPS2 makita dayon; ang imong gikopya gikan sa PC makita kung buhaton nimo pag-usab ang pack.",
    "Walay ART folder nga adunay mga hulagway sa mga gisugdang drive. Sugdi ang mga drive nga naa ang imong mga hulagway (SELECT sa ilang page), unya balik.",
]
T['Cebuano_l'] = {
    'RIPPS2_ART_PACK': "ART Pack",
    'RIPPS2_ART_PACK_BUILD': "Buhata o tangtanga",
    'HINT_RIPPS2_ART_PACK': "Giputos ang ART folder sa matag gisugdang drive ngadto sa usa ka art.tar sa drive nga imong pilion (unang gitanyag ang pinakapaspas). Ang mga cover makuha na gikan sa usa ka file nga adunay usa ka index, dili gyud pinaagi sa pagpangita sa matag dula, mao nga hapsay ang mga menu ug musika. Magpabilin ang mga ART folder.",
}

os.makedirs(OUT, exist_ok=True)
for lang in [k for k in T if not k.endswith('_l')]:
    s = {str(i): v for i, v in enumerate(T[lang])}
    json.dump({'s': s, 'l': T[lang + '_l']}, open(os.path.join(OUT, lang + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('wrote', lang)
