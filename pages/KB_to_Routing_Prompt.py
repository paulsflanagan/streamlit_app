import json
from openai import AzureOpenAI
import csv
import streamlit as st
import pandas as pd
from io import StringIO


st.title('Convert a Knowledge Base to Routing Prompts')

client = AzureOpenAI(
    api_key=st.secrets["api_key"],
    api_version=st.secrets["api_version"],
    azure_endpoint=st.secrets["azure_endpoint"]
)

sPromptIntentsFromKB = "Your job is to analyze the following article and provide a list of possible intents and description that could be served by that article. An intent is a short phrase (5 words or less) that describes something that a customer could want to do. A description is a short sentence that describes what the user is doing. You should provide at least one and not more than 10 possible intents and decription for the article. You should return each intent and description in this format: 1. Intent:<intent name>\nDescription:<description>\n2. Intent:..."
sPromptRoutesFromIntent = ""

def call_oai(prompt, systemPrompt):
    response = client.chat.completions.create(
    model="llmgateway-text-35turbo-1106-model",
    messages=[
        {
        "role": "system",
        "content": systemPrompt
        },
        {
        "role": "user",
        "content": prompt
        }
    ],
    temperature=0,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return response.choices[0].message.content




# Upload CSV

uploaded_file = st.file_uploader("Upload a Knoweldgebase CSV file", accept_multiple_files=False)
if uploaded_file is not None:
    
    try:
        bytes_data = uploaded_file.getvalue()
        #stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        #string_data = stringio.read()
        df = pd.read_csv(uploaded_file)

        st.write(df)

        generated_intents = []

        #if st.button("Run"):
        
            #rows = list(reader)
            #intent_data = []
            #armed = False
    
            #for i, row in enumerate(rows): // Ethans
            #for z in range(df.shape[1]):
                #for elem in row.keys():
                #istruct = {'intent': df[z].iloc[0], 'phrases': []}
                #intent_data.append(istruct)
            #st.write("INTEND DATA" + str(intent_data))
            
                
        for x in range(df.shape[0]):
            #title = row['title']
            #summary = row['summary']
            #detail = row['detail']
            #category = row['category']
            #tags = row["detail"]
                
            st.write(df[x].iloc['title'])
            st.write(df[x].iloc['summary'])
            st.write(df[x].iloc['detail'])
            st.write(df[x].iloc['category'])
            st.write(df[x].iloc['tags'])
    
                #phrases = []
                #for y in range(df.shape[0]):
                    #st.write(df[x].iloc[y])
                    #for i, row in enumerate(rows): // Ethans
                    # First row has intent names
                    #if len(row) == 0:
                        #if len(row) == 0:
                        #continue
                    #if df[x][y] == "SampleSentences": 
                        #if row[intent_data[0]['intent']] == "SampleSentences": 
                        #st.write("FOUND IT!!!! ::::" + df[x][y])
                        #armed = True
                        #continue
                        #pd.isnull(df.at[2, 'Salary']
                    #if pd.isnull(df.at[y,x]):
                        #armed = False
                   # if armed:
                            #phrases.append(df[x][y])
                            
                #st.write(str(phrases))
                #istruct = {'intent': df[x].iloc[0], 'phrases': phrases}
                #intent_data.append(istruct)
            #st.write("INTEND DATA" + str(intent_data))
                            #for intent_elem in intent_data:
                            #intent_elem['phrases'].append(row[intent_elem['intent']])
            #amnt = len(intent_data)
    
            #st.write(amnt)
    
            #outputString = ''
                
            #for i, intent_elem in enumerate(intent_data):
                #intent_name = intent_elem['intent']
                #if "MetaIntent" in intent_name:
                    #st.write(f"Skipping {i}/{amnt} Intent: {intent_elem['intent']}...")
                    #print(f"Skipping {i}/{amnt} Intent: {intent_elem['intent']}...")
                    #continue
                #route_name = intent_name.upper().replace(" ", "_")
                #st.write(f"{i+1}/{amnt} Intent: {intent_elem['intent']}")
                #print(f"{i}/{amnt} Intent: {intent_elem['intent']}")
                #phrases = ",".join([p for p in intent_elem['phrases'] if p and p != "" and p != "Regexes"])
                #user_message = f"Examples of user messages: {phrases}"
                #description = call_oai(user_message)
                #st.write(f"\nintent: {intent_name}\n\tdesc: {description}\n\troute: {route_name}\n")
                #outputString = outputString + f"\nintent: {intent_name}\n\tdesc: {description}\n\troute: {route_name}\n"
                #prompt_file.write(f"\nintent: {intent_name}\n\tdesc: {description}\n\troute: {route_name}\n")
            #st.write("OUTPUT:")
            #st.write(outputString)
            #strip_file_name = uploaded_file.name[:-5]
            #export_file_name = "Exported Routing Prompt - " + strip_file_name + ".txt"
            #st.download_button('Download Output', data=outputString, file_name=export_file_name)
                
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

