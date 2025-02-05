import groq
import streamlit as st

def initialize_groq_client(api_key):
    """Initialize the Groq API client"""
    client = groq.Client(api_key=api_key)
    return client

def chat_with_groq(client, conversation_history):
    """Send the conversation history to the Groq model and return a response"""
    response = client.chat.completions.create(
        model="llama3-8b-8192",  # Replace with a locally hosted model if available
        messages=conversation_history,
        max_tokens=200
    )
    return response.choices[0].message.content

st.title("Groq Chatbot")
api_key = st.text_input("Enter Groq API Key", type="password")

if "conversation" not in st.session_state:
    st.session_state.conversation = []

if api_key:
    client = initialize_groq_client(api_key)
    user_input = st.text_input("You:")
    if st.button("Send") and user_input:
        st.session_state.conversation.append({"role": "user", "content": user_input})
        response = chat_with_groq(client, st.session_state.conversation)
        st.session_state.conversation.append({"role": "assistant", "content": response})
        st.text_area("Chatbot:", response, height=200)

