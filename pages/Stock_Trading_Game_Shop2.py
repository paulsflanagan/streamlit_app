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
  fee = (int(amount) * float(value)) * feePercentage
  return fee

## Purchase Stock
def setPurchasedStock(userName,symbol,amount,value):
  fee = getFee(amount,value)
  transactionValue = (int(amount) * float(value)) + fee
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
  
  symbol = symbol.upper()
  stockData = getStockData(symbol)
  currentValue = stockData["stock_data"]["values"][0]["close"]
  #st.write(stockData)
  stockExchange = stockData["stock_data"]["meta"]["exchange"]
  stockType = stockData["stock_data"]["meta"]["type"]
  chartData = stockData["stock_data"]["values"]

  # Prepare Chart Data
  datetime_list = []
  value_list = []
  for row in chartData:
    #st.write("DateTime): " + row['datetime'])
    datetime_list.append(row['datetime'])
    #st.write("Value (USD): " + row['close'])
    value_list.append(row['close'])
    #take the date / time for x
    #and Close price for Y
  df = pd.DataFrame(list(zip(datetime_list, value_list)), columns =['Date-Time', 'Value'])#.sort_values(by='Value', ascending=True)
  df['Value'] = df['Value'].astype(float)

  st.write("") 
  st.subheader("Symbol: " + symbol)
  st.write("Current Value (USD): $" + currentValue + " Exchange: " + stockExchange + " Type: " + stockType) 
  #st.write("") 
  st.line_chart(data=df, x="Date-Time", y="Value")
  st.subheader("Purchase")


  #### Display Available Cash and Currently Owned Stock
  
  ownedStock = getOwnedStock(userName,symbol)

  available_cash_display = st.empty()
  
  if ownedStock == []:
    available_cash_display.write("Available Cash: $" + str(availableCash))
  else:
    ownedStockAmount = ownedStock['stock_amount']
    ownedStockCost = ownedStock['stock_cost']
    ownedStockValueDifference = (int(ownedStockAmount) * float(currentValue)) - float(ownedStockCost)
    available_cash_display.write("Available Cash: $" + str(availableCash) + " - Currently Owned: " + str(ownedStockAmount) + " - Current Profit/Loss: " + str(round(ownedStockValueDifference,2)))


  #### Purchase Stocks
  
  amount = st.text_input("Enter an amount to purchase 👇")
  if amount:

    purchaseFee = getFee(int(amount),float(currentValue))
    purchaseCost = (float(amount) * float(currentValue)) + purchaseFee #@@ This could Be A Function

    st.write("Cost of purchase: $" + str(round(purchaseCost,2)) + " - Including Fee: " + str(round(purchaseFee, 2)))
  

    if float(purchaseCost) <= float(availableCash):
      
      if st.button("Buy Now"):
        setPurchasedStock(userName,symbol,amount,currentValue)
        
        ownedStock = getOwnedStock(userName,symbol)

        available_cash_display = st.empty()
        
        if ownedStock == []:
          available_cash_display.write("Available Cash: $" + str(availableCash))
        else:
          ownedStockAmount = ownedStock['stock_amount']
          ownedStockCost = ownedStock['stock_cost']
          ownedStockValueDifference = (int(ownedStockAmount) * float(currentValue)) - float(ownedStockCost)
          available_cash_display.write("Available Cash: $" + str(availableCash) + " - Currently Owned: " + str(ownedStockAmount) + " - Current Profit/Loss: " + str(round(ownedStockValueDifference,2)))
        
    else:
      st.write("Insufficient Funds")        
          #if owns_current_stock:
              #total_cost_plus_fee = total_cost_plus_fee + cost_owned_current_stock
              #amount = int(amount) + int(amount_owned_current_stock)
              #data, push_count = supabase.table('StockTradingGame_OwnedStocksDB').update({"stock_amount": amount, "stock_cost": total_cost_plus_fee}).eq("id", user_stock_id).execute()
            #else:
              #data, push_count = supabase.table('StockTradingGame_OwnedStocksDB').insert({"user_name": userName, "stock_symbol": symbol, "stock_amount": amount, "stock_cost": total_cost_plus_fee}).execute()
              
            #newAvailableCash = float(availableCash) - float(total_cost_plus_fee)
            #data, push_count = supabase.table('StockTradingGame_AccountsDB').update({"available_cash": newAvailableCash}).eq("user_name", userName).execute()
            
            #account_details, pull_count = supabase.table('StockTradingGame_AccountsDB').select("*").eq('user_name', userName).execute()
            
            #trade_details = supabase.table('StockTradingGame_OwnedStocksDB').select("*").eq('user_name', userName).execute()
            
            #bank_account, pull_bank_count = supabase.table('StockTradingGame_BankDB').select("*").eq('bank_account', 'bank_account').execute()
            #st.write(bank_account)
            #bank_account_cash = bank_account[1][0]['account_balance']
            #bank_account_cash = bank_account_cash + round(fee,2)
            #data, push_count = supabase.table('StockTradingGame_BankDB').update({"account_balance": bank_account_cash}).eq("bank_account", 'bank_account').execute()
      
            #extracted_stocks_list = []
            #owns_current_stock = False
            #amount_owned_current_stock = 0
            #cost_owned_current_stock = 0
          
            #for row in trade_details.data:
            #  current_stock = row['stock_symbol']
            #  if current_stock == symbol:
            #    owns_current_stock = True
            #    user_stock_id = row['id']
            #    amount_owned_current_stock = row['stock_amount']
            #    cost_owned_current_stock = row['stock_cost']
            #   current_stock_difference = (int(amount_owned_current_stock) * float(currentValue)) - float(cost_owned_current_stock)
                
            #if pull_count == 0:
            #  st.write("No Account Found - Visit Account to Begin")
            #else:
            #availableCash = account_details[1][0]['available_cash']
            #available_cash_display.write("Available Cash: $" + str(availableCash) + " - Currently Owned: " + str(amount_owned_current_stock) + " - Current Profit/Loss: " + str(round(current_stock_difference,2)))
            




