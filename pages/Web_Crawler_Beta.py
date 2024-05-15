import streamlit as st
import requests
from bs4 import BeautifulSoup


url = st.text_input("Enter URL", "https://www.geeksforgeeks.org/")
if st.button("Run"):
    #URL = "https://en.wikipedia.org/wiki/A.I._Artificial_Intelligence"
    page = requests.get(url)
        
    soup = BeautifulSoup(page.content, "html.parser")
        
    results = soup.find()
        
    job_elements = results.find_all("a")
        
    buffer_string = ''
        
    for job_element in job_elements:
        #clean_job_element = RemoveHTMLTags(str(job_element))
        if job_element.has_attr('href'):
            buffer_string = buffer_string + "\n\n" + str(job_element)
        
    st.write(buffer_string)
