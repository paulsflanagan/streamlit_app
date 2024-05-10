import streamlit as st
import csv
import pandas as pd
from openai import AzureOpenAI
from io import StringIO

st.title('Transcript AI Annotator')
st.write("Closed for Rennovation")



master_xml = '\n<Analysis>'

client = AzureOpenAI(
    api_key=st.secrets["api_key"],
    api_version=st.secrets["api_version"],
    azure_endpoint=st.secrets["azure_endpoint"]
)

# Upload CSV

ADMIN_USERS = {
    'paul.s.flanagan@gmail.com',
    'person2@email.com',
    'person3@email.com'
}

if st.experimental_user.email in ADMIN_USERS:
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



# Build Strings For Prompt

instructionsTitle = """

% INSTRUCTIONS

"""

instructions = st.text_area('Write your instructions here:', height=200, value="""- You are an AI Bot that is very good at analysing conversation transcripts
   - Your goal is to find relevant information from the transcript
   - Only use information in the transcript provided
   - For every opening tag you must add a closing tag
   - Only use the tags provided. Do not create new tags
   - Output in xml""")

transcriptTitle = """

% TRANSCRIPT

"""

questionsTitle = '''

% QUESTIONS

'''

questions = st.text_area('Write your questions here:', height=400, value='''<Conversation>
  <Conversation_id> What is the Conversation ID?
  <Intent> What is the Intent of the conversation? [Purchase Watch, Upgrade, Payg Offers, Add Airpods, End Contract, Bolt Ons, Add Line, Unknown, Join O2, My O2, Sim Card, Refund, Billing, Stock Enquiry, network Issue]
  <Sub_Intent> What is the Sub Intent?
  <Sale_Made> Was a sale made?
  <Reason_for_No_Sale> Why do you think a sale was made? 
  <Product_or_Device> What product or device is the customer discussing?
  <Information_Asked> Summarise in a sentence the information the agent asked for?
  <Query_Resolved> Was the customer query resolved?
  <Reason_for_Unresolved> Why do you think the sale was resolved?
  <Agent_Summary> Summarise in a sentence what the agent did in this conversation?
</Conversation>''')

trigger = """

Run your Instructions

"""


t = st.empty()
if st.button('Analyse'):
    if uploaded_file is not None:
        for x in range(df.shape[0]):
            t.write("Executing: " + str(x + 1) + " of " + str(df.shape[0]) + " : " + str(round(((x)/df.shape[0])*100)) +"% Complete ")
            transcript = "Conversation ID: " + df['Conversation ID'][x] + "\n" + df['Transcript'][x]
            prompt = instructionsTitle + instructions + transcriptTitle + transcript + questionsTitle + questions;
            try:
                # Run Completion
                completion = client.chat.completions.create(
                    model='llmgateway-text-35turbo-1106-model',
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": trigger}
                    ]
                )
                master_xml = master_xml + '\n' + completion.choices[0].message.content
            except:
                st.write("Error From Open AI - Token count too high for Conversation: " + str(x) + " : " + df['Conversation ID'][x])
            
        master_xml = master_xml + '\n</Analysis>'
        master_xml = master_xml.replace('<?xml version="1.0" encoding="UTF-8"?>', '')
        master_xml = master_xml.replace('```xml', '')
        master_xml = master_xml.replace('```', '')
        master_xml = '<?xml version="1.0" encoding="UTF-8"?>' + master_xml
            
        t.write("Analysis Completed")

        # Download the Result
        try:
            strip_file_name = uploaded_file.name[:-4]
            export_file_name = "AT Output - " + strip_file_name + ".csv"
            df_out = pd.read_xml(master_xml)
            csv_ouput = df_out.to_csv()
            st.download_button('Download Output - CSV', data=csv_ouput, file_name=export_file_name)
        except:
            strip_file_name = uploaded_file.name[:-4]
            export_file_name = "AT Output - " + strip_file_name + ".xml"
            #df_out = pd.read_xml(master_xml)
            #csv_ouput = df_out.to_csv()
            #st.write("Error Encoding CSV - Outputting as XML")
            st.download_button('Download Output - XML', data=master_xml, file_name=export_file_name)
            
    else:
        st.write("No Data Set to Analyse")







