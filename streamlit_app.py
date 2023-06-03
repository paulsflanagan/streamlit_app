import os
import streamlit as st
import requests
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import Tool
from langchain.tools import BaseTool
from langchain.agents import initialize_agent
from langchain.callbacks.streaming_stdout_final_only import FinalStreamingStdOutCallbackHandler
from bs4 import BeautifulSoup



# define ui
st.title('LP AI Assistant')



# define tools row
#with st.expander("Advnaced Tools:"):
#    vanilla_enabled = st.checkbox('Vanilla', value=True)   
#    checks = st.columns(4)
#    if vanilla_enabled:
#        with checks[0]:
#            search_enabled = st.checkbox('Web Search', value=False, disabled=True)    
#        with checks[1]:
#            scrape_enabled = st.checkbox('Web Scrape', value=False, disabled=True)    
#        with checks[2]:
#            st.checkbox('2')
#        with checks[3]:
#            st.checkbox('3')
#    else:
#       with checks[0]:
#            search_enabled = st.checkbox('Web Search', value=True)    
#        with checks[1]:
#            scrape_enabled = st.checkbox('Web Scrape', value=True)    
#        with checks[2]:
#           st.checkbox('Placeholder')
#       with checks[3]:
#            st.checkbox('Placeholder')    
 
with st.sidebar:
    vanilla_enabled = st.checkbox('Vanilla', value=True)
    st.divider()
    st.write('Advanced Tools')
    if vanilla_enabled:
        search_enabled = st.checkbox('Web Search', value=False, disabled=True)
        scrape_enabled = st.checkbox('Web Scrape', value=False, disabled=True)  
    else:
        search_enabled = st.checkbox('Web Search', value=True)
        scrape_enabled = st.checkbox('Web Scrape', value=True)  

    
# user prompt
prompt = st.text_area('Write your prompt here:')




# define empty dynamic toolset
tools = []



# create our tools


# Web Search
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
    description = "useful for when you need to get the content from a specific webpage"

    def _run(self, webpage: str):
        response = requests.get(webpage)
        html_content = response.text

        def strip_html_tags(html_content):
            soup = BeautifulSoup(html_content, "html.parser")
            stripped_text = soup.get_text()
            return stripped_text

        stripped_content = strip_html_tags(html_content)
        if len(stripped_content) > 4000:
            stripped_content = stripped_content[:4000]
        return stripped_content
    
    def _arun(self, webpage: str):
        raise NotImplementedError("This tool does not support async")
if scrape_enabled:
    scrape = WebPageTool()
    tools.append(scrape)


    
st.write('Response:')    
    
# vanilla experience

if vanilla_enabled:
    llm = OpenAI(temperature=0)
    if prompt:
        response = llm(prompt)
        st.write(response)
        with st_stdout("info"):
            print(response)
else:
    # lang chain agent with tools experience
    llm = OpenAI(temperature=0, streaming=True, callbacks=[FinalStreamingStdOutCallbackHandler()])
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
        try:
            response = conversational_agent.run(prompt)
        except :
            response = 'Please try to re-phrase the question'
        st.write(response)

  
  
  
  
