import streamlit as st
import requests
from bs4 import BeautifulSoup



#stripped = text.split(sep, 1)[0]

url = st.text_input("Enter URL", "https://www.geeksforgeeks.org/")

sep = '?'
root = url
completed_list = []
buffer_list = []
buffer_list.append(url)

placeholder = st.empty()

if st.button("Run"):

    while len(buffer_list) > 0:
        
        page = requests.get(url)
            
        soup = BeautifulSoup(page.content, "html.parser")
            
        results = soup.find()
            
        job_elements = results.find_all("a")
               
        for job_element in job_elements:
            #clean_job_element = RemoveHTMLTags(str(job_element))
            if job_element.has_attr('href'):
                if root in job_element['href']:
                    if job_element['href'].split(sep, 1)[0] not in buffer_list:
                        buffer_list.append(job_element['href'].split(sep, 1)[0])
                    
        completed_list.append(url)
        buffer_list.remove(url)
        
        if len(buffer_list) > 0:
            url = buffer_list[0]

        placeholder.write("Completed: " + str(buffer_list) + " Buffer: " + str(buffer_list))
