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


# --- Function to Query Llama 3 (Corrected for Conversational Task) ---
def query_llama3_conversational(messages: list) -> str:
    """
    Sends the entire conversation history to the Llama 3 model and returns the assistant's reply.
    """
    try:
        # <-- KEY CHANGE 1: Use the .conversational() method
        response_data = client.conversational(
            messages=messages, # Pass the list of message dictionaries
            max_new_tokens=1024,
            do_sample=True,
            temperature=0.7,
            top_p=0.95,
        )
        # <-- KEY CHANGE 2: Extract the generated text from the response dictionary
        # The assistant's reply is in the 'generated_text' key
        return response_data.get('generated_text', '')
    except Exception as e:
        st.error(f"An error occurred while generating the response: {e}", icon="🔥")
        return "Sorry, I couldn't process your request. The model might be loading or experiencing high traffic."

# --- Chat History Management ---
if "messages" not in st.session_state:
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
        with st.spinner("Thinking... (this may take a moment for the 70B model)"):
            # <-- KEY CHANGE 3: Pass the entire session state messages list
            response = query_llama3_conversational(st.session_state.messages)
            st.markdown(response)
            
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
