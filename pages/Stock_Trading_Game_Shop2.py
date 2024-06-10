import requests
import streamlit as st
import json
import pandas as pd
from io import StringIO
from supabase import create_client, Client
from datetime import datetime

#### Import Keys
td_key=st.secrets["td_key"]
userName = st.experimental_user.email
spb_url = st.secrets["spb_url"]
spb_key = st.secrets["spb_key"]

#### Build Clients
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
  
def setAvailableCash(userName,cash):
  data, push_count = supabase.table('StockTradingGame_AccountsDB').update({"available_cash": cash}).eq("user_name", userName).execute()
  return 'Cash updated'

## Portfolio
def getPortfolio(userName):
   portfolio = supabase.table('StockTradingGame_OwnedStocksDB').select("*").eq('user_name', userName).execute()
   return portfolio

def displayPortfolio(userName):
  portfolio = getPortfolio(userName)
  print("Portfolio:")
  for row in portfolio.data:
    print("Stock: " + str(row['stock_symbol']) + " - Owned: " + str(row['stock_amount']) + " - Cost: " + str(row['stock_cost']))

def getOwnedStock(userName,symbol):
  ownedStock = supabase.table('StockTradingGame_OwnedStocksDB').select("*").eq('user_name', userName).eq('stock_symbol', symbol).execute()
  if ownedStock.data == []:
    return []
  else:
    return ownedStock.data[0]

## Logging
def logTrade(userName,symbol,tradeType,amount,value,fee):
  data, push_count = supabase.table('StockTradingGame_TradeLogDB').insert({"user_name": userName, "stock_symbol": symbol, "trade_type": tradeType, "stock_amount": amount, "stock_cost": value, "bank_fee": fee}).execute()

## Bank
def getBankFunds():
  bank_account, pull_bank_count = supabase.table('StockTradingGame_BankDB').select("*").eq('bank_account', 'bank_account').execute()
  return bank_account[1][0]['account_balance']

def addBankFunds(amount):
  updateFunds = getBankFunds() + amount
  supabase.table('StockTradingGame_BankDB').update({"account_balance": updateFunds}).eq("bank_account", 'bank_account').execute()
  return 'Updated Bank Funds'
  
def getFee(amount,value):
  feePercentage = 0.002
  fee = (amount * value) * feePercentage
  return fee

## Purchase Stock
def setPurchasedStock(userName,symbol,amount,value):
  fee = getFee(amount,value)
  transactionValue = (amount * value) + fee
  availableCash = getAvailableCash(userName)
  if getAvailableCash(userName) < transactionValue:
    return 'Insufficient Funds'
  ownedStock = getOwnedStock(userName,symbol)
  if ownedStock == []:
    data, push_count = supabase.table('StockTradingGame_OwnedStocksDB').insert({"user_name": userName, "stock_symbol": symbol, "stock_amount": amount, "stock_cost": transactionValue}).execute()
  else:
    updateAmount = ownedStock['stock_amount'] + amount
    updateCost = ownedStock['stock_cost'] + transactionValue
    data, push_count = supabase.table('StockTradingGame_OwnedStocksDB').update({"stock_amount": updateAmount, "stock_cost": updateCost}).eq("user_name", userName).eq("stock_symbol", symbol).execute()
  # Log Trade
  logTrade(userName,symbol,"Buy",amount,value,fee)
  # Update Cash
  updateAvailableCash = availableCash - transactionValue
  setAvailableCash(userName,updateAvailableCash)
  # Update Bank Funds
  addBankFunds(fee)
  return 'Stock purchased'
    
## Sell Stock
def setSellStock(userName,symbol,amount,value):
  fee = getFee(amount,value)
  transactionValue = (amount * value) - fee
  ownedStock = getOwnedStock(userName,symbol)
  if ownedStock == []:
    return 'Unable to sell. Stock Not owned.'
  costPerItem = ownedStock['stock_cost'] / ownedStock['stock_amount']
  updateAmount = ownedStock['stock_amount'] - amount
  if updateAmount < 0:
    return 'Unable to sell. Selling more that held stock.'
  if updateAmount == 0:
    data, count = supabase.table('StockTradingGame_OwnedStocksDB').delete().eq("user_name", userName).eq("stock_symbol", symbol).execute()
  else:
    updateCost = costPerItem * updateAmount
    data, push_count = supabase.table('StockTradingGame_OwnedStocksDB').update({"stock_amount": updateAmount, "stock_cost": updateCost}).eq("user_name", userName).eq("stock_symbol", symbol).execute()
  # Log Trade
  logTrade(userName,symbol,"Sell",amount,value,fee)
  # Update Cash
  availableCash = getAvailableCash(userName)
  updateAvailableCash = availableCash + transactionValue
  setAvailableCash(userName,updateAvailableCash) 
  # Update Bank Funds
  addBankFunds(fee)
  return 'Stock Sold.'

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
st.title("Stock Trading Game 2")
st.write(userName)


account_details = getAccountDetails(userName)
availableCash = account_details['available_cash']
availableCashStr = str(account_details['available_cash'])

st.write("Available Cash: $" + availableCashStr)

symbol = st.text_input("Enter a stock symbol 👇")
#if st.button("Check"):
if symbol:

  
  response = getStockData(symbol)
  #st.write(response.status_code)
  #st.write(response.json())
  st.write(chart_data)
  chart_data = response.json()["values"]

  st.write(response)

  #df = pd.read_json(chart_data)
  #df = pd.read_json(str(chart_data))
  #st.write(df)

  ### FOR EACH IN VALUES
#  datetime_list = []
#  value_list = []
#  for row in chart_data:
    #st.write("DateTime): " + row['datetime'])
#    datetime_list.append(row['datetime'])
    #st.write("Value (USD): " + row['close'])
#    value_list.append(row['close'])
    #take the date / time for x
    #and Close price for Y
#  df = pd.DataFrame(list(zip(datetime_list, value_list)), columns =['Date-Time', 'Value'])#.sort_values(by='Value', ascending=True)
#  df['Value'] = df['Value'].astype(float)





