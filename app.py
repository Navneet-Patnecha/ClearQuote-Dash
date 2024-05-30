import streamlit as st
import pandas as pd
import plotly.express as px
from Pages import Page1
from QueryLLM import query

# Function to display the navigation bar
def display_navigation_bar():
    nav_style = """
        <style>
            .navbar {
                background-color: #333;
                overflow: hidden;
                display: flex;
                justify-content: flex-end;
                padding: 10px;
            }
            .navbar a {
                color: white;
                text-align: center;
                padding: 14px 16px;
                text-decoration: none;
                font-size: 18px;
            }
            .navbar a:hover {
                background-color: #ddd;
                color: black;
            }
        </style>
    """
    st.markdown(nav_style, unsafe_allow_html=True)

    # Create a container for the navigation bar
    container = st.container()
    with container:
        st.markdown('<div class="navbar">', unsafe_allow_html=True)
        navigation_selection = st.radio("", ["Dashboard", "Query Your Data"], horizontal=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.sidebar.markdown("##")  # Placeholder for sidebar space

    return navigation_selection

# Main function to control the page layout and content
def main():
    st.set_page_config(page_title="ClearQuote", layout="wide")

    navigation_selection = display_navigation_bar()

    if navigation_selection == "Dashboard":
        Page1.display_dashboard()
    elif navigation_selection == "Query Your Data":
        query.query_page()

# Entry point for the application
if __name__ == "__main__":
    main()
