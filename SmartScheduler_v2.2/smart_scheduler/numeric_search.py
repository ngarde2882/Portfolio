import datetime
from .models import Meeting, Attendee, Event, MeetingTime, Conflict
from .google import *

# import modules - algorithm
from googleapiclient.discovery import build
from users.models import Profile

def no_repeat(list1,list2): #remove repeats
    for i in list1:
        boolean=True
        for j in list2:
            # if i is found in j, don't append i
            if i==j:
                boolean=False
        if boolean:
            list2.append(i)
    return list2

# pull all apischedule information associated with meeting at once from database and delete
def database_pull(primary_key):
    # get all the meeting attendees registered to the meeting
    attendees = Attendee.objects.filter(meeting_name=primary_key).filter(rsvp_status='Accepted')
    arryschedules = []
    for attendee in attendees:
        # get all event objects for that attendee from the database
        # create an apischedule class, set the user to i
        schedule = ApiSchedule()
        schedule.user = attendee
        events = Event.objects.filter(meeting = primary_key).filter(event_owner=attendee.attendee_name)
        for event in events:
            # create an apievent with the pulled data, start,end,and attendees
            ev = ApiEvent(event.event_start, event.event_end, event.event_number_of_people)
            # append the event to the schedule
            schedule.apieventlist.append(ev)
        print(" ")
        # after events for a user have been added to schedule, append schedule to list of schedules
        arryschedules.append(schedule)
    print(" ")
    return arryschedules

# create_tt takes a start and end local time as well as a day delta and a time delay for UTC conversion to output a calendar
def create_tt(s, e, delta, delay, today):
    # make_tt creates the actual timetable for each day
    def make_tt(s, e, delay):
        # create strings and ints for the start, end, and delay to be modified
        s = str(s)
        e = str(e)
        str_s = s[0:2]+s[3:5]
        str_e = e[0:2]+e[3:5]
        str_d = delay[1:3] + delay[4:]
        int_s = int(str_s)
        int_e = int(str_e)
        int_d = int(str_d)
        # adjust the start and end times to UTC using the delay
        if delay[0]=='-':
            int_s += int_d
            int_e += int_d
        elif delay[0]=='+':
            int_s -= int_d
            int_e -= int_d
        tt = []
        # create the timetable
        while int_s < int_e:
            tt.append([int_s, [], []])
            if int_s % 100 == 45:
                int_s += 55
            else:
                int_s += 15
        return tt

    x_ = 0
    cal = []
    # loop today through deadline, including both edges
    # this creates the calendar array
    if delta == 0:
        cal = []
        day = []
        day.append(today)
        day.append(make_tt(s,e,delay))
        cal.append(day)
        return cal
    while x_ <= delta:
        # future = today + x days where x is 0-delta.days
        future = today + datetime.timedelta(days=x_)
        # day = [date, timetable] = [date, [[time, [name,[freeScore]], [summary]]]]
        day = []
        if future.isoweekday()<6:
            # include every weekday between today and deadline between user selected times
            day.append(future)
            day.append(make_tt(s, e, delay))
            cal.append(day)
        x_+=1
    return cal

# revert_tt sets the calendar back to the local timezone from UTC
def revert_tt(cal, delay):
    d = int(delay[1:3]+delay[4:])
    for i in cal:
        for j in i[1]:
            # adjust the start and end times from UTC to local using the delay
            if delay[0]=='-':
                j[0] -= d
            elif delay[0]=='+':
                j[0] += d
    return cal

def numeric_search(deadline, best_length, primary_key):
    # today in date format
    # today = datetime.date.today()
    meeting_start = str(Meeting.objects.filter(id=primary_key).first().meeting_start)
    print('MS:',meeting_start)
    today = datetime.date(int(meeting_start[:4]), int(meeting_start[5:7]), int(meeting_start[8:]))
    print('TD:',today)
    # dl is the deadline in date format
    dl = datetime.date(deadline.year,deadline.month,deadline.day)
    # delta gives the # of days between dl and today using delta.days
    delta = dl-today

    # pull all of the events from sqlite database and place them in arryschedules
    meeting_primary_key = Meeting.objects.filter(id=primary_key).first().id
    meeting_name = Meeting.objects.filter(id=primary_key).first().meeting_name
    arryschedules = Event.objects.filter(meeting=meeting_primary_key)
    # print("ARRYSCHEDULES:",arryschedules)
    # pull the profile of the meeting host
    meeting_author = Meeting.objects.filter(id=primary_key).first().author # find host
    profile_info = Profile.objects.filter(user=meeting_author).first() # create user profile object
    t_s = profile_info.start_time # profile start time
    t_e = profile_info.end_time # profile end time
    tz = profile_info.timezone # profile timezone
    # create a calendar based on user preferences
    cal = create_tt(t_s, t_e, delta.days, tz, today) # s=host start, e=host end, delta=delta (above), delay=user tz delay
    # print(cal)
    required = []
    optional = []
    atees = []
    atees = Attendee.objects.filter(meeting_name_id=primary_key, required=True)
    for at in atees:
        required.append(at.attendee_name)
    print('REQUIRED:',required)
    atees = Attendee.objects.filter(meeting_name_id=primary_key, required=False)
    for at in atees:
        optional.append(at.attendee_name)
    print('OPTIONAL:',optional)
    print('pk:',primary_key)
    o = 1
    if len(required) == 0 or len(optional) == 0:
        r = 1
    elif len(required) < len(optional):
        r = 3
    elif len(required) == len(optional):
        r = 5
    elif len(required) > len(optional):
        r = 7
    # sched holds each person's schedule in the array
    for event in arryschedules:
        # store the date, start time, and end time into variables
        # event is in format: 2022-03-22T15:55:00-05:00
        # pos 0-4 stores the year, 5-7 the month, 8-10 the day
        # print("DAT:",str(event.event_start)[11:13],str(event.event_start)[14:16])
        # print("DAT2:", event.event_start)
        
        ev_date = datetime.date(int(str(event.event_start)[0:4]), int(str(event.event_start)[5:7]), int(str(event.event_start)[8:10]))
        # pos 11-13 stores the hour, 14-16 the minute
        ev_stime = int(str(event.event_start)[11:13]+str(event.event_start)[14:16])
        delay = str(event.event_start)[19:22]+str(event.event_start)[23:]
        delay_int = int(delay[1:])
        ev_etime = int(str(event.event_end)[11:13]+str(event.event_end)[14:16])
        # adjust the start and end times to UTC using the delay
        if delay[0]=='-':
            ev_stime += delay_int
            ev_etime += delay_int
        elif delay[0]=='+':
            ev_stime -= delay_int
            ev_etime -= delay_int
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
                    if (ev_stime < time[0]+15 and ev_etime > time[0]):
                        # add name and that name's cost
                        if event.event_owner in required:
                            time[1].append([event.event_owner,r]) # r signifies the cost of a required attendee
                        else:
                            time[1].append([event.event_owner,o]) # o signifies the cost of an optional attendee
                        # add summary
                        time[2].append(event.event_number_of_people)
                # Once we found and finished looking through the correct day, break to move to the next event
                break
    #search
    # cal = [day] = [[date, [[time, [names], [summary]]]]]
    cal = revert_tt(cal, tz)
    print(cal)
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
                if len(day[1][left][1])>0:
                    for name in day[1][left][1]:
                        names.append(name[0])
                        # print(name[0], " has a conflict")
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
    # print("BEST\n",best)
    return best

# extracts the information from the best array and adds best times and conflicts to the database
def best_times(best, primary_key):
    print("Best")
    print(best)
    print()
    meeting_id = Meeting.objects.filter(id=primary_key).first()
    print("Starting the best times function")
    for i in best:
        meeting_time_hours_original = i[2]//100
        time_minutes=i[2]-(meeting_time_hours_original*100)
        str_time_minutes = str(time_minutes)
        if time_minutes == 0:
            str_time_minutes = "00"
        am_or_pm = "am"
        if meeting_time_hours_original >= 12:
            if meeting_time_hours_original == 12:
                am_or_pm = "pm"
            else:
                meeting_time_hours = meeting_time_hours_original - 12
                am_or_pm = "pm"

        meeting_time_object = MeetingTime(day=i[0].strftime("%d"), month=i[0].strftime("%B"), year=i[0].strftime("%Y"), weekday=i[0].strftime("%A"), time_hours=i[2]//100, time_minutes=str_time_minutes, am_or_pm=am_or_pm, date=i[0], start=i[2], meeting=meeting_id)
        meeting_time_object.save()
        print("SPACE")
        print(i[3])
        for j in i[3]:
            conflict = Conflict(name=j, meeting_time=meeting_time_object, meeting=meeting_id)
            conflict.save()