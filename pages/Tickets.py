import streamlit as st
from supabase import create_client, Client

st.title('Submit an Improvement Ticket')

spb_url = st.secrets["spb_url"]
spb_key = st.secrets["spb_key"]

supabase: Client = create_client(spb_url, spb_key)

#current_tickets = supabase.table('ticketsDB').select("*").eq('user_name', userName).execute()

userName = st.experimental_user.email
st.write('Hello ' + st.experimental_user.email + '. Please ubmit your ticket below.')
recommendation = st.text_area('Recommendation:', height=400, value='')


if st.button("Submit"):
  data, count = supabase.table('ticketsDB').insert({"creator": userName, "context": recommendation}).execute()

