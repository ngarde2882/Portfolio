# import module
import streamlit as st
import datetime
from datetime import datetime
from datetime import date
from datetime import time

def app():
    st.title('Automated Smart Scheduler')
    st.header('Scheduled Appointments')

    my_date = date(2022, 3, 2)
    my_time = time(8,45)
    st.write('Appointment scheduled for ', my_date, 'at', my_time)
    my_date = date(2022, 3, 10)
    my_time = time(9,00)
    st.write('Appointment scheduled for ', my_date, 'at', my_time)
    my_date = date(2022, 3, 20)
    my_time = time(10,45)
    st.write('Appointment scheduled for ', my_date, 'at', my_time)
    my_date = date(2022, 4, 2)
    my_time = time(12,00)
    st.write('Appointment scheduled for ', my_date, 'at', my_time)
    my_date = date(2022, 4, 28)
    my_time = time(15,00)
    st.write('Appointment scheduled for ', my_date, 'at', my_time)