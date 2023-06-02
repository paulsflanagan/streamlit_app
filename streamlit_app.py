
import os
import streamlit as st
from langchain.llms import OpenAI
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import Tool
from langchain.tools import BaseTool
from langchain.agents import initialize_agent

st.title('LP AI Assistant')

prompt = st.text_area('Write your prompt here:')



# create our tools
search = DuckDuckGoSearchRun()
tools = [
    Tool(
        name = "search",
        func=search.run,
        description="useful for when you need to answer questions about current events. You should ask targeted questions"
    )
]


# define toolset
tools = [search]


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


#llm = OpenAI(temperature=0.9)

if prompt:
  response = conversational_agent(prompt)
  st.write(response)

  
  
  
  
  
  
  
  
