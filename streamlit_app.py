
import os
import streamlit as st
from langchain.llms import OpenAI

st.title('LP AI Assistant')

prompt = st.text_area('Write your prompt here:')

llm = OpenAI(temperature=0.9)

if prompt:
  response = llm(prompt)
  st.write(response)
