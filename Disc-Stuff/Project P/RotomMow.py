import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import klefkeys

firebase_admin.initialize_app(credentials.Certificate(klefkeys.firebase_cred), {'databaseURL':klefkeys.firebase_url})

# add Catch Rate and XP Type to database from text.csv
def addCR_XP():
    file = open('text.csv','r')
    data = file.readlines()
    for line in data:
        d = line[:-1].split(',')
        d[0] = int(d[0])
        d[2] = int(d[2])
        ref = db.reference('/dex3/'+str(d[0])+'/catchRate')
        ref.set(d[2])
        ref = db.reference('/dex3/'+str(d[0])+'/xpType')
        ref.set(d[3])
    file.close()

# add map of keys and their respective numbers for lookup
def key_num_map():
    ref = db.reference('/dex3/')
    dex = ref.get()
    l = {}
    for mon in dex[1:]:
        l[mon['key']] = mon['num']
        if 'otherFormes' in mon:
            for form in mon['otherFormes']:
                l[mon[form]['key']] = mon['num']
    db.reference('/map/').set(l)

addCR_XP()
key_num_map()