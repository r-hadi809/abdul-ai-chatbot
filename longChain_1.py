from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

load_dotenv()

model = ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

messages = [
    SystemMessage("You are a helpful assistant called LangBot!"),
    HumanMessage("Hello! Who are you?")
]

response = model.invoke(messages)
print(response.content)