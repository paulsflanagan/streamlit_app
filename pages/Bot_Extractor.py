import streamlit as st
import pandas as pd
import json
from io import StringIO


st.title('Bot Extractor - JSON Test')

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    string_data = stringio.read()
    data = jsons.load(string_data.read())


#st.json()
