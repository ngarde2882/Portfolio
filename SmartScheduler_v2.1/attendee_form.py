from __future__ import print_function
# import modules - gui
import streamlit as st
import firebase_admin
import pyrebase
from firebase_functions import *
from helper_functions import *
from datetime import date
from firebase_admin import credentials
from firebase_admin import db
from pyrsistent import v

# import modules - algorithm
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json 


#
#Beginning of Nick's Classes
#

# class that hold the information for events
class apievent:
    def __init__(self, start, end, summary): # summary now holds num of attendees
        self.start = start # start time of an event pulled by the gcal API
        self.end = end # end time of an event pulled by the gcal API
        self.summary = summary # num attendees in the event

# class that holds the user email, list of evetns, and the cost of the person
class apischedule:
    def __init__(self):
        self.user = "" # email of the user
        self.apieventlist = list() # list of events the user has
        self.cost = 0

    def print(self):
        for i in self.apieventlist: # print all values of an apischedule to terminal
            print(self.user,":", i.start, i.end, i.summary)

# class that hold the last day a meeting can be held + length of meeting in hours and minutes
class meeting_format: # Last possible day the meeting can be held + length of meeting in hours + minutes
    def __init__(self, month, day, year, hour, minutes, name):
        self.month = month
        self.day = day
        self.year = year
        self.hour = hour
        self.minutes = minutes
        self.name = name

#
# End of Nick's Classes
#




#c
# Beginning of Nick's function imports
#

# Take the data from a user's google calendar and push it to firebase
def GCal_pull(deadline, user):
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/calendar.events']

    # shows basic usage of the Google Calendar API.
    # Prints the start and name of the next 10 events on the user's calendar.
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(user+'token.json'):
        creds = Credentials.from_authorized_user_file(user+'token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(user+'token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        # today in date format
        today = datetime.date.today()
        # dl is the deadline in date format
        dl = datetime.date(deadline.year,deadline.month,deadline.day)
        # delta gives the # of days between dl and today using delta.days
        delta = dl-today
        # later holds the last possible day to schedule a meeting in datetime format
        later = (datetime.datetime(deadline.year,deadline.month,deadline.day,18,0)).isoformat() + 'Z'
        # print delta between start and end to terminal
        print('Getting the upcoming events for the next '+str(delta.days)+' days')
        # API call
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                                timeMax=later, singleEvents=True,
                                                orderBy='startTime').execute()
        # take the items from the results. The items holds start time, end time, summary, description, attendees, ect.
        events = events_result.get('items', [])

        # if nothing is found, nothing gets appended, this user will not be a constraint
        if not events:
            print('No upcoming events found.')
            return

        # create an apischedule for storing a user's events
        sched = apischedule()
        # Prints the start and name of the events from today until the deadline
        for event in events:
            # start holds a given event's start time
            start = event['start'].get('dateTime', event['start'].get('date'))
            # end holds a given event's end time
            end = event['end'].get('dateTime', event['end'].get('date'))
            try:
                # if an event holds values for attendees, att holds them
                att=len(event['attendees'])
            except:
                # if there is no attendees object in the event, set att to 1 (the user)
                att=1
            
            # create an apievent with start,end,att
            ev = apievent(start, end, att) # att was event['summary'] when we were holding event titles and not attendees
            # add the event to the apischedule's event list
            sched.apieventlist.append(ev)
        # once the full schedule is made, push it to firebase
        firebase_push(sched, user, deadline.name)
        
        # delete the user token (need to ask permission before using user data again)
        os.remove(user+'token.json')

    # print an error message
    except HttpError as error:
        print('An error occurred: %s' % error)

# push an apischedule onto firebase under the meeting it is associated with
def firebase_push(schedule, email, meeting):
    email = email.replace('.', ',') # '.' is not an allowed character in Firebase as a title, replaced with ',' for our purposes
    # set the reference to "/meeting name/user email" to store the schedule data under the user
    #ref = db.reference("/"+meeting+"/"+email)
    # for every event stored under the user, store the event's start time, end time, and summary
    for i in schedule.apieventlist:
        ref = db.child("Meetings").child(meeting).child(email)
        #db.child(meeting).child(email).child("start").set(i.start)
        #db.child(meeting).child(email).child("end").set(i.end)
        #db.child(meeting).child(email).child("summary").set(i.summary)
        ref.push({
            "start":i.start,
            "end":i.end,
            "summary":i.summary
        })


#
# End of Nick's function imports
#


# initialize firebase app
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    default_app = firebase_admin.initialize_app(cred, {'databaseURL': 'https://testing-database-1990d-default-rtdb.firebaseio.com/'})

# configuration key
firebaseConfig = {
'apiKey': "AIzaSyBnxI0zg4PRVu1Eh2i_mWBpQcq0tsowkQg",
'authDomain': "testing-database-1990d.firebaseapp.com",
'databaseURL': "https://testing-database-1990d-default-rtdb.firebaseio.com",
'projectId': "testing-database-1990d",
'storageBucket': "testing-database-1990d.appspot.com",
'messagingSenderId': "357278918380",
'appId': "1:357278918380:web:61972cf027b84eda61e7c9",
'measurementId': "G-GMT8S5SETN",
'serviceAccount': "serviceAccountKey.json"
};

# Firebase Authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Database
db = firebase.database()
storage = firebase.storage()

# setting the icon and streamlit title
st.set_page_config(
  page_title = "Join a Meeting",
  page_icon = "🤝"
)

# this function finds the meetings that the attendee is a part of and returns
# the meeting deadline, meeting name, user
def find_user_meetings():
    # initializing a user id and meeting as a placeholder
    user_id = "default"
    meeting = "default"
    # creating empty arrays to hold the current meeting information, deadline information, and user_information
    meeting_information = []
    deadline_information = []
    user_information = []
    # creating arrays that hold the duration information for each event that is to be scheduled
    # this inludes the hours and minutes
    duration_hours_information = []
    duration_minutes_information = []
    

    # potential attendees insert their contact email address to see if they have been invited to any meetings
    with st.form("my_form"):
        # this is done in a form, which is required to have a submission button
        contact_email_address = st.text_input("Please enter your contact email address. This is the address an email was just sent to.")
        # potential attendees also insert their email address used for google calendar
        # this email address is stored for when the events are pushed to their calendars
        google_email_address = st.text_input("Please enter your Google Calendar Email address.")
        # session state below allows the program to remember that the user is logged in
        if 'find_meetings' not in st.session_state: 
            st.session_state.find_meetings = False
        # the callback sets the button to true
        def callback():
            # Login button was clicked!
            st.session_state.find_meetings = True
        # if the login button is pressed, the session state is invoked
        if (
            st.form_submit_button('View my meeting invitations', on_click=callback)
            or st.session_state.find_meetings
        ): 
            # gets the reference for all smart scheduler account holders
            all_users = db.child("User").get()
            # checks if there are no accounts
            if all_users.each() is not None:
                # iterate through all accounts 
                for i in all_users.each():
                    # get each user uid
                    user_id = i.key()
                    # gets the reference for all the meetings under the current user
                    all_meetings = db.child("User").child(i.key()).child("Meetings").get()
                    # checks if there are meetings
                    if all_meetings.each() is not None:
                        # iterates through all the meetings
                        for j in all_meetings.each():
                            # get each meeting name
                            meeting = j.key()
                            # get the duration of the meeting
                            dur_hour_val =  db.child("User").child(i.key()).child("Meetings").child(meeting).child("Meeting Duration - Hours").get().val()
                            dur_min_val =  db.child("User").child(i.key()).child("Meetings").child(meeting).child("Meeting Duration - Minutes").get().val()
                            # appending these values to an array
                            duration_hours_information.append(dur_hour_val)
                            duration_minutes_information.append(dur_min_val)

                            # gets the reference for the list of all the attendees invited to the meeting that have not accepted (pending)
                            all_attendees = db.child("User").child(i.key()).child("Meetings").child(j.key()).child("Attendee List").child("Pending").get()
                            # checks that there are attendees waiting to accept the invitation
                            if all_attendees.each() is not None:
                                # iterates through all the attendees
                                for k in all_attendees.each():
                                    # if the attendee email address matches the form-submitted email address, then they are a part of the current meeting
                                    if (k.val() == contact_email_address):
                                        # append the meeting information to the array
                                        meeting_information.append(j.key())
                                        # append the deadline informatio to the array
                                        deadline_information.append(db.child("User").child(i.key()).child("Meetings").child(j.key()).child("Meeting Deadline").get().val())
                                        # append the meeting organizer to the array
                                        user_information.append(i.key())
    # check if there are no meeting invitations, and if so, let user know
    if len(meeting_information) == 0:
        st.error("No pending meeting invitations.")
    # iterate through each array that holds all of the meeting information
    for l in range(len(meeting_information)):
        #  = datetime.datetime.strptime(deadline_information[l], )
        # get the name of the relevant meeting host from firebase
        host_name = db.child("User").child(user_information[l]).child("Credentials").child("Full Name").get().val()
        # information displayed under the form. This is what the potential meeting attendee will see
        st.success("Meeting: " + meeting_information[l] + "  \nMeeting deadline: " + deadline_information[l] + "  \nMeeting host: " + host_name)
        # array value is the deadline for the current meeting
        deadline_string = deadline_information[l]
        # the three lines below separate the thring into three parts based on the month, day, and year
        deadline_month_string = deadline_string[0:2]
        deadline_day_string = deadline_string[3:5]
        deadline_year_string = deadline_string[6:10]
        # st.write("Deadline month string: " + deadline_month_string)
        # st.write("Deadline day string: " + deadline_day_string)
        # st.write("Deadline year string: " + deadline_year_string)
        
        # converting each string fragment into an integer that can be read by the Gcal_pull function
        deadline_month_int = int(deadline_month_string)
        deadline_day_int = int(deadline_day_string)
        deadline_year_int = int(deadline_year_string)

        # split into meeting accept and meeting decline columns
        col1, col2 = st.columns(2)
        with col1:
            # option to share calendar and accept the meeting invite
            accept = st.button(label = "Share calendar and RSVP", key = meeting_information[l])
            if accept:
                # upload google calendar email address to firebase for use when pushing events to calendar
                # st.write("Deadline month: ")
                # st.write("Deadline day: ")
                # st.write("Deadline year: ")
                # st.write("Duration hours: " + str(duration_hours_information[l]))
                # st.write("Duration minutes: " + str(duration_minutes_information[l]))

                # placing all of the collected values into a format the can be read by GCal_pull
                last_day = meeting_format(deadline_month_int, deadline_day_int, deadline_year_int, duration_hours_information[l], duration_minutes_information[l], meeting_information[l])
                # GCal_pull is called
                # this function gets permission from the user to share calendar data and 
                GCal_pull(last_day, google_email_address)
                # st.write("Past the Gcal pull")
                # check for the user in question under the scheduled event
                google_email_address_modified = google_email_address.replace('.', ',')
                pending_attendees = db.child("User").child(user_information[l]).child("Meetings").child(meeting_information[l]).child("Attendee List").child("Pending").get()
                meetingIndex = db.child("Meetings").child(meeting_information[l]).child(google_email_address_modified).get()
                # if the user has events under the calendar
                if meetingIndex.each() is not None:
                    for m in pending_attendees.each():
                        if (m.val() == contact_email_address):
                            # when the attendee is found, remove instance of attendee from the pending list and insert into the attending list
                            db.child("User").child(user_information[l]).child("Meetings").child(meeting_information[l]).child("Attendee List").child("Pending").child(m.key()).remove()
                            db.child("User").child(user_information[l]).child("Meetings").child(meeting_information[l]).child("Attendee List").child("Attending").child(m.key()).set(contact_email_address)
                            # adding attending google calendar information
                            db.child("User").child(user_information[l]).child("Meetings").child(meeting_information[l]).child("Google Calendar Email List").child(m.key()).set(google_email_address)
                # the rerun command below reruns the script, effectively refreshing the page, minus the meeting the user just accepted
                st.experimental_rerun()
        with col2:                  
            # option to decline attending the meeting
            decline = st.button(label = "Decline meeting", key = meeting_information[l] + "z")
            if decline:
                # change meeting status to declined in the database
                st.write("Declined!")
                # search for the attendee in the attending list, if not there nothing will be done
                pending_attendees = db.child("User").child(user_information[l]).child("Meetings").child(meeting_information[l]).child("Attendee List").child("Pending").get()
                if pending_attendees.each() is not None:
                    for m in pending_attendees.each():
                        if (m.val() == contact_email_address):
                            # when the attendee is found, remove instance of attendee from the attending list and insert into the non attending list
                            db.child("User").child(user_information[l]).child("Meetings").child(meeting_information[l]).child("Attendee List").child("Pending").child(m.key()).remove()
                            db.child("User").child(user_information[l]).child("Meetings").child(meeting_information[l]).child("Attendee List").child("Not Attending").child(m.key()).set(contact_email_address)

# beginning of the streamlit code
# title of web app
st.title("Join a Meeting")
st.success("Smart Scheduler does not store meeting names, only meeting times. Once a meeting is scheduled, all of your information is deleted from our databases.")
find_user_meetings()

    