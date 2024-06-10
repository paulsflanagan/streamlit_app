import requests
import streamlit as st
from supabase import create_client, Client
import json

#### Keys
td_key=st.secrets["td_key"]
userName = st.experimental_user.email

spb_url = st.secrets["spb_url"]
spb_key = st.secrets["spb_key"]

#### Clients
supabase: Client = create_client(spb_url, spb_key)


#### Functions

### DataBase Functions

## Initialize Account
def initialiseAccount(userName):
  account_details, push_count = supabase.table('StockTradingGame_AccountsDB').insert({"user_name": userName, "available_cash": 20000}).execute()
  return account_details

## Account Details
def getAccountDetails(userName):
  account_details, pull_count = supabase.table('StockTradingGame_AccountsDB').select("*").eq('user_name', userName).execute()
  if account_details[1] == []:
    initialiseAccount(userName)
    account_details, pull_count = supabase.table('StockTradingGame_AccountsDB').select("*").eq('user_name', userName).execute()
  return account_details[1][0]

def getAvailableCash(userName):
  account_details = getAccountDetails(userName)
  return account_details['available_cash']


#### UI

st.title("Stock Trading Game - Account2")
st.write(userName)


availableCash = getAvailableCash(userName)
  
st.subheader("Portfolio:")
st.write("Available Cash: $" + str(availableCash))



for row in trade_details.data:
    st.write("Stock: " + str(row['stock_symbol']) + " - Owned: " + str(row['stock_amount']) + " - Cost: " + str(row['stock_cost']))
