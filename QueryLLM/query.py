import streamlit as st
import pandas as pd
import os
from pandasai import SmartDatalake
from pandasai.responses.streamlit_response import StreamlitResponse
import plotly.graph_objs as go
from dotenv import load_dotenv

load_dotenv()

# Function to load and display data
def display_data():
    file_path = "ClearQuote.csv"
    if not os.path.isfile(file_path):
        st.error(f"File not found: {file_path}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error
    df = pd.read_csv(file_path)
    return df

# Function to render the query page
def query_page():
    with st.container():
        st.title("Query Your Data Using LLM")
        st.markdown(
            """
            <div style='background-color: #004d00; padding: 20px;margin-bottom: 20px;'>
                <h2 style='color: white; text-align: center;'>The query using the LLM works fine in the local environment but not in deployment</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    with st.expander("How it Works"):
        st.write("""
            This application utilizes PandasAI, a powerful library that allows you to query and analyze data using natural language. After loading a dataset from a CSV file, the application displays the data for exploration. You can then enter a query in plain English into the provided text area. When you click the "Run Query" button, PandasAI's SmartDatalake agent processes your natural language query, leveraging large language models to understand its intent and convert it into executable code. This code is then run on your dataset, and the results are rendered within the application as text. By integrating PandasAI, you can perform complex data analyses and generate insights without writing code manually, making the process more accessible and efficient.
        """)

    df = display_data()

    if df.empty:
        st.warning("The data frame is empty. Please check the file path or data source.")
        return

    with st.container():
        st.subheader("Data Preview")
        st.write(df)

    with st.container():
        st.subheader("Query Box")
        query = st.text_area("Enter your query here:")

        if st.button("Run Query"):
            pandasai_api_key = os.getenv('PANDASAI_API_KEY')
            if not pandasai_api_key:
                st.error("PANDASAI_API_KEY environment variable is not set.")
                return
            
            # Initialize SmartDatalake with the API key if applicable
            try:
                agent = SmartDatalake(
                    [df], 
                    config={
                        "verbose": True, 
                        "response_parser": StreamlitResponse,
                        "api_key": pandasai_api_key  # Pass the API key here if required by PandasAI
                    }
                )
                response = agent.chat(query)
                if isinstance(response, go.Figure):
                    st.plotly_chart(response)
                else:
                    st.write(response)
            except Exception as e:
                st.error(f"An error occurred: {e}")

