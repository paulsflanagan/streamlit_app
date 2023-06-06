import streamlit as st
import csv
    
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
#from io import StringIO

st.title('AI Transcript Assistant')


llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')
master_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<Analysis>'


# Upload CSV

uploaded_file = st.file_uploader("Upload a CSV file", accept_multiple_files=False)
if uploaded_file is not None:
    #bytes_data = uploaded_file.getvalue()
    st.write(uploaded_file.name)    
    file = open("uploaded_file.csv", "r")
    raw_data = list(csv.reader(file, delimiter=","))
    file.close()

       #print("First Conversation ID: " + raw_data[0][0])
       #print("Last Conversation ID: " + raw_data[len(raw_data)-1][0])
       #print("Conversation Count: " + str(len(raw_data)-1))
