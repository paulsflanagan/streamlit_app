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

st.title("Stock Trading Game - Player Statistics")
st.write(userName)

st.subheader("Statistics:")
st.write("Top Player Owned Stocks:")
topOwnedStocks = getOrderdTotalOwnedStocks()
for each in topOwnedStocks:
  st.write("Stock: " + each[0] + " - Owned: " + str(each[1]))
