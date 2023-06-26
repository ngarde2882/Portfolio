import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from st_btn_select import st_btn_select

import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin import db

from PIL import Image

# config = {
#   "apiKey": "AIzaSyCiE6EzVjRVESWeS7jMKHAQrdMf2u75iUw",
#   "authDomain": "project-foo-poll.firebaseapp.com",
#   "databaseURL": "https://project-foo-poll-default-rtdb.firebaseio.com",
#   "projectId": "project-foo-poll",
#   "storageBucket": "project-foo-poll.appspot.com",
#   "messagingSenderId": "758070145684",
#   "appId": "1:758070145684:web:46ca531380c213939dfa81"
# }

# firebase = pyrebase.initialize_app(config)
# authe = firebase.auth()
# database = firebase.database()

# st.markdown(""" <style>
# #MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# </style> """, unsafe_allow_html=True)

image = Image.open("img.png")

cred = credentials.Certificate("project-foo-poll-firebase-adminsdk-7du0h-61e33f73d8.json")
try:
    firebase_admin.initialize_app(cred, {'databaseURL':'https://project-foo-poll-default-rtdb.firebaseio.com'})
    st.set_page_config(page_title='Code Foo Poll', page_icon=image,layout='wide')
except:
    pass


# plt.style.use('bmh')
plt.style.use('dark_background')

if 'bolin' not in st.session_state:
    st.session_state.bolin = True

class pollData:
    def __init__(self,title,choices):
        self.title=title
        self.choices=choices

def Display(bolin):
    if bolin:
        Polls()
    else:
        Results()

def Polls():
    st.title('Code Foo Polls!')
    st.subheader('What is Code Foo?')
    st.write('Code Foo is an eight-week internship opportunity created by IGN to give developers real world experience where interns will be mentored by IGN software engineers!'+
    'As part of my application to Code Foo I have designed a realtime polling webapp where users can vote for their pick in various different fields.')
    st.subheader('So let\'s start voting!')
    ref = db.reference("/Polls")
    query = ref.get()
    # st.write(query)
    pollList = []
    for i in query:
        # st.header(i)
        choices = ['None']
        for j in query[i]:
            choices.append(j)
        pollList.append(pollData(i,choices))

    step = 0
    selection = {}
    for i in pollList:
        st.header(i.title)
        selection[i.title] = st_btn_select(i.choices)
        step += 1
    
    submit = st.button('Submit!')
    if submit:
        for i in selection:
            if selection[i]!='None':
                ref = db.reference("/Polls/"+i+"/"+selection[i])
                q = ref.get()
                ref.set(q+1)
        st.session_state.bolin = False
        st.experimental_rerun()


def Results():
    st.title('Project Foo Results!')

    ref = db.reference("/Polls")
    query = ref.get()
    # st.write(query)
    printPolls(query)
    ret = st.button('Return to Poll!')
    if ret:
        st.session_state.bolin = True
        st.experimental_rerun()

def printPolls(query):
    for i in query:
        step=0
        dat = [None]*len(query[i])
        label = [None]*len(query[i])
        for j in query[i]:
            dat[step] = query[i][j]
            label[step] = j
            step+=1
        st.header(i)
        fig = plt.figure(figsize=(3,3))
        plt.pie(np.array(dat),labels=label)
        st.pyplot(fig)

Display(st.session_state.bolin)