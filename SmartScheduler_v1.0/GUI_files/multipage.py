"""
This file can be used to host multiple Streamlit applications/pages
in one connected place.
"""

# Import libraries
import streamlit as st

# create multipage class
class MultiPage:
    def __init__(self) -> None:
        # Constructor class to generate list that stores applications as an instance variable
        self.pages = []
    
    def add_page(self, title, func) -> None:
        """ class method to add pages to the project
        Args:
            title ([str]): The title page which we are adding to the list of apps
            func: Python function to render the page in Streamlit
        """

        self.pages.append({
            "title": title,
            "function": func
        })
    
    def run(self):
        # Dropdown to select the page to run
        page = st.sidebar.selectbox(
            'App Navigation',
            self.pages,
            format_func=lambda page: page['title']
        )
        # run the app function
        page['function']()