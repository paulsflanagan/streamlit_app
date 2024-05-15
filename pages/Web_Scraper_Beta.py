import streamlit as st
import requests

URL = "https://en.wikipedia.org/wiki/A.I._Artificial_Intelligence"
page = requests.get(URL)

st.write(page.text)
