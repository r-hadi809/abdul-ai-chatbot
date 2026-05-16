import streamlit as st
import anthropic

import os
from dotenv import load_dotenv
load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

system_prompt = "You are abdul's first ever personal created assistant. You need to help him in everyway possible. You should always welcome him with his name : Sir Abdul Hadi ! and your tone has to be funny friendly and warm but still within limits as you are his assistant"

st.title("Abdul's AI Chatbox 🤖")
st.write("Welcome Sir Abdul Hadi! How may I help you today?")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=system_prompt,
        messages=st.session_state.messages
    )

    ai_reply = response.content[0].text
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
    with st.chat_message("assistant"):
        st.write(ai_reply)