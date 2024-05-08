import json
from openai import AzureOpenAI
import csv
import streamlit as st
import pandas as pd
from io import StringIO


st.title('Re-Write Knowledge Base Summarys')

client = AzureOpenAI(
    api_key=st.secrets["api_key"],
    api_version=st.secrets["api_version"],
    azure_endpoint=st.secrets["azure_endpoint"]
)

sPromptIntentsFromKB = """
Your job is to analyze the following article and provide an intent and description that could be served by that article.
An intent is a short phrase (5 words or less) that describes something that a customer could want to do. 
A description is a sentence that describes what the user could want to do in detail.
You should return each intent and description in this format: Intent:<intent name>\nDescription:<description>"""
sPromptRoutesFromIntent = ""
