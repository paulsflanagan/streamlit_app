import requests
import streamlit as st
import json
import pandas as pd
from io import StringIO

td_key=st.secrets["td_key"]

# Quote Api
#quoteApiUrl = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo"


#url = "https://api.finazon.io/latest/time_series?apikey=" + fz_key

st.title("Stock Trading Game")

symbol = st.text_input("Enter a stock symbol 👇")
if st.button("Check"):
  
  url = "https://api.twelvedata.com/time_series?apikey="+ td_key +"&interval=1min&format=JSON&symbol=" + symbol
  #try:
  response = requests.get(url)
  #st.write(response.status_code)
  #st.write(response.json())
  st.write("Symbol: " + response.json()["meta"]["symbol"])
  st.write("Exchange: " + response.json()["meta"]["exchange"]) 
  st.write("Type: " + response.json()["meta"]["type"]) 
  st.write("Value (USD): " + response.json()["values"][0]["close"])
  chart_data = response.json()["values"]
  #df = pd.read_json(chart_data)
  #df = pd.read_json(str(chart_data))
  #st.write(df)

  ### FOR EACH IN VALUES

  for row in chart_data:
    st.write("DateTime): " + row['datetime'])
    st.write("Value (USD): " + row['close'])
    #take the date / time for x
    #and Close price for Y

  
  st.line_chart(data=chart_data)
  #st.write(chart_data)
  #except:
   # st.write("Unable to find stock symbol")

# Assuming the JSON string is stored in a variable called 'json_data'
#json_data = '{"Global Quote": {"01. symbol": "IBM", "02. open": "168.2600", "03. high": "169.6300", "04. low": "167.7900", "05. price": "168.9700", "06. volume": "3492267", "07. latest trading day": "2024-05-16", "08. previous close": "168.2600", "09. change": "0.7100", "10. change percent": "0.4220%"}}'






# Convert the JSON string to a Python dictionary
#data_dict = json.loads(json_data)

# Access the price

  # Output: 168.
