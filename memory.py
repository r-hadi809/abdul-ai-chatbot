import chromadb
import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

# Setup ChromaDB
chroma_client = chromadb.PersistentClient(path="./memory_db")
collection = chroma_client.get_or_create_collection("chat_memory")

# Setup AI
model = ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

print("AI with permanent memory - type 'quit' to exit")
print("------------------------------------------------")

conversation_count = 0

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break

    # Save user message to ChromaDB
    collection.add(
        documents=[user_input],
        ids=[f"msg_{conversation_count}"]
    )

    # Get relevant past messages
    results = collection.query(
        query_texts=[user_input],
        n_results=min(3, conversation_count + 1)
    )
    past_messages = results["documents"][0] if results["documents"] else []

    # Send to AI with memory context
    response = model.invoke([
        SystemMessage(f"You are a helpful assistant. Here are relevant past messages for context: {past_messages}"),
        HumanMessage(user_input)
    ])

    ai_reply = response.content

    # Save AI reply to ChromaDB
    collection.add(
        documents=[ai_reply],
        ids=[f"reply_{conversation_count}"]
    )

    conversation_count += 1
    print(f"AI: {ai_reply}\n")