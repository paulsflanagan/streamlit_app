import streamlit as st
import csv
       
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate


st.title('AI Transcript Assistant')


llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')
master_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<Analysis>'


# Upload CSV

uploaded_file = st.file_uploader("Upload a CSV file")

file = open("Import.csv", "r")
raw_data = list(csv.reader(file, delimiter=","))
file.close()

print("First Conversation ID: " + raw_data[0][0])
print("Last Conversation ID: " + raw_data[len(raw_data)-1][0])
print("Conversation Count: " + str(len(raw_data)-1))
