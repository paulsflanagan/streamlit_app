import requests
import streamlit as st
import json

# Quote Api
quoteApiUrl = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo"

#API DOCS
#https://www.alphavantage.co/documentation/

# Time Series Monthly
#https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=IBM&apikey=demo
#https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=TSCO.LON&apikey=demo


response = requests.get(quoteApiUrl) 

st.write(response.status_code)
st.write(str(response.json()))
st.write("Price: " + response.json()['Global Quote'])

st.write(response['Global Quote']['05. price'])


# Assuming the JSON string is stored in a variable called 'json_data'
#json_data = '{"Global Quote": {"01. symbol": "IBM", "02. open": "168.2600", "03. high": "169.6300", "04. low": "167.7900", "05. price": "168.9700", "06. volume": "3492267", "07. latest trading day": "2024-05-16", "08. previous close": "168.2600", "09. change": "0.7100", "10. change percent": "0.4220%"}}'

# Convert the JSON string to a Python dictionary
#data_dict = json.loads(json_data)

# Access the price

  # Output: 168.
