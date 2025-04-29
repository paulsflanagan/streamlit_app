import streamlit as st
import requests
import json


ais_auth_geo = st.secrets["ais_auth_geo"]
ais_auth_email = st.secrets["ais_auth_email"]
ais_auth_pw = st.secrets["ais_auth_pw"]
ais_flow_id = st.secrets["ais_flow_id"]

st.title('UNIC Demo')

col1, col2 = st.columns([0.4, 0.6], gap="large")
user_query = col1.chat_input("type here")

#Generate Auth Token
if user_query:
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
        "text": user_query,
        "conv_id": conversationId,
    }
    
    response = requests.post(url, headers=headers, json=data)
    data = json.loads(response.text)
    col1.write(data[0]['text'])
    #if response.status_code == 200:
        #st.write('Success:', response.json())
    #else:
        #st.write('Error:', response.text)
