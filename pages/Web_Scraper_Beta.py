import streamlit as st
import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/A.I._Artificial_Intelligence"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find()

job_elements = results.find_all("div")

for job_element in job_elements:
    title_element = job_element.find("h2")
    company_element = job_element.find("h3")
    location_element = job_element.find("p")
    try:
        st.write("Element: " + title_element.text + company_element.text + location_element.text)
    except:
        st.write("An element missing?")

#st.write(page.text)
#text_buffer = ''
#previous_char = ''
#reading = True
#x = 0
#for current_char in page.text:
#  if current_char == '<' or current_char == '{' or current_char == '[':
#    reading = False
#  if previous_char == '>' or previous_char == '}' or previous_char == ']':
#    reading = True
#  if reading:
#    text_buffer = text_buffer + current_char
#  previous_char = current_char
#  x += 1
  
#st.write(text_buffer)
