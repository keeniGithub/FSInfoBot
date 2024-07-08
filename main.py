import FSApi
import SqlAPI
import mc
import time
import telebot
from telebot import types
import config

bot = telebot.TeleBot(config.TOKEN_TG)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Команды')
    markup.add(button1)
    bot.send_message(message.chat.id, f"👋 Привет {message.from_user.username}\n \nЭто Инфо-бот про ForScore\nТут ты можешь узнать различную информацию о состоянии ФорСкора (Список игроков, пинг, версию, IP и д.р)\nЧтобы узнать список команд пропиши /help или нажми на кнопку ниже ⤵", reply_markup=markup)
    user_id = message.from_user.id
    nickname = message.from_user.username if message.from_user.username else None
    SqlAPI.add_user_to_db(user_id, nickname)

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, f"Список команд:\n\n/start - Перезапуск\n \n/player_online - Кол-во онлайн игроков\n \n/player_max - Максимальное кол-во игроков на сервере\n\n/player_list - Список игроков на сервере\n\n/player_info НикИгрока - Узнать информация о игрока (Ник/uuid/последнее время захода на ФС)\n\n/check_player НикИгрока - Проверить, онлайн ли игрок\n\n/random_motd - Рандомный MOTD\n\n/ping - Пинг на сервере\n\n/version - Текущая версия сервера\n\n/ip - Буквенный IP сервере\n\n/numip - Цифровой IP сервере\n\n/credits - Разработчик/информация\n\n/fsinfo - информация о ForScore")

@bot.message_handler(commands=['credits'])
def credits(message):
    link = '[Ссылочки](https://t.me/Kenyka_link)'
    fsApiGit = '[FSApi](https://github.com/keeniGitHub/FSApi)'
    kenyka = '[kenyka.fun](http://kenyka.fun)'
    bot.send_message(message.chat.id, f"Разработчик: {kenyka} / {link}\n \nБот основан на {fsApiGit} от ItzKeeni\n_Вообще я хотел выложить FSApi на PyPi но у меня там 56 багов поэтому лол_\n\nВерсия бота: *{mc.ver}*", parse_mode='Markdown')

@bot.message_handler(commands=['player_online'])
def player_online(message):
    bot.send_message(message.chat.id, f"Сейчас онлайн: {FSApi.player_online()}")

@bot.message_handler(commands=['player_max'])
def player_max(message):
    bot.send_message(message.chat.id, f"Максимальное кол-во игроков: {FSApi.player_max()}")

@bot.message_handler(commands=['player_info'])
def track(message):
    if len(message.text.split()) == 1:
        bot.send_message(message.chat.id, "Вы не указали никнейм!")
    else:
        player = message.text.split("/player_info ")[1]
        last_time = SqlAPI.select_from_db("last_seen", "players", "player_name", player)
        uuid = mc.get_player_uuid(player)
        if uuid == "Player not found":
            bot.send_message(message.chat.id, "Игрок не был найден.")
        else:
            bot.send_message(message.chat.id, f"Информация о игроке\n\nНик: {player}\nuuid: {uuid}\n\nПоследний раз замечен на сервере: {last_time[0]}",)    

@bot.message_handler(commands=['player_list'])
def player_list(message):
    if FSApi.player_online() <= 12:
        list = FSApi.player_list()
        output = ""
        for ell in list:
            output += ell+"\n"
        bot.send_message(message.chat.id, f"{output}")
    else:
        bot.send_message(message.chat.id, f"Минутку...")

        loop = int(FSApi.player_online())-12
        loop = 150+loop*10
        output = ""
        list = FSApi.player_list_full(int(loop))
        for ell in list:
            output += ell+"\n"
        bot.send_message(message.chat.id, f"{output}")

@bot.message_handler(commands=['check_player'])
def check_player(message):
    if len(message.text.split()) == 1:
        bot.send_message(message.chat.id, "Вы не указали никнейм!")
    else:
        player = message.text.split("/check_player ")[1]
        if FSApi.check_player(player):
            bot.send_message(message.chat.id, f"{player} Онлайн ✔")
        else:
            bot.send_message(message.chat.id, f"{player} Оффлайн ❌")


@bot.message_handler(commands=['track_player'])
def track(message):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True)
    button1 = types.InlineKeyboardButton('Добавить игрока', callback_data='add_track')
    button2 = types.InlineKeyboardButton('Убрать игрока', callback_data='del_track')
    markup.add(button1, button2)
    bot.send_message(message.chat.id, f"Трекинг игроков\n\nСписок отслеживаемых игроков:\n\nДобавить игрока для отслеживания: /track_add Ник\nУдалить их отслеживания: /del_track Ник", reply_markup=markup)

@bot.message_handler(commands=['random_motd'])
def random_motd(message):
    bot.send_message(message.chat.id, f"{FSApi.random_motd()}")

@bot.message_handler(commands=['ping'])
def ping(message):
    bot.send_message(message.chat.id, f"Пинг: {FSApi.ping()}")

@bot.message_handler(commands=['version'])
def version(message):
    bot.send_message(message.chat.id, f"Текущая версия сервера: {FSApi.version()}")

@bot.message_handler(commands=['ip'])
def ip(message):
    bot.send_message(message.chat.id, f"Буквенный IP: {FSApi.ip()}")

@bot.message_handler(commands=['numip'])
def numip(message):
    bot.send_message(message.chat.id, f"Цифровой IP: {FSApi.numip()}")

@bot.message_handler(commands=['fsinfo'])
def fsinfo(message):
    yt_url = "[youtube.com/@MrGridlock](https://www.youtube.com/@MrGridlock)"
    fs_url = "[forscore.info](https://forscore.info/)"
    bot.send_message(message.chat.id, f"Информация о ForScore\n\nСайт - {fs_url}\n\nВладелец - {yt_url}\n\n_ДАННЫЙ БОТ НЕ ОТНОСИТСЯ К MrGridlock А ЯВЛЯЕТСЯ ФАН. РАЗРАБОТКОЙ_", parse_mode="MarkDown")

@bot.message_handler()
def menu(message):
    if message.text == "Команды":
            bot.send_message(message.chat.id, f"Список команд:\n\n/start - Перезапуск\n \n/player_online - Кол-во онлайн игроков\n \n/player_max - Максимальное кол-во игроков на сервере\n\n/player_list - Список игроков на сервере\n\n/player_info НикИгрока - Узнать информация о игрока (Ник/uuid/последнее время захода на ФС)\n\n/check_player НикИгрока - Проверить, онлайн ли игрок\n\n/random_motd - Рандомный MOTD\n\n/ping - Пинг на сервере\n\n/version - Текущая версия сервера\n\n/ip - Буквенный IP сервере\n\n/numip - Цифровой IP сервере\n\n/credits - Разработчик/информация\n\n/fsinfo - информация о ForScore")

    if message.text == "ПОСХАЛКО":
        bot.send_message(message.chat.id, f"""Кеняка шел по лесу, наслаждаясь природой и запахом свежего воздуха. Вдруг он услышал странные звуки и почувствовал, что кто-то следит за ним. Обернувшись, он увидел Модемикса - загадочного создания из другого мира.

Модемикс приблизился к Кеняке и начал ласкать его тело нежными лучами света. Кеняка не сопротивлялся и отдался этому странному существу, которое пробудило в нем нечто новое и завораживающее.

И вот, когда все казалось наивысшей степенью страсти, в лес вошел Олег Беспалов Вейс - маг, обладающий необычными способностями. Он увидел, что происходит, и решил вмешаться в этот интимный момент.

Олег Беспалов Вейс достал из-под плаща лампу Аладдина и начал натирать ее, как будто пытаясь вызвать джинна. В это время сексуальная энергия витала в воздухе, создавая атмосферу невиданных чудес и магии.

Но как закончилась эта необычная встреча - осталось тайной. Может быть, это было лишь мгновение вечности, запечатленное в памяти Кеняки и Модемикса, на которое им было суждено вспоминать с удивлением и волнением.""")

    if message.text == "МУНЛАЙТ С АКУЛИНОЧКОЙ":
        bot.send_message(message.chat.id, f"""
        Кеняка и Найсблок были лучшими друзьями уже много лет. Они вместе проходили через все трудности и радости жизни. Однажды Акулина, обаятельная и загадочная девушка, пригласила их на свою виллу на побережье. На самом деле, Кеняка и Найсблок уже давно оба тайно мечтали о ней.

Придя на виллу, друзья были поражены красотой и уютом этого места. Акулина позаботилась о каждой детали, чтобы гости чувствовали себя как дома. Она угощала их вкусными ужинами и вином, и нежными ласками.

Под лучами мягкого мунлайта, Кеняка и Найсблок были окрылены атмосферой романтики и желания. Они сидели на веранде, наслаждаясь звездным небом и шумом прибоя. Когда Акулина перешепталась им, что имеются одни желания к ним, друзья оба осмелились и натянули прохладный подбородок на дверь. Ее внутри брала лежанка: слышалась необъядный напряжение и путь были ранние взаимные дела отельного сорока. 

Под мягким светом луны, Кеняка, Найсблок и Акулина открыли в себе новые стороны, отдавшись страсти и наслаждению. Им казалось, что они находятся в моменте вечности, словно время остановилось.  В эту ночь, они обрели новый уровень близости и взаимопонимания, который укрепил их дружбу.

После этой ночи, Кеняк, Найсблок и Акулина стали еще ближе, чем прежде. Они навсегда запомнили моменты счастья и любви под лунным светом, который оставил в них незабываемые воспоминания.
""")
        
    if message.text == "/яйца.":
        bot.send_message(message.chat.id, f"ЯЙЦА:\nhttps://telesco.pe/MisterPyatorkatg/2413")

bot.infinity_polling(timeout=10, long_polling_timeout=5)


