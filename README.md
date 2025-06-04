# Agentic Chatbot with PDF + Web Search + Memory

This is a lightweight, agent-based chatbot application that can:

- 🗂 Answer questions based on the content of a PDF document.
- 🌐 Perform fallback web search if the answer is not found in the PDF.
- 🧠 Maintain short-term memory
- 📄 Compile a structured report based on your interactions.
- 🤖 Powered by [Groq API](https://groq.com/) with the free **LLaMA 3 8B model** via `ChatGroq`.

## 📺 Inspired by these YouTube tutorial

> [Build a RAG Chatbot with LangChain and Groq (LLaMA3)](https://www.youtube.com/watch?v=B5XD-qpL0FU)  
> by @codewithvikas  
> [Build a PDF AI Chatbot with Llama 3.3 + ChromaDB + Gradio +Groq Full Tutorial](https://www.youtube.com/watch?v=Qq-YDcKtzcs)  
> by @codewithvikas  

---

## ✨ Features

- ✅ **PDF Retrieval:** Load any PDF and perform semantic search using FAISS + HuggingFace MiniLM.
- ✅ **Chat UI:** Simple chat interface using Streamlit with dropdown history.
- ✅ **Final Report:** Generates a summary from your queries and answers.

---
