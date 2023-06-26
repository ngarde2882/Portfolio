import os
import smtplib
import itertools
from email.message import EmailMessage
from .configure import *

def send_invitation(
    meeting_name_id_list,
    email_list,
    attendee_pk_list,
    meeting_name,
    meeting_description,
    meeting_deadline,
    duration_hours,
    duration_minutes,
    meeting_link_location
):
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        for (email, attendee, meeting_name_id) in zip(email_list, attendee_pk_list, meeting_name_id_list):
            url_accept = "https://django-smart-scheduler.herokuapp.com/accept_meeting/" + str(meeting_name_id) + "/" + str(attendee) + "/accept"
            url_decline = "https://django-smart-scheduler.herokuapp.com/decline_meeting/" + str(meeting_name_id) + "/" + str(attendee) + "/decline"
            msg = EmailMessage()
            msg['Subject'] = meeting_name + ' Invitation'
            msg['From'] = email_address
            msg['To'] = email
            string = 'You have been invited to a meeting. Here are the details: \n\nMeeting name: ' 
            string += meeting_name 
            if meeting_description != "":
                string += '\nDescription: ' 
                string += meeting_description 
            string += '\nDeadline: ' 
            string += meeting_deadline.strftime("%B %d, %Y") 
            string += '\nDuration: ' 
            if duration_hours == 0:
                string += str(duration_minutes) 
                string += ' minutes'
            elif duration_hours == 1:
                string += str(duration_hours)
                string += ' hour and ' 
                string += str(duration_minutes) 
                string += ' minutes'
            elif duration_hours > 1:
                string += str(duration_hours)
                string += ' hours and ' 
                string += str(duration_minutes) 
                string += ' minutes'
            if meeting_link_location != "":
                string += '\nLink/Location: ' 
                string += meeting_link_location 
            string += '\n\nTo RSVP, click the following link:\n' 
            string += url_accept 
            string += '\n\nTo decline, click the following link:\n' 
            string += url_decline
            msg.set_content(string)
            smtp.login(email_address, password)
            print("Sending email to " + str(email))
            smtp.send_message(msg)

def meeting_confirmation(
    date,
    meeting_creator_email,
    meeting_name,
    meeting_description,
    meeting_time,
    duration_hours,
    duration_minutes,
    meeting_link_location
):
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        for email in meeting_creator_email:
            smtp.login(email_address, password)
            subject = meeting_name + ' Confirmation'
            body = 'You have been confirmed for the meeting. Here are the details: \n\nMeeting name: ' 
            body += meeting_name 
            if meeting_description != "":
                body += '\nDescription: ' + meeting_description
            body += '\nTime: ' 
            body += str(meeting_time)
            body += '\nDate: '
            body += date.strftime("%B %d, %Y") 
            body += '\nDuration: '  
            if duration_hours == 0:
                body += str(duration_minutes) 
                body += ' minutes'
            elif duration_hours == 1:
                body += str(duration_hours)
                body += ' hour and ' 
                body += str(duration_minutes) 
                body += ' minutes'
            elif duration_hours > 1:
                body += str(duration_hours)
                body += ' hours and ' 
                body += str(duration_minutes) 
                body += ' minutes'
            if meeting_link_location != "":
                body += '\nLink/Location: ' 
                body += meeting_link_location 
            body += '\n\nView this event in your Google calendar:\n\nhttps://calendar.google.com/calendar/u/0/r'

            msg = f'Subject: {subject}\n\n{body}'
            print("Sending email to " + str(email))
            smtp.sendmail(email_address, email, msg)