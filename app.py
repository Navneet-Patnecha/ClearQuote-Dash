import streamlit as st
import pandas as pd
import plotly.express as px
from Pages import Page1
from QueryLLM import query


# Function to display the "About Me" page
def display_about_me():
    st.title("About Me")
    # Write your code for the About Me page here

# Main function to control navigation
def main():
    st.title("ClearQuote")
    st.write("---")

    # Create navigation bar at the top-right corner
    st.sidebar.title("Navigation")
    navigation_selection = st.sidebar.radio("Go to", ["Dashboard", "Query Your Data", "About Me"])

    if navigation_selection == "Dashboard":
        Page1.display_dashboard()
    elif navigation_selection == "Query Your Data":
        query.query_page()
    elif navigation_selection == "About Me":
        display_about_me()
if __name__ == "__main__":
    main()






