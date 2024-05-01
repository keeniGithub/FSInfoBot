from mcstatus import server
from mcstatus import JavaServer
import re
import SqlAPI

server = JavaServer.lookup("grid.forscore.info")

status = JavaServer.status(server)

def player_online():
    status = JavaServer.status(server)
    if status.players.online == 0:
        return "Сервер Оффлайн."
    else:
        return status.players.online

def player_max():
    status = JavaServer.status(server)
    return status.players.max

def random_motd():
    status = JavaServer.status(server)
    s = status.description
    result = re.sub('[§\drf]', '', s)

    return result

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

def ip():
    return "grid.forscore.info"

def numip():
    return "51.89.74.9"

def ping():
    status = JavaServer.status(server)
    return int(status.latency)

def version():
    status = JavaServer.status(server)
    data = str(status.version)
    ver = re.search(r"name='([^']+)'", data).group(1)
    return ver

def check_player(player):
    status = JavaServer.status(server)
    players = status.players.sample
    if players is not None:
        for p in players:
            if p.name == player:
                return True      
            
