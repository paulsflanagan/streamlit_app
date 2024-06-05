import streamlit as st

st.title('Lucid Generator')

code = st.text_input("Enter Code", "")


api_key=st.secrets["api_key"],
api_version=st.secrets["api_version"],
azure_endpoint=st.secrets["azure_endpoint"]

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
