import discord
import random
import math
import datetime
from discord.ext import commands
# discord.Permissions(permissions=126016)

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import klefkeys

# cred = credentials.Certificate("project-p-4c372-firebase-adminsdk-rkjmv-e4e44aece1.json") old cred
firebase_admin.initialize_app(credentials.Certificate(klefkeys.firebase_cred), {'databaseURL':klefkeys.firebase_url})

url = "https://serebii.net"

intents = discord.Intents.all()
client = commands.Bot(command_prefix = 'p!',intents=intents)
guilds = {}
active_spawns = {}
keymap = db.reference("/map/").get()
ref = db.reference("/dex3/")
dex = ref.get()

wild = []
pokedex = {}
i = 1
while(i<1026):
    try:
        c = int(dex[i]['catchRate'])
        c = math.ceil(c**2) # TODO maybe ^3 for better rarity distribution? maybe create a distribution that generates these nums instead of making a list for them
        wild.extend(i for j in range(c))
        pokedex[dex[i]['name']]=i
        if 'otherFormes' in dex[i]:
            for form in dex[i]['otherFormes']:
                pokedex[dex[i][form]['name']] = i
                if '-Mega' not in form:
                    wild.extend(i for j in range(c))
    except:
        print(f'error generating wild encounters for num {i}')
    i+=1

def gen_wild():
    global wild
    global dex
    mon = random.choice(wild)
    print(dex[mon]['name'])
    return mon

def spawn(mon):
    embed = discord.Embed(
        title = "A wild pokemon has spawned",
        description = "Say its name first to catch it",
        # url = f"https://play.pokemonshowdown.com/sprites/ani/{dex[key]['name']}.gif"
    )
    if mon['shiny']:
        imageurl = f"https://play.pokemonshowdown.com/sprites/ani-shiny/{mon['name'].lower()}.gif"
    else:
        imageurl = f"https://play.pokemonshowdown.com/sprites/ani/{mon['name'].lower()}.gif"
    embed.set_image(url = imageurl)
    # embed.set_footer(text = 'This is a footer')
    # embed.set_author(name = 'Author name')
    return embed

trainer_logs = {} # hold bool and latest 5 timestamps for messages from a user: pop any later than 5m, then if length is 5 set bool true
                    # if true once length<5 it is false
                    # if true give nerf xp val instead of base
                    # run function for each gain type through case
                        # {
                        #     ;
                        # }
                    # add base amount of xp gain and check level
                    # if a level up, run a level up function to check for evolve

def timeout(id): # report if user is being timed out for frequent usage
    global trainer_logs
    if len(trainer_logs[id]) == 5:
        return True
    return False

def update_logs(id): # remove any datetime from this user's log that is over 5m old. Add datetime for now
    global trainer_logs
    now = datetime.datetime.now()
    # print(now)
    # print('id:',str(id))
    if id not in trainer_logs: trainer_logs[id] = []
    trainer_logs[id].append(now)
    for i in range(len(trainer_logs[id])): # store oldest at 0 and newest at append
        if trainer_logs[id][0] > now - datetime.timedelta(minutes=5):
            break
        else:
            trainer_logs[id].pop(0)
    while len(trainer_logs[id])>5: # ensure max length is 5
        trainer_logs[id].pop(0)

def erratic(lv, xp):
    nextlv = lv+1
    if nextlv<50:
        xp_nextlv = (nextlv**3 * (100-nextlv))/50
        if xp>=xp_nextlv:
            return erratic(nextlv,xp)
        return lv
    elif nextlv<68:
        xp_nextlv = (nextlv**3 * (150-nextlv))/100
        if xp>=xp_nextlv:
            return erratic(nextlv,xp)
        return lv
    elif nextlv<98:
        xp_nextlv = (nextlv**3 * math.floor((1911-10*nextlv)/3))/500
        if xp>=xp_nextlv:
            return erratic(nextlv,xp)
        return lv
    else:
        xp_nextlv = (nextlv**3 * (160-nextlv))/100
        if xp>=xp_nextlv:
            return erratic(nextlv,xp)
        return lv
def mediumFast(lv, xp):
    nextlv = lv+1
    xp_nextlv = nextlv**3
    if xp>=xp_nextlv:
        return mediumFast(nextlv,xp)
    return lv
def fast(lv, xp):
    nextlv = lv+1
    xp_nextlv = 4*(nextlv**3)/5
    if xp>=xp_nextlv:
        return fast(nextlv,xp)
    return lv
def mediumSlow(lv, xp):
    nextlv = lv+1
    xp_nextlv = (6*nextlv**3)/5 - 15*nextlv**2 + 100*nextlv - 140
    if xp>=xp_nextlv:
        return mediumSlow(nextlv,xp)
    return lv
def slow(lv, xp):
    nextlv = lv+1
    xp_nextlv = (5*nextlv**3)/4
    if xp>=xp_nextlv:
        return slow(nextlv,xp)
    return lv
def fluctuating(lv, xp):
    nextlv = lv+1
    if nextlv<15:
        xp_nextlv = (nextlv**3 * math.floor((nextlv+1)/3)+24)/50
        if xp>=xp_nextlv:
            return fluctuating(nextlv,xp)
        return lv
    elif nextlv<36:
        xp_nextlv = (nextlv**3 * (nextlv + 14))/50
        if xp>=xp_nextlv:
            return fluctuating(nextlv,xp)
        return lv
    else:
        xp_nextlv = (nextlv**3 * math.floor(nextlv/2)+32)/50
        if xp>=xp_nextlv:
            return fluctuating(nextlv,xp)
        return lv

def check_evo_level(pokemon):
    global dex
    global pokedex
    mon = dex[pokemon['num']]
    if mon['name'] != pokemon['species']:
        mon = mon[pokemon['species']]
    if 'evos' in mon:
        for evo_name in mon['evos']:
            evo = dex[pokedex[evo_name]]
            if evo['name'] != evo_name:
                evo = evo[evo_name]
            if 'evoLevel' in evo:
                if pokemon['lvl']>=evo['evoLevel']:
                    return evo_name
            elif 'evoType' in evo: # TODO evoRegion is currently unused
                match evo['evoType']:
                    case 'levelHold':
                        if pokemon['item'] == evo['evoItem']:
                            return evo_name
                    case 'levelExtra':
                        return f"L {evo['evoCondition']}" # TODO
                    case 'levelFriendship':
                        if pokemon['friendship'] == 220:
                            return evo_name
                    case 'levelMove':
                        if evo['evoMove'] in pokemon['moves']:
                            return evo_name
    return None
def xp(author_id):
    ref = db.reference('/trainer/'+str(author_id))
    tr = ref.get()
    if tr is None:
        return
    to = timeout(author_id)
    gain = 500
    if to: # TODO randomize these values
        gain = 100
    ref = db.reference('/trainer/'+str(author_id)+'/pkmn/'+str(db.reference('/trainer/'+str(author_id)+'/Walking/pkmn').get()))
    mon = ref.get()
    xp_speed = dex[mon['number']]['xpType']
    xp = mon['xp'] + gain
    level = mon['lvl']
    if level == 100:
        return
    match xp_speed:
        case 'Medium Fast':
            lv = mediumFast(level, xp)
        case 'Erratic':
            lv = erratic(level, xp)
        case 'Fast':
            lv = fast(level, xp)
        case 'Medium Slow':
            lv = mediumSlow(level, xp)
        case 'Slow':
            lv = slow(level, xp)
        case 'Fluctuating':
            lv = fluctuating(level, xp)
    if lv>level: # level current walking mon up
        ref.update({'xp':xp,'lvl':lv})
        mon['lvl'] = lv
        evo_name = check_evo_level(mon)
        if evo_name: # TODO find a way to send evolution message
            evolution = dex[pokedex[evo_name]]
            if evolution['name']!=evo_name:
                evolution=evolution[evo_name]
            if mon['name']==mon['species']:
                ref.update({'num':evolution['num'],'species':evolution['name'],'name':evolution['name']})
            else:
                ref.update({'num':evolution['num'],'species':evolution['name']})
        return
    ref.update({'xp':xp})
    # only add xp

def starter_display():
    # starters = {'bulbasaur':1,'charmander':4,'squirtle':7,'pikachu':25,'eevee':133,'totodile':152,'cyndaquil':155,'chikorita':158,'treeko':252,'torchic':255,'mudkip':258,'turtwig':387,'piplup':390,'chimchar':393,'snivy':495,'tepig':498,'oshawott':501,'chespin':650,'fennekin':653,'froakie':656,'rowlet':722,'litten':725,'popplio':728,'grookey':810,'scorbunny':813,'sobble':816}
    embed = discord.Embed(
        title = "Welcome to the world of Pokemon!",
        description = "Say \"p!init [name]\" of a starter to begin\nStarters:\nbulbasaur, charmander, squirtle\npikachu, eevee\ntotodile, cyndaquil, chikorita\ntreeko, torchic, mudkip\nturtwig, piplup, chimchar\nsnivy, tepig, oshawott\nchespin, fennekin, froakie\nrowlet, litten, popplio\ngrookey, scorbunny, sobble",
        # url = url+'/swordshield/pokemon/001.png'
    )
    # imageurl = 'url' # TODO: set url value
    # embed.set_image(url = imageurl)
    embed.set_footer(text = 'For more information about a Pokemon say \"p!info [name]\"')
    # embed.set_author(name = 'Author name')
    return embed

def lower(string_in):
    if type(string_in) == list: # list
        for i in range(len(string_in)):
            for c in string_in[i]:
                string_in[i] = string_in[i].replace(c, c.lower())
        return string_in
    elif type(string_in) == str: # string
        for c in string_in:
            string_in = string_in.replace(c, c.lower())
        return string_in
    else:
        raise('ONLY STRINGS AND LISTS OF STRINGS CAN BE INPUT IN THIS FUNCTION')


def evocond(mon):
    global dex
    if 'evoLevel' in mon:
        return f"L{mon['evoLevel']}"
    if 'evoType' in mon: # TODO evoRegion is currently unused
        match mon['evoType']:
            case 'levelHold':
                return f"L holding {mon['evoItem']}"
            case 'levelExtra':
                return f"L {mon['evoCondition']}" # TODO
            case 'levelFriendship':
                return f"L Friendship"
            case 'trade':
                if 'evoCondition' in mon:
                    return f"Trade {mon['evoCondition']}"
                elif 'evoItem' in mon:
                    return f"Trade holding {mon['evoItem']}"
                else:
                    return f"Trade"
            case 'useItem':
                return f"{mon['evoitem']}"
            case 'levelMove':
                return f"L with {mon['evoMove']}"
            case 'other':
                return f"???"
    return 'error'
# dive is used in combination with make_evostring to create an evolution string for a pokemon and all of its forms
def dive(mon, s, depth):
    global dex
    global pokedex
    if not s:
        s = '|'+mon['name']
        if 'evos' in mon:
            for evo in mon['evos']:
                s=dive(dex[pokedex[evo]],s,depth+1)
        if 'otherFormes' in mon:
            for form in mon['otherFormes']:
                if '-Mega' in form:
                    s=dive(mon[form],s,depth+1)
                else:
                    s=dive(mon[form],s,depth)
    else:
        # if dex[pokedex[evo]]['name'] != evo:
        #     mon = dex[pokedex[evo]][evo]
        s+='\n|'+'-'*depth+evocond(mon)+'>'+mon['name']
        if 'evos' in mon:
            for evo in mon['evos']:
                s=dive(dex[pokedex[evo]],s,depth+1)
        if 'otherFormes' in mon:
            for form in mon['otherFormes']:
                if '-Mega' in form:
                    s=dive(mon[form],s,depth+1)
                else:
                    s=dive(mon[form],s,depth)
    return s
def make_evostring(mon):
    global dex
    global pokedex
    s = ''
    while 'prevo' in mon:
        mon = dex[pokedex[mon['prevo']]]
    s=dive(mon,s,0)
    return s

def nature_table(nature):
    n = [1,1,1,1,1]
    # increase
    table = [['Hardy','Lonely','Adamant','Naughty','Brave'],
             ['Bold','Docile','Impish','Lax','Relaxed'],
             ['Modest','Mild','Bashful','Rash','Quiet'],
             ['Calm','Gentle','Careful','Quirky','Sassy'],
             ['Timid','Hasty','Jolly','Naive','Serious']]
    for i in range(len(table)):
        for j in range(len(table[i])):
            if nature == table[i][j]:
                n[i]+=0.1
                n[j]-=0.1
                return n
    raise(F'NATURE NOT FOUND? {nature}')

def stat_calc(base,ivs,evs,level,nature):
    stats = {'hp':0,'atk':0,'def':0,'spa':0,'spd':0,'spe':0}
    i=0
    n = nature_table(nature)
    for stat in stats.keys():
        if i == 0:
            stats[stat] = math.floor((2*base[stat]+ivs[i]+math.floor(evs[i]/4)*level)/100)+level+10
        else:
            stats[stat] = math.floor((math.floor((2*base[stat]+ivs[i]+math.floor(evs[i]/4)*level)/100)+5)*n[i-1])
        i+=1
    return stats
def get_ability(mon):
    dex_entry = dex[mon['num']]
    if dex_entry['name']!=mon['species']:
        dex_entry = dex_entry[mon['species']]
    if type(dex_entry['abilities'])==list:
        if mon['ability']=='H':
            return dex_entry['abilities'][0]
        if len(dex_entry['abilities'])==1:
            return dex_entry['abilities'][0]
        return dex_entry['abilities'][mon['ability']]
    if mon['ability'] in dex_entry['abilities']:
        return dex_entry['abilities'][mon['ability']]
    return dex_entry['abilities'][0]
def info_caught(author_id, i):
    ref = db.reference('/trainer/'+str(author_id)+'/pkmn/'+str(i))
    mon = ref.get()
    pokedex_entry = dex[mon['num']]
    if pokedex_entry['name'] != mon['species']:
        pokedex_entry = pokedex_entry[mon['species']]
    types = pokedex_entry['types']
    if len(types) == 2:
        typestring = types[0]+', '+types[1]
    else:
        typestring = types[0]
    stats = stat_calc(pokedex_entry['baseStats'],mon['ivs'],mon['evs'],mon['lvl'],mon['nature'])
    embed = discord.Embed(
        title = mon['name'],
        description = 'Species: ' + str(mon['species']) +
                        '\nType(s): ' + typestring +
                        '\nNumber: ' + str(mon['num']) +
                        '\nItem: ' + str(mon['item']) +
                        '\nAbility: ' + get_ability(mon) +
                        '\nGender: ' + str(mon['gender']) +
                        '\nLevel: ' + str(mon['lvl']) +
                        '\nXP: ' + str(mon['xp']) +
                        '\nNature: ' + str(mon['nature']) +
                        '\nIVs: ' + str(round(sum(mon['ivs'])/(31*6)*100,4)) + '\n\tHP: '+str(stats['hp'])+'\n\tAtk: '+str(stats['atk'])+'\n\tDef: '+str(stats['def'])+'\n\tSpA: '+str(stats['spa'])+'\n\tSpD: '+str(stats['spd'])+'\n\tSpe: '+str(stats['spe']))

    if mon['shiny']:
        imageurl = f"https://play.pokemonshowdown.com/sprites/ani-shiny/{mon['species'].lower()}.gif"
    else:
        imageurl = f"https://play.pokemonshowdown.com/sprites/ani/{mon['species'].lower()}.gif"
    embed.set_image(url = imageurl)
    # embed.set_author(name = 'Author name')
    return embed

def info_name(n):
    global keymap
    global dex
    num = keymap[n]
    mon = dex[num]
    types = mon['types']
    if len(types) == 2:
        typestring = types[0]+', '+types[1]
    else:
        typestring = types[0]
    abilitystring = ''
    for a in mon['abilities']:
        abilitystring += a+', '
    abilitystring = abilitystring[:-2]
    if 'genderRatio' in mon:
        genderstring = f"\u2642 {mon['genderRatio']['M']}%, \u2640 {mon['genderRatio']['F']}%"
    elif 'gender' in mon:
        if mon['gender'] == 'M':
            genderstring = '\u2642'
        elif mon['gender'] == 'F':
            genderstring = '\u2640'
        elif mon['gender'] == 'U':
            genderstring = 'Unknown'
        else:
            raise(f"dex[{mon['num']}][\'gender\']{mon['gender']}")
    else:
        genderstring = "\u2642 50%, \u2640 50%"
    embed = discord.Embed(
        title = mon['name'],
        description = 'Species: ' + str(mon['name']) +
                        '\nType(s): ' + typestring +
                        '\nNumber: ' + str(num) +
                        '\nAbility(s): ' + abilitystring +
                        '\nGender: ' + genderstring +
                        f"\nBase Stats:\n\tHP: {mon['baseStats']['hp']}\n\tAtk: {mon['baseStats']['atk']}\n\tDef: {mon['baseStats']['def']}\n\tSpA: {mon['baseStats']['spa']}\n\tSpD: {mon['baseStats']['spd']}\n\tSpe: {mon['baseStats']['spe']}" +
                        '\nEvo Line:\n' + make_evostring(mon)
        # url = url+'/swordshield/pokemon/001.png'
    )
    imageurl = f"https://play.pokemonshowdown.com/sprites/ani/{mon['name'].lower()}.gif"
    embed.set_image(url = imageurl)
    # embed.set_author(name = 'Author name')
    return embed

@client.event
async def on_ready():
    print('Project P is ready.')

@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.author.id != 996855122627932180:
        global guilds
        if message.guild in guilds:
            guilds[message.guild] += 1
        else:
            guilds[message.guild] = 0
        update_logs(message.author.id)

        channel = message.channel
        try: # TODO make message count spawn on increasing random chance
            print(f"{message.guild.name}: {guilds[message.guild]}")
            # await channel.send(str(guilds[message.guild]))
            global dex
            num = gen_wild() # choose randomly when to spawn with an escalating chance, then reset guilds[message.guild] to 0
            mon = gen_form(dex[num])
            xp(message.author.id)
            # TODO add a friendship increment on message
            global active_spawns
            if message.guild not in active_spawns:
                active_spawns[message.guild] = {}
            active_spawns[message.guild][num] = {
                'num':num,
                'species':mon['name'],
                'name':mon['name'],
                'item':'None',
                'lvl':1, # TODO: assign random level (normal distribution?)
                'ability':gen_ability(),
                'gender':gen_der(mon),
                'xp':0, # TODO: give base xp of random level
                'nature':gen_nature(),
                'ivs':gen_IVs(),
                'evs':[0,0,0,0,0,0],
                'shiny': gen_shiny(),
                'friendship':0,
                'moves':{
                        0:'Struggle',
                        1:'Struggle',
                        2:'Struggle',
                        3:'Struggle'
                    }
            }
            print(active_spawns)
            embed = spawn(active_spawns[message.guild][num])
            await message.channel.send(embed=embed)
        except discord.Forbidden:
            print("Couldn't send message in", message.guild.name,"missing perms")

def gen_form(mon):
    forms = []
    if 'otherFormes' in mon:
        for form in mon['otherFormes']:
            if '-Mega' not in form:
                forms.append(form)
    if not forms:
        return mon
    length = len(forms)
    r = random.randint(0,length)
    if(r==length): return mon
    return mon[forms[r]]

def gen_ability():
    if(random.randint(1, 250)==77):
        return 'H'
    return random.choice([0,1])

def gen_der(mon):
    if 'gender' in mon:
        return mon['gender']
    m = .5
    f = .5
    if 'genderRatio' in mon:
        m = mon['genderRatio']['M']
        f = mon['genderRatio']['F']
    if(random.uniform(0, 1)<m):
        return "M"
    return "F"

def gen_nature():
    natures = ['Hardy', 'Lonely', 'Adamant', 'Naughty', 'Brave', 'Bold', 'Docile', 'Impish', 'Lax', 'Relaxed', 'Modest', 'Mild', 'Bashful', 'Rash', 'Quiet', 'Calm', 'Gentle', 'Careful', 'Quirky', 'Sassy', 'Timid', 'Hasty', 'Jolly', 'Naive', 'Serious']
    return random.choice(natures)

def gen_shiny():
    if(random.randint(1,8192)==777):
        return True
    return False

def gen_IVs():
    return [random.randint(0, 31),random.randint(0, 31),random.randint(0, 31),random.randint(0, 31),random.randint(0, 31),random.randint(0, 31)]

@client.command(aliases=['w'])
async def walk(message):
    ref = db.reference('/trainer/'+str(message.author.id))
    tr = ref.get()
    if tr is None:
        await message.channel.send(f"@{message.author} you are not yet registered. Do \"p!init\" to begin your journey!")
        return
    if message.message.content == 'p!w help' or message.message.content == 'p!w' or message.message.content == 'p!walk' or message.message.content == 'p!walk help':
        await message.channel.send(f"Use \"p!walk [number]\" to start levelling a pokemon you've caught (You can use \"p!pokemon\" to see a list of your caught pokemon)\nUse \"p!info [name]\" to see a dex entry for a pokemon")
        return
    try:
        content = int(message.message.content.split(' ',1)[1])
        if(tr['pkmn'][content]):
            db.reference('/trainer/'+str(message.author.id)+'/Walking').set({'pkmn':content})
            await message.channel.send(f"You are now walking {tr['pkmn'][content]['name']}!")
            return
        await message.channel.send(f"You don\'t have a pokemon {content}. You can use \"p!pokemon\" to see a list of your caught pokemon")
        return
    except:
        await message.channel.send(f"Use \"p!walk [number]\" to start levelling a pokemon you've caught (You can use \"p!pokemon\" to see a list of your caught pokemon)\nUse \"p!info [name]\" to see a dex entry for a pokemon")
        return

@client.command(aliases=['init'])
async def initialization(message):
    # player creates a trainer account
    starters = {'bulbasaur':1,'charmander':4,'squirtle':7,'pikachu':25,'eevee':133,'totodile':152,'cyndaquil':155,'chikorita':158,'treeko':252,'torchic':255,'mudkip':258,'turtwig':387,'piplup':390,'chimchar':393,'snivy':495,'tepig':498,'oshawott':501,'chespin':650,'fennekin':653,'froakie':656,'rowlet':722,'litten':725,'popplio':728,'grookey':810,'scorbunny':813,'sobble':816}
    # Display choices to usern (maybe just a list and ask for p!info if a user wants more)
    # ensure only 'p!init' was recieved
    if message.message.content == 'p!init':
        embed = starter_display()
        await message.channel.send(embed=embed)
        return
    # request choice from user in the form of a 'p!init name'
    content = message.message.content[7:]
    try:
        choice = starters[content]
    except:
        await message.channel.send(f"{content} is not a valid starter choice. Do \"p!init\" if you need a list of starters")
        return
    ref = db.reference('/trainer/'+str(message.author.id))
    tr = ref.get()
    if tr is None:
        ref.set({
            'Walking':{ # TODO make walking into a list of 6 with equal xp gain
                'pkmn':1
            },
            'pkmn':{
                1:{
                    'number':choice,
                    'species':dex[choice]['name'],
                    'name':dex[choice]['name'],
                    'lvl':1,
                    'item':'None',
                    'ability':gen_ability(),
                    'gender':gen_der(dex[choice]),
                    'xp':0,
                    'nature':gen_nature(),
                    'ivs':gen_IVs(),
                    'evs':[0,0,0,0,0,0],
                    'OT':message.author.name,
                    'shiny': gen_shiny(),
                    'friendship':20,
                    'moves':{
                        0:'Struggle',
                        1:'Struggle',
                        2:'Struggle',
                        3:'Struggle'
                    }
                }
            },
            'bag':{
                'PokeDollars':500
            },
            'TMs':{
                'growl':0,
                'leer':0,
                'pound':0,
                'protect':0,
                'scratch':0,
                'tackle':0
            },
            'location':'Kanto'
        })
        await message.channel.send('Trainer Profile Created!')
    else:
        await message.channel.send('Trainer Profile Already Exists!')
    
    # embed = discord.Embed(
    #     title = "Title",
    #     description = "Body of the embed. This is the description"
    #     )
    # imageurl = 'https://discordapp.com/assets/e4923594e694a21542a489471ecffa50.svg'
    # embed.set_image(url = imageurl)
    # embed.set_footer(text = 'This is a footer')
    # embed.set_author(name = 'Author name')
        
    # await message.channel.send(embed=embed)

@client.command()
async def catch(message):
    ref = db.reference('/trainer/'+str(message.author.id))
    tr = ref.get()
    if tr is None:
        await message.channel.send(f"@{message.author} you are not yet registered. Do \"p!init\" to begin your journey!")
        return
    content = lower(message.message.content[8:])
    global active_spawns
    actives = active_spawns[message.guild]
    for num, mon in actives.items():
        if content == mon['name'].lower():
            print(f"{message.author} caught a {mon['name']}")
            ref = db.reference('/trainer/'+str(message.author.id)+'/pkmn')
            tr = ref.get()
            length = len(tr)
            mon['OT'] = message.author.name
            ref = db.reference('/trainer/'+str(message.author.id)+'/pkmn/'+str(length))
            ref.set(mon)
            await message.channel.send(f"<@{message.author.id}> caught a {mon['name']}")
            del active_spawns[message.guild][num]
            return

@client.command(aliases=['i'])
async def info(message):
    ref = db.reference('/trainer/'+str(message.author.id))
    tr = ref.get()
    if tr is None:
        await message.channel.send(f"@{message.author} you are not yet registered. Do \"p!init\" to begin your journey!")
        return
    ref = db.reference('/trainer/'+str(message.author.id)+'/pkmn')
    tr = ref.get()
    if message.message.content == 'p!info' or message.message.content == 'p!i' or message.message.content == 'p!info latest' or message.message.content == 'p!i latest':
        
        embed = info_caught(message.author.id, max(tr.keys())) # TODO change this to max in keys?
        await message.channel.send(embed=embed)
        return
    if message.message.content == 'p!info help' or message.message.content == 'p!i help':
        await message.channel.send(f"Use \"p!info\" to display your last caught pokemon\nUse \"p!info [number]\" to display a specific pokemon you've caught (You can use p!pokemon to see a list of your caught pokemon)\nUse \"p!info [name]\" to see a dex entry for a pokemon")
        return
    content_list = message.message.content.split(' ')
    try:
        content = int(content_list[1])
        embed = info_caught(message.author.id, content)
        await message.channel.send(embed=embed)
        return
    except:
        content = ''
        i = 2
        content+=content_list[1]
        while i<len(content_list):
            content+=' '+content_list[i]
            i+=1
        print(content)
        if content.lower() in keymap:
            embed = info_name(content.lower())
            await message.channel.send(embed=embed)
            return
        await message.channel.send(f"I don't know that Pokemon. Try using \"p!info help\"")
        
@client.command(aliases=['g'])
async def give(message):
    ref = db.reference('/trainer/'+str(message.author.id))
    tr = ref.get()
    if tr is None:
        await message.channel.send(f"@{message.author} you are not yet registered. Do \"p!init\" to begin your journey!")
        return
    ref = db.reference('/trainer/'+str(message.author.id)+'/bag')
    bag = ref.get()
    ref = db.reference('/trainer/'+str(message.author.id)+'/pkmn')
    pkmn = ref.get()
    if message.message.content == 'p!give' or message.message.content == 'p!g' or message.message.content == 'p!give help' or message.message.content == 'p!g help':
        await message.channel.send(f"Use \"p!give\" to let one of your pokemon hold an item from your bag\nUse \"p!give [item name] [number]\" You can use p!pokemon to see a list of your caught pokemon, and p!bag to see a list of your items.")
        return
    content_list = message.message.content.split(' ')[1:]
    item = ' '.join(content_list[:-1])
    if content_list[-1].isnumeric():
        if content_list[-1] in pkmn:
            pkmn = pkmn[int(content_list[-1])]
        else:
            await message.channel.send(f"I can\'t find that pokemon. You can use p!pokemon to see a list of your caught pokemon.")
            return
    else:
        await message.channel.send(f"Use \"p!give [item name] [number]\" to give an item to your pokemon. You can use p!pokemon to see a list of your caught pokemon.")
        return
    if item in bag:
        if pkmn['item']:
            held = pkmn['item']
            if held in bag:
                bag[held]+=1
            else:
                bag[held]=1
        bag[item]-=1
        db.reference('/trainer/'+str(message.author.id)+'/bag').update(bag)
        db.reference('/trainer/'+str(message.author.id)+'/pkmn/'+content_list[-1]).update({'item':item})
        await message.channel.send(f"You gave your {pkmn['name']} a {item} to hold.")
        return
    else:
        await message.channel.send(f"I can\'t find that item. You can use p!bag to see a list of your items.")
        return
    

@client.command(aliases=['p'])
async def pokemon(message):
    ref = db.reference('/trainer/'+str(message.author.id))
    tr = ref.get()
    if tr is None:
        await message.channel.send(f"@{message.author} you are not yet registered. Do \"p!init\" to begin your journey!")
        return
    ref = db.reference('/trainer/'+str(message.author.id)+'/pkmn')
    tr = ref.get()
    limit = 15
    i=1
    out = ''
    global dex
    while i<=limit:
        if i not in tr:
            limit+=1
            pass
        else:
            out+=f"{i} {tr[i]['name']} ({round(sum(tr[i]['ivs'])/(31*6)*100,4)}% ivs)\n"
        i+=1
    out = out[:-1]
    # TODO use reactions as menu buttons
    # make into an embed
    # title {Username}'s Pokemon
    # header {i}-{limit}
    # body {out}
    await message.channel.send(out)

@client.command(aliases=['b'])
async def bag(message):
    ref = db.reference('/trainer/'+str(message.author.id))
    tr = ref.get()
    if tr is None:
        await message.channel.send(f"@{message.author} you are not yet registered. Do \"p!init\" to begin your journey!")
        return
    ref = db.reference('/trainer/'+str(message.author.id)+'/bag')
    bag = ref.get()
    # limit = 20
    # i=1
    out = ''
    for item,quantity in bag.items():
        if i=='PokeDollars':
            continue
        out += f'{i}: {quantity}\n'
    if len(out)==0:
        await message.channel.send('Your bag is empty. :(')
    out = out[:-1]
    await message.channel.send(out)
    # TODO use reactions as menu buttons
    # make into an embed
    # title {Username}'s Bag
    # header {i} PokeDollars
    # body {out}

@client.command()
async def release(message):
    ref = db.reference('/trainer/'+str(message.author.id))
    tr = ref.get()
    if tr is None:
        await message.channel.send(f"@{message.author} you are not yet registered. Do \"p!init\" to begin your journey!")
        return
    content_list = message.message.content.split(' ')
    if not content_list[-1].isnumeric():
        await message.channel.send(f"Use \"p!release [number]\" to permanently release one of your pokemon. You can use p!pokemon to see a list of your caught pokemon.")
        return
    r = content_list[-1]
    ref = db.reference('/trainer/'+str(message.author.id)+'/pkmn')
    pkmn = ref.get()
    if int(r) in pkmn:
        if len(pkmn)==1:
            await message.channel.send('You can\'t release your last pokemon.')
            return
        db.reference('/trainer/'+str(message.author.id)+'/pkmn/'+r).delete()
        await message.channel.send(f"{pkmn[r]['name']} has been released.")
        return
    else:
        await message.channel.send(f"I can\'t find that pokemon. You can use p!pokemon to see a list of your pokemon.")
        return

# client.run('OTk2ODU1MTIyNjI3OTMyMTgw.GX-TgP.IH9_UtW1B3ignnwfScAtdQkyKY35iBwoKkdcO8') old token
client.run(klefkeys.discord_token)
