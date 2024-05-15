import streamlit as st
import requests

URL = "https://en.wikipedia.org/wiki/A.I._Artificial_Intelligence"
page = requests.get(URL)

#st.write(page.text)

text_buffer = ''
reading = True
for x in page.text:
  if x == '<':
    reading = False
  if x == '>':
    reading = True
  if reading:
    text_buffer = text_buffer + x
  
st.write(text_buffer)
