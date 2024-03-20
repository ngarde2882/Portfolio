# File to hold data collection functions
from Classes import Pokemon

stats = { # assigned place for each stat in an array for faster placement
    'HP':0,
    'Atk':1,
    'Def':2,
    'SpA':3,
    'SpD':4,
    'Spe':5
}

def get():
    team = []
    f = open("Paste.txt", "r")
    pokepaste = f.read().split('\n\n')
    for poke in pokepaste:
        if len(team) == 6: continue
        if poke == '': continue
        poke = poke.split('\n')
        moves = []
        evs = [0,0,0,0,0,0]
        ivs = [31,31,31,31,31,31]
        for line in poke:
            if line == '': break
            if '@' in line: # name and item, ignore nickname and gender (for now)
                line = line.split(' @ ')
                item = line[1][:-2]
                name = line[0]
                if '(' in name:
                    tname = name[name.find("(")+1:name.find(")")] # cut out substring from between two known chars
                    if len(tname)!=1:
                        name = tname
                    else: name = name[:-4]
            elif 'Ability: ' == line[:9]: ability = line[9:-2]
            elif 'Shiny: ' == line[:7]: continue # skip TODO: use this for displaying sprites?
            elif 'Tera Type: ' == line[:11]: tera = line[11:-2]
            elif 'EVs: ' == line[:5]:
                line = line[5:-2].split(' / ')
                for stat in line:
                    stat = stat.split(' ')
                    evs[stats[stat[1]]] = stat[0]
            elif 'IVs: ' == line[:5]:
                line = line[5:-2].split(' / ')
                for stat in line:
                    stat = stat.split(' ')
                    ivs[stats[stat[1]]] = stat[0]
            elif 'Nature  ' == line[-8:]: nature = line.split(' ')[0]
            elif '- ' == line[:2]: moves.append(line[2:-2]) # moves
            else: # name, no item
                name = line
                item = None
                if '(' in name:
                    tname = name[name.find("(")+1:name.find(")")]
                    if len(tname)!=1:
                        name = tname
                    else: name = name[:-4]
        team.append(Pokemon(name,item,ability,tera,nature,moves,evs,ivs,len(team)+1))
        # print(Pokemon(name,item,ability,tera,nature,moves,evs,ivs),'\n')
    f.close()
    # print(team)
    return team