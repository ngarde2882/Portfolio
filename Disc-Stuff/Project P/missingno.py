import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import klefkeys

firebase_admin.initialize_app(credentials.Certificate(klefkeys.firebase_cred), {'databaseURL':klefkeys.firebase_url})

# if(dex[n]['Male']=="0"):
#     if(dex[n]['Female']=="0"):
#         return "genderless"
#     return "female"
# if(random.uniform(0, 100)<float(dex[n]['Male'])):
#     return "male"
# return "female"
import random
import datetime
# trainer_logs = {1: [datetime.datetime(2024, 1, 30, 16, 2, 10, 605924), datetime.datetime(2024, 1, 30, 16, 2, 10, 605924), datetime.datetime(2024, 1, 30, 16, 2, 10, 605924), datetime.datetime(2024, 1, 30, 16, 2, 10, 605924)]}
# def update_logs(id):
#     global trainer_logs
#     now = datetime.datetime.now()
#     if id not in trainer_logs: trainer_logs[id] = []
#     trainer_logs[id].append(now)
#     for i in range(len(trainer_logs[id])): # store oldest at 0 and newest at append
#             if trainer_logs[id][0] > now - datetime.timedelta(minutes=5):
#                 break
#             else:
#                 trainer_logs[id].pop(0)
# update_logs(1)

print('Baby-Doll Eyes'.replace(' ','').replace('-','').lower())

ref = db.reference('/dex3')
dex = ref.get()
evos = set()
items = set()
cond = set()
for mon in dex[1:]:
    if 'evoType' in mon:
        evos.add(mon['evoType'])
        if 'evoItem' in mon:
            items.add(mon['evoItem'])
    if 'evoCondition' in mon:
        cond.add(mon['evoCondition'])
    if 'otherFormes' in mon:
        for form in mon['otherFormes']:
            if 'evoType' in mon[form]:
                evos.add(mon[form]['evoType'])
                if 'evoItem' in mon[form]:
                    items.add(mon[form]['evoItem'])
            if 'evoCondition' in mon[form]:
                cond.add(mon[form]['evoCondition'])
print(evos)
print(items)
print(cond)