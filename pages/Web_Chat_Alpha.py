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

col1, col2 = st.columns([0.9, 0.1], gap="large")
#message_space = col1.empty()
message_space = col1.empty()

#col2.write("Users")

userPrompt = st.chat_input("Say Something")

conversation_history_backwards = supabase.table('webChat').select("*").order('id', desc=True ).limit(5).execute()
conversation_history = list(reversed(conversation_history_backwards.data))
display_string = ""
for row in conversation_history:
    display_string = display_string + row['created_at'] + '  \n'
    #message_space.write(row['created_at'])
    #message_space.write(row['user_name'] + ": " + row['user_message'])
    display_string = display_string + row['user_name'] + ": " + row['user_message'] + '  \n\n'

message_space.markdown(display_string)

if userPrompt:
    data, count = supabase.table('webChat').insert({"user_name": userName, "user_message": userPrompt}).execute()


