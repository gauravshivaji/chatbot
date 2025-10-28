import streamlit as st
from huggingface_hub import InferenceClient
from huggingface_hub.errors import BadRequestError

st.title("💬 Hugging Face Chatbot")

# Initialize the InferenceClient with your model and token
try:
    client = InferenceClient(
        model="meta-llama/Llama-3-8B-Instruct",
        token=st.secrets["HUGGINGFACE_API_KEY"]
    )
except Exception:
    st.error("Please provide a valid Hugging Face API key in your secrets.")
    st.stop()


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

        try:
            # Use the client to stream the response
            response_stream = client.chat_completion(
                messages=st.session_state.messages,
                max_tokens=500,
                stream=True
            )

            for chunk in response_stream:
                token = chunk.choices[0].delta.content
                if token:
                    full_response += token
                    message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

        except BadRequestError:
            st.error("A 'Bad Request' error occurred. This might be due to an issue with the chat history or the model's input limits. Please try clearing the chat and starting over.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")


    # Add the bot's response to history ONLY if it is not empty
    if full_response:
        st.session_state.messages.append({"role": "assistant", "content": full_response})
