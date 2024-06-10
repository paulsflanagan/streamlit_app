import requests
import streamlit as st
from supabase import create_client, Client
import json

#### Keys
td_key=st.secrets["td_key"]
userName = st.experimental_user.email
st.write(userName)

spb_url = st.secrets["spb_url"]
spb_key = st.secrets["spb_key"]

#### Clients
supabase: Client = create_client(spb_url, spb_key)


#### UI

st.title("Stock Trading Game - Account2")

availableCash = 0


account_details, pull_count = supabase.table('StockTradingGame_AccountsDB').select("*").eq('user_name', userName).execute()
