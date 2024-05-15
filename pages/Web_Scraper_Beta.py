import streamlit as st
import requests

URL = "https://en.wikipedia.org/wiki/A.I._Artificial_Intelligence"
page = requests.get(URL)

#st.write(page.text)

text_buffer = ''
for x in page.text
  if x == '<':
    reading = false
  if x == '>':
    reading = true
  if reading
    text_buffer = text_buffer + x
  
st.write(text_buffer)
