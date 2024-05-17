import requests
import streamlit as st


# Quote Api
quoteApiUrl = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo"

#API DOCS
#https://www.alphavantage.co/documentation/

# Time Series Monthly
#https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=IBM&apikey=demo
#https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=TSCO.LON&apikey=demo


response = requests.get(quoteApiUrl) 

st.write(response.status_code)
st.write(response.json())

