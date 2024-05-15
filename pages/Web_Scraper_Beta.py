import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

def RemoveHTMLTags(strr):
    return re.compile(r'<[^>]+>').sub('', strr)


url = st.text_input("Enter URL", "")
if st.button("Run"):
    #URL = "https://en.wikipedia.org/wiki/A.I._Artificial_Intelligence"
    try:
        page = requests.get(url)
        
        soup = BeautifulSoup(page.content, "html.parser")
        
        results = soup.find()
        
        job_elements = results.find_all("p")
        
        buffer_string = ''
        
        for job_element in job_elements:
            clean_job_element = RemoveHTMLTags(str(job_element))
            buffer_string = buffer_string + "\n\n" + clean_job_element
        
        st.write(buffer_string)
    except MissingSchema:
        st.write(MissingSchema)
