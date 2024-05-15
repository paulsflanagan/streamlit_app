import streamlit as st
import requests
from bs4 import BeautifulSoup


sep = '...'
#stripped = text.split(sep, 1)[0]

url = st.text_input("Enter URL", "https://www.geeksforgeeks.org/")

if st.button("Run"):
    
    page = requests.get(url)
        
    soup = BeautifulSoup(page.content, "html.parser")
        
    results = soup.find()
        
    job_elements = results.find_all("a")
        
    buffer_string = ''
        
    for job_element in job_elements:
        #clean_job_element = RemoveHTMLTags(str(job_element))
        if job_element.has_attr('href'):
            buffer_string = buffer_string + "\n\n" + job_element['href'].split(sep, 1)[0]
        
    st.write(buffer_string)
