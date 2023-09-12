import streamlit as st
import sqlite3
import pandas as pd
from streamlit_autorefresh import st_autorefresh
import time
from google.oauth2 import service_account
import gspread
from google.oauth2.service_account import Credentials

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

#Scope
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']

# Credentials
credentials = Credentials.from_service_account_info(service_account_json, scopes=scope)
client = gspread.authorize(credentials)

st.set_page_config(page_title="User submissions", layout="wide")

st.markdown("""
    <style>
        table {width:100%;}
        th {font-size:1.1em;}
        td {font-size:1.5em; white-space: pre-wrap; word-wrap: break-word;}
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        table {
            border: 2px solid white;
        }
        th, td {
            border: 2px solid white !important;
        }
    </style>
""", unsafe_allow_html=True)



st.title('🔴⚪ User submissions for HTHC AI competition! 🔴⚪️')
st.markdown('<h2 style="font-size:1.5em;">Create something creative about healthtech! Scan the QR code below</h2>', unsafe_allow_html=True)
st.markdown('<h2 style="font-size:1em;">(I need to make this a bit more pretty)</h2>', unsafe_allow_html=True)
st.image('trying_llama_yt/icon white.png', width=50)

new_entry_display = st.empty()  # Move this line up to reserve space for the new entry above the table


countdown_time = 10  # Adjust the countdown time as per your requirements
countdown_time_new_entry = 20  # Adjust the countdown time as per your requirements
countdown_timer = st.empty()

page_number = st.empty()
table = st.empty()  # A container for the table

def get_total_entries():
    spreadsheet = client.open('HTHC-techbbq-sheet')
    worksheet = spreadsheet.get_worksheet(0)  # Assuming data is in the first worksheet
    total_entries = len(worksheet.get_all_values()) - 1  # Subtract 1 to exclude header row
    return total_entries

total_entries = get_total_entries()
current_page = 0

PAGE_SIZE = 5  # Set this to the number of rows you want to display on each page


def load_data(offset, limit):
    spreadsheet = client.open('HTHC-techbbq-sheet')
    worksheet = spreadsheet.get_worksheet(0)  # Assuming data is in the first worksheet
    data = worksheet.get_all_values()
    if data:
        df = pd.DataFrame(data[1:], columns=data[0])  # Convert data to pandas DataFrame
        df.drop(df.columns[[0, 1]], axis=1, inplace=True)  # Drop the first two columns
    else:
        df = pd.DataFrame()
    return df


previous_total_entries = get_total_entries()

while True:
    total_entries = get_total_entries()


    if total_entries > previous_total_entries:
        # A new entry has been added
        spreadsheet = client.open('HTHC-techbbq-sheet')
        worksheet = spreadsheet.get_worksheet(0)
        total_entries = get_total_entries()

        new_entry = worksheet.get('c' + str(total_entries+1))  # Get the new entry
        if new_entry:
            new_entry_text = new_entry[0][0].replace('\n', '<br>')
        else:
            new_entry_text = ""


        for i in range(countdown_time_new_entry, 0, -1):
            countdown_timer.write(f"{i} seconds", unsafe_allow_html=True)
            time.sleep(1)
            countdown_timer.empty()

            # Display the new entry prominently
            st.markdown('<h2 style="font-size:1em;"><i>New Entry:</i></h2>',
                        unsafe_allow_html=True)
            new_entry_display.markdown(
                f"<div style='font-size:3em;'>{new_entry_text}</div>",
                unsafe_allow_html=True)

        # Clear the new entry display
        new_entry_display.empty()

        previous_total_entries = total_entries

    offset = current_page * PAGE_SIZE
    data = load_data(offset, PAGE_SIZE)

    display_data = data[offset:offset + PAGE_SIZE]

    if display_data.empty and current_page != 0:
        current_page = 0
    else:
        page_number.markdown(
            f'<p style="font-size:0.8em;">Page: {current_page + 1}/{(total_entries // PAGE_SIZE) + 1}</p>',
            unsafe_allow_html=True)
        table.table(display_data)
        current_page += 1

    for i in range(countdown_time, 0, -1):
        countdown_timer.write(f"Next slide in: {i} seconds", unsafe_allow_html=True)
        time.sleep(1)
        countdown_timer.empty()
