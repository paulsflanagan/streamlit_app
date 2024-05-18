import requests
import streamlit as st
import json
import pandas as pd
from io import StringIO
from supabase import create_client, Client

td_key=st.secrets["td_key"]

# Quote Api
#quoteApiUrl = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo"

st.title("Stock Trading Game")

userName = st.experimental_user.email
st.write(userName)
spb_url = st.secrets["spb_url"]
spb_key = st.secrets["spb_key"]

supabase: Client = create_client(spb_url, spb_key)

account_details, pull_count = supabase.table('StockTradingGame_AccountsDB').select("*").eq('user_name', userName).execute()
#st.write(account_details)
if account_details[1] == []:
  st.write("Welcome to Stock Trading Game")
  data, push_count = supabase.table('StockTradingGame_AccountsDB').insert({"user_name": userName, "available_cash": 20000}).execute()
  availableCash = 20000
else:
  availableCash = account_details[1][0]['available_cash']
  
#st.write(account_details)
fee_percentage = 0.02


symbol = st.text_input("Enter a stock symbol 👇")
#if st.button("Check"):
if symbol:

  ### CASHE STOCK INFO TO DB? What is server time? Check last cashe vs server time > 1hour diff to determine if we re-submit api? (we only have 9 api calls per minute on free teir)
  
  url = "https://api.twelvedata.com/time_series?apikey="+ td_key +"&interval=1week&format=JSON&symbol=" + symbol
  #try:
  response = requests.get(url)
  #st.write(response.status_code)
  #st.write(response.json())
  try:
    chart_data = response.json()["values"]
  except:
    st.write("Error Pulling Data")
    break
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
  df = pd.DataFrame(list(zip(datetime_list, value_list)), columns =['Date-Time', 'Value'])#.sort_values(by='Value', ascending=True)
  df['Value'] = df['Value'].astype(float)
  
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
      user_stock_id = row['id']
      amount_owned_current_stock = row['stock_amount']
      cost_owned_current_stock = row['stock_cost']
      current_stock_difference = (int(amount_owned_current_stock) * float(currentValue)) - float(cost_owned_current_stock)
  
  available_cash_display = st.empty()

  if owns_current_stock:
    available_cash_display.write("Available Cash: $" + str(availableCash) + " - Currently Owned: " + str(amount_owned_current_stock) + " - Current Profit/Loss: " + str(round(current_stock_difference,2)))
  else:
    available_cash_display.write("Available Cash: $" + str(availableCash))
    
  amount = st.text_input("Enter an amount to purchase 👇")
  if amount:
    total_cost = float(amount) * float(currentValue)
    potential_fee = (float(amount) * float(currentValue)) * fee_percentage
    if potential_fee > 5.0:
      fee = 5.0
    else:
      fee = potential_fee
    total_cost_plus_fee = total_cost + fee
    st.write("Cost of purchase: $" + str(round(total_cost,2)) + " - Including Fee: " + str(round(fee, 2)))
    if float(total_cost) <= float(availableCash):
      if st.button("Buy Now"):
        if owns_current_stock:
          total_cost_plus_fee = total_cost_plus_fee + cost_owned_current_stock
          amount = int(amount) + int(amount_owned_current_stock)
          data, push_count = supabase.table('StockTradingGame_OwnedStocksDB').update({"stock_amount": amount, "stock_cost": total_cost_plus_fee}).eq("id", user_stock_id).execute()
        else:
          data, push_count = supabase.table('StockTradingGame_OwnedStocksDB').insert({"user_name": userName, "stock_symbol": symbol, "stock_amount": amount, "stock_cost": total_cost_plus_fee}).execute()
          
        newAvailableCash = float(availableCash) - float(total_cost_plus_fee)
        data, push_count = supabase.table('StockTradingGame_AccountsDB').update({"available_cash": newAvailableCash}).eq("user_name", userName).execute()
        
        account_details, pull_count = supabase.table('StockTradingGame_AccountsDB').select("*").eq('user_name', userName).execute()
        
        trade_details = supabase.table('StockTradingGame_OwnedStocksDB').select("*").eq('user_name', userName).execute()
        
        bank_account, pull_bank_count = supabase.table('StockTradingGame_BankDB').select("*").eq('bank_account', 'bank_account').execute()
        #st.write(bank_account)
        bank_account_cash = bank_account[1][0]['account_balance']
        bank_account_cash = bank_account_cash + round(fee,2)
        data, push_count = supabase.table('StockTradingGame_BankDB').update({"account_balance": bank_account_cash}).eq("bank_account", 'bank_account').execute()
  
        #extracted_stocks_list = []
        owns_current_stock = False
        amount_owned_current_stock = 0
        cost_owned_current_stock = 0
      
        for row in trade_details.data:
          current_stock = row['stock_symbol']
          if current_stock == symbol:
            owns_current_stock = True
            user_stock_id = row['id']
            amount_owned_current_stock = row['stock_amount']
            cost_owned_current_stock = row['stock_cost']
            current_stock_difference = (int(amount_owned_current_stock) * float(currentValue)) - float(cost_owned_current_stock)
            
        if pull_count == 0:
          st.write("No Account Found - Visit Account to Begin")
        else:
          availableCash = account_details[1][0]['available_cash']
          available_cash_display.write("Available Cash: $" + str(availableCash) + " - Currently Owned: " + str(amount_owned_current_stock) + " - Current Profit/Loss: " + str(round(current_stock_difference,2)))
        
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
