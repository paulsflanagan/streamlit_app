import streamlit as st
from io import StringIO
import requests
import json

st.title('Lucid Generator')


l_cid = st.secrets["l_cid"]
l_cs = st.secrets["l_cs"]
l_ruri = st.secrets["l_ruri"]

code = st.text_input("Enter Code", "")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    if st.button("Submit"):
        
        # Create oAuth token
        url = 'https://api.lucid.co/oauth2/token'
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            "code": code,
            "client_id": l_cid,
            "client_secret": l_cs,
            "grant_type": "authorization_code",
            "redirect_uri": l_ruri
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        tokenHolder = json.loads(response.text)
        oAuth = tokenHolder['access_token']
        st.write(oAuth)




        



        
        # Create Chart
        url = 'https://api.lucid.co/documents'
        headers = {
            'Authorization': 'Bearer '+ oAuth,
            'Lucid-Api-Version': '1'
        }
        files = {
            'file': ('import.lucid', open('import.lucid', 'rb'), 'x-application/vnd.lucid.standardImport')
        }
        data = {
            'title': '_____Ais Test Extraction',
            'product': 'lucidchart',
            #'parent': '1234'
        }
        response = requests.post(url, headers=headers, files=files, data=data)
        responseDict = json.loads(response.text)
        st.write("Here is your Lucid: " + responseDict['editUrl'])
