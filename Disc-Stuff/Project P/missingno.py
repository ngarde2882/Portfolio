import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import math

'''
cred = credentials.Certificate("C:/Users/nick2/Desktop/Disc-Stuff/Project P/project-p-4c372-firebase-adminsdk-rkjmv-e4e44aece1.json")
firebase_admin.initialize_app(cred, {'databaseURL':'https://project-p-4c372-default-rtdb.firebaseio.com/'})

ref = db.reference("/dex/")
ss = ref.get()
# print(ss[1]['Name']['English'])
# print(ss[1]['CapRate'])
i = 1
err = []
wild = []
while(i<890):
    # print(i,ss[i]['Name']['English'],ss[i]['CapRate'])
    c = int(ss[i]['CapRate'])
    c = math.ceil(c**1.3)
    wild.extend(i for j in range(c))
    # print(i,ss[i]['Name']['English'],c)
    i+=1
print(len(wild))
# print(len(err), '\n', err)
# ref = db.reference('/trainer/')
# tr = ref.get()
# if(tr['meeee']):
#     print(True)
# else:
#     print(False)
# for mon in ss:
#     print(mon)
'''

starters = {'bulbasaur':1,'charmander':4,'squirtle':7,'pikachu':25,'eevee':133,'totodile':152,'cyndaquil':155,'chikorita':158,'treeko':252,'torchic':255,'mudkip':258,'turtwig':387,'piplup':390,'chimchar':393,'snivy':495,'tepig':498,'oshawott':501,'chespin':650,'fennekin':653,'froakie':656,'rowlet':722,'litten':725,'popplio':728,'grookey':810,'scorbunny':813,'sobble':816}
lst = []
for key, val in starters.items():
    lst.append(key)
string = ''
for val in lst:
    string += val + ', '
print(string)