import streamlit as st
from supabase import create_client, Client

st.title('Submit an Improvement Ticket')

spb_url = st.secrets["spb_url"]
spb_key = st.secrets["spb_key"]

supabase: Client = create_client(spb_url, spb_key)

#current_tickets = supabase.table('ticketsDB').select("*").eq('user_name', userName).execute()

placeholder = st.empty()

userName = st.experimental_user.email
placeholder.write('Hello ' + st.experimental_user.email + '. Please submit your recommendation ticket below.')
recommendation = placeholder.text_area('Recommendation:', height=400, value='')


if st.button("Submit"):
  #data, count = supabase.table('ticketsDB').insert({"creator": userName, "context": recommendation}).execute()
  st.session_state.user_input = ""
