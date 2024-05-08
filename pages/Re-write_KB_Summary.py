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

sPromptReWriteSummary = """
Your job is to Summarize the article in a way that is optimized for searches of knowledge bases and documentation.
Specifically focus on:
Using natural keywords and keyphrases from other fields in the rewritten summary
The goal is to rewrite the summary in a way that improves its findability and searchability, helping more easily surface related knowledge, instructions or answers.
The summary cannot exceed 1000 characters.
Please provide only the optimized version of the summary."""

def call_oai(prompt, systemPrompt):
    response = client.chat.completions.create(
    model="llmgateway-text-35turbo-1106-model",
    messages=[
        {
        "role": "system",
        "content": systemPrompt
        },
        {
        "role": "user",
        "content": prompt
        }
    ],
    temperature=0,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return response.choices[0].message.content



# WORKING HERE
def fix_summary(kb_filename, new_kb_filename, llm):
    kb_df = pd.read_csv(kb_filename)
     new_summaries = [process_row(df_row, llm) for _, df_row in kb_df.iterrows()]
    new_summaries = []
    for i, row in kb_df.iterrows():
        print(f"process row: {i}")
        new_summary = process_row(row, llm)
        new_summaries.append(new_summary)
    kb_df["summary"] = new_summaries
    new_detail = []
   for i, row in kb_df.iterrows():
        new_detail.append(f"{row['summary']} {row['detail']}")
    kb_df["detail"] = new_detail
    kb_df.to_csv(new_kb_filename, index=False)




uploaded_file = st.file_uploader("Upload a Knoweldgebase CSV file", accept_multiple_files=False)
if uploaded_file is not None:
    
    try:
        bytes_data = uploaded_file.getvalue()
        kb_df = pd.read_csv(uploaded_file)

        st.write(kb_df)

        new_summaries = []
        #for i, row in kb_df.iterrows():
        for x in range(df.shape[0]):
            st.write(f"process row: {i}")
            #print(f"process row: {i}")
            
            title = df['title'].iloc[x]
            summary = df['summary'].iloc[x]
            detail = df['detail'].iloc[x]
            category = df['category'].iloc[x]
            tags = df['tags'].iloc[x]
            article_data = f'## ARTICLE ##\nTitle: {title}, Summary: {summary}, Detail: {detail},  Category: {category }, Tags: {tags}, Optimized Summary:'
            new_summary = call_oai({"knowledge_article": article_data}, sPromptReWriteSummary)
            new_summaries.append(new_summary)
            
        kb_df["summary"] = new_summaries
        
        new_detail = []
        
        for i, row in kb_df.iterrows():
            new_detail.append(f"{row['summary']} {row['detail']}")
        kb_df["detail"] = new_detail
        #kb_df.to_csv(new_kb_filename, index=False)

        st.write(kb_df)


    
    except UnicodeDecodeError:
        st.write("Error Decoding CSV - Ensure encoding is utf-8")

