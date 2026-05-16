import streamlit as st
import anthropic
import PyPDF2

import os
from dotenv import load_dotenv
import streamlit as st
import anthropic
import PyPDF2

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

st.title("Abdul's PDF AI 📄🤖")
st.write("Upload a PDF and ask me anything about it!")

uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

if uploaded_file is not None:
    pdf_text = read_pdf(uploaded_file)
    st.success("PDF loaded successfully!")
    
    if "pdf_messages" not in st.session_state:
        st.session_state.pdf_messages = []
    
    for message in st.session_state.pdf_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    if prompt := st.chat_input("Ask anything about your PDF..."):
        st.session_state.pdf_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=f"You are a helpful assistant. Answer questions based on this document:\n\n{pdf_text}",
            messages=st.session_state.pdf_messages
        )
        
        ai_reply = response.content[0].text
        st.session_state.pdf_messages.append({"role": "assistant", "content": ai_reply})
        with st.chat_message("assistant"):
            st.write(ai_reply)