import requests
import streamlit as st


url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo"

response = requests.get(url) 

st.write(response.status_code))
st.write(response.json())
#st.write(page)
