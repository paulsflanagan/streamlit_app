import streamlit as st
import csv
import pandas as pd
    
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from io import StringIO

st.title('AI Transcript Assistant')


llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')
master_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<Analysis>'


# Upload CSV

uploaded_file = st.file_uploader("Upload a CSV file", accept_multiple_files=False)
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    #st.write(bytes_data)
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    #st.write(stringio)
    string_data = stringio.read()
    #st.write(string_data)
    df = pd.read_csv(uploaded_file)
    df.columns = ['Conversation ID', 'Transcript']
    #st.write("Active CSV: " + string_data)
    st.write("First Conversation ID: " + df['Conversation ID'][0])
    st.write("Last Conversation ID: " + df['Conversation ID'][df.shape[0]-1])
    st.write("Conversation Count: " + str(df.shape[0]))

       #print("First Conversation ID: " + raw_data[0][0])
       #print("Last Conversation ID: " + raw_data[len(raw_data)-1][0])
       #print("Conversation Count: " + str(len(raw_data)-1))
