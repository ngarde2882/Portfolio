from django.shortcuts import render
import pyrebase

config = {
  "apiKey": "AIzaSyCiE6EzVjRVESWeS7jMKHAQrdMf2u75iUw",
  "authDomain": "project-foo-poll.firebaseapp.com",
  "databaseURL": "https://project-foo-poll-default-rtdb.firebaseio.com",
  "projectId": "project-foo-poll",
  "storageBucket": "project-foo-poll.appspot.com",
  "messagingSenderId": "758070145684",
  "appId": "1:758070145684:web:46ca531380c213939dfa81"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

polls = {
    'indie':{
        'option0':'Cory in the House',
        'option1':'Hollow Knight'
    },
    'RPG':{
        'option0':'Halo Infinite',
        'option1':'COD: Cold War',
        'option2':'Destiny 2'
    }
}

ref = database.child("/")
ref.set(polls)

# Create your views here.
def home(request):
    context = { # This will be retrieved from Firebase
        'polls':polls
    }
    return render(request, 'poll/home.html', context)

def results(request):
    return render(request, 'poll/results.html')
