from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import sys

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json

class event:
    def __init__(self, start, end, stamp, uid, created, description, lastMod, location, seq, status, summary, transp):
        self.start = start
        self.end = end
        self.stamp = stamp
        self.uid = uid
        self.created = created
        self.description = description
        self.lastMod = lastMod
        self.location = location
        self.seq = seq
        self.status = status
        self.summary = summary
        self.transp = transp
        self.sYear = int(start[0:4])
        self.eYear = int(end[0:4])
        self.sMonth = int(start[4:6])
        self.eMonth = int(end[4:6])
        self.sDay = int(start[6:8])
        self.eDay = int(end[6:8])
        self.sTime = int(start[9:15])
        self.eTime = int(end[9:15])

    # Print event in .ics format
    def print(self):
        print("BEGIN:VEVENT\nDTSTART:"+self.start+"\nDTEND:"+self.end+"\nDTSTAMP:"+self.stamp+"\nUID:"+self.uid+"\nCREATED:"+self.created+"\nDESCRIPTION:"+self.description+"\nLAST-MODIFIED:"+self.lastMod+"\nLOCATION:"+self.location+"\nSEQUENCE:"+self.seq+"\nSTATUS:"+self.status+"\nSUMMARY:"+self.summary+"\nTRANSP:"+self.transp+"\nEND:VEVENT")
    
    # after changing d/m/y/time, correct the start or end variable
    def reset_times(self):
        start = str(sYear)+str(sMonth)+str(sDay)+start[8]+str(sTime)+start[15]
        end = str(eYear)+str(eMonth)+str(eDay)+end[8]+str(eTime)+end[15]

class apievent:
    def __init__(self, start, end, summary):
        self.start = start
        self.end = end
        self.summary = summary

class apischedule:
    def __init__(self):
        self.user = ""
        self.apieventlist = list()

    def print(self):
        for i in self.apieventlist:
            print(user+":", i.start, i.end, i.summary)

class schedule:
    def __init__(self, proid, version, calScale, method, calName, timeZone, tzid, tzLocation, dlFrom, dlTo, dltzName, dlStart, dlRule, standardFrom, standardTo, standardtzName, standardStart, standardRule):
        self.proid = proid
        self.version = version
        self.calScale = calScale
        self.method = method
        self.calName = calName
        self.timeZone = timeZone
        self.tzid = tzid
        self.tzLocation = tzLocation
        self.dlFrom = dlFrom
        self.dlTo = dlTo
        self.dltzName = dltzName
        self.dlStart = dlStart
        self.dlRule = dlRule
        self.standardFrom = standardFrom
        self.standardTo = standardTo
        self.standardtzName = standardtzName
        self.standardStart = standardStart
        self.standardRule = standardRule
        self.eventlist = list()

    # Print schedule in .ics format
    def print(self):
        print("BEGIN:VCALENDAR\nPRODID:"+self.proid+"\nVERSION:"+self.version+"\nCALSCALE:"+self.calScale+"\nMETHOD:"+self.method+"\nX-WR-CALNAME:"+self.calName+"\nX-WR-TIMEZONE:"+self.timeZone+"\nBEGIN:VTIMEZONE\nTZID:"+self.tzid+"\nX-LIC-LOCATION:"+self.tzLocation+"\nBEGIN:DAYLIGHT\nTZOFFSETFROM:"+self.dlFrom+"\nTZOFFSETTO:"+self.dlTo+"\nTZNAME:"+self.dltzName+"\nDTSTART:"+self.dlStart+"\nRRULE:"+self.dlRule+"\nEND:DAYLIGHT\nBEGIN:STANDARD\nTZOFFSETFROM:"+self.standardFrom+"\nTZOFFSETTO:"+self.standardTo+"\nTZNAME:"+self.standardtzName+"\nDTSTART:"+self.standardStart+"\nRRULE:"+self.standardRule+"\nEND:STANDARD\nEND:VTIMEZONE")
        j=0
        for i in self.eventlist:
            self.eventlist[j].print()
            j+=1
        return "END:VCALENDAR"

class meeting:
    def __init__(self, month, day, year, hour, minutes):
        self.month = month
        self.day = day
        self.year = year
        self.hour = hour
        self.minutes = minutes

def GCal_pull(deadline, apischedule):
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
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
        later = (datetime.datetime.utcnow() + datetime.timedelta(days=delta.days)).isoformat() + 'Z'
        print('Getting the upcoming events for the next '+str(delta.days)+' days')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              timeMax=later, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the events from today until the deadline
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            ev = apievent(start, end, event['summary'])
            apischedule.apieventlist.append(ev)
        
        # os.remove("token.json")

    except HttpError as error:
        print('An error occurred: %s' % error)

# function to create a list of all times in UTC per day between today and the dealine inclusively
def event_emptysearch(schedules, deadline):
    # today in date format
    today = datetime.date.today()
    # dl is the deadline in date format
    dl = datetime.date(deadline.year,deadline.month,deadline.day)
    # delta gives the # of days between dl and today using delta.days
    delta = dl-today
    # empties contains empty areas
    # empties = [[datetime.date(year,month,day),[t1,t2]],[datetime.date(year,month,day),[t1,t2]],...]
    empties = []
    x = 0
    # loop today through deadline, including both edges
    while x <= delta.days:
        # future = today + x days where x is 0-delta.days
        future = today+datetime.timedelta(days=x)
        if future.isoweekday()<6:
            #include every weekday between today and deadline 8am-6pm
            empties.append([future,[140000,240000]])
        x+=1
    # i is each schedule in the list of schedules
    for i in schedules:
        # j is each event in the current schedule i
        for j in i.eventlist:
            # print("Year:  "+str(j.sYear)+" | "+str(today.year))
            # print("Month: "+str(j.sMonth)+" | "+str(today.month))
            # print("Day:   "+str(j.sDay)+" | "+str(today.day))
            # if the current event is today or later, ignore passed events
            if ((j.sYear>=today.year)and(j.sMonth>=today.month)and(j.sDay>=today.day)):
                # evDate is the current j event in date format
                evDate = datetime.date(j.sYear,j.sMonth,j.sDay)
                dayOfWeek = evDate.isoweekday()
                # if evDate is on a weekday
                if dayOfWeek<6:
                    # k contains every list [date,[times]] in empties
                    for k in empties:
                        # if the date in empties is the same as the date of the current event
                        # make sure that we only effect times on the day the even occurs
                        if k[0] == evDate:
                            l = 1
                            # iterate through the times of k and change them based on where the event falls
                            while l < len(k):
                                # FIRST if the event is the same as a time block, delete the block
                                if (j.sTime == k[l][0] and j.eTime == k[l][1]):
                                    k.remove(k[l])
                                    # drop l down by one as to not skip the next term
                                    l-=1
                                # THEN if the event lies entirely within a time block, cut the time block and provide new boundaries from the event
                                elif (j.sTime > k[l][0] and j.eTime < k[l][1]):
                                    temp = k[l][1]
                                    k[l][1]=j.sTime
                                    k.append([j.eTime,temp])
                                # THEN if the event shares a start time, but the end time lies within the block, shift start time to event's end time
                                elif (j.sTime == k[l][0] and j.eTime < k[l][1]):
                                    k[l][0]=j.eTime
                                # THEN if the event shares an end time, but the start time lies within the block, shift start time to event's end time
                                elif (j.sTime > k[l][0] and j.eTime == k[l][1]):
                                    k[l][1]=j.sTime
                                # THEN if the event's start time lies within a time block BUT the end does not, shift the end time of the current block to this event's start time
                                elif (j.sTime > k[l][0] and j.sTime < k[l][1]):
                                    k[l][1]=j.sTime
                                # THEN if the event's end time lies within a time block BUT the start does not, shift the start time of the current block to this event's end time
                                elif (j.eTime > k[l][0] and j.eTime < k[l][1]):
                                    k[l][0]=j.eTime
                                # THEN if the block lies within an event, delete the block
                                elif (j.sTime <= k[l][0] and j.eTime >= k[l][1]):
                                    k.remove(k[l])
                                    # drop l down by one as to not skip the next term
                                    l-=1
                                l+=1
    # return the finished list
    return empties

# temporary output to terminal for bug checking
def print_empties(empties):
    for i in empties:
        j = 1
        while j < len(i):
            print(str(i[0].month)+"/"+str(i[0].day)+"/"+str(i[0].year)+": "+str(i[j][0]-60000)+","+str(i[j][1]-60000))
            j+=1

                

# files is a list of strings that contins the names of the files that will be stored
files = ["ngarde2882@tamu.edu.ics"]
# schedules is a list that contains the schedule data of the files stored in files
schedules = list()
# events is a list that will contain all of the event data in a schedule before being copied to that schedule's eventlist
events = list()
# curr is a list that contains a LIFO queue of what part of the schedule is being saved
curr = list()

# loop for storing the data from the files into the schedule class
for i in files:
    # i should be the name of the file that we are opening, f is the open file in read mode
    f = open(i, 'r')
    if(f):
        print("File: "+i+" opened successfully!")
    for j in f:
        # j contains a whole line of f, k contains a list of the string before and the string after the ':'
        k = j.split(":")
        # In the case where the data contains any extra ':' characters, such as a link in the description or the location, k[1] still needs to contain that data. We only want the split to split the class type from its contents
        if (len(k)>2):
                l = 2
                while(l<len(k)):
                    k[1] += ":" + k[l]
                    l += 1
        # k drops the \n at the end of the second term
        k[1] = k[1][:-1]
        if k[0] == "BEGIN":
            # add begin to the LIFO queue
            curr.append(k[1])
        elif k[0] == "END":
            # pop one off of the LIFO queue, store in popped
            popped = curr.pop()
            if popped == "VEVENT":
                # after popping a VEVENT, create an event out of the data gathered and append it to the current event list (events)
                ev = event(evStart, evEnd, stamp, uid, created, description, lastMod, evLocation, seq, status, summary, transp)
                events.append(ev)
            elif popped == "VCALENDAR":
                # after popping VCALENDAR, the current schedule is complete. create a schedule class out of the data gathered
                calendar = schedule(proid, version, calScale, method, calName, timeZone, tzid, tzLocation, dlFrom, dlTo, dltzName, dlStart, dlRule, standardFrom, standardTo, standardtzName, standardStart, standardRule)
                l=0
                for m in events:
                    # for every event in the current stored events list, append them to the eventlist inside of the current schedule class
                    calendar.eventlist.append(events[l])
                    l+=1
                # append the completed schedule made to the list of schedules
                schedules.append(calendar)
        # the elifs below all take data from the k list and store it in variables based on what k[0] is. The variables are used to create the classes above whenever an event or a calendar is complete
        elif k[0] == "PRODID":
            proid = k[1]
        elif k[0] == "VERSION":
            version = k[1]
        elif k[0] == "CALSCALE":
            calScale = k[1]
        elif k[0] == "METHOD":
            method = k[1]
        elif k[0] == "X-WR-CALNAME":
            calName = k[1]
        elif k[0] == "X-WR-TIMEZONE":
            timeZone = k[1]
        elif k[0] == "TZID":
            tzid = k[1]
        elif k[0] == "X-LIC-LOCATION":
            tzLocation = k[1]
        elif k[0] == "TZOFFSETFROM":
            if curr[len(curr)-1] == "DAYLIGHT":
                dlFrom = k[1]
            elif curr[len(curr)-1] == "STANDARD":
                standardFrom = k[1]
        elif k[0] == "TZOFFSETTO":
            if curr[len(curr)-1] == "DAYLIGHT":
                dlTo = k[1]
            elif curr[len(curr)-1] == "STANDARD":
                standardTo = k[1]
        elif k[0] == "TZNAME":
            if curr[len(curr)-1] == "DAYLIGHT":
                dltzName = k[1]
            elif curr[len(curr)-1] == "STANDARD":
                standardtzName = k[1]
        elif k[0] == "DTSTART":
            if curr[len(curr)-1] == "DAYLIGHT":
                dlStart = k[1]
            elif curr[len(curr)-1] == "STANDARD":
                standardStart = k[1]
            elif curr[len(curr)-1] == "VEVENT":
                evStart = k[1]
        elif k[0] == "RRULE":
            if curr[len(curr)-1] == "DAYLIGHT":
                dlRule = k[1]
            elif curr[len(curr)-1] == "STANDARD":
                standardRule = k[1]
        elif k[0] == "DTEND":
            evEnd = k[1]
        elif k[0] == "DTSTAMP":
            stamp = k[1]
        elif k[0] == "UID":
            uid = k[1]
        elif k[0] == "CREATED":
            created = k[1]
        elif k[0] == "DESCRIPTION":
            description = k[1]
        elif k[0] == "LAST-MODIFIED":
            lastMod = k[1]
        elif k[0] == "LOCATION":
            evLocation = k[1]
        elif k[0] == "SEQUENCE":
            seq = k[1]
        elif k[0] == "STATUS":
            status = k[1]
        elif k[0] == "SUMMARY":
            summary = k[1]
        elif k[0] == "TRANSP":
            transp = k[1]
    # after leaving the j loop, the schedule has been made and added to the list of schedules, we should now close the file to be ready to open a new one
    if(f):
        f.close()

# Used for testing
last_day = meeting(3,21,2022,1,0)
a = apischedule()
GCal_pull(last_day, a)
a.print()
# empties = event_emptysearch(schedules,last_day)
# print_empties(empties)




# # save a reference to the original standard output
# original_stdout = sys.stdout
# num = 0
# # iterate through the files again, now makeing -out.ics files
# for i in files:
#     # create and open each file in write mode
#     f = open(i+"-out.ics", 'w')
#     # change the standard output to the file we created.
#     sys.stdout = f
#     # print the data from the schedule to the file using the print function created for schedules
#     print(schedules[num].print())
#     # reset the standard output to its original value
#     sys.stdout = original_stdout
#     print(i+"-out.ics created!")
#     num+=1
#     # close the file to be ready to open another one
#     f.close()
