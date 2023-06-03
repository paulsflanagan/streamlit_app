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



# define background
page_bg_img = '''
<style>
body {
background-image: url("https://authentication.liveperson.net/img/background_new.png");
background-size: cover;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)


# define ui
st.title('LP AI Assistant')



# define sidebar


with st.sidebar:
    st.title('Version')
    st.divider()
    vanilla_enabled = st.checkbox('Original', value=True)
    st.divider()
    st.write('Advanced:')
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
    llm = OpenAI(temperature=0, max_tokens = 3000)
    if prompt:
        response = llm(prompt)
        st.write(response)

else:
    # lang chain agent with tools experience
    llm = OpenAI(temperature=0, max_tokens = 3000, streaming=True, callbacks=[FinalStreamingStdOutCallbackHandler()])
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

  
  
  
  
