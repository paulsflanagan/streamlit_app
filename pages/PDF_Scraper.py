import streamlit as st
from pypdf import PdfReader 


uploaded_file = st.file_uploader("", accept_multiple_files=False)
if uploaded_file is not None:
  try:
    reader = PdfReader(uploaded_file)
    st.write(len(reader.pages))
    text = ''
    for each in reader.pages:
      text = text + "\n\n" + each.extract_text()
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
