import Pokedex
import learnsets

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import klefkeys

# This is a database generator that collects and combines data from dicts in Pokedex.py and learnsets.py to publish to my database

firebase_admin.initialize_app(credentials.Certificate(klefkeys.firebase_cred), {'databaseURL':klefkeys.firebase_url})

firedex = {}
for key, val in Pokedex.Pokedex.items():
    # print(key)
    if 'baseSpecies' in val: # forme
        if val['forme'] == 'Gmax': # remove all gmax form data
            del firedex[val['num']]['canGigantamax']
            continue
        elif val['forme'] == 'Starter':
            # this removes connections to the dozen pikachu types (as well as the starter eevee)
            # this will simplify access queries, but the data will remain in case feature is desired in the future
            del firedex[val['num']]['formeOrder']
            del firedex[val['num']]['otherFormes']
            continue
        elif 'Totem' in val['forme']: # remove all totem form data
            totemName = val['name']
            firedex[val['num']]['otherFormes'].remove(totemName)
            if len(firedex[val['num']]['otherFormes']) == 0:
                del firedex[val['num']]['otherFormes']
            firedex[val['num']]['formeOrder'].remove(totemName)
            if len(firedex[val['num']]['formeOrder']) == 1:
                del firedex[val['num']]['formeOrder']
            continue
        elif val['num']<1: # ignore missingno and fakemons
            continue
        # add a deep copy to firedex
        firedex[val['num']][val['name']] = val.copy()
        firedex[val['num']][val['name']]['key'] = key
    else: # base pokemon
        firedex[val['num']] = val.copy()
        firedex[val['num']]['key'] = key
# print(firedex[122])
# for key, val in firedex.items():
#     # print(key)
#     ref = db.reference('/dex3/'+str(key))
#     ref.set(val)

TM_List = {}
def crunch(data, name):
    move = {
        'TM':False,
        'Egg':False,
        'Level':101,
        'Event':False,
        'Tutor':False,
    }
    for i in data:
        if ('M' in i) and (not move['TM']):
            TM_List[name] = 0
            move['TM'] = True
        elif 'E' in i and (not move['Egg']):
            move['Egg'] = True
        elif 'V' in i and (not move['TM']):
            TM_List[name] = 0
            move['TM'] = True
        elif 'T' in i and (not move['Tutor']):
            move['Tutor'] = True
        elif 'S' in i and (not move['Event']):
            move['Event'] = True
        elif 'L' in i:
            l = int(i[2:])
            if l<move['Level']:
                move['Level'] = l
    return move

for num, data in firedex.items():
    moves = {}
    # print(data)
    for move, methods in learnsets.Learnsets[data['key']]['learnset'].items():
        moves[move] = crunch(methods, move)
    data['learnset'] = moves.copy()
    if 'otherFormes' in data:
        for form in data['otherFormes']:
            if data[form]['key'] in learnsets.Learnsets: # megas dont have their keys in learnsets
                if 'learnset' in learnsets.Learnsets[data[form]['key']]: # some forms are in learnsets, but dont actually have unique moves so their learnset is not listed
                    # print(form)
                    moves = {}
                    for move, methods in learnsets.Learnsets[data[form]['key']]['learnset'].items():
                        moves[move] = crunch(methods, move)
                    data[form]['learnset'] = moves.copy()

# print(firedex[19])
ref = db.reference('/TMs')
ref.set(TM_List)
ref = db.reference('/dex3')
ref.set(firedex)