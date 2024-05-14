import streamlit as st
from openai import AzureOpenAI
from supabase import create_client, Client
import time
import json


st.title('Simple LLM Interface')

placeholder = st.empty()

text_to_display = '''
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras viverra dapibus nunc, vulputate eleifend ex tincidunt sit amet.
'''

split_text = text_to_display.split(" ")

for x in split_text:
  st.write(x + '\b')

#    col1, col2, col3 = st.columns([1,1,1])
#    with col1:
#       st.button(next_query_object[0], on_click=next_query_button_click(next_query_object[0]))
#    with col2:
#        st.button(next_query_object[1], on_click=next_query_button_click(next_query_object[1]))
#    with col3:
#        st.button(next_query_object[2], on_click=next_query_button_click(next_query_object[2]))



