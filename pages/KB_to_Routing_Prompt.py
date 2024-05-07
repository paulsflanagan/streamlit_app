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

sPromptIntentsFromKB = """
Your job is to analyze the following article and provide an intent and description that could be served by that article.
An intent is a short phrase (5 words or less) that describes something that a customer could want to do. 
A description is a sentence that describes what the user is doing.
You should return each intent and description in this format: Intent:<intent name>\nDescription:<description>"""
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
            title = df['title'].iloc[x]
            summary = df['summary'].iloc[x]
            detail = df['detail'].iloc[x]
            category = df['category'].iloc[x]
            tags = df['tags'].iloc[x]
            summary = str(summary).replace("\n", ". ").replace("\"", "\\\"")
            detail = str(detail).replace("\n", ". ").replace("\"", "\\\"")

            article_data = f'## ARTICLE ##\nTitle: {title}, Summary: {summary}, Detail: {detail},  Category: {category }, Tags: {tags}\n\nIntent and Description List: '
            #print(f"{i}/{len(rows)}")
            possible_intents = call_oai(article_data, sPromptIntentsFromKB)
            generated_intents.append(possible_intents)
            
        st.write("GENERATED INTENTS:: " + str(generated_intents))

        intents_data = {}
    
        for intent_generation in generated_intents:
            intent = None
            desc = None
            for line in intent_generation.split("\n"):
                #print(line)
                if not intent and line:
                    if "Intent:" in line:
                        intent = line.split("Intent:")[1].strip()
                        line = line.split("Intent:")[1].strip()
    
                    elif line[0] in [s for s in map(str, range(11))]:
                        intent = line.split(".")[1].strip()
    
                if not desc and line:
                    if "Description:" in line:
                        desc = line.split("Description:")[1].strip()
                    elif "-" in line:
                          desc = line.split("-")[1].strip()
                    elif ":" in line:
                          desc = line.split(":")[1].strip()
                    elif ":" in line:
                          desc = line.split(":")[1].strip()
    
                if intent and desc:
                    #print(f"... 🔥 Intent: {intent} Desc: {desc}")
                    st.write(f"... 🔥 Intent: {intent} Desc: {desc}")
                    if intent not in intents_data:
                        intents_data[intent] = [desc]
                    else:
                        intents_data[intent].append(desc)
    
                    intent = None
                    desc = None
            #st.write(df['title'].iloc[x])
            #st.write(df['summary'].iloc[x])
            #st.write(df['detail'].iloc[x])
            #st.write(df['category'].iloc[x])
            #st.write(df['tags'].iloc[x])
    
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

