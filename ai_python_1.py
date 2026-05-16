import anthropic

import os
from dotenv import load_dotenv
load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

system_prompt = "You are abdul's first ever personal created assistant. You need to help him in everyway possible. You should always welcome him eich his name : Sir Abdul Hadi ! and your tone has to be funny friendly and warm but still within limits as u are his assistants "
print("Abdul's Chatbox is here ! How may I help you? To End the conversation Type : quit . ThankYou :)")
print("----------------------------------------------")

conversation_history = []

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break
    
    conversation_history.append({
        "role": "user",
        "content": user_input
    })
    
    message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    system=system_prompt,
    messages=conversation_history
    )
    
    ai_reply = message.content[0].text
    
    conversation_history.append({
        "role": "assistant",
        "content": ai_reply
    })
    
    print("AI:", ai_reply)
    print()