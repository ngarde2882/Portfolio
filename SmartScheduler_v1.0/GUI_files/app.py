import streamlit as st
from multipage import MultiPage
import homepage, schedule_an_appointment, scheduled_appointments, login, sign_up

# Create an instance of the application usign the constructor
app = MultiPage()

# Title of the main page
# st.title("Automated Scheduler")

# Add all application pages here
# app.add_page("Homepage", homepage.app)
app.add_page("Login", login.app)
app.add_page("Sign Up", sign_up.app)
app.add_page("Schedule an Appointment", schedule_an_appointment.app)
app.add_page("Scheduled Appointments", scheduled_appointments.app)

app.run()
