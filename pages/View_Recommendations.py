import streamlit as st
from supabase import create_client, Client

st.title('Submit an Improvement Ticket')

spb_url = st.secrets["spb_url"]
spb_key = st.secrets["spb_key"]

supabase: Client = create_client(spb_url, spb_key)

placeholder = st.empty()

#current_tickets = supabase.table('ticketsDB').select("*").eq('user_name', userName).execute()
current_tickets = supabase.table('ticketsDB').select("*").execute()

with placeholder.container():
  st.write("This is one element")
  st.write("This is another")
  count = 0
  for x in rcurrent_tickets.data:
      st.write('Created: ' + x['created_at'] + ' User: ' + x['creator'] + ' Reccomendation: ' + x['context'] + ' Completed: ' + str(x['context']))
      st.write(' ')
