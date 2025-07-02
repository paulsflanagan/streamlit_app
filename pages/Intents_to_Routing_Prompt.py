import json
from openai import AzureOpenAI
import csv
import streamlit as st
import pandas as pd
from io import StringIO


st.title('Convert Intents to Routing Prompts')
st.write("Original Script Thanks to Ethan Selfridge")

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
        "content": "Your job is to describe what the user is trying to do given the follow examples input messages. Your description should be a sentence at most 20 words. Do not use bullet points."
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


def callGateway(system_prompt,assistant_prompt,user_prompt):
  data = {"messages_list": [{"role": "system", "content": system_prompt},{"role": "assistant", "content": assistant_prompt},{"role": "user", "content": user_prompt},],'subscription_name': 'lp-llm-ptu','request_config': {'model_name': 'gpt-4o-mini-2024-07-18',}}
  #response = requests.post(gateway_url, headers=headers, json=data)
  #return response.json()['results'][0]['text']
  
  session = requests.Session()
  retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[ 500, 502, 503, 504 ])  # Retry on these status codes
  session.mount('https://', HTTPAdapter(max_retries=retries))
  

  try:
    response = session.post(gateway_url, headers=headers, json=data)
    response.raise_for_status()  # Raise an exception for bad status codes
    return response.json()['results'][0]['text']
  except requests.exceptions.RequestException as e:
    print(f"Error calling gateway: {e}")
    # You can choose to handle the error here, e.g., retry with a delay, skip the current row, etc.
    # For now, we'll just return an empty string
    return ""




uploaded_file = st.file_uploader("Upload an Intents CSV file", accept_multiple_files=False)
if uploaded_file is not None:
    
    try:
        bytes_data = uploaded_file.getvalue()
        df = pd.read_csv(uploaded_file, header=None)
        st.write(df)
        reader = csv.DictReader(df)

        if st.button("Run"):
            st.write("... 🔥 Creating Routes")
            intent_data = []
            armed = False        
                
            for x in range(df.shape[1]):
                phrases = []
                for y in range(df.shape[0]):
                    if df[x][y] == "SampleSentences": 
                        armed = True
                        continue
                    if pd.isnull(df.at[y,x]):
                        armed = False
                    if armed:
                            phrases.append(df[x][y])
                            
                istruct = {'intent': df[x].iloc[0], 'phrases': phrases}
                intent_data.append(istruct)
                
            amnt = len(intent_data)
            outputString = ''
                
            for i, intent_elem in enumerate(intent_data):
                intent_name = intent_elem['intent']
                if "MetaIntent" in intent_name:
                    st.write(f"Skipping {i}/{amnt} Intent: {intent_elem['intent']}...")
                    #print(f"Skipping {i}/{amnt} Intent: {intent_elem['intent']}...")
                    continue
                route_name = intent_name.upper().replace(" ", "_")
                #st.write(f"{i+1}/{amnt} Intent: {intent_elem['intent']}")
                #print(f"{i}/{amnt} Intent: {intent_elem['intent']}")
                phrases = ",".join([p for p in intent_elem['phrases'] if p and p != "" and p != "Regexes"])
                user_message = f"Examples of user messages: {phrases}"
                description = call_oai(user_message)
                #st.write(f"\nintent: {intent_name}\n\tdesc: {description}\n\troute: {route_name}\n")
                outputString = outputString + f"\nintent: {intent_name}\n\tdesc: {description}\n\troute: [ROUTE::{route_name}]\n"

            strip_file_name = uploaded_file.name[:-4]
            export_file_name = "Exported Routing Prompt - " + strip_file_name + ".txt"
            st.download_button('Download Output', data=outputString, file_name=export_file_name)
                
    except UnicodeDecodeError:
        st.write("Error Decoding CSV - Ensure encoding is utf-8")

