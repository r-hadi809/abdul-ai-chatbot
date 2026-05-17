import streamlit as st
import chromadb
import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

model = ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

chroma_client = chromadb.PersistentClient(path="./memory_db")
collection = chroma_client.get_or_create_collection("chat_memory")
search = DuckDuckGoSearchRun()

st.title("Abdul's Super AI 🚀")
st.write("I can search the web AND remember our conversations!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Search web if needed
    search_results = search.run(prompt)

    # Get past memories
    count = collection.count()
    results = collection.query(
        query_texts=[prompt],
        n_results=min(3, max(1, count))
    ) if count > 0 else {"documents": [[]]}
    past = results["documents"][0]

    # Get AI response
    response = model.invoke([
        SystemMessage(f"You are Abdul's personal AI. Past context: {past}. Web results: {search_results}"),
        HumanMessage(prompt)
    ])

    ai_reply = response.content

    # Save to memory
    collection.add(
        documents=[f"User: {prompt} | AI: {ai_reply}"],
        ids=[f"conv_{count}"]
    )

    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
    with st.chat_message("assistant"):
        st.write(ai_reply)