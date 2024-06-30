import streamlit as st
from supabase import create_client, Client
import time

## SECRETS

userName = st.experimental_user.email
spb_url = st.secrets["spb_url"]
spb_key = st.secrets["spb_key"]

supabase: Client = create_client(spb_url, spb_key)



## UI HERE

st.title('Web Chat - Alpha')

col1, col2 = st.columns([0.6, 0.4], gap="large")
message_space = col1.empty()

#col2.write("Users")

userPrompt = st.chat_input("Say Something")

conversation_history = supabase.table('webChat').select("*").order('id', desc=True ).limit(50).execute()
message_space.write(conversation_history)

for row in conversation_history.data:
    message_space.write(row['created_at'] + " " + row['user_name'] + ": " + row['user_message'])
    

if userPrompt:
    data, count = supabase.table('webChat').insert({"user_name": userName, "user_message": userPrompt}).execute()
