import requests
import streamlit as st
import json
import pandas as pd

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
  st.write(response.status_code)
  #st.write(response.json())
  st.write("Symbol: " + response.json()["meta"]["symbol"])
  st.write("Exchange: " + response.json()["meta"]["exchange"]) 
  st.write("Type: " + response.json()["meta"]["type"]) 
  st.write("Value (USD): " + response.json()["values"][0]["close"])
  #except:
   # st.write("Unable to find stock symbol")

# Assuming the JSON string is stored in a variable called 'json_data'
#json_data = '{"Global Quote": {"01. symbol": "IBM", "02. open": "168.2600", "03. high": "169.6300", "04. low": "167.7900", "05. price": "168.9700", "06. volume": "3492267", "07. latest trading day": "2024-05-16", "08. previous close": "168.2600", "09. change": "0.7100", "10. change percent": "0.4220%"}}'


data = { "meta":{ "symbol":"IBM" "interval":"1min" "currency":"USD" "exchange_timezone":"America/New_York" "exchange":"NYSE" "mic_code":"XNYS" "type":"Common Stock" } "values":[ 0:{ "datetime":"2024-05-17 12:56:00" "open":"167.99820" "high":"168.00000" "low":"167.99500" "close":"168.00000" "volume":"2255" } 1:{ "datetime":"2024-05-17 12:55:00" "open":"168.00000" "high":"168.01120" "low":"168.00000" "close":"168.00000" "volume":"1239" } 2:{ "datetime":"2024-05-17 12:54:00" "open":"168.00000" "high":"168.00999" "low":"167.99500" "close":"168.00000" "volume":"3008" } 3:{ "datetime":"2024-05-17 12:53:00" "open":"168.00999" "high":"168.00999" "low":"167.99001" "close":"167.99001" "volume":"2251" } 4:{ "datetime":"2024-05-17 12:52:00" "open":"167.98500" "high":"168.02000" "low":"167.98500" "close":"168.02000" "volume":"1111" } 5:{ "datetime":"2024-05-17 12:51:00" "open":"167.95000" "high":"168.00000" "low":"167.94991" "close":"168.00000" "volume":"3226" } 6:{ "datetime":"2024-05-17 12:50:00" "open":"167.98000" "high":"167.98289" "low":"167.98000" "close":"167.98289" "volume":"1666" } 7:{ "datetime":"2024-05-17 12:49:00" "open":"167.96750" "high":"167.97000" "low":"167.94000" "close":"167.94000" "volume":"1303" } 8:{ "datetime":"2024-05-17 12:48:00" "open":"167.93520" "high":"167.98000" "low":"167.93520" "close":"167.98000" "volume":"2155" } 9:{ "datetime":"2024-05-17 12:47:00" "open":"167.92999" "high":"167.96001" "low":"167.92999" "close":"167.95500" "volume":"2541" } 10:{ "datetime":"2024-05-17 12:46:00" "open":"167.86000" "high":"167.87000" "low":"167.86000" "close":"167.87000" "volume":"2055" } 11:{ "datetime":"2024-05-17 12:45:00" "open":"167.87000" "high":"167.88000" "low":"167.81000" "close":"167.88000" "volume":"3526" } 12:{ "datetime":"2024-05-17 12:44:00" "open":"167.89000" "high":"167.89500" "low":"167.89000" "close":"167.89500" "volume":"929" } 13:{ "datetime":"2024-05-17 12:43:00" "open":"167.95000" "high":"167.95000" "low":"167.89999" "close":"167.89999" "volume":"3202" } 14:{ "datetime":"2024-05-17 12:42:00" "open":"167.95500" "high":"167.95500" "low":"167.92999" "close":"167.94000" "volume":"2491" } 15:{ "datetime":"2024-05-17 12:41:00" "open":"167.95000" "high":"167.97000" "low":"167.92999" "close":"167.97000" "volume":"2259" } 16:{ "datetime":"2024-05-17 12:40:00" "open":"168.03999" "high":"168.03999" "low":"167.96001" "close":"167.97501" "volume":"2474" } 17:{ "datetime":"2024-05-17 12:39:00" "open":"168.00000" "high":"168.05000" "low":"168.00000" "close":"168.05000" "volume":"4838" } 18:{ "datetime":"2024-05-17 12:38:00" "open":"168.00850" "high":"168.00850" "low":"168.00000" "close":"168.00000" "volume":"749" } 19:{ "datetime":"2024-05-17 12:37:00" "open":"168.03000" "high":"168.03999" "low":"168.00999" "close":"168.03999" "volume":"2221" } 20:{ "datetime":"2024-05-17 12:36:00" "open":"168.04500" "high":"168.06000" "low":"168.04500" "close":"168.06000" "volume":"2093" } 21:{ "datetime":"2024-05-17 12:35:00" "open":"168.05000" "high":"168.05000" "low":"168.03999" "close":"168.03999" "volume":"678" } 22:{ "datetime":"2024-05-17 12:34:00" "open":"168.03999" "high":"168.03999" "low":"168.03999" "close":"168.03999" "volume":"1080" } 23:{ "datetime":"2024-05-17 12:33:00" "open":"168.00999" "high":"168.00999" "low":"168.00999" "close":"168.00999" "volume":"3542" } 24:{ "datetime":"2024-05-17 12:30:00" "open":"168.00999" "high":"168.01500" "low":"167.98000" "close":"167.99001" "volume":"4341" } 25:{ "datetime":"2024-05-17 12:29:00" "open":"168.00000" "high":"168.01500" "low":"168.00000" "close":"168.01500" "volume":"1377" } 26:{ "datetime":"2024-05-17 12:27:00" "open":"168.00500" "high":"168.00500" "low":"167.98000" "close":"167.98000" "volume":"1843" } 27:{ "datetime":"2024-05-17 12:26:00" "open":"167.99001" "high":"168.02100" "low":"167.99001" "close":"168.02100" "volume":"1982" } 28:{ "datetime":"2024-05-17 12:25:00" "open":"168.00000" "high":"168.00000" "low":"168.00000" "close":"168.00000" "volume":"1262" } 29:{ "datetime":"2024-05-17 12:24:00" "open":"168.00999" "high":"168.00999" "low":"168.00999" "close":"168.00999" "volume":"1478" } ] "status":"ok" }

chart_data = data["values"]

st.write(chart_data)

# Convert the JSON string to a Python dictionary
#data_dict = json.loads(json_data)

# Access the price

  # Output: 168.
