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
  
url = "https://0ijq1i6sp1.execute-api.us-east-1.amazonaws.com/dev/"
r = requests.get(url+'abate')
# r = urllib.request.urlopen(pageurl)
err = BeautifulSoup(r.content, 'html.parser')
f = open('seven.txt')
sevens = []
errs = []
for line in f:
    try:
        r = requests.get(url+line[:-1])
        soup = BeautifulSoup(r.content, 'html.parser')
        if(soup!=err):
            sevens.append(line[:-1])
        print(line[:-1], sevens)
    except:
        errs.append(line[:-1])
        print('err', sevens)
print(sevens)
print('Errors:',errs)