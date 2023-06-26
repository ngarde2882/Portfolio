# Smart-Scheduler

Collin Bennett
Nicholas Garde

Sponsor: Narasimha Annapareddy
TA: Swarnabha Roy

Frontend How-To:
Users of the Smart Scheduler may sign up with a first name, last name, email, and password. 
Users may schedule an appointment. This is done by inputting the following parameters:

- Meeting Name
- Meeting Description
- Meeting Deadline
- Meeting Duration (Hours)
- Meeting Duration (Minutes)
- Meeting Attendees 
- Meeting Link/Location (Optional Parameter)
- Number of Rescheduling Suggestions

Once these fields are entered and the "Generate Meeting and Invite Attendees" button is pressed,
emails will be sent to the potential attendees linking them to a calendar sharing page.
Here, attendees will give consent for their calendars to be analyzed. Once all attendees have done this,
the meeting organizer will schedule the meeting, and all the attendees who have shared their calendar data
will be included in the algorithm. The best time is returned, and the event is added to all calendars. 
Attendees will be notified via email about the scheduled meeting. Currently, this is only compatible with 
Google Calendars, but implementation with Outlook calendars will be added in the future. 

Meeting creators with registered accounts also have the option to view the invitation status of potential meeting attendees using the View Pending Members Screen. This screen lists every pending meetings, the attendees of these meetings, and a status next to each person, Attending, Not Attending, and Pending. Under these names is a button that allows the meeting organizer to schedule a meeting. This button spits out the three best meeting times. The selected time will push a meeting featuring these details to user's Google Calendar, and they can decide ultimately if they want to add this to their calendars. These attendees will alos be sent a confirmation email with the finalized meeting details. 

api_file.py classes and functions:
- classes
- apievent(start, end, summary)
    Stores start and end times of an event as datetimes
    Stores int number of attendees of an event in summary
- apischedule()
    Stores a string user which holds the contact email of the user the schedule is referencing
    Stores a list of apievents (defined above)
    Stores and int cost of rescheduling from this user's schedule, incremented every time a meeting is found while sorting in numeric_search
- meeting(month, day, year, hour, minute, name)
    Stores int month,day,year,hour,minute for the date of the last possible meeting day, and length in time of the proposed meeting
    Stores string name that holds the name of the proposed meeting
- functions
- void GCal_pull(deadline, user)
    deadline is a meeting class type
    user is a string holding the contact email of the user we are accessing
    GCal_Pull is used to send a user to an OAuth screen to allow us access to their Google Calendar, and then pulling every event that user has between the time it was run and the deadline passed. These events are then all uploaded to the database using firebase_push under the contact email of the user that we pulled from. The function concludes by deleting the token granting us access to the user's calendar, and returns nothing
- GCal_push(date,start,length,summary,description,location,attendees)
    date holds a datetime of the meeting to be pushed
    start holds an integer value HHMM for the time of the meeting
    length holds an integer value for the length of the meeting divided by 15
    summary holds a string for the title of the meeting
    description holds a string for the description
    location holds a string for the place (or link to the virtual place) the meeting will be held
    attendees holds a list of strings with the other members invited to the meeting
    GCal_push places a meeting onto the hosts calendar with the previously stated data, which also places the event on all of the attendees' calendars as well without duplicating the event
- void firebase_push(schedule, email, meeting)
    schedule is an apischedule with a user's eventlist
    email is a string holding the user's contact email
    meeting is a string holding the name of the event trying to be scheduled
    firebase_push is used to upload data onto the database, first under a meeting name, then under the user's contact email to keep relevent information together
- list<apischedule> firebase_pull(meeting)
    meeting is a string holding the name of the event trying to be scheduled
    firebase_pull is used to pull all events from every user associated with a meeting from the database (and delete the information from the database) and return a list of apischedules that contains every user's schedule
- list<datetime,list<int,int>,int,list<list<string,int>>> numeric_search(deadline)
    deadline is a meeting class type
    numeric_search first initializes a calendar that holds every day between the current day and the deadline day (inclusive). Each day contains a timetable from 8am-6pm, and 2 empty lists at every 15 minute increment to be populated with names and attendees. The function then sorts all of the user data found on the database onto the calendar after doing a firebase_pull on the proposed meeting name. after sorting every user meeting onto the calendar, the function then searches through it, scoring every sequential chunk of times the length of the proposed meeting and increasing the score for every conflict found. While doing this, every time a chunk is found to be a lower score than those saved as best, it pops the highest score found on best and gets stored as a replacement. The function returns the array of best meeting times in the format: best = [[date, [scoreNumConflicts, scoreNumParticipants], time, [names]]]
- no_repeat(list1,list2)
    list1 and list2 are lists that should contain strings
    no_repeat adds all of the content of list1 onto list2 without adding any repeated values
- ML_Push(best,victor,note)
    best holds the best array from numeric_search
    victor holds the part of best that was decided to hold the meeting
    note holds an optional user note for why they chose that meeting
    ML_Push is used to take all relevent data from a search and store it on firebase so in the future we can hopefully use it to train ML to make the descision for the user.
- pendingStatus(meeting,members)
    meeting holds a string for the name of the meeting in question
    members holds an array of strings for the users invited to the meeting
    pendingStatus is used to check what users have and have not yet added their data to firebase to display to the meeting host in an effort to inform them when an override is necessary to start searching schedules before all users have uploaded their data
