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
  for x in current_tickets.data:
      st.write('__')
      st.write('Created: ' + x['created_at'])
      st.write('User: ' + x['creator'])
      st.write('Reccomendation: ' + x['context'])
      st.write('Completed: ' + str(x['complete']))
