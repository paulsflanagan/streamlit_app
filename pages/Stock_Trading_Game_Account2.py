import requests
import streamlit as st
from supabase import create_client, Client
import json
from collections import Counter

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

## Portfolio
def getPortfolio(userName):
   portfolio = supabase.table('StockTradingGame_OwnedStocksDB').select("*").eq('user_name', userName).execute()
   return portfolio

def displayPortfolio(userName):
  portfolio = getPortfolio(userName)
  print("Portfolio:")
  for row in portfolio.data:
    st.write("Stock: " + str(row['stock_symbol']) + " - Owned: " + str(row['stock_amount']) + " - Cost: " + str(row['stock_cost']))

#### Showcase Functions
def getTotalOwnedStocks():
  trades_data = supabase.table('StockTradingGame_OwnedStocksDB').select("*").execute()
  total_owned_data = {}
  for each in trades_data.data:
    stock_symbol = each['stock_symbol']
    stock_amount = each['stock_amount']
    if total_owned_data.get(stock_symbol) == None:
      total_owned_data[stock_symbol] = stock_amount
    else:
      buffer_amount = total_owned_data[stock_symbol] + stock_amount
      total_owned_data[stock_symbol] = buffer_amount
  return total_owned_data

def getOrderdTotalOwnedStocks():
  total_owned_data = getTotalOwnedStocks()
  c = Counter(total_owned_data)
  ordered_total_owned_data = c.most_common()
  return ordered_total_owned_data



#### UI

st.title("Stock Trading Game - Account2")
st.write(userName)


availableCash = getAvailableCash(userName)
  
st.subheader("Portfolio:")
st.write("Available Cash: $" + str(availableCash))

displayPortfolio(userName)

st.subheader("Statistics:")
st.write("Top Player Owned Stocks:")
topOwnedStocks = getOrderdTotalOwnedStocks()
for each in topOwnedStocks:
  st.write("Stock: " + each[0] + " - Owned: " + str(each[1]))

