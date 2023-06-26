# import module
import streamlit as st
import pandas as pd
import datetime
from datetime import datetime
from datetime import date
from datetime import time
import sign_up

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
    st.title('Automated Smart Scheduler')
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type= 'password')

    view_all_users()
    if st.checkbox("Login"):
        # if password == '12345'
        create_usertable()
        hashed_pswd = make_hashes(password)

        result = login_user(email, check_hashes(password, hashed_pswd))
        if result:
            st.success("Logged in as {}".format(email))
        else:
            st.warning("Incorrect Username or Password")
    if st.button('Not a user? Sign up here.'):
        sign_up.app
    
"""

    def main():
        
        elif choice == "Login":
            st.subheader("Login Section")
            username = st.sidebar.text_input("User Name")
            password = st.sidebar.text_input("Password", type= 'password')
            if st.sidebar.checkbox("Login"):
                # if password == '12345'
                create_usertable()
                hashed_pswd = make_hashes(password)

                result = login_user(username, check_hashes(password, hashed_pswd))
                if result:
                    st.success("Logged in as {}".format(username))
                    task = st.selectbox("Task", ["Add Post", "Analytics","Profiles"])
                    if task == "Add post":
                        st.subheader("Add your post")
                    
                    elif task == "Analytics":
                        st.subheader("Analytics")
                    
                    elif task == "Profiles":
                        st.subheader("User Profiles")
                        user_result = view_all_users()
                        clean_db = pd.DataFrame(user_result, columns=["Username", "Password"])
                        st.dataframe(clean_db)
                else:
                    st.warning("Incorrect Username or Password")

        elif choice == "SignUp":
            st.subheader("Create New Account")
            new_user = st.text_input("Username")
            new_password = st.text_input("Password", type = 'password')

            if st.button("Signup"):
                create_usertable()
                add_userdata(new_user, make_hashes(new_password))
                st.success("You have successfully created a new account.")
                st.info("Go to the login menu to login")    
    if __name__ == '__main__':
        main()

"""