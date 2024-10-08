import streamlit as st
import requests
import json


ais_auth_geo = st.secrets["ais_auth_geo"]
ais_auth_email = st.secrets["ais_auth_email"]
ais_auth_pw = st.secrets["ais_auth_pw"]
ais_flow_id = st.secrets["ais_flow_id"]

st.title('UNIC Demo')

#Generate Auth Token
import requests
if st.button("test"):
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
    
    #if response.status_code == 200:
        #st.write('Success:', response.json())
    #else:
        #st.write('Error:', response.text)
    
    idToken = response.json()['idToken']
    #st.write(idToken)

    #Start AIStudio Conversation
    url = 'https://aistudio-p-eu.liveperson.net/api/v1/conversations'
    headers = {
        'Authorization': 'Bearer ' + idToken,
        'Content-Type': 'application/json',
    }
    data = {
        "flow_id": ais_flow_id,
        "saved": True,
        "source": "CONVERSATIONAL_CLOUD"
    
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    #if response.status_code == 200:
        #st.write('Success:', response.json())
    #else:
        #st.write('Error:', response.text)
    
    conversationId = response.json()['id']
    #st.write(conversationId)

    #Get AIStudio Response
    url = 'https://aistudio-p-eu.liveperson.net/api/v2/flows/' + ais_flow_id
    headers = {
        'Authorization': 'Bearer ' + idToken,
        'Content-Type': 'application/json',
    }
    data = {
        "text": "Can you help me?",
        "conv_id": conversationId,
    }
    
    response = requests.post(url, headers=headers, json=data)
    reply = response.text
    st.write(reply)
    #if response.status_code == 200:
        #st.write('Success:', response.json())
    #else:
        #st.write('Error:', response.text)
