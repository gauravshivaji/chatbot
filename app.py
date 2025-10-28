import streamlit as st
import google.generativeai as genai

st.title("💬 Gemini Chatbot")

# Configure the API key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Initialize the model
model = genai.GenerativeModel('gemini-pro


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
if prompt := st.chat_input("What would you like to ask?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Generate the response
        response = model.generate_content(prompt)
        st.markdown(response.text)

    st.session_state.messages.append({"role": "assistant", "content": response.text})
