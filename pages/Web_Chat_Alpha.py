import streamlit as st
from datetime import datetime, timedelta, timezone
from supabase import create_client, Client
import time

## SECRETS

userName = st.experimental_user.email
spb_url = st.secrets["spb_url"]
spb_key = st.secrets["spb_key"]

supabase: Client = create_client(spb_url, spb_key)

def format_chat_timestamp(timestamp):
    parsed_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00').split('.')[0])
    current_time = datetime.now()
    time_difference = current_time - parsed_time

    if time_difference < timedelta(minutes=1):
        return "just now"
    elif time_difference < timedelta(hours=1):
        return f"{time_difference.seconds // 60} minutes ago"
    elif current_time.date() == parsed_time.date():
        return f"today at {parsed_time.strftime('%I:%M %p')}"
    elif current_time.date() - parsed_time.date() == timedelta(days=1):
        return f"yesterday at {parsed_time.strftime('%I:%M %p')}"
    else:
        return parsed_time.strftime('%Y-%m-%d %I:%M %p')

def update_message_space():
    conversation_history_backwards = supabase.table('webChat').select("*").order('id', desc=True ).limit(5).execute()
    conversation_history = list(reversed(conversation_history_backwards.data))
    display_string = ""
    for row in conversation_history:
        formatted_timestamp = format_chat_timestamp(row['created_at'])
        display_string = display_string + ':gray[' + formatted_timestamp + ']  \n'
        clean_user_name = row['user_name'].replace("@liveperson.com", "").replace("@gmail.com", "")
        display_string = display_string + ':blue[' + clean_user_name + ":] " + row['user_message'] + '  \n\n'
    
    message_space.markdown(display_string)


## UI HERE

st.title('Web Chat - Alpha')

col1, col2 = st.columns([0.9, 0.1], gap="large")
#message_space = col1.empty()
message_space = col1.empty()

#col2.write("Users")
update_message_space()
userPrompt = st.chat_input("Say Something")


if userPrompt:
    data, count = supabase.table('webChat').insert({"user_name": userName, "user_message": userPrompt}).execute()
    update_message_space()


