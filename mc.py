import requests
import threading
import SqlAPI
import time

ver = "1.2.2"

def get_player_uuid(username):
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["id"]
    else:
        return "Player not found"

def background_task():
    while True:
        SqlAPI.last_time_to_player()
        time.sleep(60)

thread = threading.Thread(target=background_task)
thread.start()