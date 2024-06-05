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

