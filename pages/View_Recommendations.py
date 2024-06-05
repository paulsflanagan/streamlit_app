import streamlit as st
from supabase import create_client, Client

st.title('View Improvement Tickets')

spb_url = st.secrets["spb_url"]
spb_key = st.secrets["spb_key"]

supabase: Client = create_client(spb_url, spb_key)

userName = st.experimental_user.email
st.write(userName)

ADMIN_USERS=st.secrets["admin_users"]



#current_tickets = supabase.table('ticketsDB').select("*").eq('user_name', userName).execute()
current_tickets = supabase.table('ticketsDB').select("*").execute()

placeholder = st.empty()

with placeholder.container():
  if st.experimental_user.email in ADMIN_USERS:
    for x in current_tickets.data:
        st.write('__')
        st.write('Created: ' + x['created_at'])
        st.write('User: ' + x['creator'])
        st.write('Reccomendation: ' + x['context'])
        st.write('Completed: ' + str(x['complete']))
  else:
    st.write("Your Tickets:")
    for x in current_tickets.data:
      if x['creator'] == userName:
        st.write('__')
        st.write('Created: ' + x['created_at'])
        st.write('User: ' + x['creator'])
        st.write('Reccomendation: ' + x['context'])
        st.write('Completed: ' + str(x['complete']))
