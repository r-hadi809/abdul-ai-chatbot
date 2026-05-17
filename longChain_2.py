from langchain_anthropic import ChatAnthropic
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv

load_dotenv()

model = ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

search = DuckDuckGoSearchRun()

query = "What is the latest news about AI today?"
search_results = search.run(query)

response = model.invoke([
    HumanMessage(f"Based on these search results, summarize the latest AI news:\n\n{search_results}")
])

print(response.content)