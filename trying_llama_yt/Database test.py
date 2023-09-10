# Import necessary libraries
import streamlit as st
import replicate
import os

import pandas as pd
from openpyxl import load_workbook, Workbook # Import openpyxl

# Initialize an empty DataFrame
data = []

# Set the Replicate API token
os.environ["REPLICATE_API_TOKEN"] = "r8_bBCxqkUHTfwz818CIEtNtnojCT7yRZJ3gytkY"

# Set the title of the app
st.set_page_config(page_title="SQL HTHC AI 🔴⚪️")

# Add custom CSS styling to the app
st.markdown("""
    <style>
        .stApp { background-color: #000000; }
        body { font-family: 'Times New Roman', sans-serif; line-height: 1.5; color: #FFFFFF; }
        .stTextInput input { background-color: #000000; color: #FFFFFF; border: 1px solid #FF0808; }
        .stButton>button { background-color: #FF0808; border: none; }
        .st-chat-messages { border: none; }
    </style>
    """, unsafe_allow_html=True)

# Create a sidebar with some information
with st.sidebar:
    st.title('Welcome to the HTHC AI chatbot 🔴⚪️')
    st.markdown('It is called Health Tech Hygge AI')
    st.markdown('📖 Learn more about Health Tech Hub Copenhagen [here](https://healthtechhub.org/)!')

# Store LLM generated responses in session state
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "content creator", "content": "Let me help you be creative"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

### Function to clear chat history

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Let me help you be creative. Type your idea below👇"}]

# Add a button to clear chat history in the sidebar
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)


# Function for generating LLaMA2 response
def generate_llama2_response(prompt_input):
    # Build the string dialogue by combining user and assistant messages
    string_dialogue = "You are a creative content creator from Health Tech Hub Copenhagen. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'. Health Tech Hub Copenhagen's catchphrase is Making Health Tech Everyones Business"
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
               "temperature": 0.1, "top_p": 0.9, "max_length": 1024, "repetition_penalty": 1})
    # Get the output as a string
    output = ''.join(output)

    # Ensure the output ends with a complete sentence
    if not output.endswith(('.', '!', '?')):
        sentences = output.split('.')
        if len(sentences) > 1:
            output = '.'.join(sentences[:-1]) + '.'

    return output

# Get user input prompt using st.chat_input()
if prompt := st.chat_input(disabled=not os.environ['REPLICATE_API_TOKEN']):
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if the last message is not from the assistant
if st.session_state.messages[-1]["role"] != "assistant":
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

# Check if the form should be visible
if 'show_form' not in st.session_state:
    st.session_state['show_form'] = False

# Create a button to toggle the visibility of the form
if st.button('Ready to submit? Click here'):
    st.session_state['show_form'] = not st.session_state['show_form']

# Placeholder to hold the form
form_placeholder = st.empty()

submit_button = None  # or submit_button = False

# If the button has been pressed, show the form
if st.session_state['show_form']:
    with form_placeholder.form(key='entry_form'):
        st.header("please fill out below")
        participant_name = st.text_input("Name")
        participant_email = st.text_input("Email")
        participant_entry = st.text_area("Your Creative Text", value=st.session_state.get('latest_response', ''))
        submit_button = st.form_submit_button(label='Submit Entry')


### Data base

import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('submissions.db')

# Create a new SQLite cursor
cur = conn.cursor()

# Create a new table with the name 'submissions'
cur.execute("""
    CREATE TABLE IF NOT EXISTS submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        creative_text TEXT
    )
""")

# Commit the changes and close the connection
conn.commit()
conn.close()

if submit_button:
    data_dict = {'Name': participant_name, 'Email': participant_email, 'Creative Text': participant_entry}

    conn = sqlite3.connect('submissions.db')
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO submissions (name, email, creative_text)
        VALUES (?, ?, ?)
    """, (data_dict['Name'], data_dict['Email'], data_dict['Creative Text']))

    conn.commit()
    conn.close()

    st.success('Entry submitted and saved to submissions.db')
