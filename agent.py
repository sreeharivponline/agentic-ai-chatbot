# agent.py

from langchain_groq import ChatGroq # type: ignore
import os
from typing import Tuple, List, Optional

from memory import Memory
from tools.pdf_tools import load_and_embed_pdf
from tools.web_tool import search_web
from dotenv import load_dotenv
load_dotenv()
class Agent:
    def __init__(self):
        """Initializes the Agent with an LLM, vector store, and memory."""
        # Initialize Groq LLM; ensure GROQ_API_KEY environment variable is set
        self.llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model_name="llama3-8b-8192")
        self.vectorstore = None  # To hold the FAISS vector store for PDF content
        self.memory = Memory()   # To track the agent's internal reasoning process

    def load_pdf(self, pdf_path: str):
        """
        Loads and embeds a PDF document into the agent's vector store.
        Records the process in memory.
        """
        self.memory.add(
            thought=f"User uploaded a PDF: '{pdf_path}'. Initiating PDF loading and embedding.",
            action=f"Calling pdf_tools.load_and_embed_pdf('{pdf_path}')",
            observation="PDF loading and embedding process started."
        )
        try:
            self.vectorstore = load_and_embed_pdf(pdf_path)
            self.memory.add(
                thought=f"PDF '{pdf_path}' successfully processed.",
                action="Updated agent's internal vector store.",
                observation=f"FAISS vector store created from '{pdf_path}'."
            )
        except Exception as e:
            self.memory.add(
                thought=f"Failed to load PDF '{pdf_path}'.",
                action="Attempted PDF loading.",
                observation=f"Error: {e}"
            )
            raise # Re-raise the exception to inform the Streamlit app

    def _determine_tool_and_query(self, user_query: str) -> Tuple[str, str]:
        """
        Internal method to determine which tool (if any) is most relevant to the query
        and extract the specific query for that tool.
        This is a simple keyword-based approach for demonstration.
        """
        query_lower = user_query.lower()

        # Prioritize explicit tool calls or specific contexts
        if "web search for:" in query_lower:
            return "web", user_query.split("web search for:", 1)[1].strip()
        elif "search online for:" in query_lower:
            return "web", user_query.split("search online for:", 1)[1].strip()
        elif "latest news on" in query_lower or "what is the latest" in query_lower:
            return "web", user_query # Use full query as web search query

        # If a PDF is loaded, prioritize PDF questions unless explicitly web
        if self.vectorstore:
            if "according to the document" in query_lower or "in the pdf" in query_lower or "from the file" in query_lower:
                return "pdf", user_query
            # If no explicit tool, and PDF is present, assume PDF is primary source
            return "pdf", user_query
        
        # Fallback if no PDF is loaded and no web trigger
        return "general_llm", user_query


    def ask(self, query: str) -> Tuple[str, Optional[List[str]]]:
        """
        Processes a user query by planning tool use, executing tools,
        and synthesizing a response. Records steps in memory.

        Args:
            query (str): The user's question.

        Returns:
            Tuple[str, Optional[List[str]]]: The answer string and a list of sources,
                                             or None if no sources.
        """
        answer: str = ""
        sources: Optional[List[str]] = None
        context_for_llm: str = ""

        # Step 1: Plan and decompose the goal
        tool_type, tool_query = self._determine_tool_and_query(query)
        self.memory.add(
            thought=f"Analyzing user query: '{query}'. Identified '{tool_type}' as the primary tool to use.",
            action=f"Selected tool: {tool_type} with specific query: '{tool_query}'",
            observation="Ready to execute selected tool."
        )

        # Step 2: Use tools based on the plan
        if tool_type == "web":
            self.memory.add(
                thought=f"Executing web search for: '{tool_query}'.",
                action=f"Calling web_tool.search_web_stub('{tool_query}')",
                observation="Web search initiated (using stub)."
            )
            web_results = search_web(tool_query)
            context_for_llm = f"Web Search Results:\n{web_results}"
            sources = ["Web Search (Simulated)"] # Indicate source is from web search

            self.memory.add(
                thought="Web search stub returned results.",
                action="Prepared context from web results for LLM.",
                observation=f"Context snippet: {context_for_llm[:100]}..."
            )
            # For stub, we directly return the result. For real web, you'd feed to LLM.
            # Let's send it to LLM for consistency, so LLM can "summarize" the stub.
            
        elif tool_type == "pdf":
            if not self.vectorstore:
                self.memory.add(
                    thought="PDF tool selected but no PDF loaded.",
                    action="Returning error message to user.",
                    observation="Cannot answer PDF-related question without a loaded PDF."
                )
                return "Please upload a PDF first to answer questions from documents.", None

            self.memory.add(
                thought=f"Query is PDF-related. Performing similarity search in loaded PDF for: '{tool_query}'.",
                action="Performing vector store similarity search.",
                observation="Searching for top 3 relevant document chunks from PDF."
            )
            relevant_docs = self.vectorstore.similarity_search(tool_query, k=3)
            context_for_llm = "\n\n".join([doc.page_content for doc in relevant_docs])
            
            sources = []
            for doc in relevant_docs:
                if 'source' in doc.metadata:
                    source_str = os.path.basename(doc.metadata['source']) # Get just filename
                    if 'page' in doc.metadata:
                        source_str += f" (Page: {doc.metadata['page'] + 1})" # Pages are 0-indexed
                    sources.append(source_str)
            
            self.memory.add(
                thought=f"Retrieved {len(relevant_docs)} relevant PDF documents.",
                action="Prepared context from PDF for LLM.",
                observation=f"Context snippet: {context_for_llm[:100]}..."
            )

        elif tool_type == "general_llm":
            self.memory.add(
                thought="No specific tool indicated or PDF loaded. Using LLM for general knowledge.",
                action="Invoking LLM directly with the query.",
                observation="Awaiting LLM response for general query."
            )
            prompt = f"Answer the following question concisely:\nQuestion: {query}\nAnswer:"
            response = self.llm.invoke(prompt)
            return response.content, None # No specific sources for general knowledge

        # Step 3: Information Synthesis & LLM Interaction (for web and pdf contexts)
        # Only proceed to LLM if context was generated from a tool
        if context_for_llm:
            self.memory.add(
                thought="Context assembled from tool output. Sending to LLM to generate final answer.",
                action="Constructing prompt for LLM with context and query.",
                observation="Invoking LLM to synthesize response."
            )
            prompt_template = f"""Answer the question concisely based on the context below. If the answer is not in the context, state that you cannot answer from the provided information.

Context: {context_for_llm}
Question: {query}
Answer:"""
            
            response = self.llm.invoke(prompt_template)
            answer = response.content
            
            self.memory.add(
                thought="LLM generated an answer based on the provided context.",
                action="Returning final answer and sources to user.",
                observation=f"Generated Answer: {answer[:100]}..."
            )
            return answer, sources
        else:
            # Fallback for cases where a tool was selected but didn't yield context (e.g., future tool errors)
            self.memory.add(
                thought="Selected tool did not provide context. Cannot generate answer.",
                action="Returning an error or general response.",
                observation="Failed to generate specific answer due to missing context."
            )
            return "I couldn't find relevant information using the available tools.", None