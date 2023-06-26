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
pokeList = [] # a list to store pkmn
#     print(soup.prettify(),'\n')
all_matches = soup.find_all('select')
# all_matches = soup.find_all('option value')
#print(all_matches[0:8])
# print(str(all_matches[1:8]).split('\n')[2:-1]) # 0:8 pulls all pkmn, 0 has nidoran m/f that error in str
names = str(all_matches[0:8]).split('\n')[2:-1]
n = []
for x in names:
    bob = x.split('/">')
    if len(bob)>1:
        bob = bob[0].split('pokemon/')
        n.append(bob[1])

url = "https://serebii.net/pokedex-swsh/"
url2 = 'https://serebii.net/pokedex-sm/'

# i = 3 # charmander 2 evos
# i = 126 # pinsir no evo
# i = 284 # shroomish level evo
# i = 285 # breloom 2 ability, 1 HA
# i = 414 # combee 1 ability, 1 HA, conditional evo
# i = 

dex = {}

i = 494 # snivy  https://serebii.net/pokedex-sm/495.shtml
# while i<989: # stop after zamazenta
print(n[i])
r = requests.get(url2+str(i+1)+".shtml")
soup = BeautifulSoup(r.content, 'html.parser')
all_matches = soup.findAll(attrs={'class':'fooinfo'})
# print(all_matches)
# print("||||||||||||||||||||||||||||||||||")

'''
soup -> txt
'''
fp = open('snivy.txt', 'w')
# female = u"\u2640"
for item in all_matches:
    # write each item on a new line
    # if female in item:
    #     item.replace(female, "FEMALE")
    #     print(item)
    #     print("FOUND UNICODE SYMBOL")
    # a = len(item)
    j = str(item).encode("ascii","ignore")
    j = j.decode()
    # b = len(j)
    # if(a!=b):
    #     print("//////////////////////////")
    #     print(item)
    #     print("//////////////////////////")
    #     print(j)
    #     print("//////////////////////////")
    fp.write(j)
fp.close()