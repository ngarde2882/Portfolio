# import module
import streamlit as st
import datetime
from datetime import datetime
from datetime import date
from datetime import time

st.title('Automated Smart Scheduler')
st.header('Schedule an Event')
my_date = date(2021, 3, 2)
d = st.date_input("Enter your appointment date.", my_date)
# st.write('Set date is:', d)

my_time = time(8,45)
t = st.time_input('Enter your appointment time.', my_time)
# st.write('Set time is', t)

attendees = st.text_input("Enter attendee email addresses.", "Type Here ...")

if st.button('Confirm and Schedule Appointment'):
    st.write('Appointment confirmed for ', d, 'at', t)
