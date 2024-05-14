import streamlit as st
from openai import AzureOpenAI
from supabase import create_client, Client
import time
import json
import random



st.title('ChatGPT Emulator')
#uploaded_file = st.file_uploader("", accept_multiple_files=False)
col1, col2 = st.columns([0.6, 0.4])

#col1.subheader("GPT Emulator Header Test")
uploaded_file = col1.file_uploader("", accept_multiple_files=False)
col1.markdown('Conversation here')

col2.subheader("Conversation History")
#st.sidebar
with col2.expander("What is Football?"):
    st.write('''
Football, also known as soccer in some countries, is a team sport played between two teams of eleven players each. The objective is to score goals by getting the ball into the opposing team's goal. Players primarily use their feet to kick the ball, but can also use their head or torso. The team with the most goals at the end of the game wins.

Football is a popular sport played and watched by millions of people around the world. It requires skill, strategy, and teamwork, and is known for its fast pace and exciting matches. It is governed by the rules of the game set by the International Football Association Board (IFAB) and is played on a rectangular field with a goal at each end.
    ''')
with col2.expander("How do you make Chicken Soup?"):
    st.write('''
To make chicken soup, start by sautéing diced onions, carrots, and celery in a large pot with some olive oil. Once the vegetables are soft, add in diced chicken breast or thighs and cook until the chicken is no longer pink. Then, pour in chicken broth and bring the mixture to a boil. Reduce the heat and let the soup simmer for about 20-30 minutes, or until the chicken is fully cooked.

You can also add in seasonings like salt, pepper, thyme, and bay leaves for flavor. Some people like to add noodles or rice to their chicken soup, so you can add those in and cook until they are tender. Finally, taste the soup and adjust the seasonings as needed. Serve the chicken soup hot and enjoy!
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



