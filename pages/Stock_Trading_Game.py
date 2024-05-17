import requests
import streamlit as st
import json

td_key=st.secrets["td_key"]

# Quote Api
#quoteApiUrl = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo"


#url = "https://api.finazon.io/latest/time_series?apikey=" + fz_key


symbol = st.text_input("Enter a stock symbol 👇")
if st.button("Check"):
  
  url = "https://api.twelvedata.com/time_series?apikey="+ td_key +"&interval=1min&format=JSON&symbol=" + symbol
  
  response = requests.get(url)
  st.write(response.status_code)
  st.write(response.json())


# Assuming the JSON string is stored in a variable called 'json_data'
#json_data = '{"Global Quote": {"01. symbol": "IBM", "02. open": "168.2600", "03. high": "169.6300", "04. low": "167.7900", "05. price": "168.9700", "06. volume": "3492267", "07. latest trading day": "2024-05-16", "08. previous close": "168.2600", "09. change": "0.7100", "10. change percent": "0.4220%"}}'

# Convert the JSON string to a Python dictionary
#data_dict = json.loads(json_data)

# Access the price

  # Output: 168.
