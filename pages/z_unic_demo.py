import streamlit as st
import requests


ais_auth_geo = st.secrets["ais_auth_geo"]
ais_auth_email = st.secrets["ais_auth_email"]
ais_auth_pw = st.secrets["ais_auth_pw"]
ais_flow_id = st.secrets["ais_flow_id "]

st.title('UNIC Demo' + ais_flow_id )


