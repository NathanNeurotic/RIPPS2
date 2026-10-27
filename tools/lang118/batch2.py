"""Build 118 strings (s118.json) and labels: Swedish, Danish, Polish, Czech, Croatian, Serbian, Romana, Hungarian.
Run from the repo root: python tools/lang118/batch2.py (writes tr118/<Language>.json)."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'tr118')

T = {}

T['Swedish'] = [
    "%d bilder från %d ART-mappar hamnar i en enda fil, %s. ART-mapparna förblir som de är: paketet är en kopia. Du kan kopiera art.tar till en annan enhets ART-mapp med Memory Files, men att bygga det på enheten du bläddrar från går snabbast, därför står den snabbaste enheten först. Bygga nu?",
    "%sART/art.tar: %d bilder där, läser %d KB/s",
    "%sART/art.tar: %d bilder där, läser %d KB/s, den snabbaste",
    "Används: %s, %d bilder, %d MB",
    "Tittar på ART-mapparna på de startade enheterna",
    "Mäter hur snabbt varje enhet läser sina bilder: %s",
    "Inget: varje bild läses från sin egen ART-mapp.",
    "Packar bilderna i %s: %d av %d bilder, %d MB. Tryck på bakåtknappen för att stoppa.",
    "TA BORT paketet i %s (ART-mapparna förblir som de är)",
    "Ta bort ART-paketet i %s? ART-mapparna förblir som de är.",
    "Stoppat. Det ofärdiga paketet togs bort, och bilderna läses från ART-mapparna som förut.",
    "ART-paketet kunde inte skrivas till %s (finns det plats på den enheten?). Inget annat ändrades: bilderna läses från ART-mapparna som förut.",
    "ART-paketet i %s är borttaget. Bilderna läses från ART-mapparna igen.",
    "ART-paketet är byggt: %d bilder, %d MB, i %s (%d s). Bilderna läses från det från och med nu, och de %d spel det byggdes för får aldrig sin ART-mapp tillfrågad en bild i taget. Bilder som RIPPS2 hämtar eller tar syns direkt; bilder du kopierar in från en dator syns när du bygger paketet igen.",
    "Det finns ingen ART-mapp med bilder på de startade enheterna. Starta enheterna där dina bilder finns (SELECT på deras sida) och kom sedan tillbaka.",
]
T['Swedish_l'] = {
    'RIPPS2_ART_PACK': "ART-paket",
    'RIPPS2_ART_PACK_BUILD': "Bygg eller ta bort",
    'HINT_RIPPS2_ART_PACK': "Packar ART-mappen på varje startad enhet i en enda art.tar på enheten du väljer (den snabbaste erbjuds först). Omslagen läses då från en fil med ett index, aldrig med en sökning per spel, så menyerna och musiken förblir mjuka. ART-mapparna förblir som de är.",
}

T['Danish'] = [
    "%d billeder fra %d ART-mapper kommer i én fil, %s. ART-mapperne forbliver, som de er: pakken er en kopi. Du kan kopiere art.tar til et andet drevs ART-mappe med Memory Files, men det går hurtigst at bygge den på det drev, du browser fra, derfor står det hurtigste drev først. Byg den nu?",
    "%sART/art.tar: %d billeder der, læser %d KB/s",
    "%sART/art.tar: %d billeder der, læser %d KB/s, det hurtigste",
    "I brug: %s, %d billeder, %d MB",
    "Kigger på ART-mapperne på de startede drev",
    "Måler hvor hurtigt hvert drev læser sine billeder: %s",
    "Ingen: hvert billede læses fra sin egen ART-mappe.",
    "Pakker billederne i %s: %d af %d billeder, %d MB. Tryk på tilbage-knappen for at stoppe.",
    "FJERN pakken i %s (ART-mapperne forbliver, som de er)",
    "Fjern ART-pakken i %s? ART-mapperne forbliver, som de er.",
    "Stoppet. Den ufærdige pakke blev fjernet, og billederne læses fra ART-mapperne som før.",
    "ART-pakken kunne ikke skrives til %s (er der plads på det drev?). Intet andet ændrede sig: billederne læses fra ART-mapperne som før.",
    "ART-pakken i %s er fjernet. Billederne læses fra ART-mapperne igen.",
    "ART-pakken er bygget: %d billeder, %d MB, i %s (%d s). Billederne læses fra den fra nu af, og de %d spil, den blev bygget til, får aldrig deres ART-mappe spurgt ét billede ad gangen. Billeder, som RIPPS2 henter eller tager, vises med det samme; billeder, du kopierer ind fra en pc, vises, når du bygger pakken igen.",
    "Der er ingen ART-mappe med billeder på de startede drev. Start de drev, dine billeder ligger på (SELECT på deres side), og kom så tilbage.",
]
T['Danish_l'] = {
    'RIPPS2_ART_PACK': "ART-pakke",
    'RIPPS2_ART_PACK_BUILD': "Byg eller fjern",
    'HINT_RIPPS2_ART_PACK': "Pakker ART-mappen på hvert startet drev i én art.tar på det drev, du vælger (det hurtigste tilbydes først). Coverne læses så fra én fil med ét indeks, aldrig med et opslag pr. spil, så menuerne og musikken forbliver glatte. ART-mapperne forbliver, som de er.",
}

T['Polish'] = [
    "%d obrazów z %d folderów ART trafia do jednego pliku, %s. Foldery ART zostają bez zmian: paczka jest kopią. Możesz skopiować art.tar do folderu ART innego dysku w Memory Files, ale najszybciej jest zbudować ją na dysku, z którego przeglądasz, dlatego najszybszy dysk jest pierwszy. Zbudować teraz?",
    "%sART/art.tar: %d obrazów tam, czyta %d KB/s",
    "%sART/art.tar: %d obrazów tam, czyta %d KB/s, najszybszy",
    "W użyciu: %s, %d obrazów, %d MB",
    "Sprawdzanie folderów ART na uruchomionych dyskach",
    "Pomiar szybkości, z jaką każdy dysk czyta swoje obrazy: %s",
    "Brak: każdy obraz jest czytany z własnego folderu ART.",
    "Pakowanie obrazów do %s: %d z %d obrazów, %d MB. Naciśnij przycisk powrotu, aby zatrzymać.",
    "USUŃ paczkę w %s (foldery ART zostają bez zmian)",
    "Usunąć paczkę ART w %s? Foldery ART zostają bez zmian.",
    "Zatrzymano. Niedokończona paczka została usunięta, a obrazy są wczytywane z folderów ART jak wcześniej.",
    "Nie udało się zapisać paczki ART w %s (czy na tym dysku jest miejsce?). Nic innego się nie zmieniło: obrazy są wczytywane z folderów ART jak wcześniej.",
    "Paczka ART w %s została usunięta. Obrazy znów są wczytywane z folderów ART.",
    "Paczka ART jest gotowa: %d obrazów, %d MB, w %s (%d s). Od teraz obrazy są wczytywane z niej, a dla %d gier, dla których ją zbudowano, ich folder ART nigdy więcej nie jest pytany obraz po obrazie. Obrazy, które RIPPS2 pobiera lub robi, pojawiają się od razu; te skopiowane z komputera pojawią się po ponownym zbudowaniu paczki.",
    "Na uruchomionych dyskach nie ma folderu ART z obrazami. Uruchom dyski, na których są twoje obrazy (SELECT na ich stronie), a potem wróć.",
]
T['Polish_l'] = {
    'RIPPS2_ART_PACK': "Paczka ART",
    'RIPPS2_ART_PACK_BUILD': "Zbuduj lub usuń",
    'HINT_RIPPS2_ART_PACK': "Pakuje folder ART każdego uruchomionego dysku do jednego art.tar na wybranym dysku (najszybszy jest proponowany pierwszy). Okładki są wtedy wczytywane z jednego pliku z jednym indeksem, nigdy z wyszukiwaniem dla każdej gry, więc menu i muzyka działają płynnie. Foldery ART zostają bez zmian.",
}

T['Czech'] = [
    "%d obrázků z %d složek ART půjde do jednoho souboru, %s. Složky ART zůstanou, jak jsou: balíček je kopie. art.tar můžeš zkopírovat do složky ART jiného disku pomocí Memory Files, ale nejrychlejší je postavit ho na disku, ze kterého procházíš, proto je nejrychlejší disk první. Postavit teď?",
    "%sART/art.tar: %d obrázků tam, čte %d KB/s",
    "%sART/art.tar: %d obrázků tam, čte %d KB/s, nejrychlejší",
    "Používá se: %s, %d obrázků, %d MB",
    "Prohlížení složek ART na spuštěných discích",
    "Měření, jak rychle každý disk čte své obrázky: %s",
    "Žádný: každý obrázek se čte z vlastní složky ART.",
    "Balení obrázků do %s: %d z %d obrázků, %d MB. Zastavíš tlačítkem zpět.",
    "ODSTRANIT balíček v %s (složky ART zůstanou, jak jsou)",
    "Odstranit balíček ART v %s? Složky ART zůstanou, jak jsou.",
    "Zastaveno. Nedokončený balíček byl odstraněn a obrázky se načítají ze složek ART jako dřív.",
    "Balíček ART se nepodařilo zapsat do %s (je na tom disku místo?). Nic jiného se nezměnilo: obrázky se načítají ze složek ART jako dřív.",
    "Balíček ART v %s je odstraněn. Obrázky se opět načítají ze složek ART.",
    "Balíček ART je hotový: %d obrázků, %d MB, v %s (%d s). Od teď se obrázky načítají z něj a u %d her, pro které byl postaven, se už jejich složky ART nikdy neptá obrázek po obrázku. Obrázky, které RIPPS2 stáhne nebo vyfotí, se ukážou hned; obrázky zkopírované z PC se ukážou, až balíček postavíš znovu.",
    "Na spuštěných discích není žádná složka ART s obrázky. Spusť disky, na kterých máš obrázky (SELECT na jejich stránce), a pak se vrať.",
]
T['Czech_l'] = {
    'RIPPS2_ART_PACK': "Balíček ART",
    'RIPPS2_ART_PACK_BUILD': "Postavit nebo odstranit",
    'HINT_RIPPS2_ART_PACK': "Zabalí složku ART každého spuštěného disku do jednoho art.tar na disku, který vybereš (nejrychlejší je nabídnut první). Obaly se pak načítají z jednoho souboru s jedním indexem, nikdy s hledáním pro každou hru, takže menu i hudba běží plynule. Složky ART zůstanou, jak jsou.",
}

T['Croatian'] = [
    "%d slika iz %d mapa ART ide u jednu datoteku, %s. Mape ART ostaju kakve jesu: paket je kopija. art.tar možeš kopirati u mapu ART drugog pogona pomoću Memory Files, ali najbrže je izraditi ga na pogonu s kojeg pregledavaš, zato je najbrži pogon prvi. Izraditi sada?",
    "%sART/art.tar: %d slika tamo, čita %d KB/s",
    "%sART/art.tar: %d slika tamo, čita %d KB/s, najbrži",
    "U upotrebi: %s, %d slika, %d MB",
    "Pregled mapa ART na pokrenutim pogonima",
    "Mjerenje koliko brzo svaki pogon čita svoje slike: %s",
    "Nijedan: svaka se slika čita iz vlastite mape ART.",
    "Pakiranje slika u %s: %d od %d slika, %d MB. Pritisni tipku za natrag za zaustavljanje.",
    "UKLONI paket u %s (mape ART ostaju kakve jesu)",
    "Ukloniti paket ART u %s? Mape ART ostaju kakve jesu.",
    "Zaustavljeno. Nedovršeni paket je uklonjen, a slike se učitavaju iz mapa ART kao prije.",
    "Paket ART nije se mogao zapisati u %s (ima li mjesta na tom pogonu?). Ništa se drugo nije promijenilo: slike se učitavaju iz mapa ART kao prije.",
    "Paket ART u %s je uklonjen. Slike se opet učitavaju iz mapa ART.",
    "Paket ART je izrađen: %d slika, %d MB, u %s (%d s). Slike se od sada učitavaju iz njega, a za %d igara za koje je izrađen njihova se mapa ART više nikad ne pita sliku po sliku. Slike koje RIPPS2 preuzme ili snimi odmah se vide; slike koje kopiraš s računala vide se kad ponovno izradiš paket.",
    "Na pokrenutim pogonima nema mape ART sa slikama. Pokreni pogone na kojima su tvoje slike (SELECT na njihovoj stranici), pa se vrati.",
]
T['Croatian_l'] = {
    'RIPPS2_ART_PACK': "Paket ART",
    'RIPPS2_ART_PACK_BUILD': "Izradi ili ukloni",
    'HINT_RIPPS2_ART_PACK': "Pakira mapu ART svakog pokrenutog pogona u jedan art.tar na pogonu koji odabereš (najbrži se nudi prvi). Omoti se tada učitavaju iz jedne datoteke s jednim indeksom, nikad pretragom za svaku igru, pa izbornici i glazba ostaju glatki. Mape ART ostaju kakve jesu.",
}

T['Serbian'] = [
    "%d slika iz %d fascikli ART ide u jednu datoteku, %s. Fascikle ART ostaju kakve jesu: paket je kopija. art.tar možeš da kopiraš u fasciklu ART drugog diska pomoću Memory Files, ali najbrže je da ga napraviš na disku sa kog pregledaš, zato je najbrži disk prvi. Napraviti sada?",
    "%sART/art.tar: %d slika tamo, čita %d KB/s",
    "%sART/art.tar: %d slika tamo, čita %d KB/s, najbrži",
    "U upotrebi: %s, %d slika, %d MB",
    "Pregled fascikli ART na pokrenutim diskovima",
    "Merenje koliko brzo svaki disk čita svoje slike: %s",
    "Nijedan: svaka slika se čita iz sopstvene fascikle ART.",
    "Pakovanje slika u %s: %d od %d slika, %d MB. Pritisni dugme za nazad da zaustaviš.",
    "UKLONI paket u %s (fascikle ART ostaju kakve jesu)",
    "Ukloniti paket ART u %s? Fascikle ART ostaju kakve jesu.",
    "Zaustavljeno. Nedovršeni paket je uklonjen, a slike se učitavaju iz fascikli ART kao ranije.",
    "Paket ART nije mogao da se upiše u %s (ima li mesta na tom disku?). Ništa drugo se nije promenilo: slike se učitavaju iz fascikli ART kao ranije.",
    "Paket ART u %s je uklonjen. Slike se ponovo učitavaju iz fascikli ART.",
    "Paket ART je napravljen: %d slika, %d MB, u %s (%d s). Slike se od sada učitavaju iz njega, a za %d igara za koje je napravljen njihova fascikla ART se više nikad ne pita sliku po sliku. Slike koje RIPPS2 preuzme ili snimi pojavljuju se odmah; slike koje kopiraš sa računara pojavljuju se kada ponovo napraviš paket.",
    "Na pokrenutim diskovima nema fascikle ART sa slikama. Pokreni diskove na kojima su tvoje slike (SELECT na njihovoj stranici), pa se vrati.",
]
T['Serbian_l'] = {
    'RIPPS2_ART_PACK': "Paket ART",
    'RIPPS2_ART_PACK_BUILD': "Napravi ili ukloni",
    'HINT_RIPPS2_ART_PACK': "Pakuje fasciklu ART svakog pokrenutog diska u jedan art.tar na disku koji izabereš (najbrži se nudi prvi). Omoti se tada učitavaju iz jedne datoteke sa jednim indeksom, nikad pretragom za svaku igru, pa meniji i muzika ostaju glatki. Fascikle ART ostaju kakve jesu.",
}

T['Romana'] = [
    "%d imagini din %d foldere ART intră într-un singur fișier, %s. Folderele ART rămân cum sunt: pachetul este o copie. Poți copia art.tar în folderul ART al altei unități cu Memory Files, dar cel mai rapid este să-l construiești pe unitatea de pe care navighezi, de aceea unitatea cea mai rapidă apare prima. Îl construiești acum?",
    "%sART/art.tar: %d imagini acolo, citește %d KB/s",
    "%sART/art.tar: %d imagini acolo, citește %d KB/s, cea mai rapidă",
    "În uz: %s, %d imagini, %d MB",
    "Se cercetează folderele ART de pe unitățile pornite",
    "Se măsoară cât de repede își citește fiecare unitate imaginile: %s",
    "Niciunul: fiecare imagine se citește din propriul folder ART.",
    "Se împachetează imaginile în %s: %d din %d imagini, %d MB. Apasă butonul înapoi ca să oprești.",
    "ȘTERGE pachetul din %s (folderele ART rămân cum sunt)",
    "Ștergi pachetul ART din %s? Folderele ART rămân cum sunt.",
    "Oprit. Pachetul neterminat a fost șters, iar imaginile se încarcă din folderele ART ca înainte.",
    "Pachetul ART nu a putut fi scris în %s (este loc pe acea unitate?). Nimic altceva nu s-a schimbat: imaginile se încarcă din folderele ART ca înainte.",
    "Pachetul ART din %s a fost șters. Imaginile se încarcă din nou din folderele ART.",
    "Pachetul ART este gata: %d imagini, %d MB, în %s (%d s). De acum imaginile se încarcă din el, iar pentru cele %d jocuri pentru care a fost construit folderul ART nu mai este întrebat niciodată imagine cu imagine. Imaginile pe care RIPPS2 le descarcă sau le captează apar imediat; cele copiate de pe un PC apar după ce construiești pachetul din nou.",
    "Nu există niciun folder ART cu imagini pe unitățile pornite. Pornește unitățile pe care sunt imaginile tale (SELECT pe pagina lor), apoi revino.",
]
T['Romana_l'] = {
    'RIPPS2_ART_PACK': "Pachet ART",
    'RIPPS2_ART_PACK_BUILD': "Construiește sau șterge",
    'HINT_RIPPS2_ART_PACK': "Pune folderul ART al fiecărei unități pornite într-un singur art.tar pe unitatea pe care o alegi (cea mai rapidă este oferită prima). Copertele se încarcă apoi dintr-un fișier cu un index, niciodată cu o căutare pentru fiecare joc, așa că meniurile și muzica rămân fluide. Folderele ART rămân cum sunt.",
}

T['Hungarian'] = [
    "%d kép %d ART mappából egyetlen fájlba kerül: %s. Az ART mappák maradnak, ahogy vannak: a csomag másolat. Az art.tar-t a Memory Files-szal átmásolhatod egy másik meghajtó ART mappájába, de az a leggyorsabb, ha azon a meghajtón építed meg, amelyről böngészel, ezért a leggyorsabb meghajtó áll elöl. Megépíted most?",
    "%sART/art.tar: ott %d kép, %d KB/s olvasás",
    "%sART/art.tar: ott %d kép, %d KB/s olvasás, a leggyorsabb",
    "Használatban: %s, %d kép, %d MB",
    "Az elindított meghajtók ART mappáinak átnézése",
    "Annak mérése, milyen gyorsan olvassa egy meghajtó a képeit: %s",
    "Nincs: minden kép a saját ART mappájából jön.",
    "A képek csomagolása ide: %s: %d / %d kép, %d MB. A vissza gombbal leállítható.",
    "A csomag TÖRLÉSE innen: %s (az ART mappák maradnak, ahogy vannak)",
    "Törlöd az ART csomagot innen: %s? Az ART mappák maradnak, ahogy vannak.",
    "Leállítva. A félkész csomag törölve, és a képek az ART mappákból jönnek, mint eddig.",
    "Az ART csomagot nem sikerült ide írni: %s (van hely azon a meghajtón?). Semmi más nem változott: a képek az ART mappákból jönnek, mint eddig.",
    "Az ART csomag törölve innen: %s. A képek ismét az ART mappákból jönnek.",
    "Az ART csomag elkészült: %d kép, %d MB, itt: %s (%d s). Mostantól a képek belőle jönnek, és annak a %d játéknak, amelyhez készült, az ART mappáját soha többé nem kérdezi képenként. A RIPPS2 által letöltött vagy készített képek azonnal megjelennek; a PC-ről bemásolt képek akkor jelennek meg, ha újra megépíted a csomagot.",
    "Az elindított meghajtókon nincs képeket tartalmazó ART mappa. Indítsd el azokat a meghajtókat, amelyeken a képeid vannak (SELECT az oldalukon), aztán gyere vissza.",
]
T['Hungarian_l'] = {
    'RIPPS2_ART_PACK': "ART csomag",
    'RIPPS2_ART_PACK_BUILD': "Építés vagy törlés",
    'HINT_RIPPS2_ART_PACK': "Minden elindított meghajtó ART mappáját egyetlen art.tar fájlba csomagolja a választott meghajtón (a leggyorsabbat kínálja elsőként). A borítók ezután egy fájlból, egy indexszel jönnek, soha nem játékonkénti kereséssel, így a menük és a zene zökkenőmentesek maradnak. Az ART mappák maradnak, ahogy vannak.",
}

os.makedirs(OUT, exist_ok=True)
for lang in [k for k in T if not k.endswith('_l')]:
    s = {str(i): v for i, v in enumerate(T[lang])}
    json.dump({'s': s, 'l': T[lang + '_l']}, open(os.path.join(OUT, lang + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('wrote', lang)
