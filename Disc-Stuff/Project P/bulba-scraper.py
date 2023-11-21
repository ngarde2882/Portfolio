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

# print("EN:",english,"JA:",japan,"FR:",french,"GE:",german,"NS:",normalSprite,"SS:",shinySprite,"M:",male,"F:",female,"CR:",capRate,"AB:",abilities,"HA:",hiddenAbilitity,"P:",points,"N:",nombre,"T:",types,"E:",evo,evoNames)
# TODO add base stats
class Poke: 
    def __init__(self, names, normalSprite, shinySprite, male, female, capRate, abilities, hiddenAbilitity, xpPoints, xpSpeed, types, evoCond, evoNames):
        self.names
        self.normalSprite
        self.shinySprite
        self.male
        self.female
        self.capRate
        self.abilities
        self.hiddenAbilitity
        self.xpPoints
        self.xpSpeed
        self.types
        self.evoCond
        self.evoNames
    
    def __repr__(self): 
        return "Names:% s NS:% s SS:% s M:% s F:% s CR:% s AB:% s HA:% s P:% s Speed:% s T:% s E:% s % s" % (self.names, self.normalSprite, self.shinySprite, self.male, self.female, self.capRate, self.abilities, self.hiddenAbilitity, self.xpPoints, self.xpSpeed, self.types, self.evoCond, self.evoNames)
    # print([t])
    # [Test a:1234 b:5678]

def find_betweens(before, after, s):
    result = []
    b = len(before)
    a = len(after)
    i = 0
    word = ""
    while i<(len(s)-b):
        if(s[i:i+b]==before):
            i+=b
            while i<(len(s)-a):
                if(s[i:i+a]==after):
                    result.append(word)
                    word = ""
                    i += a
                    break
                else:
                    word+=s[i]
                i+=1
        i+=1
    return result

cred = credentials.Certificate("C:/Users/nick2/Desktop/Disc-Stuff/Project P/project-p-4c372-firebase-adminsdk-rkjmv-e4e44aece1.json")
firebase_admin.initialize_app(cred, {'databaseURL':'https://project-p-4c372-default-rtdb.firebaseio.com/'})
  
url = "https://serebii.net/pokemon/"
r = requests.get(url)
# r = urllib.request.urlopen(pageurl)
soup = BeautifulSoup(r.content, 'html.parser')
# print(soup.prettify(),'\n')
all_matches = soup.find_all('select')
# all_matches = soup.find_all('option value')
#print(all_matches[0:8])
# print(str(all_matches[1:8]).split('\n')[2:-1]) # 0:8 pulls all pkmn, 0 has nidoran m/f that error in str
names = str(all_matches[0:9]).split('\n')[2:-1]
n = []
for x in names:
    bob = x.split('/">')
    if len(bob)>1:
        bob = bob[0].split('pokemon/')
        n.append(bob[1])
url = "https://serebii.net/pokedex-swsh/"
url2 = 'https://serebii.net/pokedex-sm/'
url3 = 'https://www.serebii.net/pokedex-sv/'

# i = 3 # charmander 2 evos
# i = 126 # pinsir no evo
# i = 284 # shroomish level evo
# i = 285 # breloom 2 ability, 1 HA
# i = 414 # combee 1 ability, 1 HA, conditional evo
# i = 

dex = {}

i = 905 #TODO this skips the first 1-889, then skips hisui
while i<1010: # stop after zamazenta
    if(i<905):
        print(n[i])
        used_url2 = False
        used_url3 = False
        r = requests.get(url+n[i])
        soup = BeautifulSoup(r.content, 'html.parser')
        all_matches = soup.findAll(attrs={'class':'fooinfo'})
        # print(all_matches)
        # print("||||||||||||||||||||||||||||||||||")
        if(len(all_matches)==0):
            r = requests.get(url2+str(i+1)+".shtml")
            soup = BeautifulSoup(r.content, 'html.parser')
            all_matches = soup.findAll(attrs={'class':'fooinfo'})
            used_url2 = True
    else:
        print(n[i])
        used_url2 = False
        used_url3 = True
        r = requests.get(url3+n[i])
        soup = BeautifulSoup(r.content, 'html.parser')
        all_matches = soup.findAll(attrs={'class':'fooinfo'})
    '''
    soup -> txt
    '''
    # fp = open('pinsir.txt', 'w')
    # # female = u"\u2640"
    # for item in all_matches:
    #     # write each item on a new line
    #     # if female in item:
    #     #     item.replace(female, "FEMALE")
    #     #     print(item)
    #     #     print("FOUND UNICODE SYMBOL")
    #     # a = len(item)
    #     j = str(item).encode("ascii","ignore")
    #     j = j.decode()
    #     # b = len(j)
    #     # if(a!=b):
    #     #     print("//////////////////////////")
    #     #     print(item)
    #     #     print("//////////////////////////")
    #     #     print(j)
    #     #     print("//////////////////////////")
    #     fp.write(j)


    english = n[i]
    abilities = []
    temp = "null"
    hiddenAbilitity = ""
    found = False
    evo = "final evo"
    evoNames = []
    english = ""
    japan = ""
    french = ""
    german = ""
    normalSprite = ""
    shinySprite = "" 
    capRate = ""
    hiddenAbilitity = ""
    nombre = ""
    abilities = []
    types = []
    evo = []
    male = "0"
    female = "0"
    points = "0"
    for line in all_matches:
        line = str(line).encode("ascii","ignore")
        line = line.decode()
        if 'img alt=\"Normal' in line: # TODO scrap this and "hardcode" sprites
            li = line.split('src=\"')
            li[1] = li[1].split('\" style')
            li[2] = li[2].split('\" style')
            # print(li)
            lie = li
            normalSprite = li[1][0]
            shinySprite = li[2][0]
        if 'Japan' in line:
            li = line.split("</td><td>")
            japan = li[1].split("<br/></td>")[0]
            french = li[2].split("</td></tr>")[0]
            german = li[3].split("</td></tr>")[0]
        if 'Male <font color="#499FFF"></font>:</td><td>' in line:
            li = line.split('</td><td>')
            male = li[1].split('%')[0]
            female = li[2].split('%')[0]
        if 'colspan=\"5\"' in line:
            # print(cr)
            # print("||||||||||||||||||||||||||||||||||")
            # print(line)
            # print("||||||||||||||||||||||||||||||||||")
            li = cr.split("info\">")
            capRate = li[1].split("<")[0]
        if found:
            # print(line)
            if(used_url3):
                points = '1,000,000 Points'
                nombre = 'Medium'
            else:
                if len(find_betweens(">", "<", line))==2:
                    holder = find_betweens(">", "<", line)
                points = holder[0]
                nombre = holder[1]
                found = False
        if 'abilitydex' in line:
            # if 'Hidden Ability' in line:
            #     print(line)
            #     li = line.split('<b>')
            #     hiddenAbilitity = li[1].split('</b>')[0]
            #     print(li)
            # else:
            #     li = line.split('</b>')
            #     abilities.append(li[1].split('<b>')[1])
            # print(line)
            found = True
            holder = find_betweens("<b>", "</b>", line)
            # print(holder)
            for ab in holder:
                if(ab!="Hidden Ability"):
                    abilities.append(ab)
                else:
                    hiddenAbilitity = holder[-1]
                    break
        if 'evoicon' in line:
            # print(line)
            evo = find_betweens("evoicon/", ".png", line)
            evoNames = find_betweens("href=\"/pokedex-swsh/", "\"", line)
            if len(evoNames)>1:
                if evoNames[-1]==evoNames[-2]:
                    evoNames.pop()
            if len(evo)>0:
                if evo[-1]=="mega384":
                    evo.pop()
        cr = temp
        temp = line
    all_matches = soup.findAll(attrs={'class':'tooltabcon'})
    # print(len(all_matches))
    for line in all_matches:
        line = str(line).encode("ascii","ignore")
        line = line.decode()
        if 'gif' in line:
            # print(line)
            types = find_betweens("type/", ".gif", line)
        if n[i]+" is Genderless" in line:
            male = "0"
            female = "0"
    # p = Poke([english,japan,french,german], normalSprite, shinySprite, male, female, capRate, abilities, hiddenAbilitity, points, nombre, types, evo, evoNames)
    i+=1
    if used_url2:
        normalSprite = "/sunmoon/pokemon/" + str(i) + ".png"
        shinySprite = "/Shiny/SM/" + str(i) + ".png"
    ref = db.reference("/dex/"+str(i))
    ref.set({
        "Name":{
            "English":n[i-1],
            "Japan":japan,
            "French":french,
            "German":german
        },
        "Male":male,
        "Female":female,
        "Types":types,
        "CapRate":capRate,
        "Abilities":abilities,
        "HiddenAbility":hiddenAbilitity,
        "XPPoints":points,
        "XPSpeed":nombre,
        "EvoCondition":evo,
        "EvoNames":evoNames,
        "Sprite":normalSprite,
        "Shiny":shinySprite
    })

# print("EN:",english,"JA:",japan,"FR:",french,"GE:",german,"NS:",normalSprite,"SS:",shinySprite,"M:",male,"F:",female,"CR:",capRate,"AB:",abilities,"HA:",hiddenAbilitity,"P:",points,"N:",nombre,"T:",types,"E:",evo,evoNames)

# dex = {}
# i=1
# for x in n:
#     mon = {}
#     mon.update({"name":x})
#     mon.update({"image":url+'art/'+f"{i:03}"+'.png'})
#     dex.update({i:mon})
#     i+=1
# ref = db.reference("/dex")
# ref.set(dex)
