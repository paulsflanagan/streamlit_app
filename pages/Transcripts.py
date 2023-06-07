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
<A_Conversation_id> What is the Conversation ID? 
<B_Intent> What is the Intent of the conversation? [Purchase Watch, Upgrade, Payg Offers, Add Airpods, End Contract, Bolt Ons, Add Line, Unknown, Join O2, My O2, Sim Card, Refund, Billing, Stock Enquiry, network Issue]
<C_Sub_Intent> What is the Sub Intent?
<D_Sale_Made> Was a sale made?
<E_Reason_for_No_Sale> Why do you think a sale was made?
<F_Product_or_Device> What product or device is the customer discussing?
<G_Information_Asked> Summarise the information the agent asked for?
<H_Query_Resolved> Was the customer query resolved?
<I_Reason_for_Unresolved> Why do you think the sale was resolved?
<J_Agent_Summary> Summarise what the agent did in this conversation?
</Conversation>''')

t = st.empty()
if st.button('Analyse'):
    t.write('Running your request')
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
        st.write("Error From Open AI - Token count too high")

    master_xml = master_xml + '\n</Analysis>'

    #st.write(master_xml)
    
    # Download the Result
    
    st.download_button('Download Output', data=master_xml, file_name="Export1234.xml")









