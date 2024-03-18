import Paste
import Calc
import Database

def Main():
    team = Paste.get()
    print(Database.get(team))
Main()