import streamlit as st
import requests
from bs4 import BeautifulSoup

def RemoveHTMLTags(strr):
    # Print string after removing tags
    print(re.compile(r'<[^>]+>').sub('', strr))

URL = "https://en.wikipedia.org/wiki/A.I._Artificial_Intelligence"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find()

job_elements = results.find_all("p")

buffer_string = ''

for job_element in job_elements:
    clean_job_element = RemoveHTMLTags(job_element)
    buffer_string = buffer_string + "\n\n" + clean_job_element

st.write(buffer_string)
