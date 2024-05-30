import streamlit as st
import pandas as pd
import plotly.express as px
from Pages import Page1
from QueryLLM import query


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

    container = st.container()

    
    with container:
        st.markdown('<div class="navbar">', unsafe_allow_html=True)
        navigation_selection = st.radio("", ["Dashboard", "Query Your Data"], horizontal=True)
        st.markdown('</div>', unsafe_allow_html=True)

    
    st.sidebar.markdown("##")

    return navigation_selection

def main():
    st.set_page_config(page_title="ClearQuote", layout="wide")

    navigation_selection = display_navigation_bar()

    if navigation_selection == "Dashboard":
        Page1.display_dashboard()
    elif navigation_selection == "Query Your Data":
        query.query_page()
   

if __name__ == "__main__":
    main()


