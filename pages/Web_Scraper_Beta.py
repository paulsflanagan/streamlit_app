import streamlit as st
import requests

URL = "https://en.wikipedia.org/wiki/A.I._Artificial_Intelligence"
page = requests.get(URL)

#st.write(page.text)

text_buffer = ''
previous_char = ''
reading = True

for current_char in page.text:
  if current_char == '<':
    reading = False
  if previous_char == '>':
    reading = True
  if reading:
    text_buffer = text_buffer + current_char
  previous_char = current_char
  
st.write(text_buffer)
