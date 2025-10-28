import streamlit as st
from huggingface_hub import InferenceClient

# --- Page Configuration ---
st.set_page_config(
    page_title="Llama 3 70B Chatbot",
    page_icon="🤖",
    layout="centered"
)

# --- App Title and Description ---
st.title("🤖 Llama 3 (70B) Chatbot")
st.caption("Powered by Hugging Face Inference API")

# --- Hugging Face API Configuration ---
# Make sure to set your HF_TOKEN in Streamlit secrets
try:
    HF_TOKEN = st.secrets["huggingface"]["api_key"]
except (FileNotFoundError, KeyError):
    st.error("Hugging Face API key not found. Please add it to your Streamlit secrets.", icon="🚨")
    st.stop()
    
# Initialize the Inference Client with the 70B model
MODEL_ID = "meta-llama/Meta-Llama-3-70B-Instruct" # <-- This is the only line changed
try:
    client = InferenceClient(model=MODEL_ID, token=HF_TOKEN)
except Exception as e:
    st.error(f"Failed to initialize the Inference Client: {e}", icon="🚨")
    st.stop()


# --- Function to Query Llama 3 ---
def query_llama3(prompt: str) -> str:
    """
    Sends a prompt to the Llama 3 model and returns the generated text.
    """
    try:
        # The correct method is .text_generation()
        response = client.text_generation(
            prompt=prompt,
            max_new_tokens=1024,  # Increased token limit for the larger model
            do_sample=True,
            temperature=0.7,
            top_p=0.95,
        )
        # The method directly returns the generated string
        return response
    except Exception as e:
        # Provide a more user-friendly error message
        st.error(f"An error occurred while generating the response: {e}", icon="🔥")
        return "Sorry, I couldn't process your request. The model might be loading or experiencing high traffic."

# --- Chat History Management ---
# Initialize session state for messages if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am the Llama 3 70B model. How can I help you today?"}]

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- User Input and Chat Logic ---
# Accept user input via a chat input box at the bottom
if user_prompt := st.chat_input("Ask your question here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    
    # Display user message in the chat message container
    with st.chat_message("user"):
        st.markdown(user_prompt)
        
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Thinking... (this may take a moment for the 70B model)"):
            response = query_llama3(user_prompt)
            st.markdown(response)
            
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
