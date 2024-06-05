import streamlit as st

st.title('Lucid Generator')

code = st.text_input("Enter Code", "")


l_cid = st.secrets["l_cid"]
l_cs = st.secrets["l_cs"]

st.write(l_cid)

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
