import streamlit as st
import csv
import pandas as pd
    
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from io import StringIO

st.title('AI Transcript Analysis')


llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')
master_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<Analysis>'


# Upload CSV

uploaded_file = st.file_uploader("Upload a CSV file", accept_multiple_files=False)
if uploaded_file is not None:
    
    try:
        bytes_data = uploaded_file.getvalue()
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        string_data = stringio.read()
        df = pd.read_csv(uploaded_file)
        df.columns = ['Conversation ID', 'Transcript']
        st.write("First Conversation ID: " + df['Conversation ID'][0])
        st.write("Last Conversation ID: " + df['Conversation ID'][df.shape[0]-1])
        st.write("Conversation Count: " + str(df.shape[0]))
    except UnicodeDecodeError:
        st.write("Error Decoding CSV - Ensure encoding is utf-8")
        
    



# Task

task = st.text_area('Write your questions here:', height=400, value='''
<Conversation>
<Conversation_id> What is the Conversation ID? 
<Intent> What is the Intent of the conversation? [Purchase, Upgrade, MagicMobile, Customer Support, Refund, Billing, Unknown]
<Sub_Intent> What is the Sub Intent?
<Sale_Made> Was a sale made by the agent?
<Reason_for_Sale_Answer> Explain why you believe a sale was made?
<Product_or_Device> What product or device is the customer discussing?
<Information_Asked> Summarise the information the agent asked for?
<Query_Resolved> Was the customer query resolved?
<Reason_for_Resolution_Answer> Explain why you believe the customer query was resolved or not resolved?
<Agent_Summary> Summarise what the agent did in this conversation?
</Conversation>''')

t = st.empty()
if st.button('Analyse'):
    if uploaded_file is not None:
        for x in range(df.shape[0]):
          t.write("Executing: " + str(x + 1) + " of " + str(df.shape[0]) + " : " + str(round(((x)/df.shape[0])*100)) +"% Complete ")
          transcript = "Conversation ID: " + df['Conversation ID'][x] + "\n" + df['Transcript'][x]
          template = """
          % INSTRUCTIONS
           - You are an AI Bot that is very good at analysing conversation transcripts
           - Your goal is to find relevant information from the transcript
           - Do not go outside the transcript provided
           - Output in an xml format with the questions as the headers. Do not Output [<?xml version="1.0" encoding="UTF-8"?>]. Do not output a Root Node

          % Transcript for Analysis:
          {transcript}

          % YOUR TASK
          {task}

          """

          prompt = PromptTemplate(
              input_variables=["transcript","task"],
              template=template,
          )

          final_prompt = prompt.format(transcript=transcript,task=task)

          try:
            data = llm.predict(final_prompt)
            master_xml = master_xml + '\n' + data
          except:
            st.write("Error From Open AI - Token count too high for Conversation: " + str(x) + " : " + df['Conversation ID'][x])

        master_xml = master_xml + '\n</Analysis>'

        t.write("Analysis Completed")

        # Download the Result
        strip_file_name = uploaded_file.name[:-4]
        export_file_name = "AT Output - " + strip_file_name + ".csv"
        df_out = pd.read_xml(master_xml)
        csv_ouput = df_out.to_csv()
        st.download_button('Download Output', data=csv_ouput, file_name=export_file_name)
    else:
        st.write("No Data Set to Analyse")








