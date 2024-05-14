import streamlit as st
from openai import AzureOpenAI
from supabase import create_client, Client
import time
import json


st.title('Simple LLM Interface')

placeholder = st.empty()

text_to_display = '''
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras viverra dapibus nunc, vulputate eleifend ex tincidunt sit amet. Mauris sit amet dolor nulla. Sed faucibus consectetur libero, varius consequat ipsum pellentesque vel. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Mauris at interdum ex, vel egestas diam. Mauris sagittis mollis arcu et iaculis. Nulla a turpis finibus, tincidunt justo fermentum, luctus velit. Integer nisi lacus, aliquet vitae urna a, porta rutrum ex. Praesent sed aliquam sem. Nullam tincidunt ut sem dictum malesuada. Ut ut ligula nunc. Aenean consequat purus orci. Integer placerat pretium lorem, non fringilla mi tempus sit amet.

Praesent id tristique erat. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Sed id libero elit. Morbi eu porta ipsum, eget tincidunt mauris. In cursus eget velit at sollicitudin. Morbi at purus neque. Interdum et malesuada fames ac ante ipsum primis in faucibus.

In vitae risus sem. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; In condimentum tempus sapien. Duis vel neque nec est pellentesque volutpat a quis urna. Integer sodales scelerisque sapien, non bibendum felis condimentum a. Proin quis nulla urna. Donec consectetur lorem enim, in sodales lorem maximus ac. Vestibulum et tortor sed justo tincidunt pretium. Pellentesque eget sapien varius, feugiat ante eu, viverra diam. In laoreet non tellus vitae pellentesque. Fusce volutpat neque neque, ut malesuada nisl blandit faucibus. Pellentesque faucibus maximus turpis eu rhoncus. Morbi blandit diam nec sem auctor molestie.
'''

split_text = text_to_display.split(" ")
displayed_text = ''
for x in split_text:
  displayed_text = displayed_text + ' ' + x
  placeholder.write(displayed_text)
  time.sleep(0.08)

#    col1, col2, col3 = st.columns([1,1,1])
#    with col1:
#       st.button(next_query_object[0], on_click=next_query_button_click(next_query_object[0]))
#    with col2:
#        st.button(next_query_object[1], on_click=next_query_button_click(next_query_object[1]))
#    with col3:
#        st.button(next_query_object[2], on_click=next_query_button_click(next_query_object[2]))



