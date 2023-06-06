from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
import streamlit as st
import csv


llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')
master_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<Analysis>'


st.title('AI Transcript Assistant')

                                   
