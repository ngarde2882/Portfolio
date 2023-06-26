# import module
import streamlit as st
import pandas as pd
import datetime
from datetime import datetime
from datetime import date
from datetime import time

# Security
# passlib, hashlib, bcrypt, scrypt
import hashlib
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    else:
        return False

# DB Management
import sqlite3
conn = sqlite3.connect('data.db', check_same_thread=False)
c = conn.cursor()

# Database functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT)')

def add_userdata(username, password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    return data

def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    return data

def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data

def app():
    st.subheader("Create New Account")
    new_first_name = st.text_input("First Name")
    new_last_name = st.text_input("Last Name")
    new_email = st.text_input("Email")
    new_password = st.text_input("Password", type = 'password')

    if st.button("Sign Up"):
        create_usertable()
        add_userdata(new_email, make_hashes(new_password))
        st.success("You have successfully created a new account.")
        st.info("Go to the login menu to login")   
    if st.button("Login"):
        st.success("You have logged in.")
        