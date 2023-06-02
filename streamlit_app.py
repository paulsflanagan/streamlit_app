!pip install langchain 
!pip install streamlit
!pip install openai

import os
import streamlit as st
from langchain.llms import OpenAI

st.title('YoutTube GPT Creator')

prompt = st.text_input('Plug in your prompt here')

llm = OpenAI(temperature=0.9)

if prompt:
  response = llm(prompt)
  st.write(response)
