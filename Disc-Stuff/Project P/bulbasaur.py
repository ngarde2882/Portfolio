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



# stringy = "<td align=\"left\" class=\"fooinfo\" colspan=\"5\">\n<a href=\"/abilitydex/honeygather.shtml\"><b>Honey Gather</b></a>: May pick up a Honey after battle; the higher the level, the higher the chance. <br/>\n<b>Hidden Ability</b><!-- <i>(Available)</i>-->: <br/><a href=\"/abilitydex/hustle.shtml\"><b>Hustle</b></a>: Damage from physical attacks is increased by 50%, but average accuracy is only 80%. </td>"

# print(find_betweens("<b>", "</b>", stringy))


# def lower(string_in):
#     if type(string_in) == list: # list
#         for i in range(len(string_in)):
#             for c in string_in[i]:
#                 string_in[i] = string_in[i].replace(c, c.lower())
#             print('s:',string_in[i])
#         print('s_i',string_in)
#         return string_in
#     elif type(string_in) == str: # string
#         for c in string_in:
#             string_in = string_in.replace(c, c.lower())
#         return string_in
#     else:
#         raise('ONLY STRINGS AND LISTS OF STRINGS CAN BE INPUT IN THIS FUNCTION')
    
# string = ['oNe', 'Two', 'thrEE']

# print(lower(string))

# import klefkeys

# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db
# firebase_admin.initialize_app(credentials.Certificate(klefkeys.firebase_cred), {'databaseURL':klefkeys.firebase_url})

# function that checks for lowercase before an uppercase, then outputs position of uppercase
# def lower_to_upper(s):
#     for c in range(1, len(s)):
#         if s[c] == s[c].upper():
#             if s[c]=='-': return None # check against Ho-Oh and Porygon-Z that should return None
#             if s[c]==' ': return None # check against Mime Jr.
#             if s[c]=='.': return None # check against Mr. Mime and Mr. Rime
#             if s[c-1] == s[c-1].lower():
#                 return c
#     return None

# mon = 'Mr. Mime'
# i = lower_to_upper(mon)
# # print(mon[:i])
# pokedex = {
#     59:{
#         'Name':'Arcanine'
#     }
# }
# s = 'JustifiedArcanine Hidden Ability'
# t = 'Rock HeadHisuian Arcanine Hidden Ability'
# index = lower_to_upper(s)
# if s[index:index+len(pokedex[59]['Name'])]==pokedex[59]['Name']:
#     print(s[:index])
# if t[index:index+len(pokedex[59]['Name'])]==pokedex[59]['Name']:
#     print(t[:index])
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
def lower_to_upper_abilities(s):
    for c in range(1, len(s)):
        if s[c] == s[c].upper():
            if s[c]==' ': continue
            if s[c-1] == s[c-1].lower():
                if s[c-1]==' ': continue
                return c
    return None
i=128
pokedex = {}
# pokedex[i] = {
#     'Galarian Form':{
#         'Types':{
#             0:'Fighting',
#             1:'Flying'}},
#     'Name':'Zapdos',
#     'Number':i,
#     'Types':{
#             0:'Electric',
#             1:'Flying'}}
pokedex[i] = {
    'Name':'Tauros',
    'Number':i,
    'Types':{
        0:'Ghost',
        1:'Poison'
    }
}
url = 'https://bulbapedia.bulbagarden.net/wiki/'
tail = '_(Pok%C3%A9mon)'
if i==29:
    r = requests.get(url+pokedex[i]['Name']+'♀'+tail)
elif i==32:
    r = requests.get(url+pokedex[i]['Name']+'♂'+tail)
else:
    r = requests.get(url+pokedex[i]['Name']+tail)
soup = BeautifulSoup(r.content, 'html.parser')
table = soup.find('table', attrs={'class':'roundy'})
# img = 'https:' + soup.find('img', attrs={'alt':pokedex[i]['Name']})['src']
# catchTable = table.find(href='/wiki/Catch_rate').parent.parent
# print(catchTable.find('td').get_text().split(' ')[0])
genderTable = table.find(href="/wiki/List_of_Pok%C3%A9mon_by_gender_ratio").parent.parent
genderless = True
genderString = ''
for g in genderTable.find_all('span')[2:]:
    genderless = False
    g = g.get_text()
    if g == ',':
        continue
    genderString+=f'({g})'
if genderless:
    genderString = 'genderless'
pokedex[i]['Gender'] = genderString

print(pokedex[i])