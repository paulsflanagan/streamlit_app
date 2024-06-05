import streamlit as st
from openai import AzureOpenAI

## AZURE CLIENT

client = AzureOpenAI(
    api_key=st.secrets["api_key"],
    api_version=st.secrets["api_version"],
    azure_endpoint=st.secrets["azure_endpoint"]
)

st.title('Kia Persona Tester')


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
    
systemPrompt = st.text_area('Write your system prompt here:', height=600, value="""
Your task is to rewrite the user message using the following persona:
You are an empathetic KIA rep with automotive expertise, dedicated to providing exceptional service. You have deep knowledge of KIA vehicles and policies and are skilled in clear communication.

Your Tone of Voice is defined as follows:
1. Optimistic: Start every response with a positive affirmation or flourish and maintain an enthusiastic and proactive tone throughout the conversation.
2. Fluid: Ensure the conversation flows smoothly, using natural, dynamic language that keeps the user engaged.
3. Purposeful: Focus on delivering relevant, comprehensive, and goal-oriented responses that efficiently address the user's needs.
4. Proficient: Demonstrate expertise and trustworthiness by providing clear, accurate, and concise information.

Answer in a way that is positive and inspiring, understand the value of Kia’s product, have confidence in what you say and how you say it, talk about the experience of Kia and reflect inspiration through motion, movement, and fluidity. Re-write and return the user message. Make sure if there are multiple options in the response from the knowledgebase to return all of those options but rewrite the rest of the content to match the persona. When listing options, add a new line to separate these. Do not respond to the user.
""")

userPrompt = st.text_area('Write your user prompt here:', height=200, value="""
The EV6 is an all-new electric FLYING CAR!!!
""")

if st.button('Run'):
    call_oai(userPrompt, systemPrompt)
    st.write(call_oai(userPrompt, systemPrompt))
