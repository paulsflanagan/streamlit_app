import requests
import streamlit as st


url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo"

page = requests.get(url)

response = requests.get("https://api.open-notify.org/this-api-doesnt-exist") 
print(response.status_code)

#st.write(page)
