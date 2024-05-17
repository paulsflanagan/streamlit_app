import requests
import streamlit as st


url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo"

page = requests.get(url)

st.write(page)
