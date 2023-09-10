import streamlit as st
import sqlite3
import pandas as pd
from streamlit_autorefresh import st_autorefresh
import time

st.markdown("""
    <style>
        table {width:100%;}
        th {font-size:1em;}
        td {font-size:1em; white-space: pre-wrap; word-wrap: break-word;}
    </style>
""", unsafe_allow_html=True)

st.title('Submission Viewer')

countdown_time = 5  # Adjust the countdown time as per your requirements
countdown_timer = st.empty()

page_number = st.empty()
table = st.empty()

def get_total_entries():
    conn = sqlite3.connect('submissions.db')
    total_entries = pd.read_sql_query("SELECT COUNT(*) FROM submissions", conn).iloc[0, 0]
    conn.close()
    return total_entries

def load_data(offset, limit):
    conn = sqlite3.connect('submissions.db')
    query = f"SELECT * FROM submissions LIMIT {limit} OFFSET {offset}"
    data = pd.read_sql_query(query, conn)
    data = data.drop(columns=['id', 'name', 'email'])  # Dropping the specified columns
    conn.close()
    return data

total_entries = get_total_entries()
current_page = 0

PAGE_SIZE = 5  # Set this to the number of rows you want to display on each page

while True:
    offset = current_page * PAGE_SIZE
    data = load_data(offset, PAGE_SIZE)

    if data.empty and current_page != 0:
        current_page = 0
    else:
        page_number.markdown(f"### Page: {current_page + 1}/{(total_entries // PAGE_SIZE) + 1}")
        table.table(data)
        current_page += 1

    # time.sleep(5)
    for i in range(countdown_time, 0, -1):
        countdown_timer.write(f"Next slide in: {i} seconds", unsafe_allow_html=True)
        time.sleep(1)
        countdown_timer.empty()

