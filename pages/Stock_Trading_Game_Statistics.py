import requests
import streamlit as st
from supabase import create_client, Client
import json
from collections import Counter
from datetime import datetime

#### Keys
td_key=st.secrets["td_key"]
userName = st.experimental_user.email

spb_url = st.secrets["spb_url"]
spb_key = st.secrets["spb_key"]

#### Clients
supabase: Client = create_client(spb_url, spb_key)


#### Functions

### DataBase Functions

## Portfolio
def getPortfolio(userName):
   portfolio = supabase.table('StockTradingGame_OwnedStocksDB').select("*").eq('user_name', userName).execute()
   return portfolio


### Stock Data Functions
def getLiveStockData(symbol):
  url = "https://api.twelvedata.com/time_series?apikey="+ td_key +"&interval=1day&format=JSON&symbol=" + symbol
  response = requests.get(url)
  return response

def setLocalStockData(symbol, response):
  data, push_count = supabase.table('StockTradingGame_StockDataDB').insert({"stock_symbol": symbol, "stock_data": response}).execute()

def removeLocalStockData(symbol):
    data, count = supabase.table('StockTradingGame_StockDataDB').delete().eq("stock_symbol", symbol).execute()

def getLocalStockData(symbol):
  stock_data = supabase.table('StockTradingGame_StockDataDB').select("*").eq('stock_symbol', symbol).execute()
  if stock_data.data == []:
    return []
  else:
    return stock_data.data[0]

def validLocalStockData(symbol):
  current_dateTime = datetime.now()
  currentDate = current_dateTime.strftime('%Y-%m-%d')
  stockData = getLocalStockData(symbol)
  if stockData == []:
    return False
  if currentDate == stockData['created_at'][:10]:
    return True
  else:
    return False

def updateLocalStockData(symbol):
  response = getLiveStockData(symbol)
  setLocalStockData(symbol, response.json())
  return 'Updated Local Stock Data'


def getStockData(symbol):
  if not validLocalStockData(symbol):
    removeLocalStockData(symbol)
    updateLocalStockData(symbol)
  return getLocalStockData(symbol)

def getStockValue(symbol):
  response = getStockData(symbol)
  try:
    return response['stock_data']['values'][0]['close']
  except:
    return 'Invalid Stock Symbol'

#### Showcase Functions

def getTotalOwnedStocksStatistic():
  total_owned_stock, pull_count = supabase.table('StockTradingGame_StatisticsDB').select("total_owned_stock").execute()
  return total_owned_stock[1][0]['total_owned_stock']

def getHighestValuePlayer():
  account_details = supabase.table('StockTradingGame_AccountsDB').select("*").execute()
  total_value_player = {}
  for each in account_details.data:
    user_name = each['user_name']
    available_cash = each['available_cash']
    portfolio = getPortfolio(user_name)
    for stock in portfolio.data:
      stock_symbol = stock['stock_symbol']
      amount_owned = stock['stock_amount']
      stock_value = getStockValue(stock_symbol)
      value_owned = int(amount_owned) * float(stock_value)
      available_cash = available_cash + value_owned
    total_value_player[user_name] = round(available_cash,2)
  return total_value_player

def getOrderdHighestValuePlayer():
  total_value_player = getHighestValuePlayer()
  c = Counter(total_value_player)
  ordered_total_value_player = c.most_common()
  return ordered_total_value_player

#### UI

st.title("Stock Trading Game - Player Statistics")
st.write(userName)

st.subheader("Statistics:")
topOwnedStocks = getTotalOwnedStocksStatistic()
st.write("Top Player Owned Stocks " + topOwnedStocks)

st.write("Top Value Player:")
topValuePlayer = getOrderdHighestValuePlayer()
for each in topValuePlayer:
  st.write("Player: " + each[0] + " - Value: " + str(each[1]))
