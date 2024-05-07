import json
from openai import AzureOpenAI
import csv
import streamlit as st
import pandas as pd
from io import StringIO


st.title('Intents To Routing Prompt')

client = AzureOpenAI(
    api_key=st.secrets["api_key"],
    api_version=st.secrets["api_version"],
    azure_endpoint=st.secrets["azure_endpoint"]
)


def call_oai(prompt):
    response = client.chat.completions.create(
    model="llmgateway-text-35turbo-1106-model",
    messages=[
        {
        "role": "system",
        "content": "Your job is to describe what the user is trying to do given the follow examples input messages. Your description should be at most 20 words."
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

uploaded_file = st.file_uploader("Upload an Intents CSV file", accept_multiple_files=False)
if uploaded_file is not None:
    
    try:
        bytes_data = uploaded_file.getvalue()
        #stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        #string_data = stringio.read()
        df = pd.read_csv(uploaded_file, header=None)

        st.write(df)
        
        reader = csv.DictReader(df)

        for i in reader:
            st.write(i)
        
        st.write(reader)
        
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
        amnt = len(intent_data)

        st.write(amnt)
            
        for i, intent_elem in enumerate(intent_data):
            intent_name = intent_elem['intent']
            if "MetaIntent" in intent_name:
                st.write(f"Skipping {i}/{amnt} Intent: {intent_elem['intent']}...")
                #print(f"Skipping {i}/{amnt} Intent: {intent_elem['intent']}...")
                continue
            route_name = intent_name.upper().replace(" ", "_")
            st.write(f"{i}/{amnt} Intent: {intent_elem['intent']}")
            #print(f"{i}/{amnt} Intent: {intent_elem['intent']}")
            phrases = ",".join([p for p in intent_elem['phrases'] if p and p != "" and p != "Regexes"])
            user_message = f"Examples of user messages: {phrases}"
            description = call_oai(user_message)
            st.write(f"\nintent: {intent_name}\n\tdesc: {description}\n\troute: {route_name}\n")
            #prompt_file.write(f"\nintent: {intent_name}\n\tdesc: {description}\n\troute: {route_name}\n")
            
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

