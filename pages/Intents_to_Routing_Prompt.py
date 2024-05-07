import json
from openai import AzureOpenAI
import csv
import streamlit as st
#import pandas as pd
#from io import StringIO


st.title('Intents To Routing Prompt')

client = AzureOpenAI(
    api_key=st.secrets["api_key"],
    api_version=st.secrets["api_version"],
    azure_endpoint=st.secrets["azure_endpoint"]
)

# Upload CSV

uploaded_file = st.file_uploader("Upload an Intents CSV file", accept_multiple_files=False)
if uploaded_file is not None:
    
    try:
        reader = csv.DictReader(uploaded_file.getvalue())
        rows = list(reader)
        intent_data = []
        armed = False
        for i, row in enumerate(rows):
            # First row has intent names
            if not intent_data:
                for elem in row.keys():
                    istruct = {'intent': elem, 'phrases': []}
                    intent_data.append(istruct)
            if len(row) == 0:
                continue
            if row[intent_data[0]['intent']] == "SampleSentences": 
                armed = True
                continue
            if armed:
                for intent_elem in intent_data:
                    intent_elem['phrases'].append(row[intent_elem['intent']])
        #bytes_data = uploaded_file.getvalue()
        #stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        #string_data = stringio.read()
        #df = pd.read_csv(uploaded_file)
        #df.columns = ['Conversation ID', 'Transcript']
        #st.write("First Conversation ID: " + df['Conversation ID'][0])
        #st.write("Last Conversation ID: " + df['Conversation ID'][df.shape[0]-1])
        #st.write("Conversation Count: " + str(df.shape[0]))
    except UnicodeDecodeError:
        st.write("Error Decoding CSV - Ensure encoding is utf-8")

