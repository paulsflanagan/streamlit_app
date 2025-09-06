import streamlit as st
from supabase import create_client, Client
from io import StringIO
from pypdf import PdfReader 
import requests
import time
import json
import uuid
import os
from openai import OpenAI
#from openai import AzureOpenAI


## GLOBAL Settings
global_resolution_prompt_version = 1
global_max_articles = 2
global_temperature = 0.4
global_model = "openai/gpt-oss-120b"



######### THINGS TO IMPROVE






# Custom CSS for modern chat interface
st.markdown("""
<style>
    .main-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    .chat-widget {
        background: white;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        padding: 0;
        margin: 2rem auto;
        max-width: 600px;
        border: 1px solid #e5e7eb;
    }
    
    .chat-header {
        background: #f8fafc;
        border-radius: 16px 16px 0 0;
        padding: 1.5rem;
        border-bottom: 1px solid #e5e7eb;
        text-align: center;
    }
    
    .chat-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1f2937;
        margin: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    
    .chat-subtitle {
        font-size: 0.875rem;
        color: #6b7280;
        margin: 0.25rem 0 0 0;
    }
    
    .chat-body {
        padding: 1.5rem;
    }
    
    .chat-description {
        text-align: center;
        color: #6b7280;
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
        line-height: 1.5;
    }
    
    .suggestion-buttons {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        margin-bottom: 1.5rem;
    }
    
    .suggestion-btn {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        text-align: left;
        color: #374151;
        font-size: 0.875rem;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .suggestion-btn:hover {
        background: #f3f4f6;
        border-color: #d1d5db;
    }
    
    .chat-input-container {
        position: relative;
        margin-top: 1rem;
    }
    
    .chat-input {
        width: 100%;
        padding: 0.75rem 3rem 0.75rem 1rem;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        font-size: 0.875rem;
        background: #f9fafb;
    }
    
    .send-button {
        position: absolute;
        right: 0.5rem;
        top: 50%;
        transform: translateY(-50%);
        background: #10b981;
        border: none;
        border-radius: 6px;
        width: 2rem;
        height: 2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        color: white;
    }
    
    .message-container {
        margin: 1rem 0;
        padding: 1rem;
        border-radius: 12px;
        max-width: 100%;
    }
    
    .user-message {
        background: #eff6ff;
        border: 1px solid #dbeafe;
        margin-left: 2rem;
    }
    
    .assistant-message {
        background: #f0fdf4;
        border: 1px solid #dcfce7;
        margin-right: 2rem;
    }
    
    .message-header {
        font-weight: 600;
        font-size: 0.875rem;
        margin-bottom: 0.5rem;
        color: #374151;
    }
    
    .message-content {
        color: #4b5563;
        line-height: 1.6;
    }
    
    .disclaimer {
        text-align: center;
        font-size: 0.75rem;
        color: #9ca3af;
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid #f3f4f6;
    }
    
    /* Hide Streamlit default elements */
    .stApp > header {
        background-color: transparent;
    }

        .stApp {
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%); /* Changed to black gradient */
        min-height: 100vh;
    }
    #.stApp {
     #   background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      #  min-height: 100vh;
    #}

    
    /* Custom input styling */
    .stTextInput > div > div > input {
        background: #f9fafb;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 0.75rem 1rem;
    }
</style>
""", unsafe_allow_html=True)





## Initialize Global Variables
global_messages = []


# --- 🤖 Groq Config ---
groq_key = st.secrets["groq_key"]
client = OpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1")


# --- Session ID
if 'key' not in st.session_state:
    st.session_state['key'] = uuid.uuid4()
    session_id = uuid.uuid4()
else:
    session_id = st.session_state['key']

# Initialize conversation history
if 'messages' not in st.session_state:
    st.session_state.messages = []




# --- Logging

def log(session_id, message):
    """ System log message"""
    data, count = supabase.table('habits_system_logs').insert({"session_id": str(session_id), "message": message}).execute()


def log_query(session_id, user_input, ai_response, global_messages, total_input_tokens, total_output_tokens, total_tokens):
    """ System log message"""
    data, count = supabase.table('habits_conversation_logs').insert({"session_id": str(session_id), "user_query": user_input, "llm_response": ai_response, "messages": global_messages, "input_tokens": total_input_tokens, "output_tokens": total_output_tokens, "total_tokens": total_tokens}).execute()



def call_gateway(system_prompt, assistant_prompt, user_prompt):
    """Calls the LLM Gateway with system, assistant, and user prompts."""
    try:
        messages = [
                {"role": "system", "content": system_prompt},
                {"role": "assistant", "content": assistant_prompt},
                {"role": "user", "content": user_prompt}
            ]
        response = client.chat.completions.create(
            model=global_model,
            messages=messages,
            temperature=global_temperature
        )
        
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        response = response.choices[0].message.content.strip()
        log(session_id, "Gateway Call Success: " + str(messages))
        log(session_id, "Response: " + response)
        return response, input_tokens, output_tokens
    except requests.exceptions.RequestException as e:
        log(session_id, "Gateway Call Failure: " + e)
        return e, 0, 0


def call_gateway_BYOM(messages_list):
    """Calls the LLM Gateway with a custom list of messages."""
    try:
        response = client.chat.completions.create(
            model=global_model,
            messages=messages_list,
            temperature=global_temperature
        )
        
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        response = response.choices[0].message.content.strip()
        log(session_id, "Successfully Called Gateway: " + str(messages_list))
        log(session_id, "Response: " + response)
        return response, input_tokens, output_tokens
    except requests.exceptions.RequestException as e:
        log(session_id, "Gateway Call Failure: " + e)
        return e, 0, 0

# Database setup
if 'supabase_initialized' not in globals():
    spb_key = st.secrets["spb_key"]
    spb_url = st.secrets["spb_url"]
    supabase: Client = create_client(spb_url, spb_key)
    db_table = 'website_scrape'
    supabase_initialized = True

# Database functions (keeping your existing functions)
def get_data_from_table(table_name):
    try:
        response = supabase.table(table_name).select("*").execute()
        return response.data
    except Exception as e:
        return None

def get_column_data_from_table(table_name, column_name):
    try:
        response = supabase.table(table_name).select('id', column_name).execute()
        return response.data
    except Exception as e:
        return None

def get_details_from_id_list(table_name, id_list):
    results = []
    for row_id in id_list:
        try:
            response = supabase.table(table_name).select('id', 'title', 'detail').eq('id', row_id).single().execute()
            if response.data:
                results.append(response.data)
        except Exception as e:
            return None
    return results

def knowledge_search(table_name, article_limit, query):
    titles = get_column_data_from_table(db_table, 'title')
    system_prompt = f"The list provided in CONTEXT contains titles to articles relating to Habits for a Better World and their projects. Return up to {article_limit} titles that are relevant to the users message. Return them in the following format: "
    system_prompt = system_prompt + """
    [
    {
    "id": ID,
    "title": "TITLE"
    },
    {
    "id": ID,
    "title": "TITLE"
    }
    ]
    """

    
    context = "CONTEXT: " + str(titles)
    response, input_tokens, output_tokens = call_gateway(system_prompt, context, query)
    
    id_list = []
    if response:
        if response.startswith("```json") and response.endswith("```"):
            json_string = response[len("```json"):len(response)-len("```")].strip()
        else:
            json_string = response.strip()
        
        try:
            response_data = json.loads(json_string)
            id_list = [item['id'] for item in response_data]
        except json.JSONDecodeError as e:
            log(session_id, "JSON Decoder Error: " + e)
            return e, 0, 0
        except TypeError as e:
            log(session_id, "Type Error: " + e)
            return e, 0, 0
    else:
        return None, 0, 0
    
    if id_list:
        knowledge_context = get_details_from_id_list(table_name, id_list), input_tokens, output_tokens
    else:
        knowledge_context = []
    return knowledge_context, input_tokens, output_tokens


def resolve_query(db_table, article_limit, query):
    
    global global_messages
    
    knowledge_context, input_tokens_kno, output_tokens_kno = knowledge_search(db_table, article_limit, query)

    response = supabase.table("habits_prompts").select("resolution_prompt").eq("id", global_resolution_prompt_version).execute()
    
    #system_prompt = f"You are a helpful assistant working for Habits for a Better World. Answer the users query using only information found in the CONTEXT provided. Answer in polite, professional and conversational manner. Feel free to elaborate using the context and provide email addresses or links where relevant. If you are unable to answer their query or their query is off topic, make a clean joke (maybe a pun on what they said) then playfully guide them back to talking about Habits for a Better World. CONTEXT: {knowledge_context}"
    system_prompt = response.data[0]["resolution_prompt"]
    system_prompt = system_prompt + " CONTEXT: " + str(knowledge_context)

    messages_list = [{"role": "system", "content": system_prompt}]
    messages_list.append({"role": "user", "content": query})

    global_messages = messages_list
    response, input_tokens_res, output_tokens_res = call_gateway_BYOM(messages_list)
    total_input_tokens = input_tokens_kno + input_tokens_res
    total_output_tokens = output_tokens_kno + output_tokens_res
    
    return response, total_input_tokens, total_output_tokens



# Main UI
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Chat Widget Container
st.markdown("""
<div class="chat-widget">
    <div class="chat-header">
        <div class="chat-title">
             HBW AI Assistant
        </div>
        <div class="chat-subtitle">
            Grounded in trusted HBW sources
        </div>
    </div>
    <div class="chat-body">
        <div class="chat-description">
            Ask a question about HBW programs, meet-ups, challenges, or healthy swaps.
        </div>
""", unsafe_allow_html=True)

# Suggestion buttons
suggestions = [
    "What is the habits for a better world about?",
    "what is plant based diet?",
    "Tell me about ocean advocacy?"
]

# Create columns for suggestion buttons
for suggestion in suggestions:
    if st.button(suggestion, key=f"suggestion_{suggestion}", help="Click to ask this question"):
        st.session_state.current_query = suggestion

# Display conversation history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="message-container user-message">
            <div class="message-header">You</div>
            <div class="message-content">{message["content"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="message-container assistant-message">
            <div class="message-header">HBW Assistant</div>
            <div class="message-content">{message["content"]}</div>
        </div>
        """, unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Ask anything... (Enter to send, Shift+Enter for a new line)")

# Handle suggestion button clicks
if 'current_query' in st.session_state:
    user_input = st.session_state.current_query
    del st.session_state.current_query

# Process user input
if user_input:
    log(session_id, "Query Initialized: " + user_input)
    # Add user message to conversation
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get AI response with token tracking
    with st.spinner("Thinking..."):
        ai_response, total_input_tokens, total_output_tokens = resolve_query(db_table, global_max_articles, user_input)
        
    
    # Add AI response to conversation
    if ai_response:
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        total_tokens = total_input_tokens + total_output_tokens

        log_query(session_id, user_input, ai_response, global_messages, total_input_tokens, total_output_tokens, total_tokens)
    else:
        error_message = "I'm sorry, I couldn't process your request at the moment. Please try again."
        st.session_state.messages.append({"role": "assistant", "content": error_message})
        total_input_tokens = 0
        total_output_tokens = 0
        total_tokens = 0

        log_query(session_id, user_input, ai_response, error_message, total_input_tokens, total_output_tokens, total_tokens)
        
    # Rerun to display the new messages
    st.rerun()

# Close the chat widget div
st.markdown("""
        <div class="disclaimer">
            AI can be wrong. For medical issues, consult a clinician.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Add a reset button in the sidebar
with st.sidebar:
    st.title("Chat Controls")
    if st.button("🔄 Reset Conversation"):
        st.session_state.messages = []
        st.session_state['key'] = uuid.uuid4()
        st.rerun()
    
    st.markdown("---")
    st.markdown("**Session ID:**")
    st.code(str(st.session_state['key'])[:8] + "...")
