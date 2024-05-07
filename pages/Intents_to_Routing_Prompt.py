import json
from openai import AzureOpenAI
import csv

st.title('Intents To Routing Prompt')

client = AzureOpenAI(
    api_key=st.secrets["api_key"],
    api_version=st.secrets["api_version"],
    azure_endpoint=st.secrets["azure_endpoint"]
)
