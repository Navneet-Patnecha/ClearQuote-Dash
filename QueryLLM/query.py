import streamlit as st
import pandas as pd
import os
from pandasai import SmartDatalake
from pandasai.responses.streamlit_response import StreamlitResponse
import plotly.graph_objs as go
from dotenv import load_dotenv
load_dotenv()
# Function to read the CSV file and display the data
def display_data():
    # Read the CSV file from the specified location
    file_path = "ClearQuote.csv"  # Replace with the actual file path
    df = pd.read_csv(file_path)

    # Display the data in the center of the page
    st.write("## Data")
    st.write(df)

    return df

# Function to display the Query Your Data page
def query_page():
    st.title("Query Your Data Using LLM")

    # Explanation of the process
    st.subheader("How it Works")
    st.write("""
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ac massa eget justo tincidunt accumsan. Nulla sed elit a libero lacinia ullamcorper. Nam at consequat justo. Vestibulum ac quam quis nisi convallis bibendum sed ut ligula. Suspendisse potenti. Vivamus nec diam sit amet purus viverra finibus. Integer non ipsum ut turpis iaculis posuere eget vel sapien.
    """)

    # Display the data
    df = display_data()

    # Text box for user input
    st.subheader("Query Box")
    query = st.text_area("Enter your query here:")

    # Button to execute the query
    if st.button("Run Query"):
    pandasai_api_key = os.getenv("PANDASAI_API_KEY")
    os.environ["PANDASAI_API_KEY"] = pandasai_api_key
    agent = SmartDatalake([df], config={"verbose": True, "response_parser": StreamlitResponse})

    try:
        response = agent.chat(query)
        if isinstance(response, go.Figure):
            st.plotly_chart(response)
        else:
            st.write(response)
    except Exception as e:
        st.error(f"An error occurred: {e}")
        # Check if the response contains a Plotly figure
        if isinstance(response, go.Figure):
            st.plotly_chart(response)
        else:
            st.write(response)

