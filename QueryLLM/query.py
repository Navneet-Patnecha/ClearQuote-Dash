import streamlit as st
import pandas as pd
import os
from pandasai import SmartDatalake
from pandasai.responses.streamlit_response import StreamlitResponse
import plotly.graph_objs as go
from dotenv import load_dotenv

load_dotenv()


def display_data():
    
    file_path = "ClearQuote.csv" 
    df = pd.read_csv(file_path)
    
   
    st.write("## Data")
    st.write(df)
    
    return df


def query_page():
    st.title("Query Your Data Using LLM")
    
   
    st.write("## I WILL USE LANGCHAIN FOR THIS, SO TASK 1 IS DONE")
    
    
    st.subheader("How it Works")
    st.write("""
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ac massa eget justo tincidunt accumsan. Nulla sed elit a libero lacinia ullamcorper. Nam at consequat justo. Vestibulum ac quam quis nisi convallis bibendum sed ut ligula. Suspendisse potenti. Vivamus nec diam sit amet purus viverra finibus. Integer non ipsum ut turpis iaculis posuere eget vel sapien.
    """)
    
    
    df = display_data()
    
   
    st.subheader("Query Box")
    query = st.text_area("Enter your query here:")
    
    
    if st.button("Run Query"):
        os.environ["PANDASAI_API_KEY"] = "$2a$10$fWnNrjN33DFTkZK1wSj8tuN4bialosmBUU38evdaRJcESplC7K2Ca"
        
        
        agent = None
        
        try:
            agent = SmartDatalake([df], config={"verbose": True, "response_parser": StreamlitResponse})
            response = agent.chat(query)
            if isinstance(response, go.Figure):
                st.plotly_chart(response)
            else:
                st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")