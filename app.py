import streamlit as st
import requests

st.title("Llama 3 Chatbot using Hugging Face Inference API")

HF_TOKEN = st.secrets["huggingface"]["api_key"]
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.3-70B-Instruct"

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query_llama3(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 256}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    return data[0]["generated_text"]

if "messages" not in st.session_state:
    st.session_state["messages"] = []

user_input = st.text_input("Ask your question here:")

if st.button("Send") and user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.spinner("Generating response..."):
        try:
            response = query_llama3(user_input)
        except Exception as e:
            response = f"Error: {e}"
    st.session_state["messages"].append({"role": "assistant", "content": response})

for msg in st.session_state["messages"]:
    icon = "🧑" if msg["role"] == "user" else "🤖"
    st.write(f"{icon} {msg['role'].capitalize()}: {msg['content']}")
