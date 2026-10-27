"""Build 116 strings (s116.json) and labels: German, French, Spanish, Italian, Portuguese, Portuguese_BR, Dutch, Galician.
Run from the repo root: python tools/lang116/batch1.py (writes tr116/<Language>.json)."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'tr116')

T = {}

T['German'] = [
    " (Die gefundenen Konfigurationen wurden gesetzt: %s.)",
    " Speichere seine Einstellungen einmal mit seinem eigenen Konfigurator und schalte BOOT LOCK dann wieder ein.",
    "%s kann RIPPS2 nicht von seinem jetzigen Ort (%s) starten, und RIPPS2 kopiert sich nicht selbst. Lege RIPPS2.ELF auf eine Speicherkarte oder ein USB-Laufwerk und starte es von dort.",
    "BOOT LOCK konnte die Konfiguration des Bootloaders nicht schreiben. Prüfe, ob die Speicherkarte oder das Laufwerk schreibgeschützt ist, und versuche es erneut.",
    "BOOT LOCK fand keine Bootloader-Konfiguration zum Ändern.",
    "BOOT LOCK ist aus. Dein Bootloader startet wieder, was er vorher gestartet hat (%s).",
    "BOOT LOCK ist an. %s startet jetzt beim Einschalten RIPPS2 (%s), und ein leerer IGR-Pfad schickt das EXIT eines Spiels auf demselben Weg zurück. Halte beim Start der Konsole eine seiner Tasten, um etwas anderes zu erreichen.%s",
    "BOOT LOCK hat RIPPS2 an die erste Stelle im Menü von OSDMenu gesetzt (%s). OSDMenu startet von sich aus nichts: Wähle dort RIPPS2, und das EXIT eines Spiels führt zurück in dieses Menü. Für eine Konsole, die RIPPS2 sofort startet, legt BIBLE PS2BBL 1.2.0 auf eine Speicherkarte (Bootloader).",
    "BOOT LOCK arbeitet über einen Bootloader auf einer Speicherkarte (PS2BBL, FMCB oder OSDMenu), und hier gibt es keinen.",
    "Die Speicherkarte in Steckplatz %d startet beim Einschalten %s, und BOOT LOCK fand keine Konfiguration davon zum Ändern (gesucht wird %s).",
    "Die Speicherkarte in Steckplatz %d startet beim Einschalten %s, das BOOT LOCK nicht einstellen kann: Es arbeitet über PS2BBL, FMCB und OSDMenu.",
    "Auf dieser Konsole ist ein Bootloader mit der Sperre von RIPPS2.",
    "EXIT eines Spiels: der Browser, dann dein Bootloader (BOOT LOCK)",
]
T['German_l'] = {
    'HINT_EXITPATH': "Wohin EXIT im Menü im Spiel führt. Am besten leer lassen, mit BOOT LOCK an (PS2BBL, FMCB oder OSDMenu, oder BIBLE eingerichtet): EXIT führt dann über den Browser, der deinen Bootloader und RIPPS2 wie beim Einschalten startet, der sicherste Weg zurück. Leer ohne die Sperre: das eigene ELF von RIPPS2 auf einer Speicherkarte oder einem FAT32-USB-Laufwerk, direkt nach dem Reset geladen, wofür nicht jedes Spiel die Konsole bereit lässt. Browser: der PS2-Browser. Ein ELF auf MMCE ist dann gar nicht erreichbar.",
    'HINT_RIPPS2_BOOT_LOCK': "Startet RIPPS2 beim Einschalten über deinen Bootloader: PS2BBL und FMCB starten es sofort, OSDMenu setzt es an die erste Stelle seines Menüs, und das EXIT eines Spiels führt auf demselben Weg zurück. Aus stellt wieder her, was vorher da war. Noch keiner? Bootloader installiert BIBLE.",
}

T['French'] = [
    " (Les configurations trouvées ont été réglées : %s.)",
    " Enregistrez une fois ses réglages avec son propre configurateur, puis réactivez BOOT LOCK.",
    "%s ne peut pas lancer RIPPS2 depuis son emplacement actuel (%s), et RIPPS2 ne se copie pas. Mettez RIPPS2.ELF sur une carte mémoire ou une clé USB et lancez-le depuis là.",
    "BOOT LOCK n'a pas pu écrire la configuration du chargeur de démarrage. Vérifiez que la carte mémoire ou le lecteur n'est pas protégé en écriture, puis réessayez.",
    "BOOT LOCK n'a trouvé aucune configuration de chargeur de démarrage à modifier.",
    "BOOT LOCK est désactivé. Votre chargeur de démarrage lance ce qu'il lançait avant (%s).",
    "BOOT LOCK est activé. %s lance maintenant RIPPS2 à l'allumage (%s), et un Chemin IGR vide renvoie l'EXIT d'un jeu par le même chemin. Maintenez l'un de ses boutons pendant le démarrage de la console pour accéder à autre chose.%s",
    "BOOT LOCK a placé RIPPS2 en premier dans le menu d'OSDMenu (%s). OSDMenu ne lance rien de lui-même : choisissez RIPPS2 là, et l'EXIT d'un jeu revient à ce menu. Pour une console qui lance RIPPS2 tout de suite, BIBLE installe PS2BBL 1.2.0 sur une carte mémoire (Chargeur de démarrage).",
    "BOOT LOCK passe par un chargeur de démarrage sur une carte mémoire (PS2BBL, FMCB ou OSDMenu), et il n'y en a aucun ici.",
    "La carte mémoire du port %d lance %s à l'allumage, et BOOT LOCK n'a trouvé aucune de ses configurations à modifier (il cherche %s).",
    "La carte mémoire du port %d lance %s à l'allumage, que BOOT LOCK ne peut pas régler : il passe par PS2BBL, FMCB et OSDMenu.",
    "Un chargeur de démarrage avec le verrou de RIPPS2 est sur cette console.",
    "EXIT d'un jeu : le navigateur, puis votre chargeur de démarrage (BOOT LOCK)",
]
T['French_l'] = {
    'HINT_EXITPATH': "Où va EXIT dans le Menu en jeu. Mieux vaut le laisser vide avec BOOT LOCK activé (PS2BBL, FMCB ou OSDMenu, ou BIBLE installé) : EXIT passe alors par le navigateur, qui lance votre chargeur de démarrage et RIPPS2 comme à l'allumage, le retour le plus sûr. Vide sans le verrou : l'ELF de RIPPS2 lui-même sur une carte mémoire ou une clé USB FAT32, chargé juste après la réinitialisation, ce pour quoi tous les jeux ne laissent pas la console prête. Browser : le navigateur PS2. Un ELF sur MMCE n'est alors pas joignable du tout.",
    'HINT_RIPPS2_BOOT_LOCK': "Lance RIPPS2 à l'allumage via votre chargeur de démarrage : PS2BBL et FMCB le lancent tout de suite, OSDMenu le met en premier dans son menu, et l'EXIT d'un jeu revient par le même chemin. Désactivé remet ce qu'il y avait avant. Aucun encore ? Chargeur de démarrage installe BIBLE.",
}

T['Spanish'] = [
    " (Se ajustaron las configuraciones encontradas: %s.)",
    " Guarda sus ajustes una vez con su propio configurador y vuelve a activar BOOT LOCK.",
    "%s no puede iniciar RIPPS2 desde donde está ahora (%s), y RIPPS2 no se copia a sí mismo. Pon RIPPS2.ELF en una tarjeta de memoria o una unidad USB e inícialo desde allí.",
    "BOOT LOCK no pudo escribir la configuración del cargador de arranque. Comprueba que la tarjeta de memoria o la unidad no esté protegida contra escritura y vuelve a intentarlo.",
    "BOOT LOCK no encontró ninguna configuración de cargador de arranque que cambiar.",
    "BOOT LOCK está desactivado. Tu cargador de arranque inicia lo que iniciaba antes (%s).",
    "BOOT LOCK está activado. %s inicia ahora RIPPS2 al encender (%s), y una Ruta del IGR vacía devuelve el EXIT de un juego por el mismo camino. Mantén uno de sus botones mientras la consola arranca para llegar a otra cosa.%s",
    "BOOT LOCK puso RIPPS2 el primero en el menú de OSDMenu (%s). OSDMenu no inicia nada por sí mismo: elige RIPPS2 allí, y el EXIT de un juego vuelve a ese menú. Para una consola que inicie RIPPS2 al momento, BIBLE pone PS2BBL 1.2.0 en una tarjeta de memoria (Cargador de arranque).",
    "BOOT LOCK funciona a través de un cargador de arranque en una tarjeta de memoria (PS2BBL, FMCB u OSDMenu), y aquí no hay ninguno.",
    "La tarjeta de memoria de la ranura %d inicia %s al encender, y BOOT LOCK no encontró ninguna configuración suya que cambiar (busca %s).",
    "La tarjeta de memoria de la ranura %d inicia %s al encender, que BOOT LOCK no puede ajustar: funciona a través de PS2BBL, FMCB y OSDMenu.",
    "En esta consola hay un cargador de arranque con el bloqueo de RIPPS2.",
    "EXIT de un juego: el navegador, luego tu cargador de arranque (BOOT LOCK)",
]
T['Spanish_l'] = {
    'HINT_EXITPATH': "Adónde va EXIT en el Menú dentro del juego. Mejor dejarlo vacío con BOOT LOCK activado (PS2BBL, FMCB u OSDMenu, o BIBLE preparado): EXIT pasa entonces por el navegador, que inicia tu cargador de arranque y RIPPS2 como al encender, la vuelta más segura. Vacío sin el bloqueo: el propio ELF de RIPPS2 en una tarjeta de memoria o una unidad USB FAT32, cargado justo tras el reinicio, para lo que no todos los juegos dejan la consola preparada. Browser: el navegador de PS2. Un ELF en MMCE no se puede alcanzar entonces.",
    'HINT_RIPPS2_BOOT_LOCK': "Inicia RIPPS2 al encender a través de tu cargador de arranque: PS2BBL y FMCB lo inician al momento, OSDMenu lo pone el primero en su menú, y el EXIT de un juego vuelve por el mismo camino. Desactivado devuelve lo que había antes. ¿Aún ninguno? Cargador de arranque instala BIBLE.",
}

T['Italian'] = [
    " (Le configurazioni trovate sono state impostate: %s.)",
    " Salva una volta le sue impostazioni con il suo configuratore, poi riattiva BOOT LOCK.",
    "%s non può avviare RIPPS2 da dove si trova ora (%s), e RIPPS2 non si copia da solo. Metti RIPPS2.ELF su una memory card o un'unità USB e avvialo da lì.",
    "BOOT LOCK non ha potuto scrivere la configurazione del loader di avvio. Controlla che la memory card o l'unità non sia protetta da scrittura, poi riprova.",
    "BOOT LOCK non ha trovato nessuna configurazione del loader di avvio da modificare.",
    "BOOT LOCK è disattivo. Il tuo loader di avvio avvia ciò che avviava prima (%s).",
    "BOOT LOCK è attivo. %s ora avvia RIPPS2 all'accensione (%s), e un Percorso IGR vuoto riporta l'EXIT di un gioco per la stessa strada. Tieni premuto uno dei suoi tasti mentre la console si avvia per raggiungere altro.%s",
    "BOOT LOCK ha messo RIPPS2 per primo nel menu di OSDMenu (%s). OSDMenu non avvia nulla da solo: scegli RIPPS2 lì, e l'EXIT di un gioco torna a quel menu. Per una console che avvii subito RIPPS2, BIBLE mette PS2BBL 1.2.0 su una memory card (Loader di avvio).",
    "BOOT LOCK funziona tramite un loader di avvio su una memory card (PS2BBL, FMCB o OSDMenu), e qui non ce n'è nessuno.",
    "La memory card nello slot %d avvia %s all'accensione, e BOOT LOCK non ha trovato nessuna sua configurazione da modificare (cerca %s).",
    "La memory card nello slot %d avvia %s all'accensione, che BOOT LOCK non può impostare: funziona tramite PS2BBL, FMCB e OSDMenu.",
    "Su questa console c'è un loader di avvio con il blocco di RIPPS2.",
    "EXIT di un gioco: il browser, poi il tuo loader di avvio (BOOT LOCK)",
]
T['Italian_l'] = {
    'HINT_EXITPATH': "Dove porta EXIT nel Menu di gioco. Meglio lasciarlo vuoto con BOOT LOCK attivo (PS2BBL, FMCB o OSDMenu, o BIBLE impostato): EXIT passa allora dal browser, che avvia il tuo loader di avvio e RIPPS2 come all'accensione, il ritorno più sicuro. Vuoto senza il blocco: l'ELF di RIPPS2 stesso su una memory card o un'unità USB FAT32, caricato subito dopo il riavvio, per cui non tutti i giochi lasciano la console pronta. Browser: il browser della PS2. Un ELF su MMCE allora non è raggiungibile.",
    'HINT_RIPPS2_BOOT_LOCK': "Avvia RIPPS2 all'accensione tramite il tuo loader di avvio: PS2BBL e FMCB lo avviano subito, OSDMenu lo mette per primo nel suo menu, e l'EXIT di un gioco torna per la stessa strada. Disattivo rimette ciò che c'era prima. Ancora nessuno? Loader di avvio installa BIBLE.",
}

T['Portuguese'] = [
    " (As configurações encontradas foram definidas: %s.)",
    " Guarde as definições dele uma vez com o seu próprio configurador e volte a ativar o BOOT LOCK.",
    "%s não consegue iniciar o RIPPS2 a partir de onde está agora (%s), e o RIPPS2 não se copia a si próprio. Coloque o RIPPS2.ELF num cartão de memória ou numa unidade USB e inicie-o a partir daí.",
    "O BOOT LOCK não conseguiu escrever a configuração do carregador de arranque. Verifique se o cartão de memória ou a unidade não está protegido contra escrita e tente novamente.",
    "O BOOT LOCK não encontrou nenhuma configuração de carregador de arranque para alterar.",
    "O BOOT LOCK está desativado. O seu carregador de arranque inicia o que iniciava antes (%s).",
    "O BOOT LOCK está ativado. %s inicia agora o RIPPS2 ao ligar (%s), e, com «Definir saída do IGR» vazio, o EXIT de um jogo volta pelo mesmo caminho. Segure um dos botões dele enquanto a consola inicia para chegar a outra coisa.%s",
    "O BOOT LOCK pôs o RIPPS2 em primeiro no menu do OSDMenu (%s). O OSDMenu não inicia nada sozinho: escolha lá o RIPPS2, e o EXIT de um jogo volta a esse menu. Para uma consola que inicie o RIPPS2 logo, o BIBLE coloca o PS2BBL 1.2.0 num cartão de memória (Carregador de arranque).",
    "O BOOT LOCK funciona através de um carregador de arranque num cartão de memória (PS2BBL, FMCB ou OSDMenu), e aqui não há nenhum.",
    "O cartão de memória da ranhura %d inicia %s ao ligar, e o BOOT LOCK não encontrou nenhuma configuração dele para alterar (procura %s).",
    "O cartão de memória da ranhura %d inicia %s ao ligar, que o BOOT LOCK não consegue definir: funciona através do PS2BBL, FMCB e OSDMenu.",
    "Há nesta consola um carregador de arranque com o bloqueio do RIPPS2.",
    "EXIT de um jogo: o navegador, depois o seu carregador de arranque (BOOT LOCK)",
]
T['Portuguese_l'] = {
    'HINT_EXITPATH': "Para onde vai o EXIT no Menu no jogo. É melhor deixar vazio com o BOOT LOCK ativado (PS2BBL, FMCB ou OSDMenu, ou o BIBLE preparado): o EXIT passa então pelo navegador, que inicia o seu carregador de arranque e o RIPPS2 como ao ligar, o regresso mais seguro. Vazio sem o bloqueio: o próprio ELF do RIPPS2 num cartão de memória ou numa unidade USB FAT32, carregado logo após o reinício, para o qual nem todos os jogos deixam a consola pronta. Browser: o navegador da PS2. Um ELF no MMCE não fica então acessível.",
    'HINT_RIPPS2_BOOT_LOCK': "Inicia o RIPPS2 ao ligar através do seu carregador de arranque: o PS2BBL e o FMCB iniciam-no logo, o OSDMenu põe-no em primeiro no seu menu, e o EXIT de um jogo volta pelo mesmo caminho. Desligado devolve o que lá estava antes. Ainda nenhum? Carregador de arranque instala o BIBLE.",
}

T['Portuguese_BR'] = [
    " (As configurações encontradas foram definidas: %s.)",
    " Salve as configurações dele uma vez com o próprio configurador e ative o BOOT LOCK de novo.",
    "%s não consegue iniciar o RIPPS2 de onde ele está agora (%s), e o RIPPS2 não se copia. Coloque o RIPPS2.ELF num memory card ou numa unidade USB e inicie-o de lá.",
    "O BOOT LOCK não conseguiu gravar a configuração do carregador de boot. Verifique se o memory card ou a unidade não está protegido contra gravação e tente de novo.",
    "O BOOT LOCK não encontrou nenhuma configuração de carregador de boot para alterar.",
    "O BOOT LOCK está desativado. Seu carregador de boot inicia o que iniciava antes (%s).",
    "O BOOT LOCK está ativado. %s agora inicia o RIPPS2 ao ligar (%s), e um Caminho de Saída do IGR vazio manda o EXIT de um jogo de volta pelo mesmo caminho. Segure um dos botões dele enquanto o console inicia para chegar a outra coisa.%s",
    "O BOOT LOCK colocou o RIPPS2 em primeiro no menu do OSDMenu (%s). O OSDMenu não inicia nada sozinho: escolha o RIPPS2 lá, e o EXIT de um jogo volta para esse menu. Para um console que inicie o RIPPS2 na hora, o BIBLE coloca o PS2BBL 1.2.0 num memory card (Carregador de boot).",
    "O BOOT LOCK funciona por meio de um carregador de boot num memory card (PS2BBL, FMCB ou OSDMenu), e aqui não há nenhum.",
    "O memory card do slot %d inicia %s ao ligar, e o BOOT LOCK não encontrou nenhuma configuração dele para alterar (ele procura %s).",
    "O memory card do slot %d inicia %s ao ligar, que o BOOT LOCK não consegue configurar: ele funciona por meio do PS2BBL, FMCB e OSDMenu.",
    "Há neste console um carregador de boot com o bloqueio do RIPPS2.",
    "EXIT de um jogo: o navegador, depois seu carregador de boot (BOOT LOCK)",
]
T['Portuguese_BR_l'] = {
    'HINT_EXITPATH': "Para onde vai o EXIT no Menu no jogo. Melhor deixar vazio com o BOOT LOCK ativado (PS2BBL, FMCB ou OSDMenu, ou o BIBLE preparado): o EXIT então passa pelo navegador, que inicia seu carregador de boot e o RIPPS2 como ao ligar, o retorno mais seguro. Vazio sem o bloqueio: o próprio ELF do RIPPS2 num memory card ou numa unidade USB FAT32, carregado logo depois do reinício, para o qual nem todo jogo deixa o console pronto. Browser: o navegador do PS2. Um ELF no MMCE então não pode ser acessado.",
    'HINT_RIPPS2_BOOT_LOCK': "Inicia o RIPPS2 ao ligar pelo seu carregador de boot: o PS2BBL e o FMCB o iniciam na hora, o OSDMenu o coloca em primeiro no menu dele, e o EXIT de um jogo volta pelo mesmo caminho. Desligado devolve o que havia antes. Ainda nenhum? Carregador de boot instala o BIBLE.",
}

T['Dutch'] = [
    " (De gevonden configuraties zijn ingesteld: %s.)",
    " Sla de instellingen ervan één keer op met de eigen configurator en zet BOOT LOCK dan opnieuw aan.",
    "%s kan RIPPS2 niet starten vanaf de plek waar het nu staat (%s), en RIPPS2 kopieert zichzelf niet. Zet RIPPS2.ELF op een geheugenkaart of een USB-schijf en start het daarvandaan.",
    "BOOT LOCK kon de configuratie van de opstartlader niet schrijven. Controleer of de geheugenkaart of schijf niet tegen schrijven beveiligd is en probeer het opnieuw.",
    "BOOT LOCK vond geen configuratie van een opstartlader om te wijzigen.",
    "BOOT LOCK staat uit. Je opstartlader start wat hij eerder startte (%s).",
    "BOOT LOCK staat aan. %s start RIPPS2 nu bij aanzetten (%s), en een leeg IGR pad stuurt de EXIT van een game langs dezelfde weg terug. Houd een van zijn knoppen ingedrukt terwijl de console start om iets anders te bereiken.%s",
    "BOOT LOCK heeft RIPPS2 bovenaan het menu van OSDMenu gezet (%s). OSDMenu start uit zichzelf niets: kies daar RIPPS2, en de EXIT van een game komt terug in dat menu. Voor een console die RIPPS2 meteen start, zet BIBLE PS2BBL 1.2.0 op een geheugenkaart (Opstartlader).",
    "BOOT LOCK werkt via een opstartlader op een geheugenkaart (PS2BBL, FMCB of OSDMenu), en die is hier niet.",
    "De geheugenkaart in sleuf %d start %s bij aanzetten, en BOOT LOCK vond geen configuratie ervan om te wijzigen (het zoekt %s).",
    "De geheugenkaart in sleuf %d start %s bij aanzetten, wat BOOT LOCK niet kan instellen: het werkt via PS2BBL, FMCB en OSDMenu.",
    "Op deze console staat een opstartlader met de vergrendeling van RIPPS2.",
    "EXIT van een game: de browser, dan je opstartlader (BOOT LOCK)",
]
T['Dutch_l'] = {
    'HINT_EXITPATH': "Waar EXIT in het Menu in game heen gaat. Het best leeg gelaten met BOOT LOCK aan (PS2BBL, FMCB of OSDMenu, of BIBLE ingesteld): EXIT gaat dan via de browser, die je opstartlader en RIPPS2 start zoals bij aanzetten, de veiligste weg terug. Leeg zonder de vergrendeling: de eigen ELF van RIPPS2 op een geheugenkaart of een FAT32-USB-schijf, direct na de reset geladen, waarvoor niet elke game de console klaar laat. Browser: de PS2-browser. Een ELF op MMCE is dan helemaal niet bereikbaar.",
    'HINT_RIPPS2_BOOT_LOCK': "Start RIPPS2 bij aanzetten via je opstartlader: PS2BBL en FMCB starten het meteen, OSDMenu zet het bovenaan zijn menu, en de EXIT van een game gaat langs dezelfde weg terug. Uit zet terug wat er eerder was. Nog geen? Opstartlader installeert BIBLE.",
}

T['Galician'] = [
    " (Axustáronse as configuracións atopadas: %s.)",
    " Garda os seus axustes unha vez co seu propio configurador e volve activar BOOT LOCK.",
    "%s non pode iniciar RIPPS2 desde onde está agora (%s), e RIPPS2 non se copia a si mesmo. Pon RIPPS2.ELF nunha tarxeta de memoria ou nunha unidade USB e inícialo desde alí.",
    "BOOT LOCK non puido escribir a configuración do cargador de arranque. Comproba que a tarxeta de memoria ou a unidade non estea protexida contra escritura e volve tentalo.",
    "BOOT LOCK non atopou ningunha configuración de cargador de arranque que cambiar.",
    "BOOT LOCK está desactivado. O teu cargador de arranque inicia o que iniciaba antes (%s).",
    "BOOT LOCK está activado. %s inicia agora RIPPS2 ao acender (%s), e unha Ruta do IGR baleira devolve o EXIT dun xogo polo mesmo camiño. Mantén un dos seus botóns mentres a consola arrinca para chegar a calquera outra cousa.%s",
    "BOOT LOCK puxo RIPPS2 o primeiro no menú de OSDMenu (%s). OSDMenu non inicia nada por si mesmo: escolle alí RIPPS2, e o EXIT dun xogo volve a ese menú. Para unha consola que inicie RIPPS2 de inmediato, BIBLE pon PS2BBL 1.2.0 nunha tarxeta de memoria (Cargador de arranque).",
    "BOOT LOCK funciona a través dun cargador de arranque nunha tarxeta de memoria (PS2BBL, FMCB ou OSDMenu), e aquí non hai ningún.",
    "A tarxeta de memoria da rañura %d inicia %s ao acender, e BOOT LOCK non atopou ningunha configuración súa que cambiar (busca %s).",
    "A tarxeta de memoria da rañura %d inicia %s ao acender, que BOOT LOCK non pode axustar: funciona a través de PS2BBL, FMCB e OSDMenu.",
    "Nesta consola hai un cargador de arranque co bloqueo de RIPPS2.",
    "EXIT dun xogo: o navegador, despois o teu cargador de arranque (BOOT LOCK)",
]
T['Galician_l'] = {
    'HINT_EXITPATH': "A onde vai EXIT no Menú no xogo. Mellor deixalo baleiro con BOOT LOCK activado (PS2BBL, FMCB ou OSDMenu, ou BIBLE preparado): EXIT pasa entón polo navegador, que inicia o teu cargador de arranque e RIPPS2 coma ao acender, a volta máis segura. Baleiro sen o bloqueo: o propio ELF de RIPPS2 nunha tarxeta de memoria ou nunha unidade USB FAT32, cargado xusto tras o reinicio, para o que non todos os xogos deixan a consola preparada. Browser: o navegador da PS2. Un ELF en MMCE non se pode alcanzar entón.",
    'HINT_RIPPS2_BOOT_LOCK': "Inicia RIPPS2 ao acender a través do teu cargador de arranque: PS2BBL e FMCB inícino de inmediato, OSDMenu pono o primeiro no seu menú, e o EXIT dun xogo volve polo mesmo camiño. Desactivado repón o que había antes. Aínda ningún? Cargador de arranque instala BIBLE.",
}

os.makedirs(OUT, exist_ok=True)
for lang in [k for k in T if not k.endswith('_l')]:
    s = {str(i): v for i, v in enumerate(T[lang])}
    json.dump({'s': s, 'l': T[lang + '_l']}, open(os.path.join(OUT, lang + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(lang, len(s))
