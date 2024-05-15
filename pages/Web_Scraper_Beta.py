import streamlit as st
import requests

URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)

st.write(page.text)
