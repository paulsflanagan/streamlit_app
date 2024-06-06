import streamlit as st
from openai import AzureOpenAI
from supabase import create_client, Client
import time
import json
import random



st.title('LivePerson CD Tool Kit')

st.header("Updates - 06/06/24")

st.write("")

st.subheader("- AI NLU Annotator:")
st.write("Soon to be archived as this is now running through an AI Studio Simulation.")

st.subheader("- AI Transcripts:")
st.write("Locked down to Admins only. This will be archived as this has been moved to AI Studio.")

st.subheader("- Bot Extractor:")
st.write("Latest Update allows for extracting: Dialog Starter patterns and intents; Button options for multiple choice questions, quick replies, button type and structured engagements.")

st.subheader("- Bot Lucid Generator:")
st.write("Locked to Admin only through verification code. Soon to be released to GA.")

st.subheader("- Chat Gpt Emulator V2 Beta:")
st.write("Open for Beta Testing. Latest Updates: allowing for querying files (text based and pdf) and historical context.")

st.subheader("- Intents to Routing Prompts:")
st.write("No Changes.")

st.subheader("- KB to Routing Prompts:")
st.write("No Changes.")

st.subheader("- Kia Persona Tester:")
st.write("Temporary Script added to allow Kia to test Personification through our Azure llm.")

st.subheader("- Optimise KB for AI Search:")
st.write("No Changes.")

st.subheader("- PDF Scraper:")
st.write("No Changes.")

st.subheader("- Stock Trading Game Account:")
st.write("Just for Fun - Have a play.")

st.subheader("- Stock Trading Game Shop:")
st.write("Please note, you can buy but you cannot sell. Updates coming soon.")

st.subheader("- Submit Recommendation:")
st.write("Please submit any issues or requests for tools.")

st.subheader("- Web Scraper Beta:")
st.write("Soon to be archived as this has moved to an asynch batch system. Unstable on browser.")
st.write("")
st.write("")
st.write("All apps are open source: https://github.com/paulsflanagan/streamlit_app/")

#@st.cache_data
#def show_data():
#    st.header("Data analysis")
#    #data = api.get(...)
#    st.success("Fetched data from API!")
#    st.write("Here is a plot of the data:")
#    #st.line_chart(data)
#    st.write("And here is the raw data:")
#    #st.dataframe(data)
    
#@st.cache_data
#def show_data2():
#    st.header("Data analysis2")
#    #data = api.get(...)
#    st.success("Fetched data from API!2")
#    st.write("Here is a plot of the data:2")
#    #st.line_chart(data)
#    st.write("And here is the raw data:2")
#    #st.dataframe(data)

#if st.button('Button 1'):
#    show_data()

#if st.button('Button 2'):
#    show_data2()



#import uuid


# Initialization
#if 'key' not in st.session_state:
#    st.session_state['key'] = uuid.uuid4()
#    UID = uuid.uuid4()
#else:
#    UID = st.session_state['key']
    
#st.write(UID)




#st.title('Lorem ipsum dolor')

#placeholder = st.empty()

#text_to_display = '''

#Football, also known as soccer in some countries, is a team sport played between two teams of eleven players each. The objective is to score goals by getting the ball into the opposing team's goal. Players primarily use their feet to kick the ball, but can also use their head or torso. The team with the most goals at the end of the game wins.

#Football is a popular sport played and watched by millions of people around the world. It requires skill, strategy, and teamwork, and is known for its fast pace and exciting matches. It is governed by the rules of the game set by the International Football Association Board (IFAB) and is played on a rectangular field with a goal at each end.
#'''

#split_text = text_to_display.split(" ")
#displayed_text = ''
#text_buffer = ''
#word_counter = 0
#word_limit = 1
#sleep_time = 0.2

#for x in split_text:
#    displayed_text = displayed_text + ' ' + x
#    placeholder.markdown(displayed_text)
#    time.sleep(0.1)


#for x in split_text:
#  word_counter += 1
#  text_buffer = text_buffer + ' ' + x
#  if word_counter == word_limit:
#    displayed_text = displayed_text + ' ' + text_buffer
#    placeholder.write(displayed_text)
#    text_buffer = ''
#    word_counter = 0
#    time.sleep(sleep_time)
#    word_limit = random.randrange(1,4)
#    #sleep_time = word_limit / 10
    

#    col1, col2, col3 = st.columns([1,1,1])
#    with col1:
#       st.button(next_query_object[0], on_click=next_query_button_click(next_query_object[0]))
#    with col2:
#        st.button(next_query_object[1], on_click=next_query_button_click(next_query_object[1]))
#    with col3:
#        st.button(next_query_object[2], on_click=next_query_button_click(next_query_object[2]))



