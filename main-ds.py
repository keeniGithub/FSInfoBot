import FSApi
import SqlAPI
import disnake
from disnake.ext import commands
from disnake import ButtonStyle, Button
import mc
import time
import threading
import asyncio

intents = disnake.Intents.default()

bot = commands.Bot(command_prefix=None, intents=intents)

@bot.slash_command(name='help', description='Список команд')
async def link(ctx):
    embed = disnake.Embed(
        title="Список команд:",
        description=f"/start - Перезапуск\n \n/player_online - Кол-во онлайн игроков\n \n/player_max - Максимальное кол-во игроков на сервере\n\n/player_list - Список игроков на сервере\n\n/player_info НикИгрока - Узнать информация о игрока (Ник/uuid/последнее время захода на ФС)\n\n/check_player НикИгрока - Проверить, онлайн ли игрок\n\n/random_motd - Рандомный MOTD\n\n/ping - Пинг на сервере\n\n/version - Текущая версия сервера\n\n/ip - Буквенный IP сервере\n\n/numip - Цифровой IP сервере\n\n/credits - Разработчик/информация\n\n/fsinfo - информация о ForScore",
        color=0xfcff40  
    )
    await ctx.send(embed=embed)

@bot.slash_command(name='credits', description='Разработчики/ссылки')
async def link(ctx):
    link = '[Ссылочки](https://t.me/Kenyka_link)'
    fsApiGit = '[FSApi](https://github.com/keeniGitHub/FSApi)'
    kenyka = '[kenyka.fun](http://kenyka.fun)'

    embed = disnake.Embed(
        title="Разработчики/ссылки",
        description=f"Разработчик: {kenyka} / {link}\n \nБот основан на {fsApiGit} от ItzKeeni\n_Вообще я хотел выложить FSApi на PyPi но у меня там 56 багов поэтому лол_\n\nВерсия бота: *{mc.ver}*",
        color=0xfcff40  
    )
    await ctx.send(embed=embed)

@bot.slash_command(name='player_online', description='Кол-во игроков онлайн')
async def link(ctx):
    await ctx.send(f"Сейчас онлайн: {FSApi.player_online()}")

@bot.slash_command(name='player_max', description='Максимальное кол-во игроков')
async def link(ctx):
    await ctx.send(f"Максимальное кол-во игроков: {FSApi.player_max()}")

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

@bot.slash_command(name='check_player', description='Проверить, онлайн ли игрок')
async def link(ctx, player: str):
        if FSApi.check_player(player):
            await ctx.send(f"{player} Онлайн ✔")
        else:
            await ctx.send(f"{player} Оффлайн ❌")

@bot.slash_command(name='random_motd', description='Рандомный MOTD')
async def link(ctx):
    await ctx.send(f"{FSApi.random_motd()}")

@bot.slash_command(name='ping', description='Пинг на сервере')
async def link(ctx):
    await ctx.send(f"Пинг: {FSApi.ping()}")

@bot.slash_command(name='version', description='Версия сервера')
async def link(ctx):
    await ctx.send(f"Текущая версия сервера: {FSApi.version()}")

@bot.slash_command(name='ip', description='Буквенный ip Форскора')
async def link(ctx):
    await ctx.send(f"Буквенный IP: {FSApi.ip()}")

@bot.slash_command(name='numip', description='Цифровой ip Форскора')
async def link(ctx):
    await ctx.send(f"Цифровой IP: {FSApi.numip()}")

@bot.slash_command(name='fsinfo', description='Информация о Форскор')
async def link(ctx):

    yt_url = "[youtube.com/@MrGridlock](https://www.youtube.com/@MrGridlock)"
    fs_url = "[forscore.info](https://forscore.info/)"

    embed = disnake.Embed(
        title="Информация",
        description=f"Информация о ForScore\n\nСайт - {fs_url}\n\nВладелец - {yt_url}\n\n_ДАННЫЙ БОТ НЕ ОТНОСИТСЯ К MrGridlock А ЯВЛЯЕТСЯ ФАН. РАЗРАБОТКОЙ_",
        color=0xfcff40  
    )
    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    activity = disnake.Game(name="kenyka.fun/fsbot")
    await bot.change_presence(activity=activity)
    print(f'Bot is ready')

bot.run("")


