# agent.py
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
import os

class Agent:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model_name="llama3-8b-8192")
        self.vectorstore = None

    def load_pdf(self, pdf_path):
        loader = PyPDFLoader(pdf_path)
        docs = loader.load_and_split()
        self.vectorstore = FAISS.from_documents(docs, self.embeddings)

    def ask(self, query):
        if not self.vectorstore:
            return "Please upload a PDF first."

        relevant_docs = self.vectorstore.similarity_search(query, k=3)
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        prompt = f"""Answer the question based on the context below:
        
        Context: {context}
        Question: {query}
        Answer:"""
        response = self.llm.invoke(prompt)
        
        return response.content
    