import os
from dotenv import load_dotenv
import streamlit as st
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)

# Configuration (Load environment variables)
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

# Initialize LLM model
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    },
)


def get_user_steps():
    return st.text_area("What are your steps to reproduce the issue?",
                        placeholder="Example:\n1. Click Login button\n2. Fill in email\n3. Click Submit button\n4. See an error \"Failed to login\"",
                        value="",
                        height=200)


def get_expected_results():
    return st.text_area("What are your expected results?",
                        placeholder="Example: Should be able to login and redirect to Home page successfully.",
                        value="",
                        height=100)

# Process User Input Function
def generate_bug_report(query):
    """Processes the user's query, generates a response, and updates chat history."""

    # Display the Assistant's message
    with st.chat_message("assistant"):
        response = llm.invoke(query)
        st.markdown(response.content)

    # Store the User's message and Assistant's response
    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.messages.append(
        {"role": "assistant", "content": response.content})

# Display Chat History Function
def display_chat_history():
    """Displays the chat history in a conversational format."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# Streamlit App Interface
st.title("AI Bug Report Generator")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Good day buddy, I am your bug reporting assistant. Tell me something about your bug."
        }
    ]

display_chat_history()  # Show existing messages on app launch

# Get user input for steps
user_steps = get_user_steps()

# Call the function when user provides steps
if user_steps:
    # Display the User's steps
    with st.chat_message("user"):
        display_user_steps = "Steps to reproduce:\n" + user_steps
        st.markdown(display_user_steps)

    # Get user input for steps
    expected_results = get_expected_results()
    if expected_results:
        # Display the User's steps
        with st.chat_message("user"):
            display_expected_results = "Expected results:\n" + expected_results
            st.markdown(display_expected_results)

        input_prompt = user_steps + expected_results

        generate_bug_report(input_prompt)
