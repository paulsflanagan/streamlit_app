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


URLs = ["https://www.qantas.com/qcom4-sitemap.xml"]
#,"https://www.qantas.com/qcom4-sitemap.xml" - Airport Guides
#,"https://www.qantas.com/qcom3-sitemap.xml" - onbord information /seat maps
#,"https://www.qantas.com/qcom6-sitemap.xml" - frequent flyer / mebeships
#,"https://www.qantas.com/city-pairs-sitemap.xml"
#,"https://www.qantas.com/travelinsider/en/sitemap.xml"
#,"https://www.qantas.com/agencyconnect/sitemap.xml"
#,"https://www.qantas.com/qcom1-sitemap.xml"
#,"https://www.qantas.com/flights-to-city-sitemap.xml"
#,"https://www.qantas.com/flights-to-country-sitemap.xml"
#,https://www.qantas.com/qcom9-sitemap.xml - corporate cards and ?
#,"https://www.qantas.com/qcom7-sitemap.xml" - inspiration / blogs
#,"https://www.qantas.com/qcom5-sitemap.xml" - General Info (baggage payments etc)
#, "https://www.qantas.com/qcom2-sitemap.xml" - Travel guides
#,"https://www.qantas.com/qcom8-sitemap.xml" - future history / sustainability

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

st.title('Quantas Au Co-Pilot')

col1, col2 = st.columns([0.9, 0.1], gap="large")
#uploaded_file = col1.file_uploader("", accept_multiple_files=False)
user_message_space = col1.empty()
response_message_space = col1.empty()
#history_message_space = col2.empty()

conversation_history = []
additionalContext = 'None'

#col2.write("Conversation History")
#st.sidebar
#if col2.button("Reset Session"):
#    st.session_state['key'] = uuid.uuid4()
#    history_message_space.write("Session Cleared")

#conversation_history = supabase.table('StreamlitDB').select("*").eq('session_id', session_id).execute()
#counter = 1
#for row in conversation_history.data:
#    if counter > len(conversation_history.data)-6:
 #       with col2.expander(row['user_query']):
#            st.write(row['llm_response'])
#    counter += 1


# def update_screen():
#    response = supabase.table('StreamlitDB').select("*").eq('user_name', userName).execute()
    #st.text_area('Conversation:', height=400, value=str(response))
#    testString = ''
#    conversationHistory = ''#'Previous Questions Asked: '
#    with placeholder.container():
        #st.write("This is one element")
        #st.write("This is another")
#        count = 0
#        for x in response.data:
#            count += 1
#            if count > len(response.data)-3:
#                st.write('User: ' + x['user_query'])
#                st.write('Bot: ' + x['llm_response'])
#                st.write(' ')
                #conversationHistory = conversationHistory + ' - ' + x['user_query']
                #conversationHistory = conversationHistory + 'User: ' + x['user_query'] + 'Bot: ' + x['llm_response']
#    return conversationHistory



#def call_oai(userPrompt, systemPrompt, conversation_history, additionalContext):

    
#    fullPrompt = [
#        {
#            "role": "system",
#            "content": systemPrompt + " %DOCUMENT: " + additionalContext
#        }
#    ]
    
    #counter = 1
    #for row in conversation_history.data:
        #if counter > len(conversation_history.data)-3:
            #fullPrompt.append( 
                #{
                 #   "role": "user",
                #    "content": row['user_query']
                #}
            #)
            #fullPrompt.append(
                #{
                    #"role": "assistant",
                    #"content": row['llm_response']
                #}
            #)
        #counter += 1


 #   fullPrompt.append(
 #       {
 #          "role": "user",
 #           "content": userPrompt
  #      }
  #  )

    #st.write(fullPrompt)
    
 #   response = client.chat.completions.create(
 #   model="gpt-4o-mini",
 #   messages=fullPrompt,
 #   temperature=0,
 #   max_tokens=256,
 #   top_p=1,
 #   frequency_penalty=0,
 #   presence_penalty=0
 #   )
 #   return response.choices[0].message.content, fullPrompt

#def next_query_button_click(query):
#    st.session_state.key = query


#time.sleep(3)

#systemPrompt = '''You are a helpful assistant. Answer the users query. Limit your responses to 200 words unless the user states otherwise.'''
#if not userPrompt:
#if 'userPrompt' in locals():


userPrompt = st.chat_input("Say Something")

if userPrompt:

    url_links = []
    for URL in URLs:
      url_link = requests.get(URL)
      url_link_soup = bs.BeautifulSoup(url_link.text, "xml")
      url_links_buffer = url_link_soup.find_all("loc")
      url_links_buffer = url_links_buffer + url_link_soup.find_all("path")
      url_links = url_links + url_links_buffer

    completion = client_us.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
        {"role": "system", "content": """
            Your task is to select the URLs from the list that would most likely answer the users query. 
            Return the URLs as a comma seperated list. Example: link1.com, link2.com. 
            Only return the link do not return any Markdown or html.
        """},
        {"role": "assistant", "content": "URLs: " + str(url_links)},
        {"role": "user", "content": userPrompt}
      ]
    )
    urls_list_string = completion.choices[0].message.content
    #print(urls_list_string)
    
    urls_list = urls_list_string.split(',')
    
    #print(urls_list)
    
    amalgamated_article_text = ''
    
    for each_url in urls_list:
      page = requests.get(each_url)
      soup = BeautifulSoup(page.content, "html.parser")
      soup_text = soup.get_text()
      soup_text = soup_text.replace('\n', ' ')
      amalgamated_article_text = amalgamated_article_text + "URL: " + each_url + "\n Article Information: " + soup_text + "\n"
    
    #print(amalgamated_article_text)

    fullPrompt=[
        {"role": "system", "content": """
        You are a LivePerson Virtual Assistant.
        Your task is to answer the users query using the provided articles. 
        Return the response followed by any Article URL's you have referrenced in your answer. 
        """},
        {"role": "assistant", "content": "Articles: " + amalgamated_article_text},
        {"role": "user", "content": userPrompt}
      ]
    
    
    completion = client_us.chat.completions.create(
      model="gpt-4o-mini",
      messages=fullPrompt
    )
    
    llmResponse = completion.choices[0].message.content

    
    #llmResponse, fullPrompt = call_oai(userPrompt, systemPrompt, conversation_history, additionalContext)
    #st.write(fullPrompt)
    data, count = supabase.table('Quantas_GPT_DB').insert({"session_id": str(session_id), "user_name": userName, "user_query": userPrompt, "llm_response": llmResponse, "full_prompt": fullPrompt}).execute()
    user_message_space.markdown('#### You \n\n' + userPrompt)
    split_text = llmResponse.split(" ")
    displayed_text = '#### Quantas-GPT \n\n'


    ## ADD CONVERSATION HISTORY TO PROMPT

    #if conversationHistory == 'Non':
    #    conversationHistory = "%User: " + userPrompt + " %Assistant: " + llmResponse + "\n"
    #    st.write(conversationHistory)
    #else:
    #    conversationHistory = conversationHistory + "%User: " + userPrompt + " %Assistant: " + llmResponse + "\n"

    ## ADD CONV HISTORY TO COL2
    
    #with col2.expander(userPrompt):
    #    st.write(llmResponse)

    
    for x in split_text:
        displayed_text = displayed_text + ' ' + x
        response_message_space.markdown(displayed_text)
        time.sleep(0.1)


    #st.write('Bot: ' + llm_response)
    #st.write(' ')
    #next_query_llm_response = call_oai(userPrompt, nextQueryPrompt, conversationHistory)
    #st.write(next_query_llm_response)
    #try:
    #    next_query_object = json.loads(next_query_llm_response)
    #    userPrompt = ''
    #    col1, col2, col3 = st.columns([1,1,1])
    #    with col1:
    #       st.button(next_query_object[0], on_click=next_query_button_click(next_query_object[0]))
    #    with col2:
    #        st.button(next_query_object[1], on_click=next_query_button_click(next_query_object[1]))
    #    with col3:
    #        st.button(next_query_object[2], on_click=next_query_button_click(next_query_object[2]))
    #except:
    #    st.write(' ')
            
    
    #update_screen()
