import streamlit as st
from transformers import pipeline

st.title("Llama 3 Chatbot (Hugging Face & Streamlit)")
st.markdown("Chat with Meta-Llama-3-70B-Instruct! (API key stored securely with Streamlit secrets)")

# Access HF API key from Streamlit secrets
HF_TOKEN = st.secrets["huggingface"]["api_key"]

@st.cache_resource
def get_chatbot(token):
    return pipeline(
        "text-generation",
        model="meta-llama/Meta-Llama-3-70B-Instruct",
        
        use_auth_token=token
    )

chatbot = get_chatbot(HF_TOKEN)

if "messages" not in st.session_state:
    st.session_state["messages"] = []

user_input = st.text_input("Ask your question:")

if st.button("Send") and user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.spinner("Thinking..."):
        response = chatbot(user_input, max_new_tokens=256)[0]['generated_text']
    st.session_state["messages"].append({"role": "assistant", "content": response})

for msg in st.session_state["messages"]:
    role = "🧑" if msg["role"] == "user" else "🤖"
    st.write(f"{role} {msg['role'].capitalize()}: {msg['content']}")
