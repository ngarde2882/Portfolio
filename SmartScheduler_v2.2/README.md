# SmartSchedulerVer2
Django implementation of Smart Scheduler

How to Use:

Do away with the tedious back-and-forth typically associated with scheduling meetings.

Visit: https://django-smart-scheduler.herokuapp.com

Get started by registering for an account, then log in.
![alt text](https://github.com/collinbennett1999/SmartSchedulerVer2/blob/main/smart_scheduler/static/smart_scheduler/media/register.jpg)


Create some contacts under the "Contacts" tab. You'll need them to create meetings.
![alt text](https://github.com/collinbennett1999/SmartSchedulerVer2/blob/main/smart_scheduler/static/smart_scheduler/media/create_contact.jpg)

Add your contacts to a meeting.
![alt text](https://github.com/collinbennett1999/SmartSchedulerVer2/blob/main/smart_scheduler/static/smart_scheduler/media/add_contacts.jpg)

Enter your meeting details and press "Create Meeting".
![alt text](https://github.com/collinbennett1999/SmartSchedulerVer2/blob/main/smart_scheduler/static/smart_scheduler/media/create_meeting.jpg)

Give Google permission to access your calendar event.
![alt text](https://github.com/collinbennett1999/SmartSchedulerVer2/blob/main/smart_scheduler/static/smart_scheduler/media/api.jpg)

Email invites will be sent to the participants. They can decide if they want to accept or decline.
![alt text](https://github.com/collinbennett1999/SmartSchedulerVer2/blob/main/smart_scheduler/static/smart_scheduler/media/email.jpg)

When you are ready to schedule a time, choose one that best works for you.
![alt text](https://github.com/collinbennett1999/SmartSchedulerVer2/blob/main/smart_scheduler/static/smart_scheduler/media/schedule.jpg)

The event will be sent to all calendars.
![alt text](https://github.com/collinbennett1999/SmartSchedulerVer2/blob/main/smart_scheduler/static/smart_scheduler/media/event.jpg)



Email invites will be sent to the participants. They can decide if they want to accept or decline.


Weekly log of what has been done by each team member:

August 21st - August 27th

Collin:
- Made some changes to the Django application to get it ready for an initial semester presentation with Dr. Reddy. 

August 28th - September 3rd

Collin:
Removed Outlook code from the project. Got Nick up to speed on Django and how the app functions. 

September 4th - September 10th

Collin:
- Fixed broken links and HTML render errors. Settled on a new repository for hosting the Capstone project. 

September 11th - September 17th

Collin:
- Fixed meeting redirect upon creation
- Fixed meeting duration rendering error
- Attendees are now deleted from selection list after being selected
- Fixed the meeing slider
- Added a database table for conflicts associated with potential times

September 18th - September 24th

Collin:
- Changed GCal_Pull to be function based, rather than coded straight into the rendering view
- Fixed a duration formatting error
- Removed unnecessary code
- Integrated time conflict functionality
- Added additional fields to profile

September 25th - October 1st

Collin:
- Database hosted on AWS
- Attempting to host Django app on AWS as well
- Database now accounts for timezones
- Email functionality integrated into the project

October 2nd - October 8th

Collin:
- Emails styled (simple HTML styling)
- Attempts to get hosting working on AWS are lagrely unsuccessful


October 9th - October 15th

Collin:
- Implemented custom start and end times to the user profile
- Added additional checks on some of the website forms


October 16th - October 22nd

Collin:
- Switch over to Heroku for website hosting... successful
- Encountered and tackling problem of API calls not working on hosted machine

October 23rd - October 29th

Collin:
- Added profile pictures to AWS buckets. This solved loading errors associated with static folder
- Added functionality of start and end times for each meeting. 
- This helps users set an earliest date to set a meeting and a latest date to set a meeting. 

October 30th - November 5th

Collin:
- Helped Nick get the APIs functioning on the hosted site (unsuccessful so far)
- Various bugfixes
- Work on the validation of the website forms (complete)

November 6th - November 12th

Collin:
- Various bigfixes
- Helped Nick get the APIs functioning on the hosted site (successful)
- Overhauled the colors of the site. It no longer looks like it was designed by a colorblind person


November 13th - November 19th

Collin:
- Finishing final functionalities for the final presentation
- Took website off of debugging mode
- Work on the report
- Ensuring that certain validation steps are working properly

November 20th - November 27th

Collin: 
- Working on minor stylistic improvements and changes
- Working on slight code optimizations
- Preparations for demo
- Discussion with Dr. Reddy about contunued support and transfer of ownership




