import streamlit as st
import requests
from bs4 import BeautifulSoup



#stripped = text.split(sep, 1)[0]

url = st.text_input("Enter URL", "https://www.geeksforgeeks.org/")

sep = '?'
root = url

if st.button("Run"):
    
    page = requests.get(url)
        
    soup = BeautifulSoup(page.content, "html.parser")
        
    results = soup.find()
        
    job_elements = results.find_all("a")
        
    buffer_list = []
        
    for job_element in job_elements:
        #clean_job_element = RemoveHTMLTags(str(job_element))
        if job_element.has_attr('href'):
            if root in job_element['href']:
                buffer_list.append(job_element['href'].split(sep, 1)[0])
        
    st.write(str(buffer_list))
