import streamlit as st
from openai import AzureOpenAI
from supabase import create_client, Client
import time
import json
import random




col1, col2 = st.columns([0.6, 0.4])

col1.subheader("GPT Emulator Header Test")
col1.markdown('Conversation here')

col2.subheader("Conversation History")
with col2.expander("What is Football?"):
    st.write('''
Football, also known as soccer in some countries, is a team sport played between two teams of eleven players each. The objective is to score goals by getting the ball into the opposing team's goal. Players primarily use their feet to kick the ball, but can also use their head or torso. The team with the most goals at the end of the game wins.

Football is a popular sport played and watched by millions of people around the world. It requires skill, strategy, and teamwork, and is known for its fast pace and exciting matches. It is governed by the rules of the game set by the International Football Association Board (IFAB) and is played on a rectangular field with a goal at each end.
    ''')













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



