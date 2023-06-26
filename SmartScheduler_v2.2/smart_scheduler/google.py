from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .models import Meeting, PendingAttendee, Attendee, Event, Contact
from .views import *

from users.models import Profile

from requests_oauthlib import OAuth2Session


# class that hold the last day a meeting can be held + length of meeting in hours and minutes
class MeetingFormat: # Last possible day the meeting can be held + length of meeting in hours + minutes
    def __init__(self, month, day, year, hour, minutes, name):
        self.month = month
        self.day = day
        self.year = year
        self.hour = hour
        self.minutes = minutes
        self.name = name

# class that holds the user email, list of events, and the cost of the person
class ApiSchedule:
    def __init__(self):
        self.user = "" # email of the user
        self.apieventlist = list() # list of events the user has
        self.cost = 0

    def print(self):
        for i in self.apieventlist: # print all values of an apischedule to terminal
            print(self.user,":", i.start, i.end, i.summary)

# class that hold the information for events
class ApiEvent:
    def __init__(self, start, end, summary): # summary now holds num of attendees
        self.start = start # start time of an event pulled by the gcal API
        self.end = end # end time of an event pulled by the gcal API
        self.summary = summary # num attendees in the event

# TODO: we should be able to delete APIEvents and APISchedules as we are now sending them directly to the db
# this may also cause cascading errors in numeric search

def generate_oauth(google):
    authorization_base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    authorization_url, state = google.authorization_url(
        # authorization_base_url
    # offline for refresh token
    # force to always make user click authorize
    access_type="offline",
    prompt="select_account")
    # print('Please go here and authorize:', authorization_url)
    print("Returning authorization url:", authorization_url)
    return authorization_url

def generate_token(google, author, url):
    # https://django-smart-scheduler.herokuapp.com/rsvp_accept?state=X3DDm4WyPnK0t1es90hHatBI8oFym3&code=4/0AfgeXvt_m3XQrz1eLUNOL_Wk15BBdfB-_DfGKtDjReCRllJ9HdMDCdZyhNchsGUhG1cd6A&scope=https://www.googleapis.com/auth/calendar.readonly
    # token_url = "https://www.googleapis.com/oauth2/v4/token"
    token_url = 'https://oauth2.googleapis.com/token'
    client_secret = "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"
    # try:
    code = url.split('&code=')[1].split('&scope=')[0]
    if not '/' in code:
        print('did not find /')
        if '%2F' in code:
            print('found % 2 F')
            code = code.replace('%2F','/')
    print('code:',code)
    # google.fetch_token(token_url, client_secret=client_secret, code=code)
    userToken = google.fetch_token(code=code)
    credentials = google.credentials
    # userToken = userToken['access_token']
    print('userToken:',userToken)
    temp = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'id_token':credentials.id_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes,
        'expiry':datetime.datetime.strftime(credentials.expiry,'%Y-%m-%dT%H:%M:%S')
    }
    # creds = google.credentials
    # print('creds', creds)
    # except:
    #     code = None
    #     userToken = None
    #     print('token miss')
    Profile.objects.filter(user=author).update(token=temp)

def generate_contact_token(google, author, url, id):
    # https://django-smart-scheduler.herokuapp.com/rsvp_accept?state=X3DDm4WyPnK0t1es90hHatBI8oFym3&code=4/0AfgeXvt_m3XQrz1eLUNOL_Wk15BBdfB-_DfGKtDjReCRllJ9HdMDCdZyhNchsGUhG1cd6A&scope=https://www.googleapis.com/auth/calendar.readonly
    # token_url = "https://www.googleapis.com/oauth2/v4/token"
    token_url = 'https://oauth2.googleapis.com/token'
    client_secret = "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"
    # try:
    code = url.split('&code=')[1].split('&scope=')[0]
    if not '/' in code:
        print('did not find /')
        if '%2F' in code:
            print('found % 2 F')
            code = code.replace('%2F','/')
    print('code:',code)
    # google.fetch_token(token_url, client_secret=client_secret, code=code)
    userToken = google.fetch_token(code=code)
    credentials = google.credentials
    # userToken = userToken['access_token']
    print('userToken:',userToken)
    temp = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'id_token':credentials.id_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes,
        'expiry':datetime.datetime.strftime(credentials.expiry,'%Y-%m-%dT%H:%M:%S')
    }
    # creds = google.credentials
    # print('creds', creds)
    # except:
    #     code = None
    #     userToken = None
    #     print('token miss')
    Contact.objects.filter(pk=id).update(token=temp)

# Function for pulling events from a user's calendar, called when a meeting is created and when a user accepts an invite
def GCal_Pull(deadline, request, pk, author, event_owner, meeting_info, bol):
    # If modifying these scopes, delete the file token.json. -> now sent to db, tightened the scopes
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    #Shows basic usage of the Google Calendar API.
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time. This was changed to be stored on the database 
    '''
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    '''
    if bol:
        # If there are no (valid) credentials available, let the user log in.
        # rememberBool holds a boolean of whether a user has allowed us to save their token
        rememberBool = Profile.objects.filter(user=author).first().remember_me
        # userToken holds the token that is stored in th database for a user (even if there is none)
        userToken = Profile.objects.filter(user=author).first().token
    else:
        rememberBool = Contact.objects.filter(pk=request.session.get('id',None)).first().remember_me
        userToken = Contact.objects.filter(pk=request.session.get('id',None)).first().token
    print('userToken in Pull:',userToken)
    print('type of token:', type(userToken))
    # name = str(Profile.objects.filter(user=author).first().user)
    # print("Token Type:",type(userToken))
    # print(userToken)
    if userToken:
        # data holds the information in the userToken as a json object
        userToken = json.dumps(userToken)
        data = json.loads(userToken)
        # data = json.dumps(userToken)
        # print("Data Type:",type(data))
        # creds holds the credentials created by the userToken and the given scopes done by Google API
        creds = Credentials.from_authorized_user_info(data, SCOPES)

    if not creds or not creds.valid:
        # if creds are not valid, they are recreated using our app's credentials file
        if creds and creds.expiry and creds.refresh_token:
            today = datetime.datetime.now()
            if today>creds.expiry:
                print('request token refresh')
                creds.refresh(Request())
                temp = {
                    'token': creds.token,
                    'refresh_token': creds.refresh_token,
                    'id_token':creds.id_token,
                    'token_uri': creds.token_uri,
                    'client_id': creds.client_id,
                    'client_secret': creds.client_secret,
                    'scopes': creds.scopes,
                    'expiry':datetime.datetime.strftime(creds.expiry,'%Y-%m-%dT%H:%M:%S')
                }
                if bol:
                    Profile.objects.filter(user=author).update(token=temp)
                else:
                    Contact.objects.filter(pk=request.session.get('id',None)).update(token=temp)
        else:
            ''' local host stuff
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            '''
            # delete user's token in db
            userToken = None
            if bol:
                Profile.objects.filter(user=author).update(token=userToken)
            else:
                Contact.objects.filter(pk=request.session.get('id',None)).update(token=userToken)
            return None
            # in views reroute user through generating a token
            # raise TypeError('Cannot find Credentials')
        '''
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
        '''
        '''
        # Save the credentials for the next run if a user has authorized
        if rememberBool:
            userToken = creds.to_json()
            Profile.objects.filter(user=author).update(token=userToken)
        '''
    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        today = datetime.date.today()
        # dl is the deadline in date format
        dl = datetime.date(deadline.year,deadline.month,deadline.day)
        # delta gives the # of days between dl and today using delta.days
        delta = dl-today
        # later holds the last possible day to schedule a meeting in datetime format
        later = (datetime.datetime(deadline.year,deadline.month,deadline.day,23,59)).isoformat() + 'Z'
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
            pass
        # create an apischedule for storing a user's events
        sched = ApiSchedule()
        # tz = False
        # Prints the start and name of the events from today until the deadline
        for event in events:
            # start holds a given event's start time
            start = event['start'].get('dateTime', event['start'].get('date'))
            # if not tz:
            #     tz = True
            # print('tz:',event['start'].get('timeZone'))
                # tz: America/Chicago
            # print('dt:',event['start'].get('dateTime'))
                # dt: 2022-09-22T11:10:00-05:00
                
            # end holds a given event's end time
            end = event['end'].get('dateTime', event['end'].get('date'))

            # tz = event['start'].get('timeZone')
            try:
                # if an event holds values for attendees, att holds them
                att=len(event['attendees'])
            except:
                # if there is no attendees object in the event, set att to 1 (the user)
                att=1
            if(len(str(start))<15):
                # if len(start)<15 then the event is an all-day event and needs to be ignored
                continue
            # push the created event object to the database
            event_object = Event(event_owner=event_owner, event_start=start, event_end=end, event_number_of_people=att, meeting_id=pk)
            event_object.save()
            # create an apievent with start,end,att
            ev = ApiEvent(start, end, att) # att was event['summary'] when we were holding event titles and not attendees
            # add the event to the apischedule's event list
            sched.apieventlist.append(ev)
            #event_database = Attendee(event_owner=meeting_author, email_address=pending_attendee.email_address, rsvp_status='Pending', meeting_name_id=pk)
        # once the full schedule is made, push it to firebase
        # delete the user token (need to ask permission before using user data again)
        '''
        os.remove('token.json')
        '''
        # do a final check for if a user has authorized us to hold their token, if not but we have one saved, set to None
        if not rememberBool:
            userToken = None
            if bol:
                Profile.objects.filter(user=author).update(token=userToken)
            else:
                Contact.objects.filter(pk=request.session.get('id',None)).update(token=userToken)

    except HttpError as error:
        print('An error occurred: %s' % error)

    """
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    #Shows basic usage of the Google Calendar API.
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
        sched = ApiSchedule()
        # Prints the start and name of the events from today until the deadline
        for event in events:
            # start holds a given event's start time
            start = event['start'].get('dateTime', event['start'].get('date'))
            # end holds a given event's end time
            end = event['end'].get('dateTime', event['end'].get('date'))
            print("Start: ", start, " End: ", end)
            try:
                # if an event holds values for attendees, att holds them
                att=len(event['attendees'])
            except:
                # if there is no attendees object in the event, set att to 1 (the user)
                att=1
            event_object = Event(event_owner=event_owner, event_start=start, event_end=end, event_number_of_people=att, meeting_id=pk)
            event_object.save()
            # create an apievent with start,end,att
            ev = ApiEvent(start, end, att) # att was event['summary'] when we were holding event titles and not attendees
            # add the event to the apischedule's event list
            sched.apieventlist.append(ev)
            #event_database = Attendee(event_owner=meeting_author, email_address=pending_attendee.email_address, rsvp_status='Pending', meeting_name_id=pk)
        # once the full schedule is made, push it to firebase
        # delete the user token (need to ask permission before using user data again)
        os.remove('token.json')
    except HttpError as error:
        print('An error occurred: %s' % error)
    """


# Push a meeting onto the meeting creator's Google Calendar with the other users as attendees (which creates invites on their end)
def GCal_push(date, start, length, summary, description, location, attendee_emails, meeting_creator_email):
  print("Initialing GCal_push inside the function")
  print("Attendee emails: ", attendee_emails)
  # set the permission scope
  SCOPES = ['https://www.googleapis.com/auth/calendar.events']
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time. This was changed to be stored on the database
  # find the author by comparing the summary and description to the meetings stored in the database
  author = Meeting.objects.filter(meeting_name=summary,meeting_description=description).first().author
  # boolean for if a user is allowing us to hold onto their token
  rememberBool = Profile.objects.filter(user=author).first().remember_me
  # token data pulled from the database
  userToken = Profile.objects.filter(user=author).first().token
  # print("Token Type:",type(userToken))
  # print(userToken)
  if userToken:
      # data holds the information in the userToken as a json object
      userToken = json.dumps(userToken)
      data = json.loads(userToken)
      # print("Data Type:",type(data))
      # creds holds the credentials created by the userToken and the given scopes done by Google API
      creds = Credentials.from_authorized_user_info(data, SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
      # if creds are not valid, they are recreated using our app's credentials file
      if creds and creds.expiry and creds.refresh_token:
          today = datetime.datetime.now()
          if today>creds.expiry:
              print('request token refresh')
              creds.refresh(Request())
              temp = {
                  'token': creds.token,
                  'refresh_token': creds.refresh_token,
                  'id_token':creds.id_token,
                  'token_uri': creds.token_uri,
                  'client_id': creds.client_id,
                  'client_secret': creds.client_secret,
                  'scopes': creds.scopes,
                  'expiry':datetime.datetime.strftime(creds.expiry,'%Y-%m-%dT%H:%M:%S')
              }
          Profile.objects.filter(user=author).update(token=temp)
      else:
        '''
          flow = InstalledAppFlow.from_client_secrets_file(
              'credentials.json', SCOPES)
          creds = flow.run_local_server(port=0)
      # Save the credentials for the next run
      '''
        # delete user's token in db
        userToken = None
        if bol:
            Profile.objects.filter(user=author).update(token=userToken)
        else:
            Contact.objects.filter(pk=request.session.get('id',None)).update(token=userToken)
        return None
        # in views reroute user through generating a token
        # raise TypeError('Cannot find Credentials')
      '''
      with open('token.json', 'w') as token:
          token.write(creds.to_json())
      '''
      '''
      # Save the credentials for the next run if a user has authorized
      if rememberBool:
          userToken = creds.to_json()
          Profile.objects.filter(user=author).update(token=userToken)
      '''
  try:
      service = build('calendar', 'v3', credentials=creds)
      # Call the Calendar API
    #   print("LOCAL START: ",start)
      # find the user's timezone
      delta = Profile.objects.filter(user=author).first().timezone
      # pull out the integer number for the time HHMM
      delta_int = int(delta[1:3]+delta[4:])
      # convert the start time into UTC
      if delta[0]=='-':
            start += delta_int
      elif delta[0]=='+':
            start -= delta_int
    #   print("UTC START: ",start)
      # set the event date as a datetime to hold all day and time values
      if start//100 < 24:
        ev_date = datetime.datetime(date.year, date.month, date.day, start//100, start-start//100*100, 0)
      else:
        ev_date = datetime.datetime(date.year, date.month, date.day+1, start//100-24, start-start//100*100, 0)
      # event start holds ev_date in iso format
      e_start = ev_date.isoformat()
      # event end holds the same datetime in iso format, but adds the length of the meeting
      e_end = (ev_date + datetime.timedelta(minutes=length*15)).isoformat()

      # arry of attendees
      print("Made it to the attendees array.")
      att = []
      for x in attendee_emails:
          # place all of the attendees into att in json (or dictionary) format
          att.append({'email':x})
          print("PING")
      for x in att:
        print("Pushing meeting to ", str(att))
      # the event to be pushed onto google calendar
      event_result = service.events().insert(calendarId='primary', sendUpdates='all',
          # the contents of the event, in json format
          body={
              "summary": summary,
              'location': location,
              "description": description,
              "start": {"dateTime": e_start, "timeZone":'UTC',},
              "end": {"dateTime": e_end, "timeZone":'UTC',},
              'attendees': att,
          }
      ).execute()

      # delete the token allowing us to access a user's google calendar if requested
      '''
      os.remove('token.json')
      '''
      # do a final check for if a user has authorized us to hold their token, if not but we have one saved, set to None
      if not rememberBool:
        userToken = None
        Profile.objects.filter(user=author).update(token=userToken)
  # Throw error
  except HttpError as error:
      print('An error occurred: %s' % error)
