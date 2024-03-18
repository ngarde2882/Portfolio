# File to hold database functions
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import keys

firebase_admin.initialize_app(credentials.Certificate(keys.firebase_cred), {'databaseURL':keys.firebase_url})

def get(team):
    team_out = {}
    for mon in team:
        team_out[mon.name] = db.reference("/dex3/"+mon.name)
    return team_out
