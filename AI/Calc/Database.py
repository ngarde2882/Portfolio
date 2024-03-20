# File to hold database functions
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from threading import Thread
import keys

firebase_admin.initialize_app(credentials.Certificate(keys.firebase_cred), {'databaseURL':keys.firebase_url})

########TEMPORARY########
def time_start():
    global time
    import time
    global time_var 
    time_var = time.time()*1000

def time_end(message=None):
    if message:
        print(f"{message} {round(time.time()*1000-time_var)}")
    else:
        print(round(time.time()*1000-time_var))
#########################

def get(team, ref, pos):
    team[pos-1] = db.reference("/dex3/"+str(ref)).get()
    print(f"team[{pos-1}] : {team[pos-1]['name']}")

def get_all(team):
    team_out = [None] * 6
    m = db.reference("map").get()
    pos = 1
    threads = []
    for i in range(len(team)):
        print((m[(team[i].name).lower()],))
        t = Thread(target=get, args=(team_out,m[(team[i].name).lower()],team[i].position))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return team_out
