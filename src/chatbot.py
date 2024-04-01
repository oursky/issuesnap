import logging
import streamlit as st
from bug_report_generator import check_api_key, process_user_input

# Configure logging (optional, adjust log level and output as needed)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_user_steps():
    return st.text_area("**How do you reproduce the bug?**",
                        placeholder="e.g.\n1. Click Login button\n2. Fill in email and OTP\n3. Click Submit button\n4. See an error \"Failed to login\"",
                        value="",
                        height=150)


def get_expected_results():
    return st.text_area("**What do you expect to see?**",
                        placeholder="e.g. Should redirect to Home page.",
                        value="",
                        height=100)

# Process User Input Function
def generate_bug_report(user_steps, expected_results):
    """Processes the user's query, generates a response, and updates chat history."""

    # Display the Assistant's message
    with st.chat_message("assistant"):
        response = process_user_input(user_steps, expected_results)
        st.markdown(response)

try:
    # Streamlit App Interface
    st.set_page_config(
        page_title="AI Bug Report Generator",
        page_icon="🤖",
        initial_sidebar_state="collapsed",
        menu_items=None
    )
    st.title("AI Bug Report Generator")

    # Check if required API key exists
    check_api_key()

    with st.chat_message("assistant"):
        st.markdown("Good day buddy! Tell me something about your bug 🐞")

    # Get user input for steps
    user_steps = get_user_steps()

    # Call the function when user provides steps
    if user_steps:
        # Display the User's steps
        with st.chat_message("user"):
            display_user_steps = "Steps to reproduce:\n\n" + user_steps
            st.markdown(display_user_steps)

        # Get user input for steps
        expected_results = get_expected_results()
        if expected_results:
            # Display the User's steps
            with st.chat_message("user"):
                display_expected_results = "Expected results:\n\n" + expected_results
                st.markdown(display_expected_results)

            generate_bug_report(user_steps, expected_results)

    footer = """
                <style>
                    .footer {
                    position: relative;
                    width: 100%;
                    color: #888;
                    text-align: right;
                    font-size: 10px;
                    font-weight: 400;
                    }
                </style>
                <div class="footer">Made with Passion © Oursky Ltd.</div>
        """
    st.markdown(footer,unsafe_allow_html=True)
except KeyError as e:
    st.error(f"Missing environment variable: {e}")
    logging.error(f"chatbot.py: Missing environment variable: {e}")
except Exception as e:
    st.error(f"Uh oh! We seem to be having a hiccup. Give it another shot soon?")
    logging.error(f"chatbot.py: Exception: {e}")
