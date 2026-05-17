import streamlit as st
import anthropic
import os
from dotenv import load_dotenv
from duckduckgo_search import DDGS

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

st.title("Abdul's Super AI 🚀")
st.write("I can search the web for you!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Search web
    with DDGS() as ddgs:
        results = list(ddgs.text(prompt, max_results=3))
    search_text = " ".join([r["body"] for r in results])

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=f"You are Abdul's personal AI assistant. Use these web results to help answer: {search_text}",
        messages=st.session_state.messages
    )

    ai_reply = response.content[0].text
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
    with st.chat_message("assistant"):
        st.write(ai_reply)