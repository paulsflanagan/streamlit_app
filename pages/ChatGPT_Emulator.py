import streamlit as st
from openai import AzureOpenAI
from supabase import create_client, Client
from io import StringIO
from pypdf import PdfReader 
import requests
import time
import json
import uuid


## SESSION ID

if 'key' not in st.session_state:
    st.session_state['key'] = uuid.uuid4()
    session_id = uuid.uuid4()
else:
    session_id = st.session_state['key']
    
#st.write(UID)

## AZURE CLIENT

#client = AzureOpenAI(
#    api_key=st.secrets["api_key_us"],
#    api_version=st.secrets["api_version_us"],
#    azure_endpoint=st.secrets["azure_endpoint_us"]
#)

## SECRETS

# Create LLM Gateway Client

idToken = st.secrets["llm_gateway_token"]
account_id = st.secrets["cb_account_id"]
trace_id = "paul_poc_GPT_EMULATOR"
gateway_url = 'https://lo.cbllmgateway.liveperson.net/api/v1/gateway/llm/accounts/' + account_id + '/chats?trace_id=' + trace_id + '&activate_links=false&handle_hallucinations=false&highlight_hallucinations=false&use_pl_cache=false&pci_mask_prompt=false'
headers = {'Authorization': 'Bearer ' + idToken,'Content-Type': 'application/json',}

def callGateway(system_prompt,assistant_prompt,user_prompt):
  data = {"messages_list": [{"role": "system", "content": system_prompt},{"role": "assistant", "content": assistant_prompt},{"role": "user", "content": user_prompt},],'subscription_name': 'lp-llm-ptu','request_config': {'model_name': 'gpt-4o-mini-2024-07-18',}}
  response = requests.post(gateway_url, headers=headers, json=data)
  return response.json()['results'][0]['text']

def callGatewayFP(fullPrompt):
  data = {"messages_list": [fullPrompt,],'subscription_name': 'ai-studio','request_config': {'model_name': 'gpt-4o',}}
  response = requests.post(gateway_url, headers=headers, json=data)
  return response.json()['results'][0]['text']

# Create SupaBase Client

userName = "Unknown" #st.experimental_user.email # Streamlit broke experimental_user
spb_url = st.secrets["spb_url"]
spb_key = st.secrets["spb_key"]

supabase: Client = create_client(spb_url, spb_key)



## UI HERE

st.title('ChatGPT 4o-mini Emulator')
#if st.button("Clear Conversation"):
    #data, count = supabase.table('StreamlitDB').delete().eq('user_name', userName).execute()

col1, col2 = st.columns([0.6, 0.4], gap="large")
uploaded_file = col1.file_uploader("", accept_multiple_files=False)
user_message_space = col1.empty()
response_message_space = col1.empty()
#history_message_space = col2.empty()

#conversationHistory = 'None'
additionalContext = 'None'

col2.write("Conversation History")
#st.sidebar
#if col2.button("Reset Session"):
#    st.session_state['key'] = uuid.uuid4()
#    history_message_space.write("Session Cleared")

conversation_history = supabase.table('StreamlitDB').select("*").eq('session_id', session_id).execute()
counter = 1
for row in conversation_history.data:
    if counter > len(conversation_history.data)-6:
        with col2.expander(row['user_query']):
            st.write(row['llm_response'])
    counter += 1



if uploaded_file is not None:
    try:
        bytes_data = uploaded_file.getvalue()
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        string_data = stringio.read()
        additionalContext = string_data
    except:
        try:
            reader = PdfReader(uploaded_file)
            #st.write(len(reader.pages))
            text = '%PDF Document: \n\n'
            counter = 1
            for each in reader.pages:
                text = text + "%PAGE: " + str(counter) + "\n\n" + each.extract_text() + "\n\n"
                counter += 1
                additionalContext = text
                #st.write(text)
        except:
            st.write("Error Reading File")


#def update_screen():
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



def call_oai(userPrompt, systemPrompt, conversation_history, additionalContext):

    
    fullPrompt = [
        {
            "role": "system",
            "content": systemPrompt + " %DOCUMENT: " + additionalContext
        }
    ]
    
    counter = 1
    for row in conversation_history.data:
        if counter > len(conversation_history.data)-3:
            fullPrompt.append( 
                {
                    "role": "user",
                    "content": row['user_query']
                }
            )
            fullPrompt.append(
                {
                    "role": "assistant",
                    "content": row['llm_response']
                }
            )
        counter += 1


    fullPrompt.append(
        {
            "role": "user",
            "content": userPrompt
        }
    )

    #st.write(fullPrompt)

    #response = client.chat.completions.create(
    #model="gpt-4o-mini",
    #temperature=0,
    #messages=fullPrompt,

    #)
    #return response.choices[0].message.content, fullPrompt
    return callGatewayFP(fullPrompt), fullPrompt

def next_query_button_click(query):
    st.session_state.key = query


#time.sleep(3)

systemPrompt = '''You are a helpful assistant. Answer the users query. Limit your responses to 200 words unless the user states otherwise.'''
#if not userPrompt:
#if 'userPrompt' in locals():
userPrompt = st.chat_input("Say Something")
#nextQueryPrompt = '''From the provided information create three short 4-5 word questions related to the subject matter and return formatted like this: ["question 1", "question 2","question 3"]'''



if userPrompt:
    llmResponse, fullPrompt = call_oai(userPrompt, systemPrompt, conversation_history, additionalContext)
    #st.write(fullPrompt)
    data, count = supabase.table('StreamlitDB').insert({"session_id": str(session_id), "user_name": userName, "user_query": userPrompt, "llm_response": llmResponse, "full_prompt": fullPrompt}).execute()
    user_message_space.markdown('#### You \n\n' + userPrompt)
    split_text = llmResponse.split(" ")
    displayed_text = '#### ChatGPT \n\n'


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
