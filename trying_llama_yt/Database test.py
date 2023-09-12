consent = st.checkbox("I consent to the sharing of my personal data with HTHC.")
        if consent:
            submit_button = st.form_submit_button(label='Submit Entry')
        else:
            st.write("Please consent to the sharing of personal data to submit the form.")
        submit_button = st.form_submit_button(label='Submit Entry')

if submit_button:
    data_dict = {'Name': participant_name, 'Email': participant_email, 'Creative Text': participant_entry}

    # Add a new row to the Google Sheets document
    worksheet.append_row([data_dict['Name'], data_dict['Email'], data_dict['Creative Text']])

    st.success('Submitted in google, thank you!')

    clear_form()

    for i in range(5, 0, -1):
        st.write(f"New session in: {i}")
        time.sleep(1)

    st.experimental_rerun()