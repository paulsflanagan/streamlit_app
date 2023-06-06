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
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    string_data = stringio.read()
    df = pd.read_csv(uploaded_file)
    df.columns = ['Conversation ID', 'Transcript']
    st.write("First Conversation ID: " + df['Conversation ID'][0])
    st.write("Last Conversation ID: " + df['Conversation ID'][df.shape[0]-1])
    st.write("Conversation Count: " + str(df.shape[0]))


# Task


task = """ 

<Conversation>
  <Conversation_id> What is the Conversation ID? 
  <Intent> What is the Intent of the conversation? [Purchase Watch, Upgrade, Payg Offers, Add Airpods, End Contract, Bolt Ons, Add Line, Unknown, Join O2, My O2, Sim Card, Refund, Billing, Stock Enquiry, network Issue]
  <Sub_Intent> What is the Sub Intent?
  <Sale_Made> Was a sale made?
  <Reason_for_No_Sale> Why do you think a sale was made?
  <Product_or_Device> What product or device is the customer discussing?
  <Information_Asked> Summarise the information the agent asked for?
  <Query_Resolved> Was the customer query resolved?
  <Reason_for_Unresolved> Why do you think the sale was resolved?
  <Agent_Summary> Summarise what the agent did in this conversation?
</Conversation>

"""  
