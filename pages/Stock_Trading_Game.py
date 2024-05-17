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
  st.write(response.json())
  st.write("Symbol: " + response.json()["meta"]["symbol"])
  st.write("Exchange: " + response.json()["meta"]["exchange"]) 
  st.write("Type: " + response.json()["meta"]["type"]) 
  st.write("Value (USD): " + response.json()["values"][0]["close"])
  #except:
   # st.write("Unable to find stock symbol")

# Assuming the JSON string is stored in a variable called 'json_data'
#json_data = '{"Global Quote": {"01. symbol": "IBM", "02. open": "168.2600", "03. high": "169.6300", "04. low": "167.7900", "05. price": "168.9700", "06. volume": "3492267", "07. latest trading day": "2024-05-16", "08. previous close": "168.2600", "09. change": "0.7100", "10. change percent": "0.4220%"}}'


data = """
{
"meta":{
"symbol":"IBM"
"interval":"1min"
"currency":"USD"
"exchange_timezone":"America/New_York"
"exchange":"NYSE"
"mic_code":"XNYS"
"type":"Common Stock"
}
"values":[
0:{
"datetime":"2024-05-17 13:16:00"
"open":"168.17990"
"high":"168.17990"
"low":"168.17990"
"close":"168.17990"
"volume":"0"
}
1:{
"datetime":"2024-05-17 13:15:00"
"open":"168.16901"
"high":"168.23000"
"low":"168.16901"
"close":"168.23000"
"volume":"3492"
}
2:{
"datetime":"2024-05-17 13:14:00"
"open":"168.17000"
"high":"168.17500"
"low":"168.17000"
"close":"168.17410"
"volume":"1581"
}
3:{
"datetime":"2024-05-17 13:13:00"
"open":"168.11000"
"high":"168.17500"
"low":"168.11000"
"close":"168.17500"
"volume":"1664"
}
4:{
"datetime":"2024-05-17 13:12:00"
"open":"168.06000"
"high":"168.10500"
"low":"168.06000"
"close":"168.08980"
"volume":"2055"
}
5:{
"datetime":"2024-05-17 13:11:00"
"open":"168.03999"
"high":"168.08600"
"low":"168.03999"
"close":"168.03999"
"volume":"3678"
}
6:{
"datetime":"2024-05-17 13:10:00"
"open":"168.02000"
"high":"168.02000"
"low":"168.00000"
"close":"168.00000"
"volume":"895"
}
7:{
"datetime":"2024-05-17 13:09:00"
"open":"167.95900"
"high":"168.02000"
"low":"167.95000"
"close":"168.00000"
"volume":"4021"
}
8:{
"datetime":"2024-05-17 13:08:00"
"open":"167.91000"
"high":"167.96960"
"low":"167.91000"
"close":"167.94000"
"volume":"4586"
}
9:{
"datetime":"2024-05-17 13:07:00"
"open":"167.91000"
"high":"167.94141"
"low":"167.91000"
"close":"167.94141"
"volume":"1630"
}
10:{
"datetime":"2024-05-17 13:06:00"
"open":"167.92999"
"high":"167.94901"
"low":"167.91000"
"close":"167.92000"
"volume":"2307"
}
11:{
"datetime":"2024-05-17 13:05:00"
"open":"167.89999"
"high":"167.91451"
"low":"167.89999"
"close":"167.91451"
"volume":"695"
}
12:{
"datetime":"2024-05-17 13:04:00"
"open":"167.94830"
"high":"167.95500"
"low":"167.92999"
"close":"167.92999"
"volume":"2254"
}
13:{
"datetime":"2024-05-17 13:03:00"
"open":"167.93500"
"high":"167.98000"
"low":"167.93500"
"close":"167.95000"
"volume":"2141"
}
14:{
"datetime":"2024-05-17 13:02:00"
"open":"167.92000"
"high":"167.94321"
"low":"167.91100"
"close":"167.92000"
"volume":"5060"
}
15:{
"datetime":"2024-05-17 13:01:00"
"open":"167.99001"
"high":"168.00500"
"low":"167.93500"
"close":"167.93500"
"volume":"5866"
}
16:{
"datetime":"2024-05-17 13:00:00"
"open":"167.94740"
"high":"167.98000"
"low":"167.94501"
"close":"167.94501"
"volume":"2764"
}
17:{
"datetime":"2024-05-17 12:57:00"
"open":"167.98010"
"high":"167.99001"
"low":"167.96001"
"close":"167.99001"
"volume":"3988"
}
18:{
"datetime":"2024-05-17 12:56:00"
"open":"167.99820"
"high":"168.00000"
"low":"167.99500"
"close":"168.00000"
"volume":"2255"
}
19:{
"datetime":"2024-05-17 12:55:00"
"open":"168.00000"
"high":"168.01120"
"low":"168.00000"
"close":"168.00000"
"volume":"1239"
}
20:{
"datetime":"2024-05-17 12:54:00"
"open":"168.00000"
"high":"168.00999"
"low":"167.99500"
"close":"168.00000"
"volume":"3008"
}
21:{
"datetime":"2024-05-17 12:53:00"
"open":"168.00999"
"high":"168.00999"
"low":"167.99001"
"close":"167.99001"
"volume":"2251"
}
22:{
"datetime":"2024-05-17 12:52:00"
"open":"167.98500"
"high":"168.02000"
"low":"167.98500"
"close":"168.02000"
"volume":"1111"
}
23:{
"datetime":"2024-05-17 12:51:00"
"open":"167.95000"
"high":"168.00000"
"low":"167.94991"
"close":"168.00000"
"volume":"3226"
}
24:{
"datetime":"2024-05-17 12:50:00"
"open":"167.98000"
"high":"167.98289"
"low":"167.98000"
"close":"167.98289"
"volume":"1666"
}
25:{
"datetime":"2024-05-17 12:49:00"
"open":"167.96750"
"high":"167.97000"
"low":"167.94000"
"close":"167.94000"
"volume":"1303"
}
26:{
"datetime":"2024-05-17 12:48:00"
"open":"167.93520"
"high":"167.98000"
"low":"167.93520"
"close":"167.98000"
"volume":"2155"
}
27:{
"datetime":"2024-05-17 12:47:00"
"open":"167.92999"
"high":"167.96001"
"low":"167.92999"
"close":"167.95500"
"volume":"2541"
}
28:{
"datetime":"2024-05-17 12:46:00"
"open":"167.86000"
"high":"167.87000"
"low":"167.86000"
"close":"167.87000"
"volume":"2055"
}
29:{
"datetime":"2024-05-17 12:45:00"
"open":"167.87000"
"high":"167.88000"
"low":"167.81000"
"close":"167.88000"
"volume":"3526"
}
]
"status":"ok"
}
"""
jason_data = json.loads(data)
chart_data = data.json()["values"]

st.write(chart_data)

# Convert the JSON string to a Python dictionary
#data_dict = json.loads(json_data)

# Access the price

  # Output: 168.
