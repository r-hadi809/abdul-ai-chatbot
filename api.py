from fastapi import FastAPI
from pydantic import BaseModel
import anthropic

app = FastAPI()

import os
from dotenv import load_dotenv
load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
system_prompt = "You are abdul's first ever personal created assistant. You need to help him in everyway possible. You should always welcome him with his name : Sir Abdul Hadi ! and your tone has to be funny friendly and warm but still within limits as you are his assistant"

class Message(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "Abdul's AI API is running! 🚀"}

@app.post("/chat")
def chat(message: Message):
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=system_prompt,
        messages=[{"role": "user", "content": message.text}]
    )
    return {"reply": response.content[0].text}