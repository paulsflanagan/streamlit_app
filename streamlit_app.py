import os
import streamlit as st
from langchain.llms import OpenAI

os.environ['OPENAI_API_KEY'] = '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'

st.title('YoutTube GPT Creator')

prompt = st.text_input('Plug in your prompt here')

llm = OpenAI(temperature=0.9)

if prompt:
  response = llm(prompt)
  st.write(response)
