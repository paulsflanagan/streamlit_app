import streamlit as st
from openai import AzureOpenAI

## AZURE CLIENT

client = AzureOpenAI(
    api_key=st.secrets["api_key"],
    api_version=st.secrets["api_version"],
    azure_endpoint=st.secrets["azure_endpoint"]
)

st.title('ChatGPT Emulator V2b')


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
    
systemPrompt = st.text_area('Write your system prompt here:', height=200, value="""
    - You are an AI Bot that is very good at analysing conversation transcripts
    - Your goal is to find relevant information from the transcript
    - Only use information in the transcript provided
    - For every opening tag you must add a closing tag
    - Only use the tags provided. Do not create new tags
    - Output in xml""")
userPrompt = st.text_area('Write your user prompt here:', height=200, value="""
    - You are an AI Bot that is very good at analysing conversation transcripts
    - Your goal is to find relevant information from the transcript
    - Only use information in the transcript provided
    - For every opening tag you must add a closing tag
    - Only use the tags provided. Do not create new tags
    - Output in xml""")

if st.button('Run'):
    call_oai(userPrompt, systemPrompt)
    st.write(call_oai(userPrompt, systemPrompt))
