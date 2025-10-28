import streamlit as st
from huggingface_hub import InferenceClient

# --- Page Configuration ---
st.set_page_config(
    page_title="Llama 3 70B Chatbot",
    page_icon="🤖",
    layout="centered"
)

# --- App Title and Description ---
st.title("🤖gurubhai ka jwab ")
st.caption("charges extra 20rs")

# --- Hugging Face API Configuration ---
try:
    HF_TOKEN = st.secrets["huggingface"]["api_key"]
except (FileNotFoundError, KeyError):
    st.error("Hugging Face API key not found. Please add it to your Streamlit secrets.", icon="🚨")
    st.stop()
    
# Initialize the Inference Client with the 70B model
MODEL_ID = "meta-llama/Meta-Llama-3-70B-Instruct"
try:
    client = InferenceClient(model=MODEL_ID, token=HF_TOKEN)
except Exception as e:
    st.error(f"Failed to initialize the Inference Client: {e}", icon="🚨")
    st.stop()


# --- Function to Query Llama 3 (Corrected for Chat Completion) ---
def query_llama3_chat(messages: list) -> str:
    """
    Sends the entire conversation history to Llama 3 using the chat completion endpoint.
    """
    try:
        # <-- KEY CHANGE 1: Use the .chat_completion() method
        response = client.chat_completion(
            messages=messages,      # Pass the list of message dictionaries
            max_tokens=1024,        # Note: parameter is max_tokens, not max_new_tokens
            stream=False,           # We will handle the full response at once
        )
        # <-- KEY CHANGE 2: Extract the content from the response object
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"An error occurred while generating the response: {e}", icon="🔥")
        return "Sorry, I couldn't process your request. The model might be busy or still loading."

# --- Chat History Management ---
if "messages" not in st.session_state:
    # Llama 3 requires a system prompt for best performance, but for simplicity, we start with the assistant.
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am the Llama 3 70B model. How can I help you today?"}]

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- User Input and Chat Logic ---
if user_prompt := st.chat_input("Ask your question here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    
    with st.chat_message("user"):
        st.markdown(user_prompt)
        
    with st.chat_message("assistant"):
        with st.spinner("Thinking... gurubhai soch rha he"):
            # <-- KEY CHANGE 3: Call the new function
            response_content = query_llama3_chat(st.session_state.messages)
            st.markdown(response_content)
            
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_content})
