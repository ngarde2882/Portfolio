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

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import re

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

pokedex = {}
pokedex[122] = {
    'Galarian Form':{
        'Types':{
            0:'Ice',
            1:'Psychic'
        }
    },
    'Name':'Mr. Mime',
    'Number':122,
    'Types':{
        0:'Psychic',
        1:'Fairy'
    }
}
i = 122
url = 'https://bulbapedia.bulbagarden.net/wiki/'
tail = '_(Pok%C3%A9mon)'
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
    print(s)
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