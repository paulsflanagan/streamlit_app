import streamlit as st
from io import StringIO

st.title('Lucid Generator')


l_cid = st.secrets["l_cid"]
l_cs = st.secrets["l_cs"]
l_ruri = st.secrets["l_ruri"]

code = st.text_input("Enter Code", "")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    if st.button("Submit"):
        st.write("Boo")
