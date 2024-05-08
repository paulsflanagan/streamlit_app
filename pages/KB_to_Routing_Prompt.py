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
A description is a sentence that describes what the user could want to do in detail.
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
        df = pd.read_csv(uploaded_file)

        st.write(df)

        generated_intents = []
            
        if st.button("Run"):        
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
                
            #st.write("GENERATED INTENTS:: " + str(generated_intents))
    
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
                        #elif "-" in line:
                              #desc = line.split("-")[1].strip()
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
    
            # Potential here to generate user utterances to train NLU Model.
            for intent, desc_list in intents_data.items():
                tmp = ", ".join(desc_list)
                #st.write(f"{intent},{tmp}")
                #print(f"{intent},{tmp}")
    
            #json.dump(intents_data, open("kia_kb_2.json", "w+"), indent=4)
            #prompt_file = open("kia_prompts.txt", "w+")
            
            prompt_file = ''
            
            data_for_flow = []
            
            group_name = "FAQ Questions"
            
            for intent, desc in intents_data.items():
                intent_name = intent
                route_name = intent.upper().replace(" ", "_")
                #st.write(f"Intent: {intent}")
                #print(f"Intent: {intent}")
        
                #if False and len(desc) > 1:
                    #sys_msg = f"Your job is to integrate list of descriptions for the intent:'{intent_name}' into a single description. These dscriptions will be provided by the user. Your single description should fully describe the intent."
                    #user_msg = f"Here is a list of descriptions: {desc}\n\nSingle Descripton: "
                    #description = call_oai_generic()
                #else:
                    #description = desc[0]
                
                description = desc[0]
                
                prompt_file = prompt_file + f"\nintent: {intent_name}\n\tdesc: {description}\n\troute: [ROUTE::{route_name}]\n\n"
                flow_var_data = {}
                flow_var_data["enabled"] = True
                flow_var_data['name'] = intent_name
                flow_var_data["description"] = description
                flow_var_data["group"] = group_name
                data_for_flow.append(flow_var_data)
    
                #st.write(f"Desc: {desc}")
                #print(f"Desc: {desc}")
                #st.write("--")
                #print("--")

            #st.write(prompt_file)
            strip_file_name = uploaded_file.name[:-4]
            export_file_name = "Exported Routing Prompt - " + strip_file_name + ".txt"
            st.download_button('Download Output', data=prompt_file, file_name=export_file_name)

    except UnicodeDecodeError:
        st.write("Error Decoding CSV - Ensure encoding is utf-8")

