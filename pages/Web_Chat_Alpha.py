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


