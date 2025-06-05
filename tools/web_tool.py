# web_tool.py
from dotenv import load_dotenv
load_dotenv()
import os
from tavily import TavilyClient # New import
from typing import Optional, List

def search_web(query: str, max_results: int = 3) -> str:
    """
    Performs a web search using the Tavily Search API and returns a formatted string
    of the search results.

    Args:
        query (str): The search query.
        max_results (int): The maximum number of search results to return.

    Returns:
        str: A formatted string containing the search results, including title, URL,
             and a snippet for each result. Returns an error message if the API key
             is missing or if the search fails.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "Error: TAVILY_API_KEY environment variable not set. Cannot perform real web search."

    try:
        tavily = TavilyClient(api_key=api_key)
        # Perform the search
        results = tavily.search(query=query, search_depth="basic", max_results=max_results)

        formatted_results = []
        if results and results.get('results'):
            for i, result in enumerate(results['results']):
                title = result.get('title', 'No Title')
                url = result.get('url', 'No URL')
                content = result.get('content', 'No Content') # Tavily often gives 'content' (snippet)
                
                formatted_results.append(
                    f"Result {i+1}:\n"
                    f"  Title: {title}\n"
                    f"  URL: {url}\n"
                    f"  Snippet: {content}\n"
                )
            return "\n\n".join(formatted_results)
        else:
            return f"No relevant web search results found for '{query}'."

    except Exception as e:
        return f"An error occurred during web search: {e}"