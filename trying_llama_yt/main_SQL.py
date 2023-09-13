# Import necessary libraries
import streamlit as st
import replicate
import os
import time
import gspread
from google.oauth2.service_account import Credentials

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
st.set_page_config(page_title="HTHC AI 🔴⚪️")

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

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.image('trying_llama_yt/icon white.png', width=50)

# Session state variable to control the visibility of the chatbot and information box
if 'show_chatbot' not in st.session_state:
    st.session_state['show_chatbot'] = False
if 'show_info' not in st.session_state:
    st.session_state['show_info'] = True

# Button to toggle both chatbot and information box visibility
toggle_button = st.button("Hide/show rules box")

# Toggle visibility based on button click
if toggle_button:
    st.session_state['show_info'] = not st.session_state['show_info']
    st.session_state['show_chatbot'] = not st.session_state['show_chatbot']

# Display the information box when 'show_info' is True
if st.session_state['show_info']:
    st.markdown("### Rules Box and privacy policy")
    st.write("The rules: "
             "Use this as a chatbot. Prompt it to give a creative output about health tech. ")
    st.write("3 RANDOM and 2 CREATIVE submissions win a HTHC Waterbottle for each day of TechBBQ 💧")
    st.write("Creativity is measured by originality and ability to think outside the box")
    st.write("By submitting, you accept HTHC's [privacy policy](https://healthtechhub.org/privacy-policy/) and sign up for our monthly newsletter")
    st.write("")
    st.write("PRESS THE BUTTON ABOVE AND START PROMPTING!")

# Display the chatbot section when 'show_chatbot' is True
if st.session_state['show_chatbot']:

    # Store LLM generated responses in session state
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "Let me help you be creative. Type your idea below in the textbox at the buttom👇 You might need to scroll"}]

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


    # Add a button to clear the form fields
    #st.button('Clear Chat History', on_click=clear_form)


    # Function for generating LLaMA2 response
    def generate_llama2_response(prompt_input):
        # Build the string dialogue by combining user and assistant messages
        string_dialogue = "You are a marketing manager from Health Tech Hub Copenhagen. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'. Health Tech Hub Copenhagen's catchphrase is Making Health Tech Everyones Business. Here is info about our members: Brain+ aims to restore independence and quality of life in Alzheimer's and dementia patients through evidence-based digital medicine software, offering cognitive stimulation therapy as its initial product. Cerebriu automates MRI for optimized workflows and enhanced care quality. Hi Rasmus offers a digital health platform enhancing autism treatment with a personal touch. Injurymap provides personal exercise programs for muscle and joint pain treatment. Liva Healthcare delivers scalable personal health programmes for lifestyle and chronic disease management. KHORA provides VR and AR solutions, including therapies for schizophrenia and exposure therapy tools. HelloMind offers a user-friendly app for self-help through hypnotherapy and other psychological tools. Patient Journey App enhances patient care through an interactive timeline and data collection. Welldium facilitates high-quality supplement recommendations by practitioners. Briota uses AI to simplify the management of Chronic Respiratory Ailments post-Covid-19. Lenus aids health and fitness professionals in achieving scalable online business. Hedia develops digital tools for improved diabetes management. Apoteka aims to eliminate medication errors through a digital pharmacy platform. Monsenso offers a digital health solution for better and cost-effective mental health care. Visikon specializes in digital health communication combining technology with clinical knowledge. Ward 24/7 is an AI-based system for early detection and prevention of critical complications in hospitals. Epital Health offers technology solutions for better management of chronic patients. Enversion focuses on improving well-being through data platforms and solution transformation in healthcare. Hejdoktor.dk is under development. Howdy is a digital solution for monitoring employee well-being, offering early detection of declining well-being and providing corresponding support and insights to employers. STUDIES&ME: A digital Contract Research Organization (CRO) platform accelerating treatment development through decentralized clinical study designs, improving retention and data quality, and reducing market entry time and costs. | SYNCVR: A social enterprise offering a VR/AR platform with an XR App Store for healthcare organizations in Europe, enhancing healthcare through scientifically validated and CE certified XR apps. | RADIOBOTICS: A technology company utilizing AI and Machine Learning to revolutionize x-ray processing and reporting, aiming to provide affordable, expert-level diagnosis through quick and automated analysis of x-ray images. | TETON.AI: A tech company aiming to alleviate pressure on global care staff through contactless monitoring and deep learning algorithms, fostering better clinical insights and work environments. | CORTI: An AI tool that assists in real-time during 911 calls, analyzing and providing critical feedback, facilitating quality improvement and reducing liabilities. | SELFBACK: A CE-certified digital therapeutics solution offering personalized treatment plans for Low Back Pain, enhancing treatment quality through AI and data monitoring. | MIISKIN: A secure and HIPAA-compliant skin health platform offering services to research organizations, health systems, and dermatology practices. | SANI NUDGE: A platform solution aiding healthcare organizations in enhancing safety and reducing operational costs through intelligent sensor networks and actionable insights. | HEALTHBUDDY: A patient empowerment platform offering disease-specific solutions, including the flagship product RheumaBuddy for Rheumatoid Arthritis. | HEKA VR: A therapeutic solution combining psychotherapy, avatar therapy, and virtual reality to assist patients in combating auditory hallucinations through personalized treatment and fewer side effects. | OSAIA HEALTH: An initiative offering support and AI for all to optimize the diagnosis and treatment of osteoporosis through an app, advisory service, and educational platform. | EVIDO.HEALTH: A new digital diagnostic platform to detect chronic liver diseases early on, utilizing standard biomarkers for a more precise risk stratification at initial patient contact."
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

    # Check if the form should be visible
    if 'show_form' not in st.session_state:
        st.session_state['show_form'] = False

    # Create a button to toggle the visibility of the form
    if st.button('Finnished prompting and ready to submit? Click here'):
        st.session_state['show_form'] = not st.session_state['show_form']

    # Placeholder to hold the form
    form_placeholder = st.empty()

    submit_button = None  # or submit_button = False


    #    # If the button has been pressed, show the form
    #    if st.session_state['show_form']:
    #        with form_placeholder.form(key='entry_form'):
    #            st.header("please fill out below")
    #            participant_name = st.text_input("Name")
    #            participant_email = st.text_input("Email")
    #            participant_entry = st.text_area("Your Creative Text", value=st.session_state.get('latest_response', ''))
    #            submit_button = st.form_submit_button(label='Submit Entry')

    # If the button has been pressed, show the form
    if st.session_state['show_form']:
        with form_placeholder.form(key='entry_form'):
            st.header("please fill out below")
            participant_name = st.text_input("Name", value=st.session_state.get('participant_name', ''))
            participant_email = st.text_input("Email", value=st.session_state.get('participant_email', ''))
            participant_entry = st.text_area("Your Creative Text (feel free to edit it as needed)", value=st.session_state.get('latest_response', ''))
            if st.form_submit_button(label='Submit Entry'):
                data_dict = {'Name': participant_name, 'Email': participant_email, 'Creative Text': participant_entry}

                # Add a new row to the Google Sheets document
                worksheet.append_row([data_dict['Name'], data_dict['Email'], data_dict['Creative Text']])

                st.success('Submitted, thank you! Look for it on the screen when the slide changes🥳')

                clear_form()

                for i in range(5, 0, -1):
                    st.write(f"New session in: {i}")
                    time.sleep(1)

                st.experimental_rerun()


