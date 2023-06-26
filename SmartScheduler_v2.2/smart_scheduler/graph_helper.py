import requests
from .models import Meeting, Contact, Attendee, PendingAttendee, Event, MeetingTime, Conflict, MeetingImmediate
import json

graph_url = 'https://graph.microsoft.com/v1.0'

def get_user(token):
    # Send GET to /me
    user = requests.get('{0}/me'.format(graph_url),
    headers={'Authorization': 'Bearer {0}'.format(token)},
    params={
'$select':'displayName,mail,mailboxSettings,userPrincipalName'})
    return user.json()

def get_calendar_events(token):
    # Send GET to /
    events = requests.get('{0}/me/events'.format(graph_url),
    headers={'Authorization': 'Bearer {0}'.format(token)},
    params={
'$select':'organizer,attendees,start,end'})
    slug = events.json()
    json_status = slug['value']
    print()
    print('JSON Status: ')
    meeting_id = MeetingImmediate.objects.first().meeting_id
    print("Meeting id:")
    print(meeting_id)
    instance = MeetingImmediate.objects.first()
    instance.delete()
    meeting = Meeting.objects.filter(id=meeting_id).first()
    for i in json_status:
        #print(i['@odata.etag'])
        #print(i['id'])
        start = i['start']
        start_time = start['dateTime']
        end = i['end']
        end_time = end['dateTime']
        attendee_count = len(i['attendees']) + 1
        organizer = i['organizer']
        email_address = organizer['emailAddress']
        name = email_address['name']
        print()
        print(name)
        print(start_time)
        print(end_time)
        print(attendee_count)
        print(meeting)
        print()
        event = Event(event_owner=name, event_start=start_time, event_end=end_time, event_number_of_people=attendee_count, meeting=meeting)
        event.save()



    return events.json()
"""
def post_calendar_event(token):
    # Send GET to /me
    user = requests.post('{0}/me/calendar/events'.format(graph_url),
    headers={'Authorization': 'Bearer {0}'.format(token)},
    params={
'$select':'displayName,mail,mailboxSettings,userPrincipalName'})
    return user.json()
"""