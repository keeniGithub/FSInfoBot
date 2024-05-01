<img src="Logo.png">

# ForScore Info Bot | FSInfoBot

## Простой и удобный Телеграм & Дискорд бот для тебя и ForScore.

### Данный бот был создан чисто по приколу, и не является оф. разработкой от MrGridlock. Так же 1 мая бота убили тем, что запретили просто списка игроков через подсказку в майнкрафте (бот на этом держался 😁)

<h2>Установка Библиотек</h2>

- успользуя pip requirements.txt

<br>

```python
$ pip install -r requirements.txt
```

<br>

- успользуя pip устанавливая по отдельности каждый модуль

<br>

```python
$ pip install pyTelegramBotAPI
```

```python
$ pip install disnake
```

```python
$ pip install mcstatus
```

# Смена IP

### Поскольку данный бот просто собирает информацию по IP его можно изменить и использовать для другого сервера

#### FSApi.py

```python
# 6 строчка
server = JavaServer.lookup("grid.forscore.info") # вот тут изменить IP на свой
```

#### SqlAPI.py

```python
# 6 строчка
server = JavaServer.lookup("grid.forscore.info") # и тут тоже
```

# Структура файлов

**main.py** - основной файл с ТГ ботом

**main-ds.py** - файл с Диискорд ботом

**SqlAPI.py** - небольшая API для работы с SqlLite (хотя API назвать с турдом)

**FSApi.py** - API ФорСкора

**mc.py** - функция для получения UUID игрока, а так же назначения фонового процесса получения времени последней активности игрока и записи в БД

# Список Функций

## /player_online

#### Кол-во игроков онлайн

```python
# main.py / телеграм бот
@bot.message_handler(commands=['player_online'])
def player_online(message):
    bot.send_message(message.chat.id, f"Сейчас онлайн: {FSApi.player_online()}")

# main-ds.py / дискорд бот
@bot.slash_command(name='player_online', description='Кол-во игроков онлайн')
async def link(ctx):
    await ctx.send(f"Сейчас онлайн: {FSApi.player_online()}")

# FSApi.py / функция из API
def player_online():
    status = JavaServer.status(server)
    if status.players.online == 0:
        return "Сервер Оффлайн."
    else:
        return status.players.online
```

## /player_max

#### Максимальное кол-во игроков онлайн

```python
# main.py / телеграм бот
@bot.message_handler(commands=['player_max'])
def player_max(message):
    bot.send_message(message.chat.id, f"Максимальное кол-во игроков: {FSApi.player_max()}")

# main-ds.py / дискорд бот
@bot.slash_command(name='player_max', description='Максимальное кол-во игроков')
async def link(ctx):
    await ctx.send(f"Максимальное кол-во игроков: {FSApi.player_max()}")

# FSApi.py / функция из API
def player_max():
    status = JavaServer.status(server)
    return status.players.max
```

## /player_info

#### Информация об игроке (Ник, UUID, время последней активности на FS)

```python
# main.py / телеграм бот
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

# main-ds.py / дискорд бот
@bot.slash_command(name='player_info', description='Информация о игроке')
async def link(ctx, player: str):
    last_time = SqlAPI.select_from_db("last_seen", "players", "player_name", player)
    uuid = mc.get_player_uuid(player)
    try:
        if uuid == "Player not found":
            await ctx.send("Игрок не был найден.")
        else:
            embed = disnake.Embed(
                title="Информация о игроке",
                description=f"Информация о игроке\n\nНик: `{player}`\nuuid: {uuid}\n\nПоследний раз замечен на сервере: `{last_time[0]}`",
                color=0xfcff40
            )
            await ctx.send(embed=embed)
    except TypeError:
        embed = disnake.Embed(
                title="Информация о игроке",
                description=f"Информация о игроке\n\nНик: `{player}`\nuuid: {uuid}\n\nПоследний раз замечен на сервере: `Нету данных`",
                color=0xfcff40
            )
        await ctx.send(embed=embed)

# mc.py / функция фонового процесса для записи последней активности на FS
def background_task():
    while True:
        SqlAPI.last_time_to_player()
        time.sleep(60)

thread = threading.Thread(target=background_task)
thread.start()
```

## /player_list

#### Список игроков на сервере

#### Поскольку данная функцая работает при помощи подсказки в майнкрафте со списком игроков, больше 12 он не показывает и для вывода всех игроков я сделал алгоритм, где получаю список игроков, а поскольку каждый раз там разные никнеймы, я записываю в один массив ники всех кто попался в массив во время перебора ников.

```python
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


# main-ds.py / дискорд бот
@bot.slash_command(name='player_list', description='Список игроков онлайн')
async def link(ctx):
    if FSApi.player_online() <= 12:
        list = FSApi.player_list()
        output = ""
        for ell in list:
            output += ell+"\n"
            embed = disnake.Embed(
            title="Список игроков",
            description=f"`{output}`",
            color=0xfcff40
            )
        await ctx.send(embed=embed)
    else:
        embed = disnake.Embed(
            title="Список игроков",
            description=f"Минутку...\n\n_Подождите пока бот собирает информацию._",
            color=0xfcff40
        )
        await ctx.send(embed=embed, delete_after=56)
        loop = int(FSApi.player_online())-12
        loop = 150+loop*10
        output = ""
        list = FSApi.player_list_full(int(loop))
        for ell in list:
            output += ell+"\n"

        embed = disnake.Embed(
            title="Список игроков",
            description=f"`{output}`",
            color=0xfcff40
        )
        await ctx.send(embed=embed)

# FSApi.py / функция из API
# player_list() нужна для получения ДО 12 игроков, а player_list_full() если > 12
def player_list():
    status = JavaServer.status(server)
    data = str(status.players)
    all_names = []

    matches = re.finditer(r"name='(.*?)'", data)

    for match in matches:
        all_names.append(match.group(1))

    if all_names == []:
        return "Сервер Оффлайн."
    else:
        return all_names

def player_list_full(cycle_num):
    unique_players = set()
    final_result = []

    if player_list() == "Сервер Оффлайн.":
        return "Сервер Оффлайн."
    else:
        for i in range(cycle_num):
            players = player_list()
            unique_players.update(players)

            final_result = list(unique_players)

        return final_result
```

## /check_player

#### Проверить, онлайн ли игрок

```python
# main.py / телеграм бот
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


# main-ds.py / дискорд бот
@bot.slash_command(name='check_player', description='Проверить, онлайн ли игрок')
async def link(ctx, player: str):
        if FSApi.check_player(player):
            await ctx.send(f"{player} Онлайн ✔")
        else:
            await ctx.send(f"{player} Оффлайн ❌")

# FSApi.py / функция из API
def check_player(player):
    status = JavaServer.status(server)
    players = status.players.sample
    if players is not None:
        for p in players:
            if p.name == player:
                return True
```

## /random_motd

#### Рандомный MOTD

```python
# main.py / телеграм бот
@bot.message_handler(commands=['random_motd'])
def random_motd(message):
    bot.send_message(message.chat.id, f"{FSApi.random_motd()}")

# main-ds.py / дискорд бот
@bot.slash_command(name='random_motd', description='Рандомный MOTD')
async def link(ctx):
    await ctx.send(f"{FSApi.random_motd()}")

# FSApi.py / функция из API
def random_motd():
    status = JavaServer.status(server)
    s = status.description
    result = re.sub('[§\drf]', '', s)

    return result
```

## /version

#### Текущая версия сервера

```python
# main.py / телеграм бот
@bot.message_handler(commands=['version'])
def version(message):
    bot.send_message(message.chat.id, f"Текущая версия сервера: {FSApi.version()}")

# main-ds.py / дискорд бот
@bot.slash_command(name='version', description='Версия сервера')
async def link(ctx):
    await ctx.send(f"Текущая версия сервера: {FSApi.version()}")

# FSApi.py / функция из API
def version():
    status = JavaServer.status(server)
    data = str(status.version)
    ver = re.search(r"name='([^']+)'", data).group(1)
    return ver
```

## /ping

#### Пинг сервера

```python
# main.py / телеграм бот
@bot.message_handler(commands=['ping'])
def ping(message):
    bot.send_message(message.chat.id, f"Пинг: {FSApi.ping()}")

# main-ds.py / дискорд бот
@bot.slash_command(name='ping', description='Пинг на сервере')
async def link(ctx):
    await ctx.send(f"Пинг: {FSApi.ping()}")

# FSApi.py / функция из API
def ping():
    status = JavaServer.status(server)
    return int(status.latency)
```

## /ip | /numip

#### Цифровой и Буквенный IP

```python
# main.py / телеграм бот
@bot.message_handler(commands=['ip'])
def ip(message):
    bot.send_message(message.chat.id, f"Буквенный IP: {FSApi.ip()}")

@bot.message_handler(commands=['numip'])
def numip(message):
    bot.send_message(message.chat.id, f"Цифровой IP: {FSApi.numip()}")

# main-ds.py / дискорд бот
@bot.slash_command(name='ip', description='Буквенный ip Форскора')
async def link(ctx):
    await ctx.send(f"Буквенный IP: {FSApi.ip()}")

@bot.slash_command(name='numip', description='Цифровой ip Форскора')
async def link(ctx):
    await ctx.send(f"Цифровой IP: {FSApi.numip()}")

# FSApi.py / функция из API
def ip():
    return "grid.forscore.info"

def numip():
    return "51.89.74.9"
```

### /help - список команд

### /credits - разработчики | ссылки

### /fsinfo - информация о ForScore

<hr/>

### Ну вообщем бота убили одним плагином, всем спасибо и пока

# **Сайт** - [kenyka.fun](https://kenyka.fun/fsbot)
