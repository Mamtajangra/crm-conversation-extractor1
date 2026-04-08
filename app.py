import streamlit as st

# Import the main function used for extracting user information
from source.extractor import extract_info
# Set title of the web app
st.title("AI CRM Conversation Extractor")

# Create a text input area for user to paste chat conversation
user_input = st.text_area("Enter chat")
# Button to trigger extraction process
if st.button("Extract"):
    # Check if user has entered any input
    if user_input:
        # Call extraction function (LLM processing happens here)
        result = extract_info(user_input) # Ab direct call karein
    #    Display result in JSON format on UI
        st.json(result)
    else:
        # Show warning if input is empty
        st.warning("Please enter some text first.")