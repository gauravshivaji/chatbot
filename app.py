import streamlit as st
from huggingface_hub import InferenceClient

st.title("💬 Hugging Face Chatbot")

# Initialize the InferenceClient with your model and token
# The token is read from Streamlit's secrets
client = InferenceClient(
    model="meta-llama/Llama-3-8B-Instruct",
    token=st.secrets["HUGGINGFACE_API_KEY"]
)

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
if prompt := st.chat_input("What would you like to ask?"):
    # Add user's message to history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display the bot's response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Use the client to stream the response
        # The 'messages' argument should be the chat history
        response_stream = client.chat_completion(
            messages=st.session_state.messages,
            max_tokens=500, # Adjust as needed
            stream=True
        )

        for chunk in response_stream:
            # The actual text is in chunk.choices[0].delta.content
            token = chunk.choices[0].delta.content
            if token:
                full_response += token
                message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    
    # Add the bot's response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
