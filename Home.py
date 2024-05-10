import streamlit as st
from openai import AzureOpenAI
from supabase import create_client, Client

st.title('Welcome')

client = AzureOpenAI(
    api_key=st.secrets["api_key"],
    api_version=st.secrets["api_version"],
    azure_endpoint=st.secrets["azure_endpoint"]
)


spb_url = st.secrets["spb_url"]
spb_key = st.secrets["spb_key"]

#superbase_client = create_client(spb_url, spb_key)
supabase: Client = create_client(spb_url, spb_key)

# STRUCTURE HERE
#response = supabase.table('StreamlitDB').select("*").execute()
#testString = response.data[0]['test']
#data=[{'id': 1, 'created_at': '2024-05-10T15:09:19.501548+00:00', 'test': 'test 1234'}, {'id': 2, 'created_at': '2024-05-10T15:49:03.275302+00:00', 'test': 'did this work'}, {'id': 3, 'created_at': '2024-05-10T15:49:57.479494+00:00', 'test': 'YEY!!!!!'}] count=None


#st.text_area('Conversation:', height=400, value=str(response))

response = supabase.table('StreamlitDB').select("*").eq('user_name', 'paul.s.flanagan@gmail.com').execute()

st.text_area('Conversation:', height=400, value=str(response))

# ADDD STUFF HERE
#st.text_area('DID IT WORK:', height=400, value=testString)
#submit_string = st.text_area('Add Here:', height=200, value="")
#if st.button("Submit"):
    #data, count = supabase.table('StreamlitDB').insert({"test": submit_string}).execute()


systemPrompt = ''


def call_oai(userPrompt, systemPrompt):
    response = client.chat.completions.create(
    model="llmgateway-text-35turbo-1106-model",
    messages=[
        {
        "role": "system",
        "content": systemPrompt
        },
        {
        "role": "user",
        "content": userPrompt
        }
    ],
    temperature=0,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return response.choices[0].message.content

systemPrompt = st.text_area('System:', height=100, value='''You are a helpful assistant.''')
userPrompt = st.text_area('Query:', height=50, value='')

if st.button("Run"):
    st.write(call_oai(userPrompt, systemPrompt))
