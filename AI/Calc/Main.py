import Paste
import Calc
import Database

def Main():
    team = Paste.get()
    teamDB = Database.get_all(team)
    if teamDB == [None] * 6:
        print('Empty')
Main()