import openai
import streamlit as st

# Set the title for the Streamlit app
st.title("OpenAI Chatbot 🤖")

# Set the OpenAI API key from Streamlit's secrets
# This is the recommended way to handle API keys and other secrets.
openai.api_key = st.secrets["openai_api_key"]

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages from the chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input from the chat input box
if prompt := st.chat_input("What is up?"):
    # Add user's message to the chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user's message in the chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display bot's response in the chat
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Call the OpenAI API with the entire chat history
        # We use a stream to get the response word by word
        for response in openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": m["role"], "content": m["content"]}
                      for m in st.session_state.messages],
            stream=True,
        ):
            # Append the new chunk to the full response
            full_response += response.choices[0].delta.get("content", "")
            # Display the response as it comes in
            message_placeholder.markdown(full_response + "▌")

        # Update the final message in the placeholder
        message_placeholder.markdown(full_response)

    # Add the bot's complete response to the chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
