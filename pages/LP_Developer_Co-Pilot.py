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


URL = "https://developers.liveperson.com/sitemap.xml"

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

st.title('LP Developer Co-Pilot')

col1, col2 = st.columns([0.9, 0.1], gap="large")

user_message_space = col1.empty()
response_message_space = col1.empty()


conversation_history = []
additionalContext = 'None'



userPrompt = st.chat_input("Say Something")

if userPrompt:

    url_link = requests.get(URL)
    url_link_soup = bs.BeautifulSoup(url_link.text, "lxml")
    url_links = url_link_soup.find_all("loc")

    completion = client_us.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
        {"role": "system", "content": """
            Your task is to select the URLs from the list that would most likely answer the users query. 
            Return the URLs as a comma seperated list. Example: link1.com, link2.com. 
            Return a maximum of 5 URLs.
            Only return the link do not return any Markdown or html.
        """},
        {"role": "assistant", "content": "URLs: " + str(url_links)},
        {"role": "user", "content": userPrompt}
      ]
    )
    urls_list_string = completion.choices[0].message.content

    
    urls_list = urls_list_string.split(',')
    
    
    amalgamated_article_text = ''
    
    for each_url in urls_list:
      page = requests.get(each_url)
      soup = BeautifulSoup(page.content, "html.parser")
      soup_text = soup.get_text()
      soup_text = soup_text.replace('\n', ' ')
      amalgamated_article_text = amalgamated_article_text + "URL: " + each_url + "\n Article Information: " + soup_text + "\n"
    

    fullPrompt=[
        {"role": "system", "content": """
        You are a LivePerson Virtual Assistant.
        Your task is to answer the users query using the provided articles. 
        Return the response followed by any Article URL's you have used in your answer. 
        """},
        {"role": "assistant", "content": "URLs: " + amalgamated_article_text},
        {"role": "user", "content": userPrompt}
      ]
    
    
    completion = client_us.chat.completions.create(
      model="gpt-4o-mini",
      messages=fullPrompt
    )
    
    llmResponse = completion.choices[0].message.content


    data, count = supabase.table('LPDevGPT_DB').insert({"session_id": str(session_id), "user_name": userName, "user_query": userPrompt, "llm_response": llmResponse, "full_prompt": fullPrompt}).execute()
    user_message_space.markdown('#### You \n\n' + userPrompt)
    split_text = llmResponse.split(" ")
    displayed_text = '#### LP-GPT \n\n'

    
    for x in split_text:
        displayed_text = displayed_text + ' ' + x
        response_message_space.markdown(displayed_text)
        time.sleep(0.1)


 
