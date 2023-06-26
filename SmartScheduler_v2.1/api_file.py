from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json

cred = credentials.Certificate("auto-smart-scheduler-firebase-adminsdk-w0b4o-816bb8f59c.json")
firebase_admin.initialize_app(cred, {'databaseURL':'https://auto-smart-scheduler-default-rtdb.firebaseio.com/'})

class apievent:
    def __init__(self, start, end, summary): # summary now holds num of attendees
        self.start = start # start time of an event pulled by the gcal API
        self.end = end # end time of an event pulled by the gcal API
        self.summary = summary # num attendees in the event

class apischedule:
    def __init__(self):
        self.user = "" # contact email of the user
        self.apieventlist = list() # list of events the user has, stored as apievent classes
        self.cost = 0

    def print(self):
        for i in self.apieventlist: # print all values of an apischedule to terminal
            print(self.user,":", i.start, i.end, i.summary)

class meeting: # Last possible date the meeting can be held + length of meeting in hours + minutes
    def __init__(self, month, day, year, hour, minutes, name):
        self.month = month
        self.day = day
        self.year = year
        self.hour = hour
        self.minutes = minutes
        self.name = name

# Take the data from a user's google calendar and push it to firebase
def GCal_pull(deadline, user):
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/calendar.events']

    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
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
    ref = db.reference("/Meetings/"+meeting+"/"+email)
    # for every event stored under the user, store the event's start time, end time, and summary
    for i in schedule.apieventlist:
        ref.push({
            "start":i.start,
            "end":i.end,
            "summary":i.summary
        })

# pull all of the apischedule information associated with a meeting all at once from firebase and delete it from firebase
def firebase_pull(meeting):
    # set the reference to the meeting
    ref = db.reference("/Meetings/"+meeting)
    # query holds a json that contains all of the meeting data
    query = ref.get()
    # empty array of schedules
    arryschedules = []
    # i holds each user in the query
    # print(query)
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
    db.reference("/Meetings/"+meeting).delete()
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

    """
    timetable and calendar definitions
    """
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
    iterator=0
    best=[]
    while iterator<best_length:
        best.append([datetime.date(2022, 4, 9), [1000,1000], 800, []])
        iterator+=1
    # print(cal)
    index = best_length-1
    for day in cal:
        # day[0] = date
        # day[1] = timetable
        # set today to hold the values of today as well as the time it currently is
        today = datetime.datetime.now()

        # left and right are used to block out one unit of length to score, and increments after scoring to iterate through the whole day
        left = 0
        right = length-1
        """
        Redundant code for starting search after current time, added a check in scoring
        """
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
                best[index][3]=no_repeat(names,best[2][3])
                # resort best, first by attendees displaced, then by number of user conflicts
                best.sort(key=lambda x: x[1][1])
                best.sort(key=lambda x: x[1][0])
            # increment
            left=left_set
            left+=1
            right+=1
    # print(cal)
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

# Push a meeting onto the meeting creator's Google Claendar with the other users as attendees (which creates invites on their end)
def GCal_push(date, start, length, summary, description, location, attendees):
    # set the permission scope
    SCOPES = ['https://www.googleapis.com/auth/calendar.events']
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
        os.remove(user+'token.json')
    # Throw error
    except HttpError as error:
        print('An error occurred: %s' % error)

# Push information given by which choice in the "best" array onto firebase
# Also pushes the Best array (day/month/year/time/conflict data) and an optional note from the user
def ML_Push(best, victor, note):
    ref = db.reference("/ML")
    full = {}
    i=1
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
        },
        "Note":note
    })

"""
Testing for ML_Push, GCal_Pull, numeric_search, and GCal_push (and, in turn, firebase_pull/push)
"""
# best = [[datetime.date(2022, 4, 9), [0,0], 800, []],[datetime.date(2022, 4, 9), [1,3], 815, ["ngarde2882@tamu.edu"]],[datetime.date(2022, 4, 9), [2,16], 830, ["ngarde2882@tamu.edu","ngarde2882@gmail.com"]]]
# victor = [datetime.date(2022, 4, 9), [0,0], 800, []]
# note = "I prefer early morning meetings"
# ML_Push(best, victor, note)

# last_day = meeting(4, 22, 2022, 1, 0, "Goof Off")
# GCal_pull(last_day, "ngarde2882@tamu.edu")
# GCal_pull(last_day, "collinbennett@tamu.edu")
# print(numeric_search(last_day, 3))
# GCal_push(datetime.date(2022, 4,7), 1100, 4, "summary", "description", "location", ['ngarde2882@tamu.edu','ngarde2882@gmail.com'])

# firebase_pull("Goof Off")
"""
formatting notes for firebase_pull
"""
# for i in firebase_pull():
#     for j in i.apieventlist:
        # print(j.summary, j.start, j.end)
        # CSCE 420 | 2022-03-22T15:55:00-05:00 | 2022-03-22T17:10:00-05:00
        # Year = [0:4]
        # Month = [5:7]
        # Day = [8:10]
        # Time = [11:16]
        # Time = int([11:13]+[14:16]) for HHMM

# takes an array of Contact Emails and returns a list of who is already uploaded to firebase as a bool list of the same length
def pendingStatus(meeting, members):
    # set reference
    ref = db.reference("/Meetings/"+meeting)
    # query holds a json that contains all of the meeting data
    query = ref.get()
    # empty array of schedules
    arryUsers = []
    # i holds each user in the query
    for i in query:
        # set user emails back to '.' from ','
        arryUsers.append(i.replace(',', '.'))
    # create a boolean array that holds false in every position that is the same length as members
    arryBool = [False]*len(members)
    # set i to 0, i is now used as position of arryUsers
    i = 0
    while i < len(arryUsers):
        # j holds position in members
        j = 0
        while j < len(members):
            # whenever members holds the same name as arryUsers, set arryBool to true in the same position as members
            if(arryUsers[i]==members[j]):
                arryBool[j]=True
            j+=1
        i+=1
    # return the array of booleans that tells who is currently in firebase
    return arryBool

"""
Testing for pendingStatus
"""
# ref = db.reference("/")
# ref.set({"Goof Off":{
#     "collinbennett@tamu,edu":"sure",
#     "ngarde2882@gmail,com":"perhaps"
# }})
# print(pendingStatus("Goof Off", ["ngarde2882@tamu.edu","ngarde2882@gmail.com","collinbennett@tamu.edu"]))