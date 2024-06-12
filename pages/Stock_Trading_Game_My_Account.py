import requests
import streamlit as st
from supabase import create_client, Client
import json
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
  
def getPrevDividend(userName):
  prev_dividend, pull_count = supabase.table('StockTradingGame_AccountsDB').select("prev_dividend").eq('user_name', userName).execute()
  return prev_dividend[1][0]['prev_dividend']


## Portfolio
def getPortfolio(userName):
   portfolio = supabase.table('StockTradingGame_OwnedStocksDB').select("*").eq('user_name', userName).execute()
   return portfolio

#def displayPortfolio(userName):
#  portfolio = getPortfolio(userName)
#  print("My Portfolio:")
#  for row in portfolio.data:
#    st.write("Stock: " + str(row['stock_symbol']) + " - Owned: " + str(row['stock_amount']) + " - Cost: " + str(row['stock_cost']))
    
def displayPortfolio(userName):
  portfolio = getPortfolio(userName)
  print("Portfolio:")
  for row in portfolio.data:
    valueAmount = int(row['stock_amount']) * float(getStockValue(row['stock_symbol']))
    valueDifference = valueAmount - float(row['stock_cost'])
    st.write("Stock: " + str(row['stock_symbol']) + " - Owned: " + str(row['stock_amount']) + " - Cost: " + str(row['stock_cost']) + " - Value: " + str(valueAmount)+ " - Difference: " + str(round(valueDifference,2)))


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





#### UI

st.title("Stock Trading Game - Account TEST123")
st.write(userName)


availableCash = getAvailableCash(userName)
prevDividend = getPrevDividend(userName)
  
st.subheader("Portfolio:")
st.write("Available Cash: $" + str(availableCash) + " Dividend: " + str(prevDividend))

displayPortfolio(userName)

