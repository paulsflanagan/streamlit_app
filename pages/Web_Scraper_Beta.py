import streamlit as st
import requests

URL = "https://paulsflanagan.com"
page = requests.get(URL)

st.write(page.text)
