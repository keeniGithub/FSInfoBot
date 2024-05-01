import sqlite3
from mcstatus import server
from mcstatus import JavaServer
import datetime

server = JavaServer.lookup("grid.forscore.info")

status = JavaServer.status(server)

sql = sqlite3.connect('users.db',  check_same_thread=False)
db = sql.cursor()
db.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY, nickname TEXT)''')

db.execute('''CREATE TABLE IF NOT EXISTS players
                  (player_name text PRIMARY KEY, last_seen text)''')
sql.commit()

def add_user_to_db(user_id, nickname):
    db.execute("SELECT * FROM users WHERE id=?", (user_id,))
    existing_user = db.fetchone()
    
    if not existing_user:
        db.execute("INSERT INTO users (id, nickname) VALUES (?, ?)", (user_id, nickname))
        sql.commit()
        return True
    else:
        return False
    
def select_from_db(obj, table, where, var):
    db.execute(f"SELECT {obj} FROM {table} WHERE {where}=?", (var,))
    return db.fetchone()


def last_time_to_player():
    status = JavaServer.status(server)
    if len(status.players.sample) > 0:
        for player in status.players.sample:
            player_name = player.name
            current_time = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
            
            db.execute("SELECT * FROM players WHERE player_name=?", (player_name,))
            existing_player = db.fetchone()
            sql.commit()
            
            if existing_player:
                db.execute("UPDATE players SET last_seen=? WHERE player_name=?",
                            (current_time, player_name))
                sql.commit()
            else:
                db.execute("INSERT INTO players VALUES (?, ?)",
                            (player_name, current_time))
                sql.commit()


                

