import json
from openai import AzureOpenAI
import csv
import streamlit as st
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
#from io import StringIO


st.title('Knowledgebase Optimization for AI Search - Summary Only')
st.warning('Currently Adapted to NOT Update the Detail', icon="⚠️")
st.write("AI Search utilizes the KB summary for retrieval and the KB detail for response. This app will summarise the full article to replace the summary, then add the summary to the beginning of the detail. Original Script Thanks to Konrad Zuchniak")

#client = AzureOpenAI(
#    api_key=st.secrets["api_key"],
#    api_version=st.secrets["api_version"],
#    azure_endpoint=st.secrets["azure_endpoint"]
#
#)

# Create LLM Gateway Client

idToken = st.secrets["llm_gateway_token"]
account_id = st.secrets["cb_account_id"]
trace_id = "paul_poc_kb_optimiser"
gateway_url = 'https://lo.cbllmgateway.liveperson.net/api/v1/gateway/llm/accounts/' + account_id + '/chats?trace_id=' + trace_id + '&activate_links=false&handle_hallucinations=false&highlight_hallucinations=false&use_pl_cache=false&pci_mask_prompt=false'
headers = {'Authorization': 'Bearer ' + idToken,'Content-Type': 'application/json',}

def callGateway(system_prompt,assistant_prompt,user_prompt):
  data = {"messages_list": [{"role": "system", "content": system_prompt},{"role": "assistant", "content": assistant_prompt},{"role": "user", "content": user_prompt},],'subscription_name': 'ai-studio','request_config': {'model_name': 'gpt-4o',}}
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


sPromptReWriteSummary = """
Your task is to Summarize the article in a way that is optimized for searches of knowledge bases and documentation.
Specifically focus on:
Using natural keywords and keyphrases from other fields in the rewritten summary
The goal is to rewrite the summary in a way that improves its findability and searchability, helping more easily surface related knowledge, instructions or answers.
Ensure the summary less than 900 characters.
Please provide only the optimized version of the summary."""

#def call_oai(prompt, systemPrompt):
#    response = client.chat.completions.create(
#    model="llmgateway-text-35turbo-1106-model",
#    messages=[
#        {
#        "role": "system",
#        "content": systemPrompt
#        },
#        {
#        "role": "user",
#        "content": prompt
#        }
#    ],
#    temperature=0,
#    max_tokens=256,
#    top_p=1,
#    frequency_penalty=0,
#    presence_penalty=0
#    )
#    return response.choices[0].message.content




uploaded_file = st.file_uploader("Upload a Knoweldgebase CSV file", accept_multiple_files=False)
if uploaded_file is not None:
    
    try:
        bytes_data = uploaded_file.getvalue()
        df = pd.read_csv(uploaded_file)
        
        st.write("Original KB")
        st.write(df)
        
        

        if st.button("Run"):
            
            t = st.empty()
            
            new_summaries = []
            #for i, row in kb_df.iterrows():
            for x in range(df.shape[0]):
                t.write(f"... 🔥 Processing Row: {x}")
                #print(f"process row: {i}")
                
                title = df['title'].iloc[x]
                summary = df['summary'].iloc[x]
                detail = df['detail'].iloc[x]
                category = df['category'].iloc[x]
                tags = df['tags'].iloc[x]
                article_data = f'## ARTICLE ##\nTitle: {title}, Summary: {summary}, Detail: {detail},  Category: {category }, Tags: {tags}, Optimized Summary:'
                user_prompt = "Run your task."
                new_summary = callGateway(sPromptReWriteSummary,article_data,user_prompt)
                if len(new_summary) >= 1000:
                  new_summary = new_summary[:999]
                #new_summary = call_oai(article_data, sPromptReWriteSummary)
                #st.write("Old Summary: " + summary)
                #st.write("New Summary: " + new_summary)
                new_summaries.append(new_summary)
                
            t.write("... 🔥 Conversion Complete")
            
            df["summary"] = new_summaries
            
            new_detail = []
            ###################
            ###### DISABLED FOR JEN K 07/06/24 - Re enable for GA
            #for x in range(df.shape[0]):
            #    new_detail.append(f"{df['summary'].iloc[x]} {df['detail'].iloc[x]}")
            #df["detail"] = new_detail
            ###################

    
            st.write("Updated KB")
            st.write(df)
            
            # Download the Result
            data_as_csv = df.to_csv(index=False).encode("utf-8")
            
            strip_file_name = uploaded_file.name[:-4]
            export_file_name = "EXP - " + strip_file_name + ".csv"
            
            st.download_button('Download Output', data=data_as_csv, file_name=export_file_name)


    
    except UnicodeDecodeError:
        st.write("Error Decoding CSV - Ensure encoding is utf-8")
