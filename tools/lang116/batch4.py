"""Build 116 strings (s116.json) and labels: Japanese, Korean, SChinese, TChinese, Arabic, Persian, Laotian, Cebuano.
Run from the repo root: python tools/lang116/batch4.py (writes tr116/<Language>.json)."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'tr116')

T = {}

T['Japanese'] = [
    " （見つかった設定を変更しました：%s。）",
    " その設定をそれ自身の設定ツールで一度保存してから、BOOT LOCK をもう一度オンにしてください。",
    "%s は RIPPS2 を今ある場所（%s）から起動できません。RIPPS2 は自分をコピーしません。RIPPS2.ELF をメモリーカードか USB ドライブに置いて、そこから起動してください。",
    "BOOT LOCK はブートローダーの設定を書き込めませんでした。メモリーカードやドライブが書き込み禁止になっていないか確認して、もう一度お試しください。",
    "BOOT LOCK は変更できるブートローダーの設定を見つけられませんでした。",
    "BOOT LOCK はオフです。ブートローダーは以前に起動していたもの（%s）を起動します。",
    "BOOT LOCK はオンです。%s は電源投入時に RIPPS2 を起動します（%s）。IGRパスが空なら、ゲームの EXIT も同じ道で戻ります。ほかのものに行くには、本体の起動中にそのボタンのどれかを押し続けてください。%s",
    "BOOT LOCK は OSDMenu のメニューの先頭に RIPPS2 を置きました（%s）。OSDMenu は自分では何も起動しません。そこで RIPPS2 を選んでください。ゲームの EXIT はそのメニューに戻ります。RIPPS2 をすぐに起動する本体にするには、BIBLE が PS2BBL 1.2.0 をメモリーカードに入れます（ブートローダー）。",
    "BOOT LOCK はメモリーカード上のブートローダー（PS2BBL、FMCB、OSDMenu）を通じて動作しますが、ここには一つもありません。",
    "スロット %d のメモリーカードは電源投入時に %s を起動しますが、BOOT LOCK が変更できるその設定は見つかりませんでした（%s を探します）。",
    "スロット %d のメモリーカードは電源投入時に %s を起動しますが、BOOT LOCK はこれを設定できません。BOOT LOCK は PS2BBL、FMCB、OSDMenu を通じて動作します。",
    "この本体には RIPPS2 のロック付きのブートローダーがあります。",
    "ゲームの EXIT：ブラウザー、次にブートローダー（BOOT LOCK）",
]
T['Japanese_l'] = {
    'HINT_EXITPATH': "ゲーム内メニューの EXIT の行き先。BOOT LOCK をオンにして（PS2BBL、FMCB、OSDMenu、または BIBLE を設定済み）空のままにするのがおすすめです。EXIT はブラウザーを通り、ブラウザーが電源投入時と同じようにブートローダーと RIPPS2 を起動します。最も安全な戻り方です。ロックなしで空のとき：メモリーカードや FAT32 の USB ドライブにある RIPPS2 自身の ELF をリセット直後に読み込みますが、すべてのゲームが本体をその準備ができた状態にするとは限りません。Browser：PS2 のブラウザー。そのとき MMCE 上の ELF には一切アクセスできません。",
    'HINT_RIPPS2_BOOT_LOCK': "電源投入時にブートローダーを通じて RIPPS2 を起動します。PS2BBL と FMCB はすぐに起動し、OSDMenu はメニューの先頭に置きます。ゲームの EXIT も同じ道で戻ります。オフにすると以前の状態に戻します。まだない？「ブートローダー」で BIBLE をインストールできます。",
}

T['Korean'] = [
    " (찾은 설정을 변경했습니다: %s.)",
    " 그 설정을 자체 설정 도구로 한 번 저장한 다음 BOOT LOCK을 다시 켜세요.",
    "%s은(는) 지금 있는 곳(%s)에서 RIPPS2를 시작할 수 없으며, RIPPS2는 자신을 복사하지 않습니다. RIPPS2.ELF를 메모리 카드나 USB 드라이브에 두고 거기서 시작하세요.",
    "BOOT LOCK이 부트 로더의 설정을 쓰지 못했습니다. 메모리 카드나 드라이브가 쓰기 보호되어 있지 않은지 확인한 뒤 다시 시도하세요.",
    "BOOT LOCK이 바꿀 부트 로더 설정을 찾지 못했습니다.",
    "BOOT LOCK이 꺼져 있습니다. 부트 로더는 이전에 시작하던 것(%s)을 시작합니다.",
    "BOOT LOCK이 켜져 있습니다. 이제 %s은(는) 전원을 켤 때 RIPPS2를 시작하며 (%s), IGR 경로가 비어 있으면 게임의 EXIT도 같은 길로 돌아옵니다. 다른 것으로 가려면 본체가 시작될 때 그 버튼 중 하나를 누르고 있으세요.%s",
    "BOOT LOCK이 RIPPS2를 OSDMenu 메뉴의 맨 위에 두었습니다 (%s). OSDMenu는 스스로 아무것도 시작하지 않으니 거기서 RIPPS2를 고르세요. 게임의 EXIT는 그 메뉴로 돌아옵니다. RIPPS2를 바로 시작하는 본체가 되려면 BIBLE이 PS2BBL 1.2.0을 메모리 카드에 넣습니다(부트 로더).",
    "BOOT LOCK은 메모리 카드의 부트 로더(PS2BBL, FMCB 또는 OSDMenu)를 통해 작동하는데, 여기에는 하나도 없습니다.",
    "슬롯 %d의 메모리 카드는 전원을 켤 때 %s을(를) 시작하는데, BOOT LOCK이 바꿀 그 설정을 찾지 못했습니다(%s을(를) 찾습니다).",
    "슬롯 %d의 메모리 카드는 전원을 켤 때 %s을(를) 시작하는데, BOOT LOCK은 이를 설정할 수 없습니다. BOOT LOCK은 PS2BBL, FMCB, OSDMenu를 통해 작동합니다.",
    "이 본체에는 RIPPS2 잠금이 있는 부트 로더가 있습니다.",
    "게임의 EXIT: 브라우저, 그다음 부트 로더 (BOOT LOCK)",
]
T['Korean_l'] = {
    'HINT_EXITPATH': "게임 내 메뉴의 EXIT가 가는 곳. BOOT LOCK을 켜고(PS2BBL, FMCB 또는 OSDMenu, 또는 BIBLE 설정) 비워 두는 것이 가장 좋습니다. 그러면 EXIT는 브라우저를 거치고, 브라우저가 전원을 켤 때처럼 부트 로더와 RIPPS2를 시작합니다. 가장 안전한 복귀입니다. 잠금 없이 비우면: 메모리 카드나 FAT32 USB 드라이브에 있는 RIPPS2 자체 ELF를 리셋 직후 불러오는데, 모든 게임이 본체를 그에 맞게 두지는 않습니다. Browser: PS2 브라우저. 그때 MMCE의 ELF에는 전혀 접근할 수 없습니다.",
    'HINT_RIPPS2_BOOT_LOCK': "전원을 켤 때 부트 로더를 통해 RIPPS2를 시작합니다. PS2BBL과 FMCB는 바로 시작하고, OSDMenu는 메뉴 맨 위에 둡니다. 게임의 EXIT도 같은 길로 돌아옵니다. 끄면 이전 상태로 되돌립니다. 아직 없나요? 부트 로더에서 BIBLE을 설치하세요.",
}

T['SChinese'] = [
    " （找到的配置已设置：%s。）",
    " 请先用它自己的配置工具保存一次设置，然后再打开 BOOT LOCK。",
    "%s 无法从 RIPPS2 现在所在的位置（%s）启动它，而 RIPPS2 不会复制自己。请把 RIPPS2.ELF 放到记忆卡或 USB 驱动器上，再从那里启动。",
    "BOOT LOCK 无法写入引导程序的配置。请检查记忆卡或驱动器没有写保护，然后重试。",
    "BOOT LOCK 没有找到可更改的引导程序配置。",
    "BOOT LOCK 已关闭。你的引导程序会启动它以前启动的内容（%s）。",
    "BOOT LOCK 已开启。%s 现在开机时启动 RIPPS2（%s），IGR路径留空时，游戏的 EXIT 也会沿同一条路返回。主机启动时按住它的任一按键可以进入其他内容。%s",
    "BOOT LOCK 已把 RIPPS2 放在 OSDMenu 菜单的第一项（%s）。OSDMenu 自己不会启动任何东西：请在那里选择 RIPPS2，游戏的 EXIT 会回到那个菜单。若要主机开机直接启动 RIPPS2，BIBLE 会把 PS2BBL 1.2.0 装到记忆卡上（引导程序）。",
    "BOOT LOCK 通过记忆卡上的引导程序工作（PS2BBL、FMCB 或 OSDMenu），而这里一个也没有。",
    "插槽 %d 的记忆卡开机时启动 %s，但 BOOT LOCK 没有找到它可更改的配置（它查找 %s）。",
    "插槽 %d 的记忆卡开机时启动 %s，BOOT LOCK 无法设置它：BOOT LOCK 通过 PS2BBL、FMCB 和 OSDMenu 工作。",
    "这台主机上有带 RIPPS2 锁定的引导程序。",
    "游戏的 EXIT：浏览器，然后是你的引导程序（BOOT LOCK）",
]
T['SChinese_l'] = {
    'HINT_EXITPATH': "游戏内菜单中 EXIT 去哪里。最好在 BOOT LOCK 开启时留空（PS2BBL、FMCB 或 OSDMenu，或已设置好 BIBLE）：EXIT 会经过浏览器，浏览器像开机时一样启动你的引导程序和 RIPPS2，这是最安全的返回方式。未锁定时留空：记忆卡或 FAT32 USB 驱动器上 RIPPS2 自己的 ELF 会在重置后立即加载，但并非每个游戏都会让主机为此做好准备。Browser：PS2 浏览器。那时完全无法访问 MMCE 上的 ELF。",
    'HINT_RIPPS2_BOOT_LOCK': "开机时通过你的引导程序启动 RIPPS2：PS2BBL 和 FMCB 会立即启动它，OSDMenu 会把它放在菜单第一项，游戏的 EXIT 也沿同一条路返回。关闭会恢复以前的内容。还没有？“引导程序”会安装 BIBLE。",
}

T['TChinese'] = [
    " （找到的設定已設好：%s。）",
    " 請先用它自己的設定工具儲存一次設定，再開啟 BOOT LOCK。",
    "%s 無法從 RIPPS2 現在所在的位置（%s）啟動它，而 RIPPS2 不會複製自己。請把 RIPPS2.ELF 放到記憶卡或 USB 磁碟機上，再從那裡啟動。",
    "BOOT LOCK 無法寫入開機程式的設定。請確認記憶卡或磁碟機沒有防寫，然後再試一次。",
    "BOOT LOCK 找不到可變更的開機程式設定。",
    "BOOT LOCK 已關閉。你的開機程式會啟動它以前啟動的內容（%s）。",
    "BOOT LOCK 已開啟。%s 現在開機時啟動 RIPPS2（%s），IGR 位置留空時，遊戲的 EXIT 也會沿同一條路返回。主機啟動時按住它的任一按鍵可進入其他內容。%s",
    "BOOT LOCK 已把 RIPPS2 放在 OSDMenu 選單的第一項（%s）。OSDMenu 自己不會啟動任何東西：請在那裡選擇 RIPPS2，遊戲的 EXIT 會回到那個選單。若要主機開機直接啟動 RIPPS2，BIBLE 會把 PS2BBL 1.2.0 裝到記憶卡上（開機程式）。",
    "BOOT LOCK 透過記憶卡上的開機程式運作（PS2BBL、FMCB 或 OSDMenu），而這裡一個也沒有。",
    "插槽 %d 的記憶卡開機時啟動 %s，但 BOOT LOCK 找不到它可變更的設定（它會尋找 %s）。",
    "插槽 %d 的記憶卡開機時啟動 %s，BOOT LOCK 無法設定它：BOOT LOCK 透過 PS2BBL、FMCB 和 OSDMenu 運作。",
    "這台主機上有帶 RIPPS2 鎖定的開機程式。",
    "遊戲的 EXIT：瀏覽器，然後是你的開機程式（BOOT LOCK）",
]
T['TChinese_l'] = {
    'HINT_EXITPATH': "遊戲內選單中 EXIT 去哪裡。最好在 BOOT LOCK 開啟時留空（PS2BBL、FMCB 或 OSDMenu，或已設定好 BIBLE）：EXIT 會經過瀏覽器，瀏覽器像開機時一樣啟動你的開機程式和 RIPPS2，這是最安全的返回方式。未鎖定時留空：記憶卡或 FAT32 USB 磁碟機上 RIPPS2 自己的 ELF 會在重設後立即載入，但並非每個遊戲都會讓主機為此做好準備。Browser：PS2 瀏覽器。那時完全無法存取 MMCE 上的 ELF。",
    'HINT_RIPPS2_BOOT_LOCK': "開機時透過你的開機程式啟動 RIPPS2：PS2BBL 和 FMCB 會立即啟動它，OSDMenu 會把它放在選單第一項，遊戲的 EXIT 也沿同一條路返回。關閉會還原以前的內容。還沒有？「開機程式」會安裝 BIBLE。",
}

T['Arabic'] = [
    " (ضُبطت الإعدادات التي عُثر عليها: %s.)",
    " احفظ إعداداته مرة واحدة بأداة الإعداد الخاصة به، ثم شغّل BOOT LOCK من جديد.",
    "لا يستطيع %s تشغيل RIPPS2 من مكانه الحالي (%s)، وRIPPS2 لا ينسخ نفسه. ضع RIPPS2.ELF على بطاقة ذاكرة أو محرك USB وشغّله من هناك.",
    "تعذّر على BOOT LOCK كتابة إعدادات محمّل الإقلاع. تأكد أن بطاقة الذاكرة أو المحرك غير محميّ من الكتابة، ثم حاول مجدداً.",
    "لم يجد BOOT LOCK إعدادات محمّل إقلاع لتغييرها.",
    "BOOT LOCK معطّل. يشغّل محمّل الإقلاع لديك ما كان يشغّله سابقاً (%s).",
    "BOOT LOCK مفعّل. يشغّل %s الآن RIPPS2 عند التشغيل (%s)، ومع ترك مكان IGR فارغاً يعود EXIT اللعبة من الطريق نفسه. اضغط مطولاً على أحد أزراره أثناء بدء الجهاز للوصول إلى أي شيء آخر.%s",
    "وضع BOOT LOCK برنامج RIPPS2 أولاً في قائمة OSDMenu (%s). لا يشغّل OSDMenu شيئاً من تلقاء نفسه: اختر RIPPS2 هناك، ويعود EXIT اللعبة إلى تلك القائمة. لجهاز يشغّل RIPPS2 فوراً، يضع BIBLE برنامج PS2BBL 1.2.0 على بطاقة ذاكرة (محمّل الإقلاع).",
    "يعمل BOOT LOCK عبر محمّل إقلاع على بطاقة ذاكرة (PS2BBL أو FMCB أو OSDMenu)، ولا يوجد أي منها هنا.",
    "بطاقة الذاكرة في المنفذ %d تشغّل %s عند التشغيل، ولم يجد BOOT LOCK إعدادات له لتغييرها (يبحث عن %s).",
    "بطاقة الذاكرة في المنفذ %d تشغّل %s عند التشغيل، ولا يستطيع BOOT LOCK ضبطه: يعمل عبر PS2BBL وFMCB وOSDMenu.",
    "يوجد على هذا الجهاز محمّل إقلاع مع قفل RIPPS2.",
    "EXIT للعبة: المتصفح، ثم محمّل الإقلاع لديك (BOOT LOCK)",
]
T['Arabic_l'] = {
    'HINT_EXITPATH': "إلى أين يذهب EXIT في قائمة داخل اللعبة. الأفضل تركه فارغاً مع تفعيل BOOT LOCK (PS2BBL أو FMCB أو OSDMenu، أو ضبط BIBLE): عندها يمر EXIT عبر المتصفح، الذي يشغّل محمّل الإقلاع لديك وRIPPS2 كما عند التشغيل، وهي أكثر طرق العودة أماناً. فارغاً دون القفل: ملف ELF لبرنامج RIPPS2 نفسه على بطاقة ذاكرة أو محرك USB بنظام FAT32، يُحمَّل مباشرة بعد إعادة الضبط، وليست كل لعبة تترك الجهاز جاهزاً لذلك. Browser: متصفح PS2. ولا يمكن الوصول إلى ملف ELF على MMCE حينها إطلاقاً.",
    'HINT_RIPPS2_BOOT_LOCK': "يشغّل RIPPS2 عند التشغيل عبر محمّل الإقلاع لديك: يشغّله PS2BBL وFMCB فوراً، ويضعه OSDMenu أولاً في قائمته، ويعود EXIT اللعبة من الطريق نفسه. الإيقاف يعيد ما كان من قبل. لا يوجد بعد؟ محمّل الإقلاع يثبّت BIBLE.",
}

T['Persian'] = [
    " (پیکربندی‌های یافت‌شده تنظیم شدند: %s.)",
    " تنظیماتش را یک بار با ابزار پیکربندی خودش ذخیره کنید، سپس BOOT LOCK را دوباره روشن کنید.",
    "%s نمی‌تواند RIPPS2 را از جایی که اکنون هست (%s) اجرا کند، و RIPPS2 خودش را کپی نمی‌کند. RIPPS2.ELF را روی کارت حافظه یا درایو USB بگذارید و از همان‌جا اجرا کنید.",
    "BOOT LOCK نتوانست پیکربندی بوت‌لودر را بنویسد. بررسی کنید کارت حافظه یا درایو در برابر نوشتن محافظت نشده باشد، سپس دوباره امتحان کنید.",
    "BOOT LOCK هیچ پیکربندی بوت‌لودری برای تغییر پیدا نکرد.",
    "BOOT LOCK خاموش است. بوت‌لودر شما همان چیزی را اجرا می‌کند که پیش‌تر اجرا می‌کرد (%s).",
    "BOOT LOCK روشن است. %s اکنون هنگام روشن شدن RIPPS2 را اجرا می‌کند (%s)، و با مسیر IGR خالی، EXIT بازی از همان راه برمی‌گردد. برای رسیدن به چیز دیگر، هنگام شروع کنسول یکی از دکمه‌هایش را نگه دارید.%s",
    "BOOT LOCK، RIPPS2 را اولین گزینه در منوی OSDMenu کرد (%s). OSDMenu خودش چیزی اجرا نمی‌کند: RIPPS2 را آنجا انتخاب کنید، و EXIT بازی به همان منو برمی‌گردد. برای کنسولی که RIPPS2 را بی‌درنگ اجرا کند، BIBLE، PS2BBL 1.2.0 را روی کارت حافظه می‌گذارد (بوت‌لودر).",
    "BOOT LOCK از طریق یک بوت‌لودر روی کارت حافظه کار می‌کند (PS2BBL، FMCB یا OSDMenu)، و اینجا هیچ‌کدام نیست.",
    "کارت حافظه در شکاف %d هنگام روشن شدن %s را اجرا می‌کند، و BOOT LOCK هیچ پیکربندی از آن برای تغییر پیدا نکرد (به دنبال %s می‌گردد).",
    "کارت حافظه در شکاف %d هنگام روشن شدن %s را اجرا می‌کند، که BOOT LOCK نمی‌تواند تنظیمش کند: از طریق PS2BBL، FMCB و OSDMenu کار می‌کند.",
    "روی این کنسول یک بوت‌لودر با قفل RIPPS2 هست.",
    "EXIT بازی: مرورگر، سپس بوت‌لودر شما (BOOT LOCK)",
]
T['Persian_l'] = {
    'HINT_EXITPATH': "EXIT در منوی درون بازی به کجا می‌رود. بهتر است با BOOT LOCK روشن خالی بماند (PS2BBL، FMCB یا OSDMenu، یا BIBLE تنظیم‌شده): آن‌وقت EXIT از مرورگر می‌گذرد، که بوت‌لودر شما و RIPPS2 را مثل هنگام روشن شدن اجرا می‌کند، امن‌ترین راه بازگشت. خالی بدون قفل: ELF خود RIPPS2 روی کارت حافظه یا درایو USB با FAT32، درست پس از بازنشانی بارگذاری می‌شود، که هر بازی‌ای کنسول را برایش آماده نمی‌گذارد. Browser: مرورگر PS2. آن‌وقت به ELF روی MMCE اصلاً نمی‌توان رسید.",
    'HINT_RIPPS2_BOOT_LOCK': "RIPPS2 را هنگام روشن شدن از طریق بوت‌لودر شما اجرا می‌کند: PS2BBL و FMCB آن را بی‌درنگ اجرا می‌کنند، OSDMenu آن را اولین گزینه در منویش می‌کند، و EXIT بازی از همان راه برمی‌گردد. خاموش، آنچه پیش‌تر بود را برمی‌گرداند. هنوز هیچ‌کدام؟ بوت‌لودر BIBLE را نصب می‌کند.",
}

T['Laotian'] = [
    " (ການຕັ້ງຄ່າທີ່ພົບ ໄດ້ຕັ້ງແລ້ວ: %s.)",
    " ບັນທຶກການຕັ້ງຄ່າຂອງມັນ ໜຶ່ງເທື່ອ ດ້ວຍໂຕຕັ້ງຄ່າຂອງມັນເອງ, ແລ້ວເປີດ BOOT LOCK ອີກຄັ້ງ.",
    "%s ເລີ່ມ RIPPS2 ຈາກບ່ອນທີ່ມັນຢູ່ດຽວນີ້ (%s) ບໍ່ໄດ້, ແລະ RIPPS2 ບໍ່ສຳເນົາໂຕເອງ. ວາງ RIPPS2.ELF ໄວ້ໃນເມມໂມຣີກາດ ຫຼື ໄດຣຟ໌ USB ແລ້ວເລີ່ມມັນຈາກບ່ອນນັ້ນ.",
    "BOOT LOCK ຂຽນການຕັ້ງຄ່າຂອງໂຕໂຫຼດບູດບໍ່ໄດ້. ກວດເບິ່ງວ່າເມມໂມຣີກາດ ຫຼື ໄດຣຟ໌ ບໍ່ໄດ້ຖືກປ້ອງກັນການຂຽນ, ແລ້ວລອງໃໝ່.",
    "BOOT LOCK ບໍ່ພົບການຕັ້ງຄ່າໂຕໂຫຼດບູດ ທີ່ຈະປ່ຽນ.",
    "BOOT LOCK ປິດ. ໂຕໂຫຼດບູດຂອງທ່ານ ເລີ່ມສິ່ງທີ່ມັນເຄີຍເລີ່ມ (%s).",
    "BOOT LOCK ເປີດ. %s ດຽວນີ້ເລີ່ມ RIPPS2 ຕອນເປີດເຄື່ອງ (%s), ແລະ ເມື່ອເສັ້ນທາງ IGR ວ່າງ, EXIT ຂອງເກມ ກັບມາທາງດຽວກັນ. ກົດປຸ່ມໃດໜຶ່ງຂອງມັນຄ້າງໄວ້ ຕອນເຄື່ອງເລີ່ມ ເພື່ອໄປສິ່ງອື່ນ.%s",
    "BOOT LOCK ວາງ RIPPS2 ໄວ້ອັນທຳອິດ ໃນເມນູຂອງ OSDMenu (%s). OSDMenu ບໍ່ເລີ່ມຫຍັງເອງ: ເລືອກ RIPPS2 ຢູ່ບ່ອນນັ້ນ, ແລະ EXIT ຂອງເກມ ກັບມາເມນູນັ້ນ. ສຳລັບເຄື່ອງທີ່ເລີ່ມ RIPPS2 ທັນທີ, BIBLE ວາງ PS2BBL 1.2.0 ໄວ້ໃນເມມໂມຣີກາດ (ໂຕໂຫຼດບູດ).",
    "BOOT LOCK ເຮັດວຽກ ຜ່ານໂຕໂຫຼດບູດ ໃນເມມໂມຣີກາດ (PS2BBL, FMCB ຫຼື OSDMenu), ແລະ ຢູ່ນີ້ບໍ່ມີເລີຍ.",
    "ເມມໂມຣີກາດໃນຊ່ອງ %d ເລີ່ມ %s ຕອນເປີດເຄື່ອງ, ແລະ BOOT LOCK ບໍ່ພົບການຕັ້ງຄ່າຂອງມັນ ທີ່ຈະປ່ຽນ (ມັນຊອກຫາ %s).",
    "ເມມໂມຣີກາດໃນຊ່ອງ %d ເລີ່ມ %s ຕອນເປີດເຄື່ອງ, ເຊິ່ງ BOOT LOCK ຕັ້ງບໍ່ໄດ້: ມັນເຮັດວຽກ ຜ່ານ PS2BBL, FMCB ແລະ OSDMenu.",
    "ເຄື່ອງນີ້ ມີໂຕໂຫຼດບູດ ພ້ອມການລັອກຂອງ RIPPS2.",
    "EXIT ຂອງເກມ: ໂຕທ່ອງ, ແລ້ວໂຕໂຫຼດບູດຂອງທ່ານ (BOOT LOCK)",
]
T['Laotian_l'] = {
    'HINT_EXITPATH': "EXIT ໃນ ເມນູ ໃນເກມ ໄປໃສ. ດີທີ່ສຸດ ປ່ອຍວ່າງ ໂດຍເປີດ BOOT LOCK (PS2BBL, FMCB ຫຼື OSDMenu, ຫຼື ຕັ້ງ BIBLE ໄວ້): EXIT ຈະຜ່ານໂຕທ່ອງ, ເຊິ່ງເລີ່ມໂຕໂຫຼດບູດຂອງທ່ານ ແລະ RIPPS2 ຄືຕອນເປີດເຄື່ອງ, ທາງກັບທີ່ປອດໄພທີ່ສຸດ. ວ່າງ ໂດຍບໍ່ລັອກ: ELF ຂອງ RIPPS2 ເອງ ໃນເມມໂມຣີກາດ ຫຼື ໄດຣຟ໌ USB FAT32, ໂຫຼດທັນທີຫຼັງຣີເຊັດ, ເຊິ່ງບໍ່ແມ່ນທຸກເກມ ທີ່ປ່ອຍເຄື່ອງໃຫ້ພ້ອມ. Browser: ໂຕທ່ອງຂອງ PS2. ຕອນນັ້ນ ເຂົ້າ ELF ໃນ MMCE ບໍ່ໄດ້ເລີຍ.",
    'HINT_RIPPS2_BOOT_LOCK': "ເລີ່ມ RIPPS2 ຕອນເປີດເຄື່ອງ ຜ່ານໂຕໂຫຼດບູດຂອງທ່ານ: PS2BBL ແລະ FMCB ເລີ່ມມັນທັນທີ, OSDMenu ວາງມັນໄວ້ອັນທຳອິດໃນເມນູ, ແລະ EXIT ຂອງເກມ ກັບມາທາງດຽວກັນ. ປິດ ຄືນສິ່ງທີ່ເຄີຍມີ. ຍັງບໍ່ມີ? ໂຕໂຫຼດບູດ ຕິດຕັ້ງ BIBLE.",
}

T['Cebuano'] = [
    " (Gi-set ang nakit-ang mga config: %s.)",
    " I-save makausa ang mga setting niini gamit ang kaugalingon niining configurator, unya i-on pag-usab ang BOOT LOCK.",
    "Dili masugdan sa %s ang RIPPS2 gikan sa nahimutangan niini karon (%s), ug dili kopyahon sa RIPPS2 ang kaugalingon. Ibutang ang RIPPS2.ELF sa memory card o USB drive ug sugdi kini gikan didto.",
    "Wala masulat sa BOOT LOCK ang config sa boot loader. Susiha nga dili write protected ang memory card o drive, unya sulayi pag-usab.",
    "Walay nakit-ang boot loader config ang BOOT LOCK nga usbon.",
    "Gipalong ang BOOT LOCK. Gisugdan sa imong boot loader ang gisugdan niini kaniadto (%s).",
    "Gibuksan ang BOOT LOCK. Gisugdan na sa %s ang RIPPS2 sa pag-on (%s), ug kung blangko ang IGR path, mobalik ang EXIT sa dula sa samang dalan. Pindota og dugay ang usa sa mga button niini samtang nagsugod ang console aron makaadto sa uban.%s",
    "Gibutang sa BOOT LOCK ang RIPPS2 nga una sa menu sa OSDMenu (%s). Walay gisugdan ang OSDMenu sa kaugalingon: pilia didto ang RIPPS2, ug mobalik sa maong menu ang EXIT sa dula. Para sa console nga dayon mosugod sa RIPPS2, ibutang sa BIBLE ang PS2BBL 1.2.0 sa memory card (Boot Loader).",
    "Molihok ang BOOT LOCK pinaagi sa boot loader sa memory card (PS2BBL, FMCB o OSDMenu), ug walay bisan usa dinhi.",
    "Gisugdan sa memory card sa slot %d ang %s sa pag-on, ug walay nakit-ang config niini ang BOOT LOCK nga usbon (gipangita niini ang %s).",
    "Gisugdan sa memory card sa slot %d ang %s sa pag-on, nga dili ma-set sa BOOT LOCK: molihok kini pinaagi sa PS2BBL, FMCB ug OSDMenu.",
    "Adunay boot loader nga may lock sa RIPPS2 niining console.",
    "EXIT sa dula: ang browser, unya ang imong boot loader (BOOT LOCK)",
]
T['Cebuano_l'] = {
    'HINT_EXITPATH': "Asa padulong ang EXIT sa Menu sulod sa dula. Mas maayo nga biyaan nga blangko nga naka-on ang BOOT LOCK (PS2BBL, FMCB o OSDMenu, o naka-set up ang BIBLE): moagi ang EXIT sa browser, nga mosugod sa imong boot loader ug sa RIPPS2 sama sa pag-on, ang labing luwas nga pagbalik. Blangko nga walay lock: ang kaugalingong ELF sa RIPPS2 sa memory card o FAT32 USB drive, i-load dayon human sa reset, nga dili tanang dula mobiya sa console nga andam. Browser: ang PS2 browser. Dili maabot ang ELF sa MMCE niana.",
    'HINT_RIPPS2_BOOT_LOCK': "Sugdan ang RIPPS2 sa pag-on pinaagi sa imong boot loader: dayon kini sugdan sa PS2BBL ug FMCB, ibutang kini sa OSDMenu nga una sa menu niini, ug mobalik ang EXIT sa dula sa samang dalan. Ibalik sa Off ang naa kaniadto. Wala pa? Mag-install og BIBLE ang Boot Loader.",
}

os.makedirs(OUT, exist_ok=True)
for lang in [k for k in T if not k.endswith('_l')]:
    s = {str(i): v for i, v in enumerate(T[lang])}
    json.dump({'s': s, 'l': T[lang + '_l']}, open(os.path.join(OUT, lang + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(lang, len(s))
