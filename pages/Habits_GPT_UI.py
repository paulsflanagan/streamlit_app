import streamlit as st
from openai import AzureOpenAI
from supabase import create_client, Client
from io import StringIO
from pypdf import PdfReader 
import requests
import time
import json
import uuid


### SESSION ID Module ###

if 'key' not in st.session_state:
    st.session_state['key'] = uuid.uuid4()
    session_id = uuid.uuid4()
else:
    session_id = st.session_state['key']
    


### LLM Tools Module #### DO NOT USE. ####

# NOTE: Replace with LLM of Choice

## Create LLM Gateway Client

idToken = st.secrets["llm_gateway_token"]
account_id = st.secrets["cb_account_id"]
trace_id = 'paul_poc'
subscription_name = 'lp-llm-ptu'
model_name = 'gpt-4o-mini-2024-07-18'
activate_links = handle_hallucinations = highlight_hallucinations = use_pl_cache = pci_mask_prompt = False
gateway_url = f"https://lo.cbllmgateway.liveperson.net/api/v1/gateway/llm/accounts/{account_id}/chats?trace_id={trace_id}&activate_links={activate_links}&handle_hallucinations={handle_hallucinations}&highlight_hallucinations={highlight_hallucinations}&use_pl_cache={use_pl_cache}&pci_mask_prompt={pci_mask_prompt}"
headers = {'Authorization': 'Bearer ' + idToken,'Content-Type': 'application/json',}


## Call Gateway With Standard Prompts ##

def call_gateway(system_prompt,assistant_prompt,user_prompt):
  """Calls the LLM Gateway with system, assistant, and user prompts.

  Args:
    system_prompt: The system prompt for the LLM.
    assistant_prompt: The assistant prompt for the LLM.
    user_prompt: The user prompt for the LLM.

  Returns:
    The text response from the LLM.
  """
  #logging.info("Calling LLM Gateway with standard prompts.")
  #logging.debug(f"System Prompt: {system_prompt}")
  #logging.debug(f"Assistant Prompt: {assistant_prompt}")
  #logging.debug(f"User Prompt: {user_prompt}")
  try:
    data = {"messages_list": [{"role": "system", "content": system_prompt},{"role": "assistant", "content": assistant_prompt},{"role": "user", "content": user_prompt},],'subscription_name': subscription_name,'request_config': {'model_name': model_name,}}
    response = requests.post(gateway_url, headers=headers, json=data)
    response.raise_for_status() # Raise an exception for bad status codes
    #logging.info("Successfully received response from LLM Gateway.")
    #logging.debug(f"LLM Response: {response.json()['results'][0]['text']}")
    return response.json()['results'][0]['text']
  except requests.exceptions.RequestException as e:
    return None
    #logging.error(f"Error calling LLM Gateway: {e}")
    #return None


## Call Gateway With User Defined Messages Json ##
# Example: msgJson = [{"role": "system", "content": "This is the system prompt"},{"role": "assistant", "content":  "This is the assistant prompt"},{"role": "user", "content": "This is the user prompt"}]

def call_gateway_BYOM(messages_list):
  """Calls the LLM Gateway with a custom list of messages.

  Args:
    messages_list: A list of message dictionaries

  Returns:
    The text response from the LLM.
  """
  #logging.info("Calling LLM Gateway with user defined messages.")
  #logging.debug(f"Messages List: {messages_list}")
  try:
    data = {"messages_list": messages_list,'subscription_name': subscription_name,'request_config': {'model_name': model_name,}}
    response = requests.post(gateway_url, headers=headers, json=data)
    response.raise_for_status() # Raise an exception for bad status codes
    #logging.info("Successfully received response from LLM Gateway.")
    #logging.debug(f"LLM Response: {response.json()['results'][0]['text']}")
    return response.json()['results'][0]['text']
  except requests.exceptions.RequestException as e:
    return None
    #logging.error(f"Error calling LLM Gateway BYOM: {e}")
    #return None


### DataBase Tools Module

# NOTE: Replace with Knowledgebase / Database / CSM of Choice

# DataBase Client (isolate initialization)


#if 'supabase_initialized' not in globals(): ## DISABLED

## Create SupaBase Client
#td_key = userdata.get('td_key')
spb_url = st.secrets["spb_url"]
spb_key = st.secrets["spb_key"]

supabase: Client = create_client(spb_url, spb_key)

db_table = 'habits_web_scrape'

#supabase_initialized = True


## SupaBase Interaction Functions

# List Dictionary Returns

def get_data_from_table(table_name):
  """Fetches all data from a specified Supabase table.

  Args:
    table_name: The name of the table to fetch data from.

  Returns:
    A list of dictionaries representing the rows in the table.
  """
  try:
    response = supabase.table(table_name).select("*").execute()
    #logging.info(f"Successfully fetched data from table: {table_name}")
    return response.data
  except Exception as e:
    return None
    #logging.error(f"Error fetching data from {table_name}: {e}")
    #return None

def get_data_from_table_where(table_name, column_name, column_value):
  """Fetches data from a specified Supabase table where a column matches a value.

  Args:
    table_name: The name of the table to fetch data from.
    column_name: The name of the column to filter on.
    column_value: The value to filter for in the specified column.

  Returns:
    A list of dictionaries representing the filtered rows in the table.
  """
  try:
    response = supabase.table(table_name).select("*").eq(column_name, column_value).execute()
    #logging.info(f"Successfully fetched data from table: {table_name} where {column_name} is {column_value}")
    return response.data
  except Exception as e:
    return None
    #logging.error(f"Error fetching data from {table_name} where {column_name} is {column_value}: {e}")
    #return None

def insert_data_into_table(table_name, data):
  """Inserts a new row of data into a specified Supabase table.

  Args:
    table_name: The name of the table to insert data into.
    data: A dictionary representing the data to insert.

  Returns:
    The inserted data as a list of dictionaries, or None if an error occurred.
  """
  try:
    response = supabase.table(table_name).insert(data).execute()
    #logging.info(f"Successfully inserted data into table: {table_name}")
    #logging.debug(f"Inserted data: {data}")
    return response.data
  except Exception as e:
    return None
    #logging.error(f"Error inserting data into {table_name}: {e}")
    #logging.debug(f"Data that failed to insert: {data}")
    #return None

def update_data_in_table(table_name, id_value, data):
  """Updates data in a specified Supabase table based on an ID.

  Args:
    table_name: The name of the table to update data in.
    id_value: The value of the 'id' column for the row to update.
    data: A dictionary representing the data to update.

  Returns:
    The updated data as a list of dictionaries, or None if an error occurred.
  """
  try:
    response = supabase.table(table_name).update(data).eq('id', id_value).execute()
    #logging.info(f"Successfully updated data in table: {table_name} with id: {id_value}")
    #logging.debug(f"Updated data: {data}")
    return response.data
  except Exception as e:
    return None
    #logging.error(f"Error updating data in {table_name} with id: {id_value}: {e}")
    #logging.debug(f"Data that failed to update: {data}")
    #return None

def delete_data_from_table(table_name, id_value):
  """Deletes data from a specified Supabase table based on an ID.

  Args:
    table_name: The name of the table to delete data from.
    id_value: The value of the 'id' column for the row to delete.

  Returns:
    The deleted data as a list of dictionaries, or None if an error occurred.
  """
  try:
    response = supabase.table(table_name).delete().eq('id', id_value).execute()
    #logging.info(f"Successfully deleted data from table: {table_name} with id: {id_value}")
    return response.data
  except Exception as e:
    return None
    #logging.error(f"Error deleting data from {table_name} with id: {id_value}: {e}")
    #return None


# Specialty Access Functions

def get_column_data_from_table(table_name, column_name):
  """Fetches data from a specific column and the id column in a Supabase table.

  Args:
    table_name: The name of the table to fetch data from.
    column_name: The name of the column to fetch data from.

  Returns:
    A list of dictionaries, where each dictionary contains the 'id' and the value
    from the specified column for each row, or None if an error occurred.
  """
  try:
    response = supabase.table(table_name).select('id', column_name).execute()
    #logging.info(f"Successfully fetched data from columns 'id' and '{column_name}' in table: {table_name}")
    return response.data
  except Exception as e:
    return None
    #logging.error(f"Error fetching data from columns 'id' and '{column_name}' in table {table_name}: {e}")
    #return None

def get_cell_data_from_table(table_name, column_name, row_id):
  """Fetches data from a specific cell in a Supabase table based on row ID and column name.

  Args:
    table_name: The name of the table to fetch data from.
    column_name: The name of the column to fetch data from.
    row_id: The value of the 'id' column for the row to fetch data from.

  Returns:
    The value of the specified cell, or None if an error occurred or the cell was not found.
  """
  try:
    response = supabase.table(table_name).select(column_name).eq('id', row_id).single().execute()
    #logging.info(f"Successfully fetched data from cell in table: {table_name} with id: {row_id} and column: {column_name}")
    return response.data.get(column_name)
  except Exception as e:
    return None
    #logging.error(f"Error fetching data from cell in table {table_name} with id: {row_id} and column: {column_name}: {e}")
    #return None

def get_details_from_id_list(table_name, id_list):
  """Fetches 'title' and 'detail' columns for a list of row IDs from a Supabase table.

  Args:
    table_name: The name of the table to fetch data from.
    id_list: A list of row IDs to fetch data for.

  Returns:
    A list of dictionaries, where each dictionary contains the 'id', 'title', and 'detail'
    for the corresponding row ID, or an empty list if no data is found or an error occurs.
  """
  results = []
  for row_id in id_list:
    try:
      response = supabase.table(table_name).select('id', 'title', 'detail').eq('id', row_id).single().execute()
      if response.data:
        results.append(response.data)
        #logging.info(f"Successfully fetched details for id: {row_id}")
      #else:
        #logging.warning(f"No data found for id: {row_id}")
    except Exception as e:
      return None
      #logging.error(f"Error fetching details for id: {row_id}: {e}")
  return results


### Knowledge Context Retrieval Module

def knowledge_search(table_name, article_limit, query):
  """Retrieves article titles from the knowledgebase.
     LLM determines which titles are relevant to the query.
     Extracts a list of relevant article ids
     Returns the text content of the articles.

  Args:
    table_name: The name of the table to update data in.
    article_limit: The vmax number of articles to return
    data: A dictionary representing the data to update.
  Returns:
    The text content of the articles.
  """

  # Retrieves article titles - ids from the knowledgebase.
  titles = get_column_data_from_table(db_table, 'title')

  # LLM determines which titles are relevant to the query.
  system_prompt = f"The list provided in CONTEXT contains titles to articles relating to Habits for a Better World and their projects. Return up to {article_limit} titles that are relevant to the users message or if nothing is relevant return the New Home Page. Return them in json format including the relevant ids."
  context = "CONTEXT: " + str(titles)
  response = call_gateway(system_prompt,context,query)

  #logging.info(f"LLM Gateway Response for ID extraction: {response}")
  id_list = [] # Initialize id_list as an empty list
    
  # Extracts a list of relevant article ids
  if response:
    # Extract JSON string from markdown code block if present
    if response.startswith("```json") and response.endswith("```"):
        # Remove the markdown code block syntax and any leading/trailing whitespace
        json_string = response[len("```json"):len(response)-len("```")].strip()
    else:
        # If no markdown block, assume the response is the direct JSON string and strip whitespace
        json_string = response.strip()

    # Parse the JSON string into a Python object
    try:
      response_data = json.loads(json_string)
      #logging.info(f"Parsed JSON response data type: {type(response_data)}")
      #logging.info(f"Parsed JSON response data: {response_data}")
      id_list = [item['id'] for item in response_data]
      #logging.info(f"Extracted List of IDs: {id_list}")
    except json.JSONDecodeError as e:
      return None
      #logging.error(f"Error decoding JSON response: {e}")
      #logging.error(f"Response content that caused error: {response}")
    except TypeError as e:
      return None
      #logging.error(f"TypeError during ID extraction: {e}")
      #logging.error(f"Response data causing TypeError: {response_data}")
  else:
    return None
    #logging.warning("No response data from LLM to extract IDs from.")
  if id_list:
    knowledge_context = get_details_from_id_list(table_name, id_list)
  else:
    knowledge_context = []
    #logging.info(f"Retrieved Knowledge: {knowledge_context}")
  return knowledge_context




### Resolve Query - With x Turn Conversation History #CONVERSATION HISTORY NOT YET ENABLED

query = "" #"What is Habits for a better world all about eh?"
article_limit = 1


def resolve_query(db_table, article_limit, query):
  """Retrieves knowledge context from the knowledgebase.
     LLM resolves query given the user query and the knowledge context.
     Returns the text llm response to the query.

  Args:
    table_name: The name of the table to update data in.
    article_limit: The vmax number of articles to return
    query: The users query.
  Returns:
    The text llm response to the query.
  """

  knowledge_context = knowledge_search(db_table, article_limit, query)
  system_prompt = f"You are a helpful assistant working for Habits for a Better World. Answer the users query using only information found in the CONTEXT provided. Answer in polite, professional and conversational manner. CONTEXT: {knowledge_context}"
  st.write(system_prompt)
  local_conversation_history = "" #get_local_conversation_history() ##DISABLED CONVERSATION HISTORY

  # Construct messages_list ensuring it's always a flat list of dictionaries
  messages_list = [{"role": "system", "content": system_prompt}]
  #if isinstance(local_conversation_history, list):
  #    messages_list.extend(local_conversation_history)
  #elif isinstance(local_conversation_history, dict):
  #    messages_list.append(local_conversation_history)

  messages_list.append({"role": "user", "content": query})


  #print(messages_list) # Keep print for debugging for now

  response = call_gateway_BYOM(messages_list)
  #add_local_conversation_history(query, response) #DISABLED
  return response


#print(resolve_query(db_table, article_limit, query))


## UI HERE

st.title('Habits GPT UI')
#if st.button("Clear Conversation"):
    #data, count = supabase.table('StreamlitDB').delete().eq('user_name', userName).execute()

col1, col2 = st.columns([0.6, 0.4], gap="large")
#uploaded_file = col1.file_uploader("", accept_multiple_files=False)
user_message_space = col1.empty()
response_message_space = col1.empty()
#history_message_space = col2.empty()

#conversationHistory = 'None'
additionalContext = 'None'

#col2.write("Conversation History")
#st.sidebar
#if col2.button("Reset Session"):
#    st.session_state['key'] = uuid.uuid4()
#    history_message_space.write("Session Cleared")

#conversation_history = supabase.table('StreamlitDB').select("*").eq('session_id', session_id).execute()
#counter = 1
#for row in conversation_history.data:
#    if counter > len(conversation_history.data)-6:
#        with col2.expander(row['user_query']):
#            st.write(row['llm_response'])
#    counter += 1



#if uploaded_file is not None:
#    try:
#        bytes_data = uploaded_file.getvalue()
#        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
#        string_data = stringio.read()
#        additionalContext = string_data
#    except:
#        try:
#            reader = PdfReader(uploaded_file)
#            #st.write(len(reader.pages))
#            text = '%PDF Document: \n\n'
#            counter = 1
#            for each in reader.pages:
#                text = text + "%PAGE: " + str(counter) + "\n\n" + each.extract_text() + "\n\n"
#                counter += 1
#                additionalContext = text
#                #st.write(text)
#        except:
#            st.write("Error Reading File")
#

#def update_screen():
#    response = supabase.table('StreamlitDB').select("*").eq('user_name', userName).execute()
    #st.text_area('Conversation:', height=400, value=str(response))
#    testString = ''
#    conversationHistory = ''#'Previous Questions Asked: '
#    with placeholder.container():
        #st.write("This is one element")
        #st.write("This is another")
#        count = 0
#        for x in response.data:
#            count += 1
#            if count > len(response.data)-3:
#                st.write('User: ' + x['user_query'])
#                st.write('Bot: ' + x['llm_response'])
#                st.write(' ')
                #conversationHistory = conversationHistory + ' - ' + x['user_query']
                #conversationHistory = conversationHistory + 'User: ' + x['user_query'] + 'Bot: ' + x['llm_response']
#    return conversationHistory



def next_query_button_click(query):
    st.session_state.key = query


#time.sleep(3)

#systemPrompt = '''You are a helpful assistant. Answer the users query. Limit your responses to 200 words unless the user states otherwise.'''
#if not userPrompt:
#if 'userPrompt' in locals():
userPrompt = st.chat_input("Say Something")
#nextQueryPrompt = '''From the provided information create three short 4-5 word questions related to the subject matter and return formatted like this: ["question 1", "question 2","question 3"]'''



if userPrompt:
    llmResponse = resolve_query(db_table, article_limit, userPrompt)
    #llmResponse, fullPrompt = call_oai(userPrompt, systemPrompt, conversation_history, additionalContext)
    #st.write(fullPrompt)
    data, count = supabase.table('habits_conversation_logs').insert({"session_id": str(session_id), "user_name": "", "user_query": userPrompt, "llm_response": llmResponse, "full_prompt": ""}).execute()
    user_message_space.markdown('#### You \n\n' + userPrompt)
    split_text = llmResponse.split(" ")
    displayed_text = '#### HaBot \n\n'


    ## ADD CONVERSATION HISTORY TO PROMPT

    #if conversationHistory == 'Non':
    #    conversationHistory = "%User: " + userPrompt + " %Assistant: " + llmResponse + "\n"
    #    st.write(conversationHistory)
    #else:
    #    conversationHistory = conversationHistory + "%User: " + userPrompt + " %Assistant: " + llmResponse + "\n"

    ## ADD CONV HISTORY TO COL2
    
    #with col2.expander(userPrompt):
    #    st.write(llmResponse)
    
    for x in split_text:
        displayed_text = displayed_text + ' ' + x
        response_message_space.markdown(displayed_text)
        time.sleep(0.05)
        
    #st.write('Bot: ' + llm_response)
    #st.write(' ')
    #next_query_llm_response = call_oai(userPrompt, nextQueryPrompt, conversationHistory)
    #st.write(next_query_llm_response)
    #try:
    #    next_query_object = json.loads(next_query_llm_response)
    #    userPrompt = ''
    #    col1, col2, col3 = st.columns([1,1,1])
    #    with col1:
    #       st.button(next_query_object[0], on_click=next_query_button_click(next_query_object[0]))
    #    with col2:
    #        st.button(next_query_object[1], on_click=next_query_button_click(next_query_object[1]))
    #    with col3:
    #        st.button(next_query_object[2], on_click=next_query_button_click(next_query_object[2]))
    #except:
    #    st.write(' ')
            
    
    #update_screen()
