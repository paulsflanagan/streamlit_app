import streamlit as st
from supabase import create_client, Client
import time

## SECRETS

userName = st.experimental_user.email
spb_url = st.secrets["spb_url"]
spb_key = st.secrets["spb_key"]

supabase: Client = create_client(spb_url, spb_key)



## UI HERE

st.title('Messenger - Alpha')

col1, col2 = st.columns([0.6, 0.4], gap="large")
message_space = col1.empty()

#col2.write("Users")

userPrompt = st.chat_input("Say Something")

if userPrompt:
    data, count = supabase.table('StreamlitDB').insert({"user_name": userName, "user_message": userPrompt}).execute()
