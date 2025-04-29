import streamlit as st
from openai import AzureOpenAI
from supabase import create_client, Client

## AZURE CLIENT

client = AzureOpenAI(
    api_key=st.secrets["api_key"],
    api_version=st.secrets["api_version"],
    azure_endpoint=st.secrets["azure_endpoint"]
)

userName = "Unknown" #st.experimental_user.email
spb_url = st.secrets["spb_url"]
spb_key = st.secrets["spb_key"]

supabase: Client = create_client(spb_url, spb_key)

st.title('Persona Tester')


def call_oai(userPrompt, systemPrompt):
    
    fullPrompt = [
        {
            "role": "system",
            "content": systemPrompt
        }
    ]
    
    
    fullPrompt.append(
        {
            "role": "user",
            "content": userPrompt
        }
    )

    #st.write(fullPrompt)
    
    response = client.chat.completions.create(
    model="llmgateway-text-35turbo-1106-model",
    messages=fullPrompt,
    temperature=0,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return response.choices[0].message.content, fullPrompt
    
systemPrompt = st.text_area('Paste your prompt here:', height=200, value="")

userPrompt = st.text_area('Paste your unpersonified Response:', height=200, value="")

if st.button('Run'):
    llmResponse, fullPrompt = call_oai(userPrompt, systemPrompt)
    st.write(llmResponse)
    data, count = supabase.table('kiaTesting').insert({"prompt": systemPrompt, "prepersona": userPrompt, "postpersona": llmResponse, "username": userName}).execute()
