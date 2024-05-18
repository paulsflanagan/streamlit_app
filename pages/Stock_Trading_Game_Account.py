import requests
import streamlit as st
from supabase import create_client, Client
import json

td_key=st.secrets["td_key"]

st.title("Stock Trading Game - Account")

userName = st.experimental_user.email
st.write(userName)

spb_url = st.secrets["spb_url"]
spb_key = st.secrets["spb_key"]

availableCash = 0

supabase: Client = create_client(spb_url, spb_key)


account_details, pull_count = supabase.table('StockTradingGame_AccountsDB').select("*").eq('user_name', userName).execute()
st.write(account_details[1])

if account_details[1] == []:
  st.write("Welcome to Stock Trading Game " + userName)
  data, push_count = supabase.table('StockTradingGame_AccountsDB').insert({"user_name": userName, "available_cash": 20000}).execute()
  availableCash = 0
else:
  availableCash = account_details[1][0]['available_cash']
  trade_details = supabase.table('StockTradingGame_OwnedStocksDB').select("*").eq('user_name', userName).execute()
  st.subheader("Portfolio:")
  st.write("Available Cash: $" + str(availableCash))
  for row in trade_details.data:
      st.write("Stock: " + str(row['stock_symbol']) + " - Owned: " + str(row['stock_amount']) + " - Cost: " + str(row['stock_cost']))

  #extracted_stocks_list = []
  #current_stock = ""
  #current_stock_count = 0
  #current_stock_cost = 0
  
  #for row in trade_details.data:
  #  current_stock = row['stock_symbol']
  #  if current_stock not in extracted_stocks_list:
  #    extracted_stocks_list.append(row['stock_symbol'])
  #st.write(extracted_stocks_list)
  
  #for stock_symbol in extracted_stocks_list:
  #  for row in trade_details.data:
  #    if stock_symbol == row['stock_symbol']:
        
  
#st.write(account_details)
#st.write(trade_details)
