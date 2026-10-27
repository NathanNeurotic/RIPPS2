"""Build 116 strings (s116.json) and labels: Swedish, Danish, Polish, Czech, Croatian, Serbian, Romana, Hungarian.
Run from the repo root: python tools/lang116/batch2.py (writes tr116/<Language>.json)."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'tr116')

T = {}

T['Swedish'] = [
    " (De hittade konfigurationerna ställdes in: %s.)",
    " Spara dess inställningar en gång med dess egen konfigurator och slå sedan på BOOT LOCK igen.",
    "%s kan inte starta RIPPS2 där det ligger nu (%s), och RIPPS2 kopierar inte sig självt. Lägg RIPPS2.ELF på ett minneskort eller en USB-enhet och starta det därifrån.",
    "BOOT LOCK kunde inte skriva startladdarens konfiguration. Kontrollera att minneskortet eller enheten inte är skrivskyddad och försök igen.",
    "BOOT LOCK hittade ingen startladdarkonfiguration att ändra.",
    "BOOT LOCK är av. Din startladdare startar det den startade tidigare (%s).",
    "BOOT LOCK är på. %s startar nu RIPPS2 vid påslag (%s), och ett tomt Utgång till skickar ett spels EXIT tillbaka samma väg. Håll en av dess knappar medan konsolen startar för att nå något annat.%s",
    "BOOT LOCK satte RIPPS2 först i OSDMenus meny (%s). OSDMenu startar ingenting av sig själv: välj RIPPS2 där, och ett spels EXIT kommer tillbaka till den menyn. För en konsol som startar RIPPS2 direkt lägger BIBLE PS2BBL 1.2.0 på ett minneskort (Startladdare).",
    "BOOT LOCK fungerar via en startladdare på ett minneskort (PS2BBL, FMCB eller OSDMenu), och här finns ingen.",
    "Minneskortet i plats %d startar %s vid påslag, och BOOT LOCK hittade ingen konfiguration för den att ändra (den letar efter %s).",
    "Minneskortet i plats %d startar %s vid påslag, som BOOT LOCK inte kan ställa in: den fungerar via PS2BBL, FMCB och OSDMenu.",
    "En startladdare med RIPPS2:s lås finns på den här konsolen.",
    "Ett spels EXIT: webbläsaren, sedan din startladdare (BOOT LOCK)",
]
T['Swedish_l'] = {
    'HINT_EXITPATH': "Vart EXIT i Meny i spelet går. Lämna helst tomt med BOOT LOCK på (PS2BBL, FMCB eller OSDMenu, eller BIBLE inställt): EXIT går då via webbläsaren, som startar din startladdare och RIPPS2 som vid påslag, den säkraste vägen tillbaka. Tomt utan låset: RIPPS2:s egen ELF på ett minneskort eller en FAT32-USB-enhet, laddad direkt efter återställningen, vilket inte alla spel lämnar konsolen redo för. Browser: PS2-webbläsaren. En ELF på MMCE går då inte att nå alls.",
    'HINT_RIPPS2_BOOT_LOCK': "Startar RIPPS2 vid påslag via din startladdare: PS2BBL och FMCB startar det direkt, OSDMenu sätter det först i sin meny, och ett spels EXIT går tillbaka samma väg. Av lägger tillbaka det som fanns förut. Ingen ännu? Startladdare installerar BIBLE.",
}

T['Danish'] = [
    " (De fundne konfigurationer blev sat: %s.)",
    " Gem dens indstillinger én gang med dens egen konfigurator, og slå så BOOT LOCK til igen.",
    "%s kan ikke starte RIPPS2 derfra, hvor det ligger nu (%s), og RIPPS2 kopierer ikke sig selv. Læg RIPPS2.ELF på et memorykort eller et USB-drev, og start det derfra.",
    "BOOT LOCK kunne ikke skrive opstartsindlæserens konfiguration. Tjek, at memorykortet eller drevet ikke er skrivebeskyttet, og prøv igen.",
    "BOOT LOCK fandt ingen opstartsindlæser-konfiguration at ændre.",
    "BOOT LOCK er slået fra. Din opstartsindlæser starter det, den startede før (%s).",
    "BOOT LOCK er slået til. %s starter nu RIPPS2 ved opstart (%s), og en tom IGR-sti sender et spils EXIT tilbage samme vej. Hold en af dens knapper nede, mens konsollen starter, for at nå noget andet.%s",
    "BOOT LOCK satte RIPPS2 først i OSDMenus menu (%s). OSDMenu starter ikke noget af sig selv: vælg RIPPS2 der, og et spils EXIT vender tilbage til den menu. For en konsol, der starter RIPPS2 med det samme, lægger BIBLE PS2BBL 1.2.0 på et memorykort (Opstartsindlæser).",
    "BOOT LOCK virker gennem en opstartsindlæser på et memorykort (PS2BBL, FMCB eller OSDMenu), og her er ingen.",
    "Memorykortet i plads %d starter %s ved opstart, og BOOT LOCK fandt ingen konfiguration af den at ændre (den leder efter %s).",
    "Memorykortet i plads %d starter %s ved opstart, som BOOT LOCK ikke kan indstille: den virker gennem PS2BBL, FMCB og OSDMenu.",
    "En opstartsindlæser med RIPPS2's lås er på denne konsol.",
    "Et spils EXIT: browseren, derefter din opstartsindlæser (BOOT LOCK)",
]
T['Danish_l'] = {
    'HINT_EXITPATH': "Hvor EXIT i Menu i spillet fører hen. Bedst at lade stå tom med BOOT LOCK slået til (PS2BBL, FMCB eller OSDMenu, eller BIBLE sat op): EXIT går så gennem browseren, som starter din opstartsindlæser og RIPPS2 som ved opstart, den sikreste vej tilbage. Tom uden låsen: RIPPS2's egen ELF på et memorykort eller et FAT32-USB-drev, indlæst lige efter nulstillingen, som ikke alle spil efterlader konsollen klar til. Browser: PS2-browseren. En ELF på MMCE kan så slet ikke nås.",
    'HINT_RIPPS2_BOOT_LOCK': "Starter RIPPS2 ved opstart gennem din opstartsindlæser: PS2BBL og FMCB starter det med det samme, OSDMenu sætter det først i sin menu, og et spils EXIT går tilbage samme vej. Fra sætter det tilbage, der var før. Ingen endnu? Opstartsindlæser installerer BIBLE.",
}

T['Polish'] = [
    " (Ustawiono znalezione konfiguracje: %s.)",
    " Zapisz raz jego ustawienia w jego własnym konfiguratorze, a potem włącz BOOT LOCK ponownie.",
    "%s nie może uruchomić RIPPS2 z miejsca, w którym jest teraz (%s), a RIPPS2 nie kopiuje się sam. Umieść RIPPS2.ELF na karcie pamięci lub dysku USB i uruchom go stamtąd.",
    "BOOT LOCK nie mógł zapisać konfiguracji programu rozruchowego. Sprawdź, czy karta pamięci lub dysk nie jest chroniony przed zapisem, i spróbuj ponownie.",
    "BOOT LOCK nie znalazł konfiguracji programu rozruchowego do zmiany.",
    "BOOT LOCK jest wyłączony. Twój program rozruchowy uruchamia to, co uruchamiał wcześniej (%s).",
    "BOOT LOCK jest włączony. %s uruchamia teraz RIPPS2 przy włączaniu (%s), a pusta Ścieżka Dla IGR odsyła EXIT z gry tą samą drogą. Przytrzymaj jeden z jego przycisków podczas startu konsoli, aby dostać się do czegoś innego.%s",
    "BOOT LOCK umieścił RIPPS2 na pierwszym miejscu w menu OSDMenu (%s). OSDMenu samo niczego nie uruchamia: wybierz tam RIPPS2, a EXIT z gry wraca do tego menu. Aby konsola od razu uruchamiała RIPPS2, BIBLE instaluje PS2BBL 1.2.0 na karcie pamięci (Program rozruchowy).",
    "BOOT LOCK działa przez program rozruchowy na karcie pamięci (PS2BBL, FMCB lub OSDMenu), a tutaj nie ma żadnego.",
    "Karta pamięci w gnieździe %d uruchamia przy włączaniu %s, a BOOT LOCK nie znalazł jego konfiguracji do zmiany (szuka %s).",
    "Karta pamięci w gnieździe %d uruchamia przy włączaniu %s, którego BOOT LOCK nie potrafi ustawić: działa przez PS2BBL, FMCB i OSDMenu.",
    "Na tej konsoli jest program rozruchowy z blokadą RIPPS2.",
    "EXIT z gry: przeglądarka, potem twój program rozruchowy (BOOT LOCK)",
]
T['Polish_l'] = {
    'HINT_EXITPATH': "Dokąd prowadzi EXIT w Menu w grze. Najlepiej zostawić puste z włączonym BOOT LOCK (PS2BBL, FMCB lub OSDMenu, albo ustawionym BIBLE): EXIT idzie wtedy przez przeglądarkę, która uruchamia twój program rozruchowy i RIPPS2 jak po włączeniu, najbezpieczniejszy powrót. Puste bez blokady: własny ELF RIPPS2 na karcie pamięci lub dysku USB FAT32, ładowany zaraz po resecie, na co nie każda gra zostawia konsolę gotową. Browser: przeglądarka PS2. ELF na MMCE jest wtedy w ogóle nieosiągalny.",
    'HINT_RIPPS2_BOOT_LOCK': "Uruchamia RIPPS2 przy włączaniu przez twój program rozruchowy: PS2BBL i FMCB uruchamiają go od razu, OSDMenu stawia go na pierwszym miejscu w swoim menu, a EXIT z gry wraca tą samą drogą. Wył. przywraca to, co było wcześniej. Jeszcze żadnego? Program rozruchowy zainstaluje BIBLE.",
}

T['Czech'] = [
    " (Nalezená nastavení byla upravena: %s.)",
    " Jednou uložte jeho nastavení v jeho vlastním konfigurátoru a pak BOOT LOCK znovu zapněte.",
    "%s nemůže spustit RIPPS2 z místa, kde teď je (%s), a RIPPS2 se sám nekopíruje. Dejte RIPPS2.ELF na paměťovou kartu nebo USB disk a spusťte ho odtud.",
    "BOOT LOCK nemohl zapsat nastavení zavaděče. Zkontrolujte, že paměťová karta nebo disk není chráněn proti zápisu, a zkuste to znovu.",
    "BOOT LOCK nenašel žádné nastavení zavaděče ke změně.",
    "BOOT LOCK je vypnutý. Váš zavaděč spouští to, co spouštěl dřív (%s).",
    "BOOT LOCK je zapnutý. %s teď při zapnutí spouští RIPPS2 (%s) a prázdná Cesta k IGR vrací EXIT ze hry stejnou cestou. Abyste se dostali jinam, držte při startu konzole jedno z jeho tlačítek.%s",
    "BOOT LOCK dal RIPPS2 na první místo v menu OSDMenu (%s). OSDMenu samo nic nespouští: vyberte tam RIPPS2 a EXIT ze hry se vrací do toho menu. Pro konzoli, která spustí RIPPS2 hned, nainstaluje BIBLE PS2BBL 1.2.0 na paměťovou kartu (Zavaděč).",
    "BOOT LOCK funguje přes zavaděč na paměťové kartě (PS2BBL, FMCB nebo OSDMenu) a tady žádný není.",
    "Paměťová karta ve slotu %d při zapnutí spouští %s a BOOT LOCK nenašel žádné jeho nastavení ke změně (hledá %s).",
    "Paměťová karta ve slotu %d při zapnutí spouští %s, který BOOT LOCK nastavit neumí: funguje přes PS2BBL, FMCB a OSDMenu.",
    "Na této konzoli je zavaděč se zámkem RIPPS2.",
    "EXIT ze hry: prohlížeč, pak váš zavaděč (BOOT LOCK)",
]
T['Czech_l'] = {
    'HINT_EXITPATH': "Kam vede EXIT v Menu ve hře. Nejlépe nechat prázdné se zapnutým BOOT LOCK (PS2BBL, FMCB nebo OSDMenu, nebo nastaveným BIBLE): EXIT pak vede přes prohlížeč, který spustí váš zavaděč a RIPPS2 jako po zapnutí, nejbezpečnější návrat. Prázdné bez zámku: vlastní ELF RIPPS2 na paměťové kartě nebo USB disku FAT32, načtený hned po resetu, na což ne každá hra nechá konzoli připravenou. Browser: prohlížeč PS2. ELF na MMCE pak není vůbec dostupný.",
    'HINT_RIPPS2_BOOT_LOCK': "Při zapnutí spustí RIPPS2 přes váš zavaděč: PS2BBL a FMCB ho spustí hned, OSDMenu ho dá na první místo svého menu a EXIT ze hry vede zpět stejnou cestou. Vypnuto vrátí to, co tam bylo dřív. Ještě žádný? Zavaděč nainstaluje BIBLE.",
}

T['Croatian'] = [
    " (Pronađene konfiguracije su postavljene: %s.)",
    " Jednom spremi njegove postavke njegovim vlastitim konfiguratorom, pa ponovno uključi BOOT LOCK.",
    "%s ne može pokrenuti RIPPS2 s mjesta gdje je sada (%s), a RIPPS2 se ne kopira sam. Stavi RIPPS2.ELF na memorijsku karticu ili USB pogon i pokreni ga odande.",
    "BOOT LOCK nije mogao zapisati konfiguraciju učitavača. Provjeri da memorijska kartica ili pogon nisu zaštićeni od pisanja, pa pokušaj ponovno.",
    "BOOT LOCK nije pronašao konfiguraciju učitavača za promjenu.",
    "BOOT LOCK je isključen. Tvoj učitavač pokreće ono što je pokretao prije (%s).",
    "BOOT LOCK je uključen. %s sada pokreće RIPPS2 pri uključivanju (%s), a prazna IGR Putanja vraća EXIT iz igre istim putem. Drži jednu od njegovih tipki dok se konzola pokreće da dođeš do bilo čega drugog.%s",
    "BOOT LOCK je stavio RIPPS2 na prvo mjesto u izborniku OSDMenu-a (%s). OSDMenu sam ništa ne pokreće: odaberi ondje RIPPS2, a EXIT iz igre vraća se u taj izbornik. Za konzolu koja odmah pokreće RIPPS2, BIBLE stavlja PS2BBL 1.2.0 na memorijsku karticu (Učitavač).",
    "BOOT LOCK radi preko učitavača na memorijskoj kartici (PS2BBL, FMCB ili OSDMenu), a ovdje ga nema.",
    "Memorijska kartica u utoru %d pri uključivanju pokreće %s, a BOOT LOCK nije pronašao njegovu konfiguraciju za promjenu (traži %s).",
    "Memorijska kartica u utoru %d pri uključivanju pokreće %s, koji BOOT LOCK ne može postaviti: radi preko PS2BBL-a, FMCB-a i OSDMenu-a.",
    "Na ovoj konzoli je učitavač s RIPPS2 zaključavanjem.",
    "EXIT iz igre: preglednik, zatim tvoj učitavač (BOOT LOCK)",
]
T['Croatian_l'] = {
    'HINT_EXITPATH': "Kamo vodi EXIT u Izborniku u igri. Najbolje ostaviti prazno s uključenim BOOT LOCK (PS2BBL, FMCB ili OSDMenu, ili postavljenim BIBLE): EXIT tada ide kroz preglednik, koji pokreće tvoj učitavač i RIPPS2 kao pri uključivanju, najsigurniji povratak. Prazno bez zaključavanja: RIPPS2-ov vlastiti ELF na memorijskoj kartici ili FAT32 USB pogonu, učitan odmah nakon reseta, za što ne ostavlja svaka igra konzolu spremnom. Browser: PS2 preglednik. ELF na MMCE-u tada uopće nije dostupan.",
    'HINT_RIPPS2_BOOT_LOCK': "Pokreće RIPPS2 pri uključivanju preko tvog učitavača: PS2BBL i FMCB ga pokreću odmah, OSDMenu ga stavlja na prvo mjesto u svom izborniku, a EXIT iz igre vraća se istim putem. Isključeno vraća ono što je bilo prije. Još nijedan? Učitavač instalira BIBLE.",
}

T['Serbian'] = [
    " (Pronađene konfiguracije su podešene: %s.)",
    " Jednom sačuvajte njegova podešavanja njegovim sopstvenim konfiguratorom, pa ponovo uključite BOOT LOCK.",
    "%s ne može da pokrene RIPPS2 sa mesta gde je sada (%s), a RIPPS2 se ne kopira sam. Stavite RIPPS2.ELF na memorijsku karticu ili USB uređaj i pokrenite ga odatle.",
    "BOOT LOCK nije mogao da upiše konfiguraciju učitavača. Proverite da memorijska kartica ili uređaj nisu zaštićeni od upisa, pa pokušajte ponovo.",
    "BOOT LOCK nije pronašao konfiguraciju učitavača za izmenu.",
    "BOOT LOCK je isključen. Vaš učitavač pokreće ono što je pokretao ranije (%s).",
    "BOOT LOCK je uključen. %s sada pokreće RIPPS2 pri uključivanju (%s), a prazna IGR Putanja vraća EXIT iz igre istim putem. Držite jedan od njegovih tastera dok se konzola pokreće da biste stigli do nečeg drugog.%s",
    "BOOT LOCK je stavio RIPPS2 na prvo mesto u meniju OSDMenu-a (%s). OSDMenu sam ništa ne pokreće: izaberite tamo RIPPS2, a EXIT iz igre se vraća u taj meni. Za konzolu koja odmah pokreće RIPPS2, BIBLE stavlja PS2BBL 1.2.0 na memorijsku karticu (Učitavač).",
    "BOOT LOCK radi preko učitavača na memorijskoj kartici (PS2BBL, FMCB ili OSDMenu), a ovde ga nema.",
    "Memorijska kartica u slotu %d pri uključivanju pokreće %s, a BOOT LOCK nije pronašao njegovu konfiguraciju za izmenu (traži %s).",
    "Memorijska kartica u slotu %d pri uključivanju pokreće %s, koji BOOT LOCK ne može da podesi: radi preko PS2BBL-a, FMCB-a i OSDMenu-a.",
    "Na ovoj konzoli je učitavač sa RIPPS2 zaključavanjem.",
    "EXIT iz igre: pregledač, zatim vaš učitavač (BOOT LOCK)",
]
T['Serbian_l'] = {
    'HINT_EXITPATH': "Kuda vodi EXIT u Meniju u igri. Najbolje ostaviti prazno sa uključenim BOOT LOCK (PS2BBL, FMCB ili OSDMenu, ili podešenim BIBLE): EXIT tada ide kroz pregledač, koji pokreće vaš učitavač i RIPPS2 kao pri uključivanju, najbezbedniji povratak. Prazno bez zaključavanja: sopstveni ELF RIPPS2 na memorijskoj kartici ili FAT32 USB uređaju, učitan odmah posle reseta, za šta ne ostavlja svaka igra konzolu spremnom. Browser: PS2 pregledač. ELF na MMCE-u tada uopšte nije dostupan.",
    'HINT_RIPPS2_BOOT_LOCK': "Pokreće RIPPS2 pri uključivanju preko vašeg učitavača: PS2BBL i FMCB ga pokreću odmah, OSDMenu ga stavlja na prvo mesto u svom meniju, a EXIT iz igre se vraća istim putem. Isključeno vraća ono što je bilo ranije. Još nijedan? Učitavač instalira BIBLE.",
}

T['Romana'] = [
    " (Configurațiile găsite au fost setate: %s.)",
    " Salvează-i o dată setările cu propriul lui configurator, apoi pornește din nou BOOT LOCK.",
    "%s nu poate porni RIPPS2 de unde este acum (%s), iar RIPPS2 nu se copiază singur. Pune RIPPS2.ELF pe un card de memorie sau pe o unitate USB și pornește-l de acolo.",
    "BOOT LOCK nu a putut scrie configurația încărcătorului de pornire. Verifică dacă cardul de memorie sau unitatea nu e protejată la scriere, apoi încearcă din nou.",
    "BOOT LOCK nu a găsit nicio configurație de încărcător de pornire de modificat.",
    "BOOT LOCK este oprit. Încărcătorul tău de pornire pornește ce pornea înainte (%s).",
    "BOOT LOCK este pornit. %s pornește acum RIPPS2 la pornire (%s), iar o cale IGR goală trimite EXIT-ul unui joc înapoi pe același drum. Ține apăsat unul dintre butoanele lui cât timp pornește consola ca să ajungi la altceva.%s",
    "BOOT LOCK a pus RIPPS2 primul în meniul OSDMenu (%s). OSDMenu nu pornește nimic singur: alege RIPPS2 acolo, iar EXIT-ul unui joc revine în acel meniu. Pentru o consolă care pornește RIPPS2 imediat, BIBLE pune PS2BBL 1.2.0 pe un card de memorie (Boot Loader).",
    "BOOT LOCK funcționează printr-un încărcător de pornire pe un card de memorie (PS2BBL, FMCB sau OSDMenu), iar aici nu există niciunul.",
    "Cardul de memorie din slotul %d pornește %s la pornire, iar BOOT LOCK nu a găsit nicio configurație a lui de modificat (caută %s).",
    "Cardul de memorie din slotul %d pornește %s la pornire, pe care BOOT LOCK nu îl poate seta: funcționează prin PS2BBL, FMCB și OSDMenu.",
    "Pe această consolă este un încărcător de pornire cu blocarea RIPPS2.",
    "EXIT-ul unui joc: browserul, apoi încărcătorul tău de pornire (BOOT LOCK)",
]
T['Romana_l'] = {
    'HINT_EXITPATH': "Unde duce EXIT din Meniul în joc. Cel mai bine lăsat gol cu BOOT LOCK pornit (PS2BBL, FMCB sau OSDMenu, ori BIBLE setat): EXIT trece atunci prin browser, care pornește încărcătorul tău de pornire și RIPPS2 ca la aprindere, cea mai sigură întoarcere. Gol fără blocare: propriul ELF al RIPPS2 pe un card de memorie sau pe o unitate USB FAT32, încărcat imediat după resetare, pentru care nu orice joc lasă consola pregătită. Browser: browserul PS2. Un ELF pe MMCE nu poate fi atins deloc atunci.",
    'HINT_RIPPS2_BOOT_LOCK': "Pornește RIPPS2 la pornire prin încărcătorul tău de pornire: PS2BBL și FMCB îl pornesc imediat, OSDMenu îl pune primul în meniul lui, iar EXIT-ul unui joc revine pe același drum. Oprit pune la loc ce era înainte. Încă niciunul? Boot Loader instalează BIBLE.",
}

T['Hungarian'] = [
    " (A talált beállítások be lettek állítva: %s.)",
    " Mentsd el egyszer a beállításait a saját konfigurálójával, majd kapcsold be újra a BOOT LOCK-ot.",
    "A(z) %s nem tudja elindítani a RIPPS2-t onnan, ahol most van (%s), és a RIPPS2 nem másolja magát. Tedd a RIPPS2.ELF-et memóriakártyára vagy USB meghajtóra, és onnan indítsd.",
    "A BOOT LOCK nem tudta írni a rendszerbetöltő beállítását. Ellenőrizd, hogy a memóriakártya vagy a meghajtó nincs-e írásvédve, majd próbáld újra.",
    "A BOOT LOCK nem talált módosítható rendszerbetöltő-beállítást.",
    "A BOOT LOCK ki van kapcsolva. A rendszerbetöltőd azt indítja, amit korábban (%s).",
    "A BOOT LOCK be van kapcsolva. A(z) %s most bekapcsoláskor a RIPPS2-t indítja (%s), és üres IGR útvonal esetén egy játék EXIT-je ugyanazon az úton tér vissza. Ha máshová szeretnél jutni, tartsd lenyomva valamelyik gombját, miközben a konzol indul.%s",
    "A BOOT LOCK a RIPPS2-t az OSDMenu menüjének első helyére tette (%s). Az OSDMenu magától semmit sem indít: ott válaszd a RIPPS2-t, és egy játék EXIT-je abba a menübe tér vissza. Ha a konzol azonnal a RIPPS2-t indítsa, a BIBLE a PS2BBL 1.2.0-t memóriakártyára teszi (Rendszerbetöltő).",
    "A BOOT LOCK egy memóriakártyán lévő rendszerbetöltőn keresztül működik (PS2BBL, FMCB vagy OSDMenu), és itt nincs ilyen.",
    "A(z) %d. foglalat memóriakártyája bekapcsoláskor ezt indítja: %s, és a BOOT LOCK nem talált hozzá módosítható beállítást (ezt keresi: %s).",
    "A(z) %d. foglalat memóriakártyája bekapcsoláskor ezt indítja: %s, amit a BOOT LOCK nem tud beállítani: a PS2BBL-en, az FMCB-n és az OSDMenun keresztül működik.",
    "Ezen a konzolon egy rendszerbetöltő van a RIPPS2 zárával.",
    "Egy játék EXIT-je: a böngésző, aztán a rendszerbetöltőd (BOOT LOCK)",
]
T['Hungarian_l'] = {
    'HINT_EXITPATH': "Hová vezet az EXIT a Játék közbeni menüben. Legjobb üresen hagyni bekapcsolt BOOT LOCK-kal (PS2BBL, FMCB vagy OSDMenu, vagy beállított BIBLE): az EXIT ekkor a böngészőn át vezet, amely úgy indítja el a rendszerbetöltődet és a RIPPS2-t, mint bekapcsoláskor, ez a legbiztonságosabb visszaút. Üresen zár nélkül: a RIPPS2 saját ELF-je memóriakártyán vagy FAT32 USB meghajtón, közvetlenül az újraindítás után betöltve, amire nem minden játék hagyja készen a konzolt. Browser: a PS2 böngészője. Egy ELF az MMCE-n ekkor egyáltalán nem érhető el.",
    'HINT_RIPPS2_BOOT_LOCK': "Bekapcsoláskor a rendszerbetöltődön keresztül indítja a RIPPS2-t: a PS2BBL és az FMCB azonnal elindítja, az OSDMenu a menüje első helyére teszi, és egy játék EXIT-je ugyanazon az úton tér vissza. Kikapcsolva visszaállítja, ami előtte volt. Még nincs? A Rendszerbetöltő telepíti a BIBLE-t.",
}

os.makedirs(OUT, exist_ok=True)
for lang in [k for k in T if not k.endswith('_l')]:
    s = {str(i): v for i, v in enumerate(T[lang])}
    json.dump({'s': s, 'l': T[lang + '_l']}, open(os.path.join(OUT, lang + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(lang, len(s))
