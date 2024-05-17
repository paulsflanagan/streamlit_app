import requests
import streamlit as st
from supabase import create_client, Client
import json

td_key=st.secrets["td_key"]

st.title("Stock Trading Game - Account")

userName = st.experimental_user.email
spb_url = st.secrets["spb_url"]
spb_key = st.secrets["spb_key"]

availableCash = 0

supabase: Client = create_client(spb_url, spb_key)


account_details, pull_count = supabase.table('StockTradingGame_AccountsDB').select("*").eq('user_name', userName).execute()
#st.write(account_details)
if pull_count == 0:
  st.write("Welcome to Stock Trading Game " + "")
  data, push_count = supabase.table('StockTradingGame_AccountsDB').insert({"user_name": userName, "available_cash": 20000}).execute()
  availableCash = 0
else:
  availableCash = account_details[1][0]['available_cash']
  trade_details, pull_count = supabase.table('StockTradingGame_OwnedStocksDB').select("*").eq('user_name', userName).execute()
  completed_stocks_list = []
  current_stock = ""
  for row in trade_details.data:
    current_stock = row['stock_symbol']
    if current_stock not in completed_stocks_list:
      completed_stocks_list.append(row['stock_symbol'])
  st.write(completed_stocks_list)
  
#st.write(account_details)
st.write(availableCash)
st.write(trade_details)
