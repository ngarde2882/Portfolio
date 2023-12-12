import requests
import urllib.request
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from io import StringIO

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import re

import klefkeys

# def find_betweens(before, after, s):
#     result = []
#     b = len(before)
#     a = len(after)
#     i = 0
#     word = ""
#     while i<(len(s)-b):
#         if(s[i:i+b]==before):
#             i+=b
#             while i<(len(s)-a):
#                 if(s[i:i+a]==after):
#                     result.append(word)
#                     word = ""
#                     i += a
#                     break
#                 else:
#                     word+=s[i]
#                 i+=1
#         i+=1
#     return result

def lower_to_upper(s):
    for c in range(1, len(s)):
        if s[c] == s[c].upper():
            if s[c]=='-': return None # check against Ho-Oh and Porygon-Z that should return None
            if s[c]==' ': return None # check against Mime Jr.
            if s[c]=='.': return None # check against Mr. Mime and Mr. Rime
            if s[c]==':': return None # check against Type: Null
            if s[c]=='\'': return None # check against Farfetch'd and Sirfetch'd
            if s[c-1] == s[c-1].lower():
                return c
    return None

def lower_to_upper_abilities(s):
    for c in range(1, len(s)):
        if s[c] == s[c].upper():
            if s[c]==' ': continue
            if s[c-1] == s[c-1].lower():
                if s[c-1]==' ': continue
                return c
    return None

def ability_string_to_list(s):
    # test cases: ['Pickup or Technician (Meowth', 'Pickup or Technician (Alolan Meowth', 'Pickup or Tough Claws (Galarian Meowth']
    index = lower_to_upper_abilities(s)
    if index:
        s = s[:index]
    out = []
    temp = ''
    for c in s:
        temp+=c
        if ' or ' in temp: # first ability done
            out.append(temp[:-4])
            temp = ''
        if c == '(': # second ability done
            out.append(temp[:-2111])
            temp = ''
            break # no more abilities in string
    if temp: # case of single ability or no forms, temp has ability left in it
        out.append(temp)
    return out

firebase_admin.initialize_app(credentials.Certificate(klefkeys.firebase_cred), {'databaseURL':klefkeys.firebase_url})

url = "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number"
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
# print(soup.prettify(),'\n')

all_matches = soup.find_all('table', attrs={'class':'roundy'})

# # all_matches = soup.find_all('option value')
# all_matches = all_matches[0:9]
# for i in range(9):
#     all_matches[i] = all_matches[i].getText()
typeList = set(['Normal', 'Fire', 'Fighting', 'Water', 'Flying', 'Grass', 'Poison', 'Electric', 'Ground', 'Psychic', 'Ghost', 'Rock', 'Ice', 'Bug', 'Dragon', 'Dark', 'Steel', 'Fairy', 'Unknown', '???'])
pokedex = {}
for j in range(9):
    gen = list(filter(''.__ne__,all_matches[j].getText().split('\n'))) # all_matches[8] is paldea (last)
    gen = gen[4:]
    # print(gen)
    pokemon = {}
    poketype = {}
    ignoretype = False
    form = None
    for num, i in enumerate(gen):
        if i[0]=='#': # number found
            if pokemon:
                pokedex[pokemon['Number']] = pokemon # add previous pokemon to pokedex
            pokemon = {} # begin with new pokemon
            pokemon['Number'] = int(i[1:]) # set number
        elif i in typeList: # type found
            if ignoretype: # continue on second type (already added)
                ignoretype = False
                continue
            else:
                poketype[0] = i # set primary type
                if num<len(gen)-1:
                    if gen[num+1] in typeList: # if next is a secondary type, set secondary type
                        poketype[1] = gen[num+1]
                        ignoretype = True # pass on next iteration
                if form: # if type(s) are part of a form or variant set them under form
                    pokemon[form] = {'Types':poketype}
                    form = None # reset form
                else: # set pokemon's type(s)
                    pokemon['Types'] = poketype
                poketype = {} # clear types
        else: # name found
            if 'Name' not in pokemon: # name of base pokemon found
                index = lower_to_upper(i)
                if not index:
                    pokemon['Name'] = i
                else:
                    pokemon['Name'] = i[:index] # this cuts off Nidoran♀/♂ as well as any form names that are in the base version of a pokemon (CastformNormal or UnownOne form or KyogreKyogre)
                    # print('Cut Name:',pokemon['Name'])
            else: # form or variant found
                form = i[len(pokemon['Name']):] # set form to the name of the form
                while form in pokemon: # duplicate form name (different forms) add underscores until a new form is made
                    form += '_'
                print('FormName:',form, pokemon['Name'])
    pokedex[pokemon['Number']] = pokemon # add last pokemon to pokedex
print(pokedex)
url = 'https://bulbapedia.bulbagarden.net/wiki/'
tail = '_(Pok%C3%A9mon)'
# loop
for i in range(1,151): # TODO 122 is wrong, paste into bulbapy
    print(i)
    if i==29:
        r = requests.get(url+pokedex[i]['Name']+'♀'+tail)
    elif i==32:
        r = requests.get(url+pokedex[i]['Name']+'♂'+tail)
    else:
        r = requests.get(url+pokedex[i]['Name']+tail)
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('table', attrs={'class':'roundy'})
    # img = 'https:' + soup.find('img', attrs={'alt':pokedex[i]['Name']})['src']
    a = []
    try:
        abilitesTable = table.find('b',string='Abilities').parent
    except:
        abilitesTable = table.find('b',string='Ability').parent
        # print(abilitesTable.findAll('td'),len(abilitesTable.findAll('td')))
    for ability in abilitesTable.findAll('td'):
        s = ability.getText()
        s = s.replace(u'\xa0',u' ') # replace unicode nowrap space with regular space
        s = s.replace('Gen IV+','') # delete gen4+ qualifier
        s = s.replace('\n','') # delete extra newlines
        if 'Cacophony' in s: # Cacophony is used as a placeholder on source pages
            continue
        if 'Mega '+pokedex[i]['Name'] in s:
            continue
        if '('+pokedex[i]['Name']+')' in s: # form based abilities
            line = s.split(')')
            for j in line:
                if j == '':
                    continue
                if 'Alolan' in j:
                    a = ability_string_to_list(j)
                    pokedex[i]['Alolan Form']['Abilities'] = a
                    a = []
                elif 'Galarian' in j:
                    a = ability_string_to_list(j)
                    pokedex[i]['Galarian Form']['Abilities'] = a
                    a = []
                elif 'Hisuian' in j:
                    a = ability_string_to_list(j)
                    pokedex[i]['Hisuian Form']['Abilities'] = a
                    a = []
                elif 'Paldean' in j:
                    a = ability_string_to_list(j)
                    pokedex[i]['Paldean Form']['Abilities'] = a
                    a = []
                else: # base form
                    a = ability_string_to_list(j)
                    pokedex[i]['Abilities'] = a
                    a = []
        elif 'Hidden Ability' in s: # found HA
            s = s.replace(' Hidden Ability','')
            index = lower_to_upper_abilities(s)
            if not index: # case: 'Chlorophyll Hidden Ability'
                pokedex[i]['Hidden Ability'] = s
            else: # either base name or form name tagged on end of ability
                if s[index:index+len(pokedex[i]['Name'])]==pokedex[i]['Name']: # base name
                    pokedex[i]['Hidden Ability'] = s[:index]
                else: # form name(s), can have multiple in 1 line
                    if 'Alolan' in s:
                        pokedex[i]['Alolan Form']['Hidden Ability'] = s[:index]
                    if 'Galarian' in s:
                        pokedex[i]['Galarian Form']['Hidden Ability'] = s[:index]
                    if 'Hisuian' in s:
                        pokedex[i]['Hisuian Form']['Hidden Ability'] = s[:index]
                    if 'Paldean' in s:
                        pokedex[i]['Paldean Form']['Hidden Ability'] = s[:index]
        else:
            a = ability_string_to_list(s)
            pokedex[i]['Abilities'] = a # if a form doesnt have unique abilities, inherit base abilities when calling
            a = []
    print(pokedex[i])

# print(pokedex)
# ref = db.reference('/dex2')
# ref.set(pokedex)






# print(str(all_matches[1:8]).split('\n')[2:-1]) # 0:8 pulls all pkmn, 0 has nidoran m/f that error in str
# names = str(all_matches[0:9]).split('\n')[2:-1]
# n = []
# for x in names:
#     bob = x.split('/">')
#     if len(bob)>1:
#         bob = bob[0].split('pokemon/')
#         n.append(bob[1])
# url = "https://serebii.net/pokedex-swsh/"
# url2 = 'https://serebii.net/pokedex-sm/'
# url3 = 'https://www.serebii.net/pokedex-sv/'

# # i = 3 # charmander 2 evos
# # i = 126 # pinsir no evo
# # i = 284 # shroomish level evo
# # i = 285 # breloom 2 ability, 1 HA
# # i = 414 # combee 1 ability, 1 HA, conditional evo
# # i = 

# dex = {}

# i = 1
# while i<=1010: # Iron Leaves last
#     if(i<905):
#         print(n[i])
#         used_url2 = False
#         used_url3 = False
#         r = requests.get(url+n[i])
#         soup = BeautifulSoup(r.content, 'html.parser')
#         all_matches = soup.findAll(attrs={'class':'fooinfo'})
#         # print(all_matches)
#         # print("||||||||||||||||||||||||||||||||||")
#         if(len(all_matches)==0):
#             r = requests.get(url2+str(i+1)+".shtml")
#             soup = BeautifulSoup(r.content, 'html.parser')
#             all_matches = soup.findAll(attrs={'class':'fooinfo'})
#             used_url2 = True
#     else:
#         print(n[i])
#         used_url2 = False
#         used_url3 = True
#         r = requests.get(url3+n[i])
#         soup = BeautifulSoup(r.content, 'html.parser')
#         all_matches = soup.findAll(attrs={'class':'fooinfo'})
#     '''
#     soup -> txt
#     '''
#     # fp = open('pinsir.txt', 'w')
#     # # female = u"\u2640"
#     # for item in all_matches:
#     #     # write each item on a new line
#     #     # if female in item:
#     #     #     item.replace(female, "FEMALE")
#     #     #     print(item)
#     #     #     print("FOUND UNICODE SYMBOL")
#     #     # a = len(item)
#     #     j = str(item).encode("ascii","ignore")
#     #     j = j.decode()
#     #     # b = len(j)
#     #     # if(a!=b):
#     #     #     print("//////////////////////////")
#     #     #     print(item)
#     #     #     print("//////////////////////////")
#     #     #     print(j)
#     #     #     print("//////////////////////////")
#     #     fp.write(j)


#     english = n[i]
#     abilities = []
#     temp = "null"
#     hiddenAbilitity = ""
#     found = False
#     evo = "final evo"
#     evoNames = []
#     english = ""
#     japan = ""
#     french = ""
#     german = ""
#     normalSprite = ""
#     shinySprite = "" 
#     capRate = ""
#     hiddenAbilitity = ""
#     nombre = ""
#     abilities = []
#     types = []
#     evo = []
#     male = "0"
#     female = "0"
#     points = "0"
#     for line in all_matches:
#         line = str(line).encode("ascii","ignore")
#         line = line.decode()
#         if 'img alt=\"Normal' in line: # TODO scrap this and "hardcode" sprites
#             li = line.split('src=\"')
#             li[1] = li[1].split('\" style')
#             li[2] = li[2].split('\" style')
#             # print(li)
#             lie = li
#             normalSprite = li[1][0]
#             shinySprite = li[2][0]
#         if 'Japan' in line:
#             li = line.split("</td><td>")
#             japan = li[1].split("<br/></td>")[0]
#             french = li[2].split("</td></tr>")[0]
#             german = li[3].split("</td></tr>")[0]
#         if 'Male <font color="#499FFF"></font>:</td><td>' in line:
#             li = line.split('</td><td>')
#             male = li[1].split('%')[0]
#             female = li[2].split('%')[0]
#         if 'colspan=\"5\"' in line:
#             # print(cr)
#             # print("||||||||||||||||||||||||||||||||||")
#             # print(line)
#             # print("||||||||||||||||||||||||||||||||||")
#             li = cr.split("info\">")
#             capRate = li[1].split("<")[0]
#         if found:
#             # print(line)
#             if(used_url3):
#                 points = '1,000,000 Points'
#                 nombre = 'Medium'
#             else:
#                 if len(find_betweens(">", "<", line))==2:
#                     holder = find_betweens(">", "<", line)
#                 points = holder[0]
#                 nombre = holder[1]
#                 found = False
#         if 'abilitydex' in line:
#             # if 'Hidden Ability' in line:
#             #     print(line)
#             #     li = line.split('<b>')
#             #     hiddenAbilitity = li[1].split('</b>')[0]
#             #     print(li)
#             # else:
#             #     li = line.split('</b>')
#             #     abilities.append(li[1].split('<b>')[1])
#             # print(line)
#             found = True
#             holder = find_betweens("<b>", "</b>", line)
#             # print(holder)
#             for ab in holder:
#                 if(ab!="Hidden Ability"):
#                     abilities.append(ab)
#                 else:
#                     hiddenAbilitity = holder[-1]
#                     break
#         if 'evoicon' in line:
#             # print(line)
#             evo = find_betweens("evoicon/", ".png", line)
#             evoNames = find_betweens("href=\"/pokedex-swsh/", "\"", line)
#             if len(evoNames)>1:
#                 if evoNames[-1]==evoNames[-2]:
#                     evoNames.pop()
#             if len(evo)>0:
#                 if evo[-1]=="mega384":
#                     evo.pop()
#         cr = temp
#         temp = line
#     all_matches = soup.findAll(attrs={'class':'tooltabcon'})
#     # print(len(all_matches))
#     for line in all_matches:
#         line = str(line).encode("ascii","ignore")
#         line = line.decode()
#         if 'gif' in line:
#             # print(line)
#             types = find_betweens("type/", ".gif", line)
#         if n[i]+" is Genderless" in line:
#             male = "0"
#             female = "0"
#     # p = Poke([english,japan,french,german], normalSprite, shinySprite, male, female, capRate, abilities, hiddenAbilitity, points, nombre, types, evo, evoNames)
#     i+=1
#     if used_url2:
#         normalSprite = "/sunmoon/pokemon/" + str(i) + ".png"
#         shinySprite = "/Shiny/SM/" + str(i) + ".png"
#     ref = db.reference("/dex/"+str(i))
#     ref.set({
#         "Name":{
#             "English":n[i-1],
#             "Japan":japan,
#             "French":french,
#             "German":german
#         },
#         "Male":male,
#         "Female":female,
#         "Types":types,
#         "CapRate":capRate,
#         "Abilities":abilities,
#         "HiddenAbility":hiddenAbilitity,
#         "XPPoints":points,
#         "XPSpeed":nombre,
#         "EvoCondition":evo,
#         "EvoNames":evoNames,
#         "Sprite":normalSprite,
#         "Shiny":shinySprite
#     })

# # print("EN:",english,"JA:",japan,"FR:",french,"GE:",german,"NS:",normalSprite,"SS:",shinySprite,"M:",male,"F:",female,"CR:",capRate,"AB:",abilities,"HA:",hiddenAbilitity,"P:",points,"N:",nombre,"T:",types,"E:",evo,evoNames)

# # dex = {}
# # i=1
# # for x in n:
# #     mon = {}
# #     mon.update({"name":x})
# #     mon.update({"image":url+'art/'+f"{i:03}"+'.png'})
# #     dex.update({i:mon})
# #     i+=1
# # ref = db.reference("/dex")
# # ref.set(dex)
