"""Build 118 strings (s118.json) and labels: German, French, Spanish, Italian, Portuguese, Portuguese_BR, Dutch, Galician.
Run from the repo root: python tools/lang118/batch1.py (writes tr118/<Language>.json)."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'tr118')

T = {}

T['German'] = [
    "%d Bilder aus %d ART-Ordnern kommen in eine Datei, %s. Die ART-Ordner bleiben, wie sie sind: Das Paket ist eine Kopie. Du kannst art.tar mit Memory Files in den ART-Ordner eines anderen Laufwerks kopieren, aber am schnellsten ist es, das Paket auf dem Laufwerk zu bauen, auf dem du stöberst, deshalb steht das schnellste Laufwerk oben. Jetzt bauen?",
    "%sART/art.tar: %d Bilder dort, liest %d KB/s",
    "%sART/art.tar: %d Bilder dort, liest %d KB/s, das schnellste",
    "In Gebrauch: %s, %d Bilder, %d MB",
    "Die ART-Ordner auf den gestarteten Laufwerken werden angesehen",
    "Es wird gemessen, wie schnell jedes Laufwerk seine Bilder liest: %s",
    "Keins: Jedes Bild wird aus seinem eigenen ART-Ordner gelesen.",
    "Die Bilder werden in %s gepackt: %d von %d Bildern, %d MB. Drücke die Zurück-Taste zum Anhalten.",
    "Das Paket in %s ENTFERNEN (die ART-Ordner bleiben, wie sie sind)",
    "Das ART-Paket in %s entfernen? Die ART-Ordner bleiben, wie sie sind.",
    "Angehalten. Das unfertige Paket wurde entfernt, und die Bilder kommen wie zuvor aus den ART-Ordnern.",
    "Das ART-Paket konnte nicht nach %s geschrieben werden (ist auf dem Laufwerk Platz?). Sonst hat sich nichts geändert: Die Bilder kommen wie zuvor aus den ART-Ordnern.",
    "Das ART-Paket in %s ist entfernt. Die Bilder kommen wieder aus den ART-Ordnern.",
    "Das ART-Paket ist gebaut: %d Bilder, %d MB, in %s (%d s). Die Bilder kommen ab jetzt daraus, und bei den %d Spielen, für die es gebaut wurde, wird ihr ART-Ordner nie mehr Bild für Bild gefragt. Bilder, die RIPPS2 holt oder aufnimmt, erscheinen sofort; Bilder, die du am PC hineinkopierst, erscheinen, wenn du das Paket neu baust.",
    "Auf den gestarteten Laufwerken gibt es keinen ART-Ordner mit Bildern. Starte die Laufwerke mit deinen Bildern (SELECT auf ihrer Seite) und komm dann zurück.",
]
T['German_l'] = {
    'RIPPS2_ART_PACK': "ART-Paket",
    'RIPPS2_ART_PACK_BUILD': "Bauen oder entfernen",
    'HINT_RIPPS2_ART_PACK': "Packt den ART-Ordner jedes gestarteten Laufwerks in eine art.tar auf dem Laufwerk deiner Wahl (das schnellste wird zuerst angeboten). Die Cover kommen dann aus einer Datei mit einem Index, nie mit einer Suche pro Spiel, sodass die Menüs und die Musik flüssig bleiben. Die ART-Ordner bleiben, wie sie sind.",
}

T['French'] = [
    "%d images de %d dossiers ART vont dans un seul fichier, %s. Les dossiers ART restent tels quels : le pack est une copie. Tu peux copier art.tar dans le dossier ART d'un autre périphérique avec Memory Files, mais le construire sur le périphérique où tu navigues est le plus rapide, c'est pourquoi le périphérique le plus rapide est proposé en premier. Le construire maintenant ?",
    "%sART/art.tar : %d images ici, lit %d Ko/s",
    "%sART/art.tar : %d images ici, lit %d Ko/s, le plus rapide",
    "Utilisé : %s, %d images, %d Mo",
    "Lecture des dossiers ART des périphériques démarrés",
    "Mesure de la vitesse à laquelle chaque périphérique lit ses images : %s",
    "Aucun : chaque image est lue dans son propre dossier ART.",
    "Les images vont dans %s : %d sur %d images, %d Mo. Appuie sur le bouton retour pour arrêter.",
    "SUPPRIMER le pack de %s (les dossiers ART restent tels quels)",
    "Supprimer le pack ART de %s ? Les dossiers ART restent tels quels.",
    "Arrêté. Le pack inachevé a été supprimé, et les images viennent des dossiers ART comme avant.",
    "Le pack ART n'a pas pu être écrit dans %s (y a-t-il de la place sur ce périphérique ?). Rien d'autre n'a changé : les images viennent des dossiers ART comme avant.",
    "Le pack ART de %s est supprimé. Les images viennent de nouveau des dossiers ART.",
    "Le pack ART est construit : %d images, %d Mo, dans %s (%d s). Les images viennent de lui désormais, et les %d jeux pour lesquels il a été construit ne voient plus jamais leur dossier ART interrogé image par image. Les images que RIPPS2 télécharge ou capture s'affichent tout de suite ; celles que tu copies depuis un PC s'affichent quand tu reconstruis le pack.",
    "Aucun dossier ART avec des images sur les périphériques démarrés. Démarre les périphériques où sont tes images (SELECT sur leur page), puis reviens.",
]
T['French_l'] = {
    'RIPPS2_ART_PACK': "Pack ART",
    'RIPPS2_ART_PACK_BUILD': "Construire ou supprimer",
    'HINT_RIPPS2_ART_PACK': "Met le dossier ART de chaque périphérique démarré dans un seul art.tar sur le périphérique choisi (le plus rapide est proposé en premier). Les jaquettes viennent alors d'un seul fichier avec un seul index, jamais d'une recherche par jeu, et les menus comme la musique restent fluides. Les dossiers ART restent tels quels.",
}

T['Spanish'] = [
    "%d imágenes de %d carpetas ART van a un solo archivo, %s. Las carpetas ART quedan como están: el paquete es una copia. Puedes copiar art.tar a la carpeta ART de otra unidad con Memory Files, pero crearlo en la unidad desde la que navegas es lo más rápido, por eso la unidad más rápida aparece primero. ¿Crearlo ahora?",
    "%sART/art.tar: %d imágenes allí, lee %d KB/s",
    "%sART/art.tar: %d imágenes allí, lee %d KB/s, la más rápida",
    "En uso: %s, %d imágenes, %d MB",
    "Revisando las carpetas ART de las unidades iniciadas",
    "Midiendo qué tan rápido lee cada unidad sus imágenes: %s",
    "Ninguno: cada imagen se lee de su propia carpeta ART.",
    "Empaquetando las imágenes en %s: %d de %d imágenes, %d MB. Pulsa el botón de volver para detener.",
    "QUITAR el paquete de %s (las carpetas ART quedan como están)",
    "¿Quitar el paquete ART de %s? Las carpetas ART quedan como están.",
    "Detenido. Se quitó el paquete sin terminar, y las imágenes se cargan de las carpetas ART como antes.",
    "No se pudo escribir el paquete ART en %s (¿hay espacio en esa unidad?). Nada más cambió: las imágenes se cargan de las carpetas ART como antes.",
    "Se quitó el paquete ART de %s. Las imágenes vuelven a cargarse de las carpetas ART.",
    "El paquete ART está listo: %d imágenes, %d MB, en %s (%d s). Las imágenes se cargan de él a partir de ahora, y a los %d juegos para los que se creó nunca se les pregunta a su carpeta ART imagen por imagen. Las imágenes que RIPPS2 descarga o captura aparecen al momento; las que copias desde un PC aparecen cuando vuelves a crear el paquete.",
    "No hay ninguna carpeta ART con imágenes en las unidades iniciadas. Inicia las unidades donde están tus imágenes (SELECT en su página) y luego vuelve.",
]
T['Spanish_l'] = {
    'RIPPS2_ART_PACK': "Paquete ART",
    'RIPPS2_ART_PACK_BUILD': "Crear o quitar",
    'HINT_RIPPS2_ART_PACK': "Junta la carpeta ART de cada unidad iniciada en un solo art.tar en la unidad que elijas (la más rápida se ofrece primero). Las carátulas se cargan entonces de un archivo con un índice, nunca con una búsqueda por juego, y los menús y la música van fluidos. Las carpetas ART quedan como están.",
}

T['Italian'] = [
    "%d immagini da %d cartelle ART vanno in un solo file, %s. Le cartelle ART restano come sono: il pacchetto è una copia. Puoi copiare art.tar nella cartella ART di un'altra unità con Memory Files, ma crearlo sull'unità da cui navighi è la cosa più rapida, per questo l'unità più veloce è in cima. Crearlo adesso?",
    "%sART/art.tar: %d immagini lì, legge %d KB/s",
    "%sART/art.tar: %d immagini lì, legge %d KB/s, la più veloce",
    "In uso: %s, %d immagini, %d MB",
    "Controllo delle cartelle ART sulle unità avviate",
    "Misura di quanto velocemente ogni unità legge le sue immagini: %s",
    "Nessuno: ogni immagine viene letta dalla sua cartella ART.",
    "Le immagini vanno in %s: %d di %d immagini, %d MB. Premi il tasto indietro per fermare.",
    "RIMUOVI il pacchetto in %s (le cartelle ART restano come sono)",
    "Rimuovere il pacchetto ART in %s? Le cartelle ART restano come sono.",
    "Fermato. Il pacchetto incompleto è stato rimosso, e le immagini arrivano dalle cartelle ART come prima.",
    "Non è stato possibile scrivere il pacchetto ART in %s (c'è spazio su quell'unità?). Nient'altro è cambiato: le immagini arrivano dalle cartelle ART come prima.",
    "Il pacchetto ART in %s è stato rimosso. Le immagini arrivano di nuovo dalle cartelle ART.",
    "Il pacchetto ART è pronto: %d immagini, %d MB, in %s (%d s). Da ora le immagini arrivano da lì, e per i %d giochi per cui è stato creato la loro cartella ART non viene mai più interrogata immagine per immagine. Le immagini che RIPPS2 scarica o cattura compaiono subito; quelle che copi da un PC compaiono quando ricrei il pacchetto.",
    "Sulle unità avviate non c'è una cartella ART con immagini. Avvia le unità dove sono le tue immagini (SELECT sulla loro pagina), poi torna qui.",
]
T['Italian_l'] = {
    'RIPPS2_ART_PACK': "Pacchetto ART",
    'RIPPS2_ART_PACK_BUILD': "Crea o rimuovi",
    'HINT_RIPPS2_ART_PACK': "Mette la cartella ART di ogni unità avviata in un solo art.tar sull'unità che scegli (la più veloce è proposta per prima). Le copertine arrivano poi da un file con un indice, mai con una ricerca per gioco, così i menu e la musica restano fluidi. Le cartelle ART restano come sono.",
}

T['Portuguese'] = [
    "%d imagens de %d pastas ART vão para um único ficheiro, %s. As pastas ART ficam como estão: o pacote é uma cópia. Podes copiar art.tar para a pasta ART de outra unidade com o Memory Files, mas criá-lo na unidade onde navegas é o mais rápido, por isso a unidade mais rápida aparece primeiro. Criar agora?",
    "%sART/art.tar: %d imagens lá, lê %d KB/s",
    "%sART/art.tar: %d imagens lá, lê %d KB/s, a mais rápida",
    "Em uso: %s, %d imagens, %d MB",
    "A ver as pastas ART das unidades iniciadas",
    "A medir quão depressa cada unidade lê as suas imagens: %s",
    "Nenhum: cada imagem é lida da sua própria pasta ART.",
    "A juntar as imagens em %s: %d de %d imagens, %d MB. Carrega no botão de voltar para parar.",
    "REMOVER o pacote em %s (as pastas ART ficam como estão)",
    "Remover o pacote ART em %s? As pastas ART ficam como estão.",
    "Parado. O pacote inacabado foi removido, e as imagens vêm das pastas ART como antes.",
    "Não foi possível escrever o pacote ART em %s (há espaço nessa unidade?). Mais nada mudou: as imagens vêm das pastas ART como antes.",
    "O pacote ART em %s foi removido. As imagens voltam a vir das pastas ART.",
    "O pacote ART está pronto: %d imagens, %d MB, em %s (%d s). A partir de agora as imagens vêm dele, e os %d jogos para os quais foi criado nunca mais têm a sua pasta ART consultada imagem a imagem. As imagens que o RIPPS2 descarrega ou capta aparecem logo; as que copias de um PC aparecem quando voltas a criar o pacote.",
    "Não há nenhuma pasta ART com imagens nas unidades iniciadas. Inicia as unidades onde estão as tuas imagens (SELECT na página delas) e depois volta.",
]
T['Portuguese_l'] = {
    'RIPPS2_ART_PACK': "Pacote ART",
    'RIPPS2_ART_PACK_BUILD': "Criar ou remover",
    'HINT_RIPPS2_ART_PACK': "Junta a pasta ART de cada unidade iniciada num único art.tar na unidade que escolheres (a mais rápida é oferecida primeiro). As capas passam a vir de um ficheiro com um índice, nunca de uma procura por jogo, e os menus e a música ficam fluidos. As pastas ART ficam como estão.",
}

T['Portuguese_BR'] = [
    "%d imagens de %d pastas ART vão para um único arquivo, %s. As pastas ART ficam como estão: o pacote é uma cópia. Você pode copiar art.tar para a pasta ART de outra unidade com o Memory Files, mas criar o pacote na unidade em que você navega é o mais rápido, por isso a unidade mais rápida aparece primeiro. Criar agora?",
    "%sART/art.tar: %d imagens lá, lê %d KB/s",
    "%sART/art.tar: %d imagens lá, lê %d KB/s, a mais rápida",
    "Em uso: %s, %d imagens, %d MB",
    "Olhando as pastas ART das unidades iniciadas",
    "Medindo a velocidade com que cada unidade lê suas imagens: %s",
    "Nenhum: cada imagem é lida da sua própria pasta ART.",
    "Juntando as imagens em %s: %d de %d imagens, %d MB. Aperte o botão de voltar para parar.",
    "REMOVER o pacote em %s (as pastas ART ficam como estão)",
    "Remover o pacote ART em %s? As pastas ART ficam como estão.",
    "Parado. O pacote inacabado foi removido, e as imagens vêm das pastas ART como antes.",
    "Não foi possível gravar o pacote ART em %s (tem espaço nessa unidade?). Nada mais mudou: as imagens vêm das pastas ART como antes.",
    "O pacote ART em %s foi removido. As imagens voltam a vir das pastas ART.",
    "O pacote ART está pronto: %d imagens, %d MB, em %s (%d s). De agora em diante as imagens vêm dele, e os %d jogos para os quais ele foi criado nunca mais têm a pasta ART consultada imagem por imagem. As imagens que o RIPPS2 baixa ou captura aparecem na hora; as que você copia de um PC aparecem quando você cria o pacote de novo.",
    "Não há nenhuma pasta ART com imagens nas unidades iniciadas. Inicie as unidades onde estão suas imagens (SELECT na página delas) e depois volte.",
]
T['Portuguese_BR_l'] = {
    'RIPPS2_ART_PACK': "Pacote ART",
    'RIPPS2_ART_PACK_BUILD': "Criar ou remover",
    'HINT_RIPPS2_ART_PACK': "Junta a pasta ART de cada unidade iniciada em um único art.tar na unidade que você escolher (a mais rápida é oferecida primeiro). As capas passam a vir de um arquivo com um índice, nunca de uma busca por jogo, e os menus e a música ficam fluidos. As pastas ART ficam como estão.",
}

T['Dutch'] = [
    "%d afbeeldingen uit %d ART-mappen gaan in één bestand, %s. De ART-mappen blijven zoals ze zijn: het pakket is een kopie. Je kunt art.tar met Memory Files naar de ART-map van een ander station kopiëren, maar het bouwen op het station waar je doorheen bladert is het snelst, daarom staat het snelste station bovenaan. Nu bouwen?",
    "%sART/art.tar: %d afbeeldingen daar, leest %d KB/s",
    "%sART/art.tar: %d afbeeldingen daar, leest %d KB/s, het snelst",
    "In gebruik: %s, %d afbeeldingen, %d MB",
    "De ART-mappen op de gestarte stations worden bekeken",
    "Meten hoe snel elk station zijn afbeeldingen leest: %s",
    "Geen: elke afbeelding wordt uit zijn eigen ART-map gelezen.",
    "De afbeeldingen gaan in %s: %d van %d afbeeldingen, %d MB. Druk op de terugknop om te stoppen.",
    "Het pakket in %s VERWIJDEREN (de ART-mappen blijven zoals ze zijn)",
    "Het ART-pakket in %s verwijderen? De ART-mappen blijven zoals ze zijn.",
    "Gestopt. Het onvoltooide pakket is verwijderd, en de afbeeldingen komen zoals eerder uit de ART-mappen.",
    "Het ART-pakket kon niet naar %s worden geschreven (is er ruimte op dat station?). Verder is er niets veranderd: de afbeeldingen komen zoals eerder uit de ART-mappen.",
    "Het ART-pakket in %s is verwijderd. De afbeeldingen komen weer uit de ART-mappen.",
    "Het ART-pakket is gebouwd: %d afbeeldingen, %d MB, in %s (%d s). De afbeeldingen komen er voortaan uit, en bij de %d games waarvoor het gebouwd is, wordt hun ART-map nooit meer afbeelding voor afbeelding gevraagd. Afbeeldingen die RIPPS2 ophaalt of vastlegt, verschijnen meteen; afbeeldingen die je op een pc erin kopieert, verschijnen als je het pakket opnieuw bouwt.",
    "Er is geen ART-map met afbeeldingen op de gestarte stations. Start de stations waar je afbeeldingen op staan (SELECT op hun pagina) en kom dan terug.",
]
T['Dutch_l'] = {
    'RIPPS2_ART_PACK': "ART-pakket",
    'RIPPS2_ART_PACK_BUILD': "Bouwen of verwijderen",
    'HINT_RIPPS2_ART_PACK': "Zet de ART-map van elk gestart station in één art.tar op het station dat je kiest (het snelste wordt eerst aangeboden). De covers komen dan uit één bestand met één index, nooit met een zoektocht per game, zodat de menu's en de muziek soepel blijven. De ART-mappen blijven zoals ze zijn.",
}

T['Galician'] = [
    "%d imaxes de %d cartafoles ART van a un só ficheiro, %s. Os cartafoles ART quedan como están: o paquete é unha copia. Podes copiar art.tar ao cartafol ART doutra unidade con Memory Files, pero crealo na unidade desde a que navegas é o máis rápido, por iso a unidade máis rápida aparece primeiro. Crealo agora?",
    "%sART/art.tar: %d imaxes alí, le %d KB/s",
    "%sART/art.tar: %d imaxes alí, le %d KB/s, a máis rápida",
    "En uso: %s, %d imaxes, %d MB",
    "Revisando os cartafoles ART das unidades iniciadas",
    "Medindo a que velocidade le cada unidade as súas imaxes: %s",
    "Ningún: cada imaxe lese do seu propio cartafol ART.",
    "Empaquetando as imaxes en %s: %d de %d imaxes, %d MB. Preme o botón de volver para deter.",
    "QUITAR o paquete de %s (os cartafoles ART quedan como están)",
    "Quitar o paquete ART de %s? Os cartafoles ART quedan como están.",
    "Detido. Quitouse o paquete sen rematar, e as imaxes cárganse dos cartafoles ART coma antes.",
    "Non se puido escribir o paquete ART en %s (hai espazo nesa unidade?). Nada máis cambiou: as imaxes cárganse dos cartafoles ART coma antes.",
    "Quitouse o paquete ART de %s. As imaxes volven cargarse dos cartafoles ART.",
    "O paquete ART está listo: %d imaxes, %d MB, en %s (%d s). As imaxes cárganse del a partir de agora, e aos %d xogos para os que se creou nunca máis se lles pregunta ao seu cartafol ART imaxe por imaxe. As imaxes que RIPPS2 descarga ou captura aparecen ao momento; as que copias desde un PC aparecen cando volves crear o paquete.",
    "Non hai ningún cartafol ART con imaxes nas unidades iniciadas. Inicia as unidades onde están as túas imaxes (SELECT na súa páxina) e despois volve.",
]
T['Galician_l'] = {
    'RIPPS2_ART_PACK': "Paquete ART",
    'RIPPS2_ART_PACK_BUILD': "Crear ou quitar",
    'HINT_RIPPS2_ART_PACK': "Xunta o cartafol ART de cada unidade iniciada nun só art.tar na unidade que escollas (a máis rápida ofrécese primeiro). As portadas cárganse entón dun ficheiro cun índice, nunca cunha procura por xogo, e os menús e a música van fluídos. Os cartafoles ART quedan como están.",
}

os.makedirs(OUT, exist_ok=True)
for lang in [k for k in T if not k.endswith('_l')]:
    s = {str(i): v for i, v in enumerate(T[lang])}
    json.dump({'s': s, 'l': T[lang + '_l']}, open(os.path.join(OUT, lang + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('wrote', lang)
