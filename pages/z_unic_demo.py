import streamlit as st
import requests


ais_auth_geo = st.secrets["ais_auth_geo"]
ais_auth_email = st.secrets["ais_auth_email"]
ais_auth_pw = st.secrets["ais_auth_pw"]
ais_flow_id = st.secrets["ais_flow_id"]

st.title('UNIC Demo')

#Generate Auth Token
import requests

url = 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=' + ais_auth_geo
headers = {
    'Content-Type': 'application/json',
}
data = {
    "returnSecureToken": True,
    "email": ais_auth_email,
    "password": ais_auth_pw

}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    st.write('Success:', response.json())
else:
    st.write('Error:', response.text)

idToken = response.json()['idToken']
st.write(idToken)
