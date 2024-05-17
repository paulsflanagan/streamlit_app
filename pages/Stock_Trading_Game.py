import requests
import streamlit as st
import json

fz_key=st.secrets["fz_key"]

# Quote Api
#quoteApiUrl = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo"


#url = "https://api.finazon.io/latest/time_series?apikey=" + fz_key


url = "https://api.finazon.io/latest/time_series?dataset=sip_non_pro&ticker=AAPL&interval=1m&page=0&page_size=30&adjust=all?apikey=" + fz_key


response = requests.get(url)
st.write(response.status_code)
st.write(response.json())

#API DOCS
#https://www.alphavantage.co/documentation/

# Time Series Monthly
#https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=IBM&apikey=demo
#https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=TSCO.LON&apikey=demo

symbol = st.text_input("Enter a stock code 👇")
if st.button("Check"):
  function = "GLOBAL_QUOTE"  
  # GLOBAL QUOTE QUERY
  url = "https://www.alphavantage.co/query?function=" + function + "&symbol=" + symbol +"&apikey=demo" 
  response = requests.get(url) 
  st.write(response.status_code)
  st.write(str(response.json()))
  st.write(response.json()['Global Quote']['05. price'])


# Assuming the JSON string is stored in a variable called 'json_data'
#json_data = '{"Global Quote": {"01. symbol": "IBM", "02. open": "168.2600", "03. high": "169.6300", "04. low": "167.7900", "05. price": "168.9700", "06. volume": "3492267", "07. latest trading day": "2024-05-16", "08. previous close": "168.2600", "09. change": "0.7100", "10. change percent": "0.4220%"}}'

# Convert the JSON string to a Python dictionary
#data_dict = json.loads(json_data)

# Access the price

  # Output: 168.
