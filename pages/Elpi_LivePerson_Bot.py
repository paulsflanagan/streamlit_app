import streamlit as st
from openai import AzureOpenAI
from supabase import create_client, Client
import time
import json
import uuid
import bs4 as bs
import requests
import os
from bs4 import BeautifulSoup


#URL = "https://www.liveperson.com/sitemap/sitemap-0.xml"

## SESSION ID

if 'key' not in st.session_state:
    st.session_state['key'] = uuid.uuid4()
    session_id = uuid.uuid4()
else:
    session_id = st.session_state['key']

## AZURE CLIENT

client_us = AzureOpenAI(
    api_key=st.secrets["api_key_us"],
    api_version=st.secrets["api_version_us"],
    azure_endpoint=st.secrets["azure_endpoint_us"]
)

## SECRETS

userName = st.experimental_user.email
spb_url = st.secrets["spb_url"]
spb_key = st.secrets["spb_key"]

supabase: Client = create_client(spb_url, spb_key)



## UI HERE

st.title('Elpi Website Co-Pilot')

col1, col2 = st.columns([0.9, 0.1], gap="large")
user_message_space = col1.empty()
response_message_space = col1.empty()

conversation_history = []
additionalContext = 'None'

user_query = st.chat_input("Say Something")

if user_query:

    article_details_search, pull_count = supabase.table('LivePerson_site_scrape').select("*").execute()

    llm_search_string = ""

    for each in article_details_search[1]:
        buffer_string = "URL: " + each['url'] + " - (Contains: " + each['title'] + ")\n"
        llm_search_string = llm_search_string + buffer_string
    
    # US COMPLETION MODEL 4o Mini
    completion = client_us.chat.completions.create(
        model="gpt-4o-mini",
        response_format = { "type": "json_object" },
        temperature = 0,
        messages=[
            {"role": "system", "content": """
                Your task is to select the URLs from the list that would most likely answer the users query.
                Return a maximum of 5 URLs.
                Return the URLs as a Comma Seperated List.
                Return a JSON object with a field called urls that is an array of the urls.
    
            """},
            {"role": "assistant", "content": "Content: " + llm_search_string},
            {"role": "user", "content": user_query}
          ]
    )

    urls_list_string = completion.choices[0].message.content
    col1.write(urls_list_string)
    urls_list_json = json.loads(urls_list_string)
    urls_list = urls_list_json.get('urls', [])

    amalgamated_article_text = ''

    for each_url in urls_list:
        article_text, pull_count = supabase.table('LivePerson_site_scrape').select("summary").eq("url", each_url).execute()
        try:
            summary = article_text[1][0]["summary"]
        except:
            summary = ""
        
        amalgamated_article_text = amalgamated_article_text + "URL: " + each_url + "\n Article Information: " + summary + "\n"
        
    col1.write(amalgamated_article_text)
    # US COMPLETION MODEL 4o Mini
    completion = client_us.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """
                You are a LivePerson Assistant.
                Your task is to answer the users query using the provided articles.
                Return the response followed by any Article URL's you have used in your answer.
            """},
            {"role": "assistant", "content": "URLs: " + amalgamated_article_text},
            {"role": "user", "content": user_query}
          ]
    )

    llmResponse = completion.choices[0].message.content

    fullPrompt = '' #Temporary
    
    data, count = supabase.table('LPWebsiteGPT_DB').insert({"session_id": str(session_id), "user_name": userName, "user_query": user_query, "llm_response": llmResponse, "full_prompt": fullPrompt}).execute()
    user_message_space.markdown('#### You \n\n' + user_query)
    split_text = llmResponse.split(" ")
    displayed_text = '#### Elpi \n\n'
    
    for x in split_text:
        displayed_text = displayed_text + ' ' + x
        response_message_space.markdown(displayed_text)
        time.sleep(0.1)
