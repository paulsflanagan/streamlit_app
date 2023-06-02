
import os
import streamlit as st
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import Tool
from langchain.tools import BaseTool
from langchain.agents import initialize_agent
from langchain.callbacks.streaming_stdout_final_only import FinalStreamingStdOutCallbackHandler


# define ui
st.title('LP AI Assistant')
prompt = st.text_area('Write your prompt here:')


# define llm
llm = OpenAI(temperature=0, streaming=True, callbacks=[FinalStreamingStdOutCallbackHandler()])


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
    verbose=False,
    max_iterations=3,
    early_stopping_method='generate',
    memory=memory
)


if prompt:
  response = conversational_agent.run(prompt)
  st.write(response)

  
  
  
  
  
  
  
  
