# imports
import smtplib
# importing MIMEText for HMTL functoinality later
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# the email confirmation function sends a conformation email once a meeting organizer has scheduled 
# a meeting and sent it out to the attending meeting members
# the parameters include:
# sender name - the name on the account that is sending out a meeting request
# sender email - the email on the account that is sending out a meeting request
# receiver email - the email of one of the attendees that is attending the meeting
# meeting name - the name of the confirmed meeting
# meeting time - the start time of the confirmed meeting
# meeting_link_location - a string that holds the meeting link or location
def email_confirmation(
    sender_name, 
    sender_email,
    receiver_email,
    meeting_name, 
    meeting_time,
    meeting_link_location
):
    # the sender email below is sent from our custom domain
    sender_email = "notifications@smart-scheduler.com"
    # the password is the API key used with mailgun
    password = "f53cb6d4a1b0e2e516a11eac43691364-162d1f80-536e6eb6"
    message = MIMEMultipart("alternative")
    # the subject line will be read as the meeting name with a confirmatin keyword added to the end
    message["Subject"] = meeting_name + " Confirmation"
    # the from is listed as the email on file for the sender
    message["From"] = sender_email
    # message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = f"""\
    A meeting has been added to your Google calendar by {sender_name}.
    You may choose to accept or decline this meeting.
    Here are the meeting details:
    Meeting Name: {meeting_name}
    Meeting Time: {meeting_time}
    Meeting Link/Location: {meeting_link_location}
    https://calendar.google.com
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    #part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    #message.attach(part2)

    # need to pass in correct meeting information here
    try:
        smtpObj = smtplib.SMTP('smtp.mailgun.org', 587)
        smtpObj.starttls()
        smtpObj.login(sender_email,password)          
        print("Login successful")
        smtpObj.sendmail(sender_email, receiver_email, message.as_string())   
        print("Email sent!")
        print(message)

    # exception condition for debugging and letting us know that the email failed to send
    except Exception:
        print("Error: unable to send email")  

# the email invite function sends an invite email to potential attendees once the meeting organizer has set the meeting parameters
# the parameters include:
# sender name - the name on the account that is sending out a meeting request
# sender email - the email on the account that is sending out a meeting request
# receiver email - the email of one of the attendees that is attending the meeting
# meeting name - the name of the confirmed meeting
# meeting description - the description attached to the meeting, gives a brief overview of what will happen
# meeting deadline - the date by which the meeting has to take place
# meeting duration hours - the duration of the meeting, hours component
# meeting duration minutes - the duration of the meeting, minutes component
# meeting_link_location - a string that holds the meeting link or location
def email_invite(
    sender_name, 
    sender_email,
    receiver_email,
    meeting_name, 
    meeting_description, 
    meeting_deadline, 
    meeting_duration_hours, 
    meeting_duration_minutes, 
    meeting_link_location
):
    # the sender email is our custom domain email
    sender_email = "notifications@smart-scheduler.com"
    # API password - tighten security later
    password = "f53cb6d4a1b0e2e516a11eac43691364-162d1f80-536e6eb6"
    message = MIMEMultipart("alternative")
    # subject line is simply the meeting name
    message["Subject"] = meeting_name
    # the from links to the sender email address
    message["From"] = sender_email
    # message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    # this message below includes a link the the RSVP page for the scheduling application
    text = f"""\
    You have been invited to a meeting hosted by {sender_name}.
    Here are the meeting details:
    Meeting Name: {meeting_name}
    Meeting Description: {meeting_description}
    Meeting Deadline: {meeting_deadline}
    Meeting Duration: {meeting_duration_hours} hours and {meeting_duration_minutes} minutes
    Meeting Link/Location: {meeting_link_location}

    To RSVP for this meeting, go to https://user-form-2022.herokuapp.com/
    """
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    #part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    #message.attach(part2)

    # need to pass in correct meeting information here
    try:
        smtpObj = smtplib.SMTP('smtp.mailgun.org', 587)
        smtpObj.starttls()
        smtpObj.login(sender_email,password)          
        print("Login successful")
        smtpObj.sendmail(sender_email, receiver_email, message.as_string())   
        print("Email sent!")
        print(message)
    
    # exception handler in case the email fails to send
    except Exception:
        print("Error: unable to send email")  
