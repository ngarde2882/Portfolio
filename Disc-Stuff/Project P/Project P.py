import discord
import random
import math
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
ref = db.reference("/dex/")
dex = ref.get()

wild = []
pokedex = {}
i = 1
while(i<1009):
    try:
        c = int(dex[i]['CapRate'])
        c = math.ceil(c**2)
        wild.extend(i for j in range(c))
        pokedex[dex[i]['Name']['English']]=i
    except:
        pass
    i+=1

def gen_wild():
    global wild
    global dex
    mon = random.choice(wild)
    print(dex[mon]['Name']['English'])
    return mon

def spawn(num):
    global dex
    embed = discord.Embed(
        title = "A wild pokemon has spawned",
        description = "Say its name first to catch it",
        # url = url+'/swordshield/pokemon/001.png'
    )
    imageurl = url+dex[num]['Sprite'] # TODO gen random sprites, growlithe meowth show only paldean and hisuan forms
    embed.set_image(url = imageurl)
    # embed.set_footer(text = 'This is a footer')
    # embed.set_author(name = 'Author name')
    return embed

def xp(author_id):
    mon = db.reference('/trainer/'+str(author_id)+'/pkmn/'+str(db.reference('/trainer/'+str(author_id)+'/Walking/pkmn').get())).get()
    xp_speed = dex[mon['number']]['XPSpeed']
    xp_Points = dex[mon['number']]['XPPoints']
    print(mon['ivs'])

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

def make_evostring(arry):
    s = arry[0]
    i = 1
    while(i<len(arry)):
        s+=' => '+arry[i]
        i+=1
    return s

def info_caught(author_id, i):
    ref = db.reference('/trainer/'+str(author_id)+'/pkmn/'+str(i))
    mon = ref.get()
    print(sum(mon['ivs']))
    types = dex[mon['number']]['Types']
    if len(types) == 2:
        typestring = types[0]+', '+types[1]
    else:
        typestring = types[0]
    embed = discord.Embed(
        title = mon['name'],
        description = 'Species: ' + str(mon['species']) +
                        '\nType(s): ' + typestring +
                        '\nNumber: ' + str(mon['number']) +
                        '\nItem: ' + str(mon['item']) +
                        '\nAbility: ' + str(mon['ability']) +
                        '\nGender: ' + str(mon['gender']) +
                        '\nLevel: ' + str(mon['lvl']) +
                        '\nXP: ' + str(mon['xp']) +
                        '\nNature: ' + str(mon['nature']) +
                        '\nIVs: ' + str(round(sum(mon['ivs'])/(31*6)*100,4))) # TODO add stats and do a calculation with the ivs
    if mon['shiny']:
        imageurl = url+dex[mon['number']]['Shiny']
    else:
        imageurl = url+dex[mon['number']]['Sprite']
    embed.set_image(url = imageurl)
    # embed.set_author(name = 'Author name')
    return embed

def info_name(n):
    global pokedex
    num = pokedex[n]
    ref = db.reference('/dex/'+str(num))
    # print('HERE:','/dex/'+str(num))
    mon = ref.get()
    types = mon['Types']
    if len(types) == 2:
        typestring = types[0]+', '+types[1]
    else:
        typestring = types[0]
    abilitystring = ''
    for a in mon['Abilities']:
        abilitystring += a+','
    if 'HiddenAbility' in mon:
        abilitystring += f"({mon['HiddenAbility']}),"
    abilitystring = abilitystring[:-1]
    abilitystring.replace(',',', ')
    genderstring = f"\u2642 {mon['Male']}%, \u2640 {mon['Female']}%"
    embed = discord.Embed(
        title = mon['Name'],
        description = 'Species: ' + str(mon['Name']['English']) +
                        '\nType(s): ' + typestring +
                        '\nNumber: ' + str(num) +
                        '\nAbility(s): ' + abilitystring +
                        '\nGender: ' + genderstring +  # TODO add base stats
                        '\nEvo Line:\n' + make_evostring(mon['EvoNames']) # TODO add evocondition
        # url = url+'/swordshield/pokemon/001.png'
    )
    imageurl = url+mon['Sprite']
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

        channel = message.channel
        try:
            print(f"{message.guild.name}: {guilds[message.guild]}")
            # await channel.send(str(guilds[message.guild]))
            
            # mon = gen_wild() # choose randomly when to spawn with an escalating chance, then reset guilds[message.guild] to 0 TODO reactivate spawns
            xp(message.author.id)
            print('\n')
            return
            global active_spawns
            if message.guild not in active_spawns:
                active_spawns[message.guild] = []
            active_spawns[message.guild] += [mon]
            print(active_spawns)
            embed = spawn(mon)
            await message.channel.send(embed=embed)
        except discord.Forbidden:
            print("Couldn't send message in", message.guild.name,"missing perms")

def gen_ability(n):
    if(dex[n]['HiddenAbility']!=""):
        if(random.randint(1, 250)==69):
            return dex[n]['HiddenAbility']
    return random.choice(dex[n]['Abilities'])

def gen_der(n):
    if(dex[n]['Male']=="0"):
        if(dex[n]['Female']=="0"):
            return "genderless"
        return "female"
    if(random.uniform(0, 100)<float(dex[n]['Male'])):
        return "male"
    return "female"

def gen_nature():
    natures = ['Hardy', 'Lonely', 'Adamant', 'Naughty', 'Brave', 'Bold', 'Docile', 'Impish', 'Lax', 'Relaxed', 'Modest', 'Mild', 'Bashful', 'Rash', 'Quiet', 'Calm', 'Gentle', 'Careful', 'Quirky', 'Sassy', 'Timid', 'Hasty', 'Jolly', 'Naive', 'Serious']
    return random.choice(natures)

def gen_shiny():
    if(random.randint(1,8192)==420):
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
        await message.channel.send(f"You don\' have a pokemon {content}. You can use \"p!pokemon\" to see a list of your caught pokemon")
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
            'Walking':{
                'pkmn':1
            },
            'pkmn':{
                1:{
                    'number':choice,
                    'species':dex[choice]['Name']['English'],
                    'name':dex[choice]['Name']['English'],
                    'lvl':1,
                    'item':'None',
                    'ability':gen_ability(choice),
                    'gender':gen_der(choice),
                    'xp':0,
                    'nature':gen_nature(),
                    'ivs':gen_IVs(),
                    'OT':message.author.name,
                    'shiny': gen_shiny()
                }
            },
            'bag':{
                'PokeDollars':500
            }
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
    valid_names = []
    for num in actives:
        en = dex[num]['Name']['English']
        fr = dex[num]['Name']['French']
        ge = dex[num]['Name']['German']
        ja = dex[num]['Name']['Japan']
        valid_names += [[num, lower([en,fr,ge,ja])]]
    for mon in valid_names:
        if content in mon[1]:
            active_spawns[message.guild].remove(mon[0])
            print(f"{message.author} caught a {mon[1][0]}")
            ref = db.reference('/trainer/'+str(message.author.id)+'/pkmn')
            tr = ref.get()
            length = len(tr)
            catch = mon[0]
            ref = db.reference('/trainer/'+str(message.author.id)+'/pkmn/'+str(length))
            ref.set({
                'number':catch,
                'species':dex[catch]['Name']['English'],
                'name':dex[catch]['Name']['English'],
                'item':'None',
                'lvl':1, # TODO: assign random level (normal distribution?)
                'ability':gen_ability(catch),
                'gender':gen_der(catch),
                'xp':0,
                'nature':gen_nature(),
                'ivs':gen_IVs(),
                'OT':message.author.name,
                'shiny': gen_shiny()
            })
            await message.channel.send(f"<@{message.author.id}> caught a {mon[1][0]}")
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
        embed = info_caught(message.author.id, len(tr)-1)
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
        if content in list(pokedex.keys()):
            embed = info_name(content)
            await message.channel.send(embed=embed)
            return
        await message.channel.send(f"I don't know that Pokemon. Try using \"p!info help\"")
        



# client.run('OTk2ODU1MTIyNjI3OTMyMTgw.GX-TgP.IH9_UtW1B3ignnwfScAtdQkyKY35iBwoKkdcO8') old token
client.run(klefkeys.discord_token)
