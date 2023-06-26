# import module
import streamlit as st
import datetime
from datetime import datetime
from datetime import date
from datetime import time

def app():
    st.title('Schedule an Appointment')
    st.header('Enter a Time Window')
    my_date_begin = date(2021, 3, 2)
    my_date_end = date(2021, 3, 2)
    my_time_begin = time(8,45)
    my_time_end = time(8,45)
    db = st.date_input("Enter your beginning date.", my_date_begin)
    tb = st.time_input('Enter your beginning time.', my_time_begin)
    de = st.date_input("Enter your ending date.", my_date_end)
    te = st.time_input('Enter your ending time.', my_time_end)
    # st.write('Set date is:', d)
    
    # st.write('Set time is', t)

    attendees = st.text_input("Enter attendee email addresses.", "Type Here ...")

    if st.button('Confirm and Schedule Appointment'):
        st.write('Appointment confirmed for ', d, 'at', t)
