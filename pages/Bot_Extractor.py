import streamlit as st
import json

st.title('LP Bot Extractor')

uploaded_file = st.file_uploader("Upload a bot json file", accept_multiple_files=False)

if uploaded_file is not None:
    
      #bytes_data = uploaded_file.getvalue()
      stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
      string_data = stringio.read()
      data = json.load(f)
      st.write(data)  




