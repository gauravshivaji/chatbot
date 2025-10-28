import streamlit as st
from huggingface_hub import InferenceClient

st.title("Llama 3 Chatbot using Hugging Face Inference API")

HF_TOKEN = st.secrets["huggingface"]["api_key"]
client = InferenceClient(token=HF_TOKEN)

def query_llama3(prompt):
    response = client.inference(
        model="meta-llama/Llama-3.3-70B-Instruct",
        task="text-generation",
        inputs=prompt,
        parameters={"max_new_tokens": 256}
    )
    return response[0]["generated_text"]

if "messages" not in st.session_state:
    st.session_state["messages"] = []

user_input = st.text_input("Ask your question here:")

if st.button("Send") and user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.spinner("Generating response..."):
        response = query_llama3(user_input)
    st.session_state["messages"].append({"role": "assistant", "content": response})

for msg in st.session_state["messages"]:
    icon = "🧑" if msg["role"] == "user" else "🤖"
    st.write(f"{icon} {msg['role'].capitalize()}: {msg['content']}")
