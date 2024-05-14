import streamlit as st
from supabase import create_client, Client

st.title('Submit an Improvement Ticket')

spb_url = st.secrets["spb_url"]
spb_key = st.secrets["spb_key"]

supabase: Client = create_client(spb_url, spb_key)



st.text_area(
if st.button("Submit"):
  current_tickets = supabase.table('ticketsDB').select("*").eq('user_name', userName).execute()

#data, count = supabase.table('ticketsDB').insert({"creator": userName, "user_query": userPrompt, "llm_response": llm_response}).execute()

