import streamlit as st
from openai import AzureOpenAI
from supabase import create_client, Client

st.title('Welcome')

client = AzureOpenAI(
    api_key=st.secrets["api_key"],
    api_version=st.secrets["api_version"],
    azure_endpoint=st.secrets["azure_endpoint"]
)



SUPABASE_URL = st.secrets("SUPABASE_URL")
SUPABASE_KEY = st.secrets("SUPABASE_KEY")
cuperbase_client = create_client(SUPABASE_URL, SUPABASE_KEY)

response = supabase.table('StreamlitDB').select("*").execute()

st.text_area(response)


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
