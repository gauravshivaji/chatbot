import os
import streamlit as st
from transformers import pipeline

# Option A: Use environment variable for API Key
HF_TOKEN = os.getenv("HF_API_KEY")

# Option B: Accept API Key from sidebar for development
with st.sidebar:
    st.title("🤗 Hugging Face Chatbot")
    api_key_input = st.text_input("Enter Hugging Face API Key", type="password")
if api_key_input:
    HF_TOKEN = api_key_input

st.title("Llama 3 Chatbot (Hugging Face & Streamlit)")
st.markdown("Talk to Meta-Llama-3-70B-Instruct model via Hugging Face Inference API.")

if not HF_TOKEN:
    st.warning("Please enter your Hugging Face API key in the sidebar.")
    st.stop()

@st.cache_resource
def get_pipeline(token):
    # For hosted inference API, set use_auth_token argument.
    return pipeline(
        "text-generation",
        model="meta-llama/Meta-Llama-3-70B-Instruct",
        use_auth_token=token
    )

chatbot = get_pipeline(HF_TOKEN)

if "messages" not in st.session_state:
    st.session_state["messages"] = []

prompt = st.text_input("Ask a question:", "")

if st.button("Send") and prompt:
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.spinner("Thinking..."):
        response = chatbot(prompt, max_new_tokens=256)[0]['generated_text']
    st.session_state["messages"].append({"role": "assistant", "content": response})

for msg in st.session_state["messages"]:
    st.write(f"{msg['role'].capitalize()}: {msg['content']}")
