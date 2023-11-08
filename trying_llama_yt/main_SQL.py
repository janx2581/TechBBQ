# Import necessary libraries
import streamlit as st
import replicate
import os
import time
import gspread
from google.oauth2.service_account import Credentials
from HTHC_dialogue_TechBBQ import string_HTHC_dialogue
from Smartcloud_dialogue import string_Smartcloud_dialogue

import pandas as pd
from openpyxl import load_workbook, Workbook # Import openpyxl

# Set the Replicate API token
#os.environ["REPLICATE_API_TOKEN"] = "your_token_here"
os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]

# Secrets work

service_account_json = {
  "type": st.secrets["type"],
  "project_id": st.secrets["project_id"],
  "private_key_id": st.secrets["private_key_id"],
  "private_key": st.secrets["private_key"],
  "client_email": st.secrets["client_email"],
  "client_id": st.secrets["client_id"],
  "auth_uri": st.secrets["auth_uri"],
  "token_uri": st.secrets["token_uri"],
  "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
  "client_x509_cert_url": st.secrets["client_x509_cert_url"],
  "universe_domain": st.secrets["universe_domain"]
}

#For local use
#credentials = Credentials.from_service_account_file('/Users/janhoegh/Documents/GitHub/TechBBQ/trying_llama_yt/techbbq-test-06079fa24115.json', scopes=scope)

# Initialize Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']
credentials = Credentials.from_service_account_info(service_account_json, scopes=scope)
client = gspread.authorize(credentials)
spreadsheet = client.open('HTHC-techbbq-sheet')
worksheet = spreadsheet.get_worksheet(0)

# Set the title of the app
st.set_page_config(page_title="HTHC AI 🔴⚪️", initial_sidebar_state="expanded")


# Set sidebar
with st.sidebar:
    st.title('Welcome to the HTHC AI chatbot️')
    st.markdown('A demo for Schultz Jørgensen Kom')
    st.markdown('📖 Learn more about Health Tech Hub Copenhagen [here](https://healthtechhub.org/)!')
    st.markdown('*Read about Health Tech Hub Copenhagens privacy policy [here](https://healthtechhub.org/privacy-policy/)*')

# Add a button to clear chat history in the sidebar
### Function to clear chat history
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Let me help you be creative. Type your idea below👇"}]
    st.session_state['latest_response'] = ""
    st.session_state['show_form'] = False
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)


# Add custom CSS styling to the app
st.markdown("""
    <style>
        body { font-family: 'Times New Roman', sans-serif; line-height: 1.5; }
        .stTextInput input { background-color: #000000; color: #FFFFFF; border: 1px solid #FF0808; }
        .stButton>button { background-color: #FF0808; border: none; color: #FFFFFF; }
        .st-chat-messages { border: none; }
        .stChatInput { background-color: #FF0808; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
        .reportview-container::before {
            content: none;
        }
    </style>
    """, unsafe_allow_html=True)


st.image('trying_llama_yt/icon white.png', width=50)
st.title('🔴⚪ Welcome to the HTHC AI chatbot ⚪🔴')


# Store LLM generated responses in session state
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Ask me questions about Health Tech Hub Copenhagen! Use the textbox below 👇"}]


st.write('<p style="text-align: center;">', unsafe_allow_html=True)

if st.button('What is the value prop for member startups?'):
    prompt = "What is the value prop for member startups?"
    st.session_state.messages.append({"role": "user", "content": prompt})

if st.button('Who is HTHCs partners?'):
    prompt = "Who is HTHC's partners?"
    st.session_state.messages.append({"role": "user", "content": prompt})

if st.button('Who is Jan Høegh?'):
    prompt = "Who is Jan Høegh?"
    st.session_state.messages.append({"role": "user", "content": prompt})

if st.button('Explain HTHC to an Investor'):
    prompt = "Explain HTHC to an investor"
    st.session_state.messages.append({"role": "user", "content": prompt})

st.write('</p>', unsafe_allow_html=True)

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

### Function to clear chat history

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Let me help you be creative. Type your idea below👇"}]
    st.session_state['latest_response'] = ""
    st.session_state['show_form'] = False

# Function to clear the form
# Initialize session state variables for the form fields
if 'participant_name' not in st.session_state:
    st.session_state['participant_name'] = ""
if 'participant_email' not in st.session_state:
    st.session_state['participant_email'] = ""
if 'participant_entry' not in st.session_state:
    st.session_state['participant_entry'] = st.session_state.get('latest_response', '')

# Function to clear the form fields
def clear_form():
    st.session_state['participant_name'] = ""
    st.session_state['participant_email'] = ""
    st.session_state['latest_response'] = ""
    st.session_state['participant_entry'] = st.session_state.get('latest_response', '')
    st.session_state['show_form'] = False
    clear_chat_history()

# Function for generating LLaMA2 response
def generate_llama2_response(prompt_input):
    # Build the string dialogue by combining user and assistant messages
    string_dialogue = "Du er en politisk ekspert"
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"

    # Generate LLaMA2 response using the replicate.run() function
    output = replicate.run(
        # 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5', # The 13B parameter model
        "meta/llama-2-70b-chat:35042c9a33ac8fd5e29e27fb3197f33aa483f72c2ce3b0b9d201155c7fd2a287", # The 70B parameter model
        input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ",
               "temperature": 0.1, "top_p": 0.9, "max_length": 2000, "repetition_penalty": 1})
    # Get the output as a string
    output = ''.join(output)


    # Check if the response has been trimmed
    if not output.endswith(('.', '!', '?')):
        sentences = output.split('.')
        if len(sentences) > 1:
            output = '.'.join(sentences[:-1]) + '.'
            #output += ' (_Response has been trimmed. Please write "continue" to get the rest_)' and remember to put ... above
    return output

# Get user input prompt using st.chat_input()
if prompt := st.chat_input(disabled=not os.environ['REPLICATE_API_TOKEN'], placeholder="PROMPT HTHC'S AI HERE 🔴⚪️"):
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if the last message is not from the assistant
if st.session_state.messages and st.session_state.messages[-1]["role"] != "assistant": # Changed something here
    with st.chat_message("Assistant"):
        with st.spinner("Thinking..."):
            # Generate LLaMA2 response using the generate_llama2_response() function
            response = generate_llama2_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
    st.session_state['latest_response'] = full_response  # Store the latest response in session state
    st.session_state['show_form'] = False