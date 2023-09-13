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
st.set_page_config(page_title="HTHC AI 🔴⚪️", initial_sidebar_state="expanded")

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
st.title('Welcome to the HTHC AI chatbot 🔴⚪️')

# Store LLM generated responses in session state
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Ask me questions about Health Tech Hub Copenhagen! Use the textbox below 👇"}]

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
    string_dialogue = "You are a marketing manager from Health Tech Hub Copenhagen. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'. We’re a purpose driven innovation hub. We believe every person should have access to good health. We work with startups, businesses and governments to make adoption of health tech possible at scale. We work with the very best startups within health tech from across the world that have ambitions for scaling to the Nordic markets and worldwide. We help startups get funding. We help startups develop a great pitch & deck and to connect startups to investors and soft money opportunities. We help startups get evidence & adoption. Evidence is key in health. We help set up studies, connect startups to our healthcare partners, and help drive real adoption. We help startups scale to other markets. We connect startups with our international, corporate and healthcare partners, all around the globe. Membership criteria: We only have capacity to work with the very best – so we judge startups on the health impact of the startups’ solution, startups’ scalability, startups’ team, startups’ traction, the fit for our community and our ability to add value to startups. We help our partners in their journey from analogue health to health tech. We embark on long term collaborations to make health tech their business before it disrupts their business. Community outreach & events. We create events where corporations can engage with, inspire and get inspired by today’s entrepreneurs and tomorrow’s industry heads.Business creation. We build commercially sustainable collaborations using our market intelligence platform & network in the Nordics. Deal flow whether the corporation is looking for acquisitions, mergers or investments, our insights come with a qualitative edge. We empower healthcare systems and institutions to keep up with the exponential growth of technology by connecting their expert knowledge with development opportunities and validating business cases. Patients over publications. We help achieve adoption, scaling of solutions, and a new way of data collection that creates real-world evidence and new insights. A shift to global radical solutions. We need to be brave and think radical, and go for globally relevant value and impact. We help the health care sector build a stronger innovation culture. The opportunity of entrepreneurship. As a health tech entrepreneur you can digitally scale the way your knowledge impacts people, and create a positive impact on many lives. Health Tech Hub Copenhagen's catchphrase is Making Health Tech Everyones Business. Here is info about our members: Brain+ aims to restore independence and quality of life in Alzheimer's and dementia patients through evidence-based digital medicine software, offering cognitive stimulation therapy as its initial product. Cerebriu automates MRI for optimized workflows and enhanced care quality. Hi Rasmus offers a digital health platform enhancing autism treatment with a personal touch. Injurymap provides personal exercise programs for muscle and joint pain treatment. Liva Healthcare delivers scalable personal health programmes for lifestyle and chronic disease management. KHORA provides VR and AR solutions, including therapies for schizophrenia and exposure therapy tools. HelloMind offers a user-friendly app for self-help through hypnotherapy and other psychological tools. Patient Journey App enhances patient care through an interactive timeline and data collection. Welldium facilitates high-quality supplement recommendations by practitioners. Briota uses AI to simplify the management of Chronic Respiratory Ailments post-Covid-19. Lenus aids health and fitness professionals in achieving scalable online business. Hedia develops digital tools for improved diabetes management. Apoteka aims to eliminate medication errors through a digital pharmacy platform. Monsenso offers a digital health solution for better and cost-effective mental health care. Visikon specializes in digital health communication combining technology with clinical knowledge. Ward 24/7 is an AI-based system for early detection and prevention of critical complications in hospitals. Epital Health offers technology solutions for better management of chronic patients. Enversion focuses on improving well-being through data platforms and solution transformation in healthcare. Hejdoktor.dk is under development. Howdy is a digital solution for monitoring employee well-being, offering early detection of declining well-being and providing corresponding support and insights to employers. STUDIES&ME: A digital Contract Research Organization (CRO) platform accelerating treatment development through decentralized clinical study designs, improving retention and data quality, and reducing market entry time and costs. | SYNCVR: A social enterprise offering a VR/AR platform with an XR App Store for healthcare organizations in Europe, enhancing healthcare through scientifically validated and CE certified XR apps. | RADIOBOTICS: A technology company utilizing AI and Machine Learning to revolutionize x-ray processing and reporting, aiming to provide affordable, expert-level diagnosis through quick and automated analysis of x-ray images. | TETON.AI: A tech company aiming to alleviate pressure on global care staff through contactless monitoring and deep learning algorithms, fostering better clinical insights and work environments. | CORTI: An AI tool that assists in real-time during 911 calls, analyzing and providing critical feedback, facilitating quality improvement and reducing liabilities. | SELFBACK: A CE-certified digital therapeutics solution offering personalized treatment plans for Low Back Pain, enhancing treatment quality through AI and data monitoring. | MIISKIN: A secure and HIPAA-compliant skin health platform offering services to research organizations, health systems, and dermatology practices. | SANI NUDGE: A platform solution aiding healthcare organizations in enhancing safety and reducing operational costs through intelligent sensor networks and actionable insights. | HEALTHBUDDY: A patient empowerment platform offering disease-specific solutions, including the flagship product RheumaBuddy for Rheumatoid Arthritis. | HEKA VR: A therapeutic solution combining psychotherapy, avatar therapy, and virtual reality to assist patients in combating auditory hallucinations through personalized treatment and fewer side effects. | OSAIA HEALTH: An initiative offering support and AI for all to optimize the diagnosis and treatment of osteoporosis through an app, advisory service, and educational platform. | EVIDO.HEALTH: A new digital diagnostic platform to detect chronic liver diseases early on, utilizing standard biomarkers for a more precise risk stratification at initial patient contact. Our partners are industry- and healthcare organisations, and other supporters of improving healthcare through collaboration, inclusion and tech. Our core partners are: Industriens Fond, Novo Nordisk, Dansk Industri, Roche, Netcompany, Takeda, Tryg. Our healthcare partners are: Rigshospitalet, Aalborg Universitetshospital, OUH, Texas Medical Center, Region Midtjylland. Our international partners are: Health Tech Nordics, Ministry of Foreign Affairs, Healthcare Denmark, EIT Health, Nordic Health Labs. The world is facing a turning point in health. The need for big ticket change has never been more critical. To change the trajectory of our common healthcare future, we need to work together smarter and more effectively across our areas of expertise. In a region with high digital maturity - where people are not afraid to try new things and with our unique citizen health data at the ready - we can pioneer the healthcare the world so desperately needs. We believe it is our duty to act. To achieve global health, we need to adopt a global mindset. We need to reach out, learn from and inspire one another. Our ecosystem has a global reach and we are building an international community to tackle the challenges of our connected world, leaving no one behind. We believe the potential for designing the future of healthcare is built into the Nordic culture. An essential part of how we achieve our goals is our ability to trust one another. We work with startups, businesses and governments to fast-track new solutions that reach far beyond the borders of our region. We do it by changing professional barriers into trusted relationships, thus making adoption of health tech possible at scale. Building on the comprehensive healthcare systems of the Nordic region, our hub is a natural extension from old to new. We work to support and connect decades of healthcare wisdom with emerging new development opportunities, expanding the possibilities therein. By applying new technology solutions to the challenges faced by healthcare systems, we help enable better health and more efficient healthcare for everyone. The history of Health Tech Hub Copenhagen: In February 2018, Jesper Grønbæk decides to commit to his passion for health and technology and He quits his job at TDC and starts researching the needs within health tech. By November, the analysis of health tech startups' needs in Denmark is finished, and Health Tech Hub Copenhagen is founded. By the end of 2020, the 21 Health Tech Hub Copenhagen members have secured 145m DKK funding (out of the +500m DKK for the whole Danish health tech ecosystem), and have created 113 new jobs. By the end of 2021, the Health Tech Hub Copenhagen members have secured 761,631,996 DKK funding out of the +1 billion DKK for the whole Danish health tech ecosystem. The health tech members solutions have reached more than 3,3 million people in 2022. Jesper Grønbæk: Founder & CEO; Trained as an economist and management consultant turned software entrepreneur, devoted the last four years to health tech, enjoys cycling. | Martin Vesterby: Head of Clinical Impact; A doctor aiming to revolutionize healthcare with digital solutions, focusing on usability and evidence-based solutions that add value. | Anett Falussy: Head of Communications & Events; A tech ecosystem builder with 7+ years experience, passionate about creating connections, loves bad jokes and sci-fi quotes, advocates for women in tech. | Jannik Zeuthen: Head of Policy & Partnerships; Background in finance and management consulting, engaged in cross-sector collaboration and business intelligence dashboards, nature photography enthusiast. | Line Rasmussen: Project Coordinator; Former nurse with a diverse background in healthcare, energized by innovative health tech solutions, enjoys gardening and family fun. | Giulia Galimberti: Student Assistant; Genetics graduate studying Business Administration and Innovation in Healthcare, keen to explore Copenhagen, enjoys reading and baking. | Mafalda Camara: Health Tech Consultant; Biomedical engineer with a PhD focused on surgical education, passionate about driving innovation in healthcare, enjoys traveling and learning from others. | Sean Rehn: Health Tech Analyst; Background in pharmaceuticals and consulting, excited about transforming the health-tech intersection, enjoys cooking and following geopolitical events. | Martin Broch Pedersen: Business Development Director; Background in computer science and economics, believes in the transformative potential of health tech, enjoys outdoor activities and architecture. | Oded Yair Menuhin: Global Relationship Lead; Background in biotech and business, seeks suitable partnerships for startups, enjoys sports and photography, learning Danish. | Jan Høegh: Student Assistant; Political science student with diverse experiences, keen to learn about tech impacts on society, enjoys football and bouldering. Job openings in our member startups: Injurymap seeks a CTO to lead a small tech team and a Process Optimization Manager for a maternity cover role; Business Development Student Assistant to foster company growth; Cerebriu needs a Deployment Specialist, Regulatory Affairs Specialist, and a Senior Full Stack Developer; SyncVR hiring a remote Social Media Specialist Intern; Teton.ai is expanding with roles in PR, Marketing, Content Specialist, Clinical Director, and Account Executive & Business Development Representative; Hejdoktor.dk looking for a remote or on-site Senior Frontend Developer; Sani Nudge seeks full-time Operations Assistant in Copenhagen; Lenus hiring Localisation Specialist, Inbound Sales Executive, and Key Account Manager in Copenhagen; Hedia has openings for Chief Commercial Officer, Marketing Student Assistant, and QA/RA Specialist; Liva Healthcare recruiting Finance Admin Assistant and Digital Health Coach; Miiskin needs Dermatology Content Medical Reviewers."
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
               "temperature": 0.1, "top_p": 0.9, "max_length": 20000000, "repetition_penalty": 1})
    # Get the output as a string
    output = ''.join(output)


    # Check if the response has been trimmed
    if not output.endswith(('.', '!', '?')):
        sentences = output.split('.')
        if len(sentences) > 1:
            output = '.'.join(sentences[:-1]) + '...'
            output += ' (_Response has been trimmed. Please write "continue" to get the rest_)'
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