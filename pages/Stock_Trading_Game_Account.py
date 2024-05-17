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
stockOwned = []

supabase: Client = create_client(spb_url, spb_key)


account_details, pull_count = supabase.table('StockTradingGame_AccountsDB').select("*").eq('user_name', userName).execute()
st.write(account_details)
if pull_count == 0:
  data, push_count = supabase.table('StockTradingGame_AccountsDB').insert({"user_name": userName, "available_cash": 20000, "stock_owned": "[]"}).execute()
  availableCash = 0
  stockOwned = []
else:
  availableCash = account_details['data']['available_cash']
  stockOwned = account_details['data']['stock_owned']
  
st.write(account_details)
st.write(availableCash)
st.write(stockOwned)
