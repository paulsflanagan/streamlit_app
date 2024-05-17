import requests
import streamlit as st
import json
import pandas as pd
from io import StringIO
from supabase import create_client, Client

td_key=st.secrets["td_key"]

# Quote Api
#quoteApiUrl = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo"

userName = st.experimental_user.email
spb_url = st.secrets["spb_url"]
spb_key = st.secrets["spb_key"]

supabase: Client = create_client(spb_url, spb_key)

account_details, pull_count = supabase.table('StockTradingGame_AccountsDB').select("*").eq('user_name', userName).execute()
#st.write(account_details)
if pull_count == 0:
  st.write("No Account Found - Visit Account to Begin")
else:
  availableCash = account_details[1][0]['available_cash']
  
#st.write(account_details)

st.title("Stock Trading Game")

symbol = st.text_input("Enter a stock symbol 👇")
#if st.button("Check"):
if symbol:
  
  url = "https://api.twelvedata.com/time_series?apikey="+ td_key +"&interval=1week&format=JSON&symbol=" + symbol
  #try:
  response = requests.get(url)
  #st.write(response.status_code)
  #st.write(response.json())

  chart_data = response.json()["values"]
  #df = pd.read_json(chart_data)
  #df = pd.read_json(str(chart_data))
  #st.write(df)

  ### FOR EACH IN VALUES
  datetime_list = []
  value_list = []
  for row in chart_data:
    #st.write("DateTime): " + row['datetime'])
    datetime_list.append(row['datetime'])
    #st.write("Value (USD): " + row['close'])
    value_list.append(row['close'])
    #take the date / time for x
    #and Close price for Y
  df = pd.DataFrame(list(zip(datetime_list, value_list)), columns =['Date-Time', 'Value'])
  
  #st.write(df)

  currentValue = response.json()["values"][0]["close"]
  st.write("") 
  st.subheader("Symbol: " + symbol)
  st.write("Current Value (USD): $" + currentValue + " Exchange: " + response.json()["meta"]["exchange"] + " Type: " + response.json()["meta"]["type"]) 
  #st.write("") 
  st.line_chart(data=df, x="Date-Time", y="Value")
  st.subheader("Purchase")

  trade_details = supabase.table('StockTradingGame_OwnedStocksDB').select("*").eq('user_name', userName).execute()
  
  #extracted_stocks_list = []
  owns_current_stock = False
  amount_owned_current_stock = 0
  cost_owned_current_stock = 0

  for row in trade_details.data:
    current_stock = row['stock_symbol']
    if current_stock == symbol:
      owns_current_stock = True
      amount_owned_current_stock = row['stock_amount']
      cost_owned_current_stock = row['stock_cost']
  
  available_cash_display = st.empty()

  if owns_current_stock:
    available_cash_display.write("Available Cash: $" + str(availableCash) + " Currently Owned: " + str(amount_owned_current_stock))
  else:
    available_cash_display.write("Available Cash: $" + str(availableCash))
    
  amount = st.text_input("Enter an amount to purchase 👇")
  if amount:
    total_cost = float(amount) * float(currentValue)
    st.write(total_cost)
    if float(total_cost) <= float(availableCash):
      if st.button("Buy Now"):
        if owns_current_stock:
          total_cost = total_cost + cost_owned_current_stock
          amount = int(amount) + int(amount_owned_current_stock)
          data, push_count = supabase.table('StockTradingGame_OwnedStocksDB').update({"stock_amount": amount, "stock_cost": total_cost}).eq("user_name", userName).execute()
        else:
          data, push_count = supabase.table('StockTradingGame_OwnedStocksDB').insert({"user_name": userName, "stock_symbol": symbol, "stock_amount": amount, "stock_cost": total_cost}).execute()
        newAvailableCash = float(availableCash) - float(total_cost)
        data, push_count = supabase.table('StockTradingGame_AccountsDB').update({"available_cash": newAvailableCash}).eq("user_name", userName).execute()
        account_details, pull_count = supabase.table('StockTradingGame_AccountsDB').select("*").eq('user_name', userName).execute()
        if pull_count == 0:
          st.write("No Account Found - Visit Account to Begin")
        else:
          availableCash = account_details[1][0]['available_cash']
          available_cash_display.write("Available Cash: $" + str(availableCash))
        
    else:
      st.write("Insufficient Funds")
  #st.write(chart_data)
  #except:
   # st.write("Unable to find stock symbol")

# Assuming the JSON string is stored in a variable called 'json_data'
#json_data = '{"Global Quote": {"01. symbol": "IBM", "02. open": "168.2600", "03. high": "169.6300", "04. low": "167.7900", "05. price": "168.9700", "06. volume": "3492267", "07. latest trading day": "2024-05-16", "08. previous close": "168.2600", "09. change": "0.7100", "10. change percent": "0.4220%"}}'






# Convert the JSON string to a Python dictionary
#data_dict = json.loads(json_data)

# Access the price

  # Output: 168.
