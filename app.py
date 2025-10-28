import streamlit as st
from openai import OpenAI

# Initialize client
client = OpenAI(api_key=st.secrets["api_keys"]["openai"])

st.title("💬 Chatbot App")
st.write("Talk to your assistant!")

# Input box
user_input = st.text_input("You:", "")

if user_input:
    # Stream response
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}],
            stream=True,
        )

        for chunk in stream:
            if chunk.choices[0].delta.get("content"):
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
