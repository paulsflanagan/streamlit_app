import os
import streamlit as st
import requests
import pandas as pd
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import Tool
#from langchain.agents.agent_toolkits import create_python_agent
#from langchain.agents import create_pandas_dataframe_agent
from langchain.tools import BaseTool
from langchain.agents import initialize_agent
#from langchain.tools.python.tool import PythonREPLTool
from langchain.python import PythonREPL
from langchain import LLMMathChain
#from langchain.callbacks.streaming_stdout_final_only import FinalStreamingStdOutCallbackHandler
from bs4 import BeautifulSoup
from PIL import Image
from io import StringIO

import logging
logging.basicConfig(filename='scraper.log', level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

# define max tokens
max_tokens = 3000

# define empty df
#df = pd.DataFrame()

# define logo
#image = Image.open('Logo.png')
#st.image(image)
st.title('AI Assistant')




# define sidebar

with st.sidebar:
        st.title('Settings:')
        st.text("User: " + str(st.experimental_user['email']))
        st.divider()
        agent_type = st.selectbox(
            'Agent Type:',
            ('Open AI Agent', 'Python Agent','Math Agent','Pandas Agent'))
        
        if agent_type == 'Open AI Agent':
            defined_agent = False
            #st.divider()
            #st.write('Simple:')
            simple_enabled = True #!!! Remove if returning to multi tool
            #simple_enabled = st.checkbox('Open AI Only', value=True)
            #st.divider()
            #st.write('Advanced:')
            #if simple_enabled:
            #    advanced_enabled = False
            #    search_enabled = st.checkbox('Web Search Tool', value=False, disabled=True)
            #    scrape_enabled = st.checkbox('Web Scrape Tool', value=False, disabled=True)  
            #else:
            #   advanced_enabled = True
            #    search_enabled = st.checkbox('Web Search Tool', value=True)
            #    scrape_enabled = st.checkbox('Web Scrape Tool', value=True)
            st.divider() 
            temperature = st.slider('Temperature:', 0.0, 1.0, 0.5, step=0.1)
            
        else:
            defined_agent = True      
            #st.divider()
            #st.write('Simple:')
            simple_enabled = False #!!! Remove if reutning to multi tool
            #simple_enabled = st.checkbox('Open AI Only', value=False, disabled=True)
            #st.divider()
            #st.write('Advanced:')
            #advanced_enabled = False
            #search_enabled = st.checkbox('Web Search Tool', value=False, disabled=True)
            #scrape_enabled = st.checkbox('Web Scrape Tool', value=False, disabled=True)  
            st.divider() 
            temperature = st.slider('Temperature:', 0.0, 1.0, 0.0, step=0.1, disabled=True)
           

    
# user prompt
if agent_type == 'Open AI Agent':
        if simple_enabled:
                st.write(agent_type + " - Simple")
        else:
                st.write(agent_type + " - Advanced")
else:
        st.write(agent_type)

        
# get csv for pandas agent
if agent_type == 'Pandas Agent':
        uploaded_file = st.file_uploader("Upload a CSV file")

        

        
# prompt text
st.text("")
prompt = st.text_area('Write your prompt here:')




# define empty dynamic toolset
tools = []



# create our tools


# Web Search
search_enabled = False #!!! Remove if retunrning to multi tool
if search_enabled:
    search = DuckDuckGoSearchRun()
    tools = [
        Tool(
            name = "search",
            func=search.run,
            description="useful for when you need to answer questions about current events. You should ask targeted questions"
        )
    ]
    tools.append(search)


# Web Scrape 
class WebPageTool(BaseTool):
    name = "Get Webpage"
    description = "useful for when you need to get up to date content from a specific webpage"

    def _run(self, webpage: str):
        response = requests.get(webpage)
        html_content = response.text

        def strip_html_tags(html_content):
            soup = BeautifulSoup(html_content, "html.parser")
            stripped_text = soup.get_text()
            return stripped_text

        stripped_content = strip_html_tags(html_content)
        if len(stripped_content) > 1000:
            stripped_content = stripped_content[:1000]
        return stripped_content
    
    def _arun(self, webpage: str):
        raise NotImplementedError("This tool does not support async")
        
scrape_enabled = False #!!! Remove if retunrning to multi tool
if scrape_enabled:
    scrape = WebPageTool()
    tools.append(scrape)


st.text("")    
st.text("")
st.write('Response:')    
    
# simple experience

if simple_enabled:
    llm = OpenAI(temperature=temperature, max_tokens = max_tokens)
    if prompt:
        response = llm(prompt)
        st.write(response)

advanced_enabled = False #!!! Remove if retunrning to multi tool        
if advanced_enabled:
    # lang chain agent with tools experience
    #llm = OpenAI(temperature=temperature, max_tokens = max_tokens, streaming=True, callbacks=[FinalStreamingStdOutCallbackHandler()])
    llm = OpenAI(temperature=temperature, max_tokens = max_tokens)
    # conversational agent memory
    memory = ConversationBufferWindowMemory(
        memory_key='chat_history',
        k=3,
        return_messages=True
    )
    
    # create our agent
    conversational_agent = initialize_agent(
        agent='chat-conversational-react-description',
        tools=tools,
        llm=llm,
        verbose=True,
        max_iterations=3,
        early_stopping_method='generate',
        memory=memory
    )
    
    response = ''
    if prompt:
        response = conversational_agent.run(prompt)
        st.write(response)
        #try:
            #response = conversational_agent.run(prompt)
        #except :
            #response = 'Please try to re-phrase the question'
        #st.write(response)

if defined_agent:
        #if agent_type == 'Python Agent':
                #agent_executor = create_python_agent(
                #llm=OpenAI(temperature=temperature, max_tokens=max_tokens),
                #tool=PythonREPLTool(),
                #verbose=True)
        if agent_type == 'Math Agent':
                llm=OpenAI(temperature=temperature, max_tokens=max_tokens)
                agent_executor = LLMMathChain.from_llm(llm, verbose=True)
        #if agent_type == 'Pandas Agent':
                #try:
                       # if uploaded_file is not None:
                                #bytes_data = uploaded_file.getvalue()
                                #st.write(bytes_data)
                                #stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
                                #st.write(stringio)
                                #string_data = stringio.read()
                                #st.write(string_data)
                                #df = pd.read_csv(uploaded_file)
                                #st.write("Active CSV: " + string_data)
                        #agent_executor = create_pandas_dataframe_agent(OpenAI(temperature=temperature), df, verbose=True)
               # except:
                        #st.write('No DataFrame')
                
        if prompt:
                #response = agent_executor.run(prompt)
                #st.write(response)
                try:
                        response = agent_executor.run(prompt)
                        st.write(response)
                except:
                        st.write("Your request exceeds this model's maximum context length (4097 tokens)")
          
                
  
