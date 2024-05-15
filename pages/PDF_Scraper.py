import streamlit as st
from pypdf import PdfReader 


uploaded_file = st.file_uploader("", accept_multiple_files=False)
if uploaded_file is not None:
  try:
    reader = PdfReader(uploaded_file)
    st.write(len(reader.pages))
    text = '%PDF Document: \n\n'
    counter = 1
    for each in reader.pages:
      text = text + "%PAGE: " + str(counter) + "\n\n" + each.extract_text() + "\n\n"
      counter += 1
    strip_file_name = uploaded_file.name[:-4]
    export_file_name = "Exported PDF Scrape - " + strip_file_name + ".txt"
    st.download_button('Download Output', data=prompt_file, file_name=export_file_name)
    st.write(text)
    
  except UnicodeDecodeError:
    st.write("Error reading pdf")


# creating a pdf reader object 
#reader = PdfReader('example.pdf') 
  
# printing number of pages in pdf file 
#print(len(reader.pages)) 
  
# getting a specific page from the pdf file 
#page = reader.pages[0] 
  
# extracting text from page 
#text = page.extract_text() 
#print(text) 
