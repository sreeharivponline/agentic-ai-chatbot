# tools/web_tool.py

from dotenv import load_dotenv
load_dotenv()

import os
from tavily import TavilyClient  # type: ignore
from typing import Optional

def search_web(query: str, max_results: int = 3) -> str:
    """
    Performs a web search using the Tavily Search API and returns formatted results.

    Args:
        query (str): The search query.
        max_results (int): Max number of search results to return.

    Returns:
        str: A formatted string of search results, or error message.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "❌ Error: TAVILY_API_KEY environment variable not set. Cannot perform web search."

    try:
        tavily = TavilyClient(api_key=api_key)
        results = tavily.search(query=query, search_depth="basic", max_results=max_results)

        if not results or not results.get('results'):
            return f"❕ No relevant web results found for '{query}'."

        formatted_results = []
        for i, result in enumerate(results['results'], start=1):
            title = result.get('title', 'No Title')
            url = result.get('url', 'No URL')
            snippet = result.get('content', 'No Snippet')

            formatted_results.append(
                f"🔎 Result {i}:\n"
                f"📝 Title: {title}\n"
                f"🔗 URL: {url}\n"
                f"📄 Snippet: {snippet}"
            )

        return "\n\n".join(formatted_results)

    except Exception as e:
        return f"⚠️ An error occurred during Tavily web search:\n{str(e)}"
