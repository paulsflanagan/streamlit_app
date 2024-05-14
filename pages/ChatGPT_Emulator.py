import streamlit as st
from openai import AzureOpenAI
from supabase import create_client, Client
import time
import json

client = AzureOpenAI(
    api_key=st.secrets["api_key"],
    api_version=st.secrets["api_version"],
    azure_endpoint=st.secrets["azure_endpoint"]
)

userName = st.experimental_user.email
#st.session_state.text = ""
#st.text_input("Your input here", key="text")

spb_url = st.secrets["spb_url"]
spb_key = st.secrets["spb_key"]

#superbase_client = create_client(spb_url, spb_key)
supabase: Client = create_client(spb_url, spb_key)



#st.write(st.session_state.key)

st.title('ChatGPT Emulator')
#if st.button("Clear Conversation"):
    #data, count = supabase.table('StreamlitDB').delete().eq('user_name', userName).execute()


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



def call_oai(userPrompt, systemPrompt, conversationHistory, additionalContext):
    response = client.chat.completions.create(
    model="llmgateway-text-35turbo-1106-model",
    messages=[
        {
        "role": "system",
        "content": systemPrompt
        },
        {
        "role": "user",
        "content": "%CONVERSATION HISTORY: " + conversationHistory + "%USER QUERY: " userPrompt + " %ADDITIONAL CONTEXT: "
        }
    ],
    temperature=0,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return response.choices[0].message.content

def next_query_button_click(query):
    st.session_state.key = query


#time.sleep(3)

systemPrompt = '''You are a helpful assistant. Answer the users query. Limit your responses to 200 words.'''
#if not userPrompt:
#if 'userPrompt' in locals():
userPrompt = st.chat_input("Say Something")
#nextQueryPrompt = '''From the provided information create three short 4-5 word questions related to the subject matter and return formatted like this: ["question 1", "question 2","question 3"]'''

#if 'key' not in st.session_state:
#    st.write('init holding')
#    st.session_state['key'] = 'holding'

#if st.session_state.key == 'holding':
#    st.write('holding')
#else:
#    st.write('parsing' + st.session_state.key)
#    tempVariable = st.session_state.key
#    st.session_state.key = 'holding'
#    userPrompt = tempVariable


user_message_space = st.empty()
placeholder = st.empty()
conversationHistory = ''
additionalContext = ''

#placeholder.text_area('Conversation:', height=400 )



if userPrompt:
    llm_response = call_oai(userPrompt, systemPrompt, conversationHistory, additionalContext)
    data, count = supabase.table('StreamlitDB').insert({"user_name": userName, "user_query": userPrompt, "llm_response": llm_response}).execute()
    user_message_space.markdown('#### You \n\n' + userPrompt)
    split_text = llm_response.split(" ")
    displayed_text = '#### ChatGPT \n\n'
    for x in split_text:
        displayed_text = displayed_text + ' ' + x
        placeholder.markdown(displayed_text)
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
