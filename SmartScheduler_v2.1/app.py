from __future__ import print_function
# import modules - gui
from mailgun_emails import * 
import streamlit as st
import firebase_admin
import pyrebase
from sympy import numer
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
# Start of Nick's Classes
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



#
# Start of Nick's Functions
#

# Push information given by which choice in the "best" array onto firebase
# Also pushes the Best array (day/month/year/time/conflict data)
def ML_Push(best, victor):
  # setting the machine learning reference in firebase
  ref = db.child("ML")
  full = {}
  i=1
  # adding all of the proposed schedules to firebase using a for loop
  for j in best:
      full.update({i:{
          "Day":j[0].day,
          "Month":j[0].month,
          "Year":j[0].year,
          "NumConflicts":j[1][0],
          "NumParticipants":j[1][1],
          "Time":j[2],
          "Names":j[3]
      }})
      i+=1
  # once these are loaded in, they are pushed to firebase in the following format
  ref.push({
      "Best":full,
      "Victor":{
          "Day":victor[0].day,
          "Month":victor[0].month,
          "Year":victor[0].year,
          "NumConflicts":victor[1][0],
          "NumParticipants":victor[1][1],
          "Time":victor[2],
          "Names":victor[3]
      }
  })

# Push a meeting onto the meeting creator's Google Claendar with the other users as attendees (which creates invites on their end)
def GCal_push(date, start, length, summary, description, location, attendees, user_email):
  # set the permission scope
  SCOPES = ['https://www.googleapis.com/auth/calendar.events']
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists(user_email+'token.json'):
      creds = Credentials.from_authorized_user_file(user_email+'token.json', SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
          creds.refresh(Request())
      else:
          flow = InstalledAppFlow.from_client_secrets_file(
              'credentials.json', SCOPES)
          creds = flow.run_local_server(port=0)
      # Save the credentials for the next run
      with open(user_email+'token.json', 'w') as token:
          token.write(creds.to_json())

  try:
      service = build('calendar', 'v3', credentials=creds)
      # Call the Calendar API
      # set the event date as a datetime to hold all day and time values
      ev_date = datetime.datetime(date.year, date.month, date.day, start//100, start-start//100*100, 0)
      # event start holds ev_date in iso format
      e_start = ev_date.isoformat()
      # event end holds the same datetime in iso format, but adds the length of the meeting
      e_end = (ev_date + datetime.timedelta(minutes=length*15)).isoformat()

      # arry of attendees
      att = []
      for x in attendees:
          # place all of the attendees into att in json (or dictionary) format
          att.append({'email':x})

      # the event to be pushed onto google calendar
      event_result = service.events().insert(calendarId='primary',
          # the contents of the event, in json format
          body={
              "summary": summary,
              'location': location,
              "description": description,
              "start": {"dateTime": e_start, "timeZone":"America/Chicago",},
              "end": {"dateTime": e_end, "timeZone":"America/Chicago",},
              'attendees': att,
          }
      ).execute()

      # delete the token allowing us to access a user's google calendar
      os.remove(user_email+'token.json')
  # Throw error
  except HttpError as error:
      print('An error occurred: %s' % error)

# Take the data from a user's google calendar and push it to firebase
def GCal_pull(deadline, user):
  # If modifying these scopes, delete the file token.json.
  SCOPES = ['https://www.googleapis.com/auth/calendar.events']

  # Shows basic usage of the Google Calendar API.
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
    # ref = db.child(meeting).child(email)
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

# pull all of the apischedule information associated with a meeting all at once from firebase and delete it from firebase
def firebase_pull(meeting):
    # st.write(meeting)
    # set the reference to the meeting
    # ref = db.reference("/"+meeting)
    ref = db.child("Meetings").child(meeting)
    # query holds a json that contains all of the meeting data
    query = ref.get().val()
    # empty array of schedules
    arryschedules = []
    # i holds each user in the query
    # st.write(ref)
    # st.write(query)
    for i in query:
        # create an apischedule class, set the user to i
        schedule = apischedule()
        # replace the ',' with '.' to reverse the change when we stored it
        schedule.user = i.replace(',', '.')
        # j holds the events under user i
        for j in query[i]:
            # create an apievent with the pulled data, start,end,and attendees
            ev = apievent(query[i][j]['start'], query[i][j]['end'], query[i][j]['summary'])
            # append the event to the schedule
            schedule.apieventlist.append(ev)
        # after all of the events for a user has been appended to their schedule, append the schedule to the list of schedules
        arryschedules.append(schedule)
        # print("/"+meeting+"/"+i)
    # after all users have been pulled, delete all data held under the meeting
    # db.reference("/"+meeting).delete()
    # db.child("Meetings").child(meeting).remove()
    return arryschedules

# sort all user events associated with a meeting onto a calendar
# search through the sorted calendar, looking for the lowest cost options to output
def numeric_search(deadline, best_length):
  # today in date format
  today = datetime.date.today()
  # dl is the deadline in date format
  dl = datetime.date(deadline.year,deadline.month,deadline.day)
  # delta gives the # of days between dl and today using delta.days
  delta = dl-today
  x = 0

  
  #timetable and calendar definitions
  # build the timetable 8am-6pm without having to type it out, don't run this every time
  # y = 800
  # while y<1800:
  #     timetable.append([y],[],[])
  #     y+=15
  #     if y//10%10 == 6:
  #         y+=40
  # print(timetable)

  # calendar of weekdays
  # timetable = [[time, [names], [summary]]]
  # day = [date, timetable] = [date, [[time, [names], [summary]]]]
  # cal = [day] = [[date, [[time, [names], [summary]]]]]
  
  cal = []
  # loop today through deadline, including both edges
  # this creates the calendar array
  while x <= delta.days:
      # future = today + x days where x is 0-delta.days
      future = today+datetime.timedelta(days=x)
      # day = [date, timetable] = [date, [[time, [name,[freeScore]], [summary]]]]
      day = []
      if future.isoweekday()<6:
          # include every weekday between today and deadline, 8am-6pm
          day.append(future)
          # add the timetable 8am-6pm
          day.append([[800, [], []], [815, [], []], [830, [], []], [845, [], []], [900, [], []], [915, [], []], [930, [], []], [945, [], []], [1000, [], []], [1015, 
[], []], [1030, [], []], [1045, [], []], [1100, [], []], [1115, [], []], [1130, [], []], [1145, [], []], [1200, [], []], [1215, [], []], [1230, 
[], []], [1245, [], []], [1300, [], []], [1315, [], []], [1330, [], []], [1345, [], []], [1400, [], []], [1415, [], []], [1430, [], []], [1445, 
[], []], [1500, [], []], [1515, [], []], [1530, [], []], [1545, [], []], [1600, [], []], [1615, [], []], [1630, [], []], [1645, [], []], [1700, 
[], []], [1715, [], []], [1730, [], []], [1745, [], []]])
          cal.append(day)
      x+=1

  #sort
  # run firebase_pull to populate an array of schedules from the database
  arryschedules = firebase_pull(deadline.name)
  # sched holds each person's schedule in the array
  for sched in arryschedules:
      # event holds each event out of a given person's schedule
      for event in sched.apieventlist:
          # store the date, start time, and end time into variables
          # event is in format: 2022-03-22T15:55:00-05:00
          # pos 0-4 stores the year, 5-7 the month, 8-10 the day
          ev_date = datetime.date(int(event.start[0:4]), int(event.start[5:7]), int(event.start[8:10]))
          # pos 11-13 stores the hour, 14-16 the minute
          ev_stime = int(event.start[11:13]+event.start[14:16])
          ev_etime = int(event.end[11:13]+event.end[14:16])
          # day stores [date, [[time, [names], [summary]]]]
          for day in cal:
              # check if the event date is the current the same date in the calendar
              if ev_date == day[0]:
                  # once in the correct date, check through that date's times to look for all conflicting times
                  for time in day[1]:
                      # after we are completely past the event, break to stop iterating through times
                      if ev_etime < time[0]:
                          break
                      # when ev start is < l[0]+15 and ev end is > l[0] add name and summary
                      elif (ev_stime < time[0]+15 and ev_etime > time[0]):
                          # add name and that name's cost
                          time[1].append([sched.user,sched.cost])
                          # add summary
                          time[2].append(event.summary)
                          # increase the cost of rescheduling an event from this user
                          sched.cost+=1
                  # Once we found and finished looking through the correct day, break to move to the next event
                  break
  
  #search
  # cal = [day] = [[date, [[time, [names], [summary]]]]]
  
  # round the length (number of timeslots being checked) up to a 15 min interval
  if deadline.minutes%15==0:
      length = deadline.hour * 4 + deadline.minutes/15
  else:
      length = deadline.hour * 4 + deadline.minutes/15 + 1
  # best holds the date, score numbers, timeslot, and names of the people who have conflicts in that timeslot for the 3 lowest scoring times
  # best = [[date, [scoreNumConflicts, scoreNumParticipants], time, [names]]]
  iterator = 0
  best = []
  while iterator < best_length:
      best.append([datetime.date(2022, 4, 9), [1000,1000], 800, []])
      iterator += 1
  #st.write(cal)
  index = best_length-1
  for day in cal:
      # day[0] = date
      # day[1] = timetable
      # set today to hold the values of today as well as the time it currently is
      today = datetime.datetime.now()

      # left and right are used to block out one unit of length to score, and increments after scoring to iterate through the whole day
      left = 0
      right = length-1

      # Redundant code for starting search after current time, added a check in scoring
      # check current time and start search after it
      # i = 0
      # if today.day <= day[0].day and today.month <= day[0].month and today.year <= day[0].year:
      #     if today.day == day[0].day and today.month == day[0].month and today.year == day[0].year:
      #         i = 0
      #     else:
      #         continue
      # hh = day[1][i][0]//100
      # mm = day[1][i][0]-hh
      # while today.hour < hh:
      #     i+=1
      #     hh = day[1][i][0]//100
      #     mm = day[1][i][0]-hh
      # while today.hour==hh and today.minute<=mm:
      #     i+=1
      #     mm = day[1][i][0]-hh
      #     if today.minute==mm:
      #         left=i
      #         right=left+length-1
      #         if right>39:
      #             continue

      # crawl from left to right distance length, and then increment the search to pan through the whole day
      while right < len(day[1]):
          # score[0] holds Number of Conflicts
          # score[1] holds Number of Participants
          score=[0,0]
          # temp val to hold statrting place
          left_set=left
          # holds a list of every user that has a conflict with a given time
          names = []
          # increment from left to right adding up scores
          while left<=right:
              # score[0] adds the value of the length of a timetable at a given time's name array to result in how many people have a conflict at that time
              score[0]+=len(day[1][left][1])
              # This adds all of the number of attendees of every meeting that is occuring at a given time to add to score[1]
              for participants in day[1][left][2]:
                  # score[1] holds the total number of attendees that would be displaced if we were to ask to reschedule any meetings at a given time
                  score[1]+=int(participants)
              # this adds every user's name that has a conflict at a given time
              if(len(day[1][left][1])>0):
                  for name in day[1][left][1]:
                      names.append(name[0])
                      # name[1] currently holds the value for the user name[0]'s free/busy score
                      # later scoring will use this as well
              left+=1
          # if a lower score than best's highest score is found, replace best's highest score
          # and if the date and time right now is before the propesed date and time
          if score[0]<best[index][1][0] and (today<datetime.datetime(day[0].year,day[0].month,day[0].day,day[1][left_set][0]//100,day[1][left_set][0]-day[1][left_set][0])):
              # currently best is set to length 3 and is constantly sorted to keep the least viable in index 2
              # replace best[2] date with the better scoring date
              best[index][0]=day[0]
              # replace best[2] score with the better scoring score
              best[index][1]=score
              # replace best[2] time with the better scoring time
              best[index][2]=day[1][left_set][0]
              # replace best[2] names with the better scoring names
              # only add each name once
              best[index][3]= no_repeat(names,[])
              # resort best, first by attendees displaced, then by number of user conflicts
              best.sort(key=lambda x: x[1][1])
              best.sort(key=lambda x: x[1][0])
          # increment
          left=left_set
          left+=1
          right+=1
  #st.write("_______________")
  #st.write(best)
  #st.write(cal)
  return best

# place all contents of list1 into list2 without repeats       
def no_repeat(list1,list2):
  for i in list1:
      bolin=True
      for j in list2:
          # if i is found in j, don't append i
          if i==j:
              bolin=False
      if bolin:
          list2.append(i)
  return list2

#
# End of Nick's Functions
#
# function that allows users to schedule an appointment
def schedule_an_appointment():
  # adding title and header
  st.title('Schedule an Appointment')
  # creating a form that allows contacts to be added to a personal address book for every meeting organizer that creates an account
  with st.form("my_form"):
    st.write("Optional - Add contacts to contact list.")
    col1, col2 = st.columns(2) 
    with col1:
      # a first and last name are entered in the same field
      manually_add_name = st.text_input("Enter a full name.")
    with col2:
      # a contact email is entered in the second field
      # note that this value is the email address that notification emails are sent to
      # the google calendar email is different and is what will be used to push out meetings
      manually_add_email = st.text_input("Enter an email.")
    submitted = st.form_submit_button("Enter into contacts.")
    if submitted:
      # once the contents of the form are submitted, the name and email are saved under the account holder's email list in firebase 
      db.child("User").child(user['localId']).child("Email List").child(manually_add_name).set(manually_add_email)
      st.write(manually_add_name + " added to contact list.")
  st.header('Enter appointment details.')
  # beginning of the input parameters
  # meeting name input
  meeting_name = st.text_input("Enter the name of the meeting.")
  if '.' in meeting_name or '$' in meeting_name or '[' in meeting_name or ']' in meeting_name or '#' in meeting_name or '/' in meeting_name:
    st.error("Please do not add special characters, including .$[ ]#/ to the meeting name.") 
  # meeting description input
  meeting_description = st.text_input("Enter a meeting description.")
  # setting today's date, so user cannot set a date earlier than the current day
  # possibly set a maximum deadline so admins cannot schedule a meeting in the too distant future
  today = date.today()
  # scheduling deadline input
  meeting_deadline = st.date_input(
    "Enter a meeting deadline.",
    value=today,
    min_value=today,
    help="Enter a date that you would like to have this meeting by."
  )
  # putting in two side-by-side columns
  col1, col2 = st.columns(2)
  with col1:
    # input for the hours component of the meeting duration
    meeting_duration_hours = st.number_input('Meeting Duration - Hours', min_value=0, max_value=23, value=0, step=1)
  with col2:
    # input for the minutes component of the meeting duration
    meeting_duration_minutes = st.number_input('Meeting Duration - Minutes', min_value=0, max_value = 59, value=0, step=15)
  # pull the array of user contacts
  user_name_array = []
  personal_email_array = []
  user_email_array = []
  email_addresses = db.child("User").child(user['localId']).child("Email List").get()
  if email_addresses.each() is not None:
    for i in email_addresses.each():
      user_name_array.append(i.key())
      personal_email_array.append(i.val()) 
  # input for the meeting attendees
  attendees = st.multiselect(
    'Choose meeting attendees.',
    user_name_array
  )
  # all of the values in attendees are used to get the contact emails from Firebase 
  for i in attendees:
    user_email_reference = db.child("User").child(user['localId']).child("Email List").child(i).get()
    user_email_array.append(user_email_reference.val())
    # the user can easily search by name, and as a confirmation, the person's contact email is printed on screen
    st.write(user_email_reference.val(), " appended to the email list.")
  # input for an optional virtual meeting link
  meeting_location = st.text_input("Enter a virtual meeting link or physical location. (Optional)")

  # this is the button that notifies all of the potential attendees of a future meeting
  if st.button('Generate Meeting and Invite Attendees'):
    # below are checks to ensure all fields are entered on sign up
    # if the meeting name is not entered, throw error
    if meeting_name == "":
      st.error("Please enter a meeting name.")
    # if the meeting description is not entered, throw error
    if meeting_description == "":
      st.error("Please enter a meeting description.")
    # if the meeting duration is not entered, throw error
    if meeting_duration_hours == 0 and meeting_duration_minutes == 0:
      st.error("Please enter a meeting duration greater than zero.")
    # if there are no arrendees in the array, throw error
    if len(user_email_array) == 0:
      st.error("Please enter at least one attendee.")
    if '.' in meeting_name or '$' in meeting_name or '[' in meeting_name or ']' in meeting_name or '#' in meeting_name or '/' in meeting_name:
      st.error("Please do not add special characters, including .$[ ]#/ to the meeting name.") 
    # if everything is entered successfully, 
    else:
      # the meeting parameters are put into firebase
      # this may be scrapped, as we are trying to minimize stored user data
      # convert the meeting deadline to a string
      meeting_deadline_string =  meeting_deadline.strftime('%m/%d/%Y')
      # updating meeting name, meeting description, meeting deadline, mdh, mdm, and meeting link/location in firebase
      db.child("User").child(user['localId']).child("Meetings").child(meeting_name).child("Meeting Name").set(meeting_name)
      db.child("User").child(user['localId']).child("Meetings").child(meeting_name).child("Meeting Description").set(meeting_description)
      db.child("User").child(user['localId']).child("Meetings").child(meeting_name).child("Meeting Deadline").set(meeting_deadline_string)
      db.child("User").child(user['localId']).child("Meetings").child(meeting_name).child("Meeting Duration - Hours").set(meeting_duration_hours)
      db.child("User").child(user['localId']).child("Meetings").child(meeting_name).child("Meeting Duration - Minutes").set(meeting_duration_minutes)
      db.child("User").child(user['localId']).child("Meetings").child(meeting_name).child("Meeting Link or Location").set(meeting_location)
      # adding all of the potential meeting attendees to the "not attending" category by default
      count = 1
      for i in user_email_array:
        guest = "Attendee " + str(count)
        db.child("User").child(user['localId']).child("Meetings").child(meeting_name).child("Attendee List").child("Pending").child(guest).set(i)
        count = count + 1
      
      # getting the deadline as a string 
      deadline_string = meeting_deadline_string
      # parsing the string value for the month, day and year
      deadline_month_string = deadline_string[0:2]
      deadline_day_string = deadline_string[3:5]
      deadline_year_string = deadline_string[6:10]
      # st.write("Deadline month string: " + deadline_month_string)
      # st.write("Deadline day string: " + deadline_day_string)
      # st.write("Deadline year string: " + deadline_year_string)

      # converting the month, day, and year values into integers so GCal_pull gets the correct information
      deadline_month_int = int(deadline_month_string)
      deadline_day_int = int(deadline_day_string)
      deadline_year_int = int(deadline_year_string)
      # inserting values into the last day format
      last_day = meeting_format(deadline_month_int, deadline_day_int, deadline_year_int, meeting_duration_hours, meeting_duration_minutes, meeting_name)
      # triggering a GCal_pull
      # this function gets all the events in the meeting organizer calendar between now and the deadline and places them in firebase
      GCal_pull(last_day, "collinbennett@tamu.edu")
      # once this is done, the appointment is confirmed via the write statement

      # send out the notification emails
      sender_name = db.child("User").child(user['localId']).child("Credentials").child("Full Name").get().val()
      # st.write("The sender name is " + sender_name)
      sender_email = db.child("User").child(user['localId']).child("Credentials").child("Email").get().val()
      # st.write("The sender email is " + sender_email)

    
      # sending emails out to the attendee list
      for i in user_email_array:

        email_invite(
          sender_name, 
          sender_email,
          i,
          meeting_name, 
          meeting_description, 
          meeting_deadline, 
          meeting_duration_hours, 
          meeting_duration_minutes, 
          meeting_location
        )
        st.write("Email sent to " + i)
      # st.write(user_email_array)

      st.success('Appointment confirmed.')



# function that allows a meeting organizer to view the realtime status of meeting invitations
def view_pending_members():
  # adding a title to the function
  st.title("Pending Member Status")
  # reference to all of the meetings under the logged-in user
  all_meetings = db.child("User").child(user['localId']).child("Meetings").get()
  # if there are meetings existing under the user
  if all_meetings.each() is not None:
    # iterate through all of the meetings
    for i in all_meetings.each():
      meeting_name_numeric_search = i.key()
      # creating empty arrays that will hold all members that are attending and that are not attending separately
      attending_list = []
      not_attending_list = []
      pending_list = []
      # getting the meeting information for the Gcal_push
      deadline_string_unprocessed = db.child("User").child(user['localId']).child("Meetings").child(meeting_name_numeric_search).child("Meeting Deadline").get().val()
      # st.write(deadline_string_unprocessed)
      # this function does the same thing seen earlier and parses the deadlien string into useable integer values. 
      deadline_string = deadline_string_unprocessed
      deadline_month_string = deadline_string[0:2]
      deadline_day_string = deadline_string[3:5]
      deadline_year_string = deadline_string[6:10]
      #st.write("Deadline month string: " + deadline_month_string)
      #st.write("Deadline day string: " + deadline_day_string)
      #st.write("Deadline year string: " + deadline_year_string)
      deadline_month_int = int(deadline_month_string)
      deadline_day_int = int(deadline_day_string)
      deadline_year_int = int(deadline_year_string)

      # the duration in hours and minutes is pulled from firebase 
      duration_hour = db.child("User").child(user['localId']).child("Meetings").child(meeting_name_numeric_search).child("Meeting Duration - Hours").get().val()
      duration_minute = db.child("User").child(user['localId']).child("Meetings").child(meeting_name_numeric_search).child("Meeting Duration - Minutes").get().val()

      # list the names of the meetings stored in firebase in a header format
      meeting_name_placeholder = i.key()
      st.header(i.key())


      # reference to all the pending members emails
      all_pending_emails = db.child("User").child(user['localId']).child("Meetings").child(meeting_name_placeholder).child("Attendee List").child("Pending").get()
      # check if the list of attending members is empty
      if all_pending_emails.each() is not None:
        # iterate through the list and append attending members
        for i in all_pending_emails.each():
          pending_list.append(i.val())


      # reference to all the attending members emails
      all_attending_emails = db.child("User").child(user['localId']).child("Meetings").child(meeting_name_placeholder).child("Attendee List").child("Attending").get()
      # check if the list of attending members is empty
      if all_attending_emails.each() is not None:
        # iterate through the list and append attending members
        for i in all_attending_emails.each():
          attending_list.append(i.val())


      # reference to all the non-attending members emails
      all_not_attending_emails = db.child("User").child(user['localId']).child("Meetings").child(meeting_name_placeholder).child("Attendee List").child("Not Attending").get()
      # check if the list of non-attending members is empty
      if all_not_attending_emails.each() is not None:
        # iterate through the list and append non-attending members
        for i in all_not_attending_emails.each():
          not_attending_list.append(i.val())

      # creating columns which list the attending and non attending members for the meeting organizer's convenience
      col1, col2 = st.columns(2) 
      with col1:
        # prints the members attending
        for i in attending_list:
          st.info(i)
        # prints the members that are pending
        for i in pending_list:
          st.info(i)
        # prints the members that are not attending
        for i in not_attending_list:
          st.info(i)
      with col2:
        # prints statement showing the attendee is attending
        for i in attending_list:
          st.success("Attending")
        # prints statement showing the attendee is still pending
        for i in pending_list:
          st.warning("Pending")
        # prints statement showing the attendee has declined the meeting
        for i in not_attending_list:
          st.error("Declined")
      # this slider takes as input the number of scheduling suggestions that the program will generate. This number ranges from 1 to 10.
      rescheduling_number = st.slider(
        label = 'Enter the number of rescheduling suggestions.', 
        min_value = 1,
        max_value = 10,
        value = 3, 
        step = 1,
        help = "This number represents the number of scheduling options you will be able to pick from.",
        key = meeting_name_placeholder
      )
      # this is the very important button
      # it takes everyone's meeting data and schedules a meeting
      # this is regardless of if they have RSVP'd or not

      # session state for schedule a meeting
      # session state below allows the program to remember that the user is logged in
      # st.session_state.schedule_meeting_clicked = False
      if 'schedule_meeting_clicked' not in st.session_state: 
        st.session_state.schedule_meeting_clicked = False
      
      # the callback sets the button to true
      def callback():
        # Login button was clicked!
        st.session_state.schedule_meeting_clicked = True
      
      # st.write(str(st.session_state.schedule_meeting_clicked))
      # if the login button is pressed, the session state is invoked
      if (
        st.button('SCHEDULE MEETING', on_click=callback, key = meeting_name_placeholder, help = "This will schedule a meeting using the data from all user that have RSVP'd to the meeting. It will delete the meeting data and ignore all non-attending members.")
        or st.session_state.schedule_meeting_clicked 
      ): 
  
        # last_day is initialized with the given values
        last_day = meeting_format(deadline_month_int, deadline_day_int, deadline_year_int, duration_hour, duration_minute, meeting_name_numeric_search)
        # best_times is an array generated by numeric_search that contains the best scheduling suggestions
        best_times = numeric_search(last_day, rescheduling_number) # spits out an array of best times
        # users will the pick the meeting time that they would like to push to google calendar
        st.write("Pick a preferred meeting time.")
        key_val = 0
        for i in best_times:
          # st.write(i)
          meeting_day = i[0].strftime("%d")
          meeting_month = i[0].strftime("%B")
          meeting_year = i[0].strftime("%Y")
          meeting_weekday = i[0].strftime("%A")
          meeting_time_hours_original = i[2]//100
          meeting_time_hours = i[2]//100
          am_or_pm = "am"
          if (meeting_time_hours_original >= 12):
            if (meeting_time_hours_original == 12):
              am_or_pm = "pm"
            else:
              meeting_time_hours = meeting_time_hours_original - 12
              am_or_pm = "pm"

          meeting_time_hours_string = str(meeting_time_hours)
          meeting_time_minutes = i[2]-(meeting_time_hours_original*100)
          meeting_time_minutes_string = str(meeting_time_minutes)
          if (meeting_time_minutes == 0):
            meeting_time_minutes_string = "00"
          col1, col2 = st.columns(2)
          with col1:
            # prints the meeting time
            st.write(meeting_weekday + " " + meeting_month + " " + meeting_day + ", " + meeting_year + " @ " + meeting_time_hours_string + ":" + meeting_time_minutes_string  + am_or_pm)
            for j in i[3]:
              # reference to all the non-attending members emails
              time_conflict_names = db.child("User").child(user['localId']).child("Email List").get()
              # check if the list of non-attending members is empty
              if time_conflict_names.each() is not None:
                # iterate through the list and append non-attending members
                for k in time_conflict_names.each():
                  if j == k.val():
                    st.error(k.key() + " has a time conflict.")
          with col2:

            # session state for schedule a meeting
            # session state below allows the program to remember that the user is logged in
            st.session_state.pick_meeting_time_clicked = False
            if 'pick_meeting_time_clicked' not in st.session_state: 
              st.session_state.pick_meeting_time_clicked = False
            
            # the callback sets the button to true
            def callback():
              # Login button was clicked!
              st.session_state.pick_meeting_time_clicked = True
            
            # if the login button is pressed, the session state is invoked
            if (
              st.button('Pick meeting time', on_click=callback, key = key_val)
            ): 
            # button to confirm the meeting time
            # pick_meeting = st.button("Pick meeting time", key=key_val)
            # if pick_meeting:
              # st.write("Initiating Gcal_push!")
              date = i[0]
              # st.write("The date is " + str(date))
              start = i[2]
              # st.write("The start time is " + str(start))
              duration_hours_alpha = db.child("User").child(user['localId']).child("Meetings").child(meeting_name_placeholder).child("Meeting Duration - Hours").get().val()
              # st.write("The duration in hours is " + str(duration_hours_alpha))
              duration_minutes_alpha = db.child("User").child(user['localId']).child("Meetings").child(meeting_name_placeholder).child("Meeting Duration - Minutes").get().val()
              # st.write("The duration in minutes is " + str(duration_minutes_alpha))
              length = duration_hours_alpha * 4 + duration_minutes_alpha / 15
              # st.write("The length is " + str(length))
              desc = db.child("User").child(user['localId']).child("Meetings").child(meeting_name_placeholder).child("Meeting Description").get().val()
              # st.write("The description is " + desc)
              location = db.child("User").child(user['localId']).child("Meetings").child(meeting_name_placeholder).child("Meeting Link or Location").get().val()
              # st.write("The link/location is " + location)
              meeting_host_contact_email = db.child("User").child(user['localId']).child("Credentials").child("Email").get().val()
              # st.write("The host contact email is " + meeting_host_contact_email)


              email_array_alpha = []
              email_array_alpha_reference = db.child("User").child(user['localId']).child("Meetings").child(meeting_name_placeholder).child("Attendee List").child("Attending").get()
              # if there are meetings existing under the user
              # st.write(all_attendees_alpha)
              if email_array_alpha_reference.each() is not None:
                # iterate through all of the meetings
                for m in email_array_alpha_reference.each():
                  email_array_alpha.append(m.val())
              for q in email_array_alpha:
                st.write(q)



              attendees_array = []
              # reference to all of the attendees of the meetinhg under the logged-in user
              all_attendees_alpha = db.child("User").child(user['localId']).child("Meetings").child(meeting_name_placeholder).child("Google Calendar Email List").get()
              # if there are meetings existing under the user
              # st.write(all_attendees_alpha)
              if all_attendees_alpha.each() is not None:
                # iterate through all of the meetings
                for j in all_attendees_alpha.each():
                  attendees_array.append(j.val())
                  # st.write(j.val() + " appended to the contacts list")
              # ML Push implementation
              # note = st.text_input("Mind telling us why you picked that time?")
              # submit_note = st.button("Submit note")
              # if submit_note:
              sender_name = db.child("User").child(user['localId']).child("Credentials").child("Full Name").get().val()
              sender_email = db.child("User").child(user['localId']).child("Credentials").child("Email").get().val()
              meeting_link_location = db.child("User").child(user['localId']).child("Meetings").child(meeting_name_placeholder).child("Meeting Link or Location").get().val()
              meeting_time = meeting_time_hours_string + ":" + meeting_time_minutes_string

              GCal_push(date, start, length, meeting_name_placeholder, desc, location, attendees_array, meeting_host_contact_email)

              for x in email_array_alpha:
                email_confirmation(
                  sender_name,
                  sender_email,
                  x,
                  meeting_name_placeholder,
                  meeting_time,
                  meeting_link_location
                )
                st.write(x + " was sent a confirmation email.")
              # meeting confirmation email
              ML_Push(best_times, i)
              for key in st.session_state.keys():
                del st.session_state[key]
              # delete the meeting from Nick's side
              db.child("Meetings").child(meeting_name_placeholder).remove()
              # delete the meeting from Collin's side
              db.child("User").child(user['localId']).child("Meetings").child(meeting_name_placeholder).remove()
              st.experimental_rerun()
          key_val = key_val + 10
  else:
    st.error("There are no pending meetings.")            

          
          



# delete a user account
def delete_user():
  # display a warning message, so users may know the severity of deleting their account
  st.error('Are you sure you would like to delete your account? It is unrecoverable.')
  # account deletion is performed by a button
  confirm_delete_button = st.button("Confirm Account Deletion")
  if confirm_delete_button == True:
    db.child("User").child(user['localId']).remove()
    st.write("User account data purged from the database.")
    # on confirmation that the button has been pressed, the auth function that deletes the account will be run
    auth.delete_user_account(user['idToken'])
    st.write("Account successfully deleted. Please refresh the page.")

# update a password
def reset_user_password(uid):
  # users wil be asked if they would like to reset their password via email
  st.write("Would you like to reset your password?")
  # their email address is obtained from firebase according to their uid
  email_reference = db.child("User").child(uid).child("Credentials").child("Email").get()
  email = email_reference.val()
  # a button is used to confirm a password reset
  reset_password_button = st.button("Confirm password reset")
  # when the button is pressed, the user will be sent a password reset link via the email they used to sign up
  if reset_password_button:
    auth.send_password_reset_email(email)
    # confirmation message
    st.write("Password reset email sent.")

# update user name
def update_user_name(uid):
  st.write("Enter your new, updated name below.")
  # the first and last name are put side by side so they look good
  # this is done using two columns
  col1, col2 = st.columns(2)
  with col1:
    # input for the updated first name
    new_first_name = st.text_input("New first name")
  with col2:
    # input for the updated last name
    new_last_name = st.text_input("New last name")
  # the full name is gotten by combining the first and last name
  new_full_name = new_first_name + " " + new_last_name
  # the procedure is eecuted via button
  execute_name_change = st.button("Confirm Name Change")
  if (execute_name_change):
    # update the first name
    db.child("User").child(uid).child("Credentials").child("First Name").set(new_first_name)
    # update the last name
    db.child("User").child(uid).child("Credentials").child("Last Name").set(new_last_name)
    # update the full name
    db.child("User").child(uid).child("Credentials").child("Full Name").set(new_full_name)
    # update the name in the email list
    db.child("Email List").child(uid).child("Full Name").set(new_full_name)
    # the database actions below are done to confirm that the name has been changed
    # checking the new first name
    first_name_reference = db.child("User").child(uid).child("Credentials").child("First Name").get()
    first_name_check = first_name_reference.val()
    # checking the new last name
    last_name_reference = db.child("User").child(uid).child("Credentials").child("Last Name").get()
    last_name_check = last_name_reference.val()
    # checking the new full name
    full_name_reference = db.child("User").child(uid).child("Credentials").child("Full Name").get()
    full_name_check = full_name_reference.val()
    # if the names match, the procedure is completed
    if first_name_check == new_first_name and last_name_check == new_last_name and full_name_check == new_full_name:
      st.success("Name change confirmed!")

# initialize firebase app
if not firebase_admin._apps:
  #cred = credentials.Certificate("auto-smart-scheduler-firebase-adminsdk-w0b4o-816bb8f59c.json")
  #default_app = firebase_admin.initialize_app(cred, {'databaseURL': 'https://auto-smart-scheduler-default-rtdb.firebaseio.com/'})
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
  page_title = "Smart Scheduler",
  page_icon = "⏰"
)

# beginning of the streamlit code
# title of web app
st.sidebar.title("Smart Scheduler")

# Authentication
# giving choice of Login and Sign Up
# Sign Up choice bar
choice = st.sidebar.selectbox('Login/Signup',['Login', 'Sign Up'])

# using if else statements to correspond to the three selection box choices
# if registering a new user
full_name_signup = "Placeholder"
if choice == 'Sign Up':
  # users will input full name, broken into first and last name for customization purposes
  first_name_signup = st.sidebar.text_input('Please input your first name.')
  last_name_signup = st.sidebar.text_input('Please input your last name.')
  # email signup paramters
  email_signup = st.sidebar.text_input('Please enter your email address.')
  # password is given for the first time here
  password_signup = st.sidebar.text_input("Please enter your password.", type = 'password')
  # password is confirmed here
  password_confirmation_signup = st.sidebar.text_input("Please re-enter your password.", type = 'password')
  # concatenate first and last name together
  full_name_signup = full_name_function(first_name_signup, last_name_signup)
  # register_user is a button with the phrase "Register user"
  register_user = st.sidebar.button('Register User')

  # if the register user button is pressed
  if register_user:
    # below are checks to ensure all fields are entered on sign up
    # if first name is not entered, throw error
    if first_name_signup == "":
      st.error("Please enter a first name.")
    # if last name is not entered, throw error
    if last_name_signup == "":
      st.error("Please enter a last name.")
    # if email is not entered, throw error
    if email_signup == "":
      st.error("Please enter an email.")
    # if password is not entered, throw error
    if password_signup == "":
      st.error("Please enter a password.")
    # if the confirmation password is not entered, throw error
    if password_confirmation_signup == "":
      st.error("Please enter a password.")
    # if the password is less than six characters, it will not be accepted by the program
    if len(password_signup) < 6:
      st.error("Please enter a password six characters or longer.")
    # if the passwords do not match, throw an error
    if password_signup != password_confirmation_signup:
      st.error("The passwords do not match.")
    # if everything is entered successfully, 
    else:
      # if all the checks pass, then the user account is created
      user = auth.create_user_with_email_and_password(email_signup, password_signup)
      # update the user information in the Firebase realtime database
      # updating the user email
      # db.child("Email List").child(full_name_signup).child("Email").set(email_signup)
      # updating the user full name
      db.child("User").child(user['localId']).child("Credentials").child("Full Name").set(full_name_signup)
      # updating the user id
      db.child("User").child(user['localId']).child("Credentials").child("ID").set(user['localId'])
      # updating the user email
      db.child("User").child(user['localId']).child("Credentials").child("Email").set(email_signup)
      # updating the user first name
      db.child("User").child(user['localId']).child("Credentials").child("First Name").set(first_name_signup)
      # updating the last name
      db.child("User").child(user['localId']).child("Credentials").child("Last Name").set(last_name_signup)
      st.balloons()
      # a login welcome message is displayed after successful sign up
      st.success('Welcome ' + full_name_signup + "!")
      # notifying the user 
      st.info('Login via login drop down tab.')

if choice == 'Login':
  # upon login, user only has to enter email address and password for sign up
  email_login = st.sidebar.text_input('Enter your email address.')
  password_login = st.sidebar.text_input("Enter your password.", type = 'password')

  # session state below allows the program to remember that the user is logged in
  if 'login_button_clicked' not in st.session_state: 
    st.session_state.login_button_clicked = False
  
  # the callback sets the button to true
  def callback():
    # Login button was clicked!
    st.session_state.login_button_clicked = True
  
  # if the login button is pressed, the session state is invoked
  if (
    st.sidebar.button('Login', on_click=callback)
    or st.session_state.login_button_clicked 
  ): 
    # if first name is not entered, throw error
    if email_login == "":
      st.error("Please enter an email address.")
    # if last name is not entered, throw error
    if password_login == "":
      st.error("Please enter a password.")
    else: 
      # the user is now able to sign in successfully
      # automatic sign in will not be used, as this can be unsafe
      user = auth.sign_in_with_email_and_password(email_login, password_login)
      # st.title("Welcome, " + full_name)
      # saving the user's unique ID so it can be used for database retreival purposes
      user_identification_number = user['localId']

      #the admin has two privileges:
      #1. Schedule an Appointment: An admin inputs the desired meeting parameters and is able to schedule a meeting
      #2. View Pending Appointments: An admin can view the progress of invitations for an appointment that is currently waiting scheduling
      choice = st.sidebar.selectbox('Appointment Functions',['None', 'Schedule an Appointment', 'View Pending Members'])
      if choice == 'None':
        pass
      # Schedule an Appointment
      if choice == 'Schedule an Appointment':
        schedule_an_appointment()

      if choice == "View Pending Members":
        view_pending_members()
        
      # there are currently three acount settings to choose from
      account_settings = st.sidebar.selectbox('Account Settings',['None', 'Change Your Name', 'Change Your Password', 'Delete Account'])
      # the none option ensures that nothing is on screen
      if account_settings == 'None':
        pass
      # changing your name can be done with this option
      # supply a new first name and last name and the process is automatic
      if account_settings == 'Change Your Name':
        st.title('Change Your Name')
        update_user_name(user['localId'])
      # this account setting allows the user to reset his or her password via account email
      # an email is sent to the account address and the user follows the link
      if account_settings == 'Change Your Password':
        st.title('Change Password')
        reset_user_password(user['localId'])
      # the button on this feature allows a user to delete their account
      # all of their data will be expunged from the database
      if account_settings == 'Delete Account':
        st.title('Delete Account')
        delete_user()