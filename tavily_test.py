# test_tavily.py
from tavily import TavilyClient
import os
from dotenv import load_dotenv
load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
results = client.search(query="latest on llama3", search_depth="basic", max_results=2)
print(results)
